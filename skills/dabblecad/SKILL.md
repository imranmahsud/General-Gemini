---
name: dabblecad
description: Offline 3D shape modeling, laser cutting toolpaths, and depth map relief generation using DabbleCAD. Create parts for 3D printing (STL/3MF), laser engraving (G-code/GRBL), and CNC heightmaps without internet or cloud dependencies.
---

# DabbleCAD Workflow Guide

## Overview

DabbleCAD is a standalone, offline desktop computer-aided design (CAD) application combining three core capabilities in one interface:
1. **3D Design**: Direct constructive solid geometry (CSG) modeling using primitive solids (boxes, cylinders, spheres, wedges, text) and boolean operations (group, intersect, hole-punch).
2. **Laser Workspace**: 2D vector layout, layer sequencing, kerf offset, speed/power controls, and G-code export for GRBL-controlled diode and CO2 lasers.
3. **Depth Map Studio**: Translates 3D meshes or greyscale raster artwork into height-mapped relief geometry for CNC milling and 2.5D laser engraving.

Installation path:
- App Directory: `C:\tools\DabbleCAD-app\DabbleCAD.exe`
- Source Repository: `C:\tools\DabbleCAD`
- Launcher: `C:\tools\dabblecad.bat`

---

## 3D Design Workflow

1. **Launch**: Execute `C:\tools\dabblecad.bat` or run `C:\tools\DabbleCAD-app\DabbleCAD.exe`.
2. **Primitives Placement**:
   - Drag base solids from the right-hand panel onto the millimeter workplane grid.
   - Adjust dimensions numerically in the transform inspector.
3. **Boolean Subtractions & Joinery**:
   - Change a solid's attribute from `Solid` to `Hole`.
   - Align holes with the parent body using the `Align` tool ($X, Y, Z$ center/edge snaps).
   - Select both elements and invoke `Group` (`Ctrl + G`) to execute boolean difference.
4. **Export for Slicing**:
   - Select the model and click `Export`.
   - Choose **`.3MF`** (preserves unit scale and multi-part hierarchies) or **`.STL`** for import into PrusaSlicer, Bambu Studio, or Cura.

---

## Laser & 2.5D Relief Workflows

1. **Laser Toolpaths**:
   - Switch tabs to the **Laser** workspace.
   - Import DXF or SVG vector contours.
   - Assign cut vs engrave passes per color layer.
   - Output clean G-code (`.gcode` / `.nc`) directly or connect via USB serial COM port to GRBL controllers.
2. **Depth Map Reliefs**:
   - In **Depth Map Studio**, load a high-contrast terrain elevation image or 3D object.
   - Set displacement height (Z-range in mm) and step resolution.
   - Export heightfield raster or triangulated mesh for CNC carving.
