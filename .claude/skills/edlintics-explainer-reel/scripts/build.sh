#!/bin/bash
# Renders the reel (headless Chrome, 24 fps, pencil boil + draw-on) and encodes standard MP4s.
# Usage: build.sh <workdir> <name>      (uses <workdir>/scenes.json if present, else scenes.json here; audio-voice.wav + audio.wav in <workdir>)
set -e
cd "$(dirname "$0")"
REPO="$(cd ../../../.. && pwd)"
PY="$REPO/tools/tts/.venv/bin/python"
export FFMPEG=$($PY -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
[ -d node_modules ] || npm install --no-audit --no-fund >/dev/null
W="$1"; N="$2"
SCENES="${SCENES:-$W/scenes.json}"; [ -f "$SCENES" ] || SCENES="$(pwd)/scenes.json"
SCENES="$SCENES" node render.js video "$W/raw.mp4" "$W/audio-voice.wav"
$FFMPEG -y -loglevel error -i "$W/raw.mp4" -vf "scale=in_range=pc:out_range=tv,format=yuv420p" -c:v libx264 -preset medium -crf 20 -c:a aac -ar 48000 -b:a 160k -movflags +faststart "$W/$N-voice-only.mp4"
$FFMPEG -y -loglevel error -i "$W/$N-voice-only.mp4" -i "$W/audio.wav" -map 0:v -map 1:a -c:v copy -c:a aac -ar 48000 -b:a 160k -movflags +faststart -shortest "$W/$N.mp4"
# Canva upload copy: the Chrome file bridge takes at most 10 MB. Long reels (how-to, 60-90 s, 1 Nov 2026) get a lower
# video bitrate so the file stays near 9.3 MB; reels up to ~48 s keep 1500k as before
DUR=$($PY -c "import json;print(json.load(open('$W/timing.json'))['duration'])")
VB=$($PY -c "print(min(1500, int((9.3e6*8/$DUR - 128000)/1000)))")
# in-lesson videos (5 Nov 2026) are not uploaded through Canva or the social apps: no 10 MB cap, keep 1500k and the crf 20 preview
LESSON=$($PY -c "import json,sys;print(int(json.load(open(sys.argv[1])).get('meta',{}).get('type')=='lesson'))" "$W/script.json" 2>/dev/null || echo 0)
[ "$LESSON" = "1" ] && VB=1500
$FFMPEG -y -loglevel error -i "$W/$N-voice-only.mp4" -c:v libx264 -preset slow -tune animation -b:v ${VB}k -maxrate $((VB*4/3))k -bufsize $((VB*8/3))k -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart "$W/$N-canva-upload.mp4"
# the preview MP4 (voice + music) is shared and posted too: if it is 10 MB or more, re-encode it at the same capped bitrate
if [ "$LESSON" != "1" ] && [ "$(wc -c < "$W/$N.mp4")" -ge 10000000 ]; then
  $FFMPEG -y -loglevel error -i "$W/$N.mp4" -c:v libx264 -preset slow -tune animation -b:v ${VB}k -maxrate $((VB*4/3))k -bufsize $((VB*8/3))k -pix_fmt yuv420p -c:a aac -ar 48000 -b:a 128k -movflags +faststart "$W/_small.mp4" && mv "$W/_small.mp4" "$W/$N.mp4"
fi
rm "$W/raw.mp4"; ls -la "$W/$N"*.mp4
