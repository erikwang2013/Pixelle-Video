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

"""Tests for JianYing export service."""

import tempfile
from pathlib import Path

import pytest


class TestJianYingExportService:
    """Tests for JianYingExportService class."""

    def test_service_exists(self):
        from pixelle_video.services.jianying_export import JianYingExportService

        svc = JianYingExportService()
        assert hasattr(svc, "export_storyboard")
        assert hasattr(svc, "list_exports")

    def test_transition_mapping(self):
        from pixelle_video.services.jianying_export import JianYingExportService

        svc = JianYingExportService()
        assert "crossfade" in svc.SUPPORTED_TRANSITIONS
        assert "slide_left" in svc.SUPPORTED_TRANSITIONS
        assert svc.SUPPORTED_TRANSITIONS["none"] is None

    def test_list_exports_empty(self):
        from pixelle_video.services.jianying_export import JianYingExportService

        d = tempfile.mkdtemp()
        svc = JianYingExportService(output_dir=d)
        exports = svc.list_exports()
        assert isinstance(exports, list)
        assert len(exports) == 0

    def test_export_storyboard_creates_draft(self):
        """Test that export creates a draft folder with expected structure."""
        from pixelle_video.services.jianying_export import JianYingExportService

        d = tempfile.mkdtemp()
        svc = JianYingExportService(output_dir=d)

        # Create mock storyboard frames with no actual media
        frames = [
            {
                "image_path": "",
                "audio_path": "",
                "narration": "Hello world",
                "duration": 3.0,
            },
            {
                "image_path": "",
                "audio_path": "",
                "narration": "Test frame two",
                "duration": 2.0,
                "transition": "crossfade",
            },
        ]

        path = svc.export_storyboard("TestProject", frames, bgm_path=None)
        assert Path(path).exists()
        assert Path(path).is_dir()

    def test_export_storyboard_skips_missing_media(self):
        """Test that missing media paths are gracefully skipped."""
        from pixelle_video.services.jianying_export import JianYingExportService

        d = tempfile.mkdtemp()
        svc = JianYingExportService(output_dir=d)

        frames = [
            {
                "image_path": "/nonexistent/img.png",
                "audio_path": "/nonexistent/audio.mp3",
                "narration": "Test",
                "duration": 2.0,
            },
        ]

        # Should not raise an exception
        path = svc.export_storyboard("SkipMissing", frames)
        assert Path(path).exists()

    def test_supported_transitions_values(self):
        """Test that all mapped transitions are valid TransitionType enums."""
        from pixelle_video.services.jianying_export import JianYingExportService
        from pixelle_video.vendor.pyJianYingDraft import TransitionType

        svc = JianYingExportService()
        for key, value in svc.SUPPORTED_TRANSITIONS.items():
            if value is not None:
                assert isinstance(value, TransitionType), (
                    f"Key '{key}' maps to non-TransitionType: {type(value)}"
                )
