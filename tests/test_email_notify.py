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
import asyncio


def test_email_toggle(tmp_path):
    from pixelle_video.services.email_notify import EmailNotifyService

    svc = EmailNotifyService(data_dir=str(tmp_path / "test_email_toggle"))
    assert svc.is_enabled() is False
    svc.toggle(True)
    assert svc.is_enabled() is True
    svc.toggle(False)
    assert svc.is_enabled() is False


def test_email_configure(tmp_path):
    from pixelle_video.services.email_notify import EmailNotifyService

    svc = EmailNotifyService(data_dir=str(tmp_path / "test_email_configure"))
    svc.configure("smtp.example.com", 587, "user", "pass", "from@x.com", "to@x.com")
    cfg = svc.get_config()
    assert cfg["smtp_host"] == "smtp.example.com"
    assert cfg["to_addr"] == "to@x.com"
    assert cfg["enabled"] is False


def test_send_skips_when_disabled(tmp_path):
    from pixelle_video.services.email_notify import EmailNotifyService

    svc = EmailNotifyService(data_dir=str(tmp_path / "test_send_disabled"))
    result = asyncio.run(svc.send("Test", "Body"))
    assert result is False  # disabled, should skip


def test_send_skips_when_not_configured(tmp_path):
    from pixelle_video.services.email_notify import EmailNotifyService

    svc = EmailNotifyService(data_dir=str(tmp_path / "test_send_noconfig"))
    svc.toggle(True)
    result = asyncio.run(svc.send("Test", "Body"))
    assert result is False  # enabled but no SMTP host configured


def test_config_persists_to_disk(tmp_path):
    from pixelle_video.services.email_notify import EmailNotifyService

    svc = EmailNotifyService(data_dir=str(tmp_path / "test_config_persist"))
    svc.toggle(True)
    svc.configure("mx.test.com", 465, "u", "p", "a@b.com", "c@d.com")

    # reload from same directory
    svc2 = EmailNotifyService(data_dir=str(tmp_path / "test_config_persist"))
    assert svc2.is_enabled() is True
    cfg = svc2.get_config()
    assert cfg["smtp_host"] == "mx.test.com"
    assert cfg["smtp_port"] == 465
    assert cfg["to_addr"] == "c@d.com"
