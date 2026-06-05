/**
 * Turns raw Edlintics data into the three data-grounded sections of the strategy briefing.
 * Pure formatting — no fetching, no LLM. The Manager (the Claude session) reads the output and
 * adds the live trend scan + proposals on top (those are judgement, not script output).
 */
import type { Funnel, PostStat, DemandGap, FeedbackTheme } from "../types.ts";

const pct = (n: number) => `${(n * 100).toFixed(1)}%`;
const num = (n: number) => n.toLocaleString("en-US");

/** Section 1 — Performance digest: funnel + what landed on platform. */
export function performanceDigest(funnel: Funnel, posts: PostStat[]): string {
  const lines: string[] = [`## 1. Performance digest`, ``, `**Funnel — ${funnel.period}**`, ``];

  funnel.stages.forEach((stage, i) => {
    const prev = funnel.stages[i - 1];
    const step = prev ? `  ·  ${pct(stage.count / prev.count)} of previous` : "";
    lines.push(`- ${stage.name}: **${num(stage.count)}**${step}`);
  });
  const first = funnel.stages[0];
  const last = funnel.stages[funnel.stages.length - 1];
  if (first && last && first.count > 0) {
    lines.push(``, `Overall ${first.name} → ${last.name}: **${pct(last.count / first.count)}**`);
  }

  const byEngagement = [...posts].sort((a, b) => b.engagementRate - a.engagementRate);
  const top = byEngagement.slice(0, 3);
  const bottom = byEngagement.slice(-2).reverse();
  const saveRate = (p: PostStat) => (p.impressions ? p.saves / p.impressions : 0);

  lines.push(``, `**What landed** (top by engagement)`, ``);
  for (const p of top) {
    lines.push(
      `- [${p.channel}/${p.format}] "${p.title}" — ${pct(p.engagementRate)} eng, ` +
        `${num(p.saves)} saves (${pct(saveRate(p))} save rate), ${num(p.impressions)} impr`,
    );
  }
  lines.push(``, `**What underperformed**`, ``);
  for (const p of bottom) {
    lines.push(`- [${p.channel}/${p.format}] "${p.title}" — ${pct(p.engagementRate)} eng`);
  }

  // A cheap signal worth surfacing: high save rate = "I want to come back to this" = course intent.
  const bestSaver = [...posts].sort((a, b) => saveRate(b) - saveRate(a))[0];
  if (bestSaver) {
    lines.push(
      ``,
      `> Save rate is the closest free proxy for course intent. Strongest saver: ` +
        `"${bestSaver.title}" (${pct(saveRate(bestSaver))}).`,
    );
  }
  return lines.join("\n");
}

/** Section 2 — First-party signal: demand gaps + feedback themes. Your data, not generic. */
export function firstPartySignal(gaps: DemandGap[], feedback: FeedbackTheme[]): string {
  const lines: string[] = [`## 2. First-party signal`, ``, `**Wanted it, didn't enrol** (onboarding)`, ``];
  for (const g of [...gaps].sort((a, b) => b.count - a.count)) {
    lines.push(`- **${g.topic}** — ${num(g.count)} wanted it${g.note ? ` · ${g.note}` : ""}`);
  }
  lines.push(``, `**Feedback themes**`, ``);
  for (const f of feedback) {
    lines.push(`*${f.question}*`);
    for (const t of [...f.themes].sort((a, b) => b.count - a.count)) {
      const quote = t.sampleQuote ? ` — "${t.sampleQuote}"` : "";
      lines.push(`- ${t.theme} (${num(t.count)})${quote}`);
    }
    lines.push(``);
  }
  return lines.join("\n").trimEnd();
}

/** Section 3 — Trend scan: a stub the Manager fills live (WebSearch + seasonality). */
export function trendScanStub(): string {
  return [
    `## 3. Trend scan  _(fill live)_`,
    ``,
    `Not script-generated. As the Manager, fill this in-session:`,
    `- What finance/accounting students are worried about right now (WebSearch).`,
    `- Seasonality: where are we relative to exam periods? What's 4-6 weeks out?`,
    `- Format trends worth riding (and which to ignore as off-voice).`,
  ].join("\n");
}

/** Section 4 — Proposals: prompt for the Manager's own synthesis. Not script output. */
export function proposalsPrompt(): string {
  return [
    `## 4. Proposals  _(Manager synthesizes — 2-3 directions)_`,
    ``,
    `Cross the data above with the trend scan. Each proposal: a content pillar or campaign, the`,
    `angle, the evidence it rests on, and what to film. Bring 2-3. Then argue them out with Hoang;`,
    `he brings domain judgement, you bring the data. Write locked decisions to the calendar.`,
  ].join("\n");
}
