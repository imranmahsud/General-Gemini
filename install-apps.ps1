# install-apps.ps1 - Automated Software & Toolchain Installer for Windows
# Run in an elevated PowerShell session:
# powershell -ExecutionPolicy Bypass -File .\install-apps.ps1

$ErrorActionPreference = "Continue"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   Antigravity & Gemini Environment Software Installer     " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# Ensure Chocolatey is installed
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "[1/4] Chocolatey not detected. Installing Chocolatey..." -ForegroundColor Yellow
    try {
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        Write-Host " -> Chocolatey installed successfully." -ForegroundColor Green
    } catch {
        Write-Host " ! Warning: Could not automatically install Chocolatey. Please install from https://chocolatey.org" -ForegroundColor Red
    }
} else {
    Write-Host "[1/4] Chocolatey detected." -ForegroundColor Green
}

# Core Development Runtimes
Write-Host ""
Write-Host "[2/4] Installing Core Developer Runtimes & SDKs..." -ForegroundColor Yellow
$devPackages = @(
    "git",
    "python",
    "nodejs-lts",
    "openjdk21",
    "dotnet-sdk"
)

foreach ($pkg in $devPackages) {
    Write-Host " -> Ensuring package: $pkg..." -ForegroundColor Cyan
    choco install $pkg -y --no-progress
}

# Install uv package manager if missing
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host " -> Installing Astral uv package manager..." -ForegroundColor Cyan
    try {
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    } catch {
        Write-Host " ! Could not install uv automatically. Run: winget install astral-sh.uv" -ForegroundColor DarkYellow
    }
}

# Reverse Engineering Suite
Write-Host ""
Write-Host "[3/4] Installing Reverse Engineering & Security Tools (REA Toolchain)..." -ForegroundColor Yellow
$rePackages = @(
    "ghidra",
    "wireshark",
    "jadx",
    "adb",
    "apktool",
    "apimonitor"
)

foreach ($pkg in $rePackages) {
    Write-Host " -> Ensuring package: $pkg..." -ForegroundColor Cyan
    choco install $pkg -y --no-progress
}

# Architectural & Desktop CAD/BIM Applications Guide
Write-Host ""
Write-Host "[4/4] Verifying CAD/BIM, Modeling & Desktop Applications..." -ForegroundColor Yellow
Write-Host "----------------------------------------------------------" -ForegroundColor DarkGray

function Check-App ($Name, $Command, $InstallHint) {
    if (Get-Command $Command -ErrorAction SilentlyContinue) {
        Write-Host " [OK]  $Name is installed." -ForegroundColor Green
    } else {
        Write-Host " [NOTICE] $Name is not in PATH or not installed." -ForegroundColor DarkYellow
        Write-Host "          Installation Hint: $InstallHint" -ForegroundColor Gray
    }
}

Check-App "Sweet Home 3D" "sweethome3d" "Install via installer from https://www.sweethome3d.com or winget install SpaceMushrooms.SweetHome3D"
Check-App "FreeCAD" "FreeCAD" "winget install FreeCAD.FreeCAD or https://www.freecad.org"
Check-App "QGIS" "qgis" "winget install OSGeo.QGIS or https://qgis.org"
Check-App "Android Studio" "studio64" "winget install Google.AndroidStudio or https://developer.android.com/studio"
Check-App "Google Cloud CLI" "gcloud" "winget install Google.CloudSDK or choco install gcloudsdk"

Write-Host ""
Write-Host "Manual CAD/BIM Installs Required (Proprietary / Enterprise Licenses):" -ForegroundColor Cyan
Write-Host " * Autodesk Revit 2027: Install via Autodesk Desktop Access / Education / Commercial portal" -ForegroundColor White
Write-Host " * Trimble SketchUp Pro 2026: Install from https://www.sketchup.com" -ForegroundColor White
Write-Host " * AutoCAD 2006 (or DWG TrueView): Install for legacy DWG review" -ForegroundColor White
Write-Host ""
Write-Host "Software & Apps Installation Routine Completed!" -ForegroundColor Green
Write-Host "Next Step: Run 'powershell -ExecutionPolicy Bypass -File .\install.ps1' to deploy all skills and plugins." -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
