#!/usr/bin/env python3
"""Edlintics demo video A: 8 storyboard stills, drawn in code (SVG) and rendered with headless Chrome.

Run:  python3 frames_a.py            (all frames + sheet.png)
      python3 frames_a.py A3 A5      (only those frames, sheet rebuilt from what exists)
Output goes next to this file, or to the folder named in the FRAMES_OUT environment variable.

Look (v3, after Hoang's notes of 20 Nov 2026): one flat saturated background per subject, a big
subject name with the topic under it, white cards with a flat offset block, no gradients.

Ledger is drawn from the website rig numbers (assets/brand-handoff/ledger-v2/RIG.md) and the
turnaround sheet (front, 3/4 front, side, 3/4 back, back). Arms use the rig's two-segment arm
(upper 23.3, forearm 16.5, reach n <= 1.7); the script refuses to draw a longer arm.
A8 embeds the real rig state file ledger-hello.svg unchanged.
"""
import math, os, re, subprocess, sys
from PIL import Image, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('FRAMES_OUT', HERE)
STATES = '/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing/assets/brand-handoff/ledger-v2/states'
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
    DX, DT = 500, 560
    s += rrect(DX - 200, DT, 400, FL - DT, 10, WHITE, INK, 5)
    s += rrect(DX - 172, DT + 28, 344, FL - DT - 31, 6, BLUE, INK, 5)
    s += rrect(DX - 136, DT + 66, 272, 380, 8, 'none', INK, 4, 'opacity="0.55"')
    s += rrect(DX - 136, DT + 490, 272, 450, 8, 'none', INK, 4, 'opacity="0.55"')
    hx, hy = DX + 122, FL - 250
    s += rrect(hx - 22, hy - 54, 44, 108, 12, CREAM, INK, 4)
    s += panel(DX - 270, 330, 540, 140, 24) + T(DX, 421, 'Learning business', 56, maxw=500)
    s += line(DX - 130, 470, DX - 130, DT, INK, 6) + line(DX + 130, 470, DX + 130, DT, INK, 6)
    # three floating phones
    def phone(cx, cy, rot, label, inner):
        p = rrect(-104, -157, 224, 330, 30, INK, None) + rrect(-112, -165, 224, 330, 30, WHITE, INK, 5) + rrect(-30, -150, 60, 10, 5, INK, None) + inner
        return group(p, cx, cy, rot) + T(cx, cy + 230, label, 42)
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
    s += phone(916, 370, -4, 'Languages', lang)
    s += phone(916, 860, 3, 'Coding', code)
    s += phone(916, 1350, -3, 'Science', mol)
    # Ledger from 3/4 back, one hand on the handle
    L = Ledger('34b_r', hx - 258, FL + 20, 2.9)
    b, f = L.draw(armR={'hand': L.r((hx - 2, hy + 4)), 'front': True, 'bend': 1})
    return s + b + f, L, YEL


def A2():
    FL = 1740
    s = floor(FL - 60, EMER_D) + header('ACCOUNTING', 'Journal entries')
    mx, my, mw, mh = 70, 410, 940, 650
    s += monitor(mx, my, mw, mh)
    s += rrect(270, my + mh + 82, 540, 26, 8, CREAM, INK, 5)                          # wall shelf
    # T-account on the screen
    tm, ty = 540, my + 138
    s += T(315, ty - 30, 'Debit', 58) + T(765, ty - 30, 'Credit', 58)
    s += line(130, ty, 950, ty, INK, 8) + line(tm, ty, tm, my + mh - 50, INK, 8)
    s += T(315, ty + 66, 'Cash', 44, fill=SLATE) + T(765, ty + 66, 'Sales', 44, fill=SLATE)
    s += rrect(215, ty + 100, 200, 110, 16, TINT, BLUE, 5, 'stroke-dasharray="14 10"')   # where the block goes
    s += block(765, ty + 155, fill=ORANGE)
    # the source of the entry and the drag trail
    s += rrect(650, my + mh - 150, 300, 86, 43, CREAM, INK, 4) + T(800, my + mh - 95, 'Cash sale €500', 34, maxw=280)
    bx, by = 388, ty + 228
    s += path(f'M648 {my + mh - 110} Q 560 {my + mh - 96} {bx + 122} {by + 110}', stroke=INK, sw=6, dash='3 15')
    s += block(bx, by, fill=BLUE, lift=10)
    s += cursor(bx + 56, by + 22)
    # Ledger at a small desk, 3/4 back, one hand on the mouse
    L = Ledger('34b_r', 400, FL, 2.7)
    hx, hy = L.w((214, 168))
    top = hy + 42
    dx0 = L.w((192, 0))[0]
    s += line(dx0 + 40, top + 20, dx0 + 40, FL + 16, INK, 10) + line(dx0 + 320, top + 20, dx0 + 320, FL + 16, INK, 10)
    s += rrect(dx0, top, 360, 30, 8, CREAM, INK, 5)
    s += path(f'M{hx + 46} {hy + 16} C {hx + 190} {hy - 30} 930 1330 800 {my + mh + 108}', stroke=INK, sw=5)   # mouse cable
    b, f = L.draw(armR={'hand': L.r((hx, hy)), 'front': True, 'bend': 1})
    s += b
    s += rrect(hx - 38, hy - 8, 88, 50, 24, WHITE, INK, 5) + line(hx + 6, hy - 8, hx + 6, hy + 12, INK, 4)
    s += f
    return s, L, EMER


def A3():
    FL = 1700
    s = floor(FL - 60, ORANGE_D) + header('FINANCE', 'Compound interest')
    s += panel(60, 410, 960, 640)
    ox, oy, xr, yt = 150, 970, 940, 530
    s += T(ox, 490, 'Savings', 42, anchor='start')
    k = math.log((oy - yt - 30) / 60)
    cy = lambda t: oy - 60 * math.exp(k * t)
    for i in range(5):
        t = 0.16 + 0.19 * i
        x = ox + (xr - ox) * t
        n = max(1, int((oy - cy(t) - 34) // 24))
        for j in range(n):
            s += rrect(x - 40, oy - 3 - 24 * (j + 1), 80, 24, 12, YEL, INK, 3)
    pts = ' L'.join(f'{ox + (xr - ox) * i / 60:.1f} {cy(i / 60):.1f}' for i in range(61))
    s += path('M' + pts, stroke=BLUE, sw=9) + circle(xr, cy(1), 15, BLUE, INK, 4)
    s += path(f'M{ox} {yt - 4} V{oy} H{xr + 14}', sw=6)
    # slider rail on two posts
    sc = 2.8
    x0, x1, ry = 110, 970, FL - 196
    kx = x0 + (x1 - x0) * 0.7
    s += line(x0, ry, x0, FL, INK, 9) + line(x1, ry, x1, FL, INK, 9)
    s += rrect(x0 - 18, ry - 18, x1 - x0 + 36, 36, 18, WHITE, INK, 5)
    s += rrect(x0 - 12, ry - 12, kx - x0 + 12, 24, 12, BLUE, None)
    for i in range(11):
        x = x0 + (x1 - x0) * i / 10
        s += line(x, ry + 28, x, ry + 48, INK, 5)
    s += T(x0, ry - 50, '10', 50) + T(x1, ry - 50, '20', 50)
    # Ledger 3/4 front, one hand pushing the knob
    L = Ledger('34f_r', (kx - 62) - 105 * sc, FL, sc)
    b, f = L.draw(armR={'hand': L.r((kx - 62, ry)), 'front': True, 'bend': -1},
                  face={'look': (3, 0.5), 'mouth': 'grin', 'brows': 2})
    s += b
    s += circle(kx, ry, 54, WHITE, INK, 5) + circle(kx, ry, 22, BLUE, None)
    s += rrect(kx - 122, ry - 196, 244, 90, 22, BLUE, INK, 5) + T(kx, ry - 134, '17 years', 50, fill=WHITE)
    s += path(f'M{kx - 18} {ry - 108} L{kx} {ry - 78} L{kx + 18} {ry - 108} Z', fill=BLUE, stroke=None)
    s += f
    lx = L.w((58, 0))[0]
    for i in range(3):
        s += line(lx - 36, FL - 500 + i * 64, lx - 120 + i * 16, FL - 500 + i * 64, WHITE, 9)   # push lines
    return s, L, ORANGE


def A4():
    FL = 1800
    s = floor(FL - 70, VIOLET_D) + header('STATISTICS', 'Hypothesis testing')
    s += panel(40, 410, 1000, 780)
    BL, CX, SG, HH, TOP = 1090, 540, 148, 430, 440
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
        s += line(x, BL, x, BL + 18, INK, 5) + T(x, BL + 64, lab, 40)
    s += T((xa + xl) / 2, TOP + 52, 'Reject H_0', 31, fill=GREEN_D, maxw=xl - xa)
    s += T((xr + xb) / 2, TOP + 52, 'Reject H_0', 31, fill=GREEN_D, maxw=xb - xr)
    s += T(CX, TOP + 66, 'Do not reject H_0', 50, fill=RED_D)
    # the z marker, planted just past 1.96
    zx = CX + 2.0 * SG
    s += line(zx, BL, zx, 700, INK, 7) + circle(zx, BL, 14, INK, None)
    s += rrect(zx - 118 + 8, 628, 236, 92, 18, INK, None) + rrect(zx - 118, 620, 236, 92, 18, YEL, INK, 5) + T(zx, 684, 'z = 2.0', 50)
    # result badge
    s += panel(40, 1290, 556, 300)
    s += tick(128, 1392, 58) + T(206, 1418, 'Reject H_0', 70, anchor='start', maxw=380)
    s += T(78, 1530, 'z = 2.0 is beyond 1.96', 42, weight=600, anchor='start', fill=SLATE, maxw=520)
    # Ledger, happy, pointing up at the marker
    L = Ledger('34f_l', 868, FL, 2.5)
    b, f = L.draw(armL={'hand': (30, 110), 'front': True, 'bend': -1},
                  face={'look': (-2, -2), 'glad': True, 'mouth': 'grin'})
    s += b + f
    return s, L, VIOLET


def A5():
    s = header('ECONOMICS', 'Market equilibrium')
    s += panel(30, 410, 1016, 1350)
    ox, oy, yt, xr = 130, 1640, 500, 1000
    m, ex, ey, sh = 1.25, 480, 1050, 130
    S = lambda x: ey - m * (x - ex)
    D2 = lambda x: ey + m * (x - ex)
    D1 = lambda x: ey + m * (x - ex + sh)
    e1x = ex - sh / 2
    e1y = S(e1x)
    # platform for Ledger between the two lines
    sc, LX, LY = 2.5, 862, 1300
    s += rrect(LX + 8, LY + 26, 26, oy - LY - 26, 0, PINK_D, INK, 5)
    s += path(f'M{ox} {yt - 10} V{oy} H{xr + 10}', sw=7)
    s += arrow_head(ox, yt - 30, -90, 30) + arrow_head(xr + 30, oy, 0, 30)
    s += T(ox + 30, 492, 'Price', 40, anchor='start', fill=SLATE) + T(xr + 20, oy + 68, 'Quantity', 40, anchor='end', fill=SLATE)
    s += line(ox, ey, ex, ey, SLATE, 5, dash='3 14') + line(ex, ey, ex, oy, SLATE, 5, dash='3 14')
    s += line(175, D1(175), 700, D1(700), PINK, 7, dash='18 16')                       # where demand was
    s += line(180, S(180), 850, S(850), INK, 10) + T(876, S(850) - 26, 'Supply', 48, anchor='end')
    s += line(205, D2(205), 810, D2(810), PINK, 11)
    s += T(214, D2(205) - 30, 'Demand', 48, anchor='start', fill=PINK_D)
    for yy in (880, 1400):
        xa, xb = ex - sh + (yy - ey) / m, ex + (yy - ey) / m
        s += arrow(xa + 22, yy, xb - 20, yy, PINK_D, 8, head=26)
    s += circle(e1x, e1y, 14, WHITE, INK, 5) + circle(ex, ey, 20, GREEN, INK, 6)
    s += T(78, ey + 18, 'P*', 52) + T(ex, oy + 72, 'Q*', 52)
    s += rrect(LX - 126, LY, 290, 30, 8, PINK, INK, 5)
    # Ledger on the platform, 3/4 front, one hand on the grip of the demand line
    L = Ledger('34f_l', LX, LY, sc)
    gx, gy = 606, D2(606)
    b, f = L.draw(armL={'hand': L.r((gx + 16, gy - 12)), 'front': True, 'bend': 1},
                  face={'look': (-3, 1.5), 'mouth': 'smile', 'brows': 2}, shadow=False)
    s += b + f
    return s, L, PINK


def A6():
    FL = 1800
    s = floor(FL - 70, PINK_D) + header('ECONOMICS', 'The IS-LM model')
    mx, my, mw, mh = 40, 410, 1000, 730
    s += monitor(mx, my, mw, mh)
    s += rrect(250, my + mh + 82, 580, 26, 8, CREAM, INK, 5)
    ox, oy, yt, xr = 150, 1040, 480, 990
    y1, y2, m = 650, 830, 1.125
    e1, e2 = (700, y1), (700 + (y2 - y1) / m, y2)
    IS = lambda x: y1 + m * (x - 700)
    s += path(f'M{ox} {yt - 6} V{oy} H{xr + 6}', sw=7)
    s += arrow_head(ox, yt - 24, -90, 28) + arrow_head(xr + 24, oy, 0, 28)
    s += T(ox + 26, yt - 4, 'Interest rate i', 38, anchor='start', fill=SLATE)
    s += T(ox + 20, oy + 56, 'Output Y', 38, anchor='start', fill=SLATE)
    s += line(e1[0], y1, e1[0], oy, SLATE, 5, dash='3 14') + line(e2[0], y2, e2[0], oy, SLATE, 5, dash='3 14')
    s += line(ox, y1, xr - 20, y1, SLATE, 7, dash='18 16')
    s += line(ox, y2, xr - 20, y2, INK, 10)
    s += line(540, IS(540), 905, IS(905), BLUE, 10) + T(524, IS(540) + 34, 'IS', 54, anchor='end', fill=BLUE)
    s += T(ox + 26, y2 + 56, 'LM (set by the central bank)', 38, anchor='start', maxw=530)
    s += arrow(330, y1 + 26, 330, y2 - 22, PINK, 14, head=40)
    s += circle(e1[0], y1, 14, WHITE, INK, 5) + circle(e2[0], y2, 20, GREEN, INK, 6)
    s += T(e1[0], oy + 58, 'Y_1', 46) + T(e2[0], oy + 58, 'Y_2', 46)
    s += arrow(e1[0] + 44, oy + 42, e2[0] - 44, oy + 42, GREEN, 8, head=24)
    cxp = 940
    s += line(cxp, y1 + 14, cxp, y2 - 16, INK, 6, dash='3 15') + cursor(cxp - 4, y2 - 4)
    # Ledger from the back, game controller in both hands
    sc = 2.4
    L = Ledger('back', 540, FL, sc)
    pad = rrect(8, 146, 224, 46, 23, WHITE, INK, 4)
    pad += rrect(8, 160, 46, 56, 22, WHITE, INK, 4) + rrect(186, 160, 46, 56, 22, WHITE, INK, 4)
    pad += rrect(12, 150, 216, 38, 19, WHITE, None)
    pad += rrect(24, 156, 8, 24, 2, INK, None) + rrect(16, 164, 24, 8, 2, INK, None)                 # D-pad
    pad += circle(206, 160, 5.5, GREEN, INK, 2) + circle(218, 171, 5.5, RED, INK, 2) + circle(205, 177, 5.5, YEL, INK, 2)
    s += f'<g transform="translate({L.X - 120 * sc:.2f} {L.Y - 222 * sc:.2f}) scale({sc})">{pad}</g>'
    b, f = L.draw(armL={'hand': (30, 200), 'bend': 1}, armR={'hand': (210, 200), 'bend': -1})
    s += b + f
    top = L.w((0, 34))[1]
    for r in (22, 44, 66):
        s += path(f'M{540 - r} {top - 16} A{r} {r} 0 0 1 {540 + r} {top - 16}', stroke=WHITE, sw=9)   # wireless signal
    return s, L, PINK


def A7():
    s = floor(1740, YEL_D)
    def lines(rows, size, lh=None, weight=700, fill=INK):
        lh = lh or size * 1.32
        y0 = -lh * (len(rows) - 1) / 2 + size * 0.35
        return ''.join(T(0, y0 + i * lh, r, size, weight, fill=fill, check=False) for i, r in enumerate(rows))
    be = lines(['Break-even units =', 'Fixed costs ÷', '(Price − Variable cost per unit)'], 32, fill=WHITE)
    npv = T(0, -34, 'NPV =', 44, check=False, fill=WHITE)
    npv += (f'<text x="0" y="38" font-family="{FONT}" font-size="36" font-weight="700" text-anchor="middle" fill="{WHITE}">'
            f'Σ CF<tspan dy="10" font-size="24">t</tspan><tspan dy="-10"> ÷ (1 + r)</tspan><tspan dy="-16" font-size="24">t</tspan>'
            f'<tspan dy="16"> − Initial cost</tspan></text>')
    zf = lines(['z = (x − μ) ÷ σ'], 54, fill=WHITE)
    ale = lines(['Assets =', 'Liabilities + Equity'], 44, fill=WHITE)
    cards = [
        (300, 300, -4, 532, 250, be, EMER_D),
        (824, 266, 5, 404, 170, zf, VIOLET),
        (800, 610, -3, 420, 360, group(mini_sd(290, 230), 0, 4), WHITE),
        (304, 670, 3, 540, 220, npv, ORANGE),
        (274, 1030, -5, 430, 270, group(mini_t(340, 200, True, EMER, '#A7F3D0'), 0, 0), WHITE),
        (784, 1030, 4, 500, 210, ale, BLUE),
    ]
    for cx, cy, rot, w, h, inner, fill in cards:
        s += group(card(w, h, inner, fill=fill), cx, cy, rot)
    L = Ledger('back', 540, 1800, 2.5)
    b, f = L.draw(armL={'hand': (25, 127), 'bend': 1}, armR={'hand': (215, 127), 'bend': -1})
    s += b + f
    top = L.w((0, 34))[1]
    s += sparks(540, top + 150, 215, 268, (-145, -118, -90, -62, -35), WHITE, 10)
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
    s += rrect(ix + 190, iy + 18, iw - 240, 64, 32, WHITE, INK, 3) + T(ix + 190 + (iw - 240) / 2, iy + 65, 'edlintics.com', 40)
    # page
    wm, a_, b_ = 120, 'Ed', 'lintics'
    wa, wb = tw(a_, wm), tw(b_, wm)
    x0 = 540 - (wa + wb) / 2
    s += T(x0, iy + 270, a_, wm, anchor='start') + T(x0 + wa, iy + 270, b_, wm, anchor='start', fill=BLUE)
    s += T(540, iy + 370, 'Learn the language of business', 54, maxw=iw - 60)
    rows = [(('Accounting', EMER_D), ('Finance', ORANGE)), (('Economics', PINK), ('Statistics', VIOLET))]
    for r, row in enumerate(rows):
        ws = [tw(t, 46) + 76 for t, _ in row]
        x = 540 - (sum(ws) + 28) / 2
        y = iy + 430 + r * 112
        for (t, col), w_ in zip(row, ws):
            s += rrect(x, y, w_, 88, 44, col, INK, 4) + T(x + w_ / 2, y + 60, t, 46, fill=WHITE)
            x += w_ + 28
    by = iy + 700
    s += rrect(160, by + 10, 780, 160, 80, INK, None) + rrect(150, by, 780, 160, 80, BLUE, INK, 5)
    s += T(540, by + 102, 'Get started for free', 66, fill=WHITE, maxw=700)
    s += cursor(862, by + 104, 2.1)
    # Ledger below the monitor, waving
    sc = 2.5
    s += embed_state('hello', 540, FL, sc)
    s += sparks(540, FL - 300, 300, 360, (-160, -20), WHITE, 10) + sparks(540, FL - 300, 300, 360, (-172, -8), WHITE, 10)
    return s, None, BLUE


FRAMES = {'A1': A1, 'A2': A2, 'A3': A3, 'A4': A4, 'A5': A5, 'A6': A6, 'A7': A7, 'A8': A8}


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


def sheet():
    names = [n for n in FRAMES if os.path.exists(os.path.join(OUT, f'{n}.png'))]
    tw_, th = 250, 444
    im = Image.new('RGB', (tw_ * len(names), th), 'white')
    for i, n in enumerate(names):
        im.paste(Image.open(os.path.join(OUT, f'{n}.png')).convert('RGB').resize((tw_ - 4, th - 4), Image.Resampling.LANCZOS), (i * tw_ + 2, 2))
    im.save(os.path.join(OUT, 'sheet.png'))
    print('sheet.png', im.size)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for n in (sys.argv[1:] or list(FRAMES)):
        build(n)
    sheet()
