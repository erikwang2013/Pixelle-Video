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

import pytest
from pathlib import Path


def test_cloud_providers_list():
    from pixelle_video.services.cloud_storage import CloudStorageService
    svc = CloudStorageService()
    providers = svc.list_providers()
    assert "s3" in providers
    assert "oss" in providers
    assert "local" in providers


def test_cloud_local_upload():
    from pixelle_video.services.cloud_storage import CloudStorageService
    import tempfile
    svc = CloudStorageService()
    src_dir = tempfile.mkdtemp()
    dst_dir = tempfile.mkdtemp()
    f = Path(src_dir) / "test.txt"
    f.write_text("hello")
    result = svc._upload_local(str(f), {"public_dir": dst_dir, "base_url": "http://test.com"})
    assert "http://test.com/files/public/test.txt" in result["url"]


def test_rate_limiter_allows():
    from pixelle_video.services.rate_limiter import RateLimiter
    limiter = RateLimiter()
    limiter.set_limit("user1", rate=100, burst=100)
    for _ in range(50):
        assert limiter.check_limit("user1") is True


def test_rate_limiter_blocks():
    from pixelle_video.services.rate_limiter import RateLimiter
    limiter = RateLimiter()
    limiter.set_limit("user1", rate=0.1, burst=1)
    assert limiter.check_limit("user1") is True  # first one allowed via burst
    assert limiter.check_limit("user1") is False  # empty bucket


def test_analytics_export_csv():
    from pixelle_video.services.analytics_export import AnalyticsExportService
    svc = AnalyticsExportService()
    tasks = [
        {"task_id": "1", "title": "Test", "status": "completed", "duration": 60, "created_at": "2026-01-01"},
    ]
    csv_str = svc.export_csv(tasks)
    assert "Test" in csv_str
    assert "task_id" in csv_str


def test_analytics_export_html():
    from pixelle_video.services.analytics_export import AnalyticsExportService
    svc = AnalyticsExportService()
    tasks = [{"task_id": "1", "title": "Test", "status": "completed", "duration": 60, "created_at": "2026-01-01"}]
    summary = {"total_tasks": 1, "success_rate": 100, "total_duration_seconds": 60}
    html = svc.export_html_report(tasks, summary)
    assert "<html>" in html
    assert "Test" in html


def test_quality_presets():
    from pixelle_video.services.quality_presets import QualityPresetService
    svc = QualityPresetService()
    presets = svc.list_presets()
    assert len(presets) == 4
    assert "draft" in presets
    assert "ultra" in presets


def test_quality_preset_ffmpeg_params():
    from pixelle_video.services.quality_presets import QualityPresetService
    svc = QualityPresetService()
    params = svc.get_ffmpeg_params("high")
    assert params["crf"] == 18
    assert params["width"] == 1920
