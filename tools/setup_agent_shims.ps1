# setup_agent_shims.ps1 - Generates universal CLI shims in ~/.local/bin and antigravity/bin
# Enables headless, zero-path-guessing agentic execution for all installed and portable tools.

$localBin = Join-Path $HOME ".local\bin"
if (-not (Test-Path $localBin)) {
    New-Item -ItemType Directory -Path $localBin -Force | Out-Null
}

$antigravityBin = "C:\Users\Imran\.gemini\antigravity\bin"
if (Test-Path $antigravityBin) {
    # Frontload Python 3.12 shim so QGIS embedded python does not hijack 'python'
    $pyShim = "@echo off`n`"C:\Users\Imran\AppData\Local\Programs\Python\Python312\python.exe`" %*`n"
    Set-Content -Path (Join-Path $antigravityBin "python.bat") -Value $pyShim -Encoding ASCII
}

$shims = @{
    "bun.cmd"         = '@"C:\tools\bun.exe" %*'
    "blender.cmd"     = '@"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" %*'
    "freecad.cmd"     = '@"C:\Users\Imran\AppData\Local\Programs\FreeCAD 1.1\bin\FreeCAD.exe" %*'
    "freecadcmd.cmd"  = '@"C:\Users\Imran\AppData\Local\Programs\FreeCAD 1.1\bin\FreeCADCmd.exe" %*'
    "swmm5.cmd"       = '@"C:\Program Files\EPA SWMM 5.2.4 (64-bit)\runswmm.exe" %*'
    "runswmm.cmd"     = '@"C:\Program Files\EPA SWMM 5.2.4 (64-bit)\runswmm.exe" %*'
    "epanet.cmd"      = '@"C:\Program Files (x86)\EPANET 2.2\runepanet.exe" %*'
    "runepanet.cmd"   = '@"C:\Program Files (x86)\EPANET 2.2\runepanet.exe" %*'
    "tshark.cmd"      = '@"C:\Program Files\Wireshark\tshark.exe" %*'
    "wireshark.cmd"   = '@"C:\Program Files\Wireshark\Wireshark.exe" %*'
    "cloudcompare.cmd"= '@"C:\Program Files\CloudCompare\CloudCompare.exe" %*'
    "meshlab.cmd"     = '@"C:\Program Files\VCG\MeshLab\meshlab.exe" %*'
    "colmap.cmd"      = '@call "C:\tools\photogrammetry\COLMAP\COLMAP.bat" %*'
    "visualsfm.cmd"   = '@"C:\tools\photogrammetry\VisualSFM\VisualSFM.exe" %*'
    "ghidra.cmd"      = '@call "C:\ProgramData\chocolatey\lib\ghidra\tools\ghidra_12.2_PUBLIC\ghidraRun.bat" %*'
    "sumatrapdf.cmd"  = '@"C:\Program Files\SumatraPDF\SumatraPDF.exe" %*'
    "pdftk.cmd"       = '@"C:\PortableApps\PDFTKBuilderPortable\App\pdftkbuilder\pdftk.exe" %*'
    "exiftool.cmd"    = '@"C:\PortableApps\geosetter\tools\exiftool.exe" %*'
    "mkvmerge.cmd"    = '@"C:\PortableApps\mkvtoolnix\mkvmerge.exe" %*'
    "yt-dlp.cmd"      = '@"C:\PortableApps\Shutter Encoder 19.2 Windows 64bits\Library\yt-dlp.exe" %*'
    "mediainfo.cmd"   = '@"C:\PortableApps\Shutter Encoder 19.2 Windows 64bits\Library\MediaInfo.exe" %*'
    "realesrgan.cmd"  = '@"C:\PortableApps\Shutter Encoder 19.2 Windows 64bits\Library\realesrgan-ncnn-vulkan.exe" %*'
    "arenc.cmd"       = '@"C:\PortableApps\Advanced renamer portable\arenc.exe" %*'
    "iview64.cmd"     = '@"C:\PortableApps\irfanview462_x64\i_view64.exe" %*'
    "kpk-mrs.cmd"     = '@"C:\Users\Imran\AppData\Local\Programs\Python\Python312\python.exe" "C:\tools\civil-hydraulics\kpk-mrs\mrs_lookup.py" %*'
    "python.cmd"      = '@"C:\Users\Imran\AppData\Local\Programs\Python\Python312\python.exe" %*'
}

foreach ($name in $shims.Keys) {
    $targetPath = Join-Path $localBin $name
    Set-Content -Path $targetPath -Value $shims[$name] -Encoding ASCII
    Write-Host "Created shim: $name -> $($shims[$name])" -ForegroundColor Green
}

Write-Host "`nAll agent productivity shims deployed to $localBin." -ForegroundColor Cyan
