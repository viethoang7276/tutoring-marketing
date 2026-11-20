#!/usr/bin/env python3
"""Demo video A, first half as animation: A1, T1, A2, T2, A3, T3, A4.

Every scene is fn(t, dur) -> (svg_inner, background) and a pure function of time. The drawing comes from
frames_a.py (same helpers, same numbers), the timing from anim_util.py. Each A scene starts as its static
"question" frame and ends as its static "solved" frame; each T scene starts on the previous scene's last
layout and ends on the next scene's first one.

Ledger: front poses are the real website rig states (only the rig's own channels are driven: root hop,
torso tilt and breathing, eye gaze, blink, legs); the desk scenes use the straight back view; travelling
shots use frames_a.Mover. Arm reach and leg swing keep the rig asserts.

Self-check:  python anim_a1.py   runs every frame of every scene (asserts, text warnings, speed).
"""
import functools, math, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import frames_a as F
from frames_a import (T, rrect, line, path, circle, arrow_head, INK, CREAM, SUIT, BLUE, RULE, GREEN, WHITE, PAGES,
                      TINT, SLATE, EMER, ORANGE, VIOLET, PINK, YEL, EMER_D, ORANGE_D, VIOLET_D, YEL_D,
                      GREEN_T, RED_T, GREEN_D, RED_D, RED2, W, H)
from anim_util import clamp, seg, ease, ease_out, ease_in, back_out, lerp, lerp2, bez, hop, pop, fade, shift, squash

TAU = 2 * math.pi
DUST = '#FFF3C4'
VOICE = 0.25


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------
def smooth(p):
    p = clamp(p)
    return p * p * (3 - 2 * p)


def keys(t, ks, f=ease):
    """Eased keyframes [(time, value), ...]."""
    if t <= ks[0][0]:
        return ks[0][1]
    for (t0, v0), (t1, v1) in zip(ks, ks[1:]):
        if t <= t1:
            return lerp(v0, v1, f(seg(t, t0, t1)))
    return ks[-1][1]


def bump(t, t0, d=0.3):
    """0 -> 1 -> 0 over d seconds starting at t0."""
    return math.sin(math.pi * seg(t, t0, t0 + d)) if t0 < t < t0 + d else 0.0


def wave(t, end, period, phase=0.0):
    """Sine that is exactly 0 at t = end, so loops land on the static frame."""
    return math.sin(TAU * (t - end) / period + phase) - math.sin(phase)


def loop(t, end, period):
    """Loop phase 0..1 that is 0 at t = end."""
    return ((t - end) / period) % 1.0


def rot(inner, cx, cy, a):
    return f'<g transform="rotate({a:.2f} {cx:.1f} {cy:.1f})">{inner}</g>' if a else inner


def scale(inner, cx, cy, k):
    return f'<g transform="translate({cx:.1f} {cy:.1f}) scale({k:.3f}) translate({-cx:.1f} {-cy:.1f})">{inner}</g>'


def qb(p0, c, p1, u):
    q = 1 - u
    return (q * q * p0[0] + 2 * q * u * c[0] + u * u * p1[0], q * q * p0[1] + 2 * q * u * c[1] + u * u * p1[1])


def qang(p0, c, p1, u):
    q = 1 - u
    dx = 2 * q * (c[0] - p0[0]) + 2 * u * (p1[0] - c[0])
    dy = 2 * q * (c[1] - p0[1]) + 2 * u * (p1[1] - c[1])
    return math.degrees(math.atan2(dy, dx))


def qarrow(p0, c, p1, p, stroke=BLUE, sw=8, head=30, n=24):
    """Curved arrow that draws on from tail to head."""
    if p <= 0.02:
        return ''
    pts = [qb(p0, c, p1, p * i / n) for i in range(n + 1)]
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    a = qang(p0, c, p1, p)
    tip = (pts[-1][0] + 8 * math.cos(math.radians(a)), pts[-1][1] + 8 * math.sin(math.radians(a)))
    return path(d, stroke=stroke, sw=sw) + arrow_head(tip[0], tip[1], a, head * min(1, 0.4 + p * 2), stroke)


def ghost_q(p0, c, p1, t, col=SLATE, a=1.0):
    """Dotted curved arrow whose dots march towards the head and whose head pulses."""
    if a <= 0:
        return ''
    ang = qang(p0, c, p1, 1)
    k = 1 + 0.18 * math.sin(TAU * 1.6 * t)
    s = path(f'M{p0[0]} {p0[1]} Q{c[0]} {c[1]} {p1[0]} {p1[1]}', stroke=col, sw=6, dash='4 16', extra=f'stroke-dashoffset="{-44 * t:.1f}"')
    s += arrow_head(p1[0] + 8 * math.cos(math.radians(ang)), p1[1] + 8 * math.sin(math.radians(ang)), ang, 24 * k, col)
    return fade(s, a * (0.72 + 0.28 * math.sin(TAU * 1.6 * t)))


def ghost_line(x1, y1, x2, y2, t, col=SLATE, a=1.0):
    if a <= 0:
        return ''
    d = 1 if x2 >= x1 else -1
    k = 1 + 0.18 * math.sin(TAU * 1.6 * t)
    s = line(x1, y1, x2 - d * 14, y2, col, 6, dash='4 16', extra=f'stroke-dashoffset="{-44 * t:.1f}"')
    s += arrow_head(x2, y2, 0 if d > 0 else 180, 24 * k, col)
    return fade(s, a * (0.72 + 0.28 * math.sin(TAU * 1.6 * t)))


def arrow_on(x1, y1, x2, y2, p, stroke=BLUE, sw=9, head=30):
    """Straight arrow drawing on from (x1, y1); p is the share of the way to (x2, y2)."""
    if p <= 0:
        return ''
    x, y = lerp(x1, x2, p), lerp(y1, y2, p)
    if math.hypot(x - x1, y - y1) < head * 0.9:
        return ''
    return F.arrow(x1, y1, x, y, stroke, sw, head=head)


def sparks(cx, cy, r0, r1, angles, col=WHITE, sw=8, k=1.0, push=0.0):
    """frames_a.sparks with a length factor k and an outward push, for pulsing."""
    if k <= 0:
        return ''
    return F.sparks(cx, cy, r0 + push, r0 + push + (r1 - r0) * k, angles, col, sw)


def cursor(x, y, press=0.0, sc=1.2):
    return F.cursor(x, y, sc * (1 - 0.16 * press))


def click_burst(x, y, p, col=INK):
    """Short lines round a click, growing and fading."""
    if p <= 0 or p >= 1:
        return ''
    return fade(F.sparks(x, y, 18 + 26 * p, 34 + 44 * p, (-150, -110, -70, -30), col, 6), 1 - p)


def blink_at(t, period=2.3, phase=0.7):
    u = (t + phase) % period
    return seg(u, 0, 0.06) - seg(u, 0.10, 0.20)


def popup(cx, cy, text, size, sub, p, t, end, col=WHITE, sw=8, corners=(0, 1, 2), h=None, n1=50):
    """frames_a.popup that pops in (p) and whose burst lines keep pulsing; equal to the static one at t = end."""
    if p <= 0:
        return ''
    wm = F.tw(text.replace('_', ''), size) + 96
    ws = F.tw(sub, 38, True) if sub else 0
    w = max(wm, ws) + 80
    hh = h or (196 if sub else 124)
    x, y = cx - w / 2, cy - hh / 2
    body = F.popup(cx, cy, text, size, sub, col, sw, (), h, n1)
    k = wave(t, end, 0.7) * 5
    burst = fade(F.pop_lines(x, y, w, hh, col, sw, 16 + k, n1 + k, corners), seg(p, 0.5, 1))
    return burst + pop(body, cx, cy, p, rot0=-6)


def confetti(pts, origin, p, t, end):
    """Confetti thrown from origin to its storyboard places (p), then drifting a little; static at t = end."""
    if p <= 0:
        return ''
    e = ease_out(p)
    out = []
    for i, (x, y, r) in enumerate(pts):
        dx = 5 * wave(t, end, 1.1 + 0.13 * i, i)
        dy = 6 * wave(t, end, 0.9 + 0.1 * i, 2 * i) - 70 * math.sin(math.pi * clamp(p)) * 0.4
        out.append((round(lerp(origin[0], x, e) + dx, 1), round(lerp(origin[1], y, e) + dy, 1), round(r + 300 * (1 - e) + 12 * wave(t, end, 0.8, i), 1)))
    return fade(F.confetti(out), clamp(p * 4))


def qmarks(items, t, end, t0=0.15, gap=0.15, out=None):
    """Question marks (x, y, size, rot) popping in one by one, bobbing, and popping away at `out`."""
    s = ''
    for i, (x, y, size, r) in enumerate(items):
        p = seg(t, t0 + gap * i, t0 + gap * i + 0.28)
        if out is not None:
            p *= 1 - seg(t, out + 0.05 * i, out + 0.05 * i + 0.16)
        if p <= 0:
            continue
        bob = 7 * math.sin(TAU * (t * 0.9 + i * 0.31))
        s += pop(F.qmark(x, round(y + bob, 1), size, round(r + 5 * math.sin(TAU * (t * 0.7 + i * 0.4)), 1)), x, y - size * 0.3, p, rot0=20)
    return s


def thought(cx, cy, t, t0, out):
    """Thought bubble: the two small circles first, then the bubble; it floats, then pops away."""
    a = 1 - seg(t, out, out + 0.18)
    if t < t0 or a <= 0:
        return ''
    by = 6 * math.sin(TAU * t * 0.8)
    s = pop(circle(cx - 150, cy + 118, 13, WHITE, INK, 5), cx - 150, cy + 118, seg(t, t0, t0 + 0.16))
    s += pop(circle(cx - 112, cy + 86 + by * 0.4, 21, WHITE, INK, 5), cx - 112, cy + 86, seg(t, t0 + 0.08, t0 + 0.26))
    big = (f'<ellipse cx="{cx + 8}" cy="{cy + 8}" rx="110" ry="88" fill="{INK}"/>'
           f'<ellipse cx="{cx}" cy="{cy}" rx="110" ry="88" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>')
    big += rot(T(cx, cy + 44, '?', 124, fill=BLUE), cx, cy, 7 * math.sin(TAU * t * 0.9))
    s += pop(shift(big, 0, by), cx, cy, seg(t, t0 + 0.16, t0 + 0.42))
    if a < 1:
        s = scale(fade(s, a), cx, cy, 1 + 0.25 * (1 - a))
    return s


# ---------------------------------------------------------------------------------------------
# Ledger
# ---------------------------------------------------------------------------------------------
@functools.lru_cache(None)
def _state(name):
    s = open(os.path.join(F.STATES, f'ledger-{name}.svg')).read()
    inner = re.sub(r'^<svg[^>]*>', '', s).rsplit('</svg>', 1)[0]
    return re.sub(r'<title>.*?</title>', '', inner)


_ROOT = re.compile(r'(data-p="root" transform=")translate\(([-\d.]+) ([-\d.]+)\)')
_TORSO = re.compile(r'(data-p="torso" transform=")rotate\(([-\d.]+) 120 198\) translate\(120 222\) scale\(([\d.]+) ([\d.]+)\)')
_EYES = re.compile(r'(data-p="eyes" transform=")translate\(([-\d.]+) ([-\d.]+)\)')
_EYE = re.compile(r'(data-p="eye[LR]" transform="translate\([\d.]+ 110\) )scale\(1 ([\d.]+)\)')
_SHADOW = re.compile(r'(data-p="shadow"[^>]*?transform="translate\(120 236\) )scale\(([\d.]+)\)')
_LEG = {'L': re.compile(r'(data-p="legL" transform=")rotate\(([-\d.]+) 102 188\)'), 'R': re.compile(r'(data-p="legR" transform=")rotate\(([-\d.]+) 138 188\)')}


def rig(name, X, Y, sc, t=0.0, up=0.0, tilt=0.0, look=(0, 0), legs=(0, 0), sy=1.0, alive=1.0, blink=True):
    """A real rig state with its feet at (X, Y), kept alive through the rig's own channels: root hop (up, frame
    pixels), torso tilt and breathing, gaze, blink, legs. alive scales the idle layer (breathing and sway)."""
    s = _state(name)
    br = alive * 0.014 * math.sin(TAU * t / 1.7)
    sw = alive * 1.1 * math.sin(TAU * t / 2.9)
    sy = clamp(sy, 0.94, 1.06)
    if up:
        assert up >= 0
        s = _ROOT.sub(lambda m: f'{m.group(1)}translate({float(m.group(2)):.2f} {float(m.group(3)) - up / sc:.2f})', s, 1)
        s = _SHADOW.sub(lambda m: f'{m.group(1)}scale({max(0.55, 1 - up / sc / 90):.3f})', s, 1)
    s = _TORSO.sub(lambda m: (f'{m.group(1)}rotate({float(m.group(2)) + tilt + sw:.2f} 120 198) translate(120 222) '
                              f'scale({float(m.group(3)) * (1 - br * 0.4) / sy:.4f} {float(m.group(4)) * (1 + br) * sy:.4f})'), s, 1)
    if look != (0, 0):
        s = _EYES.sub(lambda m: f'{m.group(1)}translate({clamp(float(m.group(2)) + look[0], -3.4, 3.4):.2f} {clamp(float(m.group(3)) + look[1], -3.0, 3.0):.2f})', s, 1)
    if blink:
        b = blink_at(t)
        if b > 0:
            s = _EYE.sub(lambda m: f'{m.group(1)}scale(1 {1 - 0.92 * b:.3f})', s)
    for side, a in zip('LR', legs):
        if a:
            assert abs(a) <= 30
            s = _LEG[side].sub(lambda m: f'{m.group(1)}rotate({a:.1f} {102 if side == "L" else 138} 188)', s, 1)
    return f'<g transform="translate({X - 120 * sc:.2f} {Y - 222 * sc:.2f}) scale({sc})">{s}</g>'


def hops(t, starts, period=0.42, height=46):
    return sum(hop(t, t0, period, height, 1) for t0 in starts)


def land(t, starts, period=0.42):
    """Squash factor: stretch on the way up, squash on landing and in the crouch before the first hop."""
    k = 1.0
    for t0 in starts:
        k += 0.05 * bump(t, t0, period * 0.6) - 0.06 * bump(t, t0 + period - 0.02, 0.16)
    k -= 0.06 * bump(t, starts[0] - 0.14, 0.16)
    return clamp(k, 0.94, 1.06)


def back_ledger(X, Y, sc, tilt=0.0, armL=None, armR=None, legs=(0, 0)):
    """The straight back view (frames_a.Ledger) with the rig's hip swing added to its legs."""
    L = F.Ledger('back', X, Y, sc, rot=round(tilt, 2))
    b, f = L.draw(armL=armL, armR=armR, shadow=False)
    for lx, sx, a in zip((102, 138), (87.5, 123.5), legs):
        if abs(a) > 0.05:
            assert abs(a) <= 30, 'leg swing beyond the rig walk cycle'
            leg = (f'<line x1="{lx}" y1="186" x2="{lx}" y2="210" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
                   f'<rect x="{sx}" y="208" width="29" height="14" rx="7" fill="{INK}"/>')
            assert leg in b
            b = b.replace(leg, f'<g transform="rotate({a:.1f} {lx} 188)">{leg}</g>')
    return b + f


def shadow(x, y, rx, a=0.14):
    return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{rx * 0.135:.1f}" fill="{INK}" opacity="{a}"/>'


def mover(fx, fy, sc, tilt, legs, armL, armR, face, held='', opacity=1):
    return F.Mover.on_feet(fx, fy, sc, round(tilt, 2)).draw(tuple(round(a, 1) for a in legs), armL, armR, face, held, opacity)


def kick(ph, amp=24):
    """Front or back view steps: the left foot kicks out, then the right one (hip swing inside the rig limit)."""
    s = math.sin(ph)
    return (amp * max(0.0, s), -amp * max(0.0, -s))


# ---------------------------------------------------------------------------------------------
# A1  yellow: phones pop in, then the books and the door; Ledger walks up and takes the handle
# ---------------------------------------------------------------------------------------------
FL1, DX1, DT1 = 1560, 520, 560
HX1, HY1 = DX1 + 122, FL1 - 250
A1_END = (HX1 - 262, FL1 + 20, 2.9)                      # Ledger's place in the static frame
A1_DUR = 6.4
PH = ((926, 370, -4, 'Languages', 0.30), (926, 860, 3, 'Coding', 0.95), (926, 1350, -3, 'Science', 1.52))
A1_TURN = 3.67                                           # "but business ..."


@functools.lru_cache(None)
def a1_books():
    k = 1.2
    books = [(236, 78, EMER), (212, 66, CREAM), (228, 74, VIOLET), (200, 62, PINK), (224, 76, SUIT), (206, 64, ORANGE), (190, 70, TINT)]
    offs = [0, 12, -6, 14, 4, -8, 10]
    y = FL1 - 3
    out = []
    for (bw, bh, col), off in zip(books, offs):
        bw, bh = bw * k, bh * k
        x = 30 + off + (236 * k - bw) / 2
        y -= bh
        g = rrect(-bw / 2, -bh / 2, bw, bh, 9, col, INK, 5)
        g += rrect(bw / 2 - 40, -bh / 2 + 10, 30, bh - 20, 4, PAGES, INK, 3)
        g += line(-bw / 2 + 26, -bh / 2 + 7, -bw / 2 + 26, bh / 2 - 7, CREAM if col in (SUIT, VIOLET, PINK, EMER, ORANGE) else INK, 3, extra='opacity="0.6"')
        g += rrect(-bw / 2 + 54, -8, bw * 0.38, 16, 8, RULE if col in (CREAM, TINT) else CREAM, None)
        dust = rrect(-bw / 2 + 14, -bh / 2 - 6, bw * 0.55, 10, 5, DUST, None)
        out.append((x + bw / 2, y + bh / 2, g, dust))
        y -= 3
    return tuple(out), y


TUMBLE = ((-520, -700, -260), (380, -1500, 420), (-760, -900, -380), (240, -1750, 300), (-900, -1200, -460), (520, -1900, 520), (-300, -2200, -340))


def a1_pile(t, end, shake=0.0, tumble=None):
    """The dusty pile. shake: the attention beat. tumble: seconds since the books were knocked over (T1)."""
    books, top = a1_books()
    s = ''
    for i, (cx, cy, g, dust) in enumerate(books):
        if tumble is not None and tumble > 0:
            vx, vy, w = TUMBLE[i]
            u = max(0.0, tumble - 0.015 * (len(books) - i))
            s += F.group(g, cx + vx * u, cy + vy * u + 2600 * u * u, round(w * u, 1))
            continue
        dx = shake * 9 * math.sin(TAU * 5.5 * t + i * 2.1) * (0.4 + 0.1 * i)
        lift = shake * (2 + i) * 1.4
        s += shift(g + fade(shift(dust, 0, -lift * 2.5), 1 - 0.5 * shake), cx + dx, cy - lift)
    if tumble is None or tumble <= 0:
        for i, (dx, dy, r) in enumerate(((30, -40, 11), (80, -90, 8), (150, -54, 10), (216, -104, 8), (256, -34, 9), (120, -136, 6))):
            fx = 9 * wave(t, end, 2.1 + 0.3 * i, i) + shake * 16 * math.sin(i * 1.7)
            fy = 12 * wave(t, end, 1.6 + 0.25 * i, 2 * i) - shake * (30 + 9 * i)
            s += circle(34 + dx + fx, top + dy + fy, r * (1 + 0.35 * shake), DUST, None)
    return s


def a1_door(opened=0.0, rattle=0.0, inside=None, frame=True):
    """Door frame, the blue leaf (it narrows towards its hinge as it opens: flat, no perspective) and the handle."""
    s = ''
    if inside:
        s += rrect(DX1 - 172, DT1 + 28, 344, FL1 - DT1 - 31, 6, inside, None)
    leaf = rrect(DX1 - 172, DT1 + 28, 344, FL1 - DT1 - 31, 6, BLUE, INK, 5)
    leaf += rrect(DX1 - 136, DT1 + 66, 272, 380, 8, 'none', INK, 4, 'opacity="0.55"')
    leaf += rrect(DX1 - 136, DT1 + 490, 272, 450, 8, 'none', INK, 4, 'opacity="0.55"')
    leaf += rot(rrect(HX1 - 22, HY1 - 54, 44, 108, 12, CREAM, INK, 4), HX1, HY1 - 54, rattle)
    if frame:                                            # the white frame is a ring, so what is behind shows through
        a, b, c, d = DX1 - 200, DT1, DX1 + 200, FL1
        s2 = (f'<path fill-rule="evenodd" d="M{a} {b} H{c} V{d} H{a} Z M{DX1 - 172} {DT1 + 28} V{FL1 - 3} H{DX1 + 172} V{DT1 + 28} Z" '
              f'fill="{WHITE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    else:
        s2 = ''
    k = lerp(1, -0.3, opened)
    if abs(k) > 0.01:
        hx = DX1 - 172
        s2 += f'<g transform="translate({hx} 0) scale({k:.3f} 1) translate({-hx} 0)">{leaf}</g>'
    return s, s2


def a1_sign(t, on=1.0, k=1.0):
    """The sign over the door. on: the spark lines; k: the bump."""
    pulse = 0.5 + 0.5 * math.sin(TAU * 1.7 * t)
    s = sparks(DX1, 400, 300, 350, (-158, -168, -180, 168), WHITE, 8, on * (0.75 + 0.25 * pulse), 8 * pulse * on)
    s += sparks(DX1, 330, 100, 150, (-110, -90, -70), WHITE, 8, on * (0.75 + 0.25 * pulse), 8 * pulse * on)
    board = F.panel(DX1 - 270, 330, 540, 140, 24) + T(DX1, 421, 'Learning business', 56, maxw=500)
    posts = line(DX1 - 130, 470, DX1 - 130, DT1, INK, 6) + line(DX1 + 130, 470, DX1 + 130, DT1, INK, 6)
    return s + scale(board, DX1, 400, k) + posts


def _tile(x, y, txt, w, fill=WHITE, col=INK):
    return rrect(x, y, w, 40, 10, fill, INK, 3) + T(x + w / 2, y + 28, txt, 22, fill=col, check=False)


def a1_lessons(t, end):
    """The three tiny lessons, each moving a little; all equal to the static frame at t = end."""
    # languages: the word "books" hops into the gap and back
    u = loop(t, end, 2.2)
    m = ease(seg(u, 0.12, 0.30)) - ease(seg(u, 0.66, 0.84))
    lang = rrect(-84, -122, 110, 12, 6, RULE, None)
    lang += _tile(-88, -96, 'I', 40, EMER, WHITE) + _tile(-40, -96, 'read', 68, EMER, WHITE)
    lang += rrect(36, -96, 56, 40, 10, 'none', EMER, 3, 'stroke-dasharray="7 6"') + line(-88, -38, 88, -38, RULE, 4)
    lang += _tile(6, -14, 'blue', 70) + _tile(-52, 40, 'run', 62)
    lang += scale(rrect(-78, 108, 156, 34, 17, EMER, None), 0, 125, 1 + 0.08 * m)
    done = m > 0.97
    lang += _tile(lerp(-88, 22, m), lerp(-14, -96, m) - 22 * math.sin(math.pi * m), 'books', 84, EMER if done else WHITE, WHITE if done else INK)
    # coding: the lines type on one after another
    u = loop(t, end, 2.3)
    code = ''
    rows = ((0, 150, SUIT), (22, 120, VIOLET), (44, 96, PINK), (22, 132, VIOLET), (0, 90, SUIT))
    for i, (ind, ww, col) in enumerate(rows):
        if u < 0.10:
            g = 1.0
        elif u < 0.17:
            g = 0.0
        else:
            g = ease_out(seg(u, 0.17 + 0.13 * i, 0.28 + 0.13 * i))
        if g > 0.04:
            code += rrect(-84 + ind, -120 + i * 44, ww * g, 34, 9, col, INK, 3)
        if 0 < g < 1:
            code += rrect(-84 + ind + ww * g + 8, -116 + i * 44, 8, 26, 3, INK, None)
    code += scale(rrect(-78, 108, 156, 34, 17, VIOLET, None), 0, 125, 1 + 0.06 * bump(u, 0.82, 0.16))
    # science: the molecule turns a little and its atoms breathe
    a = math.radians(15 * wave(t, end, 2.4))
    pt = lambda x, y: (x * math.cos(a) - (y + 40) * math.sin(a), -40 + x * math.sin(a) + (y + 40) * math.cos(a))
    p1, p2, p3 = pt(-52, 28), pt(52, 28), pt(0, -104)
    k = 1 + 0.07 * wave(t, end, 1.2)
    mol = ''.join(line(0, -40, x, y, INK, 6) for x, y in (p1, p2, p3))
    mol += circle(0, -40, round(34 * k, 1), ORANGE, INK, 5) + circle(p1[0], p1[1], 22, CREAM, INK, 5) + circle(p2[0], p2[1], 22, CREAM, INK, 5)
    mol += circle(p3[0], p3[1], round(18 * (2 - k), 1), YEL, INK, 5) + rrect(-78, 108, 156, 34, 17, ORANGE, None)
    return lang, code, mol


def a1_phones(t, end, dx=0.0):
    s = ''
    inners = a1_lessons(t, end)
    for i, ((cx, cy, r, label, t0), inner) in enumerate(zip(PH, inners)):
        p = seg(t, t0, t0 + 0.34)
        if p <= 0:
            continue
        cx += dx * (1 + 0.25 * i)
        bob = 6 * math.sin(TAU * (t - end) / 1.9) * math.cos(i * 0.9) + 6 * (1 - math.cos(TAU * (t - end) / 1.9)) * 0.5 + 18 * bump(t, 2.5 + 0.14 * i, 0.4)
        tilt = r + 1.6 * wave(t, end, 2.6, i * 1.3)
        body = (rrect(-104, -157, 224, 330, 30, INK, None) + rrect(-112, -165, 224, 330, 30, WHITE, INK, 5) + rrect(-30, -150, 60, 10, 5, INK, None) + inner)
        mk = 0.5 + 0.5 * math.sin(TAU * 1.5 * t + i)
        marks = (path(f'M{cx - 150 - 6 * mk:.1f} {cy - 110} q-16 30 0 60', stroke=WHITE, sw=7) +
                 path(f'M{cx - 172 - 12 * mk:.1f} {cy - 96} q-10 16 0 32', stroke=WHITE, sw=7))
        s += pop(fade(marks, 0.55 + 0.45 * mk) + F.group(body, cx, cy - bob, round(tilt, 2)), cx, cy, p, rot0=12)
        s += pop(T(cx, cy + 230, label, 42, check=not dx), cx, cy + 216, seg(t, t0 + 0.12, t0 + 0.4))
    return s


def a1_ledger(t, end):
    X1, Y1, sc = A1_END
    X0, Y0 = 610, 2096                                    # he starts low in the frame, looking up at the phones
    wk = smooth(seg(t, 3.55, 5.45))
    x, y = bez((X0, Y0), (620, 1880), (400, 1800), (X1, Y1), wk)
    walking = 1 if 3.55 < t < 5.45 else 0
    ph = TAU * 3.2 * (t - 3.55)
    legs = tuple(a * walking for a in kick(ph, 22))
    y -= 12 * abs(math.sin(ph)) * walking
    pre = 1 - seg(t, 3.3, 3.6)                            # before the walk: he bobs and hops when a phone pops
    y -= pre * (hops(t, [p[4] + 0.06 for p in PH], 0.3, 34) + 6 * math.sin(TAU * t / 1.05))
    tilt = keys(t, [(0, 0), (0.3, 4), (2.9, 4), (3.35, -5), (3.6, -3), (5.45, -1.5), (5.75, 0)])
    tilt += 2.2 * math.sin(ph) * walking + pre * 1.5 * math.sin(TAU * t / 1.6)
    # hand to the handle, then it rattles
    reach = ease(seg(t, 5.38, 5.82))
    rt = math.sin(math.pi * seg(t, 5.86, end)) * math.sin(TAU * 6 * (t - end))
    L = F.Ledger('back', x, y, sc, rot=round(tilt, 2))
    armR = None
    if reach > 0:
        tx, ty = L.r((HX1 - 2, HY1 + 6 + 5 * rt))
        hx_, hy_ = lerp2((186, 188), (tx, ty), reach)
        armR = {'hand': (hx_ + 14 * math.sin(math.pi * reach), hy_), 'front': True, 'bend': 1}
    k = 1 - 0.05 * bump(t, 5.84, 0.2) + pre * 0.02 * math.sin(TAU * t / 1.05)
    s = shadow(x, y + 40.6 + 12 * abs(math.sin(ph)) * walking, 122, 0.08)
    s += squash(back_ledger(x, y, sc, tilt, None, armR, legs), x, y, k)
    # speed lines: he has just walked up
    g = ease_out(seg(t, 4.5, 5.3))
    if g > 0:
        lx, ly = X1 - 236, FL1 + 60
        pulse = 1 + 0.12 * wave(t, end, 0.6)
        for i in range(3):
            ln = (90 - (i % 2) * 22) * g * pulse
            s += line(lx, ly + i * 34, lx - ln, ly + i * 34, WHITE, 9)
    # the handle rattles
    g = seg(t, 5.8, 6.0)
    if g > 0:
        d = 6 * wave(t, end, 0.3)
        s += pop(path(f'M{HX1 - 30} {HY1 - 96 - d:.1f} q30 -34 60 0', stroke=WHITE, sw=7) + path(f'M{HX1 - 16} {HY1 - 120 - 2 * d:.1f} q16 -18 32 0', stroke=WHITE, sw=7), HX1, HY1 - 100, g)
    return s, 5 * rt


def A1(t, dur):
    turn = seg(t, A1_TURN, A1_TURN + 0.3)
    s = F.floor(FL1 - 40, YEL_D)
    shake = bump(t, 4.85, 0.75)                           # "... stuck in books"
    s += a1_pile(t, dur, shake)
    led, rattle = a1_ledger(t, dur)
    inside, door = a1_door(0, rattle * 0.6)
    s += door
    s += a1_sign(t, turn, 1 + 0.07 * bump(t, A1_TURN, 0.34) + 0.012 * wave(t, dur, 1.3))
    s += a1_phones(t, dur)
    s += led
    return s, YEL


# ---------------------------------------------------------------------------------------------
# A2  green, accounting: hesitate, drag the block onto Debit, Correct, hop
# ---------------------------------------------------------------------------------------------
FL2 = 1790
M2 = (50, 400, 980, 770)
DT2 = FL2 - 228
TY2, TB2, TM2 = 690, 1000, 540
ZY2, BW2, BH2 = TY2 + 86, 200, 100
HOME2 = (540, 1076)
DEB2, CRE2 = (340, ZY2 + BH2 / 2), (740, ZY2 + BH2 / 2)
MX2, MY2 = 742, DT2 + 46
A2_DUR = 7.0
A2_GO, A2_DROP, A2_POP, A2_HOP = 3.38, 4.55, 5.98, (6.14, 6.60)
A2_HOP_P = (0.44, 0.80)                                   # the second hop peaks exactly at the end, as in the static frame


@functools.lru_cache(None)
def a2_monitor():
    return F.monitor_desk(*M2, DT2)


@functools.lru_cache(None)
def a2_qstrip():
    return F.qstrip(M2[0] + 40, M2[1] + 38, M2[2] - 80, 150, [('Cash sale of $500', 42, SLATE, 600), ('Does Cash go on Debit or Credit?', 46, INK, 700)])


def a2_block_pos(t):
    """(x, y, held, u_left): the block follows the cursor: two tries, then the real drag onto Debit."""
    L = lambda u: qb(HOME2, (330, 1080), DEB2, u)
    R = lambda u: qb(HOME2, (750, 1080), CRE2, u)
    if t < A2_GO:
        ur = keys(t, [(0.75, 0), (1.15, 0.52), (1.5, 0)]) + keys(t, [(2.45, 0), (2.68, 0.16), (2.92, 0)])
        ul = keys(t, [(1.62, 0), (1.98, 0.4), (2.34, 0)])
        if ur > 0:
            return (*R(ur), True, 0.0)
        return (*L(ul), True, 0.0)
    u = ease(seg(t, A2_GO, A2_DROP))
    return (*L(u), t < A2_DROP, u)


def a2_screen(t, q=1.0, block=True):
    s = a2_monitor()
    s += pop(a2_qstrip(), 540, 513, q, rot0=-3)
    bx, by, held, u = a2_block_pos(t)
    lit = seg(t, A2_DROP, A2_DROP + 0.25)
    tau = t - A2_DROP - 0.02                              # the T tips like a scale under the block, then levels: "watch them balance"
    tilt = -5.5 * math.exp(-1.9 * tau) * math.sin(TAU * 1.45 * tau) * (1 - seg(t, 5.7, 5.94)) if 0 < tau < 1.4 else 0.0
    s += T(TM2, TY2 - 22, 'Cash account', 46)
    g = line(140, TY2, 940, TY2, INK, 8) + line(TM2, TY2, TM2, TB2, INK, 8)
    g += T(340, TY2 + 58, 'Debit', 46, fill=SLATE) + T(740, TY2 + 58, 'Credit', 46, fill=SLATE)
    dash = 'stroke-dasharray="14 10"'
    near_r = clamp(1 - math.hypot(bx - CRE2[0], by - CRE2[1]) / 420) if t < A2_GO else 0
    near_l = clamp(1 - math.hypot(bx - DEB2[0], by - DEB2[1]) / 420) if not lit else 0
    g += scale(rrect(640, ZY2, BW2, BH2, 16, WHITE, SLATE, 5, dash), 740, ZY2 + 50, 1 + 0.06 * near_r)
    if lit <= 0:
        g += scale(rrect(240, ZY2, BW2, BH2, 16, WHITE, SLATE, 5, dash), 340, ZY2 + 50, 1 + 0.06 * near_l)
    else:
        glow = bump(t, A2_DROP, 0.5)
        g += pop(rrect(230, ZY2 - 10, BW2 + 20, BH2 + 20, 22, GREEN_T, GREEN, 6), 340, ZY2 + 50, 0.4 + 0.6 * lit)
        if glow > 0:
            g += fade(rrect(230 - 18 * glow, ZY2 - 10 - 18 * glow, BW2 + 20 + 36 * glow, BH2 + 20 + 36 * glow, 30, 'none', GREEN, 8), 1 - seg(t, A2_DROP, A2_DROP + 0.5))
    away = clamp(math.hypot(bx - HOME2[0], by - HOME2[1]) / 90)
    s += fade(rrect(HOME2[0] - BW2 / 2, HOME2[1] - 46, BW2, BH2 - 8, 16, 'none', SLATE, 5, dash), away)
    ga = 1 - seg(t, A2_GO, A2_GO + 0.25)
    s += ghost_q((HOME2[0] - 108, HOME2[1] - 20), (330, HOME2[1] - 30), (340, ZY2 + BH2 + 22), t, SLATE, ga)
    s += ghost_q((HOME2[0] + 108, HOME2[1] - 20), (750, HOME2[1] - 30), (740, ZY2 + BH2 + 22), t, SLATE, ga)
    s += qarrow((HOME2[0] - 108, HOME2[1] - 4), (330, HOME2[1]), (338, ZY2 + BH2 + 26), seg(u, 0.12, 0.98), BLUE, 8, 30)
    press = bump(t, 0.5, 0.26) + bump(t, A2_GO - 0.16, 0.24) + bump(t, A2_DROP, 0.22)
    cur = cursor(bx + 84, by + lerp(-6, 4, u), press)
    if held:
        s += rot(g, TM2, TY2, tilt)
        if block:
            wob = 2.5 * math.sin(TAU * 2.2 * t) * (1 if t < A2_GO else 0)
            s += rot(F.block(bx, by, w=BW2, h=BH2 - 8, fill=BLUE, lift=8), bx, by, wob) + cur
    else:
        k = 1 + 0.07 * bump(t, A2_DROP, 0.3) * math.cos(TAU * (t - A2_DROP) * 3)
        if block:
            g += scale(F.block(DEB2[0], DEB2[1], w=BW2, h=BH2 - 8, fill=BLUE), DEB2[0], DEB2[1], k)
        g += cur
        s += rot(g, TM2, TY2, tilt)
    s += popup(772, 958, 'Correct', 56, None, seg(t, A2_POP, A2_POP + 0.34), t, A2_DUR, col=GREEN, sw=7, corners=(1, 2), n1=44)
    return s, (bx, by, tilt)


def a2_desk(mdx=0.0, mdy=0.0, click=0.0, tap=-1):
    """Desk, keyboard, mouse mat, cable and mouse (moved by mdx, mdy while he drags)."""
    dt, FL = DT2, FL2
    s = rrect(108, FL - 110, 20, 84, 4, SUIT, None) + rrect(952, FL - 110, 20, 84, 4, SUIT, None)
    s += rrect(70, FL - 140, 940, 36, 8, '#D9B382', INK, 5)
    s += rrect(56, dt, 968, 92, 16, '#F2D7B0', INK, 5)
    kx, ky = 110, dt + 14
    s += rrect(kx, ky, 300, 64, 12, WHITE, INK, 4)
    for r in range(2):
        for c in range(9):
            s += rrect(kx + 12 + c * 31, ky + 10 + r * 24 + (3 if (r * 9 + c) == tap else 0), 24, 17, 4, SUIT if (r, c) != (1, 8) else BLUE, None)
    mx_, my_ = MX2 + mdx, MY2 + mdy
    s += rrect(690, dt + 10, 250, 70, 14, TINT, INK, 4)
    s += path(f'M{mx_ + 40:.1f} {my_ - 6:.1f} C {mx_ + 150:.1f} {my_ - 60:.1f} 960 {dt - 60} 760 {M2[1] + M2[3] - 8}', stroke=INK, sw=5)
    s += rrect(mx_ - 40, my_ - 26, 84, 50, 24, WHITE, INK, 5) + line(mx_ + 2, my_ - 26, mx_ + 2, my_ - 6, INK, 4)
    if click > 0:
        s += fade(line(mx_ + 70, my_ - 14, mx_ + 110, my_ - 14, INK, 5) + line(mx_ + 70, my_ + 8, mx_ + 100, my_ + 8, INK, 5), click)
    return s


A2_Q = lambda top: ((300, top + 40, 120, -16), (380, top - 44, 96, -4), (742, top + 6, 140, 12))
A2_TOP = FL2 + (34 - 222) * 2.3


def a2_ledger(t, bx, by, tiltT):
    """Back view at the desk: scratching and leaning while he hesitates, the mouse hand dragging, then both arms up."""
    sc, FL = 2.3, FL2
    h1, h2 = A2_HOP
    up = hop(t, h1, A2_HOP_P[0], 52, 1) + hop(t, h2, A2_HOP_P[1], 44, 1) + 9 * abs(math.sin(TAU * 1.45 * (t - A2_DROP))) * seg(t, A2_DROP + 0.1, A2_DROP + 0.3) * (1 - seg(t, 5.7, 5.9))
    tilt = keys(t, [(0, -5), (0.75, -5), (1.12, 4), (1.5, -3), (1.98, -8), (2.34, -4), (2.68, 2), (2.95, -5), (3.2, -7),
                    (3.5, -1), (A2_DROP, -3.5), (A2_DROP + 0.25, 0)]) + tiltT * 1.1
    tilt += 0.8 * math.sin(TAU * t / 1.3) * (1 - seg(t, h1 - 0.2, h1))
    mdx = clamp((bx - HOME2[0]) * 0.16, -34, 34) * (1 - seg(t, A2_DROP + 0.25, A2_DROP + 0.6))
    mdy = clamp((by - HOME2[1]) * 0.05, -10, 0) * (1 - seg(t, A2_DROP + 0.25, A2_DROP + 0.6))
    L = F.Ledger('back', 540, FL - up, sc, rot=round(tilt, 2))
    cheer = ease_out(seg(t, h1 - 0.02, h1 + 0.2))
    # left hand: scratches his head, then drops to the keyboard, then up
    scr = math.sin(TAU * 4.6 * t) * (1 if (t % 1.2) < 0.75 else 0.2)
    down = ease(seg(t, 3.05, 3.4))
    drum = 3 * abs(math.sin(TAU * 3.2 * t)) * seg(t, A2_DROP, A2_DROP + 0.2)
    kb = L.r((356, DT2 + 50 - drum))
    hl = lerp2((45 + 3.5 * scr, 93 - 1.5 * scr), kb, down)
    hl = lerp2(hl, (26, 104), cheer)
    hr = lerp2(L.r((MX2 + mdx, MY2 + mdy - 2)), (214, 104), cheer)
    wavey = 5 * math.sin(TAU * 3 * t) * cheer * (1 - seg(t, A2_DUR - 0.25, A2_DUR))
    armL = {'hand': (hl[0] - wavey * 0.5, hl[1] + wavey * 0.3), 'bend': -1}
    armR = {'hand': (hr[0] + wavey * 0.5, hr[1] + wavey * 0.3), 'bend': 1}
    k = 1 - 0.06 * bump(t, h1 - 0.15, 0.17) + 0.04 * bump(t, h1, 0.26) - 0.06 * bump(t, h1 + A2_HOP_P[0] - 0.03, 0.14) \
        - 0.035 * bump(t, A2_DROP + 0.05, 0.3)
    s = shadow(540, FL + 32, lerp(96, 74, clamp(up / 44)))
    body = squash(back_ledger(540, FL - up, sc, tilt, armL, armR), 540, FL - up, k)
    return body, s, (mdx, mdy), up


def a2_marks(t, up):
    """Question marks and the scratch squiggle while he hesitates; sparks, confetti and hop lines when he has it."""
    top = A2_TOP
    s = qmarks(A2_Q(top), t, A2_DUR, 0.12, 0.14, out=3.0)
    sq = (1 - seg(t, 3.0, 3.2)) * seg(t, 0.1, 0.3)
    if sq > 0:
        x, y = 540 + (46 - 120) * 2.3 - 40, FL2 + (70 - 222) * 2.3
        d = 5 * math.sin(TAU * 4.6 * t)
        s += fade(path(f'M{x + d:.0f} {y:.0f} q-14 14 0 28 q14 14 0 28', stroke=WHITE, sw=7), sq)
    h1 = A2_HOP[0]
    j = seg(t, h1, h1 + 0.3)
    if j > 0:
        topj = top - up
        pulse = wave(t, A2_DUR, 0.5)
        s += sparks(540, topj + 150, 205, 252, (-126, -106, -74, -54), WHITE, 9, back_out(j) * (1 + 0.12 * pulse), 6 * pulse)
        base = top - 44
        s += confetti([(250, base + 10, -20), (205, base + 110, 30), (150, base + 30, 60), (930, base - 30, 25), (968, base + 80, -35), (700, base - 96, 10)],
                      (540, top - 40), seg(t, h1, h1 + 0.6), t, A2_DUR)
        g = seg(up, 6, 30)
        for x in (478, 602):
            s += line(x - 22 * g, FL2 + 6, x + 22 * g, FL2 + 6, WHITE, 8) if g > 0 else ''
    return s


def a2_parts(t, q=None):
    q = seg(t, 0.05, 0.42) if q is None else q
    screen, (bx, by, tiltT) = a2_screen(t, q)
    body, sh, (mdx, mdy), up = a2_ledger(t, bx, by, tiltT)
    click = seg(t, A2_DROP, A2_DROP + 0.15)
    return dict(floor=F.floor(FL2 - 60, EMER_D), head=a2_header(), screen=screen, desk=a2_desk(mdx, mdy, click) + sh, led=body, marks=a2_marks(t, up))


@functools.lru_cache(None)
def a2_header():
    return F.header('ACCOUNTING', 'Journal entries')


def A2(t, dur):
    p = a2_parts(t)
    return p['floor'] + p['head'] + p['screen'] + p['desk'] + p['led'] + p['marks'], EMER


# ---------------------------------------------------------------------------------------------
# T1  the door opens, he leaps through at us, green takes over, he lands at the desk
# ---------------------------------------------------------------------------------------------
def T1(t, dur):
    cover = seg(t, 0.14, 0.60)                            # the green burst out of the doorway
    arrive = seg(t, 0.50, 0.88)                           # the accounting scene assembling
    s = ''
    if cover < 1:
        s += F.floor(FL1 - 40, YEL_D)
        opened = ease_out(seg(t, 0.0, 0.24))
        inside, door = a1_door(opened, 0, EMER_D)
        zoom = 1 + 5.5 * ease_in(seg(t, 0.2, 0.6))        # the camera goes through the doorway
        bx, by = DX1, 1090
        s += scale(inside, bx, by, zoom)
        led_back = ''
        if t < 0.34:                                      # back view: lets go, crouches, jumps into the doorway and is swallowed by the green
            X1, Y1, sc1 = A1_END
            g = ease_in(seg(t, 0.13, 0.32))
            k = 1 - 0.06 * bump(t, 0.0, 0.16)
            rel = 1 - ease(seg(t, 0.0, 0.1))
            L = F.Ledger('back', X1, Y1, sc1)
            armR = {'hand': lerp2((186, 188), L.r((HX1 - 2, HY1 + 6)), rel), 'front': True, 'bend': 1} if rel > 0.02 else None
            a = 20 * g
            body = scale(squash(back_ledger(X1, Y1, sc1, -3 * g, None, armR, (a, -a)), X1, Y1, k), X1, Y1, 1 - 0.5 * g)
            led_back = shift(body, (DX1 - X1) * g, -230 * g)
        if t >= 0.13:
            s += led_back
        r = 1900 * ease_in(cover) + 300 * ease_out(cover)
        if r > 4:
            a0 = 40 * t
            pts = [(bx + (r if i % 2 == 0 else r * 0.81) * math.cos(math.radians(i * 360 / 32 + 4 + a0)),
                    by + (r if i % 2 == 0 else r * 0.81) * math.sin(math.radians(i * 360 / 32 + 4 + a0))) for i in range(32)]
            s += F.wipe(pts, EMER, EMER_D, 26)
        s += scale(door, bx, by, zoom)
        u = max(0.0, t - 0.1)
        pile = a1_pile(A1_DUR, A1_DUR, 0, tumble=u)
        if t < 0.13:                                      # still in front of the door and the books while he lets go of the handle
            g0 = 1 - seg(t, 0.0, 0.1)
            s += pile + shadow(A1_END[0], A1_END[1] + 40.6, 122, 0.08) + led_back
            marks = sparks(DX1, 400, 300, 350, (-158, -168, -180, 168), WHITE, 8, g0) + sparks(DX1, 330, 100, 150, (-110, -90, -70), WHITE, 8, g0)
            marks += F.speed(A1_END[0] - 236, FL1 + 60, 3, 90 * g0, 34, WHITE, 9) if g0 > 0.3 else ''
            marks += path(f'M{HX1 - 30} {HY1 - 96} q30 -34 60 0', stroke=WHITE, sw=7) + path(f'M{HX1 - 16} {HY1 - 120} q16 -18 32 0', stroke=WHITE, sw=7)
            s += fade(marks, g0)
        else:
            s += pile
        k = ease_in(seg(t, 0.1, 0.55))
        board = F.panel(DX1 - 270, 330, 540, 140, 24) + T(DX1, 421, 'Learning business', 56, check=False)
        s += f'<g transform="translate({260 * k:.1f} {-620 * k:.1f}) rotate({38 * k:.1f} {DX1} 400)">{board}</g>'
        if t < 0.12:
            s += line(DX1 - 130, 470, DX1 - 130, DT1, INK, 6) + line(DX1 + 130, 470, DX1 + 130, DT1, INK, 6)
        s += a1_phones(A1_DUR, A1_DUR, dx=700 * ease_in(seg(t, 0.0, 0.32)))
    bg = YEL if cover < 1 else EMER
    # the accounting scene drops, rises and pops into place
    if arrive > 0:
        e = ease_out(arrive)
        p2 = a2_parts(0.0, q=0.0)
        s += shift(p2['floor'], 0, 260 * (1 - e))
        s += shift(p2['head'], 0, -460 * (1 - e))
        s += pop(p2['screen'], 540, 800, arrive)
        s += shift(p2['desk'], 0, 520 * (1 - e))
    # Ledger: back view crouches and jumps in; front view flies at us; back view lands at the desk
    if 0.28 <= t < 0.78:
        g = ease_out(seg(t, 0.28, 0.54))
        d = ease(seg(t, 0.56, 0.80))
        sc = lerp(lerp(1.3, 4.4, g), 2.3, d)
        cx, cy = lerp(lerp(DX1, 610, g), 540, d), lerp(lerp(1130, 1160, g), FL2 - 107 * 2.3, d)
        tilt = lerp(-7 * g, 0, d)
        a = lerp(20, 0, d)
        zs = seg(t, 0.3, 0.5) * (1 - seg(t, 0.56, 0.66))
        if zs > 0:
            s += fade(sparks(cx, cy, 118 * sc, 139 * sc, (-128, -112, -62, -48, 48, 62, 118, 132), WHITE, 10, 1, 60 * g), zs)
        m = F.Mover(cx, cy, sc, round(tilt, 2))
        s += m.draw((round(a, 1), round(-a, 1)), F.UPL, F.UPR, F.JOY)
    if t >= 0.78:
        g = seg(t, 0.78, dur)
        e = ease(g)
        tilt = -5 * e
        L = F.Ledger('back', 540, FL2, 2.3, rot=round(tilt, 2))
        armL = {'hand': lerp2((26, 104), (45, 93), e), 'bend': -1}
        armR = {'hand': lerp2((214, 104), L.r((MX2, MY2 - 2)), e), 'bend': 1}
        k = 1 - 0.06 * bump(t, 0.77, 0.12)
        s += shadow(540, FL2 + 32, 96) + squash(back_ledger(540, FL2, 2.3, tilt, armL, armR), 540, FL2, k)
    return s, bg


# ---------------------------------------------------------------------------------------------
# A3  orange, finance: think, drag the year slider, the curve and the coins grow, it doubles, joy
# ---------------------------------------------------------------------------------------------
FL3, LX3, SC3 = 1850, 250, 2.05
OX3, OY3, PPE3 = 200, 1100, 370 / 3000
X3 = lambda yr: OX3 + 44 + yr * 35
Y3 = lambda v: OY3 - v * PPE3
V3 = lambda yr: 1000 * 1.05 ** yr
RY3 = 1222
A3_DUR = 7.0
A3_GRAB, A3_D0, A3_D1 = 1.28, 1.48, 4.08
A3_JOY = 4.34
A3_HOPS = (A3_JOY, A3_JOY + 0.42)
TOP3 = FL3 - 188 * SC3


@functools.lru_cache(None)
def a3_static():
    s = F.panel(50, 612, 980, 700)
    s += T(OX3 + 4, 676, 'Savings', 40, anchor='start')
    s += path(f'M{OX3} {Y3(3000) - 14} V{OY3} H{X3(20) + 30}', sw=6)
    for v, lab in ((1000, '$1,000'), (2000, '$2,000')):
        s += line(OX3 - 12, Y3(v), OX3, Y3(v), INK, 5) + T(OX3 - 20, Y3(v) + 11, lab, 30, anchor='end', fill=SLATE)
    s += T(118, RY3 + 12, 'Year', 34, fill=SLATE)
    s += rrect(X3(0) - 16, RY3 - 14, X3(20) - X3(0) + 32, 28, 14, WHITE, INK, 5)
    for yr in (0, 5, 10, 15, 20):
        s += line(X3(yr), RY3 + 24, X3(yr), RY3 + 38, INK, 5) + T(X3(yr), RY3 + 72, str(yr), 30, fill=SLATE)
    return s


@functools.lru_cache(None)
def a3_head():
    return F.header('FINANCE', 'Compound interest')


@functools.lru_cache(None)
def a3_qcard():
    return F.qcard(400, 180, [('$1,000 grows at 5% a year', 42, SLATE, 600), ('In which year does it double?', 48, INK, 700)])


def a3_year(t):
    return 15 * smooth(seg(t, A3_D0, A3_D1))


def a3_chart(t):
    yr = a3_year(t)
    yi = int(yr + 1e-6)
    done = seg(t, A3_D1, A3_D1 + 0.3)
    s = a3_static()
    # the Double line: it flashes when the savings cross it
    fl = bump(t, A3_D1 - 0.1, 0.6)
    s += line(OX3, Y3(2000), X3(20) + 20, Y3(2000), GREEN, 5 + 5 * fl, dash='16 12', extra=f'stroke-dashoffset="{-18 * t:.1f}"')
    s += scale(T(X3(20) + 20, Y3(2000) - 16, 'Double', 32, anchor='end', fill=GREEN_D), X3(20) - 30, Y3(2000) - 28, 1 + 0.18 * fl)
    # coin stacks: year 0 from the start, then 5, 10 and 15 stack up as the slider reaches them
    for k in (0, 5, 10, 15):
        n = round(V3(k) / 125)
        ch = V3(k) * PPE3 / n
        g = 1.0 if k == 0 else seg(yr, k - 1.6, k)
        if g <= 0:
            continue
        land_ = bump(t, 0.0, 0.3) if k == 0 else 0.0           # the coin from the transition lands on the first stack
        shine = loop(t - 0.15 * k / 5, A3_DUR, 1.6)
        for j in range(n):
            pj = seg(g * n, j, j + 1)
            if pj <= 0:
                break
            dy = -(1 - ease_out(pj)) * 70
            lit = '#FFE89A' if abs(shine * (n + 8) - j) < 0.8 and g >= 1 and t < A3_DUR - 0.05 else YEL
            s += fade(rrect(X3(k) - 27 - 4 * land_, OY3 - 3 - ch * (j + 1) * (1 - 0.1 * land_) + dy, 54 + 8 * land_, ch, 7, lit, INK, 3), clamp(pj * 3))
    cv = lambda a, b: 'M' + ' L'.join(f'{X3(a + (b - a) * i / 40):.1f} {Y3(V3(a + (b - a) * i / 40)):.1f}' for i in range(41))
    pj = seg(t, A3_JOY + 0.3, A3_JOY + 1.3)
    if pj > 0:
        s += path(cv(15, 15 + 5 * ease(pj)), stroke=SLATE, sw=5, dash='3 13')
    if yr > 0.05:
        s += path(cv(0, yr), stroke=BLUE, sw=9)
    px, py = X3(yr), Y3(V3(yr))
    if fl > 0.05:
        s += fade(circle(px, py, 15 + 60 * seg(t, A3_D1 - 0.1, A3_D1 + 0.5), 'none', GREEN, 7), fl)
    ring = loop(t, A3_DUR, 1.1)
    s += fade(circle(px, py, 15 + 26 * ring, 'none', BLUE, 4), (1 - ring) * 0.7 * seg(t, 0.4, 0.7))
    s += circle(px, py, 15, BLUE, INK, 4)
    lab = f'Year {yi}: ${V3(yi):,.0f}'
    lw = F.tw(lab, 40) + 56
    bx = px + lerp(lw / 2 - 30, -70, ease(seg(yr, 0.3, 8)))
    by = py - 118
    tickk = 1 + 0.04 * (1 - (yr % 1)) ** 3 if 0 < yr < 15 else 1          # a small tick each time the year changes
    b = rrect(bx - lw / 2, by, lw, 74, 20, BLUE, INK, 5) + T(bx, by + 51, lab, 40, fill=WHITE)
    s += scale(b, bx, by + 37, tickk * (1 + 0.1 * bump(t, A3_D1, 0.3)))
    s += path(f'M{px - 16} {by + 72} L{px} {py - 22} L{px + 16} {by + 72} Z', fill=BLUE, stroke=None)
    # slider
    moved = seg(yr, 0, 1.2)
    if yr > 0:
        s += rrect(X3(0) - 11, RY3 - 9, X3(yr) - X3(0) + 11, 18, 9, BLUE, None)
        s += fade(circle(X3(0), RY3, 30, 'none', SLATE, 5).replace('/>', ' stroke-dasharray="10 8"/>'), moved)
    s += ghost_line(X3(0) + 52, RY3 - 52, X3(8), RY3 - 52, t, SLATE, 1 - seg(t, A3_D0, A3_D0 + 0.3))
    ax = X3(yr) - 50
    if ax > X3(0) + 80:
        s += F.arrow(X3(0) + 44, RY3 - 52, ax, RY3 - 52, BLUE, 9, head=30)
    press = bump(t, A3_GRAB - 0.1, 0.3) + bump(t, A3_D1 + 0.02, 0.24)
    hold = 1 if A3_GRAB < t < A3_D1 else 0
    wig = 5 * math.sin(TAU * 1.5 * t) * (1 - seg(t, A3_GRAB - 0.25, A3_GRAB)) * seg(t, 0.3, 0.6)
    kn = 1 + 0.12 * hold + 0.06 * wave(t, A3_DUR, 0.9) * (1 - hold) * done
    s += scale(circle(X3(yr), RY3, 32, WHITE, INK, 5) + circle(X3(yr), RY3, 13, BLUE, None), X3(yr), RY3, kn)
    s += cursor(X3(yr) + 20 + wig, RY3 + 2 + abs(wig) * 0.5, press)
    return s


def a3_ledger(t):
    """Think (watching the slider) -> joy with hops; the marks of each moment round him."""
    yr = a3_year(t)
    cut = A3_JOY
    up = hops(t, A3_HOPS, 0.42, 54)
    s = ''
    dance = seg(t, A3_HOPS[1] + 0.5, A3_HOPS[1] + 0.7) * (1 - seg(t, A3_DUR - 0.4, A3_DUR - 0.05))
    up += 16 * abs(math.sin(TAU * 1.15 * (t - A3_DUR))) * dance
    if t < cut:
        look = (lerp(0, 5.6, seg(yr, 0, 15)) + 2.2 * seg(t, 0.9, 1.3), 1.8 * seg(t, 0.9, 1.3))
        tilt = keys(t, [(0, 0), (0.9, 0), (1.3, 3), (A3_D1, 6), (cut - 0.1, 2)])
        sy = 1 - 0.06 * bump(t, cut - 0.16, 0.18)
        nod = 5 * abs(math.sin(TAU * 0.9 * t)) * (1 if t < A3_D0 else 0.4)
        s += rig('think', LX3, FL3, SC3, t, nod, tilt, look, sy=sy)
    else:
        sy = land(t, A3_HOPS, 0.42)
        tilt = 4 * math.sin(TAU * 1.15 * (t - A3_DUR)) * (1 - seg(t, A3_DUR - 0.5, A3_DUR))
        s += rig('joy', LX3, FL3, SC3, t, up, tilt, sy=sy, alive=1 - seg(t, A3_DUR - 0.4, A3_DUR))
    marks = qmarks(((LX3 - 170, TOP3 + 14, 92, -16), (LX3 - 70, TOP3 - 26, 112, 4), (LX3 + 150, TOP3 + 6, 80, 16)), t, A3_DUR, 0.25, 0.14, out=cut - 0.25)
    j = seg(t, cut, cut + 0.3)
    if j > 0:
        pulse = wave(t, A3_DUR, 0.5)
        marks += sparks(LX3, TOP3 + 150 - up, 215, 262, (-128, -106, -74, -52), WHITE, 9, back_out(j) * (1 + 0.12 * pulse), 6 * pulse)
        wide = min(136 * SC3 / 2 + 110, LX3 - 50)
        marks += confetti([(LX3 - wide, TOP3 - 20, -20), (LX3 - wide + 26, TOP3 + 120, 30), (LX3 + wide, TOP3 - 40, 25),
                           (LX3 + wide - 10, TOP3 + 110, -35), (LX3 - wide + 70, TOP3 - 70, 60)], (LX3, TOP3 - 30), seg(t, cut, cut + 0.6), t, A3_DUR)
    return s, marks


def a3_parts(t, q=None):
    q = seg(t, 0.05, 0.42) if q is None else q
    led, marks = a3_ledger(t)
    extra = thought(720, FL3 - 300, t, 0.42, A3_JOY - 0.2)
    extra += popup(762, FL3 - 260, 'Correct', 68, 'It doubles in year 15', seg(t, A3_JOY + 0.12, A3_JOY + 0.48), t, A3_DUR)
    return dict(floor=F.floor(FL3 - 60, ORANGE_D), head=a3_head(), q=pop(a3_qcard(), 540, 490, q, rot0=-3), chart=a3_chart(t), led=led, marks=marks, extra=extra)


def A3(t, dur):
    p = a3_parts(t)
    return p['floor'] + p['head'] + p['q'] + p['chart'] + p['led'] + p['marks'] + p['extra'], ORANGE


# ---------------------------------------------------------------------------------------------
# T2  the $500 block becomes a coin, he runs right with it, green wipes to orange
# ---------------------------------------------------------------------------------------------
def T2(t, dur):
    e = ease(seg(t, 0.10, 0.78))
    p2, p3 = a2_parts(A2_DUR), a3_parts(0.0, q=0.0)
    scr2, _ = a2_screen(A2_DUR, 1.0, block=False)
    s = p2['floor'] + shift(p2['head'] + scr2 + a2_desk(0, 0, 1) + fade(p2['marks'], 1 - seg(t, 0.0, 0.12)), -1300 * e, 0)
    edge = lerp(1420, -460, e)
    ex = lambda y: edge - 240 * (y / 1920 - 0.5)
    s += F.wipe([(ex(-100), -100), (W + 400, -100), (W + 400, H + 100), (ex(H + 100), H + 100)], ORANGE, ORANGE_D)
    fy = FL3 - 60
    s += path(f'M{ex(fy):.0f} {fy} H{W + 400} V{H + 100} H{ex(H + 100):.0f} Z', fill=ORANGE_D, stroke=None)
    s += shift(p3['head'] + p3['chart'], 1300 * (1 - e), 0)
    # Ledger: lands from his hop (back view), turns to us with a squash and runs
    cutA = 0.11
    fx, fyy = lerp(540, LX3, e), lerp(FL2, FL3, e)
    sc = lerp(2.3, SC3, e)
    run = seg(t, 0.12, 0.2) * (1 - seg(t, 0.74, 0.84))
    ph = t - 0.12
    stop = ease(seg(t, 0.74, 0.86))
    # the block leaves the screen, turns into a coin in the air and lands in his hands
    f = seg(t, 0.0, 0.30)
    R = 36 * sc
    m = F.Mover.on_feet(fx, fyy - 14 * abs(math.sin(TAU * 4.6 * ph)) * run, sc, round(10 * run, 2))
    hx_, hy_ = m.w((120, 182))
    coin_svg = ''
    held = ''
    toss = seg(t, 0.72, 0.90)
    if f < 1:
        g = ease(f)
        cx, cy = bez(DEB2, (360, 1250), (hx_ - 60, hy_ - 420), (hx_, hy_), g)
        ww, hh, rx = lerp(BW2, 2 * R, g), lerp(BH2 - 8, 2 * R, g), lerp(16, R, g)
        if g < 0.5:
            coin_svg = rrect(cx - ww / 2, cy - hh / 2, ww, hh, rx, BLUE, INK, 5) + T(cx, cy + 18, '$500', 52, fill=WHITE, check=False)
        else:
            coin_svg = rrect(cx - ww / 2, cy - hh / 2, ww, hh, rx, YEL, INK, 5) + T(cx, cy + 16, '$500', lerp(52, R * 0.56, g), check=False)
            coin_svg += fade(F.star4(cx + ww / 2, cy - hh / 2, 30), 1 - seg(g, 0.5, 0.9))
    elif toss <= 0:
        held = F.coin(120, 182, 36, '$500')
    else:
        g = ease(toss)
        cx, cy = bez((hx_, hy_), (hx_ - 90, hy_ - 330), (150, 1290), (X3(0), 1050), g)
        coin_svg = fade(rot(F.coin(cx, cy, lerp(R, 27, g), '$500' if g < 0.6 else '$'), cx, cy, 360 * g), 1 - seg(toss, 0.85, 1))
    if t < cutA + 0.03:
        up = 44 * (1 - ease_in(seg(t, 0, 0.09)))
        b = squash(back_ledger(540, FL2 - up, 2.3, 0, {'hand': (26, 104), 'bend': -1}, {'hand': (214, 104), 'bend': 1}), 540, FL2, 1 - 0.06 * bump(t, 0.07, 0.08))
        s += shadow(540, FL2 + 32, 96) + b
    cutB = 0.86
    if cutA + 0.03 <= t < cutB:
        catch = ease(seg(t, 0.2, 0.31)) * (1 - ease(seg(t, 0.72, 0.8)))
        aL = {'hand': lerp2((28, 106), (84, 180), catch), 'front': True, 'bend': -1}
        aR = {'hand': lerp2((212, 106), (156, 180), catch), 'front': True, 'bend': 1}
        face = {'brows': 2, 'mouth': 'smile', 'look': (3, 0)} if toss <= 0.3 else {'brows': 3, 'mouth': 'open', 'look': (0, -2.4)}
        legs = tuple(a * run for a in kick(TAU * 4.6 * ph, 26))
        body = m.draw(tuple(round(a, 1) for a in legs), aL, aR, face, held)
        k = 1 - 0.05 * bump(t, cutA, 0.1) - 0.05 * bump(t, 0.79, 0.08)
        s += shadow(fx + 6, fyy + 30, 78 * sc / 2.3)
        if run > 0.3:
            s += fade(F.speed(fx - 200, fyy - 330, 3, 110 + 30 * math.sin(TAU * 6 * t), 90, WHITE, 9), run)
            for i in range(3):
                u = (t * 5 + i / 3) % 1
                s += fade(circle(fx - 120 - 130 * u, fyy - 8 - 30 * u, 20 * (1 - u) + 5, WHITE, None), run * (1 - u))
        s += squash(body, fx, fyy, k)
    if t >= cutB:
        s += rig('think', LX3, FL3, SC3, 0.0, 0, 0, sy=1 - 0.06 * bump(t, cutB - 0.02, 0.055), blink=False, alive=0)
    s += coin_svg
    return s, EMER


# ---------------------------------------------------------------------------------------------
# A4  violet, statistics: drag z from 0 to 2.0 across the 1.96 line, click Reject H0, explanation, cheer
# ---------------------------------------------------------------------------------------------
FL4, LX4, SC4 = 1856, 250, 2.0
BL4, CX4, SG4, HH4, TP4 = 1096, 540, 148, 310, 634
FY4, CY4 = 790, 1222
XA4, XB4 = CX4 - 3.15 * SG4, CX4 + 3.15 * SG4
XL4, XR4 = CX4 - 1.96 * SG4, CX4 + 1.96 * SG4
CHX4 = 540 - (300 + 470 + 30) / 2
A4_DUR = 5.9
A4_GRAB, A4_CROSS, A4_CLICK, A4_POP = 1.26, 2.46, 3.22, 3.46
TOP4 = FL4 - 188 * SC4
hy4 = lambda x: BL4 - HH4 * math.exp(-((x - CX4) / SG4) ** 2 / 2)


@functools.lru_cache(None)
def a4_head():
    return F.header('STATISTICS', 'Hypothesis testing')


@functools.lru_cache(None)
def a4_qcard():
    return F.qcard(400, 180, [('z = 2.0, 5% level, two-tailed test', 42, SLATE, 600), ('Do we reject H_0?', 50, INK, 700)])


def _area(a, b, col):
    n = max(2, int((b - a) / 5))
    p = ' L'.join(f'{a + (b - a) * i / n:.1f} {hy4(a + (b - a) * i / n):.1f}' for i in range(n + 1))
    return path(f'M{a:.1f} {BL4} L{p} L{b:.1f} {BL4} Z', fill=col, stroke=None)


@functools.lru_cache(None)
def a4_static(curve=True):
    s = F.panel(40, 612, 1000, 580)
    s += rrect(XA4, TP4, XL4 - XA4, BL4 - TP4, 0, GREEN_T, None) + rrect(XL4, TP4, XR4 - XL4, BL4 - TP4, 0, RED_T, None)
    s += rrect(XR4, TP4, XB4 - XR4, BL4 - TP4, 0, GREEN_T, None)
    s += _area(XA4, XL4, GREEN) + _area(XL4, XR4, RED2) + _area(XR4, XB4, GREEN)
    if curve:
        s += path('M' + ' L'.join(f'{XA4 + (XB4 - XA4) * i / 120:.1f} {hy4(XA4 + (XB4 - XA4) * i / 120):.1f}' for i in range(121)), sw=7)
    s += line(XL4, BL4, XL4, hy4(XL4), INK, 5) + line(XR4, BL4, XR4, hy4(XR4), INK, 5)
    s += line(XA4 - 10, BL4, XB4 + 10, BL4, INK, 6)
    for x, lab in ((XL4, '−1.96'), (CX4, '0'), (XR4, '1.96')):
        s += line(x, BL4, x, BL4 + 16, INK, 5) + T(x, BL4 + 58, lab, 38)
    s += T((XA4 + XL4) / 2, TP4 + 48, 'Reject H_0', 31, fill=GREEN_D, maxw=XL4 - XA4)
    s += T((XR4 + XB4) / 2, TP4 + 48, 'Reject H_0', 31, fill=GREEN_D, maxw=XB4 - XR4)
    s += T(CX4, TP4 + 58, 'Do not reject H_0', 46, fill=RED_D)
    return s


def a4_z(t):
    """The marker: a first pull to 1.7, a short stop, then the push over 1.96 to 2.0."""
    return keys(t, [(A4_GRAB + 0.14, 0), (2.0, 1.7), (2.2, 1.72), (2.6, 2.0)], smooth)


def a4_chip(i, on, k=1.0):
    label, w_ = (('Reject H_0', 300), ('Do not reject H_0', 470))[i]
    x = CHX4 + (0 if i == 0 else 330)
    s = rrect(x + 8, CY4 + 8, w_, 92, 46, INK, None) + rrect(x, CY4, w_, 92, 46, GREEN if on else WHITE, INK, 5)
    if on:
        s += circle(x + 50, CY4 + 46, 24, WHITE, INK, 4) + path(f'M{x + 39} {CY4 + 47} L{x + 47} {CY4 + 56} L{x + 62} {CY4 + 38}', stroke=GREEN_D, sw=7)
        s += T(x + 86, CY4 + 61, label, 42, anchor='start', fill=WHITE, maxw=w_ - 100)
    else:
        s += circle(x + 50, CY4 + 46, 22, WHITE, INK, 4) + T(x + 86, CY4 + 61, label, 42, anchor='start', maxw=w_ - 100)
    return scale(s, x + w_ / 2, CY4 + 46, k) if k != 1 else s


def a4_chart(t, curve=True):
    z = a4_z(t)
    zx, z2 = CX4 + z * SG4, CX4 + 2.0 * SG4
    s = a4_static(curve)
    crossed = t >= A4_CROSS
    fl = bump(t, A4_CROSS, 0.55)
    if fl > 0:                                            # the crossing: the green tail lights up
        s += fade(rrect(XR4, TP4, XB4 - XR4, BL4 - TP4, 0, GREEN, None), 0.55 * fl)
        s += T((XR4 + XB4) / 2, TP4 + 48, 'Reject H_0', 31, fill=WHITE, check=False) if fl > 0.4 else ''
        s += fade(line(XR4, BL4, XR4, TP4, WHITE, 10), fl)
    moved = seg(z, 0.02, 0.3)
    if moved > 0:
        s += fade(line(CX4, BL4, CX4, FY4 + 40, WHITE, 6, dash='12 12') + circle(CX4, BL4, 13, WHITE, INK, 4), moved)
        if zx - 136 > CX4 + 60:
            s += F.arrow(CX4 + 20, FY4 + 40, zx - 136, FY4 + 40, INK, 9, head=30)
    s += ghost_line(zx + 132, FY4 + 40, z2 - 6, FY4 + 40, t, INK, (1 - seg(z, 0.0, 0.5)) if zx + 190 < z2 else 0)
    wig = 4 * math.sin(TAU * 1.4 * t) * (1 - seg(t, A4_GRAB - 0.25, A4_GRAB)) * seg(t, 0.3, 0.6)
    stuck = 3 * math.sin(TAU * 7 * t) * (1 if 2.0 < t < 2.2 else 0)
    mx_ = zx + wig * 0.5 + stuck
    green = (1 - seg(t, A4_POP + 0.2, A4_POP + 0.5)) if crossed else 0.0
    s += line(mx_, BL4, mx_, FY4 + 40, INK, 7) + circle(mx_, BL4, 14 + 5 * fl, INK, None)
    box = rrect(mx_ - 110 + 8, FY4 + 8, 220, 80, 18, INK, None) + rrect(mx_ - 110, FY4, 220, 80, 18, YEL, INK, 5)
    if green > 0:
        box += fade(rrect(mx_ - 110, FY4, 220, 80, 18, GREEN, INK, 5), green)
    lab = 'z = 0' if z < 0.05 else f'z = {z:.1f}'
    box += T(mx_, FY4 + 56, lab, 46, fill=WHITE if green > 0.5 else INK)
    hold = 1 if A4_GRAB < t < 2.62 else 0
    s += scale(box, mx_, FY4 + 40, 1 + 0.05 * hold + 0.16 * fl + 0.03 * wave(t, A4_DUR, 0.9) * seg(t, 2.8, 3.0))
    if fl > 0:
        e = seg(t, A4_CROSS, A4_CROSS + 0.55)
        s += fade(circle(XR4, hy4(XR4) - 10, 20 + 90 * e, 'none', WHITE, 9), 1 - e) + F.star4(XR4 + 6, TP4 + 110, 34 * fl)
    # zoom lens: 2.0 lies just beyond 1.96
    zp = seg(t, 2.64, 2.94)
    if zp > 0:
        ix, iy, ir = 934, 982, 94
        bob = 4 * wave(t, A4_DUR, 1.3)
        s += line(z2 + 6, BL4 - 14, lerp(z2 + 6, ix - 50, ease_out(zp)), lerp(BL4 - 14, iy + 62, ease_out(zp)), INK, 4)
        g = rrect(ix - ir, iy - ir, ir - 26, 2 * ir, 0, RED_T, None) + rrect(ix - 26, iy - ir, ir + 26, 2 * ir, 0, GREEN_T, None)
        g += line(ix - 26, iy - ir, ix - 26, iy + ir, INK, 5) + line(ix + 26, iy - ir, ix + 26, iy + ir, INK, 9)
        lens = f'<clipPath id="zoom"><circle cx="{ix}" cy="{iy}" r="{ir}"/></clipPath><g clip-path="url(#zoom)">{g}</g>' + circle(ix, iy, ir, 'none', INK, 6)
        lens += T(ix - 33, iy + 10, '1.96', 26, anchor='end') + T(ix + 37, iy + 10, '2.0', 28, anchor='start')
        s += pop(shift(lens, 0, bob), ix, iy, zp)
    # chips and the click
    on = t >= A4_CLICK
    s += a4_chip(1, False)
    hov = seg(t, A4_CLICK - 0.2, A4_CLICK)
    s += a4_chip(0, on, 1 + 0.04 * hov * (0 if on else 1) + 0.09 * bump(t, A4_CLICK, 0.3) - 0.05 * bump(t, A4_CLICK - 0.08, 0.1))
    # cursor: on the marker, then along a dotted path to the chip
    c0 = (z2 - 104, FY4 + 62)
    c1 = (CHX4 + 300 - 16, CY4 + 66)
    cc = (400, 1000)
    go = ease(seg(t, 2.72, 3.14))
    press = bump(t, A4_GRAB - 0.1, 0.3) + bump(t, 2.6, 0.2) + bump(t, A4_CLICK - 0.1, 0.24)
    if go <= 0:
        s += cursor(mx_ - 104 + wig * 0.5, FY4 + 62 + abs(wig) * 0.5, press)
    else:
        trail = 1 - seg(t, A4_CLICK + 0.1, A4_CLICK + 0.5)
        if trail > 0:
            pts = [qb(c0, cc, c1, go * i / 14) for i in range(15)]
            s += fade(path('M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts), stroke=SLATE, sw=6, dash='4 16'), trail)
        x, y = qb(c0, cc, c1, go)
        s += click_burst(x, y, seg(t, A4_CLICK, A4_CLICK + 0.35), WHITE)
        wob = 3 * wave(t, A4_DUR, 1.0) * seg(t, A4_CLICK + 0.4, A4_CLICK + 0.7)
        s += cursor(x + wob, y + wob * 0.6, press)
    return s


def a4_ledger(t):
    """confused -> aha when the marker crosses 1.96 -> cheer when the explanation pops."""
    z = a4_z(t)
    c1, c2 = A4_CROSS + 0.04, A4_POP
    hop_t = (c2, c2 + 0.42)
    up = hop(t, c1, 0.36, 30, 1) + hops(t, hop_t, 0.42, 56)
    s = ''
    dance = seg(t, hop_t[1] + 0.5, hop_t[1] + 0.7) * (1 - seg(t, A4_DUR - 0.4, A4_DUR - 0.05))
    up += 16 * abs(math.sin(TAU * 1.15 * (t - A4_DUR))) * dance
    if t < c1:
        look = (lerp(1.5, 3.4, z / 2) + 1.2 * math.sin(TAU * 0.7 * t), -1.6)
        tilt = keys(t, [(0, 0), (0.7, -2), (1.2, 2), (2.0, 5), (2.2, 6.5), (c1, 4)])
        nod = 4 * abs(math.sin(TAU * 0.8 * t))
        s += rig('confused', LX4, FL4, SC4, t, nod, tilt, look, sy=1 - 0.05 * bump(t, c1 - 0.15, 0.17))
    elif t < c2:
        sy = 1 + 0.05 * bump(t, c1, 0.2) - 0.05 * bump(t, c1 + 0.33, 0.14) - 0.06 * bump(t, c2 - 0.15, 0.17)
        look = (keys(t, [(c1, 3), (2.75, 3), (3.1, 1.5)]), keys(t, [(c1, 0), (2.75, 0), (3.1, 2.6)]))
        s += rig('aha', LX4, FL4, SC4, t, up, 3 * (1 - seg(t, c1, c1 + 0.4)), look, sy=sy)
    else:
        sy = land(t, hop_t, 0.42)
        tilt = 4 * math.sin(TAU * 1.15 * (t - A4_DUR)) * (1 - seg(t, A4_DUR - 0.5, A4_DUR))
        s += rig('cheer', LX4, FL4, SC4, t, up, tilt, sy=sy, alive=1 - seg(t, A4_DUR - 0.4, A4_DUR))
    marks = qmarks(((LX4 - 170, TOP4 + 14, 92, -16), (LX4 - 70, TOP4 - 26, 112, 4), (LX4 + 150, TOP4 + 6, 80, 16)), t, A4_DUR, 0.25, 0.14, out=c1 - 0.12)
    a = seg(t, c1, c1 + 0.2) * (1 - seg(t, c2 - 0.15, c2))
    if a > 0:                                             # aha: a ring of short lines over his head
        marks += fade(sparks(LX4, TOP4 + 40 - up, 150, 196, (-120, -100, -80, -60), YEL, 9, back_out(seg(t, c1, c1 + 0.25)), 10 * math.sin(TAU * 2 * t)), a)
    j = seg(t, c2, c2 + 0.3)
    if j > 0:
        pulse = wave(t, A4_DUR, 0.5)
        marks += sparks(LX4, TOP4 + 150 - up, 215, 262, (-128, -106, -74, -52), WHITE, 9, back_out(j) * (1 + 0.12 * pulse), 6 * pulse)
        wide = min(136 * SC4 / 2 + 110, LX4 - 50)
        marks += confetti([(LX4 - wide, TOP4 - 20, -20), (LX4 - wide + 26, TOP4 + 120, 30), (LX4 + wide, TOP4 - 40, 25),
                           (LX4 + wide - 10, TOP4 + 110, -35), (LX4 - wide + 70, TOP4 - 70, 60)], (LX4, TOP4 - 30), seg(t, c2, c2 + 0.6), t, A4_DUR)
    return s, marks


def a4_parts(t, q=None, curve=True):
    q = seg(t, 0.05, 0.42) if q is None else q
    led, marks = a4_ledger(t)
    extra = thought(720, FL4 - 290, t, 0.42, A4_CROSS - 0.05)
    extra += popup(762, FL4 - 260, 'Reject H_0', 66, '2.0 is beyond 1.96', seg(t, A4_POP, A4_POP + 0.36), t, A4_DUR)
    return dict(floor=F.floor(FL4 - 60, VIOLET_D), head=a4_head(), q=pop(a4_qcard(), 540, 490, q, rot0=-3), chart=a4_chart(t, curve), led=led, marks=marks, extra=extra)


def A4(t, dur):
    p = a4_parts(t)
    return p['floor'] + p['head'] + p['q'] + p['chart'] + p['led'] + p['marks'] + p['extra'], VIOLET


# ---------------------------------------------------------------------------------------------
# T3  he rides the growth curve up; it bends over into the bell curve; orange wipes to violet
# ---------------------------------------------------------------------------------------------
BIG = (1760, 900, 330, 1050)                              # the big curve of the storyboard frame: BL, CX, SG, HH


def T3(t, dur):
    f, df = F.bell_fn(*BIG)
    out = ease_in(seg(t, 0.0, 0.26))
    s = F.floor(FL3 - 60, ORANGE_D)
    if out < 1:
        p3 = a3_parts(A3_DUR)
        s += shift(p3['head'] + p3['q'] + p3['chart'] + p3['extra'] + p3['marks'], 0, 1750 * out)
    # violet comes in from the top right along a slanted edge
    wp = ease(seg(t, 0.22, 0.70))
    c = lerp(1500, -1900, wp)
    edge = lambda y: c + 0.677 * (y + 200)
    if wp > 0:
        s += F.wipe([(edge(-200), -200), (W + 400, -200), (W + 400, H + 200), (edge(H + 200), H + 200)], VIOLET, VIOLET_D)
        fy = FL4 - 60
        s += path(f'M{edge(fy):.0f} {fy} H{W + 400} V{H + 200} H{edge(H + 200):.0f} Z', fill=VIOLET_D, stroke=None)
    arrive = seg(t, 0.72, 0.98)
    morph = ease(seg(t, 0.60, 0.94))
    if arrive > 0:
        p4 = a4_parts(0.0, q=0.0, curve=morph >= 1)
        s += shift(p4['head'], 0, -460 * (1 - ease_out(seg(t, 0.66, 0.96))))
        s += pop(p4['chart'], 540, 900, arrive)
    # the big curve draws on under his feet, then shrinks into the bell curve of the next scene
    ride = ease(seg(t, 0.14, 0.56))
    xr = lerp(250, 840, ride)
    tip = lerp(-20, 250, ease_out(seg(t, 0.02, 0.16))) if t < 0.14 else xr + 40
    BLm, CXm, SGm, HHm = (lerp(a, b, morph) for a, b in zip(BIG, (BL4, CX4, SG4, HH4)))
    fm = lambda x: BLm - HHm * math.exp(-((x - CXm) / SGm) ** 2 / 2)
    if morph <= 0:
        for i, x in enumerate((140, 300, 460)):
            g = seg(tip, x, x + 120)
            n = int((1760 - f(x) - 20) // 22 * ease_out(g))
            s += F.coin_stack(x, 1760 + 3, n) if n > 0 else ''
        over = seg(t, 0.44, 0.60)
        if over > 0:
            s += path(f'M{F.fpts(f, 840, lerp(840, W + 20, over), 30)}', stroke=WHITE, sw=9, dash='18 18')
        s += path(f'M{F.fpts(f, -20, tip)}', stroke=INK, sw=22) + path(f'M{F.fpts(f, -20, tip)}', stroke=BLUE, sw=11)
        if t >= 0.14:
            s += circle(tip + 4, f(tip + 4), 15, BLUE, INK, 5)
    elif morph < 1:
        a, b = CXm - 3.15 * SGm, CXm + 3.15 * SGm
        s += path(f'M{F.fpts(fm, a, b, 120)}', stroke=INK, sw=lerp(22, 7, morph))
        if morph < 0.7:
            s += fade(path(f'M{F.fpts(fm, a, CXm - 0.18 * SGm, 60)}', stroke=BLUE, sw=lerp(11, 3, morph)), 1 - morph / 0.7)
    # Ledger: crouch (joy), hop on, ride, jump off down to his place, land (confused)
    if t < 0.07:
        s += rig('joy', LX3, FL3, SC3, A3_DUR, 0, 0, sy=1 - 0.06 * bump(t, 0.0, 0.09), alive=0, blink=False)
    elif t < 0.90:
        on = ease(seg(t, 0.06, 0.2))
        off = seg(t, 0.56, 0.88)
        sc = lerp(lerp(SC3, 2.4, on), SC4, ease(off))
        if off <= 0:
            fx = lerp(LX3, xr, on) if t < 0.2 else xr
            fy_ = lerp(FL3, f(fx) - 14, on) - 170 * math.sin(math.pi * on) * (1 if t < 0.2 else 0)
            tilt = lerp(0, max(-15, math.degrees(math.atan(df(fx))) * 0.45), on)
            arms = ({'hand': (24, 146), 'bend': -1}, {'hand': (213, 124), 'bend': 1})
            legs = (14, -14)
        else:
            g = ease(off)
            fx, fy_ = bez((840, f(840) - 14), (820, 330), (150, 560), (LX4, FL4), g)
            tilt = -15 + 15 * g - 26 * math.sin(math.pi * g)
            arms = (F.UPL, F.UPR)
            a = 20 * math.sin(math.pi * off)
            legs = (a, -a)
        if 0.2 < t < 0.56:
            for i, (dx, r) in enumerate(((-80, 30), (-125, 25), (-168, 20), (-200, 15))):
                u = (t * 4 + i * 0.25) % 1
                x = fx + dx - 90 * u
                s += fade(F.coin(x + 70, f(x) + 110 + (-dx) * 0.5 + 160 * u * u, r), 1 - u)
            s += sparks(fx + 40, fy_ - 250, 300, 350, (-150, -168, 174), WHITE, 9, 1, 30 * math.sin(TAU * 5 * t))
        if off > 0.05 and off < 0.95:
            s += fade(sparks(fx, fy_ - 200, 260, 330, (-60, -45, -30), WHITE, 9), math.sin(math.pi * off))
        k = 1 - 0.06 * bump(t, 0.86, 0.06)
        body = squash(mover(fx, fy_, sc, tilt, legs, arms[0], arms[1], F.JOY if off < 0.8 else {'mouth': 'oh', 'brows': 3}), fx, fy_, k)
        s += body
    else:
        s += rig('confused', LX4, FL4, SC4, 0.0, 0, 0, (1.5, -1.6), sy=1 - 0.06 * bump(t, 0.88, 0.1), blink=False, alive=0)
    return s, ORANGE


SCENES = {'A1': A1, 'T1': T1, 'A2': A2, 'T2': T2, 'A3': A3, 'T3': T3, 'A4': A4}


if __name__ == '__main__':
    import time
    DUR = {'A1': 6.4, 'T1': 0.9, 'A2': 7.0, 'T2': 0.9, 'A3': 7.0, 'T3': 1.0, 'A4': 5.9}
    for name, fn in SCENES.items():
        n = round(DUR[name] * 30)
        t0 = time.time()
        for i in range(n + 1):
            a = fn(i / 30, DUR[name])
            assert fn(i / 30, DUR[name]) == a, f'{name} is not a pure function of time'
            assert 'nan' not in a[0]
        print(f'{name}: {n} frames ok, {(time.time() - t0) / (2 * n) * 1000:.1f} ms a frame')
    for w_ in sorted(set(F.WARN)):
        print('   WARNING', w_)
