/**
 * Minimal env loader — reads `.env` from the repo root if present, with zero dependencies.
 * Real shell env always wins over the file. We avoid `dotenv` to keep Tier 1 dependency-light.
 */
import { readFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const repoRoot = join(dirname(fileURLToPath(import.meta.url)), "..");

function loadDotEnv(): void {
  const path = join(repoRoot, ".env");
  if (!existsSync(path)) return;
  for (const raw of readFileSync(path, "utf8").split("\n")) {
    const line = raw.trim();
    if (!line || line.startsWith("#")) continue;
    const eq = line.indexOf("=");
    if (eq === -1) continue;
    const key = line.slice(0, eq).trim();
    const value = line.slice(eq + 1).trim().replace(/^["']|["']$/g, "");
    if (!(key in process.env)) process.env[key] = value;
  }
}

loadDotEnv();

export const env = {
  repoRoot,
  apiBase: process.env.EDLINTICS_API_BASE ?? "http://localhost:3000/api/v1",
  apiToken: process.env.EDLINTICS_API_TOKEN ?? "",
  /** No token => run against local fixtures. Flip to live the moment a token exists. */
  get useFixtures(): boolean {
    return this.apiToken.length === 0;
  },
} as const;
