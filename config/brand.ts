/**
 * Brand tokens — the single source of truth for how Edlintics marketing looks and sounds.
 *
 * Consumed by:
 *   - Tier 1 Manager     — keeps proposals/copy on-voice.
 *   - Tier 2 quality gate — voice + trademark check before anything publishes.
 *   - Remotion templates  — colors/type for animated concept graphics.
 *
 * Colors/type mirror the app brand system. Upstream sources (read, never imported):
 *   - tutoring-web/docs/product/brand.md    — the rules + reasoning
 *   - http://localhost:3000/en/brand-guidelines — the rendered truth (canonical when in doubt)
 * Values below are LITERAL copies (this repo never imports app code). When the app brand
 * changes, update these by hand.
 *
 * Reconciled 2026-06-05, then again 2026-08-03 for brand v1.2/v1.3: Castor retired in favour of
 * the EdCharacter cast, the logo redesign landed (wordmark + collar-and-tie mark), and Lato
 * replaced Geist Mono. Anything older than 2026-08-03 that mentions Castor is stale.
 */

export const audience = {
  primary: "Finance and accounting university students",
  // Topic-led: a university is named only as SECONDARY context, never the headline.
  // (trademark + independence — see voice.trademark)
  framing: "topic-led",
} as const;

export const voice = {
  adjectives: ["calm", "expert", "direct", "practical", "slightly serious"],
  /** Hard rules. The quality gate FAILS content that violates these. */
  hardRules: [
    "No exclamation points.",
    "No emoji.",
    "Lead with the concept/topic, not a university name.",
    "A university may appear only as secondary context, never in the headline.",
    "No hype, no hard-sell, no clickbait. Earn attention with the idea.",
  ],
  /** Soft guidance — preferences, not pass/fail. */
  preferences: [
    "Short sentences. One idea per line.",
    "Concrete over abstract — show the number, the journal entry, the formula.",
    "Respect the reader's time and intelligence.",
  ],
  trademark: {
    // Why we stay topic-led. Surfaced to the quality gate.
    rule: "Never headline or imply endorsement by a named university. Secondary context only.",
  },
} as const;

/** Semantic tokens — carried from the app brand system (brand.md § Color palette). */
export const colors = {
  ink: "#020817", // foreground — body text on light (hsl 222 84% 5%)
  paper: "#FFFFFF", // background — light surfaces
  brand: "#467DE3", // primary — edlintics blue (hsl 219 74% 58%). Stays in both modes.
  brandHover: "#3669CC", // primary hover, light mode
  brandHoverDark: "#6494E8", // primary hover, dark mode
  accent: "#60A5FA", // blue-400 — the gradient terminus for headline emphasis
  muted: "#64748B", // secondary text (slate-500)
  border: "#E2E8F0", // borders / dividers, light
  destructive: "#EF4444", // errors
  // Dark mode counterparts (default is light; dark ships with a user toggle):
  inkDark: "#F8FAFC", // foreground on dark
  paperDark: "#020817", // background, dark
  borderDark: "#1E293B", // borders, dark
} as const;

/**
 * Accent palette (app legacy, full range). Hard rule: no more than TWO accents per section.
 * Subject mapping matters for concept content — accounting/money = emerald, programming/data = cyan.
 */
export const accents = {
  sky: "#38BDF8", // clarity / programming
  blue: "#3B82F6", // secondary brand emphasis
  indigo: "#6366F1", // premium / advanced
  violet: "#8B5CF6", // sophistication
  emerald: "#10B981", // money / accounting subjects
  amber: "#F59E0B", // warnings / premium emphasis
  rose: "#F43F5E", // destructive accent
  pink: "#EC4899", // rare highlight
  cyan: "#06B6D4", // programming / data analytics
  green: "#22C55E", // success
  orange: "#F97316", // warning emphasis
  slate: "#64748B", // neutral secondary
} as const;

/**
 * Gradients are a PRIMARY brand element, not decoration (brand.md § Gradients). Use the primary
 * gradient for headline emphasis (it is the brand signature). Keep direction consistent.
 */
export const gradients = {
  primary: { from: "#467DE3", to: "#60A5FA", dir: "to-r" }, // headline emphasis, key H1 spans
  cta: { from: "#467DE3", via: "#3B82F6", to: "#2563EB", dir: "to-br" }, // CTA panels / buttons
  hero: { from: "#EFF6FF", via: "#FFFFFF", to: "#FFFFFF", dir: "to-b" }, // section backgrounds
} as const;

/**
 * Type system (brand.md § Typography). Inter for UI/marketing chrome + short headlines;
 * Source Serif Pro for long-form / editorial "expertise" surfaces; Lato for uppercase kickers,
 * prices and tabular figures. No italics for emphasis — bold or color instead.
 */
export const type = {
  display: "Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif", // headlines, UI chrome
  body: "Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif", // marketing/UI body
  serif: "'Source Serif Pro', Georgia, 'Times New Roman', serif", // long-form / editorial
  // Lato replaced Geist Mono in June 2026 — the brand dropped its monospace face.
  accent: "Lato, system-ui, sans-serif", // uppercase kickers, prices, tabular figures
  // Headline weight signature: extrabold (800), tracking-tight.
  displayWeight: 800,
} as const;

export const assets = {
  // The logo is a wordmark + the collar-and-tie BrandMark; both are vector geometry rendered
  // from tokens, not a stored logo.svg. Geometry mirrored in scripts/build_social_assets.py.
  // The app icon is a WHITE tie on the blue gradient. Social avatars are the inverse — the blue
  // gradient mark on white — so the profile picture reads as the logo. Built by the script below.
  appIcon: "assets/brand/app-icon-512.png",
  favicon: "assets/brand/favicon.svg",
  // EdCharacter cast, vendored 2026-08-03 from tutoring-web/public/mascot.
  characters: {
    ledger: "assets/brand/ledger.svg", // lead character
    ledgerStuck: "assets/brand/ledger-stuck.svg",
    sigma: "assets/brand/sigma.svg",
    centi: "assets/brand/centi.svg",
    plot: "assets/brand/plot.svg",
    tempo: "assets/brand/tempo.svg",
  },
  socialRenders: "assets/renders/social/", // built by scripts/build_social_assets.py
  fonts: "assets/fonts/", // Latin-subset woff2 for hermetic rendering
  // See assets/brand/README.md for the full manifest + usage rules.
} as const;

/**
 * Logo. RESOLVED — the redesign landed upstream as brand v1.2: a wordmark plus the collar-and-tie
 * BrandMark. Reconciled 2026-08-03 from `tutoring-web/docs/product/brand.md` § Logo and
 * `components/brand/BrandMark.tsx`. Both are drawn from geometry, so they stay crisp at any size.
 */
export const logo = {
  status: "current", // was pending-redesign until 2026-08-03
  wordmark: { ed: "Ed", lintics: "lintics" },
  treatment: "Ed in foreground; 'lintics' in the primary gradient (to-r, from #467DE3 to #60A5FA).",
  font: "Inter",
  weight: 800,
  tagline: null, // no tagline under the wordmark, ever
  /** The mark: a necktie framed by a collar. The cast wears it, so logo and characters rhyme. */
  mark: {
    viewBox: "0 0 64 92",
    variants: ["full", "tie"], // full = collar + tie; tie = smallest contexts (favicon, avatar)
    gradient: { from: "#6FA0F0", to: "#2F58A8", dir: "to-br" }, // never recolor
    clearSpace: "padding equal to the height of the 'E'",
  },
} as const;

/**
 * Character system (mascot) — a SCOPED EXCEPTION, not a general marketing asset.
 * Reconciled 2026-08-03 from `tutoring-web/docs/product/brand.md` § "Character system".
 *
 * The Castor beaver was RETIRED upstream on 2026-06-07 (brand v1.2) and replaced by the
 * EdCharacter object cast. v1.3 (2026-06-29) removed the suit + tie from every character
 * except Ledger, which wears the mark printed on the lower half of its book.
 *
 * The default is still mascot-free on marketing and content. The cast is an ILLUSTRATIVE
 * asset, never an icon, never given a voice. Each marketing use needs an explicit,
 * logged sign-off from Hoang — see `approvedMarketingExceptions`.
 */
export const characterSystem = {
  cast: ["Ledger", "Sigma", "Centi", "Plot", "Tempo"] as const,
  lead: "Ledger", // the manual; the character used when only one is needed
  retired: "Castor (beaver) — removed upstream 2026-06-07, do not reintroduce",
  emotions: ["idle", "cheerful", "focused", "thinking", "proud", "surprised", "stuck", "resting"],
  allowedAppSurfaces: ["404", "error", "empty-state", "onboarding", "loading"],
  /** Default remains: NOT in marketing. Each exception below is individually approved. */
  forbiddenInMarketingByDefault: true,
  approvedMarketingExceptions: [
    {
      date: "2026-10-23",
      surface: "\"5 [category] concepts you should know\" carousels (Canva proposal DAHY0JdFOLM): Ledger walks a dotted path across the slides",
      characters: ["Ledger"],
      rationale: "Hoang asked for Ledger to walk through each slide (traveling-icon carousel). Decorative only, no voice. Walking art: Canva media MAHY0KC6fFo.",
      status: "APPROVED for preparation and design use; the template awaits Hoang's approval, and publishing each post still requires approval.",
    },
    {
      date: "2026-10-23",
      surface: "meme comic social posts (Canva template proposal DAHYz_I2pNE): finance, accounting, economics, statistics",
      characters: ["Ledger"],
      rationale:
        "Hoang: 'We will use ledger in different clothes to reflect' the roles. Ledger plays every role " +
        "(tutor, student, manager...) told apart by clothes, and its lines appear as comic dialogue. " +
        "This overrides `voice` and `decorativeOnly` for this surface only. Panel art is generated per " +
        "post from the Ledger reference (Canva media MAHYzySXLrM); the printed tie stays visible and unrecolored.",
      status: "APPROVED for preparation and design use; the template itself awaits Hoang's approval, and publishing each post still requires approval.",
    },
    {
      date: "2026-10-19",
      surface: "economics, finance, accounting, and statistics quiz social posts in Canva templates",
      characters: ["Ledger", "Sigma", "Centi", "Plot", "Tempo"],
      rationale:
        "Hoang explicitly requested EdCharacter and existing graphics for quiz images, " +
        "and asked an additional agent to add the mascots. Preserve the existing character art.",
      status: "APPROVED for preparation and design use; publishing each post still requires approval.",
    },
    {
      date: "2026-08-03",
      surface: "social profile covers + Instagram pinned grid (Facebook, LinkedIn, Instagram)",
      characters: ["Ledger", "Centi", "Plot", "Sigma"],
      rationale:
        "Rebrand rollout. Matches the homepage OG card (public/og/default.png), which already " +
        "pairs the cast with accounting graphics on a marketing surface.",
      status: "PENDING — requested by Hoang in-session; confirm before the assets go live.",
    },
  ],
  voice: "none — the cast never talks, jokes, or cheers; copy stays in the real brand voice",
  decorativeOnly: true, // always aria-hidden / empty alt; meaning lives in surrounding copy
  tieRule: "the tie is on Ledger only, printed on the book; never recolored",
} as const;

export const brand = {
  audience,
  voice,
  colors,
  accents,
  gradients,
  type,
  assets,
  logo,
  characterSystem,
} as const;
export type Brand = typeof brand;
export default brand;
