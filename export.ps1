# export.ps1 - Syncs local skills, plugins, and installed apps list into this repository

$ErrorActionPreference = "Stop"

$RepoDir = $PSScriptRoot
$GeminiConfigDir = Join-Path $HOME ".gemini\config"
$SkillsSource = Join-Path $GeminiConfigDir "skills"
$PluginsSource = Join-Path $GeminiConfigDir "plugins"
$DocsDir = Join-Path $RepoDir "docs"

if (-not (Test-Path $DocsDir)) {
    New-Item -ItemType Directory -Path $DocsDir -Force | Out-Null
}

Write-Host "Syncing skills and plugins from $GeminiConfigDir into repository..." -ForegroundColor Cyan

if (Test-Path $SkillsSource) {
    Copy-Item -Path $SkillsSource -Destination $RepoDir -Recurse -Force
    Write-Host " -> Synced skills successfully." -ForegroundColor Green
}

if (Test-Path $PluginsSource) {
    Copy-Item -Path $PluginsSource -Destination $RepoDir -Recurse -Force
    Write-Host " -> Synced plugins successfully." -ForegroundColor Green
}

Write-Host "Exporting installed applications list and package manifests..." -ForegroundColor Cyan

# 1. Export Windows Installed Applications from Registry
$apps = @()
$regPaths = @(
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*"
)
foreach ($path in $regPaths) {
    Get-ItemProperty $path -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName -and $_.DisplayName.Trim() -ne "" } | ForEach-Object {
        $apps += [PSCustomObject]@{
            Name            = ($_.DisplayName -replace '[\r\n]', '').Trim()
            Version         = if ($_.DisplayVersion) { ($_.DisplayVersion -replace '[\r\n]', '').Trim() } else { "N/A" }
            Publisher       = if ($_.Publisher) { ($_.Publisher -replace '[\r\n]', '').Trim() } else { "Unknown" }
            InstallLocation = if ($_.InstallLocation) { ($_.InstallLocation -replace '[\r\n]', '').Trim() } else { "" }
        }
    }
}
$apps = $apps | Sort-Object Name -Unique
$appsCsvPath = Join-Path $DocsDir "installed_apps.csv"
$apps | Export-Csv -Path $appsCsvPath -NoTypeInformation -Encoding utf8
Write-Host " -> Exported $($apps.Count) installed applications to $appsCsvPath" -ForegroundColor Green

# 2. Export Chocolatey Packages if choco is present
if (Get-Command choco -ErrorAction SilentlyContinue) {
    $chocoTxtPath = Join-Path $DocsDir "installed_choco_packages.txt"
    choco list --limit-output | Out-File -FilePath $chocoTxtPath -Encoding utf8
    Write-Host " -> Exported Chocolatey packages to $chocoTxtPath" -ForegroundColor Green
}

Write-Host "Sync complete! You can now commit and push changes with git." -ForegroundColor Green

