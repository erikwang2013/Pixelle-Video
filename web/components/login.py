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

"""Optional login gate for web UI"""
import streamlit as st

from web.i18n import tr


def check_login() -> bool:
    """Check if user is logged in. Returns True if auth disabled."""
    # Auth is optional - skip if not configured
    if not st.session_state.get("auth_enabled", False):
        return True

    if st.session_state.get("authenticated", False):
        return True

    with st.container():
        st.markdown(f"### {tr('auth.login_title')}")
        username = st.text_input(tr("auth.username"))
        password = st.text_input(tr("auth.password"), type="password")

        if st.button(tr("auth.login_button"), type="primary"):
            from pixelle_video.services.auth import UserManager
            mgr = UserManager()
            user = mgr.authenticate(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.current_user = user
                st.rerun()
            else:
                st.error(tr("auth.login_failed"))
        return False

    return False
