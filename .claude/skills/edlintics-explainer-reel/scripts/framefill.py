"""Frame-fill check (1 Nov 2026, Hoang: "use more of the phone screen"). Measures how much of the 9:16 frame each beat uses.

Usage: tools/tts/.venv/bin/python framefill.py <workdir> [min_safe_share=0.75]
Reads <workdir>/stills/still-*.png (one per beat, from make_reel.sh) and <workdir>/scenes.json (for the layout).
For every still it finds the ink (pixels that differ clearly from the paper colour, so the paper grain and the pale wall
tint do not count), leaves out the logo, and reports:
  frame   the content bounding box (captions + art) as a share of the whole 1080x1920 frame
  safe    the share of the platform safe area (x 0-940, y 220-1540: top 220 px, bottom 380 px and right 140 px are
          covered by the app UI) that the content box covers
  span    the content's top and bottom y
  rows    the share of the safe area's rows (y 220-1540) that hold any ink: empty bands between captions and art,
          or under the art, lower it even when the box is tall
  ui      the share of ink that falls in the UI zones (top 220, bottom 380, right 140 px)
It also checks caption sync: every caption chunk in timing.json starts inside its own voice line.
The end card is reported but left out of the means. For the full-frame layout (meta.layout "full", how-to reels) it FAILs (exit 1) when the mean safe share is
under min_safe_share or any beat puts more than 2% of its ink in the UI zones. Other reel types only report.
"""
import glob, json, re, sys
import numpy as np
from PIL import Image

d = sys.argv[1]; MIN = float(sys.argv[2]) if len(sys.argv) > 2 else 0.75
SAFE = (0, 220, 940, 1540)   # x0, y0, x1, y1
try: S = json.load(open(f"{d}/scenes.json")); layout = S.get("layout", "reel"); beats = S["beats"]
except Exception: layout, beats = "reel", []
LOGO = {"full": (390, 1455, 590, 1520)}.get(layout, (430, 1330, 650, 1400))   # logo box per layout, left out of the measure
stills = sorted(glob.glob(f"{d}/stills/still-*.png"), key=lambda p: float(re.search(r"still-([\d.]+)\.png", p)[1]))
if not stills: sys.exit("no stills; run make_reel.sh first (STILLS_ONLY=1 is enough)")
paper = np.array([251, 250, 246], dtype=np.int16)
rows = []
for k, p in enumerate(stills):
    a = np.asarray(Image.open(p).convert("RGB"), dtype=np.int16)
    ink = np.abs(a - paper).max(axis=2) > 40
    x0, y0, x1, y1 = LOGO; ink[y0:y1, x0:x1] = False
    ys = np.where(ink.sum(axis=1) >= 3)[0]; xs = np.where(ink.sum(axis=0) >= 3)[0]
    if not len(ys): rows.append((k, 0, 0, 0, 0, 0, 0, 0)); continue
    top, bot, lef, rig = ys[0], ys[-1], xs[0], xs[-1]
    frame = (bot - top) * (rig - lef) / (1080 * 1920)
    ix = max(0, min(rig, SAFE[2]) - max(lef, SAFE[0])); iy = max(0, min(bot, SAFE[3]) - max(top, SAFE[1]))
    safe = ix * iy / ((SAFE[2] - SAFE[0]) * (SAFE[3] - SAFE[1]))
    ui_mask = np.zeros_like(ink); ui_mask[:SAFE[1]] = True; ui_mask[SAFE[3]:] = True; ui_mask[:, SAFE[2]:] = True
    ui = (ink & ui_mask).sum() / max(1, ink.sum())
    rws = (ink[SAFE[1]:SAFE[3], :SAFE[2]].sum(axis=1) >= 3).mean()
    rows.append((k, frame, safe, top, bot, ui, (beats[k].get("role") if k < len(beats) else ""), rws))
print(f"layout {layout}: {len(rows)} stills")
print(" beat  role       frame   safe   rows   span y      ui-zone ink")
for k, fr, sa, top, bot, ui, role, rw in rows:
    print(f" {k + 1:>4}  {str(role):<9} {fr:6.1%} {sa:6.1%} {rw:6.1%}   {top:>4}-{bot:<4}   {ui:5.1%}")
body = [r for r in rows if r[6] not in ("endcard", "defcard")]
mf = np.mean([r[1] for r in body]); ms = np.mean([r[2] for r in body]); mb = np.mean([r[4] for r in body]); mr = np.mean([r[7] for r in body])
print(f"MEAN (without end card): frame {mf:.1%}, safe area {ms:.1%}, rows {mr:.1%}, content bottom y {mb:.0f}")
E = []
if layout == "full":
    if ms < MIN: E.append(f"mean safe-area share {ms:.1%} is under {MIN:.0%}: make the scenes bigger")
    for k, fr, sa, top, bot, ui, role, rw in rows:
        if ui > 0.02 and role != "defcard": E.append(f"beat {k + 1}: {ui:.1%} of the ink sits in the UI zones (top 220, bottom 380, right 140 px)")
# caption sync: every caption chunk must start inside its own voice line (timing.json from vo.py)
try:
    T = json.load(open(f"{d}/timing.json")); bad = 0
    for k, b in enumerate(T["beats"], 1):
        for c in b.get("chunks", []):
            if not b["start"] - 0.15 <= c["t"] <= b["end"]:
                bad += 1; msg = f'beat {k}: caption "{c["text"]}" starts at {c["t"]} s, outside its voice line {b["start"]}-{b["end"]} s'
                (E.append(msg) if layout == "full" else print("WARN ", msg))
    print(f"caption sync: {sum(len(b.get('chunks', [])) for b in T['beats'])} chunks, {bad} outside their voice line")
except FileNotFoundError: pass
for e in E: print("FAIL ", e)
print("FRAMEFILL", "OK" if not E else "NOT OK"); sys.exit(1 if E else 0)
