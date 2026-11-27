---
name: herk-edit-kit
description: AI-assisted video editing toolkit for coding agents. Automates silence removal, mistake/retake cleanup, transcript-driven cuts, and motion graphics using HyperFrames templates and 406 modular cards.
---

# Herk Edit Kit (Agentic Video Editing & Motion Graphics)

Herk Edit Kit by Nate Herk enables coding agents to edit raw talking-head videos, social reels, and YouTube Shorts. It bridges transcription, automated editing decisions (EDLs), silence cutting, and HyperFrames motion graphics.

- **Local Repository**: `C:\tools\herk-edit-kit`
- **GitHub**: `https://github.com/nateherkai/herk-edit-kit`

## Built-In Specialized Agent Skills

The kit includes 15 modular skills located in `C:\tools\herk-edit-kit\.agents\skills\`:

1. **`cut-silences`**: Detects dead air and audio gaps, tightening dialogue cadence without clipping speech consonants.
2. **`cut-mistakes`**: Compares repeated takes and false starts in transcripts to pick the best performance.
3. **`edit-video`**: Multi-track timeline assembly, audio normalization, and cut sequencing.
4. **`short-form-edit`**: 9:16 vertical video reframing, hook placement, and pacing.
5. **`video-storytelling`**: Structural pacing, narrative arcs, and B-roll placement logic.
6. **`style-library`**: Access to 406 pre-designed motion graphic cards, callouts, titles, and stat callouts.
7. **`hyperframes` / `hyperframes-cli`**: High-performance browser rendering pipeline for animated lower thirds, subtitles, and chapter bumpers.
8. **`hyperframes-video-beats`**: Synchronizes graphics animations to audio beats and vocal emphasis.
9. **`motion-showreel`**: Generates showcase reels demonstrating visual styles and animations.
10. **`website-to-hyperframes`**: Converts web pages and URLs into animated motion graphics sequences.

## Running the Editing Pipeline

### 1. Silence & Mistake Pruning
```bash
node C:\tools\herk-edit-kit\scripts\cut-silences.mjs --input raw_footage.mp4 --threshold -35dB --min-duration 0.4
```

### 2. Motion Graphics Card Selection
Browse and apply cards from the style library:
```bash
node C:\tools\herk-edit-kit\scripts\render-card.mjs --template "stat-callout" --data '{"title": "KPK Investment", "value": "PKR 4.2B"}' --output card.png
```

### 3. HyperFrames Timeline Render
```bash
npx hyperframes render --entry video-projects/active/timeline.tsx --output dist/final_short.mp4 --fps 30
```
