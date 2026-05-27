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

"""
History Manager Service

Business logic for history management (UI-agnostic).
Provides high-level operations on top of PersistenceService.
"""

from typing import List, Dict, Optional, Any
from pathlib import Path
from loguru import logger

from pixelle_video.services.persistence import PersistenceService


class HistoryManager:
    """
    History management service
    
    Provides business logic for:
    - Task listing and filtering
    - Task detail retrieval
    - Task duplication (for re-generation)
    - Task deletion
    - Future: Frame regeneration, export, etc.
    """
    
    def __init__(self, persistence: PersistenceService):
        """
        Initialize history manager
        
        Args:
            persistence: PersistenceService instance
        """
        self.persistence = persistence
    
    async def get_task_list(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> Dict[str, Any]:
        """
        Get paginated task list
        
        Args:
            page: Page number (1-indexed)
            page_size: Items per page
            status: Filter by status (optional)
            sort_by: Sort field (created_at, completed_at, title, duration)
            sort_order: Sort order (asc, desc)
        
        Returns:
            {
                "tasks": [...],
                "total": 100,
                "page": 1,
                "page_size": 20,
                "total_pages": 5
            }
        """
        return await self.persistence.list_tasks_paginated(
            page=page,
            page_size=page_size,
            status=status,
            sort_by=sort_by,
            sort_order=sort_order
        )
    
    async def get_task_detail(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get full task detail including storyboard
        
        Args:
            task_id: Task ID
        
        Returns:
            {
                "metadata": {...},      # Task metadata
                "storyboard": {...}     # Storyboard data (if available)
            }
            or None if task not found
        """
        metadata = await self.persistence.load_task_metadata(task_id)
        if not metadata:
            return None
        
        storyboard = await self.persistence.load_storyboard(task_id)
        
        return {
            "metadata": metadata,
            "storyboard": storyboard,
        }
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about all tasks
        
        Returns:
            {
                "total_tasks": 100,
                "completed": 95,
                "failed": 5,
                "total_duration": 3600.5,  # seconds
                "total_size": 1024000000,  # bytes
            }
        """
        return await self.persistence.get_statistics()
    
    async def delete_task(self, task_id: str) -> bool:
        """
        Delete a task and all its files
        
        Args:
            task_id: Task ID to delete
        
        Returns:
            True if successful, False otherwise
        """
        return await self.persistence.delete_task(task_id)
    
    async def duplicate_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Duplicate a task (get input parameters for new generation)
        
        This allows users to:
        1. Copy all generation parameters from a previous task
        2. Pre-fill the generation form
        3. Regenerate with same/modified parameters
        
        Args:
            task_id: Task ID to duplicate
        
        Returns:
            Input parameters dict or None if task not found
            {
                "text": "...",
                "mode": "generate",
                "title": "...",
                "n_scenes": 5,
                "tts_inference_mode": "local",
                "tts_voice": "...",
                ...
            }
        """
        metadata = await self.persistence.load_task_metadata(task_id)
        if not metadata:
            logger.warning(f"Task {task_id} not found for duplication")
            return None
        
        # Extract input parameters
        input_params = metadata.get("input", {})
        logger.info(f"Duplicated task {task_id} parameters")
        
        return input_params
    
    async def rebuild_index(self):
        """Rebuild task index (useful for maintenance or after manual changes)"""
        await self.persistence.rebuild_index()
    
    # ========================================================================
    # Future Extensions (Phase 3)
    # ========================================================================
    
    async def regenerate_frame(
        self,
        task_id: str,
        frame_index: int,
        **override_params
    ) -> Optional[str]:
        """
        Regenerate a specific frame with optional parameter overrides.

        Updates the storyboard frame with new parameters (e.g., image_prompt)
        and persists the change. Actual media re-generation must be triggered
        by the pipeline layer, which has access to the media service.

        Args:
            task_id: Original task ID
            frame_index: Frame index to regenerate (0-based)
            **override_params: Parameters to override (image_prompt, etc.)

        Returns:
            Updated frame image path, or None if failed
        """
        try:
            # Verify task exists
            metadata = await self.persistence.load_task_metadata(task_id)
            if not metadata:
                logger.error(f"Task {task_id} not found for frame regeneration")
                return None

            # Load storyboard from persistence
            storyboard = await self.persistence.load_storyboard(task_id)
            if not storyboard or frame_index >= len(storyboard.frames):
                logger.error(
                    f"Frame {frame_index} out of range for task {task_id} "
                    f"(total frames: {len(storyboard.frames) if storyboard else 0})"
                )
                return None

            frame = storyboard.frames[frame_index]

            # Apply overrides to the frame
            if "image_prompt" in override_params:
                frame.image_prompt = override_params["image_prompt"]
                logger.info(
                    f"Updated image_prompt for frame {frame_index} "
                    f"of task {task_id}"
                )

            # Save updated storyboard
            await self.persistence.save_storyboard(task_id, storyboard)

            logger.info(
                f"Frame {frame_index} parameters updated for task {task_id}. "
                f"Run pipeline to regenerate media."
            )
            return frame.image_path

        except Exception as e:
            logger.error(f"Failed to regenerate frame: {e}")
            return None
    
    async def export_task(self, task_id: str, export_path: str) -> Optional[str]:
        """
        Export task as a ZIP package containing video, frames, and metadata.

        The archive includes:
          - metadata.json (task metadata)
          - storyboard.json (storyboard data with frame details)
          - video/<filename> (final video if available)
          - frames/<index>_image.<ext> (frame images)
          - frames/<index>_audio.<ext> (frame audio)

        Args:
            task_id: Task ID to export
            export_path: Output ZIP file path (e.g., "exports/task.zip")

        Returns:
            Export file path or None if failed
        """
        import zipfile
        import json as json_module

        try:
            # Verify task exists
            metadata = await self.persistence.load_task_metadata(task_id)
            if not metadata:
                logger.error(f"Task {task_id} not found for export")
                return None

            # Ensure parent directory exists
            Path(export_path).parent.mkdir(parents=True, exist_ok=True)

            with zipfile.ZipFile(
                export_path, "w", zipfile.ZIP_DEFLATED
            ) as zf:
                # --- metadata.json ---
                export_meta = {
                    "task_id": task_id,
                    "title": metadata.get("title", ""),
                    "created_at": str(metadata.get("created_at", "")),
                    "completed_at": str(metadata.get("completed_at", "")),
                    "status": metadata.get("status", "unknown"),
                    "pipeline": metadata.get("config", {}).get(
                        "pipeline", "standard"
                    ),
                }
                zf.writestr(
                    "metadata.json",
                    json_module.dumps(
                        export_meta, indent=2, ensure_ascii=False
                    ),
                )

                # --- storyboard.json ---
                storyboard = await self.persistence.load_storyboard(task_id)
                if storyboard:
                    sb_dict = {
                        "title": storyboard.title,
                        "total_duration": storyboard.total_duration,
                        "frames": [
                            {
                                "index": f.index,
                                "narration": f.narration,
                                "image_prompt": f.image_prompt,
                                "duration": f.duration,
                            }
                            for f in storyboard.frames
                        ],
                    }
                    zf.writestr(
                        "storyboard.json",
                        json_module.dumps(
                            sb_dict, indent=2, ensure_ascii=False
                        ),
                    )

                # --- video ---
                video_path = metadata.get("result", {}).get("video_path")
                if not video_path and storyboard:
                    video_path = storyboard.final_video_path
                if video_path and Path(video_path).exists():
                    arcname = f"video{Path(video_path).suffix}"
                    zf.write(video_path, arcname)
                    logger.debug(f"Added video: {arcname}")

                # --- frames (images + audio) ---
                if storyboard:
                    for frame in storyboard.frames:
                        idx = frame.index
                        # Image
                        img = getattr(frame, "image_path", None) or getattr(
                            frame, "composed_image_path", None
                        )
                        if img and Path(img).exists():
                            arcname = f"frames/{idx:03d}_image{Path(img).suffix}"
                            zf.write(img, arcname)
                        # Audio
                        aud = getattr(frame, "audio_path", None)
                        if aud and Path(aud).exists():
                            arcname = f"frames/{idx:03d}_audio{Path(aud).suffix}"
                            zf.write(aud, arcname)

            logger.info(f"Task {task_id} exported to {export_path}")
            return export_path

        except Exception as e:
            logger.error(f"Failed to export task {task_id}: {e}")
            return None

