# REQ-####  ·  <short title>

- **Status:** proposed   <!-- proposed | approved | deferred | rejected | relayed | building | shipped | measuring -->
- **Date:** YYYY-MM-DD
- **Source:** competitor | customer-data | research   <!-- where the signal came from -->
- **Targets metric:** <north-star session completion | funnel step | named demand-gap | acquisition>
- **Priority (CMO view):** high | medium | low
- **Effort guess (CMO, non-binding):** S | M | L

## Summary
One or two sentences. What is missing, for whom, and why it matters now.

## Evidence (lead with this)
The data or competitor signal that triggered this. Be concrete and cite it.
- First-party (post-launch): the demand-gap / feedback / funnel figure from `npm run brief`.
- Competitor / research: what a competitor does, or what the market data shows, with a source link.
- If the evidence is thin, say so — a hypothesis labelled as a hypothesis is honest; a guess dressed
  as data is not.

## Hypothesis
We believe that **<doing X>** for **<this student>** will cause **<this metric>** to move because
**<reason grounded in the evidence>**.

## Job to be done (problem, not solution)
In the student's voice: "When I … I want to … so that …". The CTO owns the design; this states the
job the design must satisfy.

## Proposed requirements (CTO owns the final design)
Rough acceptance criteria, in the CTO repo's vocabulary so it relays cleanly into
`docs/specs/<feature>/requirements.md`:
- The system shall …
- The system shall …

## Success signal (how marketing will know it worked)
The specific metric and the direction/threshold we expect. Ties back to "Targets metric" above.

## Out-of-scope check
Confirm this does not contradict a locked decision in `tutoring-web/docs/{vision,product}.md`
"out of scope". Note anything adjacent that IS ruled out, so the CTO is not asked to re-litigate it.

## Decision log
- YYYY-MM-DD — proposed by CMO.
- _(Hoang: approve / defer / reject + reason here.)_
