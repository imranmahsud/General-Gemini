---
name: documentary001
description: Forensic engineering and technical documentary video style using HyperFrames, neural TTS voiceover synchronization, procedural SFX sound design, archival photo integration, telemetry cards, and cinematic outro (code word: documentary001). Use whenever the user mentions 'documentary001' or requests an incident forensic documentary in this exact style.
---

# Documentary 001: Forensic Engineering Video Style

`documentary001` is a forensic engineering documentary style perfected on real-world civil and structural disaster investigations. It pairs technical HUD telemetry, vector schematic failure diagrams, authentic historical photography, neural voiceover, and a structured 5-piece sound design into a 68-second cinematic case study.

Whenever the user references **`documentary001`** or asks to make a documentary in this style, follow the exact narrative structure, visual tokens, audio architecture, and rendering pipeline defined below.

---

## 1. Visual Identity & Design Tokens

The aesthetic mimics a high-security military or forensic investigation terminal:

- **Resolution**: 1920x1080 @ 30 FPS (`format: mp4`, SDR BT.709).
- **Background**: Radial vignette (`radial-gradient(circle at 50% 25%, #131c2e 0%, #06080d 100%)`) with an overlaid 60px fine cyan telemetry grid (`linear-gradient` with `rgba(56, 189, 248, 0.035)`).
- **Color Palette**:
  - Background Primary: `#080b11`
  - Panel Background: `#0f172a`
  - Cyan Telemetry / Safe: `#38bdf8`
  - Amber Warning / Flaw: `#f59e0b`
  - Red Hazard / Catastrophe: `#ef4444`
  - Text White: `#f8fafc`
  - Text Dim: `#94a3b8`
  - Text Subtle: `#64748b`
- **Typography**:
  - `JetBrains Mono`: All classifications, coordinates, timecodes, metrics, and tags.
  - `Inter`: Dominant headlines, executive summaries, and forensic analysis prose.
- **HUD Frame Standards**:
  - Header: Left dossier badge (`● DOSSIER // <ID>`), center classification status, right timecode.
  - Footer: Source report attribution, audio configuration status, completion stamp.
  - Photo Frames: `border: 1px solid rgba(56, 189, 248, 0.25)`, `border-radius: 8px`, `box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6)`. Every photo includes an absolute `.photo-tag` pill in `JetBrains Mono` stating the exact date, timestamp, and location of the photograph.
  - Continuous Motion: All photos execute a slow Ken Burns zoom (`scale: 1.05 -> 1.0` over the act duration) to prevent static render holds and dead-stretch warnings.

---

## 2. The 5-Act Forensic Narrative Arc (68.0 Seconds)

Every `documentary001` production follows a strict 5-act dramatic structure:

| Act | Time Range | Title | Core Visual Elements | Narration Focus | SFX Cues |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Act 1** | `0.0s – 13.5s` | **Executive Dossier & Incident Overview** | Hazard badge, dominant title, 4 metric boxes (discharge, loss, height, date), hero archival photo. | Magnitude of incident, location, date, and sudden catastrophic nature. | UI Click (`1.0s`), Whoosh (`13.2s`) |
| **Act 2** | `13.5s – 27.0s` | **Anatomy & Failure Mechanism** | 2D SVG cross-section blueprint, animated dashed seepage vector, pulsing piping root, initial seep photo, 3 vulnerability cards. | Physical root mechanism: geology, hydraulic gradient, piping, missing defensive filters. | Bass Impact on breach node (`17.5s`) |
| **Act 3** | `27.0s – 40.5s` | **Chronology of Catastrophe** | Dual progression photos (early breach vs crest collapse), 4 time-stamped milestone cards, peak discharge alert banner. | Minute-by-minute progression on the morning of failure, frantic remediation, crest breach. | Tension Riser (`32.0s`) |
| **Act 4** | `40.5s – 54.0s` | **Forensic Root Cause Verdict** | Full breach catastrophic flood photo, official inquiry header, 3–4 fault classification cards (Design, Geology, Filters). | Formal inquiry findings, engineering deficiencies, accountability determination. | Whoosh transition (`53.5s`) |
| **Act 5** | `54.0s – 68.0s` | **Investigation Concluded & Legacy (The Outro)** | Dossier Sealed badge, post-disaster aftermath monument photo, 4 memorial metrics, legacy principle, cinematic fade to black. | Permanent engineering reforms, updated standard criteria, memorial statistics. | Resolving Chime (`55.0s`), Fade out (`66.4s`) |

### Act 5 Outro & Fade-to-Black Rule
- Between `66.4s` and `68.0s`, a top-layer `#blackout` overlay (`background: #000000; z-index: 100`) animates from `opacity: 0` to `1` with `ease: power2.inOut`.
- Concurrently, the master audio volume decays over 2.5 seconds (`afade=t=out:st=65.5:d=2.5`), preventing any abrupt cut.

---

## 3. Audio Engineering & Deterministic Sound Design

Never rely on browser-level multi-track audio during headless video rendering. All audio must be mixed into a single synchronized master track:

### Narration Guidelines
- **TTS Engine**: `edge-tts` (Offline / high-speed cloud neural speech).
- **Default Voice**: `en-US-ChristopherNeural` (deep, measured, documentary cadence) or `en-US-GuyNeural`.
- **Timing**: Each act's narration must stay between 10.0 and 11.5 seconds so it finishes cleanly before the act transition.

### The 5 Reusable SFX Tracks
The skill ships with 5 core audio assets located in `assets/audio/`:
1. `whoosh-cinematic.mp3`: Dramatic scene transition sweep.
2. `click-soft.mp3`: Subtle high-tech HUD element activation.
3. `impact-bass-1.mp3`: Sub-bass drop for catastrophic structural failure or piping initiation.
4. `riser.mp3`: Ascending tension riser for the chronological breach sequence.
5. `chime.mp3`: Clean tonal resolution chord for the Act 5 closing legacy.

### Deterministic Audio Mix Command
```bash
ffmpeg -y \
  -i assets/audio/act1.mp3 \
  -i assets/audio/act2.mp3 \
  -i assets/audio/act3.mp3 \
  -i assets/audio/act4.mp3 \
  -i assets/audio/act5.mp3 \
  -i assets/audio/whoosh-cinematic.mp3 \
  -i assets/audio/click-soft.mp3 \
  -i assets/audio/impact-bass-1.mp3 \
  -i assets/audio/riser.mp3 \
  -i assets/audio/chime.mp3 \
  -filter_complex "\
    [0:a]adelay=300|300,volume=1.0[n1];\
    [1:a]adelay=14000|14000,volume=1.0[n2];\
    [2:a]adelay=27500|27500,volume=1.0[n3];\
    [3:a]adelay=41000|41000,volume=1.0[n4];\
    [4:a]adelay=54500|54500,volume=1.0[n5];\
    [5:a]adelay=13200|13200,volume=0.35[w1];\
    [6:a]adelay=1000|1000,volume=0.30[c1];\
    [7:a]adelay=17500|17500,volume=0.45[b1];\
    [8:a]adelay=32000|32000,volume=0.30[r1];\
    [9:a]adelay=55000|55000,volume=0.35[ch1];\
    [n1][n2][n3][n4][n5][w1][c1][b1][r1][ch1]amix=inputs=10:duration=first:dropout_transition=2[mixed];\
    [mixed]apad=whole_dur=68,afade=t=out:st=65.5:d=2.5[outa]" \
  -map "[outa]" -c:a libmp3lame -b:a 192k \
  -map_metadata -1 -fflags +bitexact \
  assets/audio/master_audio.mp3
```

---

## 4. Execution Workflow

When creating a new video with `documentary001`:

### Step 1: Scaffold Project Directory
Run the automated scaffolding script from this skill:
```powershell
python "C:\Users\Imran\.gemini\config\skills\documentary001\scripts\scaffold_documentary.py" "<project_name>" --dest "."
```
This sets up `index.html`, `hyperframes.json`, `package.json`, `assets/images/`, `assets/audio/`, and bundles all 5 standard SFX tracks.

### Step 2: Download Real Archival Images
Fetch 5 high-resolution historical photos representing:
- `01_hero.jpg`: Pre-failure structure or establishing wide shot.
- `02_mechanism.jpg`: Initial leak, crack, or defect emergence.
- `03_progression_a.jpg` & `03_progression_b.jpg`: Collapse progression.
- `04_full_catastrophe.jpg`: Peak breach or impact moment.
- `05_aftermath.jpg`: Current day or post-collapse monument.

### Step 3: Author Script & Generate Master Audio
Edit `build_audio.py` in the project root with the 5 Act voiceover texts, then execute:
```powershell
python build_audio.py
```

### Step 4: Validate Composition
Ensure zero lint, layout, contrast, or audio warnings:
```powershell
npx.cmd hyperframes check --json
```

### Step 5: Render & Metadata Scrub
Render the video using HyperFrames, then immediately strip all tool and AI metadata to bitexact standards:
```powershell
# Render headless
npx.cmd hyperframes render --quality looks -o output.mp4

# Scrub metadata (Clean File Metadata Standard)
ffmpeg -y -i output.mp4 -c copy -map_metadata -1 -fflags +bitexact -flags:v +bitexact -flags:a +bitexact clean_output.mp4
Move-Item -Force clean_output.mp4 output.mp4
```

---

## 5. Reference Project
The verified, reference implementation is permanently preserved at:
- Reference HTML: [`templates/reference_teton.html`](file:///C:/Users/Imran/.gemini/config/skills/documentary001/templates/reference_teton.html)
- Clean Template: [`templates/template.html`](file:///C:/Users/Imran/.gemini/config/skills/documentary001/templates/template.html)
- Reusable SFX: [`assets/audio/`](file:///C:/Users/Imran/.gemini/config/skills/documentary001/assets/audio/)
