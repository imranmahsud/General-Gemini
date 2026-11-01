---
name: ollama-local
description: >-
  Interact with local offline Ollama models (e.g. qwen3.5:4b, llama3, deepseek-r1) running on localhost:11434.
  Use when the user asks to query a local model, execute offline inference, test local models, or preserve 100% data privacy without using cloud API credits.
---

# Ollama Local Model Integration

Route queries, code evaluations, and local reasoning directly to your offline Ollama daemon (`http://localhost:11434`).

## Active Model
- **Default Model:** `qwen3.5:4b` (4.2B Q4_K_M, with reasoning/thinking support)

## Usage

### 1. List Available Models
```bash
python scripts/ask_ollama.py --list
```

### 2. Query Local Model (Streaming)
```bash
python scripts/ask_ollama.py "Your prompt or code question here" --model qwen3.5:4b
```

### 3. Pipe Code or File into Local Model
```bash
python scripts/ask_ollama.py "Review this function for edge cases:" < path/to/file.py
```

### 4. MCP Server Integration
The local Ollama server is also registered in `~/.gemini/settings.json` under `ollama` (`ollama-mcp`), exposing native MCP tools to the agent environment.
