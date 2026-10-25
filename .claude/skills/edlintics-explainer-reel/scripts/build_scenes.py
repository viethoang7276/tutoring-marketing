"""Turn script.json scenes (presets) into s*.svg art and resolve each beat's camera framing.

Usage: python build_scenes.py <workdir>
Reads  <workdir>/script.json  {"meta": {...}, "scenes": {"s1": {"bg", "items": [...]}}, "beats": [...]}
Writes <workdir>/<scene>.svg for every scene and <workdir>/beats.json (beats with numeric focus boxes) for vo.py.

No camera moves (Hoang, 25 Oct 2026): the framing belongs to the SCENE, set once as "frame", and every beat on
that scene shows the same steady frame. Beats never carry focus or focus_end. A scene's "frame" may be:
  (omitted) / "auto"  THE DEFAULT. If the scene has Ledger: LEDGER-FIRST. The frame is sized from Ledger's own height,
                      so he always fills 74-88% of the art-box height (about 74% when the scene is busy), whatever his
                      "s" in the script. Props are then fitted around him: a prop that would fall outside the frame is
                      nudged in, and scaled down only if it is still too big. Ledger is never shrunk or moved.
                      Wide "bleed" props (desk, building, whiteboard, window, people_group) may run off the left and
                      right edges instead of shrinking (a cropped desk edge). Nothing goes above the frame top, so
                      nothing sits under the caption band. No Ledger in the scene: the renderer fits the drawn
                      subject (people and props, not the background) to about 70% of the art-box width
  "content"           the old fit for any scene: everything drawn fills ~70% of the width (Ledger may get small)
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
LEDGER_MIN, LEDGER_MAX, LEDGER_BUSY = 0.74, 0.88, 0.74   # Ledger's share of the frame height
BLEED = {"desk", "building", "whiteboard", "window", "people_group"}   # may run off the left/right edges
HELD = {"ticket", "phone", "coins", "bills", "invoice", "coffee", "price_tag", "envelope", "books", "umbrella", "receipt",
        "pizza_slice", "sandwich", "burger", "lemonade_cup", "plate"}   # props Ledger can hold (checked against his hand)


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


def _box_inside(b, win, m, bleed=False):
    """Shift box b so it sits inside win (margin m); bleed boxes only need to stay inside vertically."""
    x, y, w, h = b; wx, wy, ww, wh = win; dx = dy = 0
    if not bleed:
        if x < wx + m: dx = wx + m - x
        elif x + w > wx + ww - m: dx = wx + ww - m - (x + w)
    if y < wy + m: dy = wy + m - y
    elif y + h > wy + wh - m: dy = wy + wh - m - (y + h)
    return dx, dy


def ledger_first(spec):
    """Frame a scene around Ledger (see the module doc). Mutates the props' x, y, s; returns the frame box."""
    items = spec.get("items", [])
    led = next((it for it in items if it["p"] == "ledger"), None)
    lb = L.item_box(led); hl = lb[3]
    others = [it for it in items if it is not led]
    boxes = [lb] + [L.item_box(it) for it in others if it["p"] not in BLEED]
    u = union(boxes)
    cw, ch = u[2] * 1.12, u[3] * 1.12           # content with a little room
    hc = max(ch, cw / ASPECT)                    # frame height that would hold all the content
    hwin = min(max(hc, hl / LEDGER_MAX), hl / LEDGER_MIN)
    if hc > hl / LEDGER_MIN: hwin = hl / LEDGER_BUSY   # busy scene: Ledger at ~74%, props come in to him
    wwin = hwin * ASPECT; m = 0.04 * hwin
    cx, cy = u[0] + u[2] / 2, u[1] + u[3] / 2
    # keep Ledger fully inside, with room above his head for nothing to touch the caption band
    cx = min(max(cx, lb[0] + lb[2] - wwin / 2 + m), lb[0] + wwin / 2 - m)
    cy = min(max(cy, lb[1] + lb[3] - hwin / 2 + m), lb[1] + hwin / 2 - m)
    win = [cx - wwin / 2, cy - hwin / 2, wwin, hwin]
    for it in others:
        bleed = it["p"] in BLEED
        for _ in range(3):
            b = L.item_box(it)
            aw, ah = win[2] - 2 * m, win[3] - 2 * m
            k = min(1.0, ah / b[3] if b[3] else 1.0, 1.0 if bleed else (aw / b[2] if b[2] else 1.0))
            if k < 0.999:   # too big for the frame: scale it about its own centre
                bcx, bcy = b[0] + b[2] / 2, b[1] + b[3] / 2
                it["s"] = round(it.get("s", 1.0) * k, 3)
                nb = L.item_box(it)
                it["x"] = round(it["x"] + bcx - (nb[0] + nb[2] / 2), 1); it["y"] = round(it["y"] + bcy - (nb[1] + nb[3] / 2), 1)
                continue
            dx, dy = _box_inside(b, win, m, bleed)
            if abs(dx) < 0.5 and abs(dy) < 0.5: break
            it["x"] = round(it["x"] + dx, 1); it["y"] = round(it["y"] + dy, 1)
    return [round(v) for v in win]


def hand_check(name, spec):
    """WARN when a prop at Ledger's hand is out of proportion with his hand (a giant ticket makes the hand look tiny)."""
    out = []
    if any(it["p"] == "ledger" for it in spec.get("items", [])) and any(it["p"] == "handshake" for it in spec.get("items", [])):
        out.append(f"scene {name}: the handshake prop draws its own small hands that never match Ledger's; show the deal with an invoice (stamp true) or a check instead")
    for led in [it for it in spec.get("items", []) if it["p"] == "ledger"]:
        ls = led.get("s", 1.0); flip = -1 if led.get("flip") else 1
        pose = L.ARM_POSES.get(led.get("arm", "down"), L.ARM_POSES["down"])
        bw = L.BODY_W * ls
        for side, (_, (hx, hy)) in pose.items():
            ax, ay = led["x"] + flip * (hx - 120) * ls, led["y"] + (hy - 230) * ls
            for it in spec.get("items", []):
                if it is led or it["p"] not in HELD: continue
                b = L.item_box(it); bc = (b[0] + b[2] / 2, b[1] + b[3] / 2)
                if abs(bc[0] - ax) > 0.7 * bw or abs(bc[1] - ay) > 0.7 * bw: continue   # not in his hand
                size = max(b[2], b[3])
                if size > 1.7 * bw: out.append(f"scene {name}: {it['p']} at Ledger's hand is {size / bw:.1f}x his body width; a held prop over 1.7x makes the hand look tiny (lower its s)")
                if size < 0.2 * bw: out.append(f"scene {name}: {it['p']} at Ledger's hand is only {size / bw:.2f}x his body width; it will look like a speck in his hand")
    return out


def resolve(f, spec, where):
    items = spec.get("items", [])
    led = [it for it in items if it["p"] == "ledger"]
    if isinstance(f, list) and len(f) == 4:
        return [round(v) for v in f]
    if f == "content":
        return "auto"
    if f in (None, "auto"):
        return "auto"   # scenes with Ledger were framed by ledger_first() before resolve() is reached
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
    frames = {}
    for name, spec in S["scenes"].items():
        if spec.get("frame") in (None, "auto") and any(it["p"] == "ledger" for it in spec.get("items", [])):
            frames[name] = ledger_first(spec)   # props are nudged/scaled before the art is drawn
        for w in hand_check(name, spec): print("WARN ", w)
        open(os.path.join(d, f"{name}.svg"), "w").write(L.scene_svg(spec))
    beats = []
    for k, b in enumerate(S["beats"], 1):
        nb = dict(b); nb.pop("focus_end", None)
        if b.get("role") == "endcard":
            nb.pop("img", None); nb["focus"] = [0, 0, 1080, 1920]; nb.setdefault("chunks", [])
        else:
            spec = S["scenes"][b["img"]]
            nb["focus"] = frames.get(b["img"]) or resolve(spec.get("frame"), spec, f"scene {b['img']} frame")
        beats.append(nb)
    json.dump(beats, open(os.path.join(d, "beats.json"), "w"), indent=1)
    print("scenes", len(S["scenes"]), "beats", len(beats))


if __name__ == "__main__":
    main(sys.argv[1])
