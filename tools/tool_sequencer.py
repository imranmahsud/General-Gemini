#!/usr/bin/env python3
"""
PC Tool Sequencer & App Orchestration System
Authoritative tool sequence planner, semantic intent matcher, and preflight validator.
Automatically recalls optimal tool sequences without requiring the user to remember tool names.
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
    "visualsfm_cuda": {
        "name": "VisualSFM (CUDA 64-bit)",
        "category": "GPU Structure-from-Motion",
        "primary_interface": "Desktop / Headless CLI",
        "cli_path": r"C:\PortableApps\VisualSFM_windows_cuda_64bit\VisualSFM.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "VisualSFM.exe sfm+pmvs <images_dir> <output.nvm>",
        "docs": "http://ccwu.me/vsfm/"
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

    # 5. Core Media & Document Presentation
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
    },

    # 6. Newly Added & Superior PortableApps
    "losslesscut": {
        "name": "LosslessCut Portable",
        "category": "Lossless Video/Audio Trimmer & Joiner",
        "primary_interface": "Visual & Subprocess Engine",
        "cli_path": r"C:\PortableApps\LosslessCut-win joiner cutter without encode\LosslessCut.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "LosslessCut.exe <video.mp4> (Instant keyframe cut without transcoding)",
        "docs": "https://github.com/mifi/lossless-cut"
    },
    "mkvmerge": {
        "name": "MKVToolNix Multiplexer (mkvmerge)",
        "category": "Lossless Multi-Stream Multiplexing",
        "primary_interface": "Headless CLI (mkvmerge.exe)",
        "cli_path": r"C:\PortableApps\mkvtoolnix\mkvmerge.exe",
        "mcp_server": None,
        "test_cmd": r'"C:\PortableApps\mkvtoolnix\mkvmerge.exe" --version',
        "syntax": "mkvmerge.exe -o <out.mkv> <video.mp4> <audio.m4a> <subs.srt>",
        "docs": "https://mkvtoolnix.download/doc/mkvmerge.html"
    },
    "mkvextract": {
        "name": "MKVToolNix Track Extractor",
        "category": "Elementary Stream Demuxing",
        "primary_interface": "Headless CLI (mkvextract.exe)",
        "cli_path": r"C:\PortableApps\mkvtoolnix\mkvextract.exe",
        "mcp_server": None,
        "test_cmd": r'"C:\PortableApps\mkvtoolnix\mkvextract.exe" --version',
        "syntax": "mkvextract.exe tracks <in.mkv> 0:<video.h264> 1:<audio.aac>",
        "docs": "https://mkvtoolnix.download/doc/mkvextract.html"
    },
    "mkvpropedit": {
        "name": "MKVToolNix In-Place Header Editor",
        "category": "Zero-Rewrite Metadata & Track Modifier",
        "primary_interface": "Headless CLI (mkvpropedit.exe)",
        "cli_path": r"C:\PortableApps\mkvtoolnix\mkvpropedit.exe",
        "mcp_server": None,
        "test_cmd": r'"C:\PortableApps\mkvtoolnix\mkvpropedit.exe" --version',
        "syntax": "mkvpropedit.exe <file.mkv> --edit info --set \"title=<TITLE>\"",
        "docs": "https://mkvtoolnix.download/doc/mkvpropedit.html"
    },
    "antidupl": {
        "name": "AntiDupl.NET Image Deduplicator",
        "category": "Perceptual & Sub-Pixel Duplicate Detection",
        "primary_interface": "Desktop / Automated Scanner",
        "cli_path": r"C:\PortableApps\01-FILE OPERATION APPS\AntiDupl.NET-2.3.12 (Image Duplicate Finder)\AntiDupl.NET-2.3.12\AntiDupl.NET.WinForms.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "AntiDupl.NET.WinForms.exe (Detects blurred, resized, or re-compressed duplicates)",
        "docs": "https://github.com/ermig1979/AntiDupl"
    },
    "clonespy": {
        "name": "CloneSpy Deduplicator",
        "category": "Byte-Level & Hardlink Deduplication",
        "primary_interface": "Desktop / Scripted Batch",
        "cli_path": r"C:\PortableApps\01-FILE OPERATION APPS\CloneSpy\CloneSpy.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "CloneSpy.exe (Replaces identical files with hardlinks/symlinks)",
        "docs": "http://www.clonespy.com/"
    },
    "diffmerge": {
        "name": "DiffMerge Stable",
        "category": "Visual File & Directory Diffing",
        "primary_interface": "Headless CLI / GUI (sgdm.exe)",
        "cli_path": r"C:\PortableApps\01-FILE OPERATION APPS\DiffMerge_4_2_0_697_stable_x86\sgdm.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "sgdm.exe /title1=\"Original\" /title2=\"Modified\" file1 file2",
        "docs": "https://sourcegear.com/diffmerge/"
    },
    "pdftk": {
        "name": "PDFtk Portable",
        "category": "PDF Manipulation & Stamping",
        "primary_interface": "Headless CLI (pdftk.exe)",
        "cli_path": r"C:\PortableApps\PDFTKBuilderPortable\App\pdftkbuilder\pdftk.exe",
        "mcp_server": None,
        "test_cmd": r'"C:\PortableApps\PDFTKBuilderPortable\App\pdftkbuilder\pdftk.exe" --version',
        "syntax": "pdftk.exe in1.pdf in2.pdf cat output combined.pdf",
        "docs": "https://www.pdflabs.com/docs/pdftk-man-page/"
    },
    "realesrgan": {
        "name": "Real-ESRGAN Vulkan AI",
        "category": "AI Super-Resolution Upscaling",
        "primary_interface": "Headless CLI (realesrgan-ncnn-vulkan.exe)",
        "cli_path": r"C:\PortableApps\Shutter Encoder 19.2 Windows 64bits\Library\realesrgan-ncnn-vulkan.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "realesrgan-ncnn-vulkan.exe -i <input.png> -o <upscaled.png> -s 4",
        "docs": "https://github.com/xinntao/Real-ESRGAN"
    },
    "mediainfo": {
        "name": "MediaInfo CLI",
        "category": "Media Stream & Codec Inspection",
        "primary_interface": "Headless CLI (MediaInfo.exe)",
        "cli_path": r"C:\PortableApps\Shutter Encoder 19.2 Windows 64bits\Library\MediaInfo.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "MediaInfo.exe --Output=JSON <media_file.mp4>",
        "docs": "https://mediaarea.net/en/MediaInfo/Support/FAQ"
    },
    "ytdlp": {
        "name": "yt-dlp Portable",
        "category": "Media Stream & Asset Downloader",
        "primary_interface": "Headless CLI (yt-dlp.exe)",
        "cli_path": r"C:\PortableApps\Shutter Encoder 19.2 Windows 64bits\Library\yt-dlp.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "yt-dlp.exe -f bestvideo+bestaudio/best <URL>",
        "docs": "https://github.com/yt-dlp/yt-dlp"
    },
    "irfanview": {
        "name": "IrfanView x64",
        "category": "Batch Image Processing & Conversion",
        "primary_interface": "Headless CLI (i_view64.exe)",
        "cli_path": r"C:\PortableApps\irfanview462_x64\i_view64.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "i_view64.exe <input.png> /resize=(1920,1080) /aspectratio /convert=<out.webp>",
        "docs": "https://www.irfanview.com/main_what_is_engl.htm"
    },
    "arenc": {
        "name": "Advanced Renamer CLI",
        "category": "Batch Renaming & EXIF Reorganization",
        "primary_interface": "Headless CLI (arenc.exe)",
        "cli_path": r"C:\PortableApps\Advanced renamer portable\arenc.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "arenc.exe -p <rules.aren> -s <source_dir> -d <target_dir>",
        "docs": "https://www.advancedrenamer.com/user_guide/commandline"
    },
    "mp3gain": {
        "name": "MP3Gain CLI",
        "category": "Lossless Audio Loudness Normalization",
        "primary_interface": "Headless CLI (mp3gain.exe)",
        "cli_path": r"C:\PortableApps\mp3gain-win-full-1_2_5\mp3gain.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "mp3gain.exe -r -k -d 0 <narration.mp3>",
        "docs": "http://mp3gain.sourceforge.net/"
    },
    "imagej": {
        "name": "ImageJ (NIH)",
        "category": "Scientific Image Analysis & Morphometry",
        "primary_interface": "Macro Scripting CLI (ImageJ.exe)",
        "cli_path": r"C:\PortableApps\ImageJ\ImageJ.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "ImageJ.exe -macro <measure.ijm> <image.tif>",
        "docs": "https://imagej.net/scripting/macro"
    },
    "everything": {
        "name": "Everything Portable",
        "category": "Instant NTFS File Indexing",
        "primary_interface": "Headless CLI (Everything.exe)",
        "cli_path": r"C:\PortableApps\Everything-1.4.1.928.x64\Everything.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "Everything.exe -search <query> -export-csv <results.csv>",
        "docs": "https://www.voidtools.com/support/everything/command_line_options/"
    },
    "exiftool_portable": {
        "name": "ExifTool Portable",
        "category": "Geotagging & Metadata Extraction",
        "primary_interface": "Headless CLI (exiftool.exe)",
        "cli_path": r"C:\PortableApps\geosetter\tools\exiftool.exe",
        "mcp_server": None,
        "test_cmd": None,
        "syntax": "exiftool.exe -geotag=<track.gpx> -overwrite_original <images_dir>",
        "docs": "https://exiftool.org/"
    }
}

WORKFLOW_SEQUENCES = {
    # 1. Superior Lossless Video Pipeline
    "lossless_video_slicing_multiplexing": {
        "title": "Lossless Video Slicing & MKV Multiplexing Pipeline",
        "goal": "Trim, cut, and multiplex multi-track video, voiceover, and subtitles in seconds with ZERO re-encoding and ZERO quality loss.",
        "keywords": ["cut video", "trim video", "lossless cut", "join clips", "mkv", "merge audio video", "subtitles", "fast video edit"],
        "superiority_reason": "50x faster than FFmpeg transcoding; preserves 100% original pixel quality and avoids CPU/GPU thermal load by cutting on keyframes and remuxing stream packets directly.",
        "steps": [
            {
                "step": 1,
                "tool": "losslesscut",
                "role": "Lossless Keyframe Slicing & Trimming",
                "action": "Use LosslessCut to isolate scenes at I-frame boundaries; export cut segments with zero generation loss."
            },
            {
                "step": 2,
                "tool": "mp3gain",
                "role": "Lossless Audio Leveling",
                "action": "Execute mp3gain.exe -r -k -d 0 on voiceover narration track to normalize peak loudness."
            },
            {
                "step": 3,
                "tool": "mkvmerge",
                "role": "Ultra-Fast Multi-Stream Multiplexing",
                "action": "Run mkvmerge.exe -o final_master.mkv --default-track 0:yes cut_video.mp4 --language 0:eng narration.mp3 --language 0:eng subtitles.srt."
            },
            {
                "step": 4,
                "tool": "mkvpropedit",
                "role": "In-Place Header Tag Injection",
                "action": "Execute mkvpropedit.exe final_master.mkv --edit info --set \"title=Project Master Deliverable\" in 5 milliseconds without rewriting multi-GB file."
            },
            {
                "step": 5,
                "tool": "mediainfo",
                "role": "Automated Quality Control Gate",
                "action": "Run MediaInfo.exe --Output=JSON final_master.mkv to verify sync, frame rates, and bitrates."
            }
        ]
    },

    # 2. Perceptual Image & Survey Deduplication
    "perceptual_image_survey_deduplication": {
        "title": "Perceptual Image & Survey Photo Deduplication Pipeline",
        "goal": "Purge duplicate drone survey photos, site inspections, and CAD textures even if resized, re-compressed, or slightly cropped.",
        "keywords": ["duplicate images", "photo duplicates", "clean photos", "deduplicate", "survey images", "similar pictures"],
        "superiority_reason": "Standard MD5/SHA256 checksums fail when images are resized or re-compressed; AntiDupl uses perceptual sub-pixel algorithms to catch defective or redundant photos.",
        "steps": [
            {
                "step": 1,
                "tool": "everything",
                "role": "Instant File Discovery",
                "action": "Execute Everything.exe -search \"ext:jpg;png;tif D:\\Survey\" -export-csv survey_manifest.csv in under 1 second."
            },
            {
                "step": 2,
                "tool": "antidupl",
                "role": "Perceptual Sub-Pixel Deduplication",
                "action": "Run AntiDupl.NET on target image repository to identify blurred, defective, and near-identical captures."
            },
            {
                "step": 3,
                "tool": "exiftool_portable",
                "role": "Telemetry GPS Integrity Audit",
                "action": "Run exiftool.exe on surviving photos to confirm valid GPS Latitude/Longitude and camera timestamps."
            }
        ]
    },

    # 3. Clean Stream Demuxing & Repurposing
    "clean_stream_demuxing_repurposing": {
        "title": "Lossless Stream Demuxing & Asset Repurposing Pipeline",
        "goal": "Extract pristine raw video streams, multi-language audio stems, and subtitles from container files without re-encoding.",
        "keywords": ["extract audio", "demux", "extract stream", "rip audio", "extract subtitles", "split mkv"],
        "superiority_reason": "Demuxes byte-exact bitstreams without re-compression degradation; avoids FFmpeg container drift.",
        "steps": [
            {
                "step": 1,
                "tool": "mediainfo",
                "role": "Container Track Identification",
                "action": "Inspect input file with MediaInfo.exe to locate track indices (Video ID 0, Audio ID 1, Subtitle ID 2)."
            },
            {
                "step": 2,
                "tool": "mkvextract",
                "role": "Pristine Elementary Stream Extraction",
                "action": "Execute mkvextract.exe tracks source.mkv 0:video_raw.h264 1:narration_clean.aac 2:timing.srt."
            },
            {
                "step": 3,
                "tool": "mp3gain",
                "role": "Voice Track Loudness Normalization",
                "action": "Level extracted narration loudness losslessly with mp3gain.exe."
            }
        ]
    },

    # 4. Flood Hazard Assessment
    "flood_hazard_assessment": {
        "title": "Flood Hazard Modeling & Costed Protection Bund Workflow",
        "goal": "From raw DEM and rainfall data to 2D hydrodynamic simulation, risk mapping, and KPK MRS BOQ.",
        "keywords": ["flood", "hec-ras", "hecras", "river", "inundation", "bund", "embankment", "stone pitching", "swmm", "hydraulics"],
        "superiority_reason": "Contract-bound automation via QGIS Agent MCP, headless SWMM, and HEC-RAS MCP with integrated KPK MRS-2025 rates.",
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

    # 5. Water Supply Distribution
    "water_supply_distribution": {
        "title": "Pressurized Water Supply Distribution Network Workflow",
        "goal": "Design, hydraulic simulation, profile drawings, and material takeoffs.",
        "keywords": ["water supply", "pipe network", "epanet", "water distribution", "trench", "pipeline", "sluice valve"],
        "superiority_reason": "Links GIS spatial terrain nodes directly to EPANET solver, AutoCAD core console, and KPK MRS pipe schedules.",
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

    # 6. Architectural BIM & Walkthrough
    "architectural_bim_visualization": {
        "title": "Architectural Design, BIM & Hyper-Realistic Animation Workflow",
        "goal": "From conceptual layout to BIM compliance and cinematic client walkthrough.",
        "keywords": ["bim", "architecture", "revit", "freecad", "sketchup", "sweethome3d", "blender", "rendering", "walkthrough"],
        "superiority_reason": "Combines rapid Sweet Home 3D space planning with FreeCAD/Revit BIM intelligence and Blender 5.2 Cycles renders.",
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

    # 7. Drone Aerial Geotagging & GPU Photogrammetry
    "drone_geotag_photogrammetry": {
        "title": "Drone Aerial Geotagging & GPU Photogrammetry Pipeline",
        "goal": "Reconcile flight telemetry GPS logs with aerial imagery, solve dense point clouds, and produce terrain models.",
        "keywords": ["drone", "uav", "photogrammetry", "colmap", "visualsfm", "geotag", "point cloud", "dem", "contours", "ortho"],
        "superiority_reason": "Hardware-accelerated CUDA SiftGPU via VisualSFM and COLMAP with automated CloudCompare ground decimation.",
        "steps": [
            {
                "step": 1,
                "tool": "exiftool_portable",
                "role": "Telemetry GPS Time-Sync Geotagging",
                "action": "Execute exiftool.exe -geotag=flight_telemetry.gpx -overwrite_original ./drone_raw_images/ to embed WGS84 coordinates."
            },
            {
                "step": 2,
                "tool": "visualsfm_cuda",
                "role": "GPU Structure-from-Motion & Dense Stereo",
                "action": "Run VisualSFM.exe / colmap.bat to extract keypoints with CUDA acceleration and reconstruct dense point cloud."
            },
            {
                "step": 3,
                "tool": "cloudcompare",
                "role": "Cloud Decimation & Noise Stripping",
                "action": "Execute CloudCompare.exe -SILENT -O dense.ply -SS SPATIAL 0.05 to clean artifacts and export LAS."
            },
            {
                "step": 4,
                "tool": "qgis",
                "role": "Orthomosaic & Contour Generation",
                "action": "Load ground LAS into QGIS via qgis_agent_mcp to generate 1m topographic contours."
            }
        ]
    },

    # 8. Engineering Tender Dossier & PDF Assembly
    "pdf_engineering_dossier": {
        "title": "Engineering Technical Dossier & PDF Assembly Workflow",
        "goal": "Compile calculation sheets, drawings, and BOQ into a unified, watermarked, stamped PDF portfolio.",
        "keywords": ["pdf", "pdftk", "merge pdf", "watermark", "stamp", "dossier", "tender document", "boq print"],
        "superiority_reason": "Zero-dependency native PDFtk execution; processes thousands of pages in seconds without Acrobat subscription overhead.",
        "steps": [
            {
                "step": 1,
                "tool": "autocad",
                "role": "CAD Drawing Sheet Export",
                "action": "Run accoreconsole.exe to batch-plot DWG sheets into vector PDF layouts."
            },
            {
                "step": 2,
                "tool": "pdftk",
                "role": "Multi-Source PDF Collation & Merging",
                "action": "Execute pdftk.exe cover.pdf specs.pdf drawings.pdf boq.pdf cat output project_master.pdf."
            },
            {
                "step": 3,
                "tool": "pdftk",
                "role": "Confidential Watermarking & Page Numbering",
                "action": "Execute pdftk.exe project_master.pdf multistamp watermark.pdf output project_dossier_stamped.pdf."
            },
            {
                "step": 4,
                "tool": "irfanview",
                "role": "Executive Thumbnail & Preview Generation",
                "action": "Run i_view64.exe to render high-contrast cover thumbnails for proposal submissions."
            }
        ]
    },

    # 9. AI Super-Resolution Media Enhancement
    "ai_media_enhancement": {
        "title": "Audio Normalization & Real-ESRGAN AI Super-Resolution Workflow",
        "goal": "Produce broadcast-grade documentary footage, upscale historical maps/renderings, and level voiceover tracks.",
        "keywords": ["upscale", "super resolution", "realesrgan", "voiceover", "mp3gain", "audio level", "remux", "ytdlp"],
        "superiority_reason": "Leverages GPU Vulkan AI inference for 4x resolution reconstruction and ReplayGain mathematical loudness correction.",
        "steps": [
            {
                "step": 1,
                "tool": "ytdlp",
                "role": "Reference Footage Retrieval",
                "action": "Execute yt-dlp.exe to download high-bitrate reference satellite and documentary footage."
            },
            {
                "step": 2,
                "tool": "realesrgan",
                "role": "AI 4x Super-Resolution Upscaling",
                "action": "Execute realesrgan-ncnn-vulkan.exe -i lowres_map.png -o highres_map.png -s 4 to reconstruct fine line work."
            },
            {
                "step": 3,
                "tool": "mp3gain",
                "role": "Lossless Audio Loudness Leveling",
                "action": "Execute mp3gain.exe -r -k -d 0 narration.mp3 to achieve standard ReplayGain broadcast loudness."
            },
            {
                "step": 4,
                "tool": "ffmpeg",
                "role": "Bitexact Final Master Assembly",
                "action": "Run ffmpeg with -map_metadata -1 -fflags +bitexact to assemble final documentary clip without tool footprints."
            },
            {
                "step": 5,
                "tool": "mediainfo",
                "role": "Automated Quality Control Gate",
                "action": "Execute MediaInfo.exe --Output=JSON master.mp4 to verify frame rate, color space, and codec compliance."
            }
        ]
    },

    # 10. Binary Reverse Engineering
    "binary_reverse_engineering": {
        "title": "Binary Forensics, Protocol & Reverse Engineering Pipeline",
        "goal": "Triage unknown executable/firmware/APK, extract decompiled source, and analyze network protocols.",
        "keywords": ["reverse engineering", "ghidra", "jadx", "apk", "decompile", "disassemble", "wireshark", "tshark", "binary"],
        "superiority_reason": "Headless Ghidra decompilation coupled with real-time TShark protocol packet dissection.",
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

def find_best_sequence(query_str):
    """Semantic match from natural language intent to optimal sequence."""
    query_lower = query_str.lower().strip()
    scores = []
    for key, wf in WORKFLOW_SEQUENCES.items():
        score = 0
        title_lower = wf["title"].lower()
        goal_lower = wf["goal"].lower()
        keywords = wf.get("keywords", [])
        
        for word in query_lower.split():
            if word in title_lower:
                score += 3
            if word in goal_lower:
                score += 2
            for kw in keywords:
                if word in kw:
                    score += 4
                if kw in query_lower:
                    score += 6
        if score > 0:
            scores.append((score, key, wf))
    
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores

def print_workflow_details(key, seq):
    print(f"\n========================================================")
    print(f" WORKFLOW IDENTIFIED: {seq['title']}")
    print(f" GOAL: {seq['goal']}")
    print(f" WHY THIS IS SUPERIOR: {seq.get('superiority_reason', 'Optimized execution')}")
    print(f"========================================================")
    for s in seq["steps"]:
        tool_info = APP_REGISTRY.get(s["tool"], {})
        print(f"\n[Step {s['step']}] {s['role']} -> Tool: {tool_info.get('name', s['tool'])}")
        print(f"  Interface: {tool_info.get('primary_interface')}")
        print(f"  Command / Action: {s['action']}")
        print(f"  Syntax: {tool_info.get('syntax')}")
    print("\n========================================================\n")

def main():
    parser = argparse.ArgumentParser(description="PC Tool Sequencer & Semantic Intent Recall Engine")
    parser.add_argument("--list-workflows", action="store_true", help="List all available automated workflows")
    parser.add_argument("--sequence", type=str, help="Show tool sequence for a specific workflow key")
    parser.add_argument("--find", type=str, help="Natural language query to recall optimal tool sequence")
    parser.add_argument("--validate", action="store_true", help="Validate all PC application paths & interfaces")
    args = parser.parse_args()

    if args.list_workflows:
        print("\n=== Pre-Engineered Optimal Tool Sequences ===")
        for key, wf in WORKFLOW_SEQUENCES.items():
            print(f"- {key}: {wf['title']}")
        print()
        return

    if args.find:
        matches = find_best_sequence(args.find)
        if not matches:
            print(f"\nNo exact match for '{args.find}'. Listing all workflows:")
            for key, wf in WORKFLOW_SEQUENCES.items():
                print(f"- {key}: {wf['title']}")
            print()
            return
        best_score, best_key, best_wf = matches[0]
        print_workflow_details(best_key, best_wf)
        if len(matches) > 1:
            print("Alternative matching workflows:")
            for s, k, w in matches[1:4]:
                print(f"  * {k}: {w['title']}")
            print()
        return

    if args.sequence:
        seq = WORKFLOW_SEQUENCES.get(args.sequence)
        if not seq:
            print(f"Error: Workflow '{args.sequence}' not found. Use --list-workflows.")
            sys.exit(1)
        print_workflow_details(args.sequence, seq)
        return

    if args.validate:
        results = validate_environment()
        print("\n=== PC Application Readiness & Interface Status ===")
        print(f"{'App ID':<20} {'Name':<35} {'Interface':<35} {'Status':<15}")
        print("-" * 110)
        for r in results:
            print(f"{r['id']:<20} {r['name']:<35} {r['interface']:<35} {r['status']:<15}")
        print()
        return

    parser.print_help()

if __name__ == "__main__":
    main()
