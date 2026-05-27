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

"""User authentication and API key management"""
import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class User:
    user_id: str
    username: str
    password_hash: str
    role: str = "user"
    api_keys: List[Dict] = field(default_factory=list)
    created_at: str = ""


class UserManager:
    def __init__(self, data_dir: str = "data"):
        self._data_dir = Path(data_dir)
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._users_file = self._data_dir / "users.json"
        self._users: Dict[str, dict] = {}
        self._load()
        self._ensure_default_admin()

    def _load(self):
        if self._users_file.exists():
            self._users = json.loads(self._users_file.read_text())

    def _save(self):
        self._users_file.write_text(json.dumps(self._users, indent=2, ensure_ascii=False))

    def _hash_password(self, password: str) -> str:
        salt = uuid.uuid4().hex[:16]
        return salt + ":" + hashlib.sha256(f"{salt}{password}".encode()).hexdigest()

    def _verify_password(self, password: str, hash_str: str) -> bool:
        try:
            salt, h = hash_str.split(":", 1)
            return hashlib.sha256(f"{salt}{password}".encode()).hexdigest() == h
        except Exception:
            return False

    def _ensure_default_admin(self):
        if not self._users:
            self.create_user("admin", "admin123", role="admin")

    def create_user(self, username: str, password: str, role: str = "user") -> dict:
        if username in self._users:
            raise ValueError(f"User {username} already exists")
        user = {
            "user_id": uuid.uuid4().hex[:12],
            "username": username,
            "password_hash": self._hash_password(password),
            "role": role,
            "api_keys": [],
            "created_at": datetime.now().isoformat(),
        }
        self._users[username] = user
        self._save()
        return {k: v for k, v in user.items() if k != "password_hash"}

    def authenticate(self, username: str, password: str) -> Optional[dict]:
        user = self._users.get(username)
        if user and self._verify_password(password, user["password_hash"]):
            return {k: v for k, v in user.items() if k != "password_hash"}
        return None

    def create_api_key(self, username: str) -> str:
        user = self._users.get(username)
        if not user:
            raise ValueError(f"User {username} not found")
        key = f"pv-{uuid.uuid4().hex}"
        user["api_keys"].append({
            "key_id": uuid.uuid4().hex[:8],
            "key_prefix": key[:12],
            "key_hash": hashlib.sha256(key.encode()).hexdigest(),
            "created_at": datetime.now().isoformat(),
        })
        self._save()
        return key  # Return full key only once

    def validate_api_key(self, api_key: str) -> Optional[dict]:
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        for username, user in self._users.items():
            for k in user.get("api_keys", []):
                if k.get("key_hash") == key_hash:
                    return {"username": username, "role": user["role"], "user_id": user["user_id"]}
        return None

    def list_api_keys(self, username: str) -> list:
        user = self._users.get(username)
        if not user:
            return []
        return [{"key_id": k["key_id"], "key_prefix": k["key_prefix"], "created_at": k["created_at"]} for k in user.get("api_keys", [])]

    def revoke_api_key(self, username: str, key_id: str) -> bool:
        user = self._users.get(username)
        if not user:
            return False
        before = len(user["api_keys"])
        user["api_keys"] = [k for k in user["api_keys"] if k["key_id"] != key_id]
        if len(user["api_keys"]) != before:
            self._save()
            return True
        return False
