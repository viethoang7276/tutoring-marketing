# Brand assets

Home for the visual brand: logo, mascot, and any reusable marks. Referenced by `config/brand.ts`
(`brand.assets`) and used by Remotion templates (Tier 2).

## Manifest (current)

| File | Purpose | Status |
|---|---|---|
| `logo.svg` | Primary logo | **PENDING REDESIGN** (Hoang). App today uses a gradient wordmark — see `config/brand.ts` `logo`. |
| `mascot.svg` | Castor, default "mark" pose | Vendored from `tutoring-web/public/castor`. |
| `mascot-{mark,wave,read,shrug,loading}.svg` | Castor poses | Vendored. Monochrome edlintics blue, baked in. |
| `favicon.svg` | Small mark | Vendored (`castor-favicon`). |

SVGs are tracked in git. Large rasters/source files (`.psd`, `.ai`, big `.png`) are gitignored as
binaries — back them up separately and keep this folder as the manifest of record.

## Usage rules

- **Logo:** gradient wordmark — "Ed" in foreground + "lintics" in the primary→blue-400 gradient,
  Inter 800, tracking-tight, no tagline. Pending a redesign before we lean on it in renders. Never
  place on low-contrast backgrounds; pair with `brand.colors`.
- **Castor mascot — do NOT use in marketing.** The brand is deliberately mascot-free on marketing
  and content. Castor is an illustrative beaver (not an icon), monochrome edlintics blue, with no
  voice. Allowed only on app surfaces: 404, error, empty state, onboarding, loading. It must never
  appear in a hero, course landing, lesson/finance content, or a produced concept video/thumbnail.
  Always decorative (`aria-hidden`, empty `alt`). Source of truth: `tutoring-web/docs/brand.md`
  § "Castor (mascot)"; machine-readable in `config/brand.ts` `mascotPolicy`.

> Upstream: `tutoring-web/docs/brand.md` + the rendered page at `/en/brand-guidelines`. When the
> app brand changes, re-reconcile `config/brand.ts` and this manifest by hand (we never import app code).
