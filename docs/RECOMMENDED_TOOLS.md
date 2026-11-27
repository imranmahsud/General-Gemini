# Recommended Agent Tools & Operational Guide

Evaluation and operational guide for agent-native tools, video engines, and stealth scraping tools.

---

## Tier 1: Core Daily Tools

### 1. HyperFrames (`heygen-com/hyperframes`)
- **Category**: Agent-Native Programmatic Video Engine
- **Engine**: Declarative HTML5, CSS3, GSAP rendered via headless Chrome to H.264 MP4.
- **Why It Matters**: Replaces heavyweight React/Remotion setups. Generates animated diagrams, explainer cards, data charts, and presentations directly from code.
- **Installed Location**: Global npm (`hyperframes` v0.9.16+)
- **Verification Command**:
  ```bash
  npx hyperframes doctor
  npx hyperframes check --json
  npx hyperframes render -o out.mp4 --quality looks
  ```

### 2. Camofox Browser (`jo-inc/camofox-browser`)
- **Category**: Stealth Headless Browser & Anti-Bot Scraper
- **Engine**: C++ fingerprint-spoofed Firefox core (Camoufox).
- **Why It Matters**: Bypasses Cloudflare, Akamai, and Turnstile CAPTCHAs where Playwright/Puppeteer fail during web research.
- **MCP Adapter**: Registered in `~/.gemini/config/mcp_config.json` via `@askjo/camofox-browser-mcp`.
- **Windows Setup Note**: The REST server requires Docker or Visual Studio C++ build tools for `better-sqlite3`. The standalone MCP adapter (`C:\tools\camofox-browser\mcp`) is pre-installed.

### 3. Faster-Whisper & yt-dlp
- **Category**: Local Audio Transcription & Media Download
- **Engine**: CTranslate2 neural inference + yt-dlp CLI.
- **Why It Matters**: 100% offline speech-to-text, subtitle timing (SRT/VTT), and media extraction with zero API fees.
- **Environment**: Python 3.12 (`C:\Users\Imran\AppData\Local\Programs\Python\Python312`).
- **Command**:
  ```bash
  py -3.12 -c "import faster_whisper; print(faster_whisper.__version__)"
  yt-dlp --version
  ```

### 4. Beautiful-Mermaid
- **Category**: Technical Diagram CLI
- **Why It Matters**: CLI rendering of Mermaid code into clean SVG/PNG assets for reports and documentation.

### 5. Graphify (`graphify-labs/graphify`)
- **Category**: Codebase AST Knowledge Graph & Local GraphRAG
- **Engine**: Tree-sitter AST extractors + NetworkX graph analytics.
- **Why It Matters**: 100% local, zero-token codebase onboarding and architecture analysis. Generates call graphs, detects God nodes and circular dependencies, and builds interactive HTML maps and GraphRAG JSON.
- **Installed Location**: `~/.gemini/config/skills/graphify`
- **Execution Command**:
  ```bash
  python -m graphify <path-to-repo>
  ```

### 6. Hypit (`hypit-ai/hypit`)
- **Category**: Semantic Video Markup Language (SVML) & Video DSL
- **Engine**: SVML / SVS declarative schema for directing generative video workflows.
- **Why It Matters**: Provides structured shot lists, actor anchors, camera choreography, and audio-video timing specifications for agent-driven video pipelines.
- **Installed Location**: `~/.gemini/config/skills/hypit`

### 7. gstack (`garrytan/gstack`)
- **Category**: Multi-Skill Engineering & Review Toolbelt
- **Engine**: Curated agent prompt-skills suite by Garry Tan.
- **Why It Matters**: Includes focused modules for canary verification, deep plan auditing, and HTML design review.
- **Installed Location**: `skills/gstack`

---

## Evaluated & Disregarded / Conditional Tools

- **MoCha (`orange-3dv-team/mocha`)**: Character replacement pipeline for video. Requires ComfyUI, WanVideoWrapper, and a 16GB+ VRAM GPU. Unsuitable for standard CLI agent automation.
- **Firecrawl**: Web markdown crawler. Requires proprietary paid API key (`FIRECRAWL_API_KEY`). Camofox is installed locally and handles anti-bot bypassing without API costs.
- **AutoHedge / Vibe-Trading**: High financial loss risk, lack real order-flow execution infrastructure.
- **Open-LLM-VTuber**: Desktop streaming novelty with no engineering utility.
- **Open Higgsfield AI**: Thin Electron UI wrapping third-party APIs.
- **LibreChat / FinceptTerminal**: Redundant with Antigravity and dedicated terminal CLI agents.
