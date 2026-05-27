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

"""Video embed code generation"""
import uuid
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional


class EmbedService:
    def __init__(self, data_dir: str = "data"):
        self._data_dir = Path(data_dir)
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._embeds_file = self._data_dir / "embeds.json"

    def generate_embed_code(self, video_url: str, width: int = 640, height: int = 360,
                            autoplay: bool = False, controls: bool = True,
                            title: str = "") -> str:
        """Generate HTML iframe embed code."""
        autoplay_str = "autoplay=1&" if autoplay else ""

        html = f'''<iframe
  src="{video_url}?{autoplay_str}embed=1"
  width="{width}"
  height="{height}"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope"
  allowfullscreen
  title="{title or 'Pixelle-Video'}"
  style="border-radius: 8px; max-width: 100%;"
></iframe>'''
        return html.strip()

    def generate_share_link(self, task_id: str, video_url: str, base_url: str = "") -> dict:
        """Generate a shareable link with optional metadata."""
        share_id = uuid.uuid4().hex[:8]
        return {
            "share_id": share_id,
            "share_url": f"{base_url}/share/{share_id}",
            "embed_code": self.generate_embed_code(video_url, title=f"Pixelle-Video - {task_id[:8]}"),
            "task_id": task_id,
        }

    def generate_player_page(self, video_url: str, title: str = "Pixelle-Video") -> str:
        """Generate a standalone HTML player page."""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #000; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
video {{ max-width: 100%; max-height: 100vh; border-radius: 4px; }}
</style>
</head>
<body>
<video controls autoplay src="{video_url}"></video>
</body>
</html>'''
