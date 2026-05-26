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

from pathlib import Path


def test_subtitle_service_generates_srt():
    """SubtitleService should generate valid SRT from text + audio durations"""
    from pixelle_video.services.subtitle import SubtitleService
    svc = SubtitleService()

    segments = [
        {"text": "Hello world", "duration": 3.5, "audio_path": "/tmp/a1.mp3"},
        {"text": "This is a test", "duration": 2.0, "audio_path": "/tmp/a2.mp3"},
    ]
    srt_path = svc.generate_srt(segments, "/tmp/test.srt")

    assert Path(srt_path).exists()
    content = Path(srt_path).read_text()
    assert "Hello world" in content
    assert "00:00:00,000" in content


def test_srt_time_format():
    """Should correctly format SRT timestamps"""
    from pixelle_video.services.subtitle import SubtitleService
    svc = SubtitleService()
    assert svc._seconds_to_srt_time(0) == "00:00:00,000"
    assert svc._seconds_to_srt_time(65.5) == "00:01:05,500"
    assert svc._seconds_to_srt_time(3661.123) == "01:01:01,123"


def test_subtitle_text_wrapping():
    """Long text should wrap to max 2 lines"""
    from pixelle_video.services.subtitle import SubtitleService
    svc = SubtitleService()
    segments = [
        {
            "text": "This is a very long sentence that should be wrapped into two lines for readability",
            "duration": 3.0,
            "audio_path": "/tmp/a.mp3",
        },
    ]
    srt_path = svc.generate_srt(segments, "/tmp/test_wrap.srt", max_chars_per_line=30)
    content = Path(srt_path).read_text()
    # Text portion after timestamp should contain a newline (two lines)
    text_portion = content.split("-->")[1].split("\n", 1)[1]
    assert "\n" in text_portion.strip()
