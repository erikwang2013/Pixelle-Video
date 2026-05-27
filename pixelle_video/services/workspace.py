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

"""Team workspaces for shared resources"""
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from loguru import logger


class WorkspaceService:
    def __init__(self, data_dir: str = "data"):
        self._data_dir = Path(data_dir)
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._workspaces_file = self._data_dir / "workspaces.json"
        self._workspaces: Dict[str, dict] = {}
        self._load()
        self._ensure_default()

    def _load(self):
        if self._workspaces_file.exists():
            self._workspaces = json.loads(self._workspaces_file.read_text())

    def _save(self):
        self._workspaces_file.write_text(json.dumps(self._workspaces, indent=2, ensure_ascii=False))

    def _ensure_default(self):
        if not self._workspaces:
            self.create_workspace("Default Workspace", "admin")

    def create_workspace(self, name: str, owner: str) -> dict:
        ws = {
            "workspace_id": uuid.uuid4().hex[:12],
            "name": name,
            "owner": owner,
            "members": [owner],
            "invite_code": uuid.uuid4().hex[:8].upper(),
            "shared_config": {},
            "shared_bgm": [],
            "created_at": datetime.now().isoformat(),
        }
        self._workspaces[ws["workspace_id"]] = ws
        self._save()
        return ws

    def list_workspaces(self, user: str = None) -> List[dict]:
        if user:
            return [w for w in self._workspaces.values() if user in w.get("members", [])]
        return list(self._workspaces.values())

    def get_workspace(self, workspace_id: str) -> Optional[dict]:
        return self._workspaces.get(workspace_id)

    def join_by_invite(self, invite_code: str, username: str) -> Optional[dict]:
        for ws in self._workspaces.values():
            if ws.get("invite_code") == invite_code:
                if username not in ws["members"]:
                    ws["members"].append(username)
                    self._save()
                return ws
        return None

    def leave_workspace(self, workspace_id: str, username: str) -> bool:
        ws = self._workspaces.get(workspace_id)
        if ws and username in ws.get("members", []):
            ws["members"].remove(username)
            self._save()
            return True
        return False
