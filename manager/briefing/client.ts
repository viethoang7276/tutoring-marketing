/**
 * Edlintics data client. One switch: with a token it hits /api/v1; without one it reads fixtures.
 * Call sites never change — `npm run brief` works identically before and after the token lands.
 */
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { z } from "zod";
import { env } from "../env.ts";
import { Funnel, PostStat, DemandGap, FeedbackTheme } from "../types.ts";

const fixturesDir = join(env.repoRoot, "manager", "briefing", "fixtures");

function readFixture<T>(name: string, schema: z.ZodType<T>): T {
  const raw = JSON.parse(readFileSync(join(fixturesDir, name), "utf8"));
  return schema.parse(raw);
}

async function fetchLive<T>(path: string, schema: z.ZodType<T>): Promise<T> {
  const res = await fetch(`${env.apiBase}${path}`, {
    headers: { authorization: `Bearer ${env.apiToken}`, accept: "application/json" },
  });
  if (!res.ok) {
    throw new Error(`GET ${path} -> ${res.status} ${res.statusText}`);
  }
  return schema.parse(await res.json());
}

/**
 * Each getter maps to one assumed /api/v1 endpoint. The fixture filename mirrors the path so the
 * mapping is obvious when we reconcile shapes with the app side.
 */
async function get<T>(path: string, fixture: string, schema: z.ZodType<T>): Promise<T> {
  return env.useFixtures ? readFixture(fixture, schema) : fetchLive(path, schema);
}

export const client = {
  source: env.useFixtures ? ("fixtures" as const) : ("live" as const),

  /** Funnel: catalog view -> course view -> enrol (PostHog-backed). */
  getFunnel: () => get("/marketing/funnel", "funnel.json", Funnel),

  /** Per-post platform stats for published content. */
  getPlatformStats: () =>
    get("/marketing/platform-stats", "platform-stats.json", z.array(PostStat)),

  /** Onboarding "wanted it, didn't enrol" demand gaps. */
  getDemandGaps: () => get("/marketing/demand-gaps", "demand-gaps.json", z.array(DemandGap)),

  /** Survey / feedback campaign answers, themed. */
  getFeedback: () => get("/marketing/feedback", "feedback.json", z.array(FeedbackTheme)),
};
