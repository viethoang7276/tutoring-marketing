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
The last beat (role "endcard") has no img: the renderer shows the term, key point and logo instead. A lesson's "defcard"
beats (anywhere in the list) have no img either: the renderer shows the term, the definition and an optional equation, no logo.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene_lib as L

ASPECT = 1000 / 780
LEDGER_MIN, LEDGER_MAX, LEDGER_BUSY = 0.74, 0.88, 0.74   # Ledger's share of the frame height
# Full-frame layout (meta.layout "full", how-to reels, 1 Nov 2026): the art box is x 40-940, y 450-1440 (900x990), inside the
# platform safe zones (top 220, bottom 380, right 140 px). The box is taller than wide, so Ledger takes a smaller share of
# its height and the props get the room above and beside him
FULL = {"aspect": 900 / 990, "ledger": (0.66, 0.78, 0.66)}
BLEED = {"desk", "building", "whiteboard", "window", "people_group"}   # may run off the left/right edges
DATA_PROPS = {"data_chart", "data_table", "sheet_grid", "order_book", "live_chart", "waterfall"}   # real numbers (6 Nov 2026): the numbers are the subject, so an auto or "wide" frame shows the whole scene (data_frame) and never shrinks them around Ledger
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


def data_frame(name, spec, full):
    """The frame for a scene with a data prop, when its frame is auto or "wide": the whole scene fills the safe part of the art
    box (full layout x 50-930, y 455-1435; other layouts x 60-960, y 535-1305, clear of the right-hand buttons), never over 1:1."""
    BX, BY, BW, BH = (40, 450, 900, 990) if full else (40, 530, 1000, 780)
    x0, y0, x1, y1 = (50, 455, 930, 1435) if full else (60, 535, 960, 1305)
    u = union([L.item_box(it) for it in spec.get("items", [])])
    k = min(1.0, (x1 - x0) / u[2], (y1 - y0) / u[3])
    if k < 0.85: print(f"WARN  scene {name}: the data prop shows at {k:.2f} of its size, so its text may be too small; reduce w, h or the other items")
    fw, fh = BW / k, BH / k   # the renderer maps the frame's centre to the box's centre
    cx = u[0] + u[2] / 2 - ((x0 + x1) / 2 - (BX + BW / 2)) / k; cy = u[1] + u[3] / 2 - ((y0 + y1) / 2 - (BY + BH / 2)) / k
    return [round(cx - fw / 2), round(cy - fh / 2), round(fw), round(fh)]


def data_check(name, spec):
    """WARN when another item sits on a data_chart or data_table (Ledger and props go beside or below the numbers)."""
    out = []; items = spec.get("items", [])
    for d in [it for it in items if it["p"] in DATA_PROPS]:
        a = L.item_box(d)
        for it in items:
            if it is d or it["p"] in BLEED or it["p"] == "backdrop": continue
            c = L.item_box(it)
            if a[0] < c[0] + c[2] and c[0] < a[0] + a[2] and a[1] < c[1] + c[3] and c[1] < a[1] + a[3]:
                out.append(f"scene {name}: {it['p']} overlaps the {d['p']}; move it beside or below the numbers")
    return out


def motion_check(name, spec, beats, full):
    """WARN about motion items (keys move, reveal and so on, 6 Nov 2026): a chunk number past the end of the scene's run, Ledger-first framing that would shift items away from their "to", and items that end outside the safe art box."""
    out = []; items = spec.get("items", []); KEYS = ("move", "pulse", "shake", "out", "reveal")
    has = [it for it in items if any(L._m_keys(it.get(k)) for k in KEYS) or it["p"] in L.SELF_TIMED or it["p"] in ("order_book", "live_chart", "waterfall", "fill_grid", "trader", "counter")]
    if not has: return out
    run = 0; seen = False   # caption chunks over the first run of beats that use this scene
    for b in beats:
        if b.get("img") == name: run += len(b.get("chunks") or []); seen = True
        elif seen: break
    def refs(v):
        if isinstance(v, dict):
            for k, x in v.items():
                if k == "at" and isinstance(x, str) and x.startswith("chunk:"): yield int(x.split(":")[1])
                else: yield from refs(x)
        elif isinstance(v, list):
            for x in v: yield from refs(x)
    for it in has:
        for n in refs({k: v for k, v in it.items() if k not in ("p", "id", "x", "y", "s")}):
            if n >= run: out.append(f'scene {name}: {it["p"]} uses chunk:{n}, but this scene has only {run} caption chunks (0 to {run - 1})')
    if spec.get("frame") in (None, "auto") and any(it["p"] == "ledger" for it in items): out.append(f'scene {name}: motion with Ledger-first framing moves items after you placed them; set "frame" to an explicit box')
    x0, y0, x1, y1 = (40, 450, 940, 1440) if full else (40, 530, 1040, 1310)
    if isinstance(spec.get("frame"), list):
        for it in has:
            b = L.item_box(it); pts = [(b[0], b[1]), (b[0] + b[2], b[1] + b[3])]
            for k in L._m_keys(it.get("move")): pts += [(k["to"][0] - b[2] / 2, k["to"][1]), (k["to"][0] + b[2] / 2, k["to"][1])]
            if any(px < x0 - 6 or px > x1 + 6 or py < y0 - 6 or py > y1 + 6 for px, py in pts): out.append(f'scene {name}: {it["p"]} runs outside the art box x {x0}-{x1}, y {y0}-{y1}')
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


def cam_keys(spec, name):
    """Scene "cam" (30 Oct 2026, tutoring ad v6; the only exception to the no-camera-moves rule, for paid ads):
    a list of keyframes {"at": "chunk:N", "delay": s, "dur": s, "frame": <any frame value>}. At the start of chunk N
    (counted over the consecutive beats that share the scene, like "at" on items) plus delay, the camera moves to the
    frame over dur seconds with an ease in and out (dur 0 = a cut). The first keyframe is the opening frame."""
    out = []
    for k, c in enumerate(spec["cam"]):
        at = str(c.get("at", "chunk:0"))
        if not re.match(r"^chunk:\d+$", at): raise SystemExit(f"scene {name} cam {k}: at {at!r}; use chunk:N")
        box = resolve(c.get("frame"), spec, f"scene {name} cam {k}")
        if box == "auto": raise SystemExit(f"scene {name} cam {k}: give a frame (box, item:<id>, ledger, ledger-close, wide)")
        out.append({"at": at, "delay": float(c.get("delay", 0)), "dur": float(c.get("dur", 0)), "box": box})
    return out


def talk_frame(spec):
    """ledger-talks layout: the art fills the whole screen; Ledger faces the viewer at about 80% of the screen width,
    his feet at screen y 1360, so his mouth (~y 1010) stays above the captions (y 1110-1340). Props sit beside his head. The frame is the same for every scene,
    so jump cuts between poses never move him."""
    led = next((it for it in spec.get("items", []) if it["p"] == "ledger"), None)
    if not led: return "auto"
    lb = L.item_box(led)
    w = 1080 * lb[2] / 864.0; h = w * 1920 / 1080.0; k = 1080 / w   # the frame is the whole 1080x1920 screen
    top = (lb[1] + lb[3]) - 1360 / k                                  # his feet land at screen y 1360 (mouth ~y 1010, above the captions)
    return [round(led["x"] - w / 2), round(top), round(w), round(h)]


def main(d):
    global ASPECT, LEDGER_MIN, LEDGER_MAX, LEDGER_BUSY
    S = json.load(open(os.path.join(d, "script.json")))
    if S.get("meta", {}).get("layout") == "full":
        ASPECT = FULL["aspect"]; LEDGER_MIN, LEDGER_MAX, LEDGER_BUSY = FULL["ledger"]
    frames = {}
    talk = S.get("meta", {}).get("type") == "ledger-talks"
    for name, spec in S["scenes"].items():
        if talk and spec.get("frame") in (None, "auto"):
            frames[name] = talk_frame(spec)
        elif spec.get("frame") in (None, "auto", "wide") and any(it["p"] in DATA_PROPS for it in spec.get("items", [])):
            frames[name] = data_frame(name, spec, S.get("meta", {}).get("layout") == "full")
        elif spec.get("frame") in (None, "auto") and any(it["p"] == "ledger" for it in spec.get("items", [])):
            frames[name] = ledger_first(spec)   # props are nudged/scaled before the art is drawn
        for w in hand_check(name, spec): print("WARN ", w)
        for w in data_check(name, spec): print("WARN ", w)
        for w in motion_check(name, spec, S.get("beats", []), S.get("meta", {}).get("layout") == "full"): print("WARN ", w)
        open(os.path.join(d, f"{name}.svg"), "w").write(L.scene_svg(spec))
    beats = []
    for k, b in enumerate(S["beats"], 1):
        nb = dict(b); nb.pop("focus_end", None)
        if b.get("role") in ("endcard", "defcard"):
            nb.pop("img", None); nb["focus"] = [0, 0, 1080, 1920]; nb.setdefault("chunks", [])
        else:
            spec = S["scenes"][b["img"]]
            nb["focus"] = frames.get(b["img"]) or resolve(spec.get("frame"), spec, f"scene {b['img']} frame")
            if spec.get("cam"):   # camera keyframes (paid ads only, Hoang 30 Oct 2026); scenes without "cam" keep the steady frame
                nb["cam"] = cam_keys(spec, b["img"])
        beats.append(nb)
    json.dump(beats, open(os.path.join(d, "beats.json"), "w"), indent=1)
    print("scenes", len(S["scenes"]), "beats", len(beats))


if __name__ == "__main__":
    main(sys.argv[1])
