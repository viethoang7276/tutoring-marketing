"""Demo video A, second half (30-second cut): T4, A6, T6, A7, TR, R, T7, A8 as pure functions of time.

Each scene is fn(t, dur) -> (svg_inner, background); lengths come from timeline_a.DUR and every beat is a share of them. The layouts come from frames_a.py (same numbers), re-composed
here so every part can move. Front-facing Ledger is the real website rig state (frames_a.embed_state's source files),
with only the rig's own channels touched (blink, gaze, torso tilt, bookmark); travelling shots use frames_a.Mover;
at the monitor he is the straight back view (frames_a.Ledger('back', ...)).
"""
import functools, math, os, re
import frames_a as F
from anim_util import clamp, seg, ease, ease_out, ease_in, back_out, lerp, lerp2, bez, hop, wobble, pop, fade, shift, squash

PI2 = 2 * math.pi
W, H = F.W, F.H
from timeline_a import DUR

F.MOUTH.setdefault('hmm', (7, 3, 1, 1))                                                # rig mouth shapes frames_a does not list (RIG.md)
F.MOUTH.setdefault('sad', (12, 6, -9, -9))


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
# A6  economics, IS-LM: one hesitation, the pull-down, the answer, one hop
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



def a6_times():
    """Key moments of A6 as shares of its length (the second hop is caught at its top at the end, as in the static frame)."""
    dur = DUR['A6']
    th = dur - 1.5 * 0.485                                                             # the hop leaves the floor
    d2 = 0.6 * dur
    return dict(c0=0.03 * dur, c1=0.16 * dur, g=0.25 * dur, d0=0.27 * dur, d2=d2, ts=d2 + 0.03, th=max(th, d2 + 0.3))


def a6_y(t):
    k = a6_times()
    return LY1 + (LY2 - LY1) * back_out(ease(seg(t, k['d0'], k['d2'])), 0.6)


def a6_cursor(t):
    k = a6_times()
    if t < k['c1']:
        return bez((600, 1010), (760, 1000), (930, 900), (GX + 22, LY1 - 6), ease(seg(t, k['c0'], k['c1'])))
    return (GX + 22, a6_y(t) - 6)


def a6_mouse(t):
    cx, cy = a6_cursor(t)
    return 742 + (cx - 922) * 0.09, A6FL - 228 + 46 + (cy - 764) * 0.1


def a6(t, ledger=True, lines=True):
    dur = DUR['A6']
    K = a6_times()
    C0, C1, G, D2, TS, TH = K['c0'], K['c1'], K['g'], K['d2'], K['ts'], K['th']
    ox, oy, xr = 180, 1070, 960
    y = a6_y(t)
    IS = lambda x: LY1 + (x - 720)
    s = a6_bg()
    # the question strip
    s += scale_at(F.qbadge(160, 513, 42), 160, 513, 1 + 0.07 * bell(t, 0.05, 0.35), 8 * math.sin(PI2 * 0.8 * t) * (1 - seg(t, TS, TS + 0.3)))
    r1 = 'The central bank cuts the rate'
    s += pop(F.T(224, 496.2, r1, 42, 600, anchor='start', fill=F.SLATE), 224 + F.tw(r1, 42) / 2, 482, seg(t, 0.04, 0.28))
    s += F.T(224, 560.6, 'What happens to output Y?', 46, 700, anchor='start')
    # the graph
    moved = clamp(abs(y - LY1) / 30)
    dn = clamp((y - LY1) / 40)
    ex = 720 + (y - LY1)
    if dn > 0:
        s += fade(F.line(ex, y, ex, oy, F.SLATE, 5, dash='3 14'), dn)
    s += fade(F.line(ox, LY1, xr - 10, LY1, F.SLATE, 7, dash='18 16'), moved)
    if lines:
        s += F.line(ox, y, xr - 10, y, F.INK, 10) + F.line(640, IS(640), 940, IS(940), F.BLUE, 10)
    s += F.T(628, IS(640) + 6, 'IS', 50, anchor='end', fill=F.BLUE)
    s += F.rrect(ox + 14, y - 60, 470, 50, 0, F.WHITE, None)                          # keeps the label clear of the dashed old line as it passes
    s += F.T(ox + 24, y - 18, 'LM', 44, anchor='start')
    s += F.T(ox + 24 + F.tw('LM', 44) + 16, y - 20, 'set by the central bank', 28, 600, anchor='start', fill=F.SLATE)
    ap = 5 * math.sin(PI2 * 1.3 * (t - dur)) * seg(t, TS + 0.2, TS + 0.5)
    s += arrow_on(660, LY1 + 20 + ap, 660, LY2 - 20 + ap, seg(t, D2 - 0.45, D2), F.PINK, 14, 38)
    if dn > 0:
        s += fade(F.circle(720, LY1, 13, F.WHITE, F.INK, 5), dn)
    if t >= TS:
        s += scale_at(F.circle(ex, y, 20, F.GREEN, F.INK, 6), ex, y, 1 + 0.5 * bell(t, TS, 0.3) + 0.06 * math.sin(PI2 * 1.5 * (t - dur)))
        s += sparks_p(ex, y, 34, 60, (-140, -90, -40, 30), t, TS + 0.02, F.GREEN, 6, t_end=dur) if t < TS + 0.45 else ''
    elif lines:
        s += F.circle(ex, y, 18, F.WHITE, F.INK, 6)
    s += pop(F.T(ox - 16, LY2 + 13, 'i_2', 40, anchor='end'), ox - 40, LY2, seg(t, TS, TS + 0.22))
    s += pop(F.T(850, oy + 50, 'Y_2', 40), 850, oy + 38, seg(t, TS + 0.06, TS + 0.28))
    gp = 4 * math.sin(PI2 * 1.4 * (t - dur)) * seg(t, TS + 0.4, TS + 0.6)
    s += arrow_on(732 + gp, oy - 24, 838 + gp, oy - 24, seg(t, TS + 0.05, TS + 0.32), F.GREEN, 8, 24)
    cx, cy = a6_cursor(t)
    ga = seg(t, C1 - 0.12, C1) * (1 - seg(t, G - 0.1, G))
    if ga > 0:
        s += fade(ghost(GX, y + 30, GX, y + 140, 0.5 + 0.5 * math.sin(PI2 * 2.4 * t)) + ghost(GX, y - 30, GX, y - 90, 0.5 - 0.5 * math.sin(PI2 * 2.4 * t)), ga)
    press = seg(t, G - 0.05, G) * (1 - seg(t, TS + 0.02, TS + 0.1))
    if t > C0:
        s += trail(a6_cursor, t) + fade(cur(cx, cy, 1.3, press), seg(t, C0, C0 + 0.08))
    pk = 1 + 0.014 * math.sin(PI2 * 1.1 * (t - dur))
    s += pop(scale_at(F.popup(400, 990, 'Correct', 48, col=F.GREEN, sw=6, corners=(0, 1), h=96, n1=30), 400, 990, pk), 400, 990, seg(t, TS + 0.18, TS + 0.42), -5)
    # desk, mouse (it moves with the cursor) and Ledger from straight behind
    FL = A6FL
    dt = FL - 228
    mx_, my_ = a6_mouse(t)
    s += a6_desk()
    s += F.path(f'M{mx_ + 40:.1f} {my_ - 6:.1f} C {mx_ + 150:.1f} {my_ - 60:.1f} 960 {dt - 60} 760 1162', stroke=F.INK, sw=5)
    mouse = F.rrect(mx_ - 40, my_ - 26 + 3 * press, 84, 50, 24, F.WHITE, F.INK, 5) + F.line(mx_ + 2, my_ - 26 + 3 * press, mx_ + 2, my_ - 6 + 3 * press, F.INK, 4)
    if not ledger:
        F.WARN.clear()
        return s + mouse
    au = ease(seg(t, TH, TH + 0.14))                                                   # arms from the desk to the air
    hp = 0.0
    if t >= TH:
        hp = (72 if t < TH + 0.485 else 44) * abs(math.sin(math.pi * (t - TH) / 0.485))  # one hop, the next one caught at its top
    k = (1 - 0.06 * bell(t, TH - 0.18, 0.18)) * (0.95 + 0.05 * seg(t, 0, 0.12))
    k *= 1 + 0.012 * math.sin(PI2 * t / 1.5)
    rot = (-5 + 1.6 * math.sin(PI2 * 1.1 * t) + 3.5 * ease(seg(t, G, D2))) * (1 - au)
    L = F.Ledger('back', 540, FL - hp, 2.3, rot)
    scr = seg(t, 0.06, 0.16) * (1 - seg(t, G - 0.16, G - 0.04))                       # he rubs his head while he hesitates
    hl0 = (45 + 3.5 * math.sin(PI2 * 4.6 * t) * scr, 93 + 2 * math.cos(PI2 * 4.6 * t) * scr + 40 * ease(seg(t, G - 0.1, G + 0.12)) * (1 - au))
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
            s += qmark_p(qx, qy, size, r, t, 0.06 + 0.07 * i, G + 0.04 * i, i)
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


@functools.lru_cache(None)
def a6_open():
    return a6(0.0, ledger=False, lines=False)


@functools.lru_cache(None)
def a6_end():
    return a6(DUR['A6'], ledger=False)


# ---------------------------------------------------------------------------------------------
# T4  statistics -> IS-LM: the bell's line straightens into LM and IS, pink wipes, Ledger hops to the desk
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
    p = seg(t, 0, dur)
    s = old + fade(marks, 1 - seg(p, 0, 0.25))
    s += wiped(half(lerp(2080, -140, ease(seg(p, 0.0, 0.86))), 32.5), F.PINK, F.PINK_D, a6_open(), 'w4')
    r = ease(seg(p, 0.08, 0.94))                                                       # the bell's base and its right slope become LM and IS
    l0, l1 = lerp2((74, 1096), (180, LY1), r), lerp2((1006, 1096), (950, LY1), r)
    i0, i1 = lerp2((540, 786), (640, 690), r), lerp2((830, 1060), (940, 990), r)
    s += F.line(i0[0], i0[1], i1[0], i1[1], F.WHITE, 18, extra=f'opacity="{(1 - r) * seg(p, 0.05, 0.2):.2f}"')
    s += fade(F.line(l0[0], l0[1], l1[0], l1[1], F.INK, 10) + F.line(i0[0], i0[1], i1[0], i1[1], F.BLUE, 10), seg(p, 0.05, 0.2))
    s += pop(F.circle(720, LY1, 18, F.WHITE, F.INK, 6), 720, LY1, seg(p, 0.75, 1.0))
    # Ledger: one hop from his spot to the desk; at the top of it we cut to the back view
    x, y = lerp(250, 540, ease(p)), lerp(1856, A6FL, p) - 170 * math.sin(math.pi * p)
    sc = lerp(2.0, 2.3, ease(p))
    if p <= 0:
        s += front('cheer', 250, 1856, 2.0, 0, calm=0)
    elif p < 0.42:
        s += F.Mover.on_feet(x, y, sc, 10 * math.sin(math.pi * p)).draw((14, -14), F.UPL, F.UPR, F.JOY)
        s += fade(F.speed(x - 170, y - 300, 3, 90, 60, F.WHITE, 9), p * 2)
    else:
        q = ease(seg(p, 0.5, 1.0))
        rot = -5 * q
        L = F.Ledger('back', x, y, sc, rot)
        mx_, my_ = a6_mouse(0.0)
        hl, hr = lerp2(UP_L, (45, 93), q), lerp2(UP_R, L.r((lerp(x + 200, mx_, q), lerp(y - 240, my_ - 2, q))), q)
        g, _ = back_ledger(x, y, sc, rot, hl, hr)
        s += f'<ellipse cx="540" cy="{A6FL + 32}" rx="{96 * q:.1f}" ry="13" fill="{F.INK}" opacity="0.14"/>' + g
    F.WARN.clear()
    return s, F.VIOLET


# ---------------------------------------------------------------------------------------------
# A7  six lesson cards, "More than 1,000 lessons", the subjects answer as the voice names them
# ---------------------------------------------------------------------------------------------
CW, CH, HD = 450, 340, 84
A7X, A7FL = 540, 1810
A7G = 'translate(540 1270) scale(0.88) translate(-540 -1270)'                          # the card grid, drawn a little smaller so the headline has its own band on top
CARDS = ((296, 296, -4, F.EMER_D, 'Journal entries'), (788, 282, 4, F.ORANGE, 'Compound interest'), (290, 694, 3, F.VIOLET, 'Hypothesis testing'),
         (792, 686, -3, F.PINK, 'Supply and demand'), (296, 1092, -4, F.BLUE, 'Break-even point'), (788, 1082, 3, F.SUIT, 'Net present value'))
LAND_F = (0.07, 0.10, 0.19, 0.22, 0.31, 0.34)                                          # three waves, as shares of the scene
PERIOD = (1.0, 1.16, 0.92, 1.24, 0.84, 1.08)
OUTER = ((0,), (1,), (), (), (3,), (2,))
SUBJ_F = ((0.40, (0, 4)), (0.58, (1, 5)), (0.695, (3,)), (0.842, (2,)))               # accounting, finance, economics, statistics in A7.wav
HEAD7 = 'More than 1,000 lessons'


def a7_land(j):
    return LAND_F[j] * DUR['A7']


def a7_pulse(j, t):
    """0..1 while the voice names card j's subject."""
    dur = DUR['A7']
    return max([bell(t, f * dur, 0.55) for f, js in SUBJ_F if j in js] or [0.0])


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



def lesson(j, b, lines=1.0, glow=0.0, corners=(0, 1, 2, 3)):
    col, topic = CARDS[j][3], CARDS[j][4]
    body, icon = card_body(j, b)
    x, y = -CW / 2, -CH / 2
    g = fade(F.pop_lines(x, y, CW, CH, F.WHITE, 7, 14, 36, OUTER[j]), lines)
    if glow > 0.02:
        g += fade(F.pop_lines(x, y, CW, CH, F.WHITE, 9, 16, 30 + 26 * glow, corners), glow * 1.5)
    g += F.rrect(x + 10, y + 10, CW, CH, 26, F.INK, None) + F.rrect(x, y, CW, CH, 26, F.WHITE, F.INK, 5)
    g += F.path(f'M{x} {y + HD} V{y + 26} Q{x} {y} {x + 26} {y} H{-x - 26} Q{-x} {y} {-x} {y + 26} V{y + HD} Z', fill=col, stroke=F.INK, sw=5)
    g += F.circle(x + 50, y + HD / 2, 28, F.WHITE, F.INK, 4) + F.group(icon, x + 50, y + HD / 2)
    g += F.T(x + 92, y + HD / 2 + 12, topic, 34, anchor='start', fill=F.WHITE, check=False)
    return g + F.group(body, 0, 42)


def a7_cards(t):
    """t may be negative: the first wave is already on its way at the end of T6."""
    dur = DUR['A7']
    order = sorted(range(6), key=lambda j: a7_pulse(j, t))                             # a lifted card is drawn last, over its neighbours
    s = ''
    for j in order:
        cx, cy, rot, col, topic = CARDS[j]
        tl = a7_land(j)
        p = seg(t, tl - 0.45, tl)
        if p <= 0:
            continue
        side = -1 if cx < 540 else 1
        e = 1 - (1 - p) ** 3 * (1 + 2.2 * p) if p < 1 else 1                           # eased arrival
        x0, y0 = cx + side * 760, cy + (260 if j < 2 else (-120 if j < 4 else -300))
        bounce = math.exp(-7 * (t - tl)) * math.sin(PI2 * 3.2 * (t - tl)) if t > tl else 0
        pu = a7_pulse(j, t)
        x, y = lerp(x0, cx, e), lerp(y0, cy, e) + 16 * bounce - (14 if j < 2 else 26) * pu
        r = rot + side * 26 * (1 - e) + 3 * bounce * side + 2.5 * math.sin(PI2 * 3 * t) * pu
        b = math.sin(math.pi * (dur - t) / PERIOD[j]) ** 2 * seg(t, tl + 0.2, tl + 0.5) * (1 - pu) if t < dur else 0
        la = seg(t, tl, tl + 0.12) * (0.75 + 0.25 * math.cos(PI2 * 1.2 * (t - dur)))
        g = lesson(j, b, la, pu, (2, 3) if j < 2 else (0, 1, 2, 3))                    # the top row keeps its glow clear of the headline
        if p < 1:                                                                      # speed lines behind a flying card
            g += fade(F.speed(side * (CW / 2 + 30), -60, 3, 110, 60, F.WHITE, 9, side), (1 - p) * 1.5)
        s += grp(g, f'translate({x:.1f} {y:.1f}) rotate({r:.2f}) scale({1 + 0.05 * bell(t, tl - 0.05, 0.3) + 0.07 * pu:.3f})')
    return grp(s, A7G)


@functools.lru_cache(None)
def a7_head():
    w = F.tw(HEAD7, 72) + 110
    return F.rrect(540 - w / 2 + 9, 79, w, 120, 60, F.INK, None) + F.rrect(540 - w / 2, 70, w, 120, 60, F.WHITE, F.INK, 5) + F.T(540, 156, HEAD7, 72, maxw=w - 60)


def a7_ledger(t):
    dur = DUR['A7']
    T3 = a7_land(5) + 0.04                                                             # the last wave is down: arms thrown up
    au = ease(seg(t, T3, T3 + 0.14)) + (1 - ease(seg(t, 0.02, 0.22))) * (t < a7_land(2))
    half_up = 0.34 * bell(t, a7_land(0) - 0.06, 0.5) + 0.42 * bell(t, a7_land(2) - 0.06, 0.5)
    a = clamp(au + half_up)
    hp = 16 * bell(t, a7_land(0), 0.26) + 20 * bell(t, a7_land(2), 0.26) + hop(t, T3, 0.42, 62, 1)
    rot = 0.0
    for f, js in SUBJ_F:                                                               # he turns to each subject as it is named
        side = sum(-1 if CARDS[j][0] < 540 else 1 for j in js)
        hp += 16 * bell(t, f * dur + 0.05, 0.3)
        rot += (3.5 * side if side else 2.5 * math.sin(PI2 * 2 * (t - f * dur))) * bell(t, f * dur, 0.55)
    k = (0.94 + 0.06 * seg(t, 0, 0.14)) * (1 - 0.06 * bell(t, T3 - 0.18, 0.18)) * (1 + 0.012 * math.sin(PI2 * t / 1.5))
    rot += -4 * bell(t, a7_land(0) - 0.16, 0.42) + 4 * bell(t, a7_land(1) - 0.1, 0.42) - 4 * bell(t, a7_land(2) - 0.16, 0.42) + 4 * bell(t, a7_land(3) - 0.1, 0.42)
    wave = 5 * math.sin(PI2 * 2.2 * (t - dur)) * seg(t, T3 + 0.14, T3 + 0.34)
    hl, hr = lerp2(REST_L, (UP_L[0] - wave, UP_L[1]), a), lerp2(REST_R, (UP_R[0] + wave, UP_R[1]), a)
    s, L = back_ledger(A7X, A7FL - hp, 2.3, rot, hl, hr, k, A7FL)
    top = A7FL - 432.4
    s += sparks_p(540, top + 150 - hp * 0.6, 205, 250, (-126, -106, -74, -54), t, T3 + 0.06, t_end=dur)
    s += confetti_p([(215, top + 60, -20), (250, top + 230, 30), (860, top + 50, 25), (840, top + 230, -35), (160, top + 180, 60), (915, top + 170, 10)],
                    (540, top + 200), t, T3 + 0.06, dur)
    return s


def a7(t, ledger=True):
    dur = DUR['A7']
    s = F.floor(1740, F.YEL_D) + a7_cards(t)
    hk = 1 + 0.02 * math.sin(PI2 * 1.2 * (t - dur)) * seg(t, 0.17 * dur + 0.4, 0.17 * dur + 0.7)
    s += pop(scale_at(a7_head(), 540, 130, hk), 540, 130, seg(t, 0.17 * dur, 0.17 * dur + 0.3), -4)
    if ledger:
        s += a7_ledger(t)
    F.WARN.clear()
    return s


def A7(t, dur):
    return a7(t), F.YEL


@functools.lru_cache(None)
def a7_end():
    return a7(DUR['A7'], ledger=False)


# ---------------------------------------------------------------------------------------------
# T6  IS-LM -> lesson cards: the LM line drops through the frame and takes the pink with it
# ---------------------------------------------------------------------------------------------
def T6(t, dur):
    p = seg(t, 0, dur)
    ye = lerp(-120, 2060, ease(seg(p, 0.03, 0.97)))
    s = a6_end()
    s += wiped(half(-ye, -90), F.YEL, F.YEL_D, F.floor(1740, F.YEL_D) + a7_cards(t - dur), 'w6')
    if 0 < p < 1:
        s += F.line(-30, ye, W + 30, ye, F.INK, 12)
    y = lerp(A6FL - 44, A7FL, ease_in(p))                                              # he comes down from the top of his hop onto the new floor
    g, _ = back_ledger(540, y, 2.3, 0, UP_L, UP_R, 1.0, A7FL if ye > A7FL else A6FL, 96.6 if ye > A7FL else 74)
    s += g
    F.WARN.clear()
    return s, F.PINK


# ---------------------------------------------------------------------------------------------
# R  reading against doing (Koedinger et al., 2015)
# ---------------------------------------------------------------------------------------------
R_GREY, R_GREY_D, R_PILL = '#8C96A8', '#737F94', '#DDE2EA'
R_FL, R_SC, R_LX, R_RX = 1580, 2.6, 270, 810
R_SLOTS = (('t', 630, 960), ('coins', 990, 960), ('bell', 650, 790), ('cross', 970, 790), ('tick', 810, 915), ('bulb', 810, 740))
R_CREDIT = 'Koedinger et al., Carnegie Mellon University, 2015'


def r_times():
    dur = DUR['R']
    six = 0.59 * dur                                                                   # "six times" in R.wav
    pops = [0.11 * dur + i * (six - 0.2 - 0.11 * dur) / 5 for i in range(6)]           # the six icons, the last just before the badge
    return dur, six, pops


@functools.lru_cache(None)
def r_icon(kind):
    g = F.rrect(-49, -49, 110, 110, 22, F.INK, None) + F.rrect(-55, -55, 110, 110, 22, F.WHITE, F.INK, 5)
    if kind == 't':
        g += F.line(-34, -26, 34, -26, F.INK, 6) + F.line(0, -26, 0, 36, F.INK, 6) + F.rrect(-32, -14, 24, 16, 5, F.BLUE, None) + F.rrect(8, -14, 24, 16, 5, F.TINT, None)
        g += F.rrect(-32, 10, 18, 14, 5, F.TINT, None)
    elif kind == 'coins':
        g += F.coin_stack(-20, 38, 2, 38, 13) + F.coin_stack(20, 38, 5, 38, 13)
    elif kind == 'bell':
        f = lambda xx: 32 - 62 * math.exp(-(xx / 17) ** 2 / 2)
        g += F.path(f'M-42 32 L{F.fpts(f, -42, 42, 30)} L42 32 Z', fill=F.RED2, stroke=F.INK, sw=4) + F.line(-44, 32, 44, 32, F.INK, 5)
    elif kind == 'cross':
        g += F.line(-32, 30, 32, -30, F.INK, 6) + F.line(-32, -30, 32, 30, F.PINK, 7) + F.circle(0, 0, 9, F.GREEN, F.INK, 3)
    elif kind == 'tick':
        g += F.tick(0, 0, 36)
    else:
        g += F.sparks(0, -8, 34, 46, (-150, -90, -30), F.YEL_D, 5)
        g += F.rrect(-11, 14, 22, 20, 5, F.SUIT, None) + F.circle(0, -8, 24, F.YEL, F.INK, 4) + F.path('M-8 -4 L0 6 L8 -4', stroke=F.INK, sw=3)
    return g


def r_book():
    """Open textbook held low in front of him, seen from behind (rig units, inside the Mover)."""
    c = '#6B7688'
    s = F.path('M70 157 L118 161 L122 161 L170 157 L170 162 L70 162 Z', fill=F.PAGES, stroke=F.INK, sw=2)
    s += F.path('M68 160 L119 165 L119 210 L68 205 Z', fill=c, stroke=F.INK, sw=3) + F.path('M172 160 L121 165 L121 210 L172 205 Z', fill=c, stroke=F.INK, sw=3)
    s += F.rrect(80, 175, 28, 11, 3, R_PILL, None) + F.line(120, 164, 120, 210, F.INK, 3)
    return s


def r_tablet(t, pops):
    """Tablet held low in front of him: a tiny T-account, a block dragged across before every icon pops (rig units)."""
    u = 0.0
    hit = 0.0
    for tp in pops:
        if tp - 0.22 <= t < tp + 0.14:
            u = ease(seg(t, tp - 0.2, tp - 0.02))
            hit = bell(t, tp - 0.04, 0.18)
    bx, by = lerp(144, 100, u), lerp(196, 181.5, u)
    s = F.rrect(68, 156, 104, 56, 9, F.INK, None) + F.rrect(74, 161, 92, 46, 4, F.WHITE, None)
    s += F.line(82, 169, 158, 169, F.INK, 2.5) + F.line(120, 169, 120, 204, F.INK, 2.5)
    s += F.rrect(88, 175, 24, 13, 3, F.GREEN_T if hit > 0.2 else F.WHITE, F.GREEN if hit > 0.2 else F.SLATE, 1.6, '' if hit > 0.2 else 'stroke-dasharray="4 3"')
    s += F.rrect(bx - 11, by - 6, 22, 12, 3, F.BLUE, F.INK, 1.6)
    pts = [(0, 0), (0, 50), (12, 39), (21, 59), (30, 55), (21, 36), (37, 36)]
    k = 0.3 * (1 - 0.15 * seg(u, 0.02, 0.1) * (1 - seg(u, 0.9, 1)))
    s += F.path('M' + ' L'.join(f'{bx + 5 + px * k:.1f} {by + 1 + py * k:.1f}' for px, py in pts) + ' Z', fill=F.WHITE, stroke=F.INK, sw=1.6)
    return s


def r_pill(cx, text, fill):
    w = F.tw(text, 64) + 96
    return F.rrect(cx - w / 2 + 8, 118, w, 104, 52, F.INK, None) + F.rrect(cx - w / 2, 110, w, 104, 52, fill, F.INK, 5) + F.T(cx, 184, text, 64)


@functools.lru_cache(None)
def r_badge():
    cx, cy = R_RX, 400
    pts = []
    for i in range(28):
        rr, a = (150 if i % 2 == 0 else 126), math.radians(i * 360 / 28)
        pts.append((rr * math.cos(a), rr * math.sin(a)))
    d = lambda ox_: 'M' + ' L'.join(f'{cx + x + ox_:.1f} {cy + y + ox_:.1f}' for x, y in pts) + ' Z'
    s = F.path(d(9), fill=F.INK, stroke=None) + F.path(d(0), fill=F.YEL, stroke=F.INK, sw=6)
    s += F.T(cx, cy + 56, '6×', 160)
    return s


@functools.lru_cache(None)
def r_label():
    tx = 'more learning by doing'
    w = F.tw(tx, 36) + 56
    return F.rrect(R_RX - w / 2 + 6, 571, w, 72, 36, F.INK, None) + F.rrect(R_RX - w / 2, 565, w, 72, 36, F.WHITE, F.INK, 5) + F.T(R_RX, 614, tx, 36, maxw=w - 30)


def r_doer(t, x=None, y=None, sc=None, tablet=True):
    """The Ledger who learns by doing; x, y, sc let T7 carry him away."""
    dur, six, pops = r_times()
    hp = sum(16 * bell(t, tp, 0.24) for tp in pops) + hop(t, six, 0.34, 36, 1)
    if t > six + 0.5:
        hp += 10 * abs(math.sin(math.pi * (t - dur) / 0.42))
    fx, fy = (R_RX if x is None else x), (R_FL if y is None else y) - hp
    m = F.Mover.on_feet(fx, fy, sc or R_SC, 3 * math.sin(PI2 * 1.3 * (t - dur)))
    seen = t > pops[0]
    look_up = max(bell(t, tp, 0.3) for tp in pops)
    if t > six:
        face = F.JOY
    elif seen:
        face = {'brows': 4 + 2 * look_up, 'mouth': 'grin', 'look': (0, 2.2 - 4.6 * look_up)}
    else:
        face = {'brows': 2, 'mouth': 'smile', 'look': (0, 2.4)}
    held = r_tablet(t, pops) if tablet else ''
    return m, m.draw((0, 0), {'hand': (66, 184), 'front': True, 'bend': -1}, {'hand': (174, 184), 'front': True, 'bend': 1}, face, held)


def r_scene(t, doer=True):
    """t < 0 is the end of TR: the two Ledgers are still coming up into place."""
    dur, six, pops = r_times()
    rise = 560 * (1 - ease_out(seg(t, -0.3, 0.0)))
    s = F.rrect(0, 0, 540, H, 0, R_GREY, None) + F.rrect(540, 0, 540, H, 0, F.BLUE, None)
    s += F.rrect(0, R_FL - 50, 540, H, 0, R_GREY_D, None) + F.rrect(540, R_FL - 50, 540, H, 0, F.BLUE_D, None)
    s += pop(r_pill(R_LX, 'Reading', R_PILL), R_LX, 162, seg(t, 0.02, 0.26), -5) + pop(r_pill(R_RX, 'Doing', F.WHITE), R_RX, 162, seg(t, 0.1, 0.34), 5)
    # LEFT: reading. Sleepy, nodding off over the open book; one faint formula drifts up, slowly
    cp = seg(t, 0.12 * dur, dur)
    cy_ = lerp(1030, 720, cp) + 8 * math.sin(PI2 * 0.5 * t)
    cxx = R_LX + 14 * math.sin(PI2 * 0.35 * t)
    chip = F.rrect(cxx - 92, cy_ - 32, 184, 64, 18, F.WHITE, F.INK, 4) + F.T(cxx, cy_ + 14, 'A = L + E', 38, check=False)
    s += fade(chip, 0.55 * seg(t, 0.12 * dur, 0.12 * dur + 0.5))
    yawn = bell(t, 0.3 * dur, 0.26 * dur)
    nod_t = 0.74 * dur                                                                 # he nods off and jerks awake
    droop = ease(seg(t, 0.1 * dur, nod_t)) * (1 - ease_out(seg(t, nod_t, nod_t + 0.1))) + 0.5 * ease(seg(t, nod_t + 0.25, dur))
    lid = clamp(0.5 + 0.35 * droop + 0.6 * (yawn > 0.3) - 0.3 * bell(t, nod_t, 0.3))
    tilt = 6 * droop + 1.2 * math.sin(PI2 * 0.4 * t)
    lids = ''
    for ex in (102, 138):
        h = 4 + 15 * lid
        lids += F.rrect(ex - 9.5, 101.5, 19, h, 3, F.CREAM, None) + F.line(ex - 8.5, 101.5 + h, ex + 8.5, 101.5 + h, F.INK, 3)
    face = {'mouth': 'oh' if yawn > 0.3 else 'hmm', 'look': (0, 2.2), 'brows': 4 * bell(t, nod_t, 0.35)}
    if not face['brows']:
        face.pop('brows')
    mL = F.Mover.on_feet(R_LX, R_FL + rise + 5 * droop, R_SC, tilt)
    s += f'<ellipse cx="{R_LX}" cy="{R_FL + 26 + rise}" rx="106" ry="14" fill="{F.INK}" opacity="0.10"/>'
    s += mL.draw((0, 0), {'hand': (66, 184), 'front': True, 'bend': -1}, {'hand': (174, 184), 'front': True, 'bend': 1}, face, r_book() + lids)
    # RIGHT: doing. Every drag on the tablet throws a new idea up round his head
    if doer:
        m, g = r_doer(t, y=R_FL + rise)
        s += f'<ellipse cx="{R_RX}" cy="{R_FL + 26 + rise}" rx="106" ry="14" fill="{F.INK}" opacity="0.10"/>' + g
        src = m.w((120, 44))                                                           # ideas come out of the top of his head
    else:
        src = (R_RX, R_FL - 178 * R_SC)
    for i, ((kind, ix, iy), tp) in enumerate(zip(R_SLOTS, pops)):
        p = seg(t, tp, tp + 0.26)
        if p <= 0:
            continue
        e = back_out(p, 0.5)                                                           # a small overshoot only: the slots sit close to the divider and the frame edge
        x, y = lerp(src[0], ix, e), lerp(src[1], iy, e) + 7 * math.sin(PI2 * 0.9 * (t - dur) + i * 1.7) * p
        k = (0.3 + 0.7 * min(1, e)) * 1.15 * (1 + 0.05 * math.sin(PI2 * 1.3 * (t - dur) + i))
        s += grp(r_icon(kind), f'translate({x:.1f} {y:.1f}) rotate({(1 - p) * 40 * (-1) ** i + 4 * math.sin(PI2 * 0.7 * (t - dur) + i):.1f}) scale({k:.3f})', p * 3)
        fl = bell(t, tp + 0.12, 0.3)
        if fl > 0.02:
            s += fade(F.sparks(ix, iy, 78, 78 + 30 * fl, (-135, -45, 45, 135), F.WHITE, 7), fl * 1.5)
    bp = seg(t, six, six + 0.26)
    if bp > 0:
        bk = 1 + 0.035 * math.sin(PI2 * 1.6 * (t - dur)) * seg(t, six + 0.3, six + 0.5)
        s += fade(F.sparks(R_RX, 400, 170, 170 + 44 * back_out(bp), (-160, -125, -55, -20, 20, 160), F.WHITE, 9), bp * (0.7 + 0.3 * math.cos(PI2 * 1.6 * (t - dur))))
        s += pop(scale_at(r_badge(), R_RX, 400, bk), R_RX, 400, bp, -14)
    s += pop(r_label(), R_RX, 601, seg(t, six + 0.14, six + 0.38), 4)
    # divider and the source credit
    s += F.line(540, -10, 540, 1750, F.INK, 10, cap='butt')
    s += F.rrect(0, 1750, W, 170, 0, F.SUIT, None) + fade(F.T(540, 1846, R_CREDIT, 34, 600, fill=F.WHITE), seg(t, 0.0, 0.3))
    F.WARN.clear()
    return s


def R(t, dur):
    return r_scene(t), F.BLUE


@functools.lru_cache(None)
def r_end():
    return r_scene(DUR['R'], doer=False)


def TR(t, dur):
    """Lesson cards -> the comparison: the frame parts in the middle like curtains; he drops out, two of him come up."""
    p = seg(t, 0, dur)
    s = a7_end()
    g, _ = back_ledger(A7X, A7FL + 900 * ease_in(seg(p, 0.0, 0.8)), 2.3, 0, UP_L, UP_R, 1 - 0.05 * bell(p, 0, 0.2))
    s += g
    w = 640 * ease(seg(p, 0.04, 0.96))
    s += wiped([(540 - w, -60), (540 + w, -60), (540 + w, H + 60), (540 - w, H + 60)], F.BLUE, F.INK, r_scene(t - dur), 'wr', 7) if w > 1 else ''
    F.WARN.clear()
    return s, F.YEL


# ---------------------------------------------------------------------------------------------
# A8  the website, the button
# ---------------------------------------------------------------------------------------------
A8FL, A8SC = 1800, 2.2
IX, IY, IW = 66, 172, 948
BY = IY + 706
BTN = (540, BY + 80)
A8_CHIPS = ((('Accounting', F.EMER_D), ('Finance', F.ORANGE)), (('Economics', F.PINK), ('Statistics', F.VIOLET)))


def a8_times():
    dur = DUR['A8']
    return dict(bar=0.02 * dur, logo=0.07 * dur, line=0.14 * dur, chips=0.2 * dur, step=0.03 * dur, c0=0.3 * dur, c1=0.53 * dur, click=0.58 * dur,
                wave=0.58 * dur + 0.4, calm=dur - 0.46)


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


def a8_cursor(t):
    K = a8_times()
    return bez((952, 400), (980, 640), (720, 860), (874, BY + 112), ease(seg(t, K['c0'] + 0.06, K['c1'])))


def a8_page(t):
    """The page inside the monitor, building in order; placeholders wait where each part will pop. The button came down with the monitor."""
    dur = DUR['A8']
    K = a8_times()
    CLICK = K['click']
    lg, lh = _logo()
    s = ''
    sk = lambda inner, key: fade(inner, (1 - seg(t, K[key], K[key] + 0.1)) * (0.65 + 0.35 * math.sin(PI2 * 1.6 * t + len(key))))
    hl = bell(t, 0.24 * dur, 0.5)                                                      # "on Edlintics dot com"
    s += F.rrect(IX + 190, IY + 18, IW - 240, 64, 32, F.WHITE, F.INK, 3)
    s += pop(F.T(IX + 190 + (IW - 240) / 2, IY + 64, 'www.edlintics.com', 40), 610, IY + 50, seg(t, K['bar'], K['bar'] + 0.24))
    if hl > 0.02:
        bar = F.rrect(IX + 190, IY + 18, IW - 240, 64, 32, F.WHITE, F.BLUE if hl > 0.3 else F.INK, 3 + 3 * hl)
        s += scale_at(bar + F.T(IX + 190 + (IW - 240) / 2, IY + 64, 'www.edlintics.com', 40), 610, IY + 50, 1 + 0.04 * hl)
    s += sk(F.rrect(300, IY + 150, 480, lh - 28, 24, F.TINT, None), 'logo')
    s += pop(lg, 540, IY + 136 + lh / 2, seg(t, K['logo'], K['logo'] + 0.26), -6)
    s += sk(F.rrect(180, IY + 352, 720, 44, 22, F.TINT, None), 'line')
    s += pop(F.T(540, IY + 392, 'Learn the language of business', 54), 540, IY + 374, seg(t, K['line'], K['line'] + 0.26))
    n = 0
    for r, row in enumerate(A8_CHIPS):
        ws = [F.tw(tx, 46) + 76 for tx, _ in row]
        x = 540 - (sum(ws) + 28) / 2
        y = IY + 446 + r * 108
        for (tx, col), w_ in zip(row, ws):
            t0 = K['chips'] + K['step'] * n
            s += fade(F.rrect(x, y, w_, 88, 44, F.TINT, None), (1 - seg(t, t0, t0 + 0.1)) * (0.65 + 0.35 * math.sin(PI2 * 1.6 * t + n)))
            g = F.rrect(x, y, w_, 88, 44, col, F.INK, 4) + F.T(x + w_ / 2, y + 60, tx, 46, fill=F.WHITE)
            s += pop(g, x + w_ / 2, y + 44 - 5 * bell(t, CLICK + 0.3 + 0.1 * n, 0.36), seg(t, t0, t0 + 0.24), (-8, 8)[n % 2])
            x += w_ + 28
            n += 1
    # the button: is pressed by the click, then pulses
    press = bell(t, CLICK - 0.06, 0.2)
    pulse = 0.018 * math.sin(PI2 * 1.5 * (t - dur)) * seg(t, CLICK + 0.2, CLICK + 0.5)
    kb = 1 - 0.05 * press + pulse + 0.035 * bell(t, 0.0, 0.4) + 0.02 * bell(t, K['c0'], 0.5)
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
    s += scale_at(btn, BTN[0], BTN[1], kb)
    if t > K['c0']:                                                                    # the cursor comes down to the button and clicks
        cx, cy = a8_cursor(t)
        s += trail(a8_cursor, t)
        if t > CLICK:
            rp = seg(t, CLICK, CLICK + 0.3)
            s += f'<circle cx="874" cy="{BY + 112}" r="{20 + 70 * ease_out(rp):.1f}" fill="none" stroke="{F.WHITE}" stroke-width="{8 * (1 - rp):.1f}"/>' if rp < 1 else ''
            s += sparks_p(874, BY + 112, 24, 56, (-128, -92, -56, -20), t, CLICK, F.WHITE, 8, 1.5, dur)
        s += fade(cur(cx, cy, 1.9, bell(t, CLICK - 0.08, 0.24)), seg(t, K['c0'], K['c0'] + 0.08))
    return s


def a8_ledger(t):
    dur = DUR['A8']
    K = a8_times()
    CLICK, WV, CALM = K['click'], K['wave'], K['calm']
    X, FL, sc = 540, A8FL, A8SC
    name, u = pose(t, ((0, 'cheer'), (0.1, 'watch'), (CLICK + 0.04, 'cheer'), (WV, 'hello'), (CALM, 'cheer')))
    k = switch_k(u) * (0.94 + 0.06 * seg(t, 0, 0.1)) * (1 - 0.06 * bell(t, CLICK - 0.2, 0.22))
    hp = hop(t, CLICK + 0.04, 0.36, 90, 1) + 20 * bell(t, CALM, 0.26)
    for key in ('logo', 'line', 'chips'):                                              # a small bob up at each part of the page
        hp += 9 * bell(t, K[key] + 0.05, 0.2)
    rot, look, dx, calm = 0.0, (0, 0), 0.0, 1.0
    if name == 'watch':
        if t < K['c0']:
            look, dx = (-3.0 + 1.6 * math.sin(PI2 * 1.2 * t), -2.4), 8 * math.sin(PI2 * 0.9 * t)
        else:
            cx, cy = a8_cursor(t)
            look = (-3.0 + (cx - 540) / 110, -2.4 + (cy - 990) / 500)
            rot, dx = 3.5 * ease(seg(t, K['c0'], K['c1'])), 12 * ease(seg(t, K['c0'], K['c1']))
    elif name == 'hello':
        rot = 5 * math.sin(PI2 * 3.4 * (t - WV)) * (1 - seg(t, CALM - 0.08, CALM))       # he rocks as he waves
        dx = -8 * math.sin(PI2 * 1.7 * (t - WV))
    elif t > CALM:
        calm = 0.8
    s = front(name, X, FL, sc, t, hp, k, rot, look, (0.5,), dx, calm)
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


@functools.lru_cache(None)
def a8_start():
    return a8(0.0, ledger=False)


# ---------------------------------------------------------------------------------------------
# T7  the comparison -> the website: the monitor comes down with the blue, the Ledger who learned by doing hops to it
# ---------------------------------------------------------------------------------------------
def T7(t, dur):
    if t <= 0:
        return r_scene(DUR['R']), F.BLUE
    p = seg(t, 0, dur)
    s = r_end()
    n8 = 1 - ease_out(seg(p, 0.05, 0.95))
    s += wiped(half(-lerp(-260, 2200, ease(seg(p, 0.02, 0.96))), -84), F.BLUE, F.BLUE_D, shift(a8_start(), 0, -620 * n8), 'w7')
    RD = DUR['R']
    e = ease(p) * 0.6 + p * 0.4
    x, y = lerp(R_RX, 540, e), lerp(R_FL, A8FL, e) - 190 * math.sin(math.pi * p)
    sc = lerp(R_SC, A8SC, e)
    q = seg(p, 0.0, 0.5)                                                               # the tablet is tossed aside as his arms go up
    tb = grp(F.rrect(-135, -86, 270, 172, 23, F.INK, None) + F.rrect(-120, -70, 240, 140, 10, F.WHITE, None),
             f'translate({lerp(R_RX, 1180, ease_in(q)):.1f} {R_FL - 90 - 260 * math.sin(math.pi * q * 0.7):.1f}) rotate({200 * q:.0f})')
    s += tb if q < 1 else ''
    m = F.Mover.on_feet(x, y, sc, -12 * math.sin(math.pi * p))
    for i in range(3):
        s += fade(F.line(x + 150 + 30 * i, y - 120 - i * 70, x + 250 + 30 * i, y - 150 - i * 70, F.WHITE, 9), math.sin(math.pi * p))
    au = ease(seg(p, 0.0, 0.4))
    hl, hr = lerp2((66, 184), F.UPL['hand'], au), lerp2((174, 184), F.UPR['hand'], au)
    sw_ = 18 * math.sin(math.pi * p)
    s += f'<ellipse cx="{x:.1f}" cy="{lerp(R_FL + 26, A8FL + 31, e):.1f}" rx="{92 * (1 - 0.4 * math.sin(math.pi * p)):.1f}" ry="12" fill="{F.INK}" opacity="0.08"/>'
    s += m.draw((sw_, -sw_), {'hand': hl, 'bend': -1, 'front': au < 0.5}, {'hand': hr, 'bend': 1, 'front': au < 0.5}, F.JOY)
    F.WARN.clear()
    return s, F.BLUE


SCENES = {'T4': T4, 'A6': A6, 'T6': T6, 'A7': A7, 'TR': TR, 'R': R, 'T7': T7, 'A8': A8}
