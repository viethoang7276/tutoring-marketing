#!/bin/bash
# Renders one time range of a built reel with its audio, for pilots and quick checks (6 Nov 2026).
# Usage: render_range.sh <workdir> <t0> <t1> <out.mp4> [audio=audio.wav]   (run make_reel.sh with STILLS_ONLY=1 first, so scenes.json exists)
set -e
cd "$(dirname "$0")"
REPO="$(cd ../../../.. && pwd)"; PY="$REPO/tools/tts/.venv/bin/python"
export FFMPEG=$($PY -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
W="$1"; T0="$2"; T1="$3"; OUT="$4"; AUD="${5:-$W/audio.wav}"
read A0 AD < <($PY -c "import math;k0=math.ceil($T0*24-1e-6);k1=math.ceil($T1*24-1e-6);print(k0/24,(k1-k0)/24)")
SCENES="$W/scenes.json" node render.js range "$W/_range.mp4" "$T0" "$T1"
$FFMPEG -y -loglevel error -i "$W/_range.mp4" -ss "$A0" -t "$AD" -i "$AUD" -map 0:v -map 1:a -c:v copy -c:a aac -ar 48000 -b:a 160k -movflags +faststart -shortest "$OUT"
rm "$W/_range.mp4"; ls -la "$OUT"
