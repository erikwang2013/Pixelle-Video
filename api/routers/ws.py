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

"""WebSocket endpoint for real-time progress streaming"""
import json
import time
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger
from pixelle_video.services.progress_stream import progress_manager

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/progress/{task_id}")
async def progress_websocket(websocket: WebSocket, task_id: str):
    """WebSocket endpoint for real-time task progress updates.

    Connect to: ws://localhost:8000/api/ws/progress/{task_id}

    Receives JSON messages:
    {"task_id": "...", "event_type": "frame|step|status|error", "progress": 0.5, "message": "...", "data": {...}, "timestamp": 1234567890.123}
    """
    await websocket.accept()
    await progress_manager.subscribe(task_id, websocket)

    # Send initial connection confirmation
    await websocket.send_text(json.dumps({
        "task_id": task_id,
        "event_type": "connected",
        "progress": 0.0,
        "message": f"Subscribed to progress for task {task_id}",
        "data": {"subscribers": progress_manager.get_subscriber_count(task_id)},
        "timestamp": time.time(),
    }))

    try:
        # Keep connection alive, handle client messages
        while True:
            data = await websocket.receive_text()
            # Client can send {"action": "ping"} — we respond with pong
            msg = json.loads(data)
            if msg.get("action") == "ping":
                await websocket.send_text(json.dumps({"action": "pong"}))
    except WebSocketDisconnect:
        logger.debug(f"WebSocket disconnected from task {task_id}")
    except Exception as e:
        logger.warning(f"WebSocket error for task {task_id}: {e}")
    finally:
        await progress_manager.unsubscribe(task_id, websocket)


@router.get("/ws/stats")
async def websocket_stats():
    """Get WebSocket connection statistics."""
    return {
        "active_connections": progress_manager.active_connections,
        "tracked_tasks": len(progress_manager._connections),
    }
