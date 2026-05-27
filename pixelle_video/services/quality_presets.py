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

"""Video quality presets for different output needs"""

QUALITY_PRESETS = {
    "draft": {
        "name": "Draft",
        "name_zh": "快速草稿",
        "resolution": "1280x720",
        "crf": 28,
        "preset": "ultrafast",
        "bitrate": "1M",
        "description": "Fast generation, smaller file, good for previews",
    },
    "standard": {
        "name": "Standard",
        "name_zh": "标准质量",
        "resolution": "1920x1080",
        "crf": 23,
        "preset": "medium",
        "bitrate": "2M",
        "description": "Balanced quality and speed, good for most uses",
    },
    "high": {
        "name": "High Quality",
        "name_zh": "高清成品",
        "resolution": "1920x1080",
        "crf": 18,
        "preset": "slow",
        "bitrate": "4M",
        "description": "Best quality, larger file, suitable for final delivery",
    },
    "ultra": {
        "name": "Ultra HD",
        "name_zh": "超高清",
        "resolution": "3840x2160",
        "crf": 16,
        "preset": "slower",
        "bitrate": "8M",
        "description": "4K resolution, maximum quality, very large files",
    },
}


class QualityPresetService:
    def list_presets(self):
        return dict(QUALITY_PRESETS)

    def get_preset(self, name: str) -> dict:
        return QUALITY_PRESETS.get(name, QUALITY_PRESETS["standard"])

    def get_ffmpeg_params(self, name: str) -> dict:
        preset = self.get_preset(name)
        w, h = preset["resolution"].split("x")
        return {
            "vcodec": "libx264",
            "preset": preset["preset"],
            "crf": preset["crf"],
            "video_bitrate": preset["bitrate"],
            "width": int(w),
            "height": int(h),
        }
