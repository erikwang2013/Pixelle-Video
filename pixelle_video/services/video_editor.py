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

"""Video editing operations: trim, reorder, replace frames"""

import uuid
from pathlib import Path
from typing import List, Optional

import ffmpeg
from loguru import logger


class VideoEditorService:
    """Apply trim, reorder, and frame replacement operations on video segments."""

    def trim_segment(
        self,
        video_path: str,
        output: str,
        start: float = 0,
        end: Optional[float] = None,
    ) -> str:
        """Trim a video segment from *start* to *end* (both in seconds).

        Uses stream copy (``-c copy``) for fast trimming without re-encoding.
        """
        input_kwargs = {}
        if start > 0:
            input_kwargs["ss"] = start
        if end is not None:
            input_kwargs["t"] = end - start
        (
            ffmpeg.input(video_path, **input_kwargs)
            .output(output, c="copy")
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return output

    def reorder_and_concat(
        self, segments: List[str], order: List[int], output: str
    ) -> str:
        """Reorder *segments* according to *order* indices and concatenate.

        Raises ``ValueError`` when either list is empty or when no valid
        segments remain after applying the order filter.
        """
        if not segments:
            raise ValueError("segments list cannot be empty")
        if not order:
            raise ValueError("order list cannot be empty")

        reordered = [segments[i] for i in order if 0 <= i < len(segments)]
        if not reordered:
            raise ValueError("no valid segments after reordering")

        concat_file = f"/tmp/pixelle_edit_{uuid.uuid4().hex[:8]}.txt"
        with open(concat_file, "w") as f:
            for seg in reordered:
                f.write(f"file '{str(Path(seg).absolute())}'\n")

        try:
            (
                ffmpeg.input(concat_file, format="concat", safe=0)
                .output(output, c="copy")
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
        finally:
            Path(concat_file).unlink(missing_ok=True)

        return output

    def replace_frame(
        self,
        segments: List[str],
        frame_index: int,
        new_segment: str,
        output: str,
    ) -> str:
        """Replace the segment at *frame_index* with *new_segment*, then
        concatenate all segments in their original order.

        If *frame_index* is out of bounds the original list is used unchanged.
        """
        if 0 <= frame_index < len(segments):
            segments = list(segments)
            segments[frame_index] = new_segment
        return self.reorder_and_concat(
            segments, list(range(len(segments))), output
        )
