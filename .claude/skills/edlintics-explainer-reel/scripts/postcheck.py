"""After the build: check the MP4s and make a contact sheet of one still per beat.

Usage: tools/tts/.venv/bin/python postcheck.py <workdir> <slug>
Fails (exit 1) if the video isn't 1080x1920, has no audio, its length is off from timing.json by more than
0.5 s, or the Canva upload copy is 10 MB or more. Writes <workdir>/<slug>-contact-sheet.png from <workdir>/stills.
"""
import glob, json, os, re, subprocess, sys
import imageio_ffmpeg
from PIL import Image, ImageDraw

d, slug = sys.argv[1], sys.argv[2]; FF = imageio_ffmpeg.get_ffmpeg_exe(); E = []
T = json.load(open(f"{d}/timing.json"))
def probe(f):
    r = subprocess.run([FF, "-hide_banner", "-i", f], capture_output=True, text=True).stderr
    dur = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r); res = re.search(r"Video: .*?(\d{3,4})x(\d{3,4})", r)
    return (int(dur[1]) * 3600 + int(dur[2]) * 60 + float(dur[3]) if dur else 0), (res.groups() if res else None), ("Audio:" in r), ("yuv420p" in r)
for name in (f"{slug}.mp4", f"{slug}-voice-only.mp4", f"{slug}-canva-upload.mp4"):
    f = f"{d}/{name}"
    if not os.path.exists(f): E.append(f"missing {name}"); continue
    dur, res, aud, yuv = probe(f)
    if res != ("1080", "1920"): E.append(f"{name}: resolution {res}, expected 1080x1920")
    if not aud: E.append(f"{name}: no audio stream")
    if not yuv: E.append(f"{name}: not yuv420p")
    if abs(dur - T["duration"]) > 0.5: E.append(f"{name}: {dur:.2f} s but timing.json says {T['duration']} s")
    print(f"{name}: {dur:.2f} s, {res}, audio {aud}, {os.path.getsize(f) / 1e6:.1f} MB")
cu = f"{d}/{slug}-canva-upload.mp4"
if os.path.exists(cu) and os.path.getsize(cu) >= 10e6: E.append("canva upload copy is 10 MB or more; the Chrome file bridge refuses it")
stills = sorted(glob.glob(f"{d}/stills/still-*.png"), key=lambda p: float(re.search(r"still-([\d.]+)\.png", p)[1]))
if stills:
    tw, th, cols = 270, 480, min(6, len(stills)); rows = (len(stills) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 10) + 10, rows * (th + 34) + 10), "#E6E8EC"); dr = ImageDraw.Draw(sheet)
    for k, p in enumerate(stills):
        im = Image.open(p).convert("RGB").resize((tw, th)); x = 10 + (k % cols) * (tw + 10); y = 10 + (k // cols) * (th + 34)
        sheet.paste(im, (x, y)); dr.text((x, y + th + 6), f"beat {k + 1}  t={re.search(r'still-([\d.]+)', p)[1]}s", fill="#0F172A")
    sheet.save(f"{d}/{slug}-contact-sheet.png"); print("contact sheet:", f"{d}/{slug}-contact-sheet.png")
else:
    E.append("no stills found for the contact sheet")
for e in E: print("FAIL ", e)
print("POSTCHECK", "OK" if not E else "NOT OK"); sys.exit(1 if E else 0)
