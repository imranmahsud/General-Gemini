"""Downloads authentic imagery and compiles true-crime broadcast cards for the Skardu Quadruple Murder investigation."""

import os
import httpx
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

OUTPUT_DIR = "D:/AI-Folders/MoneyPrinterTurbo/materials/skardu_crime"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "CrimeInvestigativeDoc/1.0 (imran@example.com)"
}

CARDS = [
    {
        "filename": "01_skardu_valley.jpg",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/9f/Shangrila_resort_skardu.jpg/1280px-Shangrila_resort_skardu.jpg?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail",
        "category": "SPECIAL CRIME REPORT",
        "title": "HORRIFIC QUADRUPLE MURDER IN SKARDU",
        "subtitle": "Madina Colony Home Targeted in Gilgit-Baltistan",
        "tag_color": (220, 40, 40)
    },
    {
        "filename": "02_crime_scene.jpg",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/04/Barricade_tape_in_Japan_April_07_2019_05-15PM.jpeg/1280px-Barricade_tape_in_Japan_April_07_2019_05-15PM.jpeg?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail",
        "category": "FORENSIC INVESTIGATION",
        "title": "PARENTS & TWO TODDLERS SLAIN",
        "subtitle": "Muhammad Aslam, Hania, Son Mehdi (4) & Daughter Zahra (2)",
        "tag_color": (230, 80, 30)
    },
    {
        "filename": "03_map_motive.jpg",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/85/Gilgit-Baltistan_in_Pakistan_%28de-facto_%2B_wo_Glacier%29_%28claims_hatched%29.svg/1280px-Gilgit-Baltistan_in_Pakistan_%28de-facto_%2B_wo_Glacier%29_%28claims_hatched%29.svg.png?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail",
        "category": "THE ROOT MOTIVE",
        "title": "6-YEAR LOVE MARRIAGE & THREATS",
        "subtitle": "Couple Fled Karachi to Skardu to Escape Vengeful Relatives",
        "tag_color": (210, 160, 20)
    },
    {
        "filename": "04_police_arrest.jpg",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1a/Person_handcuffed_behind_back.jpg/1280px-Person_handcuffed_behind_back.jpg?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail",
        "category": "POLICE MANHUNT",
        "title": "UNCLE & ACCOMPLICE NABBED IN KURRAM",
        "subtitle": "Skardu Police Track Fleeing Suspect 'Rajab' Across KP Border",
        "tag_color": (30, 160, 220)
    },
    {
        "filename": "05_legal_justice.jpg",
        "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b2/CourtGavel.JPG/1280px-CourtGavel.JPG?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail",
        "category": "LEGAL PROCEEDINGS",
        "title": "5 ACCUSED NOMINATED IN FORMAL FIR",
        "subtitle": "Victim's Brother Khadim Hussain Demands Capital Justice",
        "tag_color": (160, 40, 200)
    }
]

FONT_DIR = "C:/Windows/Fonts"
try:
    FONT_TITLE = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 44)
    FONT_SUB = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 28)
    FONT_TAG = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 24)
    FONT_HEADER = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 28)
except Exception:
    FONT_TITLE = ImageFont.load_default()
    FONT_SUB = ImageFont.load_default()
    FONT_TAG = ImageFont.load_default()
    FONT_HEADER = ImageFont.load_default()

def process_card(card):
    raw_path = os.path.join(OUTPUT_DIR, "raw_" + card["filename"])
    final_path = os.path.join(OUTPUT_DIR, card["filename"])

    if not os.path.exists(raw_path):
        print(f"Downloading: {card['category']}...")
        r = httpx.get(card["url"], headers=HEADERS, timeout=20.0, follow_redirects=True)
        if r.status_code == 200:
            with open(raw_path, "wb") as f:
                f.write(r.content)
        else:
            raise RuntimeError(f"Failed to download {card['url']}, status {r.status_code}")

    img = Image.open(raw_path).convert("RGB")
    
    # Cinematic grade: slightly higher contrast and moody lighting
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)

    target_w, target_h = 1080, 1920
    orig_w, orig_h = img.size
    scale = max(target_w / orig_w, target_h / orig_h)
    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    img = img.crop((left, top, left + target_w, top + target_h))

    # Dark moody vignettes
    overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    d_ov = ImageDraw.Draw(overlay)

    # Top gradient
    for y in range(420):
        alpha = int(230 * (1.0 - y / 420.0) ** 1.3)
        d_ov.line([(0, y), (target_w, y)], fill=(8, 12, 20, alpha))

    # Bottom gradient
    for y in range(target_h - 520, target_h):
        ratio = (y - (target_h - 520)) / 520.0
        alpha = int(245 * (ratio ** 1.2))
        d_ov.line([(0, y), (target_w, y)], fill=(6, 8, 14, alpha))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Top Accent Bar
    tag_color = card["tag_color"]
    draw.rectangle([0, 0, target_w, 14], fill=tag_color)
    draw.text((80, 120), "CRIME WIRE // INVESTIGATIVE DOSSIER", fill=(255, 255, 255), font=FONT_HEADER)
    draw.line([(80, 165), (580, 165)], fill=tag_color, width=3)

    # Category Badge
    badge_text = f"  {card['category']}  "
    bbox = draw.textbbox((80, 200), badge_text, font=FONT_TAG)
    draw.rounded_rectangle([bbox[0]-4, bbox[1]-4, bbox[2]+4, bbox[3]+4], radius=6, fill=tag_color)
    draw.text((80, 200), badge_text, fill=(255, 255, 255), font=FONT_TAG)

    # Bottom Typography
    draw.text((80, target_h - 340), card["title"], fill=(255, 255, 255), font=FONT_TITLE)
    draw.text((80, target_h - 280), card["subtitle"], fill=(200, 215, 230), font=FONT_SUB)
    draw.line([(80, target_h - 230), (target_w - 80, target_h - 230)], fill=(70, 85, 110), width=2)
    draw.text((80, target_h - 190), "CASE FILE: SKARDU MADINA COLONY HOMICIDE // GILGIT-BALTISTAN", fill=(140, 160, 180), font=FONT_TAG)

    img.save(final_path, quality=95)
    print(f"Created card: {final_path}")
    return final_path

if __name__ == "__main__":
    for c in CARDS:
        process_card(c)
    print("\nALL 5 CRIME STORY BROADCAST CARDS GENERATED!")
