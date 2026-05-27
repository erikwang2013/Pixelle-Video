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

"""Export Pixelle-Video generated content to JianYing (剪映) draft format.

Uses the bundled pyJianYingDraft library to create native JianYing draft files
that can be opened in JianYing Pro (剪映专业版) / CapCut for pro-level editing.
"""

import shutil
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

from loguru import logger

from pixelle_video.vendor.pyJianYingDraft import (
    AudioSegment,
    ClipSettings,
    DraftFolder,
    SEC,
    TextSegment,
    TextStyle,
    Timerange,
    TrackType,
    TransitionType,
    VideoSegment,
    tim,
)
from pixelle_video.vendor.pyJianYingDraft.video_segment import Transition

# Track names used in the generated draft
TRACK_NAMES = {
    "video": "VideoTrack",
    "audio": "AudioTrack",
    "bgm": "BGMTrack",
    "subtitle": "SubtitleTrack",
}


class JianYingExportService:
    """Export Pixelle-Video storyboard to JianYing draft format.

    Creates a native JianYing draft folder structure that can be opened
    directly in JianYing Pro (剪映专业版) or CapCut for further editing
    and professional rendering.
    """

    SUPPORTED_TRANSITIONS = {
        "crossfade": TransitionType.叠化,
        "slide_right": TransitionType.向右,
        "slide_left": TransitionType.滑动,
        "zoom_in": TransitionType.模糊放大,
        "none": None,
    }

    def __init__(self, output_dir: str = "data/jianying_exports"):
        self._output_dir = Path(output_dir)
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def export_storyboard(
        self,
        project_name: str,
        frames: List[Dict],
        bgm_path: Optional[str] = None,
        resolution: tuple = (1080, 1920),
        fps: int = 30,
    ) -> str:
        """Export a Pixelle-Video storyboard to JianYing draft format.

        Args:
            project_name: Name for the JianYing project / draft folder.
            frames: List of frame dicts. Each dict may contain:
                - image_path (str): path to generated image
                - audio_path (str): path to TTS audio
                - narration (str): subtitle text
                - duration (float): frame duration in seconds
                - transition (str): transition name (key in SUPPORTED_TRANSITIONS)
            bgm_path: Optional path to background music file.
            resolution: (width, height) tuple in pixels.
            fps: Frames per second for the draft.

        Returns:
            Absolute path to the generated JianYing draft folder.
        """
        # Create a temporary workspace folder, then move to output dir on success
        workspace = Path(tempfile.mkdtemp(prefix="jy_workspace_"))
        try:
            # DraftFolder requires an existing folder
            draft_mgr = DraftFolder(str(workspace))

            # Create the draft (returns a ScriptFile for editing)
            width, height = resolution
            script = draft_mgr.create_draft(
                project_name,
                width=width,
                height=height,
                fps=fps,
                allow_replace=True,
            )

            # Create tracks
            script.add_track(TrackType.video, TRACK_NAMES["video"])
            script.add_track(TrackType.audio, TRACK_NAMES["audio"])
            script.add_track(TrackType.text, TRACK_NAMES["subtitle"])
            if bgm_path and Path(bgm_path).exists():
                script.add_track(TrackType.audio, TRACK_NAMES["bgm"], mute=False)

            # Track timeline position in seconds (cumulative)
            current_time = 0.0

            for i, frame in enumerate(frames):
                duration = float(frame.get("duration", 3.0))
                image_path = frame.get("image_path", "")
                audio_path = frame.get("audio_path", "")
                narration = frame.get("narration", "")

                start_us = int(current_time * SEC)
                dur_us = int(duration * SEC)
                target_range = Timerange(start_us, dur_us)

                # Add image as video segment
                if image_path and Path(image_path).exists():
                    try:
                        vid_seg = VideoSegment(
                            material=str(image_path),
                            target_timerange=target_range,
                        )

                        # Add transition to this segment (between frames)
                        if i > 0 and frame.get("transition"):
                            jy_trans = self.SUPPORTED_TRANSITIONS.get(
                                frame.get("transition")
                            )
                            if jy_trans is not None:
                                vid_seg.transition = Transition(jy_trans)

                        script.add_segment(vid_seg, TRACK_NAMES["video"])
                    except Exception as exc:
                        logger.warning(
                            f"Failed to add video segment for frame {i}: {exc}"
                        )

                # Add audio as audio segment
                if audio_path and Path(audio_path).exists():
                    try:
                        audio_seg = AudioSegment(
                            material=str(audio_path),
                            target_timerange=target_range,
                            volume=1.0,
                        )
                        script.add_segment(audio_seg, TRACK_NAMES["audio"])
                    except Exception as exc:
                        logger.warning(
                            f"Failed to add audio segment for frame {i}: {exc}"
                        )

                # Add subtitle text
                if narration:
                    try:
                        text_seg = TextSegment(
                            text=narration[:500],  # guard against overly long text
                            timerange=target_range,
                            style=TextStyle(size=5.5, align=1),
                            clip_settings=ClipSettings(transform_y=-0.8),
                        )
                        script.add_segment(text_seg, TRACK_NAMES["subtitle"])
                    except Exception as exc:
                        logger.warning(
                            f"Failed to add text segment for frame {i}: {exc}"
                        )

                current_time += duration

            # Add BGM spanning the full timeline
            if bgm_path and Path(bgm_path).exists():
                try:
                    total_us = int(current_time * SEC)
                    bgm_range = Timerange(0, total_us)
                    bgm_seg = AudioSegment(
                        material=str(bgm_path),
                        target_timerange=bgm_range,
                        volume=0.3,
                    )
                    script.add_segment(bgm_seg, TRACK_NAMES["bgm"])
                except Exception as exc:
                    logger.warning(f"Failed to add BGM: {exc}")

            # Save the draft content JSON
            script.save()

            # Move from workspace to output directory
            output_draft_dir = self._output_dir / project_name
            draft_src = workspace / project_name
            if output_draft_dir.exists():
                shutil.rmtree(str(output_draft_dir))
            shutil.move(str(draft_src), str(output_draft_dir))

            logger.info(
                f"JianYing draft exported: {output_draft_dir} "
                f"({len(frames)} frames, {current_time:.1f}s total)"
            )
            return str(output_draft_dir.absolute())

        finally:
            # Clean up workspace if still exists
            if workspace.exists():
                shutil.rmtree(str(workspace), ignore_errors=True)

    def list_exports(self) -> List[Dict]:
        """List recent JianYing exports in the output directory."""
        exports = []
        for d in self._output_dir.iterdir():
            if d.is_dir():
                # Check if it looks like a JianYing draft
                has_content = (d / "draft_content.json").exists()
                has_meta = (d / "draft_meta_info.json").exists()
                exports.append({
                    "name": d.name,
                    "path": str(d.absolute()),
                    "modified": d.stat().st_mtime,
                    "is_valid_draft": has_content and has_meta,
                })
        return sorted(exports, key=lambda x: x["modified"], reverse=True)
