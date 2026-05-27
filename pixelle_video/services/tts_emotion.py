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

"""TTS emotion profiles"""
from typing import Dict

EMOTION_PROFILES = {
    "neutral": {"speed": 1.0, "pitch": 0, "voice_hint": "natural"},
    "excited": {"speed": 1.15, "pitch": 3, "voice_hint": "energetic, enthusiastic"},
    "serious": {"speed": 0.9, "pitch": -2, "voice_hint": "deep, authoritative"},
    "gentle": {"speed": 0.85, "pitch": 1, "voice_hint": "soft, warm, soothing"},
    "sad": {"speed": 0.8, "pitch": -3, "voice_hint": "low, emotional"},
    "professional": {"speed": 1.0, "pitch": 0, "voice_hint": "clear, articulate"},
    "casual": {"speed": 1.1, "pitch": 1, "voice_hint": "friendly, relaxed"},
    "dramatic": {"speed": 1.05, "pitch": 2, "voice_hint": "dramatic, theatrical"},
}


class TTSEmotionService:
    def list_emotions(self) -> Dict:
        return dict(EMOTION_PROFILES)

    def apply_emotion(self, speed: float, emotion: str) -> dict:
        """Get adjusted TTS params for an emotion."""
        profile = EMOTION_PROFILES.get(emotion, EMOTION_PROFILES["neutral"])
        return {
            "speed": speed * profile["speed"],
            "voice_hint": profile["voice_hint"],
        }
