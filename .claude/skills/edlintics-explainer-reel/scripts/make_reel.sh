#!/bin/bash
# One command for a whole reel: validate -> scenes -> voiceover -> audio mix -> render -> encode -> checks + contact sheet.
# Usage (from anywhere):  .claude/skills/edlintics-explainer-reel/scripts/make_reel.sh <workdir> <slug> [speed=1.08]
#   <workdir>/script.json  the script (see edlintics-definition-reel or edlintics-life-of-reel)
# Output in <workdir>: <slug>.mp4 (voice + effects + quiet pad, for preview), <slug>-voice-only.mp4,
#   <slug>-canva-upload.mp4 (<10 MB, upload this to Canva), <slug>-contact-sheet.png, stills/, timing.json
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"; REPO="$(cd "$HERE/../../../.." && pwd)"; PY="$REPO/tools/tts/.venv/bin/python"
W="$(cd "$1" && pwd)"; SLUG="$2"; SPEED="${3:-1.08}"
[ -n "$SLUG" ] || { echo "usage: make_reel.sh <workdir> <slug> [speed]"; exit 2; }
echo "== 1/7 validate";      "$PY" "$HERE/validate.py" "$W/script.json"
echo "== 2/7 scenes";        "$PY" "$HERE/build_scenes.py" "$W"
echo "== 3/7 voiceover";     (cd "$REPO/tools/tts" && "$PY" "$HERE/vo.py" "$W" "$SPEED" 0.2)
echo "== 4/7 audio mix";     "$PY" "$HERE/mix_audio.py" "$W"
echo "== 5/7 scene data";    "$PY" "$HERE/make_scenes_json.py" "$W" "$W"
echo "== 6/7 stills";        cd "$HERE"; [ -d node_modules ] || npm install --no-audit --no-fund >/dev/null
TS=$("$PY" -c "import json;T=json.load(open('$W/timing.json'));print(','.join(str(round(min(b['end']-0.05, (b['chunks'][-1]['t']+0.45) if b.get('chunks') else b['start']+1.6),2)) for b in T['beats']))")
rm -rf "$W/stills"; SCENES="$W/scenes.json" OUT="$W/stills" node render.js stills "$TS"
echo "== 7/7 render video";  SCENES="$W/scenes.json" ./build.sh "$W" "$SLUG"
"$PY" "$HERE/postcheck.py" "$W" "$SLUG"
