/**
 * Brand tokens — the single source of truth for how Edlintics marketing looks and sounds.
 *
 * Consumed by:
 *   - Tier 1 Manager     — keeps proposals/copy on-voice.
 *   - Tier 2 quality gate — voice + trademark check before anything publishes.
 *   - Remotion templates  — colors/type for animated concept graphics.
 *
 * Colors/type mirror the app brand system. Upstream sources (read, never imported):
 *   - tutoring-web/docs/brand.md            — the rules + reasoning
 *   - http://localhost:3000/en/brand-guidelines — the rendered truth (canonical when in doubt)
 * Values below are LITERAL copies (this repo never imports app code). When the app brand
 * changes, update these by hand. Reconciled 2026-06-05 from brand.md.
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
 * Source Serif Pro for long-form / editorial "expertise" surfaces; Geist Mono for code and
 * tabular figures (price ladders, T-accounts). No italics for emphasis — bold or color instead.
 */
export const type = {
  display: "Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif", // headlines, UI chrome
  body: "Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif", // marketing/UI body
  serif: "'Source Serif Pro', Georgia, 'Times New Roman', serif", // long-form / editorial
  mono: "'Geist Mono', ui-monospace, 'SF Mono', Menlo, monospace", // code, formulas, figures
  // Headline weight signature: extrabold (800), tracking-tight.
  displayWeight: 800,
} as const;

export const assets = {
  logo: "assets/brand/logo.svg", // PENDING REDESIGN — current app logo is a gradient wordmark (below)
  // Castor mascot poses, vendored from tutoring-web/public/castor. Monochrome edlintics blue.
  mascot: "assets/brand/mascot.svg", // = the "mark" pose (default)
  mascotPoses: {
    mark: "assets/brand/mascot-mark.svg",
    wave: "assets/brand/mascot-wave.svg",
    read: "assets/brand/mascot-read.svg",
    shrug: "assets/brand/mascot-shrug.svg",
    loading: "assets/brand/mascot-loading.svg",
  },
  favicon: "assets/brand/favicon.svg",
  // See assets/brand/README.md for the full manifest + usage rules.
} as const;

/**
 * Logo (brand.md § Logo). PENDING REDESIGN per Hoang. The app's current logo is a wordmark with
 * gradient text — "Ed" in foreground + "lintics" in the primary→blue-400 gradient, Inter 800,
 * tracking-tight. No tagline. Recorded here so Tier 2 stays consistent until the redesign lands.
 */
export const logo = {
  status: "pending-redesign",
  wordmark: { ed: "Ed", lintics: "lintics" },
  treatment: "Ed in foreground; 'lintics' in the primary gradient (to-r, from #467DE3 to #60A5FA).",
  font: "Inter",
  weight: 800,
  tagline: null,
} as const;

/**
 * Castor mascot policy — a SCOPED EXCEPTION, not a marketing asset (brand.md § Castor).
 * The brand is deliberately mascot-free on marketing and content. Castor is an illustrative
 * beaver in monochrome edlintics blue, never an icon, never given a voice.
 *
 * For THIS engine, the operative rule is: DO NOT put Castor in produced marketing content
 * (hero/landing/concept videos/thumbnails/captions). It exists in assets/ for completeness and
 * for any app-side error/empty/loading surfaces only. The Tier 2 quality gate should treat
 * Castor appearing in a marketing render as a violation.
 */
export const mascotPolicy = {
  name: "Castor",
  color: "monochrome edlintics blue (#467DE3) — never recolor",
  allowedSurfaces: ["404", "error", "empty-state", "onboarding", "loading"],
  forbiddenInMarketing: true, // hero, course landing, lesson/finance content, anything with a "voice"
  voice: "none — Castor never talks, jokes, or cheers; copy stays in the real brand voice",
  decorativeOnly: true, // always aria-hidden / empty alt; meaning lives in surrounding copy
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
  mascotPolicy,
} as const;
export type Brand = typeof brand;
export default brand;
