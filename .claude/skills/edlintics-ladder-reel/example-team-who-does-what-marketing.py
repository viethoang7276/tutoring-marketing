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

# stage 1, manager: goal, campaign and budget, brief
S["r1a"] = scene(1,
    {"p": "meter", "x": 700, "y": 1000, "w": 440, "h": 60, "fs": 40, "label": "Goal", "limit": "Target", "to": 0.8, "fill": {"at": "chunk:3", "delay": 0.1, "dur": 1.2}},
    led(230, 2.4, "mk_manager", mood="happy", arm="point"))
S["r1b"] = scene(1,
    {"p": "cal_fill", "x": 700, "y": 965, "size": 70, "gap": 12, "title": "Campaign", "fills": [{"at": "chunk:1", "delay": 0.1, "dur": 1.3, "upto": 20}]},
    {"p": "meter", "x": 700, "y": 1350, "w": 440, "h": 60, "fs": 40, "label": "Budget", "limit": "Limit", "to": 0.86, "fill": {"at": "chunk:3", "delay": 0.1, "dur": 1.1}},
    led(218, 2.0, "mk_manager", arm="point"))
S["r1c"] = scene(1,
    {"p": "note_card", "x": 700, "y": 1060, "w": 440, "title": "The brief", "lines": ["Goal", "Audience", "Budget"], "fs": 46, "rot": -3, "at": "chunk:1"},
    {"p": "arrow", "x": 880, "y": 1400, "dx": -250, "dy": -80, "color": "blue", "s": 1.0, "at": "chunk:2"},
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
    *[{"p": "person", "x": 630 + 122 * i, "y": FEET, "s": 1.4, "color": ["#F2C7C2", "#CFE9D9", "#F3D9A6"][i], "appear": {"at": "chunk:2", "delay": 0.2 * i}} for i in range(3)],
    led(250, 2.3, "mk_specialist", arm="up"))
# stage 5, intern: schedule and replies
S["r5a"] = scene(5,
    {"p": "cal_fill", "x": 700, "y": 965, "size": 70, "gap": 12, "title": "Schedule", "fills": [{"at": "chunk:3", "delay": 0.1, "dur": 1.4, "upto": 20}]},
    {"p": "calendar", "x": 700, "y": 1400, "s": 0.4, "mark": 9, "at": "chunk:3"},
    led(230, 2.3, "mk_intern", mood="happy", arm="point"))
S["r5b"] = scene(5,
    {"p": "phone", "x": 690, "y": 1170, "s": 0.55, "screen": "chat"},
    {"p": "speech", "x": 850, "y": 880, "s": 0.7, "side": "left", "appear": {"at": "chunk:1", "delay": 0.2}},
    {"p": "check", "x": 560, "y": 880, "s": 0.5, "appear": {"at": "chunk:2", "delay": 0.4}},
    led(212, 2.0, "mk_intern", arm="point"))
# stage 6, analyst: measure, report back
S["r6a"] = scene(6,
    {"p": "chart", "x": 690, "y": 930, "s": 1.1, "trend": "up", "reveal": {"at": "chunk:3", "delay": 0.0, "dur": 0.9, "dir": "right"}},
    led(240, 2.3, "tm_analyst", mood="happy", arm="point"))
S["r6b"] = scene(6,
    {"p": "note_card", "x": 440, "y": 1000, "w": 250, "title": "Report", "fs": 40, "at": "chunk:1", "move": [{"at": "chunk:1", "delay": 0.3, "dur": 1.0, "to": [600, 1000], "ease": "inout"}]},
    {"p": "arrow", "x": 700, "y": 1340, "dx": -180, "dy": 0, "color": "green", "s": 0.9, "at": "chunk:3"},
    led(190, 1.9, "tm_analyst", arm="point"),
    led(820, 1.7, "mk_manager", mood="happy", arm="wave", at="chunk:1"))

beats = [
    B("title", "title", "Who actually makes a marketing post? Here is who does what in a marketing team, with Ledger, in ninety seconds.",
      ["Who actually makes", "a marketing post", "Here is", "who does what", "in a marketing team", ("with Ledger", "Ledger")],
      message="Who makes a marketing post? Here is who does what in a marketing team, with Ledger", tag="IN 90 SECONDS", gap=0.3),
    B("rung", "r1a", "First, Ledger is the marketing manager, and he sets the goal.",
      ["First, Ledger", ("is the marketing manager", "manager"), "and he sets", ("the goal", "goal")], 1, [("SET THE GOAL", 3)]),
    B("rung", "r1b", "Then he plans the campaign, and sets its budget.",
      ["Then he plans", ("the campaign", "campaign"), "and sets", ("its budget", "budget")], 1, [("PLAN THE CAMPAIGN", 1), ("SET THE BUDGET", 3)]),
    B("rung", "r1c", "And he writes the brief for the whole team.",
      ["And he writes", ("the brief", "brief"), "for the", "whole team"], 1, [("WRITE THE BRIEF", 1)]),
    B("climb", "h1", "Then the brief goes to the copywriter.", ["Then the brief", "goes to", ("the copywriter", "copywriter")]),
    B("rung", "r2a", "Now Ledger is the copywriter, and he writes the words.",
      ["Now Ledger", ("is the copywriter", "copywriter"), "and he writes", ("the words", "words")], 2),
    B("rung", "r2b", "He writes the headline first, and then the caption.",
      ["He writes", ("the headline", "headline"), "first, and then", ("the caption", "caption")], 2, [("WRITE HEADLINES", 1), ("WRITE CAPTIONS", 3)]),
    B("climb", "h2", "Next, the words go to the designer.", ["Next, the words", "go to", ("the designer", "designer")]),
    B("rung", "r3a", "Now Ledger is the designer, and he designs the visuals.",
      ["Now Ledger", ("is the designer", "designer"), "and he designs", ("the visuals", "visuals")], 3, [("DESIGN THE POST", 3)]),
    B("rung", "r3c", "Then he picks the colors, the fonts, and the images.",
      ["Then he picks", ("the colors", "colors"), "the fonts", ("and the images", "images")], 3, [("PICK COLORS", 1), ("CHOOSE IMAGES", 3)]),
    B("rung", "r3d", "So this is who designs the posts you see on your screen.",
      ["So this is who", ("designs the posts", "designs"), "you see", "on your screen"], 3),
    B("climb", "h3", "Then the finished design goes to the specialist.", ["Then the finished design", "goes to", ("the specialist", "specialist")]),
    B("rung", "r4a", "Now Ledger is the specialist, and he launches the post.",
      ["Now Ledger", ("is the specialist", "specialist"), "and he launches", ("the post", "post")], 4, [("LAUNCH THE POST", 3)]),
    B("rung", "r4b", "He also runs the ads, so more people see it.",
      ["He also runs", ("the ads", "ads"), "so more people", "see it"], 4, [("RUN THE ADS", 1)]),
    B("climb", "h4", "After that, the post goes to the intern.", ["After that", "the post goes to", ("the intern", "intern")]),
    B("rung", "r5a", "Now Ledger is the intern, and he schedules the posts ahead.",
      ["Now Ledger", ("is the intern", "intern"), "and he schedules", ("the posts ahead", "posts")], 5, [("SCHEDULE POSTS", 3)]),
    B("rung", "r5b", "He also replies to the comments as they come in.",
      ["He also replies", ("to the comments", "comments"), "as they", "come in"], 5, [("REPLY TO COMMENTS", 1)]),
    B("climb", "h5", "Finally, the results go to the analyst.", ["Finally, the results", "go to", ("the analyst", "analyst")]),
    B("rung", "r6a", "Last, Ledger is the analyst, and he measures the results.",
      ["Last, Ledger", ("is the analyst", "analyst"), "and he measures", ("the results", "results")], 6, [("MEASURE RESULTS", 3)]),
    B("rung", "r6b", "Then he reports back to the manager, and that closes the loop.",
      ["Then he reports", ("back to the manager", "manager"), "and that", ("closes the loop", "loop")], 6, [("REPORT BACK", 1)]),
    B("payoff", "all", "So one post passes through six pairs of hands, and each role owns one piece.",
      ["So one post", "passes through", ("six pairs of hands", "six pairs"), "and each role", ("owns one piece", "piece")], gap=0.5),
    B("cta", "cta", CTA2 + ".", ["To understand how", "a business really works", "learn technical", "business concepts", ("at Edlintics", "Edlintics")],
      say=CTA2.replace("Edlintics", "Ed-lin-tics") + ".", message=CTA2),
]

meta = {
    "term": "Marketing team", "title": "Who does what in a marketing team, explained with Ledger in 90 seconds", "slug": "team-who-does-what-marketing", "rungs": RUNGS,
    "rung_label": "STAGE {n} OF {N}", "title_question": True,
    "family_or_category": "marketing", "concept_id": "team-who-does-what-marketing", "themes": ["marketing-careers", "team-roles"],
    "caption": "Who actually makes a marketing post? One post passes through six roles\n\nThe manager sets the goal, the budget and the brief, and the copywriter writes the headline and the caption. Then the designer makes the visuals, the specialist launches the post and runs the ads, and the intern schedules it and replies to comments. Finally, the analyst measures the results and reports back to the manager\n\nSo each role owns one piece of the post. Follow one post with Ledger and note which role you would like to try\n\n#edlintics #businessstudents #marketing #teamwork",
    "caption_x": "Who makes a marketing post? Manager: goal and brief. Copywriter: the words. Designer: the visuals. Specialist: launch and ads. Intern: schedule and replies. Analyst: results #edlintics",
    "first_comment": "Which of these six roles would you want to try first? Tell us below 🎨📣",
    "first_comment_igtt": "Which of these six roles would you want to try first? Tell us below, link in bio 🎨📣",
    "hashtags": ["#edlintics", "#businessstudents", "#marketing", "#teamwork"],
    "threadsTopic": "Marketing", "threadsReason": "A reel on who does what in a marketing team fits the Marketing topic; if the Marketing community is not joined yet, use the topic Business",
    "maths_check": "No numbers are stated except the video length in the title and the count of six roles (manager, copywriter, designer, specialist, intern, analyst), which matches the six stages. No salaries and no currency",
    "sources": [], "definition_check": "", "registry_check": "",
}
if __name__ == "__main__":
    write(os.path.dirname(os.path.abspath(__file__)), meta, S, beats)
