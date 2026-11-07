#!/usr/bin/env python3
"""Edlintics Short thumbnail maker: JSON spec in, 1080x1920 PNG and JPG out (style approved by Hoang, 7 Nov 2026).

Layout, top to bottom: format pill, direct title with *key words* highlighted, art, logo. The top 290 px and the area
below the logo stay empty, because the platforms cover them.

Usage:
  python3 make_thumbnail.py spec.json [more.json ...] --out DIR [--png-dir DIR] [--html-dir DIR] [--check-only]

A spec file holds one spec or a list of them:
  {"id": "def-shrinkflation", "format": "definition", "title": "What is *shrinkflation*?",
   "items": [{"p": "groceries_bag", "x": 330, "y": 1000, "s": 1.4},
             {"p": "ledger", "x": 800, "y": 1400, "s": 1.5, "mood": "worried", "arm": "point", "flip": true}]}

format: definition, list, puzzle, howto or lifeof sets the pill colour and default wording. "pill" overrides the wording,
"color" overrides the colour. Title rules: name the term; a puzzle never gives its answer away; no exclamation point,
no emoji and no trailing full stop.

items are scene_lib presets (python3 scene_lib.py --list), drawn in order, plus these thumbnail props:
  text    {x, y, text, fs, color, weight, anchor, rot}. Colours: ink, blue, red, green, amber, grey, white or any #hex.
  board   {x, y, w, title, rows, fs, head, style, rot}. A sign, bill or receipt whose text is real. rows are [left, right]
          or {"l", "r", "c" (colour), "hl" (amber band), "strike", "b" (bold)}. style: card or receipt. y = top edge.
  say     {x, y, text, fs, tail, w}. A speech bubble; "|" breaks lines. tail: left, right, down or none.
  stamp   {x, y, text, fs, color, rot}. A rubber-stamp word.
  raw     {svg}. Hand-written SVG, last resort.
order_book also takes "open_gap" (px, opens the spread band as the reel does at rest), "hide_sizes" (no share counts) and
"spread_text" (wording of the band).
Motion props (waterfall, counter, live_chart, fill_grid) draw their first frame statically, so a waterfall comes out
blank. Use data_chart or board for those numbers.

After rendering, the browser checks every image and prints CHECK lines: text under 34 px, art over the title or the logo,
art outside the canvas, text over other text, more than 3 title lines. Fix each one, then look at the image anyway:
the checks see boxes, not whether a picture reads well.
Screenshots run one at a time at nice 15 inside one Chrome, so the laptop stays quiet.
"""
import argparse
import base64
import html
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scene_lib as L  # noqa: E402

FORMATS = {
    "definition": ("#467DE3", "DEFINITION"),
    "list": ("#0E7490", "5 TERMS TO KNOW"),
    "puzzle": ("#059669", "BUSINESS PUZZLE"),
    "howto": ("#4338CA", "HOW IT IS USED"),
    "lifeof": ("#B45309", "A DAY IN THE LIFE"),
}
COLORS = {"ink": "#0F172A", "blue": "#2F62D0", "red": "#D5372F", "green": "#128A4D", "amber": "#B7791F", "grey": "#4B5568",
          "white": "#FFFFFF", "gold": "#FFD45C"}
FONT = 'font-family="Inter,sans-serif"'


def col(c):
    return COLORS.get(c, c or COLORS["ink"])


def tw(t, fs):
    return len(str(t)) * fs * 0.58


def text_item(it):
    rot = it.get("rot", 0); x, y = it["x"], it["y"]
    return (f'<text x="{x}" y="{y}" text-anchor="{it.get("anchor", "middle")}" {FONT} font-size="{it.get("fs", 44)}" '
            f'font-weight="{it.get("weight", 900)}" fill="{col(it.get("color"))}"'
            + (f' transform="rotate({rot} {x} {y})"' if rot else "") + f'>{html.escape(str(it["text"]))}</text>')


def board(it):
    x, y = it["x"], it["y"]; w = it.get("w", 640); fs = it.get("fs", 44); style = it.get("style", "card")
    title = it.get("title", ""); rh = fs * 1.42; pad = 26; head = fs * 1.62 if title else 0
    rows = [r if isinstance(r, dict) else {"l": r[0], "r": r[1] if len(r) > 1 else "", "c": r[2] if len(r) > 2 else None} for r in it.get("rows", [])]
    H = head + rh * len(rows) + 16; hw = w / 2
    if style == "receipt":
        n = 10; st = w / n
        zig = "".join(f" L{hw - st * (i + 1):.1f} {H + (14 if i % 2 == 0 else 0):.1f}" for i in range(n))
        shape = f'<path d="M{-hw} 0 L{hw} 0 L{hw} {H:.1f}{zig} Z" fill="#FFFFFF" stroke="{COLORS["ink"]}" stroke-width="6" stroke-linejoin="round"/>'
        top = f'<text x="0" y="{fs * 1.15:.1f}" text-anchor="middle" {FONT} font-size="{fs}" font-weight="900" fill="{COLORS["ink"]}">{html.escape(title)}</text>' if title else ""
        top += f'<path d="M{-hw + pad} {head - 2:.1f} H{hw - pad}" stroke="{COLORS["ink"]}" stroke-width="4" stroke-dasharray="12 10"/>' if title else ""
    else:
        hc = col(it.get("head", "#2259C7"))
        shape = f'<rect x="{-hw}" y="0" width="{w}" height="{H:.1f}" rx="22" fill="#FFFFFF" stroke="{COLORS["ink"]}" stroke-width="6"/>'
        top = (f'<path d="M{-hw} {head:.1f} V22 Q{-hw} 0 {-hw + 22} 0 H{hw - 22} Q{hw} 0 {hw} 22 V{head:.1f} Z" fill="{hc}" stroke="{COLORS["ink"]}" stroke-width="6" stroke-linejoin="round"/>'
               f'<text x="0" y="{head * 0.69:.1f}" text-anchor="middle" {FONT} font-size="{fs}" font-weight="900" fill="#FFFFFF">{html.escape(title)}</text>') if title else ""
    body = ""; yy = head + 8
    for r in rows:
        c = col(r.get("c")); b = r.get("b", 800)
        if r.get("hl"):
            body += f'<rect x="{-hw + 10}" y="{yy + 5:.1f}" width="{w - 20}" height="{rh - 10:.1f}" rx="10" fill="#FFD45C"/>'
        base = yy + rh / 2 + fs * 0.36
        if r.get("r") in (None, ""):
            body += f'<text x="0" y="{base:.1f}" text-anchor="middle" {FONT} font-size="{fs}" font-weight="{b}" fill="{c}">{html.escape(str(r["l"]))}</text>'
        else:
            body += (f'<text x="{-hw + pad}" y="{base:.1f}" {FONT} font-size="{fs}" font-weight="{b}" fill="{c}">{html.escape(str(r["l"]))}</text>'
                     f'<text x="{hw - pad}" y="{base:.1f}" text-anchor="end" {FONT} font-size="{fs}" font-weight="900" fill="{c}">{html.escape(str(r["r"]))}</text>')
        if r.get("strike"):
            body += f'<path d="M{-hw + 14} {yy + rh / 2:.1f} H{hw - 14}" stroke="#D5372F" stroke-width="7" stroke-linecap="round"/>'
        yy += rh
    rot = it.get("rot", 0)
    return f'<g transform="translate({x} {y}) rotate({rot})">{shape}{top}{body}</g>'


def say(it):
    x, y = it["x"], it["y"]; fs = it.get("fs", 42); lines = str(it["text"]).split("|")
    w = it.get("w") or max(tw(l, fs) for l in lines) + 64; h = fs * 1.24 * len(lines) + 44; hw = w / 2; hh = h / 2
    tail = it.get("tail", "down")
    t = {"left": f"M{-hw + 40} {hh - 3} L{-hw + 8} {hh + 44} L{-hw + 96} {hh - 3}", "right": f"M{hw - 40} {hh - 3} L{hw - 8} {hh + 44} L{hw - 96} {hh - 3}",
         "down": f"M-26 {hh - 3} L0 {hh + 44} L26 {hh - 3}", "none": ""}[tail]
    s = f'<rect x="{-hw}" y="{-hh}" width="{w}" height="{h}" rx="28" fill="#FFFFFF" stroke="{COLORS["ink"]}" stroke-width="5"/>'
    if t:
        s += f'<path d="{t}" fill="#FFFFFF" stroke="{COLORS["ink"]}" stroke-width="5" stroke-linejoin="round"/><rect x="{-hw + 8}" y="{hh - 8}" width="{w - 16}" height="9" fill="#FFFFFF"/>'
    for k, l in enumerate(lines):
        s += f'<text x="0" y="{-hh + 22 + fs * 0.98 + fs * 1.24 * k:.1f}" text-anchor="middle" {FONT} font-size="{fs}" font-weight="800" fill="{col(it.get("color"))}">{html.escape(l)}</text>'
    return f'<g transform="translate({x} {y})">{s}</g>'


def stamp(it):
    x, y = it["x"], it["y"]; fs = it.get("fs", 50); c = col(it.get("color", "red")); t = str(it["text"]); w = tw(t, fs) + 46; h = fs * 1.5
    return (f'<g transform="translate({x} {y}) rotate({it.get("rot", -10)})"><rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="10" fill="#FFFFFF" fill-opacity="0.9" stroke="{c}" stroke-width="7"/>'
            f'<text x="0" y="{fs * 0.36}" text-anchor="middle" {FONT} font-size="{fs}" font-weight="900" fill="{c}">{html.escape(t)}</text></g>')


def order_book_open(svg, G):
    """Open the spread band by G px, the way the reel does at rest, for the static first frame."""
    svg = svg.replace('<g class="obtop"', f'<g class="obtop" transform="translate(0,-{G})"')
    svg = svg.replace('<g class="obasks"', f'<g class="obasks" transform="translate(0,-{G})"')
    svg = svg.replace('<g class="obbids"', f'<g class="obbids" transform="translate(0,{G})"')
    svg = re.sub(r'(class="ob[ce]" data-nodraw="1" x="[^"]+" )y="([^"]+)" width="([^"]+)" height="([^"]+)"',
                 lambda m: f'{m.group(1)}y="{float(m.group(2)) - G}" width="{m.group(3)}" height="{float(m.group(4)) + 2 * G}"', svg)
    return svg


def item_svg(it):
    p = it["p"]
    if p == "text": return text_item(it)
    if p == "board": return board(it)
    if p == "say": return say(it)
    if p == "stamp": return stamp(it)
    if p == "raw": return it["svg"]
    clean = {k: v for k, v in it.items() if k not in ("open_gap", "hide_sizes", "spread_text")}
    svg = L.item_svg(clean)
    if p == "order_book":
        if it.get("open_gap"): svg = order_book_open(svg, it["open_gap"])
        svg = re.sub(r'<path class="obla".*?/>', "", svg)  # the band's arrow is a dot before it animates
        if it.get("hide_sizes"):  # the post has prices but no share counts, so none are drawn
            svg = re.sub(r'<text class="obq".*?</text>', "", svg); svg = re.sub(r'<rect class="obb".*?/>', "", svg); svg = re.sub(r'<text[^>]*>Shares</text>', "", svg)
        if it.get("spread_text"): svg = svg.replace(">Spread</text>", f">{html.escape(it['spread_text'])}</text>")
    return svg


def page_html(spec, logo_b64):
    fmt = spec.get("format", "definition"); c0, k0 = FORMATS.get(fmt, FORMATS["definition"])
    colr = spec.get("color", c0); pill = spec.get("pill", k0); title = spec["title"]
    for word, what in ((title, "title"), (pill, "pill")):
        if "!" in word or word.rstrip().endswith("."):
            raise ValueError(f"{spec['id']}: {what} {word!r} has an exclamation point or a trailing full stop")
    t = re.sub(r"\*(.+?)\*", r'<span class="k">\1</span>', html.escape(title))
    art = "".join(f'<g data-i="{i}" data-p="{it["p"]}">{item_svg(it)}</g>' for i, it in enumerate(spec.get("items", [])))
    return f'''<!doctype html><meta charset="utf-8"><link rel=stylesheet href="https://fonts.googleapis.com/css2?family=Inter:wght@700;800;900&display=swap"><style>
html,body{{margin:0;width:1080px;height:1920px;background:#FBFAF6;overflow:hidden;font-family:Inter,sans-serif}}
.pill{{position:absolute;top:290px;left:50%;transform:translateX(-50%);background:{colr};color:#fff;font:800 34px Inter;padding:18px 34px;border-radius:40px;white-space:nowrap}}
.t{{position:absolute;top:385px;left:60px;right:60px;text-align:center;font:900 {spec.get("title_fs", 92)}px/1.08 Inter;color:#0F172A;letter-spacing:-.01em;text-wrap:balance}}
.k{{white-space:nowrap;background-image:linear-gradient(transparent 55%,#FFD45C 55%,#FFD45C 93%,transparent 93%);padding:0 8px}}
svg{{position:absolute;inset:0}} img{{position:absolute;left:420px;top:1455px;width:240px}}</style>
<svg viewBox="0 0 1080 1920" width="1080" height="1920">{art}</svg><div class=pill>{html.escape(pill)}</div><div class=t>{t}</div><img id=logo src="data:image/png;base64,{logo_b64}">'''


SHOT_JS = r"""
const p = require('puppeteer-core'), fs = require('fs'), path = require('path');
const jobs = JSON.parse(fs.readFileSync(process.argv[2]));
const check = () => {
  const out = [], R = e => e.getBoundingClientRect();
  const t = document.querySelector('.t'), logo = document.getElementById('logo'), tr = R(t), lr = R(logo);
  const lines = Math.round(tr.height / parseFloat(getComputedStyle(t).lineHeight));
  if (lines > 3) out.push(`title has ${lines} lines`);
  if (tr.width && t.scrollWidth > t.clientWidth + 2) out.push('title wider than the canvas');
  const hit = (a, b, m = 0) => a.left < b.right - m && b.left < a.right - m && a.top < b.bottom - m && b.top < a.bottom - m;
  const groups = [...document.querySelectorAll('svg > g[data-i]')], texts = [];
  for (const g of groups) {
    const r = R(g), who = `${g.dataset.p}#${g.dataset.i}`;
    if (!r.width) continue;
    if (hit(r, tr, 4)) out.push(`${who} over the title (art top ${Math.round(r.top)}, title bottom ${Math.round(tr.bottom)})`);
    if (hit(r, lr, 4)) out.push(`${who} over the logo`);
    if (r.left < 12 || r.right > 1068) out.push(`${who} outside the canvas (${Math.round(r.left)} to ${Math.round(r.right)})`);
    if (r.bottom > 1540) out.push(`${who} in the bottom safe area (${Math.round(r.bottom)})`);
    for (const e of g.querySelectorAll('text')) {
      const b = R(e); if (!b.width || !e.textContent.trim()) continue;
      const m = e.getScreenCTM(), px = parseFloat(getComputedStyle(e).fontSize) * Math.hypot(m.a, m.b);
      if (px < 33.5) out.push(`${who} text "${e.textContent}" is ${px.toFixed(1)} px`);
      if (b.left < 12 || b.right > 1068) out.push(`${who} text "${e.textContent}" leaves the canvas`);
      texts.push({ who, s: e.textContent, b });
    }
  }
  for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++)
    if (hit(texts[i].b, texts[j].b, Math.max(7, 0.24 * Math.min(texts[i].b.height, texts[j].b.height)))) out.push(`text "${texts[i].s}" (${texts[i].who}) touches "${texts[j].s}" (${texts[j].who})`);
  return { warnings: out, titleBottom: Math.round(tr.bottom), artTop: Math.round(Math.min(...groups.map(g => R(g).top).filter(v => v > 0), 9999)) };
};
(async () => {
  const b = await p.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', timeout: 240000 });
  const g = await b.newPage(); await g.setViewport({ width: 1080, height: 1920 });
  for (const j of jobs) {
    await g.goto('file://' + j.html, { waitUntil: 'networkidle0', timeout: 60000 });
    await g.evaluate(() => document.fonts.ready);
    const res = await g.evaluate(check);
    if (!j.checkOnly) {
      await g.screenshot({ path: j.png });
      await g.screenshot({ path: j.jpg, type: 'jpeg', quality: 92 });
    }
    console.log(JSON.stringify({ id: j.id, ...res }));
  }
  await b.close();
})();
"""


def main():
    ap = argparse.ArgumentParser(description="Make Edlintics Short thumbnails from JSON specs")
    ap.add_argument("specs", nargs="+")
    ap.add_argument("--out", required=True, help="folder for <id>.jpg (and <id>.png unless --png-dir)")
    ap.add_argument("--png-dir", help="folder for <id>.png")
    ap.add_argument("--html-dir", help="keep the HTML pages here")
    ap.add_argument("--check-only", action="store_true", help="run the checks without writing images")
    a = ap.parse_args()
    specs = []
    for f in a.specs:
        d = json.load(open(f)); specs += d if isinstance(d, list) else [d]
    logo = base64.b64encode(open(os.path.join(HERE, "logo", "edlintics-logo.png"), "rb").read()).decode()
    out = os.path.abspath(a.out); pngd = os.path.abspath(a.png_dir or a.out); os.makedirs(out, exist_ok=True); os.makedirs(pngd, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        hd = os.path.abspath(a.html_dir) if a.html_dir else tmp; os.makedirs(hd, exist_ok=True); jobs = []
        for s in specs:
            h = os.path.join(hd, s["id"] + ".html")
            open(h, "w").write(page_html(s, logo))
            jobs.append({"id": s["id"], "html": h, "png": os.path.join(pngd, s["id"] + ".png"), "jpg": os.path.join(out, s["id"] + ".jpg"), "checkOnly": a.check_only})
        jp = os.path.join(tmp, "jobs.json"); json.dump(jobs, open(jp, "w")); js = os.path.join(tmp, "shot.js"); open(js, "w").write(SHOT_JS)
        env = dict(os.environ, NODE_PATH=os.path.join(HERE, "node_modules"))
        r = subprocess.run(["nice", "-n", "15", "node", js, jp], env=env, capture_output=True, text=True)
        if r.returncode:
            sys.exit(r.stderr[-2000:])
        bad = 0
        for line in r.stdout.splitlines():
            d = json.loads(line)
            for w in d["warnings"]:
                print(f'CHECK {d["id"]}: {w}'); bad += 1
            print(f'{d["id"]}: title bottom {d["titleBottom"]}, art top {d["artTop"]}')
        print(f"{len(jobs)} thumbnail(s), {bad} check(s) to fix")


if __name__ == "__main__":
    main()
