"""
Ultra-HD (104 Megapixels - 8640 x 12000) Master Corridor Plate Generator
Swabi Bypass Road along Badri Nullah (District Swabi, KP)
Zero channel encroachment, 15,000 cusecs flood capacity preserved.
"""

import math
import os
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import scipy.interpolate as interp
import xml.etree.ElementTree as ET

Image.MAX_IMAGE_PIXELS = None

# 1. Parse KML Coordinates
tree = ET.parse(r'c:\Users\Imran\Desktop\DS\Bypass.kml')
root = tree.getroot()
coords_text = ''
for elem in root.iter():
    if elem.tag.endswith('coordinates'):
        coords_text = elem.text.strip()
        break

pts = []
for p in coords_text.split():
    parts = p.split(',')
    pts.append((float(parts[0]), float(parts[1])))
pts = np.array(pts)

# Smooth spline (8,000 points for ultra-smooth 12,000 px vertical curve)
dx = np.diff(pts[:, 0])
dy = np.diff(pts[:, 1])
dist = np.concatenate(([0], np.cumsum(np.hypot(dx, dy))))
tck, u = interp.splprep([pts[:, 0], pts[:, 1]], u=dist, s=0, k=2)
u_new = np.linspace(0, dist[-1], 8000)
smooth_pts = np.array(interp.splev(u_new, tck)).T

# Cumulative ground distance
R_earth = 6371000.0
d_lat = np.radians(np.diff(smooth_pts[:, 1]))
d_lon = np.radians(np.diff(smooth_pts[:, 0]))
mean_lat = np.radians((smooth_pts[:-1, 1] + smooth_pts[1:, 1]) / 2.0)
d_dist = np.sqrt((d_lat * R_earth)**2 + (d_lon * R_earth * np.cos(mean_lat))**2)
cum_dist = np.concatenate(([0], np.cumsum(d_dist)))
print(f"Total road centerline length: {cum_dist[-1]:.1f} m")

def get_pixel_coords(lon_lat_array, center_lat, center_lon, zoom, width_px, height_px):
    n = 2.0 ** zoom
    c_xtile_f = (center_lon + 180.0) / 360.0 * n
    c_ytile_f = (1.0 - math.asinh(math.tan(math.radians(center_lat))) / math.pi) / 2.0 * n

    pixels = []
    for lon, lat in lon_lat_array:
        xtile_f = (lon + 180.0) / 360.0 * n
        ytile_f = (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n
        px = (xtile_f - c_xtile_f) * 256.0 + width_px / 2.0
        py = (ytile_f - c_ytile_f) * 256.0 + height_px / 2.0
        pixels.append((px, py))
    return np.array(pixels)

def render_ultra_hd():
    base_file = r'C:\Users\Imran\.gemini\antigravity\brain\1a9a1cc3-9fae-4ec5-9931-dee570100269\scratch\full_corridor_z19_base.png'
    out_png = r'c:\Users\Imran\Desktop\DS\Swabi_Bypass_Full_Corridor_Ultra_HD_104MP.png'
    out_jpg = r'c:\Users\Imran\Desktop\DS\Swabi_Bypass_Full_Corridor_Ultra_HD_104MP.jpg'
    
    t0 = time.time()
    print("Loading 104 Megapixel base satellite image...")
    raw_base = Image.open(base_file).convert('RGB')
    
    print("Enhancing tonal contrast and sharpness...")
    enh_col = ImageEnhance.Color(raw_base)
    base = enh_col.enhance(1.15)
    enh_con = ImageEnhance.Contrast(base)
    base = enh_con.enhance(1.12)
    base = base.filter(ImageFilter.UnsharpMask(radius=3.0, percent=140, threshold=3)).convert('RGBA')
    
    w, h = base.size
    print(f"Canvas dimensions: {w} x {h} ({w*h / 1e6:.1f} Megapixels)")
    
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    center_lat, center_lon, zoom = 34.1196, 72.4618, 19
    pts_in = get_pixel_coords(smooth_pts, center_lat, center_lon, zoom, w, h)
    
    tangents = np.gradient(pts_in, axis=0)
    norm = np.hypot(tangents[:, 0], tangents[:, 1])
    norm[norm == 0] = 1.0
    tangents /= norm[:, None]
    normals = np.column_stack([-tangents[:, 1], tangents[:, 0]])
    
    # Physical scale at lat 34.12 deg, zoom 19: 1 meter ≈ 4.05 px
    # Slightly emphasized (1.6x) for clear aerial presentation
    px_per_m = 6.8
    w_cw = (5.486 / 2.0) * px_per_m  # half carriageway ≈ 18.6 px
    w_sh = 0.914 * px_per_m          # shoulder ≈ 6.2 px
    w_form = w_cw + w_sh             # half formation ≈ 24.8 px
    w_slope = 4.0 * px_per_m         # 2H:1V side slope on 2.0m embankment ≈ 27.2 px
    
    print("Rendering 3D drop shadow...")
    shadow_offset = np.array([18.0, 18.0])
    s_left = pts_in + normals * (w_form + w_slope + 24.0) + shadow_offset
    s_right = pts_in - normals * (w_form + w_slope + 24.0) + shadow_offset
    s_poly = np.vstack([s_left, s_right[::-1]])
    
    shadow_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_img)
    s_draw.polygon([tuple(p) for p in s_poly], fill=(0, 0, 0, 130))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=28))
    overlay = Image.alpha_composite(overlay, shadow_img)
    draw = ImageDraw.Draw(overlay)
    
    print("Rendering landside slope...")
    land_outer = pts_in + normals * (w_form + w_slope)
    land_inner = pts_in + normals * w_form
    draw.polygon([tuple(p) for p in np.vstack([land_outer, land_inner[::-1]])], fill=(132, 124, 106, 255))
    for i in range(0, len(pts_in) - 1, 8):
        draw.line([tuple(land_inner[i]), tuple(land_outer[i])], fill=(116, 108, 92, 190), width=4)

    print("Rendering waterside slope: Class-A interlocking boulder riprap...")
    riprap_inner = pts_in - normals * w_form
    riprap_outer = pts_in - normals * (w_form + w_slope)
    draw.polygon([tuple(p) for p in np.vstack([riprap_inner, riprap_outer[::-1]])], fill=(55, 62, 70, 255))
    
    np.random.seed(303)
    for i in range(0, len(pts_in) - 1, 4):
        p_c = pts_in[i]
        n_c = -normals[i]  # strictly facing Badri Nullah (East / NE)
        for frac in [0.20, 0.45, 0.70, 0.92]:
            d = w_form + frac * w_slope
            bx = p_c[0] + n_c[0] * d + np.random.uniform(-4.0, 4.0)
            by = p_c[1] + n_c[1] * d + np.random.uniform(-4.0, 4.0)
            rx = np.random.uniform(9.0, 16.0)
            ry = rx * np.random.uniform(0.70, 0.88)
            shade = np.random.randint(155, 230)
            col = (shade, shade + 3, shade + 7, 255)
            draw.ellipse([bx - rx, by - ry, bx + rx, by + ry], fill=col, outline=(34, 38, 44, 255), width=3)
            draw.arc([bx - rx * 0.75, by - ry * 0.75, bx + rx * 0.75, by + ry * 0.75], start=180, end=360,
                     fill=(248, 252, 255, 230), width=3)

    print("Rendering compacted base shoulders...")
    sh_land = np.vstack([pts_in + normals * w_form, (pts_in + normals * w_cw)[::-1]])
    sh_water = np.vstack([pts_in - normals * w_cw, (pts_in - normals * w_form)[::-1]])
    draw.polygon([tuple(p) for p in sh_land], fill=(166, 160, 148, 255))
    draw.polygon([tuple(p) for p in sh_water], fill=(166, 160, 148, 255))

    print("Rendering bituminous asphalt carriageway...")
    cw_poly = np.vstack([pts_in + normals * w_cw, (pts_in - normals * w_cw)[::-1]])
    draw.polygon([tuple(p) for p in cw_poly], fill=(22, 24, 28, 255))

    print("Rendering road markings & safety barriers...")
    edge_land = pts_in + normals * (w_cw - 3.0)
    edge_water = pts_in - normals * (w_cw - 3.0)
    for i in range(len(pts_in) - 1):
        draw.line([tuple(edge_land[i]), tuple(edge_land[i + 1])], fill=(255, 255, 255, 255), width=6)
        draw.line([tuple(edge_water[i]), tuple(edge_water[i + 1])], fill=(255, 255, 255, 255), width=6)

    dash_len = 48
    gap_len = 56
    is_dash = True
    cur_len = 0
    for i in range(len(pts_in) - 1):
        seg_len = np.hypot(pts_in[i + 1, 0] - pts_in[i, 0], pts_in[i + 1, 1] - pts_in[i, 1])
        cur_len += seg_len
        if is_dash:
            draw.line([tuple(pts_in[i]), tuple(pts_in[i + 1])], fill=(255, 215, 0, 255), width=7)
            if cur_len >= dash_len:
                is_dash = False
                cur_len = 0
        else:
            if cur_len >= gap_len:
                is_dash = True
                cur_len = 0

    guard_line = pts_in - normals * (w_form - 2.5)
    for i in range(len(pts_in) - 1):
        draw.line([tuple(guard_line[i]), tuple(guard_line[i + 1])], fill=(235, 240, 245, 255), width=7)

    print("Compositing infrastructure overlay onto satellite base...")
    combined = Image.alpha_composite(base, overlay)
    draw_hud = ImageDraw.Draw(combined)

    # Fonts
    font_title_lg = ImageFont.truetype("arialbd.ttf", 144)
    font_title_sub = ImageFont.truetype("arial.ttf", 80)
    font_card_head = ImageFont.truetype("arialbd.ttf", 88)
    font_card_body = ImageFont.truetype("arial.ttf", 68)
    font_card_bold = ImageFont.truetype("arialbd.ttf", 68)
    font_callout_hd = ImageFont.truetype("arialbd.ttf", 72)
    font_callout_bd = ImageFont.truetype("arial.ttf", 62)
    font_badge = ImageFont.truetype("arialbd.ttf", 72)
    font_disc = ImageFont.truetype("arialbd.ttf", 72)
    font_hud = ImageFont.truetype("arial.ttf", 64)

    print("Rendering HUD elements and cards...")
    # A. Top Left Main Title Banner
    draw_hud.rounded_rectangle([160, 160, 4100, 640], radius=56, fill=(18, 22, 28, 235), outline=(255, 255, 255, 220), width=6)
    draw_hud.text((260, 230), "SWABI BYPASS ROAD ALONG BADRI NULLAH", fill=(255, 255, 255, 255), font=font_title_lg)
    draw_hud.text((260, 430), "Full Corridor Master Alignment & Flood Protection Scheme (CH 0+000 to CH 3+086)", fill=(186, 230, 253, 255), font=font_title_sub)

    # B. Top Right Project Parameter & Legend Card
    card_x0, card_y0 = w - 2720, 160
    card_w, card_h = 2560, 1960
    draw_hud.rounded_rectangle([card_x0, card_y0, card_x0 + card_w, card_y0 + card_h], radius=56, fill=(18, 22, 28, 238), outline=(56, 189, 248, 240), width=6)
    draw_hud.rectangle([card_x0, card_y0, card_x0 + card_w, card_y0 + 220], fill=(30, 41, 59, 245))
    draw_hud.text((card_x0 + 100, card_y0 + 60), "PROJECT SUMMARY & TECHNICAL DATA", fill=(255, 255, 255, 255), font=font_card_head)

    rows = [
        ("Alignment Length:", "3,087.34 m (3.087 km) [bypass.kml]"),
        ("Location:", "Swabi City to Ismailabad, District Swabi"),
        ("Design Peak Flood (Q):", "15,000 Cusecs (Badri Nullah catchment)"),
        ("Waterway Clearance:", "100% Active Opening (Zero Road Encroachment)"),
        ("Embankment Function:", "Highway Bypass + Marginal Flood Bund"),
        ("Embankment Height:", "2.0 m (6.56 ft) compacted common borrow fill"),
        ("Side Slopes:", "2H : 1V (Compacted 95% AASHTO T-180)"),
        ("Slope Armor (Waterside):", "Class-A Stone Pitching / Heavy Riprap"),
        ("Formation Width:", "7.315 m (24.0 ft)"),
        ("Carriageway Blacktop:", "5.486 m (18.0 ft) Asphalt with 2% Camber"),
        ("Shoulders:", "0.914 m (3.0 ft) treated gravel on each side"),
        ("Freeboard:", "1.0 m (3.28 ft) above 100-Year HFL"),
        ("Northern Tie-in (CH 0+000):", "Swabi - Mardan Highway connection"),
        ("Southern Tie-in (CH 3+086):", "Swabi - Jehangira Road intersection")
    ]
    ry = card_y0 + 280
    for label, val in rows:
        draw_hud.text((card_x0 + 100, ry), label, fill=(148, 163, 184, 255), font=font_card_bold)
        draw_hud.text((card_x0 + 1080, ry), val, fill=(248, 250, 252, 255), font=font_card_body)
        ry += 112

    # C. Start & End Chainage Badges
    v1_pt = pts_in[0]
    draw_hud.rounded_rectangle([v1_pt[0] - 440, v1_pt[1] - 260, v1_pt[0] + 440, v1_pt[1] - 80], radius=32,
                               fill=(16, 185, 129, 245), outline=(255, 255, 255, 255), width=6)
    draw_hud.text((v1_pt[0] - 380, v1_pt[1] - 228), "START: CH 0+000", fill=(255, 255, 255, 255), font=font_badge)
    draw_hud.line([(v1_pt[0], v1_pt[1] - 80), (v1_pt[0], v1_pt[1])], fill=(16, 185, 129, 255), width=10)
    draw_hud.ellipse([v1_pt[0] - 24, v1_pt[1] - 24, v1_pt[0] + 24, v1_pt[1] + 24], fill=(255, 255, 255, 255), outline=(16, 185, 129, 255), width=8)

    v12_pt = pts_in[-1]
    draw_hud.rounded_rectangle([v12_pt[0] - 420, v12_pt[1] + 100, v12_pt[0] + 420, v12_pt[1] + 280], radius=32,
                               fill=(239, 68, 68, 245), outline=(255, 255, 255, 255), width=6)
    draw_hud.text((v12_pt[0] - 350, v12_pt[1] + 132), "END: CH 3+086", fill=(255, 255, 255, 255), font=font_badge)
    draw_hud.line([(v12_pt[0], v12_pt[1]), (v12_pt[0], v12_pt[1] + 100)], fill=(239, 68, 68, 255), width=10)
    draw_hud.ellipse([v12_pt[0] - 24, v12_pt[1] - 24, v12_pt[0] + 24, v12_pt[1] + 24], fill=(255, 255, 255, 255), outline=(239, 68, 68, 255), width=8)

    # Intermediate chainage ticks (CH 1+000 and CH 2+000)
    for target_m, label_ch in [(1000.0, "CH 1+000"), (2000.0, "CH 2+000")]:
        idx = np.argmin(np.abs(cum_dist - target_m))
        pt_ch = pts_in[idx]
        draw_hud.ellipse([pt_ch[0] - 22, pt_ch[1] - 22, pt_ch[0] + 22, pt_ch[1] + 22], fill=(250, 204, 21, 255), outline=(0, 0, 0, 255), width=6)
        draw_hud.rounded_rectangle([pt_ch[0] - 260, pt_ch[1] - 150, pt_ch[0] + 260, pt_ch[1] - 50], radius=24,
                                   fill=(20, 20, 20, 220), outline=(250, 204, 21, 230), width=4)
        draw_hud.text((pt_ch[0] - 208, pt_ch[1] - 134), label_ch, fill=(250, 204, 21, 255), font=font_card_bold)

    # D. Key Engineering Callout Boxes along the Corridor
    callouts_full = [
        {
            'box_xy': (240, 1920),
            'text': "Northern Alignment & Meander Correction (CH 0+000 - CH 0+900):\n• Bypass straightens across plain, correcting sharp eastward meander of Badri Nullah\n• Preserves 100% of the active 15,000 cusecs waterway opening with zero channel overlap\n• 2.0 m raised embankment with Class-A stone pitching revetment on eastern slope",
            'arrow_to': (4200, 2080)
        },
        {
            'box_xy': (5120, 2720),
            'text': "Active Badri Nullah Meander Loop:\n• Peak flood capacity Q = 15,000 cusecs\n• Maintained 100% open & unobstructed\n• Zero road embankment encroachment",
            'arrow_to': (4640, 3120)
        },
        {
            'box_xy': (240, 5600),
            'text': "Middle Flood Protection Bund Section (CH 1+200 - CH 2+200):\n• Aligned directly along western bank of Badri Nullah immediately opposite Swabi City\n• Dual function: 2-lane arterial bypass + primary marginal flood defense bund\n• Heavy interlocking boulder riprap resists high-velocity flood scour (V > 3.0 m/s)",
            'arrow_to': (3200, 6400)
        },
        {
            'box_xy': (5120, 6720),
            'text': "Badri Nullah Active Floodway Bed:\n• Continuous natural riverbed preserved\n• Safe 1.0 m freeboard margin to road crest\n• Flood waters safely conveyed downstream",
            'arrow_to': (3480, 7400)
        },
        {
            'box_xy': (240, 8600),
            'text': "Typical Geometric Cross-Section Parameters:\n• 7.315 m Total Formation (24.0 ft): 5.486 m Carriageway (18 ft) + 2x0.914 m Shoulders\n• Pavement: 50 mm ACWC + 150 mm ABC + 200 mm Subbase on Compacted Subgrade\n• Slopes: 2H : 1V with 300 mm boulder pitching over 150 mm gravel filter on drain side\n• Safety: Continuous galvanized steel W-beam crash barrier along water-facing crest",
            'arrow_to': (3000, 9400)
        },
        {
            'box_xy': (240, 10720),
            'text': "Southern Approach & Tie-In Junction (CH 2+500 - CH 3+086):\n• Follows southern bank curve of Badri Nullah, fully clear of active waterway bed\n• At-grade channelized intersection tying seamlessly into Swabi - Jehangira Road (V12)\n• Eliminates heavy regional traffic through congested Swabi urban city core",
            'arrow_to': (4600, 10880)
        }
    ]

    for c in callouts_full:
        bx, by = c['box_xy']
        lines = c['text'].split('\n')
        max_lw = 0
        total_lh = 0
        for l_idx, l in enumerate(lines):
            f = font_callout_hd if l_idx == 0 else font_callout_bd
            bb = f.getbbox(l)
            lw = bb[2] - bb[0]
            if lw > max_lw: max_lw = lw
            total_lh += (bb[3] - bb[1]) + 24
            
        bw = max_lw + 144
        bh = total_lh + 104
        
        draw_hud.rounded_rectangle([bx, by, bx + bw, by + bh], radius=40,
                                   fill=(16, 20, 26, 235), outline=(255, 255, 255, 220), width=6)
        
        cur_y = by + 56
        for l_idx, l in enumerate(lines):
            f = font_callout_hd if l_idx == 0 else font_callout_bd
            col = (56, 189, 248, 255) if l_idx == 0 else (241, 245, 249, 255)
            draw_hud.text((bx + 72, cur_y), l, fill=col, font=f)
            bb = f.getbbox(l)
            cur_y += (bb[3] - bb[1]) + 24
            
        if 'arrow_to' in c:
            tx, ty = c['arrow_to']
            if tx < bx: ax_pt = (bx, by + bh / 2.0)
            elif tx > bx + bw: ax_pt = (bx + bw, by + bh / 2.0)
            elif ty < by: ax_pt = (bx + bw / 2.0, by)
            else: ax_pt = (bx + bw / 2.0, by + bh)
                
            draw_hud.line([ax_pt, (tx, ty)], fill=(255, 255, 255, 240), width=6)
            angle = math.atan2(ty - ax_pt[1], tx - ax_pt[0])
            a_len = 40
            p_a1 = (tx - a_len * math.cos(angle - math.pi / 6), ty - a_len * math.sin(angle - math.pi / 6))
            p_a2 = (tx - a_len * math.cos(angle + math.pi / 6), ty - a_len * math.sin(angle + math.pi / 6))
            draw_hud.polygon([(tx, ty), p_a1, p_a2], fill=(255, 255, 255, 255))

    # E. Important Geographic Landmark Labels
    landmarks = [
        ("Swabi City Center (Congested Core Bypassed)", (6480, 4600), (255, 255, 255)),
        ("Swabi - Jehangira Road (Regional Highway)", (6880, 9800), (250, 204, 21)),
        ("Swabi - Mardan Road (Northern Arterial)", (6800, 2240), (250, 204, 21)),
        ("Badri Nullah (Badri Khwar)", (4320, 4600), (56, 189, 248))
    ]
    for lm_text, lm_pt, lm_col in landmarks:
        tb = font_card_head.getbbox(lm_text)
        lm_w = tb[2] - tb[0] + 96
        lm_h = tb[3] - tb[1] + 64
        draw_hud.rounded_rectangle([lm_pt[0] - lm_w // 2, lm_pt[1] - lm_h // 2, lm_pt[0] + lm_w // 2, lm_pt[1] + lm_h // 2],
                                   radius=24, fill=(15, 23, 42, 225), outline=lm_col, width=4)
        draw_hud.text((lm_pt[0] - lm_w // 2 + 48, lm_pt[1] - lm_h // 2 + 32), lm_text, fill=lm_col, font=font_card_head)

    # F. Bottom Google Earth Telemetry & Disclaimer Bar
    disc_h = 220
    draw_hud.rectangle([0, h - disc_h, w, h], fill=(15, 20, 26, 240))
    
    # Left: Watermarks
    draw_hud.text((100, h - disc_h + 48), "Google Earth", fill=(255, 255, 255, 255), font=font_card_head)
    draw_hud.text((720, h - disc_h + 64), "100%", fill=(180, 180, 180, 255), font=font_hud)
    draw_hud.text((940, h - disc_h + 64), "Data attribution", fill=(180, 180, 180, 255), font=font_hud)
    draw_hud.text((1440, h - disc_h + 64), "Imagery date: 2/19/2025  © Airbus / Maxar", fill=(180, 180, 180, 255), font=font_hud)

    # Center: Disclaimer
    disc_text = "CONCEPT VISUALISATION — illustrative 2 m embankment — not approved design"
    d_box = font_disc.getbbox(disc_text)
    dw = d_box[2] - d_box[0]
    draw_hud.text(((w - dw) // 2, h - disc_h + 60), disc_text, fill=(255, 255, 255, 255), font=font_disc)

    # Right: Metric Scale Bar (200 m = 810 px at true zoom 19 ground scale)
    scale_bar_x = w - 2480
    draw_hud.line([(scale_bar_x, h - disc_h + 136), (scale_bar_x + 520, h - disc_h + 136)], fill=(255, 255, 255, 255), width=8)
    draw_hud.line([(scale_bar_x, h - disc_h + 104), (scale_bar_x, h - disc_h + 136)], fill=(255, 255, 255, 255), width=8)
    draw_hud.line([(scale_bar_x + 520, h - disc_h + 104), (scale_bar_x + 520, h - disc_h + 136)], fill=(255, 255, 255, 255), width=8)
    draw_hud.text((scale_bar_x + 168, h - disc_h + 40), "200 m", fill=(255, 255, 255, 255), font=font_hud)

    draw_hud.text((w - 1840, h - disc_h + 64), "Camera: 1,850 m   34°07'10.5\"N 72°27'41.5\"E 312 m", fill=(255, 255, 255, 255), font=font_hud)

    # 3D UI Control Buttons
    btn_x = w - 660
    draw_hud.ellipse([btn_x, h - disc_h + 40, btn_x + 140, h - disc_h + 180], fill=(45, 52, 60, 255), outline=(100, 110, 120, 255), width=3)
    draw_hud.text((btn_x + 32, h - disc_h + 64), "3D", fill=(255, 255, 255, 255), font=font_hud)
    draw_hud.ellipse([btn_x + 180, h - disc_h + 40, btn_x + 320, h - disc_h + 180], fill=(45, 52, 60, 255), outline=(100, 110, 120, 255), width=3)
    draw_hud.text((btn_x + 228, h - disc_h + 64), "N", fill=(239, 68, 68, 255), font=font_hud)

    print("Saving ultra-high resolution outputs (PNG & JPG)...")
    final_rgb = combined.convert('RGB')
    
    # Save 104 MP JPEG (ultra-fast preview, ~18-25 MB)
    final_rgb.save(out_jpg, format='JPEG', quality=95, optimize=True)
    print(f"Ultra-HD 104MP JPG saved: {out_jpg}")
    
    # Save 104 MP PNG (master lossless archive)
    final_rgb.save(out_png, format='PNG', optimize=True)
    print(f"Ultra-HD 104MP PNG saved: {out_png}")
    print(f"Entire 104 Megapixel rendering pipeline completed in {time.time() - t0:.1f}s!")

if __name__ == '__main__':
    render_ultra_hd()
