# Brand assets

Home for the visual brand: the mark, the character cast, and any reusable artwork. Referenced by
`config/brand.ts` (`brand.assets`) and by `scripts/build_social_assets.py`.

**Re-vendored 2026-08-03** from the rebranded app (brand v1.2 / v1.3). The previous contents —
Castor the beaver — were retired upstream on 2026-06-07 and have been deleted.

## Manifest (current)

| File | Purpose | Status |
|---|---|---|
| `app-icon-512.png` | Tie mark on the brand gradient — the social avatar / app icon | Vendored from `tutoring-web/public/brand/favicon-512.png`. |
| `favicon.svg` | Small mark | Vendored from `tutoring-web/public/brand/`. |
| `ledger.svg` | **Ledger** — the manual, the lead character | Vendored from `tutoring-web/public/mascot/`. |
| `ledger-stuck.svg` | Ledger, `stuck` emotion (404 / error) | Vendored. |
| `sigma.svg` | **Sigma** — the calculator | Vendored. |
| `centi.svg` | **Centi** — the coin | Vendored. |
| `plot.svg` | **Plot** — the chart | Vendored. |
| `tempo.svg` | **Tempo** | Vendored. |

Reusable exports added 2026-10-19:

- `edlintics-logo.svg`: transparent tie + Edlintics wordmark, lettering outlined from vendored Inter 800, matching the live header proportions (26px mark / 19px text / 10px gap). Static blue gradient; live header ink is #0D1117.
- `edlintics-mark.svg`: transparent collar-and-tie mark, without lettering.
- `favicon.svg`: existing white mark on a rounded blue square.

All three uploaded to Canva on 2026-10-19. Also uploaded directly through the native Canva app into the Edlintics Brand Kit → Logos and visually verified after saving (three new logos alongside the pre-existing logo). Media IDs: wordmark `MAHYbxRt4H0`, transparent mark `MAHYbzIC5gs`, square icon `MAHYb4j6PV8`.

Reference geometry remains in `scripts/build_social_assets.py` (`tie_mark()` / `wordmark()`).

SVGs are tracked in git. Large rasters and source files (`.psd`, `.ai`, big `.png`) are gitignored —
back them up separately and keep this folder as the manifest of record.

## Usage rules

- **Logo.** Wordmark = "Ed" in foreground + "lintics" in the primary→blue-400 gradient, Inter 800,
  tracking-tight, **no tagline**. Mark = necktie framed by a collar in the `#6FA0F0 → #2F58A8`
  gradient — **never recolored**. Use `full` (collar + tie) where the logo leads; `tie` only for the
  smallest contexts (favicon, social avatar). Clear space = the height of the "E". Never place on a
  low-contrast background.
- **Character cast — not a general marketing asset.** The brand is mascot-free on marketing and
  content **by default**. The cast is an *illustrative asset, never an icon, with no voice* — it
  never talks, jokes, cheers, or appears in a speech bubble. Always decorative (`aria-hidden`, empty
  `alt`); meaning lives in the surrounding copy.
  - Always allowed on app surfaces: 404, error, empty state, onboarding, loading.
  - Every **marketing** use needs Hoang's explicit sign-off, logged in `config/brand.ts`
    `characterSystem.approvedMarketingExceptions`. Anything not on that list is a violation and the
    brand-reviewer flags it.
  - The tie is on **Ledger only** (printed on its book). The others stand on bare cream stub arms.
    Never move the tie onto another character; never recolor it.

### Quiz series exception — 2026-10-19

Hoang explicitly approved using EdCharacter and existing graphics for economics, finance,
accounting, and statistics quiz posts in the existing Canva templates, and requested an additional
agent to add the mascots. This exception is recorded in `config/brand.ts`. Preparation and design
use are approved; publication still requires post approval. Keep the original cast artwork intact.

Run `python3 scripts/build_edcharacter_assets.py` with CairoSVG and Pillow installed to create
transparent 960 × 1080 PNGs of all six existing SVG assets and a labeled contact sheet in
`assets/renders/edcharacters/`. PNGs are generated, gitignored upload assets; the SVGs and build
script are the reproducible source. The contact sheet is a selection reference, not a post image.

> Upstream: `tutoring-web/docs/product/brand.md` + the rendered page at `/en/brand-guidelines`. When
> the app brand changes, re-reconcile `config/brand.ts` and this manifest by hand (we never import
> app code). The 2026-06-07 rebrand went unnoticed here for eight weeks — check this every cycle.

Canva placement verified 2026-10-19: five idle characters uploaded to
[Edlintics / Mascots](https://www.canva.com/folder/FAHYcZVFBhg), linked in Brand Kit
Graphics. Ledger `MAHYcRGqVl4`, Sigma `MAHYcdvon44`, Centi `MAHYceRqfc4`,
Plot `MAHYccAqQy4`, Tempo `MAHYcQG8xGE`. Existing folder permissions retained.
