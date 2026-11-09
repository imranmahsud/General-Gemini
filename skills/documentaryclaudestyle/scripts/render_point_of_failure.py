import os
import sys
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE_DIR = Path(r"c:\Users\Imran\Downloads\CHeck\upper-swat-canal-doc")
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
BLENDER_DIR = ASSETS_DIR / "blender"
AUDIO_DIR = ASSETS_DIR / "audio"
OUT_DIR = BASE_DIR / "docclaude"
OUT_DIR.mkdir(parents=True, exist_ok=True)

WIDTH = 1920
HEIGHT = 1080
FPS = 30
TOTAL_DURATION = 68.0
TOTAL_FRAMES = int(TOTAL_DURATION * FPS)  # 2040

# Fonts
try:
    font_mono_lg = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 46)
    font_mono_md = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 20)
    font_mono_sm = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 15)
    font_sans_lg = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 32)
    font_sans_md = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 22)
    font_sans_sm = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 15)
except Exception:
    font_mono_lg = font_mono_md = font_mono_sm = font_sans_lg = font_sans_md = font_sans_sm = ImageFont.load_default()

# 1. Precompute RGBA Vignette & Grain Overlay (Zero-copy in per-frame loop)
def build_overlay():
    y, x = np.ogrid[:HEIGHT, :WIDTH]
    cx, cy = WIDTH / 2, HEIGHT / 2
    max_dist = math.sqrt(cx**2 + cy**2)
    dist = np.sqrt((x - cx)**2 + (y - cy)**2)
    vig_alpha = np.clip(160 * ((dist / max_dist)**2.2), 0, 180).astype(np.uint8)
    
    np.random.seed(42)
    grain = np.random.normal(0, 5, (HEIGHT, WIDTH)).astype(np.int16)
    
    # Combined black vignette with alpha
    overlay_arr = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    overlay_arr[:, :, 3] = vig_alpha
    return Image.fromarray(overlay_arr, "RGBA")

VIGNETTE_OVERLAY = build_overlay()

ACTS = [
    {
        "id": 1,
        "title": "THE MALAKAND BARRIER",
        "subtitle": "1903 IMPASSE // SWAT BASIN TO PARCHED MARDAN PLAINS",
        "epoch": "1903 // IMPASSE",
        "image": str(IMAGES_DIR / "01_swat_river.jpg"),
        "focus_box": (1050, 380, 1680, 800),
        "words": ["In", "1903,", "recurrent", "famine", "struck", "the", "arid", "Mardan", "plains", "while", "Swat", "River", "floods", "were", "barred", "by", "the", "Malakand", "granite", "ridge."],
        "dur": 13.6
    },
    {
        "id": 2,
        "title": "THE BENTON SUBTERRANEAN BORE",
        "subtitle": "11,235-FT HORSESHOE TUNNEL DRIVEN THROUGH SOLID GRANITE",
        "epoch": "1910 // EXCAVATION",
        "image": str(BLENDER_DIR / "benton_tunnel_cutaway_3d.png"),
        "focus_box": (420, 480, 1500, 780),
        "words": ["Imperial", "engineer", "Sir", "John", "Benton", "drove", "an", "eleven-thousand-foot", "horseshoe", "tunnel", "through", "solid", "quartz-diorite", "granite", "with", "sub-inch", "precision."],
        "dur": 13.6
    },
    {
        "id": 3,
        "title": "AMANDARA WEIR & SILT REJECTION",
        "subtitle": "700-FT MASONRY DIVERSION WEIR & BED-LOAD SCOURING SLUICES",
        "epoch": "1912 // DIVERSION",
        "image": str(IMAGES_DIR / "03_amandara_overflow.jpg"),
        "focus_box": (580, 360, 1480, 760),
        "words": ["At", "Batkhela,", "Amandara", "Headworks", "harnessed", "the", "river.", "A", "seven-hundred-foot", "weir", "and", "scouring", "sluices", "rejected", "coarse", "Himalayan", "boulders."],
        "dur": 13.6
    },
    {
        "id": 4,
        "title": "DARGAI CASCADE & MACHAI ARTERY",
        "subtitle": "300-FT POWER CHUTES & 80-MILE MAIN IRRIGATION ARTERY",
        "epoch": "1914 // COMMISSION",
        "image": str(IMAGES_DIR / "05_malakand_portal.jpg"),
        "focus_box": (740, 320, 1340, 840),
        "words": ["Emerging", "at", "Dargai,", "the", "flow", "plunged", "three", "hundred", "feet", "down", "power", "chutes", "before", "feeding", "the", "eighty-mile", "Machai", "Branch."],
        "dur": 13.6
    },
    {
        "id": 5,
        "title": "CENTURY OF UNBROKEN SERVICE",
        "subtitle": "112 YEARS OF WATER SECURITY // ZERO STRUCTURAL FAILURES",
        "epoch": "1914 – 2026 AD",
        "image": str(IMAGES_DIR / "02_amandara_headworks.jpg"),
        "focus_box": (500, 380, 1420, 760),
        "words": ["Commissioned", "in", "1914,", "the", "Upper", "Swat", "Canal", "has", "delivered", "unbroken", "service", "for", "over", "a", "century,", "transforming", "the", "entire", "region."],
        "dur": 13.6
    }
]

def build_procedural_soundtrack():
    print("=== Step 1: Synthesizing Procedural Point-of-Failure Drone & Heartbeat Bed ===")
    master_soundtrack = OUT_DIR / "docclaude_master_audio.mp3"
    if master_soundtrack.exists():
        print(f"  [Reusing existing] {master_soundtrack}")
        return master_soundtrack

    sr = 48000
    total_samples = int(TOTAL_DURATION * sr)
    t = np.linspace(0, TOTAL_DURATION, total_samples, endpoint=False)
    
    # 42 Hz Sub-bass Heartbeat
    beat_period = 1.4
    phase = (t % beat_period) / beat_period
    beat_env = np.exp(-5.0 * phase) * (phase < 0.35)
    heartbeat = 0.40 * np.sin(2 * np.pi * 42.0 * t) * beat_env
    
    # Minor Drone (A1=55Hz)
    chorus_lfo = 1.0 + 0.003 * np.sin(2 * np.pi * 0.15 * t)
    f_root = 55.0 * chorus_lfo
    drone = (
        0.18 * np.sin(2 * np.pi * f_root * t) +
        0.14 * np.sin(2 * np.pi * (f_root * 1.2) * t) +
        0.12 * np.sin(2 * np.pi * (f_root * 1.5) * t)
    )
    
    audio_env = np.ones(total_samples, dtype=np.float32)
    audio_env[:int(1.5 * sr)] = np.linspace(0, 1, int(1.5 * sr))
    audio_env[-int(2.5 * sr):] = np.linspace(1, 0, int(2.5 * sr))
    
    bed = np.clip(np.tanh((heartbeat + drone) * audio_env * 1.2), -0.95, 0.95)
    
    import wave
    bed_wav = OUT_DIR / "drone_bed.wav"
    with wave.open(str(bed_wav), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes((bed * 32767).astype(np.int16).tobytes())
        
    cmd_master = [
        "ffmpeg", "-y",
        "-i", str(AUDIO_DIR / "master_audio_doc001.mp3"),
        "-i", str(bed_wav),
        "-filter_complex",
        "[0:a]volume=1.0[vocal];"
        "[1:a]volume=0.55[ambient];"
        "[vocal][ambient]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
        "[mixed]loudnorm=I=-14:TP=-1.5:LRA=11[outa]",
        "-map", "[outa]", "-c:a", "libmp3lame", "-b:a", "192k",
        "-map_metadata", "-1", "-fflags", "+bitexact",
        str(master_soundtrack)
    ]
    subprocess.run(cmd_master, check=True)
    if bed_wav.exists():
        bed_wav.unlink()
    return master_soundtrack

def render_video(master_audio_path):
    print("\n=== Step 2: High-Performance Subpixel Float Rendering (Pure Video Pipe) ===")
    raw_video = OUT_DIR / "docclaude_raw.mp4"
    final_video = OUT_DIR / "upper_swat_canal_docclaude.mp4"
    
    # Pure video pipe avoids any audio interleaving deadlock
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "17",
        "-preset", "veryfast",
        str(raw_video)
    ]
    
    pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    
    # Pre-scale images to 2304x1296 (1.2x headroom for smooth float cropping)
    TARGET_W, TARGET_H = 2304, 1296
    loaded_imgs = {}
    for act in ACTS:
        im = Image.open(act["image"]).convert("RGBA")
        im = im.resize((TARGET_W, TARGET_H), Image.Resampling.BILINEAR)
        loaded_imgs[act["id"]] = im
        
    frames_per_act = int(TOTAL_FRAMES / len(ACTS))
    frame_idx = 0
    
    for act_idx, act in enumerate(ACTS):
        img_src = loaded_imgs[act["id"]]
        iw, ih = TARGET_W, TARGET_H
        focus = act["focus_box"]
        words = act["words"]
        n_words = len(words)
        
        for f in range(frames_per_act):
            t_act = f / FPS
            prog = f / frames_per_act
            sprog = 0.5 - 0.5 * math.cos(prog * math.pi)
            
            # Viewport calculation
            scale = 1.0 + 0.08 * sprog
            vw = iw / scale
            vh = ih / scale
            
            target_cx = (focus[0] + focus[2]) / 2.0 / WIDTH * iw
            target_cy = (focus[1] + focus[3]) / 2.0 / HEIGHT * ih
            cx = (iw / 2.0) * (1.0 - 0.20 * sprog) + target_cx * (0.20 * sprog)
            cy = (ih / 2.0) * (1.0 - 0.20 * sprog) + target_cy * (0.20 * sprog)
            
            x0 = max(0, min(iw - vw, cx - vw / 2.0))
            y0 = max(0, min(ih - vh, cy - vh / 2.0))
            
            # Fast float crop and resize
            crop_frame = img_src.crop((x0, y0, x0 + vw, y0 + vh)).resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)
            
            # Composite Vignette
            crop_frame.alpha_composite(VIGNETTE_OVERLAY)
            
            draw = ImageDraw.Draw(crop_frame)
            
            # Progressive Red Spotlight Highlight Tracing
            if t_act >= 1.5:
                trace_prog = min(1.0, (t_act - 1.5) / 1.5)
                fx1, fy1, fx2, fy2 = focus
                w_box = fx2 - fx1
                h_box = fy2 - fy1
                perim = 2 * (w_box + h_box)
                drawn_len = perim * trace_prog
                
                red_color = (239, 68, 68, 240)
                if drawn_len > 0:
                    draw.line([(fx1, fy1), (fx1 + min(w_box, drawn_len), fy1)], fill=red_color, width=3)
                if drawn_len > w_box:
                    draw.line([(fx2, fy1), (fx2, fy1 + min(h_box, drawn_len - w_box))], fill=red_color, width=3)
                if drawn_len > w_box + h_box:
                    draw.line([(fx2, fy2), (fx2 - min(w_box, drawn_len - w_box - h_box), fy2)], fill=red_color, width=3)
                if drawn_len > 2 * w_box + h_box:
                    draw.line([(fx1, fy2), (fx1, fy2 - min(h_box, drawn_len - 2 * w_box - h_box))], fill=red_color, width=3)
                    
                # Corner reticles
                tick = 14
                draw.line([(fx1 - 8, fy1), (fx1 + tick, fy1)], fill=(255, 255, 255, 200), width=2)
                draw.line([(fx1, fy1 - 8), (fx1, fy1 + tick)], fill=(255, 255, 255, 200), width=2)
                draw.line([(fx2 + 8, fy2), (fx2 - tick, fy2)], fill=(255, 255, 255, 200), width=2)
                draw.line([(fx2, fy2 + 8), (fx2 - tick, fy2)], fill=(255, 255, 255, 200), width=2)
                
            # Top-Left Chapter Banner
            draw.rounded_rectangle([(60, 48), (620, 134)], radius=8, fill=(10, 16, 26, 230), outline=(56, 189, 248, 70), width=1)
            draw.rectangle([(60, 48), (66, 134)], fill=(239, 68, 68, 255))
            draw.text((82, 60), f"PART {act['id']} · {act['title']}", fill=(248, 250, 252), font=font_sans_lg)
            draw.text((82, 98), act['subtitle'], fill=(148, 163, 184), font=font_mono_sm)
            
            # Top-Right Timeline Clock Widget
            draw.rounded_rectangle([(1480, 48), (1860, 134)], radius=8, fill=(10, 16, 26, 230), outline=(245, 158, 11, 70), width=1)
            draw.rectangle([(1480, 128), (1860, 134)], fill=(245, 158, 11, 255))
            draw.text((1504, 58), act['epoch'], fill=(255, 184, 28), font=font_mono_lg)
            draw.text((1504, 102), "MALAKAND HYDRAULIC PASS // KPK", fill=(148, 163, 184), font=font_mono_sm)
            
            # Top-Center GPS Coordinate Readout
            draw.rounded_rectangle([(770, 48), (1150, 88)], radius=4, fill=(10, 16, 26, 210), outline=(56, 189, 248, 50), width=1)
            draw.text((788, 58), "● INVERT // 34.618° N, 71.932° E // 2,140 FT", fill=(56, 189, 248), font=font_mono_sm)
            
            # Bottom Center Karaoke Amber Subtitles Bubble
            active_word_idx = int((t_act / 11.2) * n_words) if t_act <= 11.2 else n_words
            sub_y = 960
            draw.rounded_rectangle([(120, sub_y - 12), (1800, sub_y + 44)], radius=8, fill=(8, 12, 20, 230), outline=(56, 189, 248, 50), width=1)
            
            cur_x = 140
            for w_i, word in enumerate(words):
                is_active = (w_i <= active_word_idx)
                color = (255, 184, 28, 255) if is_active else (226, 232, 240, 200)
                draw.text((cur_x, sub_y), word, fill=color, font=font_sans_md)
                cur_x += len(word) * 13 + 10
                if cur_x > 1760:
                    break
                    
            # Final Fade Out (66.4s - 68.0s)
            global_t = (act_idx * frames_per_act + f) / FPS
            if global_t >= 66.4:
                fade_alpha = int(255 * min(1.0, (global_t - 66.4) / 1.6))
                draw.rectangle([(0, 0), (WIDTH, HEIGHT)], fill=(0, 0, 0, fade_alpha))
                
            # Write raw RGB bytes to pipe
            pipe.stdin.write(crop_frame.convert("RGB").tobytes())
            frame_idx += 1
            if frame_idx % 240 == 0:
                print(f"  Progress: {frame_idx}/{TOTAL_FRAMES} frames ({(frame_idx/TOTAL_FRAMES)*100:.1f}%)")
                
    pipe.stdin.close()
    pipe.wait()
    print(f"[OK] Raw video rendered to {raw_video}")
    
    print("\n=== Step 3: Muxing with Master Audio & Scrubbing Metadata ===")
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", str(raw_video),
        "-i", str(master_audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-map_metadata", "-1",
        "-fflags", "+bitexact",
        "-flags:v", "+bitexact",
        "-flags:a", "+bitexact",
        str(final_video)
    ]
    subprocess.run(cmd_mux, check=True)
    if raw_video.exists():
        raw_video.unlink()
    print(f"[SUCCESS] documentaryclaude video complete: {final_video}")

if __name__ == "__main__":
    audio_path = build_procedural_soundtrack()
    render_video(audio_path)
