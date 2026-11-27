---
name: raea
description: Render Anything Engine (RAEA). GPU-accelerated video, motion graphics, 3D scenes, and interactive compositions written in React and TypeScript. Use when rendering high-performance video timelines, generative animations, or 3D viewports locally on GPU.
---

# RAEA (Render Anything Engine for Anyone)

RAEA is an agent-first GPU render engine designed for building videos, motion graphics, 3D scenes, and interactive experiences using React, TypeScript, and Rust/Bevy. It renders compositions locally on your GPU significantly faster than real-time playback.

- **Local Repository**: `C:\tools\raea`
- **Official Docs**: `https://raea.io` | GitHub: `shinyobjectz/raea`

## Core Architectural Capabilities

1. **Agent-in-the-Loop GPU Rendering**:
   - Write declarative React + TypeScript scenes.
   - Trigger headless or viewport GPU rendering.
   - Inspect rendered frame buffers or video files, critique visual quality, and iteratively fix styling or animation errors.
2. **Motion Graphics & Typography**:
   - Layout engine with Tailwind CSS, typography, and SVG animation primitives.
   - Smooth interpolation, spring physics, and timeline sequencing.
3. **3D Scene Composition**:
   - Bevy-powered 3D renderer supporting glTF models, PBR materials, Gaussian splatting, and camera rigging.
4. **Format Pipeline**:
   - Export video as MP4 (H.264 / AV1), WebM, transparent MOV (ProRes / Alpha), image sequences (PNG), or interactive web apps.

## Standard Project Layout

```text
my-raea-project/
├── raea.config.ts        # Project resolution, framerate, and engine flags
├── package.json          # Dependencies (raea SDK, react, tailwind)
└── src/
    ├── scenes/           # React scene compositions
    │   ├── Intro.tsx
    │   └── Telemetry.tsx
    └── index.tsx         # Root composition timeline
```

## CLI & Workflow Patterns

- **Dev Viewport**:
  ```bash
  npx raea dev
  ```
  Launches interactive GPU preview with live hot-reloading for visual inspection.

- **Headless Render**:
  ```bash
  npx raea render --entry src/index.tsx --output dist/render.mp4 --fps 30 --gpu
  ```

- **Frame Auditing & QA**:
  Render a single frame for visual verification:
  ```bash
  npx raea render --frame 45 --output dist/audit_f45.png
  ```

## Integration with Video Pipelines

RAEA complements HyperFrames and Remotion:
- Use **RAEA** for GPU-intensive 3D scenes, dense telemetry grids, complex particle systems, and high-framerate motion graphics.
- Use **Remotion / HyperFrames** for structured narrative documentaries (`documentary001`) and standardized forensic dossiers.
