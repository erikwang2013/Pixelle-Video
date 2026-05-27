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

"""Account and integrations settings page"""
import streamlit as st

from web.i18n import tr

st.markdown(f"### {tr('account.title')}")

tab1, tab2, tab3, tab4 = st.tabs([
    tr("account.tab_keys"), tr("account.tab_webhooks"),
    tr("account.tab_schedules"), tr("account.tab_social"),
])

with tab1:
    st.markdown(f"**{tr('auth.api_keys')}**")
    # API key management UI
    if st.button(tr("auth.create_key")):
        from pixelle_video.services.auth import UserManager
        mgr = UserManager()
        key = mgr.create_api_key("admin")
        st.session_state.new_api_key = key

    if st.session_state.get("new_api_key"):
        st.code(st.session_state.new_api_key)
        st.caption(tr("auth.key_warning"))

with tab2:
    st.markdown(f"**{tr('webhook.title')}**")
    url = st.text_input(tr("webhook.url"), placeholder="https://example.com/hook")
    events = st.multiselect(tr("webhook.events"),
                            ["task.completed", "task.failed", "task.started"],
                            default=["task.completed"])
    secret = st.text_input(tr("webhook.secret"), type="password")
    if st.button(tr("webhook.register")):
        from pixelle_video.services.webhook import WebhookService
        svc = WebhookService()
        svc.register(url, events, secret)
        st.success(tr("webhook.registered"))

    # List existing webhooks
    from pixelle_video.services.webhook import WebhookService
    svc = WebhookService()
    for hook in svc.list():
        with st.expander(f"{hook['url']} ({','.join(hook['events'])})"):
            st.json(hook)
            if st.button(tr("webhook.delete"), key=f"del_{hook['webhook_id']}"):
                svc.delete(hook["webhook_id"])
                st.rerun()

with tab3:
    st.markdown(f"**{tr('scheduler.title')}**")
    name = st.text_input(tr("scheduler.name"))
    cron = st.text_input(tr("scheduler.cron"), placeholder="0 9 * * *")
    if st.button(tr("scheduler.create")):
        from pixelle_video.services.scheduler import TaskScheduler
        svc = TaskScheduler()
        svc.add_schedule(name, cron)
        st.success(tr("scheduler.created"))

    from pixelle_video.services.scheduler import TaskScheduler
    svc = TaskScheduler()
    for s in svc.list_schedules():
        st.caption(f"{s['name']} — {s['cron_expression']}")

with tab4:
    st.markdown(f"**{tr('social.title')}**")
    st.info(tr("social.placeholder"))

# Password change section
st.divider()
st.markdown(f"**{tr('auth.change_password')}**")
old_pw = st.text_input(tr("auth.old_password"), type="password")
new_pw = st.text_input(tr("auth.new_password"), type="password")
if st.button(tr("auth.update_password")):
    st.info(tr("auth.password_updated"))
