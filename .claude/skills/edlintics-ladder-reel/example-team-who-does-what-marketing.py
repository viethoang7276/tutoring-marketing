"""Team reel "Who does what in a marketing team" (16 Nov 2026): one post followed through six roles. Run: python gen.py"""
import os, sys
sys.path.insert(0, "/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing/.claude/skills/edlintics-ladder-reel")
import ladder_script as LSC
from ladder_script import *   # noqa
LSC.WALLS[6] = "#F7E7E1"

OUT = ["mk_manager", "tm_copy", "fs_designer", "mk_specialist", "mk_intern", "tm_analyst"]
RUNGS = ["THE MANAGER", "THE COPYWRITER", "THE DESIGNER", "THE SPECIALIST", "THE INTERN", "THE ANALYST"]
TAGS = ["BRIEF", "WORDS", "VISUALS", "LAUNCH", "SCHEDULE", "REPORT"]
L = Ladder(OUT[:5], ["A", "B", "C", "D", "E"])   # only for cta_beat
TY = [760 + 130 * i for i in range(6)]; TX = 740; TW = 380

def tag(i, state, **kw):
    return dict({"p": "rung_tag", "x": TX, "y": TY[i], "label": TAGS[i], "state": state, "w": TW, "h": 96, "fs": 40}, **kw)

def handoff(k, go, name):
    """The post (a phone) moves from stage k to stage k+1 on the progress strip; Ledger changes outfit when the new role is named."""
    g = f"chunk:{go}"; nm = f"chunk:{name}"; items = []
    for i in range(6):
        if i < k: items.append(tag(i, "done"))
        elif i == k: items += [tag(i, "now", until=nm), tag(i, "done", at=nm, pop="cut")]
        elif i == k + 1: items += [tag(i, "todo", until=nm), tag(i, "now", at=nm)]
        else: items.append(tag(i, "todo"))
    items += [{"p": "burst", "x": TX - TW / 2 + 40, "y": TY[k + 1], "s": 1.0, "color": "amber", "at": g, "delay": 0.85},
              {"p": "phone", "x": 520, "y": TY[k], "s": 0.24, "screen": "chat", "move": [{"at": g, "delay": 0.1, "dur": 0.8, "to": [520, TY[k + 1]], "ease": "inout"}]},
              led(240, 2.0, OUT[k], arm="down", until=nm), led(240, 2.0, OUT[k + 1], mood="happy", arm="point", at=nm, pop="cut")]
    return scene(0, *items)

def allshot():
    items = [tag(i, "done") for i in range(6)]
    items += [{"p": "ledger", "x": 330, "y": TY[i] + 44, "s": 0.52, "outfit": OUT[i], "mood": "happy" if i == 5 else "smile", "arm": "wave" if i == 5 else "down",
               "appear": {"at": "chunk:1", "delay": 0.1 + 0.3 * i}} for i in range(6)]
    items.append({"p": "phone", "x": 100, "y": 1060, "s": 0.3, "screen": "up", "at": "chunk:0"})
    return scene(0, *items)

STEP = 150; SX0 = 30; RISE_ = 18
def row(mood="happy"):
    items = [{"p": "steps", "x": SX0, "y": GY, "n": 6, "step_w": STEP, "rise": RISE_}]
    items += [{"p": "ledger", "x": SX0 + (i + 0.5) * STEP, "y": GY - (i + 1) * RISE_ - 6, "s": 0.62, "outfit": OUT[i], "mood": mood, "arm": "wave" if i in (0, 5) else "down"} for i in range(6)]
    return scene(0, *items)

CTA2 = "To understand how a business really works, learn technical business concepts at Edlintics"
S = {}
S["title"] = row(); S["cta"] = row()
S["h1"] = handoff(0, 1, 2); S["h2"] = handoff(1, 1, 2); S["h3"] = handoff(2, 1, 2); S["h4"] = handoff(3, 1, 2); S["h5"] = handoff(4, 1, 2)
S["all"] = allshot()
S["title2"] = row()

MKOUT = ["mk_intern", "mk_specialist", "mk_manager", "mk_director", "mk_cmo"]; MKTAG = ["INTERN", "SPECIALIST", "MANAGER", "DIRECTOR", "CMO"]
LDX = 500; LTW = 260
def mtag(i, state, **kw):
    return dict({"p": "rung_tag", "x": LDX + 162 + LTW / 2, "y": RY[i], "label": MKTAG[i], "state": state, "w": LTW, "h": 96, "fs": 30}, **kw)
def place(outfit, rung=None, side=False):
    """The stage Ledger beside the marketing ladder from the first reel; the rung he sits on (if any) lights up"""
    items = [{"p": "career_ladder", "x": LDX, "y": RY[0], "n": 5, "gap": 190, "w": 220}]
    items += [mtag(i, "now" if rung == i else "todo", **({"pulse": {"at": "chunk:1", "dur": 0.5, "amp": 0.12}} if rung == i else {})) for i in range(5)]
    items.append(led(215, 1.9, outfit, mood="happy", arm="point"))
    if rung is not None: items.append({"p": "arrow", "x": 470, "y": RY[rung] - 10, "dx": -50, "dy": 0, "color": "blue", "s": 0.8, "at": "chunk:2"})
    return scene(0, *items)
S["p1"] = place("mk_manager", 2); S["p2"] = place("tm_copy"); S["p3"] = place("fs_designer"); S["p4"] = place("mk_specialist", 1); S["p5"] = place("mk_intern", 0); S["p6"] = place("tm_analyst")
def closing():
    items = [{"p": "career_ladder", "x": LDX - 100, "y": RY[0], "n": 5, "gap": 190, "w": 220}]
    tg = lambda i, st, **kw: dict(mtag(i, st, **kw), x=LDX - 100 + 162 + 150, w=300, fs=32)
    for i in range(5):
        items.append(tg(i, "todo", **({"until": f"chunk:1", } if i < 3 else {})))
        if i < 3: items.append(tg(i, "now", at="chunk:1", pop="cut", pulse={"at": "chunk:1", "delay": 0.15 * i, "dur": 0.5, "amp": 0.12}))
    items += [{"p": "ledger", "x": LDX - 100 - 10, "y": RY[i], "s": 0.62, "outfit": MKOUT[i], "mood": "smile", "arm": "down", "appear": {"at": "chunk:0", "delay": 0.1 + 0.25 * i}} for i in range(3)]
    for j, (o, lab) in enumerate([("tm_copy", "COPY"), ("fs_designer", "DESIGN"), ("tm_analyst", "DATA")]):
        y = RY[j] 
        items += [{"p": "ledger", "x": 860, "y": y, "s": 0.55, "outfit": o, "mood": "happy", "arm": "wave", "appear": {"at": "chunk:2", "delay": 0.25 * j}},
                  {"p": "order_chip", "x": 860, "y": y - 150, "label": lab, "color": "light", "fs": 34, "appear": {"at": "chunk:2", "delay": 0.25 * j}}]
    return scene(0, *items)
S["closing"] = closing()

# stage 1, manager: goal, campaign and budget, brief
S["r1a"] = scene(1,
    {"p": "meter", "x": 700, "y": 1000, "w": 440, "h": 60, "fs": 40, "label": "Goal", "limit": "Target", "to": 0.8, "fill": {"at": "chunk:3", "delay": 0.1, "dur": 1.2}},
    led(230, 2.4, "mk_manager", mood="happy", arm="point"))
S["r1b"] = scene(1,
    {"p": "cal_fill", "x": 700, "y": 965, "size": 70, "gap": 12, "title": "Campaign", "fills": [{"at": "chunk:1", "delay": 0.1, "dur": 1.3, "upto": 20}]},
    {"p": "meter", "x": 700, "y": 1350, "w": 440, "h": 60, "fs": 40, "label": "Budget", "limit": "Limit", "to": 0.86, "fill": {"at": "chunk:2", "delay": 0.1, "dur": 1.1}},
    led(218, 2.0, "mk_manager", arm="point"))
S["r1c"] = scene(1,
    {"p": "note_card", "x": 700, "y": 1060, "w": 440, "title": "The brief", "lines": ["Goal", "Audience", "Budget"], "fs": 46, "rot": -3, "at": "chunk:1"},
    {"p": "arrow", "x": 880, "y": 1400, "dx": -250, "dy": -80, "color": "blue", "s": 1.0, "appear": {"at": "chunk:1", "delay": 0.5}},
    led(230, 2.2, "mk_manager", arm="point"))
# stage 2, copywriter: headline and caption
S["r2a"] = scene(2,
    {"p": "laptop", "x": 700, "y": 1200, "s": 1.0, "screen": "sheet", "at": "chunk:3"},
    led(240, 2.5, "tm_copy", mood="happy", arm="point"))
S["r2b"] = scene(2,
    {"p": "note_card", "x": 690, "y": 900, "w": 440, "title": "Headline", "lines": ["Learn the language of business"], "fs": 42, "rot": -2, "at": "chunk:1", "pop": "cut"},
    {"p": "note_card", "x": 690, "y": 1290, "w": 440, "title": "Caption", "lines": ["One idea, then a question"], "fs": 42, "rot": 2, "at": "chunk:3"},
    led(218, 2.0, "tm_copy", arm="point"))
# stage 3, designer: visuals (the answer to the comment)
S["r3a"] = scene(3,
    {"p": "laptop", "x": 700, "y": 1190, "s": 1.05, "screen": "filled", "at": "chunk:3"},
    led(240, 2.5, "fs_designer", mood="happy", arm="point"))
S["r3c"] = scene(3,
    *[{"p": "order_chip", "x": 700, "y": 880 + 150 * i, "label": ["Colors", "Fonts", "Images"][i], "color": ["blue", "amber", "green"][i], "fs": 56, "appear": {"at": "chunk:1", "delay": 0.45 * i}} for i in range(3)],
    led(240, 2.3, "fs_designer", arm="point"))
S["r3d"] = scene(3,
    {"p": "laptop", "x": 690, "y": 1100, "s": 1.3, "screen": "filled"},
    {"p": "check", "x": 900, "y": 800, "s": 0.7, "appear": {"at": "chunk:1", "delay": 0.2}},
    led(215, 2.0, "fs_designer", mood="happy", arm="up"))
# stage 4, specialist: launch, ads
S["r4a"] = scene(4,
    {"p": "order_chip", "x": 700, "y": 800, "label": "Launch", "color": "green", "fs": 70, "at": "chunk:3", "pulse": {"at": "chunk:3", "dur": 0.5, "amp": 0.14}},
    *[{"p": "phone", "x": 570 + 130 * i, "y": 1320, "s": 0.3, "screen": ["chat", "up", "chat"][i], "appear": {"at": "chunk:3", "delay": 0.35 + 0.25 * i}} for i in range(3)],
    led(230, 2.3, "mk_specialist", mood="happy", arm="point"))
S["r4b"] = scene(4,
    {"p": "chart", "x": 690, "y": 905, "s": 1.0, "trend": "up", "reveal": {"at": "chunk:1", "delay": 0.1, "dur": 0.9, "dir": "right"}},
    *[{"p": "person", "x": 630 + 122 * i, "y": FEET, "s": 1.4, "color": ["#F2C7C2", "#CFE9D9", "#F3D9A6"][i], "appear": {"at": "chunk:1", "delay": 0.3 + 0.2 * i}} for i in range(3)],
    led(250, 2.3, "mk_specialist", arm="up"))
# stage 5, intern: schedule and replies
S["r5a"] = scene(5,
    {"p": "cal_fill", "x": 700, "y": 965, "size": 70, "gap": 12, "title": "Schedule", "fills": [{"at": "chunk:3", "delay": 0.1, "dur": 1.4, "upto": 20}]},
    {"p": "calendar", "x": 700, "y": 1400, "s": 0.4, "mark": 9, "at": "chunk:3"},
    led(230, 2.3, "mk_intern", mood="happy", arm="point"))
S["r5b"] = scene(5,
    {"p": "phone", "x": 690, "y": 1170, "s": 0.55, "screen": "chat"},
    {"p": "speech", "x": 850, "y": 880, "s": 0.7, "side": "left", "appear": {"at": "chunk:1", "delay": 0.2}},
    {"p": "check", "x": 560, "y": 880, "s": 0.5, "appear": {"at": "chunk:1", "delay": 0.7}},
    led(212, 2.0, "mk_intern", arm="point"))
# stage 6, analyst: measure, report back
S["r6a"] = scene(6,
    {"p": "chart", "x": 690, "y": 930, "s": 1.1, "trend": "up", "reveal": {"at": "chunk:3", "delay": 0.0, "dur": 0.9, "dir": "right"}},
    led(240, 2.3, "tm_analyst", mood="happy", arm="point"))
S["r6b"] = scene(6,
    {"p": "note_card", "x": 440, "y": 1000, "w": 250, "title": "Report", "fs": 40, "at": "chunk:1", "move": [{"at": "chunk:1", "delay": 0.3, "dur": 1.0, "to": [600, 1000], "ease": "inout"}]},
    {"p": "arrow", "x": 700, "y": 1340, "dx": -180, "dy": 0, "color": "green", "s": 0.9, "at": "chunk:2"},
    led(190, 1.9, "tm_analyst", arm="point"),
    led(820, 1.7, "mk_manager", mood="happy", arm="wave", at="chunk:1"))

beats = [
    B("title", "title", "In our marketing ladder, Ledger climbed from intern to CMO. One of you asked who designs the posts.",
      ["In our marketing ladder", "Ledger climbed", "from intern to CMO", "One of you asked", ("who designs the posts", "designs")],
      message="Who does what in a marketing team, with Ledger", tag="UNDER 2 MINUTES", gap=0.3),
    B("climb", "title2", "Here is who does what in a marketing team.", ["Here is", "who does what", ("in a marketing team", "team")]),
    B("rung", "r1a", "First, Ledger is the marketing manager, and he sets the goal.",
      ["First, Ledger", ("is the marketing manager", "manager"), "and he sets", ("the goal", "goal")], 1, [("SET THE GOAL", 3)]),
    B("rung", "p1", "The manager is the third rung of the marketing ladder.", [("The manager", "manager"), "is the third rung", "of the marketing ladder"], 1),
    B("rung", "r1b", "Then he plans the campaign and budget.",
      ["Then he plans", ("the campaign", "campaign"), ("and budget", "budget")], 1, [("PLAN THE CAMPAIGN", 1), ("SET THE BUDGET", 2)]),
    B("rung", "r1c", "And he writes the brief.",
      ["And he writes", ("the brief", "brief")], 1, [("WRITE THE BRIEF", 1)]),
    B("climb", "h1", "Then the brief goes to the copywriter.", ["Then the brief", "goes to", ("the copywriter", "copywriter")]),
    B("rung", "r2a", "Now Ledger is the copywriter, and he writes the words.",
      ["Now Ledger", ("is the copywriter", "copywriter"), "and he writes", ("the words", "words")], 2),
    B("rung", "p2", "The copywriter works beside the ladder, not on it.", [("The copywriter", "copywriter"), "works beside the ladder", "not on it"], 2),
    B("rung", "r2b", "He writes the headline first, and then the caption.",
      ["He writes", ("the headline", "headline"), "first, and then", ("the caption", "caption")], 2, [("WRITE HEADLINES", 1), ("WRITE CAPTIONS", 3)]),
    B("climb", "h2", "Next, the words go to the designer.", ["Next, the words", "go to", ("the designer", "designer")]),
    B("rung", "r3a", "Now Ledger is the designer, and he designs the visuals.",
      ["Now Ledger", ("is the designer", "designer"), "and he designs", ("the visuals", "visuals")], 3, [("DESIGN THE POST", 3)]),
    B("rung", "p3", "The designer works beside the ladder, not on it.", [("The designer", "designer"), "works beside the ladder", "not on it"], 3),
    B("rung", "r3c", "Then he picks the colors, the fonts, and the images.",
      ["Then he picks", ("the colors", "colors"), "the fonts", ("and the images", "images")], 3, [("PICK COLORS", 1), ("CHOOSE IMAGES", 3)]),
    B("rung", "r3d", "So this is who designs the posts you see on your screen.",
      ["So this is who", ("designs the posts", "designs"), "you see", "on your screen"], 3),
    B("climb", "h3", "Then the finished design goes to the specialist.", ["Then the finished design", "goes to", ("the specialist", "specialist")]),
    B("rung", "r4a", "Now Ledger is the specialist, and he launches the post.",
      ["Now Ledger", ("is the specialist", "specialist"), "and he launches", ("the post", "post")], 4, [("LAUNCH THE POST", 3)]),
    B("rung", "p4", "The specialist is the second rung of the marketing ladder.", [("The specialist", "specialist"), "is the second rung", "of the marketing ladder"], 4),
    B("rung", "r4b", "He also runs the ads.",
      ["He also runs", ("the ads", "ads")], 4, [("RUN THE ADS", 1)]),
    B("climb", "h4", "After that, the post goes to the intern.", ["After that", "the post goes to", ("the intern", "intern")]),
    B("rung", "r5a", "Now Ledger is the intern, and he schedules the posts ahead.",
      ["Now Ledger", ("is the intern", "intern"), "and he schedules", ("the posts ahead", "posts")], 5, [("SCHEDULE POSTS", 3)]),
    B("rung", "p5", "The intern is the first rung of the marketing ladder.", [("The intern", "intern"), "is the first rung", "of the marketing ladder"], 5),
    B("rung", "r5b", "He also replies to comments.",
      ["He also replies", ("to comments", "comments")], 5, [("REPLY TO COMMENTS", 1)]),
    B("climb", "h5", "Finally, the results go to the analyst.", ["Finally, the results", "go to", ("the analyst", "analyst")]),
    B("rung", "r6a", "Last, Ledger is the analyst, and he measures the results.",
      ["Last, Ledger", ("is the analyst", "analyst"), "and he measures", ("the results", "results")], 6, [("MEASURE RESULTS", 3)]),
    B("rung", "p6", "The analyst works beside the ladder, not on it.", [("The analyst", "analyst"), "works beside the ladder", "not on it"], 6),
    B("rung", "r6b", "Then he reports back to the manager, closing the loop.",
      ["Then he reports", ("back to the manager", "manager"), ("closing the loop", "loop")], 6, [("REPORT BACK", 1)]),
    B("payoff", "closing", "So the ladder shows who you report to, and the team shows who you work with.",
      ["So the ladder shows", ("who you report to", "report"), "and the team shows", ("who you work with", "work with")], gap=0.4),
    B("cta", "cta", CTA2 + ".", ["To understand how", "a business really works", "learn technical", "business concepts", ("at Edlintics", "Edlintics")],
      say=CTA2.replace("Edlintics", "Ed-lin-tics") + ".", message=CTA2),
]

meta = {
    "term": "Marketing team", "title": "Who does what in a marketing team, the career ladder explained with Ledger", "slug": "team-who-does-what-marketing", "rungs": RUNGS,
    "rung_label": "STAGE {n} OF {N}",
    "family_or_category": "marketing", "concept_id": "team-who-does-what-marketing", "themes": ["marketing-careers", "team-roles"],
    "caption": "Who actually makes a marketing post? One post passes through six roles\n\nThe manager sets the goal, the budget and the brief, and the copywriter writes the headline and the caption. Then the designer makes the visuals, the specialist launches the post and runs the ads, and the intern schedules it and replies to comments. Finally, the analyst measures the results and reports back to the manager\n\nThe manager, the specialist and the intern are rungs of the marketing ladder, while the copywriter, the designer and the analyst work beside it. So the ladder shows who you report to, and the team shows who you work with\n\nMissed the ladder? Watch From marketing intern to CMO on our profile\n\n#edlintics #businessstudents #marketing #teamwork",
    "caption_x": "Who makes a marketing post? Manager: goal and brief. Copywriter: the words. Designer: the visuals. Specialist: launch and ads. Intern: schedule and replies. Analyst: results. Missed the ladder? Watch From marketing intern to CMO on our profile #edlintics",
    "first_comment": "Which of these six roles would you want to try first? Tell us below 🎨📣",
    "first_comment_igtt": "Which of these six roles would you want to try first? Tell us below, link in bio 🎨📣",
    "hashtags": ["#edlintics", "#businessstudents", "#marketing", "#teamwork"],
    "threadsTopic": "Marketing", "threadsReason": "A reel on who does what in a marketing team fits the Marketing topic; if the Marketing community is not joined yet, use the topic Business",
    "maths_check": "No numbers are stated except the video length in the title and the count of six roles (manager, copywriter, designer, specialist, intern, analyst), which matches the six stages. No salaries and no currency",
    "sources": [], "definition_check": "", "registry_check": "",
}
if __name__ == "__main__":
    write(os.path.dirname(os.path.abspath(__file__)), meta, S, beats)
