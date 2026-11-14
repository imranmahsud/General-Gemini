# Requires -RunAsAdministrator
[CmdletBinding()]
param(
    [ValidateSet("Auto", "1GB", "2GB", "4GB", "8GB")]
    [string]$VramSize = "4GB"
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " ThinkPad Windows 11 Optimization & Restoration Suite" -ForegroundColor Cyan
Write-Host " Target: AMD Ryzen 5000 / Vega Graphics / Dual Channel RAM" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Administrator Check
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Error "This script must be run as Administrator. Re-run from an elevated PowerShell prompt."
    exit 1
}

# 2. UMA Dedicated VRAM Configuration (Lenovo WMI BIOS)
Write-Host "`n[1/4] Configuring UMA Dedicated VRAM Allocation..." -ForegroundColor Yellow
try {
    $biosSetter = Get-CimInstance -Namespace root\wmi -ClassName Lenovo_SetBiosSetting -ErrorAction Stop
    $biosSaver  = Get-CimInstance -Namespace root\wmi -ClassName Lenovo_SaveBiosSettings -ErrorAction Stop

    $result = $biosSetter.SetBiosSetting("UMAFramebufferSize,$VramSize")
    if ($result.return -eq "Success" -or $result.ReturnValue -eq $true) {
        $biosSaver.SaveBiosSettings() | Out-Null
        Write-Host "  [OK] Dedicated UMA VRAM set to $VramSize (Takes effect after reboot)." -ForegroundColor Green
    } else {
        Write-Warning "  [WARN] BIOS returned: $($result.return). You can set this manually in BIOS: Config -> Display -> UMA Frame buffer Size -> $VramSize."
    }
} catch {
    Write-Warning "  [WARN] Lenovo WMI BIOS interface not accessible. Set manually in BIOS (F1 on boot -> Config -> Display -> UMA Frame buffer Size -> $VramSize)."
}

# 3. CPU Power, Boost & Cooling Policy (powercfg)
Write-Host "`n[2/4] Applying Thermal & CPU Power Configurations..." -ForegroundColor Yellow

$SUB_PROC    = "54533251-82be-4824-96c1-47b60b740d00"
$SYSCOOLPOL  = "94d3a615-a899-4ac5-ae2b-e4d8f634367f" # System Cooling Policy
$PERFBOOST   = "be337238-0d82-4146-a960-4f3749d470c7" # Processor Boost Mode
$THROTTLEMAX = "bc5038f7-23e0-4960-96da-33abaf5935ec" # Max Processor State
$THROTTLEMIN = "893dee8e-2bef-41e0-89c6-b55d0929964c" # Min Processor State

# Unhide power settings so they can be managed via UI and CLI
powercfg -attributes $SUB_PROC $SYSCOOLPOL -ATTRIB_HIDE | Out-Null
powercfg -attributes $SUB_PROC $PERFBOOST -ATTRIB_HIDE  | Out-Null

# System cooling policy -> Passive (0)
# Slows processor before turning on fan; prevents sudden fan ramp-ups on transient loads
powercfg /setacvalueindex SCHEME_CURRENT $SUB_PROC $SYSCOOLPOL 0 | Out-Null
powercfg /setdcvalueindex SCHEME_CURRENT $SUB_PROC $SYSCOOLPOL 0 | Out-Null
Write-Host "  [OK] System Cooling Policy set to Passive (AC & Battery)." -ForegroundColor Green

# Performance boost mode -> Efficient Enabled (3)
# Keeps CPU at cool base clock for casual tasks, boosts to 4.2GHz only under sustained real load
powercfg /setacvalueindex SCHEME_CURRENT $SUB_PROC $PERFBOOST 3 | Out-Null
powercfg /setdcvalueindex SCHEME_CURRENT $SUB_PROC $PERFBOOST 3 | Out-Null
Write-Host "  [OK] Processor Boost Mode set to Efficient Enabled (AC & Battery)." -ForegroundColor Green

# Max processor state -> 100% (Full 4.2 GHz boost unlocked when needed)
powercfg /setacvalueindex SCHEME_CURRENT $SUB_PROC $THROTTLEMAX 100 | Out-Null
powercfg /setdcvalueindex SCHEME_CURRENT $SUB_PROC $THROTTLEMAX 100 | Out-Null
Write-Host "  [OK] Maximum Processor State set to 100% (Full 4.2 GHz headroom available)." -ForegroundColor Green

# Min processor state -> 5%
powercfg /setacvalueindex SCHEME_CURRENT $SUB_PROC $THROTTLEMIN 5 | Out-Null
powercfg /setdcvalueindex SCHEME_CURRENT $SUB_PROC $THROTTLEMIN 5 | Out-Null
Write-Host "  [OK] Minimum Processor State set to 5%." -ForegroundColor Green

# Commit active scheme
powercfg /setactive SCHEME_CURRENT | Out-Null

# 4. Hardware-Accelerated GPU Scheduling (HAGS)
Write-Host "`n[3/4] Enabling Hardware-Accelerated GPU Scheduling (HAGS)..." -ForegroundColor Yellow
$gfxPath = "HKLM:\SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
if (Test-Path $gfxPath) {
    Set-ItemProperty -Path $gfxPath -Name "HwSchMode" -Value 2 -Type DWord -Force
    Write-Host "  [OK] HAGS enabled (HwSchMode = 2)." -ForegroundColor Green
}

# 5. Developer & Tools Defender Exclusions
Write-Host "`n[4/4] Configuring Defender Real-Time Scanning Exclusions..." -ForegroundColor Yellow
try {
    $toolsDir = "C:\tools"
    if (Test-Path $toolsDir) {
        Add-MpPreference -ExclusionPath $toolsDir -ErrorAction SilentlyContinue
        Write-Host "  [OK] Excluded '$toolsDir' from real-time antimalware hooks." -ForegroundColor Green
    }
} catch {
    Write-Warning "  [WARN] Could not set Defender exclusions automatically."
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Restoration Completed Successfully!" -ForegroundColor Green
Write-Host " Restart your computer to apply the BIOS UMA changes." -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
