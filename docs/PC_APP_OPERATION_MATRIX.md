# PC Application Operation Matrix & Tool Orchestration Sequences

This document provides the authoritative operational reference, headless CLI commands, MCP server contracts, and optimal execution sequences for all engineering, CAD/BIM, geospatial, reverse engineering, and media applications installed on this PC.

---

## 1. Verified Applications & Operational Interfaces Matrix

| Application | Category | Executable Path / Interface | Operational Command & Syntax |
| :--- | :--- | :--- | :--- |
| **QGIS 4.2.3** | Geospatial & Hydrology | `qgis_agent_mcp` (MCP)<br>`C:\Program Files\QGIS 4.2.3\bin\qgis_process-qgis.bat` | `qgis_agent_mcp` calls:<br>`qgis_tool_call(tool_name, params)`<br>CLI fallback: `qgis_process-qgis.bat run <alg> --PARAM=VAL` |
| **HEC-RAS 7.0** | River & Flood Hydraulics | `hecras_agent_mcp` (MCP)<br>`C:\Program Files (x86)\HEC\HEC-RAS\7.0\RasProcess.exe` | `hecras_compute_simulation(project_path, plan_name)`<br>`hecras_extract_wsel(project_path, plan_name, cross_sections)` |
| **EPA SWMM 5.2.4** | Urban Drainage & Hydrology | `C:\Program Files\EPA SWMM 5.2.4 (64-bit)\runswmm.exe` | `runswmm.exe <input.inp> <report.rpt> [output.out]` |
| **EPANET 2.2** | Pressurized Water Networks | `C:\Program Files (x86)\EPANET 2.2\runepanet.exe` | `runepanet.exe <input.inp> <report.rpt> [binary.out]` |
| **KPK MRS-2025** | Cost Estimation & Rates | `C:\tools\kpk-mrs\mrs_lookup.py` | `python C:\tools\kpk-mrs\mrs_lookup.py --item <CODE> --district <DISTRICT>` |
| **AutoCAD LT 2027** | 2D CAD Drafting | `C:\Program Files\Autodesk\AutoCAD LT 2027\accoreconsole.exe` | `accoreconsole.exe /i <drawing.dwg> /s <script.scr> /l en-US` |
| **Autodesk Revit 2027** | Parametric BIM | `C:\Program Files\Autodesk\Revit 2027\AddIns\DynamoForRevit\DynamoCLI.exe` | `DynamoCLI.exe -o <workspace.dyn> -v` |
| **FreeCAD 1.1** | Parametric 3D CAD | `C:\Users\Imran\AppData\Local\Programs\FreeCAD 1.1\bin\freecadcmd.exe` | `freecadcmd.exe <automation_script.py>` |
| **Blender 5.2.1 LTS** | 3D Animation & Render | `mcp-for-blender` (MCP)<br>`C:\Program Files\Blender Foundation\Blender 5.2\blender.exe` | `blender.exe -b <file.blend> -P <script.py> -o <render_path> -f <frame>` |
| **Trimble SketchUp 2026** | Architectural Modeling | `C:\Program Files\SketchUp\SketchUp 2026\SketchUp\SketchUp.exe` | `SketchUp.exe <model.skp>` / Ruby API automation |
| **Sweet Home 3D** | Space Planning | `C:\Program Files (x86)\Sweet Home 3D\SweetHome3D.exe` | `SweetHome3D.exe <plan.sh3d>` / OBJ batch export |
| **CloudCompare** | Point Clouds & LiDAR | `C:\Program Files\CloudCompare\CloudCompare.exe` | `CloudCompare.exe -SILENT -O <cloud.laz> -C_EXPORT_FMT LAS -SS SPATIAL 0.05 -SAVE_CLOUDS` |
| **COLMAP** | Photogrammetry & SfM | `C:\tools\photogrammetry\COLMAP\COLMAP.bat` | `colmap.bat automatic_reconstructor --workspace_path <dir> --image_path <dir>` |
| **Ghidra 12.2.0** | Binary Decompilation | `C:\ProgramData\chocolatey\lib\ghidra\tools\ghidra_12.2_PUBLIC\support\analyzeHeadless.bat` | `analyzeHeadless.bat <project_dir> <project_name> -import <bin> -postScript <py>` |
| **JADX 1.5.6** | Android DEX Decompilation | `C:\ProgramData\chocolatey\lib\jadx\tools\bin\jadx.bat` | `jadx.bat -d <out_dir> <app.apk>` |
| **Wireshark / TShark** | Network Packet Analysis | `C:\Program Files\Wireshark\tshark.exe` | `tshark.exe -r <capture.pcapng> -Y <filter> -T fields -e <field>` |
| **FFmpeg 9.0.2** | Bitexact Video Assembly | `ffmpeg` | `ffmpeg -i <in> -map_metadata -1 -fflags +bitexact -flags:v +bitexact -flags:a +bitexact <out>` |
| **PPT-Master** | Presentations & Decks | `C:\tools\ppt-master` | `python -m ppt_master --template <id> --content <data.json>` |

---

## 2. Optimal Tool Sequences (OTS) by Work Domain

### Sequence 1: River Hydraulics, Flood Hazard & Protection Bund Design
```mermaid
flowchart LR
    A["Raw DEM & Catchment"] --> B["QGIS Agent MCP<br>(Watershed Delineation)"]
    B --> C["EPA SWMM CLI<br>(Peak Flow Q_peak)"]
    C --> D["HEC-RAS Agent MCP<br>(2D Unsteady Simulation)"]
    D --> E["QGIS Agent MCP<br>(WSEL Risk Zonation)"]
    E --> F["KPK MRS-2025<br>(Stone Pitching & Gabions BOQ)"]
```
1. **Delineation**: Load DEM into `qgis_agent_mcp`, compute fill sinks, flow accumulation, and channel vectors.
2. **Hydrology**: Run `runswmm.exe input.inp report.rpt` to generate design runoff hydrographs ($Q_{10}, Q_{25}, Q_{50}, Q_{100}$).
3. **Hydraulics**: Pass geometry and peak discharge into `hecras_agent_mcp` (`hecras_compute_simulation`) to calculate water surface profiles and velocities.
4. **Hazard Mapping**: Extract WSEL rasters into QGIS, intersect with settlement footprints, and classify flood risk zones.
5. **BOQ & Costing**: Query `C:\tools\kpk-mrs\mrs_lookup.py` for stone pitching, earthwork bunds, and gabions with district location factors.

---

### Sequence 2: Potable Water Distribution Network Design
```mermaid
flowchart LR
    A["Settlement Survey"] --> B["QGIS Agent MCP<br>(Network Layout & DEM Sampling)"]
    B --> C["EPANET CLI<br>(Hydraulic Simulation)"]
    C --> D["AutoCAD LT Console<br>(Profile & Trench DWG)"]
    D --> E["KPK MRS-2025<br>(Pipes & Sluice Valves BOQ)"]
```
1. **Network Spatial Setup**: Layout distribution nodes, pipes, and reservoir in QGIS. Sample node elevations from terrain DEM.
2. **Hydraulic Analysis**: Run `runepanet.exe network.inp sim_report.rpt` to verify pressures (> 15 psi) and velocities (0.6 - 2.5 m/s).
3. **Longitudinal Profiles**: Use AutoCAD LT `accoreconsole.exe` to render pipe alignment sheets, crossing details, and thrust block schedules.
4. **Schedule of Rates**: Use `mrs_lookup.py` (KPK MRS Chapter 14 - Water Supply & Sanitary) to price HDPE/GI pipes, sluice valves, and air release valves.

---

### Sequence 3: Architectural BIM, Space Planning & Forensic Presentation
```mermaid
flowchart LR
    A["Space Concept"] --> B["Sweet Home 3D<br>(2D/3D Partition Plan)"]
    B --> C["FreeCAD 1.1 CLI<br>(Parametric IFC Model)"]
    C --> D["Autodesk Revit 2027<br>(Clash Detection & Families)"]
    D --> E["Blender 5.2 MCP<br>(Photoreal Cycles Render)"]
    E --> F["FFmpeg 9.0.2<br>(Zero-Metadata Walkthrough)"]
```
1. **Conceptual Planning**: Quick partition, door, window, and furniture layout in Sweet Home 3D; export OBJ/DXF.
2. **Parametric IFC**: Run `freecadcmd.exe` with Python BIM script to create architectural walls, slabs, and IFC export.
3. **BIM Standards**: Import into Revit 2027 via DynamoCLI to audit schedules, structural coordination, and system families.
4. **Cinematic Render**: Transfer scene to Blender 5.2 via `mcp-for-blender`, configure lighting, camera sweep, and render frames.
5. **Final Output**: Stitch frames into 1080p video with FFmpeg applying clean file bitexact scrubbing.

---

### Sequence 4: Drone Aerial Survey & Topographic Contouring
```mermaid
flowchart LR
    A["Aerial Photos"] --> B["COLMAP CLI<br>(Dense Stereo .ply)"]
    B --> C["CloudCompare CLI<br>(Noise Filter & Ground LAS)"]
    C --> D["QGIS Agent MCP<br>(1m Elevation Contours & Ortho)"]
```
1. **Reconstruction**: Run `C:\tools\photogrammetry\COLMAP\COLMAP.bat automatic_reconstructor` on drone image folder.
2. **Point Cloud Downsampling**: Execute `CloudCompare.exe -SILENT -O dense.ply -C_EXPORT_FMT LAS -SS SPATIAL 0.05 -SAVE_CLOUDS`.
3. **Topographic Contours**: Import ground LAS into QGIS via `qgis_agent_mcp`, generate DEM raster and 1m/5m contour lines.

---

### Sequence 5: Reverse Engineering & Binary Forensics
```mermaid
flowchart LR
    A["Target Binary"] --> B["JADX / Ghidra CLI<br>(Decompile C / Java AST)"]
    B --> C["Wireshark TShark CLI<br>(Protocol Payload Capture)"]
    C --> D["PPT-Master / Typst<br>(Forensic Dossier Report)"]
```
1. **Decompilation**: Run JADX for APK (`jadx.bat -d out app.apk`) or Ghidra headless (`analyzeHeadless.bat`) for native Win32/x64 binaries.
2. **Network Interception**: Run `tshark.exe -r capture.pcapng -Y "http.request or tls.handshake"` to isolate API endpoints and payloads.
3. **Documentation**: Assemble findings into a forensic dossier using PPT-Master and Typst.

---

## 3. Automation Dispatcher CLI

Use the local python tool sequencer to query or validate workflows directly:

```powershell
# Validate all application paths and interfaces on this PC:
python tools\tool_sequencer.py --validate

# View available workflows:
python tools\tool_sequencer.py --list-workflows

# Inspect a specific sequence (e.g. flood modeling):
python tools\tool_sequencer.py --sequence flood_hazard_assessment
```
