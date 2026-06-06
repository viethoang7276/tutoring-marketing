# STATUS — living state

The cross-session memory for this repo. Read after `session-start.md`. Update it at the end of any
session that changes state (append to the session log; revise "Now" / "Next").

_Last updated: 2026-06-05_

## Now (what exists and works)

- **Tier 1 slice built** (spec `docs/specs/0001-tier1-manager-calendar.md`):
  - `npm run brief` → data-grounded briefing (performance digest, first-party signal, trend-scan
    stub, proposals prompt). Runs on **fixtures** (no read token yet).
  - `npm run calendar` → renders `calendar/calendar.json` (schema-validated).
  - `npm run typecheck` → passes.
- **Brand layer:** `config/brand.ts` — voice rules + **real** color/accent/gradient/type tokens
  (reconciled 2026-06-05 from `tutoring-web/docs/brand.md`) + `docs/brand-guidelines.md`. Castor
  mascot poses vendored into `assets/brand/` with a do-not-use-in-marketing policy. Logo PENDING
  REDESIGN (app today = gradient wordmark, recorded in `config/brand.ts` `logo`).
- **Runtime:** TypeScript / Node 22, zod-validated. Deps: `zod` + dev `tsx`/`typescript`.

## Decisions locked

- 2026-06-05 — Runtime = **TypeScript/Node**. Manager = **Claude Code session + scripts** (this
  file is its operating manual). Data = **mock-first** (fixtures → live by presence of token).
  Brand is a **first-class layer** from day one.

## Next (in rough priority order)

0. **DISCUSS the fall-launch market research with Hoang (morning 2026-06-06)** —
   `docs/research/2026-06-05-fall-launch-market-research.md`. Argue out the 3 proposed directions
   (A "Worked, not watched" / B seasonal-SEO harvest / C "What AI gets wrong"), resolve the 5 open
   questions (channels, trademark trade-off, cadence, lead courses, filming setup), THEN lock
   survivors into `calendar/calendar.json`.
1. **Run the first real strategy session** — `npm run brief`, do the live trend scan, propose,
   and write the first real pillars/campaign into `calendar/calendar.json`.
2. **Issue the read-only `/api/v1` token** on the app side, set `EDLINTICS_API_TOKEN` in `.env`,
   then **reconcile fixture shapes** with the real endpoints (`manager/briefing/fixtures/*` map
   1:1 to assumed paths in `client.ts`).
3. **Brand pack** — DONE except the logo: colors/fonts reconciled from `tutoring-web/docs/brand.md`,
   mascot vendored. Remaining: drop the **redesigned** `logo.svg` into `assets/brand/` when ready.
4. **Resolve open decisions** (README): channels in scope, strategy cadence, scheduler, approval
   strictness.
5. **Tier 2** (later): ingest → transcribe → edit → atomize → publish. Not started.

## Known gaps / watch-outs

- Fixture data is illustrative, not real numbers — do not cite it as fact in a real session.
- API/token work is **parked pre-launch** (Hoang's call) — no live `/api/v1` until the app ships.
- Brand colors/fonts in `config/brand.ts` are now **real** (reconciled from `tutoring-web/docs/brand.md`).
  Upstream is read, never imported — re-reconcile by hand if the app brand changes.
- **Castor mascot is forbidden in marketing output** — vendored only for completeness; Tier 2's
  quality gate must flag it in any marketing render.
- Logo is **pending redesign** — current gradient-wordmark spec recorded but no `logo.svg` yet.
- `/api/v1` endpoint shapes are **assumed**; the app may differ. Reconcile when launch nears.

## Session log

- **2026-06-05** — Scaffolded + built Tier 1 (briefing + calendar + brand layer). Wrote
  `session-start.md`, this file, and spec 0001. Calendar still seeded/empty (no real session run).
- **2026-06-05 (night)** — CMO market-research task. Read `tutoring-web/docs` (vision/product/brand)
  to ground company understanding; ran live web research (StudyTok/Gen-Z finance media, short-form
  2026 mechanics, AI-study dynamic, creator landscape, EU exam seasonality incl. the IE 2026-2027
  calendar). Wrote `docs/research/2026-06-05-fall-launch-market-research.md` — seasonal spine,
  scenarios, monthly calendar, 3 proposed directions, 5 open questions. To discuss morning 06-06.
- **2026-06-06** — Live TikTok/Instagram hashtag scan (real browser, public pages only). Pulled
  8 live TikTok video counts + content patterns; key finding: `#financialaccounting` ~4K vs
  `#studytok` 4.2M (~1000× gap) → exact-concept lane is uncrowded but needs reach-tag stacking;
  `vinnyhale` leads the concept lane but aims at CPA/professionals, leaving the undergrad-exam
  angle open. Instagram no longer publishes hashtag counts (repurpose target, not measurement).
  Wrote `docs/research/2026-06-06-tiktok-instagram-hashtag-stats.md`.
- **2026-06-06** — Added a deeper research round (hardest accounting topics → flagship pillar
  topics; organic-growth + conversion benchmarks; YouTube-as-search) and produced a CMO→CEO
  **Word proposal**: `docs/research/Edlintics-Marketing-Proposal-Fall-2026.docx` (generator at
  `scripts/build_proposal_docx.py`, needs `python-docx`). 12 sections + appendices: exec summary,
  situation, the wedge, 3 pillars (Worked-Not-Watched / Concept-You-Will-Be-Tested-On /
  What-AI-Gets-Wrong), channels, seasonal plan, flagship topics, funnel/targets, risks, the 5
  decisions for Hoang, recommendation. Built but no calendar yet — awaiting Hoang's decisions.
- **2026-06-06** — Stood up the **CMO↔CTO loop** (human-gated). New `docs/feature-requests/`
  channel (README + `_TEMPLATE.md` + an EXAMPLE REQ-0001) and `docs/cmo-cycle.md` operating manual;
  `session-start.md` now points to both. Flow: CMO writes feature requests from customer/competitor
  data → Hoang approves → Hoang relays approved ones into `../tutoring-web/docs/backlog.md`/specs
  (CMO never writes the app repo — independence). Trigger decision: **on-demand, local** ("run a CMO
  cycle"). Remote weekly `/schedule` deferred — it runs in the cloud + needs a GitHub remote, which
  this local-first repo lacks; revisit once on GitHub + post-launch. Marketing repo still has no git
  remote.
- **2026-06-05** — Reconciled the brand pack from `tutoring-web/docs/brand.md`: real semantic
  colors + full accent palette + the three brand gradients + the Inter/Source Serif Pro/Geist Mono
  type system into `config/brand.ts`; vendored Castor poses into `assets/brand/`; added the
  do-not-use-in-marketing mascot policy + the pending-redesign logo spec. Updated
  `docs/brand-guidelines.md` + `assets/brand/README.md`. Typecheck passes. API/token work parked
  pre-launch. Logo redesign still outstanding.
