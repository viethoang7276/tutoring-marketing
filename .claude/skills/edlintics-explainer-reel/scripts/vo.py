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
def speech_segments(a, sr, thr=0.02, gap=0.28):
    """(start, end) seconds of the audible runs in a line, runs closer than `gap` merged"""
    win = int(0.03 * sr); env = np.convolve(np.abs(a), np.ones(win) / win, mode="same") > thr
    out = []; i = 0; n = len(env)
    while i < n:
        if env[i]:
            j = i
            while j < n and env[j]: j += 1
            if out and (i - out[-1][1]) / sr < gap: out[-1][1] = j
            else: out.append([i, j])
            i = j
        else: i += 1
    return [(x / sr, y / sr) for x, y in out]


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
    # pause-aware timing (29 Oct 2026): when the line's speech segments (pauses >= 0.28 s) match the chunks grouped by
    # sentence end (? . ! …), each group starts at its measured onset and spreads its chunks inside that segment
    segs = speech_segments(a, sr, gap=0.15); ch = b.get("chunks", [])
    groups, g = [], []
    for c in ch:
        g.append(c)
        if re.search(r"[?.!…]$", c["text"].strip()): groups.append(g); g = []
    if g: groups.append(g)
    while groups and len(segs) > len(groups):
        if any(e - s0 < 0.45 for s0, e in segs): segs.remove(min(segs, key=lambda q: q[1] - q[0]))   # a sigh or breath
        else:   # a pause inside a sentence: merge the two segments closest together
            k = min(range(len(segs) - 1), key=lambda i: segs[i + 1][0] - segs[i][1]); segs[k:k + 2] = [(segs[k][0], segs[k + 1][1])]
    if groups and len(segs) == len(groups):
        for (s0, e), grp in zip(segs, groups):
            gw = [w(c["text"]) for c in grp]; gt = sum(gw) or 1; ga = 0
            for c, x in zip(grp, gw): c["t"] = round(t + s0 + (e - s0) * ga / gt - 0.08, 3); ga += x
    g = float(b.get("gap", gap))   # a beat may ask for more room after its line ("gap": seconds), e.g. short hooks
    out.append(a); t += dur; out.append(np.zeros(int(g * sr), dtype=np.float32)); t += g
out.append(np.zeros(int(tail * sr), dtype=np.float32)); t += tail
sf.write(d + "/voiceover.wav", np.concatenate(out), sr)
json.dump({"duration": round(t, 2), "speed": speed, "beats": beats}, open(d + "/timing.json", "w"), indent=1)
print("duration", round(t, 2), [b["start"] for b in beats])
