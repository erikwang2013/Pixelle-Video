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

"""Analytics API endpoints."""

from fastapi import APIRouter, Query

from api.tasks import task_manager
from pixelle_video.services.analytics import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
async def get_summary():
    """Get analytics summary: total tasks, success rate, durations."""
    tasks = task_manager.list_tasks(limit=10000)
    task_dicts = [
        t.model_dump() if hasattr(t, "model_dump") else t for t in tasks
    ]
    return AnalyticsService().compute_summary(task_dicts)


@router.get("/trends")
async def get_trends(days: int = Query(30, ge=1, le=365)):
    """Get daily task generation trends for the last *days* days."""
    tasks = task_manager.list_tasks(limit=10000)
    task_dicts = [
        t.model_dump() if hasattr(t, "model_dump") else t for t in tasks
    ]
    return AnalyticsService().compute_daily_trends(task_dicts, days=days)


@router.get("/pipelines")
async def get_pipeline_stats():
    """Get pipeline usage distribution statistics."""
    tasks = task_manager.list_tasks(limit=10000)
    task_dicts = [
        t.model_dump() if hasattr(t, "model_dump") else t for t in tasks
    ]
    return AnalyticsService().compute_pipeline_stats(task_dicts)
