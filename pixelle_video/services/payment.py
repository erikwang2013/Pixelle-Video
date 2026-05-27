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

"""Stripe payment integration service"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


PLANS = {
    "free": {
        "name": "Free",
        "name_zh": "免费版",
        "price_monthly": 0,
        "generations_per_month": 10,
        "max_video_duration": 60,
        "quality_presets": ["draft", "standard"],
        "features": ["basic generation", "5 templates", "720p output"],
    },
    "pro": {
        "name": "Pro",
        "name_zh": "专业版",
        "price_monthly": 19.99,
        "generations_per_month": 100,
        "max_video_duration": 300,
        "quality_presets": ["draft", "standard", "high"],
        "features": ["unlimited templates", "1080p output", "subtitles", "transitions", "multi-voice", "batch generation"],
    },
    "enterprise": {
        "name": "Enterprise",
        "name_zh": "企业版",
        "price_monthly": 99.99,
        "generations_per_month": -1,  # unlimited
        "max_video_duration": 1800,
        "quality_presets": ["draft", "standard", "high", "ultra"],
        "features": ["everything in Pro", "4K output", "API access", "webhooks", "scheduler", "team workspaces", "priority support"],
    },
}


class PaymentService:
    def __init__(self, data_dir: str = "data"):
        self._data_dir = Path(data_dir)
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._subscriptions_file = self._data_dir / "subscriptions.json"
        self._subscriptions: Dict[str, dict] = {}
        self._load()

    def _load(self):
        if self._subscriptions_file.exists():
            self._subscriptions = json.loads(self._subscriptions_file.read_text())

    def _save(self):
        self._subscriptions_file.write_text(json.dumps(self._subscriptions, indent=2, ensure_ascii=False))

    def list_plans(self) -> Dict:
        return dict(PLANS)

    def get_plan(self, plan_id: str) -> Optional[dict]:
        return PLANS.get(plan_id)

    def get_subscription(self, user_id: str) -> dict:
        """Get user's current subscription, defaulting to free."""
        return self._subscriptions.get(user_id, {
            "user_id": user_id,
            "plan": "free",
            "generations_used": 0,
            "started_at": datetime.now().isoformat(),
            "renews_at": None,
        })

    def create_checkout_session(self, user_id: str, plan_id: str) -> dict:
        """Create a Stripe checkout session (placeholder)."""
        plan = PLANS.get(plan_id)
        if not plan:
            return {"error": f"Unknown plan: {plan_id}"}

        # In production: call stripe.checkout.Session.create()
        # For now: return a placeholder checkout URL
        return {
            "checkout_url": f"https://checkout.stripe.com/pay/{plan_id}?client_reference_id={user_id}",
            "plan": plan["name"],
            "amount": plan["price_monthly"],
            "currency": "usd",
        }

    def handle_webhook(self, event_type: str, data: dict) -> dict:
        """Handle Stripe webhook events."""
        if event_type == "checkout.session.completed":
            user_id = data.get("client_reference_id", "")
            plan_id = data.get("metadata", {}).get("plan_id", "pro")
            self._subscriptions[user_id] = {
                "user_id": user_id,
                "plan": plan_id,
                "generations_used": 0,
                "started_at": datetime.now().isoformat(),
                "renews_at": None,
            }
            self._save()
            return {"status": "subscribed", "user_id": user_id, "plan": plan_id}
        elif event_type == "customer.subscription.deleted":
            user_id = data.get("client_reference_id", "")
            if user_id in self._subscriptions:
                self._subscriptions[user_id]["plan"] = "free"
                self._save()
            return {"status": "cancelled", "user_id": user_id}
        return {"status": "ignored"}

    def check_generation_allowed(self, user_id: str) -> tuple[bool, str]:
        """Check if user can generate more videos. Returns (allowed, reason)."""
        sub = self.get_subscription(user_id)
        plan = PLANS.get(sub["plan"], PLANS["free"])
        max_gen = plan["generations_per_month"]
        if max_gen == -1:  # unlimited
            return True, ""
        if sub["generations_used"] >= max_gen:
            return False, f"Monthly limit reached ({max_gen} videos). Upgrade to continue."
        return True, ""

    def record_generation(self, user_id: str):
        """Record a video generation for usage tracking."""
        if user_id in self._subscriptions:
            self._subscriptions[user_id]["generations_used"] += 1
        else:
            self._subscriptions[user_id] = {
                "user_id": user_id, "plan": "free",
                "generations_used": 1,
                "started_at": datetime.now().isoformat(), "renews_at": None,
            }
        self._save()
