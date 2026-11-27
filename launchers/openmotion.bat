@echo off
title OpenMotion Video Studio
echo ==================================================
echo       OpenMotion Video-to-Code Framework
echo ==================================================
cd /d "C:\tools\openmotion"
if "%~1"=="" (
    echo Usage: openmotion.bat ^<check^|lock^|pack^> ^<package-dir^>
    echo Examples:
    echo   openmotion.bat check packages\motion-package\examples\intro
    echo.
    bun "packages\motion-package\cli.mjs" check packages\motion-package\examples\intro 2>nul
    pause
) else (
    bun "packages\motion-package\cli.mjs" %*
)
