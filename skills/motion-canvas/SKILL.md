---
name: motion-canvas
description: Code-driven 2D procedural motion graphics and technical video explainers using Motion Canvas, TypeScript, and Vite. Author programmatic animations, synchronized audio voiceovers, mathematical graphs, and engineering diagrams.
---

# Motion Canvas Workflow Guide

## Overview

Motion Canvas is a programmatic animation engine using TypeScript and generator functions (`function*`). It replaces traditional GUI-based animation tools (After Effects) with version-controlled, pixel-accurate vector animations rendered via HTML5 Canvas and WebGL.

Key paths:
- Monorepo & Studio: `C:\tools\motion-canvas`
- Launcher: `C:\tools\motion-canvas.bat`
- Web Editor URL: `http://localhost:9000`

---

## Core Architecture

1. **Scenes**: Each animation sequence is declared in a `.tsx` file via `makeScene2D(function*(view) { ... })`.
2. **Generators**: Flow control relies on `yield*` to step through time:
   - `yield* all(...)`: Run multiple animations concurrently.
   - `yield* sequence(...)`: Run animations with sequential stagger.
   - `yield* waitUntil("cue_name")`: Synchronize visual transitions to audio timestamps.
3. **Reactive Signals**: Node properties (position, scale, fill, size) are functions that return values or accept target values over a duration.

---

## Standard Scene Template

Create or edit scene files inside `src/scenes/` (or `packages/template/src/scenes/example.tsx`):

```tsx
import {makeScene2D, Circle, Rect, Txt, Path, Line} from '@motion-canvas/2d';
import {all, createRef, easeInOutCubic, waitUntil} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  // References
  const card = createRef<Rect>();
  const title = createRef<Txt>();

  // Scene layout
  view.add(
    <Rect
      ref={card}
      width={600}
      height={300}
      radius={16}
      fill={'#1e293b'}
      stroke={'#38bdf8'}
      lineWidth={3}
      scale={0}
    >
      <Txt
        ref={title}
        text={'ENGINEERING DOSSIER'}
        fontFamily={'JetBrains Mono'}
        fontSize={28}
        fill={'#f8fafc'}
        opacity={0}
      />
    </Rect>,
  );

  // Animation sequence
  yield* all(
    card().scale(1, 0.8, easeInOutCubic),
    title().opacity(1, 0.6),
  );

  yield* waitUntil('next_section');

  yield* all(
    card().position.y(-200, 0.6, easeInOutCubic),
    card().scale(0.8, 0.6),
  );
});
```

---

## Audio & Voiceover Synchronization

1. Place voiceover `.wav` or `.mp3` files in `src/audio/`.
2. Reference the audio file in the project definition:
   ```ts
   import {makeProject} from '@motion-canvas/core';
   import audio from './audio/voiceover.mp3';
   import example from './scenes/example?scene';

   export default makeProject({
     scenes: [example],
     audio: audio,
   });
   ```
3. Use the timeline editor at `http://localhost:9000` to scrub the waveform and place named cues matched to `yield* waitUntil('cue')`.

---

## Rendering to Video

1. In the browser editor panel:
   - Select **Renderer** tab.
   - Set Output format to **Video (MP4)** or **Image Sequence (PNG)**.
   - Select Framerate (60 FPS or 30 FPS) and Resolution (1920x1080 or 3840x2160).
   - Click **Render**.
2. Automated Headless Export via CLI:
   ```powershell
   npm run build
   npx @motion-canvas/cli render --output ./dist/output.mp4
   ```
