#!/usr/bin/env bash
# One-command setup for a Linux cloud session (Ubuntu 24.04, root): Java 17, Xvfb/xdotool/ImageMagick, the Forge 1.20.1-47.4.10 client in
# .build/mc (tools/setup_mc.py) and the release mod set in mods/. Idempotent; about 3-5 minutes on a fresh container.
# Needs network access to the hosts listed in docs/HANDOFF.md section 1 (Mojang, Forge maven, CurseForge and Modrinth CDNs).
set -euo pipefail
cd "$(dirname "$0")/.."
if [ ! -x /usr/lib/jvm/java-17-openjdk-amd64/bin/java ] || ! command -v xdotool >/dev/null || ! command -v Xvfb >/dev/null; then
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -qq
  apt-get install -y -qq openjdk-17-jre xdotool x11-utils xvfb imagemagick >/dev/null
fi
python3 tools/setup_mc.py
python3 tools/install.py --status core,std
