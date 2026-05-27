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

"""
Analytics Dashboard Page - Usage statistics and trend charts.
"""

import sys
from pathlib import Path

# Add project root to sys.path
_script_dir = Path(__file__).resolve().parent
_project_root = _script_dir.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import streamlit as st
from loguru import logger

from web.i18n import tr
from web.utils.async_helpers import run_async

# Page config
st.set_page_config(
    page_title="Analytics - Pixelle-Video",
    page_icon="📊",
    layout="wide",
)


def main():
    st.markdown(f"### 📊 {tr('analytics.title')}")

    try:
        from pixelle_video.services.persistence import PersistenceService
        from pixelle_video.services.analytics import AnalyticsService

        persistence = PersistenceService()
        tasks = run_async(persistence.list_tasks(limit=10000))

        if not tasks:
            st.info(tr("analytics.no_data"))
            return

        svc = AnalyticsService()
        summary = svc.compute_summary(tasks)
        trends = svc.compute_daily_trends(tasks, days=30)
        pipeline_stats = svc.compute_pipeline_stats(tasks)

        # Metric cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(tr("analytics.total_tasks"), summary["total_tasks"])
        with col2:
            st.metric(
                tr("analytics.success_rate"),
                f"{summary['success_rate']}%",
            )
        with col3:
            mins = int(summary["total_duration_seconds"] // 60)
            st.metric(tr("analytics.total_duration"), f"{mins} min")
        with col4:
            st.metric(
                tr("analytics.avg_duration"),
                f"{summary['avg_duration_seconds']:.0f}s",
            )

        # Trend chart
        st.markdown(f"**{tr('analytics.daily_trends')}**")
        chart_data = {}
        for t in trends:
            chart_data[t["date"]] = t["count"]
        st.line_chart(chart_data)

        # Pipeline distribution
        st.markdown(f"**{tr('analytics.pipeline_distribution')}**")
        pipe_data = {}
        for p in pipeline_stats:
            pipe_data[p["pipeline"]] = p["count"]
        st.bar_chart(pipe_data)

    except Exception as e:
        logger.error(f"Analytics page error: {e}")
        st.info(tr("analytics.no_data"))


if __name__ == "__main__":
    main()
else:
    main()
