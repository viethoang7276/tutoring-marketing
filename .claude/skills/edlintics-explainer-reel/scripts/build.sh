#!/bin/bash
# Renders the reel (headless Chrome, 24 fps, pencil boil + draw-on) and encodes standard MP4s.
# Usage: build.sh <workdir> <name>      (expects scenes.json in this folder, audio-voice.wav + audio.wav in <workdir>)
set -e
cd "$(dirname "$0")"
REPO="$(cd ../../../.. && pwd)"
PY="$REPO/tools/tts/.venv/bin/python"
export FFMPEG=$($PY -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
[ -d node_modules ] || npm install --no-audit --no-fund >/dev/null
W="$1"; N="$2"
node render.js video "$W/raw.mp4" "$W/audio-voice.wav"
$FFMPEG -y -loglevel error -i "$W/raw.mp4" -vf "scale=in_range=pc:out_range=tv,format=yuv420p" -c:v libx264 -preset medium -crf 20 -c:a aac -ar 48000 -b:a 160k -movflags +faststart "$W/$N-voice-only.mp4"
$FFMPEG -y -loglevel error -i "$W/$N-voice-only.mp4" -i "$W/audio.wav" -map 0:v -map 1:a -c:v copy -c:a aac -ar 48000 -b:a 160k -movflags +faststart -shortest "$W/$N.mp4"
# Canva upload copy: the Chrome file bridge takes at most 10 MB
$FFMPEG -y -loglevel error -i "$W/$N-voice-only.mp4" -c:v libx264 -preset slow -tune animation -b:v 1500k -maxrate 2000k -bufsize 4000k -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart "$W/$N-canva-upload.mp4"
rm "$W/raw.mp4"; ls -la "$W/$N"*.mp4
