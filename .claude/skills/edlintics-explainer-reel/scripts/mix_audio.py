# Makes audio-voice.wav (voice + soft cut effects, for Canva where the music is added) and
# audio.wav (the same plus a quiet generated pad, for local preview). All sound is generated here: no licensed audio.
# Usage: tools/tts/.venv/bin/python mix_audio.py <workdir>
# Effects: a soft whoosh at every new scene, a light tick at every reframe of the same scene, kept ~20 dB under the voice.
import json, sys, numpy as np, soundfile as sf
d = sys.argv[1]; T = json.load(open(f"{d}/timing.json")); dur = T["duration"]
vo, sr = sf.read(f"{d}/voiceover.wav", dtype="float32")
N = int(dur * sr); vo = np.pad(vo, (0, max(0, N - len(vo))))[:N]; t = np.arange(N) / sr
rng = np.random.default_rng(3); fx = np.zeros(N, dtype=np.float32)
def whoosh(at, L=0.32):
    n = int(L * sr); x = rng.standard_normal(n).astype(np.float32); env = np.sin(np.linspace(0, np.pi, n)) ** 2
    for _ in range(3): x = np.convolve(x, np.ones(6) / 6, mode="same")   # soften the noise
    i = int(max(0, at - L * 0.6) * sr); fx[i:i + n] += 0.9 * env[:N - i] * x[:N - i]
def tick(at):
    n = int(0.07 * sr); tt = np.arange(n) / sr; x = np.sin(2 * np.pi * 880 * tt) * np.exp(-tt * 60)
    i = int(at * sr); fx[i:i + n] += 0.5 * x[:N - i]
prev = None
for k, b in enumerate(T.get("beats", [])):
    if k == 0: prev = b.get("img"); continue
    (whoosh if b.get("img") != prev else tick)(b["start"] - 0.08); prev = b.get("img")
fx *= 0.1 * np.abs(vo).max() / (np.abs(fx).max() + 1e-9)
import os
TALK = False
try: TALK = json.load(open(f"{d}/script.json")).get("meta", {}).get("type") == "ledger-talks"
except Exception: pass
if TALK: fx[:] = 0   # ledger-talks: voice only, like a talking-head video (jump cuts, no whoosh, no music)
voice = vo + fx; voice /= max(1.0, np.abs(voice).max() / 0.98)
sf.write(f"{d}/audio-voice.wav", voice, sr)
chords = [[220, 277.18, 329.63], [196, 246.94, 293.66], [174.61, 220, 261.63], [196, 246.94, 293.66]]
pad = np.zeros(N, dtype=np.float32)
for k in range(int(dur // 4) + 1):
    t0 = k * 4.0; m = (t >= t0) & (t < t0 + 4.6); tt = t[m] - t0
    env = np.clip(tt / 1.2, 0, 1) * np.clip((4.6 - tt) / 1.4, 0, 1)
    for f in chords[k % 4]: pad[m] += env * (0.5 * np.sin(2 * np.pi * f * tt) + 0.15 * np.sin(2 * np.pi * 2.002 * f * tt))
pad /= np.abs(pad).max() + 1e-9
mix = voice + (0 if TALK else 0.025) * pad * np.clip(t / 1.0, 0, 1) * np.clip((dur - t) / 1.0, 0, 1)
sf.write(f"{d}/audio.wav", mix / max(1.0, np.abs(mix).max() / 0.98), sr)
print("ok", dur)
# Music bed (1 Nov 2026, opt-in): MUSIC_BED=<48 kHz stereo wav> replaces the generated pad in audio.wav with a real bed, mixed
# like the 1 Nov list reels: the bed MUSIC_BELOW_LU (default 12) under the voice, the whole mix at MUSIC_LUFS (default -17.5)
# integrated, soft limiter at -1 dBFS. audio-voice.wav (Canva copy) stays voice only. Without MUSIC_BED nothing changes.
if os.environ.get("MUSIC_BED") and not TALK:
    import re, subprocess, imageio_ffmpeg
    FF = imageio_ffmpeg.get_ffmpeg_exe()
    def _lufs(f):
        r = subprocess.run([FF, "-hide_banner", "-nostats", "-i", f, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
        r = r[r.rfind("Summary:"):]
        return float(re.search(r"I:\s+(-?[\d.]+) LUFS", r)[1]), float(re.search(r"Peak:\s+(-?[\d.inf]+) dBFS", r)[1])
    v48 = f"{d}/_v48.wav"
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", f"{d}/audio-voice.wav", "-ar", "48000", "-ac", "2", v48], check=True)
    v2, _ = sf.read(v48, dtype="float32"); bed, bsr = sf.read(os.environ["MUSIC_BED"], dtype="float32")
    assert bsr == 48000 and bed.ndim == 2, "MUSIC_BED must be 48 kHz stereo"
    n = len(v2)
    if len(bed) < n: bed = np.concatenate([bed] * (n // len(bed) + 1))
    bed = bed[:n].copy(); tb = np.arange(n) / 48000
    bed *= (np.clip(tb / 0.6, 0, 1) * np.clip((tb[-1] - tb) / 1.0, 0, 1))[:, None]
    sf.write(f"{d}/_bed.wav", bed, 48000)
    Iv, _ = _lufs(v48); Ib, _ = _lufs(f"{d}/_bed.wav"); below = float(os.environ.get("MUSIC_BELOW_LU", 12))
    sf.write(f"{d}/_mix.wav", np.clip(v2 + 10 ** ((Iv - below - Ib) / 20) * bed, -1, 1), 48000)
    target = float(os.environ.get("MUSIC_LUFS", -17.5)); I, _ = _lufs(f"{d}/_mix.wav"); gain = target - I
    for _ in range(5):
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", f"{d}/_mix.wav", "-af", f"volume={gain:.2f}dB,alimiter=limit=0.89:attack=4:release=60:level=0",
                        "-ar", "48000", "-ac", "2", f"{d}/audio.wav"], check=True)
        I2, pk = _lufs(f"{d}/audio.wav")
        if abs(I2 - target) < 0.25: break
        gain += target - I2
    for f in ("_v48", "_bed", "_mix"): os.remove(f"{d}/{f}.wav")
    print(f"music bed: voice {Iv:.1f} LUFS, bed {below:g} LU under, mix {I2:.1f} LUFS, peak {pk:.1f} dBFS ({os.path.basename(os.environ['MUSIC_BED'])})")
