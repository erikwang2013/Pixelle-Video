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

"""Task scheduling service for automated video generation"""
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from loguru import logger


@dataclass
class Schedule:
    schedule_id: str
    name: str
    cron_expression: str
    pipeline: str = "standard"
    params: dict = field(default_factory=dict)
    enabled: bool = True
    created_at: str = ""
    last_run: Optional[str] = None
    next_run: Optional[str] = None


class TaskScheduler:
    def __init__(self, data_dir: str = "data"):
        self._data_dir = Path(data_dir)
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._schedules_file = self._data_dir / "schedules.json"
        self._schedules: Dict[str, dict] = {}
        self._load()

    def _load(self):
        if self._schedules_file.exists():
            self._schedules = json.loads(self._schedules_file.read_text())

    def _save(self):
        self._schedules_file.write_text(json.dumps(self._schedules, indent=2, ensure_ascii=False))

    def _parse_cron(self, expression: str) -> Optional[dict]:
        """Parse a 5-field cron expression into components."""
        parts = expression.strip().split()
        if len(parts) != 5:
            return None
        return {"minute": parts[0], "hour": parts[1], "day": parts[2], "month": parts[3], "dow": parts[4]}

    def _next_cron_run(self, expression: str) -> Optional[datetime]:
        """Calculate next run time from cron expression."""
        from croniter import croniter
        try:
            return croniter(expression, datetime.now()).get_next(datetime)
        except ImportError:
            logger.warning("croniter not installed, cannot compute next run")
            return None
        except Exception:
            return None

    def add_schedule(self, name: str, cron_expression: str, pipeline: str = "standard", params: dict = None) -> dict:
        parsed = self._parse_cron(cron_expression)
        if not parsed:
            raise ValueError(f"Invalid cron expression: {cron_expression}")

        schedule = {
            "schedule_id": uuid.uuid4().hex[:12],
            "name": name,
            "cron_expression": cron_expression,
            "pipeline": pipeline,
            "params": params or {},
            "enabled": True,
            "created_at": datetime.now().isoformat(),
            "last_run": None,
            "next_run": None,
        }

        try:
            next_run = self._next_cron_run(cron_expression)
            if next_run:
                schedule["next_run"] = next_run.isoformat()
        except Exception:
            pass

        self._schedules[schedule["schedule_id"]] = schedule
        self._save()
        logger.info(f"Schedule added: {name} ({cron_expression})")
        return schedule

    def remove_schedule(self, schedule_id: str) -> bool:
        if schedule_id in self._schedules:
            del self._schedules[schedule_id]
            self._save()
            return True
        return False

    def list_schedules(self) -> List[dict]:
        return list(self._schedules.values())

    def get_due_schedules(self) -> List[dict]:
        """Get all enabled schedules that are due to run."""
        now = datetime.now()
        due = []
        for s in self._schedules.values():
            if not s["enabled"]:
                continue
            try:
                next_run = self._next_cron_run(s["cron_expression"])
                if next_run and next_run <= now:
                    due.append(s)
            except Exception:
                continue
        return due

    def mark_run(self, schedule_id: str):
        if schedule_id in self._schedules:
            self._schedules[schedule_id]["last_run"] = datetime.now().isoformat()
            next_run = self._next_cron_run(self._schedules[schedule_id]["cron_expression"])
            self._schedules[schedule_id]["next_run"] = next_run.isoformat() if next_run else None
            self._save()
