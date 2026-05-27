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

"""Subtitle generation and burning service"""

from pathlib import Path
from typing import Dict, List

import ffmpeg
from loguru import logger


class SubtitleService:
    """Generate SRT subtitles and burn them into video"""

    def generate_srt(
        self,
        segments: List[Dict],
        output_path: str,
        max_chars_per_line: int = 40,
    ) -> str:
        """Generate SRT file from text segments with cumulative timing.

        Each segment: {"text": str, "duration": float, "audio_path": str}
        Duration is used to calculate start/end times cumulatively.
        """
        if not segments:
            raise ValueError("segments cannot be empty")

        entries = []
        start_time = 0.0

        for i, seg in enumerate(segments, 1):
            text = seg["text"]
            duration = seg.get("duration", 2.0)
            end_time = start_time + duration

            # Wrap long text into max 2 lines
            if len(text) > max_chars_per_line:
                mid = len(text) // 2
                # Search both forward and backward for nearest space to mid
                left_idx = text.rfind(" ", 0, mid)
                right_idx = text.find(" ", mid)
                if left_idx == -1 and right_idx == -1:
                    space_idx = mid
                elif left_idx == -1:
                    space_idx = right_idx
                elif right_idx == -1:
                    space_idx = left_idx
                else:
                    # Choose the space closer to mid
                    space_idx = left_idx if (mid - left_idx) <= (right_idx - mid) else right_idx
                text = text[:space_idx].strip() + "\n" + text[space_idx:].strip()

            start_ts = self._seconds_to_srt_time(start_time)
            end_ts = self._seconds_to_srt_time(end_time)
            entries.append(f"{i}\n{start_ts} --> {end_ts}\n{text}\n")
            start_time = end_time

        srt_content = "\n".join(entries)
        Path(output_path).write_text(srt_content, encoding="utf-8")
        logger.info(f"Generated SRT: {output_path} ({len(segments)} entries)")
        return output_path

    def burn_subtitles(
        self,
        video_path: str,
        srt_path: str,
        output_path: str,
        font_size: int = 22,
        font_color: str = "white",
        outline_color: str = "black",
        position: str = "bottom",
    ) -> str:
        """Burn subtitles into video using ffmpeg subtitles filter.

        Args:
            video_path: Input video file
            srt_path: SRT subtitle file path
            output_path: Output video with burned subtitles
            font_size: Subtitle font size in pixels
            font_color: Text color name (white, black, yellow, red, green, blue)
            outline_color: Text outline color name
            position: "bottom", "top", or "center"

        Returns:
            Path to output video with subtitles
        """
        y_positions = {"bottom": "H-th-60", "top": "60", "center": "H/2-th/2"}
        y_pos = y_positions.get(position, "H-th-60")

        style = (
            f"FontSize={font_size},"
            f"PrimaryColour=&H{self._color_to_hex(font_color)},"
            f"OutlineColour=&H{self._color_to_hex(outline_color)},"
            f"Outline=2,"
            f"BorderStyle=1,"
            f"Alignment=2"
        )

        escaped = str(Path(srt_path).absolute()).replace("\\", "/").replace(":", "\\\\:")

        try:
            (
                ffmpeg
                .input(video_path)
                .output(
                    output_path,
                    vcodec="libx264",
                    acodec="aac",
                    audio_bitrate="192k",
                    preset="medium",
                    crf=23,
                    vf=f"subtitles='{escaped}':force_style='{style}'",
                )
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            logger.success(f"Subtitles burned: {output_path}")
            return output_path
        except ffmpeg.Error as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            logger.error(f"FFmpeg subtitle error: {error_msg}")
            raise RuntimeError(f"Failed to burn subtitles: {error_msg}")

    def _seconds_to_srt_time(self, seconds: float) -> str:
        """Convert seconds to SRT timestamp format: HH:MM:SS,mmm"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = round((seconds - int(seconds)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    def _color_to_hex(self, color_name: str) -> str:
        """Convert color name to BGR hex for ffmpeg (reverse byte order)"""
        colors = {
            "white": "FFFFFF",
            "black": "000000",
            "yellow": "00FFFF",
            "red": "0000FF",
            "green": "00FF00",
            "blue": "FF0000",
        }
        return colors.get(color_name.lower(), "FFFFFF")
