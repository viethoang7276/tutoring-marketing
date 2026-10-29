# Voiceover with Kokoro (voice af_heart). Run from tools/tts with its venv:
#   cd tools/tts && .venv/bin/python <skill>/scripts/vo.py <workdir> [speed=1.08] [gap=0.2]
# Reads <workdir>/beats.json (from build_scenes.py) or else <workdir>/script.json: [{"text", "img", "focus", "focus_end"?, "chunks": [{"text", "key"?}]}, ...]
# Writes <workdir>/voiceover.wav and <workdir>/timing.json: each beat gets start/end, and each caption chunk
# gets a start time spread over the beat's audio in proportion to its spoken length (Kokoro has no word timings).
import json, re, sys, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
d = sys.argv[1]; speed = float(sys.argv[2]) if len(sys.argv) > 2 else 1.08; gap = float(sys.argv[3]) if len(sys.argv) > 3 else 0.2
tail = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5   # silence after the last line (the end card stays up this long after the voice)
import os
ELEVEN = os.environ.get("TTS_ENGINE", "eleven") == "eleven"  # ElevenLabs v3 by default (Hoang, 29 Oct 2026); TTS_ENGINE=kokoro for the old voice
if ELEVEN:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import eleven_tts
else:
    k = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")
src = d + "/beats.json" if os.path.exists(d + "/beats.json") else d + "/script.json"
beats = json.load(open(src)); beats = beats["beats"] if isinstance(beats, dict) else beats; sr = 24000; lead = 0.15
out = [np.zeros(int(lead * sr), dtype=np.float32)]; t = lead
def w(s):  # spoken weight of a caption chunk: letters, numbers read as words
    s = re.sub(r"\$?([\d,]+)", lambda m: "x" * (8 * len(m.group(1).replace(",", "")) // 3 + 6), s)
    return max(1, len(re.sub(r"[^A-Za-z]", "", s)))
for b in beats:
    if ELEVEN:
        a, sr = eleven_tts.say(b.get("say") or b["text"], b.get("tempo")), eleven_tts.SR   # "tempo": per-beat pace (struggle lines slower)  # "say": TTS spelling override (e.g. Ed-lin-tics); captions and checks use "text"
    else:
        a, sr = k.create(b["text"], voice="af_heart", speed=speed, lang="en-us")
        a = a.astype(np.float32); nz = np.where(np.abs(a) > 0.01)[0]
        a = a[max(0, nz[0] - 600): nz[-1] + 1200] if len(nz) else a  # trim Kokoro's own silence
    n = int(0.03 * sr)   # 30 ms fade in and out per line, so a final consonant never ends on a hard gate
    if len(a) > 2 * n: a[:n] *= np.linspace(0, 1, n, dtype=np.float32); a[-n:] *= np.linspace(1, 0, n, dtype=np.float32)
    dur = len(a) / sr; b["start"] = round(t, 3); b["end"] = round(t + dur, 3)
    ws = [w(c["text"]) for c in b.get("chunks", [])]; tot = sum(ws) or 1; acc = 0
    for c, x in zip(b.get("chunks", []), ws): c["t"] = round(t + dur * acc / tot - 0.08, 3); acc += x
    g = float(b.get("gap", gap))   # a beat may ask for more room after its line ("gap": seconds), e.g. short hooks
    out.append(a); t += dur; out.append(np.zeros(int(g * sr), dtype=np.float32)); t += g
out.append(np.zeros(int(tail * sr), dtype=np.float32)); t += tail
sf.write(d + "/voiceover.wav", np.concatenate(out), sr)
json.dump({"duration": round(t, 2), "speed": speed, "beats": beats}, open(d + "/timing.json", "w"), indent=1)
print("duration", round(t, 2), [b["start"] for b in beats])
