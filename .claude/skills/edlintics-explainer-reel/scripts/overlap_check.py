"""Overlap check for one reel or lesson before it renders (LESSON_OVERLAP_CHECK=1 make_reel.sh, 7 Nov 2026). No render, no credits.

Usage: tools/tts/.venv/bin/python overlap_check.py <workdir> [--strict]
Flags, in <workdir>/script.json, a data table or chart (data_table, data_chart) that overlaps another item while both are on
screen, and a table whose top is above y 480 (under the title). Same rule as tutoring-content/tools/video/overlap-check.py,
for one work folder. Prints OVERLAP OK or the hits; exits 1 on hits only with --strict.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene_lib as L
d = sys.argv[1]; strict = "--strict" in sys.argv[2:]
DATA = {"data_table", "data_chart"}; SKIP = {"backdrop"}
num = lambda v: int(v[6:]) if isinstance(v, str) and v.startswith("chunk:") else None
s = json.load(open(f"{d}/script.json", encoding="utf-8")); hits = []
for n, sc in s.get("scenes", {}).items():
    it = sc.get("items", [])
    for dt in [i for i in it if i.get("p") in DATA]:
        a = L.item_box(dt)
        if a[1] < 480: hits.append(f"{n}: table top at {round(a[1])}, under the title")
        for o in it:
            if o is dt or o.get("p") in SKIP: continue
            c = L.item_box(o)
            ox = min(a[0] + a[2], c[0] + c[2]) - max(a[0], c[0]); oy = min(a[1] + a[3], c[1] + c[3]) - max(a[1], c[1])
            if ox > 0 and oy > 0:
                du, ot, ou, da = num(dt.get("until")), num(o.get("at")), num(o.get("until")), num(dt.get("at"))
                apart = (du is not None and ot is not None and ot >= du) or (ou is not None and da is not None and da >= ou)
                if not apart: hits.append(f"{n}: {o.get('p')}[{o.get('title') or ''}] on table, {round(ox)}x{round(oy)}px")
for h in sorted(set(hits)): print("OVERLAP", h)
print("OVERLAP", "OK" if not hits else f"{len(set(hits))} hit(s)")
sys.exit(1 if hits and strict else 0)
