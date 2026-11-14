# Applications & Software Inventory (APPS_LIST)

This document provides the complete, authoritative software inventory required to replicate the full Google Antigravity, Gemini agent skills, CAD/BIM modeling mastery, and reverse-engineering toolchains on any Windows machine.

---

## ⚡ Quick One-Click Installation

To automatically install the essential developer runtimes, package managers, and reverse engineering tools via Chocolatey:

```powershell
# Open an elevated PowerShell session (Run as Administrator):
powershell -ExecutionPolicy Bypass -File .\install-apps.ps1
```

Once installed, deploy all agent skills and plugins:
```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

---

## 🛠️ Categorized Software & Toolchain Matrix

### 1. Antigravity & AI Agent Core Runtimes
| Software / Tool | Version Tested | Purpose | Installation Command / Link |
| :--- | :--- | :--- | :--- |
| **Google Antigravity IDE** | 2.26.0+ | Primary agentic AI coding environment | Installed via Google internal / installer |
| **pnpm** | 12.16+ | Fast disk-efficient package manager for agent IDEs | `npm install -g --allow-scripts=pnpm pnpm` |
| **Git for Windows** | 2.53+ | Version control & skill repo sync | `choco install git -y` or `winget install Git.Git` |
| **GitHub CLI (`gh`)** | 2.103.3 | GitHub authentication, PR creation & worktree review | `winget install GitHub.cli` (installed in `Program Files\GitHub CLI`) |
| **Python** | 3.12 / 3.14.7 | Agent scripting, BigFrames, ML & science | `choco install python -y` or `winget install Python.Python.3.12` |
| **Astral uv** | 0.9+ | High-performance Python package manager | `powershell -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| **Node.js (LTS)** | 22.x+ | REA server, MCP servers, web guidance | `choco install nodejs-lts -y` |
| **Java Development Kit (JDK)** | 21 LTS | Sweet Home 3D plugin SDK, Ghidra runtime | `choco install openjdk21 -y` |
| **.NET SDK** | 10 / 8.0 | Revit 2027 C# Add-in development | `winget install Microsoft.DotNet.SDK.10` |
| **Visual Studio Build Tools** | 2026 (18.9) | C++ compilation, native module builds | `choco install visualstudio2026buildtools -y` |
| **Visual Studio Code** | 1.143+ | Code editing, extension host, terminal | `winget install Microsoft.VisualStudioCode` |
| **Ollama** | 0.40.15+ | Local offline LLM inference engine (Qwen 3.5 4B) | `winget install Ollama.Ollama` & `ollama pull qwen3.5:4b` |
| **CLI-Anything & cli-hub** | 0.4.1 | Headless CLI generation & app automation harnesses for agents (QGIS, Blender, FreeCAD) | `C:\tools\cli-anything\cli-hub` (`cli-hub`) |
| **Agent Skills (Addy Osmani)** | 1.0.0 | Spec-driven development, planning, task breakdown & verification agent framework | `C:\tools\agent-skills` & `.gemini/config/skills` |

---

### 2. Reverse Engineering & Binary Analysis (REA Suite)
Integrated directly with `reverse-engineer-anything`, `rea-analysis-optimization`, and `rea-tool-design`.

| Tool | Version | Role in Agentic Workflow | Installation / Location |
| :--- | :--- | :--- | :--- |
| **Ghidra** | 12.2.0 | Disassembly, decompilation, headless analysis | `choco install ghidra -y` |
| **Wireshark** | 4.6.9 | Network packet capture & protocol inspection | `choco install wireshark -y` |
| **JADX & JADX GUI** | 1.5.6 | Android DEX / APK decompilation | `choco install jadx -y` |
| **Android ADB** | 37.0.0 | Device inspection, logcat, shell control | `choco install adb -y` |
| **Apktool** | 3.0.3 | Android resource decoding and rebuilding | `choco install apktool -y` |
| **API Monitor** | 2.13.0 | Real-time Win32 / API call interception | `choco install apimonitor -y` |
| **x64dbg / x32dbg** | Latest | Windows interactive native debugging | `C:\tools\x64dbg` or `choco install x64dbg` |
| **Rizin & Cutter** | Latest | Disassembly engine & Cutter GUI interface | `C:\tools\rizin` & `C:\tools\cutter` |
| **ImHex** | Latest | Interactive hex editor & pattern language | `C:\tools\imhex` |
| **IDA Pro / Free MCP** | Bridge | MCP communication bridge to Hex-Rays IDA | `C:\tools\ida-pro-mcp` & `C:\tools\ida-free-mcp` |
| **Decomp-compat-kit** | Tooling | Byte-level decompilation equivalence testing | `C:\tools\decomp-compat-kit` |
| **JADX Headless MCP** | 0.7.1 | MCP headless server for APK analysis | `C:\tools\jadx-headless-mcp-0.7.1-all.jar` |

---

### 3. CAD, BIM & Architectural Modeling Suite
Governed by `cad-bim-drawing-mastery`, `architectural-plan-designer`, and `furniture-fit`.

| Application | Target Version | Workflow Role | Acquisition / Setup |
| :--- | :--- | :--- | :--- |
| **Autodesk Revit** | **2027** (or 2026) | Parametric BIM, system families, Dynamo 4.0 | Autodesk Portal / Educational license |
| **Trimble SketchUp Pro**| **2026** (or 2025) | Surface push-pull drafting, LayOut drawings | [SketchUp.com](https://www.sketchup.com) |
| **Sweet Home 3D** | **7.5** / 8.0 | Space planning, interior drafting, `.sh3d` | `winget install SpaceMushrooms.SweetHome3D` |
| **FreeCAD** | **1.1.3** | Open-source parametric 3D CAD modeling | `winget install FreeCAD.FreeCAD` |
| **QGIS** | **4.2.1** | Geospatial, terrain mapping & shapefiles | `winget install OSGeo.QGIS` |
| **AutoCAD** | **2006** / TrueView | Legacy DWG review and express tools | Autodesk Portal / Archive |
| **RevitPythonShell** | 2.2.0 | Live interactive Python execution in Revit | `RevitPythonShell.msi` |
| **Bim.com Design App** | 0.8.19 | BIMobject architectural model catalog | Direct installer |

---

### 4. Cloud, BigQuery & Data Engineering (Data Agent Kit)
| Tool / SDK | Purpose | Installation |
| :--- | :--- | :--- |
| **Google Cloud SDK (`gcloud` & `bq`)** | BigQuery, Cloud Storage, Dataproc Spark, Composer | `choco install gcloudsdk -y` or `winget install Google.CloudSDK` |
| **BigFrames (bigquery-dataframes)** | Pythonic pandas/scikit-learn on BigQuery | `uv pip install bigframes` |
| **dbt-bigquery** | Data build tool pipeline modeling | `uv pip install dbt-bigquery` |
| **Dataform CLI** | In-warehouse SQLX transformations | `npm install -g @dataform/cli` |
| **Apache Airflow Client** | Cloud Composer orchestration inspection | `uv pip install apache-airflow-client` |

---

### 5. Mobile & Frontend Frameworks
| Tool / SDK | Purpose | Installation |
| :--- | :--- | :--- |
| **Flutter SDK** | Cross-platform UI development & testing | [flutter.dev/get-started/install/windows](https://docs.flutter.dev/get-started/install/windows) |
| **Dart SDK** | CLI tools, pattern matching, `dart analyze` | Included with Flutter |
| **Android Studio** | Android emulator, SDK manager, layout inspector | `winget install Google.AndroidStudio` |

---

### 6. Science, Biomedical & OCR Toolchain
| Tool | Purpose | Installation |
| :--- | :--- | :--- |
| **Tesseract-OCR** | Screen capture OCR, automated monitoring | `C:\Program Files\Tesseract-OCR` |
| **Biomolecular Mol*** | 3D Protein structure visualization sidecar | Included in `plugins/science/sidecars` |
| **ChEMBL / UniProt / NCBI** | Python biomedical query toolkits | Managed via uv scripts in `plugins/science` |

---

### 7. Essential Utilities
| Tool | Purpose | Command |
| :--- | :--- | :--- |
| **Blip** | Fast direct device-to-device file transfer (Windows & Android mobile) | `winget install --id 9N7JSXC1SJK6 --source msstore` |
| **Syncthing** | Continuous encrypted P2P folder synchronization | `winget install BillStewart.SyncthingWindowsSetup` |
| **AutoHotkey v2** | Screen automation, global hotkeys | `choco install autohotkey -y` |
| **SumatraPDF** | Ultra-fast lightweight PDF review | `choco install sumatrapdf -y` |
| **7-Zip** | Archive decompression (tar, gz, zip, 7z) | `choco install 7zip -y` |
| **WSL 2** | Linux environment for cross-platform workflows | `wsl --install` |
| **witr** | Process & port launch-chain inspector (systemd, docker, PM2 to PID) | `winget install PranshuParmar.witr` (`witr`) |
| **Mister Download Manager (MDM)** | Open-source Rust IDM replacement with multi-segment downloads, headless daemon & CLI | `C:\tools\misterdownloadmanager` (`mdm-cli` 0.5.2) |

---

---

### 8. Business Intelligence & Data Visualization
| Tool / Platform | Purpose | Command / Installation |
| :--- | :--- | :--- |
| **QGIS 4.x / 3.x** | GIS mapping, cartography, elevation models | `winget install QGIS.QGIS` |

---

### 9. Civil, Water, Hydraulics & River Engineering
| Tool / Package | Purpose | Installation / Command |
| :--- | :--- | :--- |
| **PySWMM** | US EPA Stormwater Management Model Python API | pip install pyswmm |
| **swmmio** | Drainage network bottleneck analysis & GeoJSON export | pip install swmmio |
| **WNTR** | US EPA Water Network Tool for Resilience (EPANET) | pip install wntr |
| **WhiteboxTools** | Headless GIS hydrology & digital elevation processing | pip install whitebox |
| **open_channel** | Python open-channel hydraulics (Manning, GVF, jumps) | Cloned in C:\\tools\\civil-hydraulics\\open_channel |
| **ChannelFlowLib** | Channel geometry and Manning cross-section library | Cloned in C:\\tools\\civil-hydraulics\\ChannelFlowLib |
| **PyQGIS Cookbook** | Automated headless QGIS scripting recipes | Cloned in C:\\tools\\qgis-civil\\qgis-cookbook |
| **canal-and-drain-hydraulics** | Lacey alluvial regime, Kennedy CVR & drain design | Agent skill in skills/canal-and-drain-hydraulics |
| **river-training-and-flood-protection** | Spurs, guide bunds, Lacey scour, launching apron | Agent skill in skills/river-training-and-flood-protection |
| **civil-boq-and-cost-estimation** | CSR/NHA item rate analysis, mass-haul & BOQs | Agent skill in skills/civil-boq-and-cost-estimation |

---

### 10. Rust Toolchains & Agent Compilation Stack
| Tool / Binary | Purpose | Installation / Command |
| :--- | :--- | :--- |
| **rust-analyzer** | Official Rust Language Server Protocol (LSP) | `rustup component add rust-analyzer` |
| **cargo-nextest** | Isolated next-gen test runner with JSON reporting | `winget install nextest.cargo-nextest` |
| **sccache** | Mozilla compiler cache for rapid incremental rebuilds | `winget install Mozilla.sccache` |
| **cargo-expand** | Macro expansion debugger for derive & proc macros | `cargo binstall cargo-expand` |
| **cargo-audit** | Vulnerability security scanner (RustSec Advisory DB) | `cargo binstall cargo-audit` |
| **cargo-deny** | Dependency graph, licensing & crate ban auditor | `cargo binstall cargo-deny` |
| **rust-mcp-server** | 33-tool Model Context Protocol server for Rust | Built to `~/.cargo/bin/rust-mcp-server.exe` |

---

### 11. Technical Report Writing & PC-1 Feasibility
| Tool / Package | Purpose | Installation / Command |
| :--- | :--- | :--- |
| **Typst Compiler** | Lightning-fast markup typesetter for reports | `winget install Typst.Typst` |
| **modern-project-report** | Engineering project report framework | `typst init @preview/modern-project-report` |
| **reprobe / breezy-report** | Two-column and modular technical report templates | Cloned in `C:\tools\engineering-reports\` |

---

### 12. Media AI, Audiobook Generation & Video Localization Suite
| Tool / Package | Purpose | Installation / Command |
| :--- | :--- | :--- |
| **FFmpeg** | Multimedia transcoding, muxing, audio processing & subtitle burning | `choco install ffmpeg -y` |
| **audiblez** | Offline neural audiobook compiler from EPUB/PDF (Kokoro-82M TTS) | `pip install audiblez` & `C:\tools\media-ai\audiblez` |
| **rembg** | Zero-cloud AI image background removal (U2-Net, ONNX Runtime) | `pip install "rembg[cpu,cli]"` & `C:\tools\media-ai\rembg` |
| **pyVideoTrans** | Multilingual video translation, voice dubbing & subtitle sync (Whisper + Edge-TTS) | Cloned in `C:\tools\media-ai\pyvideotrans` (`uv run webui.py`) |
| **audiblez skill** | Agent skill for neural audiobook conversion | Agent skill in `skills/audiblez` |
| **rembg-cli skill** | Agent skill for photo background cutout | Agent skill in `skills/rembg-cli` |
| **pyvideotrans skill** | Agent skill for video dubbing & subtitle workflows | Agent skill in `skills/pyvideotrans` |
| **MoneyPrinterTurbo** | Automated AI video generator (LLM scripts + Edge TTS + auto-subtitles + 9:16 rendering) | Cloned to `D:\AI-Folders\MoneyPrinterTurbo`, skill in `skills/moneyprinterturbo` |
| **OpenWhispr** | Privacy-first local voice-to-text dictation, meeting notes & audio transcription | Installed in `C:\Users\Imran\AppData\Local\Programs\OpenWhispr\OpenWhispr.exe` |
| **Remotion** | Programmatic React-based deterministic video rendering engine | Global npm package `@remotion/cli` & `remotion` (`remotion.cmd`) |
| **HyperFrames** | HTML/CSS and GSAP timeline to MP4/WebM video compiler | Global npm package `hyperframes` (`hyperframes.cmd`) |
| **Faster-Whisper** | Fast, offline word-level timestamped subtitle extractor on CPU (int8) | CLI tool `whisper-ctranslate2` (`uv tool install --python 3.12 whisper-ctranslate2`) |
| **character-timeline-animation skill** | Agent skill for 2D/3D character design consistency & 5-parameter timeline prompts | Agent skill in `skills/character-timeline-animation` |
| **programmatic-video skill** | Agent skill for headless code-to-video and subtitle workflows | Agent skill in `skills/programmatic-video` |
| **Fuobe** | ComfyUI-powered open creative studio with Next.js frontend & 22 media creation skills | Cloned in `C:\tools\fuobe` & skills in `skills/` |

---

### 13. Photogrammetry & 3D Reconstruction Suite
| Tool / Package | Version | Purpose | Installation / Location |
| :--- | :--- | :--- | :--- |
| **VisualSFM** | 0.5.26 | Fast Structure from Motion (SfM) GUI & CLI | `C:\tools\photogrammetry\VisualSFM\VisualSFM.exe` |
| **CMVS / PMVS2** | Win64-VS2010 | Clustering View for Multi-view Stereo & dense point cloud reconstruction | Installed directly into `C:\tools\photogrammetry\VisualSFM\` (`cmvs.exe`, `pmvs2.exe`, `genOption.exe`) |
| **COLMAP** | 4.2.1 (CPU / No-CUDA) | General-purpose Structure-from-Motion (SfM) and Multi-View Stereo (MVS) pipeline | `C:\tools\photogrammetry\COLMAP\bin\colmap.exe` & `COLMAP.bat` |
| **MeshLab** | 2025.07 | 3D triangular mesh and point cloud processing, cleaning, and Poisson reconstruction | `C:\Program Files\VCG\MeshLab\meshlab.exe` |
| **Awesome Photogrammetry** | Latest | Curated knowledge base of photogrammetry tools, libraries, and benchmarks | `C:\tools\photogrammetry\awesome-photogrammetry` |
| **Python 3D Toolkit** | Latest | Point cloud and mesh manipulation (`trimesh`, `scipy`, `numpy`, `plyfile`, `laspy`) | Installed in Python 3.12 environment |

---

### 14. Portable Applications & Automation Suite (`C:\PortableApps`)
| Application | Version | Role in Orchestrated Workflows | Verified Executable Path |
| :--- | :--- | :--- | :--- |
| **PDFtk Portable** | 1.41 | Headless PDF merging, bursting, watermarking, stamping | `C:\PortableApps\PDFTKBuilderPortable\App\pdftkbuilder\pdftk.exe` |
| **Real-ESRGAN Vulkan** | Latest | AI 4x super-resolution upscaling for images & frames | `C:\PortableApps\Shutter Encoder 19.2 Windows 64bits\Library\realesrgan-ncnn-vulkan.exe` |
| **MediaInfo CLI** | Latest | Audiovisual stream, container & codec QC audit | `C:\PortableApps\Shutter Encoder 19.2 Windows 64bits\Library\MediaInfo.exe` |
| **yt-dlp Portable** | 2026.10.26 | High-bitrate video, audio & stream asset downloader (updated in-place) | `C:\PortableApps\Shutter Encoder 19.2 Windows 64bits\Library\yt-dlp.exe` |
| **IrfanView x64** | 4.62 | Headless batch image resizing, format conversion & crop | `C:\PortableApps\irfanview462_x64\i_view64.exe` |
| **Advanced Renamer** | 3.80 | Headless regex file & folder batch renaming | `C:\PortableApps\Advanced renamer portable\arenc.exe` |
| **MP3Gain** | 1.4.6 | ReplayGain lossless volume normalization | `C:\PortableApps\mp3gain-win-full-1_2_5\mp3gain.exe` |
| **ImageJ (NIH)** | 1.50 | Scientific image analysis, segmentation & macro scripting | `C:\PortableApps\ImageJ\ImageJ.exe` |
| **Everything Search** | 1.4.1.1032 | Sub-second NTFS index search & CSV export (updated in-place) | `C:\PortableApps\Everything-1.4.1.928.x64\Everything.exe` |
| **ExifTool Portable** | Latest | Camera EXIF & GPS flight telemetry sync engine | `C:\PortableApps\geosetter\tools\exiftool.exe` |
| **LosslessCut Portable** | 3.70.2 | Lossless I-frame accurate video & audio cutting (updated in-place) | `C:\PortableApps\LosslessCut-win joiner cutter without encode\LosslessCut.exe` |
| **MKVToolNix Suite** | 103.0 | Reference Matroska mkvmerge, mkvextract & mkvpropedit (updated in-place) | `C:\PortableApps\mkvtoolnix\mkvmerge.exe` |
| **AntiDupl.NET** | 2.3.12 | Perceptual sub-pixel image & survey duplicate finder | `C:\PortableApps\01-FILE OPERATION APPS\AntiDupl.NET-2.3.12 (Image Duplicate Finder)\AntiDupl.NET-2.3.12\AntiDupl.NET.WinForms.exe` |
| **CloneSpy** | Latest | Byte-level file deduplication and automated NTFS hardlinking | `C:\PortableApps\01-FILE OPERATION APPS\CloneSpy\CloneSpy.exe` |
| **DiffMerge Stable** | 4.2.0 | Visual & headless file/directory diff engine | `C:\PortableApps\01-FILE OPERATION APPS\DiffMerge_4_2_0_697_stable_x86\sgdm.exe` |

---

### 15. Semantic Search, Reverse Engineering MCP & Trading Suite
| Tool / Package | Version | Purpose | Installation / Location |
| :--- | :--- | :--- | :--- |
| **Ghidra MCP Server** | 7.0.0 | 200+ MCP tools bridging Ghidra 12.2 disassembler to AI agents | Extension in `C:\ProgramData\chocolatey\lib\ghidra\tools\ghidra_12.2_PUBLIC\Ghidra\Extensions`, Bridge in `bridge-mcp-ghidra.exe` |
| **DigUp** | 0.7.0-beta.3 | On-device semantic local file search powered by EmbeddingGemma 2 | `C:\tools\DigUp\app\DigUp.exe` (Desktop shortcut: `DigUp.lnk`) |
| **Vibe-Trading** | 0.1.19 | Personal multi-agent finance, algorithmic backtesting & trading agent | `C:\tools\vibe-trading` (`vibe-trading.exe` & `vibe-trading-mcp.exe`) |
| **Deep Task Framework** | Felix Rieseberg | 4-pillar technical deconstruction and rigor enforcement agent skill | Agent skill in `skills/deep-task` |
| **Synaps App** | Web CAD | AI-assisted architectural floor plan and 2D CAD drafting | `https://synaps.app` (Desktop shortcut: `Synaps App.url`) |




---

## 📋 Installed Chocolatey Packages Snapshot

Exported directly from `docs/installed_choco_packages.txt`:

```text
adb 37.0.0
apimonitor 2.13.0.20210213
apktool 3.0.3
chocolatey 2.7.4
dotnetfx 4.8.0.20220524
ghidra 12.2.0
jadx 1.5.6
javaruntime 8.0.431
jre8 8.0.503
python 3.14.7
python3 3.14.7
python314 3.14.7
vcredist140 14.51.36247
vcredist2015 14.0.24215.20170201
visualstudio2026buildtools 118.8.2
visualstudio2026-workload-vctools 1.0.0
visualstudio-installer 2.0.7
wireshark 4.6.9
```

---

## 📂 Complete 168-Application System Inventory

A complete snapshot of all 168 applications detected on this computer is archived in:
👉 [`docs/installed_apps.csv`](docs/installed_apps.csv)

To inspect or query the full list in PowerShell:
```powershell
Import-Csv .\docs\installed_apps.csv | Out-GridView
```
