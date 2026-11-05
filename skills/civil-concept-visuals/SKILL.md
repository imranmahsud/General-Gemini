---
name: civil-concept-visuals
description: Standardized prompt templates, design parameters, and automated rendering workflows for generating Google Earth aerial concept visualisations, 3D bridge/road embankment perspectives, and 2D engineering cross sections with technical callout boxes.
---

# Civil Engineering Concept Visualisations & 3D Renderings

This skill establishes the standard execution protocol and prompt formulation for producing presentation-grade civil engineering concept visuals, Google Earth satellite overlays, 3D photorealistic infrastructure perspectives, and engineered 2D cross sections.

---

## 1. Trigger Phrases & Intent Recognition

Activate this skill whenever the user requests:
- *"generate concept imagery / visuals like in Visuals to learn from"*
- *"prepare realistic 3D renderings on Google Earth satellite imagery"*
- *"create aerial concept visualization of bridge / road embankment"*
- *"generate typical road cross section diagram"*
- *"add engineering callout boxes and leader annotations to visualisations"*

---

## 2. The Three Visual Archetypes

### Archetype 1: Google Earth Aerial Concept Visualisation
**Purpose**: High-level corridor planning, PC-I presentations, and public stakeholder alignments.
**Reference Plates** (archived locally in `resources/`):
- `resources/01_alamabad_northern_crossing.png`: Bridge crossing arrangement at CH 0+000 over Bahr Khwar, 2 m raised embankment, 7.315 m roadway formation, and stone pitching armor.
- `resources/02_alamabad_middle_corridor.png`: Embankment corridor through Wahdat Abad village, center-line alignment, and 2H:1V side slopes.
- `resources/04_alamabad_alignment_overview.png`: Full 3.086 km corridor alignment (CH 0+000 to CH 3+086) with Google Earth markers, legend, and stationing.
**Visual Style**:
- Oblique aerial perspective looking down at 45° to 65° onto Google Earth satellite imagery.
- Top banner: Dark semi-transparent pill (`rgba(20,20,20,0.85)`) with white bold text (e.g. `ALAMABAD NORTHERN CROSSING`, `ALAMABAD MIDDLE CORRIDOR`).
- Engineered infrastructure overlaid cleanly onto terrain:
  - 2-lane dark asphalt blacktop with white edge lines and yellow dashed centerline.
  - Raised road embankment with engineered side slopes (typically 2H:1V).
  - Heavy rock riprap / stone pitching armor along water-facing slopes and bridge abutments.
  - Multi-span concrete girder bridge crossing the river/drain with hydrodynamic piers in water.
- High-contrast technical callout boxes:
  - Dark semi-transparent boxes with white border and crisp white text.
  - White leader arrows with dimension spans `<------------->`.
  - Typical callout text:
    - `"Proposed [X] m bridge (overall length) Concrete girder bridge (indicative arrangement)"`
    - `"[X] m total formation ([Y] m carriageway + [Z] m shoulders each side)"`
    - `"[X] m raised embankment with 2H:1V side slopes and stone protection"`
- Footer disclaimer: `"CONCEPT VISUALISATION — illustrative [X] m embankment — not approved design"` and authentic Google Earth UI controls.

### Archetype 2: Photorealistic Drone / Architectural Render (Imagen 3 / Blender)
**Purpose**: Executive feasibility reports, donor agency appraisal (ADB, World Bank), and environmental filings.
**Visual Style**:
- High-resolution (16:9 widescreen) daylight aerial drone shot with realistic raytraced shadows, water Fresnel reflection, and authentic vegetation.
- Parameter-locked civil infrastructure geometry matching actual hydraulic and road design criteria.
- Integrated crisp engineering annotation callout labels:
  - `Carriageway (Asphalt)`
  - `Compacted Subgrade`
  - `Raised Embankment Fill (Soil/Rock)`
  - `Class-A Stone Riprap Armour Protection`
  - `Galvanized W-Beam Guardrail`
  - `Design High Flood Level (100-Year HFL)`
  - `Hydrodynamic Pier (Founding Level below Scour)`

### Archetype 3: 2D Engineered Typical Road Section Diagram
**Purpose**: Standard geometric design plates, tender BOQ drawings, and technical report figures.
**Visual Style**:
- Clean 2D engineering cross section diagram (using Matplotlib / vector graphic).
- Shows:
  - Nominal ground datum line at $y = 0$.
  - Symmetrical trapezoidal embankment fill prism with labeled slope (e.g., `2H:1V`).
  - Road formation width callout (e.g., `24 ft formation / 7.315 m`).
  - Carriageway blacktop width callout (e.g., `18 ft blacktop / 5.486 m`) with 2% crown camber.
  - Pavement structural layers annotation: `50 mm asphalt wearing course + 150 mm base + 200 mm subbase`.

---

## 3. Standard Copy-Paste Prompt Templates for Future Use

### Template A: Master Full-Corridor Request
```text
Generate aerial civil engineering concept imagery for [PROJECT NAME] in [LOCATION] matching the style of Google Earth concept visualisations with technical callout boxes:
1. Northern / Bridge Crossing View: [Span, e.g. 64 m / 210 ft, 4 spans, prestressed girders, piers, abutments, riprap armor].
2. Middle Corridor Embankment View: [Length, e.g. 3.8 km, 28 ft formation, 20 ft blacktop, 2 m embankment, 2H:1V slopes, stone pitching facing drain, W-beam guardrail].
3. Southern Approach / Junction View: [Embankment connection to local rural road network].
4. Typical Cross Section Diagram: [2D engineered prism showing blacktop, formation, 2H:1V slope, and pavement layer callouts].
Include leader callouts, dimension lines, top location banner, and bottom concept disclaimer.
```

### Template B: Dedicated Bridge Crossing Concept
```text
Generate an aerial concept visualization of the [BRIDGE NAME] in [LOCATION].
Parameters:
- Bridge span: [X] meters ([Y] ft) overall length across [RIVER/DRAIN NAME].
- Superstructure: [N] clear spans of precast prestressed concrete I-girders with RCC deck slab and crash barriers.
- Substructure: Hydrodynamic rounded concrete piers in river water and solid abutments with stone riprap protection.
- Approaches: 2-lane asphalt road on [X] m raised embankment with 2H:1V side slopes.
- Overlays: Top banner '[LOCATION] CROSSING', dimension callout box for bridge length, formation width callout, and riprap armor callout.
- Perspective: Oblique aerial Google Earth / drone viewpoint under bright daylight.
```

### Template C: Dedicated Road on Embankment Corridor
```text
Generate an aerial concept visualization of [ROAD NAME] on embankment along [RIVER/DRAIN NAME] in [LOCATION].
Parameters:
- Carriageway: 2-lane dark asphalt paved surface ([X] ft / [Y] m wide) with yellow dashed centerline and white edge lines.
- Embankment: Raised [X] m above natural ground with 2H:1V side slopes.
- Flood Protection: Heavy grey boulder riprap / stone pitching lining the water-facing slope.
- Road Safety: Galvanized steel W-beam guardrail along the water-side shoulder.
- Overlays: Callouts for '20 ft Paved Carriageway', '2m Raised Embankment', 'Stone Riprap Armour', and 'Galvanized W-Beam Guardrail'.
- Viewpoint: Oblique drone shot along the curving river corridor showing surrounding agrarian fields.
```

---

## 4. Parameter Specification Table

When requesting concept visuals, providing values for these 6 parameters ensures 100% engineering accuracy:

| Parameter | Recommended Input | Engineering Significance |
| :--- | :--- | :--- |
| **Location & Channel** | Tehsil, District, River/Drain Name | Sets landscape context (Indus plains, Swabi soils, local architecture) |
| **Bridge Span & Spans** | Total length (m/ft) & number of spans | Dictates pier spacing, girder depth, and waterway opening |
| **Road Widths** | Formation width & Carriageway width | AASHTO / Provincial C&W road classification standard |
| **Embankment Height** | Height in meters / feet above NSL | Freeboard margin above design high flood level (100-year HFL) |
| **Side Slope Ratio** | Horizontal : Vertical (e.g. 2H:1V) | Geotechnical stability ratio for compacted common borrow fill |
| **Slope Armor** | Class-A stone pitching / boulder riprap | Erosion resistance against design channel velocity ($V > 2.5\text{ m/s}$) |

---

## 5. Automated Python Callout Compositing Script

Use this utility to stamp standardized callout boxes, dimension arrows, and Google Earth banners onto any rendered base image:

```python
import os
from PIL import Image, ImageDraw, ImageFont

def add_engineering_callout(image_path, output_path, title_text, callouts):
    """
    image_path: Input aerial/satellite image
    output_path: Path to save annotated image
    title_text: Top banner text (e.g. 'ALAMABAD NORTHERN CROSSING')
    callouts: List of dicts with {'box_xy': (x, y), 'text': str, 'arrow_to': (x, y)}
    """
    im = Image.open(image_path).convert('RGBA')
    overlay = Image.new('RGBA', im.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    # 1. Top Banner
    w, h = im.size
    banner_w, banner_h = int(w * 0.35), 55
    draw.rounded_rectangle([25, 25, 25 + banner_w, 25 + banner_h], radius=10, fill=(20, 20, 20, 215))
    draw.text((45, 38), title_text, fill=(255, 255, 255, 255))
    
    # 2. Bottom Disclaimer
    disc_text = "CONCEPT VISUALISATION — illustrative 2 m embankment — not approved design"
    draw.rectangle([0, h - 45, w, h], fill=(20, 20, 20, 230))
    draw.text((int(w * 0.35), h - 32), disc_text, fill=(255, 255, 255, 255))
    
    # 3. Callout Boxes & Arrows
    for c in callouts:
        bx, by, bw, bh = c['box']
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=8, fill=(20, 20, 20, 210), outline=(255, 255, 255, 255), width=2)
        draw.text((bx + 12, by + 10), c['text'], fill=(255, 255, 255, 255))
        if 'arrow_to' in c:
            tx, ty = c['arrow_to']
            draw.line([(bx + bw//2, by + bh), (tx, ty)], fill=(255, 255, 255, 255), width=2)
            
    final_img = Image.alpha_composite(im, overlay)
    final_img.convert('RGB').save(output_path, quality=95)
```
