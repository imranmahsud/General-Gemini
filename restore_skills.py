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
    print("\nInstalling global dependencies (impeccable, understand-anything, hyperframes, remotion)...")
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    npm_pkgs = [
        "impeccable@^4.8.0",
        "understand-anything-mcp@^2.7.8",
        "hyperframes@^0.9.16",
        "@remotion/cli@^4.0.541",
        "remotion@^4.0.541"
    ]
    try:
        subprocess.run([npm_cmd, "install", "-g"] + npm_pkgs, check=True)
        print("  [OK] Global CLI tools installed successfully.")
    except Exception as e:
        print(f"  [WARN] Note on npm global install: {e}")

    # Install faster-whisper (whisper-ctranslate2) via uv
    print("\nInstalling Faster-Whisper CLI (whisper-ctranslate2)...")
    try:
        subprocess.run(["uv", "tool", "install", "--python", "3.12", "whisper-ctranslate2"], check=True)
        print("  [OK] whisper-ctranslate2 installed successfully.")
    except Exception as e:
        print(f"  [WARN] Note on whisper-ctranslate2 install: {e}")

    # Install OpenVINO
    print("\nEnsuring OpenVINO is installed...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "openvino"], check=True)
        print("  [OK] openvino installed successfully.")
    except Exception as e:
        print(f"  [WARN] Note on openvino install: {e}")

    # Clone tools ecosystem if missing
    tools_dir = "C:\\tools" if sys.platform == "win32" else os.path.expanduser("~/tools")
    os.makedirs(tools_dir, exist_ok=True)
    sb_dir = os.path.join(tools_dir, "second-brain-suite")
    os.makedirs(sb_dir, exist_ok=True)

    git_repos = {
        os.path.join(tools_dir, "ai-engineering-hub"): "https://github.com/patchy631/ai-engineering-hub.git",
        os.path.join(tools_dir, "awesome-mcp-servers"): "https://github.com/punkpeye/awesome-mcp-servers.git",
        os.path.join(tools_dir, "Wan-Video"): "https://github.com/Wan-Video/Wan2.1.git",
        os.path.join(tools_dir, "LTX-Video"): "https://github.com/Lightricks/LTX-2.git",
        os.path.join(tools_dir, "Z-Image"): "https://github.com/Tongyi-MAI/Z-Image.git",
        os.path.join(sb_dir, "gbrain"): "https://github.com/garrytan/gbrain.git",
        os.path.join(sb_dir, "llm-wiki"): "https://github.com/lucasastorian/llmwiki.git",
        os.path.join(sb_dir, "obsidian-skills"): "https://github.com/obsidianmd/obsidian-skills.git",
        os.path.join(sb_dir, "knowledge-work-plugins"): "https://github.com/anthropics/knowledge-work-plugins.git",
        os.path.join(sb_dir, "openai-skills"): "https://github.com/openai/skills.git",
        os.path.join(sb_dir, "khoj"): "https://github.com/khoj-ai/khoj.git",
        os.path.join(sb_dir, "ai-memory"): "https://github.com/akitaonrails/ai-memory.git",
        os.path.join(sb_dir, "basic-memory"): "https://github.com/basicmachines-co/basic-memory.git",
        os.path.join(sb_dir, "COG-second-brain"): "https://github.com/huytieu/COG-second-brain.git",
        os.path.join(tools_dir, "qgis-ai-segmentation"): "https://github.com/TerraLabAI/QGIS_AI-Segmentation.git",
        os.path.join(tools_dir, "motion-canvas"): "https://github.com/motion-canvas/motion-canvas.git",
        os.path.join(tools_dir, "DabbleCAD"): "https://github.com/DJMcNewgent/DabbleCAD.git",
    }

    # Install Ollama & Chatbox for Daily Local LLM Execution
    print("\nEnsuring Ollama and Chatbox are installed via winget...")
    try:
        subprocess.run(["winget", "install", "--id", "Ollama.Ollama", "--accept-source-agreements", "--accept-package-agreements", "--silent"], check=False)
        subprocess.run(["winget", "install", "--id", "Bin-Huang.Chatbox", "--accept-source-agreements", "--accept-package-agreements", "--silent"], check=False)
        print("  [OK] Ollama and Chatbox checked.")
        
        # Create helper launchers
        if sys.platform == "win32":
            qwen_bat = os.path.join(tools_dir, "qwen.bat")
            with open(qwen_bat, "w") as f:
                f.write('@echo off\nset OLLAMA_KEEP_ALIVE=5m\ncurl.exe -s http://127.0.0.1:11434/ >nul 2>&1\nif errorlevel 1 (\n    start "" /b "%LOCALAPPDATA%\\Programs\\Ollama\\ollama.exe" serve\n    timeout /t 2 /nobreak >nul\n)\n"%LOCALAPPDATA%\\Programs\\Ollama\\ollama.exe" run qwen2.5:7b %*\n')
            
            chatbox_bat = os.path.join(tools_dir, "chatbox.bat")
            with open(chatbox_bat, "w") as f:
                f.write('@echo off\nset OLLAMA_KEEP_ALIVE=5m\ncurl.exe -s http://127.0.0.1:11434/ >nul 2>&1\nif errorlevel 1 (\n    start "" /b "%LOCALAPPDATA%\\Programs\\Ollama\\ollama.exe" serve\n    timeout /t 2 /nobreak >nul\n)\nstart "" "%LOCALAPPDATA%\\Programs\\chatbox\\Chatbox.exe"\n')
            print("  [OK] Launchers created: qwen.bat and chatbox.bat")
    except Exception as e:
        print(f"  [WARN] Note on Ollama/Chatbox setup: {e}")

    print("\nEnsuring AI Tools & Repositories are cloned...")
    for target_path, repo_url in git_repos.items():
        if not os.path.exists(target_path):
            print(f"  [CLONING] {repo_url} -> {target_path}")
            try:
                subprocess.run(["git", "clone", "--depth", "1", repo_url, target_path], check=True)
            except Exception as e:
                print(f"  [WARN] Failed to clone {repo_url}: {e}")
        else:
            print(f"  [OK] Already present: {os.path.basename(target_path)}")

    # Ensure DabbleCAD portable binary & launcher
    dabblecad_app = os.path.join(tools_dir, "DabbleCAD-app")
    if sys.platform == "win32" and not os.path.exists(os.path.join(dabblecad_app, "DabbleCAD.exe")):
        print("\nDownloading DabbleCAD portable...")
        try:
            import urllib.request, zipfile, io
            url = "https://github.com/DJMcNewgent/DabbleCAD/releases/download/v1.2.0/DabbleCAD-1.2.0-win-x64.zip"
            os.makedirs(dabblecad_app, exist_ok=True)
            data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=120).read()
            z = zipfile.ZipFile(io.BytesIO(data))
            z.extractall(dabblecad_app)
            print("  [OK] DabbleCAD extracted.")
        except Exception as e:
            print(f"  [WARN] DabbleCAD portable download note: {e}")

    if sys.platform == "win32":
        dabble_bat = os.path.join(tools_dir, "dabblecad.bat")
        with open(dabble_bat, "w") as f:
            f.write('@echo off\nstart "" "C:\\tools\\DabbleCAD-app\\DabbleCAD.exe" %*\n')

        motion_bat = os.path.join(tools_dir, "motion-canvas.bat")
        with open(motion_bat, "w") as f:
            f.write('@echo off\ncd /d "C:\\tools\\motion-canvas"\nstart "" http://localhost:9000\nnpm run template:dev\n')

        # Install QGIS AI Segmentation plugin into active QGIS profile
        qgis_plugins = os.path.expandvars(r"%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins")
        if os.path.exists(qgis_plugins):
            dest_qgis_plugin = os.path.join(qgis_plugins, "AI_Segmentation")
            src_qgis_plugin = os.path.join(tools_dir, "qgis-ai-segmentation")
            if os.path.exists(src_qgis_plugin) and not os.path.exists(dest_qgis_plugin):
                shutil.copytree(src_qgis_plugin, dest_qgis_plugin, dirs_exist_ok=True)
                print("  [OK] AI_Segmentation plugin linked to QGIS.")


    print("\n==================================================")
    print(" Skills restoration complete! Ready to use on this PC.")
    print("==================================================")

if __name__ == "__main__":
    main()
