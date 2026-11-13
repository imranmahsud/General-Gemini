#!/usr/bin/env python3
"""
PC Tool Sequencer & App Orchestration System
Authoritative tool sequence planner and preflight validator for installed PC software.
"""

import os
import sys
import json
import subprocess
import argparse

APP_REGISTRY = {
    # 1. Geospatial & Civil Hydraulics
    "qgis": {
        "name": "QGIS 4.2.3",
        "category": "Hydraulics & Geospatial",
        "primary_interface": "MCP (qgis_agent_mcp)",
        "cli_path": r"C:\Program Files\QGIS 4.2.3\bin\qgis_process-qgis.bat",
        "mcp_server": "qgis_agent_mcp",
        "test_cmd": r'"C:\Program Files\QGIS 4.2.3\bin\qgis_process-qgis.bat" --version',
        "syntax": 'qgis_process run <algorithm_id> --PARAM="value"',
        "docs": "https://docs.qgis.org/3.34/en/docs/user_manual/processing/standalone.html"
    },
    "hecras": {
        "name": "HEC-RAS 7.0",
        "category": "Hydraulics & River Modeling",
        "primary_interface": "MCP (hecras_agent_mcp) / RasProcess.exe",
        "cli_path": r"C:\Program Files (x86)\HEC\HEC-RAS\7.0\RasProcess.exe",
        "mcp_server": "hecras_agent_mcp",
        "test_cmd": None,
        "syntax": "hecras_compute_simulation(project_path, plan_name)",
        "docs": "https://www.hec.usace.army.mil/software/hec-ras/documentation.aspx"
    },
    "swmm": {
        "name": "EPA SWMM 5.2.4 (64-bit)",
        "category": "Urban Drainage & Hydrology",
        "primary_interface": "CLI (runswmm.exe)",
        "cli_path": r"C:\Program Files\EPA SWMM 5.2.4 (64-bit)\runswmm.exe",
        "mcp_server": None,
        "test_cmd": r'"C:\Program Files\EPA SWMM 5.2.4 (64-bit)\runswmm.exe"',
        "syntax": "runswmm.exe <input.inp> <report.rpt> [output.out]",
        "docs": "https://www.epa.gov/water-research/storm-water-management-model-swmm"
    },
    "epanet": {
        "name": "EPANET 2.2",
        "category": "Water Distribution & Pressurized Networks",
        "primary_interface": "CLI (runepanet.exe)",
        "cli_path": r"C:\Program Files (x86)\EPANET 2.2\runepanet.exe",
        "mcp_server": None,
        "test_cmd": r'"C:\Program Files (x86)\EPANET 2.2\runepanet.exe"',
        "syntax": "runepanet.exe <input.inp> <report.rpt> [binary.out]",
        "docs": "https://www.epa.gov/water-research/epanet"
    },
    "kpk_mrs": {
        "name": "KPK MRS-2025 (1st Bi-Annual)",
        "category": "Cost Estimation & Schedule of Rates",
        "primary_interface": "Python Tool (mrs_lookup.py)",
        "cli_path": r"C:\tools\kpk-mrs\mrs_lookup.py",
        "mcp_server": None,
        "test_cmd": r'python "C:\tools\kpk-mrs\mrs_lookup.py" --help',
        "syntax": "python C:\\tools\\kpk-mrs\\mrs_lookup.py --item <ITEM_CODE> --district <DISTRICT>",
        "docs": "https://www.finance.gkp.pk/articles/info-desk/market-rate-system"
    },

    # 2. CAD, BIM & 3D Modeling
    "autocad": {
        "name": "Autodesk AutoCAD LT 2027",
        "category": "2D CAD Drafting",
        "primary_interface": "Headless CLI (accoreconsole.exe)",
        "cli_path": r"C:\Program Files\Autodesk\AutoCAD LT 2027\accoreconsole.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "accoreconsole.exe /i <drawing.dwg> /s <script.scr>",
        "docs": "https://help.autodesk.com/view/OARX/2027/ENU/?guid=GUID-ACCORECONSOLE"
    },
    "revit": {
        "name": "Autodesk Revit 2027",
        "category": "Parametric BIM Modeling",
        "primary_interface": "Dynamo CLI / Revit API",
        "cli_path": r"C:\Program Files\Autodesk\Revit 2027\AddIns\DynamoForRevit\DynamoCLI.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "DynamoCLI.exe -o <workspace.dyn> -v",
        "docs": "https://help.autodesk.com/view/RVT/2027/ENU/"
    },
    "freecad": {
        "name": "FreeCAD 1.1",
        "category": "Parametric 3D CAD",
        "primary_interface": "Headless CLI (freecadcmd.exe)",
        "cli_path": r"C:\Users\Imran\AppData\Local\Programs\FreeCAD 1.1\bin\freecadcmd.exe",
        "mcp_server": "cli-anything/freecad",
        "test_cmd": r'"C:\Users\Imran\AppData\Local\Programs\FreeCAD 1.1\bin\freecadcmd.exe" --version',
        "syntax": "freecadcmd.exe <script.py>",
        "docs": "https://wiki.freecad.org/Headless_FreeCAD"
    },
    "blender": {
        "name": "Blender 5.2.1 LTS",
        "category": "3D Animation, Rendering & Modeling",
        "primary_interface": "MCP (mcp-for-blender) / Headless CLI",
        "cli_path": r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe",
        "mcp_server": "mcp-for-blender",
        "test_cmd": r'"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --version',
        "syntax": "blender.exe -b <file.blend> -P <script.py> -o <render_path> -f <frame>",
        "docs": "https://docs.blender.org/manual/en/latest/advanced/command_line/index.html"
    },
    "sketchup": {
        "name": "Trimble SketchUp 2026",
        "category": "Surface Architectural Modeling",
        "primary_interface": "Ruby API / Desktop CLI",
        "cli_path": r"C:\Program Files\SketchUp\SketchUp 2026\SketchUp\SketchUp.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "SketchUp.exe <model.skp>",
        "docs": "https://developer.sketchup.com/"
    },
    "sweethome3d": {
        "name": "Sweet Home 3D",
        "category": "Interior Space Planning",
        "primary_interface": "Desktop / SH3D format generator",
        "cli_path": r"C:\Program Files (x86)\Sweet Home 3D\SweetHome3D.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "SweetHome3D.exe <plan.sh3d>",
        "docs": "https://www.sweethome3d.com/documentation.jsp"
    },

    # 3. Point Clouds & Photogrammetry
    "cloudcompare": {
        "name": "CloudCompare",
        "category": "Point Cloud Processing & Inspection",
        "primary_interface": "Headless CLI (CloudCompare.exe)",
        "cli_path": r"C:\Program Files\CloudCompare\CloudCompare.exe",
        "mcp_server": "cli-anything/cloudcompare",
        "test_cmd": None,
        "syntax": "CloudCompare.exe -SILENT -O <cloud.laz> -C_EXPORT_FMT LAS -SS SPATIAL 0.05 -SAVE_CLOUDS",
        "docs": "https://www.cloudcompare.org/doc/wiki/index.php/Command_line_mode"
    },
    "colmap": {
        "name": "COLMAP Photogrammetry",
        "category": "Structure-from-Motion & Multi-View Stereo",
        "primary_interface": "CLI (COLMAP.bat)",
        "cli_path": r"C:\tools\photogrammetry\COLMAP\COLMAP.bat",
        "mcp_server": None,
        "test_cmd": r'"C:\tools\photogrammetry\COLMAP\COLMAP.bat" -h',
        "syntax": "colmap.bat automatic_reconstructor --workspace_path <path> --image_path <path>",
        "docs": "https://colmap.github.io/cli.html"
    },

    # 4. Binary Analysis & Reverse Engineering
    "ghidra": {
        "name": "Ghidra 12.2.0",
        "category": "Binary Disassembly & Decompilation",
        "primary_interface": "Headless CLI (analyzeHeadless.bat)",
        "cli_path": r"C:\ProgramData\chocolatey\lib\ghidra\tools\ghidra_12.2_PUBLIC\support\analyzeHeadless.bat",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "analyzeHeadless.bat <project_dir> <project_name> -import <target_binary> -postScript <script.py>",
        "docs": "https://ghidra.re/ghidra_docs/analyzeHeadlessREADME.html"
    },
    "jadx": {
        "name": "JADX 1.5.6",
        "category": "Android APK/DEX Decompilation",
        "primary_interface": "CLI (jadx.bat)",
        "cli_path": r"C:\ProgramData\chocolatey\lib\jadx\tools\bin\jadx.bat",
        "mcp_server": None,
        "test_cmd": r'"C:\ProgramData\chocolatey\lib\jadx\tools\bin\jadx.bat" --version',
        "syntax": "jadx.bat -d <out_dir> <file.apk>",
        "docs": "https://github.com/skylot/jadx"
    },
    "wireshark": {
        "name": "Wireshark / TShark",
        "category": "Packet Capture & Dissection",
        "primary_interface": "CLI (tshark.exe)",
        "cli_path": r"C:\Program Files\Wireshark\tshark.exe",
        "mcp_server": None,
        "test_cmd": r'"C:\Program Files\Wireshark\tshark.exe" --version',
        "syntax": "tshark.exe -r <capture.pcapng> -Y <filter> -T fields -e <field>",
        "docs": "https://www.wireshark.org/docs/man-pages/tshark.html"
    },

    # 5. Presentation, Video & Content
    "ffmpeg": {
        "name": "FFmpeg 9.0.2",
        "category": "Media Transcoding & Zero-Metadata Scrubbing",
        "primary_interface": "CLI (ffmpeg.exe)",
        "cli_path": "ffmpeg",
        "mcp_server": None,
        "test_cmd": "ffmpeg -version",
        "syntax": "ffmpeg -i <in> -map_metadata -1 -fflags +bitexact -flags:v +bitexact -flags:a +bitexact <out>",
        "docs": "https://ffmpeg.org/documentation.html"
    },
    "ppt_master": {
        "name": "PPT-Master",
        "category": "Automated Slide & Presentation Generator",
        "primary_interface": "Python/Node CLI",
        "cli_path": r"C:\tools\ppt-master",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "python -m ppt_master --template <id> --content <data.json>",
        "docs": "https://github.com/imranmahsud/General-Gemini"
    }
}

WORKFLOW_SEQUENCES = {
    "flood_hazard_assessment": {
        "title": "Flood Hazard Modeling & Costed Protection Bund Workflow",
        "goal": "From raw DEM and rainfall data to 2D hydrodynamic simulation, risk mapping, and KPK MRS BOQ.",
        "steps": [
            {
                "step": 1,
                "tool": "qgis",
                "role": "Catchment & Terrain Delineation",
                "action": "Use qgis_agent_mcp to load DEM, compute flow accumulation, delineate watershed basin, and extract stream centerline."
            },
            {
                "step": 2,
                "tool": "swmm",
                "role": "Hydrological Peak Flow Computation",
                "action": "Run runswmm.exe on catchment .inp file to calculate peak hydrograph Q_peak for 25/50/100-year return periods."
            },
            {
                "step": 3,
                "tool": "hecras",
                "role": "Hydrodynamic 2D River Simulation",
                "action": "Call hecras_agent_mcp (hecras_compute_simulation) to run 2D unsteady flow simulation and extract WSEL / velocity profiles."
            },
            {
                "step": 4,
                "tool": "qgis",
                "role": "Inundation & Risk Zonation",
                "action": "Import HEC-RAS WSEL grid via qgis_agent_mcp, overlay infrastructure footprint vector layers, and generate flood risk hazard zones."
            },
            {
                "step": 5,
                "tool": "kpk_mrs",
                "role": "BOQ & Cost Estimation",
                "action": "Execute C:\\tools\\kpk-mrs\\mrs_lookup.py to cost stone pitching, earthwork embankments, and gabion spurs using KPK MRS-2025 rates with district location factors."
            }
        ]
    },
    "water_supply_distribution": {
        "title": "Pressurized Water Supply Distribution Network Workflow",
        "goal": "Design, hydraulic simulation, profile drawings, and material takeoffs.",
        "steps": [
            {
                "step": 1,
                "tool": "qgis",
                "role": "Spatial Network Layout",
                "action": "Digitize pipeline alignments, service reservoirs, and consumer nodal points in QGIS; sample nodal elevations from DEM."
            },
            {
                "step": 2,
                "tool": "epanet",
                "role": "Hydraulic Network Simulation",
                "action": "Execute runepanet.exe on .inp model to calculate nodal pressures, headlosses, and pipe velocities under peak demand curves."
            },
            {
                "step": 3,
                "tool": "autocad",
                "role": "Production CAD Profiles",
                "action": "Run accoreconsole.exe to generate layout plans, trench sections, and longitudinal pipe profiles in DWG/DXF format."
            },
            {
                "step": 4,
                "tool": "kpk_mrs",
                "role": "Piping & Valves BOQ",
                "action": "Lookup HDPE / GI pipe excavation, laying, jointing, and sluice valves in KPK MRS-2025 Chapter 14 (Pipes) and Chapter 18."
            }
        ]
    },
    "architectural_bim_visualization": {
        "title": "Architectural Design, BIM & Hyper-Realistic Animation Workflow",
        "goal": "From conceptual layout to BIM compliance and cinematic client walkthrough.",
        "steps": [
            {
                "step": 1,
                "tool": "sweethome3d",
                "role": "Rapid Space Planning",
                "action": "Draft 2D floor plans, wall partitions, and preliminary furniture layout; export 3D OBJ model."
            },
            {
                "step": 2,
                "tool": "freecad",
                "role": "Parametric BIM & IFC Generation",
                "action": "Execute freecadcmd.exe with BIM workbench script to generate parametric wall assemblies, windows, and IFC file."
            },
            {
                "step": 3,
                "tool": "revit",
                "role": "Enterprise BIM Coordination",
                "action": "Run DynamoCLI.exe / Revit to validate clash detection, structural schedules, and system families."
            },
            {
                "step": 4,
                "tool": "blender",
                "role": "Cinematic Lighting & Walkthrough Render",
                "action": "Trigger mcp-for-blender or run blender.exe -b to assign PBR materials, set lighting rigs, and render a camera flythrough."
            },
            {
                "step": 5,
                "tool": "ffmpeg",
                "role": "Audio Dubbing & Bitexact Master Export",
                "action": "Encode master 1080p walkthrough with scrubbed metadata (-map_metadata -1 -fflags +bitexact) and synchronized narration."
            }
        ]
    },
    "drone_photogrammetry_survey": {
        "title": "Drone Aerial Survey, Point Cloud & Topographic Contouring",
        "goal": "Process aerial drone photography into georeferenced DEM, contours, and 3D terrain meshes.",
        "steps": [
            {
                "step": 1,
                "tool": "colmap",
                "role": "Structure from Motion & Dense Reconstruction",
                "action": "Run colmap.bat automatic_reconstructor to extract SIFT keypoints, perform bundle adjustment, and generate dense point cloud."
            },
            {
                "step": 2,
                "tool": "cloudcompare",
                "role": "Point Cloud Filtering & Classification",
                "action": "Execute CloudCompare.exe -SILENT -O cloud.ply -SS SPATIAL 0.05 to downsample noise, classify ground points, and export LAS."
            },
            {
                "step": 3,
                "tool": "qgis",
                "role": "DEM Raster & Topographic Contours",
                "action": "Load ground LAS into QGIS via qgis_agent_mcp, generate 1m/5m elevation contour vectors, and produce high-resolution orthomosaic."
            }
        ]
    },
    "binary_reverse_engineering": {
        "title": "Binary Forensics, Protocol & Reverse Engineering Pipeline",
        "goal": "Triage unknown executable/firmware/APK, extract decompiled source, and analyze network protocols.",
        "steps": [
            {
                "step": 1,
                "tool": "jadx",
                "role": "APK Decompilation (Mobile) or Triage",
                "action": "Execute jadx.bat -d <out_dir> <target.apk> to reconstruct Java source and AndroidManifest.xml."
            },
            {
                "step": 2,
                "tool": "ghidra",
                "role": "Native Decompilation & Symbol Recovery",
                "action": "Run analyzeHeadless.bat on native x64/ARM binary to auto-analyze entry points, recover functions, and export C pseudo-code."
            },
            {
                "step": 3,
                "tool": "wireshark",
                "role": "Live Protocol & Network Inspection",
                "action": "Run tshark.exe to capture and dissect outbound RPC/REST/TLS handshakes and decode payload structures."
            },
            {
                "step": 4,
                "tool": "ppt_master",
                "role": "Forensic Dossier Presentation",
                "action": "Generate executive forensic technical slides documenting vulnerability attack surface and logic flow."
            }
        ]
    }
}

def validate_environment():
    """Check availability of every tool on this machine."""
    report = []
    for app_id, data in APP_REGISTRY.items():
        exists = False
        path = data["cli_path"]
        if path == "ffmpeg":
            exists = True
        elif path and os.path.exists(path):
            exists = True
        
        status = "AVAILABLE" if exists else "NOT FOUND / NEEDS CONFIG"
        report.append({
            "id": app_id,
            "name": data["name"],
            "category": data["category"],
            "interface": data["primary_interface"],
            "status": status,
            "path": path
        })
    return report

def get_sequence(workflow_id):
    """Retrieve optimal tool sequence for a workflow."""
    if workflow_id not in WORKFLOW_SEQUENCES:
        return None
    return WORKFLOW_SEQUENCES[workflow_id]

def main():
    parser = argparse.ArgumentParser(description="PC Tool Sequencer & Execution Engine")
    parser.add_argument("--list-workflows", action="store_true", help="List all available automated workflows")
    parser.add_argument("--sequence", type=str, help="Show tool sequence for a specific workflow key")
    parser.add_argument("--validate", action="store_true", help="Validate all PC application paths & interfaces")
    args = parser.parse_args()

    if args.list_workflows:
        print("\n=== Pre-Engineered Optimal Tool Sequences ===")
        for key, wf in WORKFLOW_SEQUENCES.items():
            print(f"- {key}: {wf['title']}")
        print()
        return

    if args.sequence:
        seq = get_sequence(args.sequence)
        if not seq:
            print(f"Error: Workflow '{args.sequence}' not found. Use --list-workflows.")
            sys.exit(1)
        print(f"\n========================================================")
        print(f" WORKFLOW: {seq['title']}")
        print(f" GOAL: {seq['goal']}")
        print(f"========================================================")
        for s in seq["steps"]:
            tool_info = APP_REGISTRY.get(s["tool"], {})
            print(f"\n[Step {s['step']}] {s['role']} -> Tool: {tool_info.get('name', s['tool'])}")
            print(f"  Interface: {tool_info.get('primary_interface')}")
            print(f"  Command / Action: {s['action']}")
            print(f"  Syntax: {tool_info.get('syntax')}")
        print("\n========================================================\n")
        return

    if args.validate:
        results = validate_environment()
        print("\n=== PC Application Readiness & Interface Status ===")
        print(f"{'App ID':<15} {'Name':<30} {'Interface':<30} {'Status':<15}")
        print("-" * 90)
        for r in results:
            print(f"{r['id']:<15} {r['name']:<30} {r['interface']:<30} {r['status']:<15}")
        print()
        return

    parser.print_help()

if __name__ == "__main__":
    main()
