/**
 * `npm run brief` — assembles the strategy-session briefing and prints it as markdown.
 *
 * This is the Manager's prepared-arrival document: three data-grounded sections from Edlintics
 * data (fixtures until the read token lands), plus stubs for the live trend scan + proposals the
 * Manager fills in chat. Read it at the top of a strategy session (see session-start.md).
 */
import { client } from "./client.ts";
import {
  performanceDigest,
  firstPartySignal,
  trendScanStub,
  proposalsPrompt,
} from "./digest.ts";

async function main(): Promise<void> {
  const [funnel, posts, gaps, feedback] = await Promise.all([
    client.getFunnel(),
    client.getPlatformStats(),
    client.getDemandGaps(),
    client.getFeedback(),
  ]);

  const today = new Date().toISOString().slice(0, 10);
  const out = [
    `# Strategy briefing — ${today}`,
    ``,
    `_Audience: finance & accounting university students. Voice: calm, expert, direct — no exclamation points, no emoji._`,
    `_Data source: **${client.source}**${client.source === "fixtures" ? " (no read token set — using local fixtures)" : ""}._`,
    ``,
    `---`,
    ``,
    performanceDigest(funnel, posts),
    ``,
    `---`,
    ``,
    firstPartySignal(gaps, feedback),
    ``,
    `---`,
    ``,
    trendScanStub(),
    ``,
    `---`,
    ``,
    proposalsPrompt(),
    ``,
  ].join("\n");

  process.stdout.write(out);
}

main().catch((err) => {
  console.error("brief failed:", err instanceof Error ? err.message : err);
  process.exit(1);
});
