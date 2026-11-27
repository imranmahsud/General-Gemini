# General-Gemini → DeepSeek Harness import

Imported from https://github.com/imranmahsud/General-Gemini on 2026-11-27, after the repository was
cleaned (see [PURGE-REPORT.md](PURGE-REPORT.md)).

## Where things live

| What | Path |
|---|---|
| Vendored repo (source of truth, also the git checkout) | `C:\Users\Imran\.dsh\vendor\general-gemini` |
| Installed skills (live DSH user skill root) | `C:\Users\Imran\.dsh\skills` |
| Import manifest (source path → installed name) | `C:\Users\Imran\.dsh\skills\.ingest-manifest.json` |
| Import/maintenance scripts | `C:\Users\Imran\.dsh\vendor\general-gemini\tools\dsh` |
| Profile patch that bounds the catalog | `C:\Users\Imran\.dsh\profiles\desktop\cordis.patch.yml` |

`~/.dsh/skills` is the `user-dsh` root that `@deepseek-ai/dsh-skill-filesystem` scans (rank 400), so
every skill there is available in every workspace without copying it into a project.

## What was installed

- **1086 skill bundles** from the 987 skill folders in `skills/` plus 99 unique skills from the ten
  skill-bearing plugins (Flutter 25, science 41, data-agent-kit 24, Gemini API 3, modern-web 2, one
  each for Calendar/Docs/Drive/Sheets/Slides).
- Every skill parsed and validated: kebab-case name ≤ 64 chars, non-empty description, `SKILL.md`
  present, no duplicate names. 18 clashes were suffixed (`design-system-2`, `bigquery-ai-ml-2`, …)
  and 14 identical copies skipped.
- Nothing is rewritten in the repo. The installed copies are separate, and repairs (name
  normalisation, invocation flags) apply only there.

## Model invocation policy

A full-library catalog is inlined into every session, so it is split:

- **499 skills are model-invocable** — the agent sees them in `<available_skills>` and can load them.
- **587 are user-invocable only** — `ecc-*` (311), `trade-*` (74), `gsd-*` (72), `cli-anything-*` (69),
  `mp-*` (38), `sp-*` (15), plus 8 that shipped with the flag. They carry
  `disable-model-invocation: true` in their installed frontmatter: still on disk, still loadable with
  `/name`, but they cost no prompt space until invoked.
- `catalogDescriptionMaxLength: 100` is set on `@deepseek-ai/dsh-tool-skill` in the profile patch, so
  rendered descriptions stay short (the full description still arrives when a skill loads).

To make one of them model-invocable, delete the `disable-model-invocation: true` line from its
`SKILL.md`. To make everything model-invocable, run the loop under "Re-running".

## Tools, plugins, and what is not wired

Vendored but not registered as DSH tools:

| Item | Why it is not wired |
|---|---|
| `plugins/data-agent-kit-plugin/mcp/dist/index.js` | Node MCP server; needs `gcloud` auth and a GCP project. The nine regional proxy servers were removed from `mcp_config.json` because the proxy bundle they launch is absent from the repo. |
| `plugins/flutter/mcp_config.json` | Runs `dart mcp-server`; no Dart SDK on this machine. |
| `plugins/science` biomolecular sidecar | Prebuilt `dist/mcp_entry.cjs` (syntax-checked) but configured for `agy-node`; wiring it means pointing a DSH MCP bundle at a plain `node` and testing it. |
| `plugins/gemini-api` | Remote `serverUrl` MCP; DSH wiring not verified. |
| `tools/chatgpt-mcp`, `tools/hecras-mcp` | Python `mcp` SDK is installed for Python 3.12 and both servers compile, but they need `OPENAI_API_KEY` / a local HEC-RAS install. |
| `tools/kpk-mrs`, `tools/military-animator`, `tools/tool_sequencer.py` | CLI scripts, not MCP servers; run them directly with `C:\Users\Imran\AppData\Local\Programs\Python\Python312\python.exe`. |

Registering a broken MCP server adds failing tools to every session, so nothing is wired until its
runtime and credentials exist. `dsh-doc` → `references/mcp-bundle.md` covers wiring one.

## Re-running or extending

```powershell
$env:ELECTRON_RUN_AS_NODE='1'
$node = 'C:\Users\Imran\AppData\Local\Programs\DeepSeek Harness\DeepSeek Harness.exe'
$t = "$env:USERPROFILE\.dsh\vendor\general-gemini\tools\dsh"

& $node "$t\ingest.js"   # copy every skill from the repo into ~/.dsh/skills
& $node "$t\demote.js"   # apply the model/user invocation split
& $node "$t\count.js"    # report the split
```

Updates: `git -C ~\.dsh\vendor\general-gemini pull`, then re-run the steps above.

Undo the split (every skill model-invocable, much larger catalog):

```powershell
Get-ChildItem "$env:USERPROFILE\.dsh\skills" -Recurse -Filter SKILL.md |
  ForEach-Object { (Get-Content $_ -Raw) -replace '(?m)^disable-model-invocation: true\r?\n', '' |
  Set-Content $_ -NoNewline }
```
