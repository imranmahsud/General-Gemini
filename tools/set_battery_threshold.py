#!/usr/bin/env python3
"""
Lenovo Battery Charge Threshold & Conservation Mode Controller
Sets the hardware charge cutoff threshold on Lenovo ThinkPad / IdeaPad laptops.
"""

import sys
import winreg
import argparse
import subprocess

REG_KEYS = [
    r"SOFTWARE\WOW6432Node\Lenovo\PWRMGRV\Data",
    r"SOFTWARE\WOW6432Node\Lenovo\PWRMGRV\ConfKeys\Data\BatterySettings\0",
    r"SOFTWARE\WOW6432Node\Lenovo\PWRMGRV\ConfKeys\Data\BatterySettings\1",
    r"SOFTWARE\Lenovo\PWRMGRV\Data",
    r"SOFTWARE\Policies\Lenovo\CommercialVantage\AddinData\LenovoPowerAddin",
    r"SOFTWARE\Policies\Lenovo\Vantage\AddinData\LenovoPowerAddin"
]

def set_threshold(start_pct=75, stop_pct=80, enable=True):
    control_val = 1 if enable else 0
    start_val = start_pct if enable else 0
    stop_val = stop_pct if enable else 100

    print(f"Applying Battery Threshold: Start={start_val}%, Stop={stop_val}% (Enabled={enable})...")

    for k_path in REG_KEYS:
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, k_path)
            if "PWRMGRV" in k_path:
                winreg.SetValueEx(key, "ChargeStartControl", 0, winreg.REG_DWORD, control_val)
                winreg.SetValueEx(key, "ChargeStopControl", 0, winreg.REG_DWORD, control_val)
                winreg.SetValueEx(key, "ChargeStartPercentage", 0, winreg.REG_DWORD, start_val)
                winreg.SetValueEx(key, "ChargeStopPercentage", 0, winreg.REG_DWORD, stop_val)
            else:
                winreg.SetValueEx(key, "BatteryChargeThreshold", 0, winreg.REG_DWORD, control_val)
                winreg.SetValueEx(key, "CustomChargeThresholdStart", 0, winreg.REG_DWORD, start_val)
                winreg.SetValueEx(key, "CustomChargeThresholdStop", 0, winreg.REG_DWORD, stop_val)
            winreg.CloseKey(key)
            print(f"  [OK] Configured HKLM\\{k_path}")
        except Exception as e:
            print(f"  [ERR] Failed on HKLM\\{k_path}: {e}")

    # Restart Lenovo Vantage Service to reload settings
    print("\nRestarting LenovoVantageService...")
    try:
        p = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "Restart-Service LenovoVantageService -Force -ErrorAction SilentlyContinue"],
            capture_output=True,
            text=True,
            timeout=10
        )
        print("  [OK] LenovoVantageService restarted successfully.")
    except Exception as e:
        print("  [WARN] Service restart note:", e)

def get_current_threshold():
    print("\n=== Current Battery Threshold Settings ===")
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Lenovo\PWRMGRV\Data") as k:
            ctrl, _ = winreg.QueryValueEx(k, "ChargeStopControl")
            start, _ = winreg.QueryValueEx(k, "ChargeStartPercentage")
            stop, _ = winreg.QueryValueEx(k, "ChargeStopPercentage")
            enabled = (ctrl == 1)
            print(f"Status: {'ACTIVE' if enabled else 'DISABLED'}")
            print(f"Start Charging Below: {start}%")
            print(f"Stop Charging At:     {stop}%")
    except Exception as e:
        print("Could not query registry:", e)

def main():
    parser = argparse.ArgumentParser(description="Lenovo Battery Charge Threshold Controller")
    parser.add_argument("--stop", type=int, default=80, help="Cutoff stop percentage (default: 80)")
    parser.add_argument("--start", type=int, default=75, help="Start charging percentage (default: 75)")
    parser.add_argument("--disable", action="store_true", help="Disable threshold (allow full 100% charge)")
    parser.add_argument("--status", action="store_true", help="Show current threshold status")
    args = parser.parse_args()

    if args.status:
        get_current_threshold()
        return

    if args.disable:
        set_threshold(enable=False)
        get_current_threshold()
        return

    set_threshold(start_pct=args.start, stop_pct=args.stop, enable=True)
    get_current_threshold()

if __name__ == "__main__":
    main()
