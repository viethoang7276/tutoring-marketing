"""Flat-style props (17 Nov 2026, opt-in with meta.style "flat"; first used by the "Plain numbers" pilot).

Hoang (17 Nov 2026), on a flat cartoon reference reel: "More neat clean and less paper like". These props are solid flat
fills with soft simple shading and no ink outline (Ledger keeps his own clean outline), in a bright palette built around
Edlintics blue. They are drawn to be laid out as ONE continuous world (sky, ground, town, hill, valley) that the camera
moves through with scene "cam" keyframes, instead of one boxed picture per beat. Nothing here is used by other styles.

Installed into scene_lib by install(): flat_rect, flat_path, flat_sun, flat_cloud, flat_tree, flat_house, flat_sparkle,
flat_arrow, flat_tag, flat_card, flat_board, flat_brochure, flat_table, flat_bar, flat_bracket, flat_list, flat_bubble,
flat_person, flat_ring, flat_building, and (18 Nov 2026) flat_number, flat_equation, flat_waterfall, flat_sentence (numbers and key
sentences on screen, in step with the voice). (x, y) is the centre unless the docstring says "bottom centre".
"""
import hashlib, html as _h

# palette (config/brand.ts: brand #467DE3, accent #60A5FA, ink, emerald, amber), bright and limited
FLAT = {
    "blue": "#467DE3", "blue2": "#60A5FA", "navy": "#2F58A8", "deep": "#1E3A8A", "pale": "#DBEAFE", "ice": "#EFF6FF",
    "ink": "#0F172A", "slate": "#64748B", "mist": "#CBD5E1", "white": "#FFFFFF", "cream": "#FFF8EC",
    "sun": "#FFD45C", "amber": "#FFB547", "green": "#16A36A", "red": "#E5484D",
    "grass": "#7DD3A0", "grass2": "#5BBF86", "grass3": "#3FA56F", "far": "#B9E2CC", "far2": "#A7CCF2",
    "wood": "#9A6B44", "shade": "#E3ECF8",
}
FONT = 'font-family="Inter,sans-serif"'


def _c(v):
    return FLAT.get(v, v)


def _tw(txt, fs, wt=900):
    """Rough text width for Inter at weight wt (wide letters count more)."""
    k = 0.6 if wt >= 900 else 0.57
    return sum((0.36 if ch in " .,:'il1|" else 0.8 if ch in "MW%" else 1.0) for ch in str(txt)) * fs * k


def _wrap(txt, fs, width, wt=900):
    out, cur = [], ""
    for w in str(txt).split():
        t = (cur + " " + w).strip()
        if cur and _tw(t, fs, wt) > width: out.append(cur); cur = w
        else: cur = t
    if cur: out.append(cur)
    return out


def _balance(lines, fs, wt):
    """Two lines of wrapped text, split where the longer line is shortest (like CSS text-wrap: balance)."""
    if len(lines) != 2: return lines
    words = (lines[0] + " " + lines[1]).split()
    best = min(range(1, len(words)), key=lambda i: max(_tw(" ".join(words[:i]), fs, wt), _tw(" ".join(words[i:]), fs, wt)))
    return [" ".join(words[:best]), " ".join(words[best:])]


def _text(x, y, txt, fs, col="ink", wt=900, anchor="middle", extra=""):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {FONT} font-weight="{wt}" font-size="{fs}" fill="{_c(col)}"{extra}>{_h.escape(str(txt))}</text>'


def install(G):
    """Register the flat props in scene_lib (G = its globals)."""
    _f, _m_attr = G["_f"], G["_m_attr"]

    def g(x, y, s, inner, rot=0):
        return f'<g transform="translate({_f(x)} {_f(y)}) rotate({rot}) scale({s})">{inner}</g>'

    def at_attr(at, ax, ay, delay=0.0):
        """a nested pop-in, timed like an item's "at"; with a delay it uses the motion layer's appear"""
        if not at: return "", ""
        if delay:
            S = {"x": ax, "y": ay, "appear": {"at": str(at), "delay": float(delay)}}
            return f'<g data-fx="m" data-spec="{_m_attr(S)}">', "</g>"
        return f'<g data-at="{at}" data-ax="{_f(ax)}" data-ay="{_f(ay)}">', "</g>"

    def grad(stops, vertical=True):
        gid = "fg" + hashlib.sha1(str(stops).encode()).hexdigest()[:10]
        st = "".join(f'<stop offset="{o}" stop-color="{_c(c)}"/>' for o, c in stops)
        xy = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="0"'
        return gid, f'<defs><linearGradient id="{gid}" {xy}>{st}</linearGradient></defs>'

    def flat_rect(x, y, s=1.0, w=400, h=200, fill="blue", rx=0, top=None, bottom=None, opacity=1, **_):
        """A flat rectangle centred at (x, y); top and bottom give a soft vertical gradient (a sky)."""
        if top and bottom:
            gid, d = grad([(0, top), (1, bottom)]); f = f"url(#{gid})"
        else: d, f = "", _c(fill)
        return d + f'<rect x="{_f(x - w * s / 2)}" y="{_f(y - h * s / 2)}" width="{_f(w * s)}" height="{_f(h * s)}" rx="{rx}" fill="{f}" opacity="{opacity}"/>'

    def flat_rect_box(x, y, s=1.0, w=400, h=200, **_):
        return [x - w * s / 2, y - h * s / 2, w * s, h * s]

    def flat_path(x, y, s=1.0, d="", fill="grass", opacity=1, top=None, bottom=None, stroke=None, sw=0, **_):
        """Any flat shape: an SVG path d in world coordinates (x, y, s are ignored), for terrain and roads."""
        if top and bottom:
            gid, df = grad([(0, top), (1, bottom)]); f = f"url(#{gid})"
        else: df, f = "", _c(fill) if fill != "none" else "none"
        st = f' stroke="{_c(stroke)}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if stroke else ""
        return df + f'<path d="{d}" fill="{f}" opacity="{opacity}"{st}/>'

    def flat_sun(x, y, s=1.0, **_):
        """Sun with a soft halo."""
        return g(x, y, s, f'<circle r="150" fill="{FLAT["sun"]}" opacity="0.22"/><circle r="105" fill="{FLAT["sun"]}" opacity="0.35"/><circle r="72" fill="{FLAT["sun"]}"/>')

    def flat_cloud(x, y, s=1.0, opacity=0.96, **_):
        """A soft white cloud (add "bob" to drift it)."""
        return g(x, y, s, f'<g fill="#FFFFFF" opacity="{opacity}"><circle cx="-60" cy="0" r="46"/><circle cx="0" cy="-26" r="64"/><circle cx="64" cy="-4" r="50"/>'
                          f'<rect x="-106" y="0" width="216" height="46" rx="23"/></g><rect x="-96" y="30" width="196" height="16" rx="8" fill="{FLAT["pale"]}" opacity="0.7"/>')

    def flat_tree(x, y, s=1.0, kind="round", color="grass3", **_):
        """A flat tree, (x, y) = bottom centre. kind round or pine."""
        c = _c(color)
        if kind == "pine":
            inner = (f'<rect x="-8" y="-40" width="16" height="40" rx="4" fill="{FLAT["wood"]}"/>'
                     f'<path d="M-52 -34 L0 -190 L52 -34 Z" fill="{c}"/><path d="M0 -190 L52 -34 L0 -34 Z" fill="#000" opacity="0.10"/>')
        else:
            inner = (f'<rect x="-9" y="-70" width="18" height="70" rx="5" fill="{FLAT["wood"]}"/>'
                     f'<circle cx="0" cy="-118" r="62" fill="{c}"/><circle cx="22" cy="-108" r="44" fill="#000" opacity="0.08"/><circle cx="-20" cy="-138" r="18" fill="#FFF" opacity="0.18"/>')
        return g(x, y, s, f'<ellipse cx="0" cy="2" rx="46" ry="9" fill="#000" opacity="0.10"/>' + inner)

    ROOFS = {"blue": FLAT["blue"], "sky": FLAT["blue2"], "navy": FLAT["navy"], "amber": FLAT["amber"]}

    def _house_inner(roof="blue", num=None, closed=False, num_at=None, num_delay=0.0, shadow=True):
        rc = FLAT["mist"] if closed else ROOFS.get(roof, _c(roof))
        wall = "#DDE3EB" if closed else "#FFFFFF"; shade = "#C7CFDA" if closed else FLAT["shade"]
        win = "#7B8797" if closed else FLAT["sun"]; door = "#8A94A3" if closed else FLAT["navy"]
        out = ((f'<ellipse cx="0" cy="2" rx="62" ry="9" fill="#000" opacity="0.12"/>' if shadow else "") +
               f'<rect x="22" y="-118" width="16" height="34" fill="{rc}"/><rect x="22" y="-118" width="16" height="34" fill="#000" opacity="0.15"/>'
               f'<rect x="-46" y="-72" width="92" height="72" fill="{wall}"/><rect x="18" y="-72" width="28" height="72" fill="{shade}"/>'
               f'<path d="M-58 -68 L0 -126 L58 -68 Z" fill="{rc}"/><path d="M0 -126 L58 -68 L0 -68 Z" fill="#000" opacity="0.13"/>'
               f'<rect x="-12" y="-36" width="24" height="36" rx="5" fill="{door}"/>'
               f'<rect x="-38" y="-58" width="18" height="18" rx="3" fill="{win}"/><rect x="21" y="-58" width="18" height="18" rx="3" fill="{win}"/>')
        if closed:   # boarded windows and a red CLOSED board
            pl = FLAT["wood"]
            out += (f'<path d="M-40 -60 L-18 -38 M-18 -60 L-40 -38 M19 -60 L41 -38 M41 -60 L19 -38" stroke="{pl}" stroke-width="6" stroke-linecap="round"/>'
                    f'<g transform="rotate(-8 0 -30)"><rect x="-56" y="-46" width="112" height="34" rx="6" fill="{FLAT["red"]}"/>'
                    + _text(0, -21, "CLOSED", 22, "white") + '</g>')
        if num is not None:
            o, c = at_attr(num_at, 0, -88, num_delay)
            out += o + f'<circle cx="0" cy="-88" r="17" fill="#FFFFFF"/>' + _text(0, -80, num, 22, rc if not closed else "slate") + c
        return out

    def flat_house(x, y, s=1.0, roof="blue", num=None, closed=False, num_at=None, num_delay=0, rot=0, ghost=False, color="slate", shadow=True, **_):
        """A little flat house (a fund), (x, y) = bottom centre. roof blue, sky, navy, amber; num = number badge on the roof
        (num_at "chunk:N" + num_delay pop it in); closed = grey walls, boarded windows and a red CLOSED board;
        ghost = only a dashed outline (colour `color`), for the ones that are missing; shadow false = no ground shadow (a falling house)."""
        if ghost:
            c = _c(color)
            return g(x, y, s, f'<path d="M-46 0 V-68 H-58 L0 -126 L58 -68 H46 V0 Z" fill="{c}" fill-opacity="0.10" stroke="{c}" stroke-width="5" stroke-dasharray="14 10" stroke-linejoin="round"/>'
                              + _text(0, -30, "?", 44, color), rot)
        return g(x, y, s, _house_inner(roof, num, closed, num_at, num_delay, shadow), rot)

    def flat_house_box(x, y, s=1.0, **_):
        return [x - 60 * s, y - 128 * s, 120 * s, 130 * s]

    def flat_sparkle(x, y, s=1.0, color="sun", **_):
        """A four-point sparkle star."""
        c = _c(color)
        return g(x, y, s, f'<path d="M0 -34 Q5 -5 34 0 Q5 5 0 34 Q-5 5 -34 0 Q-5 -5 0 -34 Z" fill="{c}"/><circle r="6" fill="#FFF"/>')

    def flat_arrow(x, y, s=1.0, dir="down", color=None, **_):
        """A chunky flat arrow, down (red) or up (green)."""
        c = _c(color or ("red" if dir == "down" else "green"))
        p = "M-16 -40 H16 V0 H34 L0 40 L-34 0 H-16 Z" if dir == "down" else "M-16 40 H16 V0 H34 L0 -40 L-34 0 H-16 Z"
        return g(x, y, s, f'<path d="{p}" fill="{c}"/>')

    def flat_tag(x, y, s=1.0, text="", fill="ink", color="white", fs=34, pad=26, **_):
        """A rounded pill with one line of text."""
        w = _tw(text, fs) + 2 * pad; h = fs * 1.7
        return g(x, y, s, f'<rect data-fb="1" x="{-w / 2:.1f}" y="{-h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h / 2:.1f}" fill="{_c(fill)}"/>' + _text(0, fs * 0.36, text, fs, color))

    def flat_tag_box(x, y, s=1.0, text="", fs=34, pad=26, **_):
        w = (_tw(text, fs) + 2 * pad) * s; h = fs * 1.7 * s
        return [x - w / 2, y - h / 2, w, h]

    def _card_layout(w, pill, lines, pad, gap):
        rows = []; y = pad
        if pill: rows.append(("pill", pill, 34, y)); y += 34 * 1.7 + gap
        for ln in lines:
            txt, fs = ln[0], ln[1]; col = ln[2] if len(ln) > 2 else "ink"; wt = ln[3] if len(ln) > 3 else 900
            for part in _balance(_wrap(txt, fs, w - 2 * pad, wt), fs, wt):
                rows.append(("t", part, fs, y, col, wt)); y += fs * 1.16
            y += gap
        return rows, y - gap + pad

    def flat_card(x, y, s=1.0, w=860, pill="", lines=None, fill="white", pad=46, gap=14, pill_fill="blue", **_):
        """A clean rounded card: an optional pill on top, then lines [[text, size, colour?, weight?], ...] centred and wrapped.
        Used for the series title card, the term card and the next-episode card."""
        rows, h = _card_layout(w, pill, lines or [], pad, gap)
        out = (f'<rect x="{-w / 2 + 10}" y="{-h / 2 + 16}" width="{w}" height="{h:.1f}" rx="44" fill="{FLAT["deep"]}" opacity="0.16"/>'
               f'<rect data-fb="1" x="{-w / 2}" y="{-h / 2:.1f}" width="{w}" height="{h:.1f}" rx="44" fill="{_c(fill)}"/>')
        for r in rows:
            if r[0] == "pill":
                pw = _tw(r[1], r[2]) + 56; ph = r[2] * 1.7; py = -h / 2 + r[3]
                out += f'<rect data-fb="1" x="{-pw / 2:.1f}" y="{py:.1f}" width="{pw:.1f}" height="{ph:.1f}" rx="{ph / 2:.1f}" fill="{_c(pill_fill)}"/>' + _text(0, py + ph / 2 + r[2] * 0.36, r[1], r[2], "white")
            else:
                out += _text(0, -h / 2 + r[3] + r[2] * 0.86, r[1], r[2], r[4], r[5])
        return g(x, y, s, out)

    def flat_card_box(x, y, s=1.0, w=860, pill="", lines=None, pad=46, gap=14, **_):
        _, h = _card_layout(w, pill, lines or [], pad, gap)
        return [x - w * s / 2, y - h * s / 2, w * s, h * s]

    def flat_board(x, y, s=1.0, w=960, h=660, posts=120, **_):
        """A town billboard: two posts and a white board with a blue frame; (x, y) = the board's centre. Put content items on it."""
        pw = 26
        return g(x, y, s, f'<rect data-fp="1" x="{-w * 0.3 - pw / 2}" y="{h / 2 - 10}" width="{pw}" height="{posts + 10}" fill="{FLAT["navy"]}"/>'
                          f'<rect data-fp="1" x="{w * 0.3 - pw / 2}" y="{h / 2 - 10}" width="{pw}" height="{posts + 10}" fill="{FLAT["navy"]}"/>'
                          f'<rect x="{-w / 2 + 12}" y="{-h / 2 + 18}" width="{w}" height="{h}" rx="34" fill="{FLAT["deep"]}" opacity="0.18"/>'
                          f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="34" fill="{FLAT["blue"]}"/>'
                          f'<rect data-fh="1" x="{-w / 2 + 16}" y="{-h / 2 + 16}" width="{w - 32}" height="{h - 32}" rx="22" fill="#FFFFFF"/>')

    def flat_board_box(x, y, s=1.0, w=960, h=660, posts=120, **_):
        return [x - w * s / 2, y - h * s / 2, w * s, (h + posts) * s]

    def bank_icon(cx, cy, k=1.0, col="#FFFFFF"):
        return (f'<g transform="translate({cx} {cy}) scale({k})" fill="{col}"><path d="M-40 -14 L0 -40 L40 -14 Z"/><rect x="-40" y="22" width="80" height="10" rx="3"/>'
                + "".join(f'<rect x="{-34 + i * 20}" y="-10" width="10" height="30" rx="2"/>' for i in range(4)) + '</g>')

    def flat_brochure(x, y, s=1.0, w=820, h=520, n=8, title="Our funds", houses_at=None, every=0.12, checks_at=None, check_every=0.15, roofs=None, **_):
        """A bank brochure page: a blue header with a bank icon and the title, and n little fund houses in rows
        (houses_at "chunk:N" pops them in one by one, every s apart; checks_at puts a green tick on each)."""
        roofs = roofs or ["blue", "amber", "sky", "navy", "blue", "amber", "sky", "navy"]
        out = (f'<rect data-fb="1" x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="26" fill="{FLAT["ice"]}"/>'
               f'<path d="M{-w / 2} {-h / 2 + 26} Q{-w / 2} {-h / 2} {-w / 2 + 26} {-h / 2} H{w / 2 - 26} Q{w / 2} {-h / 2} {w / 2} {-h / 2 + 26} V{-h / 2 + 120} H{-w / 2} Z" fill="{FLAT["blue"]}"/>'
               + bank_icon(-w / 2 + 80, -h / 2 + 64, 0.95) + _text(-w / 2 + 150, -h / 2 + 82, title, 52, "white", 900, "start")
               + f'<rect x="{-1}" y="{-h / 2 + 120}" width="2" height="{h - 120}" fill="{FLAT["pale"]}"/>')
        cols = 4 if n > 4 else n; rws = (n + cols - 1) // cols
        top = -h / 2 + 120; ah = h - 120; sc = 1.05 if n > 4 else 1.45
        for i in range(n):
            r, c = divmod(i, cols)
            hx = -w / 2 + w * (c + 0.5) / cols; hy = top + ah * (r + 1) / rws - 14 if rws > 1 else top + ah / 2 + 92 * sc
            o, cl = at_attr(houses_at, hx, hy, every * i) if houses_at else ("", "")
            out += o + g(hx, hy, sc, _house_inner(roofs[i % len(roofs)])) + cl
            if checks_at:
                o, cl = at_attr(checks_at, hx + 44 * sc, hy - 110 * sc, 0.001 + check_every * i)
                out += o + f'<circle cx="{hx + 44 * sc:.1f}" cy="{hy - 110 * sc:.1f}" r="26" fill="{FLAT["green"]}"/><path d="M{hx + 44 * sc - 12:.1f} {hy - 110 * sc:.1f} l8 9 l16 -18" fill="none" stroke="#FFF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>' + cl
        return g(x, y, s, out)

    def flat_brochure_box(x, y, s=1.0, w=820, h=520, **_):
        return [x - w * s / 2, y - h * s / 2, w * s, h * s]

    def flat_table(x, y, s=1.0, w=860, headers=None, rows=None, colors=None, row_at=None, highlight=None, fs=40, hfs=34, rh=104, hh=84, cols=None, **_):
        """A clean numbers table: a blue header row and white body rows (text wraps to two lines). colors = one colour per body row
        for its last cell (green, red, blue); row_at = one "chunk:N" per row to pop it in; highlight = a body row index with a soft amber band."""
        headers = headers or []; rows = rows or []; nc = len(headers)
        cw = [w * f for f in cols] if cols and len(cols) == nc else [w * 0.5] + [w * 0.5 / (nc - 1)] * (nc - 1) if nc > 1 else [w]   # cols: column width fractions
        H = hh + rh * len(rows)
        out = (f'<rect data-fb="1" x="{-w / 2}" y="{-H / 2}" width="{w}" height="{H}" rx="24" fill="#FFFFFF"/>'
               f'<path d="M{-w / 2} {-H / 2 + 24} Q{-w / 2} {-H / 2} {-w / 2 + 24} {-H / 2} H{w / 2 - 24} Q{w / 2} {-H / 2} {w / 2} {-H / 2 + 24} V{-H / 2 + hh} H{-w / 2} Z" fill="{FLAT["blue"]}"/>')
        cx = -w / 2
        for k, hd in enumerate(headers):
            anchor = "start" if k == 0 else "middle"; tx = cx + 26 if k == 0 else cx + cw[k] / 2
            lines = _wrap(hd, hfs, cw[k] - 30, 800)
            for j, ln in enumerate(lines): out += _text(tx, -H / 2 + hh / 2 + hfs * 0.36 + (j - (len(lines) - 1) / 2) * hfs * 1.1, ln, hfs, "white", 800, anchor)
            cx += cw[k]
        for i, row in enumerate(rows):
            ry = -H / 2 + hh + rh * i
            ra = (row_at or [None] * len(rows))[i]; o, cl = at_attr(ra.get("at"), 0, ry + rh / 2, ra.get("delay", 0) or 0.001) if isinstance(ra, dict) else at_attr(ra, 0, ry + rh / 2)   # {"at","delay"} too
            band = f'<rect x="{-w / 2 + 8}" y="{ry + 6}" width="{w - 16}" height="{rh - 12}" rx="16" fill="{FLAT["sun"]}" opacity="0.35"/>' if highlight == i else ""
            sep = f'<rect x="{-w / 2 + 20}" y="{ry + rh - 2}" width="{w - 40}" height="3" fill="{FLAT["pale"]}"/>' if i < len(rows) - 1 else ""
            cells = ""; cx = -w / 2
            for k, v in enumerate(row):
                col = (colors or [None] * len(rows))[i] if k == nc - 1 and colors else "ink"
                anchor = "start" if k == 0 else "middle"; tx = cx + 26 if k == 0 else cx + cw[k] / 2
                f2 = fs if k else fs - 4; lines = _wrap(v, f2, cw[k] - 34, 800 if k == 0 else 900)
                for j, ln in enumerate(lines): cells += _text(tx, ry + rh / 2 + f2 * 0.36 + (j - (len(lines) - 1) / 2) * f2 * 1.08, ln, f2, col or "ink", 800 if k == 0 else 900, anchor)
                cx += cw[k]
            out += o + band + cells + sep + cl
        return g(x, y, s, out)

    def flat_table_box(x, y, s=1.0, w=860, rows=None, rh=104, hh=84, **_):
        H = (hh + rh * len(rows or [])) * s
        return [x - w * s / 2, y - H / 2, w * s, H]

    def flat_bar(x, y, s=1.0, w=180, h=400, color="blue", value="", label="", fs=54, lfs=32, num=None, pre="", suf="", dec=0, comp="",
                 grow_at=None, grow_delay=0.0, grow_dur=0.8, **_):
        """One bar of a bar chart, (x, y) = bottom centre: the value above it and a label under it. Grow it with "reveal": {"dir": "up"}.
        grow_at "chunk:N" (18 Nov 2026): the bar grows from the ground to h at that chunk (+ grow_delay, over grow_dur s) and its value label
        rides up with it; with num (and pre, suf, dec, comp) the label counts from 0 to num instead of showing the text `value`."""
        lines = _wrap(label, lfs, w + 90, 800)
        bar = f'<rect x="{-w / 2}" y="{-h}" width="{w}" height="{h}" rx="18" fill="{_c(color)}"/><rect x="{-w / 2}" y="{-24}" width="{w}" height="24" fill="{_c(color)}"/>'
        if not grow_at:
            out = bar + _text(0, -h - 22, _fmt(num, dec, pre, suf, comp) if num is not None else value, fs, color)
        else:
            q = _q(grow_at, grow_delay); cid = _cid("bar", x, y, w, h, color, label, grow_at)
            spec = dict(q, dur=float(grow_dur), dir="up", ease="out", box=[-w / 2 - 4, -h - 4, w + 8, h + 8])
            out = (f'<clipPath id="{cid}"><rect data-fx="clip" data-nodraw="1" data-spec="{_mat(spec)}" x="{-w / 2 - 4}" y="{-h - 4}" width="{w + 8}" height="0"/></clipPath>'
                   f'<g clip-path="url(#{cid})">{bar}</g>')
            lab = (_count(0, -22, 0.0, [dict(q, dur=float(grow_dur), to=float(num))], fs, color, pre, suf, dec, comp) if num is not None else _text(0, -22, value, fs, color))
            M = {"x": 0, "y": 0, "move": [dict(q, dur=float(grow_dur), to=[0, -h], arc=0.0, ease="out")], "hide": q}
            out += f'<g data-fx="m" data-spec="{_mat(M)}">{lab}</g>'
        for j, ln in enumerate(lines): out += _text(0, 46 + j * lfs * 1.12, ln, lfs, "ink", 800)
        return g(x, y, s, out)

    def flat_bar_box(x, y, s=1.0, w=180, h=400, fs=54, **_):
        return [x - (w / 2 + 50) * s, y - (h + fs + 30) * s, (w + 100) * s, (h + fs + 110) * s]

    def flat_bracket(x, y, s=1.0, h=200, label="", color="amber", fs=40, num=None, pre="", suf="", dec=0, comp="", grow_at=None, grow_delay=0.0, grow_dur=0.6, **_):
        """A vertical gap bracket from y - h/2 to y + h/2 with a label pill to its right. grow_at "chunk:N" (18 Nov 2026): the bracket draws
        from the top down at that chunk (+ grow_delay, over grow_dur s), then the pill pops in; with num (and pre, suf, dec, comp) the pill
        counts from 0 to num (label is then ignored)."""
        c = _c(color)
        path = f'<path d="M-18 {-h / 2} H0 V{h / 2} H-18" fill="none" stroke="{c}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
        txt = _fmt(num, dec, pre, suf, comp) if num is not None else label
        if grow_at:
            q = _q(grow_at, grow_delay); cid = _cid("brk", x, y, h, label, num, grow_at)
            spec = dict(q, dur=float(grow_dur), dir="down", ease="out", box=[-30, -h / 2 - 10, 50, h + 20])
            out = (f'<clipPath id="{cid}"><rect data-fx="clip" data-nodraw="1" data-spec="{_mat(spec)}" x="-30" y="{-h / 2 - 10}" width="50" height="0"/></clipPath>'
                   f'<g clip-path="url(#{cid})">{path}</g>')
        else: out = path
        if txt:
            tw = _tw(txt, fs) + 40
            pill = f'<rect data-fb="1" x="20" y="{-fs * 0.85}" width="{tw:.1f}" height="{fs * 1.7:.1f}" rx="{fs * 0.85:.1f}" fill="{c}"/>'
            if grow_at and num is not None:
                pill += _count(20 + tw / 2, fs * 0.36, 0.0, [dict(q, delay=q["delay"] + grow_dur * 0.6, dur=0.6, to=float(num))], fs, "ink", pre, suf, dec, comp)
            else: pill += _text(20 + tw / 2, fs * 0.36, txt, fs, "ink")
            if grow_at:
                o, cl = at_attr(q["at"], 20 + tw / 2, 0, q["delay"] + grow_dur * 0.6); pill = o + pill + cl
            out += pill
        return g(x, y, s, out)

    def icon(kind, cx, cy, k=1.0):
        if kind == "rocket":
            inner = (f'<path d="M0 -46 Q26 -20 22 22 H-22 Q-26 -20 0 -46 Z" fill="#FFFFFF"/><circle cx="0" cy="-8" r="9" fill="{FLAT["blue2"]}"/>'
                     f'<path d="M-22 6 L-36 30 H-22 Z M22 6 L36 30 H22 Z" fill="{FLAT["red"]}"/><path d="M-12 24 Q0 54 12 24 Z" fill="{FLAT["sun"]}"/>')
        else:   # book
            inner = (f'<rect x="-32" y="-38" width="64" height="76" rx="8" fill="#FFFFFF"/><rect x="-32" y="-38" width="12" height="76" rx="4" fill="{FLAT["amber"]}"/>'
                     f'<rect x="-10" y="-20" width="32" height="7" rx="3" fill="{FLAT["blue2"]}"/><rect x="-10" y="-6" width="24" height="7" rx="3" fill="{FLAT["pale"]}"/>')
        return f'<g transform="translate({cx} {cy}) scale({k})">{inner}</g>'

    def flat_list(x, y, s=1.0, w=420, title="Top startups", icon_kind="rocket", n=3, missing=2, fs=40, rh=74, color="blue", **_):
        """A ranked list card: a coloured header with an icon and the title, n ranked rows (number and a bar) and `missing`
        dashed rows with a question mark, for the ones nobody lists."""
        c = _c(color); H = 120 + rh * (n + missing) + 20
        out = (f'<rect data-fb="1" x="{-w / 2}" y="{-H / 2}" width="{w}" height="{H}" rx="26" fill="{FLAT["ice"]}"/>'
               f'<path d="M{-w / 2} {-H / 2 + 26} Q{-w / 2} {-H / 2} {-w / 2 + 26} {-H / 2} H{w / 2 - 26} Q{w / 2} {-H / 2} {w / 2} {-H / 2 + 26} V{-H / 2 + 110} H{-w / 2} Z" fill="{c}"/>'
               + icon(icon_kind, -w / 2 + 62, -H / 2 + 56, 0.95))
        tl = _wrap(title, fs, w - 140, 900)
        for j, ln in enumerate(tl): out += _text(-w / 2 + 118, -H / 2 + 56 + fs * 0.36 + (j - (len(tl) - 1) / 2) * fs * 1.05, ln, fs, "white", 900, "start")
        for i in range(n + missing):
            ry = -H / 2 + 130 + rh * i; miss = i >= n
            if miss:
                out += (f'<rect x="{-w / 2 + 22}" y="{ry}" width="{w - 44}" height="{rh - 16}" rx="16" fill="none" stroke="{FLAT["slate"]}" stroke-width="4" stroke-dasharray="12 10" opacity="0.7"/>'
                        + _text(0, ry + (rh - 16) / 2 + 14, "?", 38, "slate"))
            else:
                out += (f'<rect x="{-w / 2 + 22}" y="{ry}" width="{w - 44}" height="{rh - 16}" rx="16" fill="#FFFFFF"/>'
                        + _text(-w / 2 + 52, ry + (rh - 16) / 2 + 13, str(i + 1), 36, c, 900)
                        + f'<rect x="{-w / 2 + 84}" y="{ry + (rh - 16) / 2 - 8}" width="{(w - 150) * (0.9 - 0.18 * i):.1f}" height="16" rx="8" fill="{FLAT["pale"]}"/>')
        return g(x, y, s, out)

    def flat_list_box(x, y, s=1.0, w=420, n=3, missing=2, rh=74, **_):
        H = (140 + rh * (n + missing)) * s
        return [x - w * s / 2, y - H / 2, w * s, H]

    def flat_bubble(x, y, s=1.0, text="?", fs=60, side="left", fill="white", color="ink", think=False, **_):
        """A speech bubble (think: a thought bubble) with short text; the tail points down-left or down-right toward the speaker."""
        w = max(_tw(text, fs) + 70, fs * 1.9); h = fs * 1.9; sx = -1 if side == "left" else 1
        tail = (f'<circle cx="{sx * w * 0.28:.1f}" cy="{h / 2 + 18:.1f}" r="13" fill="{_c(fill)}"/><circle cx="{sx * w * 0.38:.1f}" cy="{h / 2 + 44:.1f}" r="8" fill="{_c(fill)}"/>' if think else
                f'<path d="M{sx * w * 0.12:.1f} {h / 2 - 4:.1f} L{sx * w * 0.36:.1f} {h / 2 + 40:.1f} L{sx * w * 0.3:.1f} {h / 2 - 4:.1f} Z" fill="{_c(fill)}"/>')
        return g(x, y, s, f'<rect x="{-w / 2 + 8:.1f}" y="{-h / 2 + 12:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h / 2:.1f}" fill="{FLAT["deep"]}" opacity="0.14"/>'
                          f'<rect data-fb="1" x="{-w / 2:.1f}" y="{-h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h / 2:.1f}" fill="{_c(fill)}"/>' + tail + _text(0, fs * 0.36, text, fs, color))

    def flat_bubble_box(x, y, s=1.0, text="?", fs=60, **_):
        w = max(_tw(text, fs) + 70, fs * 1.9) * s; h = fs * 1.9 * s
        return [x - w / 2, y - h / 2, w, h + 40 * s]

    def flat_person(x, y, s=1.0, shirt="amber", hair="#3B2A20", skin="#F2C49B", hold=None, flip=False, cap=False, **_):
        """A simple flat person (the saver), (x, y) = between the feet; hold "brochure" holds a little leaflet; cap = a graduation cap."""
        sh = _c(shirt)
        inner = (f'<ellipse cx="0" cy="2" rx="46" ry="9" fill="#000" opacity="0.12"/>'
                 f'<rect x="-30" y="-70" width="24" height="70" rx="10" fill="{FLAT["deep"]}"/><rect x="6" y="-70" width="24" height="70" rx="10" fill="{FLAT["deep"]}"/>'
                 f'<path d="M-44 -66 V-150 Q-44 -186 0 -186 Q44 -186 44 -150 V-66 Z" fill="{sh}"/><path d="M14 -186 Q44 -186 44 -150 V-66 H14 Z" fill="#000" opacity="0.08"/>'
                 f'<rect x="-10" y="-206" width="20" height="26" fill="{skin}"/>'
                 f'<circle cx="0" cy="-238" r="40" fill="{skin}"/><path d="M-41 -240 Q-40 -284 0 -282 Q40 -284 41 -244 Q20 -262 -10 -258 Q-30 -256 -41 -240 Z" fill="{hair}"/>'
                 f'<circle cx="-13" cy="-236" r="5" fill="{FLAT["ink"]}"/><circle cx="13" cy="-236" r="5" fill="{FLAT["ink"]}"/>'
                 f'<path d="M-11 -218 Q0 -210 11 -218" fill="none" stroke="{FLAT["ink"]}" stroke-width="4" stroke-linecap="round"/>')
        if hold == "brochure":
            inner += (f'<path d="M40 -150 Q64 -128 52 -110" fill="none" stroke="{sh}" stroke-width="18" stroke-linecap="round"/>'
                      f'<g transform="rotate(-10 70 -130)"><rect x="40" y="-176" width="70" height="90" rx="8" fill="#FFFFFF"/><rect x="40" y="-176" width="70" height="24" rx="8" fill="{FLAT["blue"]}"/>'
                      f'<rect x="52" y="-140" width="20" height="16" fill="{FLAT["blue2"]}"/><rect x="78" y="-140" width="20" height="16" fill="{FLAT["amber"]}"/></g>'
                      f'<circle cx="54" cy="-110" r="12" fill="{skin}"/>')
        if cap:
            inner += (f'<path d="M0 -306 L64 -284 L0 -262 L-64 -284 Z" fill="{FLAT["ink"]}"/><path d="M-34 -276 V-262 Q0 -248 34 -262 V-276 L0 -264 Z" fill="#334155"/>'
                      f'<path d="M54 -281 V-246" stroke="{FLAT["sun"]}" stroke-width="5"/><circle cx="54" cy="-243" r="6" fill="{FLAT["sun"]}"/>')
        return g(x, y, s, inner if not flip else f'<g transform="scale(-1 1)">{inner}</g>')

    def flat_person_box(x, y, s=1.0, **_):
        return [x - 60 * s, y - 285 * s, 120 * s, 290 * s]

    def flat_ring(x, y, s=1.0, rx=300, ry=120, color="green", dashed=False, width=10, fill_opacity=0.12, **_):
        """A soft highlight ring around a group (a halo for survivors, a dashed amber ring for the missing ones)."""
        c = _c(color); da = ' stroke-dasharray="26 18"' if dashed else ""
        return g(x, y, s, f'<ellipse rx="{rx}" ry="{ry}" fill="{c}" fill-opacity="{fill_opacity}" stroke="{c}" stroke-width="{width}"{da} stroke-linecap="round"/>')

    def flat_ring_box(x, y, s=1.0, rx=300, ry=120, **_):
        return [x - rx * s, y - ry * s, 2 * rx * s, 2 * ry * s]

    def flat_building(x, y, s=1.0, w=180, h=320, color="pale", roof=None, windows=True, **_):
        """A plain flat town building, (x, y) = bottom centre."""
        c = _c(color); win = ""
        if windows:
            for r in range(int((h - 60) // 70)):
                for k in range(int((w - 30) // 50)):
                    win += f'<rect x="{-w / 2 + 24 + k * 50}" y="{-h + 34 + r * 70}" width="26" height="36" rx="5" fill="#FFFFFF" opacity="0.85"/>'
        rf = f'<rect x="{-w / 2 - 8}" y="{-h - 16}" width="{w + 16}" height="22" rx="8" fill="{_c(roof)}"/>' if roof else ""
        return g(x, y, s, f'<rect x="{-w / 2}" y="{-h}" width="{w}" height="{h}" rx="10" fill="{c}"/><rect x="{w / 4}" y="{-h}" width="{w / 4}" height="{h}" fill="#000" opacity="0.06"/>' + rf + win)

    def flat_building_box(x, y, s=1.0, w=180, h=320, **_):
        return [x - w * s / 2, y - h * s, w * s, h * s]

    # ---- episode-2 props (17 Nov 2026): icons, tiles, chips, ruler, magnifier, checklist, quote, ranked table, connector, stat sign, bush, fence
    def _ico(kind, k=1.0, sym="€"):
        """a flat icon about 100 units wide centred on (0, 0)"""
        B, B2, N, Y, A, G, R, W, I = FLAT["blue"], FLAT["blue2"], FLAT["navy"], FLAT["sun"], FLAT["amber"], FLAT["green"], FLAT["red"], "#FFFFFF", FLAT["ink"]
        d = {
            "home": f'<path d="M-44 -6 L0 -46 L44 -6 Z" fill="{B}"/><rect x="-34" y="-8" width="68" height="50" fill="{W}"/><rect x="-10" y="12" width="20" height="30" rx="4" fill="{N}"/><rect x="14" y="0" width="14" height="14" rx="2" fill="{Y}"/>',
            "clock": f'<circle r="44" fill="{W}"/><circle r="44" fill="none" stroke="{B}" stroke-width="9"/><path d="M0 0 V-26 M0 0 L18 10" stroke="{I}" stroke-width="7" stroke-linecap="round"/>',
            "heart": f'<path d="M0 40 C-60 0 -40 -46 0 -18 C40 -46 60 0 0 40 Z" fill="{R}"/><circle cx="-18" cy="-14" r="7" fill="#FFF" opacity="0.5"/>',
            "coin": f'<circle r="42" fill="{A}"/><circle r="30" fill="none" stroke="#C2922F" stroke-width="5"/><text y="14" text-anchor="middle" {FONT} font-weight="900" font-size="40" fill="#8A5A12">{_h.escape(sym)}</text>',
            "apple": f'<circle cx="-14" cy="6" r="32" fill="{R}"/><circle cx="14" cy="6" r="32" fill="{R}"/><path d="M2 -26 q4 -16 14 -20" stroke="{FLAT["wood"]}" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M8 -30 q22 -14 30 2 q-18 10 -30 -2 Z" fill="{G}"/>',
            "car": f'<path d="M-50 10 V-6 Q-50 -14 -40 -16 L-26 -36 H24 L40 -16 Q50 -14 50 -6 V10 Z" fill="{B2}"/><rect x="-18" y="-30" width="16" height="14" fill="#EAF2FF"/><rect x="4" y="-30" width="16" height="14" fill="#EAF2FF"/><circle cx="-28" cy="14" r="11" fill="{I}"/><circle cx="28" cy="14" r="11" fill="{I}"/>',
            "book": f'<rect x="-36" y="-44" width="72" height="88" rx="8" fill="{B}"/><rect x="-36" y="-44" width="14" height="88" rx="5" fill="{N}"/><rect x="-14" y="-24" width="38" height="8" rx="4" fill="#FFF"/>',
            "people": f'<circle cx="-20" cy="-22" r="16" fill="{A}"/><path d="M-46 34 Q-46 -2 -20 -2 Q6 -2 6 34 Z" fill="{A}"/><circle cx="22" cy="-16" r="15" fill="{B2}"/><path d="M-2 36 Q-2 4 22 4 Q46 4 46 36 Z" fill="{B2}"/>',
            "sprout": f'<path d="M0 40 V-6" stroke="{G}" stroke-width="8" stroke-linecap="round"/><path d="M0 -4 Q-40 -10 -40 -42 Q-6 -40 0 -4 Z" fill="{G}"/><path d="M0 6 Q38 2 40 -28 Q8 -30 0 6 Z" fill="#7DD3A0"/><rect x="-30" y="34" width="60" height="12" rx="6" fill="{FLAT["wood"]}"/>',
            "notebook_old": f'<rect x="-36" y="-44" width="72" height="88" rx="6" fill="#D9C7A3"/><path d="M-36 -30 H36 M-36 -10 H36 M-36 10 H36 M-36 30 H36" stroke="#B9A47C" stroke-width="3"/><circle cx="20" cy="-26" r="9" fill="#B9773E" opacity="0.7"/><circle cx="-16" cy="22" r="7" fill="#B9773E" opacity="0.6"/><path d="M-44 -40 l10 8 M-44 -20 l10 8 M-44 0 l10 8 M-44 20 l10 8" stroke="{FLAT["slate"]}" stroke-width="4"/>',
            "puzzled": f'<circle r="44" fill="{Y}"/><circle cx="-15" cy="-8" r="6" fill="{I}"/><circle cx="15" cy="-8" r="6" fill="{I}"/><path d="M-16 20 Q-4 12 6 20 Q12 24 18 18" fill="none" stroke="{I}" stroke-width="5" stroke-linecap="round"/><path d="M-24 -26 l12 -4 M12 -28 l12 6" stroke="{I}" stroke-width="5" stroke-linecap="round"/>',
            "cap": f'<path d="M0 -36 L52 -14 L0 8 L-52 -14 Z" fill="{I}"/><path d="M-30 -4 V22 Q0 40 30 22 V-4 L0 8 Z" fill="#334155"/><path d="M42 -10 V20" stroke="{Y}" stroke-width="5"/><circle cx="42" cy="24" r="6" fill="{Y}"/>',
            "paper": f'<path d="M-32 -44 H16 L34 -26 V44 H-32 Z" fill="#FFFFFF"/><path d="M16 -44 V-26 H34 Z" fill="{FLAT["pale"]}"/><path d="M-20 -14 H22 M-20 2 H22 M-20 18 H10" stroke="{B2}" stroke-width="6" stroke-linecap="round"/>',
            "grade": f'<rect x="-40" y="-44" width="80" height="88" rx="10" fill="#FFFFFF"/><text y="18" text-anchor="middle" {FONT} font-weight="900" font-size="50" fill="{B}">A+</text>',
            "smile": f'<circle r="44" fill="{G}"/><circle cx="-15" cy="-8" r="6" fill="#FFF"/><circle cx="15" cy="-8" r="6" fill="#FFF"/><path d="M-20 12 Q0 32 20 12" fill="none" stroke="#FFF" stroke-width="6" stroke-linecap="round"/>',
            "comment": f'<path d="M-44 -30 Q-44 -42 -32 -42 H32 Q44 -42 44 -30 V14 Q44 26 32 26 H-6 L-26 42 V26 H-32 Q-44 26 -44 14 Z" fill="{B}"/><circle cx="-18" cy="-8" r="6" fill="#FFF"/><circle cx="0" cy="-8" r="6" fill="#FFF"/><circle cx="18" cy="-8" r="6" fill="#FFF"/>',
        }.get(kind, f'<circle r="40" fill="{B}"/>')
        return f'<g transform="scale({k})">{d}</g>'

    def flat_icon(x, y, s=1.0, kind="home", rot=0, sym="€", **_):
        """A flat icon (about 100 px wide at s 1): home, clock, heart, coin, apple, car, book, people, sprout, notebook_old, puzzled, cap, paper, grade, smile, comment.
        sym: the coin's currency sign ("€" by default; "$", "£")."""
        return g(x, y, s, _ico(kind, sym=sym), rot)

    def flat_tile(x, y, s=1.0, kind="sprout", label="", w=220, fs=34, fill="white", **_):
        """A rounded tile with a big icon and a short label under it."""
        h = 230 if label else 170
        out = (f'<rect x="{-w / 2 + 8}" y="{-h / 2 + 12}" width="{w}" height="{h}" rx="30" fill="{FLAT["deep"]}" opacity="0.14"/>'
               f'<rect data-fb="1" x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="30" fill="{_c(fill)}"/>' + f'<g transform="translate(0 {-h / 2 + 88})">{_ico(kind, 1.1)}</g>')
        if label:
            for j, ln in enumerate(_wrap(label, fs, w - 24, 800)[:2]): out += _text(0, h / 2 - 34 - (len(_wrap(label, fs, w - 24, 800)[:2]) - 1 - j) * fs * 1.08, ln, fs, "ink", 800)
        return g(x, y, s, out)

    def flat_tile_box(x, y, s=1.0, w=220, label="", **_):
        h = (230 if label else 170) * s
        return [x - w * s / 2, y - h / 2, w * s, h]

    def flat_chip(x, y, s=1.0, kind="grade", label="", fs=40, fill="white", color="ink", **_):
        """A pill with a small icon and a label (one way to measure something)."""
        w = _tw(label, fs, 800) + 120; h = fs * 1.9
        return g(x, y, s, f'<rect x="{-w / 2 + 6}" y="{-h / 2 + 9}" width="{w:.1f}" height="{h:.1f}" rx="{h / 2:.1f}" fill="{FLAT["deep"]}" opacity="0.14"/>'
                          f'<rect data-fb="1" x="{-w / 2:.1f}" y="{-h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h / 2:.1f}" fill="{_c(fill)}"/>'
                          f'<g transform="translate({-w / 2 + h / 2 + 6:.1f} 0)">{_ico(kind, h / 125)}</g>' + _text(-w / 2 + h + 18, fs * 0.36, label, fs, color, 800, "start"))

    def flat_chip_box(x, y, s=1.0, label="", fs=40, **_):
        w = (_tw(label, fs, 800) + 120) * s; h = fs * 1.9 * s
        return [x - w / 2, y - h / 2, w, h]

    def flat_ruler(x, y, s=1.0, w=420, **_):
        """A flat yellow ruler lying flat, with ticks and numbers."""
        t = "".join(f'<rect x="{-w / 2 + 14 + k * (w - 28) / 20:.1f}" y="-26" width="3" height="{22 if k % 5 == 0 else 12}" fill="{FLAT["ink"]}"/>' for k in range(21))
        nums = "".join(_text(-w / 2 + 15 + k * (w - 28) / 4, 22, str(k), 22, "ink", 800) for k in range(5))
        return g(x, y, s, f'<rect x="{-w / 2 + 6}" y="-26" width="{w}" height="60" rx="8" fill="{FLAT["deep"]}" opacity="0.14"/><rect x="{-w / 2}" y="-32" width="{w}" height="60" rx="8" fill="{FLAT["sun"]}"/>' + t + nums)

    def flat_ruler_box(x, y, s=1.0, w=420, **_):
        return [x - w * s / 2, y - 32 * s, w * s, 66 * s]

    def flat_magnifier(x, y, s=1.0, r=110, **_):
        """A big magnifying glass; (x, y) = the centre of the lens."""
        return g(x, y, s, f'<path d="M{r * 0.7:.1f} {r * 0.7:.1f} L{r * 1.5:.1f} {r * 1.5:.1f}" stroke="{FLAT["navy"]}" stroke-width="{r * 0.28:.1f}" stroke-linecap="round"/>'
                          f'<circle r="{r}" fill="#EAF2FF" fill-opacity="0.45" stroke="{FLAT["ink"]}" stroke-width="{r * 0.13:.1f}"/><path d="M{-r * 0.55:.1f} {-r * 0.3:.1f} Q{-r * 0.4:.1f} {-r * 0.6:.1f} {-r * 0.05:.1f} {-r * 0.62:.1f}" fill="none" stroke="#FFFFFF" stroke-width="{r * 0.09:.1f}" stroke-linecap="round"/>')

    def flat_checklist(x, y, s=1.0, w=620, lines=None, tick_at=None, fs=42, rh=104, title="", **_):
        """A clean card of tick-box rows; tick_at = one "chunk:N" per row for its tick (a green box with a white tick pops in)."""
        lines = lines or []; top = 96 if title else 26; H = top + rh * len(lines) + 10
        out = (f'<rect x="{-w / 2 + 8}" y="{-H / 2 + 14}" width="{w}" height="{H}" rx="30" fill="{FLAT["deep"]}" opacity="0.14"/><rect data-fb="1" x="{-w / 2}" y="{-H / 2}" width="{w}" height="{H}" rx="30" fill="#FFFFFF"/>')
        if title: out += _text(0, -H / 2 + 62, title, 40, "blue", 900)
        for i, ln in enumerate(lines):
            ry = -H / 2 + top + rh * i + rh / 2; bx = -w / 2 + 34
            out += f'<rect x="{bx}" y="{ry - 30}" width="60" height="60" rx="14" fill="none" stroke="{FLAT["mist"]}" stroke-width="6"/>'
            o, cl = at_attr((tick_at or [None] * len(lines))[i], bx + 30, ry)
            out += o + f'<rect x="{bx}" y="{ry - 30}" width="60" height="60" rx="14" fill="{FLAT["green"]}"/><path d="M{bx + 14} {ry} l11 12 l22 -24" fill="none" stroke="#FFF" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>' + cl
            parts = _wrap(ln, fs, w - 150, 800)
            for j, pt in enumerate(parts): out += _text(bx + 86, ry + fs * 0.36 + (j - (len(parts) - 1) / 2) * fs * 1.08, pt, fs, "ink", 800, "start")
        return g(x, y, s, out)

    def flat_checklist_box(x, y, s=1.0, w=620, lines=None, rh=104, title="", **_):
        H = ((96 if title else 26) + rh * len(lines or []) + 10) * s
        return [x - w * s / 2, y - H / 2, w * s, H]

    def flat_quote(x, y, s=1.0, w=900, text="", credit="", fs=62, cfs=40, **_):
        """A quote card: a big blue quote mark, the quote wrapped and centred, and the credit line in blue."""
        lines = _balance(_wrap(text, fs, w - 120, 900), fs, 900) if len(_wrap(text, fs, w - 120, 900)) == 2 else _wrap(text, fs, w - 120, 900)
        H = 120 + len(lines) * fs * 1.16 + (cfs * 1.8 if credit else 0) + 40
        out = (f'<rect x="{-w / 2 + 10}" y="{-H / 2 + 16}" width="{w}" height="{H:.1f}" rx="44" fill="{FLAT["deep"]}" opacity="0.16"/><rect data-fb="1" x="{-w / 2}" y="{-H / 2:.1f}" width="{w}" height="{H:.1f}" rx="44" fill="#FFFFFF"/>'
               + _text(0, -H / 2 + 112, "“", 150, "blue", 900))
        for j, ln in enumerate(lines): out += _text(0, -H / 2 + 120 + fs * 0.9 + j * fs * 1.16, ln, fs, "ink", 900)
        if credit: out += _text(0, H / 2 - 40, credit, cfs, "blue", 800)
        return g(x, y, s, out)

    def flat_quote_box(x, y, s=1.0, w=900, text="", credit="", fs=62, cfs=40, **_):
        H = (120 + len(_wrap(text, fs, w - 120, 900)) * fs * 1.16 + (cfs * 1.8 if credit else 0) + 40) * s
        return [x - w * s / 2, y - H / 2, w * s, H]

    PILL = {"Ana": "blue", "Ben": "amber", "Cara": "green", "Dev": "#8B5CF6"}

    def flat_rank(x, y, s=1.0, w=420, title="", rows=None, color="blue", fs=40, rh=96, row_at=None, every=0.15, **_):
        """A ranked table: a coloured header, then rows of rank number, a coloured name pill (one colour per person, so a change of
        order is easy to see) and a value. rows = [[name, value], ...]; row_at "chunk:N" pops the rows in one by one, every s apart."""
        rows = rows or []; H = 100 + rh * len(rows) + 16; c = _c(color)
        out = (f'<rect x="{-w / 2 + 8}" y="{-H / 2 + 14}" width="{w}" height="{H}" rx="26" fill="{FLAT["deep"]}" opacity="0.14"/><rect data-fb="1" x="{-w / 2}" y="{-H / 2}" width="{w}" height="{H}" rx="26" fill="#FFFFFF"/>'
               f'<path d="M{-w / 2} {-H / 2 + 26} Q{-w / 2} {-H / 2} {-w / 2 + 26} {-H / 2} H{w / 2 - 26} Q{w / 2} {-H / 2} {w / 2} {-H / 2 + 26} V{-H / 2 + 88} H{-w / 2} Z" fill="{c}"/>'
               + _text(0, -H / 2 + 58, title, 38, "white", 900))
        for i, (nm, val) in enumerate(rows):
            ry = -H / 2 + 100 + rh * i + rh / 2; pc = _c(PILL.get(nm, "blue"))
            o, cl = at_attr(row_at, 0, ry, 0.001 + every * i) if row_at else ("", "")
            pw = _tw(nm, fs - 4, 900) + 44
            out += (o + _text(-w / 2 + 40, ry + 14, str(i + 1), 40, "slate", 900)
                    + f'<rect x="{-w / 2 + 70}" y="{ry - 30}" width="{pw:.1f}" height="60" rx="30" fill="{pc}"/>' + _text(-w / 2 + 70 + pw / 2, ry + 13, nm, fs - 4, "white", 900)
                    + _text(w / 2 - 26, ry + 14, val, fs, "ink", 900, "end") + cl)
        return g(x, y, s, out)

    def flat_rank_box(x, y, s=1.0, w=420, rows=None, rh=96, **_):
        H = (116 + rh * len(rows or [])) * s
        return [x - w * s / 2, y - H / 2, w * s, H]

    def flat_connector(x, y, s=1.0, to=None, color="blue", width=8, **_):
        """A soft S-curve from (x, y) to `to` (world coordinates), with round ends; draw it in with "reveal"."""
        x1, y1 = (to or [x + 200, y]); mx = (x + x1) / 2
        return (f'<path d="M{_f(x)} {_f(y)} C{_f(mx)} {_f(y)} {_f(mx)} {_f(y1)} {_f(x1)} {_f(y1)}" fill="none" stroke="{_c(color)}" stroke-width="{width}" stroke-linecap="round" opacity="0.85"/>'
                f'<circle cx="{_f(x)}" cy="{_f(y)}" r="{width}" fill="{_c(color)}"/><circle cx="{_f(x1)}" cy="{_f(y1)}" r="{width}" fill="{_c(color)}"/>')

    def flat_connector_box(x, y, s=1.0, to=None, **_):
        x1, y1 = (to or [x + 200, y])
        return [min(x, x1) - 10, min(y, y1) - 10, abs(x1 - x) + 20, abs(y1 - y) + 20]

    def flat_stat(x, y, s=1.0, w=560, big="73%", note="Example", fs=170, **_):
        """A statistic sign: a big number in a clean card, grey placeholder lines for the headline, and a small note pill."""
        H = fs + 230
        out = (f'<rect x="{-w / 2 + 10}" y="{-H / 2 + 16}" width="{w}" height="{H}" rx="40" fill="{FLAT["deep"]}" opacity="0.16"/><rect data-fb="1" x="{-w / 2}" y="{-H / 2}" width="{w}" height="{H}" rx="40" fill="#FFFFFF"/>'
               + _text(0, -H / 2 + 40 + fs * 0.82, big, fs, "blue", 900)
               + f'<rect x="{-w / 2 + 50}" y="{-H / 2 + fs + 80}" width="{w - 100}" height="20" rx="10" fill="{FLAT["mist"]}"/><rect x="{-w / 2 + 50}" y="{-H / 2 + fs + 118}" width="{(w - 100) * 0.7:.1f}" height="20" rx="10" fill="{FLAT["mist"]}"/>')
        if note:
            tw = _tw(note, 28) + 40
            out += f'<rect x="{-tw / 2:.1f}" y="{H / 2 - 64}" width="{tw:.1f}" height="44" rx="22" fill="#E2E8F0"/>' + _text(0, H / 2 - 33, note, 28, "slate", 900)
        return g(x, y, s, out)

    def flat_stat_box(x, y, s=1.0, w=560, fs=170, **_):
        H = (fs + 230) * s
        return [x - w * s / 2, y - H / 2, w * s, H]

    def flat_bush(x, y, s=1.0, color="grass3", flowers=True, **_):
        """A round flat bush, (x, y) = bottom centre, with a few flowers."""
        c = _c(color)
        out = f'<ellipse cx="0" cy="0" rx="96" ry="12" fill="#000" opacity="0.08"/><circle cx="-50" cy="-40" r="46" fill="{c}"/><circle cx="10" cy="-66" r="58" fill="{c}"/><circle cx="60" cy="-38" r="44" fill="{c}"/><rect x="-96" y="-40" width="196" height="40" rx="20" fill="{c}"/><circle cx="22" cy="-80" r="22" fill="#FFF" opacity="0.12"/>'
        if flowers: out += "".join(f'<circle cx="{fx}" cy="{fy}" r="8" fill="{fc}"/>' for fx, fy, fc in [(-52, -46, FLAT["sun"]), (14, -84, "#FFFFFF"), (58, -40, FLAT["sun"]), (-12, -30, "#FFFFFF")])
        return g(x, y, s, out)

    def flat_fence(x, y, s=1.0, n=6, **_):
        """A low white picket fence, (x, y) = bottom left."""
        out = f'<rect x="0" y="-62" width="{n * 46}" height="12" rx="6" fill="#FFFFFF"/><rect x="0" y="-30" width="{n * 46}" height="12" rx="6" fill="#FFFFFF"/>'
        out += "".join(f'<path d="M{8 + k * 46} 0 V-80 L{22 + k * 46} -96 L{36 + k * 46} -80 V0 Z" fill="#FFFFFF"/>' for k in range(n))
        return g(x, y, s, f'<g opacity="0.95">{out}</g>')

    def flat_campus(x, y, s=1.0, w=520, h=430, **_):
        """A flat university hall with columns, steps and a flag, (x, y) = bottom centre."""
        cols = "".join(f'<rect x="{-w / 2 + 50 + k * (w - 100) / 5:.1f}" y="{-h + 150}" width="34" height="{h - 200}" fill="#FFFFFF"/>' for k in range(6))
        return g(x, y, s, f'<rect x="{-w / 2}" y="{-h + 120}" width="{w}" height="{h - 120}" fill="{FLAT["pale"]}"/>' + cols +
                 f'<path d="M{-w / 2 - 30} {-h + 124} L0 {-h} L{w / 2 + 30} {-h + 124} Z" fill="{FLAT["blue"]}"/><circle cx="0" cy="{-h + 74}" r="22" fill="#FFFFFF"/>'
                 f'<rect x="{-w / 2 - 20}" y="-50" width="{w + 40}" height="24" fill="#E2E8F0"/><rect x="{-w / 2 - 40}" y="-26" width="{w + 80}" height="26" fill="#CBD5E1"/>'
                 f'<path d="M{w / 2 - 40} {-h + 70} V{-h - 90}" stroke="{FLAT["navy"]}" stroke-width="8"/><path d="M{w / 2 - 40} {-h - 90} L{w / 2 + 40} {-h - 70} L{w / 2 - 40} {-h - 50} Z" fill="{FLAT["amber"]}"/>')

    def flat_logo(x, y, s=1.0, w=300, **_):
        """The Edlintics logo (render.html's logo/edlintics-logo.png, 654x170) centred on (x, y), w wide."""
        h = w * 170 / 654
        return f'<image href="logo/edlintics-logo.png" x="{_f(x - w * s / 2)}" y="{_f(y - h * s / 2)}" width="{_f(w * s)}" height="{_f(h * s)}"/>'

    # ---- numbers and sentences on screen (18 Nov 2026; Hoang: "Put more effort on tone explaining and visual to display the number and
    # sentences"). Every spoken number gets a big animated number, and the key sentence of a beat gets a clean card whose words light up with
    # the caption chunks. Timing keys are the usual "chunk:N" (counted over all the beats that share the scene) plus a delay in seconds.
    _fmt, _mat = G["_m_fmt"], G["_m_attr"]

    def _q(a, delay=0.0):
        """a timing key: "chunk:N" or {"at", "delay"} -> {"at", "delay"}"""
        if isinstance(a, dict): return {"at": str(a.get("at", "chunk:0")), "delay": float(a.get("delay", 0) or 0) + delay}
        return {"at": str(a or "chunk:0"), "delay": float(delay)}

    def _cid(*a):
        return "fc" + hashlib.sha1(repr(a).encode()).hexdigest()[:12]

    def _count(x, y, frm, keys, fs, col, pre="", suf="", dec=0, comp="", plus=False, anchor="middle", wt=900):
        """a number the renderer ticks (render.html fx.count): frm, then each key {"at","delay","dur","to"} in turn, eased out"""
        S = {"from": frm, "keys": keys, "dec": dec, "pre": pre, "suf": suf, "comp": comp, "plus": plus, "ease": "out"}
        return (f'<text data-fx="count" data-spec="{_mat(S)}" x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {FONT} font-weight="{wt}" font-size="{fs}" '
                f'fill="{_c(col)}">{_h.escape(_fmt(frm, dec, pre, suf, comp, plus))}</text>')

    def _shadow_card(w, h, rx=44, fill="white", y0=None):
        y0 = -h / 2 if y0 is None else y0
        return (f'<rect x="{-w / 2 + 10:.1f}" y="{y0 + 16:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{FLAT["deep"]}" opacity="0.16"/>'
                f'<rect data-fb="1" x="{-w / 2:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{_c(fill)}"/>')

    def _num_layout(value, start, keys, pre, suf, dec, comp, plus, label, fs, lfs, pill, w):
        vals = [start, value] + [k.get("to", 0) for k in (keys or [])]
        tw = max(_tw(_fmt(v, dec, pre, suf, comp, plus), fs) for v in vals) * 1.2   # Inter 900 digits run wider than _tw
        lab = _wrap(label, lfs, 900, 800) if label else []
        W = w or max(tw + 130, max([_tw(l, lfs, 800) for l in lab] + [0]) + 110, (_tw(pill, 32) + 120) if pill else 0, 380)
        H = 44 + (70 if pill else 0) + fs * 0.98 + (len(lab) * lfs * 1.18 + 14 if lab else 0) + 40
        return W, H, lab

    def flat_number(x, y, s=1.0, value=0, start=0, keys=None, pre="", suf="", dec=0, comp="", plus=False, label="", pill="", fs=190, lfs=46,
                    color="blue", card=True, w=None, count=True, count_at=None, count_delay=0.1, dur=0.9, pill_fill="blue", **_):
        """A big number that counts to its value as the voice says it, on a clean card. value: the number (5000); pre "€", "$", "£";
        suf "%", "m", " customers"; dec decimals; comp "K"/"M" (shows €5K); plus shows "+". The item's "at" pops the card in, and the count
        starts at count_at (default the same chunk) + count_delay over dur s, from start (default 0). keys [{"at","delay","dur","to"}] = several
        steps (count up, then down). count false = show the value at once. label: a short line under it ("per customer"); pill: a tag on top."""
        at = count_at or _.get("at") or "chunk:0"
        W, H, lab = _num_layout(value, start, keys, pre, suf, dec, comp, plus, label, fs, lfs, pill, w)
        out = _shadow_card(W, H) if card else ""
        yy = -H / 2 + 44
        if pill:
            pw = _tw(pill, 32) + 56; out += f'<rect data-fb="1" x="{-pw / 2:.1f}" y="{yy:.1f}" width="{pw:.1f}" height="54" rx="27" fill="{_c(pill_fill)}"/>' + _text(0, yy + 38, pill, 32, "white"); yy += 70
        base = yy + fs * 0.76
        if count:
            K = [dict(_q(k), dur=float(k.get("dur", dur)), to=float(k["to"])) for k in keys] if keys else [dict(_q(at, count_delay), dur=float(dur), to=float(value))]
            out += _count(0, base, float(start), K, fs, color, pre, suf, dec, comp, plus)
        else:
            out += _text(0, base, _fmt(value, dec, pre, suf, comp, plus), fs, color)
        yy += fs * 0.98 + 14
        for j, ln in enumerate(lab): out += _text(0, yy + lfs * 0.9 + j * lfs * 1.18, ln, lfs, "ink", 800)
        return g(x, y, s, out)

    def flat_number_box(x, y, s=1.0, value=0, start=0, keys=None, pre="", suf="", dec=0, comp="", plus=False, label="", pill="", fs=190, lfs=46, w=None, **_):
        W, H, _l = _num_layout(value, start, keys, pre, suf, dec, comp, plus, label, fs, lfs, pill, w)
        return [x - W * s / 2, y - H * s / 2, W * s, H * s]

    OPS = {"+", "-", "−", "×", "x", "÷", "/", "=", "≈"}

    def _eq_layout(terms, fs, w, wrap_at, pad, title, tfs, result):
        T = [t if isinstance(t, dict) else {"t": str(t)} for t in (terms or [])]
        res = len(T) - 1 if result is None else result
        rows = [list(range(len(T)))] if not wrap_at else [list(range(wrap_at)), list(range(wrap_at, len(T)))]

        def widths(f):
            ws = []
            for i, q in enumerate(T):
                op = q["t"] in OPS; tw = _tw(q["t"], f * (0.9 if op else 1)) * (1.3 if op else 1.14)
                ws.append(tw + (f * 0.56 if i == res else 0))
            return ws
        gapf = 0.36
        f = fs
        for _i in range(30):   # shrink until the widest row fits
            ws = widths(f)
            if max(sum(ws[i] for i in r) + gapf * f * (len(r) - 1) for r in rows) <= w - 2 * pad: break
            f *= 0.95
        notes = any(q.get("note") for q in T)
        rh = f * 1.5 + (f * 0.36 + 10 if notes else 0)
        H = pad * 0.8 + (tfs * 1.6 if title else 0) + rh * len(rows) + pad * 0.6
        return T, res, rows, f, widths(f), gapf, rh, H, notes

    def flat_equation(x, y, s=1.0, terms=None, result=None, fs=130, w=960, wrap_at=None, title="", tfs=40, card=True, pad=50, color="ink", **_):
        """A worked equation whose terms appear one by one as the voice says them, with the result in a blue pill. terms: a list of strings
        or {"t", "at", "delay", "note", "color"} ("note" = a small grey label under the term, such as "ad spend"); operators + − × ÷ = are
        drawn lighter. Each term with an "at" pops in at that chunk (+ delay); terms without one show with the card. result: the index of the
        highlighted term (default the last). wrap_at: start a second row at that index. The font shrinks so the widest row fits w."""
        T, res, rows, f, ws, gapf, rh, H, notes = _eq_layout(terms, fs, w, wrap_at, pad, title, tfs, result)
        out = _shadow_card(w, H) if card else ""
        yy = -H / 2 + pad * 0.8
        if title: out += _text(0, yy + tfs * 0.95, title, tfs, "blue", 900); yy += tfs * 1.6
        for r in rows:
            tot = sum(ws[i] for i in r) + gapf * f * (len(r) - 1); cx = -tot / 2; cy = yy + f * 0.72
            for i in r:
                q = T[i]; op = q["t"] in OPS; mid = cx + ws[i] / 2
                if i == res:
                    ph = f * 1.24
                    inner = (f'<rect data-fb="1" x="{cx:.1f}" y="{cy - ph / 2:.1f}" width="{ws[i]:.1f}" height="{ph:.1f}" rx="{ph / 2:.1f}" fill="{FLAT["blue"]}"/>'
                             + _text(mid, cy + f * 0.35, q["t"], f, "white", 900))
                else:
                    inner = _text(mid, cy + f * (0.32 if op else 0.35), q["t"], f * (0.9 if op else 1), q.get("color", "slate" if op else color), 800 if op else 900)
                if q.get("note"): inner += _text(mid, cy + f * 0.62 + f * 0.36 + 6, q["note"], max(30, f * 0.33), "slate", 800)
                o, c = at_attr(q.get("at"), mid, cy, q.get("delay", 0) or 0)
                out += o + inner + c
                cx += ws[i] + gapf * f
            yy += rh
        return g(x, y, s, out)

    def flat_equation_box(x, y, s=1.0, terms=None, result=None, fs=130, w=960, wrap_at=None, title="", tfs=40, pad=50, **_):
        H = _eq_layout(terms, fs, w, wrap_at, pad, title, tfs, result)[7]
        return [x - w * s / 2, y - H * s / 2, w * s, H * s]

    def _wf_layout(steps, rh, title):
        return 40 + (96 if title else 0) + rh * len(steps or []) + 10

    def flat_waterfall(x, y, s=1.0, steps=None, w=920, rh=150, title="", pre="", suf="", dec=0, comp="", fs=42, vfs=64, dur=0.7, max_v=None, **_):
        """Money flowing down, as a step table: one row per step with its label, a bar that grows to its value and a value that counts.
        steps: [{"label", "v", "at", "delay", "total"}]: the first is the starting amount (blue bar from 0), a negative v is a cost (red bar
        that grows leftward from the running total, value "−$2m"), a positive v later is a gain (green), and total true is what is left
        (green bar from 0; v defaults to the running total). Dashed lines link each bar end to the next row. pre, suf, dec, comp format the
        values ($7m: pre "$", suf "m"). Each row appears at its "at" (+ delay); the bar grows and the value counts over dur s."""
        steps = steps or []; H = _wf_layout(steps, rh, title); pad = 44; valw = max(_tw(_fmt(-abs(q.get("v", 0) or 0), dec, pre, suf, comp), vfs) for q in steps) + 30 if steps else 200
        bx0 = -w / 2 + pad; BW = w - 2 * pad - valw - 20
        run, spans = 0.0, []
        for i, q in enumerate(steps):
            v = float(q.get("v", run) if q.get("total") else q.get("v", 0))
            if q.get("total"): a, b, kind = 0.0, v, "total"
            elif i == 0: a, b, kind = 0.0, v, "start"
            elif v < 0: a, b, kind = run + v, run, "minus"
            else: a, b, kind = run, run + v, "plus"
            if not q.get("total"): run = run + v if i else v
            spans.append((a, b, kind, v))
        M = float(max_v or max([b for a, b, k, v in spans] + [1]))
        X = lambda v: bx0 + BW * v / M
        COL = {"start": "blue", "minus": "red", "plus": "green", "total": "green"}
        out = _shadow_card(w, H, 34)
        top = -H / 2 + 20
        if title:
            out += (f'<path d="M{-w / 2} {-H / 2 + 34} Q{-w / 2} {-H / 2} {-w / 2 + 34} {-H / 2} H{w / 2 - 34} Q{w / 2} {-H / 2} {w / 2} {-H / 2 + 34} V{-H / 2 + 90} H{-w / 2} Z" fill="{FLAT["blue"]}"/>'
                    + _text(0, -H / 2 + 60, title, 38, "white", 900)); top += 96
        bh = 54
        for i, (q, (a, b, kind, v)) in enumerate(zip(steps, spans)):
            ry = top + rh * i; by = ry + fs * 1.25 + 8; col = _c(COL[kind]); qa = _q(q.get("at"), q.get("delay", 0) or 0)
            o, c = at_attr(q.get("at"), 0, by + bh / 2, (q.get("delay", 0) or 0)) if q.get("at") else ("", "")
            band = (f'<rect x="{-w / 2 + 12}" y="{ry - 6:.1f}" width="{w - 24}" height="{rh - 8:.1f}" rx="22" fill="{FLAT["green"]}" opacity="0.10"/>' if kind == "total" else "")
            if i:
                xs = X(spans[i - 1][1] if spans[i - 1][2] != "minus" else spans[i - 1][0])
                band += f'<path d="M{xs:.1f} {ry - rh + fs * 1.25 + 8 + bh:.1f} V{by:.1f}" stroke="{FLAT["slate"]}" stroke-width="4" stroke-dasharray="8 9" opacity="0.6"/>'
            lab = _text(bx0, ry + fs * 0.95, q.get("label", ""), fs, "green" if kind == "total" else "ink", 900 if kind == "total" else 800, "start")
            x1, x2 = X(a), X(b); cid = _cid("wf", i, q.get("label"), v, x, y)
            spec = dict(qa, delay=qa["delay"] + 0.12, dur=float(dur), dir="left" if kind == "minus" else "right", ease="out", box=[x1 - 4, by - 4, x2 - x1 + 8, bh + 8])
            clip = (f'<clipPath id="{cid}"><rect data-fx="clip" data-nodraw="1" data-spec="{_mat(spec)}" x="{x1 - 4:.1f}" y="{by - 4:.1f}" width="0" height="{bh + 8}"/></clipPath>' if q.get("at") else "")
            bar = f'<rect x="{x1:.1f}" y="{by:.1f}" width="{max(6, x2 - x1):.1f}" height="{bh}" rx="14" fill="{col}"/>'
            bar = f'{clip}<g clip-path="url(#{cid})">{bar}</g>' if q.get("at") else bar
            K = [dict(qa, delay=qa["delay"] + 0.12, dur=float(dur), to=v)]
            val = (_count(w / 2 - pad, by + bh / 2 + vfs * 0.36, 0.0, K, vfs, COL[kind], pre, suf, dec, comp, anchor="end") if q.get("at")
                   else _text(w / 2 - pad, by + bh / 2 + vfs * 0.36, _fmt(v, dec, pre, suf, comp), vfs, COL[kind], 900, "end"))
            out += o + band + lab + bar + val + c
        return g(x, y, s, out)

    def flat_waterfall_box(x, y, s=1.0, steps=None, w=920, rh=150, title="", **_):
        H = _wf_layout(steps, rh, title)
        return [x - w * s / 2, y - H * s / 2, w * s, H * s]

    def _tokens(parts, key):
        toks = []
        for pi, p in enumerate(parts):
            for wi, wd in enumerate(str(p).split()): toks.append([wd, pi, wi, False])
        norm = lambda z: _h.unescape(z).lower().strip(".,;:!?\"'“”‘’()")
        for ph in ([key] if isinstance(key, str) else (key or [])):
            kw = [norm(z) for z in str(ph).split()]
            for i in range(len(toks) - len(kw) + 1):
                if kw and [norm(toks[i + j][0]) for j in range(len(kw))] == kw:
                    for j in range(len(kw)): toks[i + j][3] = True
        return toks

    def _sent_lines(toks, fs, width):
        lines, cur = [], []
        for t in toks:
            if cur and _tw(" ".join(z[0] for z in cur + [t]), fs) > width: lines.append(cur); cur = [t]
            else: cur.append(t)
        if cur: lines.append(cur)
        if len(lines) >= 2:   # balance the last two lines, so the card never ends on one short word
            a = lines[-2] + lines[-1]
            best = min(range(1, len(a)), key=lambda i: max(_tw(" ".join(z[0] for z in a[:i]), fs), _tw(" ".join(z[0] for z in a[i:]), fs)))
            if _tw(" ".join(z[0] for z in a[:best]), fs) <= width: lines[-2:] = [a[:best], a[best:]]
        return lines

    def _sent_layout(text, parts, key, fs, w, pad, pill):
        parts = parts or [text]; toks = _tokens(parts, key)
        f = fs
        for _i in range(12):   # at most 4 lines: shrink the font a little before a fifth line
            lines = _sent_lines(toks, f, w - 2 * pad)
            if len(lines) <= 4: break
            f *= 0.94
        H = pad + (76 if pill else 0) + len(lines) * f * 1.18 + pad * 0.8
        return parts, lines, f, H

    def flat_sentence(x, y, s=1.0, text="", parts=None, part_at=None, key=None, w=940, fs=72, pad=54, pill="", pill_fill="blue", ghost=0.14,
                      stagger=0.07, color="ink", key_color="blue", card=True, **_):
        """The key sentence of a beat (a definition, a rule, a takeaway) as a large clean card, its words lighting up with the caption chunks
        and the key word or phrase in Edlintics blue. parts: the sentence split as the beat's caption chunks (their texts joined = the
        sentence); part_at: one "chunk:N" (or {"at","delay"}) per part, or one "chunk:N" for consecutive chunks from N; each part's words
        light up (from `ghost` opacity, 0 = hidden) with a stagger of `stagger` s. Without part_at the whole sentence shows with the card.
        key: a word or phrase (or a list) drawn in blue. pill: a small tag on top ("Definition", "Rule", "Takeaway"). Lines wrap and balance;
        more than 4 lines shrink the font. Keep the card in the upper half of the screen: the captions sit at y 1320-1530"""
        parts, lines, f, H = _sent_layout(text, parts, key, fs, w, pad, pill)
        if isinstance(part_at, (str, dict)) or part_at is None:
            base = part_at
            if base is None: PA = [None] * len(parts)
            else:
                q0 = _q(base); n0 = int(q0["at"].split(":")[1])
                PA = [{"at": f"chunk:{n0 + i}", "delay": q0["delay"]} for i in range(len(parts))]
        else: PA = [(_q(a) if a else None) for a in part_at] + [None] * max(0, len(parts) - len(part_at))
        out = _shadow_card(w, H) if card else ""
        yy = -H / 2 + pad
        if pill:
            pw = _tw(pill, 32) + 56; out += f'<rect data-fb="1" x="{-pw / 2:.1f}" y="{yy - 8:.1f}" width="{pw:.1f}" height="56" rx="28" fill="{_c(pill_fill)}"/>' + _text(0, yy + 31, pill, 32, "white"); yy += 76
        for li, ln in enumerate(lines):
            spans = ""
            for k, (wd, pi, wi, isk) in enumerate(ln):
                col = _c(key_color if isk else color); sp = (" " if k else "") + _h.escape(wd)
                q = PA[pi] if pi < len(PA) else None
                if q:
                    S = {"at": q["at"], "delay": q["delay"] + stagger * wi, "g": float(ghost)}
                    spans += f'<tspan data-fx="wd" data-spec="{_mat(S)}" fill="{col}" fill-opacity="{ghost}">{sp}</tspan>'
                else: spans += f'<tspan fill="{col}">{sp}</tspan>'
            out += f'<text x="0" y="{yy + f * 0.88 + li * f * 1.18:.1f}" text-anchor="middle" {FONT} font-weight="900" font-size="{f:.1f}" letter-spacing="-0.5">{spans}</text>'
        return g(x, y, s, out)

    def flat_sentence_box(x, y, s=1.0, text="", parts=None, key=None, w=940, fs=72, pad=54, pill="", **_):
        H = _sent_layout(text, parts, key, fs, w, pad, pill)[3]
        return [x - w * s / 2, y - H * s / 2, w * s, H * s]

    # ---- Ledger v2 (17 Nov 2026, flat style only): the website's revamped rigged Ledger, read at build time from the brand hand-off
    # folder (assets/brand-handoff/ledger-v2/rig/ledger-rig.svg, git-ignored; override with LEDGER_V2_DIR). Never copied into tracked
    # files: the art lands only in the render work folder (assets/renders, also git-ignored). render.html drives the parts per frame.
    import os as _os, re as _re, json as _json
    _RIG = {"n": 0, "svg": None}

    def _rig_svg():
        if _RIG["svg"] is None:
            base = _os.environ.get("LEDGER_V2_DIR") or _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "../../../../assets/brand-handoff/ledger-v2"))
            f = _os.path.join(base, "rig", "ledger-rig.svg")
            if not _os.path.exists(f):
                raise SystemExit(f"ledger2: the Ledger v2 rig is missing ({f}). It comes from the website lane's brand hand-off (assets/brand-handoff/ledger-v2/, "
                                 "git-ignored, see its README.md). Ask for the export, or set LEDGER_V2_DIR to the folder that holds rig/ledger-rig.svg")
            s = open(f).read()
            s = s[s.index(">", s.index("<svg")) + 1: s.rindex("</svg>")]
            s = _re.sub(r"<title>.*?</title>", "", s)
            s = _re.sub(r'\sdata-p="[^"]*"', "", s)
            s = _re.sub(r'\sid="([^"]*)"', r' data-r="\1"', s)
            _RIG["svg"] = s
        return _RIG["svg"]

    def _held(kind):
        if kind == "ruler":
            ticks = "".join(f'<path d="M-9 {-66 + 11 * k} h{8 if k % 2 else 12}" stroke="#0f172a" stroke-width="2"/>' for k in range(9))
            return f'<g data-r2="ruler" display="none"><rect x="-9" y="-72" width="20" height="110" rx="3" fill="#FFD45C" stroke="#0f172a" stroke-width="2.5"/>{ticks}</g>'
        return ('<g data-r2="magnifier" display="none"><path d="M0 -6 V-22" stroke="#0f172a" stroke-width="8" stroke-linecap="round"/>'
                '<circle cx="0" cy="-46" r="24" fill="#EAF2FF" fill-opacity="0.75" stroke="#0f172a" stroke-width="5"/><path d="M-10 -56 q8 -6 16 -2" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/></g>')

    def ledger2(x, y, s=1.0, poses=None, walks=None, talk=True, flip=False, seed=1, **_):
        """Ledger v2, the website's rigged mascot (flat style only), (x, y) = between his feet. poses: [{"at": "chunk:N", "delay": s, "pose": name}]
        with names idle, talk, wave, point_right, point_left, point_up, think, happy, shrug, hold_ruler, point_ruler, hold_magnifier, nod;
        walks: [{"at", "delay", "dur"}] swing the legs while a "move" carries him; talk false = no lip sync. Blink, breathing, sway and arm drift always run."""
        _RIG["n"] += 1; n = _RIG["n"]
        body = _rig_svg().replace('data-r="ml"', f'id="ml{n}"').replace("url(#ml)", f"url(#ml{n})")
        for side in ("R", "L"):
            for c in ("b", "f"):
                hid = f'data-r="arm{side}-{c}-hand"'
                i = body.find(hid)
                if i < 0: continue
                j = body.index(">", i) + 1
                body = body[:j] + _held("ruler") + _held("magnifier") + body[j:]
        spec = {"poses": poses or [], "walks": walks or [], "talk": bool(talk), "seed": seed}
        k = -s if flip else s
        return (f'<g data-led2="{_m_attr(spec)}" transform="translate({_f(x - 120 * k)} {_f(y - 236 * s)}) scale({_f(k)} {_f(s)})">' + body + "</g>")

    def ledger2_box(x, y, s=1.0, **_):
        return [x - 125 * s, y - 220 * s, 250 * s, 222 * s]

    G["PRESETS"].update({
        "flat_rect": (flat_rect, flat_rect_box), "flat_path": (flat_path, lambda *a, **k: [0, 0, 1, 1]), "flat_sun": (flat_sun, None),
        "flat_cloud": (flat_cloud, None), "flat_tree": (flat_tree, None), "flat_house": (flat_house, flat_house_box), "flat_sparkle": (flat_sparkle, None),
        "flat_arrow": (flat_arrow, None), "flat_tag": (flat_tag, flat_tag_box), "flat_card": (flat_card, flat_card_box), "flat_board": (flat_board, flat_board_box),
        "flat_brochure": (flat_brochure, flat_brochure_box), "flat_table": (flat_table, flat_table_box), "flat_bar": (flat_bar, flat_bar_box),
        "flat_bracket": (flat_bracket, None), "flat_list": (flat_list, flat_list_box), "flat_bubble": (flat_bubble, flat_bubble_box),
        "flat_person": (flat_person, flat_person_box), "flat_ring": (flat_ring, flat_ring_box), "flat_building": (flat_building, flat_building_box),
        "ledger2": (ledger2, ledger2_box), "flat_icon": (flat_icon, None), "flat_tile": (flat_tile, flat_tile_box), "flat_chip": (flat_chip, flat_chip_box),
        "flat_ruler": (flat_ruler, flat_ruler_box), "flat_magnifier": (flat_magnifier, None), "flat_checklist": (flat_checklist, flat_checklist_box),
        "flat_quote": (flat_quote, flat_quote_box), "flat_rank": (flat_rank, flat_rank_box), "flat_connector": (flat_connector, flat_connector_box),
        "flat_stat": (flat_stat, flat_stat_box), "flat_number": (flat_number, flat_number_box), "flat_equation": (flat_equation, flat_equation_box),
        "flat_waterfall": (flat_waterfall, flat_waterfall_box), "flat_sentence": (flat_sentence, flat_sentence_box), "flat_bush": (flat_bush, None), "flat_fence": (flat_fence, None), "flat_campus": (flat_campus, None), "flat_logo": (flat_logo, None)})
    G["HALF"].update({"flat_sun": (150, 150), "flat_cloud": (110, 90), "flat_tree": (62, 100), "flat_sparkle": (34, 34), "flat_arrow": (34, 40), "flat_bracket": (60, 120), "flat_icon": (50, 50), "flat_magnifier": (130, 130), "flat_bush": (100, 110), "flat_fence": (140, 50), "flat_campus": (300, 300)})
