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
        "lesson": dict(chunk=(2, 5), beats=(6, 120), target=(354, 531), allowed=(177, 708), secs=(59, 241), wps=2.95)}   # 4 Nov 2026 (Hoang ok): full-sentence voice at tempo 1.0, about 38 s, 42 s with the price line   # Hoang 29 Oct 2026: 32 s target, 35 s acceptable for the emotional cut
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
        E.append('meta.type must be "definition", "life-of", "ledger-talks", "howto", "ad" or "lesson"'); t = "definition"
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
    bad = [r for r in roles if r not in R["order"]]
    if bad: E.append(f"unknown roles {sorted(set(map(str, bad)))}; {t} roles are {R['order']}")
    seq = [R["order"].index(r) for r in roles if r in R["order"]]
    if t == "lesson":   # any order; the hook, when there is one, opens the video as a direct question
        if "hook" in roles[1:]: E.append("lesson: the hook (optional) can only be beat 1")
        if roles and roles[0] == "hook" and "?" not in beats[0].get("text", ""): E.append("lesson: the hook must ask the learner a direct question (end it with ?)")
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
    if t in ("life-of", "howto", "definition", "lesson") and beats:
        LINK = re.compile(r"^\W*(but|so|then|that means|that is|which means|now|first|next|after|still|because|and|until|meanwhile|here is|here's|this is|by|at the end|finally|later|soon|instead|yet|that's"
                          + (r"|however|for example|for instance|as a result|in other words|this means|this is why|in short|to see why|let's|imagine|in the same way|on the other hand|therefore|in fact|whenever|once|when|if" if t == "lesson" else "") + r")\b", re.I)
        story = [b for b in beats[2:] if b.get("role") not in ("endcard", "summary", "loop", "defcard")]
        linked = sum(1 for b in story if LINK.search(b.get("text", "")) or re.search(r"[.:]\s*(but|so|then|that means|now)\b", b.get("text", ""), re.I))
        if story and linked / len(story) < 0.6:
            W.append(f"story flow: only {linked} of {len(story)} story beats start with a linking word (But, So, Then, That means, Now...); link each beat to the one before (Hoang, 3 Nov 2026)")
        if not any(re.match(r"^\W*(but|yet|still|instead)\b", b.get("text", ""), re.I) for b in beats if b.get("role") in ("turn", "problem")) and t not in ("definition", "lesson"):
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
    if m.get("layout") not in (None, "reel", "full"): E.append('meta.layout must be "full" (full-frame layout, how-to reels) or left out')
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
            if not (1.4 if t == "ad" else 2.2) <= sec <= (4.6 if t == "ledger-talks" else 5.6 if t == "howto" else 8.0 if t in ("definition", "life-of") else 4.2): E.append(f"{where}: end card voice is about {sec:.1f} s; keep it 2.5-3.5 s (term + key point)")
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
        if dur > (7.5 if t == "ad" else 6.5 if t == "howto" else 12 if t == "lesson" else 4.6): W.append(f"{where}: about {dur:.1f} s of voice; split it into two beats (2-4 s each)")
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
