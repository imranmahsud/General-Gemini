@echo off
title Last30Days Live Social ^& Web Search
echo ==================================================
echo   Last30Days - People-First Multi-Source Search
echo ==================================================
cd /d "C:\tools\last30days-skill\skills\last30days\scripts"
if "%~1"=="" (
    set /p topic="Enter research topic: "
    "C:\Users\Imran\AppData\Local\Programs\Python\Python312\python.exe" last30days.py --quick "!topic!"
    pause
) else (
    "C:\Users\Imran\AppData\Local\Programs\Python\Python312\python.exe" last30days.py %*
)
