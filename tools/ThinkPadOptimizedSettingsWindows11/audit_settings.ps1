Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " ThinkPad Current Configuration Audit" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Hardware Overview
$cs = Get-CimInstance Win32_ComputerSystem
$proc = Get-CimInstance Win32_Processor
$gpu = Get-CimInstance Win32_VideoController
$ramGB = [math]::Round($cs.TotalPhysicalMemory / 1GB, 1)

Write-Host "Model        : $($cs.Manufacturer) $($cs.Model)"
Write-Host "CPU          : $($proc.Name)"
Write-Host "RAM Total    : $ramGB GB"
Write-Host "GPU Name     : $($gpu.Name)"
Write-Host "Dedicated VRAM: $([math]::Round($gpu.AdapterRAM / 1GB, 2)) GB"

# 2. BIOS UMA Setting
$uma = (Get-CimInstance -Namespace root\wmi -ClassName Lenovo_BiosSetting -ErrorAction SilentlyContinue | Where-Object CurrentSetting -like "*UMA*").CurrentSetting
Write-Host "`n[BIOS Setting]"
Write-Host "UMA Framebuffer Setting: $uma"

# 3. Power & Boost Settings
$SUB_PROC    = "54533251-82be-4824-96c1-47b60b740d00"
$SYSCOOLPOL  = "94d3a615-a899-4ac5-ae2b-e4d8f634367f"
$PERFBOOST   = "be337238-0d82-4146-a960-4f3749d470c7"
$THROTTLEMAX = "bc5038f7-23e0-4960-96da-33abaf5935ec"

Write-Host "`n[Windows Power Settings]"
$cool = (powercfg /q SCHEME_CURRENT $SUB_PROC $SYSCOOLPOL) | Select-String "Current AC Power Setting Index"
$boost = (powercfg /q SCHEME_CURRENT $SUB_PROC $PERFBOOST) | Select-String "Current AC Power Setting Index"
$max = (powercfg /q SCHEME_CURRENT $SUB_PROC $THROTTLEMAX) | Select-String "Current AC Power Setting Index"

Write-Host "Cooling Policy (AC)    : $cool"
Write-Host "Boost Mode (AC)        : $boost (Target: 0x00000003 = Efficient Enabled)"
Write-Host "Max State (AC)         : $max (Target: 0x00000064 = 100%)"

# 4. HAGS
$hags = (Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\GraphicsDrivers' -ErrorAction SilentlyContinue).HwSchMode
Write-Host "`n[Graphics Scheduling]"
Write-Host "HAGS (HwSchMode)       : $hags (Target: 2 = Enabled)"

# 5. Defender Exclusions
$exclusions = (Get-MpPreference -ErrorAction SilentlyContinue).ExclusionPath
Write-Host "`n[Defender Excluded Paths]"
Write-Host ($exclusions -join ", ")

Write-Host "`n==========================================================" -ForegroundColor Cyan
