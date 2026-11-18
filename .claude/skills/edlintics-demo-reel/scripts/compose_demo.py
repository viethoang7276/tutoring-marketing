"""Compose an Edlintics demo reel (1080x1920, 30 fps, voice only) from a recorded take.
Layout: flat brand-blue background, direct title at the top, the recording in a rounded phone-style frame, chunked captions in the
middle of the bottom half (centre y 1425, inside 1320-1530), a slow zoom on the key moment, then an end card with Ledger v2.

Usage (repo root):
  tools/tts/.venv/bin/python .claude/skills/edlintics-demo-reel/scripts/compose_demo.py SPEC.json WORK_DIR TAKE_DIR OUT.mp4 [--thumb THUMB.jpg]
  WORK_DIR holds voice.wav and timings.json (demo_voice.py); TAKE_DIR holds frames/, frames.json, events.json (record_demo.cjs).
  python compose_demo.py --pick WORK_DIR/take-*   prints a smoothness score per take (largest frame gap during motion; lower is better)
"""
import bisect, json, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import imageio_ffmpeg

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
FONT = os.path.join(REPO, "assets/fonts")
LEDGER = os.path.join(REPO, "assets/brand-handoff/ledger-v2/png")   # gitignored brand art, loaded at render time
W, H, FPS = 1080, 1920, 30
BLUE, BLUE2, INK, WHITE, PALE = (70, 125, 227), (37, 99, 235), (2, 8, 23), (255, 255, 255), (239, 246, 255)
CAP_Y, CAP_W = 1425, 940          # caption centre and max text width (captions-bottom-half-center rule)
SCREEN_TOP, SCREEN_H = 300, 1000  # phone screen box; width follows the recording's aspect


def font(w, px): return ImageFont.truetype(os.path.join(FONT, f"inter-{w}.woff2"), px)


def ease(k): k = max(0.0, min(1.0, k)); return k * k * (3 - 2 * k)


def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for wd in text.split():
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = wd
    if cur: lines.append(cur)
    return lines


def background():
    bg = Image.new("RGB", (W, H), BLUE)
    g = Image.linear_gradient("L").rotate(-35, expand=False).resize((W, H))   # flat, soft diagonal: brand blue to cta blue
    bg = Image.composite(Image.new("RGB", (W, H), BLUE2), bg, g.point(lambda v: int(v * 0.55)))
    return bg


def title_layer(text):
    L = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(L)
    for px in (76, 70, 64, 58):
        f = font(800, px); lines = wrap(d, text, f, 960)
        if len(lines) <= 2: break
    lh = int(px * 1.16); y0 = 160 - (len(lines) * lh) // 2 + 10
    for i, ln in enumerate(lines):
        d.text((W // 2, y0 + i * lh), ln, font=f, fill=WHITE, anchor="mt")
    return L


def phone_layer(sw, sh, x0, y0, bez=16, r=58):
    L = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(L)
    sh_img = Image.new("RGBA", (W, H)); ds = ImageDraw.Draw(sh_img)
    ds.rounded_rectangle((x0 - bez, y0 - bez + 18, x0 + sw + bez, y0 + sh + bez + 18), r + bez, fill=(2, 8, 23, 90))
    L = Image.alpha_composite(L, sh_img.filter(ImageFilter.GaussianBlur(22)))
    d = ImageDraw.Draw(L)
    d.rounded_rectangle((x0 - bez, y0 - bez, x0 + sw + bez, y0 + sh + bez), r + bez, fill=INK)
    return L


def caption_img(text):
    f = font(700, 48); d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    lines = wrap(d, text, f, CAP_W - 56)
    lh = 60; bw = int(max(d.textlength(l, font=f) for l in lines)) + 64; bh = lh * len(lines) + 40
    im = Image.new("RGBA", (bw, bh)); dd = ImageDraw.Draw(im)
    dd.rounded_rectangle((0, 0, bw - 1, bh - 1), 26, fill=WHITE)
    for i, l in enumerate(lines): dd.text((bw // 2, 20 + i * lh), l, font=f, fill=INK, anchor="mt")
    return im, len(lines)


def chunks(text, maxc=70):
    """Split a caption into balanced on-screen chunks of at most ~maxc characters at word boundaries, preferring a split
    after a comma. Commas at a split are dropped; there is never a trailing full stop"""
    text = text.rstrip(". ")
    if len(text) <= maxc: return [text]
    words = text.split(); n = -(-len(text) // maxc)
    import itertools
    best = None
    for cuts in itertools.combinations(range(1, len(words)), n - 1):
        parts = [" ".join(words[a:b]) for a, b in zip((0,) + cuts, cuts + (len(words),))]
        if max(len(x) for x in parts) > maxc + 6: continue
        score = (max(len(x) for x in parts) - min(len(x) for x in parts) - sum(18 for x in parts[:-1] if x.endswith(","))
                 - sum(10 for x in parts[1:] if x.split()[0] in ("and", "so", "with", "from", "on", "in", "because", "but")))
        if best is None or score < best[0]: best = (score, parts)
    parts = best[1] if best else [text]
    return [x.rstrip(",") for x in parts]


def end_card(spec, shot=None):
    """End card: the CTA on top, a small screen showing the card's final state, Ledger v2 pointing at it. Nothing overlaps"""
    L = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(L)
    ec = spec.get("end_card", {})
    d.text((W // 2, 330), ec.get("line1", "Try it free on"), font=font(800, 84), fill=WHITE, anchor="mt")
    f = font(800, 92); t = ec.get("line2", "edlintics.com"); tw = d.textlength(t, font=f)
    d.rounded_rectangle((W // 2 - tw / 2 - 56, 460, W // 2 + tw / 2 + 56, 610), 75, fill=WHITE)
    d.text((W // 2, 535), t, font=f, fill=BLUE, anchor="mm")
    x0, y0 = 120, 700
    if shot is not None:
        s = 560 / shot.height; v = shot.resize((int(shot.width * s), 560), Image.LANCZOS)
        L.alpha_composite(phone_layer(v.width, v.height, x0, y0, bez=10, r=34))
        m = Image.new("L", v.size); ImageDraw.Draw(m).rounded_rectangle((0, 0, v.width - 1, v.height - 1), 26, fill=255)
        L.paste(v, (x0, y0), m); right = x0 + v.width + 10
    else: right = 300
    p = os.path.join(LEDGER, ec.get("ledger", "ledger-point-left") + ".png")
    if os.path.exists(p):
        lg = Image.open(p).convert("RGBA"); lg = lg.crop(lg.getbbox()); sc = 430 / lg.height
        lg = lg.resize((int(lg.width * sc), 430), Image.LANCZOS)
        L.alpha_composite(lg, (min(W - lg.width - 30, right + 40), y0 + 100))
    return L


def pick(takes):
    for t in takes:
        fr = json.load(open(os.path.join(t, "frames.json"))); ev = json.load(open(os.path.join(t, "events.json")))
        ts = [f["t"] for f in fr]; worst = 0
        for e in ev["events"]:
            if e["do"] == "hold": continue
            win = [x for x in ts if e["started"] - 0.05 <= x <= e["ended"] + 0.6]
            gaps = [b - a for a, b in zip(win, win[1:])]
            worst = max(worst, max(gaps) if gaps else 1)
        print(f"{t}: frames {len(fr)}, worst motion gap {worst * 1000:.0f} ms, non-GET {len(ev['nonGetRequests'])}, navs {len(ev['navigations'])}")


def main():
    if sys.argv[1] == "--pick": return pick(sys.argv[2:])
    spec = json.load(open(sys.argv[1])); work, take, out = sys.argv[2:5]
    thumb = sys.argv[sys.argv.index("--thumb") + 1] if "--thumb" in sys.argv else None
    tim = json.load(open(os.path.join(work, "timings.json"))); T = tim["total"]
    fr = json.load(open(os.path.join(take, "frames.json"))); ev = json.load(open(os.path.join(take, "events.json")))
    ts = [f["t"] for f in fr]
    rw, rh = Image.open(os.path.join(take, "frames", fr[0]["f"])).size
    sh = SCREEN_H; sw = round(sh * rw / rh); sx = (W - sw) // 2; sy = SCREEN_TOP
    css = rw / ev["viewport"][0]   # recording pixels per CSS pixel

    base = background(); base.paste(Image.alpha_composite(base.convert("RGBA"), phone_layer(sw, sh, sx, sy)).convert("RGB"))
    base_t = Image.alpha_composite(base.convert("RGBA"), title_layer(spec["title"])).convert("RGB")
    mask = Image.new("L", (sw, sh)); ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw - 1, sh - 1), 44, fill=255)

    # Captions: each line's caption split into chunks, timed by character share of the line
    caps = []
    for i, ln in enumerate(spec["lines"]):
        L = tim["lines"][i]; cs = chunks(ln.get("caption", ln["say"])); tot = sum(len(c) for c in cs); t = L["start"]
        for c in cs:
            d = (L["end"] - L["start"]) * len(c) / tot; img, nl = caption_img(c)
            if nl > 2: print("WARN caption over 2 lines:", c)
            caps.append((t, t + d, img, c)); t += d
    # Zooms: {"zoom": id} on a line zooms to that tagged element from line start + 1.0 s, 1.4 s ramp, z = spec zoom_scale
    zooms = []
    for i, ln in enumerate(spec["lines"]):
        if ln.get("zoom"):
            r = ev["rects"][-1]["r"].get(ln["zoom"])
            if r: zooms.append((tim["lines"][i]["start"] + 1.0, (r["x"] + r["w"] / 2) * css))
    top = float(spec.get("zoom_top_css", 0)) * css   # crop top after the push-in (the sticky header's bottom edge)
    zs = rh / (rh - top) if top else float(spec.get("zoom_scale", 1.12))
    end_i = next((i for i, ln in enumerate(spec["lines"]) if ln.get("end")), None)
    end_t = tim["lines"][end_i]["start"] - 0.35 if end_i is not None else T + 1
    end_bg = None

    ff = imageio_ffmpeg.get_ffmpeg_exe()
    p = subprocess.Popen([ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", os.path.join(work, "voice.wav"), "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    cache = {}; N = int(T * FPS); key_frame = None
    for n in range(N):
        t = n / FPS
        k = max(0, bisect.bisect_right(ts, t) - 1); fn = fr[k]["f"]
        if fn not in cache: cache.clear(); cache[fn] = Image.open(os.path.join(take, "frames", fn)).convert("RGB")
        src = cache[fn]
        box = (0, 0, rw, rh)
        for (zt, zx) in zooms:
            if t >= zt:
                e = ease((t - zt) / 1.4); cw, ch = rw / zs, rh / zs
                cx = min(max(zx, cw / 2), rw - cw / 2); y1 = rh - ch if top else (rh - ch) / 2
                tb = (cx - cw / 2, y1, cx + cw / 2, y1 + ch)
                box = tuple(a + (b - a) * e for a, b in zip((0, 0, rw, rh), tb))
        view = src.crop(tuple(round(v) for v in box)).resize((sw, sh), Image.LANCZOS)
        fimg = base_t.copy(); fimg.paste(view, (sx, sy), mask)
        if t >= end_t:
            if end_bg is None:   # built from the last screen state, so the end card shows the card the viewer just saw
                end_bg = Image.alpha_composite(background().convert("RGBA"), end_card(spec, last_view)).convert("RGB")
            a = ease((t - end_t) / 0.45); fimg = Image.blend(fimg, end_bg, a)
        else: last_view = view
        for (a0, a1, img, _) in caps:
            if a0 - 0.05 <= t < a1 + 0.05:
                al = min(1.0, (t - a0 + 0.05) / 0.12, (a1 + 0.05 - t) / 0.12)
                im = img if al >= 1 else Image.merge("RGBA", (*img.split()[:3], img.split()[3].point(lambda v: int(v * max(0, al)))))
                fimg.paste(im, (W // 2 - img.width // 2, CAP_Y - img.height // 2), im)
                break
        if zooms and key_frame is None and t >= zooms[0][0] + 1.6: key_frame = view.copy()
        p.stdin.write(fimg.tobytes())
    p.stdin.close(); p.wait()
    print("wrote", out, f"{N / FPS:.2f}s", f"screen {sw}x{sh} at ({sx},{sy}), {sw / ev['viewport'][0]:.2f} px per CSS px")
    if thumb:   # the cover shows exactly the key element (whole box, nothing cut), taken from the take's final frame
        zid = next((ln["zoom"] for ln in spec["lines"] if ln.get("zoom")), None); r = ev["rects"][-1]["r"].get(zid) if zid else None
        last = Image.open(os.path.join(take, "frames", fr[-1]["f"])).convert("RGB")
        if r:
            pad = 4   # the gap between options is about 10 CSS px: more padding shows the neighbours' borders
            crop = last.crop((round((r["x"] - pad) * css), round((r["y"] - pad) * css), round((r["x"] + r["w"] + pad) * css), round((r["y"] + r["h"] + pad) * css)))
        else: crop = key_frame or view
        make_thumb(spec, crop, thumb)


def make_thumb(spec, view, path):
    """Cover: title + a crop of the card in its final state + Ledger pointing at it"""
    im = background().convert("RGBA"); d = ImageDraw.Draw(im)
    f = font(800, 96); lines = wrap(d, spec.get("thumb_title", spec["title"]), f, 940)
    for i, l in enumerate(lines): d.text((W // 2, 270 + i * 112), l, font=f, fill=WHITE, anchor="mt")   # inside the 3:4 grid crop
    top = 270 + len(lines) * 112 + 50
    v = view.copy(); s = 940 / v.width; v = v.resize((940, int(v.height * s)), Image.LANCZOS)
    maxh = 1290 - top
    if v.height > maxh: s2 = maxh / v.height; v = v.resize((int(v.width * s2), maxh), Image.LANCZOS)
    vx = (W - v.width) // 2
    m = Image.new("L", v.size); ImageDraw.Draw(m).rounded_rectangle((0, 0, v.width - 1, v.height - 1), 40, fill=255)
    shadow = Image.new("RGBA", (W, H)); ImageDraw.Draw(shadow).rounded_rectangle((vx, top + 16, vx + v.width, top + v.height + 16), 40, fill=(2, 8, 23, 90))
    im = Image.alpha_composite(im, shadow.filter(ImageFilter.GaussianBlur(20))); im.paste(v, (vx, top), m)
    p = os.path.join(LEDGER, spec.get("thumb_ledger", "ledger-cheer") + ".png")
    if os.path.exists(p):
        lg = Image.open(p).convert("RGBA"); lg = lg.crop(lg.getbbox()); sc = 330 / lg.height; lg = lg.resize((int(lg.width * sc), 330), Image.LANCZOS)
        im.alpha_composite(lg, (W // 2 - lg.width // 2, top + v.height + 40))   # below the card, never on it
    im.convert("RGB").save(path, quality=92)
    print("wrote", path)


if __name__ == "__main__":
    main()
