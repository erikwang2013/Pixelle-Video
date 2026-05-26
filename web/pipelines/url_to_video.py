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

"""URL-to-Video pipeline for Streamlit UI"""
import asyncio
import streamlit as st
from web.i18n import tr


def render_url_to_video():
    """Render URL-to-Video page content."""
    st.markdown(f"### {tr('pipeline.url_to_video.name')}")
    st.caption(tr("pipeline.url_to_video.description"))

    url = st.text_input(
        tr("url_to_video.url"),
        placeholder="https://example.com/article",
        help=tr("url_to_video.url_help"),
        key="url_input",
    )

    if url and st.button(tr("url_to_video.fetch"), key="fetch_url_btn"):
        with st.spinner(tr("url_to_video.fetching")):
            try:
                from pixelle_video.services.url_fetcher import URLFetcher
                fetcher = URLFetcher()
                result = asyncio.run(fetcher.fetch_and_summarize(url))
                st.session_state.url_summary = result["summary"]
                st.session_state.url_title = result["title"]
                st.success(tr("url_to_video.fetch_success"))
            except Exception as e:
                st.error(f"{tr('url_to_video.fetch_error')}: {e}")

    if st.session_state.get("url_summary"):
        st.text_area(
            tr("url_to_video.summary"),
            value=st.session_state.url_summary,
            height=200,
        )
        if st.button(tr("btn.generate"), type="primary", use_container_width=True, key="url_generate_btn"):
            st.session_state.input_text = st.session_state.url_summary
            st.session_state.subtitles_enabled = True
            st.switch_page("pages/1_🎬_Home.py")
