---
name: audiblez
description: Local AI audiobook generator skill using audiblez and Kokoro-82M neural TTS. Converts EPUB, PDF, and MOBI e-books into chapterized M4B/MP3 audiobooks with natural human voices offline, replacing Audible and ElevenLabs subscriptions.
---

# Audiblez Local Audiobook Generator Skill

This skill provides native, offline AI audiobook compilation from digital documents, textbooks, and technical manuals using `audiblez` and the high-speed **Kokoro-82M** neural text-to-speech engine.

---

## 1. CLI Commands

### 1.1 Generate Audiobook from EPUB / Document
```bash
# Basic generation with default voice
audiblez book.epub

# Specify high-quality neural voice (e.g. af_bella, af_sarah, am_adam, am_michael)
audiblez book.epub -v af_bella

# Adjust narration playback speed (e.g. 1.1x speed)
audiblez book.epub -v af_sarah -s 1.1

# Output as single merged M4B audiobook file with embedded chapter markers
audiblez book.epub -o output_audiobook.m4b
```

### 1.2 Voice Selection & Preview
```bash
# List all available neural voices
audiblez --list-voices
```

Available Kokoro neural voice profiles:
- `af_bella`, `af_sarah`, `af_nicole`, `af_sky` (American Female)
- `am_adam`, `am_michael`, `am_george` (American Male)
- `bf_emma`, `bf_isabella` (British Female)
- `bm_george`, `bm_lewis` (British Male)

---

## 2. Converting Technical Engineering PDFs & Manuals

Audiblez processes `.epub` natively. To convert civil engineering specifications, manuals, or research papers from PDF to EPUB for Audiblez:

```python
import pypdf
from ebooklib import epub

def pdf_to_epub_simple(pdf_path: str, epub_path: str, title: str = "Audiobook Document"):
    reader = pypdf.PdfReader(pdf_path)
    book = epub.EpubBook()
    book.set_identifier("id_local_doc_01")
    book.set_title(title)
    book.set_language("en")
    
    full_text = ""
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            full_text += f"\n\n<h2>Page {i+1}</h2>\n<p>{text}</p>"
            
    c1 = epub.EpubHtml(title="Full Document", file_name="doc.xhtml", lang="en")
    c1.content = full_text
    book.add_item(c1)
    book.toc = (epub.Link("doc.xhtml", "Document", "doc"),)
    book.spine = ["nav", c1]
    epub.write_epub(epub_path, book)
    print(f"Generated EPUB for Audiblez: {epub_path}")

if __name__ == "__main__":
    pdf_to_epub_simple("manual.pdf", "manual.epub")
```

After converting, run:
```bash
audiblez manual.epub -v am_adam -o manual.m4b
```

---

## 3. Key Benefits

1. **No Subscription**: Completely free and open-source alternative to Audible ($15/mo) and ElevenLabs.
2. **Offline & Private**: Documents and voices are synthesized on the local CPU or GPU.
3. **M4B Bookmarks**: Produced M4B files are compatible with standard audiobook players (Apple Books, Smart AudioBook Player, VLC) with chapters and resume positions.
