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

"""Phase 3 integration tests for auth, webhook, scheduler, and social services."""
import pytest


def test_auth_full_flow():
    import os
    import tempfile

    from pixelle_video.services.auth import UserManager
    d = tempfile.mkdtemp()
    mgr = UserManager(data_dir=d)
    mgr.create_user("flowuser", "testpass")
    assert mgr.authenticate("flowuser", "testpass") is not None
    key = mgr.create_api_key("flowuser")
    result = mgr.validate_api_key(key)
    assert result["username"] == "flowuser"


def test_webhook_full_flow():
    import os
    import tempfile

    from pixelle_video.services.webhook import WebhookService
    d = tempfile.mkdtemp()
    svc = WebhookService(data_dir=d)
    h = svc.register("https://hook.example.com/1", ["task.completed"], "s3cret")
    assert len(svc.list()) == 1
    assert svc.delete(h["webhook_id"]) is True
    assert len(svc.list()) == 0


def test_scheduler_full_flow():
    import os
    import tempfile

    from pixelle_video.services.scheduler import TaskScheduler
    d = tempfile.mkdtemp()
    svc = TaskScheduler(data_dir=d)
    s = svc.add_schedule("Test Job", "0 9 * * 1-5")
    assert len(svc.list_schedules()) == 1
    assert svc.remove_schedule(s["schedule_id"]) is True


def test_social_platforms():
    import os
    import tempfile

    from pixelle_video.services.social_publisher import SocialPublisher
    d = tempfile.mkdtemp()
    svc = SocialPublisher(data_dir=d)
    assert len(svc.list_platforms()) == 3
    assert svc.get_history() == []


def test_i18n_keys_exist():
    import json
    for lang in ["zh_CN", "en_US"]:
        with open(f"web/i18n/locales/{lang}.json") as f:
            data = json.load(f)
        for key in ["auth.login_title", "account.title", "webhook.title", "scheduler.title"]:
            assert key in data["t"], f"{lang}: missing '{key}'"
