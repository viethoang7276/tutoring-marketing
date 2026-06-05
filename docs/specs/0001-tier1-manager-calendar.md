# Spec 0001 — Tier 1: Marketing Manager + Content Calendar

Status: **in build** · Owner: Hoang · Created: 2026-06-05

## Goal

The first build slice of the Edlintics Marketing Engine. Stand up the **strategy loop**:
a data-grounded briefing the Manager brings to each session, the back-and-forth that turns it
into locked decisions, and the **content calendar** those decisions write to. No video/publish
pipeline (Tier 2) in this slice.

## Decisions locked (2026-06-05)

| Decision | Choice | Why |
|---|---|---|
| Runtime/language | **TypeScript / Node** | Matches `tutoring-site`, the `/api/v1` JSON, and Remotion (Tier 2). One language across both tiers. |
| Manager architecture | **Claude Code session + scripts** | The Manager *is* the Claude session, guided by `session-start.md`. Scripts build the briefing; the proposal/argument happens in chat; decisions are written to the calendar. Lowest infra. |
| Data source | **Mock-first, swap later** | `EDLINTICS_API_TOKEN` is not yet issued. A typed client reads local fixtures now and flips to live `/api/v1` when the token exists — no call-site changes. |
| Brand | **First-class layer from day one** | Voice + trademark rules feed both the Manager (Tier 1) and the quality gate (Tier 2). Centralized in `config/brand.ts` + `docs/brand-guidelines.md`. |

## Non-goals (this slice)

- No transcription / editing / rendering / publishing (Tier 2).
- No standalone autonomous agent loop — the human is in the loop every strategy session.
- No live `/api/v1` calls until a read token exists (the client is built to flip with zero call-site changes).

## The briefing (what `npm run brief` produces)

A single markdown briefing the Manager reads at the top of a strategy session. Three data-grounded
sections (built from `/api/v1` or fixtures) plus a placeholder the Manager fills live:

1. **Performance digest** — funnel (catalog → course → enrol) + per-post platform stats. *What landed.*
2. **First-party signal** — onboarding "wanted-it-didn't-enrol" demand gaps + survey/feedback themes. *Your data, not generic.*
3. **Trend scan** — finance/accounting student concerns + exam-season seasonality + format trends. *Filled live by the Manager via WebSearch; the script only stubs the section.*
4. **Proposals** — the Manager synthesizes 2-3 directions in chat from the above (not script output).

## The content calendar (system of record)

A single JSON file `calendar/calendar.json`, validated by a zod schema, holding:

- `period` — the planning window this calendar covers.
- `pillars` — content pillars for the period (name, description, rationale).
- `campaigns` — active/planned campaigns (angle, status, dates, pillar links).
- `filmingQueue` — concepts to film next, prioritized (drives Tier 2 later).
- `items` — individual content assets (date, channel, format, status, pillar/campaign links).
- `decisions` — append-only log of locked decisions + rationale (the audit trail).

`npm run calendar` renders it as human-readable markdown. The Manager writes to it by editing the
JSON (validated on read) and appending a decision entry.

## Acceptance criteria

- [ ] `npm run brief` prints a complete markdown briefing from fixtures with zero network/token.
- [ ] `npm run calendar` renders the seeded calendar as markdown.
- [ ] The API client flips fixtures → live by presence of `EDLINTICS_API_TOKEN`, no call-site change.
- [ ] `npm run typecheck` passes.
- [ ] Brand voice rules are machine-readable in `config/brand.ts` and human-readable in `docs/brand-guidelines.md`.
- [ ] `session-start.md` lets a fresh Claude session act as the Manager without prior context.
- [ ] `status.md` records what is built and what is next.

## Open (deferred to later slices)

- Channels in scope (IG / LinkedIn / TikTok / blog+newsletter) — calendar is channel-agnostic for now.
- Strategy cadence (weekly ritual vs on-demand).
- Real `/api/v1` endpoint shapes (fixtures encode our *assumed* shapes; reconcile when the token lands).
- Logo + mascot source files (structure scaffolded in `assets/brand/`; awaiting assets).
