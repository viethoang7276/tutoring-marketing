"""Turn script.json scenes (presets) into s*.svg art and resolve each beat's camera framing.

Usage: python build_scenes.py <workdir>
Reads  <workdir>/script.json  {"meta": {...}, "scenes": {"s1": {"bg", "items": [...]}}, "beats": [...]}
Writes <workdir>/<scene>.svg for every scene and <workdir>/beats.json (beats with numeric focus boxes) for vo.py.

No camera moves (Hoang, 25 Oct 2026): the framing belongs to the SCENE, set once as "frame", and every beat on
that scene shows the same steady frame. Beats never carry focus or focus_end. A scene's "frame" may be:
  (omitted) / "auto"  THE DEFAULT: the renderer fits the frame to the bounding box of everything drawn in the scene
                      (people and props, not the background), so the subject fills about 70% of the art-box width
  "ledger"            Ledger (the first ledger item) with a little room around him
  "ledger-close"      a tight close-up on Ledger's face and hands
  "item:<id>"         one item, by its "id"
  "items:<id>,<id>"   several items together
  "wide"              everything in the scene
  [x, y, w, h]        an explicit box in the 1080x1920 art
Boxes are widened to the frame's 1000:780 shape, so the subject fills the frame as much as possible.
The last beat (role "endcard") has no img: the renderer shows the term, key point and logo instead.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene_lib as L

ASPECT = 1000 / 780


def union(boxes):
    x0 = min(b[0] for b in boxes); y0 = min(b[1] for b in boxes)
    x1 = max(b[0] + b[2] for b in boxes); y1 = max(b[1] + b[3] for b in boxes)
    return [x0, y0, x1 - x0, y1 - y0]


def shape(b, pad=0.08, minw=420):
    x, y, w, h = b
    w, h = w * (1 + 2 * pad), h * (1 + 2 * pad)
    cx, cy = b[0] + b[2] / 2, b[1] + b[3] / 2
    if w / h < ASPECT: w = h * ASPECT
    else: h = w / ASPECT
    if w < minw: w, h = minw, minw / ASPECT
    return [round(cx - w / 2), round(cy - h / 2), round(w), round(h)]


def resolve(f, spec, where):
    items = spec.get("items", [])
    led = [it for it in items if it["p"] == "ledger"]
    if isinstance(f, list) and len(f) == 4:
        return [round(v) for v in f]
    if f in (None, "auto"):
        return "auto"
    if f == "ledger":
        if not led:
            f = "wide"
        else:
            b = L.item_box(led[0]); return shape(b, pad=0.32)
    if f == "ledger-close":
        if not led: raise SystemExit(f"{where}: 'ledger-close' but the scene has no ledger item")
        b = L.item_box(led[0]); return shape([b[0], b[1], b[2], b[3] * 0.8], pad=0.06)
    if f == "wide":
        boxes = [L.item_box(it) for it in items] or [[60, 600, 960, 880]]
        return shape(union(boxes), pad=0.04)
    if isinstance(f, str) and f.startswith(("item:", "items:")):
        ids = f.split(":", 1)[1].split(",")
        boxes = []
        for i in ids:
            m = [it for it in items if it.get("id") == i.strip()]
            if not m: raise SystemExit(f"{where}: no item with id '{i.strip()}' in this scene")
            boxes.append(L.item_box(m[0]))
        return shape(union(boxes), pad=0.12)
    raise SystemExit(f"{where}: unknown focus {f!r} (use auto, ledger, ledger-close, wide, item:<id>, items:<id>,<id> or [x,y,w,h])")


def main(d):
    S = json.load(open(os.path.join(d, "script.json")))
    for name, spec in S["scenes"].items():
        open(os.path.join(d, f"{name}.svg"), "w").write(L.scene_svg(spec))
    beats = []
    for k, b in enumerate(S["beats"], 1):
        nb = dict(b); nb.pop("focus_end", None)
        if b.get("role") == "endcard":
            nb.pop("img", None); nb["focus"] = [0, 0, 1080, 1920]; nb.setdefault("chunks", [])
        else:
            spec = S["scenes"][b["img"]]
            nb["focus"] = resolve(spec.get("frame"), spec, f"scene {b['img']} frame")
        beats.append(nb)
    json.dump(beats, open(os.path.join(d, "beats.json"), "w"), indent=1)
    print("scenes", len(S["scenes"]), "beats", len(beats))


if __name__ == "__main__":
    main(sys.argv[1])
