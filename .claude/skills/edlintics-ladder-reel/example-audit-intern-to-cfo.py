"""Career-ladder reel "Audit intern to CFO" (the first ladder reel, look approved by Hoang 13 Nov 2026).
Run: python example-audit-intern-to-cfo.py <workdir>   (writes <workdir>/script.json; then build with make_reel.sh)
Copy this file to <workdir>/gen.py for a new career and change the parts marked CHANGE."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # CHANGE in a copy: the path of .claude/skills/edlintics-ladder-reel
from ladder_script import *   # noqa: F401,F403

OUT = ["intern", "senior", "manager", "controller", "cfo"]                                   # CHANGE: the five outfits, bottom rung first
RUNGS = ["THE INTERN", "THE SENIOR", "THE MANAGER", "THE CONTROLLER", "THE CFO"]            # CHANGE: header titles, 17 characters at most
L = Ladder(OUT, ["INTERN", "SENIOR", "MANAGER", "CONTROLLER", "CFO"],                        # CHANGE: tags on the ladder
           brackets=[("AUDIT FIRM", 0, 2, "ink"), ("COMPANY", 3, 4, "blue")], dial=("Counts", "Decides"))

S = {}
# ---- title and ladder shots (helpers). climb(k, go, name): go = the chunk he starts climbing on, name = the chunk that names the next role
S["title"] = L.title()
S["climb1"] = L.climb(0, go=0, name=1)
S["climb2"] = L.climb(1, go=0, name=1)
S["climb3"] = L.climb(2, go=0, name=2, pulses={1: "chunk:1"})
S["climb4"] = L.climb(3, go=0, name=2)

# ---- rung 1, the intern
S["r1a"] = scene(1,
    led(470, 3.4, "intern", mood="happy", arm="wave"),
    {"p": "arrow", "x": 880, "y": 1400, "dx": -290, "dy": -50, "color": "blue", "s": 1.0, "at": "chunk:2"},
    {"p": "arrow", "x": 925, "y": 1010, "dx": -150, "dy": 130, "color": "blue", "s": 1.0, "at": "chunk:3"})
S["r1b"] = scene(1,
    {"p": "match_rows", "x": 690, "y": 1070, "w": 480, "n": 4, "bad": 2, "rh": 130, "fs": 36, "link": {"at": "chunk:1", "every": 0.45}, "tick": {"at": "chunk:4", "delay": 0.1, "every": 0.4}, "flag": {"at": "chunk:7"}},
    led(212, 2.0, "intern", arm="point"))
S["r1c"] = scene(1,
    L.dial_item(490, 770, 720, start=0.06),
    *[{"p": "invoice", "x": 650 + 95 * (i % 3) + 14 * (i // 3), "y": 1400 - 180 * (i // 3) - 8 * (i % 3), "s": 0.6, "rot": [-8, 4, -3, 7, -5, 3][i], "appear": {"at": "chunk:1", "delay": 0.16 * i}} for i in range(6)],
    {"p": "calculator", "x": 548, "y": 1262, "s": 0.5, "display": "", "rot": 8},
    led(300, 2.4, "intern", arm="hold"))

# ---- rung 2, the senior
S["r2a"] = scene(2,
    {"p": "building", "x": 805, "y": 1252, "s": 0.8, "done": True, "at": "chunk:2"},
    {"p": "person", "x": 712, "y": FEET, "s": 1.25, "color": "#F3D9A6", "appear": {"at": "chunk:1", "delay": 0.0}},
    {"p": "person", "x": 872, "y": FEET, "s": 1.25, "color": "#CFE9D9", "appear": {"at": "chunk:1", "delay": 0.2}},
    {"p": "clipboard", "x": 596, "y": 1250, "s": 0.58, "rot": 6},
    led(335, 2.5, "senior", arm="hold"))
S["r2b"] = scene(2,
    {"p": "test_picker", "x": 696, "y": 1085, "w": 480, "rh": 120, "pick": {"at": "chunk:2", "every": 0.35}},
    led(218, 2.0, "senior", arm="point"))
S["r2c"] = scene(2,
    {"p": "invoice", "x": 645, "y": 965, "s": 1.3, "rot": -3},
    *[{"p": "check", "x": 782, "y": 836 + 47 * i, "s": 0.38, "appear": {"at": "chunk:0", "delay": 0.3 + 0.3 * i}} for i in range(4)],
    {"p": "person", "x": 852, "y": FEET, "s": 1.55, "color": "#7FA0DC", "at": "chunk:1"},
    led(285, 2.3, "senior", arm="point"))

# ---- rung 3, the manager
S["r3a"] = scene(3,
    {"p": "clipboard", "x": 770, "y": 900, "s": 1.0, "rot": 4, "at": "chunk:2"},
    *[{"p": "person", "x": 640 + 122 * i, "y": FEET, "s": 1.45, "color": ["#F3D9A6", "#7FA0DC", "#CFE9D9"][i], "appear": {"at": "chunk:3", "delay": 0.2 * i}} for i in range(3)],
    led(290, 2.4, "manager", arm="point"))
S["r3b"] = scene(3,
    {"p": "cal_fill", "x": 700, "y": 965, "size": 70, "gap": 12, "title": "Hours", "fills": [{"at": "chunk:0", "delay": 0.2, "dur": 1.5, "upto": 20}]},
    {"p": "meter", "x": 700, "y": 1350, "w": 440, "h": 60, "fs": 40, "label": "Budget", "limit": "Limit", "to": 0.86, "fill": {"at": "chunk:1", "delay": 0.3, "dur": 1.2}},
    led(218, 2.0, "manager", arm="point"))
S["r3c"] = scene(3,
    {"p": "bubble", "x": 310, "y": 800, "s": 1.6, "label": "?", "side": "down", "at": "chunk:1"},
    {"p": "person", "x": 810, "y": FEET, "s": 1.8, "color": "#CFE9D9", "at": "chunk:3"},
    {"p": "phone", "x": 640, "y": 1180, "s": 0.3, "screen": "call", "appear": {"at": "chunk:3", "delay": 0.25}, "shake": {"at": "chunk:3", "delay": 0.4, "dur": 0.8, "amp": 6, "hz": 9}},
    {"p": "speech", "x": 745, "y": 900, "s": 0.65, "side": "right", "appear": {"at": "chunk:3", "delay": 0.7}},
    led(300, 2.4, "manager", mood="flat", arm="down", until="chunk:3"),
    led(300, 2.4, "manager", mood="smile", arm="phone", at="chunk:3", pop="cut"))

# ---- rung 4, the controller
S["r4a"] = scene(4,
    {"p": "desk", "x": 775, "y": 1287, "w": 320},
    {"p": "laptop", "x": 775, "y": 1182, "s": 0.8, "screen": "sheet"},
    {"p": "books", "x": 775, "y": 1425, "s": 0.6, "n": 4, "at": "chunk:1"},
    led(310, 2.5, "controller", arm="point"))
S["r4b"] = scene(4,
    {"p": "checklist", "x": 695, "y": 1020, "w": 480, "rh": 110, "tick": {"at": "chunk:1", "delay": 0.15, "every": 0.5}},
    {"p": "calendar", "x": 695, "y": 1400, "s": 0.5, "mark": 27},
    led(218, 2.0, "controller", arm="point"))
S["r4c"] = scene(4,
    {"p": "chart", "x": 690, "y": 905, "s": 1.0, "trend": "up", "at": "chunk:1"},
    {"p": "check", "x": 880, "y": 770, "s": 0.6, "appear": {"at": "chunk:1", "delay": 0.45}},
    *[{"p": "person", "x": 630 + 122 * i, "y": FEET, "s": 1.4, "color": ["#F2C7C2", "#CFE9D9", "#F3D9A6"][i], "appear": {"at": "chunk:2", "delay": 0.2 * i}} for i in range(3)],
    led(285, 2.4, "controller", arm="up"))

# ---- rung 5, the CFO
PX = [524, 692, 856]
S["r5a"] = scene(5,
    {"p": "bills", "x": 690, "y": 840, "s": 1.0, "n": 4},
    *[{"p": "pot", "x": PX[i], "y": 1150, "s": 1.0, "label": ["Growth", "Debt", "Owners"][i], "color": ["blue", "amber", "green"][i], "fs": 34} for i in range(3)],
    *[{"p": "coin_stream", "x": 690, "y": 880, "to": [PX[i], 1150], "n": 4, "dur": 0.7, "stagger": 0.14, "arc": 80, "s": 1.15, "at": "chunk:1", "delay": 0.55 * i} for i in range(3)],
    led(200, 1.9, "cfo", arm="point"))
S["r5b"] = scene(5,
    {"p": "chart", "x": 255, "y": 860, "s": 0.82, "trend": "up", "reveal": {"at": "chunk:0", "delay": 0.1, "dur": 0.8, "dir": "right"}},
    {"p": "board_table", "x": 705, "y": 900, "w": 430, "n": 3, "colors": ["#BFE6CF", "#D8F1E3", "#BFE6CF"], "seat": {"at": "chunk:2", "every": 0.2}},
    {"p": "order_chip", "x": 705, "y": 998, "label": "Investors", "color": "light", "fs": 36, "at": "chunk:2"},
    {"p": "board_table", "x": 705, "y": 1270, "w": 460, "n": 3, "seat": {"at": "chunk:1", "every": 0.2}},
    {"p": "order_chip", "x": 705, "y": 1368, "label": "Board", "color": "light", "fs": 36, "at": "chunk:1"},
    led(225, 2.0, "cfo", arm="point"))
S["r5c"] = scene(5,
    L.dial_item(490, 770, 720, start=0.06, slide={"at": "chunk:0", "delay": 0.2, "to": 0.95, "dur": 1.3}),
    led(490, 3.0, "cfo", mood="smile", arm="shrug", until="chunk:2"),
    led(490, 3.0, "cfo", mood="happy", arm="up", at="chunk:2", pop="cut"))

# ---- payoff and closing scene
S["all"] = L.all(slide_chunk=1)
S["cta"] = L.cta()

beats = [
    L.title_beat("audit intern", "CFO"),   # beat 1: the title card. Beat 2 starts the first rung straight away (Hoang, 13 Nov 2026)
    B("rung", "r1a", "First, Ledger is the audit intern, with a badge and a backpack.",
      ["First, Ledger", ("is the audit intern", "intern"), "with a badge", "and a backpack"], 1),
    B("rung", "r1b", "He matches each invoice to the ledger, line by line.",
      ["He matches", ("each invoice", "invoice"), "to the ledger", "line by line"], 1, [("MATCH INVOICES", 1)]),
    B("rung", "r1b", "Then he ticks every number that agrees, and flags the rest.",
      [("Then he ticks", "ticks"), "every number", "that agrees", "and flags the rest"], 1, [("TICK AND TIE", 0), ("FLAG GAPS", 3)]),
    B("rung", "r1c", "On this rung, he counts everything himself.",
      ["On this rung", ("he counts everything", "everything"), "himself"], 1, [("COUNT IT ALL", 1)]),
    B("climb", "climb1", "After that, he climbs to senior.", ["After that, he climbs", ("to senior", "senior")]),
    B("rung", "r2a", "Now he runs the fieldwork at the client's office.",
      ["Now he runs", ("the fieldwork", "fieldwork"), "at the client's office"], 2, [("RUN FIELDWORK", 1)]),
    B("rung", "r2b", "He helps decide which numbers are big enough to test.",
      ["He helps decide", "which numbers", ("are big enough", "big enough"), "to test"], 2, [("PICK THE TESTS", 3)]),
    B("rung", "r2c", "And he reviews the intern's work.",
      [("And he reviews", "reviews"), "the intern's work"], 2, [("REVIEW WORK", 0)]),
    B("climb", "climb2", "Then he climbs again, to manager.", ["Then he climbs again", ("to manager", "manager")]),
    B("rung", "r3a", "As manager, he leads the whole engagement and its team.",
      ["As manager", "he leads", "the whole engagement", ("and its team", "team")], 3, [("LEAD THE TEAM", 1)]),
    B("rung", "r3b", "He plans the hours, so the job stays on budget.",
      [("He plans the hours", "hours"), "so the job stays", "on budget"], 3, [("PLAN THE HOURS", 0), ("HOLD THE BUDGET", 2)]),
    B("rung", "r3c", "And when a hard question comes up, he calls the client.",
      ["And when", "a hard question", "comes up", ("he calls the client", "client")], 3, [("CALL THE CLIENT", 3)]),
    B("climb", "climb3", "Next, he joins a company as controller.", ["Next, he joins", "a company", ("as controller", "controller")]),
    B("rung", "r4a", "Now he runs the company's accounting.",
      ["Now he runs", ("the company's accounting", "accounting")], 4, [("RUN ACCOUNTING", 1)]),
    B("rung", "r4b", "Every month, he closes the books, step by step.",
      ["Every month", ("he closes the books", "closes"), "step by step"], 4, [("CLOSE THE BOOKS", 1)]),
    B("rung", "r4c", "Then he signs off the reports that everyone relies on.",
      [("Then he signs off", "signs off"), "the reports", "that everyone", "relies on"], 4, [("SIGN THE REPORTS", 0)]),
    B("climb", "climb4", "Finally, he reaches the top rung, as CFO.", ["Finally, he reaches", "the top rung", ("as CFO", "CFO")]),
    B("rung", "r5a", "Now he decides where the company's money goes next.",
      [("Now he decides", "decides"), "where the company's money", "goes next"], 5, [("ALLOCATE CAPITAL", 0)]),
    B("rung", "r5b", "He explains the numbers to the board, and to investors.",
      ["He explains the numbers", ("to the board", "board"), "and to investors"], 5, [("BRIEF THE BOARD", 1), ("FACE INVESTORS", 2)]),
    B("rung", "r5c", "He hardly counts anything himself, yet he answers for every number.",
      ["He hardly counts", "anything himself", ("yet he answers", "answers"), "for every number"], 5, [("OWN THE NUMBERS", 2)]),
    B("payoff", "all", "So with each rung, Ledger counted less, and decided more.",
      ["So with each rung", "Ledger counted less", ("and decided more", "decided more")], gap=0.5),
    L.cta_beat(),
]

meta = {
    "term": "Career ladder", "title": "From audit intern to CFO, the career ladder explained with Ledger in 90 seconds", "slug": "ladder-audit-intern-to-cfo", "rungs": RUNGS,
    "family_or_category": "accounting", "concept_id": "career-ladder-audit-to-cfo", "themes": ["career-ladder", "audit"],
    "caption": "From audit intern to CFO, the job changes on every rung\n\nThe intern matches invoices and ticks numbers, and the senior runs the fieldwork. Then the manager leads the team and the budget, and the controller closes the books every month. Finally, the CFO decides where the money goes and explains the numbers to the board\n\nSo each rung up, you count less yourself and decide more. Walk up the ladder with Ledger and note which rung you are on\n\n#edlintics #businessstudents #accounting #finance",
    "caption_x": "Audit intern to CFO in five rungs: match invoices, run the fieldwork, lead the team, close the books, allocate capital. Each rung up, you count less and decide more #edlintics",
    "first_comment": "Which rung are you on right now? Tell us below 🪜📊",
    "first_comment_igtt": "Which rung are you on right now? Tell us below, link in bio 🪜📊",
    "hashtags": ["#edlintics", "#businessstudents", "#accounting", "#finance"],
    "threadsTopic": "Accounting", "threadsReason": "The audit-to-CFO path is an accounting career story, so Accounting is the closest topic",
    "maths_check": "No career numbers are stated. The only number is the video length in the title (ninety seconds): the built video must be 90 s or less. No currency amounts (the coins carry a $ sign)",
    "sources": [
        "https://tgg-accounting.com/how-to-become-a-cfo/",
        "https://www.accountingtools.com/articles/vouching", "https://www.indeed.com/hire/job-description/audit-intern",
        "https://accountingtools.com/articles/accountant-in-charge", "https://www.lhh.com/en-us/insights/job-descriptions/audit-manager",
        "https://trullion.com/blog/controller-vs-cfo/", "https://corporatefinanceinstitute.com/resources/career/what-does-a-cfo-do/"],
    "definition_check": "No term is defined in this reel. Role duties were checked against the sources (12 Nov 2026)",
    "registry_check": "registry check: clear on concepts (no concept or related concept is repeated). Theme career-ladder runs on four days in a row, 13-16 Nov 2026, cleared by Hoang on 13 Nov 2026 (\"We will post 3 more ladder career next 3 days\")",
}

if __name__ == "__main__":
    write(sys.argv[1] if len(sys.argv) > 1 else os.getcwd(), meta, S, beats)
