"""1-frame-per-second tile and an 8-frame contact sheet of a finished reel, for the visual check.
Usage: tools/tts/.venv/bin/python .claude/skills/edlintics-demo-reel/scripts/tiles.py REEL.mp4 OUT_DIR [--at 1.0,5.5,...]"""
import os, subprocess, sys, tempfile, glob
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
mp4, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True); ff = imageio_ffmpeg.get_ffmpeg_exe()
tmp = tempfile.mkdtemp()
subprocess.run([ff, "-v", "error", "-i", mp4, "-vf", "fps=1,scale=270:480", os.path.join(tmp, "f%03d.png")], check=True)
fs = sorted(glob.glob(os.path.join(tmp, "f*.png"))); cols = 8; rows = (len(fs) + cols - 1) // cols
T = Image.new("RGB", (cols * 270, rows * 500), "white"); d = ImageDraw.Draw(T)
for i, f in enumerate(fs):
    T.paste(Image.open(f), ((i % cols) * 270, (i // cols) * 500)); d.text(((i % cols) * 270 + 4, (i // cols) * 500 + 482), f"{i + 0.5:.1f}s", fill="black")
T.save(os.path.join(out, "tile-1fps.jpg"), quality=88)
ats = [float(x) for x in sys.argv[sys.argv.index("--at") + 1].split(",")] if "--at" in sys.argv else None
if ats:
    S = Image.new("RGB", (len(ats) * 540, 960), "white")
    for i, t in enumerate(ats):
        p = os.path.join(tmp, f"c{i}.png")
        subprocess.run([ff, "-v", "error", "-ss", str(t), "-i", mp4, "-frames:v", "1", "-vf", "scale=540:960", p], check=True)
        S.paste(Image.open(p), (i * 540, 0))
    S.save(os.path.join(out, "contact-sheet.jpg"), quality=90)
print("tiles in", out, len(fs), "s")
