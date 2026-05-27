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

"""Export analytics data as CSV or HTML report"""
import csv
import json
from pathlib import Path
from io import StringIO
from datetime import datetime
from typing import List, Dict


class AnalyticsExportService:
    def export_csv(self, tasks: List[Dict]) -> str:
        """Export task list as CSV string."""
        if not tasks:
            return "No data"

        output = StringIO()
        fieldnames = ["task_id", "title", "status", "pipeline", "duration", "created_at", "n_scenes"]
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()

        for t in tasks:
            row = {k: t.get(k, "") for k in fieldnames}
            writer.writerow(row)

        return output.getvalue()

    def export_html_report(self, tasks: List[Dict], summary: Dict) -> str:
        """Generate a simple HTML analytics report."""
        from pixelle_video.services.analytics import AnalyticsService
        svc = AnalyticsService()
        trends = svc.compute_daily_trends(tasks, days=7)

        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Pixelle-Video Analytics Report</title>
<style>
body {{ font-family: -apple-system, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
.card {{ background: #f5f5f5; border-radius: 8px; padding: 16px; margin: 8px 0; display: inline-block; min-width: 120px; text-align: center; }}
.card .value {{ font-size: 28px; font-weight: bold; color: #333; }}
.card .label {{ font-size: 12px; color: #666; }}
table {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
th {{ background: #f5f5f5; }}
</style></head><body>
<h1>Pixelle-Video Analytics Report</h1>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
<div>
<div class="card"><div class="value">{summary.get('total_tasks', 0)}</div><div class="label">Total Tasks</div></div>
<div class="card"><div class="value">{summary.get('success_rate', 0):.1f}%</div><div class="label">Success Rate</div></div>
<div class="card"><div class="value">{int(summary.get('total_duration_seconds', 0) // 60)}m</div><div class="label">Total Duration</div></div>
</div>
<h2>Recent Tasks</h2>
<table><tr><th>Title</th><th>Status</th><th>Duration</th><th>Date</th></tr>"""

        for t in tasks[:20]:
            status = t.get("status", "")
            emoji = {"completed": "✅", "failed": "❌"}.get(status, "⏳")
            html += f"<tr><td>{t.get('title', 'Untitled')}</td><td>{emoji} {status}</td><td>{t.get('duration', 0):.0f}s</td><td>{t.get('created_at', '')[:10]}</td></tr>"

        html += "</table></body></html>"
        return html
