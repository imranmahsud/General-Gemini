import os
import sys
import shutil
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new HyperFrames documentary in the 'documentary002' style."
    )
    parser.add_argument("name", help="Name or folder name of the documentary project")
    parser.add_argument("--dest", default=".", help="Destination root directory (default: current dir)")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parent.parent
    templates_dir = skill_root / "templates"
    sfx_dir = skill_root / "assets" / "audio"

    project_dir = Path(args.dest).resolve() / args.name
    if project_dir.exists():
        print(f"[Error] Target directory already exists: {project_dir}")
        sys.exit(1)

    print(f"Scaffolding documentary002 project in: {project_dir}")
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "assets" / "images").mkdir(parents=True, exist_ok=True)
    (project_dir / "assets" / "audio").mkdir(parents=True, exist_ok=True)

    # 1. Copy config files
    shutil.copy(templates_dir / "hyperframes.json", project_dir / "hyperframes.json")
    
    # Customize package.json with project name
    pkg_template = (templates_dir / "package.json").read_text(encoding="utf-8")
    pkg_custom = pkg_template.replace("teton-dam-documentary", args.name)
    (project_dir / "package.json").write_text(pkg_custom, encoding="utf-8")

    # 2. Copy index.html template
    shutil.copy(templates_dir / "template.html", project_dir / "index.html")

    # 3. Copy standard SFX suite
    sfx_files = ["whoosh-cinematic.mp3", "click-soft.mp3", "impact-bass-1.mp3", "riser.mp3", "chime.mp3"]
    for sfx in sfx_files:
        src = sfx_dir / sfx
        if src.exists():
            shutil.copy(src, project_dir / "assets" / "audio" / sfx)
            print(f"  + Bundled SFX: {sfx}")

    # 4. Generate starter audio builder script
    audio_builder_code = '''import subprocess
import sys
from pathlib import Path

# Voiceover scripts for the 5 Acts
ACTS = {
    "act1": "Executive dossier summary outlining the event, date, and magnitude.",
    "act2": "Engineering anatomy and structural vulnerabilities that initiated the failure.",
    "act3": "Chronology of the morning of the collapse, tracking early warnings to total failure.",
    "act4": "Official forensic commission verdict, determining primary design and operational errors.",
    "act5": "Investigation conclusion and permanent technical legacy for engineering standards."
}

def generate_voiceover(voice="en-US-ChristopherNeural"):
    audio_dir = Path("assets/audio")
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    for act, script in ACTS.items():
        out_file = audio_dir / f"{act}.mp3"
        print(f"Generating voiceover: {out_file.name}...")
        cmd = [
            "edge-tts",
            "--voice", voice,
            "--text", script,
            "--write-media", str(out_file)
        ]
        subprocess.run(cmd, check=True)

def mix_soundtrack():
    print("Mixing master soundtrack (narration + SFX + tail fade)...")
    cmd = [
        "ffmpeg", "-y",
        "-i", "assets/audio/act1.mp3",
        "-i", "assets/audio/act2.mp3",
        "-i", "assets/audio/act3.mp3",
        "-i", "assets/audio/act4.mp3",
        "-i", "assets/audio/act5.mp3",
        "-i", "assets/audio/whoosh-cinematic.mp3",
        "-i", "assets/audio/click-soft.mp3",
        "-i", "assets/audio/impact-bass-1.mp3",
        "-i", "assets/audio/riser.mp3",
        "-i", "assets/audio/chime.mp3",
        "-filter_complex",
        "[0:a]adelay=300|300,volume=1.0[n1];"
        "[1:a]adelay=14000|14000,volume=1.0[n2];"
        "[2:a]adelay=27500|27500,volume=1.0[n3];"
        "[3:a]adelay=41000|41000,volume=1.0[n4];"
        "[4:a]adelay=54500|54500,volume=1.0[n5];"
        "[5:a]adelay=13200|13200,volume=0.35[w1];"
        "[6:a]adelay=1000|1000,volume=0.30[c1];"
        "[7:a]adelay=17500|17500,volume=0.45[b1];"
        "[8:a]adelay=32000|32000,volume=0.30[r1];"
        "[9:a]adelay=55000|55000,volume=0.35[ch1];"
        "[n1][n2][n3][n4][n5][w1][c1][b1][r1][ch1]amix=inputs=10:duration=first:dropout_transition=2[mixed];"
        "[mixed]apad=whole_dur=68,afade=t=out:st=65.5:d=2.5[outa]",
        "-map", "[outa]",
        "-c:a", "libmp3lame", "-b:a", "192k",
        "-map_metadata", "-1", "-fflags", "+bitexact",
        "assets/audio/master_audio.mp3"
    ]
    subprocess.run(cmd, check=True)
    print("Master soundtrack generated at: assets/audio/master_audio.mp3")

if __name__ == "__main__":
    generate_voiceover()
    mix_soundtrack()
'''
    (project_dir / "build_audio.py").write_text(audio_builder_code, encoding="utf-8")

    print(f"\n[OK] documentary002 scaffolded successfully at: {project_dir}")
    print("Next steps:")
    print(f"  1. cd {project_dir}")
    print("  2. Place real photos in assets/images/ (01_hero.jpg, 02_mechanism.jpg, etc.)")
    print("  3. Customize narration scripts in build_audio.py and run 'python build_audio.py'")
    print("  4. Update index.html parameters")
    print("  5. Validate with 'npx hyperframes check'")
    print("  6. Render with 'npx hyperframes render --quality looks -o output.mp4'")

if __name__ == "__main__":
    main()
