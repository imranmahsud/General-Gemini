"""
Civil Engineering Corridor Master Overview Generator
Extracts coordinates from KML, downloads georeferenced satellite base tiles,
interpolates survey vertices using B-splines, and renders a presentation-grade
corridor plate with supersampled 3D road embankment, boulder riprap, markings,
HUD summary card, engineering callouts, and Google Earth telemetry.
"""

import math
import os
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import scipy.interpolate as interp

def parse_kml_coordinates(kml_path):
    tree = ET.parse(kml_path)
    root = tree.getroot()
    coords_text = ''
    for elem in root.iter():
        if elem.tag.endswith('coordinates'):
            coords_text = elem.text.strip()
            break
    pts = []
    for p in coords_text.split():
        parts = p.split(',')
        if len(parts) >= 2:
            lon, lat = float(parts[0]), float(parts[1])
            pts.append((lon, lat))
    return np.array(pts)

def interpolate_spline(pts, num_samples=4000):
    dx = np.diff(pts[:, 0])
    dy = np.diff(pts[:, 1])
    dist = np.concatenate(([0], np.cumsum(np.hypot(dx, dy))))
    tck, u = interp.splprep([pts[:, 0], pts[:, 1]], u=dist, s=0, k=2)
    u_new = np.linspace(0, dist[-1], num_samples)
    smooth_pts = np.array(interp.splev(u_new, tck)).T
    return smooth_pts

def get_pixel_coords_scaled(lon_lat_array, center_lat, center_lon, zoom, width_px, height_px, scale=1.0):
    n = 2.0 ** zoom
    c_xtile_f = (center_lon + 180.0) / 360.0 * n
    c_ytile_f = (1.0 - math.asinh(math.tan(math.radians(center_lat))) / math.pi) / 2.0 * n

    pixels = []
    for lon, lat in lon_lat_array:
        xtile_f = (lon + 180.0) / 360.0 * n
        ytile_f = (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n
        px = (xtile_f - c_xtile_f) * (256.0 * scale) + (width_px * scale) / 2.0
        py = (ytile_f - c_ytile_f) * (256.0 * scale) + (height_px * scale) / 2.0
        pixels.append((px, py))
    return np.array(pixels)

def render_corridor_master(base_img_path, smooth_pts, center_lat, center_lon, zoom, out_path,
                           title="MASTER ALIGNMENT & CORRIDOR OVERVIEW",
                           subtitle="Civil Engineering Highway Alignment & Flood Protection Scheme",
                           summary_rows=None, callouts=None, landmarks=None):
    raw_base = Image.open(base_img_path).convert('RGB')
    
    # 1. Enhance base imagery
    base = ImageEnhance.Color(raw_base).enhance(1.15)
    base = ImageEnhance.Contrast(base).enhance(1.12)
    base = base.filter(ImageFilter.UnsharpMask(radius=2.0, percent=130, threshold=3)).convert('RGBA')
    
    w, h = base.size
    scale = 2  # 2x SSAA
    sw, sh = w * scale, h * scale
    
    overlay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    centerline_px = get_pixel_coords_scaled(smooth_pts, center_lat, center_lon, zoom, w, h, scale)
    pts_in = centerline_px

    tangents = np.gradient(pts_in, axis=0)
    norm = np.hypot(tangents[:, 0], tangents[:, 1])
    norm[norm == 0] = 1.0
    tangents /= norm[:, None]
    normals = np.column_stack([-tangents[:, 1], tangents[:, 0]])
    
    px_per_m = 2.2 * scale
    w_cw = (5.486 / 2.0) * px_per_m
    w_sh = 0.914 * px_per_m
    w_form = w_cw + w_sh
    w_slope = 4.0 * px_per_m
    
    # 3D Drop Shadow
    shadow_offset = np.array([5.0 * scale, 5.0 * scale])
    s_left = pts_in + normals * (w_form + w_slope + 6 * scale) + shadow_offset
    s_right = pts_in - normals * (w_form + w_slope + 6 * scale) + shadow_offset
    s_poly = np.vstack([s_left, s_right[::-1]])
    
    shadow_img = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_img)
    s_draw.polygon([tuple(p) for p in s_poly], fill=(0, 0, 0, 125))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=8 * scale))
    overlay = Image.alpha_composite(overlay, shadow_img)
    draw = ImageDraw.Draw(overlay)

    # Landside slope (compacted earth)
    land_outer = pts_in + normals * (w_form + w_slope)
    land_inner = pts_in + normals * w_form
    draw.polygon([tuple(p) for p in np.vstack([land_outer, land_inner[::-1]])], fill=(132, 124, 106, 255))
    for i in range(0, len(pts_in) - 1, 4):
        draw.line([tuple(land_inner[i]), tuple(land_outer[i])], fill=(116, 108, 92, 190), width=max(1, int(1.2 * scale)))

    # Waterside slope (Class-A stone riprap)
    riprap_inner = pts_in - normals * w_form
    riprap_outer = pts_in - normals * (w_form + w_slope)
    draw.polygon([tuple(p) for p in np.vstack([riprap_inner, riprap_outer[::-1]])], fill=(55, 62, 70, 255))
    
    np.random.seed(303)
    for i in range(0, len(pts_in) - 1, 2):
        p_c = pts_in[i]
        n_c = -normals[i]
        for frac in [0.20, 0.45, 0.70, 0.92]:
            d = w_form + frac * w_slope
            bx = p_c[0] + n_c[0] * d + np.random.uniform(-1.6 * scale, 1.6 * scale)
            by = p_c[1] + n_c[1] * d + np.random.uniform(-1.6 * scale, 1.6 * scale)
            rx = np.random.uniform(3.2 * scale, 5.8 * scale)
            ry = rx * np.random.uniform(0.68, 0.85)
            shade = np.random.randint(155, 228)
            col = (shade, shade + 3, shade + 7, 255)
            draw.ellipse([bx - rx, by - ry, bx + rx, by + ry], fill=col, outline=(36, 40, 46, 255), width=max(1, int(1.4 * scale)))
            draw.arc([bx - rx * 0.75, by - ry * 0.75, bx + rx * 0.75, by + ry * 0.75], start=180, end=360,
                     fill=(248, 252, 255, 230), width=max(1, int(1.2 * scale)))

    # Shoulders
    draw.polygon([tuple(p) for p in np.vstack([pts_in + normals * w_form, (pts_in + normals * w_cw)[::-1]])], fill=(166, 160, 148, 255))
    draw.polygon([tuple(p) for p in np.vstack([pts_in - normals * w_cw, (pts_in - normals * w_form)[::-1]])], fill=(166, 160, 148, 255))

    # Carriageway
    draw.polygon([tuple(p) for p in np.vstack([pts_in + normals * w_cw, (pts_in - normals * w_cw)[::-1]])], fill=(22, 24, 28, 255))

    # Edges
    edge_land = pts_in + normals * (w_cw - 1.2 * scale)
    edge_water = pts_in - normals * (w_cw - 1.2 * scale)
    for i in range(len(pts_in) - 1):
        draw.line([tuple(edge_land[i]), tuple(edge_land[i + 1])], fill=(255, 255, 255, 255), width=max(1, int(2.2 * scale)))
        draw.line([tuple(edge_water[i]), tuple(edge_water[i + 1])], fill=(255, 255, 255, 255), width=max(1, int(2.2 * scale)))

    # Dashed centerline
    dash_len = int(12 * scale)
    gap_len = int(14 * scale)
    is_dash = True
    cur_len = 0
    for i in range(len(pts_in) - 1):
        seg_len = np.hypot(pts_in[i + 1, 0] - pts_in[i, 0], pts_in[i + 1, 1] - pts_in[i, 1])
        cur_len += seg_len
        if is_dash:
            draw.line([tuple(pts_in[i]), tuple(pts_in[i + 1])], fill=(255, 210, 30, 255), width=max(1, int(2.4 * scale)))
            if cur_len >= dash_len:
                is_dash = False
                cur_len = 0
        else:
            if cur_len >= gap_len:
                is_dash = True
                cur_len = 0

    # Guardrail
    guard_line = pts_in - normals * (w_form - 0.9 * scale)
    for i in range(len(pts_in) - 1):
        draw.line([tuple(guard_line[i]), tuple(guard_line[i + 1])], fill=(235, 240, 245, 255), width=max(1, int(2.6 * scale)))

    overlay_1x = overlay.resize((w, h), Image.Resampling.LANCZOS)
    combined = Image.alpha_composite(base, overlay_1x)
    draw_hud = ImageDraw.Draw(combined)

    try:
        font_lg = ImageFont.truetype("arialbd.ttf", 36)
        font_sub = ImageFont.truetype("arial.ttf", 20)
        font_hd = ImageFont.truetype("arialbd.ttf", 22)
        font_bd = ImageFont.truetype("arial.ttf", 17)
        font_bld = ImageFont.truetype("arialbd.ttf", 17)
        font_call_hd = ImageFont.truetype("arialbd.ttf", 18)
        font_call_bd = ImageFont.truetype("arial.ttf", 16)
        font_badge = ImageFont.truetype("arialbd.ttf", 18)
        font_hud = ImageFont.truetype("arial.ttf", 16)
    except:
        font_lg = ImageFont.load_default()
        font_sub = font_hd = font_bd = font_bld = font_call_hd = font_call_bd = font_badge = font_hud = font_lg

    # Banner
    draw_hud.rounded_rectangle([40, 40, 1020, 160], radius=14, fill=(18, 22, 28, 230), outline=(255, 255, 255, 220), width=2)
    draw_hud.text((65, 58), title, fill=(255, 255, 255, 255), font=font_lg)
    draw_hud.text((65, 108), subtitle, fill=(186, 230, 253, 255), font=font_sub)

    # Technical Card
    if summary_rows:
        card_x0, card_y0 = w - 680, 40
        card_w, card_h = 640, 490
        draw_hud.rounded_rectangle([card_x0, card_y0, card_x0 + card_w, card_y0 + card_h], radius=14, fill=(18, 22, 28, 235), outline=(56, 189, 248, 240), width=2)
        draw_hud.rectangle([card_x0, card_y0, card_x0 + card_w, card_y0 + 55], fill=(30, 41, 59, 240))
        draw_hud.text((card_x0 + 25, card_y0 + 15), "PROJECT SUMMARY & TECHNICAL DATA", fill=(255, 255, 255, 255), font=font_hd)
        ry = card_y0 + 70
        for label, val in summary_rows:
            draw_hud.text((card_x0 + 25, ry), label, fill=(148, 163, 184, 255), font=font_bld)
            draw_hud.text((card_x0 + 270, ry), val, fill=(248, 250, 252, 255), font=font_bd)
            ry += 28

    # Callouts
    if callouts:
        for c in callouts:
            bx, by = c['box_xy']
            lines = c['text'].split('\n')
            max_lw = max([font_call_hd.getbbox(l)[2] - font_call_hd.getbbox(l)[0] for l in lines])
            total_lh = sum([(font_call_bd.getbbox(l)[3] - font_call_bd.getbbox(l)[1]) + 6 for l in lines])
            bw = max_lw + 36
            bh = total_lh + 26
            draw_hud.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10, fill=(16, 20, 26, 230), outline=(255, 255, 255, 220), width=2)
            cur_y = by + 14
            for l_idx, l in enumerate(lines):
                f = font_call_hd if l_idx == 0 else font_call_bd
                col = (56, 189, 248, 255) if l_idx == 0 else (241, 245, 249, 255)
                draw_hud.text((bx + 18, cur_y), l, fill=col, font=f)
                cur_y += (f.getbbox(l)[3] - f.getbbox(l)[1]) + 6
            if 'arrow_to' in c:
                tx, ty = c['arrow_to']
                ax_pt = (bx + bw, by + bh / 2.0) if tx > bx + bw else (bx, by + bh / 2.0)
                draw_hud.line([ax_pt, (tx, ty)], fill=(255, 255, 255, 240), width=2)

    # Telemetry bar
    disc_h = 55
    draw_hud.rectangle([0, h - disc_h, w, h], fill=(15, 20, 26, 240))
    draw_hud.text((25, h - disc_h + 12), "Google Earth", fill=(255, 255, 255, 255), font=font_hd)
    draw_hud.text((180, h - disc_h + 16), "100%", fill=(180, 180, 180, 255), font=font_hud)
    draw_hud.text((235, h - disc_h + 16), "Data attribution", fill=(180, 180, 180, 255), font=font_hud)
    draw_hud.text((360, h - disc_h + 16), "Imagery date: 2/19/2025  © Airbus / Maxar", fill=(180, 180, 180, 255), font=font_hud)

    disc_text = "CONCEPT VISUALISATION — illustrative 2 m embankment — not approved design"
    dw = font_bld.getbbox(disc_text)[2] - font_bld.getbbox(disc_text)[0]
    draw_hud.text(((w - dw) // 2, h - disc_h + 15), disc_text, fill=(255, 255, 255, 255), font=font_bld)

    clean_img = Image.new('RGB', combined.size)
    clean_img.paste(combined)
    clean_img.save(out_path, format='PNG', optimize=True)
