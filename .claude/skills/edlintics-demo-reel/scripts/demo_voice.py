"""Voice for an Edlintics demo reel: one ElevenLabs clip per script line, laid end to end with a gap.
Writes <out>/voice.wav (24 kHz mono) and <out>/timings.json (start/end in seconds of every line, total length).
Usage: tools/tts/.venv/bin/python .claude/skills/edlintics-demo-reel/scripts/demo_voice.py SPEC.json OUT_DIR
Clips are cached by eleven_tts.py, so re-running costs no credits unless a line changes"""
import json, os, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../edlintics-explainer-reel/scripts"))
import eleven_tts

spec = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
SR = eleven_tts.SR
tag = spec.get("tag", "")
t = float(spec.get("lead_in", 0.5)); gap = float(spec.get("gap", 0.45))
chunks, lines = [np.zeros(int(t * SR), np.float32)], []
for i, ln in enumerate(spec["lines"]):
    a = eleven_tts.say((tag + " " if tag else "") + ln["say"], tempo=spec.get("tempo", 1.0), voice=spec.get("voice"))
    d = len(a) / SR
    lines.append({"i": i, "start": round(t, 3), "end": round(t + d, 3)})
    chunks += [a, np.zeros(int(gap * SR), np.float32)]
    t += d + gap
tail = float(spec.get("tail", 0.6))
chunks.append(np.zeros(int(tail * SR), np.float32))
audio = np.concatenate(chunks)
pk = np.abs(audio).max() or 1
audio = audio * min(1.0, 0.89 / pk)   # about -1 dBFS peak
with wave.open(os.path.join(out, "voice.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(audio, -1, 1) * 32767).astype("<i2").tobytes())
json.dump({"lines": lines, "total": round(len(audio) / SR, 3)}, open(os.path.join(out, "timings.json"), "w"), indent=1)
print(json.dumps(lines), "total", round(len(audio) / SR, 2))
