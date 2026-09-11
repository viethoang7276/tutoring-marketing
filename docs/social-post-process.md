# Social Post Process — Edlintics (DRAFT v1, pending Hoang's lock)

How a marketing idea becomes scheduled posts across every channel. Builds on the locked
worked-example video pipeline (`docs/shorts-format-spec.md`, `calendar/content-plan.md`); it does
**not** replace it. This doc adds the static-post lane, the humour format, and per-platform
packaging, and wires the whole thing into one weekly loop.

Decisions this encodes (Hoang, 2026-06-23):
- **One brand, one account per platform.** Customer profiles are served by *pillars*, not by
  separate channels.
- **Memes are a minor supporting format** (~15–20%), inside the locked brand voice — no emoji, no
  hype, dry accountant-humour that pays off into a real concept.
- **AI/Canva for assets + static posts + on-screen graphics; the presenter-led worked example stays
  human.** That human-on-camera core is the moat and is not AI-generated.

---

## 1. Channels (one account per platform)

| Platform | Role | What posts here | Effort |
|---|---|---|---|
| **TikTok** | Primary discovery | Short-form video (worked-example cuts, Q&A, humour) | Core |
| **Instagram** | Discovery + depth | Reels (same shorts) + feed carousels/static posts | Core |
| **YouTube** | Search + trust | Long worked examples (5–8 min) + Shorts | Core |
| **Facebook** | Mirror only | Cross-post of Reels + static; zero bespoke work | Repost |

Facebook is a zero-marginal-cost repost target, not a primary channel — Gen-Z finance undergrads
don't discover there. We mirror, we don't invest.

One brand voice everywhere (`config/brand.ts`). Profiles (first-year uni-exam / ACCA-track /
finance-track) are addressed by **which pillar and topic** a post belongs to — the algorithm
segments the audience for us.

## 2. The four content lanes

Every post is one of these. The mix is what keeps a single channel varied without fragmenting it.

| Lane | Format | Source | Owner agent | Share of feed |
|---|---|---|---|---|
| **A. Worked example** | Human-on-camera video (YT long + 2 shorts) | Hoang films | copywriter + asset-designer | ~50% |
| **B. Static / carousel** | Canva post on brand template (the trap, exam-tip, concept-in-one-card) | AI + Canva | asset-designer + copywriter | ~25% |
| **C. Q&A exercise** | Light video, numbers worked on screen (no presenter required) | AI graphics + voice/caption | asset-designer | ~10% |
| **D. Humour hook** | Dry accountant-humour short or static, brand voice | copywriter + asset-designer | copywriter | ~15% |

Lane A is the moat and the trust anchor. Lanes B–D are the reach/variety layer that AI + Canva make
cheap. Every lane maps to one of the three pillars (Worked-Not-Watched / Concept-You'll-Be-Tested-On
/ What-AI-Gets-Wrong) so nothing drifts off-strategy.

## 3. The weekly loop

```
PLAN ──► PRODUCE ──► BRAND-REVIEW ──► APPROVE ──► PACKAGE ──► SCHEDULE ──► PUBLISH ──► MEASURE
(CMO)    (roles)     (brand-reviewer)  (Hoang)    (dist-op)   (dist-op)   (Hoang gate) (analyst)
```

1. **Plan** — CMO sets the week's slots from the calendar: which pillar, topic, lane per channel.
2. **Produce** — role agents draft to brief. Lane A pulls from filmed footage; B/C/D are
   AI/Canva-generated against the brand template. All output is a **draft**.
3. **Brand-review** — `brand-reviewer` gates voice + visual rules. FAIL → owning role revises. This
   is where most meme drafts get caught and tightened.
4. **Approve** — Hoang approves. Nothing proceeds without it. (Absolute gate.)
5. **Package** — `distribution-operator` cuts per-platform variants: title/caption/hashtags per
   channel, aspect ratios, the right CTA.
6. **Schedule** — load into `calendar/calendar.json` publish slots (scheduler tool still an open
   decision — Ayrshare/Metricool/Postiz).
7. **Publish** — the post button is Hoang's. Approval to *prepare* is not approval to *post*.
8. **Measure** — `performance-analyst` reads results once channels are live; feeds the next Plan.

## 4. Per-channel weekly cadence (target for one operator)

Conservative, matched to a single filmer + AI-assisted static lane:

| Channel | Mon | Wed | Fri | Weekly |
|---|---|---|---|---|
| TikTok | Short (A) | Static→Reel or Q&A (B/C) | Humour (D) | 3 |
| Instagram | same Reel | Carousel (B) | same humour | 3 + 1 carousel |
| YouTube | Long worked example (A) | — | Short cut | 1 long + 1 short |
| Facebook | mirror | mirror | mirror | 0 bespoke |

Static/meme lanes (B/D) are AI-assisted, so they scale without more film days — they're what lets us
post 3×/week per channel while only filming one worked example a week. **Non-negotiable rule
carries over: film ahead, publish steadily — never let publishing catch up to production.**

## 5. The AI / Canva static-post sub-pipeline (the new part)

For lanes B and D, no camera needed:

1. **copywriter** drafts the card copy (hook line + the concept/trap), brand voice, from the
   pillar + topic brief.
2. **asset-designer** generates the visual in Canva from the **brand template** (Canva MCP:
   `create-design-from-brand-template` → `export-design`), locked to `config/brand.ts` tokens —
   gradient signature, two-accent rule, type system, **no mascot, no emoji**.
3. **brand-reviewer** gates the rendered asset + copy together.
4. **distribution-operator** packages captions/hashtags per channel.

This is the lane that makes "AI-generated posts with Canva + brand template" real — and it's
genuinely cheap to run at volume. The guardrail is the brand template + brand-reviewer, so AI volume
never costs us brand consistency.

## 6. Guardrails (carried from the constitution)

- **Topic-led headlines**, never university-led. Trademark independence.
- **No emoji, no exclamation points, no hype.** Especially enforced on the humour lane.
- **Characters only where approved** — the cast (Ledger, Sigma, Centi, Plot, Tempo) is forbidden in
  marketing renders by default; allowed only on surfaces listed in `config/brand.ts`
  `characterSystem.approvedMarketingExceptions`. Castor the beaver was retired 2026-06-07.
- **Human approval is absolute** at both the approve and publish steps.
- **No synthetic presenter video** — lane A stays a real person working real numbers.

## 7. What's still open before this can run

- **Scheduler choice** (Ayrshare / Metricool / Postiz) — needed for step 6 at scale.
- **Account setup** — IG/TikTok/YT accounts per the Jun-8 setup row in the content calendar;
  Facebook page if we want the mirror.
- **First static-lane proof** — produce one Canva carousel end-to-end through this loop (analogous
  to the CF-01 auto-clip pipeline test) before scaling the lane.
- **Brand template in Canva** — confirm a published brand template exists to generate from.
