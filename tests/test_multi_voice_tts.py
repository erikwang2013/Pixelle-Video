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

import pytest


def test_voice_assignment_resolves():
    """Voice assignment helper should map frame index to voice name, alternating"""
    from pixelle_video.utils.tts_util import resolve_voice_for_frame

    voices = ["voice_A", "voice_B", "voice_C"]
    assert resolve_voice_for_frame(0, voices) == "voice_A"
    assert resolve_voice_for_frame(1, voices) == "voice_B"
    assert resolve_voice_for_frame(2, voices) == "voice_C"
    assert resolve_voice_for_frame(3, voices) == "voice_A"  # wraps around


def test_empty_voice_list_returns_default():
    """Empty voice list should return default voice"""
    from pixelle_video.utils.tts_util import resolve_voice_for_frame
    result = resolve_voice_for_frame(0, [])
    assert result == "zh_CN_XiaoxiaoNeural"


def test_voice_wraps_for_any_index():
    """Voice resolution should handle any frame index"""
    from pixelle_video.utils.tts_util import resolve_voice_for_frame
    voices = ["A", "B"]
    assert resolve_voice_for_frame(5, voices) == "B"  # 5 % 2 = 1 -> "B"
    assert resolve_voice_for_frame(100, voices) == "A"  # 100 % 2 = 0 -> "A"
