# Edlintics — Brand Guidelines (marketing)

The human-readable companion to `config/brand.ts` (the machine-readable source of truth).
When these disagree, fix both — `config/brand.ts` is what the engine actually enforces.

## Audience

**Finance and accounting university students.** Everything is **topic-led**: a concept is the
headline (DCF, T-accounts, CVP, ratio analysis…). A university is named only as *secondary*
context, never the headline — for trademark and independence reasons.

## Voice

Calm, expert, direct, practical, slightly serious. We earn attention with the idea, not with hype.

**Hard rules** (the quality gate fails content that breaks these):

- No exclamation points.
- No emoji.
- Lead with the concept, not a university name.
- A university may appear only as secondary context, never in a headline.
- No hype, no hard-sell, no clickbait.

**Preferences:**

- Short sentences, one idea per line.
- Concrete over abstract — show the number, the journal entry, the formula.
- Respect the reader's time and intelligence.

## Color

Reconciled 2026-06-05 from the app brand system (`tutoring-web/docs/brand.md` + the rendered page
at `/en/brand-guidelines`). Literal hex lives in `config/brand.ts` — we never import app code, so
re-reconcile by hand when the app brand changes.

| Token | Hex | Role |
|---|---|---|
| `brand` | `#467DE3` | primary — edlintics blue. Stays in both light and dark modes. |
| `ink` | `#020817` | foreground / body text on light |
| `paper` | `#FFFFFF` | background, light |
| `accent` | `#60A5FA` | blue-400 — the gradient terminus for headline emphasis |
| `muted` | `#64748B` | secondary text (slate-500) |
| `border` | `#E2E8F0` | borders / dividers, light |
| `destructive` | `#EF4444` | errors |

Dark mode ships with a user toggle (default light): `inkDark #F8FAFC`, `paperDark #020817`,
`borderDark #1E293B`. Full accent palette (`accents`) and the three brand gradients (`gradients`)
are in `config/brand.ts`. **Hard rule: no more than two accents per section.** Subject mapping
matters for concept content — accounting/money = emerald, programming/data = cyan.

## Gradients

A **primary brand element**, not decoration. Use the primary gradient (`#467DE3` → `#60A5FA`, `to-r`)
for headline emphasis — it is the brand signature. CTA gradient for action panels; hero gradient for
section backgrounds. Don't add new gradients ad-hoc.

## Type

- **Inter** — UI chrome, marketing body, short headlines. Headline signature: extrabold (800),
  tracking-tight.
- **Source Serif Pro** — long-form / editorial "expertise" surfaces (lesson + blog body, landing H1).
- **Geist Mono** — code, formulas, tabular figures (price ladders, T-accounts).
- No italics for emphasis — use bold or color.

## Logo

**Pending redesign** (Hoang). The app today uses a gradient wordmark: "Ed" in foreground + "lintics"
in the primary→blue-400 gradient, Inter 800, tracking-tight, no tagline. Recorded in `config/brand.ts`
`logo` so Tier 2 stays consistent until the redesign lands. Never place on low-contrast backgrounds.

## Mascot — Castor (do NOT use in marketing)

The brand is deliberately **mascot-free on marketing and content**. Castor — a beaver in monochrome
edlintics blue — is a scoped exception for app surfaces only (404, error, empty state, onboarding,
loading) and is an *illustrative asset, never an icon, with no voice*. **It must never appear in a
hero, course landing, lesson/finance content, or a produced concept video/thumbnail.** Always
decorative (`aria-hidden`, empty `alt`).

Poses are vendored in `assets/brand/` (`mascot-{mark,wave,read,shrug,loading}.svg`) for completeness;
machine-readable policy is `config/brand.ts` `mascotPolicy`. The Tier 2 quality gate should flag
Castor in any marketing render as a violation. Source of truth: `tutoring-web/docs/brand.md` § Castor.
