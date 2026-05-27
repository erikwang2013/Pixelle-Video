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

"""URL content extraction and summarization service"""

import re
from typing import Dict
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from loguru import logger


class URLFetcher:
    """Fetch article content from URLs and summarize for video generation."""

    def __init__(self, llm_service=None):
        self._llm = llm_service
        self._client = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=30.0,
                follow_redirects=True,
                headers={"User-Agent": "Pixelle-Video/1.0"},
            )
        return self._client

    def _is_valid_url(self, url: str) -> bool:
        """Check if a URL is valid (http/https scheme with network location)."""
        try:
            result = urlparse(url)
            return all([result.scheme in ("http", "https"), result.netloc])
        except Exception:
            return False

    async def fetch_and_summarize(
        self, url: str, target_scenes: int = 5
    ) -> Dict[str, str]:
        """Fetch URL content and return summarized text suitable for video.

        Args:
            url: Web page URL to fetch
            target_scenes: Target number of scenes for the video

        Returns:
            {"title": str, "summary": str, "full_text": str}

        Raises:
            ValueError: If URL is invalid or content is insufficient
        """
        if not self._is_valid_url(url):
            raise ValueError(f"Invalid URL: {url}")

        client = await self._get_client()
        response = await client.get(url)
        response.raise_for_status()
        html = response.text

        text = self.extract_article_text(html)
        title = self._extract_title(html)

        if not text or len(text) < 50:
            raise ValueError(f"Insufficient content extracted from {url}")

        if self._llm:
            summary = await self._summarize_with_llm(text, target_scenes)
        else:
            sentences = re.split(r'[。.!?]', text)
            summary = '。'.join(sentences[:target_scenes * 3]) + '。'

        logger.info(f"URL content extracted: {len(text)} chars from {url}")
        return {"title": title, "summary": summary, "full_text": text}

    def extract_article_text(self, html: str) -> str:
        """Extract main article text from HTML using readability heuristics."""
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        selectors = [
            "article",
            "[role='main']",
            "main",
            ".article-content",
            ".post-content",
            ".entry-content",
            ".article",
            ".post",
            "#content",
            ".content",
        ]
        for selector in selectors:
            article = soup.select_one(selector)
            if article:
                return article.get_text(separator="\n", strip=True)

        body = soup.find("body")
        return body.get_text(separator="\n", strip=True) if body else ""

    def _extract_title(self, html: str) -> str:
        """Extract page title from HTML."""
        soup = BeautifulSoup(html, "html.parser")
        if soup.title:
            return soup.title.get_text(strip=True)
        h1 = soup.find("h1")
        return h1.get_text(strip=True) if h1 else "Untitled"

    async def _summarize_with_llm(self, text: str, target_scenes: int) -> str:
        """Use LLM to summarize article text into video script format."""
        prompt = (
            f"Summarize the following article into {target_scenes} key points, "
            f"each as a short narration paragraph suitable for a short video. "
            f"Keep each point concise (1-2 sentences).\n\n"
            f"Article:\n{text[:4000]}"
        )
        try:
            return await self._llm.chat(prompt)
        except Exception as e:
            logger.warning(f"LLM summarization failed: {e}, using truncation")
            return text[:2000]
