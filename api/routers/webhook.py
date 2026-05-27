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

"""Webhook API endpoints"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from pixelle_video.services.webhook import WebhookService

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])
webhook_service = WebhookService()


class WebhookRequest(BaseModel):
    url: str
    events: List[str]
    secret: str = ""


@router.get("")
async def list_webhooks():
    return webhook_service.list()


@router.post("")
async def create_webhook(req: WebhookRequest):
    return webhook_service.register(req.url, req.events, req.secret)


@router.delete("/{webhook_id}")
async def delete_webhook(webhook_id: str):
    if webhook_service.delete(webhook_id):
        return {"status": "ok"}
    raise HTTPException(status_code=404, detail="Webhook not found")


@router.post("/test")
async def test_webhook(webhook_id: str):
    await webhook_service.dispatch("test.event", {"message": "Test webhook dispatch"})
    return {"status": "test_dispatched"}
