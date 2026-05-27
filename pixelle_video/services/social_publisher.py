"""Social media publishing service"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from loguru import logger


class SocialPublisher:
    PLATFORMS = ["youtube", "bilibili", "tiktok"]

    def __init__(self, data_dir: str = "data"):
        self._data_dir = Path(data_dir)
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._publish_history_file = self._data_dir / "publish_history.json"

    def list_platforms(self) -> List[str]:
        return self.PLATFORMS

    async def publish(self, platform: str, video_path: str, title: str,
                      description: str = "", tags: List[str] = None,
                      credentials: dict = None) -> dict:
        """Publish video to a social media platform.

        Currently returns a placeholder result. Real implementation requires
        platform-specific OAuth and API integration.
        """
        if platform not in self.PLATFORMS:
            raise ValueError(f"Unsupported platform: {platform}")

        if platform == "youtube":
            return await self._publish_youtube(video_path, title, description, tags, credentials)
        elif platform == "bilibili":
            return await self._publish_bilibili(video_path, title, description, credentials)
        else:
            return {"status": "not_implemented", "platform": platform, "message": f"{platform} publishing not yet implemented"}

    async def _publish_youtube(self, video_path: str, title: str, description: str,
                                tags: List[str], credentials: dict) -> dict:
        """YouTube upload placeholder.

        Full implementation requires:
        1. Google Cloud Project with YouTube Data API v3 enabled
        2. OAuth 2.0 credentials with youtube.upload scope
        3. google-api-python-client library

        See: https://developers.google.com/youtube/v3/docs/videos/insert
        """
        logger.info(f"YouTube publish requested: {title} ({video_path})")
        return {
            "platform": "youtube",
            "status": "not_configured",
            "message": "YouTube publishing requires OAuth credentials. Configure in Settings > Integrations.",
            "video_path": video_path,
            "title": title,
        }

    async def _publish_bilibili(self, video_path: str, title: str, description: str,
                                 credentials: dict) -> dict:
        """Bilibili upload placeholder.

        Full implementation requires:
        1. Bilibili developer account and API credentials
        2. bilibili-api-python library
        """
        logger.info(f"Bilibili publish requested: {title} ({video_path})")
        return {
            "platform": "bilibili",
            "status": "not_configured",
            "message": "Bilibili publishing requires API credentials. Configure in Settings > Integrations.",
            "video_path": video_path,
            "title": title,
        }

    def record_publish(self, platform: str, video_id: str, title: str, url: str = ""):
        history = []
        if self._publish_history_file.exists():
            history = json.loads(self._publish_history_file.read_text())
        history.append({
            "platform": platform,
            "video_id": video_id,
            "title": title,
            "url": url,
            "published_at": datetime.now().isoformat(),
        })
        self._publish_history_file.write_text(json.dumps(history, indent=2, ensure_ascii=False))

    def get_history(self) -> List[dict]:
        if self._publish_history_file.exists():
            return json.loads(self._publish_history_file.read_text())
        return []
