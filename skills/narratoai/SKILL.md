---
name: narratoai
description: All-in-one AI documentary scriptwriting, commentary generation, TTS voice-over, and automated video editing. Automatically structures multi-scene documentary narration from video clips, generates subtitles, and exports CapCut / Jianying project drafts or rendered MP4s.
---

# NarratoAI (Automated Documentary Scripting & Video Assembly)

NarratoAI automates video commentary and documentary generation. It uses Vision-LLMs (Qwen2-VL / TwelveLabs / GPT-4o / DeepSeek) to analyze video frames, draft scene-by-scene narration scripts, synthesize neural voiceovers, and assemble synchronized edits.

- **Local Repository**: `C:\tools\NarratoAI`
- **GitHub**: `https://github.com/linyqh/NarratoAI`

## Core Workflow Capabilities
1. **Frame & Video Understanding**: Analyzes imported video footage with Vision-LLMs to index scene transitions, subjects, and emotional tone.
2. **Documentary Script Generation**: Writes structured narration tailored to the visual cadence of the footage (pacing, dramatic pauses, factual descriptions).
3. **Voice-Over & TTS Synthesis**: Generates synchronized narration audio using Edge TTS, CosyVoice, or Doubao TTS.
4. **Export Formats**:
   - CapCut / Jianying editable draft projects (JSON timeline + media).
   - Rendered final MP4 with burned-in subtitles and background music.

## Running the WebUI & Backend
From `C:\tools\NarratoAI`:
```bash
uv sync
uv run streamlit run webui.py --server.maxUploadSize=2048
```

## Integration with `documentary001`
Use NarratoAI to draft the forensic narration text, extract clip timings, and map script segments directly into our 5-Act Forensic Dossier HyperFrames timeline (`documentary001`).
