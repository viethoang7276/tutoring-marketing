#!/bin/bash
# One command for a whole reel: validate -> scenes -> voiceover -> audio mix -> render -> encode -> checks + contact sheet.
# Usage (from anywhere):  .claude/skills/edlintics-explainer-reel/scripts/make_reel.sh <workdir> <slug> [speed=1.08]
#   REUSE_AUDIO=1 make_reel.sh ...   rebuild the pictures only: keeps voiceover.wav, audio*.wav and the timing in
#                                    timing.json (use it after changing scenes, never after changing the voice text)
#   <workdir>/script.json  the script (see edlintics-definition-reel or edlintics-life-of-reel)
# Output in <workdir>: <slug>.mp4 (voice + effects + quiet pad, for preview), <slug>-voice-only.mp4,
#   <slug>-canva-upload.mp4 (<10 MB, upload this to Canva), <slug>-contact-sheet.png, <slug>-poster.jpg (the
#   first still by time, 540x960; upload it with the video), stills/, timing.json
# meta.type "lesson" (in-lesson videos, 5 Nov 2026): no social size cap, a 1080x1920 poster, and lesson_files.py writes
#   <slug>.vtt (captions) and <slug>-transcript.txt (the "Read instead" text)
# Speed options (7 Nov 2026, opt-in; with none set the build is exactly as before; numbers in ../SPEED.md):
#   ENGINE_PROFILE=1        seconds per step here, in build.sh and inside render.js
#   LESSON_SINGLE_ENCODE=1, ENGINE_ENCODER=videotoolbox   see build.sh
#   PICTURE_ONLY=1          voice-free picture mode: no voice, no credits, nothing in <workdir> but beats.json and the scene
#                           art is written. Timings come from a real timing.json when its beat count matches, else they are
#                           estimated at PICTURE_WPM (default 165). Output in <workdir>/_picture/: stills, contact sheet and
#                           a silent <slug>-picture.mp4 (with STILLS_ONLY=1 too: no video)
#   LESSON_OVERLAP_CHECK=1  runs overlap_check.py (data tables vs other items) before the voice; =strict stops on a hit
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"; REPO="$(cd "$HERE/../../../.." && pwd)"; PY="$REPO/tools/tts/.venv/bin/python"
W="$(cd "$1" && pwd)"; SLUG="$2"; SPEED="${3:-1.08}"
now() { perl -MTime::HiRes=time -e 'printf "%.2f", time'; }
P0=$(now); lap() { [ "$ENGINE_PROFILE" = "1" ] || return 0; local t; t=$(now); echo "PROFILE make_reel.sh $1: $(perl -e "printf '%.1f', $t - $P0") s"; P0=$t; }
LESSON=$("$PY" -c "import json,sys;print(int(json.load(open(sys.argv[1])).get('meta',{}).get('type')=='lesson'))" "$W/script.json")
[ -n "$SLUG" ] || { echo "usage: make_reel.sh <workdir> <slug> [speed]"; exit 2; }
echo "== 1/7 validate";      "$PY" "$HERE/validate.py" "$W/script.json"; lap validate
echo "== 2/7 scenes";        "$PY" "$HERE/build_scenes.py" "$W"; lap scenes
[ -n "$LESSON_OVERLAP_CHECK" ] && "$PY" "$HERE/overlap_check.py" "$W" $([ "$LESSON_OVERLAP_CHECK" = "strict" ] && echo --strict)
if [ "$PICTURE_ONLY" = "1" ]; then
  echo "== 3-6/7 picture only (PICTURE_ONLY=1): no voice, output in $W/_picture"
  P="$W/_picture"; "$PY" "$HERE/picture_timing.py" "$W" "$P" "${PICTURE_WPM:-165}"
  "$PY" "$HERE/make_scenes_json.py" "$P" "$P"
  cd "$HERE"; [ -d node_modules ] || npm install --no-audit --no-fund >/dev/null
  TS=$("$PY" -c "import json;T=json.load(open('$P/timing.json'));print(','.join(str(round(min(b['end']-0.05, (b['chunks'][-1]['t']+0.45) if b.get('chunks') else b['start']+1.6),2)) for b in T['beats']))")
  rm -rf "$P/stills"; SCENES="$P/scenes.json" OUT="$P/stills" node render.js stills "$TS"; lap "picture stills"
  if [ "$STILLS_ONLY" != "1" ]; then
    export FFMPEG=$("$PY" -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
    SCENES="$P/scenes.json" ENGINE_RANGE=1 node render.js video "$P/$SLUG-picture.mp4" -; lap "picture video"
  fi
  "$PY" "$HERE/postcheck.py" "$P" "$SLUG" >/dev/null 2>&1 || true; "$PY" "$HERE/framefill.py" "$P" || true
  echo "PICTURE_ONLY: $P/$SLUG-contact-sheet.png $([ "$STILLS_ONLY" != "1" ] && echo "$P/$SLUG-picture.mp4")"; exit 0
fi
if [ "$REUSE_AUDIO" = "1" ] && grep -q '"estimated": true' "$W/timing.json" 2>/dev/null; then echo "REUSE_AUDIO: timing.json is an estimate, not a voice timing; rebuild without REUSE_AUDIO"; exit 1; fi
if [ "$REUSE_AUDIO" = "1" ] && [ -f "$W/timing.json" ] && [ -f "$W/audio.wav" ]; then
  echo "== 3-4/7 reuse audio (REUSE_AUDIO=1): new frames into timing.json, voice and timings kept"
  "$PY" - "$W" <<'PYEOF'
import json, sys
d = sys.argv[1]; T = json.load(open(f"{d}/timing.json")); B = json.load(open(f"{d}/beats.json"))
if len(T["beats"]) != len(B): sys.exit("REUSE_AUDIO: beat count changed; rebuild without REUSE_AUDIO")
for t, b in zip(T["beats"], B):
    t.pop("cam", None); t.pop("rung", None); t.pop("chips", None)
    for k in ("img", "focus", "cam", "term", "keypoint", "definition", "equation", "footnote", "cta", "rung", "chips", "message", "tag"):   # picture and end-card fields; voice timings stay
        if k in b: t[k] = b[k]
json.dump(T, open(f"{d}/timing.json", "w"), indent=1)
PYEOF
lap "reuse audio"
else
echo "== 3/7 voiceover";     (cd "$REPO/tools/tts" && "$PY" "$HERE/vo.py" "$W" "$SPEED" "${VO_GAP:-0.2}" "${VO_TAIL:-0.5}")
echo "== 4/7 audio mix";     "$PY" "$HERE/mix_audio.py" "$W"; lap "voice + mix"
fi
echo "== 5/7 scene data";    "$PY" "$HERE/make_scenes_json.py" "$W" "$W"; lap "scene data"
echo "== 6/7 stills";        cd "$HERE"; [ -d node_modules ] || npm install --no-audit --no-fund >/dev/null
TS=$("$PY" -c "import json;T=json.load(open('$W/timing.json'));print(','.join(str(round(min(b['end']-0.05, (b['chunks'][-1]['t']+0.45) if b.get('chunks') else b['start']+1.6),2)) for b in T['beats']))")
rm -rf "$W/stills"; SCENES="$W/scenes.json" OUT="$W/stills" node render.js stills "$TS"; lap stills
[ "$STILLS_ONLY" = "1" ] && { "$PY" "$HERE/postcheck.py" "$W" "$SLUG" >/dev/null 2>&1 || true; "$PY" "$HERE/framefill.py" "$W" || true; echo "STILLS_ONLY: stills and contact sheet only"; exit 0; }
echo "== 7/7 render video";  SCENES="$W/scenes.json" ./build.sh "$W" "$SLUG"; lap "render video (build.sh)"
# poster: the first still by time (numeric sort, never by name), saved as <slug>-poster.jpg
# lessons: full size 1080x1920 for the in-app player
PS=$([ "$LESSON" = "1" ] && echo "1080,1920" || echo "540,960")
"$PY" -c "import glob,re;from PIL import Image;f=min(glob.glob('$W/stills/still-*.png'),key=lambda p:float(re.search(r'still-([\d.]+)\.png',p)[1]));Image.open(f).convert('RGB').resize(($PS)).save('$W/$SLUG-poster.jpg',quality=85 if '$PS'=='540,960' else 90);print('poster:','$W/$SLUG-poster.jpg','from',f.split('/')[-1])"
[ "$LESSON" = "1" ] && "$PY" "$HERE/lesson_files.py" "$W" "$SLUG"
"$PY" "$HERE/postcheck.py" "$W" "$SLUG"; lap "poster, lesson files, postcheck"
"$PY" "$HERE/framefill.py" "$W"; lap framefill   # frame-fill report; FAILs only for the full-frame layout (meta.layout "full")
