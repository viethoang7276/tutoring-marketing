/**
 * The content calendar — the system of record for Tier 1 decisions.
 *
 * Stored as `calendar/calendar.json`, validated by the Calendar schema on every read so a
 * hand-edit that breaks shape fails loudly. `npm run calendar` renders it as markdown.
 *
 * The Manager updates the calendar by editing the JSON (or via `load`/`save` here) and appending
 * a decision entry — decisions are the append-only audit trail of the strategy loop.
 */
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { env } from "./env.ts";
import { Calendar } from "./types.ts";
import type { Calendar as CalendarT, Decision } from "./types.ts";

const calendarPath = join(env.repoRoot, "calendar", "calendar.json");

export function load(): CalendarT {
  return Calendar.parse(JSON.parse(readFileSync(calendarPath, "utf8")));
}

export function save(cal: CalendarT): void {
  const validated = Calendar.parse(cal);
  writeFileSync(calendarPath, JSON.stringify(validated, null, 2) + "\n", "utf8");
}

/** Convenience for the Manager: append a locked decision (kept in date order). */
export function recordDecision(cal: CalendarT, decision: Decision): CalendarT {
  return { ...cal, decisions: [...cal.decisions, decision].sort((a, b) => a.date.localeCompare(b.date)) };
}

export function render(cal: CalendarT): string {
  const lines: string[] = [`# Content calendar — ${cal.period.label}`];
  if (cal.period.start || cal.period.end) {
    lines.push(`_${cal.period.start ?? "?"} → ${cal.period.end ?? "?"}_`);
  }

  lines.push(``, `## Pillars`);
  if (cal.pillars.length === 0) lines.push(`_none yet_`);
  for (const p of cal.pillars) {
    lines.push(`- **${p.name}** (\`${p.id}\`) — ${p.description}`, `  - _why:_ ${p.rationale}`);
  }

  lines.push(``, `## Campaigns`);
  if (cal.campaigns.length === 0) lines.push(`_none yet_`);
  for (const c of cal.campaigns) {
    const dates = c.start || c.end ? ` [${c.start ?? "?"} → ${c.end ?? "?"}]` : "";
    lines.push(`- **${c.name}** (\`${c.id}\`) · ${c.status}${dates} — angle: ${c.angle}`);
  }

  lines.push(``, `## Filming queue`);
  if (cal.filmingQueue.length === 0) lines.push(`_none yet_`);
  for (const f of [...cal.filmingQueue].sort((a, b) => order(a.priority) - order(b.priority))) {
    lines.push(`- [${f.priority}] ${f.concept}${f.notes ? ` — ${f.notes}` : ""}`);
  }

  lines.push(``, `## Content items`);
  if (cal.items.length === 0) lines.push(`_none yet_`);
  for (const it of [...cal.items].sort(byDate)) {
    const when = it.date ?? "unscheduled";
    const where = [it.channel, it.format].filter(Boolean).join("/");
    lines.push(`- ${when} · ${it.status}${where ? ` · ${where}` : ""} — ${it.title}`);
  }

  lines.push(``, `## Decisions (audit trail)`);
  if (cal.decisions.length === 0) lines.push(`_none yet_`);
  for (const d of cal.decisions) {
    lines.push(`- **${d.date}** — ${d.summary}`, `  - _why:_ ${d.rationale}`);
  }

  return lines.join("\n") + "\n";
}

const order = (p: "high" | "medium" | "low") => ({ high: 0, medium: 1, low: 2 })[p];
function byDate(a: { date?: string }, b: { date?: string }): number {
  if (!a.date) return 1;
  if (!b.date) return -1;
  return a.date.localeCompare(b.date);
}

// CLI: print the current calendar as markdown.
if (import.meta.url === `file://${process.argv[1]}`) {
  try {
    process.stdout.write(render(load()));
  } catch (err) {
    console.error("calendar failed:", err instanceof Error ? err.message : err);
    process.exit(1);
  }
}
