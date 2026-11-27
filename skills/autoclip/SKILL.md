---
name: autoclip
description: Open-source, local-first AI video clipper and repurposing engine. Ingests long videos, transcribes them, extracts viral hooks with LLMs, reframes to 9:16 vertical with speaker tracking, burns animated captions (karaoke/bold_pop), and exports platform-ready clips.
---

# AutoClip (Local-First AI Video Clipper)

AutoClip takes long-form videos (podcasts, lectures, interviews), transcribes them, identifies high-scoring moments via LLMs, reframes them to 9:16 vertical with facial/speaker tracking, burns in animated captions, and exports platform-ready MP4s.

- **Local Repository**: `C:\tools\autoclip`
- **GitHub**: `https://github.com/artbyjazi/autoclip`

## Prerequisites
- **Python**: 3.11 or 3.12 (MediaPipe dependency requires <= 3.12).
- **FFmpeg**: Full build with `libass` and `libx264` (`Gyan.FFmpeg`).
- **Model Backend**: Ollama (offline local) or Anthropic/OpenAI/Gemini API key.

## CLI Commands

### 1. Environment & Dependency Diagnostic
```bash
autoclip doctor
```
Verifies FFmpeg filters (`libass`), GPU drivers (CUDA/NVENC), Python version, and model providers.

### 2. End-to-End Clipping Pipeline
Run headless transcription, highlight detection, speaker reframing, and caption export:
```bash
autoclip clip <video_path_or_url>
```

### 3. Caption Presets
- `bold_pop`: Bold white letters with outline; active spoken word scales and turns yellow.
- `karaoke_fill`: Words fill with color in sync with speech timestamps.
- `clean_lower`: Minimalist broadcast lower-third without distracting bounce.
- `boxed`: High-contrast text on solid color bounding pill.

### 4. Interactive Review UI
Launch local review webapp for manual trim adjustments before final rendering:
```bash
autoclip serve --port 8000
```

## Agent Workflows
Use `autoclip` when:
1. Converting 16:9 full-length webinars, interviews, or engineering walkthroughs into high-yield 9:16 mobile shorts.
2. Generating captioned snippets without sending audio/video to external cloud transcription platforms.
