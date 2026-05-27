"""AI music generation service — Suno/Udio API integration"""
import json
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional
import httpx
from loguru import logger


MUSIC_STYLES = {
    "cinematic": {"name_zh": "电影感", "tags": "cinematic, orchestral, epic"},
    "lofi": {"name_zh": "轻松LoFi", "tags": "lofi, chill, study beats"},
    "electronic": {"name_zh": "电子", "tags": "electronic, synth, upbeat"},
    "acoustic": {"name_zh": "原声", "tags": "acoustic, folk, warm"},
    "jazz": {"name_zh": "爵士", "tags": "jazz, smooth, piano"},
    "rock": {"name_zh": "摇滚", "tags": "rock, energetic, guitar"},
    "ambient": {"name_zh": "氛围", "tags": "ambient, atmospheric, pad"},
    "hiphop": {"name_zh": "嘻哈", "tags": "hip hop, beats, groove"},
    "classical": {"name_zh": "古典", "tags": "classical, strings, elegant"},
    "corporate": {"name_zh": "商务", "tags": "corporate, motivational, clean"},
}


class AIMusicService:
    """Generate AI background music via external APIs."""

    def __init__(self, data_dir: str = "data"):
        self._data_dir = Path(data_dir)
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._output_dir = self._data_dir / "ai_music"
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def list_styles(self) -> Dict:
        return dict(MUSIC_STYLES)

    def recommend_style(self, topic: str, template_id: str = "") -> str:
        """Recommend a music style based on video topic/content."""
        text = f"{topic} {template_id}".lower()
        style_keywords = {
            "cinematic": ["cinematic", "movie", "epic", "trailer", "电影"],
            "ambient": ["ambient", "meditation", "sleep", "冥想", "睡眠"],
            "lofi": ["lofi", "chill", "study", "relax", "放松", "学习"],
            "electronic": ["electronic", "tech", "digital", "科技", "数码"],
            "acoustic": ["acoustic", "warm", "nature", "自然", "温暖"],
            "jazz": ["jazz", "smooth", "coffee", "咖啡", "优雅"],
            "corporate": ["business", "corporate", "finance", "商务", "财经"],
            "hiphop": ["hip hop", "beat", "urban", "街头", "潮流"],
            "classical": ["classical", "elegant", "orchestra", "古典", "优雅"],
        }
        for style, keywords in style_keywords.items():
            for kw in keywords:
                if kw in text:
                    return style
        return "lofi"  # default

    async def generate(self, style: str = "lofi", duration: int = 60,
                       title: str = "", instrumental: bool = True) -> Optional[Dict]:
        """Generate AI music. Currently generates a metadata record for manual API use.

        Returns dict with: style, duration, suggested_prompt, output_path, status.
        The actual API call (Suno/Udio) requires API keys configured separately.
        """
        if style not in MUSIC_STYLES:
            style = "lofi"

        style_info = MUSIC_STYLES[style]
        track_id = uuid.uuid4().hex[:12]

        # Build generation prompt for external API
        prompt = f"{style_info['tags']}, {duration}s, instrumental" if instrumental else style_info['tags']
        if title:
            prompt = f"{title} - {prompt}"

        result = {
            "track_id": track_id,
            "style": style,
            "style_name": style_info["name_zh"],
            "duration": duration,
            "prompt": prompt,
            "instrumental": instrumental,
            "title": title or f"AI Music - {style_info['name_zh']}",
            "status": "prompt_ready",
            "suno_url": f"https://suno.com/create?prompt={prompt.replace(' ', '+')}",
            "udio_url": f"https://www.udio.com/create?prompt={prompt.replace(' ', '+')}",
            "output_path": str(self._output_dir / f"{track_id}.mp3"),
        }

        # Save metadata
        meta_path = self._output_dir / f"{track_id}.json"
        meta_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))

        logger.info(f"AI music prompt generated: {style} ({duration}s)")
        return result

    def get_history(self) -> List[Dict]:
        """List generated music metadata."""
        history = []
        for f in sorted(self._output_dir.glob("*.json"), reverse=True):
            try:
                history.append(json.loads(f.read_text()))
            except Exception:
                continue
        return history

    def delete_track(self, track_id: str) -> bool:
        """Delete a generated track and its metadata."""
        meta = self._output_dir / f"{track_id}.json"
        audio = self._output_dir / f"{track_id}.mp3"
        deleted = False
        for p in [meta, audio]:
            if p.exists():
                p.unlink()
                deleted = True
        return deleted
