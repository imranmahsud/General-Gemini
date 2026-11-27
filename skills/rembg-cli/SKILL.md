---
name: rembg-cli
description: Local AI-powered image background removal skill using rembg (U2-Net, BriaRMBG, IS-Net, BiRefNet) via ONNX Runtime. Replaces remove.bg subscriptions with zero API cost, full privacy, and batch processing for engineering reports, site inspection photos, and CAD/GIS overlays.
---

# Rembg Local Background Removal Skill

This skill provides native, zero-cloud AI background removal for photos, equipment images, site captures, logos, and technical figures using `rembg` running on local ONNX Runtime.

---

## 1. CLI Commands

### 1.1 Single File Background Removal
```bash
# Standard cutout (creates transparent PNG)
rembg i input.jpg output.png

# High-precision alpha matting (smoother edges for hair, vegetation, fences)
rembg i -af 1 -ab 15 -ae 15 input.jpg output.png

# Use specific lightweight model (u2netp) for low-spec/CPU speed
rembg i -m u2netp input.jpg output.png

# Use high-detail human/object segmentation model (birefnet-general)
rembg i -m birefnet-general input.jpg output.png
```

### 1.2 Batch Processing a Whole Directory
```bash
# Process all images in a folder and write transparent PNGs to output folder
rembg p ./site_photos ./site_photos_transparent
```

### 1.3 Local HTTP API Server
To expose a local headless microservice on `http://127.0.0.1:5000`:
```bash
rembg s --port 5000
```
POST any image to `http://127.0.0.1:5000/api/remove` to receive the cut-out PNG.

---

## 2. Python API

```python
from rembg import remove, new_session
from PIL import Image
import io

def remove_background(input_path: str, output_path: str, model_name: str = "u2net"):
    """
    Strips image background locally and saves as transparent RGBA PNG.
    Supported models: 'u2net', 'u2netp', 'u2net_human_seg', 'isnet-general-use', 'birefnet-general'
    """
    session = new_session(model_name)
    with open(input_path, "rb") as inp:
        input_data = inp.read()
        output_data = remove(input_data, session=session)
        
    with open(output_path, "wb") as out:
        out.write(output_data)
    print(f"Background removed: {output_path}")

if __name__ == "__main__":
    remove_background("sample.jpg", "sample_cutout.png")
```

---

## 3. Engineering & Workflow Applications

1. **Site Inspection Figures**: Strip busy background landscapes from concrete test cylinders, cracks, culvert barrels, and survey monuments before pasting into PC-I reports.
2. **QGIS & CAD Overlays**: Create transparent asset overlays for orthomosaics, site layouts, and architectural floorplans.
3. **Equipment Cutouts**: Generate isolated machinery, drone, and vehicle PNGs for proposal diagrams and contractor equipment schedules.
