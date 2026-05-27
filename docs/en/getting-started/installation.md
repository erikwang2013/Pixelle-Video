# Installation Guide

---

## System Requirements

| Requirement | Notes |
|-------------|-------|
| Python | 3.11+ |
| OS | Windows / macOS / Linux |
| FFmpeg | Required for video composition |
| RAM | 4GB+ |
| Disk | 2GB+ |

**Optional:** NVIDIA GPU (6GB+ VRAM) for local ComfyUI

---

## Method 1: From Source

```bash
git clone https://github.com/AIDC-AI/Pixelle-Video.git
cd Pixelle-Video
```

### Install FFmpeg

```bash
# Ubuntu/Debian: sudo apt install ffmpeg
# macOS: brew install ffmpeg
# Windows: https://ffmpeg.org/download.html
```

### Install Dependencies

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
```

Or pip: `python -m venv .venv && source .venv/bin/activate && pip install -e .`

### Install Playwright

```bash
uv run playwright install chromium
```

---

## Method 2: Docker

```bash
docker compose up -d
```
Web UI: `http://localhost:8501` | API: `http://localhost:8000` | Swagger: `http://localhost:8000/docs`

---

## Method 3: Windows All-in-One

Download from [Releases](https://github.com/AIDC-AI/Pixelle-Video/releases/latest), extract, run `start.bat`.

---

## Verify

```bash
uv run streamlit run web/app.py
```

Open `http://localhost:8501`.

---

## Configuration

```bash
cp config.example.yaml config.yaml
```

```yaml
llm:
  api_key: "your-key"
  base_url: "https://api.openai.com/v1"
  model: "gpt-4o"
comfyui:
  runninghub_api_key: "your-rh-key"
```

---

## Optional: Local ComfyUI

```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI && pip install -r requirements.txt
python main.py  # http://127.0.0.1:8188
```

---

## Next

- [Quick Start](quick-start.md) — Create your first video
- [Configuration](configuration.md) — Detailed setup
