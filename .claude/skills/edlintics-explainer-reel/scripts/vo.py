# Voiceover with Kokoro (voice af_heart). Run from tools/tts with its venv:
#   cd tools/tts && .venv/bin/python <skill>/scripts/vo.py <workdir> [speed=1.08] [gap=0.2]
# Reads <workdir>/beats.json (from build_scenes.py) or else <workdir>/script.json: [{"text", "img", "focus", "focus_end"?, "chunks": [{"text", "key"?}]}, ...]
# Writes <workdir>/voiceover.wav and <workdir>/timing.json: each beat gets start/end, and each caption chunk
# gets a start time spread over the beat's audio in proportion to its spoken length (Kokoro has no word timings).
import json, re, sys, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
d = sys.argv[1]; speed = float(sys.argv[2]) if len(sys.argv) > 2 else 1.08; gap = float(sys.argv[3]) if len(sys.argv) > 3 else 0.2
k = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")
import os
src = d + "/beats.json" if os.path.exists(d + "/beats.json") else d + "/script.json"
beats = json.load(open(src)); beats = beats["beats"] if isinstance(beats, dict) else beats; sr = 24000; lead = 0.15
out = [np.zeros(int(lead * sr), dtype=np.float32)]; t = lead
def w(s):  # spoken weight of a caption chunk: letters, numbers read as words
    s = re.sub(r"\$?([\d,]+)", lambda m: "x" * (8 * len(m.group(1).replace(",", "")) // 3 + 6), s)
    return max(1, len(re.sub(r"[^A-Za-z]", "", s)))
for b in beats:
    a, sr = k.create(b["text"], voice="af_heart", speed=speed, lang="en-us")
    a = a.astype(np.float32); nz = np.where(np.abs(a) > 0.01)[0]
    a = a[max(0, nz[0] - 600): nz[-1] + 1200] if len(nz) else a  # trim Kokoro's own silence
    dur = len(a) / sr; b["start"] = round(t, 3); b["end"] = round(t + dur, 3)
    ws = [w(c["text"]) for c in b.get("chunks", [])]; tot = sum(ws) or 1; acc = 0
    for c, x in zip(b.get("chunks", []), ws): c["t"] = round(t + dur * acc / tot - 0.08, 3); acc += x
    out.append(a); t += dur; out.append(np.zeros(int(gap * sr), dtype=np.float32)); t += gap
out.append(np.zeros(int(0.5 * sr), dtype=np.float32)); t += 0.5
sf.write(d + "/voiceover.wav", np.concatenate(out), sr)
json.dump({"duration": round(t, 2), "speed": speed, "beats": beats}, open(d + "/timing.json", "w"), indent=1)
print("duration", round(t, 2), [b["start"] for b in beats])
