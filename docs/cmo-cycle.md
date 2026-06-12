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
   - **Need a real number before the token lands?** The app repo has a read-only CLI,
     `edctl`, with report/feedback exports. Run from `../tutoring-web`:
     `pnpm edctl reports enrollments --format csv`,
     `pnpm edctl reports course-completion --format csv`,
     `pnpm edctl reports revenue-mtd --format json`, and
     `pnpm edctl feedback export [--course <id>] --format csv`. **Use ONLY these read-only
     report/feedback commands** — they are the marketing-safe surface (no writes, no admin
     token). This does **not** change the cross-division contract: marketing's *automation*
     still reads only through `/api/v1`; these are a manual operator export, not app-code
     imports. Full reference: `../tutoring-web/docs/onboarding/content-cli.md`.
3. **Decide (marketing)** — update proposed pillars / campaigns / filming queue in
   `calendar/calendar.json` (Tier 1). Validate with `npm run calendar`. These remain *proposals*
   until Hoang locks them.
4. **Emit (product)** — when the scan or the brief reveals the product is *missing* something a
   customer or competitor signal demands, write a `REQ-####` into `docs/feature-requests/`
   (status `proposed`). Follow the guardrails in that folder's README — evidence first, tie to a
   metric, check it is not already out-of-scope.
5. **Report** — write the **weekly CMO report** to `docs/reports/YYYY-W##-cmo-weekly.md` (template
   and rules in `docs/reports/README.md`). Four sections, always: (1) current plan, (2) performance
   last week, (3) next-week implementation plan with any tweak, (4) feature proposals — plus a
   "decisions needed from you" footer. Update the index row in `docs/reports/README.md`. This report
   is the headline deliverable of the cycle; offer a `.docx` render if Hoang wants to forward it.
   If Slack is configured (`.env` has `SLACK_BOT_TOKEN` + `SLACK_CHANNEL_ID`), deliver it by running
   `python3 scripts/post_report_to_slack.py --send` — a summary message plus the Word doc in-thread
   (setup: `docs/SLACK-SETUP.md`).

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
