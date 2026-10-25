# Makes audio-voice.wav (voice only, for Canva) and audio.wav (voice + quiet generated pad, local preview).
# Usage: tools/tts/.venv/bin/python mix_audio.py <workdir>
import json, sys, numpy as np, soundfile as sf
d = sys.argv[1]; T = json.load(open(f"{d}/timing.json")); dur = T["duration"]
vo, sr = sf.read(f"{d}/voiceover.wav", dtype="float32")
N = int(dur * sr); vo = np.pad(vo, (0, max(0, N - len(vo))))[:N]; t = np.arange(N) / sr
sf.write(f"{d}/audio-voice.wav", vo, sr)
chords = [[220, 277.18, 329.63], [196, 246.94, 293.66], [174.61, 220, 261.63], [196, 246.94, 293.66]]
pad = np.zeros(N, dtype=np.float32)
for k in range(int(dur // 4) + 1):
    t0 = k * 4.0; m = (t >= t0) & (t < t0 + 4.6); tt = t[m] - t0
    env = np.clip(tt / 1.2, 0, 1) * np.clip((4.6 - tt) / 1.4, 0, 1)
    for f in chords[k % 4]: pad[m] += env * (0.5 * np.sin(2 * np.pi * f * tt) + 0.15 * np.sin(2 * np.pi * 2.002 * f * tt))
pad /= np.abs(pad).max() + 1e-9
mix = vo + 0.06 * pad * np.clip(t / 1.5, 0, 1) * np.clip((dur - t) / 2.0, 0, 1)
sf.write(f"{d}/audio.wav", mix / max(1.0, np.abs(mix).max() / 0.98), sr)
