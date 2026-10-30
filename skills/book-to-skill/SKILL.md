---
name: book-to-skill
description: Compiles technical books, architectural guides, and manuals (PDF, TXT, MD) into modular on-demand AI skills with SKILL.md, patterns.md, anti-patterns.md, and chapter modules. Use whenever the user wants to ingest a book or reference document into an executable agent skill.
---

# Book-to-Skill Compiler

Turns technical books and long-form engineering guides into structured, token-efficient agent skills. Instead of loading 400 pages into LLM context, it decomposes the book into on-demand chapter modules, key patterns, anti-patterns, and cheatsheets.

## Quick Command
To compile any book file into a new agent skill:
```powershell
python "C:\Users\Imran\.gemini\config\skills\book-to-skill\scripts\book_to_skill.py" --input "<path-to-book-file>" --name "<skill-slug>" --title "<Book Title>"
```

## Structure Created
```
<skill-name>/
├── SKILL.md           # Core philosophy, directives, and triggers
├── patterns.md        # Architecture blueprints and idioms
├── anti-patterns.md   # Smells and anti-patterns to avoid
├── cheatsheet.md      # Fast-lookup rules table
└── chapters/          # On-demand ~2k token chapter modules
```
