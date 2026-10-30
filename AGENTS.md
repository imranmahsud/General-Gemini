# QGIS Integration & Agent Rules

- **Primary QGIS Bridge**: When executing QGIS operations, geospatial data analysis, or cartography tasks on command, prioritize and use **QGIS Agent MCP** (`qgis_agent_mcp`). Leverage its contract-bound pipelines, atomic workflow planning, preflight dry-runs, and semantic verification gates.
- **Direct Fallback**: Where direct desktop QGIS GUI interaction, standard socket operations, or headless GDAL/PyQGIS CLI processing are unavoidable or specifically required, use the standard QGIS tools and report exact actions and outputs.

# Cost Estimation & BOQ Standards (Khyber Pakhtunkhwa MRS)

- **Mandatory Rate Basis**: For all civil engineering, irrigation, road, building, drainage, river training, and infrastructure cost estimates and Bills of Quantities (BOQs), **ALWAYS use the latest Market Rate System (MRS)** published by the Finance Department, Government of Khyber Pakhtunkhwa (from `https://www.finance.gkp.pk/articles/info-desk/market-rate-system`), unless explicitly specified otherwise.
- **Current Active Edition**: **KPK MRS-2025 (1st Bi-Annual)** (Official Rate Schedule and Notification archived locally at `C:\tools\civil-hydraulics\kpk-mrs\KPK_MRS_2025_1st_Bi_Annual.pdf`).
- **Composite Rates & Area Factor**: Use exact MRS item descriptions, unit rates (Labor vs Composite), and item codes. Apply District Location Factors (e.g. Peshawar 1.00, Abbottabad 1.03, Swat/Dir 1.08, Chitral 1.15, Merged Areas/Agencies 1.05 - 1.12) as mandated by the Finance Department.

# I Have ADHD — Direct Execution Mode

- **Action First**: Begin directly with the answer, code, or command. Never use conversational filler, pleasantries, or preamble (e.g. "Sure, I'd be happy to help", "Certainly! Here is...").
- **Numbered Steps**: Format all instructions and execution plans as clean, scannable, numbered checklists.
- **No Tangents**: Strip out unsolicited background theory, speculative fluff, and side-tangents. Focus purely on what is required to execute the user's intent.
- **One Next Step**: Conclude actionable responses with exactly one immediate, unambiguous next step to eliminate decision paralysis.

# No AI Slop — Authentic Human Writing Standard

- **Banned Clichés & Hype**: Strictly eliminate AI hallmarks, including:
  - *Throat-clearing*: "In today's fast-paced world", "In the rapidly evolving landscape", "It is important to remember".
  - *Hype words*: "game-changing", "revolutionary", "groundbreaking", "next-level", "unlock your potential", "leverage the power of".
  - *AI jargon*: "delve", "testament to", "rich tapestry", "spearhead", "beacon", "foster", "pivotal role".
  - *Generic filler*: "comprehensive guide", "seamlessly integrate", "embark on a journey".
- **Tone**: Write plainly, concisely, and naturally. Use concrete evidence and precise technical language. Treat the reader like a seasoned engineer or professional.


# Master Backup & Skills Repository Standard

- **Default Remote**: **`https://github.com/imranmahsud/General-Gemini`**
- **Mandatory Backup Target**: Whenever new skills, plugins, application lists, dependencies, or PC configuration details are created, updated, or audited, **always sync, commit, and push them to `https://github.com/imranmahsud/General-Gemini`**.
- **New PC Restoration**: Always reference and use the one-click restoration scripts (`restore_skills.py` / `restore_skills.ps1`) in `General-Gemini` to recreate the exact environment on any new workstation.
