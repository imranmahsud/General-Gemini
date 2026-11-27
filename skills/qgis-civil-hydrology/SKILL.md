---
name: qgis-civil-hydrology
description: Automates QGIS, PyQGIS, and WhiteboxTools pipelines for civil engineering terrain analysis, ALOS/SRTM DEM processing, watershed delineation, contour generation, and cartographic map layout exports. Use when performing geospatial analysis, catchment basin delineation, or GIS mapping for civil infrastructure.
license: MIT
metadata:
  origin: General-Gemini
tools: Read, Write, Edit, Bash, Grep, Glob
---

# QGIS & Civil Hydrology Processing Skill

Production workflows for terrain modeling, hydrology, and automated cartography using QGIS 3.x/4.x, PyQGIS, and headless WhiteboxTools.

## When to Activate

- Processing Digital Elevation Models (DEMs: SRTM 30m, ALOS PALSAR 12.5m, LiDAR 1m)
- Generating elevation contours, slopes, hillshades, and aspect rasters
- Performing catchment/watershed delineation, stream network extraction, and flow accumulation
- Exporting publication-grade engineering maps and plan sheets via QGIS print layouts
- Operating via QGIS Agent MCP (`qgis_agent_mcp`) or standalone PyQGIS scripts

---

## 1. QGIS Agent MCP Priority Workflow

Per system rules, prioritize **QGIS Agent MCP** (`qgis_agent_mcp`) for interactive and automated operations:
1. **Preflight**: Verify layer CRSs (e.g., target UTM zone like `EPSG:32642` or `EPSG:32643` for Pakistan/South Asia; avoid running hydrological operations in unprojected `EPSG:4326`).
2. **Atomic Steps**: Execute raster warping, sink filling, flow direction, and vector conversion in separate, verifiable steps.
3. **Verification**: Confirm feature count, geometry validity, and raster cell dimensions after every transformation.

---

## 2. Headless Python Hydrological Pipeline (WhiteboxTools + GeoPandas)

When running headless without GUI:

```python
import os
import geopandas as gpd
from whitebox import WhiteboxTools

wbt = WhiteboxTools()
wbt.set_verbose_mode(False)

def delineate_catchment(raw_dem: str, output_dir: str, pour_points_shp: str = None):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Fill Depressions (Wang & Liu algorithm)
    filled_dem = os.path.join(output_dir, "dem_filled.tif")
    wbt.fill_depressions_wang_and_liu(raw_dem, filled_dem, fix_flats=True)
    
    # 2. D8 Flow Direction and Accumulation
    d8_pntr = os.path.join(output_dir, "d8_pointer.tif")
    d8_accum = os.path.join(output_dir, "d8_accum.tif")
    wbt.d8_pointer(filled_dem, d8_pntr)
    wbt.d8_flow_accumulation(filled_dem, d8_accum, out_type="cells")
    
    # 3. Extract Stream Network (threshold = 1000 cells)
    streams = os.path.join(output_dir, "streams_raster.tif")
    wbt.extract_streams(d8_accum, streams, threshold=1000.0)
    
    # 4. Stream Vectorization
    streams_vector = os.path.join(output_dir, "streams.shp")
    wbt.raster_streams_to_vector(streams, d8_pntr, streams_vector)
    
    # 5. Watershed delineation (if pour points provided)
    if pour_points_shp and os.path.exists(pour_points_shp):
        watershed = os.path.join(output_dir, "watershed.tif")
        wbt.watershed(d8_pntr, pour_points_shp, watershed)
        watershed_shp = os.path.join(output_dir, "watershed.shp")
        wbt.raster_to_vector_polygons(watershed, watershed_shp)
        return streams_vector, watershed_shp
        
    return streams_vector, None
```

---

## 3. Contour & Elevation Cross-Section Generation

### A. GDAL Contour Generation
```powershell
# Extract 5-meter minor and 25-meter major index contours
gdal_contour -a ELEV -i 5.0 -f "ESRI Shapefile" input_dem_utm.tif contours_5m.shp
```

### B. PyQGIS Layer Styler
```python
from qgis.core import QgsProject, QgsVectorLayer, QgsSingleSymbolRenderer, QgsLineSymbol

layer = QgsVectorLayer("contours_5m.shp", "Contours", "ogr")
symbol = QgsLineSymbol.createSimple({'color': '#8B4513', 'width': '0.3'})
layer.setRenderer(QgsSingleSymbolRenderer(symbol))
layer.triggerRepaint()
QgsProject.instance().addMapLayer(layer)
```

---

## 4. Automated Map Layout Export

```python
from qgis.core import QgsProject, QgsPrintLayout, QgsLayoutItemMap, QgsLayoutSize, QgsUnitTypes

project = QgsProject.instance()
layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.setName("Engineering_Site_Plan")

# A4 Landscape (297 x 210 mm)
layout.pageCollection().page(0).setPageSize(QgsLayoutSize(297, 210, QgsUnitTypes.LayoutMillimeters))

# Map Item
map_item = QgsLayoutItemMap(layout)
map_item.setRect(20, 20, 257, 170)
map_item.zoomToExtent(project.viewManager().mapCanvas().extent())
layout.addLayoutItem(map_item)

# Export to PDF
from qgis.core import QgsLayoutExporter
exporter = QgsLayoutExporter(layout)
exporter.exportToPdf("C:/reports/Site_Plan_A4.pdf", QgsLayoutExporter.PdfExportSettings())
```

---

## 5. Reference Libraries on Local System

- **PyQGIS Cookbook Recipes**: `C:\tools\qgis-civil\qgis-cookbook\`
- **QGIS MCP Service Engine**: `C:\Users\Imran\.qgis-mcp\`
