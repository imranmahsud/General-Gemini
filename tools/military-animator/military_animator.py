"""Generates cinematic 9:16 (1080x1920) military defense animations for MoneyPrinterTurbo."""

import math
import os
import random
import subprocess
from PIL import Image, ImageDraw, ImageFont
import numpy as np

OUTPUT_DIR = "D:/AI-Folders/MoneyPrinterTurbo/military_clips"
FFMPEG_PATH = "C:/ProgramData/chocolatey/bin/ffmpeg.exe"
WIDTH, HEIGHT = 1080, 1920
FPS = 30
DURATION = 10  # 10 seconds per clip = 300 frames
TOTAL_FRAMES = FPS * DURATION

FONT_DIR = "C:/Windows/Fonts"
try:
    FONT_TITLE = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 48)
    FONT_MONO = ImageFont.truetype(os.path.join(FONT_DIR, "consola.ttf"), 32)
    FONT_MONO_SM = ImageFont.truetype(os.path.join(FONT_DIR, "consola.ttf"), 24)
    FONT_HUGE = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 72)
except Exception:
    FONT_TITLE = ImageFont.load_default()
    FONT_MONO = ImageFont.load_default()
    FONT_MONO_SM = ImageFont.load_default()
    FONT_HUGE = ImageFont.load_default()

def start_ffmpeg_pipe(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cmd = [
        FFMPEG_PATH, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-vcodec", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "veryfast",
        "-crf", "20",
        output_path
    ]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)

# -------------------------------------------------------------
# CLIP 1: Tactical Geopolitical Map & Threat Radar
# -------------------------------------------------------------
def render_clip1_radar():
    out_file = os.path.join(OUTPUT_DIR, "clip1_radar.mp4")
    print("Rendering Clip 1: Tactical Threat Radar...")
    proc = start_ffmpeg_pipe(out_file)
    cx, cy = WIDTH // 2, HEIGHT // 2 - 100
    radar_radius = 420

    for f in range(TOTAL_FRAMES):
        img = Image.new("RGB", (WIDTH, HEIGHT), (10, 16, 26))
        draw = ImageDraw.Draw(img)

        # Tactical Grid Lines
        for x in range(0, WIDTH, 120):
            draw.line([(x, 0), (x, HEIGHT)], fill=(18, 30, 48), width=1)
        for y in range(0, HEIGHT, 120):
            draw.line([(0, y), (WIDTH, y)], fill=(18, 30, 48), width=1)

        # Radar concentric rings
        for r in [120, 240, 340, radar_radius]:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(20, 70, 110), width=2)

        # Radar crosshairs
        draw.line([(cx - radar_radius - 40, cy), (cx + radar_radius + 40, cy)], fill=(20, 80, 120), width=1)
        draw.line([(cx, cy - radar_radius - 40), (cx, cy + radar_radius + 40)], fill=(20, 80, 120), width=1)

        # Animated Sweep line
        angle = (f * 4.5) % 360
        rad = math.radians(angle)
        sx = cx + int(radar_radius * math.cos(rad))
        sy = cy + int(radar_radius * math.sin(rad))
        draw.line([(cx, cy), (sx, sy)], fill=(0, 255, 200), width=3)

        # Draw sweep cone trail
        for trail_step in range(1, 15):
            t_angle = angle - trail_step * 2.0
            t_rad = math.radians(t_angle)
            tx = cx + int(radar_radius * math.cos(t_rad))
            ty = cy + int(radar_radius * math.sin(t_rad))
            alpha_color = (0, max(0, 180 - trail_step * 12), max(0, 150 - trail_step * 10))
            draw.line([(cx, cy), (tx, ty)], fill=alpha_color, width=2)

        # Border outline representation
        border_pts = [(160, 480), (320, 540), (520, 680), (740, 790), (920, 840)]
        draw.line(border_pts, fill=(255, 60, 60), width=4)
        draw.text((360, 500), "--- SAUDI ARABIA ---", fill=(100, 200, 255), font=FONT_MONO)
        draw.text((420, 720), "--- YEMEN / HOUTHI SECTOR ---", fill=(255, 120, 100), font=FONT_MONO)

        # Threat targets with blinking effect
        targets = [
            (560, 700, "TGT-901 [BALLISTIC TEL]"),
            (380, 620, "TGT-404 [DRONE DEPOT]"),
            (720, 760, "TGT-112 [RADAR SITE]"),
        ]
        for tx, ty, label in targets:
            blink = (f // 8) % 2 == 0
            color = (255, 40, 40) if blink else (160, 20, 20)
            draw.ellipse([tx - 12, ty - 12, tx + 12, ty + 12], fill=color, outline=(255, 200, 200), width=2)
            draw.text((tx + 20, ty - 15), label, fill=(255, 200, 100), font=FONT_MONO_SM)

        # Top HUD Banner
        draw.rectangle([60, 80, WIDTH - 60, 180], fill=(16, 26, 42), outline=(0, 220, 255), width=2)
        draw.text((90, 95), "GEOSPATIAL DEFENSE MONITOR // REGIONAL SECTOR", fill=(0, 240, 255), font=FONT_TITLE)
        draw.text((90, 140), f"SCANNING: ACTIVE | SWEEP FREQ: 3.2 GHz | AZIMUTH: {int(angle)}°", fill=(180, 210, 240), font=FONT_MONO_SM)

        # Bottom Telemetry Box
        draw.rectangle([60, HEIGHT - 320, WIDTH - 60, HEIGHT - 100], fill=(16, 26, 42), outline=(255, 70, 70), width=2)
        alert_blink = (f // 10) % 2 == 0
        banner_fill = (255, 40, 40) if alert_blink else (140, 20, 20)
        draw.rectangle([60, HEIGHT - 320, WIDTH - 60, HEIGHT - 260], fill=banner_fill)
        draw.text((100, HEIGHT - 310), "THREAT STATUS: ESCALATED BORDER MISSILE ACTIVITY", fill=(255, 255, 255), font=FONT_TITLE)
        draw.text((100, HEIGHT - 240), f"COORDINATES: LAT 17°12'N  LON 43°45'E  |  FRAME: {f:03d}/{TOTAL_FRAMES}", fill=(200, 220, 240), font=FONT_MONO)
        draw.text((100, HEIGHT - 200), "SURVEILLANCE: AIRBORNE E-3 AWACS + SATELLITE IMAGERY", fill=(160, 190, 220), font=FONT_MONO_SM)

        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    proc.wait()
    print("Clip 1 done.")

# -------------------------------------------------------------
# CLIP 2: Ballistic Missile Launch Animation
# -------------------------------------------------------------
def render_clip2_missile():
    out_file = os.path.join(OUTPUT_DIR, "clip2_missile_launch.mp4")
    print("Rendering Clip 2: Ballistic Missile Launch...")
    proc = start_ffmpeg_pipe(out_file)

    random.seed(42)
    smoke_particles = []

    for f in range(TOTAL_FRAMES):
        # Base nighttime desert background
        img = Image.new("RGB", (WIDTH, HEIGHT), (8, 12, 22))
        draw = ImageDraw.Draw(img)

        # Mountains silhouette in distance
        mountain_pts = [(0, HEIGHT - 450), (220, HEIGHT - 550), (450, HEIGHT - 480), (700, HEIGHT - 590), (950, HEIGHT - 510), (WIDTH, HEIGHT - 540), (WIDTH, HEIGHT), (0, HEIGHT)]
        draw.polygon(mountain_pts, fill=(18, 24, 38))
        draw.rectangle([0, HEIGHT - 350, WIDTH, HEIGHT], fill=(26, 32, 45))  # Ground desert floor

        # Missile physics
        # Launch starts at frame 30
        missile_x = WIDTH // 2
        initial_y = HEIGHT - 480
        if f < 30:
            missile_y = initial_y
            speed = 0
            is_launched = False
        else:
            t = (f - 30) / 30.0
            speed = 14 * t + 1.2 * (t ** 2.2)
            missile_y = initial_y - int(speed * 28)
            is_launched = True

        # Camera screen shake during launch
        shake_x, shake_y = 0, 0
        if is_launched and missile_y > 200:
            shake_x = random.randint(-4, 4)
            shake_y = random.randint(-4, 4)

        # Spawn exhaust and smoke particles if launching
        if is_launched:
            for _ in range(8):
                smoke_particles.append({
                    "x": missile_x + random.randint(-18, 18),
                    "y": missile_y + 160 + random.randint(0, 20),
                    "vx": random.uniform(-1.5, 1.5),
                    "vy": random.uniform(2.0, 5.0),
                    "size": random.randint(18, 35),
                    "life": 1.0,
                    "color": random.choice([(255, 140, 30), (255, 200, 60), (200, 200, 200), (140, 140, 140)])
                })

        # Update & draw smoke particles
        alive_particles = []
        for p in smoke_particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["size"] += 1.2
            p["life"] -= 0.02
            if p["life"] > 0 and p["y"] < HEIGHT:
                alive_particles.append(p)
                c = p["color"]
                fade = p["life"]
                fc = (int(c[0] * fade), int(c[1] * fade), int(c[2] * fade))
                sz = int(p["size"])
                draw.ellipse([p["x"] - sz, p["y"] - sz, p["x"] + sz, p["y"] + sz], fill=fc)
        smoke_particles = alive_particles

        # Draw Launch Fire Plume
        if is_launched:
            flame_len = random.randint(140, 220)
            flame_w = random.randint(22, 34)
            draw.polygon([
                (missile_x - flame_w // 2, missile_y + 140),
                (missile_x + flame_w // 2, missile_y + 140),
                (missile_x, missile_y + 140 + flame_len)
            ], fill=(255, 230, 100))
            draw.polygon([
                (missile_x - flame_w // 4, missile_y + 140),
                (missile_x + flame_w // 4, missile_y + 140),
                (missile_x, missile_y + 140 + flame_len * 0.7)
            ], fill=(255, 255, 255))
            # Ground reflection glow
            draw.ellipse([missile_x - 300, HEIGHT - 380, missile_x + 300, HEIGHT - 300], fill=(70, 40, 10))

        # Draw Ballistic Missile Body
        mx = missile_x + shake_x
        my = missile_y + shake_y
        mw, mh = 36, 160
        # Missile Nose cone
        draw.polygon([(mx, my - 50), (mx - mw//2, my), (mx + mw//2, my)], fill=(220, 225, 235))
        # Missile Fuselage
        draw.rectangle([mx - mw//2, my, mx + mw//2, my + mh], fill=(210, 215, 225), outline=(120, 130, 145), width=2)
        # Tail fins
        draw.polygon([(mx - mw//2, my + mh - 25), (mx - mw - 15, my + mh + 15), (mx - mw//2, my + mh)], fill=(160, 50, 40))
        draw.polygon([(mx + mw//2, my + mh - 25), (mx + mw + 15, my + mh + 15), (mx + mw//2, my + mh)], fill=(160, 50, 40))

        # Launch TEL launcher platform silhouette on ground
        draw.rectangle([missile_x - 70, HEIGHT - 390, missile_x + 70, HEIGHT - 340], fill=(45, 55, 65))
        draw.ellipse([missile_x - 65, HEIGHT - 350, missile_x - 35, HEIGHT - 320], fill=(20, 25, 30))
        draw.ellipse([missile_x + 35, HEIGHT - 350, missile_x + 65, HEIGHT - 320], fill=(20, 25, 30))

        # HUD Overlay
        draw.rectangle([50, 90, WIDTH - 50, 220], fill=(12, 18, 30, 220), outline=(255, 120, 30), width=2)
        draw.text((80, 105), "BALLISTIC MISSILE LAUNCH SEQUENCE", fill=(255, 140, 40), font=FONT_TITLE)
        stage = "STANDBY" if f < 30 else ("BOOSTER IGNITION" if f < 100 else "ASCENT TO APOGEE")
        draw.text((80, 160), f"STATUS: {stage}  |  CLASS: MEDIUM-RANGE BALLISTIC MISSILE", fill=(255, 220, 180), font=FONT_MONO)

        # Velocity & Alt Counter
        alt_km = max(0.0, (HEIGHT - 480 - missile_y) * 0.12)
        mach = max(0.0, speed * 0.28)
        draw.rectangle([WIDTH - 420, HEIGHT - 220, WIDTH - 60, HEIGHT - 80], fill=(12, 18, 30), outline=(0, 220, 255), width=2)
        draw.text((WIDTH - 400, HEIGHT - 205), f"ALT:  {alt_km:05.1f} KM", fill=(0, 240, 255), font=FONT_MONO)
        draw.text((WIDTH - 400, HEIGHT - 165), f"VEL:  MACH {mach:04.1f}", fill=(255, 200, 50), font=FONT_MONO)
        draw.text((WIDTH - 400, HEIGHT - 125), "STAGE 1 ACCELERATION", fill=(180, 210, 240), font=FONT_MONO_SM)

        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    proc.wait()
    print("Clip 2 done.")

# -------------------------------------------------------------
# CLIP 3: Fighter Jet Air Strike & Precision Bombing
# -------------------------------------------------------------
def render_clip3_airstrike():
    out_file = os.path.join(OUTPUT_DIR, "clip3_airstrike_bombing.mp4")
    print("Rendering Clip 3: Airstrike & Bombing...")
    proc = start_ffmpeg_pipe(out_file)

    for f in range(TOTAL_FRAMES):
        # Split: First 4.5 seconds (0-135) = Jet flying and releasing weapons
        # Next 5.5 seconds (135-300) = FLIR Targeting Pod view of bomb impact
        img = Image.new("RGB", (WIDTH, HEIGHT), (12, 16, 26))
        draw = ImageDraw.Draw(img)

        if f < 135:
            # Sky perspective with high altitude clouds
            for cy_offset in [300, 700, 1100, 1500]:
                draw.ellipse([-200, cy_offset, WIDTH + 200, cy_offset + 250], fill=(22, 32, 50))

            # Jet movement: banks from top-left to center-right
            jet_progress = f / 135.0
            jx = int(-150 + (WIDTH + 300) * jet_progress)
            jy = int(350 + 200 * math.sin(jet_progress * math.pi))

            # Fighter Jet Silhouette (F-15 / Strike Aircraft)
            draw.polygon([
                (jx + 120, jy),          # Nose
                (jx - 40, jy - 35),      # Wing port
                (jx - 140, jy - 160),    # Wing tip port
                (jx - 100, jy - 20),
                (jx - 160, jy - 70),     # Twin tail
                (jx - 180, jy),          # Engine exhaust
                (jx - 160, jy + 70),
                (jx - 100, jy + 20),
                (jx - 140, jy + 160),    # Wing tip starboard
                (jx - 40, jy + 35)
            ], fill=(160, 175, 195), outline=(90, 105, 125), width=2)

            # Glowing Afterburners
            draw.ellipse([jx - 230, jy - 25, jx - 170, jy + 25], fill=(255, 180, 50))
            draw.ellipse([jx - 210, jy - 12, jx - 175, jy + 12], fill=(255, 255, 255))

            # Weapons Release animation (Frames 60 to 135)
            if f > 60:
                bomb_prog = (f - 60) / 75.0
                bx = jx - 60 + int(bomb_prog * 180)
                by = jy + 60 + int((bomb_prog ** 1.8) * 800)
                # Guided Bomb / Missile
                draw.polygon([(bx + 30, by), (bx - 20, by - 12), (bx - 20, by + 12)], fill=(220, 60, 40))
                draw.line([(bx - 20, by), (bx - 80, by - 20)], fill=(255, 200, 50), width=3)  # Motor trail

            # HUD
            draw.rectangle([50, 100, WIDTH - 50, 220], fill=(16, 24, 38, 220), outline=(255, 80, 80), width=2)
            draw.text((80, 115), "COALITION AIR STRIKE MISSION", fill=(255, 90, 90), font=FONT_TITLE)
            draw.text((80, 170), "OPERATION: PRECISION DEPOT INTERDICTION // F-15S STRIKE", fill=(200, 225, 250), font=FONT_MONO)

        else:
            # FLIR Targeting Pod View (Thermal Night Vision Monochrome Green)
            img = Image.new("RGB", (WIDTH, HEIGHT), (4, 24, 14))
            draw = ImageDraw.Draw(img)

            # Ground Compound Target
            draw.rectangle([WIDTH//2 - 160, HEIGHT//2 - 40, WIDTH//2 + 160, HEIGHT//2 + 180], fill=(12, 45, 28), outline=(40, 160, 90), width=3)
            draw.rectangle([WIDTH//2 - 80, HEIGHT//2 + 20, WIDTH//2 + 80, HEIGHT//2 + 140], fill=(20, 65, 40))

            # FLIR Crosshair Overlay
            cx, cy = WIDTH // 2, HEIGHT // 2 + 60
            draw.line([(cx - 140, cy), (cx - 40, cy)], fill=(0, 255, 120), width=2)
            draw.line([(cx + 40, cy), (cx + 140, cy)], fill=(0, 255, 120), width=2)
            draw.line([(cx, cy - 140), (cx, cy - 40)], fill=(0, 255, 120), width=2)
            draw.line([(cx, cy + 40), (cx, cy + 140)], fill=(0, 255, 120), width=2)
            draw.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], outline=(0, 255, 120), width=1)

            # Impact Explosion at Frame 170
            if f >= 170:
                exp_frame = f - 170
                exp_r = min(360, int(15 * (exp_frame ** 0.85)))
                # Expanding fireball layers
                draw.ellipse([cx - exp_r, cy - exp_r, cx + exp_r, cy + exp_r], fill=(255, 255, 200))
                if exp_r > 40:
                    draw.ellipse([cx - exp_r*0.8, cy - exp_r*0.8, cx + exp_r*0.8, cy + exp_r*0.8], fill=(255, 190, 50))
                if exp_r > 90:
                    draw.ellipse([cx - exp_r*0.6, cy - exp_r*0.6, cx + exp_r*0.6, cy + exp_r*0.6], fill=(255, 80, 20))
                # Flying debris sparks
                for di in range(16):
                    d_angle = di * (360 / 16) + di * 5
                    d_rad = math.radians(d_angle)
                    dist = exp_r * 1.1 + di * 8
                    dx = cx + int(dist * math.cos(d_rad))
                    dy = cy + int(dist * math.sin(d_rad))
                    draw.ellipse([dx - 6, dy - 6, dx + 6, dy + 6], fill=(255, 240, 100))

            # FLIR HUD Telemetry
            draw.text((80, 120), "TGP FLIR OPTICAL TRACKING", fill=(0, 255, 120), font=FONT_TITLE)
            draw.text((80, 180), "LASER DESIGNATOR: CODE 1688 [ARMED]", fill=(0, 220, 100), font=FONT_MONO)
            status_text = "COUNTDOWN: IMPACT T-01 SEC" if f < 170 else "IMPACT CONFIRMED // TARGET DESTROYED"
            stat_color = (255, 200, 50) if f < 170 else (255, 60, 60)
            draw.rectangle([60, HEIGHT - 220, WIDTH - 60, HEIGHT - 100], fill=(8, 32, 18), outline=(0, 255, 120), width=2)
            draw.text((90, HEIGHT - 195), status_text, fill=stat_color, font=FONT_TITLE)
            draw.text((90, HEIGHT - 145), "BOMB DAMAGE ASSESSMENT: 100% NEUTRALIZATION", fill=(0, 220, 100), font=FONT_MONO_SM)

        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    proc.wait()
    print("Clip 3 done.")

# -------------------------------------------------------------
# CLIP 4: Patriot Air Defense Interception Animation
# -------------------------------------------------------------
def render_clip4_patriot():
    out_file = os.path.join(OUTPUT_DIR, "clip4_patriot_interception.mp4")
    print("Rendering Clip 4: Patriot Air Defense Interception...")
    proc = start_ffmpeg_pipe(out_file)

    for f in range(TOTAL_FRAMES):
        img = Image.new("RGB", (WIDTH, HEIGHT), (10, 14, 24))
        draw = ImageDraw.Draw(img)

        # High Altitude Stratosphere Background (Graduated deep dark blue to black)
        for y in range(0, HEIGHT, 80):
            r = int(10 + (y / HEIGHT) * 20)
            g = int(14 + (y / HEIGHT) * 25)
            b = int(30 + (y / HEIGHT) * 40)
            draw.rectangle([0, y, WIDTH, y + 80], fill=(r, g, b))

        # Target: Incoming ballistic threat descending from top right
        threat_prog = f / 220.0
        threat_x = int(WIDTH * 0.85 - threat_prog * 420)
        threat_y = int(180 + threat_prog * 750)

        # Interceptor: Patriot PAC-3 launching from bottom left towards threat
        inter_prog = max(0.0, (f - 20) / 190.0)
        inter_x = int(160 + inter_prog * 460)
        inter_y = int(HEIGHT - 280 - (inter_prog ** 1.3) * 1150)

        # Draw Patriot Interceptor Trail
        if f > 20:
            draw.line([(160, HEIGHT - 280), (inter_x, inter_y)], fill=(200, 220, 255), width=5)
            draw.line([(160, HEIGHT - 280), (inter_x, inter_y)], fill=(255, 200, 80), width=2)
            # Patriot Rocket Body
            draw.ellipse([inter_x - 10, inter_y - 10, inter_x + 10, inter_y + 10], fill=(255, 255, 255))

        # Draw Incoming Threat
        if f < 210:
            draw.line([(WIDTH * 0.85, 180), (threat_x, threat_y)], fill=(255, 60, 60), width=4)
            draw.ellipse([threat_x - 12, threat_y - 12, threat_x + 12, threat_y + 12], fill=(255, 80, 80))
            draw.text((threat_x + 18, threat_y - 18), "INCOMING WARHEAD", fill=(255, 100, 100), font=FONT_MONO_SM)

        # Kinetic Intercept Collision at Frame 210
        if f >= 210:
            col_frame = f - 210
            col_r = min(400, int(22 * (col_frame ** 0.9)))
            cx, cy = threat_x, threat_y
            draw.ellipse([cx - col_r, cy - col_r, cx + col_r, cy + col_r], fill=(255, 255, 255))
            if col_r > 30:
                draw.ellipse([cx - col_r*0.8, cy - col_r*0.8, cx + col_r*0.8, cy + col_r*0.8], fill=(0, 240, 255))
            if col_r > 80:
                draw.ellipse([cx - col_r*0.5, cy - col_r*0.5, cx + col_r*0.5, cy + col_r*0.5], fill=(255, 150, 40))

        # HUD Air Defense Display
        draw.rectangle([50, 80, WIDTH - 50, 200], fill=(12, 20, 34, 220), outline=(0, 220, 255), width=2)
        draw.text((80, 95), "PATRIOT PAC-3 AIR DEFENSE ENGAGEMENT", fill=(0, 230, 255), font=FONT_TITLE)
        draw.text((80, 150), "RADAR: AN/MPQ-65 PHASED ARRAY // TRACK-VIA-MISSILE", fill=(180, 220, 250), font=FONT_MONO_SM)

        # Intercept Status
        status_msg = "TRACKING & CLOSING: MACH 4.8" if f < 210 else "KINETIC KILL CONFIRMED // TARGET DESTROYED"
        stat_border = (0, 220, 255) if f < 210 else (80, 255, 120)
        draw.rectangle([60, HEIGHT - 220, WIDTH - 60, HEIGHT - 100], fill=(12, 20, 34), outline=stat_border, width=2)
        draw.text((90, HEIGHT - 195), status_msg, fill=stat_border, font=FONT_TITLE)
        draw.text((90, HEIGHT - 145), "DEFENSE BATTERY: ROYAL SAUDI AIR DEFENSE FORCES", fill=(180, 210, 240), font=FONT_MONO)

        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    proc.wait()
    print("Clip 4 done.")

# -------------------------------------------------------------
# CLIP 5: Suicide Drone Seeker / FLIR HUD Targeting
# -------------------------------------------------------------
def render_clip5_drone():
    out_file = os.path.join(OUTPUT_DIR, "clip5_drone_targeting.mp4")
    print("Rendering Clip 5: Drone Targeting HUD...")
    proc = start_ffmpeg_pipe(out_file)

    for f in range(TOTAL_FRAMES):
        # Tactical FLIR Seeker Optic (Green monochrome)
        img = Image.new("RGB", (WIDTH, HEIGHT), (6, 26, 18))
        draw = ImageDraw.Draw(img)

        # Rugged Desert Terrain / Mountain Ridges rushing toward camera
        terrain_offset = (f * 18) % 180
        for i in range(8):
            ty = 600 + i * 160 + terrain_offset
            draw.line([(0, ty), (WIDTH, ty)], fill=(12, 50, 32), width=2)
            draw.line([(WIDTH//2 - (ty - 500)*0.7, ty), (WIDTH//2 + (ty - 500)*0.7, ty)], fill=(18, 70, 44), width=2)

        # Oil Refinery / Infrastructure Target getting closer
        scale = 0.5 + (f / TOTAL_FRAMES) * 1.8
        tx, ty = WIDTH // 2, HEIGHT // 2 + int(f * 1.2)
        tw = int(140 * scale)
        th = int(90 * scale)
        draw.rectangle([tx - tw, ty - th, tx + tw, ty + th], fill=(20, 75, 48), outline=(0, 255, 140), width=2)
        draw.ellipse([tx - tw//2, ty - th - 30, tx - tw//2 + 40, ty - th + 10], fill=(30, 90, 60))  # Tank dome
        draw.ellipse([tx + tw//2 - 40, ty - th - 30, tx + tw//2, ty - th + 10], fill=(30, 90, 60))

        # Dynamic AI Target Bounding Box
        box_pad = int(25 * scale)
        draw.rectangle([tx - tw - box_pad, ty - th - box_pad, tx + tw + box_pad, ty + th + box_pad], outline=(255, 60, 60), width=3)
        draw.text((tx - tw - box_pad, ty - th - box_pad - 40), "OPTICAL LOCK: ENERGY INFRASTRUCTURE", fill=(255, 90, 90), font=FONT_MONO_SM)

        # Seeker Crosshairs
        cx, cy = WIDTH // 2, HEIGHT // 2
        draw.line([(cx - 160, cy), (cx - 40, cy)], fill=(0, 255, 140), width=2)
        draw.line([(cx + 40, cy), (cx + 160, cy)], fill=(0, 255, 140), width=2)
        draw.line([(cx, cy - 160), (cx, cy - 40)], fill=(0, 255, 140), width=2)
        draw.line([(cx, cy + 40), (cx, cy + 160)], fill=(0, 255, 140), width=2)

        # Top Drone Telemetry
        draw.rectangle([50, 90, WIDTH - 50, 210], fill=(8, 34, 22, 220), outline=(0, 255, 140), width=2)
        draw.text((80, 105), "UNMANNED LOITERING MUNITION (SAMAD-3)", fill=(0, 255, 140), font=FONT_TITLE)
        draw.text((80, 160), "PROPULSION: TWO-STROKE PUSHER ENGINE  |  AUTONOMOUS GPS/OPTICAL", fill=(160, 240, 190), font=FONT_MONO_SM)

        # Altitude & Range Countdown
        dist_m = max(20, int(2800 - (f / TOTAL_FRAMES) * 2760))
        draw.rectangle([60, HEIGHT - 220, WIDTH - 60, HEIGHT - 100], fill=(8, 34, 22), outline=(255, 80, 80), width=2)
        draw.text((90, HEIGHT - 195), f"RANGE TO IMPACT: {dist_m:04d} METERS", fill=(255, 80, 80), font=FONT_TITLE)
        draw.text((90, HEIGHT - 145), "TERMINAL ATTACK DIVE ANGLE: -35° // SPEED: 220 KM/H", fill=(180, 240, 200), font=FONT_MONO)

        # Final 10 frames = static interference
        if f >= TOTAL_FRAMES - 10:
            noise = np.random.randint(0, 255, (HEIGHT, WIDTH, 3), dtype=np.uint8)
            img = Image.fromarray(noise)

        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    proc.wait()
    print("Clip 5 done.")

# -------------------------------------------------------------
# CLIP 6: Red Sea Maritime Warship & VLS Missile Launch
# -------------------------------------------------------------
def render_clip6_naval():
    out_file = os.path.join(OUTPUT_DIR, "clip6_redsea_naval.mp4")
    print("Rendering Clip 6: Red Sea Naval & VLS Launch...")
    proc = start_ffmpeg_pipe(out_file)

    for f in range(TOTAL_FRAMES):
        img = Image.new("RGB", (WIDTH, HEIGHT), (8, 16, 28))
        draw = ImageDraw.Draw(img)

        # Ocean water layers (moving waves)
        wave_offset = f * 4
        for y in range(HEIGHT - 600, HEIGHT, 40):
            w_color = (12, 35 + (y - HEIGHT + 600)//20, 60 + (y - HEIGHT + 600)//15)
            pts = [(x, y + int(12 * math.sin((x + wave_offset) * 0.03))) for x in range(0, WIDTH + 40, 40)]
            pts += [(WIDTH, HEIGHT), (0, HEIGHT)]
            draw.polygon(pts, fill=w_color)

        # Guided Missile Destroyer Silhouette
        sx = WIDTH // 2 - 180
        sy = HEIGHT - 520
        # Ship hull
        hull_pts = [(sx - 280, sy + 30), (sx - 180, sy + 110), (sx + 340, sy + 110), (sx + 420, sy + 30)]
        draw.polygon(hull_pts, fill=(45, 60, 78))
        # Superstructure & Mast
        draw.rectangle([sx - 100, sy - 80, sx + 160, sy + 30], fill=(55, 72, 92))
        draw.rectangle([sx - 30, sy - 180, sx + 50, sy - 80], fill=(65, 84, 108))
        # Radar mast
        draw.line([(sx + 10, sy - 180), (sx + 10, sy - 260)], fill=(120, 140, 165), width=3)
        draw.line([(sx - 30, sy - 230), (sx + 50, sy - 230)], fill=(120, 140, 165), width=2)

        # VLS Missile Launch from Foredeck (Missile shoots straight up)
        # Launch occurs from frame 40 onwards
        vx = sx + 240
        vy = sy + 30
        if f > 40:
            m_prog = (f - 40) / (TOTAL_FRAMES - 40)
            my = vy - int((m_prog ** 1.4) * 1100)
            mx = vx - int(m_prog * 80)
            # Exhaust smoke column
            draw.line([(vx, vy), (mx, my + 50)], fill=(220, 220, 220), width=18)
            draw.line([(vx, vy), (mx, my + 50)], fill=(255, 180, 50), width=6)
            # Missile
            draw.rectangle([mx - 8, my, mx + 8, my + 55], fill=(255, 255, 255))
            # Rocket plume
            draw.polygon([(mx - 10, my + 55), (mx + 10, my + 55), (mx, my + 130)], fill=(255, 200, 50))

        # Tactical Map Radar Window (Inset)
        draw.rectangle([WIDTH - 380, 120, WIDTH - 60, 440], fill=(12, 22, 38, 230), outline=(0, 220, 255), width=2)
        draw.text((WIDTH - 360, 135), "RED SEA MARITIME RADAR", fill=(0, 240, 255), font=FONT_MONO_SM)
        # Radar circle
        rcx, rcy = WIDTH - 220, 290
        draw.ellipse([rcx - 110, rcy - 110, rcx + 110, rcy + 110], outline=(20, 80, 130), width=1)
        draw.text((rcx - 70, rcy - 10), "BAB EL-MANDEB", fill=(100, 180, 255), font=FONT_MONO_SM)
        # Sweep line
        r_angle = (f * 6) % 360
        r_rad = math.radians(r_angle)
        draw.line([(rcx, rcy), (rcx + int(110 * math.cos(r_rad)), rcy + int(110 * math.sin(r_rad)))], fill=(0, 255, 200), width=2)

        # Top HUD Banner
        draw.rectangle([50, 120, WIDTH - 420, 240], fill=(12, 22, 38, 230), outline=(0, 220, 255), width=2)
        draw.text((80, 135), "RED SEA MARITIME AIR DEFENSE", fill=(0, 230, 255), font=FONT_TITLE)
        draw.text((80, 190), "OPERATION PROSPERITY GUARDIAN // VLS INTERCEPT", fill=(180, 220, 250), font=FONT_MONO_SM)

        # Bottom Status
        draw.rectangle([60, HEIGHT - 220, WIDTH - 60, HEIGHT - 100], fill=(12, 22, 38), outline=(0, 220, 255), width=2)
        draw.text((90, HEIGHT - 195), "VERTICAL LAUNCH SYSTEM (VLS) ACTIVE", fill=(0, 240, 255), font=FONT_TITLE)
        draw.text((90, HEIGHT - 145), "DEFENDING COMMERCIAL CONVOYS FROM ANTI-SHIP MISSILES", fill=(180, 210, 240), font=FONT_MONO)

        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    proc.wait()
    print("Clip 6 done.")

if __name__ == "__main__":
    render_clip1_radar()
    render_clip2_missile()
    render_clip3_airstrike()
    render_clip4_patriot()
    render_clip5_drone()
    render_clip6_naval()
    print("\nALL 6 MILITARY ANIMATION CLIPS GENERATED SUCCESSFULLY!")
