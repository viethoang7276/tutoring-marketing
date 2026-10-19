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
- **Lato** — uppercase kickers, prices, tabular figures. (Replaced Geist Mono in June 2026; the
  brand no longer has a monospace face.)
- No italics for emphasis — use bold or color.

## Logo

**Resolved** — the redesign landed upstream as brand v1.2. Two parts:

- **Wordmark** — "Ed" in foreground + "lintics" in the primary→blue-400 gradient, Inter 800,
  tracking-tight, **no tagline**. Clear space = the height of the "E".
- **Mark** — a necktie framed by a collar, in the `#6FA0F0 → #2F58A8` gradient (never recolored).
  `full` = collar + tie; `tie` = tie only, for the smallest contexts (favicon, social avatar).

Both are drawn from geometry, so they stay crisp at any size — see `config/brand.ts` `logo.mark`
and `scripts/build_social_assets.py`. Never place on low-contrast backgrounds.

## Character system (mascot) — scoped exception

> **Castor the beaver was retired upstream on 2026-06-07 and no longer exists.** Anything in this
> repo dated before 2026-08-03 that mentions Castor is stale.

The cast is **Ledger** (the manual — the lead), **Sigma**, **Centi**, **Plot**, **Tempo**. Each is
an *illustrative asset, never an icon, with no voice*. The tie is on Ledger only, printed on its
book; the others stand on bare cream arms. Eight calm emotional states — no angry, crying or silly.

**The default is still mascot-free on marketing and content.** App surfaces (404, error, empty
state, onboarding, loading) are always allowed. Every *marketing* use is a separate exception that
needs Hoang's explicit sign-off, logged in `config/brand.ts` `characterSystem.approvedMarketingExceptions`.
Anything not on that list is a violation, and the quality gate should flag it.

Approved so far:

| Date | Surface | Characters |
|---|---|---|
| 2026-08-03 | Social profile covers + Instagram pinned grid | Ledger, Centi, Plot, Sigma |
| 2026-10-19 | Economics, finance, accounting, and statistics quiz social posts using existing Canva templates | Ledger, Sigma, Centi, Plot, Tempo |

On 2026-10-19 Hoang explicitly requested EdCharacter and existing graphics for quiz images and
asked an additional agent to add the mascots. This authorizes preparation and design use for the
quiz series. Each post still needs approval before publication. Use the existing cast artwork
unchanged, with subject clues in the surrounding graphics and copy; do not give the characters
speech bubbles or a voice.

Transparent PNG exports and a labeled contact sheet are generated by
`python3 scripts/build_edcharacter_assets.py` (requires CairoSVG and Pillow) in
`assets/renders/edcharacters/`. The SVG originals remain canonical.

The cast is vendored in `assets/brand/` (`ledger`, `ledger-stuck`, `sigma`, `centi`, `plot`,
`tempo`). Source of truth: `tutoring-web/docs/product/brand.md` § "Character system".
