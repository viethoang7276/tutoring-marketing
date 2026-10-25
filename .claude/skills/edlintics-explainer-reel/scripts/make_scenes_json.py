# Packs scene art + captions into scenes.json for render.html.
# Usage: python3 make_scenes_json.py <workdir> <skill scripts dir>
#   <workdir>/timing.json  scenes [{text, cap, img, start, dy?}] (cap = on-screen caption, short full sentence, no trailing full stop)
#   <workdir>/<img>.svg    1080x1920 scene art; art inside <g filter="url(#r)">…</g> (see scenes_example.py)
#   <workdir>/hook.json    optional {"cap": "Why keep paying for bad decisions?", "until": 3.5}
import json, os, re, sys
d, out = sys.argv[1], sys.argv[2]
T = json.load(open(f"{d}/timing.json")); scenes = []
for s in T["scenes"]:
    svg = open(f"{d}/{s['img']}.svg").read()
    a = svg.find('<g filter="url(#r)">') + len('<g filter="url(#r)">'); b = svg.rfind('</g></svg>')
    body = svg[a:b]; wall = ""
    m = re.match(r'\s*(<rect x="0" y="0" width="1080" height="1480"[^>]*/>)', body)
    if m: wall, body = m.group(1), body[m.end():]
    scenes.append({"start": s["start"], "cap": s["cap"], "body": body, "wall": wall, "dy": s.get("dy", 0)})
data = {"duration": T["duration"], "scenes": scenes}
if os.path.exists(f"{d}/hook.json"): data["hook"] = json.load(open(f"{d}/hook.json"))
json.dump(data, open(f"{out}/scenes.json", "w")); print(len(scenes), "scenes")
