---
name: deepseek
description: Query DeepSeek models (DeepSeek-V3 `deepseek-chat` and DeepSeek-R1 `deepseek-reasoner`) directly from Antigravity for reasoning, coding, and general tasks using your configured API key.
---

# DeepSeek Integration for Antigravity

This skill allows Antigravity to query the official DeepSeek API directly using the user's API key.

## Available Models
- **`deepseek-chat`** (DeepSeek-V3): Fast, high-accuracy conversational and general coding model.
- **`deepseek-reasoner`** (DeepSeek-R1): Deep reasoning model that produces chain-of-thought traces for complex engineering, math, logic, and architecture.

## Direct Python Invocation Helper
When running a query, execute the local runner script at `C:\Users\Imran\.gemini\deepseek-mcp\query_deepseek.py`:

```bash
python C:\Users\Imran\.gemini\deepseek-mcp\query_deepseek.py --model deepseek-chat --prompt "Your prompt here"
```

For DeepSeek-R1 reasoning:
```bash
python C:\Users\Imran\.gemini\deepseek-mcp\query_deepseek.py --model deepseek-reasoner --prompt "Your reasoning task here"
```

## MCP Tools
When the `deepseek` MCP server is active in the session, Antigravity also has direct access to:
- `deepseek:ask_deepseek`
- `deepseek:deepseek_r1_reason`
- `deepseek:deepseek_code_review`
- `deepseek:list_deepseek_models`
