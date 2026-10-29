"""Check a reel script.json before building (rules of 25 Oct 2026: no camera moves, end card last). Exit code 1 and a list of problems if anything fails.

Usage: python validate.py <workdir>/script.json
Checks the house rules (voice, captions, currency, no tutoring, no trailing full stop), the beat structure for
meta.type "definition" or "life-of", the scene presets, and an estimated length of 30-40 s.
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
    # paid ad (29 Oct 2026): a hook, 2-3 selling points, one call to action, the end card
    "ad": {"order": ["hook", "point", "cta", "endcard"],
           "min": {"hook": 1, "point": 2, "cta": 1, "endcard": 1}, "max": {"hook": 4, "point": 3, "cta": 1}},
}
# per type: caption chunk words, beats, word target, allowed words, length (s), spoken words per second
SPEC = {"definition": dict(chunk=(2, 5), beats=(9, 13), target=(100, 115), allowed=(85, 125), secs=(29, 41), wps=2.95),
        "life-of": dict(chunk=(2, 5), beats=(9, 13), target=(95, 115), allowed=(85, 125), secs=(29, 41), wps=2.95),
        "ledger-talks": dict(chunk=(1, 3), beats=(8, 14), target=(80, 105), allowed=(65, 115), secs=(24, 37), wps=3.05),
        # ad: 1-4 short hook questions (a problem montage), 2-3 points, a CTA; the ad voice (ElevenLabs v3 dfeOmy6Uay63tNhyO99j
        # at ELEVEN_TEMPO 1.15) speaks about 2.3 words a second (measured 29 Oct 2026); points may run 5-7 s (one line, one scene)
        "ad": dict(chunk=(2, 5), beats=(5, 10), target=(55, 75), allowed=(45, 85), secs=(21, 33), wps=2.3)}   # reviewer 29 Oct 2026: about 32 s at most
FRAMES = ("auto", "content", "ledger", "ledger-close", "wide")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF\U00002300-\U000023FF\U00002B00-\U00002BFF️]")  # + ⏳⌛⏰ and ⭐
TUTOR = re.compile(r"\btutor(s|ing|ed)?\b|\b1[:-]1\b|\bprivate lesson|\bbook a (session|call|class)", re.I)
NOT_USD = re.compile(r"[€£¥₫]|\b(euros?|eur|pounds? sterling|gbp|dong|vnd)\b", re.I)
REQ_META = ["type", "term", "title", "slug", "caption", "caption_x", "first_comment", "threadsTopic", "threadsReason", "maths_check"]
REQ_META_AD = ["type", "term", "title", "slug"]  # an ad's text lives in Ads Manager, not in caption/first comment


def words(s):
    return [w for w in re.split(r"\s+", s.strip()) if re.search(r"[A-Za-z0-9$]", w)]


def main(path):
    S = json.load(open(path)); E, W = [], []
    m = S.get("meta", {}); t = m.get("type")
    for k in (REQ_META_AD if t == "ad" else REQ_META):
        if not m.get(k): E.append(f"meta.{k} is missing")
    if t not in ROLES:
        E.append('meta.type must be "definition", "life-of", "ledger-talks" or "ad"'); t = "definition"
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
    if seq != sorted(seq): E.append(f"roles out of order; keep {' > '.join(R['order'])}")
    if roles and roles[0] != "hook": E.append("beat 1 must be the hook")
    if roles and roles[-1] != "endcard": E.append('the last beat must be the end card (role "endcard" with "term" and "keypoint")')
    if roles.count("endcard") > 1: E.append("only one end card")
    for name, sp in scenes.items():
        fr = sp.get("frame")
        if fr is not None and not (isinstance(fr, list) and len(fr) == 4) and fr not in FRAMES and not (isinstance(fr, str) and fr.startswith(("item:", "items:"))):
            E.append(f"scene {name}: frame {fr!r}; omit it (auto-fit, the default) or use auto, ledger, ledger-close, wide, item:<id>, items:<id>,<id> or [x,y,w,h]")
    if t == "life-of" and beats and "day in the life" not in beats[0].get("text", "").lower():
        E.append('life-of hook must say "a day in the life of ..."')
    total = 0; texts_extra = []
    for k, b in enumerate(beats, 1):
        where = f"beat {k}"
        if "focus" in b or "focus_end" in b: E.append(f"{where}: no camera moves; remove focus/focus_end and set the scene's \"frame\" instead")
        tx = b.get("text", ""); total += len(words(tx))
        if "gap" in b and not 0 <= float(b["gap"]) <= 1.5: E.append(f"{where}: gap {b['gap']} s; use 0-1.5")
        if not tx: E.append(f"{where}: empty voice text")
        if b.get("role") == "endcard":
            term, kp = b.get("term", ""), b.get("keypoint", "")
            if not term: E.append(f"{where}: end card needs \"term\"")
            if not kp: E.append(f"{where}: end card needs \"keypoint\" (one line to remember)")
            if term and m.get("term") and term.lower().rstrip("s") != str(m["term"]).lower().rstrip("s"): E.append(f'{where}: end card term "{term}" differs from meta.term "{m.get("term")}"')
            if kp and not 4 <= len(words(kp)) <= 12: E.append(f"{where}: key point has {len(words(kp))} words (4-12)")
            if kp.rstrip().endswith("."): E.append(f"{where}: key point ends with a full stop")
            _n = lambda z: re.sub(r"[/\-]", " ", z.lower())  # "A-B testing" says "A/B testing" (Kokoro reads "/" as "slash")
            cta = b.get("cta", "")
            if cta and t != "ad": E.append(f"{where}: \"cta\" on the end card is for ads only")
            if cta and (len(cta) > 32 or cta.rstrip().endswith(".")): E.append(f"{where}: cta pill text {cta!r}: 32 characters at most, no closing full stop")
            if cta: texts_extra.append(("endcard cta", cta))
            if term and _n(term) not in _n(tx) and not (cta and _n(cta.replace(".com", " dot com")) in _n(tx)):
                E.append(f"{where}: the voice must say the term on the end card (or, for an ad with a cta pill, the cta line)")
            fn = b.get("footnote", "")
            for ln in [z for z in fn.split("\n") if z.strip()]:   # small print under the logo, 1-2 lines
                if len(ln) > 90 or ln.rstrip().endswith("."): E.append(f"{where}: footnote line {ln[:40]!r}: 90 characters at most, no closing full stop")
            if fn: texts_extra.append(("footnote", fn))
            sec = len(words(tx)) / WPS_T
            if not (1.4 if t == "ad" else 2.2) <= sec <= (4.6 if t == "ledger-talks" else 4.2): E.append(f"{where}: end card voice is about {sec:.1f} s; keep it 2.5-3.5 s (term + key point)")
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
        if dur > (7.5 if t == "ad" else 4.6): W.append(f"{where}: about {dur:.1f} s of voice; split it into two beats (2-4 s each)")
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
        if NOT_USD.search(s): E.append(f"{where}: non-US currency: {s[:60]!r}; use US dollars")
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
