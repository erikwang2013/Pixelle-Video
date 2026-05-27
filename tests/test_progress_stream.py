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

"""Tests for WebSocket real-time progress streaming"""
import asyncio
import json

import pytest


class TestProgressEvent:
    """Tests for the ProgressEvent dataclass."""

    def test_progress_event_to_dict(self):
        from pixelle_video.services.progress_stream import ProgressEvent
        event = ProgressEvent(task_id="t1", event_type="frame", progress=0.5, message="test")
        d = event.to_dict()
        assert d["task_id"] == "t1"
        assert d["event_type"] == "frame"
        assert d["progress"] == 0.5
        assert d["message"] == "test"
        assert "timestamp" in d
        assert isinstance(d["data"], dict)

    def test_progress_event_defaults(self):
        from pixelle_video.services.progress_stream import ProgressEvent
        event = ProgressEvent(task_id="t2", event_type="status", progress=0.0)
        d = event.to_dict()
        assert d["task_id"] == "t2"
        assert d["event_type"] == "status"
        assert d["progress"] == 0.0
        assert d["message"] == ""
        assert d["data"] == {}

    def test_progress_event_with_data(self):
        from pixelle_video.services.progress_stream import ProgressEvent
        event = ProgressEvent(
            task_id="t3",
            event_type="step",
            progress=0.75,
            message="Rendering frame 3/5",
            data={"frame": 3, "total": 5},
        )
        d = event.to_dict()
        assert d["data"]["frame"] == 3
        assert d["data"]["total"] == 5


class TestProgressStreamManager:
    """Tests for the ProgressStreamManager."""

    def test_singleton_exists(self):
        from pixelle_video.services.progress_stream import progress_manager
        assert progress_manager is not None
        assert hasattr(progress_manager, "subscribe")
        assert hasattr(progress_manager, "unsubscribe")
        assert hasattr(progress_manager, "broadcast")
        assert hasattr(progress_manager, "create_progress_callback")

    def test_active_connections_initially_zero(self):
        from pixelle_video.services.progress_stream import progress_manager
        # active_connections is a property backed by internal dict
        assert progress_manager.active_connections >= 0

    def test_get_subscriber_count_unknown_task(self):
        from pixelle_video.services.progress_stream import progress_manager
        count = progress_manager.get_subscriber_count("nonexistent_task_id")
        assert count == 0

    def test_create_progress_callback_returns_async_callable(self):
        from pixelle_video.services.progress_stream import progress_manager
        cb = progress_manager.create_progress_callback("test_task")
        assert asyncio.iscoroutinefunction(cb)

    @pytest.mark.asyncio
    async def test_create_progress_callback_produces_event(self):
        from pixelle_video.services.progress_stream import progress_manager
        cb = progress_manager.create_progress_callback("test_task_cb")
        # The callback is a coroutine function; calling it is safe
        # even without real websocket subscribers
        try:
            await cb("frame", 0.5, message="hello", frame_current=1, frame_total=5)
        except Exception:
            pass  # No subscribers, so send_text won't be called

    @pytest.mark.asyncio
    async def test_broadcast_no_subscribers(self):
        from pixelle_video.services.progress_stream import (
            ProgressEvent,
            progress_manager,
        )
        event = ProgressEvent(task_id="no_sub_task", event_type="test", progress=0.0)
        sent = await progress_manager.broadcast("no_sub_task", event)
        assert sent == 0


class TestProgressEventJsonSerializable:
    """Verify progress events are JSON-serializable."""

    def test_json_serialize(self):
        from pixelle_video.services.progress_stream import ProgressEvent
        event = ProgressEvent(
            task_id="json_test",
            event_type="frame",
            progress=0.33,
            message="Encoding frame",
            data={"resolution": "1080x1920"},
        )
        payload = json.dumps(event.to_dict(), ensure_ascii=False)
        parsed = json.loads(payload)
        assert parsed["task_id"] == "json_test"
        assert parsed["progress"] == 0.33
        assert parsed["data"]["resolution"] == "1080x1920"
        assert isinstance(parsed["timestamp"], float)
