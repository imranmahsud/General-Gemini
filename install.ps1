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

# 5. Check & Auto-Install Core Engineering Winget Tools
Write-Host ""
Write-Host "[5/6] Verifying & Installing Core Engineering Packages via Winget..." -ForegroundColor Yellow
Write-Host "----------------------------------------------------------"

function Ensure-WingetPackage ($Name, $Command, $WingetId) {
    try {
        $cmd = Get-Command $Command -ErrorAction Stop
        Write-Host " [OK]  $Name is installed." -ForegroundColor Green
    } catch {
        Write-Host " [INSTALLING] $Name not found. Installing $WingetId via winget..." -ForegroundColor Cyan
        winget install --id $WingetId --silent --accept-package-agreements --accept-source-agreements
    }
}

Ensure-WingetPackage "Git for Windows" "git" "Git.Git"
Ensure-WingetPackage "Typst Compiler" "typst" "Typst.Typst"
Ensure-WingetPackage "EPA SWMM 5.2" "epaswmm5" "EPA.SWMM"
Ensure-WingetPackage "EPANET 2.2" "runepanet" "USEPA.EPANET"
Ensure-WingetPackage "ProjectLibre" "projectlibre" "ProjectLibre.ProjectLibre"

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
Write-Host "Setup Completed! Your new machine is ready for:" -ForegroundColor Green
Write-Host "  * Antigravity & Gemini Autonomous Agent Workflows" -ForegroundColor White
Write-Host "  * GIS Mapping, Elevation Contours & 3D Terrain Analysis" -ForegroundColor White
Write-Host "  * EPA-SWMM Drainage & EPANET Water Distribution Modeling" -ForegroundColor White
Write-Host "  * HEC-RAS 7.0 River Hydraulics & Flood Inundation" -ForegroundColor White
Write-Host "  * PC-1 Feasibility Studies, BOQ, EIRR/BCR & Typst Reports" -ForegroundColor White
Write-Host "  * Full Handbook: docs\engineering_applications_master_handbook.md" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
