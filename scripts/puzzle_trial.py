#!/usr/bin/env python3
"""Two-slide puzzle trial: manifest, checks and a dry-run plan.

Scope (trial only): P21-02-v1 and P21-03-v1 as editable Canva carousels.
Stdlib only. Nothing here talks to Canva, Google Sheets or any social platform.
Canva writes are carried out through the Canva connector in an agent session;
this script decides WHAT may happen next, records what DID happen, and refuses
unsafe transitions (duplicates, stale approvals, retries after uncertain writes).

Commands
  plan    [--id ID]           Dry run (default). Print the next permitted actions.
  check   [--id ID]           Maths, assumptions, answer leakage, approval freshness.
  hash    --id ID             Print the current content hash.
  record  --id ID --event E   Append an event; may change state (see EVENTS).
  approve --id ID --kind K --by NAME   Record content|design|publish approval
                              against the CURRENT content hash.
  svg     [--id ID]           Render editable SVG sources from layout JSON.

Exit codes: 0 ok, 1 check failed / transition refused, 2 usage error.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "calendar" / "puzzle-trial.json"
APPROVAL_KINDS = ("content", "design", "publish")

# Events and the canva.state they move to. "uncertain" blocks any further write
# until an "inspected" event records what the destination actually contains.
EVENTS = {
    "design_created": "copied",
    "edits_applied": "edits_open",
    "edits_committed": "saved",
    "export_ok": None,
    "export_failed": None,
    "write_uncertain": "uncertain",
    "inspected": None,
}


def now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def load(path: Path = MANIFEST) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(data: dict, path: Path = MANIFEST) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def find(data: dict, cid: str) -> dict:
    hits = [c for c in data["candidates"] if c["candidate_id"] == cid]
    if len(hits) != 1:
        raise SystemExit(f"error: expected exactly one candidate {cid!r}, found {len(hits)}")
    return hits[0]


# ---------------------------------------------------------------- content hash
def content_hash(c: dict) -> str:
    """Hash of everything a reviewer approves: wording, assumptions, visual spec."""
    payload = {
        "slides": c["slides"],
        "visual_spec_version": c["visual_spec_version"],
    }
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()
    return "sha256:" + hashlib.sha256(blob).hexdigest()[:16]


def approval_status(c: dict) -> dict:
    current = content_hash(c)
    out = {}
    for kind in APPROVAL_KINDS:
        a = c["approvals"].get(kind)
        if not a:
            out[kind] = "missing"
        elif a.get("content_hash") != current:
            out[kind] = "STALE"
        else:
            out[kind] = "valid"
    return out


# ---------------------------------------------------------------------- checks
def _slide_text(slide: dict) -> str:
    parts = [slide.get("kicker", ""), slide.get("prompt", ""), slide.get("headline", "")]
    parts += slide.get("visual_text", []) + slide.get("assumptions", [])
    parts += [slide.get("takeaway", ""), slide.get("explanation", "")]
    return "\n".join(p for p in parts if p).lower()


def check_maths(c: dict) -> list[str]:
    errs = []
    m = c["maths"]
    if m["kind"] == "two_machine_flow_shop":
        jobs = m["jobs"]  # {name: [stage1, stage2]}

        def makespan(order):
            t1 = t2 = 0
            for j in order:
                p1, p2 = jobs[j]
                t1 += p1
                t2 = max(t2, t1) + p2
            return t2

        names = list(jobs)
        got = {"".join(o): makespan(o) for o in (names, names[::-1])}
        if got != m["expected_makespans"]:
            errs.append(f"makespan mismatch: computed {got}, expected {m['expected_makespans']}")
        best = min(got, key=got.get)
        if best[0] != m["expected_first"]:
            errs.append(f"best first job computed {best[0]}, expected {m['expected_first']}")
    elif m["kind"] == "comparative_advantage":
        oc = {}
        for person, cap in m["capacity"].items():
            oc[person] = Fraction(cap["videos"], cap["logos"])  # videos per logo
        for person, exp in m["expected_oc_videos_per_logo"].items():
            if oc[person] != Fraction(exp):
                errs.append(f"{person} opportunity cost {oc[person]} != {exp}")
        winner = min(oc, key=oc.get)
        if winner != m["expected_answer"]:
            errs.append(f"lower opportunity cost is {winner}, expected {m['expected_answer']}")
        absolute = all(
            m["capacity"][m["faster_at_both"]][k] > v[k]
            for p, v in m["capacity"].items() if p != m["faster_at_both"]
            for k in ("logos", "videos")
        )
        if not absolute:
            errs.append("'faster at both' claim is false for the stated capacities")
    else:
        errs.append(f"unknown maths kind {m['kind']}")
    return errs


def check_candidate(c: dict) -> list[str]:
    errs = []
    q, a = c["slides"]["question"], c["slides"]["answer"]
    qtext = _slide_text(q)
    # 1. every required assumption must be visible on slide 1
    for req in c["required_assumptions"]:
        if req.lower() not in qtext:
            errs.append(f"missing assumption on slide 1: {req!r}")
    # 2. no answer tokens on slide 1
    for tok in c["answer_tokens"]:
        if tok.lower() in qtext:
            errs.append(f"answer leak on slide 1: {tok!r}")
    # 3. slide 2 must state the answer and one takeaway
    atext = _slide_text(a)
    if c["answer_tokens"][0].lower() not in atext:
        errs.append("slide 2 does not state the answer")
    if not a.get("takeaway"):
        errs.append("slide 2 has no takeaway")
    # 4. exactly two slides
    if set(c["slides"]) != {"question", "answer"}:
        errs.append(f"expected exactly two slides, found {sorted(c['slides'])}")
    errs += check_maths(c)
    return errs


# ------------------------------------------------------------------------ plan
def plan_for(c: dict) -> list[str]:
    cid, canva = c["candidate_id"], c["canva"]
    st = canva.get("state")
    steps = []
    if st == "uncertain":
        return [f"[{cid}] BLOCKED: last write outcome uncertain. Inspect design "
                f"{canva.get('design_id') or '(search by title ' + cid + ')'} and record 'inspected' "
                "before any retry. Do not assume nothing happened."]
    errs = check_candidate(c)
    if errs:
        return [f"[{cid}] BLOCKED by checks: " + "; ".join(errs)]
    if not canva.get("design_id"):
        steps.append(f"[{cid}] search Canva for an existing design titled '{cid}*' (duplicate guard)")
        steps.append(f"[{cid}] copy {canva['source_design']} -> new design, title '{cid} — draft'")
    elif st in ("copied", "edits_open"):
        steps.append(f"[{cid}] design {canva['design_id']} exists: reuse it, never copy again")
        steps.append(f"[{cid}] show previews; WAIT for design approval before commit")
    appr = approval_status(c)
    if st == "edits_open" and appr["design"] == "valid":
        steps.append(f"[{cid}] commit transaction {canva.get('transaction_id')} (design approved)")
    if st == "saved":
        if not c["exports"] or c["exports"][-1]["status"] != "ok":
            steps.append(f"[{cid}] export PNG pages 1-2 from {canva['design_id']}")
    for kind, s in appr.items():
        if s != "valid":
            steps.append(f"[{cid}] {kind} approval {s}")
    steps.append(f"[{cid}] publishing/scheduling: DISABLED in this trial")
    return steps


# ------------------------------------------------------------------------- svg
def render_svg(layout: dict) -> str:
    w, h = layout["width"], layout["height"]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
           f'<rect width="{w}" height="{h}" fill="{layout.get("background", "#ffffff")}"/>']
    fonts = layout["fonts"]
    for el in layout["elements"]:
        t = el["type"]
        if t == "rect":
            out.append(f'<rect id="{el["id"]}" x="{el["x"]}" y="{el["y"]}" width="{el["w"]}" height="{el["h"]}" '
                       f'rx="{el.get("r", 0)}" fill="{el["fill"]}" stroke="{el.get("stroke", "none")}" '
                       f'stroke-width="{el.get("sw", 0)}"/>')
        elif t == "circle":
            r = el["d"] / 2
            out.append(f'<circle id="{el["id"]}" cx="{el["x"] + r}" cy="{el["y"] + r}" r="{r}" fill="{el["fill"]}"/>')
        elif t == "play":
            x, y, ww, hh = el["x"], el["y"], el["w"], el["h"]
            out.append(f'<path id="{el["id"]}" d="M{x} {y}L{x + ww} {y + hh / 2}L{x} {y + hh}Z" fill="{el["fill"]}"/>')
        elif t == "logo":
            out.append(f'<image id="{el["id"]}" x="{el["x"]}" y="{el["y"]}" width="{el["w"]}" height="{el["h"]}" '
                       f'href="{el["href"]}"/>')
        elif t == "text":
            fam = fonts[el.get("font", "label")]
            anchor = {"start": "start", "center": "middle", "end": "end"}[el.get("align", "start")]
            x = {"start": el["x"], "center": el["x"] + el["w"] / 2, "end": el["x"] + el["w"]}[el.get("align", "start")]
            lh = el["size"] * el.get("lh", 1.3)
            weight = "700" if el.get("bold") else "400"
            style = "italic" if el.get("italic") else "normal"
            lines = el["lines"]
            tspans = "".join(
                f'<tspan x="{x}" dy="{0 if i == 0 else lh}">{_esc(line)}</tspan>' for i, line in enumerate(lines))
            out.append(f'<text id="{el["id"]}" x="{x}" y="{el["y"] + el["size"]}" font-family="{fam}" '
                       f'font-size="{el["size"]}" font-weight="{weight}" font-style="{style}" '
                       f'fill="{el["fill"]}" text-anchor="{anchor}">{tspans}</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ------------------------------------------------------------------------- cli
def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("command", nargs="?", default="plan",
                   choices=["plan", "check", "hash", "record", "approve", "svg"])
    p.add_argument("--id")
    p.add_argument("--event", choices=sorted(EVENTS))
    p.add_argument("--kind", choices=APPROVAL_KINDS)
    p.add_argument("--by")
    p.add_argument("--note", default="")
    p.add_argument("--design-id")
    p.add_argument("--manifest", type=Path, default=MANIFEST)
    a = p.parse_args(argv)

    data = load(a.manifest)
    cands = [find(data, a.id)] if a.id else data["candidates"]

    if a.command == "plan":
        print("DRY RUN: no external writes. Planned actions:")
        for c in cands:
            for s in plan_for(c):
                print("  " + s)
        return 0

    if a.command == "check":
        bad = 0
        for c in cands:
            errs = check_candidate(c)
            appr = approval_status(c)
            print(f"{c['candidate_id']}: {'OK' if not errs else 'FAIL'}  hash={content_hash(c)}  approvals={appr}")
            for e in errs:
                print("   - " + e)
            bad += bool(errs)
        return 1 if bad else 0

    if a.command == "hash":
        print(content_hash(cands[0]))
        return 0

    if a.command == "approve":
        if not (a.id and a.kind and a.by):
            p.error("approve needs --id, --kind and --by")
        c = cands[0]
        if a.kind == "publish":
            print("refused: publishing is disabled in this trial", file=sys.stderr)
            return 1
        errs = check_candidate(c)
        if errs:
            print("refused: checks fail: " + "; ".join(errs), file=sys.stderr)
            return 1
        c["approvals"][a.kind] = {"by": a.by, "at": now(), "content_hash": content_hash(c), "note": a.note}
        c["log"].append({"at": now(), "event": f"approved_{a.kind}", "by": a.by, "hash": content_hash(c)})
        save(data, a.manifest)
        print(f"recorded {a.kind} approval for {c['candidate_id']} at {content_hash(c)}")
        return 0

    if a.command == "record":
        if not (a.id and a.event):
            p.error("record needs --id and --event")
        c = cands[0]
        canva = c["canva"]
        if a.event == "design_created":
            if canva.get("design_id") and canva["design_id"] != a.design_id:
                print(f"refused: {c['candidate_id']} already has design {canva['design_id']} (duplicate)",
                      file=sys.stderr)
                return 1
            canva["design_id"] = a.design_id
        if canva.get("state") == "uncertain" and a.event not in ("inspected",):
            print("refused: last write uncertain; record 'inspected' first", file=sys.stderr)
            return 1
        if a.event in ("export_ok", "export_failed"):
            c["exports"].append({"at": now(), "status": "ok" if a.event == "export_ok" else "failed",
                                 "note": a.note, "content_hash": content_hash(c)})
        if a.event == "inspected":
            if not a.note.startswith(("state=",)):
                p.error("inspected needs --note 'state=<copied|edits_open|saved>; what was found'")
            canva["state"] = a.note.split(";")[0].split("=", 1)[1].strip()
        elif EVENTS[a.event]:
            canva["state"] = EVENTS[a.event]
        c["log"].append({"at": now(), "event": a.event, "note": a.note})
        save(data, a.manifest)
        print(f"{c['candidate_id']}: {a.event} -> state={canva.get('state')}")
        return 0

    if a.command == "svg":
        for c in cands:
            for slide, src in c["svg_sources"].items():
                layout = json.loads((ROOT / src["layout"]).read_text(encoding="utf-8"))
                dest = ROOT / src["svg"]
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(render_svg(layout), encoding="utf-8")
                print(f"wrote {dest.relative_to(ROOT)}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
