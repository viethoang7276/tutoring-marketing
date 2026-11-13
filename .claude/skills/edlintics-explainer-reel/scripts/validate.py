"""Check a reel script.json before building (rules of 25 Oct 2026: no camera moves, end card last). Exit code 1 and a list of problems if anything fails.

Usage: python validate.py <workdir>/script.json
Checks the house rules (voice, captions, currency, no tutoring, no trailing full stop), the beat structure for
meta.type "definition" or "life-of", the scene presets, and an estimated length (up to 2 minutes for every type from 4 Nov 2026).
meta.type "lesson" (in-lesson videos, 5 Nov 2026): no time cap (ideal 2-3 min), roles in any order, at least one defcard, nothing
promotional (no end card, logo, follow line or loop-back), currency may follow the course (meta.currency).
meta.type "ad" (paid ad creatives, 29 Oct 2026): 1-4 hooks, 2-3 points, one cta, end card, 22-30 s; tutoring and "book a
session" are allowed there (the organic no-tutoring rule does not apply to paid ads), and only type/term/title/slug are required in meta.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene_lib as L

WPS = 2.95          # spoken words per second at speed 1.08, gaps included (measured on sunk cost v4)
ROLES = {  # "loop" (a line leading back to the hook) is optional; "endcard" is required and always last
    "definition": {"order": ["hook", "story", "definition", "example", "takeaway", "loop", "endcard"],
                   "min": {"hook": 1, "story": 2, "definition": 1, "example": 2, "takeaway": 1, "endcard": 1}},
    "life-of": {"order": ["hook", "moment", "turn", "concept", "lesson", "loop", "endcard"],
                "min": {"hook": 1, "moment": 3, "turn": 1, "concept": 1, "lesson": 1, "endcard": 1}},
    # Ledger talks to camera (edlintics-ledger-talks): a hook, the points of the argument, a business takeaway, the end card
    "ledger-talks": {"order": ["hook", "point", "takeaway", "loop", "endcard"],
                     "min": {"hook": 1, "point": 3, "takeaway": 1, "endcard": 1}},
    # how-to reel (1 Nov 2026): "How [role] in [industry] deals with [problem]": hook question, the problem with a number,
    # 4 steps (one scene each, a step may take 2 beats), the named concept, the held 4-box summary diagram, the takeaway, end card
    "howto": {"order": ["hook", "problem", "step", "concept", "summary", "takeaway", "loop", "endcard"],
              "min": {"hook": 1, "problem": 1, "step": 4, "concept": 1, "summary": 1, "takeaway": 1, "endcard": 1}},
    # paid ad (29 Oct 2026): a hook, 2-3 selling points, one call to action, the end card
    "ad": {"order": ["hook", "point", "cta", "endcard"],
           "min": {"hook": 1, "point": 2, "cta": 1, "endcard": 1}, "max": {"hook": 5, "point": 5, "cta": 1}},   # 5 hooks: Hoang's urgent opener (29 Oct 2026)
    # in-lesson video (Hoang, 5 Nov 2026): an optional hook question first, then the rest in any order; defcards (term +
    # definition card, no logo) may sit after a section or all at the end, and may be last. No endcard, cta or loop
    "lesson": {"order": ["hook", "story", "definition", "example", "defcard", "takeaway"], "free": True,
               "min": {"defcard": 1}, "max": {"hook": 1}},
    # career-ladder reel (12 Nov 2026): a hook on the ladder, then for each rung its "rung" beats (the job on that rung, with duty chips)
    # and a "climb" beat to the next rung, a payoff (the wide shot) and the end card. Rung and climb beats alternate, so the order is free
    # 13 Nov 2026: the reel may close on a "cta" beat (a scene with a "message" card and the logo) instead of the end card
    # 13 Nov 2026 (Hoang: "avoid the hook just go directly to the point"): beat 1 is a "title" beat (a title card with a "message") and beat 2 starts the first rung
    "ladder": {"order": ["title", "hook", "rung", "climb", "payoff", "cta", "endcard"], "free": True,
               "min": {"rung": 3, "climb": 1, "payoff": 1}},
    # map reel (13 Nov 2026, opt-in): a title card, then for each stop on the map its "stop" beats (the city, its career, one sourced fact),
    # a "summary" beat (the whole map with every pin), and one or two closing "cta" cards. Uses the ladder layout in its bleed style
    "map": {"order": ["title", "stop", "summary", "cta"], "free": True, "min": {"title": 1, "stop": 5, "summary": 1, "cta": 1}, "max": {"cta": 2}},   # 13 Nov 2026: series parts have 5-6 stops (two beats each)
}
# per type: caption chunk words, beats, word target, allowed words, length (s), spoken words per second
# 4 Nov 2026 (Hoang): "Put all of video to 2 mins cap" - every type may run to 2 minutes
SPEC = {"definition": dict(chunk=(2, 5), beats=(9, 34), target=(100, 115), allowed=(85, 330), secs=(29, 121), wps=2.95),
        # life-of: 30-60 s target; hard cap 2 minutes from 3 Nov 2026 (Hoang: "limit up 2 minutes for videos", replacing the 1-minute cap)
        "life-of": dict(chunk=(2, 5), beats=(9, 30), target=(105, 180), allowed=(85, 350), secs=(29, 121), wps=2.95),
        # howto: ElevenLabs v3 voice at tempo 1.12 (about 2.4 spoken words a second with gaps, measured 1 Nov 2026).
        # 60-90 s target; hard cap 2 minutes from 3 Nov 2026 (Hoang: "limit up 2 minutes for videos")
        "howto": dict(chunk=(2, 5), beats=(12, 40), target=(115, 220), allowed=(100, 285), secs=(44, 121), wps=2.4),
        "ledger-talks": dict(chunk=(1, 3), beats=(8, 34), target=(80, 105), allowed=(65, 350), secs=(24, 121), wps=3.05),
        # ad: 1-4 short hook questions (a problem montage), 2-3 points, a CTA; the ad voice (ElevenLabs v3 dfeOmy6Uay63tNhyO99j
        # at ELEVEN_TEMPO 1.15) speaks about 2.3 words a second (measured 29 Oct 2026); points may run 5-7 s (one line, one scene)
        "ad": dict(chunk=(2, 5), beats=(5, 18), target=(55, 75), allowed=(45, 260), secs=(21, 121), wps=2.3),
        # lesson (Hoang, 5 Nov 2026): "no time cap for in lesson video (ideal time is 2-3 minutes)"; 60 s to about 4 minutes
        "lesson": dict(chunk=(2, 5), beats=(6, 120), target=(354, 531), allowed=(177, 708), secs=(59, 241), wps=2.95),
        # ladder: karaoke chunks of 1-4 words low in the frame; ElevenLabs v3 at tempo 1.12 (about 2.4 words a second with gaps); 90-110 s target, 2-minute cap
        "ladder": dict(chunk=(1, 4), beats=(12, 60), target=(200, 265), allowed=(120, 285), secs=(44, 121), wps=2.4),
        "map": dict(chunk=(1, 4), beats=(12, 60), target=(150, 270), allowed=(120, 285), secs=(44, 121), wps=2.4)}   # 4 Nov 2026 (Hoang ok): full-sentence voice at tempo 1.0, about 38 s, 42 s with the price line   # Hoang 29 Oct 2026: 32 s target, 35 s acceptable for the emotional cut
FRAMES = ("auto", "content", "ledger", "ledger-close", "wide")
CTX_OPEN = re.compile(r"\b(let's (imagine|use|take|say|look at|picture|follow|start with|walk through|see)|imagine|picture|suppose|for this,? let's|take the example|as (an|our) example|to see (this|why|how))\b", re.I)
CTX_BACK = re.compile(r"\b(continu(e|es|ing)|back (to|in|at|with)|going back|returning to|let's return|let's go back|staying with|still with|in our (story|example)|from the last example|same (story|example|sheet|store|shop|company)|now let's|let's (now |also )?(use|take|look at|see|apply|imagine)|imagine|as (a|an|our) (business )?example|for example|in business)\b", re.I)
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF\U00002300-\U000023FF\U00002B00-\U00002BFF️]")  # + ⏳⌛⏰ and ⭐
TUTOR = re.compile(r"\btutor(s|ing|ed)?\b|\b1[:-]1\b|\bprivate lesson|\bbook a (session|call|class)", re.I)
CURRENCY_SIGN = re.compile(r"[$€£¥₫]")
REQ_META = ["type", "term", "title", "slug", "caption", "caption_x", "first_comment", "threadsTopic", "threadsReason", "maths_check"]
REQ_META_AD = ["type", "term", "title", "slug"]  # an ad's text lives in Ads Manager, not in caption/first comment
REQ_META_LESSON = ["type", "title", "slug"]   # a lesson video is not posted: no caption, first comment or Threads fields
PROMO = re.compile(r"\bfollow (us|edlintics|for more)\b|\blike and (share|subscribe)\b|\bsubscribe\b|\blink in (the )?bio\b|\bedlintics(\.com| dot com)?\b|\bwatch (till|until|to) the end\b|\bwait for it\b|\byou won'?t believe\b", re.I)


def words(s):
    return [w for w in re.split(r"\s+", s.strip()) if re.search(r"[A-Za-z0-9$]", w)]


def main(path):
    S = json.load(open(path)); E, W = [], []
    m = S.get("meta", {}); t = m.get("type")
    for k in (REQ_META_AD if t == "ad" else REQ_META_LESSON if t == "lesson" else REQ_META):
        if not m.get(k): E.append(f"meta.{k} is missing")
    if t not in ROLES:
        E.append('meta.type must be "definition", "life-of", "ledger-talks", "howto", "ad", "lesson", "ladder" or "map"'); t = "definition"
    P = SPEC[t]; WPS_T = P["wps"]
    beats, scenes = S.get("beats", []), S.get("scenes", {})
    # Ledger's arm and hand proportions (Hoang, 25 Oct 2026: "the hands are not proportional, check that every time")
    for e in L.check_proportions(): E.append(f"scene_lib: {e}")
    # scenes and presets
    for name, sp in scenes.items():
        if sp.get("bg", "paper") not in L.BACKGROUNDS: E.append(f"scene {name}: unknown bg {sp.get('bg')!r} (use {', '.join(L.BACKGROUNDS)})")
        for it in sp.get("items", []):
            p = it.get("p")
            if p not in L.PRESETS: E.append(f"scene {name}: unknown preset {p!r} (run scene_lib.py --list)"); continue
            if "x" not in it or "y" not in it: E.append(f"scene {name}: item {p} needs x and y")
            if p == "ledger":
                if it.get("mood", "smile") not in L.MOODS: E.append(f"scene {name}: ledger mood {it.get('mood')!r} not in {L.MOODS}")
                if it.get("arm", "down") not in L.ARMS: E.append(f"scene {name}: ledger arm {it.get('arm')!r} not in {L.ARMS}")
                if it.get("larm") and it["larm"] not in L.LARMS: E.append(f"scene {name}: ledger larm {it.get('larm')!r} not in {L.LARMS}")
                if it.get("outfit", "suit") not in L.OUTFITS: E.append(f"scene {name}: ledger outfit {it.get('outfit')!r} not in {L.OUTFITS}")
    # beats
    if not P["beats"][0] <= len(beats) <= P["beats"][1]: E.append(f"{len(beats)} beats; use {P['beats'][0]}-{P['beats'][1]} beats of 2-4 s")
    roles = [b.get("role") for b in beats]
    R = ROLES[t]
    card_cta = t == "ad" and beats and bool(beats[-1].get("cta"))   # ad: the end card may carry the CTA as a button pill
    for r, n in R["min"].items():
        if r == "cta" and card_cta: continue
        if roles.count(r) < n: E.append(f'needs at least {n} beat(s) with role "{r}" (has {roles.count(r)})')
    for r, n in R.get("max", {}).items():
        if roles.count(r) > n: E.append(f'at most {n} beat(s) with role "{r}" (has {roles.count(r)})')
    texts_extra_cta = []
    bad = [r for r in roles if r not in R["order"]]
    if bad: E.append(f"unknown roles {sorted(set(map(str, bad)))}; {t} roles are {R['order']}")
    seq = [R["order"].index(r) for r in roles if r in R["order"]]
    if t == "lesson":   # any order; the hook, when there is one, opens the video as a direct question
        if "hook" in roles[1:]: E.append("lesson: the hook (optional) can only be beat 1")
        if roles and roles[0] == "hook" and "?" not in beats[0].get("text", ""): E.append("lesson: the hook must ask the learner a direct question (end it with ?)")
    elif t == "ladder":   # title (or the older hook) first, cta or end card last; rung and climb beats alternate up the ladder; the payoff comes after the last rung
        if roles and roles[0] not in ("title", "hook"): E.append('beat 1 must be the title beat (role "title" with a "message": what the video is, for example "From audit intern to CFO, the career ladder explained with Ledger")')
        if "title" in roles[1:]: E.append("the title beat can only be beat 1")
        if roles and roles[0] == "title":
            b0 = beats[0]; tg = str(b0.get("tag", ""))
            if len(tg) > 16 or tg.rstrip().endswith("."): E.append('beat 1: the title "tag" (for example "IN 90 SECONDS") is 16 characters at most, with no full stop')
            if tg: texts_extra_cta.append(("title tag", tg))
            if "?" in b0.get("text", ""): E.append("beat 1: the title says what the video is; it is not a question or a teaser (Hoang, 13 Nov 2026)")
            if re.search(r"\b(90|ninety) seconds\b", (b0.get("text", "") + " " + tg), re.I): W.append("beat 1 says the video takes 90 seconds: after the build, check timing.json duration is 90 s or less, or say \"in under two minutes\"")
        if roles and roles[-1] not in ("endcard", "cta"): E.append('the last beat must be the end card (role "endcard" with "term" and "keypoint") or a "cta" beat with a "message"')
        if roles.count("endcard") + roles.count("cta") > 1: E.append("only one closing beat (end card or cta)")
        if m.get("ladder_style") not in (None, "panel", "bleed"): E.append('ladder: meta.ladder_style must be "bleed" (full-bleed art, captions on top) or left out (the panel style)')
        for k, b in enumerate(beats, 1):
            if b.get("role") not in ("cta", "title"): continue
            msg = str(b.get("message", ""))
            if not 4 <= len(words(msg)) <= 16 or len(msg) > 90: E.append(f'beat {k}: a {b.get("role")} beat needs "message", 4-16 words and 90 characters at most')
            if msg.rstrip().endswith("."): E.append(f"beat {k}: the {b.get('role')} message ends with a full stop")
            texts_extra_cta.append((f"{b.get('role')} message", msg))
        rungs = m.get("rungs") or []
        if not (isinstance(rungs, list) and 2 <= len(rungs) <= 7 and all(isinstance(r, str) and r.strip() for r in rungs)): E.append('ladder: meta.rungs must list 2-7 rung titles, bottom rung first (for example "THE INTERN")')
        for r in rungs if isinstance(rungs, list) else []:
            if len(str(r)) > 17: E.append(f'ladder: rung title "{r}" is over 17 characters; it must fit beside the logo')
            if str(r).rstrip().endswith("."): E.append(f'ladder: rung title "{r}" ends with a full stop')
        if m.get("layout") != "ladder": E.append('ladder: set meta.layout to "ladder" (rung header on top, captions low)')
        seen = []
        for k, b in enumerate(beats, 1):
            r = b.get("role"); n = b.get("rung")
            if r == "rung":
                if not (isinstance(n, int) and 1 <= n <= len(rungs)): E.append(f'beat {k}: a rung beat needs "rung": 1-{len(rungs)} (its place in meta.rungs)'); continue
                if seen and n < seen[-1]: E.append(f"beat {k}: rung {n} comes after rung {seen[-1]}; the ladder only goes up")
                if n not in seen: seen.append(n)
            elif n is not None: E.append(f'beat {k}: only rung beats carry "rung" (the header hides on hook, climb and payoff beats)')
            cps = b.get("chips") or []
            if cps and r != "rung": E.append(f"beat {k}: duty chips belong to rung beats")
            for c in cps:
                lab = str(c.get("label", ""))
                if not 1 <= len(words(lab)) <= 3 or len(lab) > 17: E.append(f'beat {k}: chip "{lab}" must be 1-3 words and 17 characters at most')
                if lab.rstrip().endswith("."): E.append(f'beat {k}: chip "{lab}" ends with a full stop')
                if not (isinstance(c.get("at", 0), int) and 0 <= c.get("at", 0) < len(b.get("chunks") or [])): E.append(f'beat {k}: chip "{lab}" needs "at": the index of the caption chunk that names the duty (0-{len(b.get("chunks") or []) - 1})')
        if isinstance(rungs, list) and seen != list(range(1, len(rungs) + 1)): E.append(f"ladder: every rung in meta.rungs needs at least one rung beat, in order (found {seen})")
        for n in seen:
            nc = sum(len(b.get("chips") or []) for b in beats if b.get("rung") == n)
            if not 1 <= nc <= 4: E.append(f"ladder: rung {n} has {nc} duty chips; use 1-4 (two rows at most)")
        if "payoff" in roles and "rung" in roles[roles.index("payoff"):]: E.append("ladder: the payoff comes after the last rung")
        if roles and roles[0] == "hook" and not any(CTX_OPEN.search(b.get("text", "")) for b in beats if b.get("role") == "hook"): E.append("context transition: a hook beat " + "must open the story out loud, for example \"Let's follow Ledger up the ladder ...\" (Hoang, 6 Nov 2026)")
    elif t == "map":   # MAP REELS BLOCK (13 Nov 2026): title first, stops in order, the summary map after the last stop, one or two cta cards last
        if roles and roles[0] != "title": E.append('map: beat 1 must be the title beat (role "title" with a "message": what the video is)')
        if "title" in roles[1:]: E.append("map: the title beat can only be beat 1")
        if roles and roles[-1] != "cta": E.append('map: the last beat must be a "cta" beat with a "message"')
        if "cta" in roles and any(r != "cta" for r in roles[roles.index("cta"):]): E.append("map: the cta beats close the reel; nothing comes after them")
        if m.get("layout") != "ladder" or m.get("ladder_style") != "bleed": E.append('map: set meta.layout to "ladder" and meta.ladder_style to "bleed" (full-bleed art, captions on top)')
        if roles and roles[0] == "title":
            tg = str(beats[0].get("tag", ""))
            if len(tg) > 18 or tg.rstrip().endswith("."): E.append('beat 1: the title "tag" is 18 characters at most, with no full stop')
            if tg: texts_extra_cta.append(("title tag", tg))
            if "?" in beats[0].get("text", ""): E.append("beat 1: the title says what the video is; it is not a question or a teaser (Hoang, 13 Nov 2026)")
            if re.search(r"\b\d+ seconds\b|\b(ninety|hundred) seconds\b", beats[0].get("text", "") + " " + tg, re.I): W.append("beat 1 states a length in seconds: after the build, check timing.json duration is that or less, or say \"in under two minutes\"")
        for k, b in enumerate(beats, 1):
            if b.get("role") not in ("cta", "title"): continue
            msg = str(b.get("message", ""))
            if not 4 <= len(words(msg)) <= 16 or len(msg) > 90: E.append(f'beat {k}: a {b.get("role")} beat needs "message", 4-16 words and 90 characters at most')
            if msg.rstrip().endswith("."): E.append(f"beat {k}: the {b.get('role')} message ends with a full stop")
            texts_extra_cta.append((f"{b.get('role')} message", msg))
        stops = m.get("rungs") or []; cities = m.get("cities") or []
        if not (isinstance(stops, list) and 5 <= len(stops) <= 12 and all(isinstance(r, str) and r.strip() for r in stops)): E.append("map: meta.rungs must list the 5-12 stops (city names for the header), in travel order")
        for r in stops if isinstance(stops, list) else []:
            if len(str(r)) > 15: E.append(f'map: stop title "{r}" is over 15 characters; it must fit beside the stop counter and the logo')
        if not (isinstance(cities, list) and len(cities) == len(stops)): E.append("map: meta.cities must hold one {city, career, fact, source, figureDate} per stop")
        for c in cities if isinstance(cities, list) else []:
            for kk in ("city", "career", "fact", "source", "figureDate"):
                if not (isinstance(c, dict) and str(c.get(kk, "")).strip()): E.append(f"map: meta.cities entry {str(c)[:40]!r} is missing {kk} (every stop needs one sourced fact with the date of its figure)")
            if isinstance(c, dict) and str(c.get("fact", "")).rstrip().endswith("."): E.append(f'map: the fact for {c.get("city")} ends with a full stop')
        seen = []
        for k, b in enumerate(beats, 1):
            r = b.get("role"); n = b.get("rung")
            if r == "stop":
                if not (isinstance(n, int) and 1 <= n <= len(stops)): E.append(f'beat {k}: a stop beat needs "rung": 1-{len(stops)} (its place in meta.rungs)'); continue
                if seen and n < seen[-1]: E.append(f"beat {k}: stop {n} comes after stop {seen[-1]}; the trip only goes forward")
                if n not in seen: seen.append(n)
            elif n is not None: E.append(f'beat {k}: only stop beats carry "rung" (the header hides on the title, summary and cta beats)')
            cps = b.get("chips") or []
            if cps and r != "stop": E.append(f"beat {k}: chips belong to stop beats")
            for c in cps:
                lab = str(c.get("label", ""))
                if not 1 <= len(words(lab)) <= 3 or len(lab) > 19: E.append(f'beat {k}: chip "{lab}" must be 1-3 words and 19 characters at most')
                if lab.rstrip().endswith("."): E.append(f'beat {k}: chip "{lab}" ends with a full stop')
                if not (isinstance(c.get("at", 0), int) and 0 <= c.get("at", 0) < len(b.get("chunks") or [])): E.append(f'beat {k}: chip "{lab}" needs "at": the index of the caption chunk that names it')
        if isinstance(stops, list) and seen != list(range(1, len(stops) + 1)): E.append(f"map: every stop in meta.rungs needs at least one stop beat, in order (found {seen})")
        for n in seen:
            nc = sum(len(b.get("chips") or []) for b in beats if b.get("rung") == n)
            if not 1 <= nc <= 3: E.append(f"map: stop {n} has {nc} chips; use 1-3 (the career first)")
            sc = [scenes.get(b.get("img"), {}) for b in beats if b.get("rung") == n]
            if not any(it.get("p") == "landmark" for sp in sc for it in sp.get("items", [])): E.append(f"map: stop {n} shows no landmark (prop \"landmark\")")
        if "summary" in roles and "stop" in roles[roles.index("summary"):]: E.append("map: the summary map comes after the last stop")
        for name, sp in scenes.items():   # Ledger is on every scene; no country borders or labels exist in world_map, so only cities can be named
            if not any(it.get("p") == "ledger" for it in sp.get("items", [])): E.append(f"map: scene {name} has no Ledger (he must be visible on every scene)")
        if not m.get("superlative_source"):   # "best" and "highest paying" need a source that says exactly that (owner's brief, 13 Nov 2026)
            for k, b in enumerate(beats, 1):
                if re.search(r"\b(best|highest[- ]paying|top[- ]paying|richest)\b", b.get("text", ""), re.I): E.append(f'beat {k}: "best" or "highest paying" needs a source that says exactly that (set meta.superlative_source), or say "a hub for"')
    else:
        if seq != sorted(seq): E.append(f"roles out of order; keep {' > '.join(R['order'])}")
        if roles and roles[0] != "hook": E.append("beat 1 must be the hook")
        if roles and roles[-1] != "endcard": E.append('the last beat must be the end card (role "endcard" with "term" and "keypoint")')
        if roles.count("endcard") > 1: E.append("only one end card")
    for name, sp in scenes.items():   # summary pointer (Hoang, 1 Nov 2026): the boxes must leave the small Ledger room on the left
        if sp.get("pointer"):
            if t != "howto": W.append(f"scene {name}: \"pointer\" is meant for how-to summary scenes")
            for it in sp.get("items", []):
                if it.get("p") == "flow_box" and it["x"] - it.get("w", 860) * it.get("s", 1.0) / 2 < 220:
                    E.append(f"scene {name}: with \"pointer\" every flow_box needs its left edge at x 220 or more (use w 700 at x 580) so the pointing Ledger does not cover box text"); break
    for name, sp in scenes.items():
        fr = sp.get("frame")
        if fr is not None and not (isinstance(fr, list) and len(fr) == 4) and fr not in FRAMES and not (isinstance(fr, str) and fr.startswith(("item:", "items:"))):
            E.append(f"scene {name}: frame {fr!r}; omit it (auto-fit, the default) or use auto, ledger, ledger-close, wide, item:<id>, items:<id>,<id> or [x,y,w,h]")
    if t == "life-of" and beats and not any("day in the life" in b.get("text", "").lower() for b in beats[:2]):
        E.append('life-of: beat 1 or 2 must say "a day in the life of ..." (beat 1 may lead with the number and stakes, 3 Nov 2026)')
    # Ledger is never hidden (Hoang, 3 Nov 2026: "the desk cover ledger face"). Items draw in list order,
    # so furniture listed after Ledger is painted over him. Wide multi-panel scenes hold several Ledgers,
    # so only a Ledger in the same panel (within 700 px in x) counts.
    for name, sp in scenes.items():
        its = sp.get("items", [])
        for k, it in enumerate(its):
            if it.get("p") in ("desk", "school_desk", "whiteboard", "lemonade_stand", "people_group", "scale", "pit"):
                if any(l.get("p") == "ledger" and abs(l.get("x", 0) - it.get("x", 0)) < 700 for l in its[:k]):
                    E.append(f'scene {name}: "{it.get("p")}" is listed after Ledger, so it is drawn over him; list it before Ledger (Hoang, 3 Nov 2026)')
    # Story flow (Hoang, 3 Nov 2026: "no transitional words in a story"): story beats link to the one before
    if t in ("life-of", "howto", "definition", "lesson", "ladder", "map") and beats:
        LINK = re.compile(r"^\W*(but|so|then|that means|that is|which means|now|first|next|after|still|because|and|until|meanwhile|here is|here's|this is|by|at the end|finally|later|soon|instead|yet|that's"
                          + (r"|however|for example|for instance|as a result|in other words|this means|this is why|in short|to see why|let's|imagine|in the same way|on the other hand|therefore|in fact|whenever|once|when|if" if t == "lesson" else "") + r")\b", re.I)
        story = [b for b in beats[2:] if b.get("role") not in ("endcard", "summary", "loop", "defcard", "cta", "title")]
        linked = sum(1 for b in story if LINK.search(b.get("text", "")) or re.search(r"[.:]\s*(but|so|then|that means|now)\b", b.get("text", ""), re.I))
        if story and linked / len(story) < 0.6:
            W.append(f"story flow: only {linked} of {len(story)} story beats start with a linking word (But, So, Then, That means, Now...); link each beat to the one before (Hoang, 3 Nov 2026)")
        if not any(re.match(r"^\W*(but|yet|still|instead)\b", b.get("text", ""), re.I) for b in beats if b.get("role") in ("turn", "problem")) and t not in ("definition", "lesson", "ladder", "map"):
            W.append('story flow: the turn has no "But ..." (or Yet/Still/Instead); mark the turning point (Hoang, 3 Nov 2026)')
    # Context transitions (Hoang, 6 Nov 2026: "when ever you start the context explaine, please give the transitional context"):
    # the viewer is told when an example starts, and told when the reel goes back to it
    def _first(*rr):
        return next((b for b in beats if b.get("role") in rr), None)
    def _need(b, rx, what):
        if b is not None and not rx.search(b.get("text", "")): E.append(f'context transition: the {b.get("role")} beat "{b.get("text", "")[:60]}" {what} (Hoang, 6 Nov 2026)')
    OPENS = "must open the example out loud, for example \"Let's imagine ...\" or \"For this, let's use the example of ...\""
    BACK = "must say it continues or moves on, for example \"Continuing the story, ...\", \"Back to our cafe, ...\" or \"Now let's use a business example ...\""
    if t == "definition":
        _need(_first("story"), CTX_OPEN, OPENS); _need(_first("example"), CTX_BACK, BACK)
    elif t == "life-of":
        lead = [b for b in beats if b.get("role") == "hook"] + ([_first("moment")] if _first("moment") else [])
        if not any(CTX_OPEN.search(b.get("text", "")) for b in lead): E.append(f"context transition: a hook beat or the first moment {OPENS}, such as \"Let's follow a day in the life of ...\" (Hoang, 6 Nov 2026)")
        _need(_first("lesson"), CTX_BACK, BACK)
    elif t == "howto":
        _need(_first("problem"), CTX_OPEN, OPENS)
    # Time frame matches the numbers (Hoang, 3 Nov 2026: a monthly example told as clock times in one day)
    vtxt = " ".join(b.get("text", "") for b in beats).lower()
    if re.search(r"\b(\w+ (a|p)\.m\.|noon|midnight|o'clock)", vtxt) and re.search(r"\b(a|per|each|every|this) (month|year|quarter)\b|\bmonthly\b|\byearly\b", vtxt):
        W.append("time frame: clock times in one day but the numbers are per month/year; tell the story on the timescale of the numbers (Hoang, 3 Nov 2026)")
    if m.get("layout") not in (None, "reel", "full", "ladder"): E.append('meta.layout must be "full" (full-frame layout, how-to reels), "ladder" (career-ladder reels) or left out')
    if m.get("layout") == "ladder" and t not in ("ladder", "map"): E.append('meta.layout "ladder" is for meta.type "ladder"')
    if t == "howto" and m.get("layout") != "full": W.append('howto without meta.layout "full": the old layout leaves the bottom half empty (Hoang, 1 Nov 2026)')
    if t == "howto":   # how-to card fields (edlintics-howto-reel step F)
        for k in ("concept_id", "themes", "industry", "role"):
            if not m.get(k): W.append(f"meta.{k} is missing (needed for the hub card and the concepts registry)")
    # hook test (Hoang, 1 Nov 2026): hookStyle "A" opens on the question; "B" opens on the problem (1-2 hook beats with the
    # number) and asks the question second, so the question may sit in any of the first 3 beats, all with role "hook"
    _hq = lambda b: re.match(r"^how (does|do)\b.*\bdeal with\b", b.get("text", ""), re.I)
    if t == "howto" and m.get("hookStyle") not in (None, "A", "B"): E.append('meta.hookStyle must be "A" (question first) or "B" (problem first)')
    if t == "howto" and beats and m.get("hookStyle") == "B":
        lead = []
        for b in beats[:3]:
            if b.get("role") != "hook": break
            lead.append(b)
        if not any(_hq(b) for b in lead[1:]): E.append('hookStyle "B": open on the problem in a hook beat, then ask "How does <a role> ... deal with <a problem>?" in hook beat 2 or 3')
    elif t == "howto" and beats and not _hq(beats[0]):
        E.append('howto hook must ask "How does <a role> ... deal with <a problem>?"')
    if t == "howto":   # recap (Hoang, 2 Nov 2026): the diagram is voiced "Let's revise the process (or the concept). Step 1, ... Step 2, ..."
        rec = [b for b in beats if b.get("role") == "summary" and any(it.get("p") == "flow_box" for it in scenes.get(b.get("img"), {}).get("items", []))]
        if rec and not rec[0].get("text", "").lower().startswith(("let's revise the process", "let's revise the concept")):
            E.append('howto summary: the first diagram beat must start "Let\'s revise the process." or "Let\'s revise the concept." (Hoang, 2 Nov 2026)')
        for n, b in enumerate(rec, 1):
            if f"step {n}," not in b.get("text", "").lower():
                E.append(f'howto summary beat {n}: say "Step {n}, <short step>." (caption "Step {n}" as its own chunk; "say" spells the number)')
    total = 0; texts_extra = []
    for k, b in enumerate(beats, 1):
        where = f"beat {k}"
        if "focus" in b or "focus_end" in b: E.append(f"{where}: no camera moves; remove focus/focus_end and set the scene's \"frame\" instead")
        tx = b.get("text", ""); total += len(words(tx))
        if "gap" in b and not 0 <= float(b["gap"]) <= 1.5: E.append(f"{where}: gap {b['gap']} s; use 0-1.5")
        if not tx: E.append(f"{where}: empty voice text")
        if t == "lesson" and tx and b.get("role") != "defcard":   # full sentences (Hoang, 5 Nov 2026): no fragments or keyword lists
            if len(words(tx)) < 5 or not re.search(r"[.?]['\"”’)]?$", tx.strip()): E.append(f"{where}: lesson voice must be full sentences ending in . or ?: {tx[:60]!r}")
        if b.get("role") == "defcard":   # definition card (lessons, 5 Nov 2026): the term large, the definition with the highlighter, an optional equation; no logo
            if t != "lesson": E.append(f'{where}: role "defcard" is for meta.type "lesson"')
            term, df = b.get("term", ""), b.get("definition", "")
            if not term: E.append(f'{where}: defcard needs "term"')
            if not df: E.append(f'{where}: defcard needs "definition" (one full sentence)')
            if df and not 6 <= len(words(df)) <= 30: E.append(f"{where}: definition has {len(words(df))} words (6-30, one full sentence)")
            if df.rstrip().endswith("."): E.append(f"{where}: definition ends with a full stop")
            for kk in ("keypoint", "cta", "footnote", "img"):
                if b.get(kk): E.append(f'{where}: a defcard has no "{kk}" (term, definition and an optional equation only)')
            _p = lambda z: " ".join(re.sub(r"[^a-z0-9$%]+", " ", z.lower()).split())
            if term and _p(term) not in _p(tx): E.append(f"{where}: the voice must read the term")
            if df and _p(df) not in _p(tx): E.append(f"{where}: the voice must read the definition as it is on the card")
            q = b.get("equation")
            if q is not None:
                if not isinstance(q, dict) or not q.get("lhs") or not q.get("num"): E.append(f'{where}: "equation" must be {{"lhs", "num", "den" (optional)}}')
                else:
                    for kk in ("lhs", "num", "den", "example"):
                        v = str(q.get(kk, ""))
                        if v.rstrip().endswith("."): E.append(f"{where}: equation {kk} ends with a full stop")
                        if len(v) > 34: E.append(f"{where}: equation {kk} {v[:30]!r}... is over 34 characters; shorten it to fit the card")
                    texts_extra.append(("defcard equation", " ".join(str(q.get(kk, "")) for kk in ("lhs", "num", "den", "example"))))
            if len(words(tx)) / WPS_T > 14: W.append(f"{where}: defcard voice is about {len(words(tx)) / WPS_T:.1f} s; keep the definition to one sentence")
            texts_extra.append(("defcard", term + " " + df))
            continue
        if b.get("role") == "endcard":
            term, kp = b.get("term", ""), b.get("keypoint", "")
            if not term: E.append(f"{where}: end card needs \"term\"")
            if not kp: E.append(f"{where}: end card needs \"keypoint\" (one line to remember)")
            if term and m.get("term") and term.lower().rstrip("s") != str(m["term"]).lower().rstrip("s"): E.append(f'{where}: end card term "{term}" differs from meta.term "{m.get("term")}"')
            if kp and not 4 <= len(words(kp)) <= 24: E.append(f"{where}: key point has {len(words(kp))} words (4-24; a glossary-length sentence is allowed from 4 Nov 2026)")
            if kp.rstrip().endswith("."): E.append(f"{where}: key point ends with a full stop")
            _n = lambda z: re.sub(r"[/\-]", " ", z.lower())  # "A-B testing" says "A/B testing" (Kokoro reads "/" as "slash")
            cta = b.get("cta", "")
            if cta and t != "ad": E.append(f"{where}: \"cta\" on the end card is for ads only")
            if cta and (len(cta) > 32 or cta.rstrip().endswith(".")): E.append(f"{where}: cta pill text {cta!r}: 32 characters at most, no closing full stop")
            if cta: texts_extra.append(("endcard cta", cta))
            if term and _n(term) not in _n(tx) and not (cta and _n(cta.replace(".com", " dot com")) in _n(tx)):
                E.append(f"{where}: the voice must say the term on the end card (or, for an ad with a cta pill, the cta line)")
            q = b.get("equation")   # how-to end card (1 Nov 2026): the term's equation with the story's numbers
            if q is not None:
                if not isinstance(q, dict) or not q.get("lhs") or not q.get("num"): E.append(f'{where}: "equation" must be {{"lhs", "num", "den" (optional), "example" (optional)}}')
                else:
                    for kk in ("lhs", "num", "den", "example"):
                        v = str(q.get(kk, ""))
                        if v.rstrip().endswith("."): E.append(f"{where}: equation {kk} ends with a full stop")
                        if len(v) > 34: E.append(f"{where}: equation {kk} {v[:30]!r}... is over 34 characters; shorten it to fit the card")
                    texts_extra.append(("endcard equation", " ".join(str(q.get(kk, "")) for kk in ("lhs", "num", "den", "example"))))
            if t == "howto" and isinstance(q, dict) and (str(q.get("example", "")).strip() or any("=" in str(q.get(kk, "")) for kk in ("lhs", "num", "den"))):
                E.append(f'{where}: howto end card shows only the term, the definition and the equation; remove the worked example or numbers line ("example"); the numbers stay in the equation scene (Hoang, 1 Nov 2026)')
            if t == "howto" and q is None and not str(m.get("equation", "")).lower().startswith("none"): W.append(f"{where}: no \"equation\" on the end card; add one when the definition has a formula (Hoang, 1 Nov 2026)")
            fn = b.get("footnote", "")
            for ln in [z for z in fn.split("\n") if z.strip()]:   # small print under the logo, 1-2 lines
                if len(ln) > 90 or ln.rstrip().endswith("."): E.append(f"{where}: footnote line {ln[:40]!r}: 90 characters at most, no closing full stop")
            if fn: texts_extra.append(("footnote", fn))
            sec = len(words(tx)) / WPS_T
            if not (1.4 if t == "ad" else 2.2) <= sec <= (4.6 if t == "ledger-talks" else 5.6 if t == "howto" else 8.0 if t in ("definition", "life-of", "ladder") else 4.2): E.append(f"{where}: end card voice is about {sec:.1f} s; keep it 2.5-3.5 s (term + key point)")
            texts_extra.append(("endcard", term + " " + kp))
            continue
        if b.get("img") not in scenes: E.append(f"{where}: img {b.get('img')!r} is not a scene")
        ch = b.get("chunks") or []
        if not ch: E.append(f"{where}: no caption chunks")
        if not any(str(c.get("key") or "").strip() for c in ch) and b.get("role") != "loop": W.append(f"{where}: no key word highlighted (give one chunk a \"key\")")
        for c in ch:
            if "key" in c and not str(c.get("key") or "").strip(): W.append(f'{where}: chunk "{c.get("text", "")}" has an empty key; remove "key" or fill it')
        for c in ch:
            ct = c.get("text", ""); n = len(words(ct))
            lo, hi = P["chunk"]
            if not lo <= n <= hi: E.append(f'{where}: caption chunk "{ct}" has {n} words ({lo}-{hi})')
            if ct.rstrip().endswith("."): E.append(f'{where}: caption chunk "{ct}" ends with a full stop')
            if c.get("key") and c["key"] not in ct: E.append(f'{where}: key "{c["key"]}" is not inside chunk "{ct}"')
        dur = len(words(tx)) / WPS_T
        if dur > (7.5 if t == "ad" else 6.5 if t in ("howto", "ladder", "map") else 12 if t == "lesson" else 4.6): W.append(f"{where}: about {dur:.1f} s of voice; split it into two beats (2-4 s each)")
    for k, b in enumerate(beats, 1):   # takeaways and lessons avoid absolute claims (definition review, 1 Nov 2026)
        if t == "howto" and b.get("role") == "takeaway" and re.search(r"\b(never|always|only|every|all|no one|nobody|guarantees?)\b", b.get("text", ""), re.I):
            W.append(f"beat {k}: absolute word in the takeaway {b.get('text', '')[:60]!r}; prefer rarely, usually, often, can")
    est = total / WPS_T
    target = P["target"]
    if total < target[0]: W.append(f"voice has {total} words; the {t} target is {target[0]}-{target[1]} (add a beat or a few words)")
    if total > target[1]: W.append(f"voice has {total} words; the {t} target is {target[0]}-{target[1]}")
    if not P["allowed"][0] <= total <= P["allowed"][1]: E.append(f"voice has {total} words; aim for {target[0]}-{target[1]} ({P['allowed'][0]}-{P['allowed'][1]} allowed)")
    if not P["secs"][0] <= est <= P["secs"][1]: E.append(f"estimated length {est:.1f} s; must be {P['secs'][0] + 1}-{P['secs'][1] - 1} s")
    # house rules on every piece of text
    texts = [("voice", b.get("text", "")) for b in beats] + [("caption", c.get("text", "")) for b in beats for c in b.get("chunks", [])]
    texts += [(f"meta.{k}", str(m.get(k, ""))) for k in ("caption", "caption_x", "first_comment", "title")] + texts_extra
    texts += texts_extra_cta + [("chip", str(c.get("label", ""))) for b in beats for c in (b.get("chips") or [])] + [("rung title", str(r)) for r in (m.get("rungs") or [])]
    for where, s in texts:
        if "!" in s: E.append(f"{where}: exclamation point in {s[:60]!r}")
        if EMOJI.search(s):
            # emojis are allowed only as the closing characters of the first comment
            body = re.sub("[\\s" + EMOJI.pattern[1:-1] + "]+$", "", s)
            if where != "meta.first_comment" or EMOJI.search(body):
                E.append(f"{where}: emoji in {s[:60]!r} (emojis are allowed only at the end of first_comment)")
        if TUTOR.search(s) and t != "ad": E.append(f"{where}: mentions tutoring: {s[:60]!r}")
        if t == "lesson" and PROMO.search(s): E.append(f"{where}: nothing promotional in a lesson (no follow, subscribe, brand or tease lines): {s[:60]!r}")
    # currencies are mixed across posts (Hoang, 7 Nov 2026); inside one post, more than one is usually a slip
    signs = {c for _, s in texts for c in CURRENCY_SIGN.findall(s)}
    if len(signs) > 1: W.append(f"more than one currency in this post ({' '.join(sorted(signs))}); fine only if the concept is about exchange rates")
    for k in ("caption", "caption_x", "first_comment"):
        for para in [p for p in str(m.get(k, "")).split("\n") if p.strip()]:
            if para.rstrip().endswith("."): E.append(f'meta.{k}: paragraph ends with a full stop: "...{para.rstrip()[-40:]}"')
    if "edlintics.com" in str(m.get("first_comment", "")) + str(m.get("caption", "")) and "utm_" not in str(m.get("first_comment", "")) + str(m.get("caption", "")) and not m.get("utm"):
        W.append("an edlintics.com link without UTM tags; add utm_* (see performance-review.md)")
    for w in W: print("WARN ", w)
    for e in E: print("FAIL ", e)
    print(f"{'OK' if not E else 'NOT OK'}: {len(beats)} beats, {total} words, about {est:.1f} s")
    sys.exit(1 if E else 0)


if __name__ == "__main__":
    main(sys.argv[1])
