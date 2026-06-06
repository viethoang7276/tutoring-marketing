# The CMO cycle — recurring loop operating manual

The weekly loop that turns research + first-party signal into two outputs: **marketing decisions**
(the calendar) and **feature requests** (the CTO handoff). Read alongside `session-start.md` (the
ritual) and `docs/feature-requests/README.md` (the handoff channel).

## Cadence

**On-demand** for now — tell the CMO "run a CMO cycle". This fits the local-first, pre-launch setup:
the cycle needs the local repo, local fixtures, and `npm run brief`, and its output (REQ files +
calendar proposals) must land in the local working tree for Hoang to review.

A true unattended **weekly schedule** is deferred. `/schedule` runs agents remotely in the cloud and
clones from a GitHub URL, so it cannot see local files — revisit it once this repo is on GitHub and
post-launch (when `/api/v1` data is real and the loop actually closes). Either way the cycle only
ever *proposes*; nothing it produces ships or posts without Hoang.

## The five steps of one cycle

1. **Scan** — live web research: finance/accounting student trends, format/platform shifts,
   competitor moves, seasonality 4–6 weeks out. (See the research reports in `docs/research/`.)
2. **Listen** — `npm run brief` for first-party signal: funnel, demand-gaps ("wanted it, didn't
   enrol"), feedback. Fixtures until the `/api/v1` token exists; the brief says which.
3. **Decide (marketing)** — update proposed pillars / campaigns / filming queue in
   `calendar/calendar.json` (Tier 1). Validate with `npm run calendar`. These remain *proposals*
   until Hoang locks them.
4. **Emit (product)** — when the scan or the brief reveals the product is *missing* something a
   customer or competitor signal demands, write a `REQ-####` into `docs/feature-requests/`
   (status `proposed`). Follow the guardrails in that folder's README — evidence first, tie to a
   metric, check it is not already out-of-scope.
5. **Report** — a short summary for Hoang: what changed in the scan, what marketing proposals moved,
   and any new feature requests awaiting his approve/defer/reject.

## The human gate (non-negotiable)

The CMO never approves its own work. Hoang:
- locks marketing decisions into the calendar, and
- approves feature requests, then **relays approved ones** into `../tutoring-web/docs/backlog.md`
  (and, when picked up, a `docs/specs/<feature>/requirements.md`). The CMO never writes into the
  CTO repo — independence rule.

## How the loop closes

A relayed request the CTO builds → the shipped feature changes the funnel / demand-gaps / feedback →
those return through `/api/v1` into step 2 of the next cycle → which generates the next decision and
the next request. Pre-launch the loop is open on the data side (research-driven only); it closes once
the read token lands and real students are in the funnel.

## What this loop is NOT

- Not autonomous shipping. No feature builds, and nothing posts, without Hoang.
- Not a cross-repo editor. The CMO writes only inside this repo; files are the contract.
- Not a place for opinions. Every feature request carries evidence and a target metric or it does
  not get written.
