import os
import sys
import subprocess
from pathlib import Path

# Enforce non-commercial license agreement for automated run
os.environ["COQUI_TOS_AGREED"] = "1"

BASE_DIR = Path(r"c:\Users\Imran\Downloads\CHeck")
PROJECT_DIR = BASE_DIR / "teton-dam-documentary"
AUDIO_DIR = PROJECT_DIR / "assets" / "audio"
SAMPLE_VOICE = BASE_DIR / "my_voice_sample.wav"

SCRIPTS = {
    "act1": "On June 5th, 1976, the newly completed Teton Dam suffered a catastrophic internal breach during its initial reservoir filling, releasing two million cubic feet per second across the valley.",
    "act2": "Forensic analysis revealed pressurized reservoir seepage through unsealed volcanic rock fissures in the right abutment, rapidly eroding the unplastic silt core because designers omitted defensive downstream filter zones.",
    "act3": "At seven in the morning, muddy springs erupted at the downstream toe, and within hours, high-velocity piping swallowed two D9 bulldozers as the central crest collapsed into a raging vortex.",
    "act4": "The independent Chadwick panel concluded the failure was completely preventable, caused by flawed design assumptions, inadequate foundation exploration, and the total omission of granular transition filters.",
    "act5": "The disaster claimed eleven lives and caused two billion dollars in damage, fundamentally reforming geotechnical engineering and mandating modern defensive filter criteria to protect lives worldwide."
}

def check_voice_sample():
    if not SAMPLE_VOICE.exists():
        print(f"\n[ERROR] Voice sample not found at: {SAMPLE_VOICE}")
        print("Please record your voice first by running:")
        print("  record_my_voice.bat")
        print("Or drop any 10-15s clear recording named 'my_voice_sample.wav' into this folder.")
        sys.exit(1)
    print(f"[OK] Found reference voice sample: {SAMPLE_VOICE}")

def clone_narration():
    print("\n=== Step 1: Loading XTTS-v2 & Cloning Voice ===")
    from TTS.api import TTS
    
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
    
    for act, text in SCRIPTS.items():
        raw_out = AUDIO_DIR / f"{act}_cloned_raw.wav"
        final_mp3 = AUDIO_DIR / f"{act}_cloned.mp3"
        
        print(f"  Cloning {act} in your voice...")
        tts.tts_to_file(
            text=text,
            speaker_wav=str(SAMPLE_VOICE),
            language="en",
            file_path=str(raw_out)
        )
        
        # Trim trailing dead silence with FFmpeg
        cmd_trim = [
            "ffmpeg", "-y",
            "-i", str(raw_out),
            "-af", "areverse,silenceremove=start_periods=1:start_duration=0.05:start_threshold=-40dB,areverse",
            str(final_mp3)
        ]
        subprocess.run(cmd_trim, check=True, capture_output=True)
        if raw_out.exists():
            raw_out.unlink()
            
        print(f"  [OK] Generated {final_mp3.name}")

def mix_master_soundtrack():
    print("\n=== Step 2: Mixing Cloned Master Soundtrack (Tight Natural Pauses) ===")
    master_path = AUDIO_DIR / "master_audio_cloned.mp3"
    
    cmd_mix = [
        "ffmpeg", "-y",
        "-i", str(AUDIO_DIR / "act1_cloned.mp3"),
        "-i", str(AUDIO_DIR / "act2_cloned.mp3"),
        "-i", str(AUDIO_DIR / "act3_cloned.mp3"),
        "-i", str(AUDIO_DIR / "act4_cloned.mp3"),
        "-i", str(AUDIO_DIR / "act5_cloned.mp3"),
        "-i", str(AUDIO_DIR / "whoosh-cinematic.mp3"),
        "-i", str(AUDIO_DIR / "click-soft.mp3"),
        "-i", str(AUDIO_DIR / "impact-bass-1.mp3"),
        "-i", str(AUDIO_DIR / "riser.mp3"),
        "-i", str(AUDIO_DIR / "chime.mp3"),
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
        str(master_path)
    ]
    subprocess.run(cmd_mix, check=True)
    print(f"  [OK] Master soundtrack generated: {master_path}")

def multiplex_final_video():
    print("\n=== Step 3: Multiplexing Video with Your Cloned Voice ===")
    source_video = PROJECT_DIR / "teton_dam_failure_forensic.mp4"
    cloned_audio = AUDIO_DIR / "master_audio_cloned.mp3"
    output_video = BASE_DIR / "teton_dam_cloned_voice.mp4"
    
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", str(source_video),
        "-i", str(cloned_audio),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-map", "0:v:0", "-map", "1:a:0",
        "-map_metadata", "-1",
        "-fflags", "+bitexact",
        "-flags:v", "+bitexact",
        "-flags:a", "+bitexact",
        str(output_video)
    ]
    subprocess.run(cmd_mux, check=True)
    print(f"  [SUCCESS] Final cloned-voice documentary created at:\n  {output_video}")
    
    # Launch media player
    try:
        os.startfile(str(output_video))
    except Exception:
        pass

if __name__ == "__main__":
    check_voice_sample()
    clone_narration()
    mix_master_soundtrack()
    multiplex_final_video()
