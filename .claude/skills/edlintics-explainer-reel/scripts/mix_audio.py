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
voice = vo + fx; voice /= max(1.0, np.abs(voice).max() / 0.98)
sf.write(f"{d}/audio-voice.wav", voice, sr)
chords = [[220, 277.18, 329.63], [196, 246.94, 293.66], [174.61, 220, 261.63], [196, 246.94, 293.66]]
pad = np.zeros(N, dtype=np.float32)
for k in range(int(dur // 4) + 1):
    t0 = k * 4.0; m = (t >= t0) & (t < t0 + 4.6); tt = t[m] - t0
    env = np.clip(tt / 1.2, 0, 1) * np.clip((4.6 - tt) / 1.4, 0, 1)
    for f in chords[k % 4]: pad[m] += env * (0.5 * np.sin(2 * np.pi * f * tt) + 0.15 * np.sin(2 * np.pi * 2.002 * f * tt))
pad /= np.abs(pad).max() + 1e-9
mix = voice + 0.06 * pad * np.clip(t / 1.0, 0, 1) * np.clip((dur - t) / 1.0, 0, 1)
sf.write(f"{d}/audio.wav", mix / max(1.0, np.abs(mix).max() / 0.98), sr)
print("ok", dur)
