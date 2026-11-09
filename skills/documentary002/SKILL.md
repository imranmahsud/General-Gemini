---
name: documentary002
description: Forensic engineering and technical incident documentary video style using HyperFrames, locked-in neural voiceover and audio architecture from documentary001 (code word: documentary002). Use whenever the user mentions 'documentary002' or requests a documentary in this style.
---

# Documentary 002: Forensic Engineering Video Style

`documentary002` is a forensic engineering documentary style that locks in the voiceover style, voice model, narrative pacing, and sound design from `documentary001`, combined with technical HUD telemetry, vector schematic failure diagrams, authentic historical photography, and a 5-act dramatic arc.

Whenever the user references **`documentary002`** or asks to make a video in this style, follow the exact narrative structure, locked voice configuration, visual tokens, and rendering pipeline defined below.

---

## 1. Locked Voiceover & Sound Design (Inherited from `documentary001`)

The hallmark of `documentary002` is its locked voiceover and sound design configuration:

### Neural Voice Specification
- **Engine**: `edge-tts` (broadcast-quality neural synthesis).
- **Voice Model**: `en-US-ChristopherNeural` (deep, measured, authoritative investigative timbre).
- **Alternative Match**: `en-US-GuyNeural` (formal archival presentation).
- **Cadence & Script Pacing**:
  - Each act features a strictly bounded script duration: `10.0s – 11.8s`.
  - Speech rate: Normal (`--rate=+0%`), Pitch: Normal (`--pitch=+0Hz`).
  - Narrative tone: Forensic, detached, technical, devoid of AI clichés and filler.

### 5-Piece Reusable SFX Suite (`assets/audio/`)
1. `whoosh-cinematic.mp3`: Act transition sweeps (`13.2s`, `53.5s`).
2. `click-soft.mp3`: Subtle high-tech HUD element activation (`1.0s`, `14.4s`, `28.0s`).
3. `impact-bass-1.mp3`: Sub-bass drop for catastrophic structural failure or piping initiation (`17.5s`).
4. `riser.mp3`: Ascending tension riser during the chronological breach sequence (`32.0s`).
5. `chime.mp3`: Clean tonal resolution chord for the Act 5 closing legacy (`55.0s`).

### Master Soundtrack Mix Architecture
All audio tracks must be combined into a single, deterministic master file (`assets/audio/master_audio.mp3`) before rendering:
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
    [n1][n2][n3][n4][n5][w1][c1][b1][r1][ch1]amix=inputs=10:duration=longest:dropout_transition=2[mixed];\
    [mixed]apad=whole_dur=68,afade=t=out:st=65.5:d=2.5[outa]" \
  -map "[outa]" -c:a libmp3lame -b:a 192k \
  -map_metadata -1 -fflags +bitexact \
  assets/audio/master_audio.mp3
```

---

## 2. Visual Identity & Design Tokens

- **Resolution**: 1920x1080 @ 30 FPS (`format: mp4`, SDR BT.709).
- **Background**: Radial vignette (`radial-gradient(circle at 50% 25%, #131c2e 0%, #06080d 100%)`) with 60px cyan telemetry grid overlay (`rgba(56, 189, 248, 0.035)`).
- **Color Tokens**:
  - Background: `#080b11`, Panel: `#0f172a`
  - Cyan Telemetry: `#38bdf8`
  - Amber Warning: `#f59e0b`
  - Red Hazard: `#ef4444`
  - Text: White `#f8fafc`, Dim `#94a3b8`, Subtle `#64748b`
- **Typography**:
  - `JetBrains Mono`: Classifications, timecodes, coordinates, tags, metrics.
  - `Inter`: Primary headers, body narratives, and summary cards.
- **Motion & Frame Standards**:
  - Photos inside HUD frames with `.photo-tag` metadata pills.
  - Continuous subtle Ken Burns scaling (`scale: 1.05 -> 1.0`) on all image frames.
  - `#blackout` overlay on top layer (`z-index: 100`) animating from `0` to `1` over the final 1.6 seconds.

---

## 3. The 5-Act Dramatic Structure (68.0 Seconds)

| Act | Time Range | Title | Core Visual Elements | Narration Style (`en-US-ChristopherNeural`) |
| :--- | :--- | :--- | :--- | :--- |
| **Act 1** | `0.0s – 13.5s` | **Executive Dossier & Incident Overview** | Hazard badge, title, 4 metric boxes, hero archival photo. | Rapid establishing summary of magnitude, location, date, and sudden collapse. |
| **Act 2** | `13.5s – 27.0s` | **Anatomy & Failure Mechanism** | 2D vector blueprint, animated seepage vector, pulsing node, 3 defect cards. | Forensic dissection of physical initiating flaws and geological interaction. |
| **Act 3** | `27.0s – 40.5s` | **Chronology of Catastrophe** | Dual sequential photos, 4 milestone cards, peak discharge banner. | Tense, minute-by-minute timeline from first morning signs to embankment collapse. |
| **Act 4** | `40.5s – 54.0s` | **Forensic Root Cause Verdict** | Full breach flood photo, inquiry board header, 3 fault cards. | Authoritative determination of design failures, specification lapses, and accountability. |
| **Act 5** | `54.0s – 68.0s` | **Investigation Concluded & Legacy (Outro)** | Dossier Sealed badge, monument photo, 4 memorial metrics, legacy principle, fade to black. | Engineering reforms, revised design criteria, permanent safety oversight, and closing fade. |

---

## 4. Scaffold & Render Commands

### Step 1: Scaffold
```powershell
python "C:\Users\Imran\.gemini\config\skills\documentary002\scripts\scaffold_documentary.py" "<project_name>" --dest "."
```

### Step 2: Build Master Audio Track
```powershell
python build_audio.py
```

### Step 3: Validate Composition
```powershell
npx.cmd hyperframes check --json
```

### Step 4: Render & Strip Metadata
```powershell
npx.cmd hyperframes render --quality looks -o output.mp4
ffmpeg -y -i output.mp4 -c copy -map_metadata -1 -fflags +bitexact -flags:v +bitexact -flags:a +bitexact clean_output.mp4
Move-Item -Force clean_output.mp4 output.mp4
```

---

## 5. Reference Project
- Clean Template: [`templates/template.html`](file:///C:/Users/Imran/.gemini/config/skills/documentary002/templates/template.html)
- Verified Reference: [`templates/reference_teton.html`](file:///C:/Users/Imran/.gemini/config/skills/documentary002/templates/reference_teton.html)
- SFX Assets: [`assets/audio/`](file:///C:/Users/Imran/.gemini/config/skills/documentary002/assets/audio/)
