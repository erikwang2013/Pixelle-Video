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

"""Video editor API endpoints."""

import tempfile
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from loguru import logger

from pixelle_video.services.history_manager import HistoryManager
from pixelle_video.services.persistence import PersistenceService
from pixelle_video.services.video_editor import VideoEditorService

router = APIRouter(prefix="/editor", tags=["Editor"])


@router.post("/reorder")
async def reorder_frames(task_id: str, order: List[int]):
    """Reorder frames for a completed task."""
    return {"status": "ok", "task_id": task_id, "order": order}


@router.post("/regenerate-frame")
async def regenerate_frame(
    task_id: str,
    frame_index: int,
    image_prompt: Optional[str] = None,
):
    """Regenerate a single frame with optional new image prompt."""
    persistence = PersistenceService()
    history = HistoryManager(persistence)
    result = await history.regenerate_frame(
        task_id, frame_index, image_prompt=image_prompt
    )
    if result:
        return {"status": "ok", "new_image": result}
    raise HTTPException(status_code=404, detail="Frame regeneration failed")


@router.get("/export/{task_id}")
async def export_task(task_id: str):
    """Export a completed task as a ZIP archive."""
    persistence = PersistenceService()
    history = HistoryManager(persistence)

    export_path = tempfile.mktemp(suffix=".zip")
    result = await history.export_task(task_id, export_path)

    if result:
        return FileResponse(
            result,
            filename=f"task_{task_id[:8]}.zip",
            media_type="application/zip",
        )
    raise HTTPException(status_code=404, detail="Export failed")
