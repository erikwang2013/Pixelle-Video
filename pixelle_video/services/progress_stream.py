# Copyright (c) 2026 erik <erik@erik.xyz> — https://erik.xyz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""WebSocket-based real-time progress streaming for video generation"""
import asyncio
import json
import time
from typing import Dict, Set, Optional
from dataclasses import dataclass, field
from loguru import logger


@dataclass
class ProgressEvent:
    task_id: str
    event_type: str  # "frame", "step", "status", "error"
    progress: float  # 0.0 - 1.0
    message: str = ""
    data: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "event_type": self.event_type,
            "progress": self.progress,
            "message": self.message,
            "data": self.data,
            "timestamp": self.timestamp,
        }


class ProgressStreamManager:
    """Manages WebSocket connections and broadcasts progress events."""

    def __init__(self):
        self._connections: Dict[str, Set] = {}  # task_id -> set of websockets
        self._lock = asyncio.Lock()

    async def subscribe(self, task_id: str, websocket) -> None:
        """Subscribe a websocket to task progress updates."""
        async with self._lock:
            if task_id not in self._connections:
                self._connections[task_id] = set()
            self._connections[task_id].add(websocket)
            logger.debug(f"WebSocket subscribed to {task_id} (total: {len(self._connections[task_id])})")

    async def unsubscribe(self, task_id: str, websocket) -> None:
        """Unsubscribe a websocket from task progress."""
        async with self._lock:
            if task_id in self._connections:
                self._connections[task_id].discard(websocket)
                if not self._connections[task_id]:
                    del self._connections[task_id]

    async def broadcast(self, task_id: str, event: ProgressEvent) -> int:
        """Broadcast a progress event to all subscribers. Returns count of recipients."""
        async with self._lock:
            sockets = self._connections.get(task_id, set()).copy()

        payload = json.dumps(event.to_dict(), ensure_ascii=False)
        sent = 0

        for ws in sockets:
            try:
                await ws.send_text(payload)
                sent += 1
            except Exception as e:
                logger.warning(f"Failed to send to WebSocket: {e}")
                await self.unsubscribe(task_id, ws)

        return sent

    def create_progress_callback(self, task_id: str):
        """Create a callback function that broadcasts progress.

        Returns an async callable suitable for passing to pipeline.progress_callback.
        """
        async def callback(event_type: str, progress: float, **kwargs):
            event = ProgressEvent(
                task_id=task_id,
                event_type=event_type,
                progress=progress,
                message=kwargs.pop("message", ""),
                data=kwargs,
            )
            await self.broadcast(task_id, event)

        return callback

    @property
    def active_connections(self) -> int:
        return sum(len(sockets) for sockets in self._connections.values())

    def get_subscriber_count(self, task_id: str) -> int:
        sockets = self._connections.get(task_id, set())
        return len(sockets)


# Global singleton
progress_manager = ProgressStreamManager()
