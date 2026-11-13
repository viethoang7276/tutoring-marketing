# Packs scene art + beats + caption chunks into scenes.json for render.html.
# Usage: python3 make_scenes_json.py <workdir> <skill scripts dir>
#   <workdir>/timing.json  from vo.py: {"duration", "beats": [{img, focus, focus_end?, start, end, chunks:[{text, key?, t}]}]}
#   <workdir>/<img>.svg    1080x1920 scene art; art inside <g filter="url(#r)">…</g> (see scenes_example.py)
import json, re, sys
d, out = sys.argv[1], sys.argv[2]
T = json.load(open(f"{d}/timing.json")); scenes = {}
for b in T["beats"]:
    if not b.get("img") or b["img"] in scenes: continue
    svg = open(f"{d}/{b['img']}.svg").read()
    a = svg.find('<g filter="url(#r)">') + len('<g filter="url(#r)">'); z = svg.rfind('</g></svg>')
    body = svg[a:z]; wall = False
    m = re.match(r'\s*(<rect x="0" y="0" width="1080" height="1480"[^>]*/>)', body)
    if m: wall, body = True, body[m.end():]
    scenes[b["img"]] = {"body": body, "wall": wall}
layout = "reel"; env = []; nologo = False
try:
    _t = json.load(open(f"{d}/script.json")).get("meta", {}).get("type")
    if _t == "ledger-talks": layout = "talk"
    if _t == "ad": layout = "ad"   # paid ad: captions sit inside the central 4:5 safe area (Meta feed crop)
    nologo = _t == "lesson"   # in-lesson videos (5 Nov 2026): nothing promotional, so no logo on the frames or the cards
    # full-frame layout (opt-in, how-to reels, 1 Nov 2026): captions y 228-438, art x 40-940 y 450-1440, logo y 1462,
    # all inside the platform safe zones (top 220, bottom 380, right 140 px)
    if json.load(open(f"{d}/script.json")).get("meta", {}).get("layout") == "full" and layout == "reel": layout = "full"
    # ladder layout (opt-in, career-ladder reels, 12 Nov 2026): rung header y 228-446, art x 40-940 y 456-1294, captions y 1304-1520
    if json.load(open(f"{d}/script.json")).get("meta", {}).get("layout") == "ladder" and layout == "reel": layout = "ladder"
except Exception: pass
if layout == "talk":   # mouth open/closed at 12 fps from the voice loudness (lip sync for mood "talk")
    import numpy as np, soundfile as sf
    a, sr = sf.read(f"{d}/voiceover.wav", dtype="float32"); hop = sr // 12
    r = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) if len(a[i:i + hop]) else 0 for i in range(0, len(a), hop)])
    thr = 0.35 * np.percentile(r[r > 0], 90) if (r > 0).any() else 1
    env = [int(v > thr) for v in r]
    for k in range(1, len(env) - 1):   # a mouth that flaps every frame looks jittery: hold open frames for 2
        if env[k - 1] and not env[k] and env[k + 1]: env[k] = 1
data = {"duration": T["duration"], "scenes": scenes, "layout": layout, "env": env, "nologo": nologo,
        "beats": [{k: b[k] for k in ("img", "focus", "start", "end", "chunks", "role", "term", "keypoint", "definition", "footnote", "cta", "fx", "cam", "equation", "rung", "chips", "message", "tag") if k in b} for b in T["beats"]]}
if layout == "ladder": data["rungs"] = json.load(open(f"{d}/script.json")).get("meta", {}).get("rungs", [])   # rung titles for the header
if layout == "ladder" and json.load(open(f"{d}/script.json")).get("meta", {}).get("caption_pos") == "low": data["capLow"] = True   # bleed style, opt-in (13 Nov 2026): captions in the middle of the bottom half
if layout == "ladder" and json.load(open(f"{d}/script.json")).get("meta", {}).get("rung_label"): data["rungLabel"] = json.load(open(f"{d}/script.json"))["meta"]["rung_label"]   # map reels (13 Nov 2026, opt-in): header pill text such as "STOP {n} OF {N}"
if layout == "ladder" and json.load(open(f"{d}/script.json")).get("meta", {}).get("ladder_style") == "bleed": data["bleed"] = True   # full-bleed art, captions on top (13 Nov 2026)
try:   # meta.solid_cuts (7 Nov 2026, opt-in): every scene is complete on its first frame, no fade or draw-on at the cut. Without it, scenes.json is unchanged
    if json.load(open(f"{d}/script.json")).get("meta", {}).get("solid_cuts") is True: data["solidCuts"] = True
except Exception: pass
json.dump(data, open(f"{out}/scenes.json", "w")); print(len(data["beats"]), "beats,", len(scenes), "scenes")
