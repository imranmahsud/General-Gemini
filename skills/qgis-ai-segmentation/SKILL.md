---
name: qgis-ai-segmentation
description: AI-driven satellite and aerial raster segmentation inside QGIS using TerraLab AI Segmentation. Extract building footprints, roads, water bodies, solar panels, and vegetation polygons with prompt-based or click-based workflows via QGIS Processing and Python API.
---

# QGIS AI Segmentation Guide

## Overview

The TerraLab AI Segmentation plugin (`AI_Segmentation`) integrates computer vision models directly into QGIS 3.22–4.x. It extracts vector polygons (buildings, trees, roofs, solar panels, roads) from orthophotos, drone imagery, and online XYZ/WMS basemaps (Google Satellite, Bing, Esri).

Installation path:
- Plugin: `C:\Users\Imran\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\AI_Segmentation`
- Source repository: `C:\tools\qgis-ai-segmentation`

---

## Operating Modes

1. **Automatic Zone Detection (`terralab:segmentzone`)**:
   - Define a bounding box or polygon boundary on the raster.
   - Pass an object class token (e.g. `building`, `tree`, `solar_panel`, `road`).
   - The engine sweeps tiles and generates vector polygons with individual ID attributes and geometric properties.
2. **Interactive Click / Point Segmentation (`terralab:segmentpoint`)**:
   - Supply map coordinates `(X, Y)`.
   - Generates an exact boundary polygon around the selected object.
   - Refine with positive points (areas to include) and negative points (areas to exclude).

---

## QGIS Processing Algorithms

The plugin exposes the `terralab` processing provider. Use standard `processing.run()` calls:

### 1. Check Service Status
```python
import processing
status = processing.run("terralab:segmentationstatus", {})
print("Ready:", status["READY"])
print("State:", status["STATE"])
print("Allowance left:", status.get("CREDITS_REMAINING"))
```

### 2. Automatic Zone Extraction
```python
import processing
from qgis.core import QgsProject

raster_layer = QgsProject.instance().mapLayersByName("Google Satellite")[0]
extent = "381000,382000,3754000,3755000 [EPSG:32642]"

result = processing.run("terralab:segmentzone", {
    "INPUT": raster_layer,
    "EXTENT": extent,
    "CLASS": "building",
    "DETAIL": 1,
    "INSTANCE_COLORS": True
})

output_layer = result["OUTPUT_LAYER"]
print(f"Detected {result['INSTANCE_COUNT']} instances. Layer ID: {output_layer}")
```

### 3. Click-to-Segment Feature
```python
import processing
from qgis.core import QgsPointXY

point = QgsPointXY(381450.2, 3754320.8)
result = processing.run("terralab:segmentpoint", {
    "INPUT": raster_layer,
    "POINT": point,
    "DISCARD_UNSAVED": False
})
print("Outline WKT:", result["POLYGON_WKT"])
```

---

## Python API Interface (`terralab`)

The plugin registers a top-level `terralab` module in the QGIS Python environment:

```python
import terralab
seg = terralab.segmentation

# Inspect valid tokens
classes = seg.list_object_classes()

# Evaluate zone before billing
preview = seg.set_auto_zone("Polygon ((...))")
print("Area (km2):", preview["km2"])

# Run async sweep
run = seg.detect_auto(zone_wkt="Polygon ((...))", object_class="building", wait=False)
while run["running"]:
    run = seg.auto_detect_status(run_id=run["run_id"], wait_s=30)

# Save result
seg.review_save()
```

---

## Post-Processing Rules for Civil & Hydraulic Work

1. **Building Squaring**: Always execute `Vector` -> `Geometry Tools` -> `Orthogonalize` or enable "Right angles" in review settings to maintain engineering squareness.
2. **Topology Verification**: Run `v.clean` or QGIS Geometry Checker to eliminate sliver polygons and overlaps before exporting to GeoPackage (`.gpkg`).
3. **Roughness / Manning Extraction**: When segmenting land cover for 2D HEC-RAS or hydraulic modeling, map segmented building and vegetation polygons into Manning's $n$ layer regions ($n = 0.080$ for dense buildings, $n = 0.120$ for dense riparian vegetation).
