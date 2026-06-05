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
- **2026-06-05** — Reconciled the brand pack from `tutoring-web/docs/brand.md`: real semantic
  colors + full accent palette + the three brand gradients + the Inter/Source Serif Pro/Geist Mono
  type system into `config/brand.ts`; vendored Castor poses into `assets/brand/`; added the
  do-not-use-in-marketing mascot policy + the pending-redesign logo spec. Updated
  `docs/brand-guidelines.md` + `assets/brand/README.md`. Typecheck passes. API/token work parked
  pre-launch. Logo redesign still outstanding.
