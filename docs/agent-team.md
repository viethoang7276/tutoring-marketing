# The marketing agent team

The role-agent roster for this repo, defined in `.claude/agents/` — the marketing counterpart to the
engineering roster (`../tutoring-web/.claude/agents/`) and the content roster
(`../tutoring-content/.claude/agents/`). The CMO (the lead session) spawns these roles per task; they
report back in a fixed board-style block. The brand constitution (calm/expert voice, no exclamation
points, no emoji, topic-led never university-led, trademark independence, mascot ban, human gate) is
written into every role file, not just the reviewer's.

## Roster

| Role | Lane (owns) | Artifacts | Mode |
|---|---|---|---|
| `market-researcher` | External research | `docs/research/YYYY-MM-DD-*.md` | writes its lane only |
| `copywriter` | Written pillar content | `assets/copy/<topic>/` (scripts, titles, captions + hashtag stacks, carousels, blog, newsletter) | writes its lane only |
| `asset-designer` | Visuals | `assets/renders/`, templates/specs under `assets/`; Canva + Higgsfield tooling | writes its lane only |
| `distribution-operator` | Scheduling + publish mechanics | publish slots in `calendar/calendar.json` (validated with `npm run calendar`), `publish.md` packages, channel/SEO checklists, scheduler evaluation | stages everything, posts nothing |
| `performance-analyst` | Data + reporting | `docs/reports/` drafts + charts + index; `npm run brief` interpretation | drafts; CMO signs |
| `brand-reviewer` | Quality gate | review findings only | **read-only** |

Shared boundaries: nobody writes a sibling repo; nobody publishes; nobody locks a strategy decision —
Hoang's gate is absolute. Calendar *strategy* fields (pillars, campaigns, filming queue, the
`decisions` log) remain CMO + Hoang territory from the strategy session.

## When the CMO spawns whom (mapped to the two loops)

**Tier 1 — strategy loop (weekly / on-demand CMO cycle, `docs/cmo-cycle.md`):**

- Step 1 *Scan* → `market-researcher` (trend scan, seasonality, competitor/hashtag work).
- Step 2 *Listen* → `performance-analyst` (run + interpret `npm run brief`, fixtures vs live labeled).
- Steps 3–4 *Decide / Emit* → the CMO itself, arguing with Hoang; no sub-agent locks anything.
- Step 5 *Report* → `performance-analyst` drafts the weekly report; `brand-reviewer` passes it;
  the CMO signs and delivers.

**Tier 2 — production loop (daily, per calendar item):**

- `copywriter` → scripts and the written atomize outputs for the next filming-queue topic.
- `asset-designer` → thumbnails, covers, carousel visuals, templates for the same item.
- `distribution-operator` → packages the approved item per channel, fills the publish slots,
  preps the five-minute approval drop.
- `brand-reviewer` → gates every package **before** it reaches Hoang's approval (a HIGH finding
  blocks; the owning role fixes and resubmits).

A typical production chain: copywriter → asset-designer (parallel where independent) →
distribution-operator → brand-reviewer → Hoang.

## Root-session fallback

When working from the company root (or any directory where this repo's `.claude/agents/` is not
auto-discovered), spawn a **general-purpose sub-agent** and paste the relevant role file
(`edlintics-marketing/.claude/agents/<role>.md`) into its brief as the system instructions, including
the lane boundaries and the board-style report block. The role files are written to be self-contained
for exactly this use.
