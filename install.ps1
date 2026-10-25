# install.ps1 - Automated Setup & Engineering Stack Transfer Script for Windows
# Run this script on your new Windows laptop: powershell -ExecutionPolicy Bypass -File .\install.ps1

$ErrorActionPreference = "Continue"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   Antigravity & Gemini Skills & Engineering Installer    " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

$SourceDir = $PSScriptRoot
$GeminiConfigDir = Join-Path $HOME ".gemini\config"
$TargetSkillsDir = Join-Path $GeminiConfigDir "skills"
$TargetPluginsDir = Join-Path $GeminiConfigDir "plugins"

# 1. Target Directories
Write-Host "[1/6] Checking target Antigravity directories..." -ForegroundColor Yellow
if (-not (Test-Path $GeminiConfigDir)) {
    New-Item -ItemType Directory -Path $GeminiConfigDir -Force | Out-Null
    Write-Host "  + Created: $GeminiConfigDir" -ForegroundColor Green
}
if (-not (Test-Path $TargetSkillsDir)) {
    New-Item -ItemType Directory -Path $TargetSkillsDir -Force | Out-Null
    Write-Host "  + Created: $TargetSkillsDir" -ForegroundColor Green
}
if (-not (Test-Path $TargetPluginsDir)) {
    New-Item -ItemType Directory -Path $TargetPluginsDir -Force | Out-Null
    Write-Host "  + Created: $TargetPluginsDir" -ForegroundColor Green
}

# 2. Copy Skills
Write-Host ""
Write-Host "[2/6] Deploying Skills to $TargetSkillsDir..." -ForegroundColor Yellow
$SourceSkillsDir = Join-Path $SourceDir "skills"
if (Test-Path $SourceSkillsDir) {
    $skills = Get-ChildItem -Path $SourceSkillsDir -Directory
    foreach ($skill in $skills) {
        $dest = Join-Path $TargetSkillsDir $skill.Name
        Copy-Item -Path $skill.FullName -Destination $dest -Recurse -Force
        Write-Host "  -> Installed skill: $($skill.Name)" -ForegroundColor Green
    }
} else {
    Write-Host "  ! Warning: Source skills folder not found at $SourceSkillsDir" -ForegroundColor Red
}

# 3. Copy Plugins
Write-Host ""
Write-Host "[3/6] Deploying Plugins to $TargetPluginsDir..." -ForegroundColor Yellow
$SourcePluginsDir = Join-Path $SourceDir "plugins"
if (Test-Path $SourcePluginsDir) {
    $plugins = Get-ChildItem -Path $SourcePluginsDir -Directory
    foreach ($plugin in $plugins) {
        $dest = Join-Path $TargetPluginsDir $plugin.Name
        Copy-Item -Path $plugin.FullName -Destination $dest -Recurse -Force
        Write-Host "  -> Installed plugin: $($plugin.Name)" -ForegroundColor Green
    }
} else {
    Write-Host "  ! Warning: Source plugins folder not found at $SourcePluginsDir" -ForegroundColor Red
}

# 4. Deploy QGIS Civil & PC-1 Plugins
Write-Host ""
Write-Host "[4/6] Checking QGIS 4.x / 3.x Plugin Deployment..." -ForegroundColor Yellow
$qgisPluginsDir = "$HOME\AppData\Roaming\QGIS\QGIS4\profiles\default\python\plugins"
if (-not (Test-Path $qgisPluginsDir)) {
    $qgisPluginsDir = "$HOME\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins"
}

if (Test-Path (Split-Path -Parent $qgisPluginsDir)) {
    if (-not (Test-Path $qgisPluginsDir)) { New-Item -ItemType Directory -Path $qgisPluginsDir -Force | Out-Null }
    Write-Host "  + Target QGIS Plugins directory: $qgisPluginsDir" -ForegroundColor Green

    $gitCmd = Get-Command "git" -ErrorAction SilentlyContinue
    if ($gitCmd) {
        if (-not (Test-Path "$qgisPluginsDir\quick_map_services")) {
            Write-Host "  -> Cloning QuickMapServices with satellite packs..." -ForegroundColor Green
            & git clone --depth 1 "https://github.com/nextgis/quickmapservices.git" "$qgisPluginsDir\qms_temp"
            Move-Item -Path "$qgisPluginsDir\qms_temp\src\quick_map_services" -Destination "$qgisPluginsDir\quick_map_services"
            Remove-Item -Path "$qgisPluginsDir\qms_temp" -Recurse -Force -ErrorAction SilentlyContinue
            & git clone --depth 1 "https://github.com/nextgis/quickmapservices_contrib.git" "$qgisPluginsDir\quick_map_services\quickmapservices_contrib\data_sources"
        }
        if (-not (Test-Path "$qgisPluginsDir\profiletool")) {
            Write-Host "  -> Cloning Profile Tool..." -ForegroundColor Green
            & git clone --depth 1 "https://github.com/PANOimagen/profiletool.git" "$qgisPluginsDir\profiletool"
        }
        if (-not (Test-Path "$qgisPluginsDir\Qgis2threejs")) {
            Write-Host "  -> Cloning Qgis2threejs..." -ForegroundColor Green
            & git clone --depth 1 "https://github.com/minorua/Qgis2threejs.git" "$qgisPluginsDir\Qgis2threejs"
        }
    } else {
        Write-Host "  ! Git not yet installed; install Git to automatically clone QGIS plugins." -ForegroundColor DarkYellow
    }
} else {
    Write-Host "  ! QGIS profile not detected yet. Plugins will configure once QGIS is run." -ForegroundColor Gray
}

# 5. Check & Auto-Install Core Engineering & Runtime Packages
Write-Host ""
Write-Host "[5/6] Verifying Toolchains & Runtime Packages..." -ForegroundColor Yellow
Write-Host "----------------------------------------------------------"

function Ensure-Tool ($Name, $Command, $InstallHint) {
    try {
        $result = & (Get-Command $Command -ErrorAction Stop) --version 2>$null
        if (-not $result) { $result = & (Get-Command $Command -ErrorAction Stop) -v 2>$null }
        Write-Host " [OK]  $Name is installed." -ForegroundColor Green
    } catch {
        Write-Host " [NOTICE] $Name not detected in PATH." -ForegroundColor DarkYellow
        Write-Host "          Install hint: $InstallHint" -ForegroundColor Gray
    }
}

Ensure-Tool "Git for Windows" "git" "winget install Git.Git or choco install git"
Ensure-Tool "Python 3" "python" "winget install Python.Python.3.12 or choco install python"
Ensure-Tool "Typst Compiler" "typst" "winget install Typst.Typst"
Ensure-Tool "Astral uv" "uv" "powershell -c 'irm https://astral.sh/uv/install.ps1 | iex'"
Ensure-Tool ".NET SDK" "dotnet" "winget install Microsoft.DotNet.SDK.10 (or SDK.8)"
Ensure-Tool "Java JDK" "javac" "choco install openjdk21 or winget install Oracle.JDK.21"
Ensure-Tool "Google Cloud CLI" "gcloud" "winget install Google.CloudSDK or choco install gcloudsdk"
Ensure-Tool "Android CLI / ADB" "adb" "choco install adb or install via Android Studio"
Ensure-Tool "Ghidra" "ghidra" "choco install ghidra"
Ensure-Tool "Wireshark" "wireshark" "choco install wireshark"
Ensure-Tool "JADX Decompiler" "jadx" "choco install jadx"
Ensure-Tool "Rizin" "rizin" "choco install rizin or install to C:\tools\rizin"

Write-Host "----------------------------------------------------------"
Write-Host "For a one-click automated installation of all software, run:" -ForegroundColor Cyan
Write-Host "  powershell -ExecutionPolicy Bypass -File .\install-apps.ps1" -ForegroundColor Yellow

# 6. Python Civil & PC-1 Engineering Virtual Environment
Write-Host ""
Write-Host "[6/6] Verifying Python Civil & PC-1 Engineering Stack..." -ForegroundColor Yellow
$pyCmd = Get-Command "python" -ErrorAction SilentlyContinue
if ($pyCmd) {
    $venvPath = Join-Path $SourceDir ".venv"
    if (-not (Test-Path $venvPath)) {
        Write-Host "  -> Creating Python 3.12 Engineering virtual environment in $venvPath..." -ForegroundColor Green
        & python -m venv $venvPath
    }
    $pipPath = Join-Path $venvPath "Scripts\pip.exe"
    if (Test-Path $pipPath) {
        Write-Host "  -> Installing Python engineering packages (pandas, geopandas, scipy, openpyxl, python-docx, matplotlib, ezdxf, h5py, whitebox)..." -ForegroundColor Green
        & $pipPath install --upgrade pip --quiet
        & $pipPath install pandas openpyxl python-docx matplotlib geopandas shapely ezdxf h5py whitebox scipy --quiet
        Write-Host "  -> Python Engineering Stack is fully configured!" -ForegroundColor Green
    }
} else {
    Write-Host "  ! Python not detected. Run: winget install Python.Python.3.12" -ForegroundColor DarkYellow
}

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Setup Completed! Your machine is ready for:" -ForegroundColor Green
Write-Host "  * Antigravity & Gemini Autonomous Agent Workflows" -ForegroundColor White
Write-Host "  * Reverse Engineering Suite (REA, Ghidra, Wireshark, JADX)" -ForegroundColor White
Write-Host "  * GIS Mapping, Elevation Contours & 3D Terrain Analysis" -ForegroundColor White
Write-Host "  * EPA-SWMM Drainage & EPANET Water Distribution Modeling" -ForegroundColor White
Write-Host "  * HEC-RAS 7.0 River Hydraulics & Flood Inundation" -ForegroundColor White
Write-Host "  * CAD & BIM Architectural Modeling (Revit, SketchUp, Sweet Home 3D)" -ForegroundColor White
Write-Host "  * PC-1 Feasibility Studies, BOQ, EIRR/BCR & Typst Reports" -ForegroundColor White
Write-Host "  * Full Handbook: docs\engineering_applications_master_handbook.md" -ForegroundColor Cyan
Write-Host "  * Full Apps Catalog: APPS_LIST.md" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
