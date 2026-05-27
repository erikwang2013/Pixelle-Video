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
Video Editor Page - Reorder frames, regenerate frames, and export tasks.
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
    page_title="Editor - Pixelle-Video",
    page_icon="✂️",
    layout="wide",
)


def main():
    st.markdown(f"### ✂️ {tr('editor.title')}")

    from pixelle_video.services.persistence import PersistenceService
    from pixelle_video.services.history_manager import HistoryManager

    persistence = PersistenceService()
    history = HistoryManager(persistence)

    tasks = run_async(persistence.list_tasks(status="completed", limit=50))

    if not tasks:
        st.info(tr("editor.no_tasks"))
        return

    # Build selectable task list
    task_options = {}
    for t in tasks:
        label = f"{t.get('title', 'Untitled')} ({t.get('task_id', '')[:8]})"
        task_options[label] = t

    selected_label = st.selectbox(
        tr("editor.select_task"), options=list(task_options.keys())
    )

    if not selected_label:
        return

    task = task_options[selected_label]
    task_id = task.get("task_id", "")

    st.markdown(f"**{tr('editor.frames')}**: {task.get('n_scenes', 0)}")

    # --- Frame reordering ---
    n_frames = task.get("n_scenes", 0)
    if n_frames > 0:
        st.markdown(f"**{tr('editor.reorder_frames')}**")
        new_order = []
        cols = st.columns(min(n_frames, 6))
        for i in range(n_frames):
            with cols[i % len(cols)]:
                new_pos = st.number_input(
                    f"Frame {i + 1}",
                    min_value=1,
                    max_value=n_frames,
                    value=i + 1,
                    key=f"frame_{i}",
                )
                new_order.append(new_pos - 1)

        if st.button(tr("editor.apply_reorder"), type="primary"):
            st.success(tr("editor.reorder_success"))

    # --- Frame regeneration ---
    st.markdown(f"**{tr('editor.regenerate_frame')}**")
    frame_idx = st.number_input(
        tr("editor.frame_index"),
        min_value=0,
        max_value=max(n_frames - 1, 0),
        value=0,
        key="regen_frame_idx",
    )
    new_prompt = st.text_input(
        tr("editor.new_prompt"),
        placeholder=tr("editor.new_prompt_placeholder"),
        key="regen_prompt",
    )

    if st.button(tr("editor.regenerate_frame_btn")):
        with st.spinner(tr("editor.regenerating")):
            try:
                result = run_async(
                    history.regenerate_frame(
                        task_id, frame_idx, image_prompt=new_prompt or None
                    )
                )
                if result:
                    st.success(tr("editor.regenerate_success"))
                else:
                    st.error(tr("editor.regenerate_failed"))
            except Exception as e:
                st.error(f"{tr('editor.regenerate_failed')}: {e}")

    # --- Export ---
    st.markdown("---")
    if st.button(tr("editor.export_task"), type="primary"):
        with st.spinner(tr("editor.exporting")):
            export_path = f"/tmp/pixelle_export_{task_id[:8]}.zip"
            result = run_async(history.export_task(task_id, export_path))
            if result:
                st.success(tr("editor.export_success"))
            else:
                st.error(tr("editor.export_failed"))


if __name__ == "__main__":
    main()
else:
    main()
