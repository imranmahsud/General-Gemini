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
| **Git for Windows** | 2.53+ | Version control & skill repo sync | `choco install git -y` or `winget install Git.Git` |
| **Python** | 3.12 / 3.14.7 | Agent scripting, BigFrames, ML & science | `choco install python -y` or `winget install Python.Python.3.12` |
| **Astral uv** | 0.9+ | High-performance Python package manager | `powershell -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| **Node.js (LTS)** | 22.x+ | REA server, MCP servers, web guidance | `choco install nodejs-lts -y` |
| **Java Development Kit (JDK)** | 21 LTS | Sweet Home 3D plugin SDK, Ghidra runtime | `choco install openjdk21 -y` |
| **.NET SDK** | 10 / 8.0 | Revit 2027 C# Add-in development | `winget install Microsoft.DotNet.SDK.10` |
| **Visual Studio Build Tools** | 2026 (18.9) | C++ compilation, native module builds | `choco install visualstudio2026buildtools -y` |

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
| **AutoHotkey v2** | Screen automation, global hotkeys | `choco install autohotkey -y` |
| **SumatraPDF** | Ultra-fast lightweight PDF review | `choco install sumatrapdf -y` |
| **7-Zip** | Archive decompression (tar, gz, zip, 7z) | `choco install 7zip -y` |
| **WSL 2** | Linux environment for cross-platform workflows | `wsl --install` |

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
