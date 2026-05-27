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

"""Script template library for different video genres"""
from typing import Dict, List


SCRIPT_TEMPLATES = [
    {
        "id": "news",
        "name_zh": "新闻播报", "name_en": "News Report",
        "prompt_prefix": "以新闻播报风格撰写视频脚本",
        "style_hint": "客观、简洁、事实导向",
        "image_style": "clean news photography style, professional lighting",
        "preset_n_scenes": 5,
    },
    {
        "id": "tutorial",
        "name_zh": "教程教学", "name_en": "Tutorial",
        "prompt_prefix": "以分步骤教程风格撰写视频脚本",
        "style_hint": "清晰、循序渐进、可操作",
        "image_style": "clean flat illustration tutorial style, step-by-step visuals",
        "preset_n_scenes": 6,
    },
    {
        "id": "product_review",
        "name_zh": "产品测评", "name_en": "Product Review",
        "prompt_prefix": "以产品测评风格撰写视频脚本，包含优缺点分析",
        "style_hint": "客观评测、详细对比、购买建议",
        "image_style": "product photography on clean background, professional lighting",
        "preset_n_scenes": 5,
    },
    {
        "id": "storytelling",
        "name_zh": "故事叙述", "name_en": "Storytelling",
        "prompt_prefix": "以引人入胜的故事风格撰写视频脚本",
        "style_hint": "情感化、叙事性强、有起承转合",
        "image_style": "cinematic storytelling style, warm lighting, emotional atmosphere",
        "preset_n_scenes": 6,
    },
    {
        "id": "meditation",
        "name_zh": "冥想放松", "name_en": "Meditation",
        "prompt_prefix": "以冥想引导风格撰写视频脚本，语气平和舒缓",
        "style_hint": "柔和、舒缓、正念导向",
        "image_style": "peaceful nature scenes, soft colors, dreamy atmosphere",
        "preset_n_scenes": 4,
    },
    {
        "id": "tech_review",
        "name_zh": "科技数码", "name_en": "Tech Review",
        "prompt_prefix": "以科技测评风格撰写视频脚本",
        "style_hint": "参数详细、对比清晰、选购建议",
        "image_style": "futuristic tech style, dark background with neon accents",
        "preset_n_scenes": 5,
    },
    {
        "id": "recipe",
        "name_zh": "美食菜谱", "name_en": "Recipe",
        "prompt_prefix": "以美食菜谱风格撰写视频脚本，包含材料和步骤",
        "style_hint": "详细步骤、食材清单、烹饪技巧",
        "image_style": "appetizing food photography, warm kitchen lighting, overhead shots",
        "preset_n_scenes": 6,
    },
    {
        "id": "travel",
        "name_zh": "旅行游记", "name_en": "Travel Vlog",
        "prompt_prefix": "以旅行游记风格撰写视频脚本",
        "style_hint": "景点描述、文化体验、实用攻略",
        "image_style": "travel destination photography, natural lighting, wide landscapes",
        "preset_n_scenes": 5,
    },
    {
        "id": "fitness",
        "name_zh": "健身运动", "name_en": "Fitness",
        "prompt_prefix": "以健身指导风格撰写视频脚本",
        "style_hint": "动作讲解、组数次数、安全提示",
        "image_style": "athletic fitness photography, gym lighting, action shots",
        "preset_n_scenes": 5,
    },
    {
        "id": "finance",
        "name_zh": "财经理财", "name_en": "Finance",
        "prompt_prefix": "以财经分析风格撰写视频脚本",
        "style_hint": "数据驱动、理性分析、风险提示",
        "image_style": "professional business style, charts and data visualization, clean office",
        "preset_n_scenes": 5,
    },
]


class ScriptTemplateService:
    def list_templates(self) -> List[Dict]:
        return SCRIPT_TEMPLATES

    def get_template(self, template_id: str) -> Dict:
        for t in SCRIPT_TEMPLATES:
            if t["id"] == template_id:
                return t
        return {}

    def apply_template(self, template_id: str, topic: str) -> dict:
        """Apply template to topic, returning generation params."""
        t = self.get_template(template_id)
        if not t:
            return {"topic_prompt": topic}
        return {
            "topic_prompt": f"{t['prompt_prefix']}：{topic}。风格：{t['style_hint']}",
            "image_style": t["image_style"],
            "n_scenes": t["preset_n_scenes"],
            "template_id": template_id,
        }
