import sys
import os
import json
import urllib.request
import argparse

OLLAMA_BASE = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

def list_models():
    url = f"{OLLAMA_BASE}/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=10) as res:
            data = json.loads(res.read().decode('utf-8'))
            return [m['name'] for m in data.get('models', [])]
    except Exception as e:
        print(f"Error connecting to Ollama at {OLLAMA_BASE}: {e}", file=sys.stderr)
        return []

def ask(prompt, model="qwen3.5:4b", stream=True, system=None, temperature=0.7):
    url = f"{OLLAMA_BASE}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream,
        "options": {
            "temperature": temperature
        }
    }
    if system:
        payload["system"] = system

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as res:
            if stream:
                for line in res:
                    chunk = json.loads(line.decode('utf-8'))
                    text = chunk.get("response", "")
                    if text:
                        sys.stdout.write(text)
                        sys.stdout.flush()
                    if chunk.get("done", False):
                        sys.stdout.write("\n")
                        break
            else:
                data = json.loads(res.read().decode('utf-8'))
                print(data.get("response", ""))
    except Exception as e:
        print(f"Error querying Ollama: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Query local Ollama models directly from Antigravity")
    parser.add_argument("prompt", nargs="?", help="Prompt to send to local model")
    parser.add_argument("--model", "-m", default="qwen3.5:4b", help="Model name (default: qwen3.5:4b)")
    parser.add_argument("--list", "-l", action="store_true", help="List installed models")
    parser.add_argument("--system", "-s", help="System prompt")
    parser.add_argument("--no-stream", action="store_true", help="Disable streaming output")

    args = parser.parse_args()

    if args.list:
        models = list_models()
        print("Installed Ollama Models:")
        for m in models:
            print(f" - {m}")
        return

    if not args.prompt:
        # Read from stdin if piped
        if not sys.stdin.isatty():
            args.prompt = sys.stdin.read().strip()
        else:
            parser.print_help()
            return

    ask(args.prompt, model=args.model, stream=not args.no_stream, system=args.system)

if __name__ == "__main__":
    main()
