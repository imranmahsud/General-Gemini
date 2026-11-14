# ThinkPad Optimized Settings for Windows 11

Automated configuration and one-click restoration suite for Lenovo ThinkPad laptops running AMD Ryzen 5000 APUs with Radeon Vega Graphics under Windows 11 / 10.

---

## 🎯 Target Hardware & Scope

- **Platform**: Lenovo ThinkPad (AMD Ryzen 5 / 7 5000 series mobile APUs, e.g., Ryzen 5 PRO 5650U).
- **Graphics**: Integrated AMD Radeon Vega Graphics (Vega 7 / Vega 8).
- **RAM**: 16 GB / 32 GB Dual Channel DDR4.
- **Operating System**: Windows 11 Pro / Enterprise (x64).

---

## ⚡ Quick One-Click Restore

If you fresh install or refresh Windows:

1. Clone or download this repository:
   ```cmd
   git clone https://github.com/imranmahsud/ThinkPadOptimizedSettingsWindows11.git
   cd ThinkPadOptimizedSettingsWindows11
   ```
2. Right-click **`restore.bat`** and select **Run as Administrator** (or run `powershell -ExecutionPolicy Bypass -File .\restore.ps1` from an elevated PowerShell window).
3. Restart your laptop to commit the BIOS UMA VRAM changes.

---

## 🛠️ Optimizations Applied

### 1. Dedicated UMA VRAM Allocation (1 GB ➔ 4 GB)
- **Problem**: Integrated AMD Vega graphics default to 512 MB or 1 GB dedicated VRAM (`Auto`). Heavy CAD, GIS, 3D photogrammetry (VisualSFM, COLMAP), and modern games artificially lock out high-resolution textures or refuse to run despite having 32 GB of system RAM.
- **Fix**: Allocates 4 GB of dedicated UMA Framebuffer via Lenovo WMI BIOS interface (`UMAFramebufferSize,4GB`), leaving 28 GB for system memory.
- **Manual BIOS Alternative**: Press `F1` at boot ➔ `Config` ➔ `Display` ➔ `UMA Frame buffer Size` ➔ `4GB` ➔ `F10` (Save & Exit).

### 2. Intelligent CPU Boost Management (`Efficient Enabled`)
- **Problem**: Windows default power profiles set processor boost to `Aggressive`. On AMD Ryzen mobile chips, this triggers constant 4.2 GHz / 1.4V voltage spikes for trivial micro-tasks (mouse movements, browser tabs, background telemetry), causing erratic temperature spikes and fan spin-up.
- **Fix**: Changes Processor Performance Boost Mode to `Efficient Enabled` (Index 3). The CPU stays at cool base clocks during casual tasks, but instantly engages the full 4.2 GHz clock whenever sustained compute workloads demand it.

### 3. Passive System Cooling Policy
- **Problem**: Active cooling spins the fan up before throttling clocks, creating noisy bursts during transient load blips.
- **Fix**: Changes System Cooling Policy to `Passive` (`SYSCOOLPOL = 0`) across AC and Battery. The system absorbs short thermal blips silently, ramping the fan only under prolonged thermal load.

### 4. 100% Maximum Processor Headroom
- **Target**: Retains `PROCTHROTTLEMAX = 100%` so single-thread and multi-thread peak compute performance is never throttled when executing intensive tasks.

### 5. Hardware-Accelerated GPU Scheduling (HAGS)
- **Fix**: Enables `HwSchMode = 2` under `HKLM:\SYSTEM\CurrentControlSet\Control\GraphicsDrivers` to offload frame scheduling directly to the GPU scheduling processor.

### 6. Developer & Tooling Antivirus Exclusions
- **Fix**: Adds `C:\tools` to Windows Defender real-time scanning exclusions. Prevents Windows Defender (`MsMpEng`) from thrashing CPU and storage when unpacking or compiling large toolchains and photogrammetry datasets.

---

## 🔍 Verification & Audit

To inspect your current configuration at any time, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\audit_settings.ps1
```

The script will output a side-by-side verification table of active system values vs optimal targets.
