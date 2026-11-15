---
name: sherlock
description: Hunt down social media accounts and verify username availability across 400+ online networks and platforms using Sherlock OSINT. Use when the user asks to check username availability, find social media accounts, track an online handle, or investigate an online username.
license: MIT
---

# Sherlock — Social Media Username Hunter & OSINT Tool

`sherlock` searches for an account with a specific username across over 400 social networks and public sites.

## Executable Location

On this system, Sherlock is installed in Python 3.12:
- Path: `C:\Users\Imran\AppData\Local\Programs\Python\Python312\Scripts\sherlock.exe`

## Usage Patterns

### 1. Basic Search (Print only found accounts)
```powershell
& "C:\Users\Imran\AppData\Local\Programs\Python\Python312\Scripts\sherlock.exe" <username> --print-found
```

### 2. Export Results to CSV
```powershell
& "C:\Users\Imran\AppData\Local\Programs\Python\Python312\Scripts\sherlock.exe" <username> --csv --output "<output-folder>\<username>_report" --print-found
```

### 3. Fast Timeout Scan (Prevent hanging on slow endpoints)
```powershell
& "C:\Users\Imran\AppData\Local\Programs\Python\Python312\Scripts\sherlock.exe" <username> --timeout 5 --print-found
```

### 4. Search Multiple Usernames
```powershell
& "C:\Users\Imran\AppData\Local\Programs\Python\Python312\Scripts\sherlock.exe" username1 username2 --print-found
```
