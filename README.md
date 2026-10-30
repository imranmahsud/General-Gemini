# Antigravity & AI Agent Curated Skills

Collection of production-grade AI agent skills designed to eliminate generic AI output and enhance engineering, design, and analysis capabilities across **Antigravity**, **Claude Code**, and **Gemini CLI**.

## Included Skills

| Skill | Description | Primary Capabilities |
| :--- | :--- | :--- |
| **UI/UX PRO MAX** | Design intelligence for interfaces | Multi-framework layout, typography, UI systems |
| **Impeccable** | Polish interfaces & eliminate bad UI patterns | Live browser inspection, anti-pattern linting, design fix loops |
| **Taste Skill (v2)** | Art direction distilled from 247 curated sites | Unstyled page avoidance, custom design directions |
| **Humanizer** | Eliminates predictable AI tells from prose | Strips filler, rhetorical setups, formulaic triads, staged openers |
| **Understand Anything** | Codebase & architecture knowledge graph suite | Architecture graphs, domain modeling, figma tokens, visual dashboard |
| **Diagram Design** | Branded editorial diagrams (HTML/SVG) | 45+ diagram layouts, custom palettes, no generic Mermaid slop |
| **Frontend Slides** | Code-driven interactive presentations | Web presentations, Chart.js, HTML slides |
| **Stop Slop** | Writing discipline & concise technical prose | Cuts throat-clearing, active voice, authentic communication |

## How to Restore on a New PC

Clone this repository on your new PC and run either restore command:

### Option A: Using Python (Cross-platform)
```bash
python restore_skills.py
```

### Option B: Using PowerShell (Windows)
```powershell
.\restore_skills.ps1
```

### Option C: Using npm
```bash
npm run restore
```

The restore script will automatically:
1. Copy all skills directly into `~/.gemini/config/skills/` (and `~/.claude/skills/`).
2. Install required global CLI tools (`impeccable`, `understand-anything-mcp`).
3. Validate and confirm every skill is registered and ready for execution.
