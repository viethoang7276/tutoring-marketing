#!/bin/bash
# Build an Edlintics "Where your money goes" reel from a script.json (see money_build.py).
# Usage: money_build.sh <script.json> <outdir>      STILLS_ONLY=1 money_build.sh ... for a quick layout check
set -e
REPO=/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing
"$REPO/tools/tts/.venv/bin/python" "$(dirname "$0")/money_build.py" "$1" "$2"
