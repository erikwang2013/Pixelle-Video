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

"""A/B testing — generate multiple video versions for comparison"""
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from loguru import logger


# Pre-built test variants for common dimensions
TEST_VARIANTS = {
    "style": [
        {"name_zh": "现代简约", "name_en": "Modern Minimal", "template": "1080x1920/image_modern.html", "prompt_prefix": "minimalist modern style"},
        {"name_zh": "霓虹科技", "name_en": "Neon Tech", "template": "1080x1920/image_neon.html", "prompt_prefix": "neon cyberpunk style"},
        {"name_zh": "优雅经典", "name_en": "Elegant Classic", "template": "1080x1920/image_elegant.html", "prompt_prefix": "elegant classic style"},
        {"name_zh": "卡通趣味", "name_en": "Cartoon Fun", "template": "1080x1920/image_cartoon.html", "prompt_prefix": "cute cartoon style"},
    ],
    "transition": [
        {"name_zh": "无转场", "name_en": "No Transition", "transition": "none"},
        {"name_zh": "交叉淡入淡出", "name_en": "Crossfade", "transition": "crossfade"},
        {"name_zh": "黑场过渡", "name_en": "Fade to Black", "transition": "fade_in_out"},
    ],
    "voice": [
        {"name_zh": "温柔女声", "name_en": "Gentle Female", "voice": "zh_CN_XiaoxiaoNeural"},
        {"name_zh": "专业男声", "name_en": "Professional Male", "voice": "zh_CN_YunjianNeural"},
        {"name_zh": "甜美女声", "name_en": "Sweet Female", "voice": "zh_CN_XiaoyiNeural"},
    ],
    "quality": [
        {"name_zh": "快速草稿", "name_en": "Fast Draft", "quality": "draft"},
        {"name_zh": "标准质量", "name_en": "Standard", "quality": "standard"},
        {"name_zh": "高清成品", "name_en": "High Quality", "quality": "high"},
    ],
    "subtitles": [
        {"name_zh": "有字幕", "name_en": "With Subtitles", "subtitles": True},
        {"name_zh": "无字幕", "name_en": "No Subtitles", "subtitles": False},
    ],
}


class ABTestingService:
    """Generate and manage A/B test video variants."""

    def __init__(self, data_dir: str = "data"):
        self._data_dir = Path(data_dir)
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._tests_file = self._data_dir / "ab_tests.json"

    def list_dimensions(self) -> Dict:
        """List available test dimensions and their variants."""
        return {k: [{"name_zh": v["name_zh"], "name_en": v["name_en"]} for v in variants]
                for k, variants in TEST_VARIANTS.items()}

    def get_variants(self, dimension: str) -> List[Dict]:
        """Get all variants for a dimension."""
        return TEST_VARIANTS.get(dimension, [])

    def create_test(self, topic: str, dimensions: List[str]) -> dict:
        """Create an A/B test plan for a topic across given dimensions.

        Args:
            topic: Video topic
            dimensions: List of dimension names to test, e.g. ["style", "transition"]

        Returns:
            Test plan with all variant combinations
        """
        test_id = uuid.uuid4().hex[:12]

        # Build variant grid
        variants = []
        for dim in dimensions:
            dim_variants = self.get_variants(dim)
            if not dim_variants:
                continue
            for v in dim_variants:
                base_params = {"text": topic, "mode": "generate"}
                # Apply variant params
                for key in ["template", "prompt_prefix", "transition", "subtitles", "quality"]:
                    if key in v:
                        base_params[key] = v[key]
                if "voice" in v:
                    base_params["tts_voice"] = v["voice"]

                variants.append({
                    "variant_id": uuid.uuid4().hex[:8],
                    "dimension": dim,
                    "variant_name": v.get("name_zh", v.get("name_en", "")),
                    "params": base_params,
                    "status": "pending",
                    "task_id": None,
                    "result": None,
                })

        test = {
            "test_id": test_id,
            "topic": topic,
            "dimensions": dimensions,
            "variants": variants,
            "created_at": datetime.now().isoformat(),
            "status": "planned",
        }

        self._save_test(test)
        logger.info(f"A/B test created: {test_id} ({len(variants)} variants)")
        return test

    def _save_test(self, test: dict):
        tests = self._load_tests()
        tests[test["test_id"]] = test
        self._tests_file.write_text(json.dumps(tests, indent=2, ensure_ascii=False))

    def _load_tests(self) -> dict:
        if self._tests_file.exists():
            return json.loads(self._tests_file.read_text())
        return {}

    def update_variant_status(self, test_id: str, variant_id: str, status: str, task_id: str = None, result: dict = None):
        tests = self._load_tests()
        test = tests.get(test_id)
        if not test:
            return False
        for v in test["variants"]:
            if v["variant_id"] == variant_id:
                v["status"] = status
                if task_id:
                    v["task_id"] = task_id
                if result:
                    v["result"] = result
                break
        self._save_test(test)
        return True

    def get_test(self, test_id: str) -> Optional[dict]:
        return self._load_tests().get(test_id)

    def list_tests(self) -> List[dict]:
        return list(self._load_tests().values())

    def get_comparison_report(self, test_id: str) -> dict:
        """Generate a comparison summary of all variants in a test."""
        test = self.get_test(test_id)
        if not test:
            return {"error": "Test not found"}

        variants = test["variants"]
        completed = [v for v in variants if v["status"] == "completed"]
        pending = [v for v in variants if v["status"] != "completed"]

        return {
            "test_id": test_id,
            "topic": test["topic"],
            "total_variants": len(variants),
            "completed": len(completed),
            "pending": len(pending),
            "variants": [
                {
                    "name": v["variant_name"],
                    "dimension": v["dimension"],
                    "status": v["status"],
                    "task_id": v["task_id"],
                    "duration": v.get("result", {}).get("duration", 0) if v.get("result") else None,
                }
                for v in variants
            ],
            "ready_for_comparison": len(completed) >= 2,
        }
