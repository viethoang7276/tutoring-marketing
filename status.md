# STATUS — living state

The cross-session memory for this repo. Read after `session-start.md`. Update it at the end of any
session that changes state (append to the session log; revise "Now" / "Next").

_Last updated: 2026-10-22_

## Now (what exists and works)

- **Tier 1 slice built** (spec `docs/specs/0001-tier1-manager-calendar.md`):
  - `npm run brief` → data-grounded briefing (performance digest, first-party signal, trend-scan
    stub, proposals prompt). Runs on **fixtures** (no read token yet).
  - `npm run calendar` → renders `calendar/calendar.json` (schema-validated).
  - `npm run typecheck` → passes.
- **Brand layer:** `config/brand.ts` — voice rules + **real** color/accent/gradient/type tokens +
  `docs/brand-guidelines.md`. **Re-reconciled 2026-08-03** to app brand v1.2/v1.3: EdCharacter cast
  (Ledger, Sigma, Centi, Plot, Tempo) vendored into `assets/brand/`, logo RESOLVED (wordmark +
  collar-and-tie mark), Lato replaced Geist Mono. Castor is retired — do not reintroduce.
- **Social profile assets built** — `scripts/build_social_assets.py` renders avatars, the Facebook
  and LinkedIn covers, and three Instagram pinned tiles from real brand geometry, hermetically
  (embedded fonts, no network). Output + upload spec: `assets/renders/social/`.
- **Runtime:** TypeScript / Node 22, zod-validated. Deps: `zod` + dev `tsx`/`typescript`.

## Decisions locked

- 2026-06-05 — Runtime = **TypeScript/Node**. Manager = **Claude Code session + scripts** (this
  file is its operating manual). Data = **mock-first** (fixtures → live by presence of token).
  Brand is a **first-class layer** from day one.

## Next (in rough priority order)

> Launch is **2026-09-01**. The June–Aug plant window that the whole seasonal thesis depends on is
> nearly spent and **nothing has been published**. Everything below is ordered against that.

0. **FILM CF-01.** Fully prepped since June (`calendar/human-plan.md`: hook, numbers, trap, answer).
   Unfilmed. It blocks the auto-clip pipeline test, and therefore the other five takes, and therefore
   the entire lane-A catalogue. Nothing else in this list matters as much.
1. **Hoang's pending confirmations** (all small, all blocking something):
   (a) the mascot-in-marketing exception for the social profiles — logged **PENDING** in
   `config/brand.ts` `characterSystem.approvedMarketingExceptions`;
   (b) Instagram has no cover slot → three pinned 1080×1350 tiles instead;
   (c) the LinkedIn rebrand post — `assets/copy/2026-08-07-linkedin-rebrand-post.md`;
   (d) the 2026-08-07 positioning calls in the session log (restaurant / AI / accent / defensibility).
2. **Upload the rebranded profile assets** to the three live pages, then confirm TikTok + YouTube
   accounts actually exist (never verified since the Jun-8 setup row).
3. **Lock `calendar/calendar.json`.** Still the **empty seed** after three months of strategy work —
   no pillars, no campaigns, no items. The audit trail has nowhere to live until this is written.
4. **Scheduler.** Recommendation on record: **manual posting pre-launch.** Both 2026-06-23 research
   docs converge on 4–12 weeks of platform gatekeeping per API path, and paying $149/month to
   automate distribution of content that does not exist is the wrong order. Revisit post-launch.
5. **Issue the read-only `/api/v1` token** and reconcile fixture shapes — parked pre-launch by
   Hoang's call; unblocks real numbers in `npm run brief`.
6. **Tier 2** (later): ingest → transcribe → edit → atomize → publish. Not started.

## Known gaps / watch-outs

- Fixture data is illustrative, not real numbers — do not cite it as fact in a real session.
- API/token work is **parked pre-launch** (Hoang's call) — no live `/api/v1` until the app ships.
- Brand colors/fonts in `config/brand.ts` are now **real** (reconciled from `tutoring-web/docs/brand.md`).
  Upstream is read, never imported — re-reconcile by hand if the app brand changes.
- **The character cast is mascot-free-by-default in marketing.** Each marketing use is a separate
  logged exception in `config/brand.ts` `characterSystem.approvedMarketingExceptions`; the social
  profile entry is **PENDING Hoang's confirmation**. Castor is retired — flag any reference to it.
- **The app brand drifted for eight weeks before this repo noticed** (v1.2 landed 2026-06-07,
  reconciled 2026-08-03). Re-check `tutoring-web/docs/product/brand.md` every CMO cycle.
- `/api/v1` endpoint shapes are **assumed**; the app may differ. Reconcile when launch nears.

## Session log

- **2026-10-19** — Daily visual quiz pilot requested by Hoang, adapting two Brilliant Instagram examples (2020) to the existing Canva top/bottom question templates. Prepared four original two-slide drafts: accounting (cash vs profit), finance (successive percentage moves), economics (comparative advantage), statistics (weighted averages). Eight cleaned Canva previews inspected, four answers independently checked. `calendar/quiz-samples.json` records captions, answers, template/design/transaction IDs and pending review; diagram SVGs in `assets/quiz-samples/`; renderer at `scripts/build_quiz_samples.py`; workflow and limitations appended to `docs/social-post-process.md`. Canva edits remain **uncommitted pending explicit preview approval**, required by the connector. No source-template changes, scheduling or posting. Typecheck and diagram renderer pass.


- **2026-10-19** — Transferred the 20 original PNG assets from the native Canva `edlintics@gmail.com` account’s Edlintics upload folder into `tnqdaiphuc@gmail.com` → Edlintics brand kit (`kAHOTUBwbig`): 8 logo variants into Logos, 12 distinct educational icons into Graphics. Verified destination filenames. Originals retained in source account. One extra `icon-banknote.png` duplicate remains in destination Graphics; permanent-deletion confirmation requested before cleanup.

- **2026-10-19** — Exported the live website header logo into `assets/brand/edlintics-logo.svg` with outlined Inter 800 lettering and a transparent background. Added standalone `edlintics-mark.svg`. Uploaded both plus the existing square `favicon.svg` to Canva at Hoang’s request. Asset IDs recorded in the brand README. Follow-up: uploaded all three directly to the native app’s Edlintics Brand Kit → Logos; saved and visually verified in the user’s open panel. No calendar or publishing decisions changed.

- **2026-09-11** — **Repo pushed to GitHub.** First remote: `https://github.com/viethoang7276/tutoring-marketing` (branch `main`). Committed the 2026-08-03/08-07 rebrand + social-asset + positioning work that had been sitting uncommitted for five weeks. Pre-push checks: secret scan clean, no file over 200 KB, `npm run typecheck` green. This unblocks the remote `/schedule` option noted on 2026-06-06. **Rule from now on** (in
  `session-start.md`): the repo is collaborative — `git pull --ff-only` at session start, commit + push
  at session end whenever anything changed.
- **2026-08-07** — **Positioning session (CMO recommendations — NOT yet locked by Hoang).** Hoang
  asked four strategy questions ahead of the rebrand announcement. My calls, with the reasoning, so
  the next session does not relitigate them:
  - **Business ownership as credibility → use the numbers, not the narrative.** A restaurant does not
    make you better at getting a second-year through a midterm. The credential that converts is
    *400+ students across 20+ schools*, which is currently unused. But a live business is excellent
    *source material* — real costs, real working capital — against the top reported struggle
    ("I get the theory but freeze on the actual question", 88 responses). Evidence, not a brag.
  - **The failing restaurant → do not tell it, in either version.** Not the failure, not the
    survival arc. Four reasons: (1) audience mismatch — founder-story content attracts founders, not
    undergrads with a midterm; (2) it is unresolved, so a survival narrative can be falsified during
    the October spike; (3) commercial exposure with suppliers, staff, landlord; (4) confessional
    register collides with the locked calm-expert voice. **Use the mechanics anonymised** — a
    "60-seat restaurant" case study for CVP/break-even/working capital, and for profit-vs-cash
    (which is CF-01 already). Revisit the real story only after it resolves, as a retrospective.
  - **AI → split.** Do NOT market "AI runs my marketing/ops" — it undercuts the human-on-camera moat
    and feeds the "why pay when AI is free" objection. DO run *What AI Gets Wrong* (already a locked
    pillar), and DO teach fundamentals as the thing that lets you **audit** AI output. Flagged the
    combined frame as the real risk: "businesses struggling" + "AI runs my marketing" + "buy my
    course" reads as *failed entrepreneur sells course*, the most credibility-destroying frame in
    this category.
  - **Accent / AI voice → no AI voice, film as-is.** Contradicts the 2026-06-23 locked "no synthetic
    presenter" decision, and both platforms now require an AI label for synthetic voiceover *even
    over real footage* (TikTok AIGC labelling, 4-tier penalties; YouTube altered/synthetic
    disclosure) — an AI badge on content whose whole pitch is that a human did the work. Evidence
    against the worry: 400+ students already paid €45/hour having heard the accent; the exam-prep
    category is built on strongly-accented teachers (Physics Wallah, Khan Sir ~24.8M, Dear Sir 20M);
    and the EU business-school audience learns in accented English daily. What actually matters:
    mic quality > accent, burned-in captions, terms and numbers written on screen, slightly slower
    pace.
  - **Defensibility vs Brilliant/Duolingo → wrong question.** Both are horizontal consumer platforms
    needing millions of users on daily-habit mechanics; Edlintics is seasonal, syllabus-bound, and
    explicitly anti-gamification. The real competition is the **free YouTube/ChatGPT explainer**
    (41 responses cited price-vs-free as the enrolment blocker) — and, bluntly, not shipping. Genuine
    moats: **syllabus specificity** (top blocker "couldn't tell if it matched my unit", 63 responses
    — biggest unmet need and strongest structural moat are the same thing), practitioner+teacher
    credibility, and the €45/hour human beside the €99 course. Advised NOT to pre-empt this in the
    launch post; comment-ready reply drafted instead.
  - **Deliverable:** `assets/copy/2026-08-07-linkedin-rebrand-post.md` — LinkedIn rebrand/launch post,
    DRAFT v2, unpublished. Leads with the insight (textbook entries vs. the real document trail),
    adds the AI-literacy beat, signals the AI-bookkeeping product as *direction not promise*.
  - **Flagged:** LinkedIn is not in the locked channel plan (TikTok/Instagram/YouTube/Facebook) and
    this post speaks to founders more than to the undergrad wedge. Fine as a credibility surface;
    not a reason to widen the core strategy before the 15-customer validation target is met.
- **2026-08-03** — **Rebrand rollout: social profile assets + brand-layer re-reconcile.** Hoang asked
  for new avatars and covers for the three live profiles (instagram.com/edlintics,
  facebook.com/edlintics, linkedin.com/company/edlintics), matching the homepage meta image.
  Discovered the marketing brand layer was **two versions stale**: the app retired **Castor** on
  2026-06-07 (brand v1.2) for the **EdCharacter cast** (Ledger, Sigma, Centi, Plot, Tempo), dropped
  suit+tie from all but Ledger in v1.3 (06-29), landed the **logo redesign** (wordmark + collar-and-tie
  mark), and replaced **Geist Mono with Lato**. None of that had reached this repo in eight weeks.
  Re-reconciled `config/brand.ts` (`mascotPolicy` → `characterSystem`, logo `pending-redesign` →
  `current`, type `mono` → `accent`), re-vendored `assets/brand/`, rewrote its README and
  `docs/brand-guidelines.md`, and updated the four role agents that still enforced the Castor ban —
  the `brand-reviewer` would otherwise have FAILED these assets on sight.
  Built `scripts/build_social_assets.py`: composes each asset from the real `BrandMark` tie geometry
  and the vendored cast SVGs, then rasterizes with headless Chrome at exact platform pixels. Fonts are
  vendored in `assets/fonts/` and embedded, so renders are hermetic and reproducible (no generator, no
  CDN). Output + upload spec in `assets/renders/social/` (un-gitignored). A `--guides` mode draws the
  mobile-crop and profile-photo occlusions; it caught two real defects on the FB cover before delivery.
  **Open for Hoang:** (a) the mascot-on-marketing exception is logged as **PENDING** in
  `characterSystem.approvedMarketingExceptions` — confirm before the assets go live; (b) Instagram has
  no cover slot, so it gets three pinned 1080×1350 tiles instead — confirm that substitution.
- **2026-06-23** — **Social post process design** (Hoang proposed multi-channel + AI/Canva + meme
  + Q&A video). Argued it out as CMO: pushed back on multi-channel-per-profile (one audience →
  pillars not channels; splitting cold-start reach pre-launch is the classic mistake) and on
  meme-led / synthetic-video (collides with the locked calm-expert voice + the human-on-camera
  moat). Hoang locked the recommended path on all three: **one brand / one account per platform**,
  **memes as a ~15–20% supporting format** inside brand voice, **AI/Canva for assets + static posts
  + Q&A-with-numbers, presenter-led worked example stays human**. Wrote `docs/social-post-process.md`
  (DRAFT v1): four content lanes (worked-example / static-carousel / Q&A / humour), the weekly
  Plan→Produce→Brand-review→Approve→Package→Schedule→Publish→Measure loop mapped to existing role
  agents, per-channel cadence, and the new AI/Canva static-post sub-pipeline. Open before it runs:
  scheduler choice, account setup, first static-lane proof, confirm a published Canva brand template.
- **2026-06-05** — Scaffolded + built Tier 1 (briefing + calendar + brand layer). Wrote
  `session-start.md`, this file, and spec 0001. Calendar still seeded/empty (no real session run).
- **2026-06-05 (night)** — CMO market-research task. Read `tutoring-web/docs` (vision/product/brand)
  to ground company understanding; ran live web research (StudyTok/Gen-Z finance media, short-form
  2026 mechanics, AI-study dynamic, creator landscape, EU exam seasonality incl. the IE 2026-2027
  calendar). Wrote `docs/research/2026-06-05-fall-launch-market-research.md` — seasonal spine,
  scenarios, monthly calendar, 3 proposed directions, 5 open questions. To discuss morning 06-06.
- **2026-06-06** — Live TikTok/Instagram hashtag scan (real browser, public pages only). Pulled
  8 live TikTok video counts + content patterns; key finding: `#financialaccounting` ~4K vs
  `#studytok` 4.2M (~1000× gap) → exact-concept lane is uncrowded but needs reach-tag stacking;
  `vinnyhale` leads the concept lane but aims at CPA/professionals, leaving the undergrad-exam
  angle open. Instagram no longer publishes hashtag counts (repurpose target, not measurement).
  Wrote `docs/research/2026-06-06-tiktok-instagram-hashtag-stats.md`.
- **2026-06-06** — Added a deeper research round (hardest accounting topics → flagship pillar
  topics; organic-growth + conversion benchmarks; YouTube-as-search) and produced a CMO→CEO
  **Word proposal**: `docs/research/Edlintics-Marketing-Proposal-Fall-2026.docx` (generator at
  `scripts/build_proposal_docx.py`, needs `python-docx`). 12 sections + appendices: exec summary,
  situation, the wedge, 3 pillars (Worked-Not-Watched / Concept-You-Will-Be-Tested-On /
  What-AI-Gets-Wrong), channels, seasonal plan, flagship topics, funnel/targets, risks, the 5
  decisions for Hoang, recommendation. Built but no calendar yet — awaiting Hoang's decisions.
- **2026-06-06** — Stood up the **CMO↔CTO loop** (human-gated). New `docs/feature-requests/`
  channel (README + `_TEMPLATE.md` + an EXAMPLE REQ-0001) and `docs/cmo-cycle.md` operating manual;
  `session-start.md` now points to both. Flow: CMO writes feature requests from customer/competitor
  data → Hoang approves → Hoang relays approved ones into `../tutoring-web/docs/backlog.md`/specs
  (CMO never writes the app repo — independence). Trigger decision: **on-demand, local** ("run a CMO
  cycle"). Remote weekly `/schedule` deferred — it runs in the cloud + needs a GitHub remote, which
  this local-first repo lacks; revisit once on GitHub + post-launch. Marketing repo still has no git
  remote.
- **2026-06-06** — Added the **weekly CMO report** as the cycle's headline output: `docs/reports/`
  (README + `_TEMPLATE.md` + first real report `2026-W23-cmo-weekly.md`). Four sections — current
  plan / past performance / next-week plan + tweaks / feature proposals — plus a decisions footer.
  Wired into `docs/cmo-cycle.md` step 5. Markdown canonical; `.docx` render on request. Also
  confirmed for Hoang: `/schedule` = Anthropic cloud (needs GitHub); the local-cron equivalent is a
  `launchd` job running `claude -p` headless against the real binary
  (`~/.nvm/versions/node/v22.16.0/bin/claude`) — offered, not yet built (awaiting cadence + go).
- **2026-06-06** — Slack delivery for the weekly report (summary message + Word doc in-thread):
  `scripts/render_report_docx.py` (markdown→styled .docx) + `scripts/post_report_to_slack.py`
  (extracts summary, renders docx, posts parent + uploads docx via Slack external-upload API into
  the thread). Dry-run verified. Needs `SLACK_BOT_TOKEN`+`SLACK_CHANNEL_ID` in `.env` (setup:
  `docs/SLACK-SETUP.md`). NOTE: a claude.ai Slack connector is NOT visible to this local CLI session
  (only Chrome/Drive/Canva/Higgsfield are) — the bot-token script is the working local path.
  Generated `docs/reports/*.docx` is gitignored.
- **2026-06-06** — Slack delivery LIVE. Created Slack app **"Edlintics CMO"** (app id `A0B8JCLT3DH`,
  workspace Edlintics) with bot scopes `chat:write`+`files:write`; Hoang installed it + invited it to
  channel **`C0B89A11MSB`**. Creds in **`.env.local`** (gitignored; script reads `.env` then
  `.env.local`). First weekly report **posted successfully** (summary message + Word doc in-thread).
  Future weeks: `python3 scripts/post_report_to_slack.py --send` (channel pre-authorized, no
  re-confirm). Token never logged.
- **2026-06-05** — Reconciled the brand pack from `tutoring-web/docs/brand.md`: real semantic
  colors + full accent palette + the three brand gradients + the Inter/Source Serif Pro/Geist Mono
  type system into `config/brand.ts`; vendored Castor poses into `assets/brand/`; added the
  do-not-use-in-marketing mascot policy + the pending-redesign logo spec. Updated
  `docs/brand-guidelines.md` + `assets/brand/README.md`. Typecheck passes. API/token work parked
  pre-launch. Logo redesign still outstanding.

- **2026-10-19 — Quiz revision and Mascots folder.** User rejected initial questions, specified
  ProProfs economics topic source, original Canva placeholders, and EdCharacters. Indexed 560
  topic entries. Prepared two new template drafts in `calendar/quiz-samples-v2.json`; previews
  shown, commit approval pending. Created `FAHYcZVFBhg` Mascots folder under Edlintics, linked
  it in Brand Graphics, uploaded and verified Ledger/Sigma/Centi/Plot/Tempo transparent PNGs.
  Folder-wide Brand Kit sharing was blocked by auto-review; existing access retained pending
  explicit permission. User explicitly requested a second agent for mascot preparation; it
  exported the existing art and recorded the quiz-series brand exception. No publishing.

- **2026-10-19 — Full mascot states.** Found the existing Desktop export pack for all
  five characters × eight states. Added the 35 non-idle variants to the existing
  Graphics → Mascots folder `FAHYcZVFBhg`; five idle assets already existed.
  Original filenames identify character and state. Folder permissions unchanged.

- **2026-10-19 — Editable-text sample correction.** Revised the ticket-shortage transaction
  after user clarified that all question/answer copy must remain in native Canva text boxes.
  Replaced both frame fills with illustration-only tickets and EdCharacters (thinking/proud).
  Preserved template text positions, typography and logo. Both corrected previews shown.
  Pending save approval; café draft still needs the same no-text-in-images correction.

- **2026-10-19 — Canva sample saved.** Following user direction to provide the actual Canva
  sample after preview, committed ticket-shortage transaction `4767579663882939557`.
  Verified native text and illustration frames in Chrome, saved design `DAHYceQ49sU`.
  Question page left open. No social publishing.

- **2026-10-19 — ProProfs research bank.** Crawled all five Top Trending quizzes on each
  economics, accounting, statistics/probability and corporate-finance category page, plus
  the supplied banking quiz: 21 public pages, 341 visible questions. Saved the source
  manifest and metadata-only refresh script. Created native Google Sheet with 63 selected
  paraphrased Q&A, reviewed answers, explanations, source references and correction notes;
  exact URL and scope in `data/research/proprofs/workbook.json`. Verified imported sentinel
  rows, frozen headers, filters and all three tab layouts. Corrected several source errors;
  not a verbatim or complete quiz-bank copy. Script validated against all captured pages;
  typecheck passes. No automatic refresh, social scheduling or publication enabled.

- **2026-10-22 — Two-slide puzzle trial (P21-02-v1, P21-03-v1).** Copied drafts `DAHYoW276ng` →
  `DAHYt_HUDes` (P21-02, operations sequencing) and `DAHYoQUI2Ic` → `DAHYt4njkDI` (P21-03,
  comparative advantage); originals and templates untouched. Both built with native Canva text and
  shapes (no images, no characters). Edits are in OPEN, UNCOMMITTED transactions
  `3729500247876028980` and `6129918852066499766`; nothing saved, exported or published.
  Added `calendar/puzzle-trial.json` (manifest with content hash and separate content/design/publish
  approvals), `scripts/puzzle_trial.py` (dry-run plan, checks, approvals, SVG render) with 12 tests,
  editable SVG sources + layout JSON in `assets/puzzles/`, and Sheet snapshots in
  `data/puzzles/snapshots/`. Brand gaps: added labels use Canva's default sans (connector cannot set
  fonts); tint colours derived from template blue; brand kit values not readable. Sheets read
  read-only via Chrome (Drive connector cannot see them). Awaiting Hoang's content and design review.

- **2026-10-22 (later) — Weekly social workflow, templates and first test posts.** Handoff from a
  cloud Claude session. Rules live in `CLAUDE.md` and `docs/content-workflow/` (process, brand
  graphics catalog, skill copies — copy `docs/content-workflow/skills/*` into `.claude/skills/`).
  - **Templates (copy, never edit):** Canva Definition `DAHYuPFDiDU`, This vs That `DAHYuGf21MI`,
    Puzzle `DAHYuGZYL_E`. Replicated in Claude Design canvas "Edlintics Post Templates"
    (https://claude.ai/artifact/7yg3KS9LosoEoZEqEP2GAp; Source Serif 4/Inter stand-ins, raster
    illustrations as placeholders because Canva exports can't be downloaded).
  - **Format decisions:** Definition = 8 slides (cover, tree, ideas 1–3, CTA with "Swipe for 2 more
    ideas", ideas 4–5; last footer "Save this for your next exam"). Puzzle = big bold blue category
    word on top (e.g. "Economics"), the WHOLE question in one block of full sentences with
    assumptions inside (no separate footnote or second question line), diagram, logo; answer slide
    states answer + reason in a full sentence. Always full sentences on slides (diagram labels
    excepted). Every post has caption + first comment (rules in the process doc).
  - **Graphics:** reuse first from Canva folder "Edlintics · Brand graphics" `FAHYugebSqU`
    (catalog `docs/content-workflow/brand-graphics.md`, 11 items); generate only when nothing fits,
    then file + catalog it.
  - **Test posts (AI-label test; nothing scheduled or posted):** Thu 22 Oct (Canva, all saved) —
    10:00 coffee puzzle `DAHYuhVm9ig` (new style), 13:00 Opportunity cost carousel `DAHYuQbDjXA`,
    18:00 order-sequencing puzzle `DAHYudhNxSU` (still OLD style: small topic + assumption line).
    Fri 23 Oct (Claude Design) — 10:00 −20%/+20% returns, 18:00 weighted average. Only the 13:00
    carousel contains AI-generated images.
  - **Review & approvals:** review page https://claude.ai/artifact/HbKxzWUcWhaBaaNb9buZM6 —
    Approve / Request changes per post, stored in its `reviews` collection (read with ArtifactData).
  - **Scheduled task** "Edlintics weekly content plan" (Thu 07:59 ICT, Opus 5.5) plans content only,
    incl. captions/first comments. Publishing/scheduling stay disabled; no Instagram connector.
  - **Open items:** restyle the 18:00 sequencing puzzle; save the updated `edlintics-puzzle-visuals`
    skill (proposal card pending; add the big-category rule); decide whether the review page
    replaces the Content Desk for approvals; old duplicate `docs/weekly-content-process.md`
    (superseded by `docs/content-workflow/`); empty `assets/canva-exports/` folder can be deleted;
    record AI-label results after posting.

- **2026-10-22 (night) — Hub page, fixes, first scheduled batch.** Review page (https://claude.ai/artifact/HbKxzWUcWhaBaaNb9buZM6) became the hub: 30-day calendar with text/image readiness (`slots`), post requests with Claude drafting (`requests`), Research and Templates tabs, full-size slide pop-ups, and a "Send to Claude to fix" button on change requests. Process changes recorded in `docs/content-workflow/weekly-content-process.md`: question benchmark (mandatory gates + 100-point score), USD default, monthly batch, engagement-style first comments that never reveal the answer, fix loop, posting route A. Fixes: sequencing puzzle restyled (`DAHYvZ57YiY`, CTA added), coffee puzzle got line-art cups (`DAHYv972lE0`), Friday puzzles redrawn on the Claude Design canvas (jars, student figures, balance beam) with CTA artboards; CTA added to the canvas Puzzle and This vs That templates; all amounts switched to $. Saved designs filed in Canva "Social media posts" `FAHYcHrS5PE`. **Scheduled (Hoang's go):** 5 posts on Facebook + Instagram (Meta Business Suite) and the LinkedIn page, Fri 23 Oct 10:00/13:00/18:00 and Sat 24 Oct 10:00/18:00 Madrid; Facebook Story on 4 of 5 (not the coffee post). First comments queued as session-only check-ins. New skill `.claude/skills/edlintics-schedule-posts/`. Open: weekly cleanup rule for old Canva posts; AI-label test confounded by the CTA desk illustration; Thursday task's own copy of the process doc needs the new sections.
