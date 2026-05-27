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

import pytest


def test_register_and_list(tmp_path):
    from pixelle_video.services.webhook import WebhookService
    svc = WebhookService(data_dir=str(tmp_path / "test_webhook"))
    svc.register("https://example.com/hook", ["task.completed"], "secret123")
    hooks = svc.list()
    assert len(hooks) == 1
    assert hooks[0]["url"] == "https://example.com/hook"


def test_delete_webhook(tmp_path):
    from pixelle_video.services.webhook import WebhookService
    svc = WebhookService(data_dir=str(tmp_path / "test_webhook2"))
    hook = svc.register("https://example.com/hook", ["task.completed"])
    assert svc.delete(hook["webhook_id"]) is True
    assert len(svc.list()) == 0


def test_signature_consistent(tmp_path):
    from pixelle_video.services.webhook import WebhookService
    svc = WebhookService(data_dir=str(tmp_path / "test_webhook3"))
    sig1 = svc._sign("hello", "secret")
    sig2 = svc._sign("hello", "secret")
    assert sig1 == sig2
    assert svc._sign("hello", "secret") != svc._sign("hello", "different")
