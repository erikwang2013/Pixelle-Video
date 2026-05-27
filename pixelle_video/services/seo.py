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

"""AI-powered SEO metadata generation for videos"""

from typing import Dict, List


class SEOService:
    """Generate SEO-optimized metadata for video content.

    Provides title truncation, description generation, tag extraction,
    and social media post templates for multiple platforms.
    """

    MAX_TITLE_LENGTH = 60
    MAX_DESC_LENGTH = 160
    MAX_TAGS = 10

    DEFAULT_TAGS = [
        "AI视频", "短视频", "人工智能", "视频创作", "AI工具",
        "Pixelle-Video", "自动化", "内容创作", "视频制作",
    ]

    def generate_metadata(
        self, topic: str, narration: str = "", category: str = "general"
    ) -> Dict:
        """Generate SEO-optimized title, description, and tags.

        Args:
            topic: The video topic or main subject.
            narration: Optional narration text for description extraction.
            category: Content category label.

        Returns:
            Dict with title, description, tags, and category.
        """
        # Generate title (truncate topic to max length)
        title = topic.strip()
        if len(title) > self.MAX_TITLE_LENGTH:
            title = title[:self.MAX_TITLE_LENGTH - 3] + "..."

        # Generate description from narration
        if narration:
            desc = narration.strip()[:self.MAX_DESC_LENGTH]
            if len(narration) > self.MAX_DESC_LENGTH:
                desc += "..."
        else:
            desc = f"AI-generated video about {topic}. Created with Pixelle-Video."

        # Generate tags
        tags = self._extract_tags(topic, narration)

        return {
            "title": title,
            "description": desc,
            "tags": tags,
            "category": category,
        }

    def _extract_tags(self, topic: str, narration: str) -> List[str]:
        """Extract relevant tags from topic and narration text.

        Matches keywords in the combined text against a keyword-to-tag
        mapping and fills remaining slots with default tags.

        Args:
            topic: The video topic.
            narration: Optional narration text.

        Returns:
            List of tag strings, up to MAX_TAGS.
        """
        text = f"{topic} {narration}".lower()
        tags: List[str] = []

        keyword_map = {
            "tutorial": "教程", "how": "教程", "guide": "教程", "教程": "教程",
            "review": "测评", "测评": "测评", "评测": "测评",
            "news": "新闻", "新闻": "新闻", "科技": "科技",
            "recipe": "美食", "美食": "美食", "food": "美食",
            "travel": "旅行", "旅行": "旅行", "旅游": "旅行",
            "fitness": "健身", "健身": "健身", "运动": "健身",
            "finance": "理财", "理财": "理财", "投资": "理财",
            "ai": "AI", "artificial intelligence": "AI", "人工智能": "AI",
        }

        for keyword, tag in keyword_map.items():
            if keyword in text and tag not in tags:
                tags.append(tag)

        tags.extend(self.DEFAULT_TAGS[:self.MAX_TAGS - len(tags)])
        return tags[:self.MAX_TAGS]

    def generate_social_post(
        self, title: str, video_url: str = "", platform: str = "twitter"
    ) -> str:
        """Generate social media post text for video promotion.

        Args:
            title: The video title.
            video_url: Optional video URL to include.
            platform: Target platform ('twitter', 'weibo', 'linkedin').

        Returns:
            Formatted post text for the specified platform.
        """
        templates = {
            "twitter": (
                f"🎬 {title}\n\n"
                f"#PixelleVideo #AI #{' #'.join(self.DEFAULT_TAGS[2:5])}"
            ),
            "weibo": (
                f"【{title}】AI全自动生成！"
                f"使用Pixelle-Video一键创作短视频 🎬\n\n"
                f"#AI视频# #短视频创作#"
            ),
            "linkedin": (
                f"📹 {title}\n\n"
                f"Created with Pixelle-Video — AI-powered video creation.\n\n"
                f"#AI #VideoCreation #ContentCreation"
            ),
        }
        return templates.get(platform, templates["twitter"])
