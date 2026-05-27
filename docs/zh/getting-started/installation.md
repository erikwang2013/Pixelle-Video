# 安装指南

---

## 系统要求

| 要求 | 说明 |
|------|------|
| Python | 3.11+ |
| 操作系统 | Windows / macOS / Linux |
| FFmpeg | 视频合成必需 |
| 内存 | 4GB+ |
| 磁盘 | 2GB+ |

**可选：**
- NVIDIA GPU（6GB+ 显存）— 本地 ComfyUI 图像生成
- 网络连接 — LLM API 和云端服务调用

---

## 方式一：从源码安装

```bash
git clone https://github.com/AIDC-AI/Pixelle-Video.git
cd Pixelle-Video
```

### 安装 FFmpeg

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows: https://ffmpeg.org/download.html
```

### 安装依赖

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
```

或使用 pip：

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

### 安装 Playwright 浏览器

```bash
uv run playwright install chromium
```

---

## 方式二：Docker 部署

```bash
docker compose up -d
```

- Web UI: `http://localhost:8501`
- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

---

## 方式三：Windows 整合包

1. 从 [Releases](https://github.com/AIDC-AI/Pixelle-Video/releases/latest) 下载
2. 解压，双击 `start.bat`

---

## 验证安装

```bash
uv run streamlit run web/app.py
```

浏览器打开 `http://localhost:8501`，看到主页即安装成功。

---

## 配置

```bash
cp config.example.yaml config.yaml
```

编辑 `config.yaml`，填入 API 密钥：

```yaml
llm:
  api_key: "your-key"
  base_url: "https://api.openai.com/v1"
  model: "gpt-4o"

comfyui:
  runninghub_api_key: "your-rh-key"
```

---

## 可选：本地 ComfyUI

```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI && pip install -r requirements.txt
python main.py  # http://127.0.0.1:8188
```

---

## 下一步

- [快速开始](quick-start.md) — 生成第一个视频
- [配置说明](configuration.md) — 详细配置
