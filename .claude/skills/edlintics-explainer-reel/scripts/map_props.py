"""Map reels (13 Nov 2026, opt-in: nothing changes unless a script uses these names).

Hoang, 13 Nov 2026, on a "best cities for careers" reference: "create a cities map in the world for career ... Make it like a map video
with Ledger explain and graphic of important iconic monument, skytower, building of that city".
Props added here and installed into scene_lib by install(): world_map, map_pin, map_dot, map_label, map_plate, flight_path, suitcase, landmark, cloud, plane, cargo_ship.
Land outlines: map_land.json, simplified from Natural Earth 1:50m land (public domain). Coastlines only: no country borders are
drawn and nothing but cities is labelled.

Projection (shared with the script generator through map_xy): a view is {"lon", "lat", "k", "x", "y"}: the point (lon, lat) sits at
screen (x, y) and one degree of longitude is k pixels; latitude is stretched by 1 / cos(lat) so shapes look natural near the view centre.
"""
import json, math, os

_LAND = None
SEA = "#D3E4FA"; LAND = "#FBF4DF"; SHADE = "#B4CDEF"


def _land():
    global _LAND
    if _LAND is None: _LAND = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "map_land.json")))
    return _LAND


def map_ky(view):
    return view["k"] / max(0.5, math.cos(math.radians(view["lat"])))


def map_xy(lon, lat, view):
    """Screen position of (lon, lat) in a view {"lon", "lat", "k", "x", "y"}."""
    return view["x"] + (lon - view["lon"]) * view["k"], view["y"] - (lat - view["lat"]) * map_ky(view)


def _clip(poly, x0, y0, x1, y1):
    """Sutherland-Hodgman: clip a polygon to a rectangle."""
    def cut(pts, inside, inter):
        out = []
        for i, p in enumerate(pts):
            q = pts[i - 1]
            if inside(p):
                if not inside(q): out.append(inter(q, p))
                out.append(p)
            elif inside(q): out.append(inter(q, p))
        return out
    def ix(v):
        return lambda a, b: (v, a[1] + (b[1] - a[1]) * (v - a[0]) / ((b[0] - a[0]) or 1e-9))
    def iy(v):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (v - a[1]) / ((b[1] - a[1]) or 1e-9), v)
    for inside, inter in ((lambda p: p[0] >= x0, ix(x0)), (lambda p: p[0] <= x1, ix(x1)), (lambda p: p[1] >= y0, iy(y0)), (lambda p: p[1] <= y1, iy(y1))):
        if len(poly) < 3: return []
        poly = cut(poly, inside, inter)
    return poly


def _dp(pts, tol):
    if len(pts) < 3: return pts
    keep = [False] * len(pts); keep[0] = keep[-1] = True; st = [(0, len(pts) - 1)]
    while st:
        a, b = st.pop(); ax, ay = pts[a]; bx, by = pts[b]; dx, dy = bx - ax, by - ay; L = math.hypot(dx, dy) or 1e-9; md = 0; mi = None
        for i in range(a + 1, b):
            d = abs((pts[i][0] - ax) * dy - (pts[i][1] - ay) * dx) / L if L > 1e-6 else math.hypot(pts[i][0] - ax, pts[i][1] - ay)
            if d > md: md, mi = d, i
        if mi is not None and md > tol: keep[mi] = True; st += [(a, mi), (mi, b)]
    return [p for p, k in zip(pts, keep) if k]


def install(G):
    """Register the map props in scene_lib (G = its globals)."""
    _f, _g, _t, _d_tw, _appear = G["_f"], G["_g"], G["_t"], G["_d_tw"], G["_appear"]
    INK, BLUE, PAPER, GOLD, GREY, WHITE, CORAL, LB, GREEN = (G[k] for k in ("INK", "BLUE", "PAPER", "GOLD", "GREY", "WHITE", "CORAL", "LB", "GREEN"))
    YEL = "#FFD45C"

    def world_map(x, y, s=1.0, lon=0, lat=30, k=3.0, box=None, sea=True, grid=True, **_):
        """A hand-drawn map of the world or a region (map reels): pale sea, cream land with an ink coast, no country borders and no labels. (x, y) = where the point (lon, lat) sits; k = pixels per degree of longitude. box [x0, y0, x1, y1]: the part of the screen it fills (default: the whole 1080x1920 frame and a margin). Place pins with map_props.map_xy."""
        v = {"lon": lon, "lat": lat, "k": k, "x": x, "y": y}; ky = map_ky(v)
        x0, y0, x1, y1 = box or (-160, -200, 1240, 2120)
        out = f'<rect x="{_f(x0)}" y="{_f(y0)}" width="{_f(x1 - x0)}" height="{_f(y1 - y0)}" fill="{SEA}" stroke="none"/>' if sea else ""
        if grid:   # faint graticule, every 10 or 30 degrees
            st = 30 if k < 7 else 10 if k < 28 else 5; g = ""
            lo = math.floor((lon + (x0 - x) / k) / st) * st
            while lo <= lon + (x1 - x) / k:
                gx = x + (lo - lon) * k
                if x0 < gx < x1: g += f'M{_f(gx)} {_f(y0)} V{_f(y1)} '
                lo += st
            la = math.floor((lat - (y1 - y) / ky) / st) * st
            while la <= lat - (y0 - y) / ky:
                gy = y - (la - lat) * ky
                if y0 < gy < y1: g += f'M{_f(x0)} {_f(gy)} H{_f(x1)} '
                la += st
            out += f'<path data-nodraw="1" d="{g}" fill="none" stroke="{WHITE}" stroke-width="3" opacity="0.55"/>'
        shade = land = ""
        for ring in _land():
            lons = [p[0] for p in ring]; lats = [p[1] for p in ring]
            if x + (max(lons) - lon) * k < x0 or x + (min(lons) - lon) * k > x1 or y - (max(lats) - lat) * ky > y1 or y - (min(lats) - lat) * ky < y0: continue
            if (max(lons) - min(lons)) * k < 9 and (max(lats) - min(lats)) * ky < 9: continue   # specks
            pts = [(x + (a - lon) * k, y - (b - lat) * ky) for a, b in ring]
            pts = _clip(pts, x0 - 40, y0 - 40, x1 + 40, y1 + 40)
            if len(pts) < 3: continue
            pts = _dp(pts + [pts[0]], 1.6)[:-1]
            if len(pts) < 3: continue
            d = "M" + " L".join(f"{_f(px)} {_f(py)}" for px, py in pts) + " Z "
            land += d
        if land:
            out += (f'<path data-nodraw="1" d="{land}" transform="translate(7 9)" fill="{SHADE}" stroke="none"/>'
                    f'<path data-nodraw="1" d="{land}" fill="{LAND}" stroke="{INK}" stroke-width="{4 if k >= 7 else 3}" stroke-linejoin="round"/>')
        if box:
            return f'<g><svg x="{_f(x0)}" y="{_f(y0)}" width="{_f(x1 - x0)}" height="{_f(y1 - y0)}" viewBox="{_f(x0)} {_f(y0)} {_f(x1 - x0)} {_f(y1 - y0)}" overflow="hidden">{out}</svg></g><rect x="{_f(x0)}" y="{_f(y0)}" width="{_f(x1 - x0)}" height="{_f(y1 - y0)}" rx="26" fill="none" stroke="{INK}" stroke-width="6"/>'
        return out

    def world_map_box(x, y, s=1.0, box=None, **_):
        b = box or (0, 0, 1080, 1920)
        return [b[0], b[1], b[2] - b[0], b[3] - b[1]]

    def _pin_shape(col, z=1.0):
        return (f'<ellipse cx="0" cy="2" rx="{_f(13 * z)}" ry="{_f(5 * z)}" fill="{INK}" opacity="0.22"/>'
                f'<path d="M0 0 C{_f(-8 * z)} {_f(-20 * z)} {_f(-26 * z)} {_f(-32 * z)} {_f(-26 * z)} {_f(-54 * z)} A{_f(26 * z)} {_f(26 * z)} 0 1 1 {_f(26 * z)} {_f(-54 * z)} C{_f(26 * z)} {_f(-32 * z)} {_f(8 * z)} {_f(-20 * z)} 0 0 Z" fill="{col}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
                f'<circle cx="0" cy="{_f(-54 * z)}" r="{_f(9.5 * z)}" fill="{WHITE}" stroke="{INK}" stroke-width="3.5"/>')

    def _pin_label(label, side, fs, fill, z):
        if not label: return 0, 0, 0, 0, ""
        W = _d_tw(label, fs) + 34; H = fs * 1.5
        cx, cy = {"r": (34 * z + W / 2, -44 * z), "l": (-34 * z - W / 2, -44 * z), "t": (0, -92 * z - H / 2), "b": (0, 16 + H / 2),
                  "tr": (20 * z + W / 2, -92 * z - H / 2 + 14), "tl": (-20 * z - W / 2, -92 * z - H / 2 + 14), "br": (16 + W / 2, 12 + H / 2), "bl": (-16 - W / 2, 12 + H / 2)}[side]
        return cx, cy, W, H, (f'<rect x="{_f(cx - W / 2)}" y="{_f(cy - H / 2)}" width="{_f(W)}" height="{_f(H)}" rx="{_f(H / 2)}" fill="{fill}" stroke="{INK}" stroke-width="4"/>'
                              + _t(cx, cy + fs * 0.36, str(label), fs, 900, INK))

    def map_pin(x, y, s=1.0, label="", state="done", side="r", fs=34, num=None, **_):
        """A city pin on the world_map. (x, y) = the pin's point (the city). label: the city name in a pill beside it (side r, l, t, b, tr, tl, br, bl). state: done (blue: visited), now (coral pin, yellow label: where Ledger lands) or todo (grey). num: a small number in the pin head (the summary map)."""
        if state not in ("done", "now", "todo"): raise ValueError(f"map_pin: state {state!r}; use done, now or todo")
        col, fill, z = {"done": (BLUE, WHITE, 0.82), "now": ("#E8553B", YEL, 1.12), "todo": (GREY, WHITE, 0.82)}[state]
        out = _pin_shape(col, z)
        if num is not None:
            out += f'<circle cx="0" cy="{_f(-54 * z)}" r="{_f(17 * z)}" fill="{WHITE}" stroke="{INK}" stroke-width="3.5"/>' + _t(0, -54 * z + 9 * z, str(num), 26 * z, 900, INK)
        out += _pin_label(label, side, fs, fill, z)[4]
        return _g(x, y, s, out)

    def map_pin_box(x, y, s=1.0, label="", state="done", side="r", fs=34, **_):
        z = 1.12 if state == "now" else 0.82; cx, cy, W, H, _s = _pin_label(label, side, fs, WHITE, z)
        xa = min(-28 * z, cx - W / 2); xb = max(28 * z, cx + W / 2); ya = min(-82 * z, cy - H / 2); yb = max(6, cy + H / 2)
        return [x + xa * s, y + ya * s, (xb - xa) * s, (yb - ya) * s]

    def flight_path(x, y, s=1.0, to=None, arc=120, n=0, color="blue", grow=None, **_):
        """A dotted flight path from (x, y) to "to": [x, y], bowed upward by arc pixels (the same curve as a "move" with that arc). grow {"at": "chunk:N", "delay": s, "dur": s}: the dots appear one after another over dur seconds, in step with a mover; left out: all drawn from the first frame (a leg already flown)."""
        if not (isinstance(to, (list, tuple)) and len(to) == 2): raise ValueError('flight_path needs "to": [x, y]')
        col = {"blue": BLUE, "ink": INK, "coral": "#E8553B", "grey": GREY}.get(color, color)
        x1, y1 = to; cx, cy = (x + x1) / 2, (y + y1) / 2 - arc
        L = math.hypot(x1 - x, y1 - y) + abs(arc) * 0.6; n = int(n) or max(4, int(L / 30)); out = ""
        for i in range(1, n):
            u = i / n; w = 1 - u; px = w * w * x + 2 * w * u * cx + u * u * x1; py = w * w * y + 2 * w * u * cy + u * u * y1
            dot = f'<circle cx="{_f(px)}" cy="{_f(py)}" r="7.5" fill="{col}" stroke="{INK}" stroke-width="2.5"/>'
            out += _appear(dot, dict(grow, every=float(grow.get("dur", 0.9)) / n) if grow else None, i, px, py)
        return out

    def flight_path_box(x, y, s=1.0, to=None, arc=120, **_):
        x1, y1 = to or (x, y)
        return [min(x, x1) - 10, min(y, y1) - abs(arc) / 2 - 10, abs(x1 - x) + 20, abs(y1 - y) + abs(arc) / 2 + 20]

    def suitcase(x, y, s=1.0, color="coral", **_):
        """A small travel suitcase with a pull handle and two wheels (no logo). (x, y) = the ground under it. color: coral, blue, gold, green."""
        c = {"coral": "#E8765F", "blue": BLUE, "gold": "#E9B949", "green": GREEN}.get(color, color)
        return _g(x, y, s, f'<path d="M-16 -92 V-124 H16 V-92" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
                           f'<rect x="-36" y="-94" width="72" height="84" rx="12" fill="{c}" stroke="{INK}" stroke-width="5"/>'
                           f'<path d="M-14 -94 V-10 M14 -94 V-10" stroke="{INK}" stroke-width="3.5" opacity="0.45"/><rect x="-10" y="-66" width="20" height="14" rx="3" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>'
                           f'<circle cx="-22" cy="-5" r="7" fill="{INK}"/><circle cx="22" cy="-5" r="7" fill="{INK}"/>')

    def cloud(x, y, s=1.0, **_):
        """A small white cloud for a city sky. (x, y) = centre."""
        return _g(x, y, s, f'<path d="M-80 20 Q-110 20 -106 -6 Q-104 -30 -74 -28 Q-66 -62 -26 -56 Q-2 -84 34 -62 Q74 -70 82 -34 Q112 -30 108 -2 Q106 20 80 20 Z" fill="{WHITE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')

    def map_label(x, y, s=1.0, city="", career="", w=420, fs=34, to=None, num=None, **_):
        """A legend row for the summary map: a white pill with a numbered blue dot, the city in bold and its career in blue. (x, y) = centre. to [x, y]: a thin leader line from the pill to that point (the city's pin)."""
        H = fs * 1.62; out = ""
        if to: out += f'<path d="M0 0 L{_f((to[0] - x) / s)} {_f((to[1] - y) / s)}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" opacity="0.6"/>'
        need = (H if num is not None else 22) + _d_tw(city, fs) + 14 + _d_tw(career, fs) + 22
        if need > w: raise ValueError(f"map_label: {city!r} + {career!r} needs {need:.0f} px but w is {w}; shorten the career or raise w")
        out += f'<rect x="{_f(-w / 2)}" y="{_f(-H / 2)}" width="{_f(w)}" height="{_f(H)}" rx="{_f(H / 2)}" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>'
        tx = -w / 2 + 22
        if num is not None:
            out += f'<circle cx="{_f(-w / 2 + H / 2)}" cy="0" r="{_f(H / 2 - 7)}" fill="{BLUE}" stroke="{INK}" stroke-width="3"/>' + _t(-w / 2 + H / 2, fs * 0.3, str(num), fs * 0.8, 900, WHITE)
            tx = -w / 2 + H + 4
        out += _t(tx, fs * 0.36, str(city), fs, 900, INK, "start") + _t(tx + _d_tw(city, fs) + 14, fs * 0.36, str(career), fs, 800, G["ED_BLUE"], "start")
        return _g(x, y, s, out)

    def map_label_box(x, y, s=1.0, w=420, fs=34, **_):
        return [x - w / 2 * s, y - fs * 0.81 * s, w * s, fs * 1.62 * s]

    def map_plate(x, y, s=1.0, w=190, h=58, **_):
        """A soft paper plate to put under the corner logo on a busy map scene (the logo is at x 768-928, y 468-510 in the bleed layout). (x, y) = centre."""
        return f'<rect data-nodraw="1" x="{_f(x - w / 2)}" y="{_f(y - h / 2)}" width="{_f(w)}" height="{_f(h)}" rx="{_f(h / 2)}" fill="{PAPER}" fill-opacity="0.92" stroke="none"/>'

    def map_dot(x, y, s=1.0, num=1, dx=0, dy=-60, state="done", **_):
        """A small city dot for the summary map, with a numbered badge set off by (dx, dy) and joined to it by a thin line, so close cities stay readable. (x, y) = the city. num None: only the small dot (a city from an earlier part of a series)."""
        col = {"done": BLUE, "now": "#E8553B", "todo": GREY}.get(state, BLUE)
        if num is None: return _g(x, y, s, f'<circle r="9" fill="{col}" stroke="{INK}" stroke-width="3"/>')   # a plain lit dot (cities of earlier parts of a series)
        return _g(x, y, s, f'<path d="M0 0 L{_f(dx)} {_f(dy)}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/><circle r="8" fill="{col}" stroke="{INK}" stroke-width="3"/>'
                           f'<circle cx="{_f(dx)}" cy="{_f(dy)}" r="26" fill="{col}" stroke="{INK}" stroke-width="4"/>' + _t(dx, dy + 12, str(num), 34, 900, WHITE))

    def map_dot_box(x, y, s=1.0, dx=0, dy=-60, **_):
        return [x + (min(0, dx) - 26) * s, y + (min(0, dy) - 26) * s, (abs(dx) + 52) * s, (abs(dy) + 52) * s]

    def plane(x, y, s=1.0, flip=False, **_):
        """A small passenger jet seen from the side, climbing (no airline marks). (x, y) = centre. flip: faces left."""
        o = (f'<path d="M-120 10 Q-124 -14 -92 -18 L70 -30 Q118 -30 132 -8 Q118 14 70 16 Z" fill="{WHITE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             f'<path d="M-104 -16 L-134 -70 L-100 -70 L-60 -20 Z" fill="{BLUE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             f'<path d="M-10 2 L-70 62 L-34 62 L44 4 Z" fill="{BLUE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             f'<path d="M-40 -14 H60" stroke="{INK}" stroke-width="4" stroke-dasharray="10 12" stroke-linecap="round"/><path d="M92 -22 L112 -12" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
        return f'<g transform="translate({_f(x)} {_f(y)}) rotate({12 if flip else -12}) scale({-s if flip else s} {s})">{o}</g>'

    def cargo_ship(x, y, s=1.0, **_):
        """A small container ship, side view, with stacked coloured containers (no markings). (x, y) = centre of the waterline."""
        o = f'<path d="M-170 -44 H170 L140 6 H-150 Z" fill="#33435E" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/><rect x="96" y="-108" width="44" height="64" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>'
        cols = ["#E8765F", BLUE, "#E9B949", GREEN, BLUE, "#E8765F", "#E9B949", GREEN]
        o += "".join(f'<rect x="{-150 + (i % 4) * 58}" y="{-74 - (i // 4) * 30}" width="54" height="28" fill="{cols[i]}" stroke="{INK}" stroke-width="3.5"/>' for i in range(8))
        return _g(x, y, s, o)

    def delivery_van(x, y, s=1.0, flip=False, color=None, **_):
        """A delivery van, side view, with a parcel mark on its side (no brand; 13 Nov 2026). (x, y) = centre of the road under its wheels. flip faces left. color: body fill."""
        c = color or WHITE
        o = (f'<path d="M-250 -50 V-250 Q-250 -270 -230 -270 H70 V-50 Z" fill="{c}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
             f'<path d="M70 -50 V-215 H150 Q170 -215 182 -198 L236 -128 Q250 -120 250 -100 V-50 Z" fill="{BLUE}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
             f'<path d="M96 -130 V-190 H146 Q156 -190 163 -181 L200 -130 Z" fill="{G["SKY"]}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
             f'<rect x="-140" y="-212" width="96" height="96" rx="8" fill="#D9A04A" stroke="{INK}" stroke-width="4"/><path d="M-92 -212 V-116 M-140 -164 H-44" stroke="{INK}" stroke-width="3.5" opacity="0.55"/>'
             f'<path d="M-250 -92 H70" stroke="{INK}" stroke-width="3" opacity="0.35"/><circle cx="238" cy="-92" r="8" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>'
             f'<circle cx="-150" cy="-40" r="40" fill="{INK}"/><circle cx="-150" cy="-40" r="15" fill="{GREY}"/><circle cx="150" cy="-40" r="40" fill="{INK}"/><circle cx="150" cy="-40" r="15" fill="{GREY}"/>')
        if flip: o = f'<g transform="scale(-1 1)">{o}</g>'
        return _g(x, y, s, o)

    # ---- landmarks: generic silhouettes, line art with flat fills, no logos or names. (x, y) = centre of the base on the ground
    def P(d, fill="none", sw=5, stroke=None, extra=""):
        return f'<path d="{d}" fill="{fill}" stroke="{stroke or INK}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"{extra}/>'

    def R(x0, y0, w, h, fill, sw=5, rx=0):
        return f'<rect x="{_f(x0)}" y="{_f(y0)}" width="{_f(w)}" height="{_f(h)}" rx="{rx}" fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'

    def win(x0, x1, y0, y1, nx, ny, op=0.4, sw=3):
        d = "".join(f"M{_f(x0 + (x1 - x0) * i / nx)} {_f(y0)} V{_f(y1)} " for i in range(1, nx)) + "".join(f"M{_f(x0)} {_f(y0 + (y1 - y0) * j / ny)} H{_f(x1)} " for j in range(1, ny))
        return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{sw}" opacity="{op}"/>'

    def water(w, y=0):
        return (f'<rect x="{_f(-w / 2)}" y="{_f(y - 6)}" width="{_f(w)}" height="46" rx="12" fill="#9CC3F0" stroke="{INK}" stroke-width="4"/>'
                + P(f"M{_f(-w / 2 + 30)} {y + 14} q18 -12 36 0 t36 0 M{_f(w / 2 - 150)} {y + 22} q18 -12 36 0 t36 0 t36 0 M-40 {y + 18} q18 -12 36 0 t36 0", "none", 3.5, WHITE))

    def lm_golden_gate():
        red = "#E0563B"; o = water(700, -4)
        o += P("M-350 -150 Q-262 -190 -170 -400 Q0 -120 170 -400 Q262 -190 350 -150", "none", 6, red)
        o += "".join(P(f"M{xx} -128 V{_f(-128 - h)}", "none", 3, red) for xx, h in ((-120, 150), (-80, 78), (-40, 34), (0, 18), (40, 34), (80, 78), (120, 150), (-225, 105), (-275, 48), (225, 105), (275, 48)))
        for tx in (-170, 170):
            o += R(tx - 26, -410, 16, 410, red, 4) + R(tx + 10, -410, 16, 410, red, 4)
            o += "".join(R(tx - 12, yy, 24, 16, red, 4) for yy in (-400, -320, -240, -90))
        o += R(-350, -128, 700, 22, red, 5, 6)
        return o, (-350, -420, 700, 460)

    def lm_big_ben():
        st = "#EAD9A6"; dk = "#59647A"
        o = R(-250, -150, 190, 150, st) + win(-250, -60, -150, 0, 6, 2)
        o += "".join(P(f"M{xx} -150 l12 -40 l12 40", st, 4) for xx in (-250, -190, -130, -84))
        o += R(-56, -470, 112, 470, st) + win(-56, 56, -470, 0, 4, 1, 0.35) + P("M-56 -120 H56 M-56 -300 H56", "none", 3.5)
        o += R(-68, -610, 136, 140, st) + f'<circle cx="0" cy="-540" r="48" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>' + P("M0 -540 V-574 M0 -540 L22 -528", "none", 5)
        o += f'<circle cx="0" cy="-540" r="5" fill="{INK}"/>'
        o += R(-58, -660, 116, 50, GOLD, 4) + win(-58, 58, -660, -610, 5, 1, 0.5)
        o += P("M-68 -660 L-34 -740 H34 L68 -660 Z", dk) + R(-26, -772, 52, 32, GOLD, 4) + P("M-30 -772 L0 -860 L30 -772 Z", dk) + P("M0 -860 V-892", "none", 5)
        return o, (-255, -895, 330, 900)

    def lm_eiffel():
        br = "#B98D5C"
        o = P("M-200 0 Q-92 -150 -62 -330 L-30 -560 L-14 -700 L0 -790 L14 -700 L30 -560 L62 -330 Q92 -150 200 0 L128 0 Q100 -150 0 -158 Q-100 -150 -128 0 Z", br, 5)
        o += P("M-52 -330 L52 -330 M-46 -380 L46 -380 M-52 -330 L46 -380 M52 -330 L-46 -380 M-36 -470 L36 -470 M-36 -470 L30 -560 M36 -470 L-30 -560 M-150 -60 L-104 -160 M150 -60 L104 -160 M-118 -110 L-82 -200 M118 -110 L82 -200", "none", 3, INK, ' opacity="0.55"')
        o += R(-108, -222, 216, 26, br, 5, 6) + R(-66, -350, 132, 22, br, 5, 6) + R(-24, -706, 48, 16, br, 4, 4) + P("M0 -790 V-850", "none", 5)
        return o, (-205, -855, 410, 860)

    def lm_erasmus():
        o = water(700, -4) + R(-350, -96, 700, 18, "#E8EEF7", 5, 5)
        o += "".join(P(f"M-56 -{_f(560 - i * 34)} L{_f(60 + i * 30)} -96", "none", 3, "#6F7C92") for i in range(9))
        o += P("M-150 -96 L-96 -330 L-70 -600 L-34 -600 L-40 -330 L-70 -96 Z", "#DCEBFA") + P("M-150 -96 L-220 -96 L-190 -150 Z", "#DCEBFA", 4) + P("M-96 -330 L-200 -110", "none", 4)
        o += "".join(R(xx, -96, 26, 96, "#C9D4E3", 4) for xx in (-200, 120, 280))
        o += R(170, -220, 70, 124, LB, 4) + win(170, 240, -220, -96, 3, 5) + R(250, -280, 60, 184, "#E8EEF7", 4) + win(250, 310, -280, -96, 2, 7)
        return o, (-350, -605, 700, 650)

    def lm_euro():
        blue = "#2F5FD0"
        o = R(-250, -520, 110, 520, "#CBD9EE") + win(-250, -140, -520, 0, 3, 13) + P("M-250 -520 L-195 -590 L-140 -520 Z", "#AFC3E2")
        o += R(150, -640, 96, 640, "#DCE6F5") + win(150, 246, -640, 0, 3, 16) + P("M198 -640 V-720", "none", 5)
        o += R(-120, -420, 90, 420, "#E7EDF7") + win(-120, -30, -420, 0, 3, 10) + R(40, -330, 90, 330, "#BFD0EA") + win(40, 130, -330, 0, 3, 8)
        o += R(-50, -40, 100, 40, GREY, 4, 4)
        o += f'<circle cx="0" cy="-190" r="150" fill="{PAPER}" fill-opacity="0.9" stroke="{INK}" stroke-width="5"/>'
        o += P("M78 -262 A96 96 0 1 0 78 -118", "none", 44, INK) + P("M78 -262 A96 96 0 1 0 78 -118", "none", 34, blue)
        o += P("M-110 -212 H40 M-110 -168 H24", "none", 36, INK) + P("M-106 -212 H36 M-106 -168 H20", "none", 26, blue)
        for i in range(12):
            a = math.pi * 2 * i / 12; sx, sy = 124 * math.cos(a), -190 + 124 * math.sin(a)
            o += f'<path d="M{_f(sx)} {_f(sy - 15)} l4.4 9.6 10.4 1.2 -7.8 7 2.2 10.4 -9.2 -5.4 -9.2 5.4 2.2 -10.4 -7.8 -7 10.4 -1.2 Z" fill="#F7C531" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
        return o, (-255, -725, 505, 730)

    def lm_minster():
        rs = "#C97A5E"; o = water(620, -4)
        o += R(-150, -250, 360, 250, rs) + P("M-150 -250 L30 -360 L210 -250 Z", "#E9B949")
        o += "".join(P(f"M{-110 + i * 46} -256 l23 -14 l23 14 M{-87 + i * 46} -284 l23 -14 l23 14", "none", 3, "#2FA36B") for i in range(6))
        o += "".join(P(f"M{xx} 0 V-120 Q{xx + 22} -160 {xx + 44} -120 V0 Z", "#7C8FB5", 4) for xx in (-110, -30, 50, 130))
        for tx in (-230, -90):
            o += R(tx, -430, 96, 430, rs) + P(f"M{tx + 28} -330 V-380 Q{tx + 48} -410 {tx + 68} -380 V-330 Z", "#7C8FB5", 4) + P(f"M{tx} -250 H{tx + 96}", "none", 3.5)
            o += P(f"M{tx - 6} -430 L{tx + 48} -660 L{tx + 102} -430 Z", rs) + P(f"M{tx + 48} -660 V-700 M{tx + 36} -684 H{tx + 60}", "none", 5) + P(f"M{tx + 20} -490 H{tx + 76} M{tx + 32} -550 H{tx + 64}", "none", 3.5, INK, ' opacity="0.5"')
        o += f'<circle cx="-86" cy="-150" r="30" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>' + P("M-86 -180 V-120 M-116 -150 H-56", "none", 3)
        return o, (-310, -705, 620, 750)

    def lm_burj():
        gl = "#BCD3F0"
        o = R(-250, -260, 90, 260, "#DCE6F5") + win(-250, -160, -260, 0, 3, 7) + R(170, -340, 86, 340, "#E7EDF7") + win(170, 256, -340, 0, 3, 9) + R(-150, -170, 70, 170, "#CBD9EE", 4)
        L = [(-92, 0), (-92, -130), (-74, -130), (-74, -270), (-58, -270), (-58, -400), (-42, -400), (-42, -520), (-28, -520), (-28, -630), (-16, -630), (-16, -730), (-7, -730), (-7, -820), (0, -900)]
        pts = L + [(-px, py) for px, py in reversed(L[:-1])]
        o += P("M" + " L".join(f"{a} {b}" for a, b in pts) + " Z", gl) + P("M0 -880 V0 M-40 -400 V0 M40 -400 V0", "none", 3, INK, ' opacity="0.4"')
        o += P("M-74 -200 H74 M-58 -335 H58 M-42 -460 H42 M-28 -575 H28", "none", 3, INK, ' opacity="0.4"') + P("M0 -900 V-950", "none", 4)
        o += P("M-330 0 q20 -50 0 -90 M-330 -90 q-40 -18 -62 6 M-330 -90 q-30 -40 -64 -30 M-330 -90 q40 -18 62 6 M-330 -90 q30 -40 64 -30", "none", 6, "#2FA36B")
        return o, (-395, -955, 655, 960)

    def lm_mbs():
        gl = "#C5DBF4"; o = water(640, -4)
        for tx in (-190, 0, 190):
            o += P(f"M{tx - 62} -6 L{tx - 40} -430 L{tx + 40} -430 L{tx + 62} -6 Z", gl) + win(tx - 46, tx + 46, -420, -10, 3, 9, 0.38)
        o += P("M-300 -470 Q-310 -430 -260 -430 H250 Q330 -432 350 -480 Z", "#F4F8FF") + P("M-250 -470 q8 -34 0 -50 M-250 -520 q-22 -8 -34 6 M-250 -520 q22 -8 34 6 M40 -474 q8 -34 0 -50 M40 -524 q-22 -8 -34 6 M40 -524 q22 -8 34 6 M240 -476 q8 -30 0 -44 M240 -520 q-20 -8 -30 6 M240 -520 q20 -8 30 6", "none", 5, "#2FA36B")
        o += f'<path d="M-330 -4 q14 -70 62 -84 q-8 44 -62 84 Z M-330 -4 q-8 -66 -52 -92 q0 48 52 92 Z M-330 -4 q-2 -80 12 -118 q14 40 -12 118 Z" fill="{WHITE}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        return o, (-385, -530, 740, 575)

    def lm_hk():
        gl = "#BFD6F2"; o = P("M-360 -6 Q-250 -330 -120 -300 Q20 -420 150 -280 Q270 -300 360 -6 Z", "#BFE0C4", 4) + water(720, -4)
        o += R(-300, -250, 84, 246, "#E7EDF7") + win(-300, -216, -250, -6, 3, 7) + R(-200, -340, 70, 336, "#CBD9EE") + win(-200, -130, -340, -6, 2, 9)
        o += R(150, -420, 84, 416, "#DCE6F5") + win(150, 234, -420, -6, 3, 11) + P("M150 -420 Q192 -480 234 -420 Z", "#DCE6F5") + R(250, -220, 70, 216, "#E7EDF7") + win(250, 320, -220, -6, 2, 6)
        o += P("M-70 -6 V-560 L0 -640 V-480 L70 -400 V-6 Z", gl) + P("M-70 -6 L70 -150 M70 -150 L-70 -290 M-70 -290 L70 -400 M-70 -420 L0 -480 M-70 -560 L0 -480 M0 -480 V-6 M-70 -150 L70 -6 M-70 -290 L70 -150", "none", 3.5, WHITE)
        o += P("M-70 -6 V-560 L0 -640 V-480 L70 -400 V-6 Z", "none") + P("M-22 -618 V-720 M-48 -588 V-680", "none", 4)
        o += P("M-250 30 Q-200 62 -110 30 Z", "#8A5A3C", 4) + P("M-180 30 V-112", "none", 5) + P("M-176 -112 Q-104 -90 -112 0 L-176 4 Z M-186 -96 Q-246 -70 -240 0 L-186 4 Z", "#D8433B", 4) + P("M-170 -76 L-110 -62 M-172 -40 L-112 -30 M-190 -60 L-238 -44", "none", 3)
        return o, (-365, -725, 730, 795)

    def lm_fab():
        o = R(-320, -240, 420, 240, "#E7EDF7") + R(-320, -280, 420, 44, "#BFD0EA") + win(-320, 100, -200, -60, 7, 2)
        o += R(-260, -60, 70, 60, "#7C8FB5", 4) + "".join(R(xx, -350, 44, 72, "#CBD9EE", 4, 6) for xx in (-280, -210, -140))
        o += R(100, -420, 150, 420, "#CBD9EE") + win(100, 250, -420, 0, 3, 9) + P("M-330 0 q-14 -44 0 -72 q14 28 0 72 M270 0 q-18 -60 0 -104 q18 44 0 104", "#8FCBA0", 4)
        # a large microchip held up like a sign in front of the plant
        o += P("M20 -150 V-40", "none", 8) + R(-104, -350, 248, 248, "#33435E", 6, 18) + R(-58, -304, 156, 156, GOLD, 5, 8)
        o += P("M-10 -256 H50 V-196 H-10 Z M-58 -226 H-10 M50 -226 H98 M20 -304 V-256 M20 -196 V-148", "none", 4)
        o += "".join(P(f"M{-80 + i * 50} -350 v-26 M{-80 + i * 50} -102 v26 M-104 {-326 + i * 50} h-26 M144 {-326 + i * 50} h26", "none", 7) for i in range(5))
        return o, (-345, -425, 600, 430)

    def lm_tokyo_tower():
        rd = "#E8553B"
        o = R(-260, -200, 90, 200, "#E7EDF7") + win(-260, -170, -200, 0, 3, 5) + R(170, -280, 90, 280, "#DCE6F5") + win(170, 260, -280, 0, 3, 7)
        o += P("M-170 0 Q-74 -170 -50 -340 L-24 -600 L-10 -730 L0 -800 L10 -730 L24 -600 L50 -340 Q74 -170 170 0 L112 0 Q86 -140 0 -150 Q-86 -140 -112 0 Z", rd)
        o += P("M-36 -470 L-24 -600 H24 L36 -470 Z M-12 -700 L0 -800 L12 -700 Z", WHITE) + P("M-50 -340 L-58 -260 H58 L50 -340 Z", WHITE, 4)
        o += P("M-56 -260 L44 -340 M56 -260 L-44 -340 M-40 -400 L34 -470 M40 -400 L-34 -470 M-130 -60 L-88 -150 M130 -60 L88 -150", "none", 3, INK, ' opacity="0.5"')
        o += R(-78, -236, 156, 34, WHITE, 5, 5) + win(-78, 78, -236, -202, 6, 1, 0.5) + R(-40, -486, 80, 22, WHITE, 4, 4) + P("M0 -800 V-870", "none", 5)
        o += f'<circle cx="-250" cy="-560" r="54" fill="#F6B7C4" stroke="{INK}" stroke-width="4"/><circle cx="-190" cy="-520" r="40" fill="#F9CAD4" stroke="{INK}" stroke-width="4"/>' + P("M-232 -510 Q-226 -300 -250 0", "none", 9, "#8A5A3C")
        return o, (-310, -875, 575, 880)

    def lm_empire():
        st = "#D7DDE8"
        o = R(-250, -220, 100, 220, "#E7EDF7") + win(-250, -150, -220, 0, 3, 6) + R(160, -300, 96, 300, "#CBD9EE") + win(160, 256, -300, 0, 3, 8)
        o += R(-130, -150, 260, 150, st) + R(-98, -430, 196, 280, st) + R(-70, -580, 140, 150, st) + R(-44, -650, 88, 70, st) + R(-22, -700, 44, 50, "#BFC8D8") + P("M-14 -700 L0 -770 L14 -700 Z", "#BFC8D8", 4) + P("M0 -770 V-880", "none", 5)
        o += win(-98, 98, -430, -150, 7, 1, 0.4) + win(-70, 70, -580, -430, 5, 1, 0.4) + win(-130, 130, -150, 0, 9, 1, 0.4)
        return o, (-255, -885, 515, 890)

    # ---- series parts 2 and 3 (13 Nov 2026): North America, Australia and New Zealand
    def palm(px, h=150, k=1.0):
        return (P(f"M{px} 0 q{_f(14 * k)} {_f(-h / 2)} 0 {-h}", "none", 7, "#8A5A3C")
                + P(f"M{px} {-h} q{_f(-44 * k)} {_f(-22 * k)} {_f(-70 * k)} {_f(6 * k)} M{px} {-h} q{_f(-30 * k)} {_f(-50 * k)} {_f(-66 * k)} {_f(-42 * k)} M{px} {-h} q{_f(44 * k)} {_f(-22 * k)} {_f(70 * k)} {_f(6 * k)} M{px} {-h} q{_f(30 * k)} {_f(-50 * k)} {_f(66 * k)} {_f(-42 * k)} M{px} {-h} q{_f(4 * k)} {_f(-40 * k)} {_f(-4 * k)} {_f(-62 * k)}", "none", 7, "#2FA36B"))

    def lm_liberty():
        gr = "#8FC7B5"; o = water(520, -4)
        o += P("M-110 -6 L-90 -70 H90 L110 -6 Z", "#D9DEE8") + R(-70, -250, 140, 180, "#E7DDC8") + win(-70, 70, -250, -70, 3, 3, 0.35) + R(-84, -270, 168, 24, "#D9CDB4", 4, 4)
        o += P("M-52 -270 Q-64 -420 -40 -520 L40 -520 Q70 -400 60 -270 Z", gr) + P("M-30 -300 Q-20 -420 -10 -500 M14 -300 Q20 -400 22 -500 M40 -290 Q50 -380 44 -470", "none", 3, INK, ' opacity="0.45"')
        o += P("M-40 -470 L-96 -430 L-84 -380 L-36 -410 Z", gr, 4) + R(-100, -440, 34, 48, "#E7DDC8", 4, 3)
        o += P("M30 -500 L62 -640 L86 -634 L58 -486 Z", gr, 4) + P("M58 -640 H92 L84 -664 H66 Z", GOLD, 4) + P("M75 -664 Q60 -700 76 -730 Q92 -700 75 -664 Z", "#F7C531", 4)
        o += f'<circle cx="0" cy="-556" r="40" fill="{gr}" stroke="{INK}" stroke-width="5"/>' + P("M-14 -560 h8 M8 -560 h8 M-10 -540 q10 6 20 0", "none", 4)
        o += "".join(P(f"M{_f(46 * math.cos(a))} {_f(-580 - 46 * math.sin(a))} L{_f(84 * math.cos(a))} {_f(-580 - 84 * math.sin(a))}", "none", 7, gr) for a in (math.radians(d) for d in (20, 50, 80, 100, 130, 160)))
        o += P("M-38 -582 Q0 -616 38 -582", "none", 9, gr)
        return o, (-260, -735, 520, 780)

    def lm_cn_tower():
        cn = "#C9D2DE"
        o = R(-260, -300, 96, 300, "#DCE6F5") + win(-260, -164, -300, 0, 3, 8) + R(150, -380, 100, 380, "#CBD9EE") + win(150, 250, -380, 0, 3, 10) + R(-150, -210, 80, 210, "#E7EDF7", 4) + win(-150, -70, -210, 0, 2, 5)
        o += P("M-46 0 L-14 -600 H14 L46 0 Z", cn) + P("M0 -590 V0", "none", 3, INK, ' opacity="0.4"')
        o += P("M-64 -640 Q-70 -600 -40 -590 H40 Q70 -600 64 -640 Q0 -672 -64 -640 Z", WHITE) + P("M-60 -626 H60", "none", 4, "#E0563B") + R(-34, -690, 68, 46, cn, 4, 8)
        o += P("M-10 -690 L-5 -860 H5 L10 -690 Z", cn, 4) + P("M0 -860 V-950", "none", 5) + P("M-7 -780 H7 M-6 -820 H6", "none", 4, "#E0563B")
        return o, (-265, -955, 520, 960)

    def lm_space_needle():
        o = R(-250, -260, 100, 260, "#DCE6F5") + win(-250, -150, -260, 0, 3, 7) + R(150, -200, 96, 200, "#E7EDF7") + win(150, 246, -200, 0, 3, 5)
        o += P("M-90 0 Q-30 -260 -22 -520 M90 0 Q30 -260 22 -520 M-30 0 Q-6 -260 -8 -520 M30 0 Q6 -260 8 -520", "none", 9, INK) + P("M-90 0 Q-30 -260 -22 -520 M90 0 Q30 -260 22 -520 M-30 0 Q-6 -260 -8 -520 M30 0 Q6 -260 8 -520", "none", 5, WHITE)
        o += P("M-40 -300 H40 M-32 -400 H32", "none", 5) + P("M-150 -560 Q0 -610 150 -560 L110 -520 H-110 Z", WHITE) + P("M-150 -560 Q0 -520 150 -560", "none", 4)
        o += P("M-110 -572 Q0 -640 110 -572 Z", "#F29D52") + R(-26, -660, 52, 40, WHITE, 4, 6) + P("M0 -660 V-800", "none", 5)
        o += f'<path d="M-330 0 L-290 -130 L-250 0 Z M-312 -70 L-290 -190 L-268 -70 Z" fill="#2FA36B" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        return o, (-335, -805, 585, 810)

    def lm_oil_rig():
        st = "#33435E"
        o = R(150, -420, 100, 420, "#CBD9EE") + win(150, 250, -420, 0, 3, 11) + R(262, -300, 80, 300, "#E7EDF7", 4) + win(262, 342, -300, 0, 2, 8)
        o += P("M-290 0 L-240 -520 H-200 L-150 0 M-282 -90 L-158 -90 M-270 -210 L-170 -210 M-258 -330 L-182 -330 M-248 -430 L-192 -430 M-282 -90 L-170 -210 M-158 -90 L-270 -210 M-270 -210 L-182 -330 M-170 -210 L-258 -330", "none", 6, st) + R(-250, -560, 60, 40, st, 4, 4)
        o += P("M-20 0 L20 -220 L60 0 M0 -110 H40", "none", 8, st) + P("M-110 -260 L130 -200", "none", 14, INK) + P("M-110 -260 L130 -200", "none", 9, "#E0563B")
        o += P("M-150 -300 Q-90 -330 -96 -230 Q-100 -200 -140 -216 Z", "#E0563B") + P("M-124 -220 V-30", "none", 5) + R(-140, -40, 34, 40, st, 4) + P("M130 -200 L96 -40", "none", 6, st)
        o += f'<circle cx="100" cy="-40" r="34" fill="{GOLD}" stroke="{INK}" stroke-width="5"/><circle cx="100" cy="-40" r="8" fill="{INK}"/>' + R(60, -10, 110, 14, st, 3)
        return o, (-295, -565, 640, 570)

    def lm_state_house():
        br = "#C97A5E"
        o = R(-300, -200, 600, 200, br) + win(-300, 300, -160, -30, 10, 2, 0.35) + R(-150, -300, 300, 300, br)
        o += R(-130, -200, 260, 200, "#F4EFE4", 4) + "".join(R(-116 + i * 44, -196, 16, 194, WHITE, 3) for i in range(6)) + P("M-160 -300 L0 -380 L160 -300 Z", "#F4EFE4")
        o += R(-80, -430, 160, 60, "#F4EFE4", 4) + P("M-90 -430 Q-90 -560 0 -572 Q90 -560 90 -430 Z", "#F2C230") + P("M-40 -438 Q-40 -540 -14 -566 M40 -438 Q40 -540 14 -566 M0 -572 V-434", "none", 3, INK, ' opacity="0.45"')
        o += R(-14, -610, 28, 40, "#F2C230", 4, 4) + P("M0 -610 V-660", "none", 5)
        return o, (-305, -665, 610, 670)

    def lm_observatory():
        o = P("M-360 0 Q-260 -260 -90 -250 Q60 -330 220 -230 Q320 -200 360 0 Z", "#D8C79A", 4)
        o += R(-190, -330, 380, 90, WHITE) + win(-190, 190, -330, -240, 8, 1, 0.35)
        o += P("M-70 -330 Q-70 -430 0 -436 Q70 -430 70 -330 Z", "#5A6478") + P("M0 -436 V-476", "none", 5)
        o += "".join(P(f"M{xx - 40} -330 Q{xx - 40} -384 {xx} -388 Q{xx + 40} -384 {xx + 40} -330 Z", "#5A6478", 4) for xx in (-150, 150))
        o += palm(-300, 190, 1.0) + palm(300, 230, 1.1) + palm(246, 150, 0.8)
        # a film clapperboard on the ground in front
        o += f'<g transform="translate(-40 -30) rotate(-6)"><rect x="-90" y="-80" width="180" height="110" rx="8" fill="#33435E" stroke="{INK}" stroke-width="5"/><path d="M-90 -80 L-80 -122 L96 -104 L90 -80 Z" fill="{WHITE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/><path d="M-50 -119 l-10 36 M-6 -114 l-10 34 M38 -110 l-10 30 M80 -106 l-8 26" stroke="{INK}" stroke-width="12"/><path d="M-66 -40 H66 M-66 -10 H30" stroke="{WHITE}" stroke-width="5" opacity="0.7"/></g>'
        return o, (-375, -480, 750, 485)

    def lm_opera_house():
        o = water(720, -4)
        o += P("M-350 -40 Q-100 -420 150 -40", "none", 16, INK) + P("M-350 -40 Q-100 -420 150 -40", "none", 10, "#7C8FB5") + P("M-350 -110 H150", "none", 8, "#7C8FB5")
        o += "".join(P(f"M{xx} -110 V{_f(-40 - 380 * (1 - ((xx + 100) / 250) ** 2) * 0.5 - 0)}", "none", 3, "#7C8FB5") for xx in range(-310, 140, 44))
        o += "".join(R(xx, -150, 26, 150, "#C9B48A", 4) for xx in (-360, 140))
        o += R(-40, -40, 400, 40, "#D9CDB4", 4, 6)
        for bx, h, w in ((40, 250, 150), (130, 200, 130), (210, 150, 110), (285, 100, 80)):
            o += P(f"M{bx - w * 0.5} -40 Q{bx - w * 0.2} {-40 - h} {bx + w * 0.45} {-40 - h * 0.96} Q{bx + w * 0.3} {-40 - h * 0.4} {bx + w * 0.42} -40 Z", WHITE)
        o += P("M-10 -40 Q0 -120 46 -150 Q30 -90 36 -40 Z", WHITE, 4)
        return o, (-365, -300, 730, 345)

    def lm_flinders():
        ye = "#E9C46A"; gr = "#6FA58B"
        o = R(-330, -210, 560, 210, ye) + win(-330, 230, -170, -40, 9, 2, 0.35) + P("M-330 -210 H230", "none", 8, "#B5473A")
        o += R(-60, -300, 220, 300, ye) + P("M-20 0 V-150 Q50 -230 120 -150 V0 Z", "#7C8FB5", 4) + f'<circle cx="50" cy="-232" r="26" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>' + P("M50 -232 V-250 M50 -232 h12", "none", 3)
        o += P("M-70 -300 Q-70 -430 50 -444 Q170 -430 170 -300 Z", gr) + P("M-10 -306 Q-6 -410 30 -440 M110 -306 Q106 -410 70 -440 M50 -444 V-304", "none", 3, INK, ' opacity="0.45"') + R(34, -486, 32, 44, gr, 4, 4) + P("M50 -486 V-530", "none", 5)
        o += R(-330, -330, 70, 330, ye) + P("M-336 -330 Q-295 -400 -254 -330 Z", gr) + f'<circle cx="-295" cy="-250" r="24" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>' + P("M-295 -250 V-266 M-295 -250 h10", "none", 3)
        # a tram in front
        o += P("M150 -150 L170 -190 M330 -150 L310 -190 M140 -190 H340", "none", 4) + R(120, -150, 240, 120, "#2F8F5B", 5, 18) + R(120, -66, 240, 22, "#F2C230", 3) + "".join(R(138 + i * 54, -134, 42, 50, G["SKY"], 3, 6) for i in range(4))
        o += f'<circle cx="170" cy="-22" r="18" fill="{INK}"/><circle cx="310" cy="-22" r="18" fill="{INK}"/>'
        return o, (-340, -535, 705, 540)

    def lm_haul_truck():
        ye = "#F2C230"
        o = P("M-360 0 L-250 -230 L-140 -110 L-40 -300 L80 0 Z", "#C9A27C", 4) + P("M-250 -230 L-226 -170 L-270 -150 M-40 -300 L-10 -220 L-60 -200", "none", 3, INK, ' opacity="0.45"')
        o += P("M-60 -150 L-30 -330 H250 L330 -260 L300 -150 Z", ye) + P("M-20 -310 H240 M0 -260 H280", "none", 4, INK, ' opacity="0.35"') + P("M-10 -330 Q110 -400 240 -330 Z", "#8A5A3C", 4)
        o += R(-80, -150, 400, 70, "#33435E", 5, 10) + R(250, -250, 90, 110, ye, 5, 8) + R(266, -236, 58, 46, G["SKY"], 4, 6) + P("M330 -150 V-40 M345 -150 V-40 M330 -110 H345 M330 -70 H345", "none", 4)
        o += "".join(f'<circle cx="{cx}" cy="-74" r="74" fill="{INK}"/><circle cx="{cx}" cy="-74" r="30" fill="{GREY}" stroke="{WHITE}" stroke-width="5"/>' for cx in (10, 230))
        return o, (-365, -400, 715, 405)

    def lm_parliament_au():
        o = P("M-370 0 Q-200 -250 0 -250 Q200 -250 370 0 Z", "#9CCB8E", 4)
        o += R(-260, -150, 520, 150, WHITE) + "".join(R(-244 + i * 46, -140, 20, 140, "#E7EDF7", 3) for i in range(11)) + R(-90, -190, 180, 190, "#F4EFE4", 4) + "".join(R(-76 + i * 34, -180, 14, 180, WHITE, 3) for i in range(5))
        o += P("M-120 -250 L0 -560 L120 -250 M-60 -250 L0 -560 L60 -250", "none", 11, INK) + P("M-120 -250 L0 -560 L120 -250 M-60 -250 L0 -560 L60 -250", "none", 6, "#C9D2DE") + P("M0 -560 V-690", "none", 6)
        o += P("M0 -690 H110 L96 -660 L110 -630 H0 Z", BLUE, 4) + f'<circle cx="34" cy="-660" r="9" fill="{WHITE}"/>'
        return o, (-375, -695, 750, 700)

    def lm_beehive():
        cu = "#C9A27C"; o = ""
        for i, (w, y0) in enumerate(((300, 0), (280, -70), (256, -140), (228, -210), (196, -280), (160, -350))):
            o += R(-w / 2, y0 - 70, w, 70, "#E9DCC4" if i % 2 == 0 else "#D9CDB4", 5, 10) + win(-w / 2 + 8, w / 2 - 8, y0 - 62, y0 - 8, max(6, int(w / 26)), 1, 0.4)
        o += P("M-70 -420 Q-70 -480 0 -486 Q70 -480 70 -420 Z", cu) + P("M0 -486 V-540", "none", 5)
        o += R(-330, -260, 150, 260, "#E7EDF7", 5) + "".join(R(-318 + i * 36, -250, 16, 250, WHITE, 3) for i in range(4)) + P("M-340 -260 L-255 -320 L-170 -260 Z", "#E7EDF7", 4)
        o += f'<path d="M250 0 q-30 -90 0 -150 q30 60 0 150 Z M300 0 q-22 -60 0 -104 q22 44 0 104 Z" fill="#8FCBA0" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        return o, (-345, -545, 670, 550)

    def lm_sky_tower():
        cn = "#C9D2DE"; o = water(560, -4)
        o += R(-250, -280, 100, 274, "#DCE6F5") + win(-250, -150, -280, -6, 3, 8) + R(140, -200, 110, 194, "#E7EDF7") + win(140, 250, -200, -6, 3, 5)
        o += P("M-26 -6 L-16 -560 H16 L26 -6 Z", cn) + P("M-70 -6 L-18 -200 M70 -6 L18 -200", "none", 7, "#7C8FB5")
        o += P("M-58 -600 L-40 -560 H40 L58 -600 Z", "#7C8FB5") + R(-64, -650, 128, 50, WHITE, 5, 10) + win(-64, 64, -650, -600, 7, 1, 0.45) + P("M-50 -650 L-30 -690 H30 L50 -650 Z", cn, 4)
        o += P("M-9 -690 L-4 -840 H4 L9 -690 Z", cn, 4) + P("M0 -840 V-930", "none", 5) + P("M-6 -770 H6 M-5 -810 H5", "none", 4, "#E0563B")
        o += P("M-230 20 l40 -70 l0 70 Z M-180 20 l0 -90 l44 90 Z", WHITE, 4) + P("M-250 24 H-120", "none", 5)
        return o, (-285, -935, 570, 985)

    def lm_wine():
        o = P("M-370 0 Q-250 -200 -80 -170 Q80 -260 240 -150 Q330 -130 370 0 Z", "#A9CF8E", 4)
        o += "".join(P(f"M{-300 + i * 44} {-60 - (i % 3) * 14} q14 -22 28 0 M{-286 + i * 44} {-40 - (i % 3) * 14} v-40", "none", 4, "#5E7A4A") for i in range(15))
        o += f'<ellipse cx="-150" cy="-110" rx="120" ry="110" fill="#C98F52" stroke="{INK}" stroke-width="6"/><ellipse cx="-150" cy="-110" rx="78" ry="72" fill="#E2B37A" stroke="{INK}" stroke-width="4"/>'
        o += P("M-262 -150 Q-150 -190 -38 -150 M-262 -70 Q-150 -30 -38 -70", "none", 7, "#5A6478") + f'<circle cx="-150" cy="-110" r="12" fill="{INK}"/>' + R(-230, -10, 160, 14, "#8A5A3C", 4, 4)
        o += P("M60 0 V-250 Q60 -300 84 -330 V-420 H116 V-330 Q140 -300 140 -250 V0 Z", "#2F5D50") + R(80, -440, 40, 26, "#7A2E3A", 4, 4) + R(64, -210, 72, 110, "#F4EFE4", 4, 6) + P("M78 -170 H122 M78 -140 H112", "none", 4, INK, ' opacity="0.5"')
        o += P("M210 -330 Q210 -210 256 -206 Q302 -210 302 -330 Z", WHITE) + P("M216 -280 Q256 -262 296 -280 Q296 -214 256 -210 Q216 -214 216 -280 Z", "#7A2E3A", 3) + P("M256 -206 V-30 M216 -10 Q256 -40 296 -10", "none", 6)
        o += "".join(f'<circle cx="{cx}" cy="{cy}" r="17" fill="#6B3FA0" stroke="{INK}" stroke-width="3.5"/>' for cx, cy in ((-20, -40), (10, -40), (-5, -66), (-35, -66), (-20, -92), (25, -66), (-5, -16))) + P("M-20 -108 q10 -30 40 -30", "none", 5, "#5E7A4A")
        return o, (-375, -445, 750, 450)

    # ---- industry spread for a region part (13 Nov 2026): fishing, car making, pharma, farming, fashion
    def lm_lighthouse():
        o = water(720, -4)
        o += P("M-360 -4 Q-300 -120 -200 -110 Q-120 -150 -40 -90 Q20 -70 60 -4 Z", "#B9B4AA", 4) + P("M-300 -60 q40 -20 70 4 M-170 -96 q40 -10 60 20", "none", 3, INK, ' opacity="0.4"')
        o += P("M-214 -110 L-196 -420 H-124 L-106 -110 Z", WHITE) + P("M-208 -210 H-112 M-202 -320 H-118", "none", 4, INK, ' opacity="0.35"') + R(-176, -180, 32, 70, "#33435E", 4, 14)
        o += R(-216, -444, 112, 26, "#E0563B", 4, 4) + R(-190, -506, 60, 62, YEL, 4) + P("M-160 -506 V-444", "none", 3) + P("M-202 -506 L-160 -560 L-118 -506 Z", "#E0563B") + P("M-160 -560 V-590", "none", 5)
        o += P("M-126 -476 L20 -520 M-126 -470 L20 -430", "none", 4, YEL)
        # a fishing boat with its net and catch
        o += P("M90 -70 H350 L320 6 H130 Z", "#2F6FB5") + P("M96 -52 H346", "none", 5, WHITE) + R(150, -150, 96, 80, WHITE, 5, 6) + R(166, -136, 30, 30, G["SKY"], 3, 4) + R(206, -136, 30, 30, G["SKY"], 3, 4)
        o += P("M250 -70 V-280 M250 -270 L340 -110", "none", 6) + P("M340 -110 q-26 34 -52 40 q30 6 52 -40 Z", "#C9D2DE", 3)
        o += "".join(P(f"M{fx} {fy} q16 -14 34 0 q-18 14 -34 0 Z M{fx + 34} {fy} l12 -9 v18 Z", "#8FB7D9", 3) for fx, fy in ((270, -84), (296, -96), (286, -72)))
        return o, (-365, -595, 730, 640)

    def lm_motor_city():
        gl = "#9DB6D6"
        o = R(-330, -260, 90, 260, "#DCE6F5") + win(-330, -240, -260, 0, 3, 7)
        for cx, h, w in ((-150, 330, 84), (150, 330, 84), (-60, 250, 70), (60, 250, 70)):
            o += R(cx - w / 2, -h, w, h, gl, 5, 30) + win(cx - w / 2 + 6, cx + w / 2 - 6, -h + 20, -10, 3, int(h / 30), 0.35)
        o += R(-52, -520, 104, 520, "#7F9CC4", 5, 40) + win(-46, 46, -500, -10, 3, 16, 0.35) + R(-20, -560, 40, 44, "#59647A", 4, 6) + P("M0 -560 V-610", "none", 5)
        o += R(-230, -60, 460, 60, "#C9D2DE", 4, 8)
        # a car on the road in front
        o += P("M150 -40 Q150 -86 196 -90 L232 -150 Q240 -162 256 -162 H330 Q346 -162 356 -150 L392 -92 Q440 -86 440 -40 Z", "#E0563B") + P("M246 -148 H288 V-96 H214 Z M300 -148 H338 L372 -96 H300 Z", G["SKY"], 4)
        o += "".join(f'<circle cx="{cx}" cy="-34" r="34" fill="{INK}"/><circle cx="{cx}" cy="-34" r="13" fill="{GREY}"/>' for cx in (216, 380)) + f'<circle cx="434" cy="-70" r="8" fill="{YEL}" stroke="{INK}" stroke-width="3"/>'
        return o, (-335, -615, 780, 620)

    def lm_pharma():
        st = "#E4DCCB"
        o = R(-340, -230, 110, 230, "#DCE6F5") + win(-340, -230, -230, 0, 3, 6) + R(-220, -300, 100, 300, "#CBD9EE") + win(-220, -120, -300, 0, 3, 8)
        # a stone monument column on a stepped base
        o += R(-110, -40, 220, 40, st, 5, 4) + R(-84, -90, 168, 50, st, 5, 4) + R(-58, -150, 116, 60, st, 5, 4) + P("M-34 -150 L-22 -520 H22 L34 -150 Z", st) + P("M0 -500 V-170", "none", 3, INK, ' opacity="0.3"')
        o += R(-34, -548, 68, 28, st, 4, 4) + P("M-14 -548 Q-22 -600 0 -640 Q22 -600 14 -548 Z", "#8FC7B5", 4) + P("M0 -640 V-676", "none", 5)
        # a medicine bottle, capsules and a flask in front
        o += R(140, -210, 130, 210, "#F29D52", 5, 16) + R(152, -252, 106, 46, WHITE, 5, 8) + R(152, -150, 106, 96, WHITE, 4, 6) + P("M205 -128 V-76 M179 -102 H231", "none", 9, "#E0563B")
        o += "".join(f'<g transform="translate({cx} {cy}) rotate({r})"><rect x="-34" y="-15" width="68" height="30" rx="15" fill="{WHITE}" stroke="{INK}" stroke-width="4"/><path d="M0 -15 H19 Q34 -15 34 0 Q34 15 19 15 H0 Z" fill="{c}" stroke="{INK}" stroke-width="4"/></g>' for cx, cy, r, c in ((330, -22, -18, "#E0563B"), (316, -66, 24, BLUE), (372, -52, 70, "#2FA36B")))
        o += P("M-290 0 L-262 -60 V-110 H-238 V-60 L-210 0 Z", WHITE, 4) + P("M-282 -16 L-268 -46 H-232 L-218 -16 Z", "#8FCBA0", 3) + P("M-270 -110 H-230", "none", 5)
        return o, (-345, -680, 760, 685)

    def lm_farm():
        o = P("M-370 0 Q-240 -120 -60 -90 Q120 -150 370 0 Z", "#B9DA94", 4)
        o += R(-250, -210, 250, 210, "#C8463A") + P("M-270 -210 L-190 -300 H-60 L20 -210 Z", "#8E3027") + P("M-220 -260 L-125 -330 L-30 -260", "none", 5) + R(-170, -120, 90, 120, "#8E3027", 4) + P("M-170 -120 L-80 0 M-80 -120 L-170 0", "none", 4, WHITE) + R(-150, -196, 50, 44, WHITE, 4)
        o += R(40, -360, 110, 360, "#C9D2DE") + P("M40 -360 Q95 -440 150 -360 Z", "#8A94A6") + P("M40 -290 H150 M40 -210 H150 M40 -130 H150 M40 -60 H150", "none", 3, INK, ' opacity="0.4"') + P("M95 -420 V-450", "none", 5)
        # corn stalks with ears in front
        for cx, h in ((210, 230), (262, 270), (314, 240), (-320, 200)):
            o += P(f"M{cx} 0 V{-h}", "none", 7, "#4E8B3A") + P(f"M{cx} {-h * 0.45} q-44 -30 -58 -80 M{cx} {-h * 0.55} q44 -30 58 -80 M{cx} {-h * 0.8} q-30 -24 -40 -60 M{cx} {-h} q6 -30 20 -44", "none", 6, "#4E8B3A")
            o += f'<ellipse cx="{cx + 16}" cy="{_f(-h * 0.5)}" rx="15" ry="38" transform="rotate(18 {cx + 16} {_f(-h * 0.5)})" fill="{YEL}" stroke="{INK}" stroke-width="4"/>'
        return o, (-375, -455, 750, 460)

    def lm_fashion():
        o = P("M-370 0 Q-250 -150 -90 -120 Q80 -190 250 -110 Q330 -90 370 0 Z", "#E4D2A8", 4)
        o += R(-250, -250, 300, 250, "#F6E4DC") + R(-250, -280, 300, 34, "#E88FA2", 4, 4) + R(-224, -200, 110, 200, G["SKY"], 4) + R(-80, -200, 104, 200, G["SKY"], 4) + P("M-224 -100 H-114", "none", 3, INK, ' opacity="0.35"')
        o += palm(-320, 230, 1.0) + palm(100, 300, 1.1)
        # a dress form in the shop window and a rail of clothes in front
        o += P("M-190 -180 Q-170 -196 -150 -180 L-140 -120 Q-150 -84 -138 -40 H-202 Q-190 -84 -200 -120 Z", "#E0563B", 4) + P("M-170 -40 V-8 M-196 -8 H-144", "none", 5) + f'<circle cx="-170" cy="-198" r="9" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>'
        o += P("M150 0 V-230 H360 V0 M130 0 H170 M340 0 H380", "none", 6)
        for i, c in enumerate(("#467DE3", "#F2C230", "#2FA36B", "#E88FA2")):
            hx = 180 + i * 50
            o += P(f"M{hx} -230 v14 M{hx - 22} -196 L{hx} -216 L{hx + 22} -196", "none", 4) + P(f"M{hx - 22} -196 H{hx + 22} L{hx + 28} -70 H{hx - 28} Z", c, 4)
        return o, (-375, -420, 760, 425)

    LM = {"lighthouse": lm_lighthouse, "motor_city": lm_motor_city, "pharma": lm_pharma, "farm": lm_farm, "fashion": lm_fashion, "golden_gate": lm_golden_gate, "big_ben": lm_big_ben, "eiffel": lm_eiffel, "erasmus": lm_erasmus, "euro": lm_euro, "minster": lm_minster,
          "burj": lm_burj, "mbs": lm_mbs, "hk": lm_hk, "fab": lm_fab, "tokyo_tower": lm_tokyo_tower, "empire": lm_empire,
          "liberty": lm_liberty, "cn_tower": lm_cn_tower, "space_needle": lm_space_needle, "oil_rig": lm_oil_rig, "state_house": lm_state_house, "observatory": lm_observatory,
          "opera_house": lm_opera_house, "flinders": lm_flinders, "haul_truck": lm_haul_truck, "parliament_au": lm_parliament_au, "beehive": lm_beehive, "sky_tower": lm_sky_tower, "wine": lm_wine}

    def landmark(x, y, s=1.0, kind="eiffel", **_):
        """A city landmark as a simple hand-drawn silhouette with flat fills (map reels; no logos or names). (x, y) = centre of its base on the ground. kind: golden_gate, big_ben, eiffel, erasmus (a cable-stayed bridge with one bent pylon), euro (a euro-sign sculpture before bank towers), minster (a red twin-spired cathedral on a river), burj (a very tall stepped spire), mbs (three towers under one roof deck), hk (a faceted tower, a peak and a red-sailed junk), fab (a chip plant with a large microchip), tokyo_tower, empire, liberty, cn_tower, space_needle, oil_rig (a derrick and a pumpjack), state_house (a gold-domed brick state house), observatory (domes on a hill, palms and a film clapperboard), opera_house (white sails and an arch bridge), flinders (a domed yellow station and a tram), haul_truck (a mine truck before an open pit), parliament_au (a flag mast over a low white building on a hill), beehive (a round stepped building), sky_tower, wine (a barrel, a bottle and a glass before vineyard hills)."""
        if kind not in LM: raise ValueError(f"landmark: kind {kind!r}; use {', '.join(LM)}")
        return _g(x, y, s, LM[kind]()[0])

    def landmark_box(x, y, s=1.0, kind="eiffel", **_):
        b = LM[kind]()[1]
        return [x + b[0] * s, y + b[1] * s, b[2] * s, b[3] * s]

    G["PRESETS"].update({"world_map": (world_map, world_map_box), "map_pin": (map_pin, map_pin_box), "flight_path": (flight_path, flight_path_box),
                         "suitcase": (suitcase, lambda x, y, s=1.0, **_: [x - 40 * s, y - 128 * s, 80 * s, 132 * s]), "cloud": (cloud, None), "map_label": (map_label, map_label_box), "landmark": (landmark, landmark_box), "map_dot": (map_dot, map_dot_box), "map_plate": (map_plate, lambda x, y, s=1.0, w=190, h=58, **_: [x - w / 2, y - h / 2, w, h]), "plane": (plane, None), "cargo_ship": (cargo_ship, None), "delivery_van": (delivery_van, lambda x, y, s=1.0, **_: [x - 256 * s, y - 276 * s, 512 * s, 276 * s])})
    G["HALF"].update({"cloud": (112, 56), "plane": (140, 80), "cargo_ship": (175, 112)})
    G["LANDMARKS"] = tuple(LM)
