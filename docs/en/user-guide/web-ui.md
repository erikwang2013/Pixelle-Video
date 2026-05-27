# Web UI Guide

Detailed introduction to the Pixelle-Video Web interface features.

---

## Interface Layout

The Web interface uses a three-column layout:

- **Left Panel**: Content input and audio settings
- **Middle Panel**: Voice and visual settings  
- **Right Panel**: Video generation and preview
- **Sidebar**: System configuration and FAQ

---

## System Configuration

First-time use requires configuring LLM and image generation services. See [Configuration Guide](../getting-started/configuration.md).

---

## Content Input

### Generation Mode

- **AI Generate Content**: Enter a topic, AI creates script automatically
- **Fixed Script Content**: Enter complete script directly

### Fixed Script Split Mode

When using fixed script mode, you can choose how to split the content:

- **By Paragraph**: Split by empty lines, each paragraph becomes a scene
- **By Line**: Split by line breaks, each line becomes a scene
- **By Sentence**: Smart sentence boundary detection, each sentence becomes a scene

### Background Music

- Built-in music supported
- Custom music files supported

---

## Voice Settings

### TTS Workflow

- Select TTS workflow
- Supports Edge-TTS, Index-TTS, etc.

### Reference Audio

- Upload reference audio for voice cloning
- Supports MP3/WAV/FLAC formats

---

## Visual Settings

### Image/Video Generation

- Select media generation workflow (image or video)
- Adjust prompt prefix to control style

### Video Template

- **Template Preview Gallery**: Visually preview all available templates
- Supports portrait (1080x1920) / landscape (1920x1080) / square (1080x1080)
- Template types:
  - `static_*.html`: Static templates (no AI-generated media)
  - `image_*.html`: Image templates (requires AI-generated images)
  - `video_*.html`: Video templates (requires AI-generated videos)

---

## Generate Video

After clicking "Generate Video", the system will:

1. Generate video script
2. Generate images/videos for each scene
3. Synthesize voice narration
4. Compose final video

Automatically previews when complete.

---

## Advanced Video Settings

In the sidebar below system configuration, expand "Advanced Video Settings":

- **Auto Subtitles**: Generate SRT subtitles and burn into video (top/bottom position)
- **Transition Effects**: Choose frame transition animation (none/crossfade/fade to black/slide left/zoom in)
- **Multi-Speaker TTS**: Alternate different voices per frame for dialogue effect

---
## Page Navigation

The Web UI includes multiple pages:

| Page | Function |
|------|----------|
| 🎬 Home | Video generation |
| 📚 History | Generation history |
| 🔗 URL-to-Video | Convert web articles to videos |
| 📊 Analytics | Usage statistics dashboard |
| ✂️ Editor | Video frame editor |
| ⚙️ Account | Settings and integrations |

---
## Analytics

The Analytics page provides:
- Summary cards: total tasks, success rate, total duration, avg duration
- Daily generation trend line chart
- Pipeline distribution bar chart

---
## Video Editor

The Editor page supports:
- Select completed tasks to edit
- Reorder frames by index
- Trim individual frame duration
- Regenerate single frames with new prompts
- Export tasks as ZIP packages (video, frames, metadata)

---
## Account Settings

The Account page has four tabs:
- **API Keys**: Create and manage API access keys
- **Webhooks**: Register callback URLs for task completion notifications
- **Schedules**: Create cron-based scheduled video generation
- **Social**: Configure social media publishing credentials (YouTube, Bilibili coming soon)

---
## FAQ

The sidebar includes built-in FAQ for quick reference:

- Common configuration issues
- Generation failure solutions
- Performance optimization tips

