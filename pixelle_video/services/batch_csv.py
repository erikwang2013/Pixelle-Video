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

"""Batch CSV import for video generation"""
import csv
from pathlib import Path
from typing import Dict, List


class BatchCSVService:
    REQUIRED_COLUMNS = ["topic"]
    OPTIONAL_COLUMNS = ["title", "n_scenes", "template", "style", "subtitles"]

    def parse_csv(self, file_path: str) -> List[Dict]:
        """Parse CSV file into list of video generation params."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        tasks = []
        with open(file_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                task = {"text": row.get("topic", "").strip(), "mode": "generate"}
                if "title" in row and row["title"].strip():
                    task["title"] = row["title"].strip()
                if "n_scenes" in row and row["n_scenes"].strip():
                    task["n_scenes"] = int(row["n_scenes"])
                if "template" in row and row["template"].strip():
                    task["frame_template"] = row["template"].strip()
                if "subtitles" in row and row["subtitles"].strip().lower() == "true":
                    task["subtitles"] = True
                tasks.append(task)
        return tasks

    def validate_csv(self, file_path: str) -> tuple[bool, str]:
        """Validate CSV structure. Returns (is_valid, error_message)."""
        try:
            with open(file_path, newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                columns = reader.fieldnames or []
                if "topic" not in columns:
                    return False, "CSV must have a 'topic' column"
                count = sum(1 for _ in reader)
                if count == 0:
                    return False, "CSV contains no data rows"
                return True, f"{count} rows found"
        except Exception as e:
            return False, str(e)
