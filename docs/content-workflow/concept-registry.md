# Concept registry

> Added 1 Nov 2026. The registry exists so that no research or planning run proposes a concept we have already covered. Hoang noticed repeats: diminishing marginal utility (31 Oct life-of reel) and diminishing returns (1 Nov definition reel) teach the same "each extra unit adds less" idea one day apart, AI and skills ran 4 times in 8 days, and working capital ran on 24 Oct and 30 Oct. Until now the only repetition check was the puzzle rule "no reasoning trap repeats within 4 weeks". The registry covers every format.

## Where it lives

- **Hub collection `concepts`** in the hub database (artifact `865d31cf-0322-4c58-a37e-21ab240a1e4d`, the same database as `slots`). This is the system of record.
- **Repo mirror** `docs/content-workflow/concept-registry.json`, sorted by `lastUsed`, newest first. It holds only term, aliases, related, themes and uses (slotId, date, format), so it is safe for the public repo. Refresh it whenever the hub collection changes a lot. When the two disagree, the hub wins.

## One doc per canonical concept

The doc id is a kebab slug of the canonical term, for example `diminishing-returns` or `net-present-value`.

| Field | What it holds |
|---|---|
| `term` | The canonical name, for example "Diminishing returns" |
| `aliases` | Lowercase variants to match against, for example "law of diminishing returns", "diminishing marginal productivity" |
| `family` | One of the eight research families: economics, accounting, finance, statistics, econometrics, operations, management, marketing (plus workplace for spreadsheet and office concepts) |
| `themes` | Short kebab theme tags, for example `ai-and-skills`, `time-value-of-money`, `cognitive-bias`, `labor-market` |
| `related` | Slugs of near-duplicates, for example `diminishing-returns` and `diminishing-marginal-utility` list each other |
| `uses` | One entry per post: `{slotId, format, date, role, status}`. `role` is `main` (the post is about this concept) or `supporting` (one term of five, a key term on a definition carousel, a side point) |
| `firstUsed`, `lastUsed` | Dates of the first and latest use, `YYYY-MM-DD` |

A puzzle reel (`parentSlot`) is not a second post. Its use is logged under its parent puzzle. Rejected and deleted posts are not logged.

## The rules (proposed 1 Nov 2026; Hoang can change them)

1. **Same concept as the main idea: blocked for 90 days in any format.** A definition reel, a puzzle and a comic on the same concept count as repeats. Exception: a five-concepts or This vs That post may reuse a concept as a *supporting* term after 30 days.
2. **A `related` concept as the main idea: blocked for 30 days** (Hoang, 1 Nov 2026: "no potential repetition within a month"; was 14 days). The same industry in the industry series is also blocked for 30 days. Diminishing returns one day after diminishing marginal utility is the example.
3. **One theme: at most 2 posts in any 7 days**, for example `ai-and-skills`. Count main uses only.
4. **Holiday or news hooks** may reuse an old concept only when the angle is new and the old post is more than 30 days old. Log it as an exception: put `exception: "holiday"` or `exception: "news"` and a one-line reason on the use entry.
5. **Paired posts are one use.** Step 6 of the Thursday run has concept carousels explain a concept behind that week's puzzles. A carousel that explains a puzzle from the same week (slot field `explainsPuzzle`) is paired with it and does not break rules 1 to 3 against that puzzle. Log both uses and add `pairedWith: <slotId>` to the carousel's use. Pairing is one carousel per puzzle, not a third post.
6. **Planned posts count.** Uses with status `proposal`, `approved` or `scheduled` block the same windows as posted ones, measured from their planned date in both directions.

## The checks

- **Every proposal names its concepts.** A Thursday plan post, a request, a replacement or a test post lists its main concept slug and its themes in the slot (`concept`, `themes`).
- **Query before proposing.** The researcher or planner reads `concepts` before proposing and writes one line in the proposal: "registry check: clear", or the conflict, for example "registry check: conflict, diminishing-returns used as main on 2026-11-01 (reel-2026-11-01-1800)".
- **Log the use.** When a post is approved or scheduled, add its `uses` entry and update `lastUsed` (and `firstUsed` for a new concept). When a post is rejected or deleted, remove its entry.
- **New concept or alias?** Before creating a doc, search the `aliases` of existing docs. If the idea is the same under another name, add the alias instead of a new doc. If it is a close cousin, create the doc and link both ways in `related`.

## How to query it

With the hub db tools (`mcp__claude-artifacts__db_*`, load them with ToolSearch first):

- **One concept:** `db_get` path `concepts/<slug>`.
- **Recently used:** `db_query` on `concepts`, `orderBy: {field: "lastUsed", direction: "desc"}`, `limit: 100`. Everything with `lastUsed` in the last 90 days is a candidate conflict.
- **A theme:** `db_query` on `concepts` with `where: [{field: "themes", op: "array-contains", value: "ai-and-skills"}]`, then count the main uses in the last 7 days.
- **By name:** there is no text search. Match the candidate term against `term` and `aliases` in the recently-used list, or read the repo mirror.

Offline, the same check runs on the mirror, for example:

```
jq -r '.[] | select(.aliases | index("law of diminishing returns")) | .term' docs/content-workflow/concept-registry.json
```

## New concepts go to the site (Hoang, 2 Nov 2026)

Every new concept also appears on edlintics.com.

- **A business term** goes to the glossary.
  - When a concept is added here, send the tutoring-content (COO) session one row:
    - term_text;
    - the definition reviewed with 2+ sources;
    - equation and example;
    - the YouTube reel URL, if any.
  - The COO decides between a new term, attaching the reel to an existing term, or a flag. The glossary wording wins. The meaning and the equation must match.
- **Not a term** (a process or a story, such as a how-to topic): marketing prepares a blog post draft in the format tutoring-web gives.
- Reel placement on term pages:
  - the definition reel is the primary reel;
  - the how-to reel is a secondary "see it applied" reel;
  - list reels go on topic pages later;
  - puzzle reels are never shown, so they can't give away practice answers.
- Drafts only. Hoang approves before anything is published.

### Hand-off format (agreed with the COO, 2 Nov 2026)

**Batching**
- One CSV per batch, weekly, or at 10 rows if that comes sooner.
- Path: `assets/renders/glossary/new-concepts-YYYY-MM-DD.csv`.
- Send it after the Thursday plan is approved.
- This file is separate from the reel CSV.

**Format:** UTF-8, one row per concept. Columns:
- hub_concept_id
- term_text
- aliases (separated by |)
- kind: term, process or story
- definition_reviewed (verbatim)
- source_urls (2 or more, separated by |)
- equation
- variables (symbol=meaning, separated by |)
- example (with its numbers)
- framework
- topic
- related_terms (separated by |)
- reel_url, reel_type, duration_s (blank if there is no reel)

**Who handles which rows**
- The COO takes only `term` rows. Marketing writes blog drafts for `process` and `story` rows.

**What the COO does**
- Writes the glossary entry in its own wording, with a hero infographic and a practice MCQ.
- Sends back four lists: new, attach, flag and not-a-term.
- Holds reel attachments until tutoring-web ships the structured reel field.


### Blog drafts for non-term concepts (format from tutoring-web, 2 Nov 2026)

**Where and how to write it**
- One Markdown file per post: `assets/renders/blog/<slug>.md`.
- Frontmatter:
  - `slug`
  - `title`
  - `excerpt` (required, at most 1000 characters)
  - `tags` (existing tag names only; unknown ones are dropped)
  - optional: `seoTitle` (≤200), `seoDescription` (≤500), `authorLabel`
- Leave the cover and OG images empty. They're attached in the admin.
- Quote (with double quotes) any title, excerpt, seoTitle or seoDescription value that contains ": " or starts with a quote, #, & or *.

**Body rules**
- At least about 300 characters of readable text.
- At least one tag.
- No affiliation or banned claims.
- No trailing full stops, no emoji, minimal copy.
- Put a reel's Short URL on its own line as a plain link. The Markdown importer doesn't make video blocks yet; the glossary-reels spec adds Shorts support.

**Who does what**
- Marketing does not run edctl. Marketing only reads the app through its public API.
- tutoring-web imports the files with `edctl blog import` (dev first) and runs `edctl blog validate`.
- Hoang publishes.

**Blog tags (live list, 2 Nov 2026):** Accounting, Cash flow, Cost accounting, Costing, Data analysis, Finance, Financial accounting, Financial statements, Managerial accounting, Pricing, Small business, Spreadsheets, Valuation, Working capital.
- Use only these in the frontmatter.
- If a post needs a new tag, name it as a "proposed tag" in the message to tutoring-web, not in the file. They'll take it to Hoang.
