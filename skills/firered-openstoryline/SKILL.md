---
name: firered-openstoryline
description: Conversational, intention-driven AI video editing and directing agent. Orchestrates media search, multi-clip segmentation, storyline construction, beat-synced music, voice-over, transition generation, and multi-turn iterative re-editing via MCP or web API.
---

# FireRed-OpenStoryline (Intention-Driven Video Editing Agent)

FireRed-OpenStoryline turns raw media clips into edited, narrative-driven videos through conversational AI directing. It features native Model Context Protocol (MCP) tool orchestration, semantic media search, timestamp-aligned rough cuts, style transfer, and conversational refinement.

- **Local Repository**: `C:\tools\FireRed-OpenStoryline`
- **GitHub**: `https://github.com/FireRedTeam/FireRed-OpenStoryline`

## Key Capabilities
1. **Intelligent Script & Storyline Construction**: Combines user themes, emotion recognition, and visual understanding to build structured storylines.
2. **ASR-Based Speech Rough Cuts**: Removes filler words, false starts, and stutters with timestamp-aligned cuts.
3. **AI Transition Generation**: Automatically synthesizes connective transition shots between adjacent clips.
4. **Conversational Re-editing**: Swap clips, change pacing, modify captions, or adjust typography using plain text instructions within the same editing session.

## Architecture & Services
- **MCP Server**: Exposes video editing tools via standard JSON-RPC:
  ```bash
  cd C:\tools\FireRed-OpenStoryline
  python -m open_storyline.mcp.server
  ```
- **FastAPI Backend**:
  ```bash
  cd C:\tools\FireRed-OpenStoryline
  uvicorn agent_fastapi:app --host 127.0.0.1 --port 8000
  ```

## Editing Workflow Loop
1. **Initialize Session**: Supply raw input clips, target theme, and mood requirements.
2. **Review Initial Cut**: Inspect timeline arrangement, speech alignment, and generated captions.
3. **Iterative Refinement**: Send targeted revisions (e.g., "tighten scene 2 cuts", "swap B-roll on transition", "bold yellow subtitles") using the persistent `session_id`.
4. **Export Render**: Output final master MP4 or project timeline.
