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

"""Video watermark overlay service"""
import ffmpeg
from loguru import logger


class WatermarkService:
    def add_text_watermark(self, video_path: str, output: str, text: str,
                           position: str = "bottom_right", font_size: int = 24,
                           font_color: str = "white", opacity: float = 0.7) -> str:
        """Add text watermark to video using ffmpeg drawtext filter."""
        pos_map = {
            "top_left": "x=10:y=10",
            "top_right": "x=W-tw-10:y=10",
            "bottom_left": "x=10:y=H-th-10",
            "bottom_right": "x=W-tw-10:y=H-th-10",
            "center": "x=(W-tw)/2:y=(H-th)/2",
        }
        pos = pos_map.get(position, pos_map["bottom_right"])
        escaped_text = text.replace(":", "\\:").replace("'", "\\'")
        alpha = f"@{opacity:.1f}"

        drawtext = (
            f"drawtext=text='{escaped_text}':{pos}:"
            f"fontsize={font_size}:fontcolor={font_color}{alpha}:"
            f"box=1:boxcolor=black@0.3:boxborderw=5"
        )

        (
            ffmpeg.input(video_path)
            .output(output, vf=drawtext, vcodec="libx264", acodec="aac",
                    preset="medium", crf=23, audio_bitrate="192k")
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return output

    def add_image_watermark(self, video_path: str, output: str, image_path: str,
                            position: str = "bottom_right", scale: float = 0.1) -> str:
        """Add image/logo watermark overlay."""
        pos_map = {
            "top_left": "x=10:y=10",
            "top_right": "x=W-w-10:y=10",
            "bottom_left": "x=10:y=H-h-10",
            "bottom_right": "x=W-w-10:y=H-h-10",
        }
        pos = pos_map.get(position, pos_map["bottom_right"])

        overlay_filter = f"movie='{image_path}',scale=iw*{scale}:ih*{scale}[wm];[0:v][wm]overlay={pos}"

        (
            ffmpeg.input(video_path)
            .output(output, vf=overlay_filter, vcodec="libx264", acodec="aac",
                    preset="medium", crf=23, audio_bitrate="192k")
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return output
