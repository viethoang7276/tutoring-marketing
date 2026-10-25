import os, sys
D = os.path.dirname(os.path.abspath(__file__))
INK = "#0F172A"; BLUE = "#467DE3"; NAVY = "#222C3D"; PAPER = "#FBFAF6"
LB = "#C9D8F5"; GOLD = "#C2922F"; SKY = "#E8F0FC"; GREY = "#9AA3B2"

def ledger(x, y, s=1.0, mood="smile", tilt=0, arm=None):
    mouths = {
        "smile": '<path d="M106 134 Q120 146 134 134" fill="none" stroke="%s" stroke-width="4.5" stroke-linecap="round"/>' % INK,
        "frown": '<path d="M107 140 Q120 130 133 140" fill="none" stroke="%s" stroke-width="4.5" stroke-linecap="round"/>' % INK,
        "flat": '<path d="M108 137 L132 137" fill="none" stroke="%s" stroke-width="4.5" stroke-linecap="round"/>' % INK,
        "sad": '<path d="M107 140 Q120 131 133 140" fill="none" stroke="%s" stroke-width="4.5" stroke-linecap="round"/>' % INK,
        "o": '<ellipse cx="120" cy="137" rx="6" ry="7" fill="%s"/>' % INK,
    }
    brows = ""
    if mood == "frown":
        brows = '<path d="M93 96 L109 101" stroke="%s" stroke-width="4" stroke-linecap="round"/><path d="M147 96 L131 101" stroke="%s" stroke-width="4" stroke-linecap="round"/>' % (INK, INK)
    if mood == "sad":
        brows = '<path d="M93 101 L109 95" stroke="%s" stroke-width="4" stroke-linecap="round"/><path d="M147 101 L131 95" stroke="%s" stroke-width="4" stroke-linecap="round"/>' % (INK, INK)
    if mood in ("flat", "o"):
        brows = '<path d="M93 99 Q101 94 109 98" fill="none" stroke="%s" stroke-width="4" stroke-linecap="round"/><path d="M131 98 Q139 94 147 99" fill="none" stroke="%s" stroke-width="4" stroke-linecap="round"/>' % (INK, INK)
    right_arm = '<path d="M178 152 Q190 172 186 188" fill="none" stroke="%s" stroke-width="13" stroke-linecap="round"/><path d="M178 152 Q190 172 186 188" fill="none" stroke="%s" stroke-width="8" stroke-linecap="round"/><circle cx="186" cy="190" r="9" fill="%s" stroke="%s" stroke-width="3"/>' % (INK, PAPER, PAPER, INK)
    if arm == "up":  # right arm raised, pointing forward/up
        right_arm = '<path d="M180 150 Q205 132 222 112" fill="none" stroke="%s" stroke-width="13" stroke-linecap="round"/><path d="M180 150 Q205 132 222 112" fill="none" stroke="%s" stroke-width="8" stroke-linecap="round"/><circle cx="224" cy="109" r="9" fill="%s" stroke="%s" stroke-width="3"/>' % (INK, PAPER, PAPER, INK)
    if arm == "hold":  # right arm bent forward holding something at (206,150)
        right_arm = '<path d="M180 152 Q200 170 206 152" fill="none" stroke="%s" stroke-width="13" stroke-linecap="round"/><path d="M180 152 Q200 170 206 152" fill="none" stroke="%s" stroke-width="8" stroke-linecap="round"/><circle cx="207" cy="149" r="9" fill="%s" stroke="%s" stroke-width="3"/>' % (INK, PAPER, PAPER, INK)
    return f'''<g transform="translate({x} {y}) scale({s}) translate(-120 -230)">
<ellipse cx="120" cy="236" rx="46" ry="7" fill="{INK}" opacity="0.10"/>
<line x1="102" y1="186" x2="102" y2="210" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>
<line x1="138" y1="186" x2="138" y2="210" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>
<rect x="88" y="208" width="29" height="14" rx="7" fill="{INK}"/><rect x="123" y="208" width="29" height="14" rx="7" fill="{INK}"/>
<path d="M62 152 Q50 172 54 188" fill="none" stroke="{INK}" stroke-width="13" stroke-linecap="round"/><path d="M62 152 Q50 172 54 188" fill="none" stroke="{PAPER}" stroke-width="8" stroke-linecap="round"/><circle cx="54" cy="190" r="9" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>
<g transform="rotate({tilt} 120 198)">
<rect x="52" y="38" width="136" height="154" rx="18" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>
<line x1="70" y1="46" x2="70" y2="184" stroke="{INK}" stroke-width="3.5" opacity="0.45"/><line x1="74" y1="46" x2="74" y2="184" stroke="{INK}" stroke-width="1.5" opacity="0.25"/>
<path d="M150 34 h18 v26 l-9 -7 -9 7 z" fill="{BLUE}"/>
<rect x="86" y="58" width="60" height="6" rx="3" fill="#E6E3DA"/><rect x="86" y="70" width="60" height="6" rx="3" fill="#E6E3DA"/><rect x="86" y="82" width="40" height="6" rx="3" fill="#E6E3DA"/>
<path d="M54.5 150 L185.5 150 L185.5 174 Q185.5 189.5 170 189.5 L70 189.5 Q54.5 189.5 54.5 174 Z" fill="{NAVY}"/>
<path d="M108 150 L120 168 L116 173 L102 154 Z" fill="#FFF" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/><path d="M132 150 L120 168 L124 173 L138 154 Z" fill="#FFF" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>
<path d="M114 152 L126 152 L129 161 L111 161 Z" fill="{BLUE}"/><path d="M112 162 L128 162 L124 184 L120 189 L116 184 Z" fill="{BLUE}"/>
<circle cx="102" cy="110" r="7.5" fill="{INK}"/><circle cx="104.5" cy="107.5" r="2.2" fill="#FFF"/>
<circle cx="138" cy="110" r="7.5" fill="{INK}"/><circle cx="140.5" cy="107.5" r="2.2" fill="#FFF"/>
{brows}{mouths[mood]}
</g>{right_arm}</g>'''

def ticket(x, y, s=1.0, rot=0, faded=False):
    op = ' opacity="0.35" stroke-dasharray="14 10"' if faded else ""
    fill = "none" if faded else GOLD
    return f'''<g transform="translate({x} {y}) rotate({rot}) scale({s})"><g{op}>
<path d="M-110 -55 H110 V-20 A20 20 0 0 0 110 20 V55 H-110 V20 A20 20 0 0 0 -110 -20 Z" fill="{fill}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
<line x1="45" y1="-50" x2="45" y2="50" stroke="{INK}" stroke-width="4" stroke-dasharray="8 8"/>
<path d="M-40 -22 l9 18 20 3 -14 14 3 20 -18 -9 -18 9 3 -20 -14 -14 20 -3 z" fill="{PAPER if not faded else 'none'}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
<path d="M70 -18 v30 m0 -30 l18 -6 v30" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/><circle cx="64" cy="13" r="6" fill="{INK}"/><circle cx="82" cy="7" r="6" fill="{INK}"/>
</g></g>'''

def frame(body, bg=PAPER):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
<defs><filter id="r" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="5"/></filter>
<pattern id="grain" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="0.6" fill="{INK}" opacity="0.05"/></pattern></defs>
<rect width="1080" height="1920" fill="{bg}"/><rect width="1080" height="1920" fill="url(#grain)"/>
<g filter="url(#r)">{body}</g></svg>'''

ground = lambda y=1480: f'<path d="M60 {y} Q540 {y-14} 1020 {y}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'

scenes = []
# 1 bought ticket: Ledger happy holding a ticket, stage lights and notes
scenes.append(ground() + f'''
<path d="M180 640 L330 1040 M900 640 L750 1040" stroke="{GOLD}" stroke-width="5" opacity="0.5"/>
<path d="M180 640 L330 1040 L120 1040 Z" fill="{GOLD}" opacity="0.10"/><path d="M900 640 L750 1040 L960 1040 Z" fill="{GOLD}" opacity="0.10"/>
<path d="M250 820 v70 m0 -70 l40 -12 v70" fill="none" stroke="{BLUE}" stroke-width="7" stroke-linecap="round"/><circle cx="240" cy="892" r="13" fill="{BLUE}"/><circle cx="280" cy="880" r="13" fill="{BLUE}"/>
<path d="M830 760 v60" stroke="{BLUE}" stroke-width="7" stroke-linecap="round"/><path d="M830 760 q30 6 26 34" fill="none" stroke="{BLUE}" stroke-width="7" stroke-linecap="round"/><circle cx="820" cy="822" r="13" fill="{BLUE}"/>
''' + ledger(470, 1460, 2.6, "smile", arm="hold") + ticket(760, 1030, 1.15, -12))
# 2 rain and unwell: window with rain, Ledger frown with a scarf/thermometer
rain = "".join(f'<line x1="{x}" y1="{y}" x2="{x-18}" y2="{y+60}" stroke="{BLUE}" stroke-width="6" stroke-linecap="round"/>' for x in range(260, 860, 70) for y in (760, 880, 1000) )
scenes.append(ground() + f'''
<rect x="200" y="600" width="680" height="520" rx="10" fill="{SKY}" stroke="{INK}" stroke-width="7"/>
<line x1="540" y1="600" x2="540" y2="1120" stroke="{INK}" stroke-width="7"/><line x1="200" y1="860" x2="880" y2="860" stroke="{INK}" stroke-width="7"/>
<path d="M300 720 q20 -60 90 -50 q30 -50 100 -20 q70 -10 80 50 q50 10 40 60 H300 q-50 -10 0 -40 z" fill="{GREY}" opacity="0.55" stroke="{INK}" stroke-width="5"/>
<path d="M600 700 q20 -50 80 -40 q40 -40 100 0 q50 10 40 60 H600 q-40 -10 0 -20 z" fill="{GREY}" opacity="0.55" stroke="{INK}" stroke-width="5"/>
{rain}
''' + ledger(540, 1470, 2.5, "sad", tilt=4) + f'<path d="M410 1295 q130 36 260 0" fill="none" stroke="#E2928B" stroke-width="30" stroke-linecap="round"/>' + f'<g transform="translate(760 1230) rotate(25)"><rect x="-12" y="-80" width="24" height="120" rx="12" fill="#fff" stroke="{INK}" stroke-width="5"/><circle cx="0" cy="48" r="20" fill="#E2928B" stroke="{INK}" stroke-width="5"/><line x1="0" y1="-50" x2="0" y2="40" stroke="#E2928B" stroke-width="8"/></g>')
# 3 I already paid: Ledger with umbrella at the door, thought bubble with ticket
scenes.append(ground() + f'''
<rect x="700" y="760" width="250" height="720" rx="6" fill="{LB}" stroke="{INK}" stroke-width="7"/><circle cx="905" cy="1130" r="12" fill="{INK}"/>
<path d="M150 700 q-20 -70 60 -80 q20 -70 110 -40 q60 -60 130 0 q90 -10 80 70 q60 30 0 80 q-30 60 -120 30 q-60 50 -130 0 q-110 10 -130 -60 z" fill="#fff" stroke="{INK}" stroke-width="6"/>
<circle cx="360" cy="860" r="22" fill="#fff" stroke="{INK}" stroke-width="5"/><circle cx="400" cy="930" r="13" fill="#fff" stroke="{INK}" stroke-width="5"/>
<path d="M330 1080 q140 -150 280 0 z" fill="{BLUE}" stroke="{INK}" stroke-width="6"/><line x1="470" y1="1060" x2="470" y2="1300" stroke="{INK}" stroke-width="7"/>
''' + ticket(340, 660, 0.85, 6) + ledger(470, 1470, 2.4, "frown"))
# 4 gone either way: two paths, door vs sofa, faded ticket above
scenes.append(ground() + f'''
<path d="M540 1480 L250 1150 M540 1480 L830 1150" stroke="{INK}" stroke-width="5" stroke-dasharray="20 16"/>
<rect x="140" y="830" width="200" height="320" rx="6" fill="{LB}" stroke="{INK}" stroke-width="6"/><circle cx="305" cy="1000" r="10" fill="{INK}"/>
<path d="M720 1060 h240 v-70 q0 -30 -30 -30 h-180 q-30 0 -30 30 z" fill="{BLUE}" opacity="0.85" stroke="{INK}" stroke-width="6"/><rect x="700" y="1060" width="280" height="70" rx="20" fill="{BLUE}" stroke="{INK}" stroke-width="6"/><line x1="720" y1="1130" x2="720" y2="1160" stroke="{INK}" stroke-width="7"/><line x1="960" y1="1130" x2="960" y2="1160" stroke="{INK}" stroke-width="7"/>
''' + ticket(540, 700, 1.1, 0, faded=True) + ledger(540, 1520, 2.0, "flat"))
# 5 sunk cost: ticket sinking into a hole, Ledger looks down
scenes.append(f'''
<path d="M60 1180 H330 M750 1180 H1020" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>
<path d="M330 1180 Q330 1700 540 1700 Q750 1700 750 1180" fill="{NAVY}" stroke="{INK}" stroke-width="6"/>
<path d="M370 1260 q170 40 340 0" fill="none" stroke="{LB}" stroke-width="4" opacity="0.4"/><path d="M390 1380 q150 40 300 0" fill="none" stroke="{LB}" stroke-width="4" opacity="0.3"/>
''' + ticket(560, 1500, 0.8, 24) + f'<path d="M520 1330 v-60 M600 1340 v-70" stroke="{GOLD}" stroke-width="5" stroke-dasharray="10 10"/>' + ledger(190, 1170, 1.6, "o", tilt=-6) )
# 6 businesses: unfinished building, arrow forward to a sunny path, Ledger points
scenes.append(ground() + f'''
<rect x="110" y="860" width="320" height="620" fill="{LB}" opacity="0.6" stroke="{INK}" stroke-width="6" stroke-dasharray="26 14"/>
<path d="M110 1060 H430 M110 1260 H430 M215 860 V1480 M325 860 V1480" stroke="{INK}" stroke-width="4" opacity="0.5"/>
<path d="M160 640 V860 M160 650 H460 M440 650 v120" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><rect x="420" y="770" width="40" height="34" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>
<path d="M300 1000 l40 60 -30 50 50 70" fill="none" stroke="#E2928B" stroke-width="6"/>
<circle cx="900" cy="700" r="70" fill="{GOLD}" opacity="0.8" stroke="{INK}" stroke-width="6"/>
''' + "".join(f'<line x1="{900+110*__import__("math").cos(a/57.3)}" y1="{700+110*__import__("math").sin(a/57.3)}" x2="{900+145*__import__("math").cos(a/57.3)}" y2="{700+145*__import__("math").sin(a/57.3)}" stroke="{GOLD}" stroke-width="7" stroke-linecap="round"/>' for a in range(0,360,45)) + f'''
<path d="M640 1480 Q760 1200 900 1000" fill="none" stroke="{BLUE}" stroke-width="20" stroke-linecap="round" opacity="0.25"/>
<path d="M640 860 H820 M780 810 L830 860 L780 910" fill="none" stroke="{BLUE}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
''' + ledger(620, 1470, 2.2, "smile", arm="up"))


GREEN = "#2FA36B"; CORAL = "#E2928B"
def bills(x, y, n=4, s=1.0):
    out = ""
    for k in range(n):
        out += f'<g transform="translate({x+k*6} {y-k*22}) scale({s})"><rect x="-90" y="-40" width="180" height="80" rx="8" fill="{GREEN}" stroke="{INK}" stroke-width="5"/><circle cx="0" cy="0" r="22" fill="none" stroke="{INK}" stroke-width="4"/><rect x="-76" y="-28" width="152" height="56" rx="5" fill="none" stroke="{INK}" stroke-width="2" opacity="0.5"/></g>'
    return out
def coins(x, y, n=5, s=1.0):
    return "".join(f'<ellipse cx="{x}" cy="{y-k*18*s}" rx="{48*s}" ry="{16*s}" fill="{GOLD}" stroke="{INK}" stroke-width="5"/>' for k in range(n))
def phone(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="-150" y="-280" width="300" height="560" rx="40" fill="#fff" stroke="{INK}" stroke-width="8"/>'
            f'<rect x="-125" y="-235" width="250" height="450" rx="12" fill="{SKY}"/>'
            f'<circle cx="0" cy="-120" r="38" fill="none" stroke="{GREY}" stroke-width="6" stroke-dasharray="12 10"/>'
            f'<path d="M-62 -20 Q0 -80 62 -20" fill="none" stroke="{GREY}" stroke-width="6" stroke-dasharray="12 10"/>'
            f'<path d="M-95 40 V170 H100" fill="none" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M-95 160 H100" fill="none" stroke="{CORAL}" stroke-width="7" stroke-linecap="round"/>'
            f'<rect x="-30" y="232" width="60" height="10" rx="5" fill="{INK}" opacity="0.4"/></g>')
def office(wx=760):
    blinds = "".join(f'<line x1="{wx+10}" y1="{y}" x2="{wx+210}" y2="{y}" stroke="{INK}" stroke-width="3" opacity="0.35"/>' for y in range(560, 800, 40))
    return (f'<rect x="0" y="0" width="1080" height="1480" fill="{SKY}" opacity="0.55"/>' + ground() +
            f'<rect x="{wx}" y="520" width="220" height="300" rx="8" fill="#fff" stroke="{INK}" stroke-width="6"/>' + blinds +
            f'<line x1="{wx+110}" y1="520" x2="{wx+110}" y2="820" stroke="{INK}" stroke-width="5"/>')
desk = (f'<rect x="100" y="1250" width="880" height="34" rx="8" fill="{NAVY}"/>'
        f'<rect x="140" y="1284" width="26" height="196" fill="{NAVY}"/><rect x="914" y="1284" width="26" height="196" fill="{NAVY}"/>')
# s6: office, big app phone with no users, money already spent on the desk, Ledger behind the desk
s6 = office() + phone(300, 880, 1.05) + ledger(600, 1268, 1.7, "flat") + desk + bills(800, 1210, 5, 0.95) + coins(640, 1236, 6, 1.0)
# s7: Ledger frowning, arm up, sending more money toward the app
s7 = (office(120) + phone(800, 880, 1.0) +
      f'<path d="M560 980 Q640 900 690 860" fill="none" stroke="{GREEN}" stroke-width="10" stroke-dasharray="22 16" stroke-linecap="round"/>' +
      f'<g transform="rotate(-18 620 940)">{bills(600, 950, 2, 0.7)}</g>' + bills(260, 1440, 4, 1.0) + ledger(480, 1470, 2.2, "frown", arm="up"))
# s8: the old spend fades and is crossed out; a scale weighs the next cost against what it returns
s8 = (ground() + f'<g opacity="0.3">{coins(170, 1460, 8, 1.1)}</g>' +
      f'<line x1="90" y1="1330" x2="250" y2="1090" stroke="{CORAL}" stroke-width="10" stroke-linecap="round"/><line x1="90" y1="1090" x2="250" y2="1330" stroke="{CORAL}" stroke-width="10" stroke-linecap="round"/>' +
      f'<path d="M680 1480 L680 880" stroke="{INK}" stroke-width="10"/><path d="M620 1480 h120" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>' +
      f'<line x1="480" y1="900" x2="880" y2="900" stroke="{INK}" stroke-width="9" stroke-linecap="round"/><circle cx="680" cy="900" r="14" fill="{INK}"/>' +
      f'<line x1="480" y1="900" x2="440" y2="1040" stroke="{INK}" stroke-width="4"/><line x1="480" y1="900" x2="520" y2="1040" stroke="{INK}" stroke-width="4"/><path d="M410 1040 h140 q-10 40 -70 40 q-60 0 -70 -40 z" fill="{LB}" stroke="{INK}" stroke-width="5"/>' +
      f'<line x1="880" y1="900" x2="840" y2="1040" stroke="{INK}" stroke-width="4"/><line x1="880" y1="900" x2="920" y2="1040" stroke="{INK}" stroke-width="4"/><path d="M810 1040 h140 q-10 40 -70 40 q-60 0 -70 -40 z" fill="{LB}" stroke="{INK}" stroke-width="5"/>' +
      coins(480, 1030, 3, 0.9) +
      f'<path d="M880 1030 V930 M840 970 L880 930 L920 970" fill="none" stroke="{GREEN}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>' +
      ledger(380, 1470, 1.8, "flat", arm="hold"))
order = [scenes[0], scenes[1], scenes[2], scenes[3], scenes[4], s6, s7, s8, scenes[5]]
for i, b in enumerate(order, 1):
    open(f"{D}/s{i}.svg", "w").write(frame(b))
print("ok", len(order))
