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

"""Tests for Phase G: SEO, Database, and Health Check features (G3)."""


# ---------------------------------------------------------------------------
# G3: SEO Metadata Generator
# ---------------------------------------------------------------------------

def test_seo_metadata():
    from pixelle_video.services.seo import SEOService

    svc = SEOService()
    meta = svc.generate_metadata("如何使用Python自动化视频制作", "本教程将介绍Python自动化...")
    assert meta["title"] == "如何使用Python自动化视频制作"
    assert "教程" in meta["tags"]


def test_seo_social_post():
    from pixelle_video.services.seo import SEOService

    svc = SEOService()
    post = svc.generate_social_post("AI视频制作", platform="weibo")
    assert "AI视频制作" in post


def test_seo_long_title_truncation():
    from pixelle_video.services.seo import SEOService

    svc = SEOService()
    long_topic = "这是一个非常非常长的标题" * 5
    meta = svc.generate_metadata(long_topic)
    assert len(meta["title"]) <= svc.MAX_TITLE_LENGTH


def test_seo_default_description():
    from pixelle_video.services.seo import SEOService

    svc = SEOService()
    meta = svc.generate_metadata("Test Topic")
    assert "AI-generated video about Test Topic" in meta["description"]


def test_seo_max_tags():
    from pixelle_video.services.seo import SEOService

    svc = SEOService()
    meta = svc.generate_metadata("tutorial how to guide review news recipe travel fitness finance ai")
    assert len(meta["tags"]) <= svc.MAX_TAGS
