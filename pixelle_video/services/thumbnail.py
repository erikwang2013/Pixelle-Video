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

"""AI thumbnail generation service"""
import os
from pathlib import Path

import ffmpeg
from PIL import Image, ImageDraw, ImageFont


class ThumbnailService:
    def extract_best_frame(self, video_path: str, output: str, time_offset: float = 1.0) -> str:
        """Extract a frame from video at given time offset."""
        (
            ffmpeg.input(video_path, ss=time_offset)
            .output(output, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return output

    def add_text_overlay(self, image_path: str, output: str, text: str,
                         font_size: int = 48, color: str = "white") -> str:
        """Add text overlay to thumbnail image."""
        img = Image.open(image_path).convert("RGBA")
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (img.width - tw) // 2
        y = img.height - th - 60

        # Semi-transparent background bar
        draw.rectangle([(0, y - 10), (img.width, y + th + 10)], fill=(0, 0, 0, 160))
        draw.text((x, y), text, fill=color, font=font)

        combined = Image.alpha_composite(img, overlay)
        combined.convert("RGB").save(output, "JPEG", quality=90)
        return output

    def generate_thumbnail(self, video_path: str, output: str, text: str = "",
                           time_offset: float = 1.0) -> str:
        """Generate thumbnail: extract frame + add text overlay."""
        temp_frame = output.replace(".jpg", "_frame.jpg")
        self.extract_best_frame(video_path, temp_frame, time_offset)
        if text:
            self.add_text_overlay(temp_frame, output, text)
        else:
            Path(temp_frame).rename(output)
        if os.path.exists(temp_frame):
            os.unlink(temp_frame)
        return output
