import argparse
import json
import sys

def format_timeline_prompt(title, duration_sec, style, segments):
    lines = [
        f"{duration_sec}-second timeline prompt — \"{title}\"",
        f"Style: {style}",
        ""
    ]
    for seg in segments:
        ts = seg.get("time", "0:00-0:02")
        heading = seg.get("title", "Scene")
        lines.append(f"{ts} — {heading}")
        lines.append(f"Camera: {seg.get('camera', '')}")
        lines.append(f"Action: {seg.get('action', '')}")
        lines.append(f"Expressions: {seg.get('expressions', '')}")
        if "dialogue" in seg and seg["dialogue"]:
            lines.append(f"Dialogue: {seg['dialogue']}")
        if "sound" in seg and seg["sound"]:
            lines.append(f"Sound: {seg['sound']}")
        lines.append("")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Generate 5-parameter timeline prompt")
    parser.add_argument("--json_file", required=True, help="Path to JSON file containing timeline segments")
    args = parser.parse_args()
    
    with open(args.json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    title = data.get("title", "Animation Scene")
    duration = data.get("duration_sec", 10)
    style = data.get("style", "Bright, hand-drawn comic animation with bold black outlines")
    segments = data.get("segments", [])
    
    formatted = format_timeline_prompt(title, duration, style, segments)
    print(formatted)

if __name__ == "__main__":
    main()
