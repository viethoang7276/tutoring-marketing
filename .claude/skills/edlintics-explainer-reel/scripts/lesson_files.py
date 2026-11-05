"""In-lesson video extras (meta.type "lesson", 5 Nov 2026), written next to the MP4 by make_reel.sh.

Usage: tools/tts/.venv/bin/python lesson_files.py <workdir> <slug>
Reads <workdir>/timing.json (vo.py) and writes:
  <slug>.vtt             WebVTT captions: one cue per caption chunk, from its start to the next chunk (or the end of its line);
                         defcard lines have no chunks, so their spoken text is split into cues of up to 7 words over the line
  <slug>-transcript.txt  the "Read instead" text: the spoken sentences ("text", never "say", [tags] dropped) in order, one
                         paragraph per run of beats with the same role, and each defcard as its term and definition on their
                         own lines. No full stop at the end of a paragraph (house rule)
"""
import json, re, sys
d, slug = sys.argv[1], sys.argv[2]
T = json.load(open(f"{d}/timing.json")); B = T["beats"]
clean = lambda s: " ".join(re.sub(r"\[[^\]]*\]", " ", s).split())
ts = lambda x: f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{x % 60:06.3f}"
cues = []
for b in B:
    ch = [c for c in b.get("chunks", []) if c.get("text")]
    if ch:
        for k, c in enumerate(ch):
            a = max(b["start"], c["t"]) if k else min(b["start"], max(0, c["t"]))
            z = ch[k + 1]["t"] if k + 1 < len(ch) else b["end"]
            cues.append([a, max(z, a + 0.3), c["text"]])
    else:
        w = clean(b.get("text", "")).split(); n = max(1, -(-len(w) // 7)); parts = [" ".join(w[len(w) * i // n: len(w) * (i + 1) // n]) for i in range(n)]
        tot = sum(len(p) for p in parts) or 1; acc = 0; dur = b["end"] - b["start"]
        for p in parts:
            cues.append([b["start"] + dur * acc / tot, b["start"] + dur * (acc + len(p)) / tot, p]); acc += len(p)
for k in range(len(cues) - 1): cues[k][1] = min(cues[k][1], cues[k + 1][0])   # no overlaps
with open(f"{d}/{slug}.vtt", "w") as f:
    f.write("WEBVTT\n\n")
    for k, (a, z, x) in enumerate(cues, 1): f.write(f"{k}\n{ts(a)} --> {ts(z)}\n{x}\n\n")
paras, run, role = [], [], None
for b in B:
    if b.get("role") == "defcard":
        if run: paras.append(" ".join(run)); run = []
        paras.append(b.get("term", "") + "\n" + clean(b.get("definition", ""))); role = None; continue
    if b.get("role") != role and run: paras.append(" ".join(run)); run = []
    run.append(clean(b.get("text", ""))); role = b.get("role")
if run: paras.append(" ".join(run))
paras = ["\n".join(ln.rstrip().rstrip(".") for ln in p.split("\n")) for p in paras]
open(f"{d}/{slug}-transcript.txt", "w").write("\n\n".join(paras) + "\n")
print(f"lesson files: {d}/{slug}.vtt ({len(cues)} cues), {d}/{slug}-transcript.txt ({len(paras)} paragraphs)")
