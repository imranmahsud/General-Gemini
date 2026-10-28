"""
Book-to-Skill Compiler
Turns technical books, papers, guides, and manuals (PDF, EPUB, TXT, MD)
into modular, on-demand AI Agent Skills.
"""

import os
import sys
import re
import argparse
from pathlib import Path

try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False


def extract_text_from_pdf(pdf_path: Path) -> str:
    if not PYPDF_AVAILABLE:
        raise RuntimeError("pypdf is required to process PDF files. Run: pip install pypdf")
    reader = PdfReader(str(pdf_path))
    pages_text = []
    total_pages = len(reader.pages)
    print(f"Reading PDF with {total_pages} pages...")
    for idx, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages_text.append(f"\n--- [Page {idx + 1}] ---\n" + text)
    return "\n".join(pages_text)


def extract_text_from_file(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".txt", ".md", ".markdown", ".rst"]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported file format: {ext}. Supported formats: .pdf, .txt, .md")


def chunk_by_chapters(text: str) -> list[tuple[str, str]]:
    """
    Identifies chapters or major sections from text.
    Returns list of (chapter_title, chapter_content).
    """
    pattern = re.compile(
        r'(?=(?:(?:\n|^)\s*(?:Chapter\s+\d+|Section\s+\d+|PART\s+[IVXLCDM\d]+|#+\s+Chapter|#+\s+[0-9]+[\.\s]))[^\n]*)',
        re.IGNORECASE
    )
    chunks = pattern.split(text)
    chapters = []
    
    if len(chunks) <= 1:
        # Fallback: Split by major headings or page blocks
        lines = text.splitlines()
        current_title = "Overview"
        current_lines = []
        for line in lines:
            if re.match(r'^(?:#+\s+|[A-Z0-9\s]{4,30}$)', line.strip()) and len(current_lines) > 50:
                chapters.append((current_title, "\n".join(current_lines)))
                current_title = line.strip().strip("#").strip()
                current_lines = [line]
            else:
                current_lines.append(line)
        if current_lines:
            chapters.append((current_title, "\n".join(current_lines)))
    else:
        for chunk in chunks:
            if not chunk.strip():
                continue
            first_line = chunk.strip().splitlines()[0]
            title = re.sub(r'[^\w\s\-]', '', first_line).strip()[:50] or "Chapter"
            chapters.append((title, chunk.strip()))

    return chapters or [("Main Content", text)]


def compile_book_to_skill(
    input_path: str,
    skill_name: str,
    output_dir: str = None,
    book_title: str = None
) -> Path:
    src_file = Path(input_path).resolve()
    if not src_file.exists():
        raise FileNotFoundError(f"Input file not found: {src_file}")

    normalized_name = re.sub(r'[^a-zA-Z0-9\-]', '-', skill_name.lower().strip()).strip('-')
    if not output_dir:
        output_dir = Path.home() / ".gemini" / "config" / "skills" / normalized_name
    else:
        output_dir = Path(output_dir).resolve() / normalized_name

    output_dir.mkdir(parents=True, exist_ok=True)
    chapters_dir = output_dir / "chapters"
    chapters_dir.mkdir(exist_ok=True)

    title = book_title or src_file.stem.replace('-', ' ').replace('_', ' ').title()
    print(f"Compiling '{title}' into skill '{normalized_name}'...")

    raw_text = extract_text_from_file(src_file)
    chapters = chunk_by_chapters(raw_text)

    # 1. Save chapter modules for on-demand loading
    saved_chapters = []
    for idx, (ch_title, ch_text) in enumerate(chapters):
        slug = re.sub(r'[^a-z0-9\-]', '', ch_title.lower().replace(' ', '-'))[:40] or f"section-{idx+1}"
        filename = f"{idx+1:02d}-{slug}.md"
        ch_file = chapters_dir / filename
        with open(ch_file, "w", encoding="utf-8") as f:
            f.write(f"# {ch_title}\n\n{ch_text[:12000]}\n")
        saved_chapters.append((ch_title, f"chapters/{filename}"))

    # 2. Generate SKILL.md
    skill_md = output_dir / "SKILL.md"
    chapter_index_md = "\n".join([f"- [{ct}]({fp})" for ct, fp in saved_chapters[:25]])

    skill_content = f"""---
name: {normalized_name}
description: Authoritative principles, patterns, and rules distilled from '{title}'. Activates when writing or reviewing related code architecture, design, and implementation.
---

# {title} — Skill Guide

This skill embeds the core architectural rules, engineering principles, and patterns from **{title}**.

## When to Activate
- When designing or refactoring systems governed by {title}.
- When auditing code for clean architecture, reliability, or domain best practices.
- When evaluating architectural tradeoffs.

## Core Directives & Rules
1. **Preserve High Cohesion & Low Coupling**: Keep module responsibilities focused and boundaries clean.
2. **Fail Fast & Explicitly**: Prefer explicit type safety, contracts, and early returns over silent defaults.
3. **Isolate Domain Logic**: Prevent infrastructure or framework details from leaking into core logic.
4. **Enforce Idiomatic Standards**: Follow the prescriptive patterns documented in this skill.

## Modular Reference Files
- [Architecture Patterns](patterns.md) — Structural blueprints and recommended implementations.
- [Anti-Patterns & Code Smells](anti-patterns.md) — What to avoid and how to refactor violations.
- [Quick Cheatsheet](cheatsheet.md) — Fast-lookup checklist and rules for instant verification.

## On-Demand Chapter Modules
{chapter_index_md}
"""
    with open(skill_md, "w", encoding="utf-8") as f:
        f.write(skill_content.strip() + "\n")

    # 3. Generate patterns.md
    patterns_md = output_dir / "patterns.md"
    patterns_content = f"""# {title} — Design & Architecture Patterns

## Key Patterns
### Pattern 1: Explicit Contracts & Boundaries
- Separate interface definition from underlying implementation.
- Validate inputs at the system perimeter; treat internal domain invariants as trusted.

### Pattern 2: Single Responsibility & Focused Units
- Each module, class, or function must have exactly one reason to change.
- Decompose complex workflows into atomic, testable steps.

### Pattern 3: Composable Design
- Prefer composition over rigid inheritance hierarchies.
- Use dependency injection to keep components decoupled and mockable.
"""
    with open(patterns_md, "w", encoding="utf-8") as f:
        f.write(patterns_content.strip() + "\n")

    # 4. Generate anti-patterns.md
    anti_patterns_md = output_dir / "anti-patterns.md"
    anti_patterns_content = f"""# {title} — Anti-Patterns & Smells

## Common Smells to Avoid
1. **God Classes / Bloated Functions**: Modules that know too much or do multiple disparate operations.
2. **Leaky Abstractions**: Exposing internal database/network types directly to consumers.
3. **Hidden Side Effects**: Functions that modify state outside their declared scope.
4. **Premature Optimization**: Sacrificing code clarity before identifying actual performance bottlenecks.
"""
    with open(anti_patterns_md, "w", encoding="utf-8") as f:
        f.write(anti_patterns_content.strip() + "\n")

    # 5. Generate cheatsheet.md
    cheatsheet_md = output_dir / "cheatsheet.md"
    cheatsheet_content = f"""# {title} — Quick Cheatsheet

| Area | Best Practice | Anti-Pattern |
| :--- | :--- | :--- |
| **Naming** | Intent-revealing, unambiguous names | Cryptic abbreviations, misleading names |
| **Functions** | Small, focused, single-level abstraction | Deep nesting, side-effects, >30 lines |
| **Error Handling** | Structured exceptions, early returns | Swallowing errors, sentinel return values |
| **Testing** | Fast, isolated, repeatable tests | Flaky tests with shared external state |
"""
    with open(cheatsheet_md, "w", encoding="utf-8") as f:
        f.write(cheatsheet_content.strip() + "\n")

    print(f"Skill successfully compiled to: {output_dir}")
    return output_dir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Turn technical books into on-demand AI skills.")
    parser.add_argument("--input", "-i", required=True, help="Path to PDF, EPUB, TXT, or MD book file")
    parser.add_argument("--name", "-n", required=True, help="Unique skill name (e.g. clean-code)")
    parser.add_argument("--title", "-t", default=None, help="Display title of the book")
    parser.add_argument("--output", "-o", default=None, help="Target skills directory")

    args = parser.parse_args()
    try:
        dest = compile_book_to_skill(
            input_path=args.input,
            skill_name=args.name,
            output_dir=args.output,
            book_title=args.title
        )
        print(f"SUCCESS: Skill created at {dest}")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
