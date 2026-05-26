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

"""Video transition effects between frames"""

import subprocess
from pathlib import Path
from typing import List

import ffmpeg
from loguru import logger


class TransitionService:
    """Apply transition effects between concatenated video segments."""

    def list_transitions(self) -> List[str]:
        """Return available transition types."""
        return ["none", "crossfade", "fade_in_out", "slide_left", "zoom_in"]

    def concat_with_transitions(
        self,
        segments: List[str],
        output: str,
        transition: str = "none",
        transition_duration: float = 0.5,
        fps: int = 30,
    ) -> str:
        """Concatenate video segments with a transition effect between each.

        Args:
            segments: List of video file paths to concatenate
            output: Output video file path
            transition: Transition type ("none", "crossfade", "fade_in_out", "slide_left", "zoom_in")
            transition_duration: Duration of each transition in seconds
            fps: Frames per second for transition calculation

        Returns:
            Path to output video

        Raises:
            ValueError: If segments list is empty
        """
        if not segments:
            raise ValueError("segments cannot be empty")

        if len(segments) == 1 or transition == "none":
            return self._concat_simple(segments, output)

        return self._concat_xfade(segments, output, transition, transition_duration, fps)

    def _concat_simple(self, segments: List[str], output: str) -> str:
        """Simple concat without transitions."""
        concat_file = "/tmp/pixelle_concat_list.txt"
        with open(concat_file, "w") as f:
            for seg in segments:
                f.write(f"file '{str(Path(seg).absolute())}'\n")

        try:
            (
                ffmpeg
                .input(concat_file, format="concat", safe=0)
                .output(output, c="copy")
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
        finally:
            Path(concat_file).unlink(missing_ok=True)
        return output

    def _build_xfade_filters(
        self,
        n_segments: int,
        durations: List[float],
        transition: str,
        duration: float,
    ) -> tuple:
        """Build xfade filter complex string and final video label.

        Returns:
            (filter_complex_string, final_video_label)
        """
        xfade_map = {
            "crossfade": "fade",
            "fade_in_out": "fadeblack",
            "slide_left": "slideright",
            "zoom_in": "zoomin",
        }
        xfade_type = xfade_map.get(transition, "fade")

        parts = []
        running_offset = durations[0] - duration

        # First xfade: segment 0 + segment 1
        parts.append(
            f"[0:v][1:v]xfade=transition={xfade_type}:duration={duration}:offset={running_offset}[v1]"
        )
        running_offset += durations[1] - duration

        # Subsequent xfades
        for i in range(2, n_segments):
            prev = f"v{i-1}"
            curr = f"v{i}"
            parts.append(
                f"[{prev}][{i}:v]xfade=transition={xfade_type}:duration={duration}:offset={running_offset}[{curr}]"
            )
            running_offset += durations[i] - duration

        # Audio: concat all audio streams
        audio_inputs = "".join(f"[{i}:a]" for i in range(n_segments))
        parts.append(f"{audio_inputs}concat=n={n_segments}:v=0:a=1[a]")

        filter_complex = ";".join(parts)
        final_label = f"v{n_segments-1}" if n_segments > 1 else "0:v"
        return filter_complex, final_label

    def _concat_xfade(
        self,
        segments: List[str],
        output: str,
        transition: str,
        duration: float,
        fps: int,
    ) -> str:
        """Execute xfade concatenation via ffmpeg CLI."""
        # Get durations for offset calculation
        durations = []
        for seg in segments:
            try:
                probe = ffmpeg.probe(seg)
                durations.append(float(probe["format"]["duration"]))
            except Exception:
                durations.append(5.0)

        filter_complex, final_label = self._build_xfade_filters(
            len(segments), durations, transition, duration
        )

        cmd = ["ffmpeg"]
        for seg in segments:
            cmd.extend(["-i", seg])
        cmd.extend([
            "-filter_complex", filter_complex,
            "-map", f"[{final_label}]",
            "-map", "[a]",
            "-c:v", "libx264", "-c:a", "aac",
            "-preset", "medium", "-crf", "23",
            "-y", output,
        ])

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.success(f"Video with {transition} transitions: {output}")
            return output
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg xfade error: {e.stderr}")
            logger.warning("Falling back to simple concatenation")
            return self._concat_simple(segments, output)
