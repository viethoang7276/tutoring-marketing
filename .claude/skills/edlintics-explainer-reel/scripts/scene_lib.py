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
MOODS = ["smile", "happy", "frown", "sad", "flat", "o", "worried", "tired", "angry", "talk", "dizzy"]
ARMS = ["down", "hold", "up", "both_up", "point", "phone", "shrug", "wave", "mic"]
LARMS = ["down", "up_l", "point_l", "open_l", "shrug_l"]   # left-arm gestures (larm), used with arm "mic" in ledger-talks reels
OUTFITS = ["suit", "student", "casual", "sales", "vest", "dracula", "professor", "lecturer", "graduate", "mathprof"]
PROF = ("professor", "lecturer", "graduate", "mathprof")   # puzzle-guide family (2 Nov 2026 design options)


def _arm(path, hand):
    hx, hy = hand
    return (f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="13" stroke-linecap="round"/>'
            f'<path d="{path}" fill="none" stroke="{PAPER}" stroke-width="8" stroke-linecap="round"/>'
            f'<circle cx="{hx}" cy="{hy}" r="9" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')


GAZES = {None: (0, 0, 0), "right": (6, 2, 0), "left": (-6, 2, 0), "down": (0, 7, 4), "up": (0, -5, 0)}   # eye dx, eye dy, mouth dy


def ledger(x, y, s=1.0, mood="smile", arm="down", outfit="suit", tilt=0, flip=False, larm=None, gaze=None, lanyard=False, glasses=False, pointer=False, **_):
    """The Edlintics mascot (from assets/brand/ledger.svg). (x, y) = between his feet. mood, arm, outfit, tilt, flip, larm (left-arm gesture), gaze (right, left, down, up: eyes look that way; down also lowers the mouth, head-down sad), lanyard (true: a staff lanyard with an ID badge, the job prop for a store manager or HR). mood "talk" lip-syncs to the voice; arm "mic" holds a small handheld mic."""
    mouth = {
        "smile": "M106 134 Q120 146 134 134", "happy": "M104 130 Q120 150 136 130",
        "frown": "M107 140 Q120 130 133 140", "sad": "M107 140 Q120 131 133 140",
        "flat": "M108 137 L132 137", "worried": "M108 139 Q114 134 120 138 Q126 142 132 137",
        "tired": "M110 138 L130 138", "angry": "M108 139 L132 139",
        "dizzy": "M106 139 Q111 133 116 139 Q121 145 126 139 Q131 133 134 138",
    }
    if mood == "talk":  # two mouths: the renderer shows "mo" (open) while the voice is loud and "mc" (closed) in pauses
        m = (f'<g class="mc"><path d="M108 136 Q120 145 132 136" fill="none" stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/></g>'
             f'<g class="mo" style="display:none"><path d="M108 133 Q120 131 132 133 Q131 148 120 149 Q109 148 108 133 Z" fill="{INK}"/>'
             f'<path d="M113 144 Q120 140 127 144 Q124 148 120 148 Q116 148 113 144 Z" fill="{CORAL}"/></g>')
    else:
        m = (f'<ellipse cx="120" cy="137" rx="6" ry="7" fill="{INK}"/>' if mood == "o" else
             f'<path d="{mouth.get(mood, mouth["smile"])}" fill="none" stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/>')
    if mood == "dizzy":  # spiral eyes (29 Oct 2026, paid ad): same eye size and places as the brand eyes
        def _sp(cx, cy):
            pts = " ".join(f"{cx + 1.05 * t * math.cos(t):.1f} {cy + 1.05 * t * math.sin(t):.1f}" for t in [k * 0.45 for k in range(0, 23)])
            return f'<path d="M{pts}" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/>'
        eyes = _sp(102, 110) + _sp(138, 110)
    elif mood == "happy":  # closed happy eyes
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
    if mood == "dizzy":  # a ring of three small stars circling over his head
        st = lambda cx, cy, r: "M" + " L".join(f"{cx + (r if k % 2 == 0 else r * 0.45) * math.cos(-math.pi / 2 + k * math.pi / 5):.1f} {cy + (r if k % 2 == 0 else r * 0.45) * math.sin(-math.pi / 2 + k * math.pi / 5):.1f}" for k in range(10)) + " Z"
        extra = (f'<ellipse cx="120" cy="22" rx="62" ry="13" fill="none" stroke="{INK}" stroke-width="2.5" stroke-dasharray="7 7" opacity="0.7"/>'
                 + "".join(f'<path d="{st(cx, cy, 11)}" fill="{GOLD}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>' for cx, cy in ((64, 24), (120, 9), (176, 24))))
    gx, gy, my = GAZES.get(gaze, (0, 0, 0))   # gaze (30 Oct 2026, tutoring ad v5): shift eyes and brows (and the mouth for "down")
    if gx or gy: eyes = f'<g transform="translate({gx} {gy})">{eyes}</g>'; brows = f'<g transform="translate({gx} {gy})">{brows}</g>' if brows else ""
    if my: m = f'<g transform="translate(0 {my})">{m}</g>'
    # body band, collar and tie by outfit
    band_col = {"suit": NAVY, "sales": NAVY, "vest": NAVY, "dracula": NAVY, "student": BLUE, "casual": "#5B6B86", "lecturer": "#8B6B4A", "graduate": "#1A1A22"}.get(outfit, NAVY)
    band = f'<path d="M54.5 150 L185.5 150 L185.5 174 Q185.5 189.5 170 189.5 L70 189.5 Q54.5 189.5 54.5 174 Z" fill="{band_col}"/>'
    if outfit in ("suit", "sales", "vest", "dracula"):
        collar = (f'<path d="M108 150 L120 168 L116 173 L102 154 Z" fill="{WHITE}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
                  f'<path d="M132 150 L120 168 L124 173 L138 154 Z" fill="{WHITE}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
                  f'<path d="M114 152 L126 152 L129 161 L111 161 Z" fill="{BLUE}"/><path d="M112 162 L128 162 L124 184 L120 189 L116 184 Z" fill="{BLUE}"/>')
    elif outfit == "casual":
        collar = (f'<path d="M106 150 L120 164 L134 150" fill="none" stroke="{WHITE}" stroke-width="5" stroke-linejoin="round"/>')
    elif outfit in ("professor", "lecturer", "mathprof", "graduate"):  # puzzle-reel guide (2 Nov 2026): white wing collar and a blue bow tie on the navy band
        collar = (f'<path d="M106 150 L120 160 L112 164 L100 154 Z" fill="{WHITE}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
                  f'<path d="M134 150 L120 160 L128 164 L140 154 Z" fill="{WHITE}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
                  f'<path d="M120 166 L103 157 L103 175 Z M120 166 L137 157 L137 175 Z" fill="{BLUE}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
                  f'<rect x="115" y="161" width="10" height="10" rx="2.5" fill="{BLUE}" stroke="{INK}" stroke-width="2"/>')
    else:  # student hoodie: drawstrings
        collar = (f'<path d="M110 150 v22 M130 150 v22" stroke="{WHITE}" stroke-width="4" stroke-linecap="round"/>'
                  f'<circle cx="110" cy="174" r="3.5" fill="{WHITE}"/><circle cx="130" cy="174" r="3.5" fill="{WHITE}"/>')
    if outfit == "graduate":  # gown band with a blue hood stripe in a V under the collar
        collar = (f'<path d="M58 152 L104 176 M182 152 L136 176" stroke="{BLUE}" stroke-width="7" stroke-linecap="round"/>' + collar)
    if outfit == "lecturer":  # tweed hint (a few short flecks) and brown elbow patches at the band's sides
        collar = ("".join(f'<path d="M{x0} {y0} l5 3" stroke="#6B4F33" stroke-width="2" stroke-linecap="round"/>' for x0, y0 in ((64, 158), (78, 176), (90, 162), (150, 160), (164, 178), (172, 162)))
                  + f'<ellipse cx="62" cy="172" rx="7" ry="11" fill="#5C4129" stroke="{INK}" stroke-width="2"/><ellipse cx="178" cy="172" rx="7" ry="11" fill="#5C4129" stroke="{INK}" stroke-width="2"/>' + collar)
    if lanyard:   # staff lanyard (1 Nov 2026, how-to reels): gold strap under the tie, a blank ID badge on his right side, clear of the tie
        collar = (f'<path d="M94 150 L158 170 M178 150 L160 170" fill="none" stroke="{GOLD}" stroke-width="4.5" stroke-linecap="round"/>' + collar +
                  f'<rect x="146" y="167" width="28" height="24" rx="3" fill="{WHITE}" stroke="{INK}" stroke-width="2.5"/>'
                  f'<rect x="146" y="167" width="28" height="7" rx="2" fill="{BLUE}"/><path d="M151 180 h18 M151 186 h12" stroke="{GREY}" stroke-width="2.2" stroke-linecap="round"/>')
    behind = ""
    if outfit == "student":  # backpack peeking out on both sides
        behind = (f'<rect x="38" y="96" width="30" height="80" rx="10" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>'
                  f'<rect x="172" y="96" width="30" height="80" rx="10" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>')
    head = ""
    if outfit == "dracula":  # Halloween costume (31 Oct 2026): black cape with red lining and a tall stand-up collar behind the body, small fangs
        behind = (f'<path d="M58 70 Q20 140 14 228 Q60 214 120 226 Q180 214 226 228 Q220 140 182 70 Z" fill="#B3262E" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                  f'<path d="M62 74 Q30 140 26 220 Q66 208 120 218 Q174 208 214 220 Q210 140 178 74 Z" fill="#1A1A22"/>'
                  f'<path d="M66 120 L18 30 L44 52 L56 18 L82 96 Z" fill="#1A1A22" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                  f'<path d="M64 110 L30 46 L48 62 L58 36 L76 96 Z" fill="#B3262E"/>'
                  f'<path d="M174 120 L222 30 L196 52 L184 18 L158 96 Z" fill="#1A1A22" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                  f'<path d="M176 110 L210 46 L192 62 L182 36 L164 96 Z" fill="#B3262E"/>')
        extra += (f'<path d="M111 139 L114 149 L117 140 Z M123 140 L126 149 L129 139 Z" fill="{WHITE}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
    if outfit == "vest":  # finance-bro look (31 Oct 2026): grey fleece vest over the shirt and tie, white earbuds
        collar += (f'<path d="M57 124 L104 151 L110 189 L70 189 Q57 189 57 176 Z" fill="#4B5563" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
                   f'<path d="M183 124 L136 151 L130 189 L170 189 Q183 189 183 176 Z" fill="#4B5563" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
                   f'<path d="M66 146 L100 166 M174 146 L140 166" stroke="#6B7280" stroke-width="2.5"/>')
        head = (f'<rect x="38" y="98" width="13" height="24" rx="6.5" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>'
                f'<rect x="189" y="98" width="13" height="24" rx="6.5" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>')
    GL = (f'<circle cx="102" cy="110" r="14" fill="none" stroke="{INK}" stroke-width="3.5"/><circle cx="138" cy="110" r="14" fill="none" stroke="{INK}" stroke-width="3.5"/>'
          f'<path d="M116 108 Q120 104 124 108" fill="none" stroke="{INK}" stroke-width="3"/>')
    if outfit in ("lecturer", "mathprof") or (glasses and outfit not in PROF): head = GL
    if outfit == "mathprof":  # yellow pencil tucked behind the right side of the head
        head += (f'<g transform="rotate(-35 196 64)"><rect x="180" y="58" width="44" height="11" rx="2" fill="{GOLD}" stroke="{INK}" stroke-width="2.5"/>'
                 f'<path d="M224 58 L236 63.5 L224 69 Z" fill="#F5DEB3" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/><circle cx="234" cy="63.5" r="1.8" fill="{INK}"/>'
                 f'<rect x="174" y="58" width="7" height="11" rx="2" fill="#E8A0A0" stroke="{INK}" stroke-width="2"/></g>')
    if outfit in ("professor", "graduate"):  # mortarboard with a gold tassel, small round glasses
        head = (f'<path d="M84 40 L84 26 Q120 34 156 26 L156 40 Q120 48 84 40 Z" fill="#1A1A22" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
                f'<path d="M120 2 L190 22 L120 42 L50 22 Z" fill="#1A1A22" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                f'<circle cx="120" cy="22" r="4" fill="{GOLD}" stroke="{INK}" stroke-width="1.5"/>'
                f'<path d="M120 22 Q160 26 176 34 L176 62" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round"/>'
                f'<path d="M171 60 L181 60 L183 76 L169 76 Z" fill="{GOLD}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
                f'<circle cx="102" cy="110" r="14" fill="none" stroke="{INK}" stroke-width="3.5"/><circle cx="138" cy="110" r="14" fill="none" stroke="{INK}" stroke-width="3.5"/>'
                f'<path d="M116 108 Q120 104 124 108" fill="none" stroke="{INK}" stroke-width="3"/>')
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
    if arm == "point" and (outfit in ("professor", "graduate", "mathprof") or pointer):  # thin teaching pointer held in the pointing hand, tip up and to the right
        prop = (f'<path d="M222 146 L292 112" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
                f'<path d="M222 146 L292 112" stroke="#8A5A2B" stroke-width="3.5" stroke-linecap="round"/>'
                f'<circle cx="293" cy="111.5" r="4.5" fill="{INK}"/>')
    if arm == "point" and outfit == "lecturer":  # a long white chalk stick instead of the wooden pointer
        prop = (f'<path d="M222 146 L280 118" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
                f'<path d="M222 146 L280 118" stroke="{WHITE}" stroke-width="6" stroke-linecap="round"/>'
                f'<path d="M272 122 L280 118" stroke="#D9D6CC" stroke-width="6" stroke-linecap="round"/>')
    if outfit == "graduate" and (larm in (None, "down")):  # rolled diploma with a blue ribbon in the left hand
        prop += (f'<g transform="rotate(-25 52 190)"><rect x="18" y="182" width="62" height="16" rx="8" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>'
                 f'<ellipse cx="22" cy="190" rx="4" ry="8" fill="#E6E3DA" stroke="{INK}" stroke-width="2"/>'
                 f'<rect x="44" y="181" width="8" height="18" fill="{BLUE}" stroke="{INK}" stroke-width="2"/></g>')
    if outfit == "mathprof" and (larm in (None, "down")):  # small calculator in the left hand
        prop += (f'<g transform="rotate(-10 52 196)"><rect x="30" y="176" width="34" height="46" rx="5" fill="{NAVY}" stroke="{INK}" stroke-width="3"/>'
                 f'<rect x="35" y="181" width="24" height="10" rx="2" fill="{LB}"/>'
                 + "".join(f'<rect x="{35 + 8.5 * (k % 3):.1f}" y="{195 + 8 * (k // 3)}" width="6" height="5" rx="1.2" fill="{WHITE}"/>' for k in range(9)) + '</g>')
    if arm == "phone":
        prop = (f'<g transform="rotate(-14 200 92)"><rect x="185" y="60" width="30" height="58" rx="8" fill="{NAVY}" stroke="{INK}" stroke-width="3"/>'
                f'<rect x="190" y="68" width="20" height="38" rx="3" fill="{LB}"/></g>')
    body = (f'<rect x="52" y="38" width="136" height="154" rx="18" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'
            f'<line x1="70" y1="46" x2="70" y2="184" stroke="{INK}" stroke-width="3.5" opacity="0.45"/><line x1="74" y1="46" x2="74" y2="184" stroke="{INK}" stroke-width="1.5" opacity="0.25"/>'
            f'<path d="M150 34 h18 v26 l-9 -7 -9 7 z" fill="{BLUE}"/>'
            f'<rect x="86" y="58" width="60" height="6" rx="3" fill="#E6E3DA"/><rect x="86" y="70" width="60" height="6" rx="3" fill="#E6E3DA"/><rect x="86" y="82" width="40" height="6" rx="3" fill="#E6E3DA"/>'
            f'{band}{collar}{eyes}{brows}{m}{extra}{head}')
    legs = (f'<ellipse cx="120" cy="236" rx="46" ry="7" fill="{INK}" opacity="0.10"/>'
            f'<line x1="102" y1="186" x2="102" y2="210" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
            f'<line x1="138" y1="186" x2="138" y2="210" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
            f'<rect x="88" y="208" width="29" height="14" rx="7" fill="{INK}"/><rect x="123" y="208" width="29" height="14" rx="7" fill="{INK}"/>')
    fl = " scale(-1 1) translate(-240 0)" if flip else ""
    # tilt rotates the body WITH its arms and any held prop about the body's base (120,198), so the hands stay on the
    # shoulders (29 Oct 2026: a tilted body with untilted arms left a hand floating off the corner); the legs stay put
    return (f'<g transform="translate({_f(x)} {_f(y)}) scale({s}) translate(-120 -230){fl}">'
            f'{behind}{legs}<g transform="rotate({tilt} 120 198)">{left}{body}{prop}{right}</g></g>')


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


def person(x, y, s=1.0, mood="smile", color=None, carry=None, **_):
    """A simple customer/classmate figure (round head, rounded body). (x, y) = between the feet. carry="box": holds a cardboard box with a plant (an employee leaving)."""
    c = color or LB
    mouth = {"smile": "M-12 -168 Q0 -158 12 -168", "flat": "M-11 -164 H11", "sad": "M-12 -160 Q0 -170 12 -160"}.get(mood, "M-12 -168 Q0 -158 12 -168")
    inner = (f'<ellipse cx="0" cy="4" rx="44" ry="7" fill="{INK}" opacity="0.10"/>'
             f'<path d="M-46 0 V-90 Q-46 -130 0 -130 Q46 -130 46 -90 V0 Z" fill="{c}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<circle cx="0" cy="-178" r="40" fill="{PAPER}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<circle cx="-13" cy="-184" r="5" fill="{INK}"/><circle cx="13" cy="-184" r="5" fill="{INK}"/>'
             f'<path d="{mouth}" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    if carry == "box":   # leaving with a box (1 Nov 2026): plant leaves poking out, the box held in front of the body
        inner += (f'<path d="M-30 -110 q-14 -24 -46 -26 M-20 -110 q-30 -6 -50 8 M32 -110 q14 -24 46 -26 M22 -110 q30 -6 50 8" fill="none" stroke="{GREEN}" stroke-width="7" stroke-linecap="round"/>'
                  f'<path d="M-58 -112 H62 L56 -30 H-52 Z" fill="#D9B27C" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
                  f'<path d="M-58 -112 L-40 -96 H44 L62 -112" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                  f'<circle cx="-56" cy="-70" r="9" fill="{PAPER}" stroke="{INK}" stroke-width="3"/><circle cx="60" cy="-70" r="9" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')
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
    """A big smartphone. screen: empty (no users, flat line), up (rising chart), down (falling chart), call (call screen), chat, pay (a generic send-money screen)."""
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
    elif screen == "down":  # falling price chart (31 Oct 2026)
        inner += (f'<path d="M-95 -160 V170 H100" fill="none" stroke="{INK}" stroke-width="4"/>'
                  f'<path d="M-90 -140 L-50 -110 L-20 -40 L20 -20 L60 90 L95 130" fill="none" stroke="{CORAL}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
    elif screen == "pay":  # a generic send-money screen (how-to w46, no real app UI): a contact, an amount bar and a green send button
        inner += (f'<circle cx="0" cy="-140" r="50" fill="{LB}" stroke="{INK}" stroke-width="5"/><path d="M-36 -96 Q0 -130 36 -96" fill="none" stroke="{INK}" stroke-width="4"/>'
                  f'<rect x="-100" y="-50" width="200" height="70" rx="14" fill="{WHITE}" stroke="{INK}" stroke-width="5"/><path d="M-70 -15 H40" stroke="{GREY}" stroke-width="10" stroke-linecap="round"/>'
                  f'<rect x="-100" y="70" width="200" height="80" rx="40" fill="{GREEN}" stroke="{INK}" stroke-width="5"/><path d="M-20 110 H20 M6 94 L22 110 L6 126" fill="none" stroke="{WHITE}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>')
    else:  # chat
        inner += (f'<rect x="-100" y="-200" width="160" height="60" rx="18" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>'
                  f'<rect x="-40" y="-110" width="140" height="60" rx="18" fill="{LB}" stroke="{INK}" stroke-width="4"/>'
                  f'<rect x="-100" y="-20" width="180" height="60" rx="18" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>')
    return _g(x, y, s, inner)


def laptop(x, y, s=1.0, screen="chart", **_):
    """Open laptop seen from the front. screen: chart, sheet (spreadsheet grid), call (online lesson: a student tile and a shared whiteboard), lesson (an interactive lesson card with a progress bar), empty."""
    inner = (f'<rect x="-180" y="-150" width="360" height="230" rx="16" fill="{NAVY}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<rect x="-160" y="-132" width="320" height="192" rx="6" fill="{SKY}"/>'
             f'<path d="M-230 80 H230 L210 110 H-210 Z" fill="{GREY}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>')
    if screen == "chart":
        inner += f'<path d="M-130 30 L-60 -20 L0 0 L70 -70 L130 -100" fill="none" stroke="{GREEN}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
    elif screen == "filled":
        cs = [BLUE, GREEN, GOLD, CORAL, LB]
        for r in range(5):
            for c in range(4):
                inner += f'<rect x="{-156 + c * 80}" y="{-128 + r * 38}" width="72" height="30" rx="3" fill="{cs[(r * 3 + c * 2) % 5]}" opacity="0.8"/>'
    elif screen == "call":   # generic video-call layout, no real app UI: one student tile, one shared board
        inner += (f'<rect x="-150" y="-122" width="120" height="110" rx="8" fill="{LB}" stroke="{INK}" stroke-width="3"/>'
                  f'<circle cx="-90" cy="-78" r="20" fill="{PAPER}" stroke="{INK}" stroke-width="3"/><path d="M-122 -14 Q-122 -48 -90 -48 Q-58 -48 -58 -14 Z" fill="{BLUE}" stroke="{INK}" stroke-width="3"/>'
                  f'<rect x="-150" y="-2" width="120" height="54" rx="8" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>'
                  f'<path d="M-130 40 L-110 22 L-90 32 L-50 10" fill="none" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>'
                  f'<rect x="-20" y="-122" width="170" height="174" rx="8" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>'
                  f'<path d="M0 -100 V30 H135" fill="none" stroke="{INK}" stroke-width="3"/>'
                  f'<path d="M10 -85 L125 20" stroke="{BLUE}" stroke-width="5" stroke-linecap="round"/><path d="M10 20 L125 -85" stroke="{GREEN}" stroke-width="5" stroke-linecap="round"/>'
                  f'<circle cx="-110" cy="64" r="0" fill="none"/>')
    elif screen == "lesson":  # an interactive lesson card: a diagram, answer options (one ticked), a progress bar
        inner += (f'<rect x="-145" y="-120" width="290" height="70" rx="8" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>'
                  f'<path d="M-125 -66 L-80 -96 L-40 -78 L0 -108" fill="none" stroke="{BLUE}" stroke-width="5" stroke-linecap="round"/>'
                  f'<rect x="20" y="-104" width="110" height="10" rx="5" fill="{GREY}"/><rect x="20" y="-84" width="80" height="10" rx="5" fill="{GREY}"/>'
                  + "".join(f'<rect x="-145" y="{yy}" width="290" height="30" rx="8" fill="{"#CFE9D9" if k == 1 else WHITE}" stroke="{INK}" stroke-width="3"/>'
                            f'<rect x="-125" y="{yy + 11}" width="{120 - 25 * k}" height="8" rx="4" fill="{GREY}"/>' for k, yy in enumerate((-40, -4)))
                  + f'<path d="M110 {-4 + 15} l8 8 l16 -16" fill="none" stroke="{GREEN}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
                  f'<rect x="-145" y="40" width="290" height="12" rx="6" fill="{WHITE}" stroke="{INK}" stroke-width="2"/><rect x="-145" y="40" width="180" height="12" rx="6" fill="{BLUE}"/>')
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


def calendar(x, y, s=1.0, mark=None, weeks=0, **_):
    """Wall calendar, no text. mark: day index 0-27 to circle (e.g. 2 = the 3rd). weeks: the first n week rows filled in green with shift bars (a schedule posted ahead)."""
    inner = (f'<rect x="-150" y="-170" width="300" height="340" rx="14" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<rect x="-150" y="-170" width="300" height="70" rx="14" fill="{CORAL}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<circle cx="-80" cy="-176" r="10" fill="{INK}"/><circle cx="80" cy="-176" r="10" fill="{INK}"/>')
    for k in range(28):
        cx, cy = -105 + (k % 7) * 35, -70 + (k // 7) * 55
        inner += f'<rect x="{cx - 12}" y="{cy - 12}" width="24" height="24" rx="4" fill="{SKY}"/>'
        if k // 7 < int(weeks):
            inner += f'<rect x="{cx - 14}" y="{cy - 14}" width="28" height="28" rx="5" fill="{GREEN}" opacity="0.85"/><path d="M{cx - 8} {cy + 2} h16" stroke="{WHITE}" stroke-width="4" stroke-linecap="round"/>'
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


def chart(x, y, s=1.0, trend="up", color=None, **_):
    """Framed line chart on a wall or board. trend: up, down, flat, bend (high and flat, then bending down). color: green, coral, blue, grey overrides the trend colour (a falling line can be good news)."""
    pts = {"up": "-150 90 -70 40 0 60 80 -20 150 -80", "down": "-150 -80 -70 -20 0 -40 80 40 150 90", "flat": "-150 20 -70 30 0 15 80 25 150 20",
           "bend": "-150 -70 -100 -80 -50 -66 0 -74 40 -40 90 30 150 80"}[trend]
    col = {"green": GREEN, "coral": CORAL, "blue": BLUE, "grey": GREY}.get(color) or {"up": GREEN, "down": CORAL, "flat": GREY, "bend": GREEN}[trend]
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
        inner = inner.replace(f'fill="{SKY}"', f'fill="{NAVY}"', 1).replace(f'stroke="{INK}"', f'stroke="{GREY}"') + f'<circle cx="170" cy="-140" r="50" fill="#F3E3B0" stroke="{INK}" stroke-width="5"/>'   # light frame strokes, so the frame shows on the dark glass
    else:
        inner += f'<circle cx="170" cy="-140" r="56" fill="{GOLD}" opacity="0.8" stroke="{INK}" stroke-width="5"/>'
    return _g(x, y, s, inner)


def door(x, y, s=1.0, ajar=False, **_):
    """A tall door (leaving, going out). ajar=True: the door swings open onto a bright doorway with a small figure walking out, and swing marks (staff who keep leaving)."""
    if not ajar:
        return _g(x, y, s, f'<rect x="-125" y="-360" width="250" height="720" rx="6" fill="{LB}" stroke="{INK}" stroke-width="7"/><circle cx="80" cy="10" r="12" fill="{INK}"/>')
    inner = (f'<rect x="-135" y="-370" width="270" height="730" rx="6" fill="{SKY}" stroke="{INK}" stroke-width="8"/>'
             f'<path d="M-135 250 H135" stroke="{INK}" stroke-width="3" opacity="0.35"/>'
             f'<g transform="translate(40 250) scale(0.62)" opacity="0.75"><path d="M-46 0 V-90 Q-46 -130 0 -130 Q46 -130 46 -90 V0 Z" fill="{GREY}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<circle cx="0" cy="-178" r="40" fill="{GREY}" stroke="{INK}" stroke-width="{SW}"/></g>'
             f'<path d="M135 -370 L250 -330 L250 330 L135 360 Z" fill="{LB}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
             f'<circle cx="230" cy="10" r="11" fill="{INK}"/>'
             f'<path d="M290 -230 q30 60 0 120 M318 -270 q44 100 0 200 M290 110 q30 60 0 120" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" opacity="0.7"/>'
             f'<path d="M135 360 Q230 400 300 330" fill="none" stroke="{INK}" stroke-width="4" stroke-dasharray="14 12" opacity="0.6"/>')
    return _g(x, y, s, inner)


def door_box(x, y, s=1.0, ajar=False, **_):
    return [x - 140 * s, y - 375 * s, (470 if ajar else 280) * s, 780 * s]


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
    """Whiteboard on a stand or wall. drawing: graph (supply/demand cross), shift (supply curve moves right: dashed old line, arrow), lines (notes), boxes (diagram)."""
    inner = (f'<rect x="-350" y="-210" width="700" height="420" rx="12" fill="{WHITE}" stroke="{INK}" stroke-width="7"/>'
             f'<rect x="-120" y="210" width="240" height="14" rx="7" fill="{GREY}"/>')
    if drawing == "graph":
        inner += (f'<path d="M-240 -150 V150 H250" fill="none" stroke="{INK}" stroke-width="5"/>'
                  f'<path d="M-200 -120 L200 120" stroke="{BLUE}" stroke-width="9" stroke-linecap="round"/><path d="M-200 120 L200 -120" stroke="{GREEN}" stroke-width="9" stroke-linecap="round"/>'
                  f'<circle cx="0" cy="0" r="14" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>')
    elif drawing == "shift":
        inner += (f'<path d="M-240 -150 V150 H250" fill="none" stroke="{INK}" stroke-width="5"/>'
                  f'<path d="M-200 -120 L200 120" stroke="{BLUE}" stroke-width="9" stroke-linecap="round"/>'
                  f'<path d="M-200 120 L120 -120" stroke="{GREEN}" stroke-width="7" stroke-linecap="round" stroke-dasharray="16 14" opacity="0.6"/>'
                  f'<path d="M-90 120 L230 -120" stroke="{GREEN}" stroke-width="9" stroke-linecap="round"/>'
                  f'<path d="M-40 -95 H50" stroke="{CORAL}" stroke-width="8" stroke-linecap="round"/><path d="M50 -95 L32 -110 M50 -95 L32 -80" stroke="{CORAL}" stroke-width="8" stroke-linecap="round"/>'
                  f'<circle cx="43" cy="26" r="14" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>')
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


def speech(x, y, s=1.0, side="left", inner="none", **_):
    """Speech bubble with lines (no words). side: which side the tail points to. inner = a preset drawn small inside instead of the lines (e.g. calendar)."""
    tail = "M-60 70 L-120 140 L-10 80" if side == "left" else "M60 70 L120 140 L10 80"
    if inner in PRESETS and inner not in ("thought", "speech"):
        body = (f'<rect x="-200" y="-150" width="400" height="230" rx="40" fill="{WHITE}" stroke="{INK}" stroke-width="6"/>'
                f'<path d="{tail}" fill="{WHITE}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
                f'<rect x="-150" y="60" width="300" height="16" fill="{WHITE}"/>' + PRESETS[inner][0](0, -35, 0.5))
        return _g(x, y, s, body)
    return _g(x, y, s, (f'<rect x="-200" y="-90" width="400" height="170" rx="40" fill="{WHITE}" stroke="{INK}" stroke-width="6"/>'
                        f'<path d="{tail}" fill="{WHITE}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
                        f'<line x1="-130" y1="-25" x2="130" y2="-25" stroke="{GREY}" stroke-width="12" stroke-linecap="round"/>'
                        f'<line x1="-130" y1="25" x2="60" y2="25" stroke="{GREY}" stroke-width="12" stroke-linecap="round"/>'))


def speech_box(x, y, s=1.0, inner="none", **_):
    return [x - 205 * s, y - (155 if inner in PRESETS else 95) * s, 410 * s, (300 if inner in PRESETS else 240) * s]


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


def blocks(x, y, s=1.0, n=3, fallen=False, **_):
    """Toy building blocks. A tower of n cubes (default 3); fallen=True shows a small stack with two blocks tumbled on the floor. (x, y) = centre."""
    cols = [BLUE, GOLD, GREEN, CORAL, LB]
    def cube(cx, cy, c, rot=0):
        return (f'<g transform="translate({cx} {cy}) rotate({rot})"><rect x="-40" y="-40" width="80" height="80" rx="8" fill="{c}" stroke="{INK}" stroke-width="5"/>'
                f'<circle cx="0" cy="0" r="14" fill="{PAPER}" stroke="{INK}" stroke-width="4"/></g>')
    if fallen:
        inner = cube(-60, 40, cols[0]) + cube(-60, -40, cols[1]) + cube(50, 54, cols[2], 25) + cube(125, 48, cols[3], -18)
    else:
        n = int(n)
        inner = "".join(cube((k % 2) * 8 - 4, 40 * (n - 1) - 80 * k, cols[k % 5]) for k in range(n))
    return _g(x, y, s, inner)


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


# ---------------------------------------------------------------- ad props (paid ads, 29 Oct 2026)
def chip(x, y, s=1.0, label="Accounting", color="blue", **_):
    """Subject chip for paid ads: a rounded pill with a short label (the one place text is allowed in the art). color: blue, light."""
    import html as _h
    w = 40 + 26 * len(label); fill, tc = (BLUE, WHITE) if color == "blue" else (LB, INK)
    return _g(x, y, s, (f'<rect x="{-w / 2:.0f}" y="-40" width="{w:.0f}" height="80" rx="40" fill="{fill}" stroke="{INK}" stroke-width="5"/>'
                        f'<text x="0" y="15" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" font-size="44" fill="{tc}">{_h.escape(label)}</text>'))


def swirl(x, y, s=1.0, symbols="$ % ? 7 + 2 =", rx=200, ry=46, **_):
    """Numbers and symbols orbiting on a flat ellipse (rx, ry) round (x, y): a head spinning with figures (ads; pair with mood dizzy over his head).
    With "anim": "orbit" (and optional "hz", default 0.45) the renderer moves them round the ellipse; without it they stand still."""
    import html as _h
    syms = symbols.split(); n = len(syms); cols = (INK, BLUE, GOLD)
    out = ""
    for k, sym in enumerate(syms):
        a = 2 * math.pi * k / n; px, py = rx * math.cos(a), ry * math.sin(a)
        out += (f'<g class="orb" data-a0="{a:.4f}" data-rx="{rx}" data-ry="{ry}" transform="translate({px:.1f} {py:.1f})">'
                f'<text x="0" y="20" text-anchor="middle" font-family="Inter,sans-serif" font-weight="900" font-size="60" fill="{cols[k % 3]}" stroke="{WHITE}" stroke-width="3" paint-order="stroke">{_h.escape(sym)}</text></g>')
    return _g(x, y, s, out)


def swirl_box(x, y, s=1.0, rx=200, ry=46, **_):
    return [x - (rx + 40) * s, y - (ry + 40) * s, 2 * (rx + 40) * s, 2 * (ry + 40) * s]


def bubble(x, y, s=1.0, label="Hello?", side="left", **_):
    """Chat bubble with a short line of text (ads only): white rounded box, tail to the left, right or down. Pops in with "at": "chunk:N"."""
    import html as _h
    lines = [_h.escape(x.strip()) for x in label.split("|")]   # "Course|problem" = two lines, the first bold-blue
    w = 48 + 22 * max(len(x) for x in label.split("|")); h = 56 + 44 * len(lines)
    tail = {"left": f"M{-w / 2 + 40:.0f} {h / 2 - 2} L{-w / 2 + 10:.0f} {h / 2 + 46} L{-w / 2 + 92:.0f} {h / 2 - 2}",
            "right": f"M{w / 2 - 40:.0f} {h / 2 - 2} L{w / 2 - 10:.0f} {h / 2 + 46} L{w / 2 - 92:.0f} {h / 2 - 2}",
            "down": f"M-26 {h / 2 - 2} L0 {h / 2 + 46} L26 {h / 2 - 2}", "none": ""}[side]
    return _g(x, y, s, (f'<rect x="{-w / 2:.0f}" y="{-h / 2}" width="{w:.0f}" height="{h}" rx="30" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>'
                        + (f'<path d="{tail}" fill="{WHITE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                           f'<rect x="{-w / 2 + 6:.0f}" y="{h / 2 - 8}" width="{w - 12:.0f}" height="12" fill="{WHITE}"/>' if tail else "")
                        + "".join(f'<text x="0" y="{-h / 2 + 46 + 44 * k:.0f}" text-anchor="middle" font-family="Inter,sans-serif" font-weight="{800 if k == 0 and len(lines) > 1 else 700}" font-size="36" fill="{BLUE if k == 0 and len(lines) > 1 else INK}">{ln}</text>' for k, ln in enumerate(lines))))


def bubble_box(x, y, s=1.0, label="Hello?", **_):
    w = 48 + 22 * max(len(x) for x in label.split("|")); h = 56 + 44 * len(label.split("|"))
    return [x - w / 2 * s, y - h / 2 * s, w * s, (h + 50) * s]


def lamp(x, y, s=1.0, on=True, **_):
    """A desk lamp; (x, y) = centre of its base on the desk. on=True adds a warm glow cone under the shade."""
    glow = f'<path d="M-150 -60 L-10 -250 L120 -250 L220 -60 Z" fill="{GOLD}" opacity="0.22"/>' if on else ""
    return _g(x, y, s, (glow + f'<ellipse cx="0" cy="0" rx="90" ry="22" fill="{NAVY}" stroke="{INK}" stroke-width="5"/>'
                        f'<path d="M0 -10 L40 -230" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
                        f'<path d="M-30 -230 L110 -230 L140 -300 L-60 -300 Z" fill="{NAVY}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
                        + (f'<ellipse cx="40" cy="-228" rx="68" ry="12" fill="{GOLD}" opacity="0.9"/>' if on else "")))


def stat_card(x, y, s=1.0, big="400+", small="students", **_):
    """Proof card (ads only): a white card with a big blue number and a small label under it. (x, y) = centre."""
    return _g(x, y, s, (f'<rect x="-230" y="-150" width="460" height="300" rx="28" fill="{WHITE}" stroke="{INK}" stroke-width="6"/>'
                        f'<text x="0" y="10" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" font-size="124" fill="{BLUE}">{big}</text>'
                        f'<text x="0" y="90" text-anchor="middle" font-family="Inter,sans-serif" font-weight="700" font-size="44" fill="{INK}">{small}</text>'))


def lightbulb(x, y, s=1.0, **_):
    """A lit lightbulb with short rays: the moment it clicks. (x, y) = centre of the bulb."""
    rays = "".join(f'<line x1="{_f(120 * math.cos(a))}" y1="{_f(120 * math.sin(a))}" x2="{_f(160 * math.cos(a))}" y2="{_f(160 * math.sin(a))}" stroke="{GOLD}" stroke-width="9" stroke-linecap="round"/>' for a in [k * math.pi / 4 for k in range(8)] if abs(math.sin(a)) < 0.95 or math.sin(a) < 0)
    return _g(x, y, s, (rays + f'<circle cx="0" cy="0" r="80" fill="#FFE49A" stroke="{INK}" stroke-width="6"/>'
                        f'<path d="M-30 70 L-24 118 H24 L30 70 Z" fill="{GREY}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                        f'<path d="M-18 30 L0 -10 L18 30" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'))


def chip_box(x, y, s=1.0, label="Accounting", **_):
    w = 40 + 26 * len(label)
    return [x - w / 2 * s, y - 42 * s, w * s, 84 * s]


def exam_sheet(x, y, s=1.0, rows=4, ticked=0, rot=0, **_):
    """A past-exam paper: numbered question rows (bullets, no words); the first `ticked` rows carry a green tick."""
    h = 70 + rows * 62
    inner = f'<rect x="-130" y="{-h / 2:.0f}" width="260" height="{h}" rx="10" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/>'
    inner += f'<line x1="-95" y1="{-h / 2 + 34:.0f}" x2="40" y2="{-h / 2 + 34:.0f}" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
    for k in range(rows):
        yy = -h / 2 + 90 + k * 62
        inner += (f'<circle cx="-92" cy="{yy:.0f}" r="10" fill="{BLUE}"/>'
                  f'<line x1="-62" y1="{yy:.0f}" x2="{30 if k % 2 else 55}" y2="{yy:.0f}" stroke="{GREY}" stroke-width="8" stroke-linecap="round"/>')
        if k < ticked:
            inner += f'<path d="M62 {yy:.0f} L80 {yy + 18:.0f} L112 {yy - 16:.0f}" fill="none" stroke="{GREEN}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
    return _g(x, y, s, inner, rot)


def cost_pools(x, y, s=1.0, **_):
    """ABC costing: one overhead pool (a box of coins) splits by arrows into three activity pools, then into two products. No text."""
    inner = (f'<rect x="-120" y="-250" width="240" height="120" rx="16" fill="#F3D9A6" stroke="{INK}" stroke-width="{SW}"/>'
             + "".join(f'<ellipse cx="{cx}" cy="-178" rx="26" ry="10" fill="{GOLD}" stroke="{INK}" stroke-width="3"/><ellipse cx="{cx}" cy="-192" rx="26" ry="10" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>' for cx in (-60, 0, 60)))
    for k, cx in enumerate((-230, 0, 230)):
        col = (LB, "#CFE9D9", "#F6D0CC")[k]
        inner += (f'<path d="M{cx * 0.35:.0f} -128 L{cx:.0f} -50" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                  f'<path d="M{cx:.0f} -48 l-14 -20 h28 z" fill="{INK}"/>'
                  f'<rect x="{cx - 80}" y="-40" width="160" height="90" rx="14" fill="{col}" stroke="{INK}" stroke-width="{SW}"/>'
                  f'<circle cx="{cx}" cy="5" r="18" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>')
    for k, cx in enumerate((-130, 130)):
        for src in ((-230, 0) if k == 0 else (0, 230)):
            inner += f'<path d="M{src} 52 L{cx} 128" stroke="{BLUE}" stroke-width="5" stroke-linecap="round" stroke-dasharray="12 10"/>'
        inner += (f'<path d="M{cx - 70} 135 h140 v100 h-140 z" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
                  f'<path d="M{cx - 70} 135 l70 -30 l70 30" fill="#E6E3DA" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>')
    return _g(x, y, s, inner)


def scatter_plot(x, y, s=1.0, line=True, **_):
    """Regression: a framed scatter plot of dots with a fitted gold line (line=False hides it). No text."""
    pts = [(-200, 110), (-160, 70), (-130, 95), (-90, 40), (-60, 60), (-20, 10), (10, 30), (50, -20), (80, 0), (120, -60), (150, -40), (190, -95)]
    inner = (f'<rect x="-270" y="-200" width="540" height="400" rx="14" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<path d="M-230 -160 V160 H240" fill="none" stroke="{INK}" stroke-width="5"/>'
             + "".join(f'<circle cx="{px}" cy="{py}" r="12" fill="{BLUE}" stroke="{INK}" stroke-width="2.5"/>' for px, py in pts))
    if line: inner += f'<path d="M-220 120 L220 -110" stroke="{GOLD}" stroke-width="10" stroke-linecap="round"/>'
    return _g(x, y, s, inner)


def exam_sheet_box(x, y, s=1.0, rows=4, **_):
    h = 70 + rows * 62
    return [x - 135 * s, y - (h / 2 + 5) * s, 270 * s, (h + 10) * s]


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
# ---------------------------------------------------------------- scenario graphics (added 25 Oct 2026, Ledger not required in every scene)
def code_screen(x, y, s=1.0, trend="none", **_):
    """Big desktop monitor showing abstract code lines (no words). (x, y) = centre of the monitor. trend: none, down (falling line) or up."""
    cols = [BLUE, GREEN, CORAL, LB, GOLD]
    inner = (f'<rect x="-290" y="-200" width="580" height="380" rx="20" fill="{NAVY}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<rect x="-266" y="-176" width="532" height="332" rx="8" fill="#16203A"/>'
             f'<path d="M-40 180 L-60 240 H60 L40 180 Z" fill="{GREY}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
             f'<rect x="-130" y="240" width="260" height="22" rx="10" fill="{GREY}" stroke="{INK}" stroke-width="{SW}"/>')
    rows = [(0, 190, 0), (40, 260, 1), (40, 150, 2), (80, 300, 3), (80, 200, 0), (40, 230, 4), (0, 120, 1), (0, 250, 2), (40, 170, 3)]
    for k, (ind, ln, c) in enumerate(rows):
        yy = -145 + k * 34
        inner += f'<line x1="{-240 + ind}" y1="{yy}" x2="{-240 + ind + ln}" y2="{yy}" stroke="{cols[c]}" stroke-width="12" stroke-linecap="round"/>'
    if trend in ("down", "up"):
        pts = "M120 -40 L170 -10 L215 30 L250 100" if trend == "down" else "M120 100 L170 60 L215 20 L250 -50"
        inner += f'<rect x="100" y="-80" width="160" height="200" rx="8" fill="#16203A"/><path d="{pts}" fill="none" stroke="{CORAL if trend == "down" else GREEN}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
    return _g(x, y, s, inner)


def chessboard(x, y, s=1.0, **_):
    """Chessboard seen from above with a few abstract pieces (a logic game). (x, y) = centre."""
    inner = f'<rect x="-210" y="-210" width="420" height="420" rx="8" fill="{PAPER}" stroke="{INK}" stroke-width="{SW}"/>'
    for r in range(8):
        for c in range(8):
            if (r + c) % 2:
                inner += f'<rect x="{-200 + c * 50}" y="{-200 + r * 50}" width="50" height="50" fill="{BLUE}" opacity="0.55"/>'
    def piece(cx, cy, kind, col):
        base = f'<path d="M{cx - 16} {cy + 22} H{cx + 16} L{cx + 10} {cy + 4} H{cx - 10} Z" fill="{col}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        if kind == "pawn":
            return base + f'<circle cx="{cx}" cy="{cy - 6}" r="11" fill="{col}" stroke="{INK}" stroke-width="3"/>'
        if kind == "king":
            return base + (f'<path d="M{cx - 11} {cy + 6} L{cx - 14} {cy - 14} H{cx + 14} L{cx + 11} {cy + 6} Z" fill="{col}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
                           f'<path d="M{cx} {cy - 14} V{cy - 30} M{cx - 7} {cy - 23} H{cx + 7}" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>')
        return base + f'<path d="M{cx - 10} {cy + 6} L{cx - 12} {cy - 16} L{cx - 4} {cy - 8} L{cx} {cy - 20} L{cx + 4} {cy - 8} L{cx + 12} {cy - 16} L{cx + 10} {cy + 6} Z" fill="{col}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    for cx, cy, k, col in [(-125, 125, "pawn", WHITE), (-25, 125, "pawn", WHITE), (75, 125, "pawn", WHITE), (-75, 175, "king", WHITE), (125, 175, "queen", WHITE),
                           (-125, -75, "pawn", GOLD), (-25, -75, "pawn", GOLD), (75, -125, "pawn", GOLD), (125, -175, "king", GOLD), (-75, -25, "queen", GOLD)]:
        inner += piece(cx, cy, k, col)
    return _g(x, y, s, inner)


def robot_arm(x, y, s=1.0, hold="none", drop=False, flip=False, **_):
    """Industrial robot arm on a base with a two-finger claw. hold: none, block or piece. drop=True opens the claw and lets the block fall. flip faces left. (x, y) = centre."""
    gap = 52 if drop else 30
    inner = (f'<rect x="-90" y="190" width="180" height="34" rx="10" fill="{NAVY}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<rect x="-40" y="140" width="80" height="55" rx="8" fill="{GREY}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<path d="M0 140 L-110 10" stroke="{INK}" stroke-width="46" stroke-linecap="round"/><path d="M0 140 L-110 10" stroke="{BLUE}" stroke-width="34" stroke-linecap="round"/>'
             f'<path d="M-110 10 L90 -90" stroke="{INK}" stroke-width="40" stroke-linecap="round"/><path d="M-110 10 L90 -90" stroke="{LB}" stroke-width="28" stroke-linecap="round"/>'
             f'<circle cx="0" cy="140" r="24" fill="{GOLD}" stroke="{INK}" stroke-width="{SW}"/><circle cx="-110" cy="10" r="22" fill="{GOLD}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<circle cx="90" cy="-90" r="20" fill="{GOLD}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<rect x="{90 - gap - 10}" y="-78" width="{2 * gap + 20}" height="14" rx="6" fill="{NAVY}" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M{90 - gap} -66 V-10" stroke="{INK}" stroke-width="14" stroke-linecap="round"/><path d="M{90 + gap} -66 V-10" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>'
             f'<path d="M{90 - gap} -66 V-10" stroke="{GREY}" stroke-width="7" stroke-linecap="round"/><path d="M{90 + gap} -66 V-10" stroke="{GREY}" stroke-width="7" stroke-linecap="round"/>')
    if hold == "block" and not drop:
        inner += f'<g transform="translate(90 -22)"><rect x="-28" y="-28" width="56" height="56" rx="6" fill="{CORAL}" stroke="{INK}" stroke-width="4"/></g>'
    elif hold == "piece" and not drop:
        inner += f'<path d="M80 -2 L76 -34 L84 -24 L90 -42 L96 -24 L104 -34 L100 -2 Z" fill="{WHITE}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    elif drop:
        inner += f'<g transform="translate(70 120) rotate(24)"><rect x="-28" y="-28" width="56" height="56" rx="6" fill="{CORAL}" stroke="{INK}" stroke-width="4"/></g>'
    if flip:
        inner = f'<g transform="scale(-1 1)">{inner}</g>'
    return _g(x, y, s, inner)


def robot_arm_box(x, y, s=1.0, **_):
    return [x - 150 * s, y - 115 * s, 300 * s, 340 * s]


def toddler(x, y, s=1.0, reach=True, **_):
    """A small child (big head, short body) reaching up to place a block. (x, y) = between the feet."""
    arms = (f'<path d="M-38 -70 L-62 -130 M38 -70 L62 -130" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
            f'<path d="M-38 -70 L-62 -130 M38 -70 L62 -130" stroke="{PAPER}" stroke-width="10" stroke-linecap="round"/>'
            f'<circle cx="-62" cy="-132" r="12" fill="{PAPER}" stroke="{INK}" stroke-width="3.5"/><circle cx="62" cy="-132" r="12" fill="{PAPER}" stroke="{INK}" stroke-width="3.5"/>') if reach else ""
    inner = (f'<ellipse cx="0" cy="4" rx="44" ry="7" fill="{INK}" opacity="0.10"/>'
             f'<path d="M-40 0 V-50 Q-40 -88 0 -88 Q40 -88 40 -50 V0 Z" fill="{GOLD}" stroke="{INK}" stroke-width="{SW}"/>' + arms +
             f'<circle cx="0" cy="-140" r="48" fill="{PAPER}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<path d="M-22 -184 Q0 -200 22 -184" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
             f'<circle cx="-16" cy="-142" r="5.5" fill="{INK}"/><circle cx="16" cy="-142" r="5.5" fill="{INK}"/>'
             f'<path d="M-14 -122 Q0 -110 14 -122" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    return _g(x, y, s, inner)


def toddler_box(x, y, s=1.0, **_):
    return [x - 75 * s, y - 192 * s, 150 * s, 196 * s]


def meeting_table(x, y, s=1.0, deal=True, **_):
    """Two people facing each other across a table, a speech bubble over each and (deal=True) a handshake between them. No words. (x, y) = centre of the table top."""
    inner = (person(-290, 250 - 10, 1.0, mood="smile", color=BLUE) + person(290, 250 - 10, 1.0, mood="smile", color="#F3D9A6") +
             f'<rect x="-190" y="-14" width="380" height="30" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<rect x="-160" y="16" width="24" height="230" fill="{GOLD}" stroke="{INK}" stroke-width="5"/><rect x="136" y="16" width="24" height="230" fill="{GOLD}" stroke="{INK}" stroke-width="5"/>'
             + speech(-260, -150, 0.55, side="left") + speech(260, -150, 0.55, side="right"))
    if deal:
        inner += handshake(0, -70, 0.45)
    return _g(x, y, s, inner)


def meeting_table_box(x, y, s=1.0, **_):
    return [x - 345 * s, y - 245 * s, 690 * s, 500 * s]


def whiteboard_team(x, y, s=1.0, **_):
    """A whiteboard with a diagram and three people in front: the middle one points at it with a stick (leading a team). No words. (x, y) = centre of the board."""
    inner = whiteboard(0, 0, 1.0, drawing="boxes")
    inner += person(-250, 440, 0.95, mood="smile", color=BLUE) + person(250, 440, 0.95, mood="smile", color="#CFE9D9")
    inner += person(0, 440, 1.1, mood="smile", color="#F3D9A6")
    inner += f'<path d="M45 330 L150 80" stroke="{INK}" stroke-width="9" stroke-linecap="round"/><circle cx="150" cy="80" r="9" fill="{CORAL}" stroke="{INK}" stroke-width="3"/>'
    return _g(x, y, s, inner)


def whiteboard_team_box(x, y, s=1.0, **_):
    return [x - 360 * s, y - 215 * s, 720 * s, 665 * s]


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
    if name == "store":   # department store floor (1 Nov 2026): warm wall, cubby shelves of folded clothes, a hanging rail sign (no text), floor tiles
        cub = "".join(f'<rect x="{x}" y="{y}" width="70" height="70" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>'
                      f'<rect x="{x + 10}" y="{y + 36}" width="50" height="14" rx="3" fill="{c}" stroke="{INK}" stroke-width="2.5"/><rect x="{x + 10}" y="{y + 48}" width="50" height="14" rx="3" fill="{c}" stroke="{INK}" stroke-width="2.5"/>'
                      for k, (x, y) in enumerate((x, y) for y in (900, 970, 1040) for x in (790, 860, 930)) for c in [[BLUE, CORAL, GREEN, "#F3D9A6", LB, NAVY, CORAL, GREEN, BLUE][k]])
        return (wall("#F6EEE3", 0.85) + ground() +
                f'<rect x="780" y="890" width="230" height="230" rx="6" fill="#E3D2B5" stroke="{INK}" stroke-width="5"/>' + cub +
                f'<path d="M150 820 V860 M330 820 V860" stroke="{INK}" stroke-width="4"/><rect x="110" y="860" width="260" height="70" rx="12" fill="{BLUE}" stroke="{INK}" stroke-width="5"/>'
                f'<path d="M210 900 q30 -26 60 0" fill="none" stroke="{WHITE}" stroke-width="6" stroke-linecap="round"/><path d="M240 880 v-8" stroke="{WHITE}" stroke-width="6" stroke-linecap="round"/>')
    if name == "none":
        return ""
    return ground()  # paper


# ---------------------------------------------------------------- course visuals and zone backdrops (tutoring ad v6, 30 Oct 2026)
RED = "#D64545"


def _t(x, y, txt, size=34, w=800, col=INK, anchor="middle", extra=""):
    import html as _h
    return f'<text x="{_f(x)}" y="{_f(y)}" text-anchor="{anchor}" font-family="Inter,sans-serif" font-weight="{w}" font-size="{size}" fill="{col}"{extra}>{_h.escape(txt)}</text>'


def backdrop(x, y, s=1.0, w=1080, wall=SKY, floor="#F1ECE2", **_):
    """A self-contained room panel for a scene made of several zones: a wall of colour `wall` w wide, a floor band below and the ground line. (x, y) = centre of the ground line."""
    h = w / 2
    return (f'<rect x="{_f(x - h)}" y="{_f(y - 1100)}" width="{_f(w)}" height="1100" fill="{wall}" stroke="none"/>'
            f'<rect x="{_f(x - h)}" y="{_f(y)}" width="{_f(w)}" height="500" fill="{floor}" stroke="none"/>'
            f'<path d="M{_f(x - h + 30)} {_f(y)} Q{_f(x)} {_f(y - 14)} {_f(x + h - 30)} {_f(y)}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')


def backdrop_box(x, y, s=1.0, w=1080, **_):
    return [x - w / 2, y - 1100, w, 1600]


def balance_sheet(x, y, s=1.0, left="$12,400", right="$11,900", **_):
    """Financial accounting: a balance sheet card, Assets against Liabilities + Equity, whose totals do not match (red not-equal mark)."""
    inner = (f'<rect x="-360" y="-250" width="720" height="500" rx="20" fill="{WHITE}" stroke="{INK}" stroke-width="6"/>'
             + _t(0, -168, "Balance sheet", 54, 900)
             + f'<line x1="-320" y1="-132" x2="320" y2="-132" stroke="{INK}" stroke-width="4"/>'
             + _t(-320, -58, "Assets", 48, 800, BLUE, "start") + _t(320, -58, left, 60, 900, INK, "end")
             + f'<circle cx="200" cy="22" r="40" fill="{WHITE}" stroke="{RED}" stroke-width="7"/>'
             f'<path d="M180 12 H220 M180 32 H220 M210 -6 L190 50" stroke="{RED}" stroke-width="7" stroke-linecap="round"/>'
             + _t(-320, 108, "Liabilities + Equity", 46, 800, BLUE, "start") + _t(320, 200, right, 60, 900, RED, "end"))
    return _g(x, y, s, inner)


def abc_tangle(x, y, s=1.0, **_):
    """Cost accounting (ABC costing): overhead flows to three activities (setups, orders, inspection), then by crossing, tangled arrows to two products, with a question mark."""
    inner = f'<rect x="-360" y="-250" width="720" height="500" rx="20" fill="{WHITE}" stroke="{INK}" stroke-width="6"/>'
    inner += f'<rect x="-140" y="-228" width="280" height="80" rx="16" fill="#F3D9A6" stroke="{INK}" stroke-width="5"/>' + _t(0, -173, "Overhead", 44, 900)
    acts = ((-232, "Setups", LB), (0, "Orders", "#CFE9D9"), (232, "Inspection", "#F6D0CC"))
    for ax, lab, col in acts:
        inner += (f'<path d="M{ax * 0.3:.0f} -146 L{ax} -84" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><path d="M{ax} -74 l-12 -18 h24 z" fill="{INK}"/>'
                  f'<rect x="{ax - 110}" y="-72" width="220" height="76" rx="14" fill="{col}" stroke="{INK}" stroke-width="5"/>' + _t(ax, -22, lab, 36, 800))
    prods = (-150, 150)
    for k, (ax, _l, _c) in enumerate(acts):   # every activity feeds every product: arrows cross and loop (the confusing part)
        for j, px in enumerate(prods):
            bend = (70 if (k + j) % 2 else -70)
            inner += f'<path d="M{ax} 6 Q{(ax + px) / 2 + bend:.0f} 74 {px} 132" fill="none" stroke="{BLUE}" stroke-width="5" stroke-linecap="round" stroke-dasharray="12 9"/>'
    for px, lab in zip(prods, ("Product A", "Product B")):
        inner += f'<rect x="{px - 130}" y="134" width="260" height="86" rx="16" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>' + _t(px, 192, lab, 42, 800)
    inner += _t(0, 122, "?", 92, 900, RED, extra=f' stroke="{WHITE}" stroke-width="8" paint-order="stroke"')
    return _g(x, y, s, inner)


def regression_guess(x, y, s=1.0, **_):
    """Statistics (regression): a scatter plot of points on x and y axes with three dashed candidate lines and a big question mark (which line fits?)."""
    pts = [(-200, 110), (-160, 70), (-130, 95), (-90, 40), (-60, 60), (-20, 10), (10, 30), (50, -20), (80, 0), (120, -60), (150, -40), (190, -95)]
    inner = (f'<rect x="-300" y="-230" width="600" height="460" rx="20" fill="{WHITE}" stroke="{INK}" stroke-width="6"/>'
             f'<path d="M-240 -180 V160 H260" fill="none" stroke="{INK}" stroke-width="5"/>'
             + _t(-266, -140, "y", 50, 900, INK) + _t(266, 215, "x", 50, 900, INK))
    for (x0, y0, x1, y1), col in (((-230, 40, 230, 40), CORAL), ((-230, -120, 230, 150), GOLD), ((-230, 150, 200, -170), GREY)):
        inner += f'<path d="M{x0} {y0} L{x1} {y1}" stroke="{col}" stroke-width="8" stroke-linecap="round" stroke-dasharray="18 12"/>'
    inner += "".join(f'<circle cx="{px}" cy="{py}" r="12" fill="{BLUE}" stroke="{INK}" stroke-width="2.5"/>' for px, py in pts)
    inner += _t(205, -100, "?", 120, 900, RED)
    return _g(x, y, s, inner)


def supply_shift(x, y, s=1.0, **_):
    """Economics: supply and demand on Price and Quantity axes. Supply S shifts right to S′ (arrow); the old equilibrium is a dot, the new one is marked ?."""
    D = lambda q: -150 + 0.7 * (q + 200); S0 = lambda q: 130 - 0.8 * (q + 200); S1 = lambda q: 130 - 0.8 * (q + 90)
    e0 = (-20 / 1.5, D(-20 / 1.5)); e1 = (68 / 1.5, D(68 / 1.5))
    inner = (f'<rect x="-320" y="-250" width="640" height="500" rx="20" fill="{WHITE}" stroke="{INK}" stroke-width="6"/>'
             f'<path d="M-240 -200 V170 H280" fill="none" stroke="{INK}" stroke-width="5"/>'
             + _t(-226, -208, "Price", 42, 800, INK, "start") + _t(290, 226, "Quantity", 42, 800, INK, "end")
             + f'<path d="M-200 {D(-200):.0f} L200 {D(200):.0f}" stroke="{BLUE}" stroke-width="9" stroke-linecap="round"/>' + _t(222, D(200) + 12, "D", 54, 900, BLUE, "start")
             + f'<path d="M-200 {S0(-200):.0f} L150 {S0(150):.0f}" stroke="{NAVY}" stroke-width="9" stroke-linecap="round" opacity="0.55"/>' + _t(150, S0(150) - 16, "S", 54, 900, NAVY)
             + f'<path d="M-90 {S1(-90):.0f} L260 {S1(260):.0f}" stroke="{GOLD}" stroke-width="9" stroke-linecap="round"/>' + _t(250, S1(260) - 16, "S′", 54, 900, GOLD)
             + f'<path d="M126 -120 H196" stroke="{INK}" stroke-width="6" stroke-linecap="round"/><path d="M212 -120 l-20 -12 v24 z" fill="{INK}"/>'
             + f'<circle cx="{e0[0]:.0f}" cy="{e0[1]:.0f}" r="13" fill="{INK}"/>'
             + f'<circle cx="{e1[0]:.0f}" cy="{e1[1]:.0f}" r="16" fill="{WHITE}" stroke="{RED}" stroke-width="7"/>' + _t(e1[0] + 6, e1[1] + 82, "?", 90, 900, RED))
    return _g(x, y, s, inner)



# ---------------------------------------------------------------- Halloween (31 Oct 2026, finance-bro life-of reel)
ORANGE = "#F08A24"


def pumpkin(x, y, s=1.0, face=True, **_):
    """A jack-o'-lantern pumpkin (no text). (x, y) = centre. face=False draws a plain pumpkin."""
    inner = (f'<path d="M-6 -66 Q-4 -86 10 -92" fill="none" stroke="#3F6B2F" stroke-width="9" stroke-linecap="round"/>'
             f'<ellipse cx="-38" cy="6" rx="52" ry="66" fill="{ORANGE}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<ellipse cx="38" cy="6" rx="52" ry="66" fill="{ORANGE}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<ellipse cx="0" cy="6" rx="46" ry="70" fill="{ORANGE}" stroke="{INK}" stroke-width="{SW}"/>')
    if face:
        inner += (f'<path d="M-40 -14 L-22 -34 L-6 -14 Z M6 -14 L22 -34 L40 -14 Z" fill="{INK}"/>'
                  f'<path d="M-46 20 Q0 60 46 20 L30 26 L22 16 L10 30 L0 18 L-10 30 L-22 16 L-30 26 Z" fill="{INK}"/>')
    return _g(x, y, s, inner)


def candy_bowl(x, y, s=1.0, n=5, **_):
    """A bowl of wrapped candies (no brands). (x, y) = centre. n = candies on top (0-6; 0 = empty bowl)."""
    cols = [BLUE, GOLD, CORAL, GREEN, LB, BLUE]
    pos = [(-56, -36), (-18, -46), (20, -42), (56, -32), (-36, -58), (36, -60)]
    inner = ""
    for k in range(min(n, 6)):
        cx, cy = pos[k]
        inner += (f'<path d="M{cx - 34} {cy - 10} L{cx - 20} {cy} L{cx - 34} {cy + 10} Z M{cx + 34} {cy - 10} L{cx + 20} {cy} L{cx + 34} {cy + 10} Z" fill="{cols[k]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
                  f'<ellipse cx="{cx}" cy="{cy}" rx="22" ry="14" fill="{cols[k]}" stroke="{INK}" stroke-width="3.5"/>')
    inner += (f'<path d="M-100 -26 H100 Q96 50 0 54 Q-96 50 -100 -26 Z" fill="{ORANGE}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
              f'<path d="M-70 4 Q0 18 70 4" fill="none" stroke="{INK}" stroke-width="3" opacity="0.35"/>')
    return _g(x, y, s, inner)


def ghost_kid(x, y, s=1.0, eyes="open", bucket=True, **_):
    """A small trick-or-treater in a ghost sheet holding a pumpkin bucket. (x, y) = between the feet. eyes: open, hope, wide, flat."""
    e = {"open": f'<ellipse cx="-20" cy="-176" rx="10" ry="14" fill="{INK}"/><ellipse cx="20" cy="-176" rx="10" ry="14" fill="{INK}"/>',
         "hope": f'<ellipse cx="-20" cy="-178" rx="11" ry="16" fill="{INK}"/><ellipse cx="20" cy="-178" rx="11" ry="16" fill="{INK}"/>'
                 f'<circle cx="-16" cy="-184" r="4" fill="{WHITE}"/><circle cx="24" cy="-184" r="4" fill="{WHITE}"/>',
         "wide": f'<circle cx="-20" cy="-176" r="14" fill="{INK}"/><circle cx="20" cy="-176" r="14" fill="{INK}"/>',
         "flat": f'<rect x="-32" y="-180" width="22" height="8" rx="4" fill="{INK}"/><rect x="10" y="-180" width="22" height="8" rx="4" fill="{INK}"/>'}.get(eyes)
    inner = (f'<ellipse cx="0" cy="4" rx="66" ry="9" fill="{INK}" opacity="0.10"/>'
             f'<path d="M-30 -6 v8 M30 -6 v8" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
             f'<path d="M-66 -4 Q-74 -140 -46 -204 Q0 -266 46 -204 Q74 -140 66 -4 Q50 -20 33 -4 Q17 -20 0 -4 Q-17 -20 -33 -4 Q-50 -20 -66 -4 Z" '
             f'fill="{WHITE}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>{e}')
    if bucket:
        inner += (f'<path d="M52 -116 Q82 -128 92 -108" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                  f'<path d="M76 -96 Q76 -44 104 -44 Q132 -44 132 -96 Z" fill="{ORANGE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                  f'<path d="M76 -96 Q104 -136 132 -96" fill="none" stroke="{INK}" stroke-width="4"/>'
                  f'<path d="M90 -80 l7 -7 7 7 M106 -80 l7 -7 7 7" fill="none" stroke="{INK}" stroke-width="3.5"/>'
                  f'<path d="M92 -64 Q104 -54 116 -64" fill="none" stroke="{INK}" stroke-width="3.5"/>')
    return _g(x, y, s, inner)


def ghost_kid_box(x, y, s=1.0, **_):
    return [x - 75 * s, y - 250 * s, 215 * s, 262 * s]


# ---------------------------------------------------------------- how-to reel props (1 Nov 2026: "How [role] in [industry] deals with [problem]")
def name_board(x, y, s=1.0, n=12, filled=12, cols=4, **_):
    """Staff board of name tags (no text): n tags in `cols` columns, the first `filled` are filled in (blue strip, face, lines), the rest are empty dashed outlines with only a pin. (x, y) = centre."""
    rows = (int(n) + int(cols) - 1) // int(cols); tw, th, gx, gy = 104, 70, 26, 26
    W = cols * tw + (cols - 1) * gx + 60; H = rows * th + (rows - 1) * gy + 60
    out = (f'<rect x="{-W / 2:.0f}" y="{-H / 2:.0f}" width="{W:.0f}" height="{H:.0f}" rx="12" fill="#E9D3AE" stroke="{INK}" stroke-width="{SW}"/>'
           f'<rect x="{-W / 2 + 12:.0f}" y="{-H / 2 + 12:.0f}" width="{W - 24:.0f}" height="{H - 24:.0f}" rx="6" fill="none" stroke="{INK}" stroke-width="2.5" opacity="0.35"/>')
    for k in range(int(n)):
        cx = -W / 2 + 30 + (k % cols) * (tw + gx); cy = -H / 2 + 30 + (k // cols) * (th + gy)
        if k < int(filled):
            out += (f'<rect x="{cx:.0f}" y="{cy:.0f}" width="{tw}" height="{th}" rx="8" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>'
                    f'<rect x="{cx:.0f}" y="{cy:.0f}" width="{tw}" height="16" rx="6" fill="{BLUE}"/>'
                    f'<circle cx="{cx + 24:.0f}" cy="{cy + 42:.0f}" r="12" fill="{LB}" stroke="{INK}" stroke-width="3"/>'
                    f'<path d="M{cx + 46:.0f} {cy + 36:.0f} h44 M{cx + 46:.0f} {cy + 52:.0f} h30" stroke="{GREY}" stroke-width="5" stroke-linecap="round"/>')
        else:
            out += f'<rect x="{cx:.0f}" y="{cy:.0f}" width="{tw}" height="{th}" rx="8" fill="none" stroke="{INK}" stroke-width="3.5" stroke-dasharray="10 9" opacity="0.55"/>'
        out += f'<circle cx="{cx + tw / 2:.0f}" cy="{cy + 4:.0f}" r="7" fill="{CORAL}" stroke="{INK}" stroke-width="2.5"/>'
    return _g(x, y, s, out)


def name_board_box(x, y, s=1.0, n=12, cols=4, **_):
    rows = (int(n) + int(cols) - 1) // int(cols); W = cols * 104 + (cols - 1) * 26 + 60; H = rows * 70 + (rows - 1) * 26 + 60
    return [x - W / 2 * s, y - H / 2 * s, W * s, H * s]


def clothes_rack(x, y, s=1.0, **_):
    """A clothing rail on two stands with shirts on hangers (a department store floor). (x, y) = centre of the floor line under it."""
    cols = [BLUE, CORAL, "#F3D9A6", GREEN, LB, NAVY]
    out = (f'<path d="M-200 0 V-330 M200 0 V-330" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
           f'<path d="M-240 0 H-160 M160 0 H240" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
           f'<path d="M-215 -330 H215" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
    for k, c in enumerate(cols):
        hx = -160 + k * 64
        out += (f'<path d="M{hx} -330 q0 -18 10 -18 M{hx - 26} -296 L{hx} -318 L{hx + 26} -296" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<path d="M{hx - 30} -298 L{hx - 46} -260 L{hx - 34} -254 L{hx - 30} -150 H{hx + 30} L{hx + 34} -254 L{hx + 46} -260 L{hx + 30} -298 Q{hx} -284 {hx - 30} -298 Z" fill="{c}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    return _g(x, y, s, out)


def clothes_rack_box(x, y, s=1.0, **_):
    return [x - 245 * s, y - 352 * s, 490 * s, 360 * s]


def calculator(x, y, s=1.0, display="", rot=0, **_):
    """A desk calculator with a short display text (e.g. "60%"; the one number shown in the art) and a key grid. (x, y) = centre."""
    import html as _h
    out = (f'<rect x="-110" y="-150" width="220" height="300" rx="22" fill="{NAVY}" stroke="{INK}" stroke-width="{SW}"/>'
           f'<rect x="-86" y="-126" width="172" height="70" rx="8" fill="#DCEFD8" stroke="{INK}" stroke-width="4"/>'
           f'<text x="74" y="-74" text-anchor="end" font-family="Inter,sans-serif" font-weight="900" font-size="{46 if len(display) <= 5 else 34 if len(display) <= 7 else 27}" fill="{INK}">{_h.escape(display)}</text>')
    for r in range(4):
        for c in range(4):
            col = GOLD if c == 3 else (WHITE if r < 3 else LB)
            out += f'<rect x="{-86 + c * 46}" y="{-36 + r * 44}" width="34" height="32" rx="7" fill="{col}" stroke="{INK}" stroke-width="3"/>'
    return _g(x, y, s, out, rot)


def job_ad(x, y, s=1.0, **_):
    """A job ad poster (no words): a blue header, a person icon with a plus badge (hiring) and blank lines. (x, y) = centre."""
    return _g(x, y, s, (f'<rect x="-130" y="-170" width="260" height="340" rx="12" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/>'
                        f'<path d="M-130 -110 V-158 Q-130 -170 -118 -170 H118 Q130 -170 130 -158 V-110 Z" fill="{BLUE}" stroke="{INK}" stroke-width="{SW}"/>'
                        f'<circle cx="0" cy="-42" r="30" fill="{LB}" stroke="{INK}" stroke-width="5"/>'
                        f'<path d="M-52 40 Q-52 -6 0 -6 Q52 -6 52 40 Z" fill="{LB}" stroke="{INK}" stroke-width="5"/>'
                        f'<circle cx="56" cy="-60" r="26" fill="{GREEN}" stroke="{INK}" stroke-width="4"/><path d="M56 -74 v28 M42 -60 h28" stroke="{WHITE}" stroke-width="6" stroke-linecap="round"/>'
                        f'<path d="M-90 82 h180 M-90 112 h130 M-90 142 h160" stroke="{GREY}" stroke-width="9" stroke-linecap="round"/>'
                        f'<circle cx="0" cy="-178" r="9" fill="{CORAL}" stroke="{INK}" stroke-width="3"/>'))


def manual(x, y, s=1.0, **_):
    """A thick training manual (ring binder, no words): spine with rings, a label with blank lines and a small cap icon. (x, y) = centre."""
    return _g(x, y, s, (f'<rect x="-120" y="-150" width="250" height="300" rx="10" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>'
                        f'<rect x="-130" y="-160" width="250" height="300" rx="12" fill="{GREEN}" stroke="{INK}" stroke-width="{SW}"/>'
                        f'<rect x="-130" y="-160" width="44" height="300" rx="10" fill="#24855A" stroke="{INK}" stroke-width="{SW}"/>'
                        + "".join(f'<circle cx="-108" cy="{yy}" r="9" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>' for yy in (-100, -10, 80))
                        + f'<rect x="-60" y="-110" width="150" height="110" rx="8" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>'
                        f'<path d="M-25 -66 L15 -84 L55 -66 L15 -48 Z" fill="{NAVY}"/><path d="M-5 -58 v18 q20 10 40 0 v-18" fill="none" stroke="{NAVY}" stroke-width="5"/>'
                        f'<path d="M-40 -22 h110" stroke="{GREY}" stroke-width="7" stroke-linecap="round"/>'))


def clipboard(x, y, s=1.0, rot=0, **_):
    """A clipboard with a form (blank lines and tick boxes): taking notes in an interview. (x, y) = centre."""
    return _g(x, y, s, (f'<rect x="-90" y="-120" width="180" height="240" rx="12" fill="#C79A5B" stroke="{INK}" stroke-width="{SW}"/>'
                        f'<rect x="-72" y="-96" width="144" height="200" rx="4" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>'
                        f'<rect x="-36" y="-132" width="72" height="30" rx="8" fill="{GREY}" stroke="{INK}" stroke-width="4"/>'
                        + "".join(f'<rect x="-56" y="{yy - 9}" width="18" height="18" rx="3" fill="none" stroke="{INK}" stroke-width="3"/><path d="M-26 {yy} h74" stroke="{GREY}" stroke-width="6" stroke-linecap="round"/>' for yy in (-56, -12, 32, 76))
                        + f'<path d="M-54 -56 l6 7 l12 -14" fill="none" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>'), rot)


def headcount(x, y, s=1.0, n=10, left=6, cols=5, **_):
    """A staff headcount diagram (no words): n small figures in rows; the last `left` are coral and dashed, walking out past an arrow (the share of staff who leave). Under it a bar split in the same share. (x, y) = centre."""
    out = ""; stay = int(n) - int(left)
    for k in range(int(n)):
        cx = -250 + (k % cols) * 110; cy = -60 + (k // cols) * 150
        leave = k >= stay
        c, dash, op = (CORAL, ' stroke-dasharray="8 7"', 0.95) if leave else (LB, "", 1)
        out += (f'<g opacity="{op}"><circle cx="{cx}" cy="{cy - 62}" r="24" fill="{PAPER if not leave else "#F8DEDB"}" stroke="{INK}" stroke-width="4"{dash}/>'
                f'<path d="M{cx - 32} {cy + 30} V{cy - 4} Q{cx - 32} {cy - 32} {cx} {cy - 32} Q{cx + 32} {cy - 32} {cx + 32} {cy - 4} V{cy + 30} Z" fill="{c}" stroke="{INK}" stroke-width="4"{dash}/></g>')
    out += (f'<path d="M296 -40 H366 M346 -62 L370 -40 L346 -18" fill="none" stroke="{CORAL}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M296 110 H366 M346 88 L370 110 L346 132" fill="none" stroke="{CORAL}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    bw = 560; fx = -280 + bw * stay / int(n)
    out += (f'<rect x="-280" y="190" width="{bw}" height="44" rx="10" fill="{LB}" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="{fx:.0f}" y="190" width="{280 - fx:.0f}" height="44" rx="10" fill="{CORAL}" stroke="{INK}" stroke-width="4"/>')
    return _g(x, y, s, out)


def _tw(t, fs, k=0.58):
    """Rough rendered width of Inter 800-900 text at font size fs (used to fit lines into boxes)."""
    return len(str(t)) * fs * k


def flow_box(x, y, s=1.0, num=1, title="Step", sub="", w=860, h=150, ghost=False, **_):
    """Summary-diagram box (the one place with words in the art, for a screenshot-able recap): a hand-drawn rounded box with a blue step number, a bold title and a short key point. (x, y) = centre. w, h: size; the number, title and key point grow with h (h 150 = title 58 px) and shrink to fit w. Pops in with "at": "chunk:N". ghost=True: a grey dashed placeholder with only the number, put under a box that pops in later so the whole diagram fills the frame from the first summary beat."""
    import html as _h
    k = h / 150.0; x0 = -w / 2; tx = x0 + 146 * k; room = w / 2 - tx - 24
    if ghost:
        return _g(x, y, s, (f'<rect x="{x0:.0f}" y="{-h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="24" fill="none" stroke="{GREY}" stroke-width="5" stroke-dasharray="18 14"/>'
                            f'<circle cx="{x0 + 74 * k:.0f}" cy="0" r="{44 * k:.0f}" fill="none" stroke="{GREY}" stroke-width="5" stroke-dasharray="12 10"/>'
                            f'<text x="{x0 + 74 * k:.0f}" y="{19 * k:.0f}" text-anchor="middle" font-family="Inter,sans-serif" font-weight="900" font-size="{54 * k:.0f}" fill="{GREY}">{int(num)}</text>'))
    ft = min(58 * k, room / max(1, len(title) * 0.62)); fsb = min(46 * k, room / max(1, len(sub) * 0.62)) if sub else 0   # 0.62: digits and $ run wide (w46)
    out = (f'<path d="M{x0 + 22:.0f} {-h / 2 + 2:.0f} H{w / 2 - 20:.0f} Q{w / 2 - 1:.0f} {-h / 2:.0f} {w / 2:.0f} {-h / 2 + 22:.0f} V{h / 2 - 20:.0f} Q{w / 2 + 1:.0f} {h / 2:.0f} {w / 2 - 22:.0f} {h / 2 - 1:.0f} H{x0 + 20:.0f} Q{x0 + 1:.0f} {h / 2 + 1:.0f} {x0:.0f} {h / 2 - 22:.0f} V{-h / 2 + 20:.0f} Q{x0 - 1:.0f} {-h / 2 + 1:.0f} {x0 + 22:.0f} {-h / 2 + 2:.0f} Z" fill="{WHITE}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
           f'<circle cx="{x0 + 74 * k:.0f}" cy="0" r="{44 * k:.0f}" fill="{BLUE}" stroke="{INK}" stroke-width="5"/>'
           f'<text x="{x0 + 74 * k:.0f}" y="{19 * k:.0f}" text-anchor="middle" font-family="Inter,sans-serif" font-weight="900" font-size="{54 * k:.0f}" fill="{WHITE}">{int(num)}</text>'
           f'<text x="{tx:.0f}" y="{(-0.1 * h + 9) if sub else (0.35 * ft):.0f}" font-family="Inter,sans-serif" font-weight="900" font-size="{ft:.0f}" fill="{INK}">{_h.escape(title)}</text>')
    if sub:
        out += f'<text x="{tx + 2:.0f}" y="{50 * k - (46 * k - fsb) * 0.4:.0f}" font-family="Inter,sans-serif" font-weight="800" font-size="{fsb:.0f}" fill="#3B4A63">{_h.escape(sub)}</text>'
    return _g(x, y, s, out)


def flow_box_box(x, y, s=1.0, w=860, h=150, **_):
    return [x - w / 2 * s - 4, y - h / 2 * s - 4, w * s + 8, h * s + 8]


def _wobble_line(x0, x1, y, amp=4):
    """A hand-drawn horizontal line (a fraction bar) from x0 to x1 at y, with a slight wave."""
    m = (x0 + x1) / 2
    return f'M{x0:.0f} {y + 2:.0f} Q{(x0 + m) / 2:.0f} {y - amp:.0f} {m:.0f} {y:.0f} T{x1:.0f} {y - 1:.0f}'


def equation(x, y, s=1.0, mode="formula", lhs="", num="", den="", result="", note="", w=880, terms=None, **_):
    """Hand-drawn equation (how-to reels, 1 Nov 2026), drawn in the art so it boils and draws on like the rest. (x, y) = centre.
    mode "formula": `lhs =` on top, then `num` over a hand-drawn fraction bar over `den` (den "" = one line: lhs = num).
    mode "numbers": the real numbers, `num` over `den` (or one line when den is "") then `= result` with a yellow
    highlighter swipe behind the result, and an optional small `note` under it (e.g. "in one year"; state the period).
    Text shrinks to fit width w. Put the numbers row below the formula and pop it in with "at": "chunk:N".
    terms (formula mode, w46 batch): a list of added terms drawn one per line under "lhs =" ("Materials", "+ Labor",
    "+ Overhead rate × hours"), for a sum that is too long for one line; num and den are then ignored.
    In "numbers" mode, terms (["$1,200", "+ $600", "+ $600"]) stack the story's numbers over a sum line and "= result"."""
    import html as _h
    e = _h.escape; out = ""
    T = lambda tx, xx, yy, fs, col=INK, wt=900, anc="middle": f'<text x="{xx:.0f}" y="{yy:.0f}" text-anchor="{anc}" font-family="Inter,sans-serif" font-weight="{wt}" font-size="{fs:.0f}" fill="{col}">{e(str(tx))}</text>'
    if mode == "formula" and terms:
        f1 = min(100, w / max(1, (len(lhs) + 2) * 0.6)); f2 = min(84, w / max(1, max(len(t) for t in terms) * 0.6)); n = len(terms)
        y0 = -(f1 + n * f2 * 1.2) / 2 + f1 * 0.8
        out += T(f"{lhs} =", 0, y0, f1)
        for k, tm in enumerate(terms):
            out += T(tm, 0, y0 + f1 * 0.45 + (k + 1) * f2 * 1.2, f2, BLUE)
        return _g(x, y, s, out)
    if mode == "formula":
        f1 = min(100, w / max(1, (len(lhs) + 2) * 0.6)); f2 = min(84, w / max(1, max(len(num), len(den)) * 0.6))
        if den:
            out += T(f"{lhs} =", 0, -f2 * 1.25, f1)
            bw = max(_tw(num, f2), _tw(den, f2)) + 50
            out += T(num, 0, f2 * 0.62, f2, BLUE)
            out += f'<path d="{_wobble_line(-bw / 2, bw / 2, f2 * 1.0)}" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
            out += T(den, 0, f2 * 2.05, f2, BLUE)
        else:
            out += T(f"{lhs} = {num}", 0, f1 * 0.35, min(f1, w / max(1, (len(lhs) + len(num) + 3) * 0.6)))
        return _g(x, y, s, out)
    if terms:   # numbers mode with terms (w46 batch): the story's numbers one per line, a hand-drawn sum line, "= result" highlighted
        n = len(terms); fs = min(104, w / max(1, max(len(t) for t in list(terms) + ["= " + result]) * 0.62))
        y0 = -((n + 1) * fs * 1.12 + fs * 0.3) / 2 + fs * 0.85
        for k, tm in enumerate(terms):
            out += T(tm, 0, y0 + k * fs * 1.12, fs)
        ly = y0 + (n - 1) * fs * 1.12 + fs * 0.32; hw = max(_tw(t, fs) for t in terms) / 2 + 30
        out += f'<path d="{_wobble_line(-hw, hw, ly, 5)}" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
        ry = ly + fs * 1.05; rw = _tw("= " + result, fs * 1.1, 0.66)
        out += f'<path d="M{-rw / 2 + _tw("= ", fs) - 6:.0f} {ry - fs * 0.3:.0f} L{rw / 2 + 6:.0f} {ry - fs * 0.34:.0f}" fill="none" stroke="#FFD45C" stroke-width="{fs * 0.62:.0f}" stroke-linecap="round" opacity="0.9"/>'
        out += T("= " + result, 0, ry, fs * 1.1)
        if note: out += T(note, 0, ry + fs * 0.75, fs * 0.42, "#3B4A63", 800)
        return _g(x, y, s, out)
    # numbers
    fs = 180
    for _ in range(6):   # shrink until the row fits w
        fw = max(_tw(num, fs), _tw(den, fs)) if den else _tw(num, fs)
        gap = 0.3 * fs; tot = fw + gap + _tw("=", fs) + gap + _tw(result, fs * 1.1, 0.66)
        if tot <= w: break
        fs *= w / tot
    x0 = -tot / 2; cx = x0 + fw / 2
    if den:
        out += T(num, cx, -fs * 0.25, fs)
        out += f'<path d="{_wobble_line(x0 - 10, x0 + fw + 10, fs * 0.02, 5)}" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
        out += T(den, cx, fs * 0.98, fs)
        ey = fs * 0.36
    else:
        out += T(num, cx, fs * 0.36, fs); ey = fs * 0.36
    ex = x0 + fw + gap + _tw("=", fs) / 2
    out += T("=", ex, ey, fs)
    rx = ex + _tw("=", fs) / 2 + gap; rw = _tw(result, fs * 1.1, 0.66)
    out += f'<path d="M{rx - 6:.0f} {ey - fs * 0.3:.0f} L{rx + rw + 6:.0f} {ey - fs * 0.34:.0f}" fill="none" stroke="#FFD45C" stroke-width="{fs * 0.62:.0f}" stroke-linecap="round" opacity="0.9"/>'
    out += T(result, rx, ey, fs * 1.1, INK, 900, "start")
    if note:
        out += T(note, rx + rw / 2, ey + fs * 0.85, fs * 0.42, "#3B4A63", 800)
    return _g(x, y, s, out)


def equation_box(x, y, s=1.0, mode="formula", den="", w=880, terms=None, **_):
    h = (100 + 100 * len(terms) if terms else 400 if den else 150) if mode == "formula" else (130 * (len(terms) + 1) + 60 if terms else 480 if den else 260)
    return [x - w / 2 * s, y - h / 2 * s, w * s, h * s]


def flow_arrow(x, y, s=1.0, dy=50, **_):
    """A short hand-drawn down arrow joining two summary boxes, from (x, y) down by dy."""
    return (f'<path d="M{_f(x)} {_f(y)} q4 {_f(dy / 2)} 0 {_f(dy)}" fill="none" stroke="{BLUE}" stroke-width="{9 * s}" stroke-linecap="round"/>'
            f'<path d="M{_f(x - 16 * s)} {_f(y + dy - 18 * s)} L{_f(x)} {_f(y + dy + 2)} L{_f(x + 16 * s)} {_f(y + dy - 18 * s)}" fill="none" stroke="{BLUE}" stroke-width="{9 * s}" stroke-linecap="round" stroke-linejoin="round"/>')


def flow_arrow_box(x, y, s=1.0, dy=50, **_):
    return [x - 20, y - 4, 40, dy + 10]


# ---------------------------------------------------------------- how-to reel props, week 46 batch (1 Nov 2026): brewery, bike shop, marketplace, payment app, charity, gas stations
STEEL = "#C9D1DC"; AMBER = "#E7A93B"; FOAM = "#FFF7E6"; BRICK = "#C8665A"


def brew_tanks(x, y, s=1.0, n=3, new=False, **_):
    """Craft brewery: n steel conical fermenting tanks on legs, joined by a pipe (no logos). new=True adds a dashed outline of one more tank on the right (a second brewhouse still to be built). (x, y) = centre of the floor line under them."""
    n = int(n); k = n + (1 if new else 0); gap = 180; x0 = -(k - 1) * gap / 2; out = ""
    out += f'<path d="M{x0 - 40:.0f} -300 H{x0 + (n - 1) * gap + 40:.0f}" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
    for i in range(k):
        cx = x0 + i * gap; ghost = i >= n
        st = f'stroke="{GREY if ghost else INK}" stroke-width="{5 if ghost else SW}"' + (' stroke-dasharray="16 12"' if ghost else "")
        fill = "none" if ghost else STEEL
        out += (f'<path d="M{cx - 52:.0f} -128 L{cx - 62:.0f} 0 M{cx + 52:.0f} -128 L{cx + 62:.0f} 0 M{cx - 58:.0f} -50 H{cx + 58:.0f}" {st} fill="none" stroke-linecap="round"/>'
                f'<path d="M{cx - 70:.0f} -390 Q{cx - 70:.0f} -440 {cx:.0f} -440 Q{cx + 70:.0f} -440 {cx + 70:.0f} -390 V-150 L{cx:.0f} -60 L{cx - 70:.0f} -150 Z" fill="{fill}" {st} stroke-linejoin="round"/>')
        if not ghost:
            out += (f'<path d="M{cx - 44:.0f} -400 V-170" stroke="{WHITE}" stroke-width="10" stroke-linecap="round" opacity="0.8"/>'
                    f'<circle cx="{cx + 30:.0f}" cy="-250" r="16" fill="{WHITE}" stroke="{INK}" stroke-width="4"/><path d="M{cx + 30:.0f} -250 l8 -8" stroke="{INK}" stroke-width="3"/>'
                    f'<path d="M{cx:.0f} -60 V-38" stroke="{INK}" stroke-width="8"/><circle cx="{cx:.0f}" cy="-36" r="9" fill="{CORAL}" stroke="{INK}" stroke-width="3"/>')
    return _g(x, y, s, out)


def brew_tanks_box(x, y, s=1.0, n=3, new=False, **_):
    k = int(n) + (1 if new else 0); W = (k - 1) * 180 + 160
    return [x - W / 2 * s, y - 445 * s, W * s, 450 * s]


def pint(x, y, s=1.0, **_):
    """A glass of beer with a foam head (no label). (x, y) = centre."""
    return _g(x, y, s, (f'<path d="M-52 -78 L-42 92 Q-40 104 -28 104 H28 Q40 104 42 92 L52 -78 Z" fill="{AMBER}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
                        f'<path d="M-58 -70 Q-64 -112 -30 -104 Q-14 -128 10 -110 Q36 -126 50 -100 Q70 -96 58 -70 Z" fill="{FOAM}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                        f'<path d="M-30 -40 V70" stroke="{WHITE}" stroke-width="9" stroke-linecap="round" opacity="0.6"/>'
                        f'<circle cx="14" cy="10" r="5" fill="{FOAM}"/><circle cx="24" cy="50" r="4" fill="{FOAM}"/><circle cx="4" cy="-30" r="4" fill="{FOAM}"/>'))


def share_pie(x, y, s=1.0, share=1.0, r=200, mine="", other="", **_):
    """Ownership pie: the founder's share in blue, a new owner's slice in gold (share = founder fraction 0-1). r = radius (a bigger pie after new money). mine / other: short labels in the slices (e.g. "80%", "20%"), optional. (x, y) = centre."""
    import html as _h
    share = max(0.0, min(1.0, float(share))); out = ""
    if share >= 0.999:
        out += f'<circle cx="0" cy="0" r="{r}" fill="{BLUE}" stroke="{INK}" stroke-width="{SW}"/>'
    else:
        a = 2 * math.pi * (1 - share); ex, ey = r * math.sin(a), -r * math.cos(a)
        out += (f'<circle cx="0" cy="0" r="{r}" fill="{BLUE}" stroke="{INK}" stroke-width="{SW}"/>'
                f'<path d="M0 0 L0 {-r} A{r} {r} 0 {1 if a > math.pi else 0} 1 {ex:.1f} {ey:.1f} Z" fill="{GOLD}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>')
    fs = r * 0.36
    T = lambda t, xx, yy, col: (lambda f: f'<text x="{xx:.0f}" y="{yy - fs * 0.35 + f * 0.35:.0f}" text-anchor="middle" font-family="Inter,sans-serif" font-weight="900" font-size="{f:.0f}" fill="{col}">{_h.escape(t)}</text>')(fs * min(1.0, 3.2 / max(3.2, len(t))))
    if mine:
        ma = math.pi * (1 - share) + math.pi * share if share < 0.999 else math.pi
        ma = 2 * math.pi * (1 - share) + math.pi * share
        out += T(mine, 0.5 * r * math.sin(ma), -0.5 * r * math.cos(ma) + fs * 0.35, WHITE)
    if other and share < 0.999:
        oa = math.pi * (1 - share)
        out += T(other, 0.62 * r * math.sin(oa), -0.62 * r * math.cos(oa) + fs * 0.35, INK)
    return _g(x, y, s, out)


def share_pie_box(x, y, s=1.0, r=200, **_):
    return [x - (r + 6) * s, y - (r + 6) * s, (2 * r + 12) * s, (2 * r + 12) * s]


def bike(x, y, s=1.0, frame_only=False, **_):
    """A custom bicycle, side view, blue frame. frame_only=True: the bare frame with dashed wheels (parts still to come). (x, y) = centre of the ground under the wheels."""
    wst = f'stroke="{GREY}" stroke-width="6" stroke-dasharray="16 12"' if frame_only else f'stroke="{INK}" stroke-width="{SW}"'
    out = ""
    for cx in (-190, 190):
        out += f'<circle cx="{cx}" cy="-120" r="118" fill="none" {wst}/>'
        if not frame_only:
            out += (f'<circle cx="{cx}" cy="-120" r="100" fill="none" stroke="{GREY}" stroke-width="3"/>'
                    + "".join(f'<path d="M{cx} -120 L{cx + 100 * math.cos(a):.0f} {-120 + 100 * math.sin(a):.0f}" stroke="{GREY}" stroke-width="2.5"/>' for a in [j * math.pi / 6 for j in range(12)])
                    + f'<circle cx="{cx}" cy="-120" r="12" fill="{INK}"/>')
    # frame: rear hub (-190,-120), bottom bracket (-20,-110), seat top (-70,-300), head top (140,-300), head bottom (150,-250)
    out += (f'<path d="M-190 -120 L-20 -110 L-70 -300 Z M-70 -300 L140 -290 L-20 -110 M140 -290 L190 -120" fill="none" stroke="{BLUE}" stroke-width="16" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="M-190 -120 L-20 -110 L-70 -300 Z M-70 -300 L140 -290 L-20 -110 M140 -290 L190 -120" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round" opacity="0.6"/>')
    if not frame_only:
        out += (f'<path d="M-70 -300 L-80 -335" stroke="{INK}" stroke-width="8"/><path d="M-125 -345 H-30 Q-20 -345 -30 -332 H-120 Z" fill="{NAVY}" stroke="{INK}" stroke-width="4"/>'
                f'<path d="M140 -290 L130 -350 Q150 -372 190 -360" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
                f'<circle cx="-20" cy="-110" r="26" fill="none" stroke="{INK}" stroke-width="6"/><path d="M-20 -110 L10 -60 M-6 -60 H26" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
                f'<path d="M-20 -110 Q-110 -90 -190 -120" fill="none" stroke="{INK}" stroke-width="3" stroke-dasharray="6 5"/>')
    return _g(x, y, s, out)


def bike_box(x, y, s=1.0, **_):
    return [x - 312 * s, y - 375 * s, 624 * s, 377 * s]


def tool_wall(x, y, s=1.0, **_):
    """Workshop pegboard with hanging tools (wrench, hammer, pliers, tape) and a hanging lamp: the shop's overhead (rent, tools and power). No text. (x, y) = centre."""
    holes = "".join(f'<circle cx="{xx}" cy="{yy}" r="4" fill="{INK}" opacity="0.25"/>' for xx in range(-190, 200, 40) for yy in range(-130, 140, 40))
    return _g(x, y, s, (f'<rect x="-220" y="-160" width="440" height="320" rx="12" fill="#E9D3AE" stroke="{INK}" stroke-width="{SW}"/>' + holes +
                        f'<path d="M-150 -100 V60" stroke="{GREY}" stroke-width="18" stroke-linecap="round"/><path d="M-170 -110 a22 22 0 1 1 40 0" fill="none" stroke="{GREY}" stroke-width="16"/><path d="M-150 -100 V60" stroke="{INK}" stroke-width="3" opacity="0.5"/>'
                        f'<path d="M-60 -90 V80" stroke="#B07A3E" stroke-width="16" stroke-linecap="round"/><rect x="-100" y="-118" width="80" height="40" rx="8" fill="{NAVY}" stroke="{INK}" stroke-width="4"/>'
                        f'<path d="M40 -100 L20 60 M80 -100 L100 60" stroke="{CORAL}" stroke-width="14" stroke-linecap="round"/><path d="M40 -100 Q60 -150 80 -100" fill="none" stroke="{GREY}" stroke-width="12"/>'
                        f'<circle cx="160" cy="-40" r="42" fill="{GOLD}" stroke="{INK}" stroke-width="5"/><circle cx="160" cy="-40" r="16" fill="#E9D3AE" stroke="{INK}" stroke-width="4"/>'
                        f'<path d="M160 -220 V-185" stroke="{INK}" stroke-width="4"/><path d="M130 -160 Q160 -200 190 -160 Z" fill="{NAVY}" stroke="{INK}" stroke-width="4"/>'
                        f'<circle cx="160" cy="-150" r="14" fill="#FFE49A" stroke="{INK}" stroke-width="3"/>'))


def parcel(x, y, s=1.0, n=3, ret=False, **_):
    """A stack of n cardboard shipping boxes with tape (online orders). ret=True adds a coral U-turn arrow (a return coming back). (x, y) = centre of the bottom of the stack."""
    out = ""
    for k in range(int(n)):
        w = 220 - k * 30; hh = 120; yy = -hh * (k + 1); dx = (k % 2) * 18 - 9
        out += (f'<rect x="{-w / 2 + dx:.0f}" y="{yy}" width="{w}" height="{hh}" rx="6" fill="#D9A866" stroke="{INK}" stroke-width="{SW}"/>'
                f'<rect x="{-18 + dx:.0f}" y="{yy}" width="36" height="{hh}" fill="#F3D9A6" stroke="{INK}" stroke-width="3"/>'
                f'<rect x="{w / 2 - 70 + dx:.0f}" y="{yy + 70}" width="44" height="30" rx="3" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>')
    if ret:
        out += (f'<path d="M150 -300 Q260 -300 260 -190 Q260 -80 160 -80" fill="none" stroke="{CORAL}" stroke-width="16" stroke-linecap="round"/>'
                f'<path d="M190 -112 L150 -80 L190 -46" fill="none" stroke="{CORAL}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>')
    return _g(x, y, s, out)


def parcel_box(x, y, s=1.0, n=3, ret=False, **_):
    hh = 120 * int(n); W = 290 if ret else 140
    return [x - 130 * s, y - hh * s, (130 + W) * s, hh * s]


def network(x, y, s=1.0, n=6, r=220, color="blue", **_):
    """A network of n users (small people icons on a circle) with a line between every pair: the possible connections, n x (n - 1) / 2. color: blue or grey (a smaller rival). (x, y) = centre."""
    n = int(n); c = BLUE if color == "blue" else GREY; pts = [(r * math.sin(2 * math.pi * i / n), -r * math.cos(2 * math.pi * i / n)) for i in range(n)]
    lw = 5 if n <= 6 else 3 if n <= 12 else 1.6; op = 0.8 if n <= 6 else 0.55
    out = "".join(f'<path d="M{a[0]:.0f} {a[1]:.0f} L{b[0]:.0f} {b[1]:.0f}" stroke="{c}" stroke-width="{lw}" opacity="{op}"/>' for i, a in enumerate(pts) for b in pts[i + 1:])
    hr = max(10, min(34, 1.1 * r / max(n, 3)))
    for px, py in pts:
        out += (f'<path d="M{px - hr * 1.2:.0f} {py + hr * 1.5:.0f} Q{px:.0f} {py - hr * 0.2:.0f} {px + hr * 1.2:.0f} {py + hr * 1.5:.0f} Z" fill="{LB if color == "blue" else "#DDE1E7"}" stroke="{INK}" stroke-width="{max(2.5, hr / 7):.1f}"/>'
                f'<circle cx="{px:.0f}" cy="{py - hr * 0.2:.0f}" r="{hr * 0.62:.0f}" fill="{PAPER}" stroke="{INK}" stroke-width="{max(2.5, hr / 7):.1f}"/>')
    return _g(x, y, s, out)


def network_box(x, y, s=1.0, n=6, r=220, **_):
    hr = max(10, min(34, 1.1 * r / max(int(n), 3))); R = r + hr * 1.3
    return [x - R * s, y - (r + hr) * s, 2 * R * s, (2 * r + hr * 2.6) * s]


def school(x, y, s=1.0, roof="leak", **_):
    """A small school building with a pitched roof (charity project). roof: leak (a hole and rain drops coming through), build (scaffolding and a dashed new roof), new (a finished red roof with a green tick). (x, y) = centre of the ground under it."""
    out = (f'<rect x="-230" y="-300" width="460" height="300" fill="#F4ECDD" stroke="{INK}" stroke-width="{SW}"/>'
           + "".join(f'<rect x="{xx}" y="-230" width="80" height="80" rx="6" fill="{SKY}" stroke="{INK}" stroke-width="4"/><path d="M{xx + 40} -230 V-150 M{xx} -190 H{xx + 80}" stroke="{INK}" stroke-width="3"/>' for xx in (-190, 110))
           + f'<path d="M-45 0 V-130 Q0 -170 45 -130 V0" fill="{BLUE}" stroke="{INK}" stroke-width="5"/><circle cx="25" cy="-60" r="5" fill="{GOLD}"/>'
           f'<path d="M-30 -310 V-345 M-30 -345 L20 -335 L-30 -325" fill="{CORAL}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    tri = "M-270 -300 L0 -470 L270 -300 Z"
    if roof == "new":
        out += (f'<path d="{tri}" fill="{BRICK}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
                + "".join(f'<path d="M{-270 + k * 54} -300 L{-270 + k * 54 + (0 - (-270 + k * 54)) * 0.35:.0f} -360" stroke="{INK}" stroke-width="3" opacity="0.35"/>' for k in range(1, 10))
                + f'<circle cx="230" cy="-430" r="46" fill="{GREEN}" stroke="{INK}" stroke-width="5"/><path d="M208 -430 l16 18 l30 -36" fill="none" stroke="{WHITE}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    elif roof == "build":
        out += (f'<path d="{tri}" fill="none" stroke="{GREY}" stroke-width="6" stroke-dasharray="18 12" stroke-linejoin="round"/>'
                f'<path d="M-300 0 V-330 M-250 0 V-330 M250 0 V-330 M300 0 V-330 M-300 -110 H-250 M-300 -220 H-250 M250 -110 H300 M250 -220 H300 M-300 -330 H300" stroke="{GOLD}" stroke-width="8" stroke-linecap="round"/>'
                f'<path d="M-270 -300 L-90 -413" stroke="{BRICK}" stroke-width="22" stroke-linecap="round"/>')
    else:
        out += (f'<path d="{tri}" fill="{BRICK}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
                f'<path d="M30 -420 L70 -400 L50 -370 L90 -350 L40 -340 Z" fill="{INK}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                + "".join(f'<path d="M{xx} {yy} q-9 16 0 22 q9 -6 0 -22 Z" fill="{BLUE}" stroke="{INK}" stroke-width="2.5"/>' for xx, yy in ((60, -300), (40, -250), (75, -220), (50, -180))))
    return _g(x, y, s, out)


def school_box(x, y, s=1.0, **_):
    return [x - 305 * s, y - 478 * s, 610 * s, 480 * s]


def money_jar(x, y, s=1.0, n=4, lock=False, tag="", **_):
    """A glass jar of n banknotes and coins. lock=True: a padlock and a ribbon on the lid (money the donor restricted to one use). tag: a short label on a hanging tag (e.g. "Roof"), optional. (x, y) = centre."""
    import html as _h
    out = (f'<path d="M-100 -110 Q-110 -110 -110 -90 V120 Q-110 150 -80 150 H80 Q110 150 110 120 V-90 Q110 -110 100 -110 Z" fill="{SKY}" fill-opacity="0.7" stroke="{INK}" stroke-width="{SW}"/>')
    for k in range(int(n)):
        yy = 120 - k * 40
        out += f'<rect x="{-70 + (k % 2) * 16}" y="{yy - 26}" width="124" height="44" rx="6" fill="{GREEN}" stroke="{INK}" stroke-width="4" transform="rotate({(-6 if k % 2 else 5)} 0 {yy})"/>'
    out += (f'<ellipse cx="40" cy="128" rx="28" ry="10" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M-80 -90 V100" stroke="{WHITE}" stroke-width="8" stroke-linecap="round" opacity="0.7"/>'
            f'<rect x="-116" y="-150" width="232" height="44" rx="10" fill="{NAVY if lock else GREY}" stroke="{INK}" stroke-width="{SW}"/>')
    if lock:
        out += (f'<path d="M-10 -128 V60 M10 -128 V60" stroke="{CORAL}" stroke-width="10" opacity="0.9"/>'
                f'<path d="M-26 -10 V-36 a26 26 0 0 1 52 0 V-10" fill="none" stroke="{INK}" stroke-width="9"/>'
                f'<rect x="-40" y="-14" width="80" height="64" rx="10" fill="{GOLD}" stroke="{INK}" stroke-width="5"/><circle cx="0" cy="12" r="8" fill="{INK}"/>')
    if tag:
        out += (f'<path d="M100 -128 Q150 -110 150 -60" fill="none" stroke="{INK}" stroke-width="3"/>'
                f'<rect x="110" y="-60" width="{max(80, len(tag) * 24 + 30)}" height="56" rx="8" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>'
                f'<text x="{110 + max(80, len(tag) * 24 + 30) / 2:.0f}" y="-20" text-anchor="middle" font-family="Inter,sans-serif" font-weight="900" font-size="34" fill="{INK}">{_h.escape(tag)}</text>')
    return _g(x, y, s, out)


def money_jar_box(x, y, s=1.0, tag="", **_):
    W = 232 + (max(80, len(tag) * 24 + 30) + 2 if tag else 0)
    return [x - 118 * s, y - 152 * s, W * s, 305 * s]


def gas_station(x, y, s=1.0, price="", color="blue", **_):
    """A small gas station (no brand): a canopy on two posts over one pump, and a pole sign with the price per gallon (price, e.g. "$4.20"; the one number shown in the art). color: blue or coral canopy (two rival stations). (x, y) = centre of the ground under it."""
    import html as _h
    c = BLUE if color == "blue" else CORAL
    out = (f'<rect x="-250" y="-470" width="440" height="60" rx="10" fill="{c}" stroke="{INK}" stroke-width="{SW}"/>'
           f'<path d="M-250 -420 H190" stroke="{WHITE}" stroke-width="6" opacity="0.7"/>'
           f'<path d="M-200 -410 V0 M140 -410 V0" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>'
           f'<rect x="-80" y="-230" width="110" height="230" rx="12" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/>'
           f'<rect x="-62" y="-208" width="74" height="50" rx="6" fill="#DCEFD8" stroke="{INK}" stroke-width="4"/>'
           f'<path d="M30 -150 Q70 -150 70 -100 V-40 Q70 -20 90 -20" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
           f'<rect x="-60" y="-130" width="70" height="20" rx="4" fill="{c}" stroke="{INK}" stroke-width="3"/>'
           f'<path d="M260 0 V-300" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
           f'<rect x="180" y="-440" width="170" height="150" rx="14" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/>'
           f'<rect x="180" y="-440" width="170" height="40" rx="12" fill="{c}" stroke="{INK}" stroke-width="5"/>'
           f'<path d="M248 -428 q17 -0 17 14 q0 10 -17 10 q-17 0 -17 -10 q0 -14 17 -14 z" fill="{WHITE}" opacity="0.9"/>')
    if price:
        out += f'<text x="265" y="-322" text-anchor="middle" font-family="Inter,sans-serif" font-weight="900" font-size="{54 if len(price) <= 5 else 44}" fill="{INK}">{_h.escape(price)}</text>'
    return _g(x, y, s, out)


def gas_station_box(x, y, s=1.0, **_):
    return [x - 256 * s, y - 476 * s, 612 * s, 480 * s]


def payoff_grid(x, y, s=1.0, w=860, ch=230, circle=True, title="Profit a day", a="Station A", b="Station B", cells=None, **_):
    """Game theory summary picture (the one place with words in the art): a hand-drawn 2 x 2 payoff grid. Rows are A's price (High, Low), columns B's price (High, Low); ch = cell height (230; 300 fills a full-frame scene); each cell shows A's profit (blue) and B's profit (coral). circle=True circles the both-low cell in red. cells: [[aHH, bHH], [aHL, bHL], [aLH, bLH], [aLL, bLL]] as strings. (x, y) = centre."""
    import html as _h
    e = _h.escape
    cells = cells or [["$2,000", "$2,000"], ["$600", "$2,600"], ["$2,600", "$600"], ["$1,200", "$1,200"]]
    lw = 220; cw = (w - lw) / 2; ch = float(ch); top = -330; gx = -w / 2 + lw
    T = lambda t, xx, yy, fs, col=INK, wt=900, anc="middle": f'<text x="{xx:.0f}" y="{yy:.0f}" text-anchor="{anc}" font-family="Inter,sans-serif" font-weight="{wt}" font-size="{fs:.0f}" fill="{col}">{e(str(t))}</text>'
    out = T(title, gx + cw, top - 92, 58)
    out += T(f"{b}'s price", gx + cw, top - 32, 38, CORAL, 800) + T("High", gx + cw / 2, top + 18, 42, CORAL) + T("Low", gx + cw * 1.5, top + 18, 42, CORAL)
    g0 = top + 40
    out += f'<text transform="translate({-w / 2 + 30:.0f} {g0 + ch:.0f}) rotate(-90)" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" font-size="38" fill="{BLUE}">{e(a)}\'s price</text>'
    out += T("High", -w / 2 + 140, g0 + ch / 2 + 14, 42, BLUE) + T("Low", -w / 2 + 140, g0 + ch * 1.5 + 14, 42, BLUE)
    out += f'<rect x="{gx:.0f}" y="{g0:.0f}" width="{2 * cw:.0f}" height="{2 * ch:.0f}" rx="16" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/>'
    out += f'<path d="M{gx + cw:.0f} {g0:.0f} q4 {ch:.0f} 0 {2 * ch:.0f} M{gx:.0f} {g0 + ch:.0f} q{cw:.0f} -4 {2 * cw:.0f} 0" fill="none" stroke="{INK}" stroke-width="5"/>'
    for i, (va, vb) in enumerate(cells):
        r, c = divmod(i, 2); cx = gx + cw * (c + 0.5); cy = g0 + ch * (r + 0.5)
        fs = min(64 * max(1.0, ch / 230), cw * 0.86 / max(1, max(len(va), len(vb)) * 0.66))
        out += T(va, cx, cy - 8, fs, BLUE) + T(vb, cx, cy + fs + 4, fs, CORAL)
    if circle:
        cx = gx + cw * 1.5; cy = g0 + ch * 1.5 + 14; rx = cw * 0.44; ry = ch * 0.4
        out += f'<path d="M{cx - rx:.0f} {cy - 10:.0f} Q{cx - rx:.0f} {cy - ry:.0f} {cx:.0f} {cy - ry:.0f} Q{cx + rx * 1.04:.0f} {cy - ry * 0.98:.0f} {cx + rx:.0f} {cy:.0f} Q{cx + rx * 0.98:.0f} {cy + ry:.0f} {cx:.0f} {cy + ry * 0.98:.0f} Q{cx - rx * 1.04:.0f} {cy + ry * 0.95:.0f} {cx - rx * 0.95:.0f} {cy - ry * 0.25:.0f}" fill="none" stroke="#D64545" stroke-width="9" stroke-linecap="round"/>'
    return _g(x, y, s, out)


def payoff_grid_box(x, y, s=1.0, w=860, ch=230, **_):
    return [x - w / 2 * s, y - 430 * s, w * s, (140 + 2 * float(ch)) * s]


# ---------------------------------------------------------------- FA1 course cast and lesson diagram props (in-lesson videos, 5 Nov 2026)
# Plot and Tempo are EdCharacter cast members (geometry from tutoring-web/public/mascot/plot.svg and tempo.svg, 240x270 units,
# the same frame, legs, arms and hands as Ledger). No-suit design: no collar and no tie (tutoring-content mascot skill, "The cast").
# Identity kept in every pose: the face-screen with its instrument (Plot: the bar chart; Tempo: the hourglass), the brand
# colours and the eyes. Moods and arms change the expression only.
CAST_MOODS = ["smile", "happy", "focused", "surprised", "worried", "thinking", "sigh"]
SAND = "#EAF2FF"; BAR_GREY = "#94A3B8"


def _cast_face(mood, ey, er, my, msw, gaze=None):
    """Eyes, brows, mouth and effect marks for a cast face. ey/er: eye centre y and radius; my: mouth line y; msw: mouth stroke."""
    gx, gy, _ = GAZES.get(gaze, (0, 0, 0))
    mouth = f'<path d="M106 {my} Q120 {my + 12} 134 {my}" fill="none" stroke="{INK}" stroke-width="{msw}" stroke-linecap="round"/>'
    eyes = "".join(f'<circle cx="{cx + gx}" cy="{ey + gy}" r="{er}" fill="{INK}"/><circle cx="{cx + gx + er * 0.34:.1f}" cy="{ey + gy - er * 0.34:.1f}" r="{er * 0.3:.1f}" fill="{WHITE}"/>' for cx in (102, 138))
    brows = extra = ""
    if mood == "happy":
        eyes = "".join(f'<path d="M{cx - 7} {ey + 2} Q{cx} {ey - 7} {cx + 7} {ey + 2}" fill="none" stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/>' for cx in (102, 138))
        mouth = f'<path d="M104 {my - 2} Q120 {my + 16} 136 {my - 2}" fill="none" stroke="{INK}" stroke-width="{msw}" stroke-linecap="round"/>'
    elif mood == "focused":
        brows = f'<path d="M93 {ey - 15.5} L110 {ey - 10.5} M147 {ey - 15.5} L130 {ey - 10.5}" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
        mouth = f'<path d="M108 {my + 1} L132 {my + 1}" stroke="{INK}" stroke-width="{msw}" stroke-linecap="round"/>'
    elif mood == "surprised":
        R = er * 1.5
        eyes = "".join(f'<circle cx="{cx}" cy="{ey}" r="{R:.1f}" fill="{WHITE}" stroke="{INK}" stroke-width="2.5"/><circle cx="{cx + gx * 0.5:.1f}" cy="{ey + 1}" r="{er * 0.7:.1f}" fill="{INK}"/>' for cx in (102, 138))
        mouth = f'<ellipse cx="120" cy="{my + 3}" rx="5" ry="6.5" fill="{INK}"/>'
        extra = f'<path d="M176 6 L172 30" stroke="{BLUE}" stroke-width="6" stroke-linecap="round"/><circle cx="170.5" cy="40" r="3.6" fill="{BLUE}"/>'
    elif mood == "worried":
        brows = f'<path d="M93 {ey - 10} L109 {ey - 16} M147 {ey - 10} L131 {ey - 16}" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
        mouth = f'<path d="M108 {my + 4} Q114 {my - 1} 120 {my + 3} Q126 {my + 7} 132 {my + 2}" fill="none" stroke="{INK}" stroke-width="{msw}" stroke-linecap="round"/>'
        extra = f'<path d="M172 40 q8 14 0 20 q-8 -6 0 -20 z" fill="{LB}" stroke="{INK}" stroke-width="2.5"/>'
    elif mood == "thinking":
        brows = f'<path d="M94 {ey - 11} q8 -4 16 0 M130 {ey - 11} q8 -4 16 0" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        mouth = f'<path d="M110 {my + 1} q11 -5 20 2" fill="none" stroke="{INK}" stroke-width="{msw}" stroke-linecap="round"/>'
        extra = (f'<circle cx="152" cy="30" r="3.5" fill="{BLUE}" opacity="0.5"/><circle cx="163" cy="17" r="5" fill="{BLUE}" opacity="0.7"/>'
                 f'<circle cx="178" cy="2" r="7" fill="{BLUE}"/>')
    elif mood == "sigh":   # eyes closed downwards, a small frown, a breath puff (a tired sigh)
        eyes = "".join(f'<path d="M{cx - 8} {ey - 1} Q{cx} {ey + 6} {cx + 8} {ey - 1}" fill="none" stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/>' for cx in (102, 138))
        brows = f'<path d="M93 {ey - 10} L109 {ey - 15} M147 {ey - 10} L131 {ey - 15}" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
        mouth = f'<path d="M110 {my + 6} Q120 {my - 1} 130 {my + 6}" fill="none" stroke="{INK}" stroke-width="{msw}" stroke-linecap="round"/>'
        extra = f'<path d="M150 {my + 4} q18 -6 26 4 q8 10 22 2" fill="none" stroke="{GREY}" stroke-width="3.5" stroke-linecap="round"/>'
    return eyes + brows + mouth + extra


def _cast(body_fn, x, y, s, mood, arm, flip, tilt, larm, gaze, **_):
    pose = ARM_POSES.get(arm, ARM_POSES["down"])
    right = _arm(*pose["R"]); left = _arm(*pose.get("L", ARM_POSES["down"]["L"]))
    if larm and larm != "down":
        left = _arm(*ARM_POSES.get(larm, ARM_POSES["down"]).get("L", ARM_POSES["down"]["L"]))
    prop = ""
    if arm == "phone":   # the same small phone Ledger holds
        prop = (f'<g transform="rotate(-14 200 92)"><rect x="185" y="60" width="30" height="58" rx="8" fill="{NAVY}" stroke="{INK}" stroke-width="3"/>'
                f'<rect x="190" y="68" width="20" height="38" rx="3" fill="{LB}"/></g>')
    legs = (f'<ellipse cx="120" cy="236" rx="46" ry="7" fill="{INK}" opacity="0.10"/>'
            f'<line x1="102" y1="186" x2="102" y2="210" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
            f'<line x1="138" y1="186" x2="138" y2="210" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
            f'<rect x="88" y="208" width="29" height="14" rx="7" fill="{INK}"/><rect x="123" y="208" width="29" height="14" rx="7" fill="{INK}"/>')
    fl = " scale(-1 1) translate(-240 0)" if flip else ""
    return (f'<g transform="translate({_f(x)} {_f(y)}) scale({s}) translate(-120 -230){fl}">'
            f'{legs}<g transform="rotate({tilt} 120 198)">{left}{body_fn(mood, gaze)}{prop}{right}</g></g>')


def plot(x, y, s=1.0, mood="smile", arm="down", flip=False, tilt=0, larm=None, gaze=None, **_):
    """FA1 cast: Plot, the bar-chart character (owns the clothes store in FA1 unit 2). No collar or tie. (x, y) = between the feet, same size as Ledger. mood: smile, happy, focused, surprised, worried, thinking, sigh. arm/larm: Ledger's arm poses (down, point, up, both_up, phone, shrug, wave, hold...). flip, tilt, gaze as Ledger."""
    def body(mood, gaze):
        return (f'<rect x="52" y="42" width="136" height="150" rx="16" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'
                f'<line x1="66" y1="176" x2="174" y2="176" stroke="{INK}" stroke-width="2.5" opacity="0.4"/>'
                f'<rect x="72" y="150" width="24" height="26" rx="4" fill="{BAR_GREY}"/><rect x="104" y="132" width="24" height="44" rx="4" fill="{BAR_GREY}"/>'
                f'<rect x="136" y="116" width="24" height="60" rx="4" fill="{BLUE}"/>' + _cast_face(mood, 80, 7.5, 100, 4.5, gaze))
    return _cast(body, x, y, s, mood, arm, flip, tilt, larm, gaze)


def tempo(x, y, s=1.0, mood="smile", arm="down", flip=False, tilt=0, larm=None, gaze=None, **_):
    """FA1 cast: Tempo, the hourglass character (works at the till in FA1 unit 2). No collar or tie. (x, y) = between the feet, same size as Ledger. mood: smile, happy, focused, surprised, worried, thinking, sigh. arm/larm: Ledger's arm poses. flip, tilt, gaze as Ledger."""
    def body(mood, gaze):
        return (f'<line x1="74" y1="52" x2="74" y2="182" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
                f'<line x1="166" y1="52" x2="166" y2="182" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
                f'<rect x="62" y="44" width="116" height="12" rx="5" fill="{INK}"/><rect x="62" y="180" width="116" height="12" rx="5" fill="{INK}"/>'
                f'<path d="M76 58 L164 58 L120 119 Z" fill="{SAND}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                f'<path d="M120 121 L164 178 L76 178 Z" fill="{SAND}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                f'<path d="M104 102 L136 102 L120 119 Z" fill="{BLUE}"/><path d="M120 121 L121 150 L119 150 Z" fill="{BLUE}"/>'
                f'<path d="M86 178 L154 178 L120 150 Z" fill="{BLUE}"/>' + _cast_face(mood, 78, 6, 90, 3.5, gaze))
    return _cast(body, x, y, s, mood, arm, flip, tilt, larm, gaze)


def till(x, y, s=1.0, w=420, **_):
    """A shop counter with a cash register (the till). Put the character behind it BEFORE it in the item list, so the counter hides the legs. (x, y) = centre of the floor line under the counter. w = counter width."""
    h = 170; x0 = -w / 2
    return _g(x, y, s, (f'<rect x="{x0:.0f}" y="{-h}" width="{w}" height="{h}" rx="8" fill="#E3D2B5" stroke="{INK}" stroke-width="{SW}"/>'
                        f'<rect x="{x0 - 14:.0f}" y="{-h - 18}" width="{w + 28}" height="22" rx="8" fill="#C9AE84" stroke="{INK}" stroke-width="5"/>'
                        f'<path d="M{x0 + 30:.0f} {-h + 60} H{-x0 - 30:.0f} M{x0 + 30:.0f} {-h + 110} H{-x0 - 30:.0f}" stroke="{INK}" stroke-width="3" opacity="0.3"/>'
                        # register on the right of the counter top
                        f'<path d="M{-x0 - 190:.0f} {-h - 18} L{-x0 - 175:.0f} {-h - 120} H{-x0 - 30:.0f} L{-x0 - 15:.0f} {-h - 18} Z" fill="{NAVY}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                        f'<rect x="{-x0 - 150:.0f}" y="{-h - 190}" width="96" height="58" rx="6" fill="{NAVY}" stroke="{INK}" stroke-width="5"/>'
                        f'<rect x="{-x0 - 140:.0f}" y="{-h - 180}" width="76" height="38" rx="4" fill="#DCEFD8"/>'
                        f'<path d="M{-x0 - 102:.0f} {-h - 132} V{-h - 120}" stroke="{INK}" stroke-width="10"/>'
                        + "".join(f'<rect x="{-x0 - 160 + c * 36:.0f}" y="{-h - 100 + r * 26}" width="26" height="16" rx="4" fill="{WHITE if c < 3 else GOLD}"/>' for r in range(3) for c in range(4))))


def till_box(x, y, s=1.0, w=420, **_):
    return [x - (w / 2 + 16) * s, y - 360 * s, (w + 32) * s, 362 * s]


_COL = {"blue": BLUE, "green": GREEN, "coral": "#D0675E", "grey": "#7C8698", "ink": INK, "gold": GOLD}


def _label_dims(title, amount, note, fs, w):
    ft, fa, fn = fs * 0.82, fs * 1.2, fs * 0.6
    tl = [z for z in str(title).split("/")] if title else []
    tw = max(max((_tw(z, ft, 0.56) for z in tl), default=0), _tw(amount, fa, 0.6) if amount else 0, _tw(note, fn, 0.56) if note else 0)
    W = max(w or 0, tw + 64, 160)
    H = 34 + ((ft + 6) * len(tl) + 6 if title else 0) + (fa + 8 if amount else 0) + (fn + 10 if note else 0)
    return W, H, ft, fa, fn


def label(x, y, s=1.0, title="", amount="", note="", color="blue", w=0, fs=44, faded=False, strike=False, fill=None, **_):
    """Lesson label card (in-lesson videos; words allowed, like flow_box): a hand-drawn white card with a bold title, a big coloured amount (e.g. "$30,000") and an optional small note; "/" in the title breaks it into lines. Any line may be empty, so it also makes a title card or a tag. color: blue, green, coral, grey, ink, gold. fs = base font size. w = minimum width. faded=True: grey dashed card (set aside). strike=True: a coral line through it. fill: card colour. (x, y) = centre."""
    import html as _h
    W, H, ft, fa, fn = _label_dims(title, amount, note, fs, w)
    col = _COL.get(color, BLUE); stroke = GREY if faded else INK
    out = (f'<rect x="{-W / 2:.0f}" y="{-H / 2:.0f}" width="{W:.0f}" height="{H:.0f}" rx="22" fill="{fill or WHITE}" stroke="{stroke}" stroke-width="5"'
           + (' stroke-dasharray="16 12"' if faded else "") + '/>')
    yy = -H / 2 + 22
    tcol = GREY if faded else INK; acol = GREY if faded else col
    if title:
        for z in str(title).split("/"):
            yy += ft; out += f'<text x="0" y="{yy:.0f}" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" font-size="{ft:.0f}" fill="{tcol}">{_h.escape(z)}</text>'; yy += 6
        yy += 6
    if amount:
        yy += fa * 0.92; out += f'<text x="0" y="{yy:.0f}" text-anchor="middle" font-family="Inter,sans-serif" font-weight="900" font-size="{fa:.0f}" fill="{acol}">{_h.escape(amount)}</text>'; yy += 16
    if note:
        yy += fn; out += f'<text x="0" y="{yy:.0f}" text-anchor="middle" font-family="Inter,sans-serif" font-weight="700" font-size="{fn:.0f}" fill="#4B5568">{_h.escape(note)}</text>'
    if strike:
        out += f'<path d="M{-W / 2 - 10:.0f} {H / 4:.0f} L{W / 2 + 10:.0f} {-H / 4:.0f}" stroke="{CORAL}" stroke-width="9" stroke-linecap="round"/>'
    return _g(x, y, s, out)


def label_box(x, y, s=1.0, title="", amount="", note="", fs=44, w=0, **_):
    W, H, *_r = _label_dims(title, amount, note, fs, w)
    return [x - W / 2 * s - 4, y - H / 2 * s - 4, W * s + 8, H * s + 8]


def _icon(kind):
    """Small hand-drawn icons (about 110 units across, centred) for icon_tile."""
    if kind == "bags":
        return (f'<path d="M-30 -30 q0 -26 16 -26 q16 0 16 26" fill="none" stroke="{INK}" stroke-width="4"/><rect x="-50" y="-30" width="58" height="76" rx="6" fill="{BLUE}" stroke="{INK}" stroke-width="4"/>'
                f'<path d="M18 -18 q0 -24 14 -24 q14 0 14 24" fill="none" stroke="{INK}" stroke-width="4"/><rect x="2" y="-18" width="54" height="64" rx="6" fill="{CORAL}" stroke="{INK}" stroke-width="4"/>')
    if kind == "key":
        return (f'<circle cx="-26" cy="0" r="22" fill="{GOLD}" stroke="{INK}" stroke-width="5"/><circle cx="-26" cy="0" r="8" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>'
                f'<path d="M-4 0 H52 M36 0 V16 M48 0 V12" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>')
    if kind == "shield":
        return (f'<path d="M0 -50 L42 -34 V0 Q42 34 0 52 Q-42 34 -42 0 V-34 Z" fill="{LB}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                f'<path d="M-16 0 L-4 14 L18 -14" fill="none" stroke="{BLUE}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == "invoice":
        return (f'<path d="M-36 -50 H24 L38 -36 V50 H-36 Z" fill="{WHITE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                + "".join(f'<path d="M-24 {yy} H{20 if k % 2 else 26}" stroke="{GREY}" stroke-width="5" stroke-linecap="round"/>' for k, yy in enumerate((-28, -12, 4, 20)))
                + f'<path d="M0 36 H26" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
    if kind == "box":
        return (f'<path d="M-50 -20 L0 -42 L50 -20 L0 2 Z" fill="#E7C893" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                f'<path d="M-50 -20 V30 L0 52 V2 Z" fill="#D9B27C" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                f'<path d="M50 -20 V30 L0 52 V2 Z" fill="#C99C62" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                f'<path d="M-25 -31 L25 -9" stroke="{WHITE}" stroke-width="6" opacity="0.8"/>')
    if kind == "poster":   # advertising: a megaphone
        return (f'<path d="M-40 -14 L22 -44 V44 L-40 14 Z" fill="{CORAL}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                f'<rect x="-54" y="-16" width="16" height="32" rx="5" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>'
                f'<path d="M-28 14 L-20 40 H-6 L-12 18" fill="{WHITE}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                f'<path d="M34 -24 L50 -34 M36 0 H54 M34 24 L50 34" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    if kind == "mirror":
        return "".join(f'<ellipse cx="{cx}" cy="-8" rx="20" ry="40" fill="{SKY}" stroke="{INK}" stroke-width="4"/><path d="M{cx - 8} -30 L{cx + 4} -42" stroke="{WHITE}" stroke-width="5" stroke-linecap="round"/>'
                       f'<path d="M{cx} 32 V50 M{cx - 14} 52 H{cx + 14}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>' for cx in (-26, 26))
    if kind == "bank":
        return (f'<path d="M-52 -18 L0 -50 L52 -18 Z" fill="{LB}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                + "".join(f'<rect x="{cx - 6}" y="-14" width="12" height="50" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>' for cx in (-36, -12, 12, 36))
                + f'<rect x="-56" y="36" width="112" height="12" rx="3" fill="{LB}" stroke="{INK}" stroke-width="4"/>')
    if kind == "wallet":
        return (f'<rect x="-50" y="-34" width="100" height="72" rx="12" fill="#8B5E3C" stroke="{INK}" stroke-width="5"/>'
                f'<path d="M-50 -14 H50" stroke="{INK}" stroke-width="3" opacity="0.5"/><rect x="14" y="-6" width="40" height="26" rx="8" fill="#A9774F" stroke="{INK}" stroke-width="4"/>'
                f'<circle cx="28" cy="7" r="4" fill="{GOLD}"/><rect x="-38" y="-46" width="54" height="22" rx="3" fill="#BFE0C5" stroke="{INK}" stroke-width="3"/>')
    if kind == "payslip":
        return (f'<rect x="-38" y="-50" width="76" height="100" rx="6" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>'
                f'<rect x="-38" y="-50" width="76" height="22" rx="6" fill="{GREEN}" stroke="{INK}" stroke-width="5"/>'
                + "".join(f'<path d="M-24 {yy} H{14 if k % 2 else 24}" stroke="{GREY}" stroke-width="5" stroke-linecap="round"/>' for k, yy in enumerate((-12, 4, 20)))
                + f'<path d="M-4 36 H24" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
    if kind == "percent":
        return (f'<circle cx="0" cy="0" r="50" fill="{LB}" stroke="{INK}" stroke-width="5"/>'
                f'<circle cx="-16" cy="-16" r="10" fill="none" stroke="{INK}" stroke-width="6"/><circle cx="16" cy="16" r="10" fill="none" stroke="{INK}" stroke-width="6"/>'
                f'<path d="M22 -26 L-22 26" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
    if kind == "bulb":
        return (f'<path d="M0 -50 Q34 -50 34 -16 Q34 4 18 18 V28 H-18 V18 Q-34 4 -34 -16 Q-34 -50 0 -50 Z" fill="#FFE08A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                f'<rect x="-16" y="28" width="32" height="18" rx="4" fill="{GREY}" stroke="{INK}" stroke-width="4"/><path d="M-8 -6 L0 6 L8 -6" fill="none" stroke="{INK}" stroke-width="3"/>')
    if kind == "shelf":   # a slightly worn shelf: scuffs and a dashed crack
        return (f'<path d="M-52 -40 V48 M52 -40 V48" stroke="#8B5E3C" stroke-width="8" stroke-linecap="round"/>'
                f'<rect x="-56" y="-14" width="112" height="14" rx="3" fill="#C99C62" stroke="{INK}" stroke-width="4"/><rect x="-56" y="26" width="112" height="14" rx="3" fill="#C99C62" stroke="{INK}" stroke-width="4"/>'
                f'<path d="M-20 -14 L-8 0 L4 -14" fill="none" stroke="{INK}" stroke-width="3" stroke-dasharray="5 4"/><path d="M18 30 l10 6 M30 28 l8 6" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
                f'<rect x="-40" y="-40" width="26" height="26" rx="3" fill="{BLUE}" stroke="{INK}" stroke-width="3"/><rect x="10" y="-36" width="30" height="22" rx="3" fill="{CORAL}" stroke="{INK}" stroke-width="3"/>')
    if kind == "jacket":
        return (f'<path d="M-20 -46 L-50 -30 L-56 20 L-38 22 L-36 48 H36 L38 22 L56 20 L50 -30 L20 -46 Q0 -32 -20 -46 Z" fill="{BLUE}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                f'<path d="M0 -36 V48" stroke="{INK}" stroke-width="3"/>')
    return f'<circle cx="0" cy="0" r="40" fill="{LB}" stroke="{INK}" stroke-width="5"/>'


ICONS = ["bags", "key", "shield", "invoice", "box", "poster", "mirror", "bank", "wallet", "payslip", "percent", "bulb", "shelf", "jacket"]


def icon_tile(x, y, s=1.0, icon="key", amount="", note="", color="ink", w=200, **_):
    """Lesson tile: a small hand-drawn icon over an amount (e.g. "$2,500") and a short note (e.g. "rent"; "/" splits it into two lines). icon: bags, key (rent), shield (insurance), invoice, box (stock), poster (a megaphone: advertising), mirror, bank, wallet, payslip (wages), percent (interest), bulb (electricity), shelf (wear), jacket. color: the amount colour. (x, y) = centre; the tile is w x 230."""
    import html as _h
    h = 230; col = _COL.get(color, INK)
    fa = min(44, (w - 24) / max(1, len(amount) * 0.6)); fn = min(28, (w - 20) / max(1, len(str(note)) * 0.55))
    out = (f'<rect x="{-w / 2:.0f}" y="{-h / 2}" width="{w}" height="{h}" rx="20" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>'
           f'<g transform="translate(0 -46) scale(0.95)">{_icon(icon)}</g>')
    if amount: out += f'<text x="0" y="{58}" text-anchor="middle" font-family="Inter,sans-serif" font-weight="900" font-size="{fa:.0f}" fill="{col}">{_h.escape(amount)}</text>'
    nl = [z.strip() for z in str(note).split("/") if z.strip()]
    if len(nl) > 1: fn = min(23, min((w - 20) / max(1, len(z) * 0.55) for z in nl))
    for j, z in enumerate(nl): out += f'<text x="0" y="{(96 if len(nl) == 1 else 88 + j * 26)}" text-anchor="middle" font-family="Inter,sans-serif" font-weight="700" font-size="{fn:.0f}" fill="#4B5568">{_h.escape(z)}</text>'
    return _g(x, y, s, out)


def icon_tile_box(x, y, s=1.0, w=200, **_):
    return [x - w / 2 * s - 4, y - 119 * s, w * s + 8, 238 * s]


def big_icon(x, y, s=1.0, icon="key", **_):
    """One of the icon_tile icons drawn on its own, without the tile (s 2-3 for a prop). (x, y) = centre."""
    return _g(x, y, s, _icon(icon))


def months(x, y, s=1.0, used=1, total=12, **_):
    """A year as 12 month boxes in two rows (insurance paid ahead): the first `used` are coral with a tick (used up), the rest light blue (still to come). (x, y) = centre."""
    out = f'<rect x="-230" y="-100" width="460" height="200" rx="18" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>'
    for k in range(int(total)):
        cx, cy = -175 + (k % 6) * 70, -40 + (k // 6) * 80
        u = k < int(used)
        out += f'<rect x="{cx - 28}" y="{cy - 28}" width="56" height="56" rx="8" fill="{CORAL if u else LB}" stroke="{INK}" stroke-width="3.5"/>'
        if u: out += f'<path d="M{cx - 13} {cy} L{cx - 3} {cy + 11} L{cx + 14} {cy - 11}" fill="none" stroke="{WHITE}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
    return _g(x, y, s, out)


def block(x, y, s=1.0, w=420, h=120, title="", amount="", color="blue", faded=False, **_):
    """A bar piece for stacked bars, trays and running sums (lessons): a hand-drawn filled rectangle with its title and amount inside (one line when h < 110, else two). color: blue, green, coral, gold, grey, light, white. faded=True: dashed grey outline (set aside). (x, y) = centre."""
    import html as _h
    fills = {"blue": (BLUE, WHITE), "green": (GREEN, WHITE), "coral": (CORAL, INK), "gold": ("#F3D9A6", INK), "grey": ("#CBD2DC", INK), "light": (LB, INK), "white": (WHITE, INK)}
    fc, tc = fills.get(color, fills["blue"])
    if faded: fc, tc = "none", GREY
    out = (f'<rect x="{-w / 2:.0f}" y="{-h / 2:.0f}" width="{w}" height="{h}" rx="14" fill="{fc}" stroke="{GREY if faded else INK}" stroke-width="5"'
           + (' stroke-dasharray="16 12"' if faded else "") + '/>')
    if h < 110:
        line = (title + "  " + amount).strip()
        f = min(h * 0.5, 46, (w - 30) / max(1, len(line) * 0.57))
        out += f'<text x="0" y="{f * 0.36:.0f}" text-anchor="middle" font-family="Inter,sans-serif" font-weight="900" font-size="{f:.0f}" fill="{tc}">{_h.escape(line)}</text>'
    else:
        ft = min(40, (w - 30) / max(1, len(title) * 0.56)); fa = min(58, h * 0.4, (w - 30) / max(1, len(amount) * 0.6))
        gap = (h - ft - fa) / 3
        if title: out += f'<text x="0" y="{-h / 2 + gap + ft * 0.8:.0f}" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" font-size="{ft:.0f}" fill="{tc}">{_h.escape(title)}</text>'
        if amount: out += f'<text x="0" y="{h / 2 - gap - fa * 0.12:.0f}" text-anchor="middle" font-family="Inter,sans-serif" font-weight="900" font-size="{fa:.0f}" fill="{tc}">{_h.escape(amount)}</text>'
    return _g(x, y, s, out)


def block_box(x, y, s=1.0, w=420, h=120, **_):
    return [x - w / 2 * s - 4, y - h / 2 * s - 4, w * s + 8, h * s + 8]


def t_account(x, y, s=1.0, title="Cash", left="", right="", w=420, move="", **_):
    """A hand-drawn T-account: the account name over the T, Dr and Cr heads, one amount on the debit (left) and/or credit (right) side. move: "up" (green arrow) or "down" (coral arrow) beside the name. (x, y) = centre of the T's cross bar."""
    import html as _h
    out = (f'<text x="0" y="-40" text-anchor="middle" font-family="Inter,sans-serif" font-weight="900" font-size="50" fill="{INK}">{_h.escape(title)}</text>'
           f'<path d="{_wobble_line(-w / 2, w / 2, 0, 3)}" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
           f'<path d="M0 0 Q3 110 -1 230" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
           f'<text x="{-w / 4:.0f}" y="46" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" font-size="34" fill="#7C8698">Dr</text>'
           f'<text x="{w / 4:.0f}" y="46" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" font-size="34" fill="#7C8698">Cr</text>')
    if left: out += f'<text x="{-w / 4:.0f}" y="130" text-anchor="middle" font-family="Inter,sans-serif" font-weight="900" font-size="58" fill="{BLUE}">{_h.escape(left)}</text>'
    if right: out += f'<text x="{w / 4:.0f}" y="130" text-anchor="middle" font-family="Inter,sans-serif" font-weight="900" font-size="58" fill="{BLUE}">{_h.escape(right)}</text>'
    tx = _tw(title, 50, 0.6) / 2 + 40
    if move == "down":
        out += f'<path d="M{tx:.0f} -88 V-30 M{tx - 16:.0f} -48 L{tx:.0f} -28 L{tx + 16:.0f} -48" fill="none" stroke="{CORAL}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
    elif move == "up":
        out += f'<path d="M{tx:.0f} -28 V-86 M{tx - 16:.0f} -68 L{tx:.0f} -88 L{tx + 16:.0f} -68" fill="none" stroke="{GREEN}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
    return _g(x, y, s, out)


def t_account_box(x, y, s=1.0, title="Cash", w=420, **_):
    ww = max(w, _tw(title, 50, 0.6) + 120)
    return [x - ww / 2 * s, y - 95 * s, ww * s, 330 * s]


def letter_tiles(x, y, s=1.0, word="DEAD", head="Debit +", labels="", color="blue", glow=-1, **_):
    """Memory-trick letter tiles (DEAD CURLS, FA1 lesson 1.5): a head pill (e.g. "Debit +") over the letters stacked as square tiles; labels ("|"-separated per letter, "/" breaks a line) expand each letter into its account type to the right. glow = index of a letter to light up with a yellow halo. color: blue or coral tiles. (x, y) = top centre of the head pill; the column is about 430 wide."""
    import html as _h
    col = _COL.get(color, BLUE); L = [z for z in str(labels).split("|")] if labels else []
    out = (f'<rect x="-200" y="0" width="400" height="80" rx="40" fill="{col}" stroke="{INK}" stroke-width="5"/>'
           f'<text x="0" y="56" text-anchor="middle" font-family="Inter,sans-serif" font-weight="900" font-size="50" fill="{WHITE}">{_h.escape(head)}</text>')
    for k, ch in enumerate(word):
        ty = 110 + k * 116; tx = -205
        if k == int(glow):
            out += f'<rect x="{tx - 14}" y="{ty - 14}" width="{128 + (330 if L else 0)}" height="128" rx="26" fill="#FFD45C" opacity="0.85"/>'
        out += (f'<rect x="{tx}" y="{ty}" width="100" height="100" rx="16" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>'
                f'<text x="{tx + 50}" y="{ty + 72}" text-anchor="middle" font-family="Inter,sans-serif" font-weight="900" font-size="70" fill="{col}">{_h.escape(ch)}</text>')
        if k < len(L) and L[k]:
            lines = L[k].split("/")
            fsz = 40 if len(lines) == 1 else 34
            for j, ln in enumerate(lines):
                yy = ty + 50 + (j - (len(lines) - 1) / 2) * (fsz + 4) + fsz * 0.36
                out += f'<text x="{tx + 122}" y="{yy:.0f}" font-family="Inter,sans-serif" font-weight="800" font-size="{fsz}" fill="{INK}">{_h.escape(ln.strip())}</text>'
    return _g(x, y, s, out)


def letter_tiles_box(x, y, s=1.0, word="DEAD", **_):
    return [x - 225 * s, y - 4 * s, 450 * s, (110 + len(word) * 116 + 10) * s]


def shopfront(x, y, s=1.0, **_):
    """A small clothes shop from the street (no sign text): a striped awning, a big shop window with a rail of shirts and a door. Put a character after it in the list at the window (about x - 120, y - 40 at s 1) to show them inside. (x, y) = centre of the ground under it; about 800 wide and 760 tall at s 1."""
    stripes = "".join(f'<path d="M{-400 + k * 80} -600 h80 l-6 70 q-34 22 -68 0 Z" fill="{BLUE if k % 2 == 0 else WHITE}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>' for k in range(10))
    shirts = "".join(f'<path d="M{hx - 24} -404 L{hx - 38} -374 L{hx - 28} -370 L{hx - 24} -300 H{hx + 24} L{hx + 28} -370 L{hx + 38} -374 L{hx + 24} -404 Q{hx} -394 {hx - 24} -404 Z" fill="{c}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
                     for hx, c in ((-300, CORAL), (-240, "#F3D9A6"), (-180, GREEN), (-120, LB), (-60, NAVY)))
    return _g(x, y, s, (f'<rect x="-380" y="-720" width="760" height="720" fill="#F4ECDD" stroke="{INK}" stroke-width="{SW}"/>'
                        f'<rect x="-380" y="-720" width="760" height="110" fill="#E3D2B5" stroke="{INK}" stroke-width="{SW}"/>'
                        f'<rect x="-250" y="-690" width="500" height="54" rx="10" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>'
                        f'<path d="M-200 -663 H200" stroke="{GREY}" stroke-width="8" stroke-linecap="round" stroke-dasharray="40 18"/>'
                        f'{stripes}<rect x="-340" y="-480" width="420" height="440" rx="6" fill="{SKY}" stroke="{INK}" stroke-width="{SW}"/>'
                        f'<path d="M-330 -404 H70" stroke="{INK}" stroke-width="5"/>{shirts}'
                        f'<path d="M-300 -150 L-260 -200 M-280 -120 L-220 -190" stroke="{WHITE}" stroke-width="8" stroke-linecap="round" opacity="0.8"/>'
                        f'<rect x="130" y="-420" width="200" height="420" rx="6" fill="{BLUE}" stroke="{INK}" stroke-width="{SW}"/>'
                        f'<rect x="160" y="-390" width="140" height="170" rx="6" fill="{SKY}" stroke="{INK}" stroke-width="4"/>'
                        f'<circle cx="300" cy="-200" r="10" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>'
                        f'<path d="M-420 0 H420" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'))


def shopfront_box(x, y, s=1.0, **_):
    return [x - 405 * s, y - 725 * s, 810 * s, 728 * s]


def shopping_bag(x, y, s=1.0, color="blue", **_):
    """A paper shopping bag with rope handles (no logo). color: blue, coral, gold, green. (x, y) = centre."""
    c = {"blue": BLUE, "coral": CORAL, "gold": "#F3D9A6", "green": GREEN}.get(color, BLUE)
    return _g(x, y, s, (f'<path d="M-24 -50 q0 -36 24 -36 q24 0 24 36" fill="none" stroke="{INK}" stroke-width="6"/>'
                        f'<path d="M-60 -50 H60 L68 80 H-68 Z" fill="{c}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
                        f'<path d="M-60 -50 L-48 -30 H48 L60 -50" fill="none" stroke="{INK}" stroke-width="3" opacity="0.5"/>'))


def bank_app(x, y, s=1.0, amount="", note="", **_):
    """A big phone showing a generic banking app (no real brand): a balance card with a coral amount going out (e.g. "-$23,950"), a short note and a draining bar. (x, y) = centre (phone size)."""
    import html as _h
    fa = min(64, 230 / max(1, len(amount) * 0.6))
    return _g(x, y, s, (f'<rect x="-150" y="-280" width="300" height="560" rx="40" fill="{WHITE}" stroke="{INK}" stroke-width="8"/>'
                        f'<rect x="-125" y="-235" width="250" height="450" rx="12" fill="{SKY}"/>'
                        f'<rect x="-30" y="232" width="60" height="10" rx="5" fill="{INK}" opacity="0.4"/>'
                        f'<circle cx="-80" cy="-190" r="22" fill="{LB}" stroke="{INK}" stroke-width="4"/><path d="M-44 -196 H60 M-44 -178 H20" stroke="{GREY}" stroke-width="8" stroke-linecap="round"/>'
                        f'<rect x="-108" y="-130" width="216" height="150" rx="14" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>'
                        f'<text x="0" y="-48" text-anchor="middle" font-family="Inter,sans-serif" font-weight="900" font-size="{fa:.0f}" fill="#D0675E">{_h.escape(amount)}</text>'
                        f'<text x="0" y="0" text-anchor="middle" font-family="Inter,sans-serif" font-weight="700" font-size="26" fill="#4B5568">{_h.escape(note)}</text>'
                        f'<rect x="-100" y="60" width="200" height="34" rx="17" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>'
                        f'<rect x="-96" y="64" width="54" height="26" rx="13" fill="{CORAL}"/>'
                        f'<path d="M-20 130 V190 M-40 172 L-20 192 L0 172" fill="none" stroke="{CORAL}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
                        f'<path d="M30 130 V190 M10 172 L30 192 L50 172" fill="none" stroke="{CORAL}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>'))


# ---------------------------------------------------------------- data props: real numbers on screen (Hoang, 6 Nov 2026)
# Hand-drawn like the rest (they boil and draw on), blue main colour, amber highlight. They compute nothing but the scale:
# every value shows as given. Text stays at DATA_FLOOR or larger at s=1; if it cannot, the build stops with a clear message.
ED_BLUE = "#2960c7"; DATA_FLOOR = 34; DATA_SUB = INK; DATA_RULE = "#C9D1DC"
_D_PREFIX = ("$", "€", "£")


def _d_tw(txt, fs):
    """Estimated width of Inter 800-900 text, by character class, a touch wide on purpose so labels never touch."""
    w = 0.0
    for c in str(txt):
        if c in "il.,:;'|!": w += 0.31
        elif c in "jftr ()-": w += 0.42
        elif c in "mw": w += 0.9
        elif c in "MW%": w += 0.98
        elif c.isupper(): w += 0.73
        else: w += 0.62
    return w * fs


def _d_num(v, unit, where):
    """The number behind a shown value, used only for the scale. Accepts 0.44, "0.44", "$0.44", "3,000", "12%"."""
    if isinstance(v, bool): raise ValueError(f"{where}: {v!r} is not a number")
    if isinstance(v, (int, float)): return float(v)
    t = str(v).replace("−", "-")
    if unit: t = t.replace(unit, "")
    for c in _D_PREFIX + (",", "%", " "): t = t.replace(c, "")
    try: return float(t)
    except ValueError: raise ValueError(f'{where}: value {v!r} is not a number; put words in "unit" or "labels"') from None


def _d_label(v, unit):
    """The value as shown: the given text plus the unit ("$" and other currency signs in front, the rest behind). Pass strings to keep zeros ("0.40")."""
    t = v if isinstance(v, str) else (str(int(v)) if float(v).is_integer() else str(v))
    t = t.replace("−", "-").strip()
    if not unit or unit in t: return t
    if unit in _D_PREFIX: return ("-" + unit + t[1:]) if t.startswith("-") else unit + t
    return t + unit if unit == "%" else f"{t} {unit}"


def _d_wrap(txt, fs, width):
    """Greedy word wrap by estimated width. A word wider than width stays on its own line (the caller rejects that size)."""
    lines = []; cur = ""
    for word in str(txt).split():
        t = f"{cur} {word}".strip()
        if cur and _d_tw(t, fs) > width: lines.append(cur); cur = word
        else: cur = t
    return lines + [cur] if cur else [""]


def _d_fit(labels, width, top, maxlines, where):
    """The largest font size (top down to DATA_FLOOR) at which every label wraps into maxlines lines inside width."""
    fs = top
    while fs >= DATA_FLOOR:
        wrapped = [_d_wrap(t, fs, width) for t in labels]
        if all(len(w) <= maxlines and all(_d_tw(l, fs) <= width for l in w) for w in wrapped): return fs, wrapped
        fs -= 2
    raise ValueError(f"{where}: labels {labels!r} do not fit {width:.0f} wide at the {DATA_FLOOR} px minimum; shorten them, use fewer of them or raise w")


def _d_index(hl, n, where):
    if hl is None: return None
    if isinstance(hl, bool) or not isinstance(hl, int) or not -n <= hl < n: raise ValueError(f"{where}: highlight {hl!r} is out of range (there are {n})")
    return hl % n


def _d_rect_hits_seg(r, a, b):
    """True when the segment a-b passes through the rectangle r = (x0, y0, x1, y1) (Liang-Barsky clip)."""
    t0, t1 = 0.0, 1.0; dx, dy = b[0] - a[0], b[1] - a[1]
    for p, q in ((-dx, a[0] - r[0]), (dx, r[2] - a[0]), (-dy, a[1] - r[1]), (dy, r[3] - a[1])):
        if p == 0:
            if q < 0: return False
        else:
            u = q / p
            if p < 0: t0 = max(t0, u)
            else: t1 = min(t1, u)
            if t0 > t1: return False
    return True


def data_chart(x, y, s=1.0, kind="bars", values=None, labels=None, unit="", y_title="", x_title="", highlight=None, w=860, h=760, zero=True, **_):
    """Real numbers as a hand-drawn bar or line chart (6 Nov 2026). (x, y) = centre, box w x h. kind: bars (always from zero) or line. values: numbers or number strings, shown as given (use strings to keep zeros: "0.40"). labels: one category per value (equally spaced, 1-8). unit: "$" goes in front, "%" or a word behind. y_title, x_title: optional axis titles. highlight: index or category label, drawn in amber. zero false (line only): the scale starts near the lowest value instead of 0."""
    where = "data_chart"
    values = list(values or []); labels = [str(l) for l in (labels or [])]
    if kind not in ("bars", "line"): raise ValueError(f'{where}: kind {kind!r}; use "bars" or "line"')
    if not 1 <= len(values) <= 8: raise ValueError(f"{where}: {len(values)} values; use 1 to 8")
    if len(labels) != len(values): raise ValueError(f"{where}: {len(values)} values but {len(labels)} labels")
    n = len(values); nums = [_d_num(v, unit, where) for v in values]; shown = [_d_label(v, unit) for v in values]
    if isinstance(highlight, str):
        if highlight not in labels: raise ValueError(f"{where}: highlight {highlight!r} is not one of the labels")
        highlight = labels.index(highlight)
    hl = _d_index(highlight, n, where)
    hw, hh = w / 2, h / 2; pw = w - 16; slot = pw / n; left = -pw / 2; out = ""
    cx = [left + slot * (k + 0.5) for k in range(n)]
    # top: the y title
    top = -hh
    if y_title:
        fs, (ls,) = _d_fit([y_title], w, 42, 2, where)
        for l in ls:
            top += fs * 1.02; out += _t(-hw + 6, top, l, round(fs), 800, DATA_SUB, "start"); top += fs * 0.16
        top += 10
    # bottom: the x title under the category labels
    bot = hh
    if x_title:
        fs, (ls,) = _d_fit([x_title], w, 42, 2, where)
        for k, l in enumerate(reversed(ls)): out += _t(0, bot - 8 - k * fs * 1.16, l, round(fs), 800, DATA_SUB)
        bot -= len(ls) * fs * 1.16 + 14
    stagger = 0
    try: fc, wrapped = _d_fit(labels, slot - 6, 50, 3, where)
    except ValueError:   # too tight in one row: every second label drops to a second row, so each gets about two slots of width
        fc, wrapped = _d_fit(labels, slot * 2 - 16, 44, 2, where)
        stagger = max(len(l) for l in wrapped[::2]) * fc * 1.16 + 6 if n > 1 else 0
    nl = max(len(l) for l in wrapped); bot -= stagger + nl * fc * 1.16 + 8
    fv = 84
    while fv > DATA_FLOOR and max(_d_tw(t, fv) for t in shown) > slot - 20: fv -= 2
    if max(_d_tw(t, fv) for t in shown) > slot - 20: raise ValueError(f"{where}: values {shown!r} do not fit {slot:.0f} wide at the {DATA_FLOOR} px minimum; use fewer values or raise w")
    # scale: from the numbers only. Bars always include zero
    lo, hi = min(nums + [0.0]), max(nums + [0.0])
    if kind == "line" and not zero and min(nums) > 0:
        rng = (max(nums) - min(nums)) or max(nums); lo, hi = min(nums) - 0.1 * rng, max(nums)
    head = fv * 0.78 + 56 if kind == "line" else fv * 1.34   # room for the value above the top point or bar, and below when the scale goes under the axis
    foot = head if lo < 0 or (kind == "line" and lo > 0) else 0
    ph = bot - top - head - foot
    if ph < 110: raise ValueError(f"{where}: h {h} leaves only {ph:.0f} px for the plot; raise h or shorten the labels and titles")
    k_y = ph / ((hi - lo) or 1.0); ptop = top + head
    Y = lambda v: ptop + (hi - v) * k_y
    base = Y(max(lo, 0.0)) if lo <= 0 else Y(lo)
    out += f'<path d="{_wobble_line(-hw + 4, hw - 4, base, 3)}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
    if kind == "bars":
        bw = min(slot * 0.66, 240)
        for k, v in enumerate(nums):
            c = cx[k]; yt = Y(v); d = yt - base; xl, xr = c - bw / 2, c + bw / 2
            if abs(d) >= 1:
                r = min(12, abs(d) / 2) * (1 if d < 0 else -1); m = (yt + base) / 2
                out += (f'<path d="M{xl:.1f} {base:.1f} Q{xl - 2:.1f} {m:.1f} {xl + 1:.1f} {yt + r:.1f} Q{xl + 1:.1f} {yt:.1f} {xl + 1 + abs(r):.1f} {yt:.1f} '
                        f'L{xr - abs(r):.1f} {yt + 1.5:.1f} Q{xr:.1f} {yt + 1:.1f} {xr:.1f} {yt + r:.1f} Q{xr + 2:.1f} {m:.1f} {xr - 1:.1f} {base:.1f}" '
                        f'fill="{AMBER if k == hl else ED_BLUE}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
            out += _t(c, yt - fv * 0.3 if v >= 0 else yt + fv * 1.04, shown[k], round(fv), 900, INK)
    else:
        pts = [(cx[k], Y(v)) for k, v in enumerate(nums)]
        segs = list(zip(pts, pts[1:])) + [((-hw, base), (hw, base))]
        for c in cx: out += f'<path d="M{c:.1f} {base - 9:.1f} L{c:.1f} {base + 9:.1f}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
        if n > 1: out += '<path d="M' + " L".join(f"{p[0]:.1f} {p[1]:.1f}" for p in pts) + f'" fill="none" stroke="{ED_BLUE}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
        for k, p in enumerate(pts):
            out += f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{22 if k == hl else 14}" fill="{AMBER if k == hl else ED_BLUE}" stroke="{INK}" stroke-width="5"/>'
        dots = [(p[0] - 24, p[1] - 24, p[0] + 24, p[1] + 24) for p in pts]; m = 8
        def spots(fs):   # for each value, the first spot that clears the line, the dots, the axis and the other values; None if one has no spot at this size
            placed = []; res = []
            for k, p in enumerate(pts):
                lw = _d_tw(shown[k], fs); lh = fs * 0.78; gap = 38 if k == hl else 24; spot = None
                for extra in (0, 18, 44, 90, 150):
                    for dx, above in ((0, True), (lw / 2 + 14, True), (-lw / 2 - 14, True), (0, False), (lw / 2 + 14, False), (-lw / 2 - 14, False)):
                        y1 = p[1] - gap - extra if above else p[1] + gap + extra + lh
                        r = (p[0] + dx - lw / 2 - m, y1 - lh - m, p[0] + dx + lw / 2 + m, y1 + m)
                        if r[0] < -hw or r[2] > hw or r[1] < top or r[3] > bot: continue
                        if any(_d_rect_hits_seg(r, a, b) for a, b in segs): continue
                        if any(r[0] < q[2] and q[0] < r[2] and r[1] < q[3] and q[1] < r[3] for q in placed + [d for j, d in enumerate(dots) if j != k]): continue
                        spot = (p[0] + dx, y1, r, lw, lh); break
                    if spot: break
                if not spot: return None
                placed.append(spot[2]); res.append(spot)
            return res
        fl = fv; found = spots(fl)
        while not found and fl > DATA_FLOOR:   # a tight zigzag: smaller values find room before the build gives up
            fl = max(DATA_FLOOR, fl - 4); found = spots(fl)
        if not found: raise ValueError(f"{where}: no clear spot for the values {shown!r} at the {DATA_FLOOR} px minimum; use fewer points or raise w or h")
        for k, (lx, ly, _r, lw, lh) in enumerate(found):
            if k == hl: out += f'<rect x="{lx - lw / 2 - 8:.1f}" y="{ly - lh - 2:.1f}" width="{lw + 16:.1f}" height="{lh + 10:.1f}" rx="10" fill="{AMBER}" fill-opacity="0.6" stroke="none"/>'
            out += _t(lx, ly, shown[k], round(fl), 900, INK)
    for k, ls in enumerate(wrapped):
        for j, l in enumerate(ls): out += _t(min(max(cx[k], -hw + _d_tw(l, fc) / 2), hw - _d_tw(l, fc) / 2), bot + 8 + (stagger if k % 2 else 0) + fc * 0.92 + j * fc * 1.16, l, round(fc), 900 if k == hl else 800, INK)
    return _g(x, y, s, out)


def data_chart_box(x, y, s=1.0, w=860, h=760, **_):
    return [x - w / 2 * s - 4, y - h / 2 * s - 4, w * s + 8, h * s + 8]


def _dt_numeric(t):
    import re
    return bool(re.match(r"^[-+−(]?\s?[$€£]?\s?\d[\d,]*(\.\d+)?\s?(%|[A-Za-z]{1,3})?\)?$", str(t).strip()))


def _dt_layout(headers, rows, w, h):
    """Font size, column widths, row heights and wrapped text for data_table."""
    where = "data_table"
    head = [str(c) for c in (headers or [])]; body = [[str(c) for c in r] for r in (rows or [])]; nc = len(head)
    if not 1 <= nc <= 5: raise ValueError(f"{where}: {nc} columns; use 1 to 5")
    if not 1 <= len(body) <= 6: raise ValueError(f"{where}: {len(body)} rows; use 1 to 6")
    for r in body:
        if len(r) != nc: raise ValueError(f"{where}: row {r!r} has {len(r)} cells; the headers have {nc}")
    num = []   # a column reads as numbers when most of its filled cells are numbers: it aligns right, the rest left
    for c in range(nc):
        cells = [r[c] for r in body if r[c].strip()]
        num.append(bool(cells) and sum(_dt_numeric(t) for t in cells) * 2 >= len(cells))
    px = {1: 24, 2: 24, 3: 24, 4: 18}.get(nc, 14); fs = 66
    while fs >= DATA_FLOOR:
        mins, ideal = [], []
        for c in range(nc):
            col = [r[c] for r in body]
            words = [wd for t in [head[c]] + (col if not num[c] else []) for wd in t.split()] + (col if num[c] else [])
            mins.append(max(_d_tw(t, fs) for t in words + [""]) + 2 * px)
            ideal.append(max(_d_tw(t, fs) for t in [head[c]] + col) + 2 * px)
        if sum(mins) <= w:
            spare = w - sum(mins); need = [i - m for i, m in zip(ideal, mins)]; tot = sum(need)
            if tot <= spare: cw = [i + (spare - tot) / nc for i in ideal]
            else: cw = [m + spare * d / tot for m, d in zip(mins, need)]
            hd = [_d_wrap(t, fs, cw[c] - 2 * px + 1) for c, t in enumerate(head)]
            bd = [[_d_wrap(t, fs, cw[c] - 2 * px + 1) if not num[c] else [t] for c, t in enumerate(r)] for r in body]
            if max(len(l) for l in hd) <= 3 and all(len(l) <= 3 for r in bd for l in r):
                lh = fs * 1.16; vp = max(14, fs * 0.3)
                rh = [max(len(l) for l in hd) * lh + 2 * vp] + [max(len(l) for l in r) * lh + 2 * vp for r in bd]
                if not h or sum(rh) <= h:
                    if h: rh = [v + (h - sum(rh)) / len(rh) for v in rh]
                    return {"fs": fs, "lh": lh, "cw": cw, "rh": rh, "num": num, "hd": hd, "bd": bd, "W": w, "H": sum(rh), "px": px}
        fs -= 2
    raise ValueError(f"{where}: the table does not fit {w} wide{f' x {h} high' if h else ''} at the {DATA_FLOOR} px minimum; shorten the text, drop a column or raise w")


def data_table(x, y, s=1.0, headers=None, rows=None, highlight=None, w=860, h=None, **_):
    """Real numbers as a hand-drawn table (6 Nov 2026). (x, y) = centre. headers: up to 5 columns; rows: up to 6 rows of cells, shown as given (strings: "$1,200"). Number columns align right; text wraps. highlight: amber on a row (2, -1 or {"row": 2}) or a cell ({"cell": [row, column]}), counted in body rows from 0. w, h: size (h optional: rows stretch to fill it)."""
    L_ = _dt_layout(headers, rows, w, h); W, H = L_["W"], L_["H"]; fs = L_["fs"]; lh = L_["lh"]; nr = len(L_["bd"]); nc = len(L_["cw"])
    hl_row = hl_cell = None
    if isinstance(highlight, dict) and "cell" in highlight:
        r, c = highlight["cell"]; hl_cell = (_d_index(r, nr, "data_table"), _d_index(c, nc, "data_table"))
    elif isinstance(highlight, dict): hl_row = _d_index(highlight.get("row"), nr, "data_table")
    else: hl_row = _d_index(highlight, nr, "data_table")
    x0, y0 = -W / 2, -H / 2; x1, y1 = W / 2, H / 2; R = 20
    edge = lambda a, b, c, d: f"M{a + R:.1f} {b:.1f} L{c - R:.1f} {b - 1.5:.1f} Q{c:.1f} {b:.1f} {c:.1f} {b + R:.1f} L{c + 1.5:.1f} {d - R:.1f} Q{c:.1f} {d:.1f} {c - R:.1f} {d:.1f} L{a + R:.1f} {d + 1.5:.1f} Q{a:.1f} {d:.1f} {a:.1f} {d - R:.1f} L{a - 1.5:.1f} {b + R:.1f} Q{a:.1f} {b:.1f} {a + R:.1f} {b:.1f} Z"
    out = f'<path d="{edge(x0, y0, x1, y1)}" fill="{WHITE}" stroke="none"/>'
    yh = y0 + L_["rh"][0]
    out += f'<path d="M{x0:.1f} {yh:.1f} L{x0:.1f} {y0 + R:.1f} Q{x0:.1f} {y0:.1f} {x0 + R:.1f} {y0:.1f} L{x1 - R:.1f} {y0:.1f} Q{x1:.1f} {y0:.1f} {x1:.1f} {y0 + R:.1f} L{x1:.1f} {yh:.1f} Z" fill="{ED_BLUE}" stroke="none"/>'
    ys = [yh]
    for v in L_["rh"][1:]: ys.append(ys[-1] + v)
    xs = [x0]
    for v in L_["cw"]: xs.append(xs[-1] + v)
    if hl_row is not None:
        a, b = ys[hl_row], ys[hl_row + 1]
        if hl_row == nr - 1: out += f'<path d="M{x0:.1f} {a:.1f} L{x1:.1f} {a:.1f} L{x1:.1f} {b - R:.1f} Q{x1:.1f} {b:.1f} {x1 - R:.1f} {b:.1f} L{x0 + R:.1f} {b:.1f} Q{x0:.1f} {b:.1f} {x0:.1f} {b - R:.1f} Z" fill="{AMBER}" stroke="none"/>'
        else: out += f'<rect x="{x0:.1f}" y="{a:.1f}" width="{W:.1f}" height="{b - a:.1f}" fill="{AMBER}" stroke="none"/>'
    if hl_cell:
        r, c = hl_cell
        out += f'<rect x="{xs[c] + 6:.1f}" y="{ys[r] + 6:.1f}" width="{xs[c + 1] - xs[c] - 12:.1f}" height="{ys[r + 1] - ys[r] - 12:.1f}" rx="12" fill="{AMBER}" stroke="none"/>'
    for v in ys[1:-1]: out += f'<path d="{_wobble_line(x0 + 12, x1 - 12, v, 2)}" fill="none" stroke="{DATA_RULE}" stroke-width="4" stroke-linecap="round"/>'
    out += f'<path d="{edge(x0, y0, x1, y1)}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    def cell(lines, c, top, height, col, wt):
        nn = len(lines); fy = top + (height - nn * lh) / 2 + lh * 0.5 + fs * 0.36; right = L_["num"][c]; px = L_["px"]
        return "".join(_t(xs[c + 1] - px if right else xs[c] + px, fy + j * lh, l, fs, wt, col, "end" if right else "start") for j, l in enumerate(lines))
    for c, ls in enumerate(L_["hd"]): out += cell(ls, c, y0, L_["rh"][0], WHITE, 900)
    for r, row in enumerate(L_["bd"]):
        for c, ls in enumerate(row):
            out += cell(ls, c, ys[r], ys[r + 1] - ys[r], INK, 900 if r == hl_row or (r, c) == hl_cell else 800)
    return _g(x, y, s, out)


def data_table_box(x, y, s=1.0, headers=None, rows=None, w=860, h=None, **_):
    L_ = _dt_layout(headers, rows, w, h)
    return [x - w / 2 * s - 4, y - L_["H"] / 2 * s - 4, w * s + 8, L_["H"] * s + 8]


_XL = {"blue": ("#2F6FDE", "#DCE8FC"), "red": ("#D6453D", "#FBE3E1"), "green": ("#1F8A4C", "#DDF3E5"), "violet": ("#7A5AF8", "#EAE5FE"), "amber": ("#B97A00", "#FFF0C9")}


def _xl_layout(cols, rows, w, h, fs):
    from html import escape
    cols = cols or []; rows = rows or []
    if not cols or not rows: raise ValueError("sheet_grid: needs cols and rows")
    if any(len(r) != len(cols) for r in rows): raise ValueError("sheet_grid: each row needs one cell per column (use \"\" for an empty cell)")
    head = 76; col_h = 56; gut = 66; rh = 78
    H = h or head + col_h + rh * len(rows) + 10
    rh = (H - head - col_h - 10) / len(rows)
    want = [max(3.2, max(len(str(r[c])) for r in rows) + 1.6) for c in range(len(cols))]
    avail = w - gut - 8; unit = avail / sum(want)
    size = min(fs, unit / 0.62)
    if size < 30: raise ValueError(f"sheet_grid: cell text needs {size:.0f} px to fit; shorten the cells or drop a column (30 px is the minimum)")
    cw = [v * unit for v in want]
    return dict(H=H, head=head, col_h=col_h, gut=gut, rh=rh, cw=cw, fs=size, esc=escape)


def sheet_grid(x, y, s=1.0, cols=None, rows=None, name_box="", formula="", selected=None, refs=None, start_row=1, popup=None, w=880, h=None, fs=40, **_):
    """A real spreadsheet (6 Nov 2026, Hoang: "real excel reference and equation"): name box, formula bar with the formula as typed, lettered columns, numbered rows, a selected cell and coloured reference boxes that match the formula. (x, y) = centre. cols: ["A", "B"]; rows: cells as given; start_row: number of the first row shown; selected: [row, col] counted from 0; refs: [{"cell": [row, col], "color": "blue", "label": "B2"}] (blue, red, green, violet, amber; label colours that text in the formula); popup: {"title", "text"} is an error box over the grid. Show states with several items and at/until."""
    L_ = _xl_layout(cols, rows, w, h, fs); W, H = w, L_["H"]; esc = L_["esc"]; f = L_["fs"]
    x0, y0 = -W / 2, -H / 2; out = f'<rect x="{x0}" y="{y0}" width="{W}" height="{H}" rx="10" fill="{WHITE}" stroke="none"/>'
    # name box and formula bar
    nb = 170; bh = L_["head"] - 16; by = y0 + 8
    out += f'<rect x="{x0 + 8}" y="{by}" width="{nb}" height="{bh}" rx="6" fill="#F3F5F8" stroke="{INK}" stroke-width="3"/>'
    out += _t(x0 + 8 + nb / 2, by + bh * 0.72, esc(str(name_box)), 38, 800, INK)
    fx = x0 + nb + 22
    out += _t(fx + 18, by + bh * 0.72, "fx", 36, 800, "#64748B")
    fb = fx + 52; out += f'<rect x="{fb}" y="{by}" width="{W / 2 - 8 - fb}" height="{bh}" rx="6" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>'
    # formula text, reference names in their colours
    import re as _re
    colour = {str(r["label"]): _XL[r.get("color", "blue")][0] for r in (refs or []) if r.get("label")}
    parts = _re.split("(" + "|".join(_re.escape(k) for k in sorted(colour, key=len, reverse=True)) + ")", str(formula)) if colour else [str(formula)]
    ffs = 42; room = W / 2 - 8 - fb - 28; flen = len(str(formula)) * ffs * 0.58
    if flen > room: ffs = ffs * room / flen
    if ffs < 30: raise ValueError(f"sheet_grid: the formula {formula!r} is too long for the bar; widen the sheet or shorten it")
    spans = "".join(f'<tspan fill="{colour.get(p, INK)}">{esc(p)}</tspan>' for p in parts if p)
    out += f'<text x="{fb + 14}" y="{by + bh * 0.72}" font-family="Inter" font-size="{ffs:.1f}" font-weight="800">{spans}</text>'
    # grid
    gy = y0 + L_["head"]; gx = x0 + L_["gut"]; xs = [gx]
    for v in L_["cw"]: xs.append(xs[-1] + v)
    ch = L_["col_h"]; rh = L_["rh"]; ys = [gy + ch + i * rh for i in range(len(rows) + 1)]
    out += f'<rect x="{x0}" y="{gy}" width="{W}" height="{ch}" fill="#E8ECF1" stroke="none"/><rect x="{x0}" y="{gy}" width="{L_["gut"]}" height="{ys[-1] - gy}" fill="#E8ECF1" stroke="none"/>'
    for c, nm in enumerate(cols):
        on = selected and selected[1] == c
        if on: out += f'<rect x="{xs[c]}" y="{gy}" width="{L_["cw"][c]}" height="{ch}" fill="#CFE8D8" stroke="none"/>'
        out += _t((xs[c] + xs[c + 1]) / 2, gy + ch * 0.72, esc(str(nm)), 32, 800, "#475569")
    for r in range(len(rows)):
        on = selected and selected[0] == r
        if on: out += f'<rect x="{x0}" y="{ys[r]}" width="{L_["gut"]}" height="{rh}" fill="#CFE8D8" stroke="none"/>'
        out += _t(x0 + L_["gut"] / 2, ys[r] + rh * 0.64, str(start_row + r), 32, 800, "#475569")
    for rf in refs or []:
        a, b = rf["cell"]; col, tint = _XL[rf.get("color", "blue")]
        out += f'<rect x="{xs[b]}" y="{ys[a]}" width="{L_["cw"][b]}" height="{rh}" fill="{tint}" stroke="none"/>'
    for v in ys: out += f'<line x1="{gx}" y1="{v}" x2="{xs[-1]}" y2="{v}" stroke="#AEB8C4" stroke-width="2.5"/>'
    for v in xs: out += f'<line x1="{v}" y1="{gy}" x2="{v}" y2="{ys[-1]}" stroke="#AEB8C4" stroke-width="2.5"/>'
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            sv = str(val)
            if not sv: continue
            right = bool(_re.match(r"^[-$\d]", sv))
            tx = xs[c + 1] - 14 if right else xs[c] + 14
            out += _t(tx, ys[r] + rh * 0.66, esc(sv), f, 700, INK, "end" if right else "start")
    for rf in refs or []:
        a, b = rf["cell"]; col = _XL[rf.get("color", "blue")][0]
        out += f'<rect x="{xs[b] + 2}" y="{ys[a] + 2}" width="{L_["cw"][b] - 4}" height="{rh - 4}" fill="none" stroke="{col}" stroke-width="6"/>'
    if selected:
        a, b = selected
        out += f'<rect x="{xs[b] + 1}" y="{ys[a] + 1}" width="{L_["cw"][b] - 2}" height="{rh - 2}" fill="none" stroke="#107C41" stroke-width="8"/><rect x="{xs[b + 1] - 9}" y="{ys[a + 1] - 9}" width="16" height="16" fill="#107C41" stroke="{WHITE}" stroke-width="2"/>'
    out += f'<rect x="{x0}" y="{y0}" width="{W}" height="{H}" rx="10" fill="none" stroke="{INK}" stroke-width="6"/>'
    if popup:
        pw = W * 0.82; ph = 230; px = -pw / 2; py = ys[-1] - ph - 12
        out += f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="14" fill="{WHITE}" stroke="#D6453D" stroke-width="7"/>'
        out += f'<circle cx="{px + 62}" cy="{py + 74}" r="34" fill="#D6453D"/>' + _t(px + 62, py + 90, "×", 52, 900, WHITE)
        out += _t(px + 116, py + 90, esc(str(popup.get("title", ""))), 44, 900, INK, "start")
        out += _t(px + 40, py + 170, esc(str(popup.get("text", ""))), 38, 700, INK, "start")
    return _g(x, y, s, out)


def sheet_grid_box(x, y, s=1.0, cols=None, rows=None, w=880, h=None, fs=40, **_):
    L_ = _xl_layout(cols, rows, w, h, fs)
    return [x - w / 2 * s - 4, y - L_["H"] / 2 * s - 4, w * s + 8, L_["H"] * s + 8]


BACKGROUNDS = ["paper", "office", "classroom", "lecture", "home", "street", "campus", "store", "none"]

# name -> (draw function, box function or None = default box from size)
PRESETS = {
    "ledger": (ledger, ledger_box), "person": (person, person_box), "people_group": (people_group, people_group_box),
    "phone": (phone, None), "laptop": (laptop, None), "bills": (bills, None), "coins": (coins, None),
    "calendar": (calendar, None), "invoice": (invoice, None), "chart": (chart, None), "coffee": (coffee, None),
    "window": (window, None), "door": (door, door_box), "sofa": (sofa, None), "bed": (bed, None), "scale": (scale, scale_box),
    "pit": (pit, pit_box), "sun_arrow": (sun_arrow, None), "handshake": (handshake, None), "whiteboard": (whiteboard, None),
    "desk": (desk, desk_box), "school_desk": (school_desk, None), "ticket": (ticket, None), "thought": (thought, thought_box),
    "speech": (speech, speech_box), "building": (building, building_box), "clock": (clock, None), "umbrella": (umbrella, None),
    "books": (books, None), "blocks": (blocks, None), "price_tag": (price_tag, None), "funnel": (funnel, funnel_box), "envelope": (envelope, None),
    "arrow": (arrow, arrow_box), "cross": (cross, cross_box), "check": (check, None),
    "bubble": (bubble, bubble_box), "lamp": (lamp, None), "stat_card": (stat_card, None), "lightbulb": (lightbulb, None),
    "pizza": (pizza, None), "pizza_slice": (pizza_slice, None), "sandwich": (sandwich, None), "lemonade_cup": (lemonade_cup, None),
    "lemonade_stand": (lemonade_stand, lemonade_stand_box), "plate": (plate, None), "burger": (burger, None),
    "groceries_bag": (groceries_bag, None), "receipt": (receipt, None), "gym": (gym, gym_box), "bus": (bus, bus_box),
    "code_screen": (code_screen, None), "chessboard": (chessboard, None), "robot_arm": (robot_arm, robot_arm_box), "toddler": (toddler, toddler_box),
    "meeting_table": (meeting_table, meeting_table_box), "whiteboard_team": (whiteboard_team, whiteboard_team_box),
    "chip": (chip, chip_box), "swirl": (swirl, swirl_box),
    "backdrop": (backdrop, backdrop_box), "balance_sheet": (balance_sheet, None), "abc_tangle": (abc_tangle, None), "regression_guess": (regression_guess, None), "supply_shift": (supply_shift, None), "exam_sheet": (exam_sheet, exam_sheet_box), "cost_pools": (cost_pools, None), "scatter_plot": (scatter_plot, None),
    "pumpkin": (pumpkin, None), "candy_bowl": (candy_bowl, None), "ghost_kid": (ghost_kid, ghost_kid_box),
    "name_board": (name_board, name_board_box), "clothes_rack": (clothes_rack, clothes_rack_box), "calculator": (calculator, None),
    "job_ad": (job_ad, None), "manual": (manual, None), "clipboard": (clipboard, None), "headcount": (headcount, None),
    "flow_box": (flow_box, flow_box_box), "flow_arrow": (flow_arrow, flow_arrow_box), "equation": (equation, equation_box),
    "brew_tanks": (brew_tanks, brew_tanks_box), "pint": (pint, None), "share_pie": (share_pie, share_pie_box), "bike": (bike, bike_box),
    "tool_wall": (tool_wall, None), "parcel": (parcel, parcel_box), "network": (network, network_box), "school": (school, school_box),
    "money_jar": (money_jar, money_jar_box), "gas_station": (gas_station, gas_station_box), "payoff_grid": (payoff_grid, payoff_grid_box),
}
# half-sizes at s=1 for props that use the default box (centre +- these)
HALF = {"pumpkin": (95, 100), "candy_bowl": (110, 85), "phone": (155, 285), "laptop": (235, 155), "bills": (95, 110), "coins": (50, 95), "calendar": (155, 185),
        "invoice": (115, 155), "chart": (205, 155), "coffee": (95, 160), "window": (345, 265), "door": (130, 365),
        "sofa": (165, 105), "bed": (225, 90), "sun_arrow": (270, 220), "handshake": (305, 75), "whiteboard": (355, 225),
        "school_desk": (175, 185), "ticket": (115, 60), "speech": (205, 145), "clock": (115, 115), "umbrella": (145, 245),
        "books": (125, 110), "blocks": (130, 125), "price_tag": (125, 55), "envelope": (135, 90), "check": (75, 55),
        "pizza": (160, 160), "pizza_slice": (100, 165), "sandwich": (145, 90), "lemonade_cup": (100, 200), "plate": (155, 50),
        "burger": (150, 105), "groceries_bag": (125, 250), "receipt": (95, 195),
        "code_screen": (290, 262), "chessboard": (210, 210), "cost_pools": (315, 255), "scatter_plot": (275, 205),
        "lamp": (230, 160), "stat_card": (235, 155), "lightbulb": (165, 165),
        "calculator": (115, 155), "job_ad": (135, 190), "manual": (135, 165), "clipboard": (95, 140), "headcount": (380, 240),
        "pint": (66, 132), "tool_wall": (225, 225), "balance_sheet": (362, 252), "abc_tangle": (332, 252), "regression_guess": (302, 232), "supply_shift": (322, 252)}
# FA1 cast and lesson diagram props (in-lesson videos, 5 Nov 2026)
PRESETS.update({"plot": (plot, ledger_box), "tempo": (tempo, ledger_box), "till": (till, till_box), "label": (label, label_box),
                "icon_tile": (icon_tile, icon_tile_box), "big_icon": (big_icon, None), "months": (months, None), "block": (block, block_box),
                "t_account": (t_account, t_account_box), "letter_tiles": (letter_tiles, letter_tiles_box), "shopfront": (shopfront, shopfront_box),
                "shopping_bag": (shopping_bag, None), "bank_app": (bank_app, None)})
HALF.update({"big_icon": (60, 56), "months": (234, 104), "shopping_bag": (72, 90), "bank_app": (155, 285)})
# data props: real numbers on screen (6 Nov 2026)
PRESETS.update({"data_chart": (data_chart, data_chart_box), "data_table": (data_table, data_table_box)})
PRESETS.update({"sheet_grid": (sheet_grid, sheet_grid_box)})


def pin(x, y, s=1.0, color="coral", **_):
    """A small map pin that marks a field on a document (lessons). (x, y) = the pin's point."""
    col = {"coral": CORAL, "blue": BLUE, "green": GREEN}.get(color, CORAL)
    return _g(x, y, s, f'<path d="M0 0 C-6 -14 -18 -22 -18 -36 A18 18 0 1 1 18 -36 C18 -22 6 -14 0 0 Z" fill="{col}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                       f'<circle cx="0" cy="-36" r="6" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>')


def pin_box(x, y, s=1.0, **_):
    return [x - 20 * s, y - 56 * s, 40 * s, 58 * s]


PRESETS.update({"pin": (pin, pin_box)})


def car(x, y, s=1.0, flip=False, color=None, **_):
    """A small family car, side view, no brand (7 Nov 2026). (x, y) = centre of the road under its wheels. flip faces left. color: body fill."""
    c = color or LB
    inner = (f'<path d="M-200 -50 V-105 Q-200 -125 -175 -128 L-115 -135 L-65 -200 Q-55 -212 -38 -212 H70 Q88 -212 100 -198 L145 -135 L180 -128 Q205 -122 205 -100 V-50 Q205 -40 195 -40 H-190 Q-200 -40 -200 -50 Z" fill="{c}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
             f'<path d="M-88 -135 L-50 -187 Q-45 -194 -36 -194 H0 V-135 Z" fill="{SKY}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/><path d="M18 -135 V-194 H68 Q78 -194 85 -186 L122 -135 Z" fill="{SKY}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
             f'<path d="M30 -110 H62" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><circle cx="192" cy="-100" r="8" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>'
             f'<circle cx="-115" cy="-40" r="40" fill="{INK}"/><circle cx="-115" cy="-40" r="15" fill="{GREY}"/><circle cx="125" cy="-40" r="40" fill="{INK}"/><circle cx="125" cy="-40" r="15" fill="{GREY}"/>')
    if flip: inner = f'<g transform="scale(-1 1)">{inner}</g>'
    return _g(x, y, s, inner)


def car_box(x, y, s=1.0, **_):
    return [x - 210 * s, y - 216 * s, 420 * s, 216 * s]


PRESETS.update({"car": (car, car_box)})


# ---------------------------------------------------------------- motion layer (opt-in, 6 Nov 2026)
# Hoang: "the animation sometimes too simple ... arrow green red illustation with graph, number inside with people trading action and supplement info".
# Nothing here runs unless a script uses these props or item keys. The renderer computes every state from the time alone, so frames can be rendered by seeking.
UP = "#1F9D61"; DOWN = "#D8433B"; UP_TINT = "#D8F1E3"; DOWN_TINT = "#FBDDDA"; NOTE_FILL = "#FFF6D1"; GHOST = "#D5DBE4"
SELF_TIMED = {"coin_stream", "burst"}   # these props use "at" as their own start time; for the rest "at" is the usual pop-in


def _m_attr(o):
    import html as _h, json as _j
    return _h.escape(_j.dumps(o, separators=(",", ":"), ensure_ascii=False), quote=True)


def _m_fmt(v, dec=0, pre="", suf="", comp="", plus=False):
    """Money and number text, the same rules as fmtN in render.html: $1,234.50, −$5, $500K. comp "K" or "M" divides and appends the letter."""
    c = {"K": 1e3, "M": 1e6}.get(comp, 1); t = f"{abs(float(v)) / c:.{int(dec)}f}"; a, _, b = t.partition(".")
    a = f"{int(a):,}"; zero = float(t) == 0
    return ("−" if float(v) < 0 and not zero else "+" if plus and not zero else "") + pre + a + ("." + b if b else "") + comp + suf


def _m_unit(unit):
    """(prefix, suffix) for a unit: a currency sign goes in front, the rest behind."""
    u = str(unit or "")
    if u in _D_PREFIX: return u, ""
    return "", (u if u == "%" or not u else " " + u)


def _m_keys(v):
    """Motion keys are a dict or a list of dicts. Anything else is ignored, because older scripts use "move" and "pulse" as their own fields."""
    if isinstance(v, dict): return [v]
    if isinstance(v, list) and v and all(isinstance(k, dict) for k in v): return v
    return []


def _m_at(k):
    q = {"at": str(k.get("at", "chunk:0")), "delay": float(k.get("delay", 0))}
    if not str(q["at"]).startswith("chunk:"): raise ValueError(f'motion: at {q["at"]!r}; use "chunk:N"')
    return q


def _m_wrap(it, inner):
    """Generic motion on any item, opt-in by key. move: {"at","delay","dur","to":[x,y],"arc","ease","scale","rot","trail"} or a list of them, played in order. arc: pixels the path bows upward. trail: a colour name or {"color","fade","width"}. pulse: {"at","dur","amp"}. shake: {"at","dur","amp","hz"}. bob: {"amp","hz"}. out: {"at","dur"} fades it away. reveal: {"at","dur","dir"} wipes it in, dir right, left, up or down."""
    mv, pl, sh, ot, rv = [_m_keys(it.get(k)) for k in ("move", "pulse", "shake", "out", "reveal")]
    bob = it.get("bob") if isinstance(it.get("bob"), dict) else None
    if not (mv or pl or sh or ot or rv or bob): return inner
    trails = ""; x0, y0 = it["x"], it["y"]; S = {"x": x0, "y": y0}
    if mv:
        S["move"] = []
        for k in mv:
            if not (isinstance(k.get("to"), (list, tuple)) and len(k["to"]) == 2): raise ValueError(f'{it["p"]}: move needs "to": [x, y]')
            q = dict(_m_at(k), dur=float(k.get("dur", 0.7)), to=list(k["to"]), arc=float(k.get("arc", 0)), ease=k.get("ease", "inout"))
            if "scale" in k: q["scale"] = float(k["scale"])
            if "rot" in k: q["rot"] = float(k["rot"])
            S["move"].append(q)
            tr = k.get("trail")
            if tr:
                tr = tr if isinstance(tr, dict) else {"color": tr}
                x1, y1 = k["to"]; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 - q["arc"]
                col = {"green": UP, "red": DOWN, "blue": ED_BLUE, "ink": INK, "amber": AMBER}.get(tr.get("color", "blue"), tr.get("color", ED_BLUE))
                spec = dict(_m_at(k), dur=q["dur"], ease=q["ease"], fade=float(tr.get("fade", 0)))
                trails += (f'<path data-fx="trail" data-nodraw="1" data-spec="{_m_attr(spec)}" d="M{_f(x0)} {_f(y0)} Q{_f(cx)} {_f(cy)} {_f(x1)} {_f(y1)}" pathLength="1" '
                           f'stroke-dasharray="0 1" fill="none" stroke="{col}" stroke-width="{tr.get("width", 7)}" stroke-linecap="round" opacity="0"/>')
            x0, y0 = k["to"]
    if pl: S["pulse"] = [dict(_m_at(k), dur=float(k.get("dur", 0.5)), amp=float(k.get("amp", 0.12))) for k in pl]
    if sh: S["shake"] = [dict(_m_at(k), dur=float(k.get("dur", 0.6)), amp=float(k.get("amp", 9)), hz=float(k.get("hz", 7))) for k in sh]
    if ot: S["out"] = [dict(_m_at(k), dur=float(k.get("dur", 0.3))) for k in ot]
    if bob: S["bob"] = {"amp": float(bob.get("amp", 5)), "hz": float(bob.get("hz", 1.1))}
    if rv:
        k = rv[0]; b = item_box(it); pad = 24; cid = "clip-" + format(abs(hash_text(inner)) % 10 ** 10)
        spec = dict(_m_at(k), dur=float(k.get("dur", 0.8)), dir=k.get("dir", "right"), ease=k.get("ease", "inout"), box=[b[0] - pad, b[1] - pad, b[2] + 2 * pad, b[3] + 2 * pad])
        inner = (f'<clipPath id="{cid}"><rect data-fx="clip" data-nodraw="1" data-spec="{_m_attr(spec)}" x="{_f(b[0] - pad)}" y="{_f(b[1] - pad)}" width="0" height="{_f(b[3] + 2 * pad)}"/></clipPath>'
                 f'<g clip-path="url(#{cid})">{inner}</g>')
    return trails + f'<g data-fx="m" data-spec="{_m_attr(S)}">{inner}</g>'


def hash_text(t):
    h = 0
    for c in t: h = (h * 131 + ord(c)) % 2147483647
    return h


def _m_count(x, y, S, txt, fs, wt=900, col=INK, anchor="middle"):
    """A number text the renderer ticks. S: from, keys, dec, pre, suf, comp, plus."""
    return f'<text data-fx="count" data-spec="{_m_attr(S)}" x="{_f(x)}" y="{_f(y)}" text-anchor="{anchor}" font-family="Inter,sans-serif" font-weight="{wt}" font-size="{_f(fs)}" fill="{col}">{txt}</text>'


def counter(x, y, s=1.0, start=0, to=None, keys=None, unit="$", dec=0, comp="", plus=False, tick=None, dur=1.2, fs=96, color="ink", title="", tfs=40, **_):
    """A number that ticks between caption chunks, with correct money formatting. (x, y) = centre. start, to: the values; tick: the chunk it starts ticking ("chunk:N", default its "at"), dur: seconds. keys: several steps instead, [{"at","delay","dur","to"}]. unit: "$" goes in front, "%" or a word behind. dec: decimals. comp: "K" or "M" shows $500K. plus: shows + on positive values. color: ink, blue, green, red. title: small line above it. Show only numbers the voice or the script supports."""
    kk = _.get("at")
    pre, suf = _m_unit(unit); col = {"ink": INK, "blue": ED_BLUE, "green": UP, "red": DOWN}.get(color, color)
    K = [dict(_m_at(k), dur=float(k.get("dur", dur)), to=_d_num(k["to"], unit, "counter")) for k in (keys or [])]
    if not K and to is not None: K = [dict(_m_at({"at": tick or kk or "chunk:0", "delay": _.get("delay", 0)}), dur=float(dur), to=_d_num(to, unit, "counter"))]
    S = {"from": _d_num(start, unit, "counter"), "keys": K, "dec": dec, "pre": pre, "suf": suf, "comp": comp, "plus": plus, "ease": "out"}
    out = ""
    if title: out += _t(0, -fs * 0.55, str(title), tfs, 800, INK)
    out += _m_count(0, fs * 0.35, S, _m_fmt(S["from"], dec, pre, suf, comp, plus), fs, 900, col)
    return _g(x, y, s, out)


def counter_box(x, y, s=1.0, fs=96, to=None, start=0, keys=None, unit="$", dec=0, comp="", title="", **_):
    pre, suf = _m_unit(unit); vals = [start] + ([to] if to is not None else []) + [k["to"] for k in (keys or [])]
    w = max(_d_tw(_m_fmt(_d_num(v, unit, "counter"), dec, pre, suf, comp), fs) for v in vals) + 12
    if title: w = max(w, _d_tw(title, 40))
    top = fs * 0.55 + 40 if title else fs * 0.5
    return [x - w / 2 * s, y - top * s, w * s, (top + fs * 0.55) * s]


def order_chip(x, y, s=1.0, label="Buy", color="green", fs=44, plain=False, **_):
    """A hand-drawn pill with short text: an order on its way ("Bid $50.00"), or a tag ("Buyer"). color: green, red, blue, amber, light. plain: true draws only the coloured words, for a name under a figure. (x, y) = centre. Add "move" to send it somewhere."""
    fill, tc = {"green": (UP, WHITE), "red": (DOWN, WHITE), "blue": (ED_BLUE, WHITE), "amber": (AMBER, INK), "light": (WHITE, INK), "white": (WHITE, INK)}.get(color, (ED_BLUE, WHITE))
    W = _d_tw(label, fs) + 44; H = fs * 1.5
    if plain: return _g(x, y, s, _t(0, fs * 0.36, str(label), fs, 900, fill if color != "light" else INK))
    return _g(x, y, s, f'<rect x="{-W / 2:.1f}" y="{-H / 2:.1f}" width="{W:.1f}" height="{H:.1f}" rx="{H / 2:.1f}" fill="{fill}" stroke="{INK}" stroke-width="5"/>' + _t(0, fs * 0.36, str(label), fs, 900, tc))


def order_chip_box(x, y, s=1.0, label="Buy", fs=44, **_):
    W = _d_tw(label, fs) + 44; H = fs * 1.5
    return [x - W / 2 * s, y - H / 2 * s, W * s, H * s]


def coin(x, y, s=1.0, **_):
    """One gold coin with a dollar sign, to send somewhere with "move". (x, y) = centre."""
    return _g(x, y, s, f'<circle r="34" fill="{GOLD}" stroke="{INK}" stroke-width="5"/><circle r="24" fill="none" stroke="{INK}" stroke-width="3" opacity="0.45"/>' + _t(0, 14, "$", 40, 900, INK))


def _stream_piece(kind, color):
    col = {"green": UP, "red": DOWN, "blue": ED_BLUE, "amber": AMBER}.get(color, color)
    if kind == "coin": return f'<circle r="26" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>' + _t(0, 11, "$", 32, 900, INK)
    if kind == "chip": return f'<rect x="-34" y="-18" width="68" height="36" rx="18" fill="{col}" stroke="{INK}" stroke-width="4"/>'
    return f'<circle r="15" fill="{col}" stroke="{INK}" stroke-width="4"/>'


def coin_stream(x, y, s=1.0, to=None, n=5, dur=0.9, stagger=0.16, arc=60, kind="coin", color="green", delay=0, **_):
    """Several pieces flowing from (x, y) to "to": [x, y], one after another, then gone, from its "at" chunk. kind: coin, chip or dot. n: pieces; dur: seconds each; stagger: seconds between them; arc: how far the path bows upward. Coins moving between people, orders arriving at a book."""
    if not to: raise ValueError('coin_stream: needs "to": [x, y]')
    S = {"at": str(_.get("at", "chunk:0")), "delay": float(delay), "dur": float(dur), "stagger": float(stagger), "x": x, "y": y, "to": list(to), "arc": float(arc), "s": s}
    return f'<g data-fx="stream" data-spec="{_m_attr(S)}">' + "".join(f'<g class="sp" opacity="0">{_stream_piece(kind, color)}</g>' for _i in range(int(n))) + "</g>"


def coin_stream_box(x, y, s=1.0, to=None, **_):
    to = to or [x, y]
    return [min(x, to[0]) - 30, min(y, to[1]) - 30, abs(to[0] - x) + 60, abs(to[1] - y) + 60]


def burst(x, y, s=1.0, color="amber", label="", delay=0, dur=0.7, **_):
    """A brief flash when something happens, such as a trade matching: rays and a ring grow and fade from its "at" chunk. label: optional pill text that stays a little longer. (x, y) = centre."""
    col = {"amber": AMBER, "green": UP, "red": DOWN, "blue": ED_BLUE}.get(color, color)
    rays = "".join(f'<path d="M{math.cos(a) * 52:.1f} {math.sin(a) * 52:.1f} L{math.cos(a) * (88 + 16 * (i % 2)):.1f} {math.sin(a) * (88 + 16 * (i % 2)):.1f}" stroke="{col}" stroke-width="11" stroke-linecap="round" fill="none"/>'
                   for i, a in enumerate(math.pi * 2 * k / 12 for k in range(12)))
    S = {"at": str(_.get("at", "chunk:0")), "delay": float(delay), "dur": float(dur), "x": x, "y": y, "s": s}
    tag = ""
    if label:
        W = _d_tw(label, 44) + 44
        tag = (f'<g class="bl" opacity="0"><rect x="{-W / 2:.1f}" y="-36" width="{W:.1f}" height="72" rx="36" fill="{AMBER}" stroke="{INK}" stroke-width="5"/>' + _t(0, 16, str(label), 44, 900, INK) + "</g>")
    return f'<g data-fx="burst" data-spec="{_m_attr(S)}"><g class="br" opacity="0"><circle r="60" fill="{col}" fill-opacity="0.28" stroke="{col}" stroke-width="7"/>{rays}</g>{tag}</g>'


def burst_box(x, y, s=1.0, **_):
    return [x - 105 * s, y - 105 * s, 210 * s, 210 * s]


def _nc_layout(title, lines, w, fs):
    lines = [str(l) for l in (lines or [])]
    size = fs
    while size >= DATA_FLOOR:
        wr = [wl for l in lines for wl in _d_wrap(l, size, w - 56)]
        if all(_d_tw(l, size) <= w - 56 for l in wr): break
        size -= 2
    else: raise ValueError(f"note_card: {lines!r} does not fit {w} wide at the {DATA_FLOOR} px minimum; shorten it or raise w")
    tl = _d_wrap(title, size, w - 56) if title else []
    H = 54 + len(tl) * size * 1.2 + (10 if tl else 0) + len(wr) * size * 1.22
    return size, tl, wr, H


def note_card(x, y, s=1.0, title="", lines=None, w=480, fs=42, rot=0, mark=False, **_):
    """A small pinned note for supporting information, such as "Spread = $50.05 − $50.00 = 5 cents". (x, y) = centre. title: bold blue line. lines: list of lines, wrapped to w; text stays at 34 px or more. mark: yellow highlighter on the last line. rot: slight tilt in degrees."""
    size, tl, wr, H = _nc_layout(title, lines, w, fs)
    out = (f'<path d="M{-w / 2 + 16} {-H / 2} L{w / 2 - 14} {-H / 2 - 2} Q{w / 2} {-H / 2} {w / 2} {-H / 2 + 16} L{w / 2 + 2} {H / 2 - 16} Q{w / 2} {H / 2} {w / 2 - 16} {H / 2} L{-w / 2 + 14} {H / 2 + 2} Q{-w / 2} {H / 2} {-w / 2} {H / 2 - 16} L{-w / 2 - 2} {-H / 2 + 16} Q{-w / 2} {-H / 2} {-w / 2 + 16} {-H / 2} Z" '
           f'fill="{NOTE_FILL}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    out += f'<rect x="-46" y="{-H / 2 - 15:.1f}" width="92" height="30" rx="5" fill="{BLUE}" fill-opacity="0.75" stroke="{INK}" stroke-width="3"/>'
    yy = -H / 2 + 24
    for l in tl:
        yy += size * 1.0; out += _t(0, yy, l, size, 900, ED_BLUE); yy += size * 0.2
    if tl: yy += 10
    for i, l in enumerate(wr):
        yy += size * 1.0
        if mark and i == len(wr) - 1:
            lw = _d_tw(l, size) + 14
            out += f'<rect x="{-lw / 2:.1f}" y="{yy - size * 0.72:.1f}" width="{lw:.1f}" height="{size * 0.84:.1f}" rx="6" fill="#FFD45C" stroke="none"/>'
        out += _t(0, yy, l, size, 800, INK); yy += size * 0.22
    return _g(x, y, s, out, rot)


def note_card_box(x, y, s=1.0, title="", lines=None, w=480, fs=42, **_):
    H = _nc_layout(title, lines, w, fs)[3]
    return [x - w / 2 * s - 4, y - (H / 2 + 16) * s, w * s + 8, (H + 18) * s]


def trend_arrow(x, y, s=1.0, dir="up", length=240, width=110, text="", fs=56, **_):
    """A chunky market arrow: green pointing up, red pointing down. (x, y) = centre. text: short label to its right, such as "+20%". Add "reveal" with dir up or down so it grows."""
    col = UP if dir == "up" else DOWN; L = length / 2; hw = width / 2; sw = width * 0.28; hh = width * 0.62; k = -1 if dir == "up" else 1
    d = f"M{-sw:.1f} {-k * L:.1f} L{sw:.1f} {-k * L:.1f} L{sw:.1f} {k * (L - hh):.1f} L{hw:.1f} {k * (L - hh):.1f} L0 {k * L:.1f} L{-hw:.1f} {k * (L - hh):.1f} L{-sw:.1f} {k * (L - hh):.1f} Z"
    out = f'<path d="{d}" fill="{col}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    if text: out += _t(hw + 14, fs * 0.35, str(text), fs, 900, col, "start")
    return _g(x, y, s, out)


def trend_arrow_box(x, y, s=1.0, length=240, width=110, text="", fs=56, **_):
    tw = _d_tw(text, fs) + 18 if text else 0
    return [x - width / 2 * s - 4, y - length / 2 * s - 4, (width + tw) * s + 8, length * s + 8]


def trader(x, y, s=1.0, side="buy", mood="smile", acts=None, name="", look=0, color=None, **_):
    """A person who acts: same look as "person", with arms. (x, y) = between the feet. side: buy (green top) or sell (red top). name: small label under the feet, such as "Buyer". acts: [{"at","delay","pose","mood"}]; pose: down, raise, both, point (right arm in), point_l (left arm in), cheer, shrug; a small hop plays on each act unless "hop": false. mood: smile, happy, flat, sad, o, worried. look: -1 or 1 moves the eyes left or right."""
    c = color or {"buy": "#BFE6CF", "sell": "#F6C9C4"}.get(side, LB)
    Mouth = {"smile": "M-12 -168 Q0 -158 12 -168", "happy": "M-14 -170 Q0 -148 14 -170 Z", "flat": "M-11 -164 H11", "sad": "M-12 -158 Q0 -170 12 -158", "worried": "M-12 -160 Q-6 -166 0 -161 Q6 -156 12 -162", "o": ""}
    moods = [mood] + [a["mood"] for a in (acts or []) if a.get("mood")]
    mouths = ""
    for m in dict.fromkeys(moods):
        if m not in Mouth: raise ValueError(f"trader: mood {m!r}; use {', '.join(Mouth)}")
        body = f'<circle cx="0" cy="-162" r="8" fill="{INK}"/>' if m == "o" else f'<path d="{Mouth[m]}" fill="{"#FFFFFF" if m == "happy" else "none"}" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
        mouths += f'<g class="tm" data-m="{m}" opacity="{1 if m == mood else 0}">{body}</g>'
    ex = 4 * (look or 0)
    A = {"mood": mood, "acts": [dict(_m_at(a), pose=a.get("pose"), mood=a.get("mood"), hop=a.get("hop", True), dur=float(a.get("dur", 0.3))) for a in (acts or [])]}
    arm = lambda sx, ex_: f'<path d="M{sx} -112 Q{sx + (5 if sx > 0 else -5)} -84 {ex_} -58" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><path d="M{sx} -112 Q{sx + (5 if sx > 0 else -5)} -84 {ex_} -58" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round"/><circle cx="{ex_}" cy="-56" r="9" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>'
    inner = (f'<path d="M-46 0 V-90 Q-46 -130 0 -130 Q46 -130 46 -90 V0 Z" fill="{c}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<circle cx="0" cy="-178" r="40" fill="{PAPER}" stroke="{INK}" stroke-width="{SW}"/>'
             f'<circle cx="{-13 + ex}" cy="-184" r="5" fill="{INK}"/><circle cx="{13 + ex}" cy="-184" r="5" fill="{INK}"/>{mouths}'
             f'<g class="ta" data-side="L" data-sx="-44" data-sy="-110">{arm(-44, -52)}</g><g class="ta" data-side="R" data-sx="44" data-sy="-110">{arm(44, 52)}</g>')
    out = f'<ellipse cx="0" cy="4" rx="46" ry="7" fill="{INK}" opacity="0.10"/><g data-fx="trader" data-spec="{_m_attr(A)}">{inner}</g>'
    if name: out += _t(0, 46, str(name), round(36 / min(s, 1)), 900, UP if side == "buy" else DOWN if side == "sell" else INK)
    return _g(x, y, s, out)


def trader_box(x, y, s=1.0, name="", **_):
    return [x - 70 * s, y - 222 * s, 140 * s, (226 + (56 if name else 0)) * s]


def _ob_layout(asks, bids, w, rh, states, gap_min, gap_max):
    if not asks or not bids: raise ValueError("order_book: needs asks and bids")
    def nums(rows, where): return [[_d_num(r[0], "$", where), _d_num(r[1], "", where)] for r in rows]
    A, B = nums(asks, "order_book asks"), nums(bids, "order_book bids")
    for v, nm in ((A, "asks"), (B, "bids")):
        pr = [r[0] for r in v]
        if pr != sorted(pr, reverse=nm == "bids"): raise ValueError(f"order_book: {nm} go best price first (asks rising, bids falling): {pr}")
    sps = [A[0][0] - B[0][0]]; St = []
    for st in states or []:
        a2, b2 = nums(st.get("asks") or asks, "order_book states"), nums(st.get("bids") or bids, "order_book states")
        if len(a2) != len(A) or len(b2) != len(B): raise ValueError("order_book: each state must have the same number of rows")
        sps.append(a2[0][0] - b2[0][0]); St.append(dict(_m_at(st), dur=float(st.get("dur", 0.9)), asks=a2, bids=b2))
    if min(sps) <= 0: raise ValueError(f"order_book: the best ask must be above the best bid (spreads {sps})")
    gmin = float(gap_min); gmax = float(gap_max) if gap_max else (gmin if len(set(round(v, 6) for v in sps)) == 1 else gmin + 110)
    qmax = max(r[1] for v in [A, B] + [st["asks"] for st in St] + [st["bids"] for st in St] for r in v) or 1
    return A, B, St, sps, gmin, gmax, qmax


def order_book(x, y, s=1.0, asks=None, bids=None, w=620, rh=64, fs=46, title="Order book", example=True, states=None, show=None, flash=None, gap_min=76, gap_max=None, spread_range=None, spread_label=True, dec=2, **_):
    """A trading ladder: red asks above, green bids below, real numbers inside, and a highlighted spread band between the best ask and the best bid. (x, y) = centre of the band. asks, bids: rows of [price, shares], BEST PRICE FIRST (index 0 sits next to the band), e.g. "asks": [["50.05", 300], ["50.06", 500]]. states: [{"at","dur","asks","bids"}] move the prices and shares, so the spread narrows or widens and the band follows. show: {"bids": "chunk:N", "asks": "chunk:N", "band": "chunk:N"} when each part comes in (default: from the start); a value may be {"at","delay"}. flash: [{"at","side":"ask","row":0}] flashes a row. example: true writes "Example prices" in the header; use false only when the voice says every number or the scene labels them. spread_label: writes the live spread on the band. spread_range: [low, high] in dollars, the spreads that map to gap_min and gap_max; give two books the same range so their bands compare fairly."""
    A, B, St, sps, gmin, gmax, qmax = _ob_layout(asks, bids, w, rh, states, gap_min, gap_max)
    na, nb = len(A), len(B); head = 78; sub = 52; wl = w / 2; pad = 22; fq = max(DATA_FLOOR, fs - 8)
    if _d_tw("$00.00", fs) + _d_tw("0,000", fq) + 2 * pad + 20 > w: raise ValueError(f"order_book: w {w} is too narrow for the numbers at {fs} px; raise w")
    tA = head + sub + na * rh; tB = sub + nb * rh; g0 = 0
    S = {"asks": A, "bids": B, "states": St, "dec": dec, "qmax": qmax, "gmin": gmin, "gmax": gmax, "spmax": float(spread_range[1]) if spread_range else max(sps), "spmin": float(spread_range[0]) if spread_range else min(sps), "w": w, "rh": rh, "tA": tA, "tB": tB, "show": {k: _m_at(v if isinstance(v, dict) else {"at": v}) for k, v in (show or {}).items()}, "label": bool(spread_label),
         "flash": [dict(_m_at(f), side=f.get("side", "ask"), row=int(f.get("row", 0)), dur=float(f.get("dur", 0.7))) for f in (flash or [])]}
    def row(k, r, side):
        col, tint, bar_y = (DOWN, DOWN_TINT, 0) if side == "ask" else (UP, UP_TINT, 0)
        best = k == 0; bw = (w - 8) * 0.62 * r[1] / qmax; wt = 900
        return (f'<g class="obr" data-side="{side}" data-i="{k}">'
                f'<rect class="obb" data-nodraw="1" x="{wl - 4 - bw:.1f}" y="4" width="{bw:.1f}" height="{rh - 8}" rx="8" fill="{tint}" stroke="none"/>'
                + (f'<rect data-nodraw="1" x="-{wl - 8}" y="3" width="{w - 16}" height="{rh - 6}" rx="10" fill="none" stroke="{col}" stroke-width="5"/>' if best else "")
                + f'<rect class="obf" data-nodraw="1" x="-{wl - 8}" y="3" width="{w - 16}" height="{rh - 6}" rx="10" fill="{AMBER}" opacity="0" stroke="none"/>'
                + f'<text class="obp" x="{-wl + pad}" y="{rh / 2 + fs * 0.36:.1f}" font-family="Inter,sans-serif" font-size="{fs}" font-weight="{wt}" fill="{col}">{_m_fmt(r[0], dec, "$")}</text>'
                + f'<text class="obq" x="{wl - pad}" y="{rh / 2 + fq * 0.36:.1f}" text-anchor="end" font-family="Inter,sans-serif" font-size="{fq}" font-weight="800" fill="{INK}">{_m_fmt(r[1])}</text></g>')
    # top group: header, "Asks" line and ask rows, best ask at the bottom; it sits above the band and moves up as the band opens
    top = ""; yy = -tA
    ex = bool(example) and _d_tw(title, 40) + _d_tw("Example prices", 34) + 56 <= w
    if example and not ex: raise ValueError(f'order_book: w {w} cannot hold "{title}" and "Example prices" in the header; shorten the title, raise w, or set example false and label the scene')
    top += f'<path d="M{-wl} {yy + head} V{yy + 20} Q{-wl} {yy} {-wl + 20} {yy} H{wl - 20} Q{wl} {yy} {wl} {yy + 20} V{yy + head} Z" fill="{ED_BLUE}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    top += _t(-wl + pad, yy + 52, str(title), 40, 900, WHITE, "start")
    if ex: top += _t(wl - pad, yy + 50, "Example prices", 34, 800, "#FFE9A8", "end")
    yy += head
    asks_g = f'<text x="{-wl + pad}" y="{yy + 38}" font-family="Inter,sans-serif" font-size="36" font-weight="900" fill="{DOWN}">Asks: sellers</text><text x="{wl - pad}" y="{yy + 38}" text-anchor="end" font-family="Inter,sans-serif" font-size="34" font-weight="800" fill="#475569">Shares</text>'
    yy += sub
    for k in range(na - 1, -1, -1):
        asks_g += f'<g transform="translate(0 {yy:.1f})">{row(k, A[k], "ask")}</g>'; yy += rh
    bot = ""; yy = 0
    for k in range(nb):
        bot += f'<g transform="translate(0 {yy:.1f})">{row(k, B[k], "bid")}</g>'; yy += rh
    bot += f'<text x="{-wl + pad}" y="{yy + 38}" font-family="Inter,sans-serif" font-size="36" font-weight="900" fill="{UP}">Bids: buyers</text>'
    card = f'<rect class="obc" data-nodraw="1" x="{-wl}" y="{-tA}" width="{w}" height="{tA + tB}" rx="20" fill="{WHITE}" stroke="none"/>'
    edge = f'<rect class="obe" data-nodraw="1" x="{-wl}" y="{-tA}" width="{w}" height="{tA + tB}" rx="20" fill="none" stroke="{INK}" stroke-width="6"/>'
    band = (f'<g class="obband"><rect class="obbr" data-nodraw="1" x="{-wl + 5}" y="-30" width="{w - 10}" height="60" fill="{AMBER}" fill-opacity="0.75" stroke="none"/>'
            f'<path class="obla" d="M{-wl + 30} 0 L{-wl + 30} 0" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round" data-nodraw="1"/>'
            + (f'<text class="obl" x="20" y="16" text-anchor="middle" font-family="Inter,sans-serif" font-size="{42 if w >= 500 else 36}" font-weight="900" fill="{INK}">Spread</text>' if spread_label else "") + "</g>")
    out = f'<g data-fx="book" data-spec="{_m_attr(S)}">{card}<g class="obtop">{top}</g><g class="obasks">{asks_g}</g><g class="obbids">{bot}</g>{band}{edge}</g>'
    return _g(x, y, s, out)


def order_book_box(x, y, s=1.0, asks=None, bids=None, w=620, rh=64, states=None, gap_min=76, gap_max=None, **_):
    A, B, St, sps, gmin, gmax, qmax = _ob_layout(asks, bids, w, rh, states, gap_min, gap_max)
    tA = 78 + 52 + len(A) * rh + gmax / 2; tB = 52 + len(B) * rh + gmax / 2
    return [x - w / 2 * s - 4, y - tA * s - 4, w * s + 8, (tA + tB) * s + 8]


def _lc_stops(stops, n):
    R = _m_keys(stops) or [{"at": "chunk:0", "dur": 1.5, "upto": n - 1}]
    return [dict(_m_at(k), dur=float(k.get("dur", 1.5)), upto=float(k.get("upto", n - 1))) for k in R]


def live_chart(x, y, s=1.0, kind="candles", candles=None, points=None, unit="$", dec=2, w=860, h=620, stops=None, marks=None, ticks=None, title="", example=True, color="market", **_):
    """A price chart that draws itself over time. (x, y) = centre. kind: candles (candles: [[open, high, low, close], ...]) or line (points: [...]). stops: [{"at","delay","dur","upto"}]: by that chunk's time + dur the chart has reached index upto, so it stays in sync with the voice. marks: [{"i": 3, "dir": "up", "text": "Buyers"}]: a green up or red down arrow that pops when the chart reaches index i. ticks: price labels on the right axis. A price tag on the axis follows the latest price, green when rising, red when falling. example: true writes "Example prices"; use false only when the voice says every number. color (line): market (green up, red down) or blue."""
    where = "live_chart"; pre, suf = _m_unit(unit)
    if kind == "candles":
        C = [[_d_num(v, unit, where) for v in c] for c in (candles or [])]
        if not C or any(len(c) != 4 for c in C): raise ValueError(f"{where}: candles need [[open, high, low, close], ...]")
        for c in C:
            if not (c[2] <= min(c[0], c[3]) and c[1] >= max(c[0], c[3])): raise ValueError(f"{where}: candle {c} has a high or low outside its open and close")
        P = [c[3] for c in C]; lo, hi = min(c[2] for c in C), max(c[1] for c in C)
    elif kind == "line":
        P = [_d_num(v, unit, where) for v in (points or [])]
        if len(P) < 2: raise ValueError(f"{where}: a line needs at least 2 points")
        C = None; lo, hi = min(P), max(P)
    else: raise ValueError(f'{where}: kind {kind!r}; use "candles" or "line"')
    n = len(P); hw, hh = w / 2, h / 2; R = 150; top = -hh
    out = ""
    if title or example:
        if title: out += _t(-hw + 6, top + 40, str(title), 42, 900, INK, "start")
        if example:
            tw = _d_tw("Example prices", 36) + 30
            if title and _d_tw(title, 42) + tw + 20 > w: raise ValueError(f"{where}: the title and \"Example prices\" do not fit {w} wide; shorten the title")
            out += f'<rect x="{hw - tw:.1f}" y="{top + 2:.1f}" width="{tw:.1f}" height="54" rx="12" fill="{NOTE_FILL}" stroke="{INK}" stroke-width="4"/>' + _t(hw - tw / 2, top + 41, "Example prices", 36, 800, INK)
        top += 70
    plotL, plotR, plotT, plotB = -hw + 4, hw - R, top + 6, hh - 14
    ups = [m for m in (marks or []) if m.get("dir") == "up"]; dns = [m for m in (marks or []) if m.get("dir") != "up"]
    padT = 40 + (130 if dns else 0); padB = 30 + (130 if ups else 0)
    if plotB - plotT - padT - padB < 110: raise ValueError(f"{where}: h {h} leaves too little room for the plot; raise h or use fewer marks")
    span = (hi - lo) or 1.0; ky = (plotB - plotT - padT - padB) / span
    Y = lambda v: plotT + padT + (hi - v) * ky
    slot = (plotR - plotL) / n; X = lambda i: plotL + slot * (i + 0.5)
    tk = ticks if ticks is not None else [lo, (lo + hi) / 2, hi]
    out += f'<path d="M{plotR:.1f} {plotT:.1f} L{plotR:.1f} {plotB:.1f} L{plotL:.1f} {plotB:.1f}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
    for v in tk:
        vv = _d_num(v, unit, where); yy = Y(vv)
        out += f'<path d="M{plotL:.1f} {yy:.1f} L{plotR:.1f} {yy:.1f}" fill="none" stroke="{DATA_RULE}" stroke-width="4" stroke-dasharray="4 14" stroke-linecap="round"/>' + _t(plotR + 10, yy + 12, _m_fmt(vv, dec, pre, suf), DATA_FLOOR, 800, "#334155", "start")
    S = {"u0": -1 if kind == "candles" else 0, "stops": _lc_stops(stops, n), "dec": dec, "pre": pre, "suf": suf, "n": n, "kind": kind, "P": P, "Y": [round(Y(v), 2) for v in P], "X": [round(X(i), 2) for i in range(n)], "plotR": plotR}
    bw = min(slot * 0.62, 70); plot = ""; boxes = []
    if kind == "candles":
        S["C"] = C; S["YC"] = [[round(Y(v), 2) for v in c] for c in C]
        for i, c in enumerate(C):
            up = c[3] >= c[0]; col = UP if up else DOWN; cx = X(i)
            plot += (f'<g class="cc" data-i="{i}" opacity="0"><path class="cw" data-nodraw="1" d="M{cx:.1f} {Y(c[1]):.1f} L{cx:.1f} {Y(c[2]):.1f}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
                     f'<rect class="cb" data-nodraw="1" x="{cx - bw / 2:.1f}" y="{min(Y(c[0]), Y(c[3])):.1f}" width="{bw:.1f}" height="{max(6, abs(Y(c[3]) - Y(c[0]))):.1f}" rx="5" fill="{col}" stroke="{INK}" stroke-width="5"/></g>')
            boxes.append((cx - bw / 2, Y(c[1]), cx + bw / 2, Y(c[2])))
    else:
        for i in range(n - 1):
            col = ED_BLUE if color == "blue" else (UP if P[i + 1] >= P[i] else DOWN)
            plot += f'<path class="cs" data-i="{i}" data-nodraw="1" d="M{X(i):.1f} {Y(P[i]):.1f} L{X(i + 1):.1f} {Y(P[i + 1]):.1f}" pathLength="1" stroke-dasharray="0 1" fill="none" stroke="{col}" stroke-width="11" stroke-linecap="round" opacity="0"/>'
        plot += f'<circle class="cd" data-nodraw="1" r="15" fill="{ED_BLUE}" stroke="{INK}" stroke-width="5"/>'
        boxes = [(X(i) - 16, Y(P[i]) - 16, X(i) + 16, Y(P[i]) + 16) for i in range(n)]
    # marks, each with its text on the far side of the arrow; nothing may touch another mark or a candle
    placed = []; mk = ""
    for m in marks or []:
        i = int(m.get("i", 0)); up = m.get("dir") == "up"; col = UP if up else DOWN
        if not 0 <= i < n: raise ValueError(f"{where}: mark index {i} is outside the chart")
        cx = X(i); edge = (Y(C[i][2]) if C else Y(P[i])) + 14 if up else (Y(C[i][1]) if C else Y(P[i])) - 14
        tail = edge + 72 if up else edge - 72; head_w = 26; d = 1 if up else -1
        arrow_svg = (f'<path d="M{cx - 11:.1f} {tail:.1f} L{cx + 11:.1f} {tail:.1f} L{cx + 11:.1f} {edge + d * 30:.1f} L{cx + head_w:.1f} {edge + d * 30:.1f} L{cx:.1f} {edge:.1f} L{cx - head_w:.1f} {edge + d * 30:.1f} L{cx - 11:.1f} {edge + d * 30:.1f} Z" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
        rects = [(cx - head_w, min(edge, tail), cx + head_w, max(edge, tail))]; txt = ""
        if m.get("text"):
            tw = _d_tw(m["text"], 36); tx = min(max(cx, plotL + tw / 2), plotR - tw / 2 - 4); ty = tail + 38 if up else tail - 12
            txt = _t(tx, ty, str(m["text"]), 36, 900, col); rects.append((tx - tw / 2, ty - 30, tx + tw / 2, ty + 6))
        for r in rects:
            if r[1] < plotT or r[3] > plotB: raise ValueError(f"{where}: the mark at index {i} runs out of the plot; raise h or move it")
            hit = lambda a, b: a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]
            if any(hit(r, q) for q in placed): raise ValueError(f"{where}: the mark at index {i} overlaps another mark; move it or shorten its text")
            if any(hit(r, q) for j, q in enumerate(boxes) if j != i): raise ValueError(f"{where}: the mark at index {i} overlaps the chart at another index; move it to a higher or lower point")
        placed += rects
        mk += f'<g class="cm" data-i="{i}" data-ax="{cx:.1f}" data-ay="{edge:.1f}" opacity="0">{arrow_svg}{txt}</g>'
    tag_w = R - 2
    tag = (f'<g class="ct" opacity="0"><path d="M{plotL:.1f} 0 L{plotR:.1f} 0" fill="none" stroke="{INK}" stroke-width="3" stroke-dasharray="10 12"/>'
           f'<rect class="ctr" x="{plotR + 4:.1f}" y="-29" width="{tag_w:.1f}" height="58" rx="10" fill="{UP}" stroke="{INK}" stroke-width="4"/>'
           f'<text class="ctt" x="{plotR + 4 + tag_w / 2:.1f}" y="13" text-anchor="middle" font-family="Inter,sans-serif" font-size="36" font-weight="900" fill="{WHITE}"></text></g>')
    out += f'<g data-fx="chart" data-spec="{_m_attr(S)}">{plot}{tag}{mk}</g>'
    return _g(x, y, s, out)


def live_chart_box(x, y, s=1.0, w=860, h=620, **_):
    return [x - w / 2 * s - 4, y - h / 2 * s - 4, w * s + 8, h * s + 8]


def waterfall(x, y, s=1.0, steps=None, unit="$", comp="", dec=0, w=860, h=720, rider=None, connect=True, **_):
    """A waterfall chart that builds bar by bar, each number ticking up as its bar grows. (x, y) = centre. steps: [{"label","value","kind","at","delay","dur"}]; kind: total (blue, from zero), down (red, drops from the running level), up (green). at: the chunk that bar starts ("chunk:N"). comp: "K" or "M" shows $500K. connect: false drops the dashed line between bars, for a plain comparison of two bars. Labels too wide for one row drop to two staggered rows. rider: {"s","outfit","moods":{step index: mood}} puts a small Ledger on the newest bar, hopping down as the money falls. Show only numbers the voice or the script supports."""
    where = "waterfall"; steps = steps or []; pre, suf = _m_unit(unit)
    if not 1 <= len(steps) <= 8: raise ValueError(f"{where}: {len(steps)} steps; use 1 to 8")
    n = len(steps); hw, hh = w / 2, h / 2; slot = (w - 12) / n
    labels = [st.get("label", "") for st in steps]; stagger = 0
    try: fc, wrapped = _d_fit(labels, slot - 6, 44, 3, where)
    except ValueError:   # too tight in one row: every second label drops to a second row, so each gets about two slots of width
        fc, wrapped = _d_fit(labels, slot * 2 - 20, 40, 2, where)
        stagger = max(len(l) for l in wrapped[::2]) * fc * 1.16 + 6
    nl = max(len(l) for l in wrapped); base = hh - nl * fc * 1.16 - 14 - stagger
    level = 0.0; levels = []; vals = []
    for st in steps:
        v = _d_num(st["value"], unit, where); kind = st.get("kind", "total"); a = level if kind != "total" else 0.0
        if kind == "total": b = v; show = v
        elif kind == "down": b = level - abs(v); show = -abs(v)
        elif kind == "up": b = level + abs(v); show = abs(v)
        else: raise ValueError(f"{where}: kind {kind!r}; use total, down or up")
        levels.append((a, b)); vals.append(show); level = b
    shown = [_m_fmt(v, dec, pre, suf, comp) for v in vals]; fv = 62
    while fv > DATA_FLOOR and max(_d_tw(t, fv) for t in shown) > slot - 8: fv -= 2
    if max(_d_tw(t, fv) for t in shown) > slot - 8: raise ValueError(f"{where}: values {shown!r} do not fit {slot:.0f} wide at the {DATA_FLOOR} px minimum; use comp \"K\" or fewer steps")
    rs = float((rider or {}).get("s", 0.56)); rh = 232 * rs + 6 if rider else 0; lh = fv * 1.08 + 10
    hi = max(max(l) for l in levels); ptop = -hh + lh + rh
    if base - ptop < 110: raise ValueError(f"{where}: h {h} leaves too little room for the bars; raise h")
    ky = (base - ptop) / (hi or 1.0); Y = lambda v: base - v * ky
    X = [-hw + 6 + slot * (i + 0.5) for i in range(n)]; bw = min(slot * 0.72, 170)
    out = f'<path d="{_wobble_line(-hw + 2, hw - 2, base, 3)}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
    S = {"steps": [], "dec": dec, "pre": pre, "suf": suf, "comp": comp, "fv": fv}; bars = ""; conn = ""
    for i, st in enumerate(steps):
        ya, yb = Y(levels[i][0]), Y(levels[i][1]); kind = st.get("kind", "total"); col = {"total": ED_BLUE, "down": DOWN, "up": UP}[kind]
        S["steps"].append(dict(_m_at(st), dur=float(st.get("dur", 0.8)), a=round(ya, 2), b=round(yb, 2), v=vals[i]))
        cl = ""
        if i and connect:
            yc = Y(levels[i - 1][1])
            cl = f'<path d="M{X[i - 1] + bw / 2:.1f} {yc:.1f} L{X[i] - bw / 2:.1f} {yc:.1f}" fill="none" stroke="{INK}" stroke-width="5" stroke-dasharray="10 10" stroke-linecap="round"/>'
        lbl = "".join(_t(min(max(X[i], -hw + _d_tw(l, fc) / 2), hw - _d_tw(l, fc) / 2), base + 8 + (stagger if i % 2 else 0) + fc * 0.92 + j * fc * 1.16, l, round(fc), 800, INK) for j, l in enumerate(wrapped[i]))
        bars += (f'<g class="wf" data-i="{i}" opacity="0">{cl}<rect class="wb" data-nodraw="1" x="{X[i] - bw / 2:.1f}" y="{min(ya, yb):.1f}" width="{bw:.1f}" height="{abs(yb - ya):.1f}" rx="8" fill="{col}" stroke="{INK}" stroke-width="6"/>{lbl}'
                 + f'<text class="wv" x="{X[i]:.1f}" y="{min(ya, yb) - 10:.1f}" text-anchor="middle" font-family="Inter,sans-serif" font-size="{fv}" font-weight="900" fill="{col if kind != "total" else INK}">{shown[i]}</text></g>')
    out += f'<g data-fx="wf" data-spec="{_m_attr(S)}">{bars}</g>'
    if rider:
        outfit = rider.get("outfit", "suit"); moods = {int(k): v for k, v in (rider.get("moods") or {}).items()}
        tops = [min(Y(levels[i][0]), Y(levels[i][1])) - lh + 4 for i in range(n)]
        keys = []
        for i, st in enumerate(steps):
            q = dict(_m_at(st), to=[round(X[i], 1), round(tops[i], 1)], dur=float(st.get("dur", 0.8)), ease="out" if i == 0 else "inout", arc=0 if i == 0 else 90)
            keys.append(q)
        start = [X[0], base - lh + 4]
        faces = ""; chg = sorted(moods) or [0]
        cur_keys = [0] + [k for k in chg if k > 0]
        for j, k in enumerate(cur_keys):
            m = moods.get(k, rider.get("mood", "smile")); attrs = ""
            if j: attrs += f' data-at="{_m_at(steps[k])["at"]}" data-pop="cut"'
            if j + 1 < len(cur_keys): attrs += f' data-until="{_m_at(steps[cur_keys[j + 1]])["at"]}"'
            faces += f'<g{attrs}>{ledger(start[0], start[1], rs, mood=m, arm=rider.get("arm", "down"), outfit=outfit)}</g>'
        spec = {"x": start[0], "y": start[1], "move": keys, "hide": _m_at(steps[0])}
        out += f'<g data-fx="m" data-spec="{_m_attr(spec)}">{faces}</g>'
    return _g(x, y, s, out)


def waterfall_box(x, y, s=1.0, w=860, h=720, **_):
    return [x - w / 2 * s - 4, y - h / 2 * s - 4, w * s + 8, h * s + 8]


def fill_grid(x, y, s=1.0, n=100, cols=10, capacity=None, size=64, gap=10, cell="person", fills=None, fades=None, start=0, color="blue", over_color="red", **_):
    """A grid of small people or rooms that fills one by one. (x, y) = centre. n: cells; cols: per row; capacity: cells from this index on go on their own row below, in over_color (6 bookings too many). cell: person or square. fills: [{"at","delay","dur","upto"}]: by then cells up to number upto are filled. fades: [{"at","delay","dur","cells":[...]}]: those cells empty out again, leaving a red outline. start: cells filled from the first frame."""
    cap = capacity if capacity is not None else n
    if n > 400 or cols < 1: raise ValueError("fill_grid: use at most 400 cells")
    rows = math.ceil(cap / cols); over = n - cap; G = size + gap; W = cols * G - gap; extra = (G + 14) if over > 0 else 0; H = rows * G - gap + extra
    col = {"blue": ED_BLUE, "green": UP, "red": DOWN, "amber": AMBER}.get(color, color); oc = {"blue": ED_BLUE, "green": UP, "red": DOWN, "amber": AMBER}.get(over_color, over_color)
    gone = {c for f in (fades or []) for c in f.get("cells", [])}   # cells that empty out leave a red outline, so the viewer can find them
    def shape(c, solid, edge=GHOST):
        z = size / 64
        st = f'fill="{c}" stroke="{INK}" stroke-width="{3.5:.1f}"' if solid else f'fill="none" stroke="{edge}" stroke-width="{3.5 if edge == GHOST else 5}"'
        if cell == "square": return f'<rect x="{-size / 2 + 3:.1f}" y="{-size / 2 + 3:.1f}" width="{size - 6:.1f}" height="{size - 6:.1f}" rx="{8 * z:.1f}" {st}/>'
        return f'<circle cy="{-15 * z:.1f}" r="{12 * z:.1f}" {st}/><path d="M{-19 * z:.1f} {27 * z:.1f} V{12 * z:.1f} Q{-19 * z:.1f} {-1 * z:.1f} 0 {-1 * z:.1f} Q{19 * z:.1f} {-1 * z:.1f} {19 * z:.1f} {12 * z:.1f} V{27 * z:.1f} Z" {st}/>'
    out = ""; ghost = ""; solid = ""
    for i in range(n):
        if i < cap: cx = -W / 2 + G * (i % cols) + size / 2; cy = -H / 2 + G * (i // cols) + size / 2
        else: cx = -W / 2 + G * (i - cap) + size / 2; cy = -H / 2 + G * rows + 14 + size / 2
        if i < cap: ghost += f'<g transform="translate({cx:.1f} {cy:.1f})">{shape(col, False, DOWN if i in gone else GHOST)}</g>'
        solid += f'<g class="gc" data-i="{i}" data-ax="{cx:.1f}" data-ay="{cy:.1f}" opacity="0"><g transform="translate({cx:.1f} {cy:.1f})">{shape(oc if i >= cap else col, True)}</g></g>'
    S = {"start": start, "fills": [dict(_m_at(f), dur=float(f.get("dur", 1.0)), upto=float(f.get("upto", n))) for f in (fills or [])],
         "fades": [dict(_m_at(f), dur=float(f.get("dur", 1.0)), cells=list(f.get("cells", []))) for f in (fades or [])]}
    out = f'{ghost}<g data-fx="grid" data-spec="{_m_attr(S)}">{solid}</g>'
    return _g(x, y, s, out)


def fill_grid_box(x, y, s=1.0, n=100, cols=10, capacity=None, size=64, gap=10, **_):
    cap = capacity if capacity is not None else n
    rows = math.ceil(cap / cols); G = size + gap; W = cols * G - gap; H = rows * G - gap + ((G + 14) if n > cap else 0)
    return [x - W / 2 * s - 4, y - H / 2 * s - 4, W * s + 8, H * s + 8]


PRESETS.update({"counter": (counter, counter_box), "order_chip": (order_chip, order_chip_box), "coin": (coin, None), "coin_stream": (coin_stream, coin_stream_box), "burst": (burst, burst_box),
                "note_card": (note_card, note_card_box), "trend_arrow": (trend_arrow, trend_arrow_box), "trader": (trader, trader_box), "order_book": (order_book, order_book_box),
                "live_chart": (live_chart, live_chart_box), "waterfall": (waterfall, waterfall_box), "fill_grid": (fill_grid, fill_grid_box)})
HALF.update({"coin": (36, 36)})


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


def summary_pointer(spec):
    """How-to summary pointer (Hoang, 1 Nov 2026, opt-in): a scene with "pointer": true (or {"s", "outfit", "lanyard", "mood"})
    gets a small Ledger left of the 4-box summary diagram who points at each real (non-ghost) flow_box while the voice names
    it: one Ledger per box, placed so his pointing hand touches the box's left edge at mid-height, shown from that box's
    "at" chunk until the next box's (pop "cut", so he steps box to box in sync with the voice). The boxes must leave him
    room: flow_box w 700 centred at x 580 (left edge 230); he then stands in x 60-200, inside the safe area, off the text."""
    items = list(spec.get("items", [])); pt = spec.get("pointer")
    if not pt: return items
    pt = pt if isinstance(pt, dict) else {}; ps = float(pt.get("s", 0.8))
    boxes = [it for it in items if it.get("p") == "flow_box" and not it.get("ghost")]
    for k, bx in enumerate(boxes):
        left = bx["x"] - bx.get("w", 860) * bx.get("s", 1.0) / 2
        led = {"p": "ledger", "id": f"ptr{k + 1}", "x": round(left - 107 * ps - 6), "y": round(bx["y"] + 88 * ps), "s": ps,
               "outfit": pt.get("outfit", "suit"), "mood": pt.get("mood", "smile"), "arm": "point", "lanyard": bool(pt.get("lanyard", False))}
        if k and bx.get("at"): led["at"] = bx["at"]; led["pop"] = "cut"
        if k + 1 < len(boxes) and boxes[k + 1].get("at"): led["until"] = boxes[k + 1]["at"]
        items.append(led)
    return items


def scene_body(spec):
    # items sit in <g class="content"> so the renderer can auto-fit the frame to the drawn subject (not the background)
    def _attrs(it):   # anim "wobble" (29 Oct 2026): the renderer sways the item +-amp degrees about its (x, y), hz times a second
        a = f' data-p="{it["p"]}"'
        if it.get("anim") or it.get("at") or it.get("until"): a += f' data-ax="{_f(it["x"])}" data-ay="{_f(it["y"])}"'
        if it.get("anim"): a += f' data-anim="{it["anim"]}" data-amp="{it.get("amp", 4)}" data-hz="{it.get("hz", 1.1)}"'
        if it.get("at") and it["p"] not in SELF_TIMED: a += f' data-at="{it["at"]}"'   # "chunk:N": pops in when caption chunk N of this scene starts
        if it.get("until"): a += f' data-until="{it["until"]}"'   # "chunk:N" (30 Oct 2026): hidden from the start of caption chunk N
        if it.get("pop"): a += f' data-pop="{it["pop"]}"'   # "cut": appears at once on its chunk, no fade or scale (a state swap)
        return a
    tint = spec.get("tint")   # {"color", "opacity"}: a wash over the whole scene (dim cool night, warm morning); drawn over the content
    tint_svg = f'<rect class="tint" x="-3000" y="-3000" width="7080" height="7840" fill="{tint["color"]}" fill-opacity="{tint.get("opacity", 0.3)}" stroke="none"/>' if tint else ""
    items = summary_pointer(spec); lit = [it for it in items if it.get("lit")]   # "lit": drawn above the tint (chat bubbles stay bright at night)
    return (bg_svg(spec.get("bg", "paper")) + '<g class="content">' + "".join(_m_wrap(it, f'<g{_attrs(it)}>{item_svg(it)}</g>') for it in items if not it.get("lit")) + '</g>'
            + tint_svg + ('<g class="lit">' + "".join(_m_wrap(it, f'<g{_attrs(it)}>{item_svg(it)}</g>') for it in lit) + '</g>' if lit else ""))


def scene_svg(spec):
    """Full 1080x1920 SVG in the layout make_scenes_json.py expects (art inside <g filter="url(#r)">)."""
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">'
            '<defs><filter id="r" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="4"/>'
            '<feDisplacementMap in="SourceGraphic" scale="5"/></filter></defs>'
            f'<rect width="1080" height="1920" fill="{PAPER}"/><g filter="url(#r)">{scene_body(spec)}</g></svg>')


if __name__ == "__main__" and "--list" in sys.argv:
    print("Backgrounds (scene 'bg'):", ", ".join(BACKGROUNDS))
    print("Ledger: mood", MOODS, "| arm", ARMS, "| larm", LARMS, "| outfit", OUTFITS, "| tilt (deg), flip (true faces left), gaze", list(GAZES)[1:])
    for k, v in PRESET_HELP.items():
        print(f"- {k}: {v.splitlines()[0] if v else ''}")
