#!/bin/bash
# Build an Edlintics puzzle reel from a puzzle JSON.
# Usage: build.sh <puzzle.json> [outdir=.] [voice|novoice|both=both]
#   STILLS_ONLY=1 build.sh ...   -> timeline, audio and contact sheet only (fast layout check)
set -e
REPO=/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing
"$REPO/tools/tts/.venv/bin/python" "$(dirname "$0")/build.py" "$1" "${2:-.}" "${3:-both}"
