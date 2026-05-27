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


def test_create_user(tmp_path):
    from pixelle_video.services.auth import UserManager
    mgr = UserManager(data_dir=str(tmp_path / "test_auth"))
    user = mgr.create_user("testuser", "password123")
    assert user["username"] == "testuser"
    assert "password_hash" not in str(user)


def test_auth_success_and_fail(tmp_path):
    from pixelle_video.services.auth import UserManager
    mgr = UserManager(data_dir=str(tmp_path / "test_auth2"))
    mgr.create_user("authuser", "correct")
    assert mgr.authenticate("authuser", "correct") is not None
    assert mgr.authenticate("authuser", "wrong") is None
    assert mgr.authenticate("nobody", "x") is None


def test_api_key_flow(tmp_path):
    from pixelle_video.services.auth import UserManager
    mgr = UserManager(data_dir=str(tmp_path / "test_auth3"))
    mgr.create_user("keyuser", "pass")
    key = mgr.create_api_key("keyuser")
    assert key.startswith("pv-")
    result = mgr.validate_api_key(key)
    assert result is not None
    assert result["username"] == "keyuser"


def test_default_admin_created(tmp_path):
    from pixelle_video.services.auth import UserManager
    mgr = UserManager(data_dir=str(tmp_path / "test_auth4"))
    result = mgr.authenticate("admin", "admin123")
    assert result is not None
    assert result["role"] == "admin"
