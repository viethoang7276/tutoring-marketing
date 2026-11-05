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
        if it.get("at"): a += f' data-at="{it["at"]}"'   # "chunk:N": pops in when caption chunk N of this scene starts
        if it.get("until"): a += f' data-until="{it["until"]}"'   # "chunk:N" (30 Oct 2026): hidden from the start of caption chunk N
        if it.get("pop"): a += f' data-pop="{it["pop"]}"'   # "cut": appears at once on its chunk, no fade or scale (a state swap)
        return a
    tint = spec.get("tint")   # {"color", "opacity"}: a wash over the whole scene (dim cool night, warm morning); drawn over the content
    tint_svg = f'<rect class="tint" x="-3000" y="-3000" width="7080" height="7840" fill="{tint["color"]}" fill-opacity="{tint.get("opacity", 0.3)}" stroke="none"/>' if tint else ""
    items = summary_pointer(spec); lit = [it for it in items if it.get("lit")]   # "lit": drawn above the tint (chat bubbles stay bright at night)
    return (bg_svg(spec.get("bg", "paper")) + '<g class="content">' + "".join(f'<g{_attrs(it)}>{item_svg(it)}</g>' for it in items if not it.get("lit")) + '</g>'
            + tint_svg + ('<g class="lit">' + "".join(f'<g{_attrs(it)}>{item_svg(it)}</g>' for it in lit) + '</g>' if lit else ""))


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
