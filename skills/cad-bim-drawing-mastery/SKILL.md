---
name: cad-bim-drawing-mastery
description: Architectural modeling, drafting, programmatic drawing, and file conversion across Autodesk Revit 2027 (.NET 10 / Dynamo 4.0), Trimble SketchUp 2026 (Ruby API / PBR / LayOut), and Sweet Home 3D (Java Plugin API / .sh3d / OBJ). Use when generating 2D/3D architectural geometry, drafting walls, floors, rooms, or automating CAD/BIM pipelines.
---

# CAD & BIM Drawing Mastery: Revit 2027, SketchUp 2026, & Sweet Home 3D

This skill provides expert procedures, programmatic code patterns, and converter pipelines for architectural modeling across three distinct design environments:

1. **Autodesk Revit 2027**: Enterprise BIM with parametric system families, level constraints, .NET 10 API, Dynamo 4.0.2 MCP, and IFC4.3.
2. **Trimble SketchUp 2026**: Boundary-representation surface modeling, inference engine, ambient occlusion, PBR graphics engine, and Ruby API automation.
3. **Sweet Home 3D (v7.x / 8.x)**: Rapid interior floor planning with synchronized 2D/3D views, Java Swing MVC architecture, and `.sh3d` ZIP/XML archive manipulation.

---

## 1. Autodesk Revit 2027 Modeling & API Guidelines

### 1.1 Core Principles
* **System Families**: Walls, floors, roofs, ceilings, and stairs cannot exist outside a project document (`.rvt`). They are defined by layer assemblies (compound structures) and generated via 2D sketch loops (`CurveLoop`) or path curves (`Curve`).
* **Level & Workplane Association**: All elements must reference a host `Level` or `ReferencePlane`. In plan views, elevation is bound to the view's level; in 3D views, set workplanes explicitly before drafting.
* **Sketch Loops**: Boundaries for floors and ceilings must form closed, non-self-intersecting loops of coplanar curves with no duplicate or microscopic segments.

### 1.2 Programmatic Creation (.NET 10 / C#)
Revit 2027 runs on **.NET 10 (`net10.0-windows`)**. All database changes require an active `Transaction`.

#### Native Wall Creation:
```csharp
using Autodesk.Revit.DB;

public Wall CreateParametricWall(Document doc, XYZ startPt, XYZ endPt, Level level)
{
    using (Transaction tx = new Transaction(doc, "Create Wall"))
    {
        tx.Start();
        Line wallLine = Line.CreateBound(startPt, endPt);
        WallType wallType = new FilteredElementCollector(doc)
            .OfClass(typeof(WallType))
            .Cast<WallType>()
            .First(wt => wt.Kind == WallKind.Basic);

        // Parameters: Document, Curve, WallTypeId, LevelId, Height, Offset, Flip, IsStructural
        Wall wall = Wall.Create(doc, wallLine, wallType.Id, level.Id, 10.0, 0.0, false, false);
        tx.Commit();
        return wall;
    }
}
```

#### Native Floor Creation (`Floor.Create`):
```csharp
public Floor CreateFloor(Document doc, IList<XYZ> points, Level level)
{
    using (Transaction tx = new Transaction(doc, "Create Floor"))
    {
        tx.Start();
        CurveLoop profile = new CurveLoop();
        for (int i = 0; i < points.Count; i++)
        {
            XYZ p1 = points[i];
            XYZ p2 = points[(i + 1) % points.Count];
            profile.Append(Line.CreateBound(p1, p2));
        }

        FloorType floorType = new FilteredElementCollector(doc)
            .OfClass(typeof(FloorType))
            .Cast<FloorType>()
            .First();

        Floor floor = Floor.Create(doc, new List<CurveLoop> { profile }, floorType.Id, level.Id);
        tx.Commit();
        return floor;
    }
}
```

---

## 2. Trimble SketchUp 2026 Modeling & Ruby API Guidelines

### 2.1 Core Principles
* **Raw Geometry vs. Containers**: Never leave raw geometry ungrouped. Always encapsulate walls, furniture, and rooms into **Groups** (`entities.add_group`) or **Components** (`Sketchup::ComponentDefinition`) to avoid unintended face merging.
* **Inference Engine**:
  * Arrow keys lock axes: Right = Red (X), Left = Green (Y), Up = Blue (Z), Down = Parallel/Perpendicular.
  * Inference snaps: Endpoint (green), Midpoint (cyan), On Edge (red), On Face (blue), Intersection (black).
* **Push/Pull Mechanics**: Extrude planar faces normal to their surface. Hold `Ctrl` (Windows) to create a new extrusion face while retaining the base face.

### 2.2 Ruby API Automation
Always wrap programmatic changes in `model.start_operation` and `model.commit_operation`.

```ruby
model = Sketchup.active_model
entities = model.active_entities

model.start_operation('Generate Wall System', true)

# 1. Establish outer footprint (inches)
width = 240.inch
depth = 180.inch
height = 108.inch
thickness = 6.inch

pts_outer = [
  Geom::Point3d.new(0, 0, 0),
  Geom::Point3d.new(width, 0, 0),
  Geom::Point3d.new(width, depth, 0),
  Geom::Point3d.new(0, depth, 0)
]
outer_face = entities.add_face(pts_outer)

# 2. Cut inner core for wall thickness
pts_inner = [
  Geom::Point3d.new(thickness, thickness, 0),
  Geom::Point3d.new(width - thickness, thickness, 0),
  Geom::Point3d.new(width - thickness, depth - thickness, 0),
  Geom::Point3d.new(thickness, depth - thickness, 0)
]
inner_face = entities.add_face(pts_inner)
inner_face.erase!

# 3. Extrude walls
wall_face = entities.grep(Sketchup::Face).first
wall_face.pushpull(height)

# 4. Encapsulate into group
group = entities.add_group(entities.grep(Sketchup::Drawingelement))
group.name = "Walls_Level1"

model.commit_operation
```

---

## 3. Sweet Home 3D Modeling & Java Plugin Guidelines

### 3.1 Core Principles
* **Dual-View Drafting**: Draw walls, rooms, and dimensions on the 2D floor plan canvas while simultaneously reviewing the 3D aerial or virtual visitor view.
* **Mitered Wall Joins**: Connecting wall endpoints automatically calculates mitered joints and thickness bevels.
* **Cutouts**: Doors and windows automatically cut precise openings through walls when placed along their length.
* **`.sh3d` Container**: The `.sh3d` file is a ZIP archive containing `Home.xml` (the DOM representation of all walls, rooms, coordinates, and metadata) along with textures and `.obj` 3D furniture models.

### 3.2 Java Plugin API Automation
Sweet Home 3D uses a Swing MVC pattern. All modifications to the `Home` model must be executed on the **Event Dispatch Thread (EDT)**.

```java
import com.eteks.sweethome3d.model.Home;
import com.eteks.sweethome3d.model.Wall;
import com.eteks.sweethome3d.model.Room;
import com.eteks.sweethome3d.plugin.Plugin;
import com.eteks.sweethome3d.plugin.PluginAction;
import javax.swing.SwingUtilities;

public class CustomLayoutPlugin extends Plugin {
    @Override
    public PluginAction[] getActions() {
        return new PluginAction[] {
            new PluginAction() {
                @Override
                public String getName() { return "Build Master Suite"; }

                @Override
                public void execute() {
                    Home home = getHome();
                    SwingUtilities.invokeLater(() -> {
                        // Dimensions in centimeters
                        float x1 = 100, y1 = 100, x2 = 700, y2 = 500;
                        float thickness = 15.0f;
                        float height = 280.0f;

                        Wall w1 = new Wall(x1, y1, x2, y1, thickness);
                        Wall w2 = new Wall(x2, y1, x2, y2, thickness);
                        Wall w3 = new Wall(x2, y2, x1, y2, thickness);
                        Wall w4 = new Wall(x1, y2, x1, y1, thickness);

                        for (Wall w : new Wall[]{w1, w2, w3, w4}) {
                            w.setHeight(height);
                            home.addWall(w);
                        }

                        float[][] points = {{x1, y1}, {x2, y1}, {x2, y2}, {x1, y2}};
                        Room room = new Room(points);
                        room.setName("Master Suite");
                        home.addRoom(room);
                    });
                }
            }
        };
    }
}
```

---

## 4. Cross-Platform Conversion & Interoperability

### 4.1 Unit Scale Normalization
* **Sweet Home 3D**: Centimeters ($1.0 = 1\text{ cm}$).
* **SketchUp**: Inches ($1.0 = 1\text{ inch} = 2.54\text{ cm}$).
* **Revit**: Decimal Feet ($1.0 = 1\text{ foot} = 12\text{ inches} = 30.48\text{ cm}$).
* *Conversion Formula*: $P_{\text{Revit}} = P_{\text{SweetHome}} \times \frac{1}{30.48} = P_{\text{SketchUp}} \times \frac{1}{12}$.

### 4.2 Tri-Directional Pipeline
1. **Sweet Home 3D $\rightarrow$ SketchUp 2026**:
   * Export 3D view as `.obj` + `.mtl`.
   * Import into SketchUp, soften coplanar edges, organize into Groups, and assign SketchUp 2026 PBR materials and Ambient Occlusion.
2. **SketchUp 2026 $\rightarrow$ Revit 2027**:
   * *Option 1 (Production BIM)*: Export clean floor boundaries as `.dwg`. Link into Revit, and use `Wall by Pick Lines` to generate native parametric walls.
   * *Option 2 (openBIM)*: Classify components as `IfcWall`, `IfcDoor`, etc., and export as IFC4. Link IFC into Revit.
   * *Option 3 (DirectShape API)*: Ingest custom mesh solids using `TessellatedShapeBuilder` into `DirectShape.CreateElement(doc, BuiltInCategory.OST_GenericModel)`.
