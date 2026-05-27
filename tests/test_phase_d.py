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

"""Tests for Phase D: Content Quality services."""
from pathlib import Path

import pytest


def test_thumbnail_frame_extraction():
    from pixelle_video.services.thumbnail import ThumbnailService
    svc = ThumbnailService()
    assert hasattr(svc, "generate_thumbnail")
    assert hasattr(svc, "add_text_overlay")


def test_watermark_text():
    from pixelle_video.services.watermark import WatermarkService
    svc = WatermarkService()
    assert hasattr(svc, "add_text_watermark")
    assert hasattr(svc, "add_image_watermark")


def test_script_templates_list():
    from pixelle_video.services.script_templates import ScriptTemplateService
    svc = ScriptTemplateService()
    templates = svc.list_templates()
    assert len(templates) >= 10
    assert svc.get_template("news")["name_zh"] == "新闻播报"


def test_script_template_apply():
    from pixelle_video.services.script_templates import ScriptTemplateService
    svc = ScriptTemplateService()
    result = svc.apply_template("tutorial", "如何使用Python")
    assert "分步骤" in result["topic_prompt"]
    assert result["n_scenes"] == 6


def test_tts_emotion_list():
    from pixelle_video.services.tts_emotion import TTSEmotionService
    svc = TTSEmotionService()
    emotions = svc.list_emotions()
    assert "excited" in emotions
    assert "gentle" in emotions


def test_tts_emotion_apply():
    from pixelle_video.services.tts_emotion import TTSEmotionService
    svc = TTSEmotionService()
    result = svc.apply_emotion(1.0, "excited")
    assert result["speed"] > 1.0


def test_batch_csv_validate():
    from pixelle_video.services.batch_csv import BatchCSVService
    svc = BatchCSVService()
    # Create temp CSV
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write("topic,title,n_scenes\nTest Topic,My Title,5\n")
        f.flush()
        valid, msg = svc.validate_csv(f.name)
        assert valid
        Path(f.name).unlink()


def test_batch_csv_parse():
    from pixelle_video.services.batch_csv import BatchCSVService
    svc = BatchCSVService()
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write("topic,title,n_scenes\nTest Topic,My Title,5\nAnother,Title2,3\n")
        f.flush()
        tasks = svc.parse_csv(f.name)
        assert len(tasks) == 2
        assert tasks[0]["text"] == "Test Topic"
        Path(f.name).unlink()
