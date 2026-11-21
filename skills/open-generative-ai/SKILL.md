---
name: open-generative-ai
description: Unified multi-model visual generation interface for image and video synthesis using Open Generative AI. Run 600+ cloud and local generation backends with bring-your-own-keys (BYOK) or zero-cost local weights.
---

# Open Generative AI Workflow Guide

## Overview

`Open Generative AI` (`Anil-matcha/Open-Generative-AI`) is an open-source, full-stack studio alternative to closed-source video generation suites (such as Higgsfield, Runway, and Luma). It supports over 600 diffusion, video generation, and transformer models.

Repository Path: `C:\tools\open-generative-ai`

---

## Capabilities

1. **Multi-Model Unification**: Single interface connecting Flux, SDXL, Wan 2.1/2.2, LTX-Video, CogVideoX, and proprietary APIs via BYO API keys.
2. **Local Engine**: Connects to local ComfyUI or native Diffusers pipelines at zero cloud cost.
3. **Batch Generation**: Scriptable prompts and camera trajectories across scene transitions.

---

## Local Setup & Launch

```powershell
cd C:\tools\open-generative-ai
npm install
npm run dev
```
Open `http://localhost:3000` to access the generation studio.
