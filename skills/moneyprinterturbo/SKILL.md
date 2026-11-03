---
name: moneyprinterturbo
description: Automated short-form video generation pipeline using MoneyPrinterTurbo. Generates AI scripts (DeepSeek/Gemini/OpenAI), Edge-TTS voiceovers, synchronized subtitles, and dynamic vertical (9:16) video compositions.
---

# MoneyPrinterTurbo Skill

Use this skill to autonomously produce short-form vertical videos (YouTube Shorts, TikTok, Instagram Reels) and horizontal videos using the local MoneyPrinterTurbo installation at `D:\AI-Folders\MoneyPrinterTurbo`.

## Environment & Prerequisites
- **Location:** `D:\AI-Folders\MoneyPrinterTurbo`
- **Virtualenv & Package Manager:** Astral `uv` (Python 3.11)
- **Video Renderer:** FFmpeg (`C:\ProgramData\chocolatey\bin\ffmpeg.EXE` or system PATH)
- **Active LLM Provider:** DeepSeek (`deepseek-chat` via `config.toml`)
- **Default TTS:** Microsoft Edge TTS (`azure_tts_v1` / `en-US-ChristopherNeural`, `en-US-GuyNeural`, `en-US-JennyNeural` - zero cost, no key required)

## Common Commands

### 1. Launch the Web UI
```powershell
cd D:\AI-Folders\MoneyPrinterTurbo
.\webui.bat
# Accessible in browser at http://localhost:8501
```

### 2. Generate Video via CLI (Local Thematic Materials)
```powershell
cd D:\AI-Folders\MoneyPrinterTurbo
uv run python cli.py `
  --video-script "Your complete narration script text..." `
  --video-source local `
  --video-materials "materials/path/slide1.jpg,materials/path/slide2.jpg" `
  --voice-name "en-US-ChristopherNeural" `
  --image-motion zoom `
  --bgm-type random
```

### 3. Generate Video from a Topic Prompt (Autonomous Scripting via DeepSeek)
```powershell
cd D:\AI-Folders\MoneyPrinterTurbo
uv run python cli.py `
  --video-subject "Your topic here" `
  --video-source local `
  --video-materials "path/to/media1.jpg,path/to/media2.jpg" `
  --voice-name "en-US-GuyNeural" `
  --image-motion zoom `
  --bgm-type random
```

### 4. Output Location
Rendered videos are saved under:
- `D:\AI-Folders\MoneyPrinterTurbo\storage\tasks\<task-id>\final-1.mp4`
- Custom copies can be staged in `D:\AI-Folders\MoneyPrinterTurbo\outputs\`.
