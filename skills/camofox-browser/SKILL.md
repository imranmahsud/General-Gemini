---
name: camofox-browser
description: Stealth headless browser automation and anti-bot web scraping engine using Camoufox (C++ fingerprint spoofing). Use when scraping or automating websites protected by Cloudflare, Akamai, Datadome, CAPTCHAs, or aggressive anti-bot protections where standard fetch, Puppeteer, or Playwright get blocked. Provides human-like browser fingerprints, tab lifecycle management, DOM snapshots with element references, and interactive click/type controls.
license: MIT
metadata:
  version: 1.18.1
---

# Camofox Browser Automation

Camofox is a stealth browser engine built on a specialized C++ Firefox fork (Camoufox) designed specifically for AI agents to interact with web pages without triggering bot detection or CAPTCHA walls.

## Architecture

- **Core REST Server**: `server.js` running on `http://localhost:9377`.
- **MCP Server Adapter**: `C:\tools\camofox-browser\mcp\server.mjs` exposing tools for Claude Code, Antigravity, and Cursor.
- **Local Directory**: `C:\tools\camofox-browser`

---

## 1. Start the Camofox REST Server

From PowerShell:

```powershell
cd C:\tools\camofox-browser
node server.js
```

Or run via Docker / PowerShell helper:

```powershell
cd C:\tools\camofox-browser
.\build.ps1 up
```

The REST server listens on `http://localhost:9377`.

---

## 2. Core Agent Interaction Workflow

### Step 1: Create a Tab
```bash
curl -X POST http://localhost:9377/tabs \
  -H "Content-Type: application/json" \
  -d '{"userId": "agent", "sessionKey": "task-01", "url": "https://target-site.com"}'
```
Returns: `{"tabId": "tab-xxx", "url": "...", "title": "..."}`

### Step 2: Get Accessibility Snapshot (Element References)
```bash
curl -X GET "http://localhost:9377/tabs/tab-xxx/snapshot?userId=agent"
```
Returns structured accessibility tree with interactable element IDs (`e1`, `e2`, etc.):
```
[heading] Target Site
[link e1] Documentation
[button e2] Search
```

### Step 3: Interact (Click / Type)
```bash
# Click by reference
curl -X POST http://localhost:9377/tabs/tab-xxx/click \
  -H "Content-Type: application/json" \
  -d '{"userId": "agent", "ref": "e1"}'

# Type text into input field
curl -X POST http://localhost:9377/tabs/tab-xxx/type \
  -H "Content-Type: application/json" \
  -d '{"userId": "agent", "ref": "e2", "text": "engineering specs"}'
```

### Step 4: Close Tab
```bash
curl -X DELETE "http://localhost:9377/tabs/tab-xxx?userId=agent"
```

---

## 3. Advanced Features

- **Macros**: Use `{"macro": "@google_search", "query": "..."}` for fast navigation.
- **Cookie Injection**: Inject existing session cookies via `/tabs/:tabId/cookies`.
- **Stealth Verification**: Tests pass against bot-detection benchmarks (CreepJS, Pixelscan, Cloudflare Turnstile).
