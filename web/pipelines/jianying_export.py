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

"""JianYing export pipeline for Streamlit UI."""

import streamlit as st

from web.i18n import tr


def render_jianying_export():
    """Render JianYing export section in the output area."""
    st.markdown(f"### ✂️ {tr('jianying.title')}")
    st.caption(tr("jianying.description"))

    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input(
            tr("jianying.project_name"),
            value="Pixelle-Video-Export",
            help=tr("jianying.project_name_help"),
        )
    with col2:
        jy_version = st.selectbox(
            tr("jianying.version"),
            options=["5.9", "6.0+"],
            index=0,
            help=tr("jianying.version_help"),
        )

    if st.button(tr("jianying.export_button"), type="primary", use_container_width=True):
        with st.spinner(tr("jianying.exporting")):
            try:
                from pixelle_video.services.jianying_export import JianYingExportService

                svc = JianYingExportService()

                # Get storyboard data from session
                frames = st.session_state.get("storyboard_frames", [])
                bgm = st.session_state.get("bgm_path", None)

                path = svc.export_storyboard(project_name, frames, bgm)

                st.success(tr("jianying.export_success"))
                st.code(path)
                st.info(tr("jianying.open_hint"))
            except Exception as e:
                st.error(f"{tr('jianying.export_failed')}: {e}")
