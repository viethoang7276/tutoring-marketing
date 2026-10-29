#!/bin/bash
# Build an Edlintics highlighter reel from a script.json (see SKILL.md).
# Usage: build.sh <script.json> <outdir>      STILLS_ONLY=1 build.sh ... for a quick layout check
set -e
REPO=/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing
"$REPO/tools/tts/.venv/bin/python" "$(dirname "$0")/build.py" "$1" "$2"
