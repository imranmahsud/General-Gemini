import argparse
import json
import sys

def build_character_sheet_prompt(name, role, description, style, clothing, palette, lighting):
    prompt = (
        f"Character prompt — {name} ({role})\n\n"
        f"Create an original, full-body character design for {description}, using a {style} style. "
        f"His/Her posture should feel grounded with clear silhouette readability. "
        f"Dress the character in {clothing}. "
        f"Use bold, clean line work and clear graphic shapes. "
        f"Color palette: {palette}. Lighting: {lighting}.\n\n"
        f"Character reference sheet composition: clean neutral background, full-body front view, "
        f"three-quarter view, profile side view, plus small close-up of face and hands. "
        f"Keep the exact same face, clothing, build, colours, and proportions across every view. "
        f"No text, labels, logos, watermarks, or extra characters."
    )
    return prompt

def main():
    parser = argparse.ArgumentParser(description="Generate character reference sheet prompt")
    parser.add_argument("--name", required=True, help="Character name")
    parser.add_argument("--role", default="Protagonist", help="Character role")
    parser.add_argument("--description", required=True, help="Physical traits, build, age, expression")
    parser.add_argument("--style", default="cinematic painterly 2D cartoon", help="Visual art style")
    parser.add_argument("--clothing", required=True, help="Outfit details and wear/distress")
    parser.add_argument("--palette", default="muted tones, deep earth shades, warm skin tones", help="Color palette")
    parser.add_argument("--lighting", default="subtle amber key light casting soft directional shadows", help="Lighting setup")
    
    args = parser.parse_args()
    prompt = build_character_sheet_prompt(
        name=args.name,
        role=args.role,
        description=args.description,
        style=args.style,
        clothing=args.clothing,
        palette=args.palette,
        lighting=args.lighting
    )
    print(prompt)

if __name__ == "__main__":
    main()
