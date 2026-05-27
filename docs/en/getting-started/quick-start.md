# Usage Guide

---

## Launch

```bash
uv run streamlit run web/app.py
# Or: uv run uvicorn api.app:app --host 0.0.0.0 --port 8000
```

---

## Pages

| Page | Function |
|------|----------|
| 🎬 Home | Video generation — choose pipeline, configure, generate |
| 📚 History | View/download/duplicate/delete past videos |
| 🔗 URL-to-Video | Paste URL, AI extracts and creates video |
| 📊 Analytics | Usage stats dashboard |
| ✂️ Editor | Frame reorder, trim, replace, ZIP export |
| ⚙️ Account | API keys, webhooks, schedules, social |

---

## Pipelines

| Pipeline | How it works |
|----------|-------------|
| Quick Create | Enter topic → AI generates everything |
| Custom Media | Upload photos/videos → AI analyzes and creates |
| Digital Human | Avatar + product → AI talking-head video |
| Image-to-Video | First frame + prompt → dynamic video |
| Motion Transfer | Reference video + image → motion transfer |

---

## Advanced Features

**Subtitles** — Sidebar → Advanced → enable Auto Subtitles (top/bottom).

**Transitions** — Crossfade / Fade to Black / Slide / Zoom.

**Multi-Speaker TTS** — Alternate voices per frame.

**Batch Generation** — Multiple topics, one click.

**URL to Video** — Paste article URL → AI extracts and generates.

**Video Editor** — Reorder frames, trim, regenerate single frame, export ZIP.

**Script Templates** — 10 presets: News/Tutorial/Review/Storytelling/Meditation/Tech/Recipe/Travel/Fitness/Finance.

**AI Music** — 10 genres with smart style recommendation.

**A/B Testing** — Multi-variant comparison: style/voice/transition/quality/subtitles.

---

## API Usage

```bash
# Sync
curl -X POST http://localhost:8000/api/video/generate/sync \
  -H "Content-Type: application/json" \
  -d '{"text": "How to be productive", "mode": "generate"}'

# Async + WebSocket progress
curl -X POST http://localhost:8000/api/video/generate/async \
  -d '{"text": "Future of AI", "mode": "generate"}'
# → ws://localhost:8000/api/ws/progress/{task_id}
```

---

## JianYing/CapCut Export

Generate → "Export to JianYing" → open CapCut Pro → find in Drafts.

---

## Docker

```bash
docker compose up -d
```

---

## FAQ

See sidebar FAQ or [FAQ page](../faq.md).
