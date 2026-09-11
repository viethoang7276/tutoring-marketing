# Social profile assets — rebrand rollout

Built 2026-08-03 by `scripts/build_social_assets.py`. Rebuild any time with:

```bash
python3 scripts/build_social_assets.py                 # all assets
python3 scripts/build_social_assets.py cover-facebook   # one asset
python3 scripts/build_social_assets.py --guides         # safe-zone proofs
```

Everything is composed from the **real** brand geometry — the `BrandMark` tie paths and the
EdCharacter SVGs vendored in `assets/brand/` — and rasterized by headless Chrome. Fonts are embedded
from `assets/fonts/`, so a render is reproducible and needs no network. No image generator is
involved: the cast and the mark are fixed vector artwork, and a diffusion model would only produce
a lookalike.

## What to upload where

| Platform | Asset | File | Pixels |
|---|---|---|---|
| Instagram | Profile picture | `avatar-instagram.png` | 320 × 320 |
| Facebook | Profile picture | `avatar-facebook.png` | 320 × 320 |
| Facebook | Cover photo | `cover-facebook.png` | 1640 × 624 |
| LinkedIn | Company logo | `avatar-linkedin.png` | 400 × 400 |
| LinkedIn | Page banner | `cover-linkedin.png` | 4200 × 700 |
| Instagram | Pinned grid (3 posts) | `instagram-tile-{1,2,3}-*.png` | 1080 × 1350 |

### Instagram has no cover photo

There is no cover-image slot on an Instagram profile — the equivalent surface is the top row of the
grid. The three 1080 × 1350 tiles are designed to be **pinned** so they hold that row:

1. `instagram-tile-1-statement` — the brand statement
2. `instagram-tile-2-cast` — the cast + accounting graphics
3. `instagram-tile-3-concept` — a worked-example hook

**Post them in reverse order (3, then 2, then 1)** so tile 1 ends up top-left, then pin all three.

## Safe zones (why the layouts are off-centre)

Both covers are laid out around two crops. The `*-guides.png` proofs draw them; those files are
verification only and are never uploaded.

- **Facebook** — mobile crops ~90 px per side (180 px at our 2× canvas), so the safe zone is the
  centre 1280 px. The page profile photo also overlaps the lower-left, so that corner is empty by
  design.
- **LinkedIn** — mobile crops to roughly the centre 80 %, so the safe zone is the centre 3350 px.
  The company logo tile overlaps the lower-left, which is again deliberately empty.

## Brand notes

- Type: Source Serif 4 headline, Inter wordmark and cards, Lato kicker. No emoji, no exclamation
  points, no tagline under the wordmark.
- The avatar is the `full` mark (collar + tie) in the brand gradient on a **white** ground — the
  logo's own colours, matching the lockup on the covers. This is deliberately the inverse of the app
  icon (`public/brand/favicon-512.png`), which is a white tie on blue. It sits at 62 % of the frame
  so it stays clear of the circular crop every platform applies.
- Characters used: Ledger, Centi, Plot, Sigma. Always decorative, never with a voice or speech
  bubble. This surface is a **logged exception** to the mascot-free-in-marketing default — see
  `config/brand.ts` `characterSystem.approvedMarketingExceptions`.
