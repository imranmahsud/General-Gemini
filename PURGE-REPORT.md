# Purge report

Cleaning pass run 2026-11-27 against `General-Gemini`. Removed 45 items,
**145.4 MB** across 18636, with no skill instructions lost.

Rule used: delete only what is provably duplicated, empty, stale, unsafe, or not discoverable by any
harness. Anything unique was kept, and every removal lists how to get it back.

## Removed

| Path | MB | Why |
| --- | ---: | --- |
| `General-Gemini-Ready-For-New-PC.zip` | 0.0 | Stale partial snapshot (705 entries, docs/ and plugins/ only) that drifted from the live tree; the repo itself is the source of truth. |
| `Check` | 0.7 | Nine hash-named screenshots from a one-off verification run; nothing references them. |
| `configs/syncthing` | 0.0 | Machine-specific Syncthing config that ships private keys (key.pem, https-key.pem, cert.pem) in a public repo. Regenerate the config instead of publishing it. |
| `skills/everything-claude-code` | 59.0 | Vendored upstream collection. Its 1062 skills sit four levels deep (.agents/skills/*/SKILL.md), which no harness discovers, so they were never loadable. The curated 311 are kept as ecc-*; recover from the upstream project if the rest is wanted. |
| `skills/mattpocock-skills` | 0.7 | Vendored upstream collection; all 38 skills are already installed as mp-* at the top level. |
| `skills/superpowers` | 1.5 | Vendored upstream collection; all 15 skills are already installed as sp-* at the top level. |
| `skills/gstack` | 9.7 | Vendored upstream collection; all 18 skills are already installed as gstack-* at the top level. |
| `skills/day-trader-skill` | 1.1 | Vendored upstream collection; all 11 skills are already installed as trader-* at the top level. |
| `skills/take-one` | 0.0 | Empty container: no SKILL.md and no nested skills. |
| `plugins/googlecloudtools.datacloud_telemetry` | 0.0 | Gemini-only telemetry hook (hooks.json + one JS bundle). Carries no skills and exposes no tools, so it does nothing in any other harness. |
| `tools/make_crime_materials.py` | 0.0 | One-off content generator hardcoded to D:/AI-Folders/MoneyPrinterTurbo/materials/skardu_crime; that path does not exist and the script needs httpx/Pillow outside the repo requirements. |
| `tools/make_real_materials.py` | 0.0 | One-off content generator hardcoded to D:/AI-Folders/MoneyPrinterTurbo/materials/houthi_saudi_real; path does not exist, deps outside requirements. |
| `tools/make_monetization_doc.py` | 0.0 | One-off generator that writes a single .docx to D:/AI-Folders/MoneyPrinterTurbo/outputs; path does not exist, python-docx outside requirements. |
| `tools/setup_agent_shims.ps1` | 0.0 | Generates .cmd shims for 28 hardcoded install paths from the original workstation; three targets are already missing. Superseded by install.ps1 and install-apps.ps1. |
| `skills/impeccable/.agent` | 2.1 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.agents` | 2.2 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.claude` | 2.2 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.claude-plugin` | 0.0 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.codex` | 0.0 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.cursor` | 2.2 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.cursor-plugin` | 0.0 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.devin` | 2.1 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.dsh` | 2.1 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.gemini` | 2.1 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.grok` | 2.2 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.hermes` | 2.1 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.kiro` | 2.1 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.omp` | 2.1 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.opencode` | 2.1 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.pi` | 2.1 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.qoder` | 2.1 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.rovodev` | 2.1 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.trae` | 2.1 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.trae-cn` | 2.1 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.veto` | 2.1 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/.vibe` | 2.1 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/cursor-plugin` | 2.2 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/plugin` | 2.2 | Per-harness mirror of the same skill content (generated install format for another agent); skill/ is the canonical source and is kept. |
| `skills/impeccable/tests` | 15.9 | The vendored CLI's own test suite and fixtures (2385 files); not used by the skill instructions. |
| `skills/ui-ux-pro-max` | 3.5 | Trimmed duplicate of the full UI/UX package (same name and description). Its instructions resolve ${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py, a path the trimmed bundle does not contain. The complete package takes over this name. |
| `skills/ui-ux-pro-max-skill -> skills/ui-ux-pro-max` | 0 | Renamed to the canonical skill name; this is the complete package (cli, data, search script). |
| `skills/ui-ux-pro-max/.claude/skills/{banner-design, brand, design, design-system, slides, ui-styling}` | 6.1 | Six skills duplicated inside the package mirror; every one ships at the top level of skills/. |
| `skills/ui-ux-pro-max/.github` | 0 | CI workflows inside a vendored skill bundle. |
| `skills/impeccable/.github` | 2.2 | CI workflows and issue templates from the upstream project; the skill never uses them. |
| `skills/sherlock/sherlock` | 0 | Nested duplicate of the skill's own SKILL.md. |

## Repaired

| Path | Change |
| --- | --- |
| `plugins/data-agent-kit-plugin/mcp_config.json` | Dropped 9 servers (dak-alloydb, dak-spark, dak-bigquery, dak-bigtable-data, dak-bigtable, dak-cloudsql, dak-gcs, dak-kc, dak-spanner) that launch `mcp/bin/mcp_proxy_bundle.cjs`, a file that is not in this repo. `dak-notebook` and `dak-viz` remain: both run `mcp/dist/index.js`, which passes `node --check`.
| `plugins/google_maps_platform/skills/SKILL.md` | Was a skill file in a layout no harness scans. Promoted to `skills/google-maps-platform/SKILL.md`; the plugin shell (plugin.json + installed_version.json, no tools) was removed. |

## Recovering something that was removed

| Item | How |
| --- | --- |
| `everything-claude-code` (1062 upstream skills) | `git clone https://github.com/affaan-m/everything-claude-code` — the 311 curated ones stay here as `ecc-*`. |
| `mattpocock-skills` / `superpowers` / `gstack` / `day-trader-skill` | Their skills remain here as `mp-*` / `sp-*` / `gstack-*` / `trader-*`; the upstream repos can be re-vendored if the packaging is needed. |
| `configs/syncthing` | Regenerate with `syncthing generate` on the target machine. The removed copy held private keys and should never have been public. |
| impeccable / ui-ux-pro-max per-harness mirrors | `npx impeccable install` / re-clone the upstream package. The canonical `skill/` sources are still here. |
| one-off generators (`make_*_materials.py`, `make_monetization_doc.py`) | Recoverable from git history before this overwrite (commit `960276a1`). |

## Not touched

All 986 remaining skills, the ten skill-bearing plugins, `tools/` (kpk-mrs, military-animator, chatgpt-mcp,
hecras-mcp, ThinkPad settings, tool sequencer, battery threshold), `docs/`, `templates/`, `configs/ollama`,
`launchers/`, and the installers.
