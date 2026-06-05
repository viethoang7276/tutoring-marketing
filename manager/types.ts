/**
 * Schemas for everything the Manager reads and writes.
 *
 * Two groups:
 *   1. Briefing source data — the shapes we read from /api/v1 (or fixtures). These encode our
 *      ASSUMED endpoint shapes; reconcile with the app when the read token lands (spec 0001).
 *   2. Calendar — the system of record the Manager writes decisions into.
 */
import { z } from "zod";

/* ----------------------------- briefing source data ----------------------------- */

export const FunnelStage = z.object({
  name: z.string(), // e.g. "catalog view", "course view", "enrol"
  count: z.number().int().nonnegative(),
});

export const Funnel = z.object({
  period: z.string(), // human label, e.g. "last 28 days"
  stages: z.array(FunnelStage).min(2),
});
export type Funnel = z.infer<typeof Funnel>;

export const PostStat = z.object({
  id: z.string(),
  date: z.string(), // ISO date
  channel: z.string(), // instagram | linkedin | tiktok | blog | newsletter
  format: z.string(), // short | carousel | hero | post | email
  title: z.string(),
  impressions: z.number().int().nonnegative(),
  engagementRate: z.number().nonnegative(), // 0..1
  saves: z.number().int().nonnegative(),
  clicks: z.number().int().nonnegative(),
});
export type PostStat = z.infer<typeof PostStat>;

/** Onboarding "wanted it, didn't enrol" — first-party demand gaps. */
export const DemandGap = z.object({
  topic: z.string(),
  count: z.number().int().nonnegative(), // people who wanted it
  note: z.string().optional(),
});
export type DemandGap = z.infer<typeof DemandGap>;

export const FeedbackTheme = z.object({
  question: z.string(),
  themes: z.array(
    z.object({
      theme: z.string(),
      count: z.number().int().nonnegative(),
      sampleQuote: z.string().optional(),
    }),
  ),
});
export type FeedbackTheme = z.infer<typeof FeedbackTheme>;

/* --------------------------------- calendar --------------------------------- */

export const Pillar = z.object({
  id: z.string(),
  name: z.string(),
  description: z.string(),
  rationale: z.string(), // why this pillar, grounded in data
});
export type Pillar = z.infer<typeof Pillar>;

export const Campaign = z.object({
  id: z.string(),
  name: z.string(),
  angle: z.string(),
  status: z.enum(["planned", "active", "done"]),
  start: z.string().optional(), // ISO date
  end: z.string().optional(),
  pillarIds: z.array(z.string()).default([]),
});
export type Campaign = z.infer<typeof Campaign>;

export const FilmingItem = z.object({
  id: z.string(),
  concept: z.string(), // what to talk through on camera
  pillarId: z.string().optional(),
  priority: z.enum(["high", "medium", "low"]).default("medium"),
  notes: z.string().optional(),
});
export type FilmingItem = z.infer<typeof FilmingItem>;

export const ContentItem = z.object({
  id: z.string(),
  date: z.string().optional(), // ISO date; absent = unscheduled idea
  channel: z.string().optional(),
  format: z.string().optional(),
  status: z.enum(["idea", "scheduled", "published"]).default("idea"),
  pillarId: z.string().optional(),
  campaignId: z.string().optional(),
  title: z.string(),
  notes: z.string().optional(),
});
export type ContentItem = z.infer<typeof ContentItem>;

export const Decision = z.object({
  date: z.string(), // ISO date the decision was locked
  summary: z.string(),
  rationale: z.string(),
});
export type Decision = z.infer<typeof Decision>;

export const Calendar = z.object({
  period: z.object({
    label: z.string(),
    start: z.string().optional(),
    end: z.string().optional(),
  }),
  pillars: z.array(Pillar).default([]),
  campaigns: z.array(Campaign).default([]),
  filmingQueue: z.array(FilmingItem).default([]),
  items: z.array(ContentItem).default([]),
  decisions: z.array(Decision).default([]),
});
export type Calendar = z.infer<typeof Calendar>;
