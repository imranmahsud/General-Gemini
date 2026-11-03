"""Generates an executive, professional Word document (.docx) detailing monetization strategies for automated Geopolitics & Defense video channels."""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOC_PATH = "D:/AI-Folders/MoneyPrinterTurbo/outputs/Geopolitics_Shorts_Monetization_Masterclass.docx"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin_name, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{margin_name}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_monetization_doc():
    doc = Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    COLOR_PRIMARY = RGBColor(24, 43, 73)      # Deep Navy
    COLOR_SECONDARY = RGBColor(180, 40, 30)   # Strategic Crimson
    COLOR_TEXT = RGBColor(40, 45, 55)        # Charcoal Body
    COLOR_MUTED = RGBColor(100, 110, 125)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(4)
    run_title = p_title.add_run("GEOPOLITICS & DEFENSE SHORT-FORM CHANNELS")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(24)
    run_sub = p_sub.add_run("Strategic Monetization Roadmap, Production Upgrades & Execution Blueprint")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(12)
    run_sub.font.color.rgb = COLOR_SECONDARY
    run_sub.font.bold = True

    # Callout Box: Executive Brief
    tbl_box = doc.add_table(rows=1, cols=1)
    tbl_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl_box.cell(0, 0)
    set_cell_background(c, "F0F4F8")
    set_cell_margins(c, top=160, bottom=160, left=220, right=220)
    p_box = c.paragraphs[0]
    p_box.paragraph_format.space_after = Pt(4)
    r_box_title = p_box.add_run("EXECUTIVE SUMMARY: THE HIGH-CPM DEFENSE NICHE\n")
    r_box_title.font.bold = True
    r_box_title.font.size = Pt(11)
    r_box_title.font.color.rgb = COLOR_PRIMARY
    r_box_body = p_box.add_run(
        "Geopolitics and modern military defense rank among the top 5 highest-paying informational niches on short-form platforms (YouTube Shorts, TikTok, and Instagram Reels). "
        "Average RPM (Revenue Per Mille) ranges between $0.12 and $0.45 per 1,000 Shorts views—up to 4x higher than comedy or lifestyle content. "
        "By replacing robotic speech with ultra-realistic neural human narration (Kokoro-82M) and swapping 2D drawings with real-world 4K military B-roll (DVIDS & Pexels), "
        "a single operator can build an autonomous multi-platform media asset generating $3,000 to $10,000+ per month."
    )
    r_box_body.font.size = Pt(10)
    r_box_body.font.color.rgb = COLOR_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Section 1: Revenue Architecture
    h1 = doc.add_paragraph()
    r_h1 = h1.add_run("1. Four Pillars of Channel Monetization")
    r_h1.font.name = "Arial"
    r_h1.font.size = Pt(15)
    r_h1.font.bold = True
    r_h1.font.color.rgb = COLOR_PRIMARY
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)

    # Pillar 1
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("Pillar A: Ad Revenue & Platform Creator Pools\n")
    r.font.bold = True
    r.font.color.rgb = COLOR_SECONDARY
    p.add_run(
        "• YouTube Shorts Revenue Share: Monetization unlocks at 1,000 subscribers and 10 million Shorts views in 90 days (or 4,000 watch hours on long-form). Geopolitics channels command an RPM of $0.15–$0.35.\n"
        "• TikTok Creator Rewards Program: Pays for qualified views on videos over 60 seconds (target: 62–75s). Typical payout is $0.40–$0.90 per 1,000 views in US/UK/EU audiences—significantly higher than sub-minute shorts.\n"
        "• Multi-Platform Re-purposing: Each finished render must be uploaded identically across YouTube Shorts, TikTok, Instagram Reels, and Facebook Reels. 1 video render = 4 platform income streams."
    )

    # Pillar 2
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("Pillar B: High-Ticket Gaming & Defense Tech Sponsorships\n")
    r.font.bold = True
    r.font.color.rgb = COLOR_SECONDARY
    p.add_run(
        "• Military Simulation Advertisers: Games like War Thunder, World of Warships, Conflict of Nations, and Hearts of Iron sponsor defense channels aggressively. "
        "Standard payout: $500 to $2,500 per sponsored Short integration (or $3 to $8 per confirmed player registration via your dedicated trackable link).\n"
        "• Hardware & Defense Tech Tools: Tactical gear brands, VPN providers (NordVPN/Surfshark - highly relevant to security-conscious geopolitical viewers), and audio gear brands pay monthly retainers."
    )

    # Pillar 3
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("Pillar C: High-Conversion Affiliate Arbitrage\n")
    r.font.bold = True
    r.font.color.rgb = COLOR_SECONDARY
    p.add_run(
        "• Audiobook Affiliates: Audible / Blinkist offer $5 to $10 per free-trial signup. In every video, pin a comment: 'Listen to the declassified account of this operation on Audible (free with trial link below)'.\n"
        "• Geopolitical Book Reviews: Amazon Associates links to authoritative military books (e.g. 'The Accidental Superpower' by Zeihan, 'Chip War' by Miller) generating 4.5% lifetime cart commissions."
    )

    # Pillar 4
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run("Pillar D: Premium Dossiers & Substack Memberships\n")
    r.font.bold = True
    r.font.color.rgb = COLOR_SECONDARY
    p.add_run(
        "• Converting Shorts Viewers to Recurring Subscribers: High-curiosity defense viewers readily convert to a $7/month Substack or Patreon newsletter for full battle maps, satellite imagery breakdowns, and source documents.\n"
        "• Conversion Benchmark: Converting just 500 loyal viewers from a 100,000-subscriber Shorts channel yields $3,500/month in predictable, platform-independent recurring revenue."
    )

    # Section 2: Production Upgrades (Fixing Robotic Sound & Cartoonish Visuals)
    h2 = doc.add_paragraph()
    r_h2 = h2.add_run("2. Production Upgrades: Achieving Broadcast-Grade Quality")
    r_h2.font.name = "Arial"
    r_h2.font.size = Pt(15)
    r_h2.font.bold = True
    r_h2.font.color.rgb = COLOR_PRIMARY
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(6)

    # Comparison Table
    tbl = doc.add_table(rows=3, cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Production Element", "Current Robotic / Cartoon Setup", "Recommended Broadcast Upgrade"]
    for i, title in enumerate(headers):
        cell = tbl.cell(0, i)
        set_cell_background(cell, "182B49")
        set_cell_margins(cell, 120, 120, 140, 140)
        p = cell.paragraphs[0]
        r = p.add_run(title)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    data = [
        ("Voice Narration", "Edge TTS (GuyNeural / ChristopherNeural)\n• Robotic inflection\n• Flat cadence & synthetic pauses", "Kokoro-82M Neural TTS (Free & Offline)\n• Human breath modeling & dynamic pitch\n• ElevenLabs-grade quality with zero API cost\n• Voices: 'am_adam', 'am_michael', 'bm_george'"),
        ("Visual Materials", "Procedural 2D Line Drawings\n• Cartoonish appearance\n• Low viewer retention", "Authentic 4K Military B-Roll & DVIDS Footage\n• Free DVIDS Public Domain US Military footage\n• Pexels/Pixabay stock video API integration\n• Real F-15/Typhoon strikes, carrier launches, PAC-3 tests")
    ]
    for row_idx, row_data in enumerate(data, start=1):
        bg = "FFFFFF" if row_idx % 2 == 1 else "F8FAFC"
        for col_idx, text in enumerate(row_data):
            cell = tbl.cell(row_idx, col_idx)
            set_cell_background(cell, bg)
            set_cell_margins(cell, 120, 120, 140, 140)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            r.font.color.rgb = COLOR_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Section 3: Free Resources & Implementation Blueprint
    h3 = doc.add_paragraph()
    r_h3 = h3.add_run("3. Free Internet Sources for Real Military Footage")
    r_h3.font.name = "Arial"
    r_h3.font.size = Pt(15)
    r_h3.font.bold = True
    r_h3.font.color.rgb = COLOR_PRIMARY
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(6)

    p_sources = doc.add_paragraph()
    p_sources.add_run(
        "1. DVIDS (Defense Visual Information Distribution Service - dvidshub.net):\n"
        "   • The #1 secret used by top documentary and defense creators. All media produced by the US Military (Air Force, Navy, Marines, Army) is 100% PUBLIC DOMAIN by US federal law (17 U.S.C. § 105).\n"
        "   • Provides broadcast-grade 1080p and 4K footage of real missile launches, F-15/F-35 live weapons tests, Aegis destroyer VLS launches, and radar operations—completely free without licensing fees.\n\n"
        "2. Pexels & Pixabay Free Video APIs:\n"
        "   • Free instant API keys (200 requests/hr free tier).\n"
        "   • Configure 'pexels_api_keys' in MoneyPrinterTurbo config.toml; the system will autonomously search and download matching real B-roll for every keyword in your script.\n\n"
        "3. Wikimedia Commons & Internet Archive:\n"
        "   • Thousands of declassified historical and contemporary defense operation clips and satellite passes, free under Creative Commons or Public Domain."
    )

    # Section 4: 90-Day Execution Roadmap
    h4 = doc.add_paragraph()
    r_h4 = h4.add_run("4. 90-Day Execution & Scaling Roadmap")
    r_h4.font.name = "Arial"
    r_h4.font.size = Pt(15)
    r_h4.font.bold = True
    r_h4.font.color.rgb = COLOR_PRIMARY
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(6)

    p_road = doc.add_paragraph()
    p_road.add_run(
        "• Days 1–14 (Channel Foundation):\n"
        "  - Launch YouTube channel ('Strategic Frontline' or 'Chokepoint Watch') and matching TikTok/IG accounts.\n"
        "  - Establish 3 content templates: (A) Chokepoint & Maritime Flashpoints, (B) Weapon System Deep Dives, (C) Tactical Border Conflicts.\n"
        "  - Generate initial 15-video backlog using MoneyPrinterTurbo.\n\n"
        "• Days 15–45 (Algorithmic Traction):\n"
        "  - Maintain strict upload cadence: 2 Shorts daily (12:00 PM and 6:00 PM UTC).\n"
        "  - Pin affiliate links on all high-performing videos.\n"
        "  - Target 62–70 second video duration to maximize TikTok Creator Rewards eligibility.\n\n"
        "• Days 46–90 (Monetization Activation & Scale):\n"
        "  - Qualify for YouTube Shorts Revenue Pool (10M views threshold) and TikTok Creator Rewards.\n"
        "  - Begin accepting gaming sponsorships (War Thunder / World of Warships) at $800–$1,500/integration.\n"
        "  - Launch Substack newsletter for long-form battle maps and tactical dossiers."
    )

    os.makedirs(os.path.dirname(DOC_PATH), exist_ok=True)
    doc.save(DOC_PATH)
    print(f"Document successfully created at: {DOC_PATH}")

if __name__ == "__main__":
    create_monetization_doc()
