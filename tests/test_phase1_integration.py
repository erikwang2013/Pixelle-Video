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

"""Phase 1 integration tests: subtitles, transitions, multi-voice, URL fetcher"""
import pytest
from pathlib import Path


class TestSubtitleService:
    """Integration tests for subtitle generation"""

    def test_srt_format_has_correct_timestamps(self, tmp_path):
        from pixelle_video.services.subtitle import SubtitleService

        svc = SubtitleService()
        segments = [
            {"text": "First segment", "duration": 1.0, "audio_path": "/tmp/a.mp3"},
            {"text": "Second segment", "duration": 2.0, "audio_path": "/tmp/b.mp3"},
        ]
        srt = svc.generate_srt(segments, str(tmp_path / "test_integration.srt"))
        content = Path(srt).read_text()
        assert "00:00:00,000" in content  # first starts at 0
        assert "00:00:01,000" in content  # second starts at 1s
        assert "00:00:03,000" in content  # second ends at 3s

    def test_empty_segments_raises(self):
        from pixelle_video.services.subtitle import SubtitleService

        with pytest.raises(ValueError, match="segments cannot be empty"):
            SubtitleService().generate_srt([], "/tmp/empty.srt")

    def test_color_hex_all_colors(self):
        from pixelle_video.services.subtitle import SubtitleService

        svc = SubtitleService()
        assert svc._color_to_hex("white") == "FFFFFF"
        assert svc._color_to_hex("black") == "000000"
        assert svc._color_to_hex("yellow") == "00FFFF"
        assert svc._color_to_hex("red") == "0000FF"
        assert svc._color_to_hex("green") == "00FF00"
        assert svc._color_to_hex("blue") == "FF0000"
        assert svc._color_to_hex("unknown") == "FFFFFF"


class TestTransitionService:
    """Integration tests for transition effects"""

    def test_all_five_transitions_listed(self):
        from pixelle_video.services.transition import TransitionService

        types = TransitionService().list_transitions()
        assert len(types) == 5
        for t in ["none", "crossfade", "fade_in_out", "slide_left", "zoom_in"]:
            assert t in types, f"Missing transition: {t}"

    def test_empty_segments_raises(self):
        from pixelle_video.services.transition import TransitionService

        with pytest.raises(ValueError, match="segments cannot be empty"):
            TransitionService().concat_with_transitions([], "/tmp/out.mp4")

    def test_xfade_filter_for_3_segments(self):
        from pixelle_video.services.transition import TransitionService

        svc = TransitionService()
        filters, label = svc._build_xfade_filters(3, [3.0, 2.0, 4.0], "crossfade", 0.5)
        assert "[0:v][1:v]xfade" in filters
        assert "[v1][2:v]xfade" in filters
        assert "concat" in filters  # audio concat
        assert "[a]" in filters
        assert label == "v2"


class TestMultiVoiceTTS:
    """Integration tests for multi-voice TTS"""

    def test_alternating_voices(self):
        from pixelle_video.utils.tts_util import resolve_voice_for_frame

        voices = ["A", "B", "C"]
        # Pattern: A, B, C, A, B, C, ...
        assert resolve_voice_for_frame(0, voices) == "A"
        assert resolve_voice_for_frame(1, voices) == "B"
        assert resolve_voice_for_frame(2, voices) == "C"
        assert resolve_voice_for_frame(3, voices) == "A"
        assert resolve_voice_for_frame(5, voices) == "C"
        assert resolve_voice_for_frame(100, voices) == "B"  # 100 % 3 = 1 -> B

    def test_single_voice_always_returns_it(self):
        from pixelle_video.utils.tts_util import resolve_voice_for_frame

        assert resolve_voice_for_frame(0, ["only"]) == "only"
        assert resolve_voice_for_frame(99, ["only"]) == "only"

    def test_empty_voices_returns_default(self):
        from pixelle_video.utils.tts_util import resolve_voice_for_frame

        assert resolve_voice_for_frame(0, []) == "zh_CN_XiaoxiaoNeural"


class TestURLFetcher:
    """Integration tests for URL content fetcher"""

    def test_valid_urls(self):
        from pixelle_video.services.url_fetcher import URLFetcher

        f = URLFetcher()
        assert f._is_valid_url("https://example.com/path?q=1") is True
        assert f._is_valid_url("http://localhost:8080") is True
        assert f._is_valid_url("https://sub.domain.org/path/to/page") is True

    def test_invalid_urls(self):
        from pixelle_video.services.url_fetcher import URLFetcher

        f = URLFetcher()
        assert f._is_valid_url("not-a-url") is False
        assert f._is_valid_url("ftp://files.com") is False
        assert f._is_valid_url("") is False
        assert f._is_valid_url("just text") is False

    def test_html_noise_removed(self):
        from pixelle_video.services.url_fetcher import URLFetcher

        f = URLFetcher()
        html = "<html><body><script>alert('xss')</script><style>.a{}</style><p>Good content</p></body></html>"
        text = f.extract_article_text(html)
        assert "Good content" in text
        assert "alert" not in text
        assert ".a{}" not in text
        assert "xss" not in text

    def test_article_selector_preferred(self):
        from pixelle_video.services.url_fetcher import URLFetcher

        f = URLFetcher()
        html = "<html><body><nav>Menu</nav><article><p>Main article</p></article><footer>Bottom</footer></body></html>"
        text = f.extract_article_text(html)
        assert "Main article" in text
        assert "Menu" not in text
        assert "Bottom" not in text
