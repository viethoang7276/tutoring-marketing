"""Write the thumbnail spec of a career-ladder reel for make_thumbnail.py (skill edlintics-ladder-reel).
Usage: python thumbnail_spec.py <slug> "<From *first role* to *top role*>" <outfit1,outfit2,outfit3,outfit4,outfit5> <BOTTOM TAG> <TOP TAG> <out.json>
Example: python thumbnail_spec.py ladder-audit-intern-to-cfo "From *audit intern* to *CFO*" intern,senior,manager,controller,cfo INTERN CFO assets/renders/thumbnails-v2/specs/ladder-audit-intern-to-cfo.json
The picture: a four-rung ladder with Ledger in outfits 1, 2, 4 and 5, the bottom tag ticked, the top tag yellow, a dashed arrow up.
Keep the tags short (about 9 letters: "ANALYST", not "JUNIOR ANALYST"); the build stops when a tag does not fit."""
import json, sys
slug, title, outfits, bottom, top, out = sys.argv[1:7]; outfits = outfits.split(",")
RY = [1335, 1145, 955, 765]; LX = 300
items = [{"p": "career_ladder", "x": LX, "y": RY[0], "n": 4, "gap": 190, "w": 220},
         {"p": "rung_tag", "x": LX + 377, "y": RY[0], "label": bottom, "state": "done", "w": 430, "h": 96, "fs": 44},
         {"p": "rung_tag", "x": LX + 377, "y": RY[3], "label": top, "state": "now", "w": 430, "h": 96, "fs": 44},
         {"p": "arrow", "x": 760, "y": 1225, "dx": 0, "dy": -330, "color": "blue", "s": 1.1, "dashed": True}]
pick = [outfits[0], outfits[1], outfits[3], outfits[4]]
items += [{"p": "ledger", "x": LX, "y": RY[i], "s": 0.8, "outfit": pick[i], "mood": "happy" if i == 3 else "smile", "arm": "wave" if i == 3 else ("both_up" if i == 2 else "down")} for i in range(4)]
spec = {"id": slug, "format": "lifeof", "pill": "CAREER LADDER IN 90 SECONDS", "color": "#467DE3", "title": title, "items": items}
if len(title) > 28: spec["title_fs"] = 78   # a long title stays on two lines
json.dump(spec, open(out, "w"), indent=1); print("wrote", out)
