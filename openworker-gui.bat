@echo off
title OpenWorker AI Studio
echo ==================================================
echo           Starting OpenWorker AI Studio
echo ==================================================

REM Check if Ollama is listening on 11434
curl.exe -s http://127.0.0.1:11434/ >nul 2>&1
if errorlevel 1 (
    if exist "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" (
        echo Starting Ollama local server...
        start "Ollama Server" /b "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" serve
        timeout /t 3 /nobreak >nul
    )
)

REM Start OpenWorker Backend Server
echo Starting OpenWorker API Server on port 8765...
start "OpenWorker Backend" /b "C:\tools\openworker\.venv\Scripts\python.exe" -m coworker.server.run --port 8765 --cwd "%USERPROFILE%\Downloads\Check"

REM Wait for server initialization
timeout /t 2 /nobreak >nul

REM Launch GUI Front-End
echo Launching OpenWorker Web GUI on http://localhost:5173...
cd /d "C:\tools\openworker\surfaces\gui"
start "" http://localhost:5173
bun run preview --port 5173
