---
name: openworker-agent
description: Autonomous desktop AI co-worker framework by Andrew Ng (AI Fund). Executes end-to-end tasks, coordinates tools with human approval, and supports local Ollama or cloud LLM backends via aisuite.
---

# OpenWorker Desktop Agent Guide

## Overview

`OpenWorker` (`andrewyng/openworker`) is an open-source, local-first autonomous desktop agent framework. Unlike conventional prompt/response chatbots, it runs multi-step task loops (gathering research, organizing workspaces, running code, assembling documents) until a finished deliverable is produced.

Repository Path: `C:\tools\openworker`

---

## Architecture & Features

1. **Aisuite Core**: Unified model interface supporting OpenAI, Anthropic, Gemini, Groq, and local Ollama (`qwen2.5:7b`).
2. **Human-in-the-Loop Governance**: File modifications and shell command execution can be gated behind interactive human approval.
3. **OpenWorker Harness SDK**: TypeScript and Rust interfaces to compose custom subagents and specialized desktop copilots.

---

## Local Setup

```powershell
cd C:\tools\openworker
python -m pip install -e .
python -m openworker --model ollama:qwen2.5:7b
```
