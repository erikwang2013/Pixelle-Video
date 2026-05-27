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

"""Webhook registration and dispatch service"""
import json
import hmac
import hashlib
import uuid
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import httpx
from loguru import logger


class WebhookService:
    def __init__(self, data_dir: str = "data"):
        self._data_dir = Path(data_dir)
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._webhooks_file = self._data_dir / "webhooks.json"
        self._webhooks: List[dict] = []
        self._load()

    def _load(self):
        if self._webhooks_file.exists():
            self._webhooks = json.loads(self._webhooks_file.read_text())

    def _save(self):
        self._webhooks_file.write_text(json.dumps(self._webhooks, indent=2, ensure_ascii=False))

    def register(self, url: str, events: List[str], secret: str = "") -> dict:
        hook = {
            "webhook_id": uuid.uuid4().hex[:12],
            "url": url,
            "events": events,
            "secret": secret,
            "created_at": datetime.now().isoformat(),
            "enabled": True,
        }
        self._webhooks.append(hook)
        self._save()
        return hook

    def list(self) -> List[dict]:
        return self._webhooks

    def delete(self, webhook_id: str) -> bool:
        before = len(self._webhooks)
        self._webhooks = [h for h in self._webhooks if h["webhook_id"] != webhook_id]
        if len(self._webhooks) != before:
            self._save()
            return True
        return False

    def _sign(self, payload: str, secret: str) -> str:
        return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

    async def dispatch(self, event_type: str, payload: dict) -> None:
        matching = [h for h in self._webhooks if h["enabled"] and event_type in h["events"]]
        if not matching:
            return

        payload_str = json.dumps({"event": event_type, "timestamp": datetime.now().isoformat(), "data": payload})

        async with httpx.AsyncClient(timeout=10.0) as client:
            for hook in matching:
                headers = {"Content-Type": "application/json", "X-Pixelle-Event": event_type}
                if hook["secret"]:
                    headers["X-Pixelle-Signature"] = self._sign(payload_str, hook["secret"])

                for attempt in range(3):
                    try:
                        resp = await client.post(hook["url"], content=payload_str, headers=headers)
                        if resp.status_code < 400:
                            logger.info(f"Webhook {hook['webhook_id']} delivered (attempt {attempt+1})")
                            break
                        else:
                            logger.warning(f"Webhook {hook['webhook_id']} returned {resp.status_code}")
                    except Exception as e:
                        logger.error(f"Webhook {hook['webhook_id']} attempt {attempt+1} failed: {e}")
                        if attempt < 2:
                            await asyncio.sleep(2 ** attempt)
