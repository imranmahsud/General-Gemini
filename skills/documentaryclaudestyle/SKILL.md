---
name: documentaryclaudestyle
description: Production-grade faceless forensic engineering documentary video generation system based on Point of Failure. Produces 1080p30 videos with subpixel float crops, animated red highlights, dimming spotlight masks, Natural Earth vector maps, word-synced karaoke amber subtitles, timeline clock widgets, and procedural drone audio.
---

# documentaryclaudestyle: Forensic Engineering Documentary Engine

Use this skill whenever generating, scripting, or rendering forensic engineering disaster documentaries in the "Point of Failure" style.

## Core Rules & Architecture

1. **Resolution & Canvas**: Always 1920x1080 @ 30 fps progressive.
2. **Subpixel Float Rendering**: Render each frame in Python Pillow using float-coordinate cropping (`box=(x0, y0, x0 + vw, y0 + vh)`). Never use CLI `zoompan` to avoid stair-step integer pixel jitter.
3. **Film Texture**: Add precomputed Gaussian grain + radial corner vignette to every frame.
4. **Highlights & Spotlight**: Progressive animated red border tracing (`rect`, `circle`, `arrow`, `line`) with Gaussian-blurred dimming spotlight mask over the failure region.
5. **Screen Graphics**:
   - Word-level synchronized amber subtitles (`#FFB81C` active word, `#F5F5F5` inactive words in `rgba(0,0,0,140)` bubble).
   - Upper-left chapter banner (`PART X · TITLE`).
   - Upper-right timeline clock widget (76pt monospace amber time + silver date + red accent bar).
6. **Vector Cartography**: Mercator projection of Natural Earth GeoJSON with smooth zoom, pulsing pin rings, place labels, and monospace coordinate readout.
7. **Procedural Audio**: Edge-TTS `en-US-ChristopherNeural` (-6% rate, -4Hz pitch), procedural minor drone music bed (A, C, G, Bb root progression), 42 Hz heartbeat pulse, and procedural SFX (`sfx_whoosh`, `sfx_hit`, `sfx_blip`).
8. **Mastering**: Soft-clip `tanh`, mastered to -14 LUFS (`loudnorm=I=-14:TP=-1.5:LRA=11`).
