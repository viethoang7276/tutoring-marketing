"""After build.sh: mix the two music beds, write the -final and -youtube copies and the poster.
Usage: tools/tts/.venv/bin/python finish.py <outdir> <slug>   (run through quiet-run.sh)"""
import glob, os, re, subprocess, sys
from PIL import Image
import imageio_ffmpeg
REPO = "/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing"; HERE = os.path.dirname(os.path.abspath(__file__))
W, sid = sys.argv[1:3]; work = f"{W}/work-{sid}-voice"; M = f"{REPO}/assets/renders/money-reels/music"
for bed, out in ((f"{M}/light-minimal-ambient-bed.wav", "final"), (f"{M}/youtube-sleep-music-no1-bed.wav", "youtube")):
    subprocess.run([sys.executable, f"{HERE}/mixbed.py", f"{work}/audio.wav", f"{W}/puzzle-reel-{sid}.mp4", bed, f"{W}/puzzle-reel-{sid}-{out}.mp4"], check=True)
st = sorted(glob.glob(f"{work}/stills/still-*.png"), key=lambda f: float(re.search(r"still-([\d.]+)\.png", f).group(1)))
Image.open(st[1]).convert("RGB").resize((540, 960), Image.LANCZOS).save(f"{W}/poster-{sid}.jpg", quality=88)
r = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-i", f"{W}/puzzle-reel-{sid}-final.mp4"], capture_output=True, text=True).stderr
m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r); print("duration", round(int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]), 2))
