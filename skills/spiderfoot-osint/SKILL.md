---
name: spiderfoot-osint
description: Automated OSINT intelligence gathering, reconnaissance, attack surface mapping, and domain/IP investigation using SpiderFoot. Scan targets across 200+ public and threat-intelligence sources.
---

# SpiderFoot OSINT Reconnaissance Guide

## Overview

`SpiderFoot` (`smicallef/spiderfoot`) is an open-source intelligence (OSINT) automation platform. It queries over 200 data sources to gather intelligence on IP addresses, domain names, e-mail addresses, phone numbers, Bitcoin addresses, and network subnets.

Repository Path: `C:\tools\spiderfoot`
Launcher: `C:\tools\spiderfoot.bat`

---

## Capabilities

1. **Target Types**: Domain names, hostnames, IP subnets (CIDR), e-mail addresses, human names, usernames, phone numbers.
2. **Modules**: Passive DNS, WHOIS, BGP routing, SSL certificates, leaked credentials, darkweb mentions, port scans, cloud asset discovery.
3. **Output Formats**: Interactive web graph UI, CSV, JSON, and SQLite database.

---

## Local Startup

```powershell
cd C:\tools\spiderfoot
python -m pip install -r requirements.txt
python sf.py -l 127.0.0.1:5001
```
Web console runs at `http://127.0.0.1:5001`.
