#!/usr/bin/env bash
# ==============================================================
# General-Gemini: Debian Environment Restoration Script
# One-click restorer for Agent Skills, CLI tools, and Syncthing
# ==============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_USER="${SUDO_USER:-$USER}"
USER_HOME=$(eval echo "~$TARGET_USER")

echo "=================================================="
echo " Starting Debian Environment Restoration"
echo " Target User: $TARGET_USER ($USER_HOME)"
echo " Source Repo: $SCRIPT_DIR"
echo "=================================================="

# 1. System Package Installation (Apt)
echo "[1/6] Installing system dependencies via apt..."
sudo apt-get update -y
sudo apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    pkg-config \
    libssl-dev \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    ffmpeg \
    gdal-bin \
    python3-gdal \
    qgis \
    syncthing \
    jq

# 2. Node.js LTS Installation
if ! command -v node >/dev/null 2>&1; then
    echo "[2/6] Installing Node.js LTS from NodeSource..."
    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
    sudo apt-get install -y nodejs
else
    echo "[2/6] Node.js $(node -v) is already installed."
fi

# 3. Python 'uv' Package Manager
if [ ! -f "$USER_HOME/.cargo/bin/uv" ] && ! command -v uv >/dev/null 2>&1; then
    echo "[3/6] Installing Astral uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$USER_HOME/.cargo/bin:$PATH"
else
    echo "[3/6] uv is already installed."
fi

# 4. Global NPM CLI Tools
echo "[4/6] Installing global agent packages..."
sudo npm install -g \
    impeccable@^4.8.0 \
    understand-anything-mcp@^2.7.8 \
    hyperframes@^0.9.16 \
    remotion@^4.0.541 \
    @remotion/cli@^4.0.541

# 5. Restore Agent Skills, Plugins, and System Rules
echo "[5/6] Restoring Agent Skills & Rules..."
GEMINI_SKILLS="$USER_HOME/.gemini/config/skills"
CLAUDE_SKILLS="$USER_HOME/.claude/skills"
AGENTS_SKILLS="$USER_HOME/.agents/skills"
GEMINI_PLUGINS="$USER_HOME/.gemini/config/plugins"

mkdir -p "$GEMINI_SKILLS" "$CLAUDE_SKILLS" "$AGENTS_SKILLS" "$GEMINI_PLUGINS"

if [ -d "$SCRIPT_DIR/skills" ]; then
    echo " -> Restoring skills to $GEMINI_SKILLS, $CLAUDE_SKILLS, $AGENTS_SKILLS"
    cp -r "$SCRIPT_DIR/skills/"* "$GEMINI_SKILLS/" 2>/dev/null || true
    cp -r "$SCRIPT_DIR/skills/"* "$CLAUDE_SKILLS/" 2>/dev/null || true
    cp -r "$SCRIPT_DIR/skills/"* "$AGENTS_SKILLS/" 2>/dev/null || true
fi

if [ -d "$SCRIPT_DIR/plugins" ]; then
    echo " -> Restoring plugins to $GEMINI_PLUGINS"
    cp -r "$SCRIPT_DIR/plugins/"* "$GEMINI_PLUGINS/" 2>/dev/null || true
fi

if [ -f "$SCRIPT_DIR/AGENTS.md" ]; then
    echo " -> Restoring global AGENTS.md rules"
    cp "$SCRIPT_DIR/AGENTS.md" "$USER_HOME/.gemini/config/AGENTS.md"
    mkdir -p "$USER_HOME/.claude"
    cp "$SCRIPT_DIR/AGENTS.md" "$USER_HOME/.claude/AGENTS.md"
fi

# 6. Restore Syncthing Configuration & WhatsApp Sync Targets
echo "[6/6] Restoring Syncthing configuration & pairing..."
SYNCTHING_DIR="$USER_HOME/.config/syncthing"
mkdir -p "$SYNCTHING_DIR"

if [ -d "$SCRIPT_DIR/configs/syncthing" ]; then
    cp "$SCRIPT_DIR/configs/syncthing/cert.pem" "$SYNCTHING_DIR/"
    cp "$SCRIPT_DIR/configs/syncthing/key.pem" "$SYNCTHING_DIR/"
    cp "$SCRIPT_DIR/configs/syncthing/https-cert.pem" "$SYNCTHING_DIR/"
    cp "$SCRIPT_DIR/configs/syncthing/https-key.pem" "$SYNCTHING_DIR/"
    chmod 600 "$SYNCTHING_DIR/key.pem" "$SYNCTHING_DIR/https-key.pem"

    # Adapt paths in config.xml
    sed "s|HOMEDIR|$USER_HOME|g" "$SCRIPT_DIR/configs/syncthing/config.linux.template.xml" > "$SYNCTHING_DIR/config.xml"
    chmod 600 "$SYNCTHING_DIR/config.xml"

    # Create WhatsApp media sync directory placeholder
    WA_MEDIA_DIR="$USER_HOME/WhatsappDataSynced"
    mkdir -p "$WA_MEDIA_DIR/.stfolder"
    echo " -> Created Syncthing target folder at: $WA_MEDIA_DIR"

    # Fix ownership
    chown -R "$TARGET_USER:$TARGET_USER" "$USER_HOME/.config/syncthing" "$USER_HOME/.gemini" "$USER_HOME/.claude" "$USER_HOME/.agents" "$WA_MEDIA_DIR" 2>/dev/null || true

    # Enable and start Syncthing user daemon
    if command -v systemctl >/dev/null 2>&1; then
        echo " -> Starting Syncthing user daemon..."
        systemctl --user enable syncthing.service 2>/dev/null || true
        systemctl --user restart syncthing.service 2>/dev/null || true
    fi
fi

echo "=================================================="
echo " Restoration Complete!"
echo " All skills, tools, and Syncthing keys are active."
echo " Just paste your WhatsappDataSynced media into: $USER_HOME/WhatsappDataSynced"
echo "=================================================="
