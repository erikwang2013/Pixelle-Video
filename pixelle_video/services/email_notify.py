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

"""Email notification service with SMTP"""
import json
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from loguru import logger


class EmailNotifyService:
    def __init__(self, data_dir: str = "data"):
        self._data_dir = Path(data_dir)
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._config_file = self._data_dir / "email_config.json"
        self._config = self._load_config()

    def _load_config(self) -> dict:
        if self._config_file.exists():
            return json.loads(self._config_file.read_text())
        return {
            "enabled": False,
            "smtp_host": "",
            "smtp_port": 587,
            "username": "",
            "password": "",
            "from_addr": "",
            "to_addr": "",
        }

    def _save_config(self):
        self._config_file.write_text(
            json.dumps(self._config, indent=2, ensure_ascii=False)
        )

    def is_enabled(self) -> bool:
        return self._config.get("enabled", False)

    def toggle(self, enabled: bool):
        self._config["enabled"] = enabled
        self._save_config()

    def configure(
        self,
        smtp_host: str,
        smtp_port: int,
        username: str,
        password: str,
        from_addr: str,
        to_addr: str,
    ):
        self._config.update(
            {
                "smtp_host": smtp_host,
                "smtp_port": smtp_port,
                "username": username,
                "password": password,
                "from_addr": from_addr,
                "to_addr": to_addr,
            }
        )
        self._save_config()

    def get_config(self) -> dict:
        return dict(self._config)

    async def send(self, subject: str, body: str) -> bool:
        """Send email notification. Returns True if sent successfully."""
        if not self.is_enabled():
            logger.debug("Email notifications disabled, skipping")
            return False

        config = self._config
        if not config.get("smtp_host") or not config.get("to_addr"):
            logger.warning("Email not configured")
            return False

        msg = MIMEMultipart()
        msg["From"] = config["from_addr"] or config["username"]
        msg["To"] = config["to_addr"]
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html" if "<" in body else "plain", "utf-8"))

        try:
            server = smtplib.SMTP(
                config["smtp_host"], config["smtp_port"], timeout=10
            )
            server.starttls()
            server.login(config["username"], config["password"])
            server.send_message(msg)
            server.quit()
            logger.info(f"Email sent: {subject}")
            return True
        except Exception as e:
            logger.error(f"Email send failed: {e}")
            return False

    async def notify_task_completed(
        self,
        task_id: str,
        title: str = "",
        duration: float = 0,
        video_url: str = "",
    ):
        """Send notification when a video task completes."""
        subject = f"[Pixelle-Video] Video Complete: {title or task_id[:8]}"
        body = f"""
        <h2>Video Generation Complete</h2>
        <p><b>Task:</b> {task_id[:12]}</p>
        <p><b>Title:</b> {title or 'Untitled'}</p>
        <p><b>Duration:</b> {duration:.1f}s</p>
        {f'<p><b>Video:</b> <a href="{video_url}">{video_url}</a></p>' if video_url else ''}
        <hr><p><small>Sent by Pixelle-Video</small></p>
        """
        return await self.send(subject, body)
