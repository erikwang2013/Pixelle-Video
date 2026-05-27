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

import os
import tempfile
from pathlib import Path

import pytest


def test_create_workspace():
    from pixelle_video.services.workspace import WorkspaceService
    d = tempfile.mkdtemp()
    svc = WorkspaceService(data_dir=d)
    ws = svc.create_workspace("Test WS", "user1")
    assert ws["name"] == "Test WS"
    assert "invite_code" in ws
    assert "user1" in ws["members"]

def test_join_by_invite():
    from pixelle_video.services.workspace import WorkspaceService
    d = tempfile.mkdtemp()
    svc = WorkspaceService(data_dir=d)
    ws = svc.create_workspace("Team", "admin")
    joined = svc.join_by_invite(ws["invite_code"], "newuser")
    assert joined is not None
    assert "newuser" in joined["members"]

def test_payment_plans():
    from pixelle_video.services.payment import PaymentService
    d = tempfile.mkdtemp()
    svc = PaymentService(data_dir=d)
    plans = svc.list_plans()
    assert "free" in plans
    assert "pro" in plans
    assert "enterprise" in plans

def test_payment_check_generation():
    from pixelle_video.services.payment import PaymentService
    d = tempfile.mkdtemp()
    svc = PaymentService(data_dir=d)
    allowed, _ = svc.check_generation_allowed("newuser")
    assert allowed is True  # new user gets free plan

def test_embed_code_generation():
    from pixelle_video.services.embed import EmbedService
    svc = EmbedService()
    code = svc.generate_embed_code("https://example.com/video.mp4")
    assert "<iframe" in code
    assert "https://example.com/video.mp4" in code
    assert "width=" in code

def test_share_link():
    from pixelle_video.services.embed import EmbedService
    svc = EmbedService()
    share = svc.generate_share_link("task123", "https://example.com/v.mp4", "https://mysite.com")
    assert share["share_url"] == "https://mysite.com/share/" + share["share_id"]
    assert "iframe" in share["embed_code"]

def test_player_page():
    from pixelle_video.services.embed import EmbedService
    svc = EmbedService()
    page = svc.generate_player_page("https://example.com/v.mp4", "My Video")
    assert "<video" in page
    assert "My Video" in page
