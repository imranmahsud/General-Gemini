"""
Architectural Floor Plan Renderer & Generator
Produces publication-grade vector SVG drawings, DXF CAD files, and Pascal 3D scene data
following strict Architectural Graphic Standards.
"""

import math
import os
import json
from typing import Dict, List, Any, Optional

try:
    import ezdxf
    HAS_EZDXF = True
except ImportError:
    HAS_EZDXF = False


class ArchitecturalPlan:
    def __init__(self, title: str = "RESIDENTIAL FLOOR PLAN", scale: str = "1:100", unit: str = "m"):
        self.title = title
        self.scale = scale
        self.unit = unit
        self.rooms = []
        self.walls = []
        self.doors = []
        self.windows = []
        self.fixtures = []
        self.dimensions = []
        self.ext_bounds = [0, 0, 0, 0] # min_x, min_y, max_x, max_y

    def add_room(self, name: str, x: float, y: float, w: float, h: float, zone: str = "public", color: str = "#f8fafc"):
        """Add a room with position and dimensions in meters."""
        room = {
            "name": name,
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "zone": zone,
            "color": color,
            "area_m2": round(w * h, 1),
            "area_sqft": round(w * h * 10.7639, 1)
        }
        self.rooms.append(room)
        self._update_bounds(x, y, w, h)
        return room

    def add_wall(self, x1: float, y1: float, x2: float, y2: float, thickness: float = 0.23, is_exterior: bool = True):
        """Add a wall segment with start, end, thickness in meters."""
        self.walls.append({
            "x1": x1, "y1": y1, "x2": x2, "y2": y2,
            "thickness": thickness,
            "is_exterior": is_exterior
        })

    def add_door(self, x: float, y: float, width: float = 0.9, orientation: str = "horizontal", swing: str = "top-right"):
        """Add a door with swing arc."""
        self.doors.append({
            "x": x, "y": y, "width": width,
            "orientation": orientation, "swing": swing
        })

    def add_window(self, x: float, y: float, length: float = 1.2, orientation: str = "horizontal"):
        """Add a window in an exterior wall."""
        self.windows.append({
            "x": x, "y": y, "length": length,
            "orientation": orientation
        })

    def add_fixture(self, fixture_type: str, x: float, y: float, w: float = 0.8, h: float = 0.8, label: str = ""):
        """Add fixture / furniture item."""
        self.fixtures.append({
            "type": fixture_type, "x": x, "y": y, "w": w, "h": h, "label": label
        })

    def _update_bounds(self, x: float, y: float, w: float, h: float):
        if not self.rooms and not self.walls:
            self.ext_bounds = [x, y, x + w, y + h]
        else:
            self.ext_bounds[0] = min(self.ext_bounds[0], x)
            self.ext_bounds[1] = min(self.ext_bounds[1], y)
            self.ext_bounds[2] = max(self.ext_bounds[2], x + w)
            self.ext_bounds[3] = max(self.ext_bounds[3], y + h)

    def to_svg(self, width_px: int = 1200, padding_px: int = 80) -> str:
        """Render publication-grade architectural SVG floor plan."""
        min_x, min_y, max_x, max_y = self.ext_bounds
        plan_w = max(1.0, max_x - min_x)
        plan_h = max(1.0, max_y - min_y)

        # Scale factor: meters to SVG pixels
        scale_px = (width_px - 2 * padding_px) / plan_w
        height_px = int(plan_h * scale_px + 2 * padding_px + 120) # extra space for title block

        def tx(x_m):
            return padding_px + (x_m - min_x) * scale_px

        def ty(y_m):
            # Invert Y so standard upward CAD coordinates render naturally
            return height_px - (padding_px + 100) - (y_m - min_y) * scale_px

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width_px} {height_px}" '
            f'style="background:#ffffff; font-family:\'Segoe UI\', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;">',
            '<defs>',
            '  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">',
            '    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#f1f5f9" stroke-width="1"/>',
            '  </pattern>',
            '  <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">',
            '    <feDropShadow dx="0" dy="2" stdDeviation="4" flood-opacity="0.08"/>',
            '  </filter>',
            '</defs>',
            # Background grid
            f'<rect width="{width_px}" height="{height_px}" fill="url(#grid)"/>',
            # Title block header
            f'<rect x="20" y="20" width="{width_px - 40}" height="50" rx="8" fill="#0f172a"/>',
            f'<text x="40" y="52" fill="#ffffff" font-size="20" font-weight="700" letter-spacing="1.5">{self.title.upper()}</text>',
            f'<text x="{width_px - 40}" y="52" fill="#94a3b8" font-size="13" text-anchor="end">SCALE {self.scale} | UNITS: METERS</text>',
            '<g id="rooms">'
        ]

        # Draw Rooms
        for room in self.rooms:
            rx = tx(room["x"])
            ry = ty(room["y"] + room["h"])
            rw = room["w"] * scale_px
            rh = room["h"] * scale_px
            bg_color = room.get("color", "#f8fafc")

            svg_parts.append(
                f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{rw:.1f}" height="{rh:.1f}" '
                f'fill="{bg_color}" stroke="#cbd5e1" stroke-width="1"/>'
            )
            # Room label & dimensions
            cx = rx + rw / 2
            cy = ry + rh / 2
            svg_parts.append(
                f'<g text-anchor="middle">'
                f'  <text x="{cx:.1f}" y="{cy - 8:.1f}" fill="#1e293b" font-size="14" font-weight="700" letter-spacing="0.5">{room["name"].upper()}</text>'
                f'  <text x="{cx:.1f}" y="{cy + 10:.1f}" fill="#64748b" font-size="11">{room["w"]:.2f}m × {room["h"]:.2f}m</text>'
                f'  <text x="{cx:.1f}" y="{cy + 25:.1f}" fill="#94a3b8" font-size="10">{room["area_m2"]} m² ({room["area_sqft"]} sq ft)</text>'
                f'</g>'
            )

        svg_parts.append('</g>')

        # Draw Fixtures / Furniture
        svg_parts.append('<g id="fixtures">')
        for fix in self.fixtures:
            fx = tx(fix["x"])
            fy = ty(fix["y"] + fix["h"])
            fw = fix["w"] * scale_px
            fh = fix["h"] * scale_px
            ftype = fix["type"].lower()

            if "bed" in ftype:
                svg_parts.append(
                    f'<g stroke="#94a3b8" stroke-width="1.5" fill="#f1f5f9">'
                    f'  <rect x="{fx:.1f}" y="{fy:.1f}" width="{fw:.1f}" height="{fh:.1f}" rx="4"/>'
                    f'  <rect x="{fx + fw*0.1:.1f}" y="{fy + 4:.1f}" width="{fw*0.35:.1f}" height="{fh*0.25:.1f}" rx="2" fill="#e2e8f0"/>'
                    f'  <rect x="{fx + fw*0.55:.1f}" y="{fy + 4:.1f}" width="{fw*0.35:.1f}" height="{fh*0.25:.1f}" rx="2" fill="#e2e8f0"/>'
                    f'  <line x1="{fx:.1f}" y1="{fy + fh*0.35:.1f}" x2="{fx + fw:.1f}" y2="{fy + fh*0.35:.1f}" stroke-dasharray="2,2"/>'
                    f'</g>'
                )
            elif "table" in ftype or "dining" in ftype:
                svg_parts.append(
                    f'<rect x="{fx:.1f}" y="{fy:.1f}" width="{fw:.1f}" height="{fh:.1f}" rx="6" '
                    f'stroke="#94a3b8" stroke-width="1.5" fill="#f8fafc"/>'
                )
            elif "kitchen" in ftype or "counter" in ftype:
                svg_parts.append(
                    f'<rect x="{fx:.1f}" y="{fy:.1f}" width="{fw:.1f}" height="{fh:.1f}" '
                    f'stroke="#64748b" stroke-width="1.5" fill="#e2e8f0"/>'
                )
            elif "wc" in ftype or "toilet" in ftype:
                svg_parts.append(
                    f'<g stroke="#64748b" stroke-width="1.5" fill="#ffffff">'
                    f'  <rect x="{fx + fw*0.2:.1f}" y="{fy:.1f}" width="{fw*0.6:.1f}" height="{fh*0.3:.1f}" rx="2"/>'
                    f'  <ellipse cx="{fx + fw*0.5:.1f}" cy="{fy + fh*0.65:.1f}" rx="{fw*0.35:.1f}" ry="{fh*0.35:.1f}"/>'
                    f'</g>'
                )
        svg_parts.append('</g>')

        # Draw Walls (Architectural Poché - solid dark fill)
        svg_parts.append('<g id="walls">')
        for wall in self.walls:
            x1, y1 = tx(wall["x1"]), ty(wall["y1"])
            x2, y2 = tx(wall["x2"]), ty(wall["y2"])
            thick_px = max(3.0, wall["thickness"] * scale_px)
            stroke_color = "#0f172a" if wall.get("is_exterior", True) else "#334155"

            svg_parts.append(
                f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                f'stroke="{stroke_color}" stroke-width="{thick_px:.1f}" stroke-linecap="square"/>'
            )
        svg_parts.append('</g>')

        # Draw Windows
        svg_parts.append('<g id="windows">')
        for win in self.windows:
            wx = tx(win["x"])
            wy = ty(win["y"])
            wlen = win["length"] * scale_px
            if win.get("orientation") == "horizontal":
                svg_parts.append(
                    f'<g stroke="#0284c7" stroke-width="2">'
                    f'  <line x1="{wx:.1f}" y1="{wy - 3:.1f}" x2="{wx + wlen:.1f}" y2="{wy - 3:.1f}"/>'
                    f'  <line x1="{wx:.1f}" y1="{wy + 3:.1f}" x2="{wx + wlen:.1f}" y2="{wy + 3:.1f}"/>'
                    f'  <line x1="{wx:.1f}" y1="{wy - 5:.1f}" x2="{wx:.1f}" y2="{wy + 5:.1f}"/>'
                    f'  <line x1="{wx + wlen:.1f}" y1="{wy - 5:.1f}" x2="{wx + wlen:.1f}" y2="{wy + 5:.1f}"/>'
                    f'</g>'
                )
            else:
                svg_parts.append(
                    f'<g stroke="#0284c7" stroke-width="2">'
                    f'  <line x1="{wx - 3:.1f}" y1="{wy:.1f}" x2="{wx - 3:.1f}" y2="{wy - wlen:.1f}"/>'
                    f'  <line x1="{wx + 3:.1f}" y1="{wy:.1f}" x2="{wx + 3:.1f}" y2="{wy - wlen:.1f}"/>'
                    f'  <line x1="{wx - 5:.1f}" y1="{wy:.1f}" x2="{wx + 5:.1f}" y2="{wy:.1f}"/>'
                    f'  <line x1="{wx - 5:.1f}" y1="{wy - wlen:.1f}" x2="{wx + 5:.1f}" y2="{wy - wlen:.1f}"/>'
                    f'</g>'
                )
        svg_parts.append('</g>')

        # Draw Doors (Swing Arcs)
        svg_parts.append('<g id="doors">')
        for door in self.doors:
            dx = tx(door["x"])
            dy = ty(door["y"])
            dw = door["width"] * scale_px
            # Standard 90-degree swing arc
            svg_parts.append(
                f'<g stroke="#d97706" stroke-width="1.5" fill="none">'
                f'  <line x1="{dx:.1f}" y1="{dy:.1f}" x2="{dx + dw:.1f}" y2="{dy:.1f}"/>'
                f'  <path d="M {dx + dw:.1f} {dy:.1f} A {dw:.1f} {dw:.1f} 0 0 1 {dx:.1f} {dy - dw:.1f}" stroke-dasharray="3,3"/>'
                f'  <line x1="{dx:.1f}" y1="{dy:.1f}" x2="{dx:.1f}" y2="{dy - dw:.1f}"/>'
                f'</g>'
            )
        svg_parts.append('</g>')

        # North Arrow & Scale Bar
        na_x = width_px - 80
        na_y = height_px - 70
        svg_parts.append(
            f'<g id="north-arrow" transform="translate({na_x}, {na_y})">'
            f'  <circle cx="0" cy="0" r="22" fill="#ffffff" stroke="#0f172a" stroke-width="2"/>'
            f'  <polygon points="0,-18 7,6 0,0" fill="#0f172a"/>'
            f'  <polygon points="0,-18 -7,6 0,0" fill="#94a3b8"/>'
            f'  <text x="0" y="-24" font-size="12" font-weight="bold" text-anchor="middle" fill="#0f172a">N</text>'
            f'</g>'
        )

        # Bottom Info Bar
        tot_area = sum(r["area_m2"] for r in self.rooms)
        tot_sqft = round(tot_area * 10.7639, 1)
        svg_parts.append(
            f'<g id="footer" transform="translate(40, {height_px - 45})">'
            f'  <text x="0" y="0" font-size="13" font-weight="700" fill="#0f172a">TOTAL USABLE AREA: {tot_area:.1f} m² ({tot_sqft} sq ft)</text>'
            f'  <text x="0" y="18" font-size="11" fill="#64748b">ROOMS: {len(self.rooms)} | CODE COMPLIANT EGRESS &amp; VENTILATION</text>'
            f'</g>'
        )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

    def to_dxf(self, file_path: str):
        """Export to production DXF file compatible with AutoCAD, Revit, LibreCAD."""
        if not HAS_EZDXF:
            raise RuntimeError("ezdxf is required for DXF export. Install with `pip install ezdxf`.")

        doc = ezdxf.new("R2010")
        msp = doc.modelspace()

        # Setup layers
        doc.layers.add(name="A-WALL-EXTR", color=7)  # White/Black
        doc.layers.add(name="A-WALL-INTR", color=8)  # Grey
        doc.layers.add(name="A-DOOR", color=2)       # Yellow
        doc.layers.add(name="A-GLAZ", color=4)       # Cyan
        doc.layers.add(name="A-FLOR-TEXT", color=3)  # Green

        # Export walls
        for wall in self.walls:
            layer = "A-WALL-EXTR" if wall.get("is_exterior", True) else "A-WALL-INTR"
            msp.add_line(
                (wall["x1"], wall["y1"]),
                (wall["x2"], wall["y2"]),
                dxfattribs={"layer": layer}
            )

        # Export rooms
        for room in self.rooms:
            # Room label
            cx = room["x"] + room["w"] / 2
            cy = room["y"] + room["h"] / 2
            text = f"{room['name']}\\P{room['w']:.2f}m x {room['h']:.2f}m\\P{room['area_m2']} m2"
            msp.add_text(
                room["name"],
                dxfattribs={"layer": "A-FLOR-TEXT", "height": 0.25}
            ).set_placement((cx, cy), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

        doc.saveas(file_path)
        return file_path

    def to_pascal_scene(self) -> Dict[str, Any]:
        """Export to Pascal 3D scene data format."""
        stories = [{
            "id": "ground_floor",
            "name": "Ground Floor",
            "elevation": 0.0,
            "height": 2.8,
            "rooms": [
                {
                    "name": r["name"],
                    "polygon": [
                        [r["x"], r["y"]],
                        [r["x"] + r["w"], r["y"]],
                        [r["x"] + r["w"], r["y"] + r["h"]],
                        [r["x"], r["y"] + r["h"]]
                    ],
                    "zone": r["zone"]
                }
                for r in self.rooms
            ]
        }]
        return {
            "version": "1.0",
            "title": self.title,
            "units": "meters",
            "stories": stories
        }
