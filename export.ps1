# export.ps1 - Syncs local skills and plugins from $HOME\.gemini\config into this repository

$ErrorActionPreference = "Stop"

$RepoDir = $PSScriptRoot
$GeminiConfigDir = Join-Path $HOME ".gemini\config"
$SkillsSource = Join-Path $GeminiConfigDir "skills"
$PluginsSource = Join-Path $GeminiConfigDir "plugins"

Write-Host "Syncing skills and plugins from $GeminiConfigDir into repository..." -ForegroundColor Cyan

if (Test-Path $SkillsSource) {
    Copy-Item -Path $SkillsSource -Destination $RepoDir -Recurse -Force
    Write-Host " -> Synced skills successfully." -ForegroundColor Green
}

if (Test-Path $PluginsSource) {
    Copy-Item -Path $PluginsSource -Destination $RepoDir -Recurse -Force
    Write-Host " -> Synced plugins successfully." -ForegroundColor Green
}

Write-Host "Sync complete! You can now commit and push changes with git." -ForegroundColor Green
