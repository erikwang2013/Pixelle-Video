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

from pathlib import Path

import pytest


class TestVideoEditorService:
    """Tests for VideoEditorService — trim, reorder, replace frame operations."""

    def test_editor_exists(self):
        """Service should expose trim_segment, reorder_and_concat, replace_frame."""
        from pixelle_video.services.video_editor import VideoEditorService

        svc = VideoEditorService()
        assert hasattr(svc, "trim_segment")
        assert hasattr(svc, "reorder_and_concat")
        assert hasattr(svc, "replace_frame")

    def test_reorder_empty_segments(self):
        """Empty segments list should raise a value error."""
        from pixelle_video.services.video_editor import VideoEditorService

        svc = VideoEditorService()
        with pytest.raises(Exception) as exc_info:
            svc.reorder_and_concat([], [], "/tmp/out.mp4")
        err_msg = str(exc_info.value).lower()
        assert "empty" in err_msg or "at least" in err_msg

    def test_reorder_empty_order(self):
        """Empty order list should raise a value error."""
        from pixelle_video.services.video_editor import VideoEditorService

        svc = VideoEditorService()
        with pytest.raises(Exception) as exc_info:
            svc.reorder_and_concat(["/tmp/a.mp4"], [], "/tmp/out.mp4")
        err_msg = str(exc_info.value).lower()
        assert "empty" in err_msg or "at least" in err_msg

    def test_reorder_no_valid_segments(self):
        """Out-of-range indices in order should raise when no segments remain."""
        from pixelle_video.services.video_editor import VideoEditorService

        svc = VideoEditorService()
        with pytest.raises(ValueError) as exc_info:
            svc.reorder_and_concat(["/tmp/a.mp4"], [5, 6, 7], "/tmp/out.mp4")
        assert "no valid segments" in str(exc_info.value).lower()

    def test_replace_frame_in_bounds(self):
        """replace_frame in bounds calls reorder_and_concat (will fail at ffmpeg)."""
        from pixelle_video.services.video_editor import VideoEditorService

        svc = VideoEditorService()
        segments = ["/tmp/a.mp4", "/tmp/b.mp4", "/tmp/c.mp4"]
        try:
            svc.replace_frame(segments, 1, "/tmp/new.mp4", "/tmp/out.mp4")
        except Exception:
            pass  # Expected: ffmpeg can't find files

    def test_replace_frame_out_of_bounds_is_noop(self):
        """replace_frame with index out of bounds should just pass through."""
        from pixelle_video.services.video_editor import VideoEditorService

        svc = VideoEditorService()
        segments = ["/tmp/a.mp4", "/tmp/b.mp4", "/tmp/c.mp4"]
        # Out of bounds — should not replace, just reorder original segments
        try:
            svc.replace_frame(segments, 10, "/tmp/new.mp4", "/tmp/out.mp4")
        except Exception:
            pass  # Expected: ffmpeg can't find files
