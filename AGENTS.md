# QGIS Integration & Agent Rules

- **Primary QGIS Bridge**: When executing QGIS operations, geospatial data analysis, or cartography tasks on command, prioritize and use **QGIS Agent MCP** (`qgis_agent_mcp`). Leverage its contract-bound pipelines, atomic workflow planning, preflight dry-runs, and semantic verification gates.
- **Direct Fallback**: Where direct desktop QGIS GUI interaction, standard socket operations, or headless GDAL/PyQGIS CLI processing are unavoidable or specifically required, use the standard QGIS tools and report exact actions and outputs.
