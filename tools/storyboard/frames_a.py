#!/usr/bin/env python3
"""Edlintics demo video A: 13 storyboard stills plus 7 transition frames (T1..T7), drawn in code (SVG) and rendered with headless Chrome.

Run:  python3 frames_a.py            (all frames + sheet.png)
      python3 frames_a.py A3a A5b    (only those frames, sheet rebuilt from what exists)
Output goes next to this file, or to the folder named in the FRAMES_OUT environment variable.

Look (v4, after Hoang's notes of 20 Nov 2026): one flat saturated background per subject, a big
subject name with the topic under it, white cards with a flat offset block, no gradients (the
embedded logo file keeps its own). Every subject scene is two frames: "a" the question moment
(question card, object at its start, ghost arrow, Ledger puzzled) and "b" the solved moment
(object moved with an arrow, answer pop-up with a green tick, Ledger joyful).

Ledger: front-facing frames embed the real website rig states unchanged (think, confused, scratch,
joy, cheer). Frames where he works at something behind him use the straight back view drawn from
the rig numbers (assets/brand-handoff/ledger-v2/RIG.md); the three-quarter back view is gone
because its exposed page block read wrongly. Arms use the rig's two-segment arm (upper 23.3,
forearm 16.5, reach n <= 1.7); the script refuses to draw a longer arm.
"""
import math, os, re, subprocess, sys
from PIL import Image, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('FRAMES_OUT', HERE)
STATES = '/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing/assets/brand-handoff/ledger-v2/states'
LOGO = '/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing/assets/brand/edlintics-logo.svg'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
W, H = 1080, 1920

INK, CREAM, SUIT, BLUE, RULE = '#0F172A', '#FBFAF6', '#222C3D', '#467DE3', '#E6E3DA'
GREEN, RED, WHITE, BG, PAGES = '#16A34A', '#DC2626', '#FFFFFF', '#F3F7FE', '#F1EEE4'
TINT = '#DCE8FB'      # light blue tint of the lead colour
SLATE = '#64748B'     # secondary text
# one flat background per subject (accounting = emerald as in config/brand.ts), each with a darker floor tone
EMER, ORANGE, VIOLET, PINK, YEL = '#10B981', '#F97316', '#8B5CF6', '#EC4899', '#FBBF24'
EMER_D, ORANGE_D, VIOLET_D, PINK_D, YEL_D, BLUE_D = '#0B9468', '#DD5C0A', '#7443E0', '#D2307F', '#F2A60C', '#3565C4'
GREEN_T, RED_T, GREEN_D, RED_D, RED2 = '#DCFCE7', '#FEE2E2', '#15803D', '#B91C1C', '#EF4444'
FONT = "Rubik, Arial, Helvetica, sans-serif"
_F = {}


def font(size, bold):
    k = (round(size), bold)
    if k not in _F:
        p = '/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else '/System/Library/Fonts/Supplemental/Arial.ttf'
        _F[k] = ImageFont.truetype(p, round(size))
    return _F[k]


def tw(s, size, bold=True):
    return font(size, bold).getlength(s)


WARN = []


def T(x, y, s, size, weight=700, anchor='middle', fill=INK, maxw=None, check=True, extra=''):
    """Text. Measures with Arial and warns when it leaves the frame or its box. No trailing full stop."""
    assert not s.rstrip().endswith('.'), 'no full stop at the end of on-screen text: ' + s
    w = tw(s.replace('_', ''), size, weight >= 600)
    if check:
        x0 = x - w / 2 if anchor == 'middle' else (x if anchor == 'start' else x - w)
        if x0 < 24 or x0 + w > W - 24:
            WARN.append(f'text outside frame: "{s}" {x0:.0f}..{x0 + w:.0f}')
        if maxw and w > maxw:
            WARN.append(f'text wider than its box: "{s}" {w:.0f} > {maxw}')
    s = s.replace('&', '&amp;').replace('<', '&lt;')
    if '_' in s:                                # "H_0" draws the 0 as a subscript
        a, b = s.split('_', 1)
        d = size * 0.18
        s = f'{a}<tspan dy="{d:.1f}" font-size="{size * 0.62:.1f}">{b[0]}</tspan>'
        if b[1:]:
            s += f'<tspan dy="{-d:.1f}" font-size="{size}">{b[1:]}</tspan>'
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>')


def rrect(x, y, w, h, r=0, fill=WHITE, stroke=INK, sw=5, extra=''):
    st = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}" {st} {extra}/>'


def line(x1, y1, x2, y2, stroke=INK, sw=5, dash=None, cap='round', extra=''):
    d = f'stroke-dasharray="{dash}"' if dash else ''
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="{cap}" {d} {extra}/>')


def path(d, fill='none', stroke=INK, sw=5, dash=None, extra=''):
    da = f'stroke-dasharray="{dash}"' if dash else ''
    st = f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if stroke else ''
    return f'<path d="{d}" fill="{fill}" {st} {da} {extra}/>'


def circle(x, y, r, fill=WHITE, stroke=INK, sw=5):
    st = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" {st}/>'


def arrow_head(x, y, ang, size=22, fill=INK):
    """Filled triangle whose tip is at x,y and which points along ang (degrees, screen)."""
    a = math.radians(ang)
    p = []
    for da, r in ((0, 0), (155, size), (-155, size)):
        p.append((x + r * math.cos(a + math.radians(da)), y + r * math.sin(a + math.radians(da))))
    return f'<path d="M{p[0][0]:.1f} {p[0][1]:.1f} L{p[1][0]:.1f} {p[1][1]:.1f} L{p[2][0]:.1f} {p[2][1]:.1f} Z" fill="{fill}"/>'


def arrow(x1, y1, x2, y2, stroke=INK, sw=6, dash=None, head=22):
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    bx, by = x2 - 0.6 * head * math.cos(math.radians(ang)), y2 - 0.6 * head * math.sin(math.radians(ang))
    return line(x1, y1, bx, by, stroke, sw, dash) + arrow_head(x2, y2, ang, head, stroke)


def curve_arrow(x1, y1, cx, cy, x2, y2, stroke=BLUE, sw=6, dash='4 16', head=24):
    ang = math.degrees(math.atan2(y2 - cy, x2 - cx))
    return path(f'M{x1} {y1} Q{cx} {cy} {x2} {y2}', stroke=stroke, sw=sw, dash=dash) + arrow_head(
        x2 + 8 * math.cos(math.radians(ang)), y2 + 8 * math.sin(math.radians(ang)), ang, head, stroke)


def chip(label):
    w = tw(label, 46) + 96
    return rrect(540 - w / 2, 190, w, 96, 48, BLUE, None) + T(540, 254, label, 46, fill=WHITE)


def floor_line(x1, x2, y):
    return line(x1, y, x2, y, INK, 5)


def group(inner, cx, cy, rot=0, sc=1):
    return f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({rot}) scale({sc})">{inner}</g>'


# ---------------------------------------------------------------------------------------------
# Ledger
# ---------------------------------------------------------------------------------------------
UP, FORE, NMAX = 23.3, 16.5, 1.7
MOUTH = {'smile': (14, 0, 12, 12), 'calm': (10, 2, 5, 5), 'grin': (15, -1, 5, 21), 'open': (9, 1, -1, 17),
         'oh': (6, 2, -5, 13), 'shut': (11, 1, 6, 7)}

VIEWS = {
    # shoulders L/R, leg x positions, shoe left edges, which arm is nearer the viewer by default
    'front': dict(sh=(62, 178), legs=(102, 138), shoes=(87.5, 123.5)),
    'back':  dict(sh=(62, 178), legs=(102, 138), shoes=(87.5, 123.5)),
    '34f_l': dict(sh=(60, 176), legs=(98, 132), shoes=(83.5, 117.5)),    # faces viewer-left, page edges show on the right
    '34f_r': dict(sh=(64, 180), legs=(108, 142), shoes=(93.5, 127.5)),   # faces viewer-right, spine shows on the left
    'side_l': dict(sh=(120, 120), legs=(120,), shoes=(99.5,)),           # faces left, page edges
    'side_r': dict(sh=(120, 120), legs=(120,), shoes=(111.5,)),          # faces right, spine
}


class Ledger:
    """Ledger at feet point (X, Y) in frame pixels, scale sc (book is 136*sc wide in front view).
    rot leans the torso about the rig's tilt pivot (120,198); the legs stay upright, as in the rig."""

    def __init__(self, view, X, Y, sc, rot=0):
        self.view, self.X, self.Y, self.sc, self.rot = view, X, Y, sc, rot
        self.v = VIEWS[view]
        self.reach = []

    # rig (torso space) -> frame pixels
    def w(self, p):
        a = math.radians(self.rot)
        dx, dy = p[0] - 120, p[1] - 198
        x = 120 + dx * math.cos(a) - dy * math.sin(a)
        y = 198 + dx * math.sin(a) + dy * math.cos(a)
        return (self.X + (x - 120) * self.sc, self.Y + (y - 222) * self.sc)

    # frame pixels -> rig (torso space)
    def r(self, pw):
        x = 120 + (pw[0] - self.X) / self.sc
        y = 222 + (pw[1] - self.Y) / self.sc
        a = math.radians(-self.rot)
        dx, dy = x - 120, y - 198
        return (120 + dx * math.cos(a) - dy * math.sin(a), 198 + dx * math.sin(a) + dy * math.cos(a))

    def shoulder(self, side):
        return (self.v['sh'][0 if side == 'L' else 1], 152)

    def _arm(self, side, spec):
        sx, sy = self.shoulder(side)
        sign = -1 if side == 'L' else 1
        if self.view.startswith('side'):
            sign = -0.4 if self.view == 'side_l' else 0.4
        hand = spec.get('hand') if spec else None
        if hand is None:                        # rest pose from the rig
            ex, ey, hx, hy = sx + sign * 12, sy + 20, sx + sign * 8, sy + 36
        else:
            hx, hy = hand
            d = math.hypot(hx - sx, hy - sy)
            n = max(1.0, d / (UP + FORE) * 1.04)
            self.reach.append((side, round(d, 1), round(n, 2)))
            assert n <= NMAX, f'arm too long for the rig: reach {n:.2f} > {NMAX} ({side})'
            a, b = UP * n, FORE * n
            d = max(d, abs(a - b) + 0.5)
            along = (a * a - b * b + d * d) / (2 * d)
            hgt = math.sqrt(max(a * a - along * along, 0))
            ux, uy = (hx - sx) / d, (hy - sy) / d
            bend = spec.get('bend', 1)
            ex, ey = sx + along * ux + bend * hgt * (-uy), sy + along * uy + bend * hgt * ux
        d = f'M{sx:.1f} {sy:.1f} Q{ex:.1f} {ey:.1f} {hx:.1f} {hy:.1f}'
        return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="13" stroke-linecap="round"/>'
                f'<path d="{d}" fill="none" stroke="{CREAM}" stroke-width="8" stroke-linecap="round"/>'
                f'<circle cx="{hx:.1f}" cy="{hy + (2 if hand is None else 0):.1f}" r="9" fill="{CREAM}" stroke="{INK}" stroke-width="3"/>')

    @staticmethod
    def _slab(x, kind, w=25):
        s = f'<rect x="{x}" y="42" width="{w}" height="146" rx="5" fill="{PAGES if kind == "pages" else CREAM}" stroke="{INK}" stroke-width="4"/>'
        if kind == 'pages':
            n = 3 if w == 25 else 4
            for i in range(1, n + 1):
                lx = x + w * i / (n + 1)
                s += f'<line x1="{lx:.1f}" y1="48" x2="{lx:.1f}" y2="182" stroke="{INK}" stroke-width="1.2" opacity="0.28"/>'
        else:                                   # spine: cover material, the suit band wraps round it
            s += f'<path d="M{x + 2} 150 H{x + w - 2} V183 Q{x + w - 2} 186 {x + w - 5} 186 H{x + 5} Q{x + 2} 186 {x + 2} 183 Z" fill="{SUIT}"/>'
            s += f'<line x1="{x + w / 2:.1f}" y1="50" x2="{x + w / 2:.1f}" y2="144" stroke="{INK}" stroke-width="1.5" opacity="0.25"/>'
        return s

    @staticmethod
    def _cover(x0, k, face=None, back=False, spine_side='left'):
        """Front or back cover, 136*k wide starting at x0 (k = 1 front view, 109/136 for 3/4 views)."""
        w = 136 * k
        fx = lambda x: x0 + (x - 52) * k
        rx = 18 if k == 1 else 17.1
        s = f'<rect x="{x0}" y="38" width="{w:.1f}" height="154" rx="{rx}" fill="{CREAM}" stroke="{INK}" stroke-width="5"/>'
        a, b = x0 + 2.5, x0 + w - 2.5
        c = 15.5 * (k if k < 1 else 1)
        s += f'<path d="M{a} 150 L{b:.1f} 150 L{b:.1f} 174 Q{b:.1f} 189.5 {b - c:.1f} 189.5 L{a + c:.1f} 189.5 Q{a} 189.5 {a} 174 Z" fill="{SUIT}"/>'
        if back:
            l1, l2 = (fx(170), fx(166)) if spine_side == 'right' else (fx(70), fx(74))
            s += f'<line x1="{l1:.1f}" y1="46" x2="{l1:.1f}" y2="148" stroke="{INK}" stroke-width="3.5" opacity="0.45"/>'
            s += f'<line x1="{l2:.1f}" y1="46" x2="{l2:.1f}" y2="148" stroke="{INK}" stroke-width="1.5" opacity="0.25"/>'
            nub = fx(72) if spine_side == 'right' else fx(150)
            s += f'<rect x="{nub:.1f}" y="33" width="{18 * k:.1f}" height="6" fill="{BLUE}"/>'
            return s
        face = face or {}
        s += f'<line x1="{fx(70):.1f}" y1="46" x2="{fx(70):.1f}" y2="184" stroke="{INK}" stroke-width="3.5" opacity="0.45"/>'
        s += f'<line x1="{fx(74):.1f}" y1="46" x2="{fx(74):.1f}" y2="184" stroke="{INK}" stroke-width="1.5" opacity="0.25"/>'
        s += f'<path d="M{fx(150):.1f} 34 H{fx(168):.1f} V60 L{fx(159):.1f} 53 L{fx(150):.1f} 60 Z" fill="{BLUE}"/>'
        for y, ww in ((58, 60), (70, 60), (82, 40)):
            s += f'<rect x="{fx(86):.1f}" y="{y}" width="{ww * k:.1f}" height="6" rx="3" fill="{RULE}"/>'
        P = lambda pts: ' L'.join(f'{fx(x):.1f} {y}' for x, y in pts)
        s += f'<path d="M{P([(108, 150), (120, 168), (116, 173), (102, 154)])} Z" fill="#fff" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
        s += f'<path d="M{P([(132, 150), (120, 168), (124, 173), (138, 154)])} Z" fill="#fff" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
        s += f'<path d="M{P([(114, 152), (126, 152), (129, 161), (111, 161)])} Z" fill="{BLUE}"/>'
        s += f'<path d="M{P([(112, 162), (128, 162), (124, 184), (120, 189), (116, 184)])} Z" fill="{BLUE}"/>'
        lx, ly = face.get('look', (0, 0))
        erx = 7.5 if k == 1 else 6.5
        for ex in (102, 138):
            cx, cy = fx(ex) + lx * k, 110 + ly
            if face.get('glad'):
                s += f'<path d="M{cx - erx:.1f} {cy + 2.5} Q{cx:.1f} {cy - 10.5} {cx + erx:.1f} {cy + 2.5}" fill="none" stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/>'
            else:
                s += f'<ellipse cx="{cx:.1f}" cy="{cy}" rx="{erx}" ry="7.5" fill="{INK}"/><circle cx="{cx + 2.5 * k:.1f}" cy="{cy - 2.55}" r="2.25" fill="#fff"/>'
            if face.get('brows'):
                by = 95.5 - face.get('brows')
                s += f'<line x1="{fx(ex - 6.5):.1f}" y1="{by}" x2="{fx(ex + 6.5):.1f}" y2="{by}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        Wm, E, Tt, B = MOUTH[face.get('mouth', 'smile')]
        Y = 134 + E
        s += (f'<path d="M{fx(120 - Wm):.1f} {Y} Q{fx(120):.1f} {Y + Tt} {fx(120 + Wm):.1f} {Y} Q{fx(120):.1f} {Y + B} {fx(120 - Wm):.1f} {Y}Z" '
              f'fill="{INK}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round"/>')
        return s

    def draw(self, armL=None, armR=None, face=None, shadow=True, shadow_rx=42):
        """Returns (body, front): draw body, then anything held, then front (arms flagged front=True)."""
        v, view = self.v, self.view
        armL, armR = armL or {}, armR or {}
        tf = f'translate({self.X - 120 * self.sc:.2f} {self.Y - 222 * self.sc:.2f}) scale({self.sc})'
        tr = f'rotate({self.rot} 120 198)'
        legs = ''
        if shadow:
            legs += f'<ellipse cx="120" cy="236" rx="{shadow_rx}" ry="6" fill="{INK}" opacity="0.08"/>'
        for lx, sx in zip(v['legs'], v['shoes']):
            legs += f'<line x1="{lx}" y1="186" x2="{lx}" y2="210" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
            legs += f'<rect x="{sx}" y="208" width="29" height="14" rx="7" fill="{INK}"/>'
        k = 109 / 136
        back_arms, front_arms, body = '', '', ''
        # default layering from the turnaround sheet: which arm sits in front of the book
        near = {'34f_l': 'R', '34f_r': 'L', 'side_l': 'R', 'side_r': 'R'}.get(view)
        for side, spec in (('L', armL), ('R', armR)):
            if view.startswith('side') and side == 'L' and not spec.get('hand'):
                continue                          # side view at rest shows one arm
            a = self._arm(side, spec)
            if spec.get('front', side == near):
                front_arms += a
            else:
                back_arms += a
        if view == 'front':
            body = self._cover(52, 1, face)
        elif view == 'back':
            body = self._cover(52, 1, back=True, spine_side='right')
        elif view == '34f_l':
            body = self._slab(157, 'pages') + self._cover(52, k, face)
        elif view == '34f_r':
            body = self._slab(58, 'spine') + self._cover(79, k, face)
        else:
            body = self._slab(103, 'pages' if view == 'side_l' else 'spine', 34)
            for cx in (100, 133):
                body += f'<rect x="{cx}" y="38" width="7" height="154" rx="3.5" fill="{CREAM}" stroke="{INK}" stroke-width="3"/>'
                body += f'<rect x="{cx + 1.5}" y="150" width="4" height="40" fill="{SUIT}"/>'
            body += f'<rect x="{97 if view == "side_l" else 138}" y="34" width="5" height="26" fill="{BLUE}"/>'
        b = f'<g transform="{tf}">{legs}<g transform="{tr}">{back_arms}{body}</g></g>'
        f = f'<g transform="{tf}"><g transform="{tr}">{front_arms}</g></g>'
        return b, f


def embed_state(name, X, Y, sc):
    """The real website rig state, unchanged, placed with its feet at (X, Y)."""
    s = open(os.path.join(STATES, f'ledger-{name}.svg')).read()
    inner = re.sub(r'^<svg[^>]*>', '', s).rsplit('</svg>', 1)[0]
    inner = re.sub(r'<title>.*?</title>', '', inner)
    return f'<g transform="translate({X - 120 * sc:.2f} {Y - 222 * sc:.2f}) scale({sc})">{inner}</g>'


# ---------------------------------------------------------------------------------------------
# Small reusable pictures
# ---------------------------------------------------------------------------------------------
def card(w, h, inner, r=24, fill=WHITE):
    return rrect(-w / 2 + 9, -h / 2 + 9, w, h, r, INK, None) + rrect(-w / 2, -h / 2, w, h, r, fill, INK, 5) + inner


def panel(x, y, w, h, r=30, fill=WHITE, off=12):
    """Flat card with a flat offset block behind it (no blur, no gradient)."""
    return rrect(x + off, y + off, w, h, r, INK, None) + rrect(x, y, w, h, r, fill, INK, 5)


def floor(y, col):
    return rrect(0, y, W, H - y, 0, col, None)


def header(cat, topic, fg=WHITE):
    """Big subject name with the topic on a pill under it."""
    size = 126
    while tw(cat, size) > 980:
        size -= 2
    s = ''
    if fg != INK:
        s += T(546, 216, cat, size, fill=INK, check=False)
    s += T(540, 210, cat, size, fill=fg)
    w = tw(topic, 60) + 100
    s += rrect(540 - w / 2 + 8, 266, w, 104, 52, INK, None) + rrect(540 - w / 2, 258, w, 104, 52, WHITE, INK, 5)
    s += T(540, 331, topic, 60, maxw=w - 60)
    return s


def monitor(x, y, w, h, screen=WHITE):
    """Flat monitor: bezel, screen, neck and foot. The screen is inset 22 px."""
    cx = x + w / 2
    s = rrect(cx - 46, y + h - 6, 92, 66, 0, SUIT, None)
    s += rrect(cx - 180, y + h + 54, 360, 28, 14, SUIT, None)
    s += rrect(x, y, w, h, 34, INK, None) + rrect(x + 22, y + 22, w - 44, h - 44, 14, screen, None)
    return s


def cursor(x, y, sc=1.8):
    pts = [(0, 0), (0, 50), (12, 39), (21, 59), (30, 55), (21, 36), (37, 36)]
    d = 'M' + ' L'.join(f'{x + px * sc:.1f} {y + py * sc:.1f}' for px, py in pts) + ' Z'
    return path(d, fill=WHITE, stroke=INK, sw=5)


def mini_t(w, h, labels=True, c1=BLUE, c2=TINT):
    s = line(-w / 2, -h / 2 + (34 if labels else 0), w / 2, -h / 2 + (34 if labels else 0), INK, 5)
    s += line(0, -h / 2 + (34 if labels else 0), 0, h / 2, INK, 5)
    if labels:
        s += T(-w / 4, -h / 2 + 18, 'Debit', 24, check=False) + T(w / 4, -h / 2 + 18, 'Credit', 24, check=False)
    y0 = -h / 2 + (60 if labels else 22)
    s += rrect(-w / 2 + 14, y0, w / 2 - 34, 22, 8, c1, None)
    s += rrect(14, y0, w / 2 - 34, 22, 8, c2, None)
    s += rrect(-w / 2 + 14, y0 + 34, w / 2 - 70, 22, 8, c2, None)
    if labels:
        s += rrect(14, y0 + 34, w / 2 - 80, 22, 8, c1, None) + rrect(-w / 2 + 14, y0 + 68, w / 2 - 50, 22, 8, c1, None)
        s += rrect(14, y0 + 68, w / 2 - 54, 22, 8, c2, None)
    return s


def mini_sd(w, h):
    top = -h / 2 + 44
    s = path(f'M{-w / 2} {-h / 2} V{h / 2} H{w / 2}', sw=5)
    s += line(-w / 2 + 24, h / 2 - 22, w / 2 - 30, top, INK, 6)
    s += line(-w / 2 + 24, top, w / 2 - 30, h / 2 - 22, PINK, 6)
    s += circle(-3, (top + h / 2 - 22) / 2, 9, WHITE, INK, 4)
    s += T(w / 2 - 6, -h / 2 + 22, 'Supply', 24, anchor='end', check=False)
    s += T(-w / 2 + 18, -h / 2 + 22, 'Demand', 24, anchor='start', fill=PINK_D, check=False)
    s += T(-w / 2 - 4, -h / 2 - 16, 'Price', 22, anchor='start', fill=SLATE, check=False)
    s += T(w / 2, h / 2 + 32, 'Quantity', 22, anchor='end', fill=SLATE, check=False)
    return s


def block(cx, cy, label='€500', w=200, h=110, fill=BLUE, lift=0):
    s = rrect(cx - w / 2 + lift, cy - h / 2 + lift, w, h, 16, INK, None) if lift else ''
    return s + rrect(cx - w / 2, cy - h / 2, w, h, 16, fill, INK, 5) + T(cx, cy + 18, label, 52, fill=WHITE)


def tick(cx, cy, r=34):
    return (circle(cx, cy, r, GREEN, INK, 5) +
            path(f'M{cx - r * 0.42} {cy + r * 0.02} L{cx - r * 0.1} {cy + r * 0.34} L{cx + r * 0.46} {cy - r * 0.3}', stroke=WHITE, sw=r * 0.2))


def sparks(cx, cy, r0, r1, angles, col=WHITE, sw=8):
    s = ''
    for ang in angles:
        a = math.radians(ang)
        s += line(cx + r0 * math.cos(a), cy + r0 * math.sin(a), cx + r1 * math.cos(a), cy + r1 * math.sin(a), col, sw)
    return s


def embed_logo(x, y, w):
    """The real Edlintics logo file (mark + wordmark), unchanged, w pixels wide."""
    s = open(LOGO).read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    inner = re.sub(r'^<svg[^>]*>', '', s).rsplit('</svg>', 1)[0]
    inner = re.sub(r'<title>.*?</title>', '', inner, count=1)
    vw, vh = [float(v) for v in vb.split()[2:]]
    return f'<svg x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{w * vh / vw:.1f}" viewBox="{vb}">{inner}</svg>'


def monitor_desk(x, y, w, h, desk_y, screen=WHITE):
    """Monitor on a tall stand that goes down to the desk top at desk_y."""
    cx = x + w / 2
    s = rrect(cx - 40, y + h - 6, 80, desk_y - y - h + 30, 0, SUIT, None)
    s += rrect(cx - 190, desk_y + 14, 380, 26, 13, SUIT, None)
    s += rrect(x, y, w, h, 34, INK, None) + rrect(x + 22, y + 22, w - 44, h - 44, 14, screen, None)
    return s


def qbadge(cx, cy, r=50):
    return circle(cx, cy, r, BLUE, INK, 5) + T(cx, cy + r * 0.44, '?', r * 1.3, fill=WHITE)


def qcard(y, h, rows, ctx=None):
    """Question card: blue question badge on the left, optional context chip, then the rows of text."""
    s = panel(50, y, 980, h) + qbadge(136, y + h / 2)
    x = 216
    yy = y + 34
    if ctx:
        cw = tw(ctx, 38) + 56
        s += rrect(x, yy, cw, 66, 33, YEL, INK, 4) + T(x + cw / 2, yy + 46, ctx, 38, maxw=cw - 30)
        yy += 66 + 14
    n = len(rows)
    free = y + h - 30 - yy
    step = free / n
    for i, (t, size, fill, wt) in enumerate(rows):
        s += T(x, yy + step * i + step / 2 + size * 0.35, t, size, wt, anchor='start', fill=fill, maxw=790)
    return s


def qstrip(x, y, w, h, rows):
    """Question strip inside a monitor screen."""
    s = rrect(x, y, w, h, 22, TINT, INK, 4) + qbadge(x + 70, y + h / 2, 42)
    step = (h - 24) / len(rows)
    for i, (t, size, fill, wt) in enumerate(rows):
        s += T(x + 134, y + 12 + step * i + step / 2 + size * 0.35, t, size, wt, anchor='start', fill=fill, maxw=w - 160)
    return s


def pop_lines(x, y, w, h, col=WHITE, sw=8, n0=16, n1=50, corners=(0, 1, 2, 3)):
    """Short lines bursting from the four corners of a box: the pop-up cue."""
    s = ''
    for i, (cx, cy, base) in enumerate(((x, y, 225), (x + w, y, 315), (x + w, y + h, 45), (x, y + h, 135))):
        if i not in corners:
            continue
        for da in (-28, 0, 28):
            a = math.radians(base + da)
            s += line(cx + n0 * math.cos(a), cy + n0 * math.sin(a), cx + n1 * math.cos(a), cy + n1 * math.sin(a), col, sw)
    return s


def popup(cx, cy, text, size=64, sub=None, col=WHITE, sw=8, corners=(0, 1, 2), h=None, n1=50):
    """Answer pop-up: white pill, green tick, the answer, an optional second line, burst lines."""
    wm = tw(text.replace('_', ''), size) + 96
    ws = tw(sub, 38, True) if sub else 0
    w = max(wm, ws) + 80
    h = h or (196 if sub else 124)
    x, y = cx - w / 2, cy - h / 2
    s = pop_lines(x, y, w, h, col, sw, 16, n1, corners)
    s += rrect(x + 10, y + 10, w, h, 30, INK, None) + rrect(x, y, w, h, 30, WHITE, GREEN, 8)
    my = y + (62 if sub else h / 2)
    x0 = cx - wm / 2
    s += tick(x0 + 36, my, min(36, h * 0.32)) + T(x0 + 96, my + size * 0.35, text, size, anchor='start', fill=GREEN_D)
    if sub:
        s += T(cx, y + h - 34, sub, 38, 600, fill=SLATE, maxw=w - 40)
    return s


def confetti(pts):
    cols = (WHITE, YEL, TINT)
    s = ''
    for i, (x, y, rot) in enumerate(pts):
        c = cols[i % len(cols)]
        if i % 3 == 2:
            s += circle(x, y, 10, c, INK, 3)
        else:
            s += f'<rect x="{x - 14}" y="{y - 7}" width="28" height="14" rx="3" fill="{c}" stroke="{INK}" stroke-width="3" transform="rotate({rot} {x} {y})"/>'
    return s


def qmark(x, y, size, rot=0, col=WHITE):
    g = T(4, 4, '?', size, fill=INK, check=False) + T(0, 0, '?', size, fill=col, check=False)
    return f'<g transform="translate({x} {y}) rotate({rot})">{g}</g>'


def thought(cx, cy, to=(-1, 1)):
    """Thought bubble with a question mark; two small circles trail towards Ledger."""
    dx, dy = to
    s = circle(cx + dx * 150, cy + dy * 118, 13, WHITE, INK, 5) + circle(cx + dx * 112, cy + dy * 86, 21, WHITE, INK, 5)
    s += f'<ellipse cx="{cx + 8}" cy="{cy + 8}" rx="110" ry="88" fill="{INK}"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="110" ry="88" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>'
    s += T(cx, cy + 44, '?', 124, fill=BLUE)
    return s


def speed(x, y, n=3, length=70, gap=30, col=WHITE, sw=8, d=-1):
    """Horizontal speed lines starting at x and running in direction d."""
    return ''.join(line(x, y + i * gap, x + d * (length - (i % 2) * 22), y + i * gap, col, sw) for i in range(n))


def solved_marks(X, top, wide=250):
    """Joy marks round Ledger: spark lines over his head and confetti either side."""
    s = sparks(X, top + 150, 215, 262, (-128, -106, -74, -52), WHITE, 9)
    wide = min(wide, X - 50)
    s += confetti([(X - wide, top - 20, -20), (X - wide + 26, top + 120, 30), (X + wide, top - 40, 25),
                   (X + wide - 10, top + 110, -35), (X - wide + 70, top - 70, 60)])
    return s


def state_ledger(name, X, FL, sc, solved, hop=0):
    """A real rig state at the bottom of a frame with the marks of the moment."""
    s = embed_state(name, X, FL - hop, sc)
    top = FL - hop - 188 * sc
    if solved:
        s += solved_marks(X, top, 136 * sc / 2 + 110)
    else:
        s += qmark(X - 170, top + 14, 92, -16) + qmark(X - 70, top - 26, 112, 4) + qmark(X + 150, top + 6, 80, 16)
    return s


# ---------------------------------------------------------------------------------------------
# Frames. Each returns (svg, Ledger or None, background colour)
# ---------------------------------------------------------------------------------------------
def A1():
    FL = 1560
    s = floor(FL - 40, YEL_D)
    # pile of thick dusty textbooks in the four subject colours
    k = 1.2
    books = [(236, 78, EMER), (212, 66, CREAM), (228, 74, VIOLET), (200, 62, PINK), (224, 76, SUIT), (206, 64, ORANGE), (190, 70, TINT)]
    offs = [0, 12, -6, 14, 4, -8, 10]
    y = FL - 3
    for (bw, bh, col), off in zip(books, offs):
        bw, bh = bw * k, bh * k
        x = 30 + off + (236 * k - bw) / 2
        y -= bh
        s += rrect(x, y, bw, bh, 9, col, INK, 5)
        s += rrect(x + bw - 40, y + 10, 30, bh - 20, 4, PAGES, INK, 3)                # page edges
        s += line(x + 26, y + 7, x + 26, y + bh - 7, CREAM if col in (SUIT, VIOLET, PINK, EMER, ORANGE) else INK, 3, extra='opacity="0.6"')
        s += rrect(x + 54, y + bh / 2 - 8, bw * 0.38, 16, 8, RULE if col in (CREAM, TINT) else CREAM, None)
        s += rrect(x + 14, y - 6, bw * 0.55, 10, 5, '#FFF3C4', None)                  # dust lying on the book
        y -= 3
    top = y
    for dx, dy, r in ((30, -40, 11), (80, -90, 8), (150, -54, 10), (216, -104, 8), (256, -34, 9), (120, -136, 6)):
        s += circle(34 + dx, top + dy, r, '#FFF3C4', None)                            # dust in the air
    # door with its sign
    DX, DT = 520, 560
    s += rrect(DX - 200, DT, 400, FL - DT, 10, WHITE, INK, 5)
    s += rrect(DX - 172, DT + 28, 344, FL - DT - 31, 6, BLUE, INK, 5)
    s += rrect(DX - 136, DT + 66, 272, 380, 8, 'none', INK, 4, 'opacity="0.55"')
    s += rrect(DX - 136, DT + 490, 272, 450, 8, 'none', INK, 4, 'opacity="0.55"')
    hx, hy = DX + 122, FL - 250
    s += rrect(hx - 22, hy - 54, 44, 108, 12, CREAM, INK, 4)
    s += sparks(DX, 400, 300, 350, (-158, -168, -180, 168), WHITE, 8) + sparks(DX, 330, 100, 150, (-110, -90, -70), WHITE, 8)
    s += panel(DX - 270, 330, 540, 140, 24) + T(DX, 421, 'Learning business', 56, maxw=500)
    s += line(DX - 130, 470, DX - 130, DT, INK, 6) + line(DX + 130, 470, DX + 130, DT, INK, 6)
    # three floating phones, each with small bobbing marks
    def phone(cx, cy, rot, label, inner):
        p = rrect(-104, -157, 224, 330, 30, INK, None) + rrect(-112, -165, 224, 330, 30, WHITE, INK, 5) + rrect(-30, -150, 60, 10, 5, INK, None) + inner
        bob = path(f'M{cx - 150} {cy - 110} q-16 30 0 60', stroke=WHITE, sw=7) + path(f'M{cx - 172} {cy - 96} q-10 16 0 32', stroke=WHITE, sw=7)
        return bob + group(p, cx, cy, rot) + T(cx, cy + 230, label, 42)
    def tile(x, y, t, w, fill=WHITE, col=INK):
        return rrect(x, y, w, 40, 10, fill, INK, 3) + T(x + w / 2, y + 28, t, 22, fill=col, check=False)
    lang = rrect(-84, -122, 110, 12, 6, RULE, None)
    lang += tile(-88, -96, 'I', 40, EMER, WHITE) + tile(-40, -96, 'read', 68, EMER, WHITE) + rrect(36, -96, 56, 40, 10, 'none', EMER, 3, 'stroke-dasharray="7 6"')
    lang += line(-88, -38, 88, -38, RULE, 4)
    lang += tile(-88, -14, 'books', 84) + tile(6, -14, 'blue', 70) + tile(-52, 40, 'run', 62)
    lang += rrect(-78, 108, 156, 34, 17, EMER, None)
    code = ''
    for i, (ind, ww, col) in enumerate(((0, 150, SUIT), (22, 120, VIOLET), (44, 96, PINK), (22, 132, VIOLET), (0, 90, SUIT))):
        code += rrect(-84 + ind, -120 + i * 44, ww, 34, 9, col, INK, 3)
    code += rrect(-78, 108, 156, 34, 17, VIOLET, None)
    mol = line(0, -40, -52, 28, INK, 6) + line(0, -40, 52, 28, INK, 6) + line(0, -40, 0, -104, INK, 6)
    mol += circle(0, -40, 34, ORANGE, INK, 5) + circle(-52, 28, 22, CREAM, INK, 5) + circle(52, 28, 22, CREAM, INK, 5) + circle(0, -104, 18, YEL, INK, 5)
    mol += rrect(-78, 108, 156, 34, 17, ORANGE, None)
    s += phone(926, 370, -4, 'Languages', lang)
    s += phone(926, 860, 3, 'Coding', code)
    s += phone(926, 1350, -3, 'Science', mol)
    # Ledger from straight behind, standing at the door, one hand on the handle
    L = Ledger('back', hx - 262, FL + 20, 2.9)
    s += speed(L.X - 236, FL + 60, 3, 90, 34, WHITE, 9)                               # he has just walked up
    s += path(f'M{hx - 30} {hy - 96} q30 -34 60 0', stroke=WHITE, sw=7) + path(f'M{hx - 16} {hy - 120} q16 -18 32 0', stroke=WHITE, sw=7)   # handle rattles
    b, f = L.draw(armR={'hand': L.r((hx - 2, hy + 6)), 'front': True, 'bend': 1})
    s += b + f
    return s, L, YEL


def desk_and_ledger(FL, solved, cable_to):
    """Desk with keyboard, mouse and mouse mat; Ledger from straight behind in front of it."""
    sc = 2.3
    dt = FL - 228                                                                    # desk top edge
    s = rrect(108, FL - 110, 20, 84, 4, SUIT, None) + rrect(952, FL - 110, 20, 84, 4, SUIT, None)
    s += rrect(70, FL - 140, 940, 36, 8, '#D9B382', INK, 5)
    s += rrect(56, dt, 968, 92, 16, '#F2D7B0', INK, 5)
    # keyboard, left of him
    kx, ky = 110, dt + 14
    s += rrect(kx, ky, 300, 64, 12, WHITE, INK, 4)
    for r in range(2):
        for c in range(9):
            s += rrect(kx + 12 + c * 31, ky + 10 + r * 24, 24, 17, 4, SUIT if (r, c) != (1, 8) else BLUE, None)
    # mouse mat and mouse, right of him
    mx_, my_ = 742, dt + 46
    s += rrect(690, dt + 10, 250, 70, 14, TINT, INK, 4)
    s += path(f'M{mx_ + 40} {my_ - 6} C {mx_ + 150} {my_ - 60} 960 {dt - 60} {cable_to[0]} {cable_to[1]}', stroke=INK, sw=5)
    mouse = rrect(mx_ - 40, my_ - 26, 84, 50, 24, WHITE, INK, 5) + line(mx_ + 2, my_ - 26, mx_ + 2, my_ - 6, INK, 4)
    hop = 44 if solved else 0
    L = Ledger('back', 540, FL - hop, sc, rot=0 if solved else -5)
    s += f'<ellipse cx="540" cy="{FL + 32}" rx="{(74 if solved else 96)}" ry="13" fill="{INK}" opacity="0.14"/>'
    if solved:
        s += mouse
        b, f = L.draw(armL={'hand': (26, 104), 'bend': -1}, armR={'hand': (214, 104), 'bend': 1}, shadow=False)
        s += b + f
        top = L.w((0, 34))[1]
        s += sparks(540, top + 150, 205, 252, (-126, -106, -74, -54), WHITE, 9)
        s += confetti([(250, top + 10, -20), (205, top + 110, 30), (150, top + 30, 60), (930, top - 30, 25), (968, top + 80, -35), (700, top - 96, 10)])
        for x in (478, 602):                                                         # hop lines under his shoes
            s += line(x - 22, FL + 6, x + 22, FL + 6, WHITE, 8)
        s += line(mx_ + 70, my_ - 14, mx_ + 110, my_ - 14, INK, 5) + line(mx_ + 70, my_ + 8, mx_ + 100, my_ + 8, INK, 5)   # click marks
    else:
        s += mouse
        b, f = L.draw(armL={'hand': (45, 93), 'bend': -1}, armR={'hand': L.r((mx_, my_ - 2)), 'bend': 1}, shadow=False)
        s += b + f
        top = L.w((0, 34))[1]
        s += qmark(300, top + 40, 120, -16) + qmark(380, top - 44, 96, -4) + qmark(742, top + 6, 140, 12)
        s += path(f'M{L.w((46, 70))[0] - 40:.0f} {L.w((46, 70))[1]:.0f} q-14 14 0 28 q14 14 0 28', stroke=WHITE, sw=7)   # scratch squiggle
    return s, L


def A2(solved):
    FL = 1790
    s = floor(FL - 60, EMER_D) + header('ACCOUNTING', 'Journal entries')
    mx, my, mw, mh = 50, 400, 980, 770
    s += monitor_desk(mx, my, mw, mh, FL - 228)
    sx, sy, sw_ = mx + 22, my + 22, mw - 44
    s += qstrip(sx + 18, sy + 16, sw_ - 36, 150, [('Cash sale of €500', 42, SLATE, 600), ('Does Cash go on Debit or Credit?', 46, INK, 700)])
    # T-account for Cash
    ty, tb, tm = 690, 1000, 540
    s += T(tm, ty - 22, 'Cash account', 46)
    s += line(140, ty, 940, ty, INK, 8) + line(tm, ty, tm, tb, INK, 8)
    s += T(340, ty + 58, 'Debit', 46, fill=SLATE) + T(740, ty + 58, 'Credit', 46, fill=SLATE)
    zl, zr, zy = (240, 440), (640, 840), ty + 86
    bw, bh = 200, 100
    home = (tm, 1076)                                                                # the block starts in the tray under the T
    s += rrect(zr[0], zy, bw, bh, 16, WHITE, SLATE, 5, 'stroke-dasharray="14 10"')
    if not solved:
        s += rrect(zl[0], zy, bw, bh, 16, WHITE, SLATE, 5, 'stroke-dasharray="14 10"')
        s += curve_arrow(home[0] - 108, home[1] - 20, 330, home[1] - 30, 340, zy + bh + 22, SLATE, 6, '4 16', 24)
        s += curve_arrow(home[0] + 108, home[1] - 20, 750, home[1] - 30, 740, zy + bh + 22, SLATE, 6, '4 16', 24)
        s += block(home[0], home[1], w=bw, h=bh - 8, fill=BLUE, lift=8)
        s += cursor(home[0] + 84, home[1] - 6, 1.2)
    else:
        s += rrect(home[0] - bw / 2, home[1] - 46, bw, bh - 8, 16, 'none', SLATE, 5, 'stroke-dasharray="14 10"')   # where it was
        s += curve_arrow(home[0] - 108, home[1] - 4, 330, home[1], 338, zy + bh + 26, BLUE, 8, None, 30)
        s += rrect(zl[0] - 10, zy - 10, bw + 20, bh + 20, 22, GREEN_T, GREEN, 6)
        s += block(340, zy + bh / 2, w=bw, h=bh - 8, fill=BLUE)
        s += cursor(340 + 84, zy + bh / 2 + 4, 1.2)
        s += popup(772, 958, 'Correct', 56, col=GREEN, sw=7, corners=(1, 2), n1=44)
    d, L = desk_and_ledger(FL, solved, (760, my + mh - 8))
    return s + d, L, EMER


def A3(solved):
    FL = 1850
    s = floor(FL - 60, ORANGE_D) + header('FINANCE', 'Compound interest')
    s += qcard(400, 180, [('€1,000 grows at 5% a year', 42, SLATE, 600), ('In which year does it double?', 48, INK, 700)])
    s += panel(50, 612, 980, 700)
    ox, oy, top_v, ppe = 200, 1100, 3000, 370 / 3000
    X = lambda t: ox + 44 + t * 35
    Y = lambda v: oy - v * ppe
    val = lambda t: 1000 * 1.05 ** t
    year = 15 if solved else 0
    assert val(14) < 2000 < val(15) and round(val(15)) == 2079
    s += T(ox + 4, 676, 'Savings', 40, anchor='start')
    s += path(f'M{ox} {Y(top_v) - 14} V{oy} H{X(20) + 30}', sw=6)
    for v, lab in ((1000, '€1,000'), (2000, '€2,000')):
        s += line(ox - 12, Y(v), ox, Y(v), INK, 5) + T(ox - 20, Y(v) + 11, lab, 30, anchor='end', fill=SLATE)
    s += line(ox, Y(2000), X(20) + 20, Y(2000), GREEN, 5, dash='16 12') + T(X(20) + 20, Y(2000) - 16, 'Double', 32, anchor='end', fill=GREEN_D)
    for t in ((0, 5, 10, 15) if solved else (0,)):
        n = round(val(t) / 125)
        ch = val(t) * ppe / n
        for j in range(n):
            s += rrect(X(t) - 27, oy - 3 - ch * (j + 1), 54, ch, 7, YEL, INK, 3)
    pts = lambda a, b_: 'M' + ' L'.join(f'{X(a + (b_ - a) * i / 40):.1f} {Y(val(a + (b_ - a) * i / 40)):.1f}' for i in range(41))
    if solved:
        s += path(pts(15, 20), stroke=SLATE, sw=5, dash='3 13') + path(pts(0, 15), stroke=BLUE, sw=9)
    s += circle(X(year), Y(val(year)), 15, BLUE, INK, 4)
    lab = f'Year {year}: €{val(year):,.0f}'
    lw = tw(lab, 40) + 56
    px, py = X(year), Y(val(year))
    bx = px - 70 if solved else px + lw / 2 - 30
    by = py - 118                                                                   # top of the read-out bubble
    s += rrect(bx - lw / 2, by, lw, 74, 20, BLUE, INK, 5) + T(bx, by + 51, lab, 40, fill=WHITE)
    s += path(f'M{px - 16} {by + 72} L{px} {py - 22} L{px + 16} {by + 72} Z', fill=BLUE, stroke=None)
    # slider on the same scale as the chart
    ry = 1222
    s += T(118, ry + 12, 'Year', 34, fill=SLATE)
    s += rrect(X(0) - 16, ry - 14, X(20) - X(0) + 32, 28, 14, WHITE, INK, 5)
    for t in (0, 5, 10, 15, 20):
        s += line(X(t), ry + 24, X(t), ry + 38, INK, 5) + T(X(t), ry + 72, str(t), 30, fill=SLATE)
    if solved:
        s += rrect(X(0) - 11, ry - 9, X(15) - X(0) + 11, 18, 9, BLUE, None)
        s += circle(X(0), ry, 30, 'none', SLATE, 5).replace('/>', ' stroke-dasharray="10 8"/>')
        s += arrow(X(0) + 44, ry - 52, X(15) - 50, ry - 52, BLUE, 9, head=30)
    else:
        s += arrow(X(0) + 52, ry - 52, X(8), ry - 52, SLATE, 6, dash='4 16', head=24)
    s += circle(X(year), ry, 32, WHITE, INK, 5) + circle(X(year), ry, 13, BLUE, None)
    s += cursor(X(year) + 20, ry + 2, 1.2)
    # Ledger below: thinking, then joyful
    LX = 250
    if solved:
        s += state_ledger('joy', LX, FL, 2.05, True)
        s += popup(762, FL - 260, 'Correct', 68, 'It doubles in year 15')
    else:
        s += state_ledger('think', LX, FL, 2.05, False)
        s += thought(720, FL - 300)
    return s, None, ORANGE


def A4(solved):
    FL = 1856
    s = floor(FL - 60, VIOLET_D) + header('STATISTICS', 'Hypothesis testing')
    s += qcard(400, 180, [('z = 2.0, 5% level, two-tailed test', 42, SLATE, 600), ('Do we reject H_0?', 50, INK, 700)])
    s += panel(40, 612, 1000, 580)
    BL, CX, SG, HH, TOP = 1096, 540, 148, 310, 634
    hy = lambda x: BL - HH * math.exp(-((x - CX) / SG) ** 2 / 2)
    xa, xb = CX - 3.15 * SG, CX + 3.15 * SG
    xl, xr = CX - 1.96 * SG, CX + 1.96 * SG
    s += rrect(xa, TOP, xl - xa, BL - TOP, 0, GREEN_T, None) + rrect(xl, TOP, xr - xl, BL - TOP, 0, RED_T, None)
    s += rrect(xr, TOP, xb - xr, BL - TOP, 0, GREEN_T, None)
    def area(a, b_, col):
        n = max(2, int((b_ - a) / 5))
        p = ' L'.join(f'{a + (b_ - a) * i / n:.1f} {hy(a + (b_ - a) * i / n):.1f}' for i in range(n + 1))
        return path(f'M{a:.1f} {BL} L{p} L{b_:.1f} {BL} Z', fill=col, stroke=None)
    s += area(xa, xl, GREEN) + area(xl, xr, RED2) + area(xr, xb, GREEN)
    n = 120
    s += path('M' + ' L'.join(f'{xa + (xb - xa) * i / n:.1f} {hy(xa + (xb - xa) * i / n):.1f}' for i in range(n + 1)), sw=7)
    s += line(xl, BL, xl, hy(xl), INK, 5) + line(xr, BL, xr, hy(xr), INK, 5)
    s += line(xa - 10, BL, xb + 10, BL, INK, 6)
    for x, lab in ((xl, '−1.96'), (CX, '0'), (xr, '1.96')):
        s += line(x, BL, x, BL + 16, INK, 5) + T(x, BL + 58, lab, 38)
    s += T((xa + xl) / 2, TOP + 48, 'Reject H_0', 31, fill=GREEN_D, maxw=xl - xa)
    s += T((xr + xb) / 2, TOP + 48, 'Reject H_0', 31, fill=GREEN_D, maxw=xb - xr)
    s += T(CX, TOP + 58, 'Do not reject H_0', 46, fill=RED_D)
    # the z marker: starts at 0, is dragged to 2.0
    z = 2.0 if solved else 0.0
    zx, z2 = CX + z * SG, CX + 2.0 * SG
    fy = 790
    if solved:
        s += line(CX, BL, CX, fy + 40, WHITE, 6, dash='12 12') + circle(CX, BL, 13, WHITE, INK, 4)
        s += arrow(CX + 20, fy + 40, zx - 136, fy + 40, INK, 9, head=30)
    else:
        s += arrow(zx + 132, fy + 40, z2 - 6, fy + 40, INK, 6, dash='4 16', head=24)
    s += line(zx, BL, zx, fy + 40, INK, 7) + circle(zx, BL, 14, INK, None)
    s += rrect(zx - 110 + 8, fy + 8, 220, 80, 18, INK, None) + rrect(zx - 110, fy, 220, 80, 18, YEL, INK, 5)
    s += T(zx, fy + 56, 'z = 2.0' if solved else 'z = 0', 46)
    if not solved:
        s += cursor(zx - 104, fy + 62, 1.2)
    if solved:                                                                        # zoom: 2.0 lies just beyond 1.96
        ix, iy, ir = 934, 982, 94
        s += line(zx + 6, BL - 14, ix - 50, iy + 62, INK, 4)
        s += f'<clipPath id="zoom"><circle cx="{ix}" cy="{iy}" r="{ir}"/></clipPath>'
        g = rrect(ix - ir, iy - ir, ir - 26, 2 * ir, 0, RED_T, None) + rrect(ix - 26, iy - ir, ir + 26, 2 * ir, 0, GREEN_T, None)
        g += line(ix - 26, iy - ir, ix - 26, iy + ir, INK, 5) + line(ix + 26, iy - ir, ix + 26, iy + ir, INK, 9)
        s += f'<g clip-path="url(#zoom)">{g}</g>' + circle(ix, iy, ir, 'none', INK, 6)
        s += T(ix - 33, iy + 10, '1.96', 26, anchor='end') + T(ix + 37, iy + 10, '2.0', 28, anchor='start')
    # answer chips
    cy_ = 1222
    chips = [('Reject H_0', 300), ('Do not reject H_0', 470)]
    x = 540 - (300 + 470 + 30) / 2
    for i, (t, w_) in enumerate(chips):
        on = solved and i == 0
        s += rrect(x + 8, cy_ + 8, w_, 92, 46, INK, None) + rrect(x, cy_, w_, 92, 46, GREEN if on else WHITE, INK, 5)
        if on:
            s += circle(x + 50, cy_ + 46, 24, WHITE, INK, 4) + path(f'M{x + 39} {cy_ + 47} L{x + 47} {cy_ + 56} L{x + 62} {cy_ + 38}', stroke=GREEN_D, sw=7)
            s += T(x + 86, cy_ + 61, t, 42, anchor='start', fill=WHITE, maxw=w_ - 100)
            s += cursor(x + w_ - 16, cy_ + 66, 1.2)
        else:
            s += circle(x + 50, cy_ + 46, 22, WHITE, INK, 4) + T(x + 86, cy_ + 61, t, 42, anchor='start', maxw=w_ - 100)
        x += w_ + 30
    LX = 250
    if solved:
        s += state_ledger('cheer', LX, FL, 2.0, True)
        s += popup(762, FL - 260, 'Reject H_0', 66, '2.0 is beyond 1.96')
    else:
        s += state_ledger('confused', LX, FL, 2.0, False)
        s += thought(720, FL - 290)
    return s, None, VIOLET


def A5(solved):
    FL = 1860
    s = floor(FL - 60, PINK_D) + header('ECONOMICS', 'Market equilibrium')
    s += qcard(400, 214, [('What happens to demand?', 52, INK, 700)], ctx='Coffee becomes more popular')
    s += panel(40, 646, 1000, 690)
    ox, oy, yt, xr = 160, 1244, 700, 990
    e1, sh = (450, 1010), 200
    S = lambda x: e1[1] - (x - e1[0])
    D = lambda x, k=0: e1[1] + (x - e1[0] - k)
    e2 = (e1[0] + sh / 2, S(e1[0] + sh / 2))
    assert abs(D(e2[0], sh) - e2[1]) < 1e-6
    s += path(f'M{ox} {yt - 6} V{oy} H{xr + 4}', sw=7)
    s += arrow_head(ox, yt - 26, -90, 28) + arrow_head(xr + 24, oy, 0, 28)
    s += T(ox + 26, yt + 6, 'Price', 38, anchor='start', fill=SLATE) + T(xr + 20, oy + 56, 'Quantity', 38, anchor='end', fill=SLATE)
    s += line(260, S(260), 740, S(740), INK, 10) + T(762, S(740) + 26, 'Supply', 44, anchor='start')
    dl = lambda k, col, sw_, dash=None: line(220 + k, D(220 + k, k), 640 + k, D(640 + k, k), col, sw_, dash)
    if not solved:
        s += line(ox, e1[1], e1[0], e1[1], SLATE, 5, dash='3 14') + line(e1[0], e1[1], e1[0], oy, SLATE, 5, dash='3 14')
        s += dl(0, PINK, 11) + T(626, 1150 + 14, 'Demand', 44, anchor='start', fill=PINK_D)
        s += circle(e1[0], e1[1], 18, WHITE, INK, 6)
        s += T(ox - 20, e1[1] + 14, 'P_1', 40, anchor='end') + T(e1[0], oy + 56, 'Q_1', 40)
        gy = 860                                                                      # grab point on the line, could go either way
        gx = e1[0] + (gy - e1[1])
        s += arrow(gx + 40, gy, gx + 190, gy, SLATE, 6, dash='4 16', head=24) + arrow(gx - 40, gy, gx - 120, gy, SLATE, 6, dash='4 16', head=24)
        s += cursor(gx - 6, gy - 4, 1.4)
    else:
        for e in (e1, e2):
            s += line(ox, e[1], e[0], e[1], SLATE, 5, dash='3 14') + line(e[0], e[1], e[0], oy, SLATE, 5, dash='3 14')
        s += dl(0, PINK, 7, '18 16') + dl(sh, PINK, 11) + T(826, 1150 + 14, 'Demand', 44, anchor='start', fill=PINK_D)
        for yy in (812, 1130):
            xa_ = e1[0] + (yy - e1[1])
            s += arrow(xa_ + 26, yy, xa_ + sh - 22, yy, PINK_D, 9, head=28)
        s += circle(e1[0], e1[1], 13, WHITE, INK, 5) + circle(e2[0], e2[1], 20, GREEN, INK, 6)
        s += T(ox - 20, e1[1] + 14, 'P_1', 40, anchor='end') + T(ox - 20, e2[1] + 14, 'P_2', 40, anchor='end')
        s += T(e1[0], oy + 56, 'Q_1', 40) + T(e2[0], oy + 56, 'Q_2', 40)
        s += arrow(ox + 24, e1[1] - 8, ox + 24, e2[1] + 8, GREEN, 8, head=24)
        s += arrow(e1[0] + 10, oy - 24, e2[0] - 10, oy - 24, GREEN, 8, head=24)
        gy = 1040
        gx = e1[0] + sh + (gy - e1[1])
        s += cursor(gx - 6, gy - 4, 1.4)
    LX = 250
    if solved:
        s += state_ledger('joy', LX, FL, 2.0, True)
        s += popup(762, FL - 260, 'Correct', 68, 'Demand shifts right')
    else:
        s += state_ledger('scratch', LX, FL, 2.0, False)
        s += thought(720, FL - 290)
    return s, None, PINK


def A6(solved):
    FL = 1790
    s = floor(FL - 60, PINK_D) + header('ECONOMICS', 'The IS-LM model')
    mx, my, mw, mh = 50, 400, 980, 770
    s += monitor_desk(mx, my, mw, mh, FL - 228)
    sx, sy, sw_ = mx + 22, my + 22, mw - 44
    s += qstrip(sx + 18, sy + 16, sw_ - 36, 150, [('The central bank cuts the rate', 42, SLATE, 600), ('What happens to output Y?', 46, INK, 700)])
    ox, oy, yt, xr = 180, 1070, 650, 960
    y1, y2 = 770, 900
    e1 = (720, y1)
    IS = lambda x: e1[1] + (x - e1[0])
    e2 = (e1[0] + (y2 - y1), y2)
    assert IS(e2[0]) == y2
    s += path(f'M{ox} {yt - 6} V{oy} H{xr + 4}', sw=7)
    s += arrow_head(ox, yt - 24, -90, 26) + arrow_head(xr + 22, oy, 0, 26)
    s += T(ox + 24, yt + 8, 'Interest rate i', 34, anchor='start', fill=SLATE)
    s += T(ox + 24, oy + 50, 'Output Y', 34, anchor='start', fill=SLATE)
    s += line(e1[0], y1, e1[0], oy, SLATE, 5, dash='3 14')
    s += T(e1[0], oy + 50, 'Y_1', 40) + T(ox - 16, y1 + 13, 'i_1', 40, anchor='end')
    isl = line(640, IS(640), 940, IS(940), BLUE, 10) + T(628, IS(640) + 6, 'IS', 50, anchor='end', fill=BLUE)
    cx_ = 900                                                                         # where the cursor holds the LM line
    lm = lambda y: (T(ox + 24, y - 18, 'LM', 44, anchor='start') +
                    T(ox + 24 + tw('LM', 44) + 16, y - 20, 'set by the central bank', 28, 600, anchor='start', fill=SLATE, maxw=340))
    if not solved:
        s += line(ox, y1, xr - 10, y1, INK, 10) + isl + lm(y1)
        s += circle(e1[0], y1, 18, WHITE, INK, 6)
        s += arrow(cx_, y1 + 30, cx_, y1 + 140, SLATE, 6, dash='4 16', head=24) + arrow(cx_, y1 - 30, cx_, y1 - 90, SLATE, 6, dash='4 16', head=24)
        s += cursor(cx_ + 22, y1 - 6, 1.3)
    else:
        s += line(e2[0], y2, e2[0], oy, SLATE, 5, dash='3 14')
        s += line(ox, y1, xr - 10, y1, SLATE, 7, dash='18 16') + line(ox, y2, xr - 10, y2, INK, 10) + isl + lm(y2)
        s += arrow(660, y1 + 20, 660, y2 - 20, PINK, 14, head=38)
        s += circle(e1[0], y1, 13, WHITE, INK, 5) + circle(e2[0], y2, 20, GREEN, INK, 6)
        s += T(e2[0], oy + 50, 'Y_2', 40) + T(ox - 16, y2 + 13, 'i_2', 40, anchor='end')
        s += arrow(e1[0] + 12, oy - 24, e2[0] - 12, oy - 24, GREEN, 8, head=24)
        s += cursor(cx_ + 22, y2 - 6, 1.3)
        s += popup(400, 990, 'Correct', 48, col=GREEN, sw=6, corners=(0, 1), h=96, n1=30)
    d, L = desk_and_ledger(FL, solved, (760, my + mh - 8))
    return s + d, L, PINK


def A7():
    s = floor(1740, YEL_D)
    CW, CH, HD = 450, 340, 84

    def lesson(col, topic, icon, body):
        x, y = -CW / 2, -CH / 2
        g = rrect(x + 10, y + 10, CW, CH, 26, INK, None) + rrect(x, y, CW, CH, 26, WHITE, INK, 5)
        g += path(f'M{x} {y + HD} V{y + 26} Q{x} {y} {x + 26} {y} H{-x - 26} Q{-x} {y} {-x} {y + 26} V{y + HD} Z', fill=col, stroke=INK, sw=5)
        g += circle(x + 50, y + HD / 2, 28, WHITE, INK, 4) + group(icon, x + 50, y + HD / 2)
        g += T(x + 92, y + HD / 2 + 12, topic, 34, anchor='start', fill=WHITE, check=False)
        assert tw(topic, 34) < CW - 110, topic
        return g + group(body, 0, 42)

    def cur(x, y):
        return cursor(x, y, 0.8)

    # 1 journal entries: drag the block onto a side of the T-account
    b1 = line(-190, -62, 190, -62, INK, 5) + line(0, -62, 0, 100, INK, 5)
    b1 += T(-95, -74, 'Debit', 26, check=False) + T(95, -74, 'Credit', 26, check=False)
    b1 += rrect(-160, -40, 130, 56, 10, WHITE, SLATE, 4, 'stroke-dasharray="9 7"') + rrect(30, -40, 130, 56, 10, WHITE, SLATE, 4, 'stroke-dasharray="9 7"')
    b1 += curve_arrow(26, 70, -80, 80, -95, 30, SLATE, 4, '3 10', 16)
    b1 += rrect(34, 44, 130, 56, 10, INK, None) + rrect(28, 38, 130, 56, 10, BLUE, INK, 4) + T(93, 77, '€500', 30, fill=WHITE, check=False) + cur(142, 78)
    i1 = line(-13, -9, 13, -9, INK, 5) + line(0, -9, 0, 14, INK, 5)
    # 2 compound interest: slider under a growing curve
    gy_ = lambda i: 30 - 19 * 1.026 ** i
    cv = 'M' + ' L'.join(f'{-160 + 3.3 * i:.1f} {gy_(i):.1f}' for i in range(0, 71))
    b2 = path('M-180 -98 V30 H190', sw=5)
    for i in (12, 32, 52):
        for j in range(int((30 - gy_(i)) // 10)):
            b2 += rrect(-160 + 3.3 * i - 18, 28 - 10 * (j + 1), 36, 10, 5, YEL, INK, 2.5)
    b2 += path(cv, stroke=BLUE, sw=7) + circle(-160 + 3.3 * 70, gy_(70), 9, BLUE, INK, 3)
    b2 += rrect(-180, 82, 370, 16, 8, WHITE, INK, 4) + rrect(-176, 86, 250, 8, 4, BLUE, None) + circle(74, 90, 18, WHITE, INK, 4) + circle(74, 90, 8, BLUE, None)
    b2 += arrow(-70, 58, 40, 58, BLUE, 5, head=16) + cur(84, 88)
    i2 = T(0, 13, '€', 36, check=False)
    # 3 hypothesis testing: drag the marker along the bell curve
    hb = lambda x: 90 - 150 * math.exp(-(x / 62) ** 2 / 2)
    seg = lambda a, b_: ' L'.join(f'{a + (b_ - a) * i / 30:.1f} {hb(a + (b_ - a) * i / 30):.1f}' for i in range(31))
    b3 = path(f'M-190 90 L{seg(-190, -121)} L-121 90 Z', fill=GREEN, stroke=None) + path(f'M121 90 L{seg(121, 190)} L190 90 Z', fill=GREEN, stroke=None)
    b3 += path(f'M-121 90 L{seg(-121, 121)} L121 90 Z', fill=RED2, stroke=None)
    b3 += path(f'M{seg(-190, 190)}', sw=5) + line(-196, 90, 196, 90, INK, 5)
    b3 += line(134, 90, 134, -20, INK, 5) + rrect(98, -62, 72, 44, 10, YEL, INK, 4) + T(134, -30, 'z', 30, check=False)
    b3 += arrow(40, -40, 88, -40, INK, 5, head=16) + cur(150, -30)
    i3 = path('M-16 10 C-6 10 -6 -12 0 -12 C6 -12 6 10 16 10', sw=4)
    # 4 supply and demand: drag the demand line
    b4 = path('M-170 -92 V96 H180', sw=5)
    b4 += line(-140, 76, 60, -80, INK, 6) + line(-150, -70, 20, 70, PINK, 4, '10 9') + line(-70, -70, 100, 70, PINK, 7)
    b4 += arrow(-52, 18, 8, 18, PINK_D, 5, head=16) + circle(1.5, -34, 9, GREEN, INK, 3)
    b4 += T(72, -70, 'Supply', 24, anchor='start', check=False) + T(112, 62, 'Demand', 24, anchor='start', fill=PINK_D, check=False) + cur(70, 30)
    i4 = line(-13, -12, 13, 12, INK, 5) + line(-13, 12, 13, -12, PINK, 5)
    # 5 break-even point: pick the right answer
    assert 1000 / 4 == 250
    b5 = T(0, -52, '€1,000 fixed costs ÷ €4 a unit', 26, check=False)
    assert tw('€1,000 fixed costs ÷ €4 a unit', 26) < CW - 50
    for i, (t, on) in enumerate((('150 units', False), ('250 units', True), ('400 units', False))):
        yy = -30 + i * 44
        b5 += rrect(-150, yy, 300, 36, 18, GREEN if on else WHITE, INK, 4) + T(-10 if on else 0, yy + 27, t, 26, fill=WHITE if on else INK, check=False)
        if on:
            b5 += path(f'M64 {yy + 18} L72 {yy + 26} L86 {yy + 10}', stroke=WHITE, sw=5) + cur(138, yy + 22)
    i5 = rrect(-14, 0, 8, 12, 1, INK, None) + rrect(-4, -6, 8, 18, 1, INK, None) + rrect(6, -13, 8, 25, 1, BLUE, None)
    # 6 net present value: cash flows on a timeline and a rate slider
    b6 = line(-180, 10, 180, 10, INK, 5) + rrect(-160, 10, 44, 62, 4, RED2, INK, 4)
    for i, hgt in enumerate((40, 54, 66, 80)):
        b6 += rrect(-80 + i * 62, 10 - hgt, 44, hgt, 4, GREEN, INK, 4)
    b6 += rrect(-40, 78, 220, 14, 7, WHITE, INK, 4) + circle(60, 85, 16, WHITE, INK, 4) + circle(60, 85, 6, BLUE, None) + T(-64, 96, 'Rate', 24, anchor='end', fill=SLATE, check=False)
    b6 += arrow(140, 62, 92, 62, BLUE, 5, head=16) + cur(66, 88)
    i6 = T(0, 12, 'Σ', 34, check=False)
    cards = [
        (296, 296, -4, EMER_D, 'Journal entries', i1, b1),
        (788, 282, 4, ORANGE, 'Compound interest', i2, b2),
        (290, 694, 3, VIOLET, 'Hypothesis testing', i3, b3),
        (792, 686, -3, PINK, 'Supply and demand', i4, b4),
        (296, 1092, -4, BLUE, 'Break-even point', i5, b5),
        (788, 1082, 3, SUIT, 'Net present value', i6, b6),
    ]
    for cx, cy, rot, col, topic, icon, body in cards:
        outer = {True: {296: (0,), 1092: (3,)}, False: {282: (1,), 1082: (2,)}}[cx < 540].get(cy, ())   # pop lines on the four outer corners
        s += group(pop_lines(-CW / 2, -CH / 2, CW, CH, WHITE, 7, 14, 36, outer) + lesson(col, topic, icon, body), cx, cy, rot)
    L = Ledger('back', 540, 1810, 2.3)
    b, f = L.draw(armL={'hand': (26, 104), 'bend': -1}, armR={'hand': (214, 104), 'bend': 1})
    s += b + f
    top = L.w((0, 34))[1]
    s += sparks(540, top + 150, 205, 250, (-126, -106, -74, -54), WHITE, 9)
    s += confetti([(215, top + 60, -20), (250, top + 230, 30), (860, top + 50, 25), (840, top + 230, -35), (160, top + 180, 60), (915, top + 170, 10)])
    return s, L, YEL


def A8():
    FL = 1800
    s = floor(FL - 70, BLUE_D)
    mx, my, mw, mh = 44, 150, 992, 1030
    s += monitor(mx, my, mw, mh)
    ix, iy, iw = mx + 22, my + 22, mw - 44
    # browser bar
    s += rrect(ix, iy, iw, 100, 14, TINT, None) + rrect(ix, iy + 50, iw, 50, 0, TINT, None)
    for i, col in enumerate((RED, YEL, GREEN)):
        s += circle(ix + 54 + i * 44, iy + 50, 14, col, None)
    s += rrect(ix + 190, iy + 18, iw - 240, 64, 32, WHITE, INK, 3) + T(ix + 190 + (iw - 240) / 2, iy + 64, 'www.edlintics.com', 40)
    # page: the real logo, the headline, the four subjects and the button
    lw = 640
    s += embed_logo(540 - lw / 2, iy + 136, lw)
    s += T(540, iy + 392, 'Learn the language of business', 54, maxw=iw - 60)
    rows = [(('Accounting', EMER_D), ('Finance', ORANGE)), (('Economics', PINK), ('Statistics', VIOLET))]
    for r, row in enumerate(rows):
        ws = [tw(t, 46) + 76 for t, _ in row]
        x = 540 - (sum(ws) + 28) / 2
        y = iy + 446 + r * 108
        for (t, col), w_ in zip(row, ws):
            s += rrect(x, y, w_, 88, 44, col, INK, 4) + T(x + w_ / 2, y + 60, t, 46, fill=WHITE)
            x += w_ + 28
    by = iy + 706
    s += rrect(160, by + 10, 780, 160, 80, INK, None) + rrect(150, by, 780, 160, 80, BLUE, INK, 5)
    s += T(500, by + 102, 'Get started for free', 60, fill=WHITE, maxw=640)
    s += sparks(874, by + 112, 24, 56, (-128, -92, -56, -20), WHITE, 8)             # click burst
    s += cursor(874, by + 112, 1.9)
    # Ledger below the monitor, cheering
    sc = 2.2
    s += embed_state('cheer', 540, FL, sc)
    top = FL - 188 * sc
    s += solved_marks(540, top, 136 * sc / 2 + 120)
    return s, None, BLUE


# ---------------------------------------------------------------------------------------------
# Transition frames T1..T7 (Hoang, 20 Nov 2026: "Ledger stands still too much at the bottom").
# Between every pair of scenes Ledger is the thing that travels: he leaps, runs, rides, slides, drops
# and hops, the camera changes distance, and the next subject's colour wipes in along his path.
# He is the front rig drawn from the rig numbers; only the whole book is rotated, the legs swing
# about the rig's hip pivots (at most 30 degrees) and the arms keep the 1.7 reach cap.
# ---------------------------------------------------------------------------------------------
class Mover:
    """Front-view Ledger for travelling shots. (cx, cy) is the frame position of the book centre
    (rig 120,115); tilt rotates the whole figure about it. Nothing is scaled unevenly."""

    def __init__(self, cx, cy, sc, tilt=0):
        self.cx, self.cy, self.sc, self.tilt = cx, cy, sc, tilt
        self.view = f'front, whole book tilted {tilt}'
        self.reach = []

    @classmethod
    def on_feet(cls, fx, fy, sc, tilt=0):
        a, d = math.radians(tilt), 107 * sc
        return cls(fx + d * math.sin(a), fy - d * math.cos(a), sc, tilt)

    def w(self, p):
        a = math.radians(self.tilt)
        dx, dy = (p[0] - 120) * self.sc, (p[1] - 115) * self.sc
        return (self.cx + dx * math.cos(a) - dy * math.sin(a), self.cy + dx * math.sin(a) + dy * math.cos(a))

    def draw(self, legs=(0, 0), armL=None, armR=None, face=None, held='', opacity=1):
        R = Ledger('front', 0, 0, 1)
        back = front = ''
        for side, spec in (('L', armL or {}), ('R', armR or {})):
            a = R._arm(side, spec)
            if spec.get('front'):
                front += a
            else:
                back += a
        self.reach += R.reach
        lg = ''
        for lx, sx, a in zip((102, 138), (87.5, 123.5), legs):
            assert abs(a) <= 30, 'leg swing beyond the rig walk cycle'
            lg += (f'<g transform="rotate({a} {lx} 188)"><line x1="{lx}" y1="186" x2="{lx}" y2="210" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
                   f'<rect x="{sx}" y="208" width="29" height="14" rx="7" fill="{INK}"/></g>')
        body = R._cover(52, 1, face)
        return (f'<g transform="translate({self.cx:.1f} {self.cy:.1f}) rotate({self.tilt}) scale({self.sc}) translate(-120 -115)" '
                f'opacity="{opacity}">{lg}{back}{body}{held}{front}</g>')


UPL, UPR = {'hand': (28, 106), 'bend': -1}, {'hand': (212, 106), 'bend': 1}        # both arms up, as in the rig's cheer
JOY = {'glad': True, 'mouth': 'grin'}


def wipe(pts, col, band, bw=34):
    """The next scene's colour coming in: a flat region with a darker band on its leading edge."""
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ' Z'
    return (f'<path d="{d}" fill="{band}" stroke="{band}" stroke-width="{2 * bw}" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="{col}"/>')


def travel(p0, c1, c2, p3, ring=True, head=True, col=INK):
    """Storyboard path arrow: dashed curve from where he came (ring) to where he goes (head)."""
    s = path(f'M{p0[0]} {p0[1]} C{c1[0]} {c1[1]} {c2[0]} {c2[1]} {p3[0]} {p3[1]}', stroke=col, sw=8, dash='10 20')
    if ring:
        s += circle(p0[0], p0[1], 14, WHITE, col, 6)
    if head:
        ang = math.degrees(math.atan2(p3[1] - c2[1], p3[0] - c2[0]))
        s += arrow_head(p3[0] + 22 * math.cos(math.radians(ang)), p3[1] + 22 * math.sin(math.radians(ang)), ang, 34, col)
    return s


def star4(cx, cy, r, fill=WHITE, stroke=INK, sw=4):
    p = []
    for i in range(8):
        rr, a = (r if i % 2 == 0 else r * 0.34), math.radians(i * 45 - 90)
        p.append(f'{cx + rr * math.cos(a):.1f} {cy + rr * math.sin(a):.1f}')
    return path('M' + ' L'.join(p) + ' Z', fill=fill, stroke=stroke, sw=sw)


def coin(cx, cy, r, label='€'):
    s = circle(cx, cy, r, YEL, INK, max(2.5, r * 0.09)) + circle(cx, cy, r * 0.74, 'none', YEL_D, max(2, r * 0.07))
    if label:
        size = r * (0.95 if len(label) == 1 else 0.56)
        s += T(cx, cy + size * 0.36, label, size, check=False)
    return s


def coin_stack(x, base, n, w=84, ch=22):
    return ''.join(rrect(x - w / 2, base - 3 - ch * (j + 1), w, ch, 8, YEL, INK, 3) for j in range(n))


def bell_fn(BL, CX, SG, HH):
    g = lambda x: HH * math.exp(-((x - CX) / SG) ** 2 / 2)
    return (lambda x: BL - g(x)), (lambda x: g(x) * (x - CX) / SG ** 2)


def fpts(f, a, b, n=80):
    return ' L'.join(f'{a + (b - a) * i / n:.1f} {f(a + (b - a) * i / n):.1f}' for i in range(n + 1))


def tbook(cx, cy, rot, col, bw=210, bh=74):
    dark = col in (SUIT, VIOLET, PINK, EMER, ORANGE)
    g = rrect(-bw / 2, -bh / 2, bw, bh, 9, col, INK, 5) + rrect(bw / 2 - 40, -bh / 2 + 10, 30, bh - 20, 4, PAGES, INK, 3)
    g += rrect(-bw / 2 + 40, -8, bw * 0.38, 16, 8, CREAM if dark else RULE, None)
    return group(g, cx, cy, rot)


def mini_lesson(col, kind, w=280, h=200):
    """Small lesson card without words: coloured header, icon dot, a title bar and one picture."""
    x, y = -w / 2, -h / 2
    g = rrect(x + 9, y + 9, w, h, 22, INK, None) + rrect(x, y, w, h, 22, WHITE, INK, 5)
    g += path(f'M{x} {y + 54} V{y + 22} Q{x} {y} {x + 22} {y} H{-x - 22} Q{-x} {y} {-x} {y + 22} V{y + 54} Z', fill=col, stroke=INK, sw=5)
    g += circle(x + 34, y + 27, 15, WHITE, INK, 3) + rrect(x + 62, y + 18, w * 0.5, 18, 9, WHITE, None)
    b = ''
    if kind == 't':
        b = line(-96, -30, 96, -30, INK, 5) + line(0, -30, 0, 52, INK, 5) + rrect(-84, -14, 64, 30, 8, BLUE, None) + rrect(20, -14, 64, 30, 8, TINT, None)
        b += rrect(-84, 22, 44, 22, 8, TINT, None)
    elif kind == 'curve':
        f = lambda i: 46 - 12 * 1.03 ** i
        b = path('M-100 -44 V46 H104', sw=5) + path('M' + ' L'.join(f'{-90 + 2.6 * i:.1f} {f(i):.1f}' for i in range(71)), stroke=BLUE, sw=7)
        b += coin_stack(-50, 49, 1, 34, 10) + coin_stack(10, 49, 3, 34, 10) + coin_stack(66, 49, 5, 34, 10)
    elif kind == 'bell':
        f = lambda xx: 48 - 86 * math.exp(-(xx / 40) ** 2 / 2)
        b = path(f'M-104 48 L{fpts(f, -104, 104, 40)} L104 48 Z', fill=RED2, stroke=INK, sw=5) + line(-110, 48, 110, 48, INK, 5)
    elif kind == 'x':
        b = path('M-100 -44 V48 H104', sw=5) + line(-76, 36, 70, -36, INK, 6) + line(-76, -36, 70, 36, PINK, 7) + circle(-3, 0, 9, GREEN, INK, 3)
    elif kind == 'bars':
        b = line(-100, 10, 100, 10, INK, 5) + rrect(-86, 10, 34, 36, 4, RED2, INK, 4)
        for i, hh in enumerate((24, 36, 46, 58)):
            b += rrect(-36 + i * 34, 10 - hh, 24, hh, 4, GREEN, INK, 4)
    else:
        for i, on in enumerate((False, True, False)):
            b += rrect(-100, -44 + i * 34, 200, 26, 13, GREEN if on else WHITE, INK, 4)
    return g + group(b, 0, 30)


def T1():
    """Door -> accounting: the door is open and Ledger leaps through it at the camera."""
    FL = 1560
    s = floor(FL - 40, YEL_D)
    bx, by = 470, 1090                                                                 # the green bursts out of the doorway
    pts = []
    for i in range(32):
        r, a = (690 if i % 2 == 0 else 560), math.radians(i * 360 / 32 + 4)
        pts.append((bx + r * math.cos(a), by + r * math.sin(a)))
    s += wipe(pts, EMER, EMER_D, 26)
    D0, D1, DT = 150, 760, 480
    s += rrect(D0, DT, D1 - D0, FL - DT, 10, WHITE, INK, 5) + rrect(D0 + 30, DT + 30, D1 - D0 - 60, FL - DT - 33, 6, EMER_D, INK, 5)
    s += rrect(D0 - 104, DT + 14, 104, FL - DT + 16, 8, BLUE, INK, 5)                  # the door leaf, swung wide open
    s += rrect(D0 - 84, DT + 54, 64, 400, 6, 'none', INK, 4, 'opacity="0.55"') + rrect(D0 - 84, DT + 500, 64, 520, 6, 'none', INK, 4, 'opacity="0.55"')
    s += rrect(D0 - 92, FL - 290, 26, 96, 10, CREAM, INK, 4)
    s += path(f'M{D0 - 120} {DT - 20} q-34 30 -34 80', stroke=WHITE, sw=8) + path(f'M{D0 - 96} {DT - 56} q-70 44 -74 130', stroke=WHITE, sw=8)
    # the sign is knocked off and the old textbooks tumble aside
    s += group(panel(-270, -70, 540, 140, 24) + T(0, 21, 'Learning business', 56, check=False), 730, 250, 13)
    s += sparks(730, 250, 330, 380, (-28, -10, 8), WHITE, 8)
    for cx, cy, rot, col in ((110, 300, -24, CREAM), (960, 640, 38, SUIT), (120, 1730, 28, VIOLET), (350, 1830, -10, PINK), (955, 1690, -34, ORANGE)):
        s += tbook(cx, cy, rot, col)
    s += path('M40 1630 q-20 -50 20 -90', stroke=WHITE, sw=7) + path('M1030 1590 q22 -46 -12 -90', stroke=WHITE, sw=7)
    s += path('M1010 540 q30 -40 4 -86', stroke=WHITE, sw=7) + path('M50 220 q-14 -40 14 -70', stroke=WHITE, sw=7)
    # Ledger himself, big and in the air; the zoom lines say he is coming at the camera
    m = Mover(610, 1160, 4.4, -7)
    s += sparks(610, 1160, 520, 610, (-128, -112, -62, -48, 48, 62, 118, 132), WHITE, 10)
    s += f'<ellipse cx="640" cy="1722" rx="170" ry="20" fill="{INK}" opacity="0.14"/>'
    s += m.draw((20, -20), UPL, UPR, JOY)
    s += travel((250, 1520), (250, 1700), (560, 1850), (900, 1830))
    return s, m, YEL


def T2():
    """Accounting -> finance: the €500 block is now a big coin and Ledger runs right with it."""
    GY = 1560
    ex = lambda y: 800 - 240 * y / 1920
    s = floor(GY, EMER_D)
    s += wipe([(ex(-100), -100), (W + 200, -100), (W + 200, H + 100), (ex(H + 100), H + 100)], ORANGE, ORANGE_D)
    s += path(f'M{ex(GY):.0f} {GY} H{W} V{H} H{ex(H):.0f} Z', fill=ORANGE_D, stroke=None)
    # the T-account slides away behind him
    t = line(-230, 0, 230, 0, INK, 8) + line(0, 0, 0, 290, INK, 8)
    t += T(-115, 62, 'Debit', 44, fill=WHITE, check=False) + T(115, 62, 'Credit', 44, fill=WHITE, check=False)
    t += rrect(-200, 96, 170, 90, 16, 'none', WHITE, 5, 'stroke-dasharray="14 10"') + rrect(30, 96, 170, 90, 16, 'none', WHITE, 5, 'stroke-dasharray="14 10"')
    t += line(270, 70, 370, 70, WHITE, 9) + line(270, 130, 340, 130, WHITE, 9) + line(270, 190, 360, 190, WHITE, 9)
    s += group(t, 200, 300, -12)
    # finance is waiting on the right: coin stacks
    s += coin_stack(925, GY + 60, 3) + coin_stack(1022, GY + 60, 6)
    s += star4(930, GY - 60, 20) + star4(1010, GY - 130, 14)
    held = coin(120, 182, 36, '€500')
    legs = (24, -24)
    s += Mover.on_feet(310, GY - 56, 4.1, 10).draw((-24, 24), opacity=0.2)
    s += speed(96, 1010, 3, 84, 120, WHITE, 10)
    m = Mover.on_feet(600, GY - 30, 4.1, 10)
    s += f'<ellipse cx="610" cy="{GY + 18}" rx="165" ry="18" fill="{INK}" opacity="0.14"/>'
    for x, y, r in ((420, GY + 2, 26), (366, GY - 20, 16), (326, GY + 8, 10)):
        s += circle(x, y, r, WHITE, None)
    s += m.draw(legs, {'hand': (84, 180), 'front': True, 'bend': -1}, {'hand': (156, 180), 'front': True, 'bend': 1},
                {'brows': 2, 'mouth': 'smile', 'look': (3, 0)}, held)
    sx, sy = m.w((150, 138))
    s += star4(sx, sy, 26)
    s += travel((110, 1800), (380, 1720), (700, 1720), (950, 1800))
    return s, m, EMER


def T3():
    """Finance -> statistics: he surfs up the growth curve, which is already bending into the bell."""
    BL = 1760
    f, df = bell_fn(BL, 900, 330, 1050)
    s = floor(BL, ORANGE_D)
    s += wipe([(105, -200), (1300, -200), (1300, 1440), (1215, 1440)], VIOLET, VIOLET_D)
    for x in (140, 300, 460):
        s += coin_stack(x, BL + 3, int((BL - f(x) - 20) // 22))
    xt = 840
    s += path(f'M{fpts(f, xt, W + 20, 30)}', stroke=WHITE, sw=9, dash='18 18')
    s += path(f'M{fpts(f, -20, xt)}', stroke=INK, sw=22) + path(f'M{fpts(f, -20, xt)}', stroke=BLUE, sw=11)
    for x, r in ((760, 30), (715, 25), (672, 20), (640, 15)):                          # coins flung off behind him
        y = f(x) + 110 + (760 - x) * 0.5
        s += coin(x + 70, y, r) + line(x + 70 - r - 30, y + r + 14, x + 70 - r - 12, y + r - 6, WHITE, 7)
    tl = lambda x: math.degrees(math.atan(df(x))) * 0.45
    s += Mover.on_feet(610, f(610) - 12, 2.5, tl(610)).draw((14, -14), {'hand': (24, 146), 'bend': -1}, {'hand': (213, 124), 'bend': 1}, JOY, opacity=0.18)
    m = Mover.on_feet(xt, f(xt) - 14, 2.5, -15)
    s += sparks(m.cx, m.cy, 300, 350, (-150, -168, 174), WHITE, 9)
    s += m.draw((14, -14), {'hand': (24, 146), 'bend': -1}, {'hand': (213, 124), 'bend': 1}, JOY)
    s += circle(xt + 44, f(xt + 44), 15, BLUE, INK, 5)
    s += travel((70, 1560), (230, 1520), (300, 1400), (320, 1230))
    return s, m, ORANGE


def T4():
    """Statistics -> economics: he slides down the bell curve, whose tail becomes supply and demand."""
    BL = 1640
    f, df = bell_fn(BL, 300, 330, 900)
    s = wipe([(1207, 500), (1300, 500), (1300, 2220), (113, 2220)], PINK, PINK_D)
    xf = 800                                                                           # where the curve turns into straight lines
    mF = df(xf)
    x2 = 1050
    ec = ((xf + x2) / 2, f(xf) + mF * (x2 - xf) / 2)
    s += line(-10, BL, 640, BL, INK, 6) + line(300, BL, 300, f(300) + 30, WHITE, 6, dash='12 12')
    zx = 130                                                                           # the z marker is left behind
    s += line(zx, BL, zx, BL - 510, INK, 7) + circle(zx, BL, 14, INK, None)
    s += rrect(zx - 100 + 8, BL - 582, 200, 80, 18, INK, None) + rrect(zx - 100, BL - 590, 200, 80, 18, YEL, INK, 5) + T(zx, BL - 534, 'z = 2.0', 44)
    lo = (xf, ec[1] + (ec[1] - f(xf)))                                                 # lower end of the supply line
    s += path(f'M{xf} {f(xf):.0f} C{xf - 90} {f(xf) + 90:.0f} {xf - 90} {lo[1] - 70:.0f} {lo[0]} {lo[1]:.0f}', stroke=WHITE, sw=7, dash='4 16')
    s += line(lo[0], lo[1], x2, f(xf), WHITE, 12)
    s += path(f'M{fpts(f, -20, xf)} L{x2} {f(xf) + mF * (x2 - xf):.1f}', sw=11)
    s += circle(ec[0], ec[1], 20, WHITE, INK, 6)
    tl = lambda x: math.degrees(math.atan(df(x))) * 0.55
    s += Mover.on_feet(350, f(350) - 10, 2.4, tl(350)).draw((0, 0), UPL, UPR, JOY, opacity=0.14)
    s += Mover.on_feet(465, f(465) - 10, 2.4, tl(465)).draw((-8, -20), UPL, UPR, JOY, opacity=0.28)
    m = Mover.on_feet(600, f(600) - 10, 2.4, 30)
    s += m.draw((-8, -24), UPL, UPR, JOY)
    s += travel((850, 1000), (960, 1080), (1000, 1180), (ec[0] + 40, ec[1] - 110), ring=False)
    return s, m, VIOLET


def T5():
    """Market equilibrium -> IS-LM: the camera jumps in to an extreme close-up of his face."""
    cx, cy = 540, 1000
    s = ''
    for i in range(12):                                                                # flat burst behind him
        a0, a1 = math.radians(i * 30 - 8), math.radians(i * 30 + 8)
        s += path(f'M{cx} {cy} L{cx + 2400 * math.cos(a0):.0f} {cy + 2400 * math.sin(a0):.0f} L{cx + 2400 * math.cos(a1):.0f} {cy + 2400 * math.sin(a1):.0f} Z', fill=PINK_D, stroke=None)
    m = Mover(530, 1100, 11, -5)                                                       # so close that his sides, arms and legs are out of frame
    s += m.draw((0, 0), face={'brows': 5, 'mouth': 'grin', 'look': (1.5, -2)})
    for ex in (102, 138):                                                              # star highlights: the "aha" eyes
        x, y = m.w((ex - 2.6 + 1.5, 113.4 - 2))
        s += star4(x, y, 30, WHITE, None)
    for px, py, r in ((930, 700, 44), (840, 820, 22), (150, 880, 34)):                 # sparkle marks on the cover
        s += star4(px, py, r)
    # the question drops in from the top edge
    s += panel(60, -80, 960, 250) + qbadge(150, 84, 46)
    s += T(224, 104, 'What happens to output Y?', 54, anchor='start', maxw=760)
    s += line(300, 214, 300, 262, WHITE, 8) + line(540, 214, 540, 280, WHITE, 8) + line(700, 214, 700, 262, WHITE, 8)   # it has just dropped in
    # the supply and demand cross shrinks away to the corner
    g = panel(-180, -160, 360, 320, 26) + group(mini_sd(250, 200), 0, 4)
    s += group(g, 840, 1650, 6)
    s += pop_lines(640, 1478, 400, 340, WHITE, 8, 14, 52, (0,))
    return s, m, PINK


def T6():
    """IS-LM -> lesson cards: wide shot, he rides the LM line down like a lift while the cards fly in."""
    ox, oy, y0, y1 = 130, 1560, 560, 980
    isx = lambda y: 580 + (y - 330) * 420 / 970
    s = wipe([(-100, 1337), (W + 100, 1123), (W + 100, H + 100), (-100, H + 100)], YEL, YEL_D)
    s += path(f'M{ox} 250 V{oy} H1010', sw=7) + arrow_head(ox, 226, -90, 28) + arrow_head(1034, oy, 0, 28)
    s += T(ox + 26, 262, 'Interest rate i', 38, anchor='start') + T(1000, oy + 58, 'Output Y', 38, anchor='end')
    s += line(580, 330, 1000, 1300, INK, 20) + line(580, 330, 1000, 1300, BLUE, 10) + T(640, 330, 'IS', 56, anchor='start')
    s += line(ox, y0, 1000, y0, WHITE, 8, dash='18 18') + circle(isx(y0), y0, 14, WHITE, INK, 5)
    s += line(ox, y1, 1000, y1, INK, 13) + T(1000, y1 - 26, 'LM', 56, anchor='end')
    s += circle(isx(y1), y1, 22, GREEN, INK, 6)
    LX, pose = 390, dict(armL={'hand': (24, 142), 'bend': -1}, armR={'hand': (216, 142), 'bend': 1})
    s += Mover.on_feet(LX, y0 - 6, 1.35).draw((0, 0), face={'mouth': 'smile'}, opacity=0.16, **pose)
    s += Mover.on_feet(LX, (y0 + y1) / 2 - 6, 1.35).draw((0, 0), face={'mouth': 'oh', 'look': (0, 2)}, opacity=0.3, **pose)
    m = Mover.on_feet(LX, y1 - 8, 1.35, -4)
    s += m.draw((8, -8), face={'mouth': 'oh', 'brows': 3, 'look': (0, 2.5)}, **pose)
    for dx in (-150, 150):                                                             # drop lines either side of him
        s += line(LX + dx, y1 - 330, LX + dx, y1 - 230, WHITE, 8) + line(LX + dx * 0.72, y1 - 400, LX + dx * 0.72, y1 - 320, WHITE, 8)
    s += arrow(215, y0 + 26, 215, y1 - 40, INK, 8, dash='10 20', head=32) + circle(215, y0, 14, WHITE, INK, 6)
    s += arrow(215, y1 + 40, 215, 1280, INK, 8, dash='10 20', head=32)
    # lesson cards fly in from the edges
    cards = ((250, 1730, -12, EMER_D, 't', 180), (840, 1420, 10, ORANGE, 'curve', 0), (610, 1760, 6, VIOLET, 'bell', 90), (880, 190, 12, SUIT, 'bars', -30))
    for cx, cy, rot, col, kind, ang in cards:
        a = math.radians(ang)
        for k in (-1, 0, 1):
            px, py = cx + 190 * math.cos(a) - k * 60 * math.sin(a), cy + 190 * math.sin(a) + k * 60 * math.cos(a)
            ln = 70 - abs(k) * 22
            s += line(px, py, px + ln * math.cos(a), py + ln * math.sin(a), WHITE if cy < 1000 else INK, 8)
        s += group(mini_lesson(col, kind), cx, cy, rot)
    return s, m, PINK


def T7():
    """Lesson cards -> ending: he hops up the cards like stepping stones towards the button."""
    s = wipe([(32, -200), (1300, -200), (1300, 1250), (1248, 1250)], BLUE, BLUE_D)
    s += monitor(520, -360, 1500, 740)
    for t, col, x in (('Economics', PINK, 572), ('Statistics', VIOLET, 824)):
        w_ = tw(t, 36) + 56
        s += rrect(x, 56, w_, 76, 38, col, INK, 4) + T(x + w_ / 2, 107, t, 36, fill=WHITE)
    s += rrect(582, 200, 470, 126, 63, INK, None) + rrect(572, 190, 470, 126, 63, BLUE, INK, 5)
    s += T(807, 268, 'Get started for free', 42, fill=WHITE, maxw=420)
    s += group(mini_lesson(SUIT, 'bars'), 850, 1640, 9) + group(mini_lesson(BLUE, 'pick'), 170, 900, -9)
    stones = ((180, 1700, -7, EMER_D, 't'), (490, 1400, 6, ORANGE, 'curve'), (800, 1110, -6, VIOLET, 'bell'))
    tops = [(cx, cy - 104) for cx, cy, *_ in stones]
    hop = lambda a, b, lift, **k: travel(a, (a[0] + (b[0] - a[0]) * 0.15, a[1] - lift), (b[0] - (b[0] - a[0]) * 0.4, b[1] - lift), b, **k)
    s += hop((30, 1800), tops[0], 150, head=False)
    s += hop(tops[0], tops[1], 230, ring=False, head=False) + hop(tops[1], tops[2], 230, ring=False, head=False)
    for cx, cy, rot, col, kind in stones:
        s += group(mini_lesson(col, kind), cx, cy, rot)
        s += line(cx - 80, cy - 126, cx - 108, cy - 156, WHITE, 8) + line(cx + 80, cy - 126, cx + 108, cy - 156, WHITE, 8)
    s += Mover.on_feet(tops[1][0], tops[1][1] + 4, 1.9, 6).draw((10, -10), UPL, UPR, JOY, opacity=0.22)
    m = Mover(790, 740, 2.0, 12)
    s += sparks(m.cx - 20, m.cy + 40, 250, 300, (112, 130, 148), WHITE, 9)
    s += m.draw((22, -22), UPL, UPR, JOY)
    s += travel((960, 560), (1010, 500), (1000, 420), (950, 356), ring=False)
    return s, m, YEL


FRAMES = {'A1': A1, 'T1': T1, 'A2a': lambda: A2(False), 'A2b': lambda: A2(True), 'T2': T2,
          'A3a': lambda: A3(False), 'A3b': lambda: A3(True), 'T3': T3, 'A4a': lambda: A4(False), 'A4b': lambda: A4(True), 'T4': T4,
          'A5a': lambda: A5(False), 'A5b': lambda: A5(True), 'T5': T5, 'A6a': lambda: A6(False), 'A6b': lambda: A6(True), 'T6': T6,
          'A7': A7, 'T7': T7, 'A8': A8}


def build(name):
    WARN.clear()
    inner, L, bg = FRAMES[name]()
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
           f'<rect width="{W}" height="{H}" fill="{bg}"/>{inner}</svg>')
    open(os.path.join(OUT, f'{name}.svg'), 'w').write(svg)
    html = os.path.join(OUT, f'_{name}.html')
    open(html, 'w').write(f'<!doctype html><meta charset="utf-8"><style>html,body{{margin:0;background:{bg}}}svg{{display:block}}</style>{svg}')
    png = os.path.join(OUT, f'{name}.png')
    subprocess.run([CHROME, '--headless=new', '--hide-scrollbars', '--force-device-scale-factor=1', f'--window-size={W},{H}',
                    f'--screenshot={png}', 'file://' + html], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(html)
    im = Image.open(png)
    msg = f'{name}: {im.size[0]}x{im.size[1]}'
    if L:
        msg += f'  view {L.view}  arms (side, length, reach) {L.reach}'
    print(msg)
    for w_ in WARN:
        print('   WARNING', w_)


def sheet(per_row=7):
    names = [n for n in FRAMES if os.path.exists(os.path.join(OUT, f'{n}.png'))]
    tw_, th = 250, 444
    rows = math.ceil(len(names) / per_row)
    im = Image.new('RGB', (tw_ * min(per_row, len(names)), th * rows), 'white')
    for i, n in enumerate(names):
        im.paste(Image.open(os.path.join(OUT, f'{n}.png')).convert('RGB').resize((tw_ - 4, th - 4), Image.Resampling.LANCZOS),
                 ((i % per_row) * tw_ + 2, (i // per_row) * th + 2))
    im.save(os.path.join(OUT, 'sheet.png'))
    print('sheet.png', im.size)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for n in (sys.argv[1:] or list(FRAMES)):
        build(n)
    sheet()
