#!/usr/bin/env python3
"""Edlintics demo video A: 8 storyboard stills, drawn in code (SVG) and rendered with headless Chrome.

Run:  python3 frames_a.py            (all frames + sheet.png)
      python3 frames_a.py A3 A5      (only those frames, sheet rebuilt from what exists)

Ledger is drawn from the website rig numbers (assets/brand-handoff/ledger-v2/RIG.md) and the
turnaround sheet (front, 3/4 front, side, 3/4 back, back). Arms use the rig's two-segment arm
(upper 23.3, forearm 16.5, reach n <= 1.7); the script refuses to draw a longer arm.
A8 embeds the real rig state file ledger-point-left.svg unchanged.
"""
import math, os, re, subprocess, sys
from PIL import Image, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
STATES = '/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing/assets/brand-handoff/ledger-v2/states'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
W, H = 1080, 1920

INK, CREAM, SUIT, BLUE, RULE = '#0F172A', '#FBFAF6', '#222C3D', '#467DE3', '#E6E3DA'
GREEN, RED, WHITE, BG, PAGES = '#16A34A', '#DC2626', '#FFFFFF', '#F3F7FE', '#F1EEE4'
TINT = '#DCE8FB'      # light blue tint of the lead colour
SLATE = '#64748B'     # secondary text
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
    w = tw(s, size, weight >= 600)
    if check:
        x0 = x - w / 2 if anchor == 'middle' else (x if anchor == 'start' else x - w)
        if x0 < 24 or x0 + w > W - 24:
            WARN.append(f'text outside frame: "{s}" {x0:.0f}..{x0 + w:.0f}')
        if maxw and w > maxw:
            WARN.append(f'text wider than its box: "{s}" {w:.0f} > {maxw}')
    s = s.replace('&', '&amp;').replace('<', '&lt;')
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
    '34b_r': dict(sh=(64, 180), legs=(108, 142), shoes=(93.5, 127.5)),   # back, turned right, page edges on the left
    '34b_l': dict(sh=(60, 176), legs=(98, 132), shoes=(83.5, 117.5)),    # back, turned left, spine on the right
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
        near = {'34f_l': 'R', '34f_r': 'L', '34b_r': 'L', '34b_l': 'R', 'side_l': 'R', 'side_r': 'R'}.get(view)
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
        elif view == '34b_r':
            body = self._slab(58, 'pages') + self._cover(79, k, back=True, spine_side='right')
        elif view == '34b_l':
            body = self._slab(157, 'spine') + self._cover(52, k, back=True, spine_side='right')
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
def card(w, h, inner, r=24):
    return rrect(-w / 2, -h / 2, w, h, r, WHITE, INK, 5) + inner


def mini_t(w, h, labels=True):
    s = line(-w / 2, -h / 2 + (34 if labels else 0), w / 2, -h / 2 + (34 if labels else 0), INK, 5)
    s += line(0, -h / 2 + (34 if labels else 0), 0, h / 2, INK, 5)
    if labels:
        s += T(-w / 4, -h / 2 + 18, 'Debit', 24, check=False) + T(w / 4, -h / 2 + 18, 'Credit', 24, check=False)
    y0 = -h / 2 + (60 if labels else 22)
    s += rrect(-w / 2 + 14, y0, w / 2 - 34, 22, 8, BLUE, None)
    s += rrect(14, y0, w / 2 - 34, 22, 8, TINT, None)
    s += rrect(-w / 2 + 14, y0 + 34, w / 2 - 70, 22, 8, TINT, None)
    if labels:
        s += rrect(14, y0 + 34, w / 2 - 80, 22, 8, BLUE, None) + rrect(-w / 2 + 14, y0 + 68, w / 2 - 50, 22, 8, BLUE, None)
        s += rrect(14, y0 + 68, w / 2 - 54, 22, 8, TINT, None)
    return s


def mini_growth(w, h):
    s = path(f'M{-w / 2} {-h / 2} V{h / 2} H{w / 2}', sw=4)
    s += path(f'M{-w / 2 + 6} {h / 2 - 12} Q{w * 0.2} {h / 2 - 16} {w / 2 - 6} {-h / 2 + 6}', stroke=BLUE, sw=6)
    return s


def mini_bell(w, h):
    pts = []
    for i in range(41):
        z = -3 + 6 * i / 40
        pts.append(f'{z * w / 6:.1f} {h / 2 - (h - 8) * math.exp(-z * z / 2):.1f}')
    s = path('M' + ' L'.join(pts), stroke=BLUE, sw=6)
    s += line(-w / 2, h / 2, w / 2, h / 2, INK, 4)
    return s


def mini_sd(w, h, labels=False):
    top = -h / 2 + (44 if labels else 26)
    s = path(f'M{-w / 2} {-h / 2} V{h / 2} H{w / 2}', sw=5)
    s += line(-w / 2 + 24, h / 2 - 22, w / 2 - 30, top, INK, 6)
    s += line(-w / 2 + 24, top, w / 2 - 30, h / 2 - 22, BLUE, 6)
    s += circle(-3, (top + h / 2 - 22) / 2, 9, WHITE, INK, 4)
    if labels:
        s += T(w / 2 - 6, -h / 2 + 22, 'Supply', 24, anchor='end', check=False)
        s += T(-w / 2 + 18, -h / 2 + 22, 'Demand', 24, anchor='start', fill=BLUE, check=False)
        s += T(-w / 2 - 4, -h / 2 - 16, 'Price', 22, anchor='start', fill=SLATE, check=False)
        s += T(w / 2, h / 2 + 32, 'Quantity', 22, anchor='end', fill=SLATE, check=False)
    return s


def block(cx, cy, label='€500', w=160, h=88):
    return rrect(cx - w / 2, cy - h / 2, w, h, 14, BLUE, INK, 5) + T(cx, cy + 15, label, 42, fill=WHITE)


def tick(cx, cy, r=34):
    return circle(cx, cy, r, GREEN, None) + path(f'M{cx - r * 0.42} {cy + r * 0.02} L{cx - r * 0.1} {cy + r * 0.34} L{cx + r * 0.46} {cy - r * 0.3}', stroke=WHITE, sw=r * 0.2)


# ---------------------------------------------------------------------------------------------
# Frames
# ---------------------------------------------------------------------------------------------
def A1():
    FL = 1340
    s = floor_line(24, 740, FL)
    # pile of thick dusty textbooks
    books = [(236, 78, SUIT), (212, 66, CREAM), (228, 74, TINT), (200, 62, RULE), (224, 76, SUIT), (206, 64, CREAM), (190, 70, TINT)]
    offs = [0, 12, -6, 14, 4, -8, 10]
    y = FL - 3
    for (bw, bh, col), off in zip(books, offs):
        x = 30 + off + (236 - bw) / 2
        y -= bh
        s += rrect(x, y, bw, bh, 9, col, INK, 5)
        s += rrect(x + bw - 34, y + 9, 26, bh - 18, 4, PAGES, INK, 3)                 # page edges
        s += line(x + 22, y + 6, x + 22, y + bh - 6, INK if col != SUIT else CREAM, 3, extra='opacity="0.5"')
        s += rrect(x + 46, y + bh / 2 - 7, bw * 0.38, 14, 7, CREAM if col in (SUIT, RULE) else RULE, None)
        s += rrect(x + 12, y - 5, bw * 0.55, 9, 4.5, '#CBD5E1', None)                 # dust lying on the book
        y -= 3
    top = y
    for dx, dy, r in ((30, -40, 9), (70, -84, 6), (130, -54, 8), (186, -96, 6), (222, -34, 7), (104, -122, 5)):
        s += circle(34 + dx, top + dy, r, '#CBD5E1', None)                            # dust in the air
    # door with its sign
    DX = 500
    s += rrect(DX - 178, 670, 356, FL - 670, 10, WHITE, INK, 5)
    s += rrect(DX - 152, 696, 304, FL - 696 - 3, 6, BLUE, INK, 5)
    s += rrect(DX - 120, 730, 240, 250, 8, 'none', INK, 4, 'opacity="0.55"')
    s += rrect(DX - 120, 1020, 240, 270, 8, 'none', INK, 4, 'opacity="0.55"')
    hx, hy = DX + 108, 1104
    s += rrect(hx - 20, hy - 50, 40, 100, 12, CREAM, INK, 4)
    s += rrect(DX - 226, 508, 452, 116, 22, WHITE, INK, 5) + T(DX, 583, 'Learning business', 46, maxw=420)
    s += line(DX - 110, 624, DX - 110, 670, INK, 5) + line(DX + 110, 624, DX + 110, 670, INK, 5)
    # three floating phones
    def phone(cx, cy, rot, label, inner):
        p = rrect(-112, -165, 224, 330, 30, WHITE, INK, 5) + rrect(-30, -150, 60, 10, 5, INK, None) + inner
        p += rrect(-78, 108, 156, 34, 17, BLUE, None)
        return group(p, cx, cy, rot) + T(cx, cy + 226, label, 40)
    def tile(x, y, t, w, fill=WHITE, col=INK):
        return rrect(x, y, w, 40, 10, fill, INK, 3) + T(x + w / 2, y + 28, t, 22, fill=col, check=False)
    lang = rrect(-84, -122, 110, 12, 6, RULE, None)
    lang += tile(-88, -96, 'I', 40, BLUE, WHITE) + tile(-40, -96, 'read', 68, BLUE, WHITE) + rrect(36, -96, 56, 40, 10, 'none', BLUE, 3, 'stroke-dasharray="7 6"')
    lang += line(-88, -38, 88, -38, RULE, 4)
    lang += tile(-88, -14, 'books', 84) + tile(6, -14, 'blue', 70) + tile(-52, 40, 'run', 62)
    code = ''
    for i, (ind, ww, col) in enumerate(((0, 150, SUIT), (22, 120, BLUE), (44, 96, TINT), (22, 132, BLUE), (0, 90, SUIT))):
        code += rrect(-84 + ind, -120 + i * 44, ww, 34, 9, col, INK, 3)
    mol = line(0, -40, -52, 28, INK, 6) + line(0, -40, 52, 28, INK, 6) + line(0, -40, 0, -104, INK, 6)
    mol += circle(0, -40, 34, BLUE, INK, 5) + circle(-52, 28, 22, CREAM, INK, 5) + circle(52, 28, 22, CREAM, INK, 5) + circle(0, -104, 18, TINT, INK, 5)
    s += phone(912, 500, -4, 'Languages', lang)
    s += phone(912, 980, 3, 'Coding', code)
    s += phone(912, 1460, -3, 'Science', mol)
    # Ledger from 3/4 back, one hand on the handle
    L = Ledger('34b_r', hx - 222, FL + 26, 2.5)
    b, f = L.draw(armR={'hand': L.r((hx - 2, hy + 4)), 'front': True, 'bend': 1}, shadow=False)
    return s + b + f, L


def A2():
    FL = 1450
    s = chip('Accounting') + floor_line(24, 1056, FL)
    # T-account
    tx0, tx1, tm, ty = 506, 1046, 776, 760
    s += T((tx0 + tm) / 2, ty - 32, 'Debit', 54) + T((tm + tx1) / 2, ty - 32, 'Credit', 54)
    s += line(tx0, ty, tx1, ty, INK, 7) + line(tm, ty, tm, 1230, INK, 7)
    s += T((tx0 + tm) / 2, ty + 72, 'Cash', 44, fill=SLATE) + T((tm + tx1) / 2, ty + 72, 'Sales', 44, fill=SLATE)
    slot = ((tx0 + tm) / 2 - 80, ty + 110, 160, 88)
    s += rrect(*slot, 14, 'none', BLUE, 5, 'stroke-dasharray="14 10"')
    s += rrect((tm + tx1) / 2 - 80, ty + 110, 160, 88, 14, 'none', BLUE, 5, 'stroke-dasharray="14 10"')
    # balance scale under the T-account
    cx = 690
    s += path(f'M{cx - 46} {FL - 3} L{cx} {FL - 46} L{cx + 46} {FL - 3} Z', fill=WHITE)
    s += line(cx, FL - 46, cx, FL - 150, INK, 6) + line(cx - 110, FL - 142, cx + 110, FL - 142, INK, 6) + circle(cx, FL - 148, 9, BLUE, INK, 4)
    for px in (cx - 110, cx + 110):
        s += line(px, FL - 142, px - 34, FL - 72, INK, 3) + line(px, FL - 142, px + 34, FL - 72, INK, 3)
        s += path(f'M{px - 44} {FL - 72} H{px + 44} Q{px} {FL - 40} {px - 44} {FL - 72} Z', fill=TINT, sw=4)
    # second block waiting on the floor by the credit side
    s += block(958, FL - 47)
    # three small steps
    st = [(30, FL - 80), (120, FL - 160), (208, FL - 240)]
    R = 408
    s += path(f'M{st[0][0]} {FL} V{st[0][1]} H{st[1][0]} V{st[1][1]} H{st[2][0]} V{st[2][1]} H{R} V{FL} Z', fill=WHITE)
    s += line(st[1][0], st[0][1], R, st[0][1], RULE, 4) + line(st[2][0], st[1][1], R, st[1][1], RULE, 4)
    # Ledger on the top step, block against his cover in both hands
    sc = 2.5
    L = Ledger('34f_r', (st[2][0] + R) / 2 - 5 * sc, FL - 240, sc)
    bc = L.w((127, 167))
    b, f = L.draw(armL={'hand': L.r((bc[0] - 82, bc[1] + 6)), 'front': True, 'bend': 1},
                  armR={'hand': L.r((bc[0] + 82, bc[1] + 6)), 'front': True, 'bend': -1},
                  face={'look': (3, -1.5), 'mouth': 'smile'}, shadow=False)
    s += b + block(bc[0], bc[1]) + f
    s += curve_arrow(bc[0] + 96, bc[1] - 50, slot[0] - 40, slot[1] - 30, slot[0] + 44, slot[1] + 40)
    return s, L


def A3():
    FL = 1560
    s = chip('Finance')
    # savings chart
    s += rrect(80, 400, 920, 660, 30, WHITE, INK, 5)
    ox, oy, xr, yt = 170, 970, 930, 480
    s += T(ox, 462, 'Savings', 38, anchor='start')
    k = math.log((oy - yt - 30) / 60)
    cy = lambda t: oy - 60 * math.exp(k * t)
    for i in range(5):
        t = 0.16 + 0.19 * i
        x = ox + (xr - ox) * t
        n = max(1, int((oy - cy(t) - 34) // 22))
        for j in range(n):
            s += rrect(x - 36, oy - 3 - 22 * (j + 1), 72, 22, 11, BLUE, INK, 3)
    pts = ' L'.join(f'{ox + (xr - ox) * i / 60:.1f} {cy(i / 60):.1f}' for i in range(61))
    s += path('M' + pts, sw=7) + circle(xr, cy(1), 12, INK, None)
    s += path(f'M{ox} {yt - 4} V{oy} H{xr + 14}', sw=5)
    # slider rail on two posts
    x0, x1, ry = 140, 940, 1400
    kx = x0 + (x1 - x0) * 0.7
    s += floor_line(60, 1020, FL)
    s += line(x0, ry, x0, FL, INK, 7) + line(x1, ry, x1, FL, INK, 7)
    s += rrect(x0 - 14, ry - 14, x1 - x0 + 28, 28, 14, WHITE, INK, 5)
    s += rrect(x0 - 9, ry - 9, kx - x0 + 9, 18, 9, BLUE, None)
    for i in range(11):
        x = x0 + (x1 - x0) * i / 10
        s += line(x, ry + 22, x, ry + 40, INK, 4)
    s += T(x0, ry - 44, '10', 44) + T(x1, ry - 44, '20', 44)
    s += T(540, FL + 78, 'Years', 46)
    s += circle(kx, ry, 48, WHITE, INK, 5) + circle(kx, ry, 18, BLUE, None)
    s += rrect(kx - 50, ry - 150, 100, 70, 18, BLUE, None) + T(kx, ry - 99, '17', 44, fill=WHITE)
    s += path(f'M{kx - 14} {ry - 82} L{kx} {ry - 62} L{kx + 14} {ry - 82} Z', fill=BLUE, stroke=None)
    # Ledger in side view leans into the knob with both hands
    L = Ledger('side_r', 0, FL, 2.3, rot=9)
    L.X = (kx - 48 - 18) - (L.w((156, 150))[0] - L.X)
    b, f = L.draw(armL={'hand': L.r((kx - 50, ry - 24)), 'front': True, 'bend': -1},
                  armR={'hand': L.r((kx - 54, ry + 14)), 'front': True, 'bend': 1}, shadow=False)
    s += b + f
    for i in range(3):
        s += line(L.X - 110 - i * 8, 1210 + i * 52, L.X - 172 - i * 8, 1210 + i * 52, BLUE, 6)   # push lines
    return s, L


def A4():
    BL, CX, SG, HH = 1150, 430, 180, 440
    hy = lambda x: BL - HH * math.exp(-((x - CX) / SG) ** 2 / 2)
    s = chip('Statistics')
    # shaded right tail (z above 2)
    x2 = CX + 2 * SG
    tail = f'M{x2} {BL} L' + ' L'.join(f'{x:.1f} {hy(x):.1f}' for x in range(int(x2), 1041, 6)) + f' L1040 {BL} Z'
    s += path(tail, fill=BLUE, stroke=None)
    hill = 'M40 %.1f L' % hy(40) + ' L'.join(f'{x} {hy(x):.1f}' for x in range(46, 1041, 6))
    s += path(hill + f' L1040 {BL} L40 {BL} Z', fill=TINT, stroke=None) + path(tail, fill=BLUE, stroke=None)
    # steps down the right slope
    xs = [502, 634, 766]
    for a, b_ in zip(xs, xs[1:]):
        w = f'M{a} {hy(a):.1f} H{b_} V{hy(b_):.1f} L' + ' L'.join(f'{x:.1f} {hy(x):.1f}' for x in range(b_, a - 1, -6)) + ' Z'
        s += path(w, fill=WHITE, sw=5)
    s += path(hill, sw=7)
    s += line(30, BL, 1050, BL, INK, 5)
    for z in range(-2, 4):
        x = CX + z * SG
        s += line(x, BL, x, BL + 16, INK, 4) + T(x, BL + 58, str(z).replace('-', '−'), 34, fill=SLATE if z != 2 else INK)
    s += line(x2, BL, x2, hy(x2), INK, 4, dash='8 8')
    # Ledger on the lower step carrying the dot toward the tail
    ty = hy(xs[1])
    L = Ledger('34f_r', (xs[1] + xs[2]) / 2 - 5 * 1.9 + 4, ty, 1.9)
    bc = L.w((126, 164))
    b, f = L.draw(armL={'hand': L.r((bc[0] - 40, bc[1] + 12)), 'front': True, 'bend': 1},
                  armR={'hand': L.r((bc[0] + 40, bc[1] + 12)), 'front': True, 'bend': -1},
                  face={'look': (3, 2), 'mouth': 'smile'}, shadow=False)
    s += b + circle(bc[0], bc[1], 36, BLUE, INK, 5) + f
    tx, tyy = x2 + 96, BL - 22
    s += curve_arrow(L.w((196, 150))[0], bc[1] + 10, tx + 10, bc[1] + 30, tx + 4, tyy - 54)
    s += circle(tx, tyy, 14, 'none', WHITE, 4)
    # card
    s += rrect(100, 1310, 880, 250, 30, WHITE, INK, 5)
    s += T(150, 1412, 'z = 2.0', 76, anchor='start') + tick(150 + tw('z = 2.0', 76) + 62, 1386, 36)
    s += T(150, 1500, 'Only about 2% of results are this high', 40, weight=600, anchor='start', maxw=790)
    return s, L


def A5():
    ox, oy, xr, yt = 150, 1330, 1010, 560
    m = 0.21                                             # demand: x falls by m for each px up
    s = chip('Economics')
    # three small cards floating behind
    s += group(card(190, 140, mini_t(140, 96, False)), 300, 400, -6)
    s += group(card(190, 140, mini_growth(130, 86)), 550, 380, 4)
    s += group(card(190, 140, mini_bell(140, 84)), 800, 404, -3)
    # chart
    s += path(f'M{ox} {yt - 10} V{oy} H{xr + 10}', sw=6)
    s += T(ox - 22, yt - 34, 'Price', 40, anchor='start') + T(xr + 14, oy + 62, 'Quantity', 40, anchor='end')
    S = lambda x: 1280 - 0.9067 * (x - 230)
    s += line(230, S(230), 990, S(990), INK, 7) + T(982, S(990) - 26, 'Supply', 40, anchor='end')
    d1b, d2b = 650, 840
    D = lambda b, y: b - (oy - y) * m
    s += line(D(d1b, yt + 30), yt + 30, d1b, oy, BLUE, 6, dash='16 14', extra='opacity="0.7"')
    s += line(D(d2b, yt + 30), yt + 30, d2b, oy, BLUE, 8)
    s += T(D(d2b, yt + 30) + 22, yt + 62, 'Demand', 40, anchor='start', fill=BLUE)
    def eq(b):
        y = (1280 - 0.9067 * (b - oy * m - 230)) / (1 + 0.9067 * m)
        return D(b, y), y
    (e1x, e1y), (e2x, e2y) = eq(d1b), eq(d2b)
    s += line(ox, e1y, e1x, e1y, SLATE, 4, dash='4 12') + line(ox, e2y, e2x, e2y, SLATE, 4, dash='4 12')
    s += circle(e1x, e1y, 12, WHITE, INK, 5) + circle(e2x, e2y, 14, INK, None)
    s += arrow(ox + 44, e1y - 16, ox + 44, e2y + 14, GREEN, 10, head=34)
    s += arrow(D(d1b, 668) + 40, 668, D(d2b, 668) - 30, 668, BLUE, 6, head=24)   # the line moves right
    # Ledger in side view pushes the new demand line: shoulder (top corner) and both hands
    L = Ledger('side_r', 0, oy, 2.2, rot=4)
    cxw, cyw = L.w((140.5, 40))
    L.X += D(d2b, cyw) - cxw - 6
    h1y, h2y = L.w((0, 128))[1], L.w((0, 153))[1]
    b, f = L.draw(armL={'hand': L.r((D(d2b, h1y) - 24, h1y)), 'front': True, 'bend': -1},
                  armR={'hand': L.r((D(d2b, h2y) - 24, h2y)), 'front': True, 'bend': 1}, shadow=False)
    s += b + f
    return s, L


def A6():
    ox, oy, xr, yt = 140, 1340, 1010, 600
    sl = 0.40
    e2 = (770, 990)
    IS2 = lambda x: e2[1] + sl * (x - e2[0])
    IS1 = lambda x: IS2(x) + 140
    LM = lambda x: e2[1] - 0.85 * (x - e2[0])
    d = -140 / (0.85 + sl)
    e1 = (e2[0] + d, LM(e2[0] + d))
    s = path(f'M{ox} {yt - 10} V{oy} H{xr + 10}', sw=6)
    s += T(ox - 22, yt - 36, 'Interest rate', 40, anchor='start') + T(xr + 14, oy + 62, 'Output', 40, anchor='end')
    s += line(560, LM(560), 1000, LM(1000), INK, 7) + T(1000, LM(1000) - 26, 'LM', 44, anchor='end')
    s += line(ox + 20, IS1(ox + 20), 990, IS1(990), BLUE, 6, dash='16 14', extra='opacity="0.7"')
    s += line(ox + 20, IS2(ox + 20), 990, IS2(990), BLUE, 8)
    s += T(1004, IS2(990) - 34, 'IS', 44, anchor='end', fill=BLUE)
    # crossing point moves along LM
    off = 34
    s += curve_arrow(e1[0] + off, e1[1] + 10, (e1[0] + e2[0]) / 2 + off + 16, (e1[1] + e2[1]) / 2 + 20, e2[0] + off - 4, e2[1] + 22, stroke=INK, sw=5, dash='3 13', head=22)
    s += circle(e1[0], e1[1], 12, WHITE, INK, 5) + circle(e2[0], e2[1], 15, INK, None)
    for i in range(3):
        x = 850 + i * 40
        s += arrow(x, IS1(x) - 22, x, IS2(x) + 30, BLUE, 6, head=22) if i != 1 else ''
    # ladder and Ledger from the back, both hands under the IS line
    LX, sc = 400, 2.1
    LY = IS2(LX) + (222 - 136) * sc
    s += line(LX - 62, LY + 8, LX - 112, oy - 3, INK, 9) + line(LX + 62, LY + 8, LX + 112, oy - 3, INK, 9)
    n = 3
    for i in range(1, n + 1):
        t = i / (n + 0.6)
        yy = LY + 8 + (oy - LY - 8) * t
        xx = 62 + 50 * t
        s += line(LX - xx, yy, LX + xx, yy, INK, 7)
    s += rrect(LX - 86, LY, 172, 18, 6, WHITE, INK, 5)
    L = Ledger('back', LX, LY, sc)
    hl = L.w((39, 0))[0]
    hr = L.w((201, 0))[0]
    b, f = L.draw(armL={'hand': L.r((hl, IS2(hl) + 9 * sc + 4)), 'bend': 1},
                  armR={'hand': L.r((hr, IS2(hr) + 9 * sc + 4)), 'bend': -1}, shadow=False)
    s += b + f
    return s, L


def A7():
    s = ''
    def lines(rows, size, lh=None, weight=700, fill=INK):
        lh = lh or size * 1.32
        y0 = -lh * (len(rows) - 1) / 2 + size * 0.35
        return ''.join(T(0, y0 + i * lh, r, size, weight, fill=fill, check=False) for i, r in enumerate(rows))
    be = lines(['Break-even units =', 'Fixed costs ÷', '(Price − Variable cost per unit)'], 32)
    npv = T(0, -34, 'NPV =', 42, check=False)
    npv += (f'<text x="0" y="38" font-family="{FONT}" font-size="36" font-weight="700" text-anchor="middle" fill="{INK}">'
            f'Σ CF<tspan dy="10" font-size="24">t</tspan><tspan dy="-10"> ÷ (1 + r)</tspan><tspan dy="-16" font-size="24">t</tspan>'
            f'<tspan dy="16"> − Initial cost</tspan></text>')
    zf = lines(['z = (x − μ) ÷ σ'], 54)
    ale = lines(['Assets =', 'Liabilities + Equity'], 44)
    cards = [
        (300, 400, -4, 532, 250, be),
        (824, 366, 5, 404, 170, zf),
        (800, 700, -3, 420, 360, group(mini_sd(290, 230, True), 0, 4)),
        (304, 760, 3, 540, 220, npv),
        (274, 1110, -5, 430, 270, group(mini_t(340, 200), 0, 0)),
        (784, 1110, 4, 500, 210, ale),
    ]
    for cx, cy, rot, w, h, inner in cards:
        s += group(card(w, h, inner), cx, cy, rot)
    s += floor_line(300, 780, 1720)
    L = Ledger('back', 540, 1720, 1.7)
    b, f = L.draw(armL={'hand': (25, 127), 'bend': 1}, armR={'hand': (215, 127), 'bend': -1}, shadow=False)
    s += b + f
    for dx, dy, r in ((-250, -330, 40), (0, -400, 44), (250, -330, 40)):
        s += line(540 + dx * 0.72, 1720 + dy * 0.72 - 60, 540 + dx * 0.86, 1720 + dy * 0.86 - 60, BLUE, 6)
    return s, L


def A8():
    s = T(540, 560, 'Get started', 124) + T(540, 706, 'for free', 124)
    sc, X, Y = 2.4, 846, 1262
    py = Y - (222 - 152.9) * sc
    s += rrect(64, py - 74, 540, 148, 74, BLUE, None) + T(292, py + 20, 'edlintics.com', 56, fill=WHITE, maxw=400)
    s += embed_state('point-left', X, Y, sc)
    hxw = X + (3.65 - 120) * sc
    for ang in (-140, -100, -60):
        a = math.radians(ang)
        s += line(hxw - 16 + 92 * math.cos(a), py + 92 * math.sin(a), hxw - 16 + 132 * math.cos(a), py + 132 * math.sin(a), INK, 7)
    return s, None


FRAMES = {'A1': A1, 'A2': A2, 'A3': A3, 'A4': A4, 'A5': A5, 'A6': A6, 'A7': A7, 'A8': A8}


def build(name):
    WARN.clear()
    inner, L = FRAMES[name]()
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
           f'<rect width="{W}" height="{H}" fill="{BG}"/>{inner}</svg>')
    open(os.path.join(HERE, f'{name}.svg'), 'w').write(svg)
    html = os.path.join(HERE, f'_{name}.html')
    open(html, 'w').write(f'<!doctype html><meta charset="utf-8"><style>html,body{{margin:0;background:{BG}}}svg{{display:block}}</style>{svg}')
    png = os.path.join(HERE, f'{name}.png')
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


def sheet():
    names = [n for n in FRAMES if os.path.exists(os.path.join(HERE, f'{n}.png'))]
    tw_, th = 250, 444
    im = Image.new('RGB', (tw_ * len(names), th), 'white')
    for i, n in enumerate(names):
        im.paste(Image.open(os.path.join(HERE, f'{n}.png')).convert('RGB').resize((tw_ - 4, th - 4), Image.Resampling.LANCZOS), (i * tw_ + 2, 2))
    im.save(os.path.join(HERE, 'sheet.png'))
    print('sheet.png', im.size)


if __name__ == '__main__':
    for n in (sys.argv[1:] or list(FRAMES)):
        build(n)
    sheet()
