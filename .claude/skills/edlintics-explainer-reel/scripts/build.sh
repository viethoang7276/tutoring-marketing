#!/bin/bash
# Renders the reel (headless Chrome, 24 fps, pencil boil + draw-on) and encodes standard MP4s.
# Usage: build.sh <workdir> <name>      (uses <workdir>/scenes.json if present, else scenes.json here; audio-voice.wav + audio.wav in <workdir>)
# Speed options (7 Nov 2026, opt-in; with none set the commands are exactly the old ones; numbers in ../SPEED.md):
#   LESSON_SINGLE_ENCODE=1  lessons only: one libx264 encode with the range conversion in the first pass, straight into
#                           <name>-voice-only.mp4; <name>.mp4 is a stream copy as before; <name>-canva-upload.mp4 is a plain
#                           copy of the voice-only file (lessons never go through Canva). Ignored for other types
#   ENGINE_ENCODER=videotoolbox  every encode uses Apple hardware H.264: the first pass at ENGINE_VB kbit/s (default 3000),
#                           the Canva copy and the 10 MB re-encode at the same capped bitrate as libx264
#   ENGINE_PROFILE=1        prints the seconds of each step
set -e
cd "$(dirname "$0")"
REPO="$(cd ../../../.. && pwd)"
PY="$REPO/tools/tts/.venv/bin/python"
export FFMPEG=$($PY -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
[ -d node_modules ] || npm install --no-audit --no-fund >/dev/null
W="$1"; N="$2"
SCENES="${SCENES:-$W/scenes.json}"; [ -f "$SCENES" ] || SCENES="$(pwd)/scenes.json"
LESSON=$($PY -c "import json,sys;print(int(json.load(open(sys.argv[1])).get('meta',{}).get('type')=='lesson'))" "$W/script.json" 2>/dev/null || echo 0)
SINGLE=0; [ "$LESSON_SINGLE_ENCODE" = "1" ] && [ "$LESSON" = "1" ] && SINGLE=1
VT=0; [ "$ENGINE_ENCODER" = "videotoolbox" ] && VT=1
now() { perl -MTime::HiRes=time -e 'printf "%.2f", time'; }
P0=$(now); lap() { [ "$ENGINE_PROFILE" = "1" ] || return 0; local t; t=$(now); echo "PROFILE build.sh $1: $(perl -e "printf '%.1f', $t - $P0") s"; P0=$t; }
if [ "$SINGLE" = "1" ]; then
  SCENES="$SCENES" ENGINE_RANGE=1 node render.js video "$W/$N-voice-only.mp4" "$W/audio-voice.wav"; lap "render + single encode"
else
SCENES="$SCENES" node render.js video "$W/raw.mp4" "$W/audio-voice.wav"; lap "render + first encode"
if [ "$VT" = "1" ]; then
  $FFMPEG -y -loglevel error -i "$W/raw.mp4" -vf "scale=in_range=pc:out_range=tv,format=yuv420p" -c:v h264_videotoolbox -profile:v high -b:v ${ENGINE_VB:-3000}k -c:a aac -ar 48000 -b:a 160k -movflags +faststart "$W/$N-voice-only.mp4"
else
$FFMPEG -y -loglevel error -i "$W/raw.mp4" -vf "scale=in_range=pc:out_range=tv,format=yuv420p" -c:v libx264 -preset medium -crf 20 -c:a aac -ar 48000 -b:a 160k -movflags +faststart "$W/$N-voice-only.mp4"
fi; lap "voice-only re-encode"
fi
$FFMPEG -y -loglevel error -i "$W/$N-voice-only.mp4" -i "$W/audio.wav" -map 0:v -map 1:a -c:v copy -c:a aac -ar 48000 -b:a 160k -movflags +faststart -shortest "$W/$N.mp4"; lap "music mux (stream copy)"
# Canva upload copy: the Chrome file bridge takes at most 10 MB. Long reels (how-to, 60-90 s, 1 Nov 2026) get a lower
# video bitrate so the file stays near 9.3 MB; reels up to ~48 s keep 1500k as before
DUR=$($PY -c "import json;print(json.load(open('$W/timing.json'))['duration'])")
VB=$($PY -c "print(min(1500, int((9.3e6*8/$DUR - 128000)/1000)))")
# in-lesson videos (5 Nov 2026) are not uploaded through Canva or the social apps: no 10 MB cap, keep 1500k and the crf 20 preview
[ "$LESSON" = "1" ] && VB=1500
if [ "$SINGLE" = "1" ]; then
  cp "$W/$N-voice-only.mp4" "$W/$N-canva-upload.mp4"
elif [ "$VT" = "1" ]; then
  $FFMPEG -y -loglevel error -i "$W/$N-voice-only.mp4" -c:v h264_videotoolbox -profile:v high -b:v ${VB}k -maxrate $((VB*4/3))k -bufsize $((VB*8/3))k -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart "$W/$N-canva-upload.mp4"
else
$FFMPEG -y -loglevel error -i "$W/$N-voice-only.mp4" -c:v libx264 -preset slow -tune animation -b:v ${VB}k -maxrate $((VB*4/3))k -bufsize $((VB*8/3))k -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart "$W/$N-canva-upload.mp4"
fi; lap "canva copy"
# the preview MP4 (voice + music) is shared and posted too: if it is 10 MB or more, re-encode it at the same capped bitrate
if [ "$LESSON" != "1" ] && [ "$(wc -c < "$W/$N.mp4")" -ge 10000000 ]; then
  if [ "$VT" = "1" ]; then
  $FFMPEG -y -loglevel error -i "$W/$N.mp4" -c:v h264_videotoolbox -profile:v high -b:v ${VB}k -maxrate $((VB*4/3))k -bufsize $((VB*8/3))k -pix_fmt yuv420p -c:a aac -ar 48000 -b:a 128k -movflags +faststart "$W/_small.mp4" && mv "$W/_small.mp4" "$W/$N.mp4"
  else
  $FFMPEG -y -loglevel error -i "$W/$N.mp4" -c:v libx264 -preset slow -tune animation -b:v ${VB}k -maxrate $((VB*4/3))k -bufsize $((VB*8/3))k -pix_fmt yuv420p -c:a aac -ar 48000 -b:a 128k -movflags +faststart "$W/_small.mp4" && mv "$W/_small.mp4" "$W/$N.mp4"
  fi; lap "10 MB re-encode"
fi
rm -f "$W/raw.mp4"; ls -la "$W/$N"*.mp4
