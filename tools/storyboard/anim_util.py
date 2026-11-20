"""Shared timing helpers for the demo video A animation (film_a.py). Keep every scene on these so the film moves one way."""
import math


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def seg(t, a, b):
    """0 before a, 1 after b, linear in between."""
    return clamp((t - a) / (b - a)) if b > a else float(t >= b)


def ease(p):
    """Smooth in and out (cubic)."""
    p = clamp(p)
    return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2


def ease_out(p):
    p = clamp(p)
    return 1 - (1 - p) ** 3


def ease_in(p):
    return clamp(p) ** 3


def back_out(p, s=1.7):
    """Overshoots a little and settles: the pop used for cards, chips and pop-ups."""
    p = clamp(p) - 1
    return 1 + (s + 1) * p ** 3 + s * p ** 2


def lerp(a, b, p):
    return a + (b - a) * p


def lerp2(p0, p1, p):
    return (lerp(p0[0], p1[0], p), lerp(p0[1], p1[1], p))


def bez(p0, c1, c2, p3, p):
    """Point on a cubic Bezier."""
    q = 1 - p
    return tuple(q ** 3 * p0[i] + 3 * q * q * p * c1[i] + 3 * q * p * p * c2[i] + p ** 3 * p3[i] for i in (0, 1))


def hop(t, t0, period=0.42, height=46, n=2):
    """Height above the floor of n hops starting at t0 (0 outside them)."""
    u = (t - t0) / period
    if u < 0 or u >= n:
        return 0.0
    return height * math.sin(math.pi * (u % 1))


def wobble(t, amp=1.0, hz=1.6, phase=0.0):
    return amp * math.sin(2 * math.pi * hz * t + phase)


def pop(inner, cx, cy, p, rot0=0):
    """inner scaled about (cx, cy) with the overshoot pop; nothing drawn while p <= 0."""
    if p <= 0:
        return ''
    k = max(0.001, back_out(p))
    r = rot0 * (1 - clamp(p))
    return f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({r:.1f}) scale({k:.3f}) translate({-cx:.1f} {-cy:.1f})" opacity="{clamp(p * 3):.2f}">{inner}</g>'


def fade(inner, a):
    a = clamp(a)
    return '' if a <= 0 else (inner if a >= 1 else f'<g opacity="{a:.2f}">{inner}</g>')


def shift(inner, dx, dy):
    return f'<g transform="translate({dx:.1f} {dy:.1f})">{inner}</g>'


def squash(inner, cx, floor_y, k):
    """Squash and stretch about the feet: k > 1 is taller and thinner. Keep |k - 1| <= 0.06 so Ledger's proportions hold."""
    k = clamp(k, 0.94, 1.06)
    return f'<g transform="translate({cx:.1f} {floor_y:.1f}) scale({1 / k:.3f} {k:.3f}) translate({-cx:.1f} {-floor_y:.1f})">{inner}</g>'
