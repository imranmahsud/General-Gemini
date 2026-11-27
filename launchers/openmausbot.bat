@echo off
title OpenMausBot Multi-Agent Studio
echo ==================================================
echo         OpenMausBot Local Agent Harness
echo ==================================================
cd /d "C:\tools\OpenMausBot"
echo Starting OpenMausBot local workspace...
bun run dev --port 4173 2>nul
if errorlevel 1 (
    npm run dev
)
pause
