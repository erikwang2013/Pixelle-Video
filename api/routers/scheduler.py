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

"""Scheduler API endpoints"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from pixelle_video.services.scheduler import TaskScheduler

router = APIRouter(prefix="/schedules", tags=["Scheduler"])
scheduler = TaskScheduler()


class ScheduleRequest(BaseModel):
    name: str
    cron_expression: str
    pipeline: str = "standard"
    params: dict = {}


@router.get("")
async def list_schedules():
    return scheduler.list_schedules()


@router.post("")
async def create_schedule(req: ScheduleRequest):
    return scheduler.add_schedule(req.name, req.cron_expression, req.pipeline, req.params)


@router.delete("/{schedule_id}")
async def delete_schedule(schedule_id: str):
    if scheduler.remove_schedule(schedule_id):
        return {"status": "ok"}
    raise HTTPException(status_code=404, detail="Schedule not found")
