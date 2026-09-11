#!/usr/bin/env python3
"""
Build the social profile assets (avatars + covers) for the Edlintics rebrand.

Composes each asset as HTML/SVG using the REAL brand geometry — the BrandMark tie
paths and the EdCharacter cast SVGs vendored from the app — then rasterizes with
headless Chrome at exact platform pixel dimensions.

Why not an image generator: the cast, the mark and the gradient are fixed vector
geometry. Redrawing them with a diffusion model produces a lookalike, not the brand.

Usage:  python3 scripts/build_social_assets.py [name ...]
Output: assets/renders/social/*.png
"""

import base64
import pathlib
import shutil
import subprocess
import time
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = ROOT.parent / "tutoring-web"
MASCOTS = APP / "public" / "mascot"
OUT = ROOT / "assets" / "renders" / "social"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SHOW_GUIDES = False  # set by --guides; draws safe-zone / occlusion proofs

# --- brand tokens (config/brand.ts / tutoring-web docs/product/brand.md) -------
BLUE = "#467DE3"          # primary — edlintics blue
BLUE_400 = "#60A5FA"      # gradient terminus
BLUE_DEEP = "#2F58A8"     # BrandMark gradient end
BLUE_LIGHT = "#6FA0F0"    # BrandMark gradient start
INK = "#0F172A"           # near-black slate
CREAM = "#FBFAF6"         # cast body cream / warm paper
BLOB = "#E8F0FE"          # light blue field (homepage og)
MUTED = "#64748B"
HAIRLINE = "#E3E6EB"

# Latin-subset webfonts are vendored in assets/fonts/ and embedded as data URIs.
# The generator is deliberately hermetic: headless Chrome makes no network request,
# so a render is byte-reproducible and never blocks on a CDN.
FONT_FACES = [
    ("Inter", 600, "inter-600.woff2"),
    ("Inter", 700, "inter-700.woff2"),
    ("Inter", 800, "inter-800.woff2"),
    ("Source Serif 4", 700, "serif-700.woff2"),
    ("Lato", 700, "lato-700.woff2"),
]


def font_css() -> str:
    out = []
    for family, weight, filename in FONT_FACES:
        path = ROOT / "assets" / "fonts" / filename
        b64 = base64.b64encode(path.read_bytes()).decode()
        out.append(f"@font-face{{font-family:'{family}';font-weight:{weight};font-style:normal;"
                   f"font-display:block;src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "".join(out)


def mascot(name: str) -> str:
    """Inline an EdCharacter SVG as a data URI (exact vendored geometry)."""
    raw = (MASCOTS / f"{name}.svg").read_bytes()
    return "data:image/svg+xml;base64," + base64.b64encode(raw).decode()


def tie_mark(size: int, variant: str = "full", gid: str = "g1") -> str:
    """The BrandMark necktie, geometry copied from components/brand/BrandMark.tsx."""
    w = size * 64 / 92
    collar = (
        f'<path d="M32 2 L4 2 L28 27 Z" fill="url(#{gid})" opacity="0.82"/>'
        f'<path d="M32 2 L60 2 L36 27 Z" fill="url(#{gid})" opacity="0.82"/>'
    ) if variant == "full" else ""
    return f'''<svg width="{w}" height="{size}" viewBox="0 0 64 92" aria-hidden="true">
  <defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BLUE_LIGHT}"/><stop offset="1" stop-color="{BLUE_DEEP}"/>
  </linearGradient></defs>
  {collar}
  <path d="M24 6 L40 6 L44 24 L20 24 Z" fill="url(#{gid})"/>
  <path d="M20 24 L22 36 L8 64 L32 90 L56 64 L42 36 L44 24 Z" fill="url(#{gid})"/>
</svg>'''


def wordmark(px: int) -> str:
    """Ed + lintics gradient wordmark, locked to the brand treatment."""
    return (f'<span style="font-family:Inter;font-weight:800;font-size:{px}px;'
            f'letter-spacing:-.03em;color:{INK};line-height:1">Ed'
            f'<span style="background:linear-gradient(90deg,{BLUE},{BLUE_400});'
            f'-webkit-background-clip:text;background-clip:text;color:transparent">lintics</span></span>')


def lockup(mark_px: int, word_px: int, gap: int, gid: str) -> str:
    return (f'<div style="display:flex;align-items:center;gap:{gap}px">'
            f'{tie_mark(mark_px, "full", gid)}{wordmark(word_px)}</div>')


# --- reusable "accounting graphic" cards, matching the homepage og card style --
def card(inner: str, pad: int, radius: int, extra: str = "") -> str:
    return (f'<div style="background:#fff;border:1px solid {HAIRLINE};border-radius:{radius}px;'
            f'padding:{pad}px;box-shadow:0 8px 28px rgba(15,23,42,.07);{extra}">{inner}</div>')


def t_account(scale: float = 1.0) -> str:
    s = lambda v: round(v * scale)
    return card(
        f'<div style="font-family:Inter;font-weight:700;font-size:{s(15)}px;color:{INK};'
        f'text-align:center;padding-bottom:{s(9)}px">Cash</div>'
        f'<div style="display:flex;border-top:1px solid {HAIRLINE};font-family:Inter;'
        f'font-size:{s(13)}px;font-weight:600">'
        f'<div style="flex:1;padding:{s(9)}px {s(14)}px {s(20)}px;color:{BLUE};'
        f'border-right:1px solid {HAIRLINE}">Debit</div>'
        f'<div style="flex:1;padding:{s(9)}px {s(14)}px {s(20)}px;color:{MUTED}">Credit</div></div>',
        pad=s(8), radius=s(10), extra="min-width:%dpx" % s(132))


def equation(scale: float = 1.0) -> str:
    s = lambda v: round(v * scale)
    return card(
        f'<div style="font-family:Inter;font-weight:700;font-size:{s(15)}px;color:{INK};'
        f'white-space:nowrap">Assets = Liabilities + Equity</div>',
        pad=s(14), radius=s(10))


def chart(scale: float = 1.0) -> str:
    s = lambda v: round(v * scale)
    w, h = s(170), s(84)
    return card(
        f'<svg width="{w}" height="{h}" viewBox="0 0 170 84" aria-hidden="true">'
        f'<line x1="6" y1="70" x2="164" y2="18" stroke="{BLUE}" stroke-width="3" stroke-linecap="round"/>'
        f'<line x1="6" y1="30" x2="164" y2="60" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        f'<circle cx="92" cy="46" r="4.5" fill="{INK}"/></svg>',
        pad=s(10), radius=s(10))


def journal(scale: float = 1.0) -> str:
    """A two-line journal entry card — Dr / Cr with round numbers."""
    s = lambda v: round(v * scale)
    row = lambda label, amt, indent, color: (
        f'<div style="display:flex;justify-content:space-between;gap:{s(26)}px;'
        f'padding-left:{indent}px;color:{color}">'
        f'<span>{label}</span><span style="font-family:Lato;font-weight:700">{amt}</span></div>')
    return card(
        f'<div style="font-family:Inter;font-size:{s(13)}px;font-weight:600;'
        f'line-height:{s(24)}px;color:{INK}">'
        + row("Dr&nbsp; Depreciation", "9,000", 0, INK)
        + row("Cr&nbsp; Acc. depreciation", "9,000", s(14), MUTED) + "</div>",
        pad=s(13), radius=s(10))


# ------------------------------------------------------------------ page shell
def page(w: int, h: int, body: str, bg: str = CREAM) -> str:
    return f'''<!doctype html><html><head><meta charset="utf-8">
<style>{font_css()}
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{width:{w}px;height:{h}px;overflow:hidden}}
  body{{background:{bg};font-family:Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
  .stage{{position:relative;width:{w}px;height:{h}px;overflow:hidden}}
  .abs{{position:absolute}}
  .serif{{font-family:"Source Serif 4",Georgia,serif}}
  .grad{{background:linear-gradient(90deg,{BLUE},{BLUE_400});-webkit-background-clip:text;
        background-clip:text;color:transparent}}
</style></head><body><div class="stage">{body}</div></body></html>'''


def blob(cx, cy, rx, ry, color=BLOB, extra=""):
    return (f'<div class="abs" style="left:{cx-rx}px;top:{cy-ry}px;width:{rx*2}px;height:{ry*2}px;'
            f'background:{color};border-radius:50%;{extra}"></div>')


def frame(px: int, color: str = BLUE) -> str:
    return (f'<div class="abs" style="inset:0;border:{px}px solid {color};'
            f'pointer-events:none;z-index:5"></div>')


def char(name: str, top: int, left: int, height: int, rotate: float = 0) -> str:
    rot = f"transform:rotate({rotate}deg);" if rotate else ""
    return (f'<img class="abs" src="{mascot(name)}" style="top:{top}px;left:{left}px;'
            f'height:{height}px;{rot}" alt="">')


# ================================================================== the assets
def avatar(size: int, gid: str) -> str:
    """The logo mark on white: blue gradient tie, white ground.

    Note this is the inverse of the app icon (`public/brand/favicon-512.png`), which is a
    white tie on the blue gradient. Hoang's call for social: the profile picture reads as
    the logo, so it uses the logo's own colours and matches the lockup on the covers.

    All three platforms crop the avatar to a circle, so the mark sits at 0.62 of the frame
    — its diagonal half-extent (0.39) clears the inscribed circle (0.5) with room to spare.
    """
    mark = round(size * 0.62)
    return page(size, size,
        f'<div class="abs" style="inset:0;display:flex;align-items:center;justify-content:center">'
        f'{tie_mark(mark, "full", gid)}</div>', bg="#FFFFFF")


def guides(regions) -> str:
    """Optional overlay: dashed safe zone + the area the profile photo covers.
    Rendered only for the *-guides proofs, never on the shipping asset."""
    if not SHOW_GUIDES:
        return ""
    out = []
    for x, y, w, h, label, color in regions:
        out.append(
            f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'border:3px dashed {color};z-index:20;pointer-events:none">'
            f'<span style="position:absolute;top:6px;left:10px;font-family:Inter;font-weight:700;'
            f'font-size:20px;color:{color};background:#fff;padding:2px 8px;border-radius:4px">'
            f'{label}</span></div>')
    return "".join(out)


def fb_cover() -> str:
    """1640x624 = 2x of Facebook's 820x312 desktop cover.

    Two occlusions drive this layout:
      - mobile crops ~90px per side at 1x, so the safe zone is the centre
        1280px: x 180 -> 1460.
      - the page profile photo overlaps the lower-left of the cover on desktop,
        roughly x 30-390 / y 370-624. Nothing legible goes there.
    """
    W, H = 1640, 624
    return page(W, H,
        blob(1180, 300, 450, 340)
        + f'<div class="abs" style="top:58px;left:206px">{lockup(46, 38, 16, "fb")}</div>'
        # 60px x 3 lines from y=150 ends at ~357, clearing the profile photo (y>=370).
        + f'<div class="abs serif" style="top:150px;left:206px;width:640px;font-weight:700;'
          f'font-size:60px;line-height:1.14;color:{INK};letter-spacing:-.02em">'
          f'Your entrance into<br>the <span class="grad">language of<br>business</span></div>'
        # accounting graphics — all inside x <= 1450
        + f'<div class="abs" style="top:66px;left:970px">{t_account(1.2)}</div>'
        + f'<div class="abs" style="top:88px;left:1176px">{equation(1.0)}</div>'
        + f'<div class="abs" style="top:452px;left:1252px">{chart(0.95)}</div>'
        + f'<div class="abs" style="top:462px;left:906px">{journal(0.92)}</div>'
        # the cast
        + char("ledger", top=186, left=1096, height=224)
        + char("centi", top=284, left=944, height=142)
        + char("plot", top=262, left=1300, height=148)
        + guides([(180, 0, 1280, 624, "mobile safe zone", "#DC2626"),
                  (30, 370, 360, 254, "profile photo", "#7C3AED")])
        + frame(8))


def li_banner() -> str:
    """4200x700 — LinkedIn's official 6:1 company-page upload spec.

    Occlusions:
      - mobile crops to the centre ~900 of the 1128 display width (~80%), so the
        safe zone is the centre 3350px: x 425 -> 3775.
      - the company logo tile overlaps the lower-left, roughly x 150-700 /
        y 400-700.
    """
    W, H = 4200, 700
    return page(W, H,
        blob(3000, 350, 860, 420)
        + f'<div class="abs" style="top:96px;left:762px">{lockup(58, 48, 20, "li")}</div>'
        + f'<div class="abs serif" style="top:212px;left:762px;width:1440px;font-weight:700;'
          f'font-size:88px;line-height:1.16;color:{INK};letter-spacing:-.02em">'
          f'Your entrance into the<br><span class="grad">language of business</span></div>'
        + f'<div class="abs" style="top:474px;left:764px;font-family:Lato;font-weight:700;'
          f'font-size:26px;letter-spacing:.18em;color:{MUTED}">'
          f'WORKED EXAMPLES &middot; EXAM-TARGETED PRACTICE</div>'
        + f'<div class="abs" style="top:186px;left:2160px">{t_account(1.4)}</div>'
        + f'<div class="abs" style="top:104px;left:2800px">{equation(1.4)}</div>'
        + f'<div class="abs" style="top:474px;left:2760px">{journal(1.15)}</div>'
        + f'<div class="abs" style="top:150px;left:3420px">{chart(1.25)}</div>'
        + char("ledger", top=200, left=2490, height=290)
        + char("centi", top=372, left=2318, height=164)
        + char("plot", top=344, left=3286, height=184)
        + char("sigma", top=396, left=3606, height=156)
        + guides([(425, 0, 3350, 700, "mobile safe zone", "#DC2626"),
                  (150, 400, 550, 300, "company logo", "#7C3AED")])
        + frame(10))


def ig_tile(kind: str) -> str:
    """Instagram has no cover photo. These are 1080x1350 pinned posts that act as
    the profile header row. Post in reverse order so tile 1 lands top-left."""
    W, H = 1080, 1350
    if kind == "statement":
        return page(W, H,
            blob(540, 1180, 620, 420)
            + f'<div class="abs" style="top:96px;left:96px">{lockup(58, 48, 20, "ig1")}</div>'
            + f'<div class="abs serif" style="top:300px;left:96px;width:900px;font-weight:700;'
              f'font-size:104px;line-height:1.12;color:{INK};letter-spacing:-.025em">'
              f'Your entrance into the <span class="grad">language of business</span></div>'
            + f'<div class="abs" style="top:800px;left:98px;font-family:Lato;font-weight:700;'
              f'font-size:28px;letter-spacing:.16em;color:{MUTED}">'
              f'FINANCE &amp; ACCOUNTING, WORKED THROUGH</div>'
            + char("ledger", top=930, left=390, height=330)
            + frame(10))
    if kind == "cast":
        return page(W, H,
            blob(540, 706, 424, 424)
            + f'<div class="abs" style="top:96px;left:96px">{lockup(58, 48, 20, "ig2")}</div>'
            + f'<div class="abs" style="top:284px;left:126px">{t_account(1.55)}</div>'
            + f'<div class="abs" style="top:322px;left:606px">{equation(1.2)}</div>'
            + f'<div class="abs" style="top:996px;left:138px">{journal(1.22)}</div>'
            + f'<div class="abs" style="top:1006px;left:632px">{chart(1.22)}</div>'
            + char("ledger", top=560, left=396, height=356)
            + char("centi", top=744, left=172, height=196)
            + char("plot", top=724, left=742, height=210)
            + f'<div class="abs" style="top:1232px;left:98px;font-family:Lato;font-weight:700;'
              f'font-size:26px;letter-spacing:.15em;color:{MUTED}">'
              f'DEBITS &middot; CREDITS &middot; CASH FLOW &middot; DEFERRED TAX</div>'
            + frame(10))
    # "concept"
    return page(W, H,
        blob(880, 1130, 520, 400)
        + f'<div class="abs" style="top:96px;left:96px">{lockup(58, 48, 20, "ig3")}</div>'
        + f'<div class="abs" style="top:296px;left:96px;font-family:Lato;font-weight:700;'
          f'font-size:28px;letter-spacing:.16em;color:{BLUE}">THE PART THAT LOSES MARKS</div>'
        + f'<div class="abs serif" style="top:360px;left:96px;width:890px;font-weight:700;'
          f'font-size:88px;line-height:1.14;color:{INK};letter-spacing:-.02em">'
          f'Profit was €2m. Cash <span class="grad">fell €1m.</span> Both are correct.</div>'
        + f'<div class="abs" style="top:706px;left:96px">{journal(1.35)}</div>'
        + char("sigma", top=956, left=690, height=310)
        + frame(10))


ASSETS = {
    "avatar-instagram": (lambda: avatar(320, "av1"), 320, 320),
    "avatar-facebook":  (lambda: avatar(320, "av2"), 320, 320),
    "avatar-linkedin":  (lambda: avatar(400, "av3"), 400, 400),
    "cover-facebook":   (fb_cover, 1640, 624),
    "cover-linkedin":   (li_banner, 4200, 700),
    "instagram-tile-1-statement": (lambda: ig_tile("statement"), 1080, 1350),
    "instagram-tile-2-cast":      (lambda: ig_tile("cast"), 1080, 1350),
    "instagram-tile-3-concept":   (lambda: ig_tile("concept"), 1080, 1350),
}


def render(name, builder, w, h):
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = pathlib.Path(tempfile.mkdtemp())
    html = tmp / f"{name}.html"
    html.write_text(builder(), encoding="utf-8")
    dest = OUT / f"{name}.png"
    if dest.exists():
        dest.unlink()
    # Chrome 150 headless writes the screenshot and then does not always exit. So we poll for
    # the file to appear and stop growing, then terminate it ourselves. Fonts are embedded, so
    # there is no network wait — the render itself is effectively instant.
    proc = subprocess.Popen([
        CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
        "--no-default-browser-check", "--disable-extensions", "--mute-audio",
        f"--window-size={w},{h}", "--force-device-scale-factor=1",
        "--default-background-color=FFFFFFFF",
        f"--screenshot={dest}", f"--user-data-dir={tmp}/prof", html.as_uri(),
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        deadline, last, stable = time.time() + 60, -1, 0
        while time.time() < deadline:
            if proc.poll() is not None:
                break
            size = dest.stat().st_size if dest.exists() else -1
            stable = stable + 1 if size == last and size > 0 else 0
            last = size
            if stable >= 3:  # unchanged across ~0.9s — the write is done
                break
            time.sleep(0.3)
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
    if not dest.exists() or dest.stat().st_size == 0:
        raise RuntimeError(f"render failed for {name}")
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"  {dest.relative_to(ROOT)}  ({w}x{h})")


if __name__ == "__main__":
    if not MASCOTS.exists():
        sys.exit(f"Character SVGs not found at {MASCOTS}")
    argv = [a for a in sys.argv[1:] if a != "--guides"]
    SHOW_GUIDES = "--guides" in sys.argv
    wanted = argv or list(ASSETS)
    suffix = "-guides" if SHOW_GUIDES else ""
    print("Rendering social assets:")
    for n in wanted:
        if n not in ASSETS:
            sys.exit(f"Unknown asset '{n}'. Known: {', '.join(ASSETS)}")
        builder, w, h = ASSETS[n]
        render(n + suffix, builder, w, h)
