import subprocess
import sys
import shutil
from pathlib import Path

def run_cmd(cmd, check=True):
    print(f"Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, check=check, text=True, capture_output=False)
    return res

def main():
    output_name = sys.argv[1] if len(sys.argv) > 1 else "documentary_output.mp4"
    clean_name = "clean_" + output_name

    print("=== Step 1: Preflight Check ===")
    run_cmd(["npx.cmd", "hyperframes", "check"])

    print("\n=== Step 2: Render Video ===")
    run_cmd(["npx.cmd", "hyperframes", "render", "--quality", "looks", "-o", output_name])

    print("\n=== Step 3: Strip Metadata (Bitexact Clean) ===")
    cmd_scrub = [
        "ffmpeg", "-y",
        "-i", output_name,
        "-c", "copy",
        "-map_metadata", "-1",
        "-fflags", "+bitexact",
        "-flags:v", "+bitexact",
        "-flags:a", "+bitexact",
        clean_name
    ]
    run_cmd(cmd_scrub)
    shutil.move(clean_name, output_name)
    print(f"Scrubbed tool/AI metadata from: {output_name}")

    print("\n=== Step 4: Stream & Tag Verification ===")
    cmd_probe = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration,size,bit_rate:format_tags",
        "-show_entries", "stream=codec_name,width,height,r_frame_rate,duration",
        "-of", "json",
        output_name
    ]
    subprocess.run(cmd_probe)

    print(f"\n[SUCCESS] Final delivery ready: {output_name}")

if __name__ == "__main__":
    main()
