"""Team reel "Who does what in a marketing team" v3 (16 Nov 2026): two ladders (specialist and manager), the intern does real work in every lane,
four lanes (content, design, performance, analytics), one post flowing through the team. Run: python gen.py"""
import os, sys
sys.path.insert(0, "/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing/.claude/skills/edlintics-ladder-reel")
import ladder_script as LSC
from ladder_script import *   # noqa
LSC.WALLS[6] = "#F7E7E1"

C = lambda n: f"chunk:{n}"
INTERN, COPY, DES, SPEC, ANA, MGR, DIR, CMO_ = "mk_intern", "tm_copy", "fs_designer", "mk_specialist", "tm_analyst", "mk_manager", "mk_director", "mk_cmo"
OUT5 = [INTERN, SPEC, MGR, DIR, CMO_]
L = Ladder(OUT5, ["A", "B", "C", "D", "E"])   # only for cta_beat
RUNGS = ["THE INTERN", "CONTENT LANE", "DESIGN LANE", "PERFORMANCE", "ANALYTICS LANE", "MANAGER LADDER"]

STEP = 150; SX0 = 30; RISE_ = 18
def row(mood="happy"):
    team = [INTERN, COPY, DES, SPEC, ANA, MGR]
    items = [{"p": "steps", "x": SX0, "y": GY, "n": 6, "step_w": STEP, "rise": RISE_}]
    items += [{"p": "ledger", "x": SX0 + (i + 0.5) * STEP, "y": GY - (i + 1) * RISE_ - 6, "s": 0.62, "outfit": team[i], "mood": mood, "arm": "wave" if i in (0, 5) else "down"} for i in range(6)]
    return scene(0, *items)

CTA2 = "To understand how a business really works, learn technical business concepts at Edlintics"
S = {}
S["title"] = row(); S["title2"] = row(); S["cta"] = row()

# ---------- helpers for tag stacks beside a ladder ----------
def tg(xc, y, lab, state, w, fs, h=84, **kw):
    return dict({"p": "rung_tag", "x": xc, "y": y, "label": lab, "state": state, "w": w, "h": h, "fs": fs}, **kw)

def tag_stack(xc, ys, labels, cs, w, fs, first_now=False, h=84):
    """Tags that light up one by one on chunks cs (now), then tick (done); the last stays lit."""
    items = []
    for j, lab in enumerate(labels):
        cj = cs[j]; nxt = cs[j + 1] if j + 1 < len(cs) else None
        if not (first_now and j == 0): items.append(tg(xc, ys[j], lab, "todo", w, fs, h, until=C(cj)))
        if first_now and j == 0:
            if nxt is None: items.append(tg(xc, ys[j], lab, "now", w, fs, h))
            else: items += [tg(xc, ys[j], lab, "now", w, fs, h, until=C(nxt)), tg(xc, ys[j], lab, "done", w, fs, h, at=C(nxt), pop="cut")]
        elif nxt is None: items.append(tg(xc, ys[j], lab, "now", w, fs, h, at=C(cj), pop="cut"))
        else: items += [tg(xc, ys[j], lab, "now", w, fs, h, at=C(cj), until=C(nxt), pop="cut"), tg(xc, ys[j], lab, "done", w, fs, h, at=C(nxt), pop="cut")]
    return items

def climbers(x, ys, outfits, cs, s, first_now=False):
    """One Ledger per rung, swapped on chunks cs (a hop up the ladder); the first can stand there from the start."""
    items = []
    for j, o in enumerate(outfits):
        nxt = cs[j + 1] if j + 1 < len(cs) else None
        kw = {}
        if not (first_now and j == 0): kw.update(at=C(cs[j]), pop="cut")
        if nxt is not None: kw["until"] = C(nxt)
        items.append({"p": "ledger", "x": x, "y": ys[j], "s": s, "outfit": o, "mood": "happy" if nxt is None else "smile", "arm": "wave" if nxt is None else "both_up", **kw})
    return items

RY3 = [1400, 1210, 1020]

# ---------- beat 3-5: the two ladders ----------
def two_ladders():
    XA, XB, LW, TW_, FS = 90, 550, 110, 270, 30
    TXA, TXB = XA + LW / 2 + 11 + 50 + TW_ / 2, XB + LW / 2 + 11 + 50 + TW_ / 2
    items = [{"p": "career_ladder", "x": XA, "y": 1400, "n": 3, "gap": 190, "w": LW}, {"p": "career_ladder", "x": XB, "y": 1400, "n": 3, "gap": 190, "w": LW},
             {"p": "order_chip", "x": 250, "y": 780, "label": "SPECIALIST LADDER", "color": "blue", "fs": 32, "appear": {"at": C(1), "delay": 0.1}},
             {"p": "order_chip", "x": 716, "y": 780, "label": "MANAGER LADDER", "color": "amber", "fs": 32, "appear": {"at": C(1), "delay": 0.5}}]
    items += tag_stack(TXA, RY3, ["JUNIOR", "SENIOR", "LEAD"], [5, 6, 7], TW_, FS)
    items += tag_stack(TXB, RY3, ["MANAGER", "DIRECTOR", "CMO"], [11, 12, 13], TW_, FS)
    items += climbers(XA, RY3, [INTERN, SPEC, COPY], [5, 6, 7], 0.62)
    items += climbers(XB, RY3, [MGR, DIR, CMO_], [11, 12, 13], 0.62)
    return scene(0, *items)
S["two"] = two_ladders()

# ---------- beat 6-8: the intern (rung 1) ----------
S["r1a"] = scene(1,
    {"p": "order_chip", "x": 260, "y": 770, "label": "INTERN", "color": "blue", "fs": 44, "appear": {"at": C(1), "delay": 0.1}},
    {"p": "order_chip", "x": 790, "y": 770, "label": "ASSISTANT", "color": "amber", "fs": 44, "appear": {"at": C(2), "delay": 0.1}},
    led(540, 2.8, INTERN, mood="happy", arm="wave"))
def tile(x, y, lab, at, item):
    return [dict(item, x=x, y=y, appear={"at": C(at), "delay": 0.05}), {"p": "order_chip", "x": x, "y": y + 175, "label": lab, "color": "light", "fs": 34, "appear": {"at": C(at), "delay": 0.2}}]
S["r1b"] = scene(2 if False else 1,
    *tile(590, 905, "Draft", 1, {"p": "note_card", "title": "Post", "lines": ["Draft"], "w": 240, "fs": 36, "rot": -3}),
    *tile(820, 905, "Resize", 2, {"p": "laptop", "s": 0.52, "screen": "filled"}),
    *tile(590, 1260, "Schedule", 3, {"p": "calendar", "s": 0.46, "mark": 9}),
    *tile(820, 1260, "Numbers", 5, {"p": "chart", "s": 0.52, "trend": "up"}),
    led(200, 2.0, INTERN, arm="point"))
S["r1c"] = scene(1,
    *[{"p": "order_chip", "x": 700, "y": 860 + 135 * i, "label": ["CONTENT", "DESIGN", "ADS", "ANALYTICS"][i], "color": ["blue", "amber", "green", "light"][i], "fs": 44, "appear": {"at": C(1), "delay": 0.3 * i}} for i in range(4)],
    {"p": "arrow", "x": 450, "y": 1230, "dx": 140, "dy": -250, "color": "blue", "s": 0.9, "appear": {"at": C(2), "delay": 0.1}},
    led(215, 2.2, INTERN, mood="happy", arm="point"))

# ---------- beat 9-10: content lane (rung 2) ----------
S["r2a"] = scene(2,
    {"p": "note_card", "x": 520, "y": 880, "w": 250, "title": "Post", "lines": ["Learn business"], "fs": 36, "rot": -3, "at": C(1)},
    {"p": "note_card", "x": 800, "y": 880, "w": 250, "title": "Caption", "lines": ["One idea"], "fs": 36, "rot": 3, "at": C(2)},
    {"p": "cal_fill", "x": 690, "y": 1230, "cols": 4, "rows": 3, "size": 46, "gap": 8, "title": "Calendar", "fills": [{"at": C(3), "delay": 0.1, "dur": 1.4, "upto": 12}]},
    led(180, 1.9, COPY, mood="happy", arm="point"))
def lane_ladder(k, labels, cs, outfit, fs=34):
    xc = 230 + 162 + 470 / 2
    items = [{"p": "career_ladder", "x": 230, "y": 1400, "n": 3, "gap": 190, "w": 220}]
    items += tag_stack(xc, RY3, labels, cs, 470, fs, first_now=True, h=96)
    items += climbers(230, RY3, [outfit] * 3, cs, 0.8, first_now=True)
    return scene(k, *items)
S["r2b"] = lane_ladder(2, ["SPECIALIST", "SENIOR", "LEAD STRATEGIST"], [0, 2, 4], COPY)

# ---------- beat 11-13: design lane (rung 3) ----------
S["r3a"] = scene(3,
    *[{"p": "order_chip", "x": 730, "y": 790 + 95 * i, "label": ["Visuals", "Colors", "Layout", "Images"][i], "color": ["blue", "amber", "green", "light"][i], "fs": 48, "appear": {"at": C(1 + i), "delay": 0.05}} for i in range(4)],
    {"p": "laptop", "x": 700, "y": 1340, "s": 0.95, "screen": "filled", "at": C(1)},
    {"p": "check", "x": 900, "y": 1180, "s": 0.6, "appear": {"at": C(4), "delay": 0.4}},
    led(215, 2.2, DES, mood="happy", arm="point"))
S["r3b"] = scene(3,
    {"p": "laptop", "x": 590, "y": 1250, "s": 0.85, "screen": "filled", "at": C(1)},
    {"p": "check", "x": 560, "y": 880, "s": 0.6, "appear": {"at": C(2), "delay": 0.2}},
    {"p": "phone", "x": 860, "y": 1220, "s": 0.5, "screen": "up", "at": C(3)},
    {"p": "arrow", "x": 590, "y": 1010, "dx": 200, "dy": 80, "color": "blue", "s": 0.8, "appear": {"at": C(3), "delay": 0.1}},
    led(190, 2.0, DES, mood="happy", arm="point"))
S["r3c"] = lane_ladder(3, ["JUNIOR", "SENIOR DESIGNER", "DESIGN LEAD"], [0, 2, 4], DES)

# ---------- beat 14: performance lane (rung 4) ----------
PX = [560, 730, 900]; PY = 1210
S["r4a"] = scene(4,
    *[{"p": "phone", "x": PX[i], "y": 920, "s": 0.26, "screen": ["chat", "up", "chat"][i], "appear": {"at": C(1), "delay": 0.2 + 0.3 * i}} for i in range(3)],
    {"p": "order_chip", "x": 730, "y": 1075, "label": "BUDGET", "color": "green", "fs": 40, "appear": {"at": C(3), "delay": 0.0}},
    *[{"p": "pot", "x": PX[i], "y": PY + 20, "s": 0.8, "label": ["Search", "Social", "Video"][i], "color": ["blue", "amber", "green"][i], "fs": 34, "at": C(3)} for i in range(3)],
    {"p": "coin_stream", "x": 730, "y": 1100, "to": [PX[0], PY + 20], "n": 3, "kind": "chip", "color": "blue", "at": C(3), "delay": 0.3},
    {"p": "coin_stream", "x": 730, "y": 1100, "to": [PX[1], PY + 20], "n": 5, "kind": "chip", "color": "amber", "at": C(3), "delay": 0.45},
    {"p": "coin_stream", "x": 730, "y": 1100, "to": [PX[2], PY + 20], "n": 2, "kind": "chip", "color": "green", "at": C(3), "delay": 0.6},
    {"p": "coin_stream", "x": PX[2], "y": PY + 20, "to": [PX[1], PY + 20], "n": 3, "kind": "chip", "color": "green", "at": C(4), "delay": 0.1, "arc": 90},
    led(180, 2.0, SPEC, mood="happy", arm="point"))

# ---------- beat 15: analytics lane (rung 5) ----------
S["r5a"] = scene(5,
    {"p": "chart", "x": 640, "y": 960, "s": 0.95, "trend": "up", "reveal": {"at": C(1), "delay": 0.0, "dur": 1.6, "dir": "right"}},
    *[{"p": "order_chip", "x": [520, 690, 850][i], "y": 1250, "label": ["Views", "Clicks", "Sales"][i], "color": ["blue", "amber", "green"][i], "fs": 38, "appear": {"at": C(2 + i), "delay": 0.0}, "until": C(5)} for i in range(3)],
    *[{"p": "arrow", "x": [520, 690, 850][i], "y": 1360, "dx": 0, "dy": -70, "color": "green", "s": 0.8, "appear": {"at": C(2 + i), "delay": 0.25}, "until": C(5)} for i in range(3)],
    {"p": "note_card", "x": 520, "y": 1290, "w": 250, "title": "Report", "fs": 40, "at": C(5), "move": [{"at": C(5), "delay": 0.3, "dur": 1.0, "to": [690, 1290], "ease": "inout"}]},
    {"p": "arrow", "x": 700, "y": 1420, "dx": -140, "dy": 0, "color": "green", "s": 0.8, "at": C(6)},
    led(180, 2.0, ANA, mood="happy", arm="point"),
    led(880, 1.4, MGR, mood="happy", arm="wave", at=C(5)))

# ---------- beat 16-17: manager ladder (rung 6) ----------
S["r6a"] = scene(6,
    {"p": "meter", "x": 520, "y": 830, "w": 380, "h": 56, "fs": 36, "label": "Goal", "limit": "Target", "to": 0.8, "fill": {"at": C(2), "delay": 0.1, "dur": 1.2}},
    {"p": "note_card", "x": 510, "y": 1130, "w": 290, "title": "The brief", "lines": ["Goal", "Audience", "Budget"], "fs": 38, "rot": -3, "at": C(3)},
    *[{"p": "order_chip", "x": 800, "y": 900 + 130 * i, "label": ["CONTENT", "DESIGN", "ADS", "ANALYTICS"][i], "color": ["blue", "amber", "green", "light"][i], "fs": 32, "appear": {"at": C(4), "delay": 0.7 + 0.2 * i}} for i in range(4)],
    *[{"p": "coin_stream", "x": 660, "y": 1130, "to": [700, 900 + 130 * i], "n": 3, "kind": "chip", "color": "blue", "at": C(4), "delay": 0.1 + 0.12 * i, "arc": 40} for i in range(4)],
    led(190, 2.0, MGR, mood="happy", arm="point"))
XL, LW = 130, 180
xc = XL + LW / 2 + 11 + 50 + 135
mi = [{"p": "career_ladder", "x": XL, "y": 1400, "n": 3, "gap": 190, "w": LW},
      tg(xc, RY3[0], "MANAGER", "done", 270, 30),
      tg(xc, RY3[1], "DIRECTOR", "now", 270, 30, until=C(2)), tg(xc, RY3[1], "DIRECTOR", "done", 270, 30, at=C(2), pop="cut"),
      tg(xc, RY3[2], "CMO", "todo", 270, 30, until=C(2)), tg(xc, RY3[2], "CMO", "now", 270, 30, at=C(2), pop="cut"),
      {"p": "ledger", "x": XL, "y": RY3[0], "s": 0.7, "outfit": MGR, "mood": "smile", "arm": "down"}]
TEAMC = ["#F2C7C2", "#CFE9D9", "#F3D9A6"]
mi += [{"p": "person", "x": 620 + 62 * j + (20 if j >= 2 else 0) + (20 if j >= 4 else 0), "y": FEET, "s": 0.95, "color": TEAMC[j // 2], "appear": {"at": C(1), "delay": 0.15 * j}} for j in range(6)]
mi += [{"p": "note_card", "x": 740, "y": 880, "w": 360, "title": "Marketing plan", "fs": 36, "at": C(3), "rot": 2},
       {"p": "meter", "x": 740, "y": 1060, "w": 340, "h": 52, "fs": 34, "label": "Budget", "limit": "Limit", "to": 0.85, "at": C(3), "fill": {"at": C(4), "delay": 0.1, "dur": 1.0}}]
mi += [{"p": "ledger", "x": XL, "y": RY3[1], "s": 0.7, "outfit": DIR, "mood": "happy", "arm": "up", "until": C(2)},
       {"p": "ledger", "x": XL, "y": RY3[2], "s": 0.7, "outfit": CMO_, "mood": "happy", "arm": "wave", "at": C(2), "pop": "cut"}]
S["r6b"] = scene(6, *mi)

# ---------- flow: one post through the team (payoff) ----------
NODES = [(500, 700, MGR, "BRIEF"), (814, 928, COPY, "WORDS"), (694, 1290, DES, "DESIGN"), (306, 1290, INTERN, "SCHEDULE"), (186, 928, ANA, "RESULTS")]
def flow():
    items = []
    cen = [(x, y - 55) for x, y, _, _ in NODES]
    for i in range(5):
        a, b = cen[i], cen[(i + 1) % 5]
        p0 = (a[0] + 0.3 * (b[0] - a[0]), a[1] + 0.3 * (b[1] - a[1])); p1 = (a[0] + 0.7 * (b[0] - a[0]), a[1] + 0.7 * (b[1] - a[1]))
        items.append({"p": "arrow", "x": p0[0], "y": p0[1], "dx": p1[0] - p0[0], "dy": p1[1] - p0[1], "color": "green" if i == 4 else "blue", "s": 0.9, "appear": {"at": C([4, 6, 8, 9, 11][i]), "delay": 0.0}})
    chip_at = [3, 4, 7, 8, 9]
    for i, (x, y, o, lab) in enumerate(NODES):
        items.append({"p": "order_chip", "x": x, "y": y - 175, "label": lab, "color": "amber" if i == 4 else "light", "fs": 34, "appear": {"at": C(chip_at[i]), "delay": 0.0}})
    pos = [(x + 85, y - 40) for x, y, _, _ in NODES]
    mv = [{"at": C(c), "delay": 0.1, "dur": 0.8, "to": list(pos[j]), "ease": "inout"} for c, j in [(4, 1), (6, 2), (8, 3), (9, 4), (11, 0)]]
    items.append({"p": "phone", "x": pos[0][0], "y": pos[0][1], "s": 0.2, "screen": "chat", "at": C(3), "move": mv})
    items += [{"p": "ledger", "x": x, "y": y, "s": 0.7, "outfit": o, "mood": "happy", "arm": "wave" if i == 0 else "down", "appear": {"at": C(1), "delay": 0.2 + 0.2 * i}} for i, (x, y, o, _) in enumerate(NODES)]
    return scene(0, *items)
S["flow"] = flow()

# ---------- close ----------
S["small"] = scene(0,
    *[{"p": "order_chip", "x": [300, 770, 330, 740][i], "y": [790, 790, 940, 940][i], "label": ["CONTENT", "DESIGN", "ADS", "DATA"][i], "color": ["blue", "amber", "green", "light"][i], "fs": 44, "appear": {"at": C(1 + (i // 2)), "delay": 0.25 * (i % 2)}} for i in range(4)],
    led(540, 2.5, INTERN, mood="happy", arm="up"))
def big_team():
    xs = [115, 345, 575, 805]; labs = ["CONTENT", "DESIGN", "ADS", "DATA"]; outs = [COPY, DES, SPEC, ANA]; cols = ["blue", "amber", "green", "light"]
    items = []
    for i, x in enumerate(xs):   # ladders, labels and the bottom-rung Ledgers are there from the first frame; the climb follows the voice
        items += [{"p": "career_ladder", "x": x, "y": 1400, "n": 3, "gap": 150, "w": 100},
                  {"p": "order_chip", "x": x, "y": 880, "label": labs[i], "color": cols[i], "fs": 34}]
    for i, x in enumerate(xs):
        items.append({"p": "ledger", "x": x, "y": 1400, "s": 0.55, "outfit": outs[i], "mood": "smile", "arm": "down"})
        items += [{"p": "ledger", "x": x, "y": 1400 - 150 * j, "s": 0.55, "outfit": outs[i], "mood": "happy", "arm": "wave" if j == 2 else "down", "appear": {"at": C(2), "delay": 0.1 * i + 0.25 * (j - 1)}} for j in (1, 2)]
    return scene(0, *items)
S["big"] = big_team()

beats = [
    B("title", "title", "In our marketing ladder, Ledger climbed from intern to CMO.",
      ["In our marketing ladder", "Ledger climbed", ("from intern to CMO", "CMO")],
      message="Who does what in a marketing team, with Ledger", tag="UNDER 2 MINUTES", gap=0.3),
    B("climb", "title2", "One of you asked who designs the posts.", ["One of you asked", ("who designs the posts", "designs")]),
    B("climb", "title2", "Here is how a marketing team divides the work.", ["Here is how", ("a marketing team", "team"), "divides the work"]),
    B("climb", "two", "Most companies have two ladders.", ["Most companies", ("have two ladders", "two ladders")]),
    B("climb", "two", "On the specialist ladder, you get better at one craft, from junior to senior to lead.",
      ["On the specialist ladder", "you get better", ("at one craft", "craft"), "from junior", "to senior", "to lead"]),
    B("climb", "two", "On the manager ladder, you lead people and budgets, from manager to director to CMO.",
      ["On the manager ladder", ("you lead people", "lead"), "and budgets", "from manager", "to director", "to CMO"]),
    B("rung", "r1a", "Everyone starts as an intern or an assistant.", ["Everyone starts", ("as an intern", "intern"), ("or an assistant", "assistant")], 1),
    B("rung", "r1b", "The intern drafts posts, resizes designs, schedules them and pulls the numbers.",
      ["The intern drafts", ("posts", "posts"), ("resizes designs", "resizes"), ("schedules them", "schedules"), "and pulls", ("the numbers", "numbers")], 1,
      [("DRAFT POSTS", 1), ("RESIZE DESIGNS", 2), ("SCHEDULE POSTS", 3), ("PULL NUMBERS", 5)]),
    B("rung", "r1c", "So the intern learns every lane before picking one.", ["So the intern", ("learns every lane", "lane"), "before picking one"], 1),
    B("rung", "r2a", "The content specialist writes the posts and the captions, and plans the content calendar.",
      ["The content specialist", ("writes the posts", "posts"), ("and the captions", "captions"), "and plans", ("the content calendar", "calendar")], 2,
      [("WRITE POSTS", 1), ("WRITE CAPTIONS", 2), ("PLAN CALENDAR", 4)]),
    B("rung", "r2b", "A content specialist can climb to senior and then to lead content strategist.",
      ["A content specialist", "can climb", ("to senior", "senior"), "and then", ("to lead", "lead"), "content strategist"], 2),
    B("rung", "r3a", "The designer makes the visuals, the colors, the layout and the images.",
      ["The designer makes", ("the visuals", "visuals"), ("the colors", "colors"), ("the layout", "layout"), ("and the images", "images")], 3,
      [("MAKE VISUALS", 1), ("PICK COLORS", 2), ("DESIGN LAYOUT", 3), ("CHOOSE IMAGES", 4)]),
    B("rung", "r3b", "So this is who designs the posts you see on your screen.",
      ["So this is who", ("designs the posts", "designs"), "you see", "on your screen"], 3),
    B("rung", "r3c", "A designer climbs from junior to senior designer and then to design lead.",
      ["A designer climbs", ("from junior", "junior"), ("to senior designer", "senior"), "and then", ("to design lead", "lead")], 3),
    B("rung", "r4a", "The performance marketer runs the paid ads and decides how much budget each channel gets.",
      ["The performance marketer", ("runs the paid ads", "ads"), "and decides", ("how much budget", "budget"), "each channel gets"], 4,
      [("RUN PAID ADS", 1), ("SPLIT BUDGET", 3)]),
    B("rung", "r5a", "The marketing analyst tracks the results, the views, the clicks and the sales, and reports them every week.",
      ["The marketing analyst", ("tracks the results", "results"), ("the views", "views"), ("the clicks", "clicks"), ("and the sales", "sales"), ("and reports them", "reports"), "every week"], 5,
      [("TRACK RESULTS", 1), ("WEEKLY REPORT", 6)]),
    B("rung", "r6a", "On the manager ladder, the marketing manager sets the goal, writes the brief and splits the work across these lanes.",
      ["On the manager ladder", ("the marketing manager", "manager"), ("sets the goal", "goal"), ("writes the brief", "brief"), ("and splits the work", "splits"), "across these lanes"], 6,
      [("SET THE GOAL", 2), ("WRITE THE BRIEF", 3), ("SPLIT THE WORK", 4)]),
    B("rung", "r6b", "The director runs several teams, and the CMO owns the marketing plan and budget.",
      ["The director", ("runs several teams", "teams"), "and the CMO", ("owns the marketing plan", "plan"), ("and budget", "budget")], 6,
      [("OWN THE PLAN", 3)]),
    B("payoff", "flow", "So one post moves through the team.", ["So one post", "moves through", ("the team", "team")]),
    B("payoff", "flow", "The brief becomes words, the words become a design, the design is scheduled, and the results go back to the manager.",
      [("The brief", "brief"), ("becomes words", "words"), "the words", ("become a design", "design"), "the design", ("is scheduled", "scheduled"), "and the results", "go back", ("to the manager", "manager")]),
    B("payoff", "small", "In a small team, one person may do all of this.", ["In a small team", ("one person", "one person"), "may do", ("all of this", "all")], gap=0.3),
    B("payoff", "big", "In a big team, every lane has its own ladder.", ["In a big team", ("every lane", "lane"), "has its own", ("ladder", "ladder")], gap=0.3),
    B("cta", "cta", CTA2 + ".", ["To understand how", "a business really works", "learn technical", "business concepts", ("at Edlintics", "Edlintics")],
      say=CTA2.replace("Edlintics", "Ed-lin-tics") + ".", message=CTA2),
]

meta = {
    "term": "Marketing team", "title": "Who does what in a marketing team, the specialist and manager ladders explained with Ledger", "slug": "team-who-does-what-marketing", "rungs": RUNGS,
    "rung_label": "PART {n} OF {N}",
    "family_or_category": "marketing", "concept_id": "team-who-does-what-marketing", "themes": ["marketing-careers", "team-roles"],
    "caption": "Who actually makes the posts in a marketing team? Most companies have two ladders\n\nOn the specialist ladder, you get better at one craft, from junior to senior to lead. On the manager ladder, you lead people and budgets, from manager to director to CMO. Everyone starts as an intern, who drafts posts, resizes designs, schedules them and pulls the numbers, so the intern learns every lane before picking one\n\nThe content specialist writes the posts and the captions, the designer makes the visuals, the performance marketer runs the paid ads and the budget, and the analyst tracks the results. The manager sets the goal and the brief, and in a small team one person may do all of this\n\nMissed the ladder? Watch From marketing intern to CMO on our profile\n\n#edlintics #businessstudents #marketing #teamwork",
    "caption_x": "Who makes a marketing post? Two ladders: specialists get better at one craft, managers lead people and budgets. Lanes: content, design, ads, analytics. Missed the ladder? Watch From marketing intern to CMO on our profile #edlintics",
    "first_comment": "Which lane would you pick first, content, design, ads or analytics? Tell us below 🎨📣",
    "first_comment_igtt": "Which lane would you pick first, content, design, ads or analytics? Tell us below, link in bio 🎨📣",
    "hashtags": ["#edlintics", "#businessstudents", "#marketing", "#teamwork"],
    "threadsTopic": "Marketing", "threadsReason": "A reel on who does what in a marketing team fits the Marketing topic; if the Marketing community is not joined yet, use the topic Business",
    "maths_check": "No numbers are stated except the video length in the title tag and the counts of two ladders and four lanes (content, design, performance, analytics), which match the pictures. No salaries, no currency",
    "sources": [], "definition_check": "", "registry_check": "",
}
if __name__ == "__main__":
    write(os.path.dirname(os.path.abspath(__file__)), meta, S, beats)
