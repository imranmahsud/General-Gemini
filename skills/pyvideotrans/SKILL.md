---
name: pyvideotrans
description: Local AI video translation, transcription, voice dubbing, and subtitle embedding pipeline using pyVideoTrans. Translates speech across languages, synthesizes localized audio, and syncs subtitles offline, replacing Rask.ai and HeyGen subscriptions.
---

# pyVideoTrans Video Dubbing & Translation Skill

This skill provides an automated local pipeline for translating video dialogue, generating synchronized multilingual subtitles, and dubbing speech using `pyVideoTrans` (Faster-Whisper, Edge-TTS/XTTS, and FFmpeg) without recurring cloud fees.

---

## 1. Running the System

The repository is maintained locally at:
`C:\tools\media-ai\pyvideotrans`

### 1.1 Launch Interactive Web GUI
```powershell
cd C:\tools\media-ai\pyvideotrans
uv run webui.py
```
Opens an interactive browser interface for drag-and-drop video processing, audio waveform preview, and subtitle editing.

---

## 2. CLI Command Workflows

All commands are executed inside `C:\tools\media-ai\pyvideotrans`:

### 2.1 Speech-to-Text Transcription (STT)
Extract and transcribe video speech into `.srt` subtitles:
```powershell
uv run cli.py --task stt --name "C:/videos/site_inspection.mp4" --recogn_type 0 --model_name base
```

### 2.2 Subtitle Translation (STS)
Translate existing `.srt` subtitle file into another language:
```powershell
# Translate Urdu/Chinese/etc to English (en)
uv run cli.py --task sts --name "C:/videos/site_inspection.srt" --target_language_code en
```

### 2.3 Text-to-Speech Dubbing (TTS)
Synthesize voiceover from subtitle file:
```powershell
uv run cli.py --task tts --name "C:/videos/site_inspection.srt" --tts_type 0 --voice_role "en-US-GuyNeural"
```

### 2.4 End-to-End Video Translation & Dubbing (VTV)
Full pipeline: transcribes, translates dialogue, replaces audio track with AI voice, and embeds subtitles:
```powershell
uv run cli.py --task vtv `
  --name "C:/videos/presentation.mp4" `
  --source_language_code ur `
  --target_language_code en `
  --voice_role "en-US-GuyNeural"
```
*(Add `--cuda` flag if running on an NVIDIA GPU for 10x faster execution).*

---

## 3. Supported Languages & Voice Engines

- **Languages**: English (`en`), Urdu (`ur`), Arabic (`ar`), Chinese (`zh-cn`), Spanish (`es`), French (`fr`), German (`de`), Hindi (`hi`), Pashto, etc.
- **Voice Engines**:
  - `edge-tts`: Microsoft Edge high-fidelity neural voices (100% free, fast, no GPU required).
  - `faster-whisper`: Optimized CTranslate2 implementation of OpenAI Whisper for sub-second audio transcription.
  - `XTTS / Coqui`: Zero-shot voice cloning from a 6-second speaker audio sample.

---

## 4. Key Benefits

1. **Replaces Rask.ai**: Avoids \$60 to \$150/month subscription plans.
2. **Field Video Localization**: Enables engineering teams to localize site walkthroughs, dam safety tutorials, and equipment operation videos for multi-lingual stakeholders.
3. **No Docker Requirement**: Runs directly via `uv` and Python on Windows with native FFmpeg integration.
