"""Downloads real-world, public-domain military photographs and prepares cinematic 1080x1920 vertical broadcast cards."""

import os
import httpx
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

OUTPUT_DIR = "D:/AI-Folders/MoneyPrinterTurbo/materials/houthi_saudi_real"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "GeopoliticsDefenseDoc/1.0 (https://github.com/imranmahsud/General-Gemini; contact@local.net)"
}

IMAGE_SOURCES = [
    {
        "filename": "01_border_map.jpg",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/84/Yemen_relief_location_map.jpg/1280px-Yemen_relief_location_map.jpg?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail",
        "badge": "TACTICAL GEOGRAPHY",
        "title": "YEMEN - SAUDI ARABIA BORDER CORRIDOR",
        "subtitle": "1,800 KM BORDER CORRIDOR & RED SEA CHOKEPOINT"
    },
    {
        "filename": "02_ballistic_missile.jpg",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/7f/Scud-launcher-England1.jpg/1280px-Scud-launcher-England1.jpg?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail",
        "badge": "BALLISTIC MISSILE CAPABILITY",
        "title": "MOBILE MISSILE TEL LAUNCH PLATFORM",
        "subtitle": "BURKAN & QUDS CLASS SOLID/LIQUID ROCKET SYSTEMS"
    },
    {
        "filename": "03_strike_fighter.jpg",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/43/F-15EX_Eagle_II.jpg/1280px-F-15EX_Eagle_II.jpg?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail",
        "badge": "AIR INTERDICTION",
        "title": "COALITION AIR STRIKE OPERATIONS",
        "subtitle": "STANDOFF PRECISION-GUIDED MUNITIONS & DEEP RECON"
    },
    {
        "filename": "04_patriot_defense.jpg",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/2f/U-s-service-members-stand-by-a-patriot-missile-battery-in-gaziantep-turkey.jpg/1280px-U-s-service-members-stand-by-a-patriot-missile-battery-in-gaziantep-turkey.jpg?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail",
        "badge": "AIR & MISSILE DEFENSE",
        "title": "MIM-104 PATRIOT PAC-3 BATTERY",
        "subtitle": "POINT DEFENSE INTERCEPTION OF SUPERSONIC WARHEADS"
    },
    {
        "filename": "05_loitering_drone.jpg",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/41/IAI_Harop_PAS_2013_01.jpg/1280px-IAI_Harop_PAS_2013_01.jpg?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail",
        "badge": "ASYMMETRIC AERIAL THREAT",
        "title": "DELTA-WING LOITERING MUNITION",
        "subtitle": "LOW-ALTITUDE TERRAIN-FOLLOWING OPTICAL DRONES"
    },
    {
        "filename": "06_naval_destroyer.jpg",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1d/USS_Lake_Erie_%28CG-70%29_SM-3_start.jpg/1280px-USS_Lake_Erie_%28CG-70%29_SM-3_start.jpg?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail",
        "badge": "RED SEA MARITIME SECURITY",
        "title": "GUIDED MISSILE VLS AIR DEFENSE",
        "subtitle": "INTERCEPTING ANTI-SHIP MISSILES IN BAB EL-MANDEB"
    }
]

FONT_DIR = "C:/Windows/Fonts"
try:
    FONT_TITLE = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 46)
    FONT_SUB = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 30)
    FONT_TAG = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 26)
    FONT_HEADER = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 28)
except Exception:
    FONT_TITLE = ImageFont.load_default()
    FONT_SUB = ImageFont.load_default()
    FONT_TAG = ImageFont.load_default()
    FONT_HEADER = ImageFont.load_default()

def process_item(item):
    raw_path = os.path.join(OUTPUT_DIR, "raw_" + item["filename"])
    final_path = os.path.join(OUTPUT_DIR, item["filename"])

    # Download if not present
    if not os.path.exists(raw_path):
        print(f"Downloading: {item['badge']}...")
        r = httpx.get(item["url"], headers=HEADERS, timeout=20.0, follow_redirects=True)
        if r.status_code == 200:
            with open(raw_path, "wb") as f:
                f.write(r.content)
        else:
            raise RuntimeError(f"Failed to download {item['url']}, status {r.status_code}")

    # Open image
    img = Image.open(raw_path).convert("RGB")
    
    # Enhance contrast and slight color boost for cinematic look
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.15)
    color_enhancer = ImageEnhance.Color(img)
    img = color_enhancer.enhance(1.1)

    # Crop/Scale to 1080x1920 (center crop preserving aspect ratio)
    target_w, target_h = 1080, 1920
    orig_w, orig_h = img.size
    scale = max(target_w / orig_w, target_h / orig_h)
    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    img = img.crop((left, top, left + target_w, top + target_h))

    # Add dark cinematic vignette gradients on top and bottom
    overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    d_ov = ImageDraw.Draw(overlay)

    # Top gradient (height: 400px)
    for y in range(400):
        alpha = int(220 * (1.0 - y / 400.0) ** 1.3)
        d_ov.line([(0, y), (target_w, y)], fill=(10, 15, 25, alpha))

    # Bottom gradient (height: 500px)
    for y in range(target_h - 500, target_h):
        ratio = (y - (target_h - 500)) / 500.0
        alpha = int(240 * (ratio ** 1.2))
        d_ov.line([(0, y), (target_w, y)], fill=(8, 12, 20, alpha))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Top Header Bar
    draw.rectangle([0, 0, target_w, 14], fill=(220, 50, 40))
    draw.text((80, 120), "STRATEGIC FRONTLINE // REGIONAL BRIEFING", fill=(255, 255, 255), font=FONT_HEADER)
    draw.line([(80, 165), (550, 165)], fill=(220, 50, 40), width=3)

    # Badge Tag
    badge_text = f"  {item['badge']}  "
    bbox = draw.textbbox((80, 200), badge_text, font=FONT_TAG)
    draw.rounded_rectangle([bbox[0]-4, bbox[1]-4, bbox[2]+4, bbox[3]+4], radius=6, fill=(220, 50, 40))
    draw.text((80, 200), badge_text, fill=(255, 255, 255), font=FONT_TAG)

    # Bottom Title and Subtitle Box
    draw.text((80, target_h - 320), item["title"], fill=(255, 255, 255), font=FONT_TITLE)
    draw.text((80, target_h - 260), item["subtitle"], fill=(190, 210, 230), font=FONT_SUB)
    draw.line([(80, target_h - 210), (target_w - 80, target_h - 210)], fill=(60, 80, 110), width=2)
    draw.text((80, target_h - 180), "SPECIAL REPORT: YEMEN - SAUDI COMBAT OPERATIONS", fill=(140, 160, 180), font=FONT_TAG)

    img.save(final_path, quality=95)
    print(f"Created broadcast card: {final_path}")
    return final_path

if __name__ == "__main__":
    paths = [process_item(item) for item in IMAGE_SOURCES]
    print("\nALL 6 BROADCAST CARDS GENERATED SUCCESSFULLY!")
