"""Edlintics reel scene library: compose 1080x1920 scenes from named presets, never hand-written SVG.

A scene in script.json:
  "s1": {"bg": "office", "items": [
      {"p": "ledger", "x": 540, "y": 1470, "s": 2.4, "mood": "smile", "arm": "hold", "outfit": "suit"},
      {"p": "phone", "id": "app", "x": 300, "y": 880, "s": 1.0}]}
Coordinates are in the 1080x1920 art. Ledger's (x, y) is the point between his feet; every other prop's
(x, y) is its centre. The ground line is at y 1480. Draw order = list order (later items on top).
Run `python3 scene_lib.py --list` to print every preset with its options.
"""
import math, sys

INK = "#0F172A"; BLUE = "#467DE3"; NAVY = "#222C3D"; PAPER = "#FBFAF6"; LB = "#C9D8F5"
GOLD = "#C2922F"; SKY = "#E8F0FC"; GREY = "#9AA3B2"; GREEN = "#2FA36B"; CORAL = "#E2928B"; WHITE = "#FFFFFF"
SW = 6  # default stroke width


def _f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------- Ledger (from assets/brand/ledger.svg)
MOODS = ["smile", "happy", "frown", "sad", "flat", "o", "worried", "tired", "angry", "talk"]
ARMS = ["down", "hold", "up", "both_up", "point", "phone", "shrug", "wave", "mic"]
LARMS = ["down", "up_l", "point_l", "open_l", "shrug_l"]   # left-arm gestures (larm), used with arm "mic" in ledger-talks reels
OUTFITS = ["suit", "student", "casual", "sales"]


def _arm(path, hand):
    hx, hy = hand
    return (f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="13" stroke-linecap="round"/>'
            f'<path d="{path}" fill="none" stroke="{PAPER}" stroke-width="8" stroke-linecap="round"/>'
            f'<circle cx="{hx}" cy="{hy}" r="9" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')


def ledger(x, y, s=1.0, mood="smile", arm="down", outfit="suit", tilt=0, flip=False, larm=None, **_):
    """The Edlintics mascot (from assets/brand/ledger.svg). (x, y) = between his feet. mood, arm, outfit, tilt, flip, larm (left-arm gesture). mood "talk" lip-syncs to the voice; arm "mic" holds a small handheld mic."""
    mouth = {
        "smile": "M106 134 Q120 146 134 134", "happy": "M104 130 Q120 150 136 130",
        "frown": "M107 140 Q120 130 133 140", "sad": "M107 140 Q120 131 133 140",
        "flat": "M108 137 L132 137", "worried": "M108 139 Q114 134 120 138 Q126 142 132 137",
        "tired": "M110 138 L130 138", "angry": "M108 139 L132 139",
    }
    if mood == "talk":  # two mouths: the renderer shows "mo" (open) while the voice is loud and "mc" (closed) in pauses
        m = (f'<g class="mc"><path d="M108 136 Q120 145 132 136" fill="none" stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/></g>'
             f'<g class="mo" style="display:none"><path d="M108 133 Q120 131 132 133 Q131 148 120 149 Q109 148 108 133 Z" fill="{INK}"/>'
             f'<path d="M113 144 Q120 140 127 144 Q124 148 120 148 Q116 148 113 144 Z" fill="{CORAL}"/></g>')
    else:
        m = (f'<ellipse cx="120" cy="137" rx="6" ry="7" fill="{INK}"/>' if mood == "o" else
             f'<path d="{mouth.get(mood, mouth["smile"])}" fill="none" stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/>')
    if mood == "happy":  # closed happy eyes
        eyes = (f'<path d="M95 112 Q102 103 109 112" fill="none" stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/>'
                f'<path d="M131 112 Q138 103 145 112" fill="none" stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/>')
    else:
        eyes = (f'<circle cx="102" cy="110" r="7.5" fill="{INK}"/><circle cx="104.5" cy="107.5" r="2.2" fill="{WHITE}"/>'
                f'<circle cx="138" cy="110" r="7.5" fill="{INK}"/><circle cx="140.5" cy="107.5" r="2.2" fill="{WHITE}"/>')
        if mood == "tired":  # heavy lids
            eyes += (f'<path d="M93 108 H111" stroke="{PAPER}" stroke-width="9"/><path d="M129 108 H147" stroke="{PAPER}" stroke-width="9"/>'
                     f'<path d="M93 112 H111 M129 112 H147" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>')
    brows = ""
    if mood in ("frown", "angry"):
        brows = f'<path d="M93 96 L109 101 M147 96 L131 101" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    elif mood in ("sad", "worried"):
        brows = f'<path d="M93 101 L109 95 M147 101 L131 95" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    elif mood in ("flat", "o", "tired", "talk"):
        brows = f'<path d="M93 99 Q101 94 109 98 M131 98 Q139 94 147 99" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    extra = ""
    if mood == "worried":  # sweat drop
        extra = f'<path d="M166 70 q8 14 0 20 q-8 -6 0 -20 z" fill="{LB}" stroke="{INK}" stroke-width="2.5"/>'
    # body band, collar and tie by outfit
    band_col = {"suit": NAVY, "sales": NAVY, "student": BLUE, "casual": "#5B6B86"}.get(outfit, NAVY)
    band = f'<path d="M54.5 150 L185.5 150 L185.5 174 Q185.5 189.5 170 189.5 L70 189.5 Q54.5 189.5 54.5 174 Z" fill="{band_col}"/>'
    if outfit in ("suit", "sales"):
        collar = (f'<path d="M108 150 L120 168 L116 173 L102 154 Z" fill="{WHITE}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
                  f'<path d="M132 150 L120 168 L124 173 L138 154 Z" fill="{WHITE}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
                  f'<path d="M114 152 L126 152 L129 161 L111 161 Z" fill="{BLUE}"/><path d="M112 162 L128 162 L124 184 L120 189 L116 184 Z" fill="{BLUE}"/>')
    elif outfit == "casual":
        collar = (f'<path d="M106 150 L120 164 L134 150" fill="none" stroke="{WHITE}" stroke-width="5" stroke-linejoin="round"/>')
    else:  # student hoodie: drawstrings
        collar = (f'<path d="M110 150 v22 M130 150 v22" stroke="{WHITE}" stroke-width="4" stroke-linecap="round"/>'
                  f'<circle cx="110" cy="174" r="3.5" fill="{WHITE}"/><circle cx="130" cy="174" r="3.5" fill="{WHITE}"/>')
    behind = ""
    if outfit == "student":  # backpack peeking out on both sides
        behind = (f'<rect x="38" y="96" width="30" height="80" rx="10" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>'
                  f'<rect x="172" y="96" width="30" height="80" rx="10" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>')
    head = ""
    if outfit == "sales":  # headset
        head = (f'<path d="M58 70 Q120 6 182 70" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                f'<rect x="48" y="64" width="16" height="30" rx="7" fill="{INK}"/><path d="M58 92 Q66 128 98 130" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
                f'<circle cx="100" cy="130" r="5" fill="{INK}"/>')
    # arms: every pose keeps the brand proportions (assets/brand/ledger.svg): shoulder-to-hand 38-48 units,
    # arm stroke 13/8, hand r 9, so hands never look tiny or huge next to the body. See ARM_POSES and check_proportions().
    pose = ARM_POSES.get(arm, ARM_POSES["down"])
    right = _arm(*pose["R"]); left = _arm(*pose.get("L", ARM_POSES["down"]["L"]))
    if larm and larm != "down":
        left = _arm(*ARM_POSES.get(larm, ARM_POSES["down"]).get("L", ARM_POSES["down"]["L"]))
    prop = ""
    if arm == "mic":  # small handheld mic with a fuzzy windscreen, held at cheek height (drawn under the hand)
        fuzz = "".join(f'<path d="M{163 + 9 * math.cos(a):.1f} {139 + 9 * math.sin(a):.1f} l{3 * math.cos(a):.1f} {3 * math.sin(a):.1f}" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>' for a in [k * math.pi / 6 for k in range(12)])
        prop = (f'<path d="M199 122 L172 135" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
                f'<circle cx="163" cy="139" r="11" fill="#6B7280" stroke="{INK}" stroke-width="3"/>{fuzz}')
    if arm == "phone":
        prop = (f'<g transform="rotate(-14 200 92)"><rect x="185" y="60" width="30" height="58" rx="8" fill="{NAVY}" stroke="{INK}" stroke-width="3"/>'
                f'<rect x="190" y="68" width="20" height="38" rx="3" fill="{LB}"/></g>')
    body = (f'<g transform="rotate({tilt} 120 198)">'
            f'<rect x="52" y="38" width="136" height="154" rx="18" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'
            f'<line x1="70" y1="46" x2="70" y2="184" stroke="{INK}" stroke-width="3.5" opacity="0.45"/><line x1="74" y1="46" x2="74" y2="184" stroke="{INK}" stroke-width="1.5" opacity="0.25"/>'
            f'<path d="M150 34 h18 v26 l-9 -7 -9 7 z" fill="{BLUE}"/>'
            f'<rect x="86" y="58" width="60" height="6" rx="3" fill="#E6E3DA"/><rect x="86" y="70" width="60" height="6" rx="3" fill="#E6E3DA"/><rect x="86" y="82" width="40" height="6" rx="3" fill="#E6E3DA"/>'
            f'{band}{collar}{eyes}{brows}{m}{extra}{head}</g>')
    legs = (f'<ellipse cx="120" cy="236" rx="46" ry="7" fill="{INK}" opacity="0.10"/>'
            f'<line x1="102" y1="186" x2="102" y2="210" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
            f'<line x1="138" y1="186" x2="138" y2="210" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
            f'<rect x="88" y="208" width="29" height="14" rx="7" fill="{INK}"/><rect x="123" y="208" width="29" height="14" rx="7" fill="{INK}"/>')
    fl = " scale(-1 1) translate(-240 0)" if flip else ""
    return (f'<g transform="translate({_f(x)} {_f(y)}) scale({s}) translate(-120 -230){fl}">'
            f'{behind}{legs}{left}{body}{prop}{right}</g>')


# Arm poses, all measured against the brand file: shoulders at (62,152) and (178,152), hand r 9, arm 38-48 units long.
ARM_POSES = {
    "down":    {"R": ("M178 152 Q190 172 186 188", (186, 190)), "L": ("M62 152 Q50 172 54 188", (54, 190))},
    "hold":    {"R": ("M180 152 Q206 168 214 150", (215, 147))},
    "up":      {"R": ("M180 150 Q202 142 207 113", (208, 109))},
    "both_up": {"R": ("M180 150 Q202 142 207 113", (208, 109)), "L": ("M60 150 Q38 142 33 113", (32, 109))},
    "point":   {"R": ("M180 152 Q202 152 224 143", (227, 142))},
    "phone":   {"R": ("M180 152 Q208 140 198 116", (197, 112))},
    "shrug":   {"R": ("M180 152 Q212 150 210 124", (210, 120)), "L": ("M60 152 Q28 150 30 124", (30, 120))},
    "wave":    {"R": ("M180 152 Q207 144 204 116", (204, 112))},
    "mic":     {"R": ("M178 152 Q208 152 199 122", (198, 118))},
    # left-arm gestures (larm); mirrors of the right poses, same lengths
    "up_l":    {"L": ("M60 150 Q38 142 33 113", (32, 109))},
    "point_l": {"L": ("M60 152 Q38 152 16 143", (13, 142))},
    "open_l":  {"L": ("M60 152 Q34 168 26 150", (25, 147))},
    "shrug_l": {"L": ("M60 152 Q28 150 30 124", (30, 120))},
}
HAND_R, BODY_W = 9, 136


def check_proportions():
    """Return a list of problems if any arm pose breaks the brand proportions (run by validate.py on every build)."""
    import re as _re
    bad = []
    for name, pose in ARM_POSES.items():
        for side, (path, hand) in pose.items():
            sx, sy = map(float, _re.match(r"M([\d.]+) ([\d.]+)", path).groups())
            L = math.hypot(hand[0] - sx, hand[1] - sy)
            if not 30 <= L <= 50: bad.append(f"arm pose {name} {side}: shoulder-to-hand {L:.0f} units (brand 38-48)")
            if abs(sx - (62 if side == "L" else 178)) > 4: bad.append(f"arm pose {name} {side}: shoulder at x {sx:.0f}, not at the body edge")
    if not 0.06 <= HAND_R / BODY_W <= 0.075: bad.append("hand radius out of proportion with the body")
    return bad


def ledger_box(x, y, s=1.0, **_):
    return [x - 125 * s, y - 225 * s, 250 * s, 232 * s]


# ---------------------------------------------------------------- props (x, y = centre)
def _g(x, y, s, inner, rot=0):
    return f'<g transform="translate({_f(x)} {_f(y)}) rotate({rot}) scale({s})">{inner}</g>'


def person(x, y, s=1.0, mood="smile", color=None, **_):
    """A simple customer/classmate figure (round head, rounded body). (x, y) = between the feet."""
    c = color or LB
    mouth = {"smile": "M-12 -168 Q0 -158 12 -168", "flat": "M-11 -164 H11", "sad": "M-12 -160 Q0 -170 12 -160"}.get(mood, "M-12 -168 Q0 -158 12 -168")
    inner = (f'<ellipse cx="0" cy="4" rx="44" ry="7" fill="{INK}" opacity="0.10"/>'
             f'<path d="M-46 0 V-90 Q-46 -130 0 -130 Q46 -130 46 -90 V0 Z" fill="{c}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<circle cx="0" cy="-178" r="40" fill="{PAPER}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<circle cx="-13" cy="-184" r="5" fill="{INK}"/><circle cx="13" cy="-184" r="5" fill="{INK}"/>'
             f'<path d="{mouth}" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    return _g(x, y, s, inner)


def person_box(x, y, s=1.0, **_):
    return [x - 50 * s, y - 222 * s, 100 * s, 226 * s]


def people_group(x, y, s=1.0, n=4, busy=1, **_):
    """n people around a small table; `busy` of them (from the left) hold papers and look stressed."""
    out = f'<ellipse cx="0" cy="40" rx="230" ry="50" fill="{LB}" stroke="{INK}" stroke-width="{SW}"/>'
    xs = [(-260 + 520 * k / max(1, n - 1)) for k in range(n)]
    for k, px in enumerate(xs):
        mood = "sad" if k < busy else "smile"
        col = BLUE if k < busy else [LB, "#F3D9A6", "#CFE9D9", "#F2C7C2"][k % 4]
        out += person(px, 0, 0.8, mood=mood, color=col)
        if k < busy:
            out += f'<g transform="translate({px + 30} -70) rotate(-8)">' + paper_stack_inner() + '</g>'
        else:
            out += f'<path d="M{px - 10} -110 l-30 -20" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
    return _g(x, y, s, out)


def people_group_box(x, y, s=1.0, **_):
    return [x - 320 * s, y - 220 * s, 640 * s, 320 * s]


def paper_stack_inner():
    return "".join(f'<rect x="{-30 + k * 4}" y="{-40 - k * 8}" width="60" height="78" rx="4" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>' for k in range(3))


def phone(x, y, s=1.0, screen="empty", **_):
    """A big smartphone. screen: empty (no users, flat line), up (rising chart), call (call screen), chat."""
    inner = (f'<rect x="-150" y="-280" width="300" height="560" rx="40" fill="{WHITE}" stroke="{INK}" stroke-width="8"/>'
             f'<rect x="-125" y="-235" width="250" height="450" rx="12" fill="{SKY}"/>'
             f'<rect x="-30" y="232" width="60" height="10" rx="5" fill="{INK}" opacity="0.4"/>')
    if screen == "empty":
        inner += (f'<circle cx="0" cy="-120" r="38" fill="none" stroke="{GREY}" stroke-width="6" stroke-dasharray="12 10"/>'
                  f'<path d="M-62 -20 Q0 -80 62 -20" fill="none" stroke="{GREY}" stroke-width="6" stroke-dasharray="12 10"/>'
                  f'<path d="M-95 40 V170 H100" fill="none" stroke="{INK}" stroke-width="4"/><path d="M-95 160 H100" fill="none" stroke="{CORAL}" stroke-width="7" stroke-linecap="round"/>')
    elif screen == "up":
        inner += (f'<path d="M-95 -60 V170 H100" fill="none" stroke="{INK}" stroke-width="4"/>'
                  f'<path d="M-90 150 L-40 100 L0 120 L50 40 L95 -30" fill="none" stroke="{GREEN}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
    elif screen == "call":
        inner += (f'<circle cx="0" cy="-90" r="56" fill="{LB}" stroke="{INK}" stroke-width="5"/>'
                  f'<circle cx="-60" cy="130" r="34" fill="{CORAL}" stroke="{INK}" stroke-width="5"/><circle cx="60" cy="130" r="34" fill="{GREEN}" stroke="{INK}" stroke-width="5"/>')
    else:  # chat
        inner += (f'<rect x="-100" y="-200" width="160" height="60" rx="18" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>'
                  f'<rect x="-40" y="-110" width="140" height="60" rx="18" fill="{LB}" stroke="{INK}" stroke-width="4"/>'
                  f'<rect x="-100" y="-20" width="180" height="60" rx="18" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>')
    return _g(x, y, s, inner)


def laptop(x, y, s=1.0, screen="chart", **_):
    """Open laptop seen from the front. screen: chart, sheet (spreadsheet grid), empty."""
    inner = (f'<rect x="-180" y="-150" width="360" height="230" rx="16" fill="{NAVY}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<rect x="-160" y="-132" width="320" height="192" rx="6" fill="{SKY}"/>'
             f'<path d="M-230 80 H230 L210 110 H-210 Z" fill="{GREY}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>')
    if screen == "chart":
        inner += f'<path d="M-130 30 L-60 -20 L0 0 L70 -70 L130 -100" fill="none" stroke="{GREEN}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
    elif screen == "sheet":
        inner += "".join(f'<line x1="-160" y1="{yy}" x2="160" y2="{yy}" stroke="{INK}" stroke-width="2" opacity="0.4"/>' for yy in range(-100, 60, 32))
        inner += "".join(f'<line x1="{xx}" y1="-132" x2="{xx}" y2="60" stroke="{INK}" stroke-width="2" opacity="0.4"/>' for xx in (-80, 0, 80))
        inner += f'<rect x="0" y="-36" width="80" height="32" fill="{GOLD}" opacity="0.6"/>'
    return _g(x, y, s, inner)


def bills(x, y, s=1.0, n=4, **_):
    """A stack of n banknotes (money). (x, y) = the bottom note."""
    out = ""
    for k in range(int(n)):
        out += (f'<g transform="translate({k * 6} {-k * 22})"><rect x="-90" y="-40" width="180" height="80" rx="8" fill="{GREEN}" stroke="{INK}" stroke-width="5"/>'
                f'<circle cx="0" cy="0" r="22" fill="none" stroke="{INK}" stroke-width="4"/><rect x="-76" y="-28" width="152" height="56" rx="5" fill="none" stroke="{INK}" stroke-width="2" opacity="0.5"/></g>')
    return _g(x, y, s, out)


def coins(x, y, s=1.0, n=5, **_):
    """A stack of n gold coins. (x, y) = the bottom coin."""
    return _g(x, y, s, "".join(f'<ellipse cx="0" cy="{-k * 18}" rx="48" ry="16" fill="{GOLD}" stroke="{INK}" stroke-width="5"/>' for k in range(int(n))))


def calendar(x, y, s=1.0, mark=None, **_):
    """Wall calendar, no text. mark: day index 0-27 to circle (e.g. 2 = the 3rd)."""
    inner = (f'<rect x="-150" y="-170" width="300" height="340" rx="14" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<rect x="-150" y="-170" width="300" height="70" rx="14" fill="{CORAL}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<circle cx="-80" cy="-176" r="10" fill="{INK}"/><circle cx="80" cy="-176" r="10" fill="{INK}"/>')
    for k in range(28):
        cx, cy = -105 + (k % 7) * 35, -70 + (k // 7) * 55
        inner += f'<rect x="{cx - 12}" y="{cy - 12}" width="24" height="24" rx="4" fill="{SKY}"/>'
        if mark is not None and int(mark) == k:
            inner += f'<circle cx="{cx}" cy="{cy}" r="24" fill="none" stroke="{BLUE}" stroke-width="6"/>'
    return _g(x, y, s, inner)


def invoice(x, y, s=1.0, stamp=False, rot=0, **_):
    """A bill/invoice sheet with lines (no text). stamp=True adds a red due stamp circle."""
    inner = (f'<path d="M-110 -150 H80 L110 -120 V150 H-110 Z" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
             f'<path d="M80 -150 V-120 H110" fill="none" stroke="{INK}" stroke-width="4"/>'
             + "".join(f'<line x1="-80" y1="{yy}" x2="{60 if k % 2 else 80}" y2="{yy}" stroke="{GREY}" stroke-width="7" stroke-linecap="round"/>' for k, yy in enumerate(range(-100, 60, 36)))
             + f'<line x1="10" y1="105" x2="80" y2="105" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
    if stamp:
        inner += f'<circle cx="-40" cy="95" r="34" fill="none" stroke="{CORAL}" stroke-width="7"/>'
    return _g(x, y, s, inner, rot)


def chart(x, y, s=1.0, trend="up", **_):
    """Framed line chart on a wall or board. trend: up, down, flat."""
    pts = {"up": "-150 90 -70 40 0 60 80 -20 150 -80", "down": "-150 -80 -70 -20 0 -40 80 40 150 90", "flat": "-150 20 -70 30 0 15 80 25 150 20"}[trend]
    col = {"up": GREEN, "down": CORAL, "flat": GREY}[trend]
    inner = (f'<rect x="-200" y="-150" width="400" height="300" rx="10" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<path d="M-170 -120 V120 H180" fill="none" stroke="{INK}" stroke-width="4"/>'
             f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    return _g(x, y, s, inner)


def coffee(x, y, s=1.0, steam=True, **_):
    """A coffee cup with steam (steam=False to hide it)."""
    inner = (f'<path d="M-50 -60 H50 L42 60 Q40 70 30 70 H-30 Q-40 70 -42 60 Z" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
             f'<path d="M50 -30 Q90 -30 85 5 Q80 30 46 26" fill="none" stroke="{INK}" stroke-width="{SW}"/>'
             f'<rect x="-50" y="-20" width="100" height="34" fill="{GOLD}" opacity="0.7"/>')
    if steam:
        inner += f'<path d="M-20 -80 q-12 -20 0 -40 q12 -20 0 -40 M20 -80 q-12 -20 0 -40 q12 -20 0 -40" fill="none" stroke="{GREY}" stroke-width="5" stroke-linecap="round"/>'
    return _g(x, y, s, inner)


def window(x, y, s=1.0, weather="clear", **_):
    """A window. weather: clear (sun), rain (clouds and rain), night (moon)."""
    inner = (f'<rect x="-340" y="-260" width="680" height="520" rx="10" fill="{SKY}" stroke="{INK}" stroke-width="7"/>'
             f'<line x1="0" y1="-260" x2="0" y2="260" stroke="{INK}" stroke-width="7"/><line x1="-340" y1="0" x2="340" y2="0" stroke="{INK}" stroke-width="7"/>')
    if weather == "rain":
        inner += (f'<path d="M-240 -140 q20 -60 90 -50 q30 -50 100 -20 q70 -10 80 50 q50 10 40 60 H-240 q-50 -10 0 -40 z" fill="{GREY}" opacity="0.55" stroke="{INK}" stroke-width="5"/>'
                  f'<path d="M60 -160 q20 -50 80 -40 q40 -40 100 0 q50 10 40 60 H60 q-40 -10 0 -20 z" fill="{GREY}" opacity="0.55" stroke="{INK}" stroke-width="5"/>'
                  + "".join(f'<line x1="{xx}" y1="{yy}" x2="{xx - 18}" y2="{yy + 60}" stroke="{BLUE}" stroke-width="6" stroke-linecap="round"/>' for xx in range(-280, 320, 70) for yy in (-20, 100, 180)))
    elif weather == "night":
        inner = inner.replace(f'fill="{SKY}"', f'fill="{NAVY}"', 1) + f'<circle cx="170" cy="-140" r="50" fill="#F3E3B0" stroke="{INK}" stroke-width="5"/>'
    else:
        inner += f'<circle cx="170" cy="-140" r="56" fill="{GOLD}" opacity="0.8" stroke="{INK}" stroke-width="5"/>'
    return _g(x, y, s, inner)


def door(x, y, s=1.0, **_):
    """A tall door (leaving, going out)."""
    return _g(x, y, s, f'<rect x="-125" y="-360" width="250" height="720" rx="6" fill="{LB}" stroke="{INK}" stroke-width="7"/><circle cx="80" cy="10" r="12" fill="{INK}"/>')


def sofa(x, y, s=1.0, **_):
    """A sofa (staying home)."""
    return _g(x, y, s, (f'<path d="M-140 0 h280 v-70 q0 -30 -30 -30 h-220 q-30 0 -30 30 z" fill="{BLUE}" opacity="0.85" stroke="{INK}" stroke-width="{SW}"/>'
                        f'<rect x="-160" y="0" width="320" height="70" rx="20" fill="{BLUE}" stroke="{INK}" stroke-width="{SW}"/>'
                        f'<line x1="-130" y1="70" x2="-130" y2="100" stroke="{INK}" stroke-width="7"/><line x1="130" y1="70" x2="130" y2="100" stroke="{INK}" stroke-width="7"/>'))


def bed(x, y, s=1.0, **_):
    """A bed with a pillow and blanket (sleeping in)."""
    return _g(x, y, s, (f'<rect x="-220" y="-40" width="440" height="80" rx="16" fill="{LB}" stroke="{INK}" stroke-width="{SW}"/>'
                        f'<rect x="-210" y="-80" width="120" height="50" rx="20" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>'
                        f'<path d="M-90 -40 Q60 -90 210 -40" fill="{BLUE}" opacity="0.7" stroke="{INK}" stroke-width="5"/>'
                        f'<line x1="-210" y1="40" x2="-210" y2="80" stroke="{INK}" stroke-width="8"/><line x1="210" y1="40" x2="210" y2="80" stroke="{INK}" stroke-width="8"/>'))


def scale(x, y, s=1.0, tilt="level", left="coins", right="arrow", **_):
    """Balance scale; (x, y) = the pivot, the base stands 300 below it. tilt: level, left (left pan lower), right. left/right pan content: coins, bills, arrow, none."""
    a = {"level": 0, "left": -8, "right": 8}[tilt]

    def pan(px, content):
        c = {"coins": coins(0, -14, 0.8, 3), "bills": bills(0, -30, 0.55, 2),
             "arrow": f'<path d="M0 -20 V-110 M-36 -74 L0 -110 L36 -74" fill="none" stroke="{GREEN}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>',
             "none": ""}.get(content, "")
        return (f'<g transform="translate({px} 0)"><line x1="0" y1="0" x2="-40" y2="140" stroke="{INK}" stroke-width="4"/><line x1="0" y1="0" x2="40" y2="140" stroke="{INK}" stroke-width="4"/>'
                f'<g transform="translate(0 140)"><path d="M-70 0 h140 q-10 40 -70 40 q-60 0 -70 -40 z" fill="{LB}" stroke="{INK}" stroke-width="5"/>{c}</g></g>')
    beam = (f'<g transform="rotate({a})"><line x1="-200" y1="0" x2="200" y2="0" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
            f'<g transform="rotate({-a} -200 0)">{pan(-200, left)}</g><g transform="rotate({-a} 200 0)">{pan(200, right)}</g></g>')
    inner = (f'<path d="M0 300 V0" stroke="{INK}" stroke-width="10"/><path d="M-60 300 h120" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
             f'{beam}<circle cx="0" cy="0" r="14" fill="{INK}"/>')
    return _g(x, y, s, inner)


def scale_box(x, y, s=1.0, **_):
    return [x - 290 * s, y - 60 * s, 580 * s, 370 * s]


def pit(x, y, s=1.0, item="ticket", **_):
    """A dark hole in the ground (money lost for good). (x, y) = centre of the opening. item: ticket, coins, bills, none."""
    c = {"ticket": ticket(20, 300, 0.8, rot=24), "coins": coins(10, 330, 0.9, 3), "bills": bills(0, 320, 0.7, 2)}.get(item, "")
    inner = (f'<path d="M-480 0 H-210 M210 0 H480" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
             f'<path d="M-210 0 Q-210 520 0 520 Q210 520 210 0" fill="{NAVY}" stroke="{INK}" stroke-width="6"/>'
             f'<path d="M-170 80 q170 40 340 0 M-150 200 q150 40 300 0" fill="none" stroke="{LB}" stroke-width="4" opacity="0.35"/>{c}')
    return _g(x, y, s, inner)


def pit_box(x, y, s=1.0, **_):
    return [x - 300 * s, y - 120 * s, 600 * s, 660 * s]


def sun_arrow(x, y, s=1.0, **_):
    """A sun with a forward arrow: the future, what comes next."""
    rays = "".join(f'<line x1="{_f(110 * math.cos(a / 57.3))}" y1="{_f(110 * math.sin(a / 57.3))}" x2="{_f(145 * math.cos(a / 57.3))}" y2="{_f(145 * math.sin(a / 57.3))}" stroke="{GOLD}" stroke-width="7" stroke-linecap="round"/>' for a in range(0, 360, 45))
    inner = (f'<circle cx="0" cy="0" r="70" fill="{GOLD}" opacity="0.8" stroke="{INK}" stroke-width="6"/>{rays}'
             f'<path d="M-260 160 H-80 M-120 110 L-70 160 L-120 210" fill="none" stroke="{BLUE}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>')
    return _g(x, y, s, inner)


def handshake(x, y, s=1.0, **_):
    """Two hands shaking (a deal is closed)."""
    inner = (f'<path d="M-260 30 H-90 L-30 -10 Q0 -30 30 -10 L90 30 H260" fill="none" stroke="{INK}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<path d="M-260 30 H-90 L-30 -10 Q0 -30 30 -10 L90 30 H260" fill="none" stroke="{LB}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<path d="M-60 0 Q0 -60 60 0 Q0 50 -60 0 Z" fill="{PAPER}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<rect x="-300" y="0" width="60" height="70" rx="10" fill="{NAVY}" stroke="{INK}" stroke-width="5"/><rect x="240" y="0" width="60" height="70" rx="10" fill="{BLUE}" stroke="{INK}" stroke-width="5"/>')
    return _g(x, y, s, inner)


def whiteboard(x, y, s=1.0, drawing="graph", **_):
    """Whiteboard on a stand or wall. drawing: graph (supply/demand cross), lines (notes), boxes (diagram)."""
    inner = (f'<rect x="-350" y="-210" width="700" height="420" rx="12" fill="{WHITE}" stroke="{INK}" stroke-width="7"/>'
             f'<rect x="-120" y="210" width="240" height="14" rx="7" fill="{GREY}"/>')
    if drawing == "graph":
        inner += (f'<path d="M-240 -150 V150 H250" fill="none" stroke="{INK}" stroke-width="5"/>'
                  f'<path d="M-200 -120 L200 120" stroke="{BLUE}" stroke-width="9" stroke-linecap="round"/><path d="M-200 120 L200 -120" stroke="{GREEN}" stroke-width="9" stroke-linecap="round"/>'
                  f'<circle cx="0" cy="0" r="14" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>')
    elif drawing == "boxes":
        inner += (f'<rect x="-280" y="-60" width="150" height="110" rx="10" fill="{LB}" stroke="{INK}" stroke-width="5"/>'
                  f'<rect x="-60" y="-60" width="150" height="110" rx="10" fill="#F3D9A6" stroke="{INK}" stroke-width="5"/>'
                  f'<rect x="160" y="-60" width="130" height="110" rx="10" fill="#CFE9D9" stroke="{INK}" stroke-width="5"/>'
                  f'<path d="M-130 -5 H-60 M90 -5 H160" stroke="{INK}" stroke-width="5"/>')
    else:
        inner += "".join(f'<line x1="-280" y1="{yy}" x2="{200 - (k % 3) * 60}" y2="{yy}" stroke="{BLUE}" stroke-width="9" stroke-linecap="round"/>' for k, yy in enumerate(range(-140, 160, 60)))
    return _g(x, y, s, inner)


def desk(x, y, s=1.0, w=880, **_):
    """Office desk; (x, y) = centre of the desktop surface. w = width (default 880; 360 = a short desk segment).
    With Ledger in the scene the desk may run off the frame edges (a cropped desk edge) instead of shrinking him."""
    h = w / 2
    return _g(x, y, s, (f'<rect x="{-h}" y="-17" width="{w}" height="34" rx="8" fill="{NAVY}"/>'
                        f'<rect x="{-h + 40}" y="17" width="26" height="196" fill="{NAVY}"/><rect x="{h - 66}" y="17" width="26" height="196" fill="{NAVY}"/>'))


def desk_box(x, y, s=1.0, w=880, **_):
    return [x - w / 2 * s, y - 20 * s, w * s, 235 * s]


def school_desk(x, y, s=1.0, **_):
    """Small student desk with an open notebook; (x, y) = centre of the desktop."""
    return _g(x, y, s, (f'<rect x="-170" y="-14" width="340" height="28" rx="6" fill="{GOLD}" stroke="{INK}" stroke-width="5"/>'
                        f'<line x1="-140" y1="14" x2="-140" y2="180" stroke="{INK}" stroke-width="9"/><line x1="140" y1="14" x2="140" y2="180" stroke="{INK}" stroke-width="9"/>'
                        f'<path d="M-90 -14 L-80 -50 H0 L0 -14 M0 -14 L0 -50 H80 L90 -14" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>'))


def ticket(x, y, s=1.0, rot=0, faded=False, **_):
    """A gold event ticket. rot (degrees), faded=True for a ghost outline (money that is gone)."""
    op = ' opacity="0.35" stroke-dasharray="14 10"' if faded else ""
    fill = "none" if faded else GOLD
    inner = (f'<g{op}><path d="M-110 -55 H110 V-20 A20 20 0 0 0 110 20 V55 H-110 V20 A20 20 0 0 0 -110 -20 Z" fill="{fill}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
             f'<line x1="45" y1="-50" x2="45" y2="50" stroke="{INK}" stroke-width="4" stroke-dasharray="8 8"/>'
             f'<path d="M-40 -22 l9 18 20 3 -14 14 3 20 -18 -9 -18 9 3 -20 -14 -14 20 -3 z" fill="{"none" if faded else PAPER}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
             f'<path d="M70 -18 v30 m0 -30 l18 -6 v30" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/><circle cx="64" cy="13" r="6" fill="{INK}"/><circle cx="82" cy="7" r="6" fill="{INK}"/></g>')
    return _g(x, y, s, inner, rot)


def thought(x, y, s=1.0, inner="none", **_):
    """Thought bubble; inner = another preset name drawn small inside (ticket, coins, bills, invoice, calendar, coffee, bed, phone, chart)."""
    shape = (f'<path d="M-200 40 q-20 -70 60 -80 q20 -70 110 -40 q60 -60 130 0 q90 -10 80 70 q60 30 0 80 q-30 60 -120 30 q-60 50 -130 0 q-110 10 -130 -60 z" fill="{WHITE}" stroke="{INK}" stroke-width="6"/>'
             f'<circle cx="-40" cy="190" r="22" fill="{WHITE}" stroke="{INK}" stroke-width="5"/><circle cx="-10" cy="250" r="13" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>')
    c = PRESETS[inner][0](0, 10, 0.45) if inner in PRESETS and inner not in ("thought", "speech") else ""
    return _g(x, y, s, shape + c)


def thought_box(x, y, s=1.0, **_):
    return [x - 240 * s, y - 130 * s, 480 * s, 400 * s]


def speech(x, y, s=1.0, side="left", **_):
    """Speech bubble with lines (no words). side: which side the tail points to."""
    tail = "M-60 70 L-120 140 L-10 80" if side == "left" else "M60 70 L120 140 L10 80"
    return _g(x, y, s, (f'<rect x="-200" y="-90" width="400" height="170" rx="40" fill="{WHITE}" stroke="{INK}" stroke-width="6"/>'
                        f'<path d="{tail}" fill="{WHITE}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
                        f'<line x1="-130" y1="-25" x2="130" y2="-25" stroke="{GREY}" stroke-width="12" stroke-linecap="round"/>'
                        f'<line x1="-130" y1="25" x2="60" y2="25" stroke="{GREY}" stroke-width="12" stroke-linecap="round"/>'))


def building(x, y, s=1.0, done=False, **_):
    """A building; done=False draws it unfinished with a crane and a crack (a failing project)."""
    dash = "" if done else ' stroke-dasharray="26 14"'
    inner = (f'<rect x="-160" y="-310" width="320" height="620" fill="{LB}" opacity="0.6" stroke="{INK}" stroke-width="{SW}"{dash}/>'
             f'<path d="M-160 -110 H160 M-160 90 H160 M-55 -310 V310 M55 -310 V310" stroke="{INK}" stroke-width="4" opacity="0.5"/>')
    if not done:
        inner += (f'<path d="M-110 -530 V-310 M-110 -520 H190 M170 -520 v120" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
                  f'<rect x="150" y="-400" width="40" height="34" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>'
                  f'<path d="M30 -170 l40 60 -30 50 50 70" fill="none" stroke="{CORAL}" stroke-width="6"/>')
    return _g(x, y, s, inner)


def building_box(x, y, s=1.0, **_):
    return [x - 170 * s, y - 540 * s, 380 * s, 860 * s]


def clock(x, y, s=1.0, hour=8, **_):
    """A wall clock. hour sets the hour hand."""
    a_h = (hour % 12) * 30 - 90; a_m = -90
    return _g(x, y, s, (f'<circle cx="0" cy="0" r="110" fill="{WHITE}" stroke="{INK}" stroke-width="7"/>'
                        + "".join(f'<line x1="{_f(88 * math.cos(a / 57.3))}" y1="{_f(88 * math.sin(a / 57.3))}" x2="{_f(100 * math.cos(a / 57.3))}" y2="{_f(100 * math.sin(a / 57.3))}" stroke="{INK}" stroke-width="5"/>' for a in range(0, 360, 30))
                        + f'<line x1="0" y1="0" x2="{_f(55 * math.cos(a_h / 57.3))}" y2="{_f(55 * math.sin(a_h / 57.3))}" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
                        f'<line x1="0" y1="0" x2="{_f(80 * math.cos(a_m / 57.3))}" y2="{_f(80 * math.sin(a_m / 57.3))}" stroke="{BLUE}" stroke-width="6" stroke-linecap="round"/><circle r="8" fill="{INK}"/>'))


def umbrella(x, y, s=1.0, **_):
    """An open umbrella."""
    return _g(x, y, s, f'<path d="M-140 0 q140 -150 280 0 z" fill="{BLUE}" stroke="{INK}" stroke-width="{SW}"/><line x1="0" y1="-20" x2="0" y2="220" stroke="{INK}" stroke-width="7"/><path d="M0 220 q0 30 -26 24" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')


def books(x, y, s=1.0, n=4, **_):
    """A stack of n books."""
    cols = [BLUE, GOLD, GREEN, CORAL, LB]
    return _g(x, y, s, "".join(f'<rect x="{-110 + (k % 2) * 12}" y="{-k * 40 - 40}" width="220" height="40" rx="6" fill="{cols[k % 5]}" stroke="{INK}" stroke-width="5"/>' for k in range(int(n))))


def price_tag(x, y, s=1.0, rot=-12, **_):
    """A price tag (no text). rot (degrees)."""
    return _g(x, y, s, (f'<path d="M-120 -50 H60 L120 0 L60 50 H-120 Z" fill="{GOLD}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
                        f'<circle cx="60" cy="0" r="12" fill="{PAPER}" stroke="{INK}" stroke-width="4"/><line x1="-90" y1="0" x2="10" y2="0" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'), rot)


def funnel(x, y, s=1.0, top=10, bottom=2, **_):
    """Sales funnel: `top` dots enter, `bottom` dots come out (conversion), no text."""
    inner = f'<path d="M-260 -220 H260 L60 40 V200 H-60 V40 Z" fill="{LB}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
    for k in range(int(top)):
        inner += f'<circle cx="{-220 + 440 * k / max(1, top - 1)}" cy="-260" r="16" fill="{BLUE}" stroke="{INK}" stroke-width="3"/>'
    for k in range(int(bottom)):
        inner += f'<circle cx="{-30 + 60 * k / max(1, bottom - 1) if bottom > 1 else 0}" cy="250" r="20" fill="{GREEN}" stroke="{INK}" stroke-width="4"/>'
    return _g(x, y, s, inner)


def funnel_box(x, y, s=1.0, **_):
    return [x - 280 * s, y - 290 * s, 560 * s, 570 * s]


def envelope(x, y, s=1.0, **_):
    """A closed letter or email."""
    return _g(x, y, s, f'<rect x="-130" y="-85" width="260" height="170" rx="10" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/><path d="M-130 -85 L0 20 L130 -85" fill="none" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>')


def arrow(x, y, s=1.0, dx=200, dy=0, color="blue", dashed=False, **_):
    """Straight arrow from (x, y) by (dx, dy). color: blue, green, coral, ink."""
    c = {"blue": BLUE, "green": GREEN, "coral": CORAL, "ink": INK}.get(color, BLUE)
    L = math.hypot(dx, dy) or 1; ux, uy = dx / L, dy / L; hx, hy = x + dx, y + dy
    d = ' stroke-dasharray="22 16"' if dashed else ""
    return (f'<line x1="{_f(x)}" y1="{_f(y)}" x2="{_f(hx)}" y2="{_f(hy)}" stroke="{c}" stroke-width="{14 * s}" stroke-linecap="round"{d}/>'
            f'<path d="M{_f(hx - 40 * s * ux + 30 * s * uy)} {_f(hy - 40 * s * uy - 30 * s * ux)} L{_f(hx)} {_f(hy)} L{_f(hx - 40 * s * ux - 30 * s * uy)} {_f(hy - 40 * s * uy + 30 * s * ux)}" fill="none" stroke="{c}" stroke-width="{14 * s}" stroke-linecap="round" stroke-linejoin="round"/>')


def arrow_box(x, y, s=1.0, dx=200, dy=0, **_):
    return [min(x, x + dx) - 40, min(y, y + dy) - 40, abs(dx) + 80, abs(dy) + 80]


def cross(x, y, s=1.0, w=200, h=200, **_):
    """A red X over something that no longer counts."""
    return (f'<line x1="{_f(x - w / 2)}" y1="{_f(y - h / 2)}" x2="{_f(x + w / 2)}" y2="{_f(y + h / 2)}" stroke="{CORAL}" stroke-width="{10 * s}" stroke-linecap="round"/>'
            f'<line x1="{_f(x - w / 2)}" y1="{_f(y + h / 2)}" x2="{_f(x + w / 2)}" y2="{_f(y - h / 2)}" stroke="{CORAL}" stroke-width="{10 * s}" stroke-linecap="round"/>')


def cross_box(x, y, s=1.0, w=200, h=200, **_):
    return [x - w / 2, y - h / 2, w, h]


def check(x, y, s=1.0, **_):
    """A green tick: the right choice."""
    return _g(x, y, s, f'<path d="M-60 0 L-15 45 L70 -50" fill="none" stroke="{GREEN}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>')


# ---------------------------------------------------------------- food and everyday props (added 25 Oct 2026)
CRUST = "#D9A04A"; CHEESE = "#F6D27A"; BREAD = "#E8C27E"; LETT = "#7FBF6A"; LEMON = "#F2D64B"


def _wedge(r, a0, a1):
    p0 = (r * math.cos(math.radians(a0)), r * math.sin(math.radians(a0)))
    p1 = (r * math.cos(math.radians(a1)), r * math.sin(math.radians(a1)))
    return f"M0 0 L{_f(p0[0])} {_f(p0[1])} A{r} {r} 0 0 1 {_f(p1[0])} {_f(p1[1])} Z"


def pizza(x, y, s=1.0, slices=8, **_):
    """A whole round pizza seen from above, 8 slices; slices = how many are left (0-8; eaten ones show as a dashed outline)."""
    r = 150; n = max(0, min(8, int(slices)))
    out = f'<circle r="{r + 6}" fill="none" stroke="{GREY}" stroke-width="4" stroke-dasharray="14 12"/>'
    for i in range(n):
        a0 = -90 + 45 * i; a1 = a0 + 45; am = math.radians(a0 + 22.5); rc = r - 9
        out += (f'<path d="{_wedge(r, a0, a1)}" fill="{CHEESE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                f'<path d="M{_f(rc * math.cos(math.radians(a0 + 3)))} {_f(rc * math.sin(math.radians(a0 + 3)))} A{rc} {rc} 0 0 1 '
                f'{_f(rc * math.cos(math.radians(a1 - 3)))} {_f(rc * math.sin(math.radians(a1 - 3)))}" fill="none" stroke="{CRUST}" stroke-width="14" stroke-linecap="round"/>'
                f'<circle cx="{_f(88 * math.cos(am))}" cy="{_f(88 * math.sin(am))}" r="15" fill="{CORAL}" stroke="{INK}" stroke-width="3"/>')
    return _g(x, y, s, out)


def pizza_slice(x, y, s=1.0, bite=False, rot=0, **_):
    """One pizza slice, tip down; bite = true takes a bite out of the tip; rot = degrees."""
    tip = "L0 150" if not bite else "L22 118 Q8 108 0 126 Q-8 108 -22 118"
    inner = (f'<path d="M-95 -120 Q0 -150 95 -120 {tip} Z" fill="{CHEESE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             f'<path d="M-92 -122 Q0 -152 92 -122" fill="none" stroke="{CRUST}" stroke-width="22" stroke-linecap="round"/>'
             f'<path d="M-95 -132 Q0 -164 95 -132" fill="none" stroke="{INK}" stroke-width="4"/>'
             f'<circle cx="-30" cy="-60" r="16" fill="{CORAL}" stroke="{INK}" stroke-width="3"/><circle cx="26" cy="-30" r="14" fill="{CORAL}" stroke="{INK}" stroke-width="3"/>'
             f'<circle cx="-4" cy="40" r="11" fill="{CORAL}" stroke="{INK}" stroke-width="3"/>')
    return _g(x, y, s, inner, rot)


def sandwich(x, y, s=1.0, **_):
    """A stacked sandwich, side view."""
    inner = (f'<rect x="-130" y="30" width="260" height="46" rx="18" fill="{BREAD}" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M-140 30 q20 -22 40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0" fill="{LETT}" stroke="{INK}" stroke-width="4"/>'
             f'<rect x="-120" y="2" width="240" height="20" rx="8" fill="{CORAL}" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M-126 2 L126 2 L100 -16 L-100 -16 Z" fill="{CHEESE}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
             f'<path d="M-134 -16 Q-134 -70 0 -76 Q134 -70 134 -16 Z" fill="{BREAD}" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M-60 -50 l8 -4 M10 -58 l8 -3 M70 -46 l8 -4" stroke="{INK}" stroke-width="4" stroke-linecap="round" opacity="0.5"/>')
    return _g(x, y, s, inner)


def lemonade_cup(x, y, s=1.0, **_):
    """A cup of lemonade with a straw and a lemon slice."""
    spokes = "".join(f'<path d="M-56 -110 l{_f(24 * math.cos(math.radians(a)))} {_f(24 * math.sin(math.radians(a)))}" stroke="{INK}" stroke-width="2.5" opacity="0.6"/>' for a in range(0, 360, 60))
    inner = (f'<path d="M14 -110 L40 -190 L66 -190" fill="none" stroke="{CORAL}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<path d="M-62 -110 L62 -110 L46 110 L-46 110 Z" fill="{WHITE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             f'<path d="M-56 -70 L56 -70 L45 104 L-45 104 Z" fill="{LEMON}" opacity="0.85"/>'
             f'<circle cx="-56" cy="-110" r="34" fill="{LEMON}" stroke="{INK}" stroke-width="4"/>{spokes}')
    return _g(x, y, s, inner)


def lemonade_stand(x, y, s=1.0, **_):
    """A small street stall with a striped awning, a counter and a pitcher (no sign text). (x, y) = centre bottom of the counter."""
    stripes = "".join(f'<path d="M{-230 + 46 * i} -420 L{-184 + 46 * i} -420 L{-184 + 46 * i} -360 Q{-207 + 46 * i} -340 {-230 + 46 * i} -360 Z" '
                      f'fill="{BLUE if i % 2 == 0 else WHITE}" stroke="{INK}" stroke-width="4"/>' for i in range(10))
    inner = (f'<rect x="-214" y="-420" width="14" height="420" fill="{NAVY}"/><rect x="200" y="-420" width="14" height="420" fill="{NAVY}"/>'
             f'{stripes}<rect x="-240" y="-200" width="480" height="200" rx="10" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>'
             f'<rect x="-250" y="-214" width="500" height="22" rx="8" fill="{NAVY}"/>'
             f'<rect x="-150" y="-150" width="300" height="90" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M120 -214 L120 -300 Q150 -310 180 -300 L176 -214 Z" fill="{LEMON}" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M180 -290 q26 6 18 34 q-6 18 -22 20" fill="none" stroke="{INK}" stroke-width="4"/>')
    return _g(x, y, s, inner)


def lemonade_stand_box(x, y, s=1.0, **_):
    return [x - 255 * s, y - 425 * s, 510 * s, 430 * s]


def plate(x, y, s=1.0, item="none", **_):
    """A round plate, side view; item = none, slice (a pizza slice on it) or crumbs."""
    top = ""
    if item == "slice":
        top = (f'<path d="M-80 -26 Q0 -44 80 -26 L0 0 Z" fill="{CHEESE}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
               f'<path d="M-78 -28 Q0 -46 78 -28" fill="none" stroke="{CRUST}" stroke-width="12" stroke-linecap="round"/>')
    elif item == "crumbs":
        top = "".join(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{CRUST}"/>' for cx, cy in ((-40, -6), (-10, -10), (24, -5), (50, -9), (6, -3)))
    inner = (f'<ellipse cx="0" cy="0" rx="150" ry="34" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>'
             f'<ellipse cx="0" cy="-4" rx="100" ry="18" fill="none" stroke="{GREY}" stroke-width="3"/>{top}')
    return _g(x, y, s, inner)


def burger(x, y, s=1.0, **_):
    """A burger, side view."""
    inner = (f'<path d="M-130 40 L130 40 Q130 84 96 84 L-96 84 Q-130 84 -130 40 Z" fill="{BREAD}" stroke="{INK}" stroke-width="5"/>'
             f'<rect x="-140" y="8" width="280" height="34" rx="16" fill="#7A4A2A" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M-140 8 L140 8 L110 30 L80 10 L40 32 L0 10 L-40 32 L-80 10 L-110 30 Z" fill="{CHEESE}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
             f'<path d="M-146 4 q24 -20 48 0 t48 0 t48 0 t48 0 t48 0 t48 0" fill="{LETT}" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M-136 0 Q-136 -96 0 -100 Q136 -96 136 0 Z" fill="{BREAD}" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M-50 -60 l8 -4 M10 -72 l8 -3 M60 -56 l8 -4" stroke="{INK}" stroke-width="4" stroke-linecap="round" opacity="0.5"/>')
    return _g(x, y, s, inner)


def groceries_bag(x, y, s=1.0, **_):
    """A paper grocery bag with a baguette and greens poking out."""
    folds = " ".join(f"L{-120 + 20 * i} {-150 if i % 2 == 0 else -120}" for i in range(13))
    inner = (f'<path d="M30 -150 L70 -250 Q82 -262 92 -248 L60 -150 Z" fill="{BREAD}" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M-60 -150 Q-80 -230 -40 -240 Q-30 -190 -20 -150 Z" fill="{LETT}" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M-20 -150 Q-10 -220 20 -226 Q20 -180 10 -150 Z" fill="{LETT}" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M-120 -150 L120 -150 L104 160 L-104 160 Z" fill="#C9A06A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             f'<path d="M{folds[1:]}" fill="none" stroke="{INK}" stroke-width="3" opacity="0.5"/>')
    return _g(x, y, s, inner)


def receipt(x, y, s=1.0, rot=-4, **_):
    """A long till receipt with blank lines and a bold total line (no text)."""
    zig = "".join(f" L{80 - 20 * (i + 1)} {170 if i % 2 == 0 else 186}" for i in range(8))
    lines = "".join(f'<rect x="-56" y="{-140 + 30 * i}" width="{60 + (i * 37) % 50}" height="8" rx="4" fill="#D9D5CA"/>'
                    f'<rect x="34" y="{-140 + 30 * i}" width="24" height="8" rx="4" fill="#D9D5CA"/>' for i in range(8))
    inner = (f'<path d="M-80 -180 L80 -180 L80 186{zig} L-80 186 Z" fill="{WHITE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             f'{lines}<rect x="-56" y="112" width="112" height="14" rx="5" fill="{INK}"/>')
    return _g(x, y, s, inner, rot)


def gym(x, y, s=1.0, **_):
    """Gym kit: a weight bench with a barbell on its rack and a dumbbell on the floor. (x, y) = centre of the floor line."""
    inner = (f'<rect x="-200" y="-90" width="320" height="34" rx="12" fill="{NAVY}" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M-170 -56 L-170 0 M90 -56 L90 0" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
             f'<path d="M150 -230 L150 0 M190 -230 L190 0" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
             f'<path d="M-40 -226 L340 -226" stroke="{GREY}" stroke-width="10" stroke-linecap="round"/>'
             f'<rect x="-30" y="-276" width="34" height="100" rx="8" fill="{BLUE}" stroke="{INK}" stroke-width="4"/>'
             f'<rect x="290" y="-276" width="34" height="100" rx="8" fill="{BLUE}" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M-290 -22 L-210 -22" stroke="{GREY}" stroke-width="10" stroke-linecap="round"/>'
             f'<rect x="-306" y="-48" width="26" height="52" rx="6" fill="{CORAL}" stroke="{INK}" stroke-width="4"/>'
             f'<rect x="-220" y="-48" width="26" height="52" rx="6" fill="{CORAL}" stroke="{INK}" stroke-width="4"/>')
    return _g(x, y, s, inner)


def gym_box(x, y, s=1.0, **_):
    return [x - 310 * s, y - 280 * s, 650 * s, 290 * s]


def bus(x, y, s=1.0, flip=False, **_):
    """A city bus, side view; (x, y) = centre of the road under its wheels; flip = true faces left."""
    win = "".join(f'<rect x="{-250 + 92 * i}" y="-240" width="72" height="70" rx="8" fill="{SKY}" stroke="{INK}" stroke-width="4"/>' for i in range(5))
    inner = (f'<rect x="-290" y="-270" width="580" height="230" rx="30" fill="{BLUE}" stroke="{INK}" stroke-width="6"/>'
             f'{win}<rect x="216" y="-240" width="54" height="170" rx="8" fill="{SKY}" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M243 -240 V-70" stroke="{INK}" stroke-width="3"/><rect x="-290" y="-110" width="580" height="18" fill="{WHITE}" opacity="0.8"/>'
             f'<circle cx="-170" cy="-40" r="40" fill="{INK}"/><circle cx="-170" cy="-40" r="15" fill="{GREY}"/>'
             f'<circle cx="170" cy="-40" r="40" fill="{INK}"/><circle cx="170" cy="-40" r="15" fill="{GREY}"/>')
    if flip: inner = f'<g transform="scale(-1 1)">{inner}</g>'
    return _g(x, y, s, inner)


def bus_box(x, y, s=1.0, **_):
    return [x - 295 * s, y - 275 * s, 590 * s, 275 * s]


# ---------------------------------------------------------------- backgrounds
def ground(y=1480):
    return f'<path d="M60 {y} Q540 {y - 14} 1020 {y}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'


def wall(color=SKY, op=0.55):
    # must stay the FIRST element: make_scenes_json.py turns it into a full-bleed wall
    return f'<rect x="0" y="0" width="1080" height="1480" fill="{color}" opacity="{op}"/>'


def bg_svg(name):
    if name == "office":
        blinds = "".join(f'<line x1="770" y1="{y}" x2="970" y2="{y}" stroke="{INK}" stroke-width="3" opacity="0.35"/>' for y in range(560, 800, 40))
        return (wall() + ground() + f'<rect x="760" y="520" width="220" height="300" rx="8" fill="{WHITE}" stroke="{INK}" stroke-width="6"/>' + blinds +
                f'<line x1="870" y1="520" x2="870" y2="820" stroke="{INK}" stroke-width="5"/>')
    if name == "classroom":
        return (wall("#EAF4EE", 0.7) + ground() + f'<rect x="140" y="420" width="800" height="380" rx="10" fill="#2F4A3F" stroke="{INK}" stroke-width="8"/>'
                f'<path d="M200 520 H520 M200 580 H700 M200 640 H460" stroke="{WHITE}" stroke-width="8" stroke-linecap="round" opacity="0.7"/>')
    if name == "lecture":
        rows = "".join(f'<path d="M40 {1180 + k * 100} H1040" stroke="{INK}" stroke-width="6" opacity="0.5"/>'
                       + "".join(f'<circle cx="{120 + j * 140 + (k % 2) * 70}" cy="{1150 + k * 100}" r="26" fill="{GREY}" opacity="0.45"/>' for j in range(7)) for k in range(3))
        return (wall("#F1ECE2", 0.8) + f'<rect x="200" y="400" width="680" height="380" rx="10" fill="{WHITE}" stroke="{INK}" stroke-width="7"/>'
                f'<path d="M260 700 L420 560 L540 620 L800 460" fill="none" stroke="{BLUE}" stroke-width="9" stroke-linecap="round"/>' + rows)
    if name == "home":
        return (wall("#F6EEE3", 0.8) + ground() + f'<rect x="90" y="560" width="260" height="320" rx="8" fill="{SKY}" stroke="{INK}" stroke-width="6"/>'
                f'<line x1="220" y1="560" x2="220" y2="880" stroke="{INK}" stroke-width="5"/><line x1="90" y1="720" x2="350" y2="720" stroke="{INK}" stroke-width="5"/>')
    if name == "street":
        return wall("#EAF1FB", 0.6) + ground() + f'<path d="M0 1480 H1080" stroke="{GREY}" stroke-width="3"/>'
    if name == "campus":
        # outdoor campus for ledger-talks: sky, a college hall behind Ledger, a tree left, a flagpole right, grass.
        # Placed for the talk frame (Ledger centred at x 540, feet at y 1470, s 2.4): visible art is about x 190-890, y 760-1490
        win = "".join(f'<rect x="{x}" y="{y}" width="34" height="48" rx="4" fill="{SKY}" stroke="{INK}" stroke-width="3"/>' for y in (900, 990) for x in (250, 310, 370, 690, 750, 810))
        return (wall("#DCEAFB", 0.9) +
                f'<path d="M0 1080 Q540 1050 1080 1080 L1080 1480 L0 1480 Z" fill="#DDEFD9"/>'
                f'<path d="M210 1100 V880 L540 790 L870 880 V1100 Z" fill="#F4ECDD" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                f'<path d="M190 885 L540 780 L890 885" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>' + win +
                f'<circle cx="150" cy="900" r="70" fill="#9CCB8F" stroke="{INK}" stroke-width="4"/><circle cx="205" cy="960" r="55" fill="#8BBE7E" stroke="{INK}" stroke-width="4"/>'
                f'<path d="M170 1010 V1110" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
                f'<path d="M930 1110 V800" stroke="{INK}" stroke-width="5"/><path d="M930 805 L985 820 L930 838 Z" fill="{BLUE}" stroke="{INK}" stroke-width="3"/>'
                f'<path d="M0 1090 Q540 1060 1080 1090" fill="none" stroke="{INK}" stroke-width="4" opacity="0.6"/>'
                f'<rect x="-200" y="1478" width="1480" height="700" fill="#DDEFD9"/><rect x="-200" y="-400" width="1480" height="400" fill="#DCEAFB" opacity="0.9"/>' + ground())
    if name == "none":
        return ""
    return ground()  # paper


BACKGROUNDS = ["paper", "office", "classroom", "lecture", "home", "street", "campus", "none"]

# name -> (draw function, box function or None = default box from size)
PRESETS = {
    "ledger": (ledger, ledger_box), "person": (person, person_box), "people_group": (people_group, people_group_box),
    "phone": (phone, None), "laptop": (laptop, None), "bills": (bills, None), "coins": (coins, None),
    "calendar": (calendar, None), "invoice": (invoice, None), "chart": (chart, None), "coffee": (coffee, None),
    "window": (window, None), "door": (door, None), "sofa": (sofa, None), "bed": (bed, None), "scale": (scale, scale_box),
    "pit": (pit, pit_box), "sun_arrow": (sun_arrow, None), "handshake": (handshake, None), "whiteboard": (whiteboard, None),
    "desk": (desk, desk_box), "school_desk": (school_desk, None), "ticket": (ticket, None), "thought": (thought, thought_box),
    "speech": (speech, None), "building": (building, building_box), "clock": (clock, None), "umbrella": (umbrella, None),
    "books": (books, None), "price_tag": (price_tag, None), "funnel": (funnel, funnel_box), "envelope": (envelope, None),
    "arrow": (arrow, arrow_box), "cross": (cross, cross_box), "check": (check, None),
    "pizza": (pizza, None), "pizza_slice": (pizza_slice, None), "sandwich": (sandwich, None), "lemonade_cup": (lemonade_cup, None),
    "lemonade_stand": (lemonade_stand, lemonade_stand_box), "plate": (plate, None), "burger": (burger, None),
    "groceries_bag": (groceries_bag, None), "receipt": (receipt, None), "gym": (gym, gym_box), "bus": (bus, bus_box),
}
# half-sizes at s=1 for props that use the default box (centre +- these)
HALF = {"phone": (155, 285), "laptop": (235, 155), "bills": (95, 110), "coins": (50, 95), "calendar": (155, 185),
        "invoice": (115, 155), "chart": (205, 155), "coffee": (95, 160), "window": (345, 265), "door": (130, 365),
        "sofa": (165, 105), "bed": (225, 90), "sun_arrow": (270, 220), "handshake": (305, 75), "whiteboard": (355, 225),
        "school_desk": (175, 185), "ticket": (115, 60), "speech": (205, 145), "clock": (115, 115), "umbrella": (145, 245),
        "books": (125, 110), "price_tag": (125, 55), "envelope": (135, 90), "check": (75, 55),
        "pizza": (160, 160), "pizza_slice": (100, 165), "sandwich": (145, 90), "lemonade_cup": (100, 200), "plate": (155, 50),
        "burger": (150, 105), "groceries_bag": (125, 250), "receipt": (95, 195)}
PRESET_HELP = {k: (v[0].__doc__ or "").strip() for k, v in PRESETS.items()}


def item_svg(it):
    p = it["p"]; fn = PRESETS[p][0]
    kw = {k: v for k, v in it.items() if k not in ("p", "id", "x", "y", "s")}
    return fn(it["x"], it["y"], it.get("s", 1.0), **kw)


def item_box(it):
    p = it["p"]; bx = PRESETS[p][1]; s = it.get("s", 1.0)
    if bx:
        kw = {k: v for k, v in it.items() if k not in ("p", "id", "x", "y", "s")}
        return bx(it["x"], it["y"], s, **kw)
    hw, hh = HALF.get(p, (150, 150))
    return [it["x"] - hw * s, it["y"] - hh * s, 2 * hw * s, 2 * hh * s]


def scene_body(spec):
    # items sit in <g class="content"> so the renderer can auto-fit the frame to the drawn subject (not the background)
    return bg_svg(spec.get("bg", "paper")) + '<g class="content">' + "".join(f'<g data-p="{it["p"]}">{item_svg(it)}</g>' for it in spec.get("items", [])) + '</g>'


def scene_svg(spec):
    """Full 1080x1920 SVG in the layout make_scenes_json.py expects (art inside <g filter="url(#r)">)."""
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">'
            '<defs><filter id="r" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="4"/>'
            '<feDisplacementMap in="SourceGraphic" scale="5"/></filter></defs>'
            f'<rect width="1080" height="1920" fill="{PAPER}"/><g filter="url(#r)">{scene_body(spec)}</g></svg>')


if __name__ == "__main__" and "--list" in sys.argv:
    print("Backgrounds (scene 'bg'):", ", ".join(BACKGROUNDS))
    print("Ledger: mood", MOODS, "| arm", ARMS, "| larm", LARMS, "| outfit", OUTFITS, "| tilt (deg), flip (true faces left)")
    for k, v in PRESET_HELP.items():
        print(f"- {k}: {v.splitlines()[0] if v else ''}")
