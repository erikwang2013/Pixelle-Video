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
import json
from pathlib import Path


def test_manifest_exists():
    p = Path("web/static/manifest.json")
    assert p.exists()
    data = json.loads(p.read_text())
    assert data["name"] == "Pixelle-Video"
    assert "icons" in data


def test_sw_exists():
    p = Path("web/static/sw.js")
    assert p.exists()
    content = p.read_text()
    assert "serviceworker" in content.lower() or "fetch" in content


def test_icons_exist():
    assert Path("web/static/icon-192.png").exists()
    assert Path("web/static/icon-512.png").exists()
