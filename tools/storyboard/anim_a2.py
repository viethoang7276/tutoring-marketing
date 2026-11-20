"""Demo video A, second half: T4, A5, T5, A6, T6, A7, T7, A8 as pure functions of time.

Each scene is fn(t, dur) -> (svg_inner, background). The layouts come from frames_a.py (same numbers), re-composed
here so every part can move. Front-facing Ledger is the real website rig state (frames_a.embed_state's source files),
with only the rig's own channels touched (blink, gaze, torso tilt, bookmark); travelling shots use frames_a.Mover;
at the monitor he is the straight back view (frames_a.Ledger('back', ...)).
"""
import functools, math, os, re
import frames_a as F
from anim_util import clamp, seg, ease, ease_out, ease_in, back_out, lerp, lerp2, bez, hop, wobble, pop, fade, shift, squash

PI2 = 2 * math.pi
W, H = F.W, F.H
D = {'T4': 1.0, 'A5': 4.9, 'T5': 0.9, 'A6': 6.5, 'T6': 1.0, 'A7': 3.4, 'T7': 0.9, 'A8': 4.6}   # as film_a.TIMELINE


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def tri(u):
    return max(0.0, 1 - abs(2 * u - 1)) if 0 < u < 1 else 0.0


def bell(t, t0, length):
    """0 -> 1 -> 0 smoothly over [t0, t0 + length]."""
    u = (t - t0) / length
    return math.sin(math.pi * u) ** 2 if 0 < u < 1 else 0.0


def grp(inner, tf, opacity=None):
    o = '' if opacity is None else f' opacity="{clamp(opacity):.2f}"'
    return f'<g transform="{tf}"{o}>{inner}</g>' if inner else ''


def scale_at(inner, cx, cy, k, rot=0.0):
    return grp(inner, f'translate({cx:.1f} {cy:.1f}) rotate({rot:.2f}) scale({k:.4f}) translate({-cx:.1f} {-cy:.1f})')


def pop_io(inner, cx, cy, t, t_in, t_out=None, d=0.3, rot0=0):
    """Pops in at t_in and (optionally) shrinks away at t_out."""
    if t_out is not None and t > t_out:
        p = 1 - ease_in(seg(t, t_out, t_out + 0.16))
        return '' if p <= 0.02 else grp(inner, f'translate({cx:.1f} {cy:.1f}) scale({p:.3f}) translate({-cx:.1f} {-cy:.1f})', p * 2)
    return pop(inner, cx, cy, seg(t, t_in, t_in + d), rot0)


def arrow_on(x1, y1, x2, y2, p, stroke=F.INK, sw=6, head=22, dash=None):
    """Arrow that draws on from its tail to its head."""
    p = clamp(p)
    if p <= 0.02:
        return ''
    xe, ye = lerp(x1, x2, p), lerp(y1, y2, p)
    if math.hypot(xe - x1, ye - y1) < head * 0.75:
        return F.line(x1, y1, xe, ye, stroke, sw)
    return F.arrow(x1, y1, xe, ye, stroke, sw, dash, head)


def ghost(x1, y1, x2, y2, pulse):
    """Dotted 'could go this way' arrow that breathes: pulse 0..1."""
    xe, ye = lerp(x1, x2, 0.72 + 0.28 * pulse), lerp(y1, y2, 0.72 + 0.28 * pulse)
    return fade(F.arrow(x1, y1, xe, ye, F.SLATE, 6, dash='4 16', head=24), 0.45 + 0.55 * pulse)


def cur(x, y, sc, press=0.0):
    s = F.cursor(x, y, sc * (1 - 0.14 * press))
    if press > 0.3:
        s += F.line(x - 16, y - 6, x - 30, y - 12, F.INK, 4) + F.line(x - 6, y - 16, x - 12, y - 30, F.INK, 4)
    return s


def trail(fn, t, col=F.SLATE):
    """A short dotted tail behind a moving cursor, so its path is visible."""
    x0, y0 = fn(t)
    s = ''
    for i in range(1, 7):
        x, y = fn(t - 0.045 * i)
        if math.hypot(x - x0, y - y0) > 14:
            s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{6 - i * 0.6:.1f}" fill="{col}" opacity="{0.6 - i * 0.08:.2f}"/>'
    return s


def half(c, ang):
    """Polygon of the half plane x*nx + y*ny >= c, n at ang degrees."""
    a = math.radians(ang)
    nx, ny = math.cos(a), math.sin(a)
    tx, ty, L = -ny, nx, 5000
    px, py = nx * c, ny * c
    return [(px + L * tx, py + L * ty), (px - L * tx, py - L * ty), (px - L * tx + L * nx, py - L * ty + L * ny), (px + L * tx + L * nx, py + L * ty + L * ny)]


def wiped(pts, col, band, inner, cid, bw=34):
    """The next colour coming in (frames_a.wipe) with the next layout showing only inside it."""
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ' Z'
    return F.wipe(pts, col, band, bw) + f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">{inner}</g>'


def sparks_p(cx, cy, r0, r1, angles, t, t_in, col=F.WHITE, sw=9, hz=1.6, t_end=0.0):
    """Spark lines that shoot out at t_in and then keep breathing (at rest when t == t_end)."""
    p = seg(t, t_in, t_in + 0.22)
    if p <= 0:
        return ''
    k = back_out(p)
    pulse = math.sin(PI2 * hz * (t - t_end))
    a = r0 + (r1 - r0) * (1 - k) * 0.6
    b = r0 + (r1 - r0) * k + 9 * pulse * p
    return F.sparks(cx, cy, a + 5 * pulse * p, b, angles, col, sw)


def confetti_p(pts, origin, t, t_in, t_end=0.0):
    """Confetti thrown from origin to pts, then fluttering a little (at rest when t == t_end)."""
    p = seg(t, t_in, t_in + 0.35)
    if p <= 0:
        return ''
    k = back_out(p, 1.2)
    out = []
    for i, (x, y, rot) in enumerate(pts):
        w = math.sin(PI2 * (0.9 + 0.13 * i) * (t - t_end))
        out.append((round(lerp(origin[0], x, k) + 5 * w * p, 1), round(lerp(origin[1], y, k) + 7 * w * p - 40 * math.sin(math.pi * p) * (1 - p), 1),
                    round(rot + 22 * w + 200 * (1 - p), 1)))
    return fade(F.confetti(out), seg(p, 0.3, 0.6))


def qmark_p(x, y, size, rot, t, t_in, t_out, i=0):
    if t < t_in or t > t_out + 0.2:
        return ''
    g = F.qmark(x, y + 7 * math.sin(PI2 * 1.3 * t + i * 1.9), size, rot + 7 * math.sin(PI2 * 0.9 * t + i * 2.3))
    return pop_io(g, x + size * 0.25, y - size * 0.35, t, t_in, t_out, 0.28, rot0=-30)


# ---------------------------------------------------------------------------------------------
# Ledger: the real rig states, alive
# ---------------------------------------------------------------------------------------------
@functools.lru_cache(None)
def _state(name):
    s = open(os.path.join(F.STATES, f'ledger-{name}.svg')).read()
    inner = re.sub(r'^<svg[^>]*>', '', s).rsplit('</svg>', 1)[0]
    inner = re.sub(r'<title>.*?</title>', '', inner)
    return inner.replace('opacity="0.080"', 'opacity="0"')          # the floor shadow is drawn by front(), so it stays on the floor in a hop


def st(name, X, Y, sc, blink=0.0, look=(0, 0), rot=0.0, bm=0.0):
    """A rig state with its feet at (X, Y); only rig channels are changed: blink, gaze, torso tilt, bookmark swing."""
    s = _state(name)
    if blink > 0.02:
        s = s.replace('scale(1 1.000)', f'scale(1 {1 - 0.92 * blink:.3f})')
    if look[0] or look[1]:
        s = re.sub(r'(data-p="eyes" transform="translate\()([-\d.]+) ([-\d.]+)\)',
                   lambda m: f'{m.group(1)}{clamp(float(m.group(2)) + look[0], -3.2, 3.2):.2f} {clamp(float(m.group(3)) + look[1], -2.8, 2.8):.2f})', s, count=1)
    if rot:
        s = re.sub(r'(data-p="torso" transform="rotate\()([-\d.]+) ', lambda m: f'{m.group(1)}{float(m.group(2)) + rot:.2f} ', s, count=1)
    if bm:
        s = s.replace('data-p="bm" transform="rotate(0 159 37)"', f'data-p="bm" transform="rotate({clamp(bm, -22, 22):.1f} 159 37)"')
    return f'<g transform="translate({X - 120 * sc:.2f} {Y - 222 * sc:.2f}) scale({sc})">{s}</g>'


def pose(t, sched):
    """sched: ((t0, name), ...) ascending. Returns (name, seconds since that pose began)."""
    name, t0 = sched[0][1], sched[0][0]
    for a, n in sched:
        if t >= a:
            name, t0 = n, a
    return name, t - t0


def switch_k(u):
    """Squash then stretch that sells a pose change (u = seconds since the change)."""
    return 1 - 0.055 * math.sin(PI2 * u / 0.3) * (1 - u / 0.3) if 0 <= u < 0.3 else 1.0


def blinkv(t, times):
    return max([tri((t - b) / 0.2) for b in times] or [0.0])


def front(name, X, FL, sc, t, hop_=0.0, k=1.0, rot=0.0, look=(0, 0), blinks=(), dx=0.0, calm=1.0):
    """Rig state standing at (X, FL): breathing, a slow sway, blinks, a bookmark that lags, his own floor shadow."""
    k *= 1 + 0.013 * calm * math.sin(PI2 * t / 1.5)
    rot += 1.0 * calm * math.sin(PI2 * t / 2.6)
    bmk = -6 * math.cos(PI2 * t / 2.6) * calm + hop_ * 0.2
    air = clamp(hop_ / 260)
    sh = (f'<ellipse cx="{X + dx:.1f}" cy="{FL + 14 * sc:.1f}" rx="{42 * sc * (1 - 0.45 * air):.1f}" ry="{6 * sc * (1 - 0.45 * air):.1f}" '
          f'fill="{F.INK}" opacity="{0.08 * (1 - 0.4 * air):.3f}"/>')
    return sh + squash(st(name, X + dx, FL - hop_, sc, blinkv(t, blinks), look, rot, bmk), X + dx, FL - hop_, k)


def back_ledger(X, Y, sc, rot=0.0, handL=None, handR=None, k=1.0, floor_y=None, shadow_rx=96.6):
    """Straight back view; hands in rig units (None = the rig's rest arm). floor_y places his shadow."""
    L = F.Ledger('back', X, Y, sc, rot)
    b, f = L.draw(armL={'hand': handL, 'bend': -1} if handL else None, armR={'hand': handR, 'bend': 1} if handR else None, shadow=False)
    s = ''
    if floor_y is not None:
        air = clamp((floor_y - Y) / 260)
        s = f'<ellipse cx="{X:.1f}" cy="{floor_y + 14 * sc:.1f}" rx="{shadow_rx * (1 - 0.3 * air):.1f}" ry="13.8" fill="{F.INK}" opacity="0.10"/>'
    return s + squash(b + f, X, Y, k), L


REST_L, REST_R, UP_L, UP_R = (54, 188), (186, 188), (26, 104), (214, 104)


# ---------------------------------------------------------------------------------------------
# A5  economics, market equilibrium
# ---------------------------------------------------------------------------------------------
A5FL = 1860
E1, SH = (450, 1010), 200


@functools.lru_cache(None)
def a5_bg(supply=True, guides=True):
    ox, oy, yt, xr = 160, 1244, 700, 990
    s = F.floor(A5FL - 60, F.PINK_D) + F.header('ECONOMICS', 'Market equilibrium')
    s += F.panel(50, 400, 980, 214) + F.qbadge(136, 507)
    s += F.panel(40, 646, 1000, 690)
    s += F.path(f'M{ox} {yt - 6} V{oy} H{xr + 4}', sw=7) + F.arrow_head(ox, yt - 26, -90, 28) + F.arrow_head(xr + 24, oy, 0, 28)
    s += F.T(ox + 26, yt + 6, 'Price', 38, anchor='start', fill=F.SLATE) + F.T(xr + 20, oy + 56, 'Quantity', 38, anchor='end', fill=F.SLATE)
    if guides:
        s += a5_guides()
    s += F.T(762, 720 + 26, 'Supply', 44, anchor='start')
    if supply:
        s += F.line(260, 1200, 740, 720, F.INK, 10)
    return s


@functools.lru_cache(None)
def a5_guides():
    ox, oy = 160, 1244
    return (F.line(ox, E1[1], E1[0], E1[1], F.SLATE, 5, dash='3 14') + F.line(E1[0], E1[1], E1[0], oy, F.SLATE, 5, dash='3 14')
            + F.T(ox - 20, E1[1] + 14, 'P_1', 40, anchor='end') + F.T(E1[0], oy + 56, 'Q_1', 40))


def a5_k(t):
    """How far the demand line has been dragged right (a wrong little pull to the left first)."""
    return -34 * bell(t, 1.0, 0.5) + SH * back_out(ease(seg(t, 1.78, 2.55)), 0.7)


def a5_cursor(t):
    k = a5_k(t)
    gy = lerp(860, 1040, ease(seg(t, 1.78, 2.55)))
    grab = (E1[0] + k + (gy - E1[1]) - 6, gy - 4)
    if t < 0.92:
        p = ease(seg(t, 0.38, 0.92))
        return bez((880, 1262), (700, 1240), (420, 1040), (294, 856), p)
    return grab


def a5(t, ledger=True):
    dur = D['A5']
    ox, oy = 160, 1244
    k = a5_k(t)
    s = a5_bg()
    # question card: the context chip, then the question
    ctx, cw = 'Coffee becomes more popular', F.tw('Coffee becomes more popular', 38) + 56
    s += pop(F.rrect(216, 434, cw, 66, 33, F.YEL, F.INK, 4) + F.T(216 + cw / 2, 480, ctx, 38), 216 + cw / 2, 467, seg(t, 0.08, 0.36), -4)
    qw = F.tw('What happens to demand?', 52)
    s += pop(F.T(216, 567.2, 'What happens to demand?', 52, 700, anchor='start'), 216 + qw / 2, 550, seg(t, 0.26, 0.56))
    s += scale_at(F.qbadge(136, 507), 136, 507, 1 + 0.07 * bell(t, 0.3, 0.4) + 0.05 * bell(t, 1.05, 0.4), 8 * math.sin(PI2 * 0.8 * t) * (1 - seg(t, 2.5, 2.8)))
    # the graph
    moved = clamp(abs(k) / 36)
    solved = seg(t, 2.5, 2.62)
    ex, ey = E1[0] + k / 2, E1[1] - k / 2
    if k > 2:                                                                          # guides follow the dot
        s += fade(F.line(ox, ey, ex, ey, F.SLATE, 5, dash='3 14') + F.line(ex, ey, ex, oy, F.SLATE, 5, dash='3 14'), clamp(k / 40))
    s += fade(F.line(220, 780, 640, 1200, F.PINK, 7, '18 16'), moved)                  # where the line was
    s += F.line(220 + k, 780, 640 + k, 1200, F.PINK, 11)
    s += F.T(626 + max(k, 0), 1164, 'Demand', 44, anchor='start', fill=F.PINK_D)
    for i, yy in enumerate((812, 1130)):                                               # the shift arrows draw on
        xa = E1[0] + (yy - E1[1])
        nud = 5 * math.sin(PI2 * 1.2 * (t - dur) + i) * seg(t, 3.0, 3.3)
        s += arrow_on(xa + 26 + nud, yy, xa + SH - 22 + nud, yy, seg(t, 2.3 + 0.12 * i, 2.66 + 0.12 * i), F.PINK_D, 9, 28)
    if k > 2:
        s += fade(F.circle(E1[0], E1[1], 13, F.WHITE, F.INK, 5), clamp(k / 40))
    if solved > 0:
        s += scale_at(F.circle(ex, ey, 20, F.GREEN, F.INK, 6), ex, ey, 1 + 0.5 * bell(t, 2.5, 0.3) + 0.06 * math.sin(PI2 * 1.5 * (t - dur)))
        s += sparks_p(ex, ey, 34, 62, (-150, -100, -40, 20), t, 2.52, F.GREEN, 6, t_end=dur) if t < 3.0 else ''
    else:
        s += F.circle(ex, ey, 18, F.WHITE, F.INK, 6)
    e2 = (E1[0] + SH / 2, E1[1] - SH / 2)
    s += pop(F.T(ox - 20, e2[1] + 14, 'P_2', 40, anchor='end'), ox - 50, e2[1], seg(t, 2.6, 2.85))
    s += pop(F.T(e2[0], oy + 56, 'Q_2', 40), e2[0], oy + 44, seg(t, 2.72, 2.97))
    gp = 4 * math.sin(PI2 * 1.4 * (t - dur)) * seg(t, 3.2, 3.5)
    s += arrow_on(ox + 24, E1[1] - 8 - gp, ox + 24, e2[1] + 8 - gp, seg(t, 2.66, 2.96), F.GREEN, 8, 24)
    s += arrow_on(E1[0] + 10 + gp, oy - 24, e2[0] - 10 + gp, oy - 24, seg(t, 2.8, 3.1), F.GREEN, 8, 24)
    # ghost arrows and the cursor
    cx, cy = a5_cursor(t)
    ga = seg(t, 0.9, 1.0) * (1 - seg(t, 1.7, 1.82))
    if ga > 0:
        gx, gy = cx + 6, cy + 4
        s += fade(ghost(gx + 40, gy, gx + 190, gy, 0.5 + 0.5 * math.sin(PI2 * 1.5 * t)) + ghost(gx - 40, gy, gx - 120, gy, 0.5 - 0.5 * math.sin(PI2 * 1.5 * t)), ga)
    if t > 0.36:
        press = seg(t, 0.94, 1.0) * (1 - seg(t, 1.5, 1.56)) + seg(t, 1.66, 1.72) * (1 - seg(t, 2.62, 2.7))
        s += trail(a5_cursor, t) + fade(cur(cx, cy, 1.4, press), seg(t, 0.36, 0.44))
    # thought bubble, then the answer
    s += pop_io(F.thought(720, A5FL - 290), 720, A5FL - 290, t, 0.5, 2.5)
    pk = 1 + 0.012 * math.sin(PI2 * 1.1 * (t - dur))
    s += pop(scale_at(F.popup(762, A5FL - 260, 'Correct', 68, 'Demand shifts right'), 762, A5FL - 260, pk), 762, A5FL - 260, seg(t, 2.95, 3.25), -5)
    if ledger:
        s += a5_ledger(t)
    F.WARN.clear()
    return s


A5_POSES = ((0, 'cheer'), (0.14, 'scratch'), (1.02, 'confused'), (1.6, 'watch'), (2.52, 'aha'), (2.92, 'joy'))


def a5_ledger(t):
    dur = D['A5']
    X, FL, sc = 250, A5FL, 2.0
    name, u = pose(t, A5_POSES)
    k = switch_k(u) * (0.94 + 0.06 * seg(t, 0, 0.12)) * (1 - 0.05 * bell(t, 2.78, 0.16))
    hp = hop(t, 2.92, 0.4, 64, 2) + 18 * bell(t, 2.52, 0.24) + (14 * abs(math.sin(math.pi * (t - dur) / 0.48)) if t > 3.94 else 0)
    rot, look, dx = 0.0, (0, 0), 0.0
    if name == 'scratch':
        rot = 1.4 * math.sin(PI2 * 4.6 * t) * seg(t, 0.3, 0.5)
        look = (1.5, -1.0)
    elif name == 'confused':
        dx, look = -8 * bell(t, 1.02, 0.56), (2.4 * math.sin(PI2 * 1.6 * (t - 1.02)), -1.5)
    elif name == 'watch':
        lean = ease(seg(t, 1.6, 1.9))
        rot, dx, look = 4 * lean, 14 * lean, (0.2 * lean, -2.2 - 0.4 * seg(t, 1.8, 2.5))
    top = FL - hp - 188 * sc
    s = ''
    if t < 2.7:                                                                        # the three question marks of the static frame
        for i, (qx, qy, size, r) in enumerate(((X - 170, top + 14, 92, -16), (X - 70, top - 26, 112, 4), (X + 150, top + 6, 80, 16))):
            s += qmark_p(qx, qy, size, r, t, 0.3 + 0.12 * i, 1.66 + 0.06 * i, i)
    s += front(name, X, FL, sc, t, hp, k, rot, look, (0.72, 1.42, 3.7), dx)
    wide = 136 * sc / 2 + 110
    wide = min(wide, X - 50)
    top0 = FL - 188 * sc
    s += sparks_p(X, top0 + 150 - hp * 0.5, 215, 262, (-128, -106, -74, -52), t, 2.94, t_end=dur)
    s += confetti_p([(X - wide, top0 - 20, -20), (X - wide + 26, top0 + 120, 30), (X + wide, top0 - 40, 25), (X + wide - 10, top0 + 110, -35),
                     (X - wide + 70, top0 - 70, 60)], (X, top0 + 150), t, 2.94, dur)
    return s


def A5(t, dur):
    return a5(t), F.PINK


# ---------------------------------------------------------------------------------------------
# T4  statistics -> economics
# ---------------------------------------------------------------------------------------------
@functools.lru_cache(None)
def a4_end():
    s = F.A4(True)[0]
    led = F.embed_state('cheer', 250, 1856, 2.0)
    marks = F.solved_marks(250, 1856 - 188 * 2.0, 136 * 2.0 / 2 + 110)
    assert led in s and marks in s
    F.WARN.clear()
    return s.replace(led, '').replace(marks, ''), marks


def T4(t, dur):
    old, marks = a4_end()
    q = ease(seg(t, 0.06, 0.4))
    sl = ease(seg(t, 0.36, 0.86))
    BL, CX, SG, HH = lerp(1096, 1900, q), lerp(540, 300, q) - 650 * sl, lerp(148, 300, q), lerp(310, 650, q)
    f, df = F.bell_fn(BL, CX, SG, HH)
    # the old scene slips away up and left while the pink comes in from the bottom right
    o = ease_in(seg(t, 0.1, 0.7))
    s = shift(old + fade(marks, 1 - seg(t, 0, 0.12)), -200 * o, -320 * o)
    n5 = (1 - ease_out(seg(t, 0.2, 0.86)))
    s += wiped(half(lerp(2080, -140, ease(seg(t, 0.16, 0.8))), 32.5), F.PINK, F.PINK_D, shift(a5_bg(False, False), 150 * n5, 210 * n5), 'w4')
    s += fade(a5_guides(), seg(t, 0.8, 0.98))
    # the bell grows under him, then its tail splits into the two lines of the market
    xa, xb = lerp(74, -60, q), lerp(1006, 1140, q)
    ba = seg(t, 0.04, 0.14) * (1 - seg(t, 0.62, 0.86))
    if ba > 0:
        s += fade(F.path(f'M{F.fpts(f, xa, xb, 70)}', sw=lerp(7, 12, q)), ba)
    r = ease(seg(t, 0.5, 0.94))
    la = seg(t, 0.5, 0.62)
    if la > 0:
        a0, a1 = (430, f(430)), (830, f(830))
        d0, d1 = lerp2(a0, (220, 780), r), lerp2(a1, (640, 1200), r)
        s0, s1 = lerp2(a1, (260, 1200), r), lerp2(a0, (740, 720), r)
        g = F.line(s0[0], s0[1], s1[0], s1[1], F.INK, 10)
        g += F.line(d0[0], d0[1], d1[0], d1[1], F.WHITE, 17, extra=f'opacity="{1 - r:.2f}"') + F.line(d0[0], d0[1], d1[0], d1[1], F.PINK, 11)
        s += fade(g, la)
    s += pop(F.circle(E1[0], E1[1], 18, F.WHITE, F.INK, 6), E1[0], E1[1], seg(t, 0.84, 1.0))
    # Ledger: crouch, leap onto the bell, ride its slope down, land where the next scene finds him
    X, FL = 250, 1856
    if t < 0.1:
        s += front('cheer', X, FL, 2.0, t, 0, 1 - 0.06 * ease(seg(t, 0, 0.1)), calm=0)
    else:
        fB, dfB = F.bell_fn(1900, 300, 300, 650)
        if t < 0.36:
            p = ease(seg(t, 0.1, 0.36))
            fx, fy = bez((250, 1856), (200, 1350), (300, fB(330) - 330), (330, fB(330) - 10), p)
            tilt = lerp(-10, 14, p)
            legs = (10 - 20 * p, -16 - 4 * p)
        else:
            fx = lerp(330, 250, sl)
            land = ease(seg(t, 0.84, 1.0))
            fy = lerp(f(fx) - 10, A5FL, land)
            tilt = min(30, math.degrees(math.atan(df(fx))) * 0.55) * (1 - land) + 5 * math.sin(PI2 * 3 * t) * (1 - land)
            legs = (-8 * (1 - land), -24 * (1 - land))
            for i in range(3):                                                         # speed lines streaming off behind him
                yy = fy - 330 - i * 70 + 40 * math.sin(PI2 * 4 * t + i)
                s += fade(F.line(fx - 250 - i * 26, yy - 60, fx - 150 - i * 26, yy, F.WHITE, 9), (1 - land) * seg(t, 0.38, 0.46))
        m = F.Mover.on_feet(fx, fy, 2.0, tilt)
        s += f'<ellipse cx="{fx:.1f}" cy="{A5FL + 28}" rx="{84 * seg(t, 0.8, 1.0):.1f}" ry="12" fill="{F.INK}" opacity="0.08"/>'
        s += m.draw(legs, F.UPL, F.UPR, F.JOY)
    F.WARN.clear()
    return s, F.VIOLET


# ---------------------------------------------------------------------------------------------
# A6  economics, IS-LM
# ---------------------------------------------------------------------------------------------
A6FL = 1790
LY1, LY2, GX = 770, 900, 900                                                           # LM before and after, where the cursor holds it


@functools.lru_cache(None)
def a6_bg():
    mx, my, mw, mh = 50, 400, 980, 770
    ox, oy, yt, xr = 180, 1070, 650, 960
    s = F.floor(A6FL - 60, F.PINK_D) + F.header('ECONOMICS', 'The IS-LM model')
    s += F.monitor_desk(mx, my, mw, mh, A6FL - 228)
    s += F.rrect(90, 438, 900, 150, 22, F.TINT, F.INK, 4)
    s += F.path(f'M{ox} {yt - 6} V{oy} H{xr + 4}', sw=7) + F.arrow_head(ox, yt - 24, -90, 26) + F.arrow_head(xr + 22, oy, 0, 26)
    s += F.T(ox + 24, yt + 8, 'Interest rate i', 34, anchor='start', fill=F.SLATE) + F.T(ox + 24, oy + 50, 'Output Y', 34, anchor='start', fill=F.SLATE)
    s += F.line(720, LY1, 720, oy, F.SLATE, 5, dash='3 14')
    s += F.T(720, oy + 50, 'Y_1', 40) + F.T(ox - 16, LY1 + 13, 'i_1', 40, anchor='end')
    return s


@functools.lru_cache(None)
def a6_desk():
    FL = A6FL
    dt = FL - 228
    s = F.rrect(108, FL - 110, 20, 84, 4, F.SUIT, None) + F.rrect(952, FL - 110, 20, 84, 4, F.SUIT, None)
    s += F.rrect(70, FL - 140, 940, 36, 8, '#D9B382', F.INK, 5) + F.rrect(56, dt, 968, 92, 16, '#F2D7B0', F.INK, 5)
    kx, ky = 110, dt + 14
    s += F.rrect(kx, ky, 300, 64, 12, F.WHITE, F.INK, 4)
    for r in range(2):
        for c in range(9):
            s += F.rrect(kx + 12 + c * 31, ky + 10 + r * 24, 24, 17, 4, F.SUIT if (r, c) != (1, 8) else F.BLUE, None)
    s += F.rrect(690, dt + 10, 250, 70, 14, F.TINT, F.INK, 4)
    return s


def a6_times(dur=None):
    """Key moments of A6, laid out from its length: hesitation, grab, two pulls, solved, hops (the last hop is caught at its top at dur)."""
    dur = dur or D['A6']
    th = dur - 3.5 * 0.485                                                             # first hop leaves the floor
    ts = th - 0.35                                                                     # the dot turns green
    return dict(n1=0.2 * dur, n2=0.31 * dur, g=0.4 * dur, d0=0.415 * dur, dm=0.51 * dur, d1=0.54 * dur, d2=ts - 0.05, ts=ts, th=th)


def a6_y(t):
    k = a6_times()
    pull = 0.55 * ease(seg(t, k['d0'], k['dm'])) + 0.45 * back_out(ease(seg(t, k['d1'], k['d2'])), 0.6)
    return LY1 - 30 * bell(t, k['n1'], 0.6) + 16 * bell(t, k['n2'], 0.5) + (LY2 - LY1) * pull


def a6_cursor(t):
    if t < 1.0:
        return bez((600, 1010), (760, 1000), (930, 900), (GX + 22, LY1 - 6), ease(seg(t, 0.3, 1.0)))
    return (GX + 22, a6_y(t) - 6)


def a6(t, ledger=True, row2=True):
    dur = D['A6']
    K = a6_times()
    N1, N2, G, D2, TS, TH = K['n1'], K['n2'], K['g'], K['d2'], K['ts'], K['th']
    ox, oy, xr = 180, 1070, 960
    y = a6_y(t)
    IS = lambda x: LY1 + (x - 720)
    s = a6_bg()
    # the question strip
    s += scale_at(F.qbadge(160, 513, 42), 160, 513, 1 + 0.07 * bell(t, 0.12, 0.4) + 0.06 * bell(t, N1, 0.4), 8 * math.sin(PI2 * 0.8 * t) * (1 - seg(t, TS, TS + 0.3)))
    r1 = 'The central bank cuts the rate'
    s += pop(F.T(224, 496.2, r1, 42, 600, anchor='start', fill=F.SLATE), 224 + F.tw(r1, 42) / 2, 482, seg(t, 0.1, 0.4))
    if row2:
        s += F.T(224, 560.6, 'What happens to output Y?', 46, 700, anchor='start')
    # the graph
    moved = clamp(abs(y - LY1) / 30)
    dn = clamp((y - LY1) / 40) * seg(t, G, G + 0.2)
    ex = 720 + (y - LY1)
    if dn > 0:
        s += fade(F.line(ex, y, ex, oy, F.SLATE, 5, dash='3 14'), dn)
    s += fade(F.line(ox, LY1, xr - 10, LY1, F.SLATE, 7, dash='18 16'), moved)
    s += F.line(ox, y, xr - 10, y, F.INK, 10)
    s += F.line(640, IS(640), 940, IS(940), F.BLUE, 10) + F.T(628, IS(640) + 6, 'IS', 50, anchor='end', fill=F.BLUE)
    s += F.rrect(ox + 14, y - 60, 470, 50, 0, F.WHITE, None)                          # keeps the label clear of the dashed old line as it passes
    s += F.T(ox + 24, y - 18, 'LM', 44, anchor='start')
    s += F.T(ox + 24 + F.tw('LM', 44) + 16, y - 20, 'set by the central bank', 28, 600, anchor='start', fill=F.SLATE)
    ap = 5 * math.sin(PI2 * 1.3 * (t - dur)) * seg(t, TS + 0.2, TS + 0.5)
    s += arrow_on(660, LY1 + 20 + ap, 660, LY2 - 20 + ap, seg(t, D2 - 0.55, D2), F.PINK, 14, 38)
    if dn > 0:
        s += fade(F.circle(720, LY1, 13, F.WHITE, F.INK, 5), dn)
    if t >= TS:
        s += scale_at(F.circle(ex, y, 20, F.GREEN, F.INK, 6), ex, y, 1 + 0.5 * bell(t, TS, 0.3) + 0.06 * math.sin(PI2 * 1.5 * (t - dur)))
        s += sparks_p(ex, y, 34, 60, (-140, -90, -40, 30), t, TS + 0.02, F.GREEN, 6, t_end=dur) if t < TS + 0.5 else ''
    else:
        s += F.circle(ex, y, 18, F.WHITE, F.INK, 6)
    s += pop(F.T(ox - 16, LY2 + 13, 'i_2', 40, anchor='end'), ox - 40, LY2, seg(t, TS, TS + 0.25))
    s += pop(F.T(850, oy + 50, 'Y_2', 40), 850, oy + 38, seg(t, TS + 0.1, TS + 0.35))
    gp = 4 * math.sin(PI2 * 1.4 * (t - dur)) * seg(t, TS + 0.5, TS + 0.8)
    s += arrow_on(732 + gp, oy - 24, 838 + gp, oy - 24, seg(t, TS + 0.14, TS + 0.5), F.GREEN, 8, 24)
    cx, cy = a6_cursor(t)
    ga = seg(t, 1.0, 1.1) * (1 - seg(t, G - 0.12, G))
    if ga > 0:
        s += fade(ghost(GX, y + 30, GX, y + 140, 0.5 + 0.5 * math.sin(PI2 * 1.5 * t)) + ghost(GX, y - 30, GX, y - 90, 0.5 - 0.5 * math.sin(PI2 * 1.5 * t)), ga)
    press = (seg(t, N1 - 0.06, N1) * (1 - seg(t, N1 + 0.6, N1 + 0.66)) + seg(t, N2 - 0.06, N2) * (1 - seg(t, N2 + 0.5, N2 + 0.56))
             + seg(t, G - 0.04, G + 0.02) * (1 - seg(t, TS + 0.02, TS + 0.1)))
    if t > 0.28:
        s += trail(a6_cursor, t) + fade(cur(cx, cy, 1.3, press), seg(t, 0.28, 0.36))
    pk = 1 + 0.014 * math.sin(PI2 * 1.1 * (t - dur))
    s += pop(scale_at(F.popup(400, 990, 'Correct', 48, col=F.GREEN, sw=6, corners=(0, 1), h=96, n1=30), 400, 990, pk), 400, 990, seg(t, TH + 0.12, TH + 0.4), -5)
    # desk, mouse (it moves with the cursor) and Ledger from straight behind
    FL = A6FL
    dt = FL - 228
    mdx, mdy = (cx - 922) * 0.09, (cy - 764) * 0.1
    mx_, my_ = 742 + mdx, dt + 46 + mdy
    s += a6_desk()
    s += F.path(f'M{mx_ + 40:.1f} {my_ - 6:.1f} C {mx_ + 150:.1f} {my_ - 60:.1f} 960 {dt - 60} 760 1162', stroke=F.INK, sw=5)
    mouse = F.rrect(mx_ - 40, my_ - 26 + 3 * press, 84, 50, 24, F.WHITE, F.INK, 5) + F.line(mx_ + 2, my_ - 26 + 3 * press, mx_ + 2, my_ - 6 + 3 * press, F.INK, 4)
    if not ledger:
        return s + mouse
    au = ease(seg(t, TH, TH + 0.16))                                                   # arms from the desk to the air
    hp = 0.0
    if t >= TH:
        hp = (72 if t < TH + 0.485 else 44) * abs(math.sin(math.pi * (t - TH) / 0.485))  # 3.5 hops, the last one caught at its top
    k = (1 - 0.06 * bell(t, TH - 0.2, 0.2)) * (0.95 + 0.05 * seg(t, 0, 0.15))
    k *= 1 + 0.012 * math.sin(PI2 * t / 1.5)
    rot = (-5 + 1.6 * math.sin(PI2 * 0.7 * t) + 3.5 * ease(seg(t, G, D2)) - 2.5 * bell(t, N1, 0.6) + 2 * bell(t, N2, 0.5)) * (1 - au)
    L = F.Ledger('back', 540, FL - hp, 2.3, rot)
    scr = seg(t, 0.25, 0.4) * (1 - seg(t, G - 0.25, G - 0.1)) * (1 - 0.7 * bell(t, N1 - 0.1, 0.8))   # he rubs his head while he hesitates
    hl0 = (45 + 3.5 * math.sin(PI2 * 4.6 * t) * scr, 93 + 2 * math.cos(PI2 * 4.6 * t) * scr + 40 * ease(seg(t, G - 0.15, G + 0.1)) * (1 - au))
    mr = L.r((mx_, my_ - 2))
    wave = 4 * math.sin(PI2 * 2.4 * (t - dur)) * au
    hl, hr = lerp2(hl0, (26 - wave, 104), au), lerp2(mr, (214 + wave, 104), au)
    s += f'<ellipse cx="540" cy="{FL + 32}" rx="{lerp(96, 74, au) * (1 - hp / 500):.1f}" ry="13" fill="{F.INK}" opacity="0.14"/>'
    s += mouse
    b, f = L.draw(armL={'hand': hl, 'bend': -1}, armR={'hand': hr, 'bend': 1}, shadow=False)
    s += squash(b + f, 540, FL - hp, k)
    top = FL - hp - 432.4
    if t < G + 0.4:
        for i, (qx, qy, size, r) in enumerate(((300, top + 40, 120, -16), (380, top - 44, 96, -4), (742, top + 6, 140, 12))):
            s += qmark_p(qx, qy, size, r, t, 0.22 + 0.13 * i, G + 0.05 * i, i)
        sq = scr * (0.5 + 0.5 * math.sin(PI2 * 4.6 * t))
        hx_, hy_ = L.w((46, 70))
        s += fade(F.path(f'M{hx_ - 40 - 6 * sq:.0f} {hy_:.0f} q-14 14 0 28 q14 14 0 28', stroke=F.WHITE, sw=7), scr)
    top1 = FL - 44 - 432.4
    s += sparks_p(540, top + 150, 205, 252, (-126, -106, -74, -54), t, TH + 0.06, t_end=dur)
    s += confetti_p([(250, top1 + 10, -20), (205, top1 + 110, 30), (150, top1 + 30, 60), (930, top1 - 30, 25), (968, top1 + 80, -35), (700, top1 - 96, 10)],
                    (540, top1 + 200), t, TH + 0.06, dur)
    if hp > 8:
        for x in (478, 602):
            s += F.line(x - 22, FL + 6, x + 22, FL + 6, F.WHITE, 8, extra=f'opacity="{clamp(hp / 30):.2f}"')
    if t > TS:                                                                         # click marks beside the mouse
        ca = seg(t, TS + 0.02, TS + 0.1)
        s += fade(F.line(mx_ + 70, my_ - 14, mx_ + 110, my_ - 14, F.INK, 5) + F.line(mx_ + 70, my_ + 8, mx_ + 100, my_ + 8, F.INK, 5), ca)
    F.WARN.clear()
    return s


def A6(t, dur):
    return a6(t), F.PINK


# ---------------------------------------------------------------------------------------------
# T5  market equilibrium -> IS-LM: push in to his face, the next question drops in
# ---------------------------------------------------------------------------------------------
@functools.lru_cache(None)
def a5_end():
    return a5(D['A5'], ledger=False)


@functools.lru_cache(None)
def a6_start():
    return a6(0.0, row2=False)                                                         # the question itself arrives as T5's card


def T5(t, dur):
    if t <= 0.0:
        return a5(D['A5']), F.PINK
    z = ease(seg(t, 0, 0.34))
    k = lerp(1, 5.5, z)
    px, py = 250, A5FL - 107 * 2.0
    cx, cy = lerp(px, 530, z), lerp(py, 1100, z)
    s = ''
    ra = seg(t, 0.14, 0.34)
    if ra > 0:                                                                         # flat burst turning slowly behind him
        g = ''
        for i in range(12):
            a0, a1 = math.radians(i * 30 - 8 + 40 * t), math.radians(i * 30 + 8 + 40 * t)
            g += F.path(f'M540 1000 L{540 + 2400 * math.cos(a0):.0f} {1000 + 2400 * math.sin(a0):.0f} L{540 + 2400 * math.cos(a1):.0f} {1000 + 2400 * math.sin(a1):.0f} Z',
                        fill=F.PINK_D, stroke=None)
        s += fade(g, ra)
    s += fade(grp(a5_end(), f'translate({cx:.1f} {cy:.1f}) scale({k:.3f}) translate({-px} {-py})'), 1 - seg(t, 0.16, 0.34))
    wide = seg(t, 0.14, 0.22)                                                          # the glad eyes open wide
    bob = 10 * math.sin(PI2 * 2.2 * t) * z
    m = F.Mover(cx, cy + bob, 2.0 * k, -5 * z + 1.5 * math.sin(PI2 * 1.8 * t) * z)
    face = F.JOY if wide < 0.5 else {'brows': 5 + 1.5 * math.sin(PI2 * 2.2 * t), 'mouth': 'grin', 'look': (1.5 * (1 - seg(t, 0.3, 0.45)), -2 - 0.8 * seg(t, 0.3, 0.45))}
    s += m.draw((0, 0), {'hand': (19, 155), 'bend': -1}, {'hand': (221, 155), 'bend': 1}, face)   # arms as in the joy state he comes from
    if wide >= 0.5:
        sp = back_out(seg(t, 0.2, 0.4))
        for i, ex in enumerate((102, 138)):
            lx, ly = face['look']
            x, y = m.w((ex - 2.6 + lx, 113.4 + ly))
            tw_ = 1 + 0.22 * math.sin(PI2 * 3 * t + i * 2)
            s += scale_at(F.star4(x, y, 30 * sp * tw_, F.WHITE, None), x, y, 1, 50 * t)
        for i, (sx, sy, r) in enumerate(((930, 700, 44), (840, 820, 22), (150, 880, 34))):
            p = back_out(seg(t, 0.24 + 0.05 * i, 0.44 + 0.05 * i))
            if p > 0.02:
                s += scale_at(F.star4(sx, sy, r * p * (1 + 0.25 * math.sin(PI2 * 2.5 * t + i * 2))), sx, sy, 1, 70 * t + 20 * i)
    # the next scene comes down over the close-up, the question card rides in front and settles into the monitor's strip
    u = ease(seg(t, 0.54, 0.9))
    if u > 0:
        s += wiped(half(-lerp(-120, 2060, u), -90), F.PINK, F.PINK_D, a6_start(), 'w5')
    dp = seg(t, 0.22, 0.48)
    if dp > 0:
        dy = -330 * (1 - back_out(dp, 1.4))
        card = fade(F.panel(60, -80, 960, 250) + F.qbadge(150, 84, 46), 1 - seg(u, 0.55, 0.95))
        card += F.T(224, 104, 'What happens to output Y?', 54, anchor='start')
        if u < 0.02:
            ln = seg(t, 0.4, 0.5) * (1 - seg(t, 0.5, 0.6))
            card += fade(F.line(300, 214, 300, 262, F.WHITE, 8) + F.line(540, 214, 540, 280, F.WHITE, 8) + F.line(700, 214, 700, 262, F.WHITE, 8), ln)
        sc_ = lerp(1, 46 / 54, u)
        s += grp(card, f'translate(224 {104 + dy + (560.6 - 104) * u:.1f}) scale({sc_:.4f}) translate(-224 -104)')
    F.WARN.clear()
    return s, F.PINK


# ---------------------------------------------------------------------------------------------
# A7  six lesson cards
# ---------------------------------------------------------------------------------------------
CW, CH, HD = 450, 340, 84
A7X, A7FL = 540, 1810
CARDS = ((296, 296, -4, F.EMER_D, 'Journal entries'), (788, 282, 4, F.ORANGE, 'Compound interest'), (290, 694, 3, F.VIOLET, 'Hypothesis testing'),
         (792, 686, -3, F.PINK, 'Supply and demand'), (296, 1092, -4, F.BLUE, 'Break-even point'), (788, 1082, 3, F.SUIT, 'Net present value'))
LAND = (0.30, 0.40, 0.76, 0.86, 1.22, 1.32)                                            # three waves
PERIOD = (1.0, 1.16, 0.92, 1.24, 0.84, 1.08)
OUTER = ((0,), (1,), (), (), (3,), (2,))


def _cur(x, y):
    return F.cursor(x, y, 0.8)


def card_body(j, b):
    """The small exercise inside card j; b in 0..1 is how far its control is pulled away from the static frame."""
    T, line, rrect, circle, path, arrow = F.T, F.line, F.rrect, F.circle, F.path, F.arrow
    if j == 0:
        dx, dy = -188 * b, -78 * b
        s = line(-190, -62, 190, -62, F.INK, 5) + line(0, -62, 0, 100, F.INK, 5)
        s += T(-95, -74, 'Debit', 26, check=False) + T(95, -74, 'Credit', 26, check=False)
        s += rrect(-160, -40, 130, 56, 10, F.WHITE, F.SLATE, 4, 'stroke-dasharray="9 7"') + rrect(30, -40, 130, 56, 10, F.WHITE, F.SLATE, 4, 'stroke-dasharray="9 7"')
        s += fade(F.curve_arrow(26, 70, -80, 80, -95, 30, F.SLATE, 4, '3 10', 16), 1 - 0.7 * b)
        s += rrect(34 + dx, 44 + dy, 130, 56, 10, F.INK, None) + rrect(28 + dx, 38 + dy, 130, 56, 10, F.BLUE, F.INK, 4)
        s += T(93 + dx, 77 + dy, '$500', 30, fill=F.WHITE, check=False) + _cur(142 + dx, 78 + dy)
        icon = line(-13, -9, 13, -9, F.INK, 5) + line(0, -9, 0, 14, F.INK, 5)
    elif j == 1:
        gy_ = lambda i: 30 - 19 * 1.026 ** i
        im = 70 - 44 * b
        n = int(im)
        cv = 'M' + ' L'.join(f'{-160 + 3.3 * i:.1f} {gy_(i):.1f}' for i in range(0, n + 1)) + f' L{-160 + 3.3 * im:.1f} {gy_(im):.1f}'
        s = path('M-180 -98 V30 H190', sw=5)
        for i in (12, 32, 52):
            if i <= im + 6:
                for jj in range(int((30 - gy_(i)) // 10)):
                    s += rrect(-160 + 3.3 * i - 18, 28 - 10 * (jj + 1), 36, 10, 5, F.YEL, F.INK, 2.5)
        s += path(cv, stroke=F.BLUE, sw=7) + circle(-160 + 3.3 * im, gy_(im), 9, F.BLUE, F.INK, 3)
        kx = 74 - 145 * b
        s += rrect(-180, 82, 370, 16, 8, F.WHITE, F.INK, 4) + rrect(-176, 86, kx + 176, 8, 4, F.BLUE, None) + circle(kx, 90, 18, F.WHITE, F.INK, 4) + circle(kx, 90, 8, F.BLUE, None)
        s += arrow(-70, 58, 40, 58, F.BLUE, 5, head=16) + _cur(kx + 10, 88)
        icon = T(0, 13, '$', 36, check=False)
    elif j == 2:
        hb = lambda x: 90 - 150 * math.exp(-(x / 62) ** 2 / 2)
        sg = lambda a, b_: ' L'.join(f'{a + (b_ - a) * i / 30:.1f} {hb(a + (b_ - a) * i / 30):.1f}' for i in range(31))
        zx = 134 - 112 * b
        s = path(f'M-190 90 L{sg(-190, -121)} L-121 90 Z', fill=F.GREEN, stroke=None) + path(f'M121 90 L{sg(121, 190)} L190 90 Z', fill=F.GREEN, stroke=None)
        s += path(f'M-121 90 L{sg(-121, 121)} L121 90 Z', fill=F.RED2, stroke=None)
        s += path(f'M{sg(-190, 190)}', sw=5) + line(-196, 90, 196, 90, F.INK, 5)
        s += line(zx, 90, zx, -20, F.INK, 5) + rrect(zx - 36, -62, 72, 44, 10, F.YEL, F.INK, 4) + T(zx, -30, 'z', 30, check=False)
        s += fade(arrow(40, -40, 88, -40, F.INK, 5, head=16), 1 - b) + _cur(zx + 16, -30)
        icon = path('M-16 10 C-6 10 -6 -12 0 -12 C6 -12 6 10 16 10', sw=4)
    elif j == 3:
        dx = -80 * b
        xs = dx * 0.5136
        s = path('M-170 -92 V96 H180', sw=5)
        s += line(-140, 76, 60, -80, F.INK, 6) + line(-150, -70, 20, 70, F.PINK, 4, '10 9') + line(-70 + dx, -70, 100 + dx, 70, F.PINK, 7)
        s += fade(arrow(-52, 18, 8, 18, F.PINK_D, 5, head=16), 1 - b) + circle(1.5 + xs, -34 - 0.78 * xs, 9, F.GREEN, F.INK, 3)
        s += T(72, -70, 'Supply', 24, anchor='start', check=False) + T(112, 62, 'Demand', 24, anchor='start', fill=F.PINK_D, check=False) + _cur(70 + dx, 30)
        icon = line(-13, -12, 13, 12, F.INK, 5) + line(-13, 12, 13, -12, F.PINK, 5)
    elif j == 4:
        s = T(0, -52, '$1,000 fixed costs ÷ $4 a unit', 26, check=False)
        for i, (tx, on) in enumerate((('150 units', False), ('250 units', True), ('400 units', False))):
            yy = -30 + i * 44
            g = rrect(-150, yy, 300, 36, 18, F.GREEN if on else F.WHITE, F.INK, 4) + T(-10 if on else 0, yy + 27, tx, 26, fill=F.WHITE if on else F.INK, check=False)
            if on:
                g += path(f'M64 {yy + 18} L72 {yy + 26} L86 {yy + 10}', stroke=F.WHITE, sw=5)
                g = scale_at(g, 0, yy + 18, 1 + 0.07 * b) + _cur(138 + 14 * b, yy + 22 + 12 * b)
            s += g
        icon = rrect(-14, 0, 8, 12, 1, F.INK, None) + rrect(-4, -6, 8, 18, 1, F.INK, None) + rrect(6, -13, 8, 25, 1, F.BLUE, None)
    else:
        s = line(-180, 10, 180, 10, F.INK, 5) + rrect(-160, 10, 44, 62, 4, F.RED2, F.INK, 4)
        for i, hgt in enumerate((40, 54, 66, 80)):
            hh = hgt * (1 - (0.14 + 0.1 * i) * b)
            s += rrect(-80 + i * 62, 10 - hh, 44, hh, 4, F.GREEN, F.INK, 4)
        kx = 60 - 76 * b
        s += rrect(-40, 78, 220, 14, 7, F.WHITE, F.INK, 4) + circle(kx, 85, 16, F.WHITE, F.INK, 4) + circle(kx, 85, 6, F.BLUE, None) + T(-64, 96, 'Rate', 24, anchor='end', fill=F.SLATE, check=False)
        s += arrow(140, 62, 92, 62, F.BLUE, 5, head=16) + _cur(kx + 6, 88)
        icon = T(0, 12, 'Σ', 34, check=False)
    return s, icon


def lesson(j, b, lines=1.0):
    col, topic = CARDS[j][3], CARDS[j][4]
    body, icon = card_body(j, b)
    x, y = -CW / 2, -CH / 2
    g = fade(F.pop_lines(x, y, CW, CH, F.WHITE, 7, 14, 36, OUTER[j]), lines)
    g += F.rrect(x + 10, y + 10, CW, CH, 26, F.INK, None) + F.rrect(x, y, CW, CH, 26, F.WHITE, F.INK, 5)
    g += F.path(f'M{x} {y + HD} V{y + 26} Q{x} {y} {x + 26} {y} H{-x - 26} Q{-x} {y} {-x} {y + 26} V{y + HD} Z', fill=col, stroke=F.INK, sw=5)
    g += F.circle(x + 50, y + HD / 2, 28, F.WHITE, F.INK, 4) + F.group(icon, x + 50, y + HD / 2)
    g += F.T(x + 92, y + HD / 2 + 12, topic, 34, anchor='start', fill=F.WHITE, check=False)
    return g + F.group(body, 0, 42)


def a7_cards(t, dy=0.0, dips=None):
    """t may be negative: the first wave is already on its way at the end of T6."""
    dur = D['A7']
    s = ''
    for j, (cx, cy, rot, col, topic) in enumerate(CARDS):
        p = seg(t, LAND[j] - 0.5, LAND[j])
        if p <= 0:
            continue
        side = -1 if cx < 540 else 1
        e = back_out(ease_out(p) if p < 1 else 1, 1.1) if p < 1 else 1
        e = 1 - (1 - p) ** 3 * (1 + 2.2 * p) if p < 1 else 1                           # eased arrival
        x0, y0 = cx + side * 760, cy + (260 if j < 2 else (-120 if j < 4 else -300))
        bounce = math.exp(-7 * (t - LAND[j])) * math.sin(PI2 * 3.2 * (t - LAND[j])) if t > LAND[j] else 0
        x, y = lerp(x0, cx, e), lerp(y0, cy, e) + 16 * bounce
        r = rot + side * 26 * (1 - e) + 3 * bounce * side
        b = math.sin(math.pi * (dur - t) / PERIOD[j]) ** 2 * seg(t, LAND[j] + 0.2, LAND[j] + 0.5) if t < dur else 0
        la = seg(t, LAND[j], LAND[j] + 0.12) * (0.75 + 0.25 * math.cos(PI2 * 1.2 * (t - dur)))
        g = lesson(j, b, la)
        if p < 1:                                                                      # speed lines behind a flying card
            g += fade(F.speed(side * (CW / 2 + 30), -60, 3, 110, 60, F.WHITE, 9, side), (1 - p) * 1.5)
        d = dips[j] if dips else 0
        s += grp(g, f'translate({x:.1f} {y + dy + d:.1f}) rotate({r:.2f}) scale({1 + 0.05 * bell(t, LAND[j] - 0.05, 0.3):.3f})')
    return s


def a7_ledger(t):
    dur = D['A7']
    au = ease(seg(t, 1.36, 1.5)) + (1 - ease(seg(t, 0.02, 0.24))) * (t < 1.0)          # arms: down from T6's landing, thrown up with the last wave
    half_up = 0.34 * bell(t, 0.24, 0.5) + 0.42 * bell(t, 0.7, 0.5)                     # a little "whoa" as each wave lands
    a = clamp(au + half_up)
    hp = 16 * bell(t, 0.3, 0.26) + 20 * bell(t, 0.76, 0.26) + hop(t, 1.38, 0.42, 62, 1)
    if t > 1.8:
        hp += 15 * abs(math.sin(math.pi * (t - dur) / 0.4)) * (0.55 + 0.45 * math.cos(PI2 * (t - dur) / 1.6) ** 2)
    k = (0.94 + 0.06 * seg(t, 0, 0.14)) * (1 - 0.06 * bell(t, 1.2, 0.18)) * (1 + 0.012 * math.sin(PI2 * t / 1.5))
    rot = -4 * bell(t, 0.14, 0.42) + 4 * bell(t, 0.3, 0.42) - 4 * bell(t, 0.6, 0.42) + 4 * bell(t, 0.78, 0.42) + 2.2 * math.sin(PI2 * 0.8 * (t - dur)) * seg(t, 1.8, 2.2)
    wave = 5 * math.sin(PI2 * 2.2 * (t - dur)) * seg(t, 1.5, 1.7)
    hl, hr = lerp2(REST_L, (UP_L[0] - wave, UP_L[1]), a), lerp2(REST_R, (UP_R[0] + wave, UP_R[1]), a)
    s, L = back_ledger(A7X, A7FL - hp, 2.3, rot, hl, hr, k, A7FL)
    top = A7FL - 432.4
    s += sparks_p(540, top + 150 - hp * 0.6, 205, 250, (-126, -106, -74, -54), t, 1.42, t_end=dur)
    s += confetti_p([(215, top + 60, -20), (250, top + 230, 30), (860, top + 50, 25), (840, top + 230, -35), (160, top + 180, 60), (915, top + 170, 10)],
                    (540, top + 200), t, 1.42, dur)
    return s


def a7(t, ledger=True):
    s = F.floor(1740, F.YEL_D) + a7_cards(t)
    if ledger:
        s += a7_ledger(t)
    F.WARN.clear()
    return s


def A7(t, dur):
    return a7(t), F.YEL


# ---------------------------------------------------------------------------------------------
# T6  IS-LM -> lesson cards: he jumps into the graph and rides the LM line down like a lift
# ---------------------------------------------------------------------------------------------
@functools.lru_cache(None)
def a6_end():
    return a6(D['A6'], ledger=False)


def T6(t, dur):
    if t <= 0.0:
        return a6(D['A6']), F.PINK
    yl = lerp(LY2, 1740, ease(seg(t, 0.3, 0.74))) + 24 * bell(t, 0.73, 0.16)           # the lift drops and lands with a small bump
    s = a6_end()
    yw = lerp(-140, LY2, ease(seg(t, 0.06, 0.36))) if t < 0.36 else yl                           # the yellow comes down and then travels with the line
    streaks = ''
    for i in range(7):                                                                 # the air rushing up past the lift
        x = 90 + i * 150 + (40 if i % 2 else 0)
        yy = (i * 397 - t * 2600) % 2100 - 200
        streaks += F.line(x, yy, x, yy + 120 + 40 * (i % 3), F.WHITE, 8, extra='opacity="0.75"')
    s += wiped(half(-yw, -90), F.YEL, F.YEL_D, fade(streaks, seg(t, 0.3, 0.4) * (1 - seg(t, 0.7, 0.8))) + a7_cards(t - dur), 'w6')
    fy = lerp(H + 40, 1740, ease(seg(t, 0.5, 0.8)))
    s += F.rrect(0, max(fy, yl), W, H, 0, F.YEL_D, None) if t > 0.5 else ''
    # the LM line: widens to the whole frame, drops, becomes the edge of the floor and is gone
    wd = ease(seg(t, 0.26, 0.44))
    gone = ease(seg(t, 0.8, 0.96))
    xa, xb = lerp(180, -30, wd), lerp(950, W + 30, wd)
    xa, xb = lerp(xa, 540, gone), lerp(xb, 540, gone)
    if gone < 0.98:
        s += F.line(xa, yl, xb, yl, F.INK, lerp(10, 13, wd))
    if t < 0.8:
        dx_ = 720 + (LY2 - LY1)
        s += fade(F.circle(dx_, yl, 20, F.GREEN, F.INK, 6), 1 - seg(t, 0.4, 0.6))
    # Ledger
    LX = 390
    if t < 0.28:                                                                       # still the back view: the hop becomes a leap into the screen
        p = seg(t, 0, 0.28)
        e = ease_out(p)
        x, y = bez((540, A6FL - 44), (540, 1380), (420, 760), (LX, LY2 - 4), ease(p))
        sc = lerp(2.3, 1.35, e)
        g, _ = back_ledger(x, y, sc, lerp(0, -8, math.sin(math.pi * p)), UP_L, UP_R)
        s += g + fade(F.sparks(x, y - 100 * sc, 150 * sc, 190 * sc, (60, 90, 120), F.WHITE, 8), p * (1 - p) * 4)
    elif t < 0.76:
        k = 1 - 0.06 * bell(t, 0.28, 0.14)
        fall = seg(t, 0.34, 0.7) * (1 - seg(t, 0.7, 0.76))
        m = F.Mover.on_feet(LX, yl - 8 - 14 * fall, 1.35, 4 * math.sin(PI2 * 2.6 * t))
        armL = {'hand': (24 + 4 * fall, 142 - 34 * fall), 'bend': -1}
        armR = {'hand': (216 - 4 * fall, 142 - 34 * fall), 'bend': 1}
        face = F.JOY if t > 0.36 else {'mouth': 'grin', 'brows': 4, 'look': (0, 2)}
        s += squash(m.draw((8 * fall, -8 * fall), armL, armR, face), LX, yl - 8, k)
        for dx in (-150, 150):
            la = seg(t, 0.36, 0.44) * (1 - seg(t, 0.66, 0.74))
            s += fade(F.line(LX + dx, yl - 420, LX + dx, yl - 300, F.WHITE, 8) + F.line(LX + dx * 0.72, yl - 500, LX + dx * 0.72, yl - 400, F.WHITE, 8), la)
    else:                                                                              # he hops off the line towards the camera and lands as the next scene's Ledger
        p = seg(t, 0.76, 1.0)
        x, y = lerp(LX, A7X, ease(p)), lerp(1732, A7FL, p) - 170 * math.sin(math.pi * p)
        sc = lerp(1.35, 2.3, ease(p))
        s += f'<ellipse cx="{x:.1f}" cy="{lerp(1750, A7FL + 32, p):.1f}" rx="{42 * sc * 0.8:.1f}" ry="{6 * sc * 0.8:.1f}" fill="{F.INK}" opacity="0.08"/>'
        if p < 0.45:
            s += F.Mover.on_feet(x, y, sc, -8 * p).draw((14, -14), F.UPL, F.UPR, F.JOY)
        else:
            if p < 0.62:
                s += F.sparks(x, y - 107 * sc, 150 * sc * 0.8, 200 * sc * 0.8, (-150, -30, 30, 150), F.WHITE, 8)
            g, _ = back_ledger(x, y, sc, 0, UP_L, UP_R)
            s += g
    F.WARN.clear()
    return s, F.PINK


# ---------------------------------------------------------------------------------------------
# A8  the website, the button
# ---------------------------------------------------------------------------------------------
A8FL, A8SC = 1800, 2.2
IX, IY, IW = 66, 172, 948
BY = IY + 706
BTN = (540, BY + 80)
CLICK = 2.55


@functools.lru_cache(None)
def _logo():
    s = F.embed_logo(540 - 320, IY + 136, 640)
    h = float(re.search(r'height="([\d.]+)"', s).group(1))
    return s, h


@functools.lru_cache(None)
def a8_bg():
    s = F.floor(A8FL - 70, F.BLUE_D) + F.monitor(44, 150, 992, 1030)
    s += F.rrect(IX, IY, IW, 100, 14, F.TINT, None) + F.rrect(IX, IY + 50, IW, 50, 0, F.TINT, None)
    for i, col in enumerate((F.RED, F.YEL, F.GREEN)):
        s += F.circle(IX + 54 + i * 44, IY + 50, 14, col, None)
    return s


A8_CHIPS = ((('Accounting', F.EMER_D), ('Finance', F.ORANGE)), (('Economics', F.PINK), ('Statistics', F.VIOLET)))
A8_IN = {'bar': 0.12, 'logo': 0.32, 'line': 0.58, 'chips': 0.8, 'btn': 1.2}


def a8_cursor(t):
    p = ease(seg(t, 1.56, 2.38))
    return bez((952, 400), (980, 640), (720, 860), (874, BY + 112), p)


def a8_page(t):
    """The page inside the monitor, building in order; placeholders wait where each part will pop."""
    dur = D['A8']
    lg, lh = _logo()
    s = ''
    sk = lambda inner, key: fade(inner, (1 - seg(t, A8_IN[key], A8_IN[key] + 0.12)) * (0.65 + 0.35 * math.sin(PI2 * 1.6 * t + len(key))))
    # address bar
    hl = bell(t, 1.5, 0.5)
    bar = F.rrect(IX + 190, IY + 18, IW - 240, 64, 32, F.WHITE, F.BLUE if hl > 0.3 else F.INK, 3 + 3 * hl)
    s += F.rrect(IX + 190, IY + 18, IW - 240, 64, 32, F.WHITE, F.INK, 3)
    s += pop(F.T(IX + 190 + (IW - 240) / 2, IY + 64, 'www.edlintics.com', 40), 610, IY + 50, seg(t, A8_IN['bar'], A8_IN['bar'] + 0.28))
    if hl > 0.02:
        s += scale_at(bar + F.T(IX + 190 + (IW - 240) / 2, IY + 64, 'www.edlintics.com', 40), 610, IY + 50, 1 + 0.04 * hl)
    # logo
    s += sk(F.rrect(300, IY + 150, 480, lh - 28, 24, F.TINT, None), 'logo')
    s += pop(lg, 540, IY + 136 + lh / 2, seg(t, A8_IN['logo'], A8_IN['logo'] + 0.3), -6)
    # headline
    s += sk(F.rrect(180, IY + 352, 720, 44, 22, F.TINT, None), 'line')
    s += pop(F.T(540, IY + 392, 'Learn the language of business', 54), 540, IY + 374, seg(t, A8_IN['line'], A8_IN['line'] + 0.3))
    # subject chips
    n = 0
    for r, row in enumerate(A8_CHIPS):
        ws = [F.tw(tx, 46) + 76 for tx, _ in row]
        x = 540 - (sum(ws) + 28) / 2
        y = IY + 446 + r * 108
        for (tx, col), w_ in zip(row, ws):
            t0 = A8_IN['chips'] + 0.09 * n
            s += fade(F.rrect(x, y, w_, 88, 44, F.TINT, None), (1 - seg(t, t0, t0 + 0.1)) * (0.65 + 0.35 * math.sin(PI2 * 1.6 * t + n)))
            g = F.rrect(x, y, w_, 88, 44, col, F.INK, 4) + F.T(x + w_ / 2, y + 60, tx, 46, fill=F.WHITE)
            s += pop(g, x + w_ / 2, y + 44 - 5 * bell(t, 2.9 + 0.12 * n, 0.4), seg(t, t0, t0 + 0.28), (-8, 8)[n % 2])
            x += w_ + 28
            n += 1
    # the button: pops, is pressed by the click, then pulses
    s += sk(F.rrect(150, BY, 780, 160, 80, F.TINT, None), 'btn')
    press = bell(t, CLICK - 0.06, 0.2)
    pulse = 0.018 * math.sin(PI2 * 1.5 * (t - dur)) * seg(t, CLICK + 0.2, CLICK + 0.5)
    kb = 1 - 0.05 * press + pulse + 0.02 * bell(t, 1.9, 0.5)
    off = 10 * (1 - 0.8 * press)
    btn = F.rrect(150 + off, BY + off, 780, 160, 80, F.INK, None) + F.rrect(150, BY, 780, 160, 80, F.BLUE, F.INK, 5)
    btn += F.T(500, BY + 102, 'Get started for free', 60, fill=F.WHITE)
    if t > CLICK:                                                                      # rings spreading from the click, again and again
        for i in range(2):
            u = ((t - CLICK) / 1.0 + i * 0.5) % 1.0 if t > CLICK + 0.5 * i else -1
            if u >= 0:
                e = ease_out(u)
                s += (f'<rect x="{150 - 34 * e:.1f}" y="{BY - 34 * e:.1f}" width="{780 + 68 * e:.1f}" height="{160 + 68 * e:.1f}" rx="{80 + 34 * e:.1f}" fill="none" '
                      f'stroke="{F.BLUE}" stroke-width="{7 * (1 - u) + 1:.1f}" opacity="{0.7 * (1 - u) * seg(dur - t, 0, 0.3):.2f}"/>')
    s += pop(scale_at(btn, BTN[0], BTN[1], kb), BTN[0], BTN[1], seg(t, A8_IN['btn'], A8_IN['btn'] + 0.32), -4)
    # the cursor comes down to the button and clicks
    if t > 1.5:
        cx, cy = a8_cursor(t)
        s += trail(a8_cursor, t)
        if t > CLICK:
            rp = seg(t, CLICK, CLICK + 0.3)
            s += f'<circle cx="874" cy="{BY + 112}" r="{20 + 70 * ease_out(rp):.1f}" fill="none" stroke="{F.WHITE}" stroke-width="{8 * (1 - rp):.1f}"/>' if rp < 1 else ''
            s += sparks_p(874, BY + 112, 24, 56, (-128, -92, -56, -20), t, CLICK, F.WHITE, 8, 1.5, dur)
        s += fade(cur(cx, cy, 1.9, bell(t, CLICK - 0.08, 0.24)), seg(t, 1.5, 1.6))
    return s


A8_POSES = ((0, 'cheer'), (0.12, 'watch'), (1.24, 'aha'), (1.66, 'watch'), (CLICK + 0.04, 'cheer'), (3.1, 'joy'), (3.62, 'hello'), (4.12, 'cheer'))


def a8_ledger(t):
    dur = D['A8']
    X, FL, sc = 540, A8FL, A8SC
    name, u = pose(t, A8_POSES)
    k = switch_k(u) * (0.94 + 0.06 * seg(t, 0, 0.12)) * (1 - 0.06 * bell(t, CLICK - 0.2, 0.22))
    hp = (14 * bell(t, 1.24, 0.24) + hop(t, CLICK + 0.04, 0.5, 96, 1) + hop(t, 3.1, 0.26, 40, 2) + 22 * bell(t, 4.12, 0.3))
    for t0 in (A8_IN['logo'], A8_IN['line'], A8_IN['chips'] + 0.1):                    # a small nod up at each part of the page
        hp += 9 * bell(t, t0 + 0.05, 0.22)
    rot, look, dx, calm = 0.0, (0, 0), 0.0, 1.0
    if name == 'watch':
        if t < 1.3:
            look = (-3.0 + 1.6 * math.sin(PI2 * 0.9 * t), -2.4)
            dx = 10 * math.sin(PI2 * 0.6 * t)
        else:
            cx, cy = a8_cursor(t)
            look = (-3.0 + (cx - 540) / 110, -2.4 + (cy - 990) / 500)
            rot, dx = 3.5 * ease(seg(t, 1.7, 2.3)), 12 * ease(seg(t, 1.7, 2.3))
    elif name == 'hello':
        rot = 5 * math.sin(PI2 * 3.2 * (t - 3.62)) * (1 - seg(t, 4.0, 4.12))             # he rocks as he waves
        dx = -8 * math.sin(PI2 * 1.6 * (t - 3.62))
    elif name == 'cheer' and t > 4.12:
        calm = 0.8
    s = front(name, X, FL, sc, t, hp, k, rot, look, (0.75, 2.0), dx, calm)
    top = FL - 188 * sc
    wide = 136 * sc / 2 + 120
    s += sparks_p(X, top + 150 - hp * 0.5, 215, 262, (-128, -106, -74, -52), t, CLICK + 0.1, t_end=dur)
    s += confetti_p([(X - wide, top - 20, -20), (X - wide + 26, top + 120, 30), (X + wide, top - 40, 25), (X + wide - 10, top + 110, -35),
                     (X - wide + 70, top - 70, 60)], (X, top + 150), t, CLICK + 0.1, dur)
    return s


def a8(t, ledger=True):
    s = a8_bg() + a8_page(t)
    if ledger:
        s += a8_ledger(t)
    F.WARN.clear()
    return s


def A8(t, dur):
    return a8(t), F.BLUE


# ---------------------------------------------------------------------------------------------
# T7  lesson cards -> the website: he hops up the cards while the monitor comes down
# ---------------------------------------------------------------------------------------------
@functools.lru_cache(None)
def a8_start():
    return a8(0.0, ledger=False)


def T7(t, dur):
    if t <= 0.0:
        return a7(D['A7']), F.YEL
    A7D = D['A7']
    wy = lambda tt: 940 * ease(seg(tt, 0.1, 0.82))                                     # the camera climbs: the cards sink
    top = lambda j, tt: (CARDS[j][0], CARDS[j][1] - CH / 2 + 6 + wy(tt))
    t1, t2, t3 = 0.12, 0.40, 0.64
    dips = [0.0] * 6
    dips[5] = 40 * math.exp(-9 * (t - t2)) * math.sin(PI2 * 2.2 * (t - t2) + 0.9) if t > t2 else 0
    dips[2] = 40 * math.exp(-9 * (t - t3)) * math.sin(PI2 * 2.2 * (t - t3) + 0.9) if t > t3 else 0
    s = shift(F.floor(1740, F.YEL_D), 0, wy(t)) + a7_cards(A7D, wy(t), dips)
    n8 = 1 - ease_out(seg(t, 0.4, 0.9))
    s += wiped(half(-lerp(-260, 2200, ease(seg(t, 0.4, 0.9))), -84), F.BLUE, F.BLUE_D, shift(a8_start(), 0, -520 * n8), 'w7')
    X0, FL0 = A7X, A7FL
    if t < t1:                                                                         # crouch, still the back view
        g, _ = back_ledger(X0, FL0, 2.3, 0, UP_L, UP_R, 1 - 0.06 * ease(seg(t, 0, t1)), FL0)
        s += g
    else:
        if t < t2:
            a, b_, p, lift = (X0, FL0), top(5, t2), seg(t, t1, t2), 260
        elif t < t3:
            a, b_, p, lift = top(5, t2), top(2, t3), seg(t, t2, t3), 300
            a = (a[0], a[1] + wy(t) - wy(t2))
        else:
            a, b_, p, lift = top(2, t3), (540, A8FL), seg(t, t3, dur), 330
            a = (a[0], a[1] + wy(t) - wy(t3))
        e = ease(p) * 0.6 + p * 0.4
        x, y = lerp(a[0], b_[0], e), lerp(a[1], b_[1], e) - lift * math.sin(math.pi * p)
        dirx = 1 if b_[0] > a[0] else -1
        tilt = dirx * 12 * math.sin(math.pi * p)
        sq = 1 - 0.05 * (bell(t, t2 - 0.03, 0.1) + bell(t, t3 - 0.03, 0.1))
        m = F.Mover.on_feet(x, y, 2.2, tilt)
        sw_ = 20 * math.sin(math.pi * p)
        for i in range(3):
            s += fade(F.line(x - dirx * (150 + 30 * i), y - 120 - i * 70, x - dirx * (250 + 30 * i), y - 90 - i * 70, F.WHITE, 9), math.sin(math.pi * p))
        s += squash(m.draw((sw_, -sw_), F.UPL, F.UPR, F.JOY), x, y, sq)
        for tl, j in ((t2, 5), (t3, 2)):                                               # landing puffs on the card he just hit
            if 0 <= t - tl < 0.16:
                px_, py_ = top(j, t)
                s += fade(F.line(px_ - 90, py_ - 6, px_ - 130, py_ - 40, F.WHITE, 8) + F.line(px_ + 90, py_ - 6, px_ + 130, py_ - 40, F.WHITE, 8), 1 - (t - tl) / 0.16)
    F.WARN.clear()
    return s, F.YEL


SCENES = {'T4': T4, 'A5': A5, 'T5': T5, 'A6': A6, 'T6': T6, 'A7': A7, 'T7': T7, 'A8': A8}
