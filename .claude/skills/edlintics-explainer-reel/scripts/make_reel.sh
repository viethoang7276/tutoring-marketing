#!/bin/bash
# One command for a whole reel: validate -> scenes -> voiceover -> audio mix -> render -> encode -> checks + contact sheet.
# Usage (from anywhere):  .claude/skills/edlintics-explainer-reel/scripts/make_reel.sh <workdir> <slug> [speed=1.08]
#   REUSE_AUDIO=1 make_reel.sh ...   rebuild the pictures only: keeps voiceover.wav, audio*.wav and the timing in
#                                    timing.json (use it after changing scenes, never after changing the voice text)
#   <workdir>/script.json  the script (see edlintics-definition-reel or edlintics-life-of-reel)
# Output in <workdir>: <slug>.mp4 (voice + effects + quiet pad, for preview), <slug>-voice-only.mp4,
#   <slug>-canva-upload.mp4 (<10 MB, upload this to Canva), <slug>-contact-sheet.png, <slug>-poster.jpg (the
#   first still by time, 540x960; upload it with the video), stills/, timing.json
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"; REPO="$(cd "$HERE/../../../.." && pwd)"; PY="$REPO/tools/tts/.venv/bin/python"
W="$(cd "$1" && pwd)"; SLUG="$2"; SPEED="${3:-1.08}"
[ -n "$SLUG" ] || { echo "usage: make_reel.sh <workdir> <slug> [speed]"; exit 2; }
echo "== 1/7 validate";      "$PY" "$HERE/validate.py" "$W/script.json"
echo "== 2/7 scenes";        "$PY" "$HERE/build_scenes.py" "$W"
if [ "$REUSE_AUDIO" = "1" ] && [ -f "$W/timing.json" ] && [ -f "$W/audio.wav" ]; then
  echo "== 3-4/7 reuse audio (REUSE_AUDIO=1): new frames into timing.json, voice and timings kept"
  "$PY" - "$W" <<'PYEOF'
import json, sys
d = sys.argv[1]; T = json.load(open(f"{d}/timing.json")); B = json.load(open(f"{d}/beats.json"))
if len(T["beats"]) != len(B): sys.exit("REUSE_AUDIO: beat count changed; rebuild without REUSE_AUDIO")
for t, b in zip(T["beats"], B):
    t.pop("cam", None)
    for k in ("img", "focus", "cam"):
        if k in b: t[k] = b[k]
json.dump(T, open(f"{d}/timing.json", "w"), indent=1)
PYEOF
else
echo "== 3/7 voiceover";     (cd "$REPO/tools/tts" && "$PY" "$HERE/vo.py" "$W" "$SPEED" "${VO_GAP:-0.2}" "${VO_TAIL:-0.5}")
echo "== 4/7 audio mix";     "$PY" "$HERE/mix_audio.py" "$W"
fi
echo "== 5/7 scene data";    "$PY" "$HERE/make_scenes_json.py" "$W" "$W"
echo "== 6/7 stills";        cd "$HERE"; [ -d node_modules ] || npm install --no-audit --no-fund >/dev/null
TS=$("$PY" -c "import json;T=json.load(open('$W/timing.json'));print(','.join(str(round(min(b['end']-0.05, (b['chunks'][-1]['t']+0.45) if b.get('chunks') else b['start']+1.6),2)) for b in T['beats']))")
rm -rf "$W/stills"; SCENES="$W/scenes.json" OUT="$W/stills" node render.js stills "$TS"
[ "$STILLS_ONLY" = "1" ] && { "$PY" "$HERE/postcheck.py" "$W" "$SLUG" >/dev/null 2>&1; echo "STILLS_ONLY: stills and contact sheet only"; exit 0; }
echo "== 7/7 render video";  SCENES="$W/scenes.json" ./build.sh "$W" "$SLUG"
# poster: the first still by time (numeric sort, never by name), saved as <slug>-poster.jpg
"$PY" -c "import glob,re;from PIL import Image;f=min(glob.glob('$W/stills/still-*.png'),key=lambda p:float(re.search(r'still-([\d.]+)\.png',p)[1]));Image.open(f).convert('RGB').resize((540,960)).save('$W/$SLUG-poster.jpg',quality=85);print('poster:','$W/$SLUG-poster.jpg','from',f.split('/')[-1])"
"$PY" "$HERE/postcheck.py" "$W" "$SLUG"
