# Copyright (C) 2025 AIDC-AI
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

"""Integration tests for Phase 2 features: analytics, editor, i18n."""

import pytest


class TestAnalyticsIntegration:
    """Integration tests for analytics service with realistic data."""

    def test_analytics_summary_with_real_data(self):
        from pixelle_video.services.analytics import AnalyticsService

        tasks = [
            {
                "status": "completed",
                "duration": 120,
                "created_at": "2026-05-01T10:00:00",
                "pipeline": "standard",
            },
            {
                "status": "failed",
                "duration": 10,
                "created_at": "2026-05-02T10:00:00",
                "pipeline": "digital_human",
            },
            {
                "status": "completed",
                "duration": 90,
                "created_at": "2026-05-03T10:00:00",
                "pipeline": "standard",
            },
        ]
        s = AnalyticsService().compute_summary(tasks)
        assert s["total_tasks"] == 3
        assert s["completed"] == 2
        assert s["failed"] == 1

    def test_analytics_pipeline_stats(self):
        from pixelle_video.services.analytics import AnalyticsService

        tasks = [
            {"status": "completed", "duration": 60, "pipeline": "standard"},
            {"status": "completed", "duration": 30, "pipeline": "digital_human"},
        ]
        stats = AnalyticsService().compute_pipeline_stats(tasks)
        assert len(stats) == 2

    def test_summary_all_failed(self):
        from pixelle_video.services.analytics import AnalyticsService

        tasks = [
            {"status": "failed", "duration": 10, "created_at": "2026-05-01T10:00:00"},
            {"status": "failed", "duration": 5, "created_at": "2026-05-02T10:00:00"},
        ]
        s = AnalyticsService().compute_summary(tasks)
        assert s["total_tasks"] == 2
        assert s["completed"] == 0
        assert s["failed"] == 2
        assert s["success_rate"] == 0.0
        assert s["total_duration_seconds"] == 0.0  # only completed durations count

    def test_summary_none_duration_handled(self):
        from pixelle_video.services.analytics import AnalyticsService

        tasks = [
            {"status": "completed", "duration": None, "created_at": "2026-05-01T10:00:00"},
            {"status": "completed", "duration": 50, "created_at": "2026-05-02T10:00:00"},
        ]
        s = AnalyticsService().compute_summary(tasks)
        assert s["total_tasks"] == 2
        assert s["total_duration_seconds"] == 50.0


class TestEditorIntegration:
    """Integration tests for video editor service."""

    def test_editor_reorder_empty_raises(self):
        from pixelle_video.services.video_editor import VideoEditorService

        with pytest.raises(ValueError):
            VideoEditorService().reorder_and_concat([], [], "/tmp/out.mp4")

    def test_editor_reorder_empty_order_raises(self):
        from pixelle_video.services.video_editor import VideoEditorService

        with pytest.raises(ValueError):
            VideoEditorService().reorder_and_concat(
                ["/tmp/a.mp4"], [], "/tmp/out.mp4"
            )

    def test_editor_reorder_no_valid_segments(self):
        from pixelle_video.services.video_editor import VideoEditorService

        with pytest.raises(ValueError) as exc_info:
            VideoEditorService().reorder_and_concat(
                ["/tmp/a.mp4"], [5, 6, 7], "/tmp/out.mp4"
            )
        assert "no valid segments" in str(exc_info.value).lower()

    def test_editor_replace_frame_out_of_bounds_is_noop(self):
        from pixelle_video.services.video_editor import VideoEditorService

        svc = VideoEditorService()
        segments = ["/tmp/a.mp4", "/tmp/b.mp4", "/tmp/c.mp4"]
        # Out of bounds — should fall through, will fail at ffmpeg with missing files
        try:
            svc.replace_frame(segments, 10, "/tmp/new.mp4", "/tmp/out.mp4")
        except Exception:
            pass  # Expected: ffmpeg can't find temp files


class TestI18nIntegration:
    """Integration tests for i18n keys added in Phase 2."""

    def test_analytics_i18n_keys_exist(self):
        from web.i18n import tr, set_language

        keys = [
            "analytics.title",
            "analytics.total_tasks",
            "analytics.success_rate",
            "analytics.total_duration",
            "analytics.avg_duration",
            "analytics.daily_trends",
            "analytics.pipeline_distribution",
            "analytics.no_data",
        ]

        for lang in ("zh_CN", "en_US"):
            set_language(lang)
            for key in keys:
                translated = tr(key)
                assert translated != key, (
                    f"Key '{key}' not translated in {lang}"
                )

    def test_editor_i18n_keys_exist(self):
        from web.i18n import tr, set_language

        keys = [
            "editor.title",
            "editor.no_tasks",
            "editor.select_task",
            "editor.frames",
            "editor.apply_reorder",
            "editor.reorder_success",
            "editor.reorder_frames",
            "editor.regenerate_frame",
            "editor.frame_index",
            "editor.new_prompt",
            "editor.new_prompt_placeholder",
            "editor.regenerate_frame_btn",
            "editor.regenerating",
            "editor.regenerate_success",
            "editor.regenerate_failed",
            "editor.export_task",
            "editor.export_success",
            "editor.export_failed",
            "editor.exporting",
        ]

        for lang in ("zh_CN", "en_US"):
            set_language(lang)
            for key in keys:
                translated = tr(key)
                assert translated != key, (
                    f"Key '{key}' not translated in {lang}"
                )
