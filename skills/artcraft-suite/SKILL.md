---
name: artcraft-suite
description: Comprehensive toolsuite and MCP bridge for the 14 native ArtCraft creative, CAD, media, and publishing applications.
---

# ArtCraft Production Suite Guide

The ArtCraft ecosystem consists of 14 native, professional-grade, headless-capable creative and engineering tools installed in `C:\Program Files\ArtCraft\`. Each tool features both a high-performance desktop GUI and an agent-native CLI with an embedded Model Context Protocol (MCP) server.

## Tool Directory & MCP Server Mapping

| App | Binary / Launcher | Core Domain | MCP Stdio Command | Key Capabilities |
| :--- | :--- | :--- | :--- | :--- |
| **CADCraft** | `cadcraft.bat` | 2D/3D CAD & Drafting | `cadcraft mcp` | DXF/DWG/DWT/SVG/PDF conversion, geometry analysis, headless plotting, layer management |
| **FilmCraft** | `filmcraft.bat` | Non-Linear Video Editor | `filmcraft mcp` | Timeline editing, EDL/XML assembly, multi-track cuts, speed ramps, LUT/grading, render pipeline |
| **AniCraft** | `anicraft.bat` | 2D/3D Animation | `anicraft mcp` | Character rigs, procedural motion, keyframing, timeline export, frame-by-frame rendering |
| **PhotoCraft** | `photocraft.bat` | Raster Photo & Image Editor | `photocraft mcp` | Layer stacks, blend modes, retouching, masking, color curves, automated droplets |
| **VectorCraft** | `vectorcraft.bat` | Vector Illustration | `vectorcraft mcp` | Bezier geometry, SVG generation, scalable icon sets, Boolean shapes, typography |
| **FigCraft** | `figcraft.bat` | UI / UX Design Engine | `figcraft mcp` | Figma file compatibility, UI components, auto-layout, design tokens, responsive frames |
| **SoundCraft** | `soundcraft.bat` | Digital Audio Workstation | `soundcraft mcp` | Multi-track audio DAW, stem isolation, EQ/compression, Foley SFX, loudness normalization |
| **EffectCraft** | `effectcraft.bat` | VFX & Motion Graphics | `effectcraft mcp` | Particle systems, visual effects compositing, filter graphs, procedural shaders |
| **DeckCraft** | `deckcraft.bat` | Slide Presentations | `deckcraft mcp` | PPTX / `.deckcraft` authoring, pitch decks, data slides, template rendering |
| **GridCraft** | `gridcraft.bat` | Spreadsheets & Tables | `gridcraft mcp` | High-throughput data tables, XLSX/CSV processing, formula evaluation, data analysis |
| **PdfCraft** | `pdfcraft.bat` | Document PDF & OCR Engine | `pdfcraft mcp` | Deep OCR (ONNX text detection + recognition), PDF splitting, merging, forms, redaction |
| **LightCraft** | `lightcraft.bat` | RAW Photo Developer | `lightcraft mcp` | RAW camera sensor development, batch exposure/white balance, catalog metadata |
| **DesignCraft** | `designcraft.bat` | Page Layout & Publishing | `designcraft mcp` | Print publications, magazines, flyers, multi-page grids, bleed & trim marks |
| **WordCraft** | `wordcraft.bat` | Word Processing & Typesetting | `wordcraft mcp` | Typography, markdown/DOCX publishing, academic/forensic dossier formatting |

---

## Agent Usage Protocols

### 1. Direct Headless CLI Execution
Whenever the user needs a quick conversion, drawing inspection, image edit, or audio render, call the launcher directly via `run_command`:
```powershell
# CAD conversion:
cadcraft convert input.dwg output.pdf

# CAD drawing metadata inspection:
cadcraft info drawing.dxf

# PDF extraction & OCR:
pdfcraft info input.pdf

# Photo droplet / batch filter:
photocraft convert input.png output.webp
```

### 2. MCP Server Bridge
To drive any Craft app interactively or in live collaboration with a running window:
```powershell
# Launch MCP on stdio (headless session):
cadcraft mcp

# Connect MCP to a running GUI application on its local control port:
cadcraft mcp --connect 127.0.0.1:7979 --lazy
```

### 3. Integrated Engineering & Production Pipelines
- **Civil & Structural Projects**: Bridge **CADCraft** with **rvt-mcp** and **qgis_agent_mcp** for complete CAD/BIM/GIS interoperability.
- **Video & Documentary Production**: Bridge **FilmCraft** and **SoundCraft** with the **documentary001** HyperFrames standard for automated assembly of forensic dossiers, voiceovers, and SFX.
- **Contract & BOQ Work**: Use **GridCraft** and **PdfCraft** to parse MRS cost schedules, BOQs, and tenders with zero data loss.
