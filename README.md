# General-Gemini: Antigravity Skills, Plugins & CAD/BIM/GIS Engineering Transfer

This repository contains the complete bundle of agent skills, plugins, architectural drafting/modeling knowledge, civil infrastructure solvers, and PC-1 technical feasibility tools for Google Antigravity and Gemini.

---

## 🚀 Quick Setup on Your New Windows Laptop

### Step 1: Clone this Repository
Open PowerShell or Windows Terminal:
```powershell
cd $HOME\Downloads   # or Documents
git clone https://github.com/imranmahsud/General-Gemini.git
cd General-Gemini
```

### Step 2: Run the Turnkey Installer
Run the automated installation script:
```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```
This script automatically:
* Creates `$HOME\.gemini\config\skills` and `$HOME\.gemini\config\plugins`
* Deploys all 36 custom skills and 8 plugins into active Antigravity/Gemini discovery paths
* Clones QGIS civil engineering plugins (`quick_map_services` + satellite packs, `profiletool`, `Qgis2threejs`)
* Auto-installs core engineering tools via winget (`Typst`, `EPA-SWMM`, `EPANET`, `ProjectLibre`, `Git`)
* Configures the Python Civil & PC-1 Engineering virtual environment (`pandas`, `geopandas`, `scipy`, `openpyxl`, `python-docx`, `matplotlib`, `ezdxf`, `h5py`, `whitebox`)

---

## 📚 Master Engineering Documentation

* **Engineering Applications Master Handbook**: [`docs/engineering_applications_master_handbook.md`](docs/engineering_applications_master_handbook.md)
  * Comprehensive operating manual and CLI/API automation guide covering 23+ engineering, GIS, CAD/BIM, hydraulic, photogrammetric, and document management applications.
* **CAD & BIM Mastery Report**: [`docs/mastery_report_revit2027_sketchup2026_sweethome3d.md`](docs/mastery_report_revit2027_sketchup2026_sweethome3d.md)
  * Technical reference for Autodesk Revit 2027 (.NET 10), Trimble SketchUp 2026 (Ruby API / PBR), and Sweet Home 3D (.sh3d / Java).
* **PC-1 Feasibility Templates**: [`templates/`](templates/)
  * `pc1_financial_model.py`: Automated Planning Commission Proforma 1 economic evaluation (PVC, PVB, NPV, BCR, EIRR with sensitivity analysis).
  * `pc1_technical_report.typ`: Typst 0.15 template for publication-grade project technical inception reports.

---

## 💻 Software Stack for Your Windows Machine

### 1. Essential Development & Agent Runtime
* **Git for Windows**: `winget install Git.Git`
* **Python 3.12+** & **uv Package Manager**:
  ```powershell
  winget install Python.Python.3.12
  winget install astral-sh.uv
  ```
* **Typst Document Compiler**: `winget install Typst.Typst`
* **Visual Studio Code**: `winget install Microsoft.VisualStudioCode`

---

### 2. Civil Infrastructure, Hydraulics & Project Management
* **EPA-SWMM 5.2.4** (Urban Stormwater Drainage & Culvert Sizing): `winget install EPA.SWMM`
* **EPANET 2.2** (Water Supply Distribution Networks): `winget install USEPA.EPANET`
* **USACE HEC-RAS 7.0.1** (1D/2D River Hydraulics & Floodplains): Download from USACE HEC website
* **QGIS 4.2.3** (Geospatial Analysis, Contours, Watersheds): Download from QGIS.org
* **ProjectLibre 1.9.8** (PC-1 Implementation Scheduling, CPM, Gantt): `winget install ProjectLibre.ProjectLibre`
* **Google Earth Pro** (Satellite Desk Studies & KML/KMZ Tours): `winget install Google.GoogleEarthPro`

---

### 3. Architectural Drawing, Modeling & BIM Software
* **Autodesk Revit 2027** (or 2026/2025):
  * Enterprise BIM modeling, parametric system families, Dynamo 4.0 visual scripting, openBIM IFC4.3 export.
  * Companion SDK: **.NET 10 SDK** for compiling Revit C# add-ins: `winget install Microsoft.DotNet.SDK.10`
* **AutoCAD LT 2027** (or 2026/2025):
  * Precision 2D/3D CAD drafting; integrates with AutoCAD MCP Server (`acmcp.dll`).
* **Trimble SketchUp Pro 2026** (or 2025):
  * Rapid surface modeling, push-pull drafting, Scan Essentials point cloud modeling, LayOut 2026 drawings.
* **Sweet Home 3D (v7.x / 8.x)**:
  * Residential space planning, 2D floor plans, 3D synchronized views, `.sh3d` manipulation.

---

### 4. Cloud, Data & Analytics Tools (for Data Agent Kit Skills)
* **Google Cloud SDK (`gcloud` and `bq` CLI)**:
  * Required for BigQuery, Cloud Composer, Dataproc Spark, and GCS skills.
  ```powershell
  winget install Google.CloudSDK
  ```

---

## 📦 What's Included in this Transfer

### 1. Custom Agent Skills (36 Specialized Skills)
* **CAD, BIM & Spatial**: `cad-bim-drawing-mastery`, `architectural-plan-designer`, `furniture-fit`, `pascal-3d`, `ai-image-generation`
* **BigQuery & Data**: `bigquery-ai-ml`, `bigquery-bigframes`, `bigquery-data-transfer-service`, `bigquery-graph`, `bigquery-sql`, `dbt-bigquery`, `dataform-bigquery`, `data-autocleaning`, `schema-mapping`, `building-data-apps`
* **Google Cloud & Pipelines**: `gcp-data-pipelines`, `gcp-pipeline-orchestration`, `gcp-pipeline-resource-provisioning`, `gcp-composer-troubleshooting`, `gcp-dataflow`, `gcp-managed-airflow-dag-authoring`, `gcp-managed-airflow-migrations`, `gcp-managed-airflow-recommendations`, `gcp-spark`, `google-cloud-auth-verification`, `google-cloud-storage-basics`, `gcs-security-assessment`, `discovering-gcp-data-assets`, `federate-lakehouse-catalog`, `enforcing-resource-attribution`
* **Engineering & Safety**: `accidental-data-loss-prevention`, `managing-python-dependencies`, `ml-best-practices`, `notebook-guidance`, `skill-repair`, `find-skills`

### 2. Plugins (8 Plugins)
* `android-cli-plugin`
* `data-agent-kit-plugin`
* `flutter`
* `gemini-api`
* `googlecloudtools.datacloud_telemetry`
* `google_maps_platform`
* `modern-web-guidance-plugin`
* `science`

---

## 🔄 Keeping Updated
Whenever you make improvements or add new skills on either computer:
```powershell
powershell -ExecutionPolicy Bypass -File .\export.ps1
git add .
git commit -m "Update skills, engineering tools, and handbooks"
git push
```
And on your new laptop:
```powershell
git pull
powershell -ExecutionPolicy Bypass -File .\install.ps1
```
