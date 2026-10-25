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
data = {"duration": T["duration"], "scenes": scenes,
        "beats": [{k: b[k] for k in ("img", "focus", "start", "end", "chunks", "role", "term", "keypoint") if k in b} for b in T["beats"]]}
json.dump(data, open(f"{out}/scenes.json", "w")); print(len(data["beats"]), "beats,", len(scenes), "scenes")
