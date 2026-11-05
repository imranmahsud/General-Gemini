---
name: character-timeline-animation
description: Master prompt framework and generation tools for consistent 2D/3D character design (multi-angle turnaround sheets) and timestamped timeline video generation (5-parameter temporal blocks) across local and cloud video diffusion engines.
---

# Character Consistency & Timeline Video Animation Framework

This skill establishes the production standard for generating consistent character animation and coherent multi-scene video sequences across modern video generation engines (FreeVideo, MiniMax, Runway, Kling, ComfyUI, MoneyPrinterTurbo).

---

## 1. Core Principles

1. **Character Persistence Over Random Generation**:
   Never prompt a scene directly without first establishing an authoritative Character Reference Sheet. Lock the facial geometry, clothing distress, color palette, and lighting vector before animating.
2. **5-Parameter Temporal Decomposition**:
   Decompose video timelines into discrete 2-to-3-second blocks. Every block must specify five synchronized parameters: **Camera**, **Action**, **Expressions**, **Dialogue**, and **Sound**.
3. **Zero Hallucination / Clutter Constraints**:
   Enforce strict negative constraints: clean neutral background, no floating logos, no random text, and identical clothing/proportions across views.

---

## 2. Character Reference Sheet Prompt Architecture

Use this blueprint to generate consistent reference sheets with 2D/3D image generation models:

```text
[Character Name & Role]
Create an original, full-body character design for [Character Description & Age], using a [Visual Style, e.g. cinematic painterly 2D cartoon / hand-drawn comic animation].
[Physical Traits]: Build, facial features, hair, posture, and facial expression indicating emotional state.
[Attire & Textures]: Specific clothing items, visible fabric creases, wear/distress, color accents. Keep design readable.
[Style & Art Direction]: Bold line weight, graphic shapes, shading technique (painterly blocks vs gradients).
[Color Palette & Lighting]: Explicit color tones (e.g., deep charcoal, dusty brown, amber key light at 45 degrees).
[Composition Constraint]: Character reference sheet composition: clean neutral background, full-body front view, three-quarter view, profile side view, plus small close-up of face and hands. Keep exact same face, clothing, build, colours, and proportions in every view. No text, labels, logos, or extra characters.
```

---

## 3. Second-by-Second Timeline Video Prompt Format

When generating multi-second video clips (in FreeVideo or cloud diffusion models), format the timeline into synchronized blocks:

```text
[N]-second timeline prompt — "[Scene Title]"
Style: [Art style description, lighting, environmental ambiance, tone].

0:00-0:02 — [Segment 1 Title]
Camera: [Lens angle, shot size, and camera motion, e.g. Wide establishing shot with slow push-in]
Action: [Primary kinematics and secondary physical movements]
Expressions: [Eye direction, facial expressions, micro-reactions]
Dialogue: [Character Name]: "[Exact spoken words]"
Sound: [Foley effects, environmental audio, scoring cue]

0:02-0:05 — [Segment 2 Title]
Camera: [Hard cut / pan / low-angle tracking]
Action: [Kinematic progression from previous segment]
Expressions: [Emotional transition beat]
Dialogue: [Character Name]: "[Exact spoken words]"
Sound: [Sound effects synchronization]
```

---

## 4. Automation Utilities

The skill includes two standalone CLI scripts located in `scripts/`:

1. `generate_character_sheet_prompt.py`: Prompts for character attributes and outputs a formatted reference sheet prompt.
2. `generate_timeline_prompt.py`: Converts a storyboard outline or script into 5-parameter temporal blocks ready for video generation engines.
