---
name: auto-subs
description: Local-first, on-device AI transcription and subtitle generation using Whisper, Moonshine, or Parakeet with speaker diarization. Exports SRT, VTT, and JSON subtitles with direct integrations for DaVinci Resolve, Premiere Pro, and After Effects.
---

# AutoSubs (Local On-Device Subtitling & Diarization)

AutoSubs runs headless local AI speech recognition, speaker diarization, and formatting without uploading data to cloud services.

- **Local Repository**: `C:\tools\auto-subs`
- **GitHub**: `https://github.com/tmoroney/auto-subs`

## CLI Usage

### 1. Basic Transcription
Generate plain text transcript to console:
```bash
autosubs <input_media> --model small
```

### 2. Export Subtitle Formats (SRT, VTT, JSON)
Specify format via flag or output file extension:
```bash
# Export SRT
autosubs video.mp4 -f srt -o captions.srt

# Export JSON with word-level timestamps
autosubs interview.mp4 -o transcript.json
```

### 3. Speaker Diarization
Label speaker turns automatically (up to 8 speakers with `sortformer` or >8 with `pyannote`):
```bash
autosubs podcast.mp4 --diarize --max-speakers 3 --lang en -o podcast.srt
```

### 4. Text Formatting & Density
Adjust subtitle line wrapping and cadence for video overlays:
```bash
# Custom characters per line (e.g. for vertical 9:16 mobile reels)
autosubs video.mp4 --density custom --max-lines 2 --max-chars-per-line 32 -o reels.srt

# Uppercase style with punctuation stripped
autosubs video.mp4 --text-case uppercase --remove-punctuation -o captions.srt
```

### 5. Translation to English
```bash
autosubs foreign_audio.mp3 --translate -o english.srt
```

## Supported Models
- **Whisper**: `tiny`, `base`, `small`, `medium`, `large-v3`
- **Parakeet** / **Moonshine**: High-speed on-device models
- Check available models:
  ```bash
  autosubs --list-models
  ```
