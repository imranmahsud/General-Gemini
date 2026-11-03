"""OpenAI / ChatGPT MCP Server for Antigravity."""

import os
from typing import Optional
from mcp.server.fastmcp import FastMCP
import openai

mcp = FastMCP("chatgpt")

def _get_client() -> openai.OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is missing.")
    return openai.OpenAI(api_key=api_key)

@mcp.tool()
def ask_chatgpt(
    prompt: str,
    model: str = "gpt-4o",
    system_prompt: str = "You are an expert AI assistant.",
    temperature: float = 0.7,
    max_tokens: Optional[int] = 2048,
) -> str:
    """Send a query to OpenAI's ChatGPT models (e.g. gpt-4o, gpt-4o-mini, o1, o3-mini) and receive the completion."""
    client = _get_client()
    
    # Reasoner models (o1, o3) don't support custom temperature or max_tokens in the standard way
    is_reasoning_model = model.startswith("o1") or model.startswith("o3")
    
    messages = []
    if system_prompt and not is_reasoning_model:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    kwargs = {
        "model": model,
        "messages": messages,
    }
    if not is_reasoning_model:
        kwargs["temperature"] = temperature
        if max_tokens:
            kwargs["max_tokens"] = max_tokens

    response = client.chat.completions.create(**kwargs)
    choice = response.choices[0]
    return choice.message.content or ""

@mcp.tool()
def chatgpt_code_review(
    code: str,
    language: str = "auto",
    guidelines: str = "Check for bugs, security vulnerabilities, edge cases, and performance optimizations.",
    model: str = "gpt-4o",
) -> str:
    """Ask ChatGPT to perform a thorough code review against supplied source code."""
    prompt = f"Language: {language}\nGuidelines: {guidelines}\n\nCode to review:\n```\n{code}\n```"
    system_prompt = "You are a senior software architect and principal security engineer performing a rigorous code review."
    return ask_chatgpt(prompt=prompt, model=model, system_prompt=system_prompt)

@mcp.tool()
def list_chatgpt_models() -> str:
    """List available OpenAI models for this account."""
    client = _get_client()
    models = client.models.list()
    relevant = sorted([m.id for m in models if any(k in m.id for k in ("gpt-4", "gpt-3.5", "o1", "o3", "chatgpt"))])
    return "\n".join(relevant)

if __name__ == "__main__":
    mcp.run()
