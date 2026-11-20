#!/usr/bin/env python3
"""Demo video A as a film: every scene of frames_a.py animated over time, voiced, 1080x1920 at 30 fps.

Scenes live in anim_a1.py (A1..A4, T1..T3) and anim_a2.py (T4..T7, A5..A8). Each is fn(t, dur) -> (svg_inner, background),
t in seconds from the start of the scene, dur its length from TIMELINE below.

Run with tools/tts/.venv/bin/python (needs Pillow, numpy, soundfile, imageio-ffmpeg); FILM_OUT names the work folder.
  film_a.py stills A2 [n]     n evenly spaced frames of one scene (default 10) as PNGs plus <scene>-sheet.png
  film_a.py at A2 1.5,3.2     frames of one scene at those seconds, full size
  film_a.py clip A2 [T2 ...]  silent MP4 of just those scenes, for checking motion
  film_a.py render            the whole film with voice -> demo-a.mp4
"""
import importlib, json, math, os, shutil, subprocess, sys
import numpy as np, soundfile as sf, imageio_ffmpeg
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.environ.get('FILM_OUT', os.path.join(HERE, 'film-out'))
W, H, FPS = 1080, 1920, 30
import timeline_a
from timeline_a import DUR
VER = os.environ.get('FILM_VER', 'a')
TIMELINE = timeline_a.TIMELINE_B if VER == 'b' else timeline_a.TIMELINE
VOICE = timeline_a.VOICE_B if VER == 'b' else timeline_a.VOICE


def scenes():
    s = {}
    for m in ('anim_a1', 'anim_a2'):
        try:
            s.update(importlib.import_module(m).SCENES)
        except ModuleNotFoundError as e:
            if e.name != m:
                raise
    return s


def svg(fn, t, dur):
    inner, bg = fn(t, dur)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>{inner}</svg>')


def write(folder, items):
    """items: (scene, t). Writes numbered SVGs into a fresh folder."""
    S = scenes()
    shutil.rmtree(folder, ignore_errors=True); os.makedirs(folder)
    for i, (name, t) in enumerate(items):
        open(os.path.join(folder, f'{i:06d}.svg'), 'w').write(svg(S[name], t, DUR[name]))


def node(*args):
    env = dict(os.environ, FFMPEG=imageio_ffmpeg.get_ffmpeg_exe())
    subprocess.run(['node', os.path.join(HERE, 'render_frames.cjs'), *[str(a) for a in args]], check=True, env=env)


def frames_of(names):
    items = []
    for n in names:
        k = round(DUR[n] * FPS)
        items += [(n, i / FPS) for i in range(k)]
    return items


def voice_track(total):
    vdir = os.path.join(OUT, 'voice')
    a = np.zeros(int(total * 24000) + 24000, dtype=np.float32)
    for n, t0 in VOICE:
        x, sr = sf.read(os.path.join(vdir, f'{n}.wav'), dtype='float32'); assert sr == 24000
        i = int(t0 * sr); a[i:i + len(x)] += x
    out = os.path.join(OUT, 'voice.wav'); sf.write(out, a[:int(total * 24000)], 24000)
    return out


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    mode, args = sys.argv[1], sys.argv[2:]
    if mode in ('stills', 'at'):
        name = args[0]
        if mode == 'stills':
            n = int(args[1]) if len(args) > 1 else 10
            ts = [DUR[name] * i / (n - 1) * 0.999 for i in range(n)]
        else:
            ts = [float(x) for x in args[1].split(',')]
        folder = os.path.join(OUT, f'stills-{name}')
        write(folder, [(name, t) for t in ts]); node('png', folder)
        for i, t in enumerate(ts):
            os.replace(os.path.join(folder, f'{i:06d}.png'), os.path.join(folder, f'{name}-{t:05.2f}.png'))
            os.remove(os.path.join(folder, f'{i:06d}.svg'))
        if mode == 'stills':
            tw, th = 270, 480
            im = Image.new('RGB', (tw * min(5, n), th * math.ceil(n / 5)), 'white')
            for i, t in enumerate(ts):
                im.paste(Image.open(os.path.join(folder, f'{name}-{t:05.2f}.png')).convert('RGB').resize((tw - 4, th - 4), Image.Resampling.LANCZOS),
                         ((i % 5) * tw + 2, (i // 5) * th + 2))
            im.save(os.path.join(OUT, f'{name}-sheet.png')); print(os.path.join(OUT, f'{name}-sheet.png'))
        print(folder)
    elif mode == 'clip':
        folder = os.path.join(OUT, 'frames-clip')
        write(folder, frames_of(args)); out = os.path.join(OUT, f'clip-{"-".join(args)}.mp4')
        node('video', folder, out, FPS); shutil.rmtree(folder); print(out)
    elif mode == 'render':
        folder = os.path.join(OUT, 'frames')
        write(folder, frames_of([n for n, _ in TIMELINE]))
        total = sum(d for _, d in TIMELINE); out = os.path.join(OUT, f'demo-a-{VER}.mp4')
        node('video', folder, out, FPS, voice_track(total)); shutil.rmtree(folder); print(out, total, 's')
