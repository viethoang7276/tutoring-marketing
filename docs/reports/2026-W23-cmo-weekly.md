# CMO weekly report — 2026-W23

- **Week:** Mon 2026-06-01 → Sun 2026-06-07
- **Prepared for:** Hoang (CEO)  ·  **By:** Marketing Manager (CMO)
- **Data source this week:** research / live scan only (brief still on fixtures — no `/api/v1` token yet)
- **Status:** proposal — nothing locked until you approve

## 1. Current plan
- **Goal:** be visible to an exam-anxious business undergraduate at the moment of peak need, so the
  Sept 1 launch converts into the autumn exam cycle.
- **Timing:** we are in the **June–Aug build window**. Demand spikes mid-Oct–early-Nov (midterms)
  and early–mid-Dec (finals); IE classes start 31 Aug. Content has ranking lag, so the rule is
  build now, harvest in October.
- **Proposed direction — three pillars** (from `docs/research/Edlintics-Marketing-Proposal-Fall-2026.docx`):
  1. **Worked, Not Watched** — screen-recorded worked exam problems; the moat, filmed. The spine.
  2. **The Concept You Will Be Tested On** — seasonal concept series timed to the exam waves.
  3. **What AI Gets Wrong** — the differentiator (AI gives an answer; it can't watch you try).
- **Channels (proposed):** YouTube primary, TikTok + Reels as the net, Reddit/Discord light-touch,
  LinkedIn deferred.
- **Locked vs proposed:** brand pack is **locked** (real colours/type reconciled). Everything
  strategic above is **proposed** — it gates on your five decisions (see footer).

## 2. Performance — past week
No channel metrics exist yet (pre-launch, nothing posted, brief is fixtures). This week was research
and infrastructure. What got done:
- **Company grounding** — read `tutoring-web/docs` (vision, product, brand); persona, edge, model,
  Sept 1 launch, north-star (session completion) all internalised.
- **Two research reports** — fall-launch market research (seasonal spine, scenarios, monthly plan)
  and a **live TikTok/Instagram hashtag scan**. Key finding: the exact-concept lane is ~1,000× less
  crowded than broad study tags (`#financialaccounting` ~4K vs `#studytok` 4.2M), and its incumbents
  aim at US/CPA professionals — the EU-undergraduate exam angle is open.
- **CEO proposal** — the Word document above (3 pillars, channels, funnel model, decisions).
- **Brand pack reconciled** — real edlintics-blue colours, accent palette, gradients, type system,
  Castor mascot vendored (with a do-not-use-in-marketing policy). Logo pending your redesign.
- **CMO↔CTO loop built** — feature-request channel + cycle manual + this report format.
- **Pipeline status:** zero of the flagship worked-examples filmed yet (blocked on your go + a
  confirmed screen-recording setup).

## 3. Next week — implementation plan (with tweaks)
- **Get your five decisions** (footer) so the strategy moves from proposed to locked.
- **Pick the 1–2 lead courses** — the surest October converters — to build the first flagship
  worked-examples around (candidates: cash-flow statement, T-accounts).
- **Confirm the filming setup** (screen capture + clean audio). If ready, **film the first two
  worked-examples** next week — this is the long-lead item; every week we wait is a week off the
  October ranking runway.
- **Decide scheduling** — whether to wire the local `launchd` job so this report and the cycle run
  unattended (vs staying on-demand).
- **Tweak:** none yet. No performance data exists to tweak against; the plan stands as proposed.
  The first real tweak cycle begins once content is live or the `/api/v1` token lands.

## 4. Feature proposals
| REQ | Title | Status | Targets metric | Needs from you |
|---|---|---|---|---|
| REQ-0001 | Free concept pages for SEO + lead capture | **example** (format demo) | acquisition → course-page visits | Say if you want it promoted to a **live** proposal |

No live feature requests this week — pre-launch, there is no customer data yet (the request engine
runs on `demand-gaps` + `feedback` from `npm run brief`, which is fixtures until the token exists).
REQ-0001 is a worked example of the format, not a live ask.

## Decisions needed from you
- [ ] **1 — Channels:** confirm YouTube-primary / TikTok+Reels net / Reddit+Discord light / defer LinkedIn.
- [ ] **2 — Trademark trade-off:** confirm we stay strictly topic-led (forfeit the branded-exam hook).
- [ ] **3 — Cadence:** the realistic produced-pieces-per-week you can hold through the build.
- [ ] **4 — Lead courses:** which 1–2 exams lead the flagship worked-examples.
- [ ] **5 — Filming setup:** confirmed, or a gap to close before June filming.
- [ ] **6 — Scheduling:** wire the local `launchd` weekly job, or keep the cycle on-demand.
- [ ] **7 — REQ-0001:** promote the concept-SEO-pages idea to a live feature request, or leave as example.
