# Antigravity Ollama Integration: Skills, Settings & MCP Suite

This configuration bridges Google Antigravity's settings, custom skills library (4,100+ skills), and Model Context Protocol (MCP) servers directly into local offline Ollama models.

---

## 🚀 Quick Execution

### 1. Run Antigravity Model in Ollama
The `antigravity` model is registered directly inside Ollama (`FROM qwen2.5:7b`), with built-in:
- **ADHD Direct Execution Mode** (Action-first, clean numbered checklists, no preamble).
- **No AI Slop Standard** (Zero AI hallmarks, authentic engineering prose).
- **KPK MRS-2025 (1st Bi-Annual)** mandatory civil cost estimation standard.
- **QGIS Agent MCP & ALOS World 3D DEM** integration rules.
- **Full Universal CLI Shims** awareness (`bun`, `blender`, `freecadcmd`, `runswmm`, `runepanet`, `tshark`, `colmap`, `kpk-mrs`).

```powershell
# Interactive prompt
ollama run antigravity

# Direct command execution
ollama run antigravity "Calculate 50 m3 concrete foundation using KPK MRS-2025"
```

---

### 2. Autonomous MCP Agent Runner (`ollama-agent`)
To enable Ollama to actively execute MCP tools (`qgis_agent_mcp`, `rvt-mcp`, `hecras_agent_mcp`), system CLI commands, and query Antigravity skills dynamically:

```powershell
# Run task with tool execution
ollama-agent "Search skills for river training and inspect KPK MRS item 06-03-a"
```

---

## 🛠️ MCP Configuration for Frontends & IDEs
For Open-WebUI, Continue (VS Code), Roo Code, LibreChat, or Claude Desktop:
Point the client's MCP configuration to:
- `C:\Users\Imran\.ollama\mcp_servers.json` (or `configs/ollama/mcp_servers.json`).
