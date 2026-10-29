"""Frame checks on a built reel or ad (reviewer rules, 29 Oct 2026): no near-blank or half-drawn frame after a cut.

Usage: tools/tts/.venv/bin/python cutcheck.py <workdir> <slug> [fps=4]
Reads <workdir>/timing.json and <workdir>/<slug>.mp4 (the preview with captions). For every cut it decodes the cut frame,
the next two frames and a steady frame 12 frames later, measures the ink coverage of the art box (y 530-1310: share of
pixels darker than the paper) and FAILS if a first frame has less than 85% of the steady frame's ink. It also writes
<workdir>/review/fps-<n>.png (one still every 1/fps s, as sheets of 8) and <workdir>/review/cuts-pm2.png (every cut
at -2..+2 frames). Exit code 1 on a failure.
"""
import json, os, subprocess, sys
import imageio_ffmpeg, numpy as np
from PIL import Image, ImageDraw

FF = imageio_ffmpeg.get_ffmpeg_exe(); FPS = 24


def frame(mp4, k):
    """Decode frame k (0-based) of mp4 as an RGB array."""
    p = subprocess.run([FF, "-v", "error", "-i", mp4, "-vf", f"select=eq(n\\,{k})", "-vframes", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True)
    return np.frombuffer(p.stdout, dtype=np.uint8).reshape(1920, 1080, 3)


def ink(im):
    box = im[530:1310, 40:1040].astype(int)
    return float((box.min(axis=2) < 150).mean())


def sheet(frames, labels, path, tw=216, th=384, per=8):
    rows = (len(frames) + per - 1) // per
    s = Image.new("RGB", (per * (tw + 6) + 6, rows * (th + 30) + 6), "#E6E8EC"); d = ImageDraw.Draw(s)
    for i, (f, l) in enumerate(zip(frames, labels)):
        x, y = 6 + (i % per) * (tw + 6), 6 + (i // per) * (th + 30)
        s.paste(Image.fromarray(f).resize((tw, th)), (x, y)); d.text((x, y + th + 8), l, fill="#0F172A")
    s.save(path)


def main(w, slug, fps=4):
    T = json.load(open(f"{w}/timing.json")); mp4 = f"{w}/{slug}.mp4"; os.makedirs(f"{w}/review", exist_ok=True)
    cuts = [int(np.ceil((b["start"] - 0.08) * FPS - 1e-6)) for b in T["beats"][1:]]
    N = int(T["duration"] * FPS); bad = []
    print("cut  frame   ink k / k+1 / k+2  vs steady (k+12)")
    pm = []; pml = []
    for k in cuts:
        f = {j: frame(mp4, k + j) for j in range(-2, 3)}; steady = frame(mp4, min(k + 12, N - 1))
        s = ink(steady); vals = [ink(f[0]), ink(f[1]), ink(f[2])]
        flag = any(v < 0.85 * s for v in vals)
        print(f"{k / FPS:6.3f} {k:5d}   {vals[0]:.4f} / {vals[1]:.4f} / {vals[2]:.4f}  vs {s:.4f}  {'FAIL' if flag else 'ok'}")
        if flag: bad.append(k)
        for j in range(-2, 3): pm.append(f[j]); pml.append(f"cut {k / FPS:.3f}s  {j:+d}f")
    sheet(pm, pml, f"{w}/review/cuts-pm2.png", per=10)
    ks = list(range(0, N, max(1, FPS // fps)))
    sheet([frame(mp4, k) for k in ks], [f"{k / FPS:.2f}s" for k in ks], f"{w}/review/fps-{fps}.png")
    print("sheets:", f"{w}/review/cuts-pm2.png", f"{w}/review/fps-{fps}.png")
    print("CUTCHECK", "OK" if not bad else f"NOT OK at frames {bad}"); sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 4)
