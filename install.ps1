# install.ps1 - Automated Setup & Skill Transfer Script for Windows
# Run this script on your new Windows laptop: powershell -ExecutionPolicy Bypass -File .\install.ps1

$ErrorActionPreference = "Continue"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   Antigravity & Gemini Skills & Customizations Installer  " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

$SourceDir = $PSScriptRoot
$GeminiConfigDir = Join-Path $HOME ".gemini\config"
$TargetSkillsDir = Join-Path $GeminiConfigDir "skills"
$TargetPluginsDir = Join-Path $GeminiConfigDir "plugins"

Write-Host "[1/4] Checking target directories..." -ForegroundColor Yellow
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
Write-Host "[2/4] Deploying Skills to $TargetSkillsDir..." -ForegroundColor Yellow
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
Write-Host "[3/4] Deploying Plugins to $TargetPluginsDir..." -ForegroundColor Yellow
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

# 4. Check Environment Prerequisites
Write-Host ""
Write-Host "[4/4] Verifying Installed Software & Toolchains..." -ForegroundColor Yellow
Write-Host "----------------------------------------------------------"

function Check-Tool ($Name, $Command, $InstallHint) {
    try {
        $result = & (Get-Command $Command -ErrorAction Stop) --version 2>$null
        if (-not $result) { $result = & (Get-Command $Command -ErrorAction Stop) -v 2>$null }
        Write-Host " [OK]  $Name is installed." -ForegroundColor Green
    } catch {
        Write-Host " [MISSING] $Name not found." -ForegroundColor DarkYellow
        Write-Host "         -> Recommendation: $InstallHint" -ForegroundColor Gray
    }
}

Check-Tool "Git for Windows" "git" "winget install Git.Git"
Check-Tool "Python 3" "python" "winget install Python.Python.3.12"
Check-Tool "uv Package Manager" "uv" "winget install astral-sh.uv"
Check-Tool ".NET SDK" "dotnet" "winget install Microsoft.DotNet.SDK.10 (or SDK.8)"
Check-Tool "Java JDK" "javac" "winget install Oracle.JDK.21 (or EclipseAdoptium.Temurin.21.JDK)"
Check-Tool "Google Cloud CLI" "gcloud" "winget install Google.CloudSDK"
Check-Tool "Flutter SDK" "flutter" "Download from https://docs.flutter.dev/get-started/install/windows"
Check-Tool "Android CLI / Tools" "adb" "Install via Android Studio or Android SDK Tools"

Write-Host "----------------------------------------------------------"
Write-Host "Specialized CAD/BIM Applications to install manually:" -ForegroundColor Cyan
Write-Host "  * Autodesk Revit 2027 (or 2026/2025) - for BIM modeling and C# add-ins" -ForegroundColor White
Write-Host "  * Trimble SketchUp Pro 2026 (or 2025) - for surface modeling and Ruby scripts" -ForegroundColor White
Write-Host "  * Sweet Home 3D (v7.x or 8.x) - for residential interior planning" -ForegroundColor White
Write-Host "  * Visual Studio 2026 / VS Code - for .NET 10, C#, Ruby, and Java development" -ForegroundColor White
Write-Host ""
Write-Host "Setup Completed! Your Antigravity and Gemini agents will now automatically discover all transferred skills and plugins." -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
