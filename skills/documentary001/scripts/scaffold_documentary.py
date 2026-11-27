import os
import sys
import shutil
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new HyperFrames documentary in the 'documentary001' style."
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

    print(f"Scaffolding documentary001 project in: {project_dir}")
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

# Voiceover scripts for the 5 Acts (calibrated for natural speech and tight pacing)
ACTS = {
    "act1": "On June 5th, 1976, the newly completed Teton Dam suffered a catastrophic internal breach during its initial reservoir filling, releasing two million cubic feet per second across the valley.",
    "act2": "Forensic analysis revealed pressurized reservoir seepage through unsealed volcanic rock fissures in the right abutment, rapidly eroding the unplastic silt core because designers omitted defensive downstream filter zones.",
    "act3": "At seven in the morning, muddy springs erupted at the downstream toe, and within hours, high-velocity piping swallowed two D9 bulldozers as the central crest collapsed into a raging vortex.",
    "act4": "The independent Chadwick panel concluded the failure was completely preventable, caused by flawed design assumptions, inadequate foundation exploration, and the total omission of granular transition filters.",
    "act5": "The disaster claimed eleven lives and caused two billion dollars in damage, fundamentally reforming geotechnical engineering and mandating modern defensive filter criteria to protect lives worldwide."
}

def generate_voiceover(voice="en-US-ChristopherNeural"):
    audio_dir = Path("assets/audio")
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    for act, script in ACTS.items():
        raw_file = audio_dir / f"{act}_raw.mp3"
        out_file = audio_dir / f"{act}.mp3"
        print(f"Generating voiceover: {out_file.name}...")
        cmd_tts = [
            "edge-tts",
            "--voice", voice,
            "--rate=+1%",
            "--text", script,
            "--write-media", str(raw_file)
        ]
        subprocess.run(cmd_tts, check=True)
        
        # Trim trailing silence to guarantee natural crisp inter-act pauses
        cmd_trim = [
            "ffmpeg", "-y",
            "-i", str(raw_file),
            "-af", "areverse,silenceremove=start_periods=1:start_duration=0.05:start_threshold=-40dB,areverse",
            str(out_file)
        ]
        subprocess.run(cmd_trim, check=True, capture_output=True)
        if raw_file.exists():
            raw_file.unlink()

def mix_soundtrack():
    print("Mixing master soundtrack with calibrated tight pauses (1.3s - 1.6s between acts)...")
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
        "[0:a]adelay=600|600,volume=1.0[n1];"
        "[1:a]adelay=13800|13800,volume=1.0[n2];"
        "[2:a]adelay=27200|27200,volume=1.0[n3];"
        "[3:a]adelay=39800|39800,volume=1.0[n4];"
        "[4:a]adelay=52400|52400,volume=1.0[n5];"
        "[5:a]adelay=13200|13200,volume=0.35[w1];"
        "[6:a]adelay=1000|1000,volume=0.30[c1];"
        "[7:a]adelay=17500|17500,volume=0.45[b1];"
        "[8:a]adelay=32000|32000,volume=0.30[r1];"
        "[9:a]adelay=53000|53000,volume=0.35[ch1];"
        "[n1][n2][n3][n4][n5][w1][c1][b1][r1][ch1]amix=inputs=10:duration=longest:dropout_transition=2[mixed];"
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

    print(f"\n[OK] documentary001 scaffolded successfully at: {project_dir}")
    print("Next steps:")
    print(f"  1. cd {project_dir}")
    print("  2. Place real photos in assets/images/ (01_hero.jpg, 02_mechanism.jpg, etc.)")
    print("  3. Customize narration scripts in build_audio.py and run 'python build_audio.py'")
    print("  4. Update index.html parameters")
    print("  5. Validate with 'npx hyperframes check'")
    print("  6. Render with 'npx hyperframes render --quality looks -o output.mp4'")

if __name__ == "__main__":
    main()
