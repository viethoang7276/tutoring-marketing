# Weekly CMO reports

The standing deliverable of each CMO cycle (`docs/cmo-cycle.md`): one report per week, for Hoang.
It is the cover sheet over the cycle's work — what the plan is, how last week went, what happens
next, and what product features the data is asking for.

## The four sections (always, in this order)

1. **Current plan** — the standing strategy: direction, pillars, where we are in the season, and
   what is locked vs still proposed.
2. **Performance — past week** — what actually moved. Post-launch this pulls from `npm run brief`
   (funnel, platform stats, demand-gaps, feedback). Pre-launch there are no channel metrics, so it
   tracks research + build-pipeline progress instead, and says so plainly.
3. **Next week — implementation plan** — the concrete actions, with any **tweak** to the plan driven
   by what last week's data showed. If nothing changed, say nothing changed and why.
4. **Feature proposals** — new or updated `REQ-####` from `docs/feature-requests/` this week, with
   status, awaiting Hoang's approve / defer / reject.

Plus a short **Decisions needed from you** footer — the human-gate items.

## Format and cadence

- One markdown file per week: `YYYY-W##-cmo-weekly.md` (ISO week). Markdown is the working copy.
- Want a polished Word version to forward or print? Say so and the report is rendered to `.docx`
  (same approach as `scripts/build_proposal_docx.py`).
- Produced each time the cycle runs (intended weekly). On-demand for now — say "run a CMO cycle".

## Honesty rules

- Pre-launch, do not invent engagement numbers. If there is no data, the performance section reports
  progress and research, not metrics.
- Every claimed result names its source (`npm run brief` fixtures vs live, a research report, a live
  scan). Never present a fixture figure as a real result.
- The report proposes; it never marks anything locked. Hoang locks.

## Index

| Week | Report | Headline |
|---|---|---|
| 2026-W23 | [2026-W23-cmo-weekly.md](2026-W23-cmo-weekly.md) | Research + proposal + loop built; awaiting Hoang's 5 launch-strategy decisions |
