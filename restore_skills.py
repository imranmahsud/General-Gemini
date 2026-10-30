import os
import sys
import shutil
import subprocess
import glob
import re

def main():
    print("==================================================")
    print("   Antigravity & Agent Skills Restore Utility     ")
    print("==================================================")

    home = os.path.expanduser("~")
    gemini_skills = os.path.join(home, ".gemini", "config", "skills")
    claude_skills = os.path.join(home, ".claude", "skills")

    target_dirs = [gemini_skills]
    # If .claude exists, also populate it
    if os.path.exists(os.path.join(home, ".claude")):
        target_dirs.append(claude_skills)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_skills_dir = os.path.join(script_dir, "skills")

    if not os.path.exists(source_skills_dir):
        print(f"Error: Source skills directory not found at {source_skills_dir}")
        sys.exit(1)

    for target in target_dirs:
        os.makedirs(target, exist_ok=True)
        print(f"\nRestoring skills to: {target}")
        
        for item in sorted(os.listdir(source_skills_dir)):
            src_path = os.path.join(source_skills_dir, item)
            dst_path = os.path.join(target, item)
            if os.path.isdir(src_path):
                if os.path.exists(dst_path):
                    shutil.rmtree(dst_path)
                shutil.copytree(src_path, dst_path)
                
                # Check SKILL.md
                skill_md = os.path.join(dst_path, "SKILL.md")
                name = item
                if os.path.exists(skill_md):
                    with open(skill_md, "r", encoding="utf-8", errors="ignore") as f:
                        m = re.search(r"^name:\s*([^\n]+)", f.read(500), re.MULTILINE)
                        if m:
                            name = m.group(1).strip()
                print(f"  [OK] Restored skill: {item} (ID: {name})")

    # Install global npm dependencies
    print("\nInstalling global dependencies (impeccable, understand-anything-mcp)...")
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    try:
        subprocess.run([npm_cmd, "install", "-g", "impeccable@^4.8.0", "understand-anything-mcp@^2.7.8"], check=True)
        print("  [OK] Global CLI tools installed successfully.")
    except Exception as e:
        print(f"  [WARN] Note on npm global install: {e}")
        print("  You can run 'npm install -g impeccable understand-anything-mcp' manually.")

    print("\n==================================================")
    print(" Skills restoration complete! Ready to use on this PC.")
    print("==================================================")

if __name__ == "__main__":
    main()
