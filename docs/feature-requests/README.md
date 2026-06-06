# Feature requests — CMO → CTO handoff

This folder is the **marketing-owned inbox** for product/feature ideas the CMO surfaces from
customer or competitor data. It is one half of the CMO↔CTO loop. The other repo (`../tutoring-web`,
"the CTO") never reads this folder directly — **Hoang is the bridge**: he approves a request here,
then relays the approved ones into the CTO repo's own inbox (`tutoring-web/docs/backlog.md` →
`docs/specs/<feature>/requirements.md`).

This keeps the two repos cleanly independent (this repo never touches app code) and keeps a human in
the loop on every feature decision — per `session-start.md`.

## The loop

```
CMO cycle (on-demand) ──► writes REQ-####-slug.md here (status: proposed)
                          │
                   HOANG reviews ──► approve / defer / reject  (logged in the file)
                          │ approved
                   HOANG relays ──► tutoring-web/docs/backlog.md (+ a spec when picked up)
                          │
                   CTO builds ──► feature ships
                          │
        Result returns via /api/v1 (funnel / demand-gaps / feedback) into the next CMO brief
```

Pre-launch, requests are mostly **competitor/research-driven** (the data side is empty until the
`/api/v1` read token exists). Post-launch they become **customer-data-driven** — born from the
`demand-gaps` ("wanted it, didn't enrol") and `feedback` (new-course / feature requests) signals in
`npm run brief`.

## How to write one

1. Copy `_TEMPLATE.md` to `REQ-####-short-slug.md` (next number, kebab-case slug).
2. Fill every section. Lead with the **evidence**, not the idea — a request without a data or
   competitor signal behind it does not belong here.
3. Leave `Status: proposed`. The CMO never approves its own requests.
4. Surface it to Hoang in the cycle summary.

## Guardrails (do not skip)

- **Never propose something already ruled out** in `tutoring-web/docs/{vision,product}.md`
  "out of scope" (gamification, AI student tutor, subscriptions, certificates, multi-tutor, etc.).
  Check before writing. Contradicting a locked decision wastes the CTO's time and ours.
- **Marketing states the problem + the signal; the CTO owns the design.** Requests describe the
  job-to-be-done and a success signal, not an implementation. Propose requirements, not code.
- **Tie every request to a metric.** Which number is it supposed to move (north-star session
  completion, a funnel step, a demand-gap)? If none, it is not a product request — it is an opinion.

## Status lifecycle

`proposed` → `approved` / `deferred` / `rejected` → (if approved) `relayed` → `building` → `shipped`
→ `measuring`. Update the file's `Status:` line and the Decision log as it moves.

## Index

| ID | Title | Status | Source | Metric it targets |
|---|---|---|---|---|
| REQ-0001 | (example) Free concept pages for SEO + lead capture | example | research | acquisition → course-page visits |
