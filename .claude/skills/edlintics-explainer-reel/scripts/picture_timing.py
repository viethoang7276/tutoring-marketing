"""Voice-free picture mode (PICTURE_ONLY=1 make_reel.sh, 7 Nov 2026): timings without the voice, in a side folder.

Usage: tools/tts/.venv/bin/python picture_timing.py <workdir> <outdir> [wpm=165]
Writes <outdir>/timing.json and links the scene art and script.json into <outdir>, so make_scenes_json.py, render.js,
postcheck.py and framefill.py run there. Nothing in <workdir> is written, so the real timing.json and audio stay as they are.
If <workdir>/timing.json is a real voice timing with the same beat count, it is reused with the new picture fields (exact
timings, like REUSE_AUDIO). Otherwise each beat lasts its spoken words at <wpm> (FA1 lessons measured ~161 wpm, reels
~195), with the chunks spread by spoken length as in vo.py, and the file says "estimated": true. No voice is made or paid for.
"""
import glob, json, os, re, sys
d, out = sys.argv[1], sys.argv[2]; wpm = float(sys.argv[3]) if len(sys.argv) > 3 else 165.0
os.makedirs(out, exist_ok=True)
B = json.load(open(f"{d}/beats.json")); B = B["beats"] if isinstance(B, dict) else B
T = None
if os.path.exists(f"{d}/timing.json"):
    R = json.load(open(f"{d}/timing.json"))
    if not R.get("estimated") and len(R["beats"]) == len(B): T = R
if T is not None:
    for t, b in zip(T["beats"], B):   # same picture fields as REUSE_AUDIO in make_reel.sh
        t.pop("cam", None); t.pop("rung", None); t.pop("chips", None)
        for k in ("img", "focus", "cam", "term", "keypoint", "definition", "equation", "footnote", "cta", "rung", "chips", "message", "tag"):
            if k in b: t[k] = b[k]
    print("picture timing: the real voice timings from timing.json")
else:
    def w(s):   # spoken weight of a caption chunk, as in vo.py
        s = re.sub(r"\$?([\d,]+)", lambda m: "x" * (8 * len(m.group(1).replace(",", "")) // 3 + 6), s)
        return max(1, len(re.sub(r"[^A-Za-z]", "", s)))
    t = 0.15
    for b in B:
        words = len(re.sub(r"\[[^\]]*\]", " ", b.get("say") or b.get("text", "")).split())
        dur = max(1.2, words * 60.0 / wpm)   # per-beat "tempo" is ignored: this is a picture check, not the final timing
        b["start"] = round(t, 3); b["end"] = round(t + dur, 3)
        ws = [w(c["text"]) for c in b.get("chunks", [])]; tot = sum(ws) or 1; acc = 0
        for c, x in zip(b.get("chunks", []), ws): c["t"] = round(t + dur * acc / tot - 0.08, 3); acc += x
        t += dur + float(b.get("gap", 0.2))
    t += 0.5
    T = {"duration": round(t, 2), "estimated": True, "wpm": wpm, "beats": B}
    print(f"picture timing: estimated at {wpm:g} wpm, {T['duration']} s (no voice)")
json.dump(T, open(f"{out}/timing.json", "w"), indent=1)
for f in glob.glob(f"{d}/*.svg") + [f"{d}/script.json"]:
    dst = f"{out}/{os.path.basename(f)}"
    if os.path.lexists(dst): os.remove(dst)
    os.symlink(os.path.abspath(f), dst)
