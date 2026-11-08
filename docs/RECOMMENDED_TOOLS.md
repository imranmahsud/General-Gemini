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

---

## Disregarded Tools (Hype / Low Utility)

- **AutoHedge / Vibe-Trading**: High financial loss risk, lack real order-flow execution infrastructure.
- **Open-LLM-VTuber**: Desktop streaming novelty with no engineering utility.
- **Open Higgsfield AI**: Thin Electron UI wrapping third-party APIs.
- **LibreChat / FinceptTerminal**: Redundant with Antigravity and dedicated terminal CLI agents.
