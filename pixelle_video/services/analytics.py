# Copyright (C) 2025 AIDC-AI
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

"""Usage analytics and stats computation."""
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List


class AnalyticsService:
    def compute_summary(self, tasks: List[Dict]) -> Dict:
        total = len(tasks)
        if total == 0:
            return {"total_tasks": 0, "completed": 0, "failed": 0,
                    "success_rate": 0.0, "total_duration_seconds": 0.0,
                    "avg_duration_seconds": 0.0}
        completed = [t for t in tasks if t.get("status") == "completed"]
        failed = [t for t in tasks if t.get("status") == "failed"]
        total_dur = sum(t.get("duration", 0) or 0 for t in completed)
        return {
            "total_tasks": total,
            "completed": len(completed),
            "failed": len(failed),
            "success_rate": round(len(completed) / total * 100, 1),
            "total_duration_seconds": total_dur,
            "avg_duration_seconds": round(total_dur / len(completed), 1) if completed else 0,
        }

    def compute_daily_trends(self, tasks: List[Dict], days: int = 30) -> List[Dict]:
        now = datetime.now()
        daily = defaultdict(lambda: {"count": 0, "duration": 0.0})
        for t in tasks:
            try:
                created = datetime.fromisoformat(t.get("created_at", ""))
                if created >= now - timedelta(days=days):
                    key = created.strftime("%Y-%m-%d")
                    daily[key]["count"] += 1
                    daily[key]["duration"] += t.get("duration", 0) or 0
            except (ValueError, TypeError):
                continue
        result = []
        for i in range(days):
            date = (now - timedelta(days=days - 1 - i)).strftime("%Y-%m-%d")
            result.append({"date": date, **daily.get(date, {"count": 0, "duration": 0.0})})
        return result

    def compute_pipeline_stats(self, tasks: List[Dict]) -> List[Dict]:
        pipelines = defaultdict(lambda: {"count": 0, "duration": 0.0})
        for t in tasks:
            pipe = t.get("pipeline", "standard")
            pipelines[pipe]["count"] += 1
            if t.get("status") == "completed":
                pipelines[pipe]["duration"] += t.get("duration", 0) or 0
        return [{"pipeline": k, **v} for k, v in sorted(pipelines.items())]
