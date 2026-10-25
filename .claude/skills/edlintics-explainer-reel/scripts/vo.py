# Voiceover with Kokoro (voice af_heart). Run from tools/tts with its venv:
#   cd tools/tts && .venv/bin/python <skill>/scripts/vo.py <workdir>
# Reads <workdir>/script.json: [{"text": "...", "cap": "...", "img": "s1"}, ...]
# Writes <workdir>/voiceover.wav and <workdir>/timing.json (scene start times).
import json, sys, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
d = sys.argv[1]; k = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")
s = json.load(open(d + "/script.json")); out = []; t = 0.6; sr = 24000; starts = []
out.append(np.zeros(int(0.6 * sr), dtype=np.float32))
for sc in s:
    a, sr = k.create(sc["text"], voice="af_heart", speed=1.0, lang="en-us")
    starts.append(round(t, 2)); out.append(a.astype(np.float32)); t += len(a) / sr
    out.append(np.zeros(int(0.45 * sr), dtype=np.float32)); t += 0.45
out.append(np.zeros(int(0.8 * sr), dtype=np.float32)); t += 0.8
sf.write(d + "/voiceover.wav", np.concatenate(out), sr)
for i, sc in enumerate(s): sc["start"] = starts[i]
json.dump({"duration": round(t, 2), "scenes": s}, open(d + "/timing.json", "w"), indent=1)
print(round(t, 2), starts)
