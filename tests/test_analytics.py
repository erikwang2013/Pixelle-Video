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

"""Tests for the analytics service."""

import pytest


def test_summary_empty():
    from pixelle_video.services.analytics import AnalyticsService
    summary = AnalyticsService().compute_summary([])
    assert summary["total_tasks"] == 0
    assert summary["success_rate"] == 0.0


def test_summary_with_data():
    from pixelle_video.services.analytics import AnalyticsService
    tasks = [
        {"status": "completed", "duration": 120.0, "created_at": "2026-05-01T10:00:00"},
        {"status": "completed", "duration": 180.0, "created_at": "2026-05-02T10:00:00"},
        {"status": "failed", "duration": 30.0, "created_at": "2026-05-03T10:00:00"},
        {"status": "completed", "duration": 90.0, "created_at": "2026-05-04T10:00:00"},
    ]
    s = AnalyticsService().compute_summary(tasks)
    assert s["total_tasks"] == 4
    assert s["completed"] == 3
    assert s["failed"] == 1
    assert s["success_rate"] == 75.0
    assert s["total_duration_seconds"] == 390.0
    assert s["avg_duration_seconds"] == 130.0


def test_daily_trends():
    from pixelle_video.services.analytics import AnalyticsService
    tasks = [
        {"status": "completed", "duration": 60, "created_at": "2026-05-01T10:00:00"},
        {"status": "completed", "duration": 60, "created_at": "2026-05-01T14:00:00"},
        {"status": "completed", "duration": 60, "created_at": "2026-05-03T10:00:00"},
    ]
    trends = AnalyticsService().compute_daily_trends(tasks, days=7)
    assert len(trends) == 7


def test_pipeline_stats():
    from pixelle_video.services.analytics import AnalyticsService
    tasks = [
        {"status": "completed", "duration": 60, "pipeline": "standard"},
        {"status": "completed", "duration": 30, "pipeline": "digital_human"},
        {"status": "completed", "duration": 20, "pipeline": "standard"},
    ]
    stats = AnalyticsService().compute_pipeline_stats(tasks)
    assert len(stats) == 2  # 2 unique pipelines
