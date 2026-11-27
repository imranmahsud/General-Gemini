---
name: architectural-plan-designer
description: >-
  Design and generate attractive, coherent, structurally-sound, and code-compliant
  architectural building plans and floor plans from user requirements. Solves
  unattractive or disjointed AI plans by enforcing architectural graphic standards,
  functional zoning, egress corridors, wall poché, door swings, and dimension chains.
  Directly outputs publication-grade vector SVG, production DXF CAD drawings
  (via AI-CAD / ezdxf), and 3D building models (via Pascal 3D MCP).
compatibility: Works across Antigravity, Python (ezdxf), AI-CAD, and Pascal 3D.
---

# Architectural Floor Plan Designer

Transform natural language user requirements into attractive, coherent, professional architectural plans.

---

## Why Generic AI Plans Look Incoherent (And How This Skill Fixes It)

| Common AI Flaw | Architectural Fix Enforced by this Skill |
| :--- | :--- |
| **Landlocked Rooms & Weird Circulation** | Establishes a dedicated **Circulation Spine** (Hallway $\ge 1.1\text{m} / 3'6"$). No walking through bedrooms or bathrooms to access other areas. |
| **Random Room Adjacency** | Strict **3-Zone Layout**: Public (Living, Dining, Foyer), Private (Bedrooms, Ensuite), and Service (Kitchen, Laundry, Utility). |
| **Arbitrary or Impossible Dimensions** | Uses **Standard Ergonomic Baselines** (e.g. Master Bedroom $\ge 3.6\text{m} \times 4.2\text{m}$, Bathroom $\ge 1.5\text{m} \times 2.4\text{m}$, Kitchen counter depth $0.6\text{m}$). |
| **Flat, Cluttered, or Ugly Presentation** | **Architectural Poché**: Solid dark cut walls, 90° door swing arcs, double-line window mullions, room tags with metric + imperial area, dimension chains, and north arrow. |
| **Lack of Structural & Plumbing Realism** | **Stacked Wet Walls**: Back-to-back bathrooms and kitchen plumbing. Continuous exterior structural perimeter. |

---

## Architectural Dimensioning & Ergonomic Standards

Always check these dimensions when synthesizing a floor plan:

### 1. Room Minimum Sizes
*   **Foyer / Entryway**: Min width $1.2\text{m} (4'-0")$
*   **Living Room**: Min $4.0\text{m} \times 4.5\text{m} (13'-0" \times 15'-0")$
*   **Dining Room**: Min $3.0\text{m} \times 3.6\text{m} (10'-0" \times 12'-0")$
*   **Kitchen**: Min width $2.4\text{m} (8'-0")$, standard counter depth $0.6\text{m} (24")$
*   **Master Bedroom**: Min $3.6\text{m} \times 4.2\text{m} (12'-0" \times 14'-0")$
*   **Secondary Bedroom**: Min $3.0\text{m} \times 3.6\text{m} (10'-0" \times 12'-0")$
*   **Full Bathroom**: Min $1.5\text{m} \times 2.4\text{m} (5'-0" \times 8'-0")$
*   **Powder Room (Half Bath)**: Min $0.9\text{m} \times 1.8\text{m} (3'-0" \times 6'-0")$
*   **Hallway / Corridor**: Min clear width $1.0\text{m} - 1.2\text{m} (3'-3" - 4'-0")$

### 2. Wall Thicknesses
*   **Exterior / Load-Bearing Walls**: $230\text{mm} (9" \text{ or } 0.23\text{m})$
*   **Interior Partitions**: $115\text{mm} (4.5" \text{ or } 0.12\text{m})$
*   **Plumbing / Wet Wall**: $150\text{mm} (6" \text{ or } 0.15\text{m})$

### 3. Openings & Clearances
*   **Main Entrance Door**: $1.0\text{m} (3'-4")$ clear opening
*   **Bedroom Doors**: $0.9\text{m} (3'-0")$ clear opening
*   **Bathroom / Closet Doors**: $0.75\text{m} - 0.8\text{m} (2'-6" - 2'-8")$
*   **Door Swing**: Must swing against an adjacent wall, never into a hallway path or fixture.
*   **Windows**: Every habitable room (Living, Bedrooms) **must** touch an exterior wall with windows $\ge 10\%$ of floor area for code-compliant natural light & ventilation.

---

## 5-Step Plan Generation Protocol

When asked to create or refine a building plan:

1.  **Extract the Program Requirements**:
    *   List all requested spaces (bedrooms, bathrooms, kitchen, living, outdoor).
    *   Calculate the target Built-Up Area (BUA) and add $10-15\%$ for circulation / walls.
2.  **Formulate Functional Adjacency & Zoning**:
    *   **Public Zone**: Near entrance.
    *   **Service Zone**: Direct access from kitchen to dining; external utility access.
    *   **Private Zone**: Buffer through a hallway, away from the front door.
3.  **Build Geometry with the Helper Script**:
    *   Use `C:\Users\imran\.gemini\config\skills\architectural-plan-designer\scripts\architectural_renderer.py` or write Python with `ezdxf` to establish coordinates and room bounds.
4.  **Render the Visual Artifact (SVG)**:
    *   Generate a clean, high-resolution SVG with poché walls, room tags, fixtures, and title block. Render it directly in the conversation artifact or HTML widget.
5.  **Export to CAD (DXF) and Pascal 3D**:
    *   Export to `.dxf` for AutoCAD / Revit using `AI-CAD`.
    *   Connect to Pascal 3D using `pascal mcp connect` or `pascal editor` to view in real-time 3D.

---

## Python Execution Example

```python
import sys
sys.path.insert(0, r"C:\Users\imran\.gemini\config\skills\architectural-plan-designer\scripts")
from architectural_renderer import ArchitecturalPlan

# 1. Initialize plan
plan = ArchitecturalPlan(title="Modern 2-Bedroom Apartment", scale="1:100")

# 2. Add Rooms (x, y, width, height in meters)
plan.add_room("Living & Dining", x=0.0, y=0.0, w=5.5, h=4.0, zone="public", color="#f0f9ff")
plan.add_room("Kitchen", x=5.5, y=0.0, w=3.0, h=4.0, zone="service", color="#fefce8")
plan.add_room("Master Bedroom", x=0.0, y=4.0, w=4.0, h=4.2, zone="private", color="#f8fafc")
plan.add_room("Master Bath", x=4.0, y=4.0, w=1.8, h=2.2, zone="private", color="#f1f5f9")
plan.add_room("Common Bath", x=4.0, y=6.2, w=1.8, h=2.0, zone="public", color="#f1f5f9")
plan.add_room("Bedroom 2", x=5.8, y=4.0, w=3.2, h=4.2, zone="private", color="#f8fafc")

# 3. Add Exterior & Interior Walls
# Outer envelope
plan.add_wall(0.0, 0.0, 9.0, 0.0, thickness=0.23, is_exterior=True)
plan.add_wall(9.0, 0.0, 9.0, 8.2, thickness=0.23, is_exterior=True)
plan.add_wall(9.0, 8.2, 0.0, 8.2, thickness=0.23, is_exterior=True)
plan.add_wall(0.0, 8.2, 0.0, 0.0, thickness=0.23, is_exterior=True)
# Interior partitions
plan.add_wall(0.0, 4.0, 9.0, 4.0, thickness=0.12, is_exterior=False)
plan.add_wall(5.5, 0.0, 5.5, 4.0, thickness=0.12, is_exterior=False)
plan.add_wall(4.0, 4.0, 4.0, 8.2, thickness=0.12, is_exterior=False)
plan.add_wall(5.8, 4.0, 5.8, 8.2, thickness=0.12, is_exterior=False)

# 4. Add Doors with Swing Arcs
plan.add_door(x=0.5, y=0.0, width=1.0) # Main entrance
plan.add_door(x=0.5, y=4.0, width=0.9) # Master bed door
plan.add_door(x=4.0, y=4.5, width=0.75) # Master bath door
plan.add_door(x=6.0, y=4.0, width=0.9) # Bed 2 door

# 5. Add Windows
plan.add_window(x=1.5, y=0.0, length=2.0, orientation="horizontal")
plan.add_window(x=7.0, y=0.0, length=1.2, orientation="horizontal")
plan.add_window(x=1.0, y=8.2, length=1.8, orientation="horizontal")
plan.add_window(x=6.5, y=8.2, length=1.5, orientation="horizontal")

# 6. Add Fixtures
plan.add_fixture("bed", x=0.5, y=5.5, w=2.0, h=1.8)
plan.add_fixture("bed", x=6.5, y=5.5, w=1.8, h=1.8)
plan.add_fixture("toilet", x=4.3, y=5.0, w=0.6, h=0.7)

# 7. Generate outputs
svg_code = plan.to_svg()
plan.to_dxf("apartment_floor_plan.dxf")
pascal_data = plan.to_pascal_scene()
```
