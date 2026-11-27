---
name: programmatic-video
description: Automated, headless code-to-video production pipeline using Remotion, HyperFrames, and Faster-Whisper (whisper-ctranslate2). Renders programmatic motion graphics, HTML scene captures, and word-timed subtitles on CPU without discrete GPU or recurring editing subscriptions.
---

# Programmatic Video Production Stack

Headless code-driven video creation, procedural animation, and timestamped subtitling running entirely on CPU and web standards.

## Core Capabilities

1. **Remotion (`@remotion/cli`, `remotion`)**
   - React-based deterministic video rendering.
   - Code-driven transitions, data visualizers, typographic motion, and audio track synchronization.
   - Preview server: `remotion studio [entry]`
   - Headless render: `remotion render [entry] [composition-id] [output.mp4]`

2. **HyperFrames (`hyperframes`)**
   - HTML/CSS/Tailwind scene-to-MP4 video compiler.
   - Rapidly converts web layouts, banners, and interactive DOM states into video clips via headless browser capture.
   - Initialize project: `hyperframes init [project-name]`
   - Live studio preview: `hyperframes preview`
   - Render output: `hyperframes render [file.html] -o output.mp4`

3. **Faster-Whisper (`whisper-ctranslate2`)**
   - Offline, fast CPU-optimized CTranslate2 Whisper implementation.
   - Generates exact word-level timestamped subtitle tracks (`.srt`, `.vtt`, `.json`).
   - CLI command:
     ```bash
     whisper-ctranslate2 input.mp4 --model base --language en --output_format srt --compute_type int8
     ```

## Directory & File Standards

- Put video project scaffolds in `projects/` or user-specified workspaces.
- Always use `int8` quantization for `whisper-ctranslate2` to prevent memory bottlenecks on 16 GB machines.
- For Remotion compositions, structure standard props:
  - `fps`: 30 or 60
  - `width`: 1920 (or 1080 for 9:16 vertical shorts)
  - `height`: 1080 (or 1920 for 9:16 vertical shorts)
  - `durationInFrames`: `durationInSeconds * fps`

## Automation Workflow

1. **Step 1 - Scene Layout**: Define UI / graphics in Remotion React components or HyperFrames HTML.
2. **Step 2 - Voiceover Sync**: Synthesize audio or supply recorded voice track.
3. **Step 3 - Subtitle Alignment**: Run `whisper-ctranslate2 <audio-or-video> --model small --compute_type int8 --output_format srt` to produce word-level timing.
4. **Step 4 - Assembly & Render**: Execute headless render via `remotion render` or `hyperframes render` to emit clean, optimized MP4.
