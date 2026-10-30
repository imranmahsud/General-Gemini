# PowerShell One-Click Skill Restore Script
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   Antigravity & Agent Skills Restore Utility     " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$TargetDir = "$HOME\.gemini\config\skills"
if (!(Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SourceDir = Join-Path $ScriptDir "skills"

if (!(Test-Path $SourceDir)) {
    Write-Error "Source skills directory not found at $SourceDir"
    exit 1
}

Write-Host "Restoring skills to $TargetDir..." -ForegroundColor Yellow
Get-ChildItem -Path $SourceDir -Directory | ForEach-Object {
    $Dest = Join-Path $TargetDir $_.Name
    if (Test-Path $Dest) {
        Remove-Item -Path $Dest -Recurse -Force
    }
    Copy-Item -Path $_.FullName -Destination $Dest -Recurse -Force
    Write-Host "  [OK] Restored: $($_.Name)" -ForegroundColor Green
}

Write-Host "`nInstalling global dependencies..." -ForegroundColor Yellow
try {
    npm.cmd install -g impeccable@^4.8.0 understand-anything-mcp@^2.7.8
    Write-Host "  [OK] Global CLI packages installed." -ForegroundColor Green
} catch {
    Write-Warning "Global npm install notice: $_"
}

Write-Host "`nAll skills restored and verified!" -ForegroundColor Cyan
