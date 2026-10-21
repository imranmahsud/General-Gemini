# General-Gemini: Antigravity Skills, Plugins & CAD/BIM Knowledge Transfer

This repository contains the complete bundle of agent skills, plugins, architectural drafting/modeling knowledge, and API automation tools for Google Antigravity and Gemini.

---

## 🚀 Quick Setup on Your New Windows Laptop

### Step 1: Clone this Repository
Open PowerShell or Windows Terminal and clone to your preferred location:
```powershell
cd $HOME\Downloads   # or Documents
git clone https://github.com/imranmahsud/General-Gemini.git
cd General-Gemini
```

### Step 2: Run the One-Click Installer
Run the automated installation script:
```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```
This script automatically:
* Creates `$HOME\.gemini\config\skills` and `$HOME\.gemini\config\plugins`
* Copies all custom skills and plugins into the active Antigravity/Gemini discovery paths
* Verifies software prerequisites on your new laptop

---

## 💻 List of Required Software for Your New Laptop

To fully utilize all the transferred skills and capabilities, install the following software packages on your new Windows machine:

### 1. Essential Development & Agent Runtime
* **Git for Windows** (with Git Credential Manager)
  ```powershell
  winget install Git.Git
  ```
* **Python 3.12+** & **uv Package Manager** (for Data Agent Kit, BigQuery BigFrames, and ML skills)
  ```powershell
  winget install Python.Python.3.12
  winget install astral-sh.uv
  ```
* **Visual Studio Code** or **Visual Studio 2026**
  ```powershell
  winget install Microsoft.VisualStudioCode
  ```

---

### 2. Architectural Drawing, Modeling & BIM Software
* **Autodesk Revit 2027** (or 2026/2025):
  * Required for: Enterprise BIM modeling, parametric system families, Dynamo 4.0 visual scripting, and openBIM IFC4.3 export.
  * Companion SDK: **.NET 10 SDK** (or .NET 8) for compiling Revit C# add-ins:
    ```powershell
    winget install Microsoft.DotNet.SDK.10
    ```
  * Companion tool: **pyRevit** or **Revit Python Shell** for live Python scripting.
* **Trimble SketchUp Pro 2026** (or 2025):
  * Required for: Rapid surface modeling, push-pull drafting, inference engine snapping, PBR materials, and LayOut 2026 construction drawings.
  * Companion tool: **Ruby 3.x** and VS Code Ruby extension for developing SketchUp Ruby scripts.
* **Sweet Home 3D (v7.x / 8.x)**:
  * Required for: Residential space planning, 2D floor plans, 3D aerial/visitor navigation, and `.sh3d` manipulation.
  * Companion SDK: **Java Development Kit (JDK 21 LTS)** for compiling custom Sweet Home 3D Java plugins (`.sh3p`):
    ```powershell
    winget install Oracle.JDK.21
    ```

---

### 3. Cloud, Data & Analytics Tools (for Data Agent Kit Skills)
* **Google Cloud SDK (`gcloud` and `bq` CLI)**:
  * Required for: BigQuery, Cloud Composer, Dataproc Spark, and GCS skills.
  ```powershell
  winget install Google.CloudSDK
  ```

---

### 4. Mobile & App Frameworks (for Flutter & Android Skills)
* **Flutter & Dart SDK**:
  * Follow official guide: [flutter.dev/get-started/install/windows](https://docs.flutter.dev/get-started/install/windows)
* **Android Studio & Command-line Tools**:
  * Required for: `android-cli-plugin`, ADB, and emulator testing.
  ```powershell
  winget install Google.AndroidStudio
  ```

---

## 📦 What's Included in this Transfer

### 1. New CAD & BIM Drawing Mastery Skill
* Located at: `skills/cad-bim-drawing-mastery/`
* Full architectural modeling, drafting methods, API syntax, and converter pipelines across **Revit 2027**, **SketchUp 2026**, and **Sweet Home 3D**.
* Full technical reference report: `docs/mastery_report_revit2027_sketchup2026_sweethome3d.md`.

### 2. Custom Agent Skills (32+ Specialized Skills)
* **Architectural & Spatial**: `architectural-plan-designer`, `furniture-fit`, `pascal-3d`, `cad-bim-drawing-mastery`
* **Data & BigQuery**: `bigquery-ai-ml`, `bigquery-bigframes`, `bigquery-data-transfer-service`, `bigquery-graph`, `bigquery-sql`, `dbt-bigquery`, `dataform-bigquery`, `data-autocleaning`, `schema-mapping`
* **Google Cloud & Pipelines**: `gcp-data-pipelines`, `gcp-pipeline-orchestration`, `gcp-pipeline-resource-provisioning`, `gcp-composer-troubleshooting`, `gcp-managed-airflow-dag-authoring`, `gcp-managed-airflow-migrations`, `gcp-managed-airflow-recommendations`, `gcp-spark`, `google-cloud-auth-verification`, `google-cloud-storage-basics`, `gcs-security-assessment`, `federate-lakehouse-catalog`, `enforcing-resource-attribution`
* **Engineering & Safety**: `accidental-data-loss-prevention`, `managing-python-dependencies`, `ml-best-practices`, `notebook-guidance`, `skill-repair`, `find-skills`

### 3. Plugins
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
Whenever you make improvements or add new skills on either computer, run:
```powershell
powershell -ExecutionPolicy Bypass -File .\export.ps1
git add .
git commit -m "Update skills and configurations"
git push
```
And on the other machine:
```powershell
git pull
powershell -ExecutionPolicy Bypass -File .\install.ps1
```
