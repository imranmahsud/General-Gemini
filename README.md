# General-Gemini — agent skills, plugins and engineering toolchain

Master backup of the skills, plugin configurations and CAD/BIM/GIS/PC-1 engineering tooling used on
the Windows workstation. Clone it on a new machine and run one script to restore everything.

**Last cleaned: 2026-11-27.** 40 stale, duplicated, unsafe or non-discoverable items were removed and
two broken plugin configs repaired — see [PURGE-REPORT.md](PURGE-REPORT.md) for every change and how
to recover anything that was dropped.

---

## What is in here

| Path | Contents |
| --- | --- |
| `skills/` | **987 skills**, one directory per skill: `skills/<name>/SKILL.md` plus its `scripts/`, `references/`, `assets/` |
| `plugins/` | 11 Gemini/Antigravity plugin folders (skills, MCP configs, hooks) |
| `tools/` | Working CLIs and MCP servers: `kpk-mrs`, `military-animator`, `chatgpt-mcp`, `hecras-mcp`, `ThinkPadOptimizedSettingsWindows11`, `tool_sequencer.py`, `set_battery_threshold.py` |
| `templates/` | PC-1 financial model (Python) and Typst technical-report template |
| `docs/` | Engineering applications handbook, CAD/BIM mastery report, installed-apps inventory |
| `configs/` | Ollama model + MCP server definitions |
| `launchers/` | `.bat` launchers for the bundled tooling |
| `install.ps1`, `install-apps.ps1` | Software stack + skills/plugins deployment |
| `restore_skills.py`, `restore_skills.ps1` | Skills-only restore (Gemini and Claude skill roots) |
| `export.ps1` | Pull installed skills back into this repo before committing |
| `DSH-INGEST.md` | Import into DeepSeek Harness |
| `PURGE-REPORT.md` | Clean-up log from 2026-11-27 |

## Skill layout rules

Every skill is exactly one level deep and self-contained. Breaking these rules is what produced the
dead weight that was purged, so keep them when adding skills:

1. `skills/<name>/SKILL.md` — never `skills/collection/skills/<name>/SKILL.md`. Nested bundles are
   invisible to Gemini, Claude Code and DeepSeek Harness; they load nothing.
2. `<name>` is kebab-case, lower case, ≤ 64 characters, unique in the repo.
3. `SKILL.md` starts with YAML frontmatter containing at least `name:` and `description:`.
4. Keep the whole bundle together (`scripts/`, `references/`, `assets/`) — skill bodies reference them
   by relative path.
5. No build output, CI workflows, per-harness mirror directories or vendored `.git` inside a skill.

## Largest skill groups

| Group | Count | What it covers |
| --- | ---: | --- |
| `ecc-*` | 311 | Everything Claude Code: engineering workflow, reviews, evals, language patterns |
| `trade-*` | 74 | US equity screening, risk, post-trade review |
| `gsd-*` | 72 | GSD project/milestone planning workflow |
| `cli-anything-*` | 70 | Agent-native CLIs for desktop apps (Blender, FreeCAD, QGIS, GIMP, …) |
| unprefixed | 56 | Single-purpose skills: `documentary001`, `impeccable`, `hyperframes*`, `humanizer`, `office*` |
| `mp-*` | 38 | Matt Pocock's engineering skills |
| `sp-*` | 15 | Superpowers workflow skills |
| `cad-*`, `sci-*` | 13 each | Parametric CAD, scientific Python |
| `founder-*`, `threejs-*`, `trader-*` | 11 each | Business planning, Three.js, trading desk |

Full inventory: `restore_skills.py --list` or count `skills/*/SKILL.md`.

## Restore on a new Windows machine

```powershell
git clone https://github.com/imranmahsud/General-Gemini.git
cd General-Gemini

# 1. software: runtimes, choco/winget packages, reverse-engineering and engineering tools
powershell -ExecutionPolicy Bypass -File .\install-apps.ps1

# 2. skills + plugins + Python engineering environment
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

Skills land in `~\.gemini\config\skills` (and `~\.claude\skills` when that root exists). Plugins land
in `~\.gemini\config\plugins`. For DeepSeek Harness use `DSH-INGEST.md` instead.

## Engineering toolchain

The workstation stack (Revit 2027, SketchUp 2026, Sweet Home 3D, AutoCAD LT, FreeCAD, QGIS, HEC-RAS,
EPA-SWMM, EPANET, ProjectLibre, Ghidra, Wireshark, …) with exact `winget`/`choco` commands is catalogued
in [APPS_LIST.md](APPS_LIST.md) and `docs/installed_apps.csv`. Operating notes for 23+ of those
applications are in `docs/engineering_applications_master_handbook.md`.

## Keeping it in sync

```powershell
powershell -ExecutionPolicy Bypass -File .\export.ps1   # pull installed skills back in
git add -A
git commit -m "Update skills and tooling"
git push origin main
```
