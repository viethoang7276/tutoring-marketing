# STATUS — living state

The cross-session memory for this repo. Read after `session-start.md`. Update it at the end of any
session that changes state (append to the session log; revise "Now" / "Next").

_Last updated: 2026-11-12_

**Current ads handoff (11 Nov, 21:13 VN):** use fresh manual draft **120251906822720036**, not the imported migration campaign. Two ad sets / six manually uploaded ads; campaign OFF and unpublished. Import is blocked by Meta #3738001. Website migration remains on hold for Claude. Read the final session entry below before continuing.

## Social posting engine: handover (read first, updated 2026-10-24; current rules: see "Rules: current state" at the end)

Any session can take over from here. Do these in order:
1. `git pull`.
2. Run the posting safeguard and change-request checks in `session-start.md`. This means reading `runs` and `slots` in the hub, catching up missed first comments from the last 24 h, and applying, generalising and sweeping every "Request change".

**Systems**
- **Hub** (system of record for approvals, schedule and the Performance tab): https://claude.ai/artifact/HbKxzWUcWhaBaaNb9buZM6. Page source: the scratchpad `post-review.html`. If it is missing, rebuild from the published version with the Artifact read action.
  - DB collections: `slots` (one per post: status proposal/approved/scheduled/posted, statusNote = Hoang's instruction or our note), `runs` (first-comment results per platform), `perf/latest` (Performance tab data, weekly review and next-week list), `requests`, `reviews`.
- **Full dashboard:** https://claude.ai/artifact/2QsDUdLpSPuzWrzn7AznSa. Refresh steps: `docs/content-workflow/performance-review.md`.
- **Daily cloud check** (runs even when the laptop is off): routine `trig_01CD3Zj6BoqtbE3EU5TxPmCY`, 08:00 Vietnam, Opus 5.5. It applies change requests, adds rules, sweeps and reports first-comment misses. Tested OK on 24 Oct.
- **Rules:**
  - `docs/content-workflow/weekly-content-process.md`: the week's formats and slots, the "Rules learned so far" list, and the running tests.
  - `.claude/skills/edlintics-schedule-posts/SKILL.md`: how to schedule and do first comments per platform.
  - `docs/content-workflow/skills/` for visuals.

**Week of 24 Oct to 1 Nov: all 29 approved posts scheduled (24 Oct)**
- Puzzles at 10:00 and 18:00, carousels and videos at 13:00, and comics Mon/Wed/Fri/Sun at 16:00 (Madrid; Vietnam = Madrid + 6 h).
- Every post is on Facebook, Instagram, LinkedIn, X and Threads, with a Facebook Story.
- **Gap:** Threads for the four 1 Nov posts (Threads holds max 25 scheduled). A session cron at 00:20 Vietnam on 26 Oct should add them; if it did not fire, schedule them by hand (the espresso thread is in Threads Drafts).
- **First-comment crons are session-only** (CronCreate). After any restart they are gone: recreate them for every scheduled slot still ahead (4 minutes after each slot), or rely on catch-up. Each run posts the slot's `first_comment` and likes, reposts on IG/X/Threads only, hides the IG like count and tries the IG Story (phone fallback). Results go in `runs`.

**Threads (24 Oct)**
- All 25 scheduled Threads posts are retagged to subject topics: Statistics 5, Finance 5, Economics 4, Accounting 3, Business 3, Spreadsheets 2. The 3 marketing posts went to the Marketing community.
- Edlintics joined Study Threads.
- Every new post must propose its Threads destination in the slot (`threadsTopic`/`threadsTopicVariant`/`threadsCommunity`/`threadsReason`). The hub Review card shows it.
- The 1 Nov Threads posts are still unscheduled because of the 25-limit; they use the alternate topics.

**YouTube (added 24 Oct)**
- Channel: UCUx_KFGdEVdBoKvCS3BxYRA. Five-concepts videos go up as Shorts (full MP4); all others as channel Posts with the slides.
- Done 24 Oct: 6 Shorts (accounting published; finance, economics, statistics, marketing, management scheduled 19:00 Vietnam) and 13 Posts (5 old ones published; 25-1000, 25-1800, 26-1000, 26-1600, 26-1800, 27-1000, 30-1000, 01-1800 scheduled). Each slot's `youtube` field has status and URL.
- **To do:** 15 Posts are `youtube.status: "pending"` (27-1300 through 01-1600). YouTube returned HTTP 429 `posts_soft_rate_limit` after about 14 posts in 90 minutes, and it still held 45+ minutes later. Schedule them in batches of about 5, an hour or more apart, earliest date first, before their slot time. 27-1300 (Oct 27 19:00 Vietnam) is the first.
- Skill: `.claude/skills/edlintics-youtube-upload/SKILL.md` (scripts in its `scripts/`), written for a cheaper model. The UI shows no error on a 429; only the script's status is reliable.

**Daily routine**
- After the first comment on the day's last post (18:00 Madrid), run the daily metrics refresh (performance-review.md): last-7-day posts, plus posts in running tests until their judge date.
- Before any automated action, check the active account is Edlintics on that platform (skill section 0a).

**Running tests**
- **Ledger walk "5 concepts", 24 Oct to 21 Nov, Instagram only:** alternate a 7-clip carousel and one long video. Other platforms always get the long video. On carousel days the long-video IG reel sits in Business Suite Drafts. Slots carry `test: "5c-format"` and `variant`. Decide on 21 Nov.
- **Threads topics, 25 Oct to 7 Nov (H1 to H6 in weekly-content-process.md, judge 8 Nov):** done 24 Oct. All 25 scheduled Threads posts (24 Oct 23:00 to 1 Nov 00:00 Vietnam) now carry a subject topic instead of "edlintics": Statistics 5, Finance 5, Economics 4, Accounting 3, Business 3, Marketing 3, Spreadsheets 2. Marketing posts go into the Marketing community (114K members, 11.3K recent posts), not a plain topic. The Threads texts had no hashtags. Every slot has `threadsTopic`, `threadsTopicVariant` (primary/alternate) and `threadsTopicKind` (topic/community). Edlintics joined **Study Threads** on 24 Oct.
  - **1 Nov posts use the alternate arm and no hashtags:** espresso puzzle = Financial Literacy, management 5c = Finance, economics comic = Finance, expected-value puzzle = Finance. These slots carry `threadsTopicPending: true`; clear it once scheduled. The espresso thread is an unscheduled draft in Threads Drafts and still shows "edlintics", so set the topic when scheduling.

**Waiting on Hoang**
- **Instagram Stories:** share each post's Story from the phone (desktop cannot).
- **Instagram account:** it keeps reverting to hoang.vtrg. Suggest logging the personal account out of that Chrome profile.
- **Puzzle subject label:** should the big subject label at the top of puzzles go, like the comic tags did?
- **Definition template:** should it be updated to the key-terms-map structure?
- **Bios updated 24 Oct** to the Brilliant-style two lines ("Your entrance into the language of business. / Accounting, Finance, Economics, and Statistics.") on Instagram, Threads, X, LinkedIn (tagline and overview) and Facebook. Links are set on all five. There is no Edlintics TikTok; TikTok in Chrome is the restaurant account.
- **Postiz:** a scheduler trial to replace slow Chrome scheduling (would also need him to connect accounts). Not started.

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

### 2026-10-24 (long session)
- **Captions:** general-audience rule (no exam-only wording).
- **Meme comics:**
  - Pain-point research.
  - Scripts v1 and v2 (spreadsheet jokes, Introverted Attorney style).
  - 4-panel template as the default; 2-panel only as an option.
  - Speech bubbles, no topic tag.
  - 4 comics built and scheduled; new flow Mon/Wed/Fri/Sun at 16:00.
- **Puzzles:**
  - Hoang's 7 change requests fixed.
  - The 1 Nov puzzle was replaced three times; final pick: café espresso machine depreciation.
  - "Learning from change requests" process added (fix, then a new rule, then a sweep); the sweep fixed 20 posts.
- **Definition carousels:** rebuilt as definition, key-terms map, then one slide per term. This is a standing design principle.
- **Music:** on all 5 "5 concepts" videos and on template DAHY0pRBfnM; rule: every video carousel gets music.
- **Performance:** dashboard built and made the hub's first tab, with a weekly review and a next-week list; the hub was rebranded to Edlintics tokens.
- **Daily cloud check routine created and tested.**
- **Story and Instagram rules:**
  - Facebook Story kept.
  - Instagram Story added (phone fallback).
  - IG like count hidden on every post.
  - Check IG like and repost state before clicking.
- **Scheduling:** all 29 approved posts scheduled; Instagram-only 5-concepts format test started.


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

## 25 Oct 2026 (later): reels, waitlist, rules
- **Explainer reels are live in the mix.**
  - Skills: edlintics-explainer-reel (engine), edlintics-definition-reel and edlintics-life-of-reel. edlintics-ledger-talks exists but Hoang rejected the mic format.
  - Look: Ledger, Kokoro af_heart, Canva music, no camera moves, an end card with the term and the key point, brand-proportional hands, Ledger-first framing.
  - Scheduled on all 6 platforms: sunk cost (25 Oct, 14:30 Madrid), free rider (26 Oct), and 6 reels (27 Oct to 1 Nov, 08:30 Madrid).
  - Proposal waiting for Hoang: test-ledger-talks-moravec (illustrated, 27 Oct 12:00 Madrid).
  - From 2 Nov: 1 puzzle a day at 10:00, and an explainer reel at 18:00 that alternates definition and life-of (H14).
- **Threads:** the 25-thread cap leaves a backlog (5 reels and the four 1 Nov slots, flagged thPending/threadsPending). A daily session cron at 09:07 VN adds them.
- **Rules added:**
  - No full stop at the end of any paragraph anywhere: captions, comments, slides, web copy and video captions. All 26 upcoming captions on every platform are fixed, and so are the Canva designs. Hoang chose NOT to replace the media on scheduled posts (option C), so the fixed slides apply from the next plan.
  - Colourful puzzles, always with Edlintics blue.
  - first_comment_x is needed when a first comment is over 280 characters.
  - No tutoring in organic posts.
  - No reference-creator credit in public captions.
- **REQ-0003 waitlist:**
  - Hoang approved the WL001 pages and the SEO/GEO work. tutoring-web built it on branch feat/wl-launch-waitlist.
  - Open with Hoang: keep the AI training-bot block (recommended), and whether tutoring-web may run the dev DB migration.
- **YouTube:** the 429 cleared after advanced features were approved. All pending Posts are scheduled.
- **Phone tasks for Hoang:** Instagram Stories for the 25 Oct posts.

## Rules: current state (checked 27 Oct 2026; this list wins over older entries above)
**Approvals and safety**
- Show planned external writes before making them. Content, design and publishing approvals are separate; scheduling or posting needs Hoang's explicit go (an "approve" on the hub Review card counts as approval of the content and its proposed slot).
- Act only as Edlintics, never as Hoang. Never type passwords. Stop on Instagram if it shows "Continue as hoang.vtrg" or a login page. Never Boost; never "Always share stories". No reshare or repost on Facebook or LinkedIn.
- Never put secrets in chat, code or logs. Ask before credentials, OAuth, installs or permission changes. Don't change Chrome or system settings (Hoang can "Mute site" himself).
- The repo remote is PUBLIC: never commit data/contacts/ PII, never bulk-message.
- If the permission system blocks an action (for example editing a published LinkedIn post), don't work around it; hand it to Hoang.
- A timeout is not proof that nothing happened: check before retrying. When a run is interrupted, the next run checks each platform and only does what's missing (no double likes or comments).

**Copy**
- No full stop at the end of any paragraph anywhere: captions, first comments, slides, image text, video captions and web copy.
- No exclamation points. No emoji, except at the end of first comments.
- USD by default ($1.80, $3,000).
- Every slide line is a full sentence; the audience is general (students and business people), not exam-only.
- No tutoring in organic posts; Hoang's face is never shown.
- Never promise what we can't deliver. The 13:00 caption line is now "Comment 'Learn' and we will tell you first when the courses open" (26 Oct, option A; the old "free course" promise is gone from every scheduled post).
- No reference-creator credit in public captions. Ideas from Hoang's references are paraphrased, fact-checked, and unverifiable claims dropped.
- Captions carry no link. Links go in the first comment (link-drop type) as plain edlintics.com with no UTM tags; Instagram and TikTok say "link in bio" (`first_comment_igtt`). Tagged links only in bios and Story stickers (28 Oct)
- First comments: 1–2 sentences, under 150 characters, ending with emojis, and one of 5 types (link drop, question, hashtag stash, bonus, pinned CTA), stored in `firstCommentType`. They never reveal a puzzle answer.
- Every post proposes its Threads topic or community, with a reason. Threads posts carry no hashtags.

**Design and video**
- Puzzles may be colourful, but Edlintics blue must be present and main.
- Canva: save (commit) every draft at once and file it in Social media posts FAHYcHrS5PE. Never leave an open transaction. Delete rejected designs.
- Explainer reels:
  - Ledger with the Kokoro af_heart voice; hand-drawn style; the Edlintics logo at the bottom; no zoom cuts.
  - An end card with the term and the key point.
  - Hands in brand proportion, checked in every contact sheet.
  - Ledger is optional per scene; the talking-to-a-mic format was rejected.
  - Skills: edlintics-definition-reel, edlintics-life-of-reel, engine edlintics-explainer-reel.
- **Background music is very quiet (26 Oct):** in every video, the Canva music track Volume is 8 and the voice/video stays at 100. The local preview pad is 0.025. Every scheduled video was re-exported and swapped on all 7 platforms on 26 Oct, except the free-rider reel, which was already live.
- **Reel covers (26 Oct):** every reel gets a cover from `make_cover.js`:
  - a kicker ("Explained in 40 seconds" or "A day in the life") plus a 3–6 word title with one highlighted keyword;
  - laid out for the 3:4 grid crop.
  - The editable Canva template is "Shorts cover template - explainer reels", DAHZGJ1m_8E.
  - Applying covers to the platforms waits for Hoang's edits ("covers ready"). On TikTok, the cover goes up together with the caption fix as one re-post per video.

**Platforms**
- Seven platforms: Facebook, Instagram, LinkedIn, X, Threads, YouTube and TikTok, all kept.
- **TikTok:**
  - Uploads go through TikTok Studio (skill edlintics-tiktok-upload). Scheduled posts can't be edited, so they are re-posted, and the old one is deleted only after the new one is checked.
  - Scheduled posts carry NO location; live uploads get "IE Tower - IE University".
  - **No self-likes from 26 Oct:** the likes reverted under the new-account limit. Only save and first comment on OUR posts; never click a heart on them. Likes on other creators' videos are fine (Hoang, 27 Oct): no undo or report needed, but always recognise which posts are ours (URL id and caption match the slot) before acting.
  - **Studio first (27 Oct):** do engagement from TikTok Studio. `/tiktokstudio/comment/<id>` posts a top-level comment (insert the text by script, click send). Studio can't save, so check the profile Favourites tab and only open the single public post if the save is missing.
  - Reach is very low (0–1 views per post); judge it on 2 Nov.
- **YouTube:**
  - After a post goes live: like it, save Shorts to "Edlintics saves", and post the first comment (pinned when pinFirstComment is set).
  - Scheduled Shorts are swapped by re-uploading.
  - A Content ID claim on Canva music is expected and harmless.
- **Always mute (26 Oct):** on TikTok and YouTube, run the persistent muter (it mutes and pauses, and survives auto-advance) right after every page load. Close the tab when done, and check things in Studio pages where possible. Hoang may be using the laptop during runs. The half-second of sound before the muter runs can only be fixed by Hoang's Chrome "Mute site" (suggested to him 27 Oct).
- **No typing on TikTok or YouTube pages (27 Oct):** never use computer type or key actions there (on 26 Oct, 75 keystrokes landed on a stranger's video after auto-advance). Insert text with javascript_tool (`execCommand('insertText')`), check the URL before every click, click Post instead of pressing Enter.
- **Threads:** the 25-scheduled-thread cap applies. The daily 09:07 VN run (cron fee9d397, session-only) adds pending posts using only the quiet-music files (music8/) and fixed images. Deskilling and the 29 Oct–1 Nov reels are pending.
- **Instagram:** desktop can't share to a Story, so Stories are phone tasks for Hoang. Hide the like count after a post goes live. Scheduled reels can only have their caption edited, so a media change means recreating them.
- **LinkedIn:** the edit dialog can change the text of scheduled posts but not their media. Use the open-and-check-before-delete order when recreating.

**AI labels (research 27 Oct, `reports/Chat videos and AI labels.md`)**
- The auto AI labels come from Canva: designs containing Canva AI or AI-generated media (the five-concepts Ledger clips) get a signed C2PA manifest ("Canva AI", compositeWithTrainedAlgorithmicMedia). The Kokoro-voiced explainer reels carry none. Proposed rule, waiting on Hoang: no Canva AI media in post designs, and scan every export before upload. Never strip a manifest from an AI file.
- Platform rules: YouTube exempts fully animated video; TikTok (rules in force 24 Sep 2026) only requires labels for realistic-looking scenes or people; Meta names "realistic-sounding audio", so switch on "AI info" for Kokoro reels on Facebook, Instagram and Threads.
- Labels don't change ranking per YouTube (and reportedly TikTok); the best study shows about 7% fewer likes per view.
- Test H16 (AI label effect) is in perf/latest `tests`, not started; the plan is being simplified to Meta-only labels (waiting on Hoang).

**Operations**
- First-comment runs are one-shot session crons about 4 minutes after each slot. The 07:13 VN morning Performance refresh is cron 9ec74f4e. All crons are session-only and need recreating after a restart.
- The hub first-comment tracker (version 32) checks each platform for its own steps:
  - Instagram, X and Threads: comment, like, repost;
  - Facebook, LinkedIn and YouTube: comment, like;
  - TikTok: comment, save.
- When Hoang says "pause", stop the Chrome agents and hold the crons until he says resume. Run Chrome agents one at a time (parallel ones collapse the tab group); queue a cron that fires while another run is using Chrome.
- The hub page is v33, titled "Edlintics Marketing Hub" (27 Oct). Its Performance tab reads perf/latest live; data updates need no republish.
- If the Chrome extension shows as not connected, Hoang restarts Chrome (worked 27 Oct).

## 26 Oct 2026: session log
- **Morning refresh:** perf/latest was already fresh.
- **Threads backlog:** at cap, nothing added.
- **TikTok likes:** Hoang liked the coffee and cake puzzles himself. The no-self-like rule was added.
- **Deskilling reel:**
  - Idea test T2 from Hoang's reference; studies fact-checked.
  - Approved and scheduled for 28 Oct, 12:00 Madrid, on 6 platforms; Threads is pending.
  - Canva DAHZFddgpwY.
- **Quiet-music swap:** 11 scheduled videos replaced on 7 platforms; the rule was saved.
- **"Free course" caption line:** replaced everywhere it could be edited. Two posts are left for Hoang by hand: the LinkedIn live 25 Oct post (the edit was blocked) and possibly the Facebook live 25 Oct reel (it showed a "Failed to publish" badge, but the stats and new caption look fine).
- **Reel covers:** a draft sheet and a Canva template were made.
- **Free-rider reel:** the TikTok comment was posted on the second try. The hub tracker was fixed.
- **Hoang's open items:**
  - the LinkedIn 25 Oct post edit;
  - "covers ready";
  - Instagram Stories (free rider, sunk cost, fraud, finance video, cake, 26 Oct 10:00);
  - whether to switch YouTube to watch-page URLs and Studio checks;
  - "Mute site" in Chrome (optional);
  - turning puzzles into short Instagram Reels (proposal).
- **Correction to the 25 Oct entry above:** Hoang finally chose B, so the media WAS replaced on all 26 scheduled posts.

## 27 Oct 2026: session log
- **First comments:** the 22:00 comic (2026-10-26-1600) resumed after Hoang's pause, checking first; the 00:00 puzzle (2026-10-26-1800) done, TikTok through Studio. Both complete on all 7 platforms (runs v2).
- **TikTok incident:** on 26 Oct, keystrokes landed on a stranger's video after auto-advance. The no-typing rule and Studio-first engagement were added to the skills.
- **Hub:** title fixed to "Edlintics Marketing Hub" (v33).
- **AI-label research:** report `reports/Chat videos and AI labels.md` (notes in `research_notes/`). The labels come from Canva AI clips, not the voice.
- **Chat-story reels:** Hoang's reference is @orbi_the_alien "Corporate Life in 2026" (a Slack-style chat with the mascot as a user, voice-free). Fictional characters are fine; no testimonials or outcome claims about Edlintics; layouts only, never real app names, logos, colours or sounds; drawn avatars.
- **Video engine software (REQ-0004): CLOSED 7 Nov 2026.** Hoang stopped `video-engine-software` (too much technical debt); do not use it, the `ve` CLI or plan on it. Our explainer engine stays; the content team forks it into `tutoring-content/tools/video/engine/` (16:9 lessons) with a scene_lib sync script and coordinates with us. Old note: **Video engine software (REQ-0004):** Hoang wants a REUSABLE video editor app, not one-off videos. The tutoring-web CTO session owns it, in `tutoring/video-engine-software/` (spec on branch spec/editor, `docs/specs/video-engine/`).
  - Screens: Projects, Media library, Templates, Exports, and an Editor (preview, inspector, six-track timeline, Script and Agent tabs).
  - One JSON project format with a schema, shared by the editor, the `ve` CLI and the MCP tools. Its own engine (no Remotion).
  - Build order is editor-first; marketing's dates were dropped.
  - Mockups: the CMO's template canvas https://claude.ai/artifact/1wEyHdXGe6fZBs84hqjA4j, the CTO's animated player https://claude.ai/artifact/CZqaU4vXCDBHTaZox6eHMs, and the CTO's editor mockup https://claude.ai/artifact/PRRu2xvr3Es2aEMFFBbdjZ.
  - Marketing input sent: templates work-chat, then messenger, then assistant, then email; inserts are the file card, spreadsheet cell change, notification, end card and cursor with zoom; CLI needs, house-style lints, and a per-slot export folder with a manifest; Canva stays the last step. Music risk: Canva tracks can't be taken out of Canva.
- **Morning refresh (07:45-08:25 VN):** perf/latest v13, 118 rows, windowEnd 26 Oct; runs/daily-2026-10-27. Yesterday 699 views across 5 posts (best: economics five-concepts, 372; worst: profit-vs-cash comic, 34). 7 days: 2,518 views. Followers unchanged. Threads topic posts: median 4 views against 10 before the test. TikTok Studio shows 0 comments even where first comments exist.
- **Hoang's open items:**
  - approve the editor mockup;
  - the chat panel crossing the right-hand button column (CMO recommends narrowing it);
  - BOARD.md and root AGENTS.md entries for the engine;
  - separate repo or folder; the export folder; the music folder;
  - the "no Canva AI in posts" rule;
  - simplifying H16 to Meta-only labels;
  - plus every item still open from the 26 Oct log (covers ready, Instagram Stories including the comic and the 00:00 puzzle, the LinkedIn 25 Oct edit, the Facebook 25 Oct badge).

- **Afternoon 27 Oct:** Threads backlog: 5 of 9 scheduled (deskilling 28 Oct, salesperson 29, working capital 30, marginal utility 31, diminishing returns 1 Nov); the four 1 Nov slots wait for the 25-thread cap (cron fee9d397 stays). First comments done for the accruals reel and the 27 Oct 10:00 café puzzle (Hoang: Instagram Stories from the phone; TikTok save of the café post not done)
- **Puzzle reels (Hoang, 27 Oct):** approved the voiced format, then v3 with a hand tap and the end card "Follow Edlintics to learn business concepts interactively". Skill `edlintics-puzzle-reel` (commit 50d6354). All 11 scheduled puzzles 27 Oct 18:00 to 1 Nov 18:00 built as reels (videos in assets/renders/puzzle-reels/, gitignored) and put on the Review tab as `reel-puzzle-<slot>` cards (status proposal). If approved they replace the image post on Facebook, Instagram, YouTube Shorts and TikTok; Threads, X and LinkedIn keep the images. Test H17 added to perf/latest (v14, judge 17 Nov). Hub v34 shows "Puzzle reel" cards. Weekly process updated: every puzzle gets a reel
- **REQ-0005** interactive puzzle exercise relayed to the CTO (backlog, after video engine Phase 2) and COO (FYI)
- **LinkedIn:** two runs opened Hoang's personal Notifications by a stray click; skill rule added (never coordinate clicks near the top bar)
## Next session: start here (27 Oct 2026)
1. Run git pull, then read this file's "Rules: current state" and the 26 and 27 Oct session logs.
2. **Recreate the session crons** (they die with the session). Times are Vietnam:
   - **First-comment runs**, 4 minutes after every slot still ahead: puzzles, five-concepts and comics at 16:04, 19:04, 22:04 and 00:04; reels at 14:34 (accruals 27 Oct, break-even 28, salesperson 29, working capital 30, economics student 31, diminishing returns 1 Nov); Moravec 27 Oct 18:04; deskilling 28 Oct 18:04.
   - **Daily Threads backlog** at 09:07, using music8/ media only.
   - **Morning Performance refresh** at 07:13.
   - Every run follows the mute rule, the no-typing rule, Studio-first TikTok, and no likes on our own TikTok posts. Run one Chrome agent at a time.
3. Catch up on anything the hub tracker shows as missed, checking first so nothing is doubled.
4. Check messages from the tutoring-web CTO session about the video engine, and relay them to Hoang.
5. Ask Hoang about the open items in the 27 Oct log.

## 28 Oct 2026: session log
- **First comments done (all platforms, runs docs written):** def-break-even, 2026-10-28-1000 (R-squared), reel-def-deskilling (7 platforms), 2026-10-28-1300 five-concepts statistics (5 platforms). Hoang phone tasks: Instagram Stories for break-even, R-squared, deskilling and statistics; confirm the Facebook Stories
- **Link rule (Hoang approved):** no UTM tags in first comments; plain edlintics.com, "link in bio" on Instagram/TikTok (`first_comment_igtt`). Tagged links only in bios and Story stickers. ga-H7 paused. REQ-0006 owned short links (`/go/<code>`) proposed to the CTO (b80e001)
- **Waitlist:** final URL https://edlintics.com/en/waitlist, merged into development, NOT on prod yet. Do not publish bio links until the CTO confirms prod
- **Puzzle reel layout v4** (Hoang: use the screen height): from the 2 Nov puzzles; 27 Oct-1 Nov reels keep v3 (cedbd62). New diagrams about 900x500-540
- **Threads:** first-comment runs never open Threads Drafts (b95b685). Pending Hoang: R-squared thread is an unscheduled draft ("post 20:30" or "skip"); AI-skills caption shortened to 455 characters ("ok caption", Business topic, 30 Oct 18:00 VN)
- **Hub v35:** Performance split into sub-tabs (Overview, Posts, Platforms and formats, Tests, Review and ideas) with charts; Schedule split into Calendar, First comments, Request a post. Page file copy at `assets/renders/hub/post-review.html` (gitignored; the scratchpad is wiped on restart)
- **Research:** `docs/research/2026-10-28-week45-inspiration.md` (6852aa8) plus section 6 "From Hoang's videos" (347b6a3). Top 5 for week 45: automation bias puzzle reel, Simpson's paradox puzzle reel (Dana and Eli), five checks on AI output (five concepts), skill compression definition reel, operating leverage diagram reel (confirm formula source). Check whether the Microsoft/CMU survey is the deskilling reel's study before reuse. Open decisions: election week (neutral fictional tariff explainer or skip), chat-story test, logged-in Chrome trend scan
- **Hoang's inspiration videos (new rule, 84efeca + cb9abf8):** every shared video is logged in hub `trends` with a `direction` and `directionStatus` (waiting / pending / proven / dropped). A direction steers research only after our version is published AND beats our platform median views on 2+ platforms (3 days, confirmed at 7). Now proven: AI and business skills (Moravec Instagram 1,114 vs median 42), twist stories (sunk cost), animated diagrams (puzzle reels). Pending: deskilling (check 31 Oct). Waiting: career lists, chat stories. 8 trend docs in the hub
- **Female voice blind test (in progress, free tools only; Hoang said no Vercel AI Gateway and no paid voices):**
  - Chatterbox installed locally in `tools/tts-chatterbox/` (gitignored; uv venv Python 3.11, `setuptools<81` needed for the watermarker, HF cache in `.cache`). Render per sentence to avoid truncation; MPS, a few minutes per reel
  - Samples in `assets/renders/voicetest/blind/Voice-A..E.mp3` (gitignored, sent to Hoang). Answer key in `assets/renders/voicetest/answer-key.json` (seed 7281). Same 13 s working-capital script, loudness -16 LUFS
  - The 5 options: Kokoro af_heart 1.08 (current); Kokoro 70% af_heart + 30% af_bella at 1.0 with EQ/de-ess/compression polish; Chatterbox default; Chatterbox expressive (exaggeration 0.75, cfg 0.35); Chatterbox cloned from the tuned Kokoro sample
  - Waiting on Hoang's pick (best and worst). Then reveal the key, and if he picks a new voice, update `edlintics-explainer-reel` vo.py (and the puzzle-reel voice) and the explainer-reel-choices memory. If the scratchpad is gone, regenerate with the settings above

## Next session: start here (28 Oct 2026)
1. git pull, read "Rules: current state" and the 27 and 28 Oct logs
2. Recreate session crons if the session restarted (they die with it), Vietnam times: first comments 4 min after each slot through 2 Nov 00:04 (puzzles/five-concepts/comics at 16:04, 19:04, 22:04, 00:04; reels at 14:34 on 29 Oct-1 Nov; reel-talks-ai-skills 30 Oct 18:06; reel-talks-finance-interview-terms 31 Oct 18:06); Threads backlog daily 09:07 (delete when nothing is pending); morning Performance refresh 07:13. One Chrome agent at a time
3. Ask Hoang: voice blind-test result; R-squared Threads ("post 20:30"/"skip"); "ok caption" for AI-skills Threads; the three research decisions
4. Before the next Thursday plan: check that it reads proven directions from hub `trends`; update deskilling directionStatus on 31 Oct from perf
5. Check Instagram and TikTok bios have a link before relying on "link in bio"; prepare tagged waitlist bio links for Hoang only after the CTO confirms prod

### 28 Oct 2026 (evening, 21:07 VN): session restart
- Safeguard clean: every post live in the last 24 h has its first comment; no `changes` slots; runs/daily-2026-10-28 exists
- Crons recreated (session-only): 22 one-shot first-comment runs from 28 Oct 22:04 to 2 Nov 00:04 VN (reels 14:34, talks reels 18:06, others +4 min); Threads backlog daily 09:07 (b668474a); morning refresh 07:13 (6101cbcc)
- Still waiting on Hoang: voice blind-test pick, R-squared Threads ("post 20:30"/"skip"), "ok caption" for AI-skills Threads, the three research decisions (election week, chat-story test, logged-in trend scan)

## 29 Oct 2026: session log
- **Catch-ups:** 00:04 puzzle first comments ran ~12 h late (Mac asleep), all 7 platforms done. The 28 Oct statistics five-concepts video's YouTube Short and TikTok had been skipped by the 13:00 run; done 29 Oct. Cause: runs `platforms` listed only 5 platforms; 18 upcoming runs docs now include yt and tt
- **Metrics refresh (late, 12:35 VN):** perf/latest v16, runs/daily-2026-10-29. 28 Oct: 1,957 views across 6 posts (best deskilling reel 579, worst lookup comic 52). 7 days 7,243 (prev 4,702). Followers flat. H17 puzzle reels about 4.5x the image baseline on FB/IG; Threads topics median 4 vs 10 baseline. R-squared never went live on Threads
- **Threads backlog:** the four 1 Nov slots were already scheduled 28 Oct; stale threadsTopicPending flags cleared. Only reel-talks-ai-skills is pending (waits on "ok caption")
- **Voice round 2 (Hoang: all round-1 voices too flat):** directed delivery (per-clause rendering, punctuation pauses, `/` and `//` extra pauses, `*word*` emphasis). Files in `assets/renders/voicetest/round2/` (gitignored; listen.html, key answer-key-round2.json). Hoang picked F = Kokoro 70% af_heart + 30% af_bella, directed. He asked whether a paid model would be better; proposed a blind round 3 (ElevenLabs / OpenAI TTS vs F, under $1), waiting on his OK and his own API key in .env. Not yet applied to vo.py
- **Week 45 plan:** the 07:59 scheduled task wrote an OUTDATED W45 plan to the Content Desk (two puzzles a day, euros, no reels/comics). Its instructions need updating. A planner wrote the current-format week to hub slots: 32 proposals (25 posts + 7 puzzle-reel cards), research in `docs/research/2026-10-29-week45-research-run.md`. Waiting on Hoang's review
- **Early bird (Hoang: financial accounting course ready in about a week):** proposed a ~10-day plan (accounting-heavy W45 warm-up, waitlist CTA, "what's inside" post, open-day announcement, manual replies to "Learn" commenters). Blocked on: waitlist on prod, open date, offer terms, currency shown, course promos vs no-tutoring rule
- **Stale rule text to fix:** the process doc puzzle captions still end "More puzzles at edlintics.com"; the carousel skill and Canva Definition template still say "free course"
- **REQ-0007 early-bird free access** (Hoang: posts should lead to the platform for sign-up plus early-bird free access; the CTO builds the system): written and relayed to the tutoring-web session 29 Oct. CTA target is `edlintics.com/en/sign-up` (live on prod; `/en/waitlist` is 404). The offer is NOT to be posted until it works on prod and Hoang fixes the terms (what it covers, length, who qualifies, existing accounts)
- **REQ-0008 course prelaunch mode** (Hoang 29 Oct: Financial Accounting - Part 1 as coming soon with sign-up, reusable for every launch): written and relayed to tutoring-web with REQ-0007. Prod already has "Coming soon" with an email-only notify box; also flagged "8m Est. study time" on that card
- **Voice: ElevenLabs v3** (voice gPiEpcKoaZywgOzc0Zn9) chosen by Hoang after round 3. `TTS_ENGINE=eleven` switch in vo.py and the puzzle-reel build.py (scripts/eleven_tts.py, cached). Kokoro stays default until he confirms a paid ElevenLabs plan (advised: ElevenLabs direct, not the Vercel AI Gateway); then re-voice the week-45 reels. Free-access proposal is local HTML: `docs/feature-requests/assets/REQ-0007-0008-course-prelaunch.html` (artifact copy published by mistake; delete if Hoang confirms)
- **ElevenLabs plan:** Hoang chose Creator (29 Oct; ~50-55k credits/month needed: explainer ~630 chars, puzzle reel ~550, ~9.3k/week). Switch the reel default to `TTS_ENGINE=eleven` as soon as he confirms the plan is active, then re-voice the week-45 reels
- **Week 45 built and reviewed (29 Oct):** 32 cards built (Canva + reels with ElevenLabs v3 at 1.12x, explainer reels 40.5-47.7 s, puzzle reels 36.7-43.4 s); hub v36/v37 with previews and playable reel videos (assets). Hoang approved 31; change on 2026-11-02-1300 applied ("5 checks for AI output in finance"), back to proposal. New rule: titles name the field. Open: Canva music (volume 8) and five-concepts MP4 exports need the Canva editor in Chrome; 51 Canva AI images (AI-label risk, "no Canva AI" rule still undecided); delete leftover Canva copy DAHZX1RSi5U by hand
- **Week 45 go (Hoang 29 Oct, "approved all ... schedule for me"):** all 32 cards approved. Pipeline: (1) Chrome agent adds Canva music (volume 8) and exports final MP4s for 7 explainer reels, 7 puzzle reels, 4 five-concepts; Canva-MCP agent exports full-size PNGs and creates week-45 runs docs; (2) then one Chrome agent per day schedules 2-8 Nov on all 7 platforms (Threads 25-cap, YouTube about 5 posts an hour). 25 week-45 first-comment crons created (2 Nov 16:04 to 9 Nov 00:04 VN); when one fires during a Chrome job it is handed to the running agent. Recurring crons (Threads backlog 09:07, morning refresh 07:13) expire after 7 days, about 5 Nov: recreate
- **Puzzle reels on all 7 platforms (Hoang 29 Oct):** week-45 puzzles post the reel on LinkedIn, X and Threads too (slots mediaNow updated). Already-scheduled 29 Oct-1 Nov puzzles keep their images on those three (Hoang: ignore them)
- **Chatterbox removed (29 Oct, Hoang):** `tools/tts-chatterbox` (4.0 GB) deleted; voice is ElevenLabs v3, Kokoro in tools/tts stays as fallback. Proposed (not yet agreed): delete a post's videos, stills and exported images 7 days after it goes live, keeping its JSON, contact sheet, poster and Canva design
- **CTO 29 Oct: REQ-0007 + REQ-0008 approved, building as feature EB, target prod 4-5 Nov** (spec tutoring-web/docs/specs/course-prelaunch/, preview docs/previews/EB000.html). Stats: GET /api/v1/marketing/prelaunch-stats (marketing:read). Do NOT post the offer until Hoang sets a cap AND an end date in the admin (sign-up does not verify email; the cap is the main protection). /en/waitlist + waitlist bot-protection fix ship in release PR #98 (awaiting Hoang). 8m study-time bug = EB060
- **Meta Pixel (dataset "Edlintics Meta Pixel" 1000075088350707):** CTO ETA on prod about 7-10 Nov, after EB, as its own spec (new "marketing" consent purpose = CONSENT_VERSION bump that re-prompts visitors, cookie policy and audit; CAPI on the Stripe booking webhook behind the security gate). Hoang sends the CAPI token and domain code to the CTO directly. Do not set the ad set conversion event until the CTO confirms events in Events Manager; until then optimise for landing page views and read UTM visits in GA

## 31 Oct 2026 (00:54 VN): session restart
- Safeguard: no `changes` slots; runs/daily-2026-10-30 exists. Every post live in the last 24 h had its first comment except the 00:00 VN safety-stock puzzle (2026-10-30-1800); a catch-up run was started. Still open: the 30 Oct 19:00 "5 marketing concepts" video never went out on LinkedIn (Hoang: repost or skip)
- Committed the 30 Oct reel-engine work left uncommitted (34e49d4): tutoring-ad v5/v6 features (state swaps, gaze, swirl, ad camera keyframes, zone scenes, course visuals, mid-run chunk fix) and the compounding end-card wording. The automatic security check on that push did not run (model unreachable)
- Crons recreated (session-only, Vietnam time): 35 one-shot first-comment runs from 31 Oct 14:34 to 9 Nov 00:04 (reels 14:34, talks reel 18:06, others +4 min; the 00:04 runs also do the daily metrics refresh); morning refresh 07:13 (813289b8); Threads backlog 09:07 (67c2693e). The recurring ones expire about 7 Nov
- **31 Oct day runs:** first comments done on all 7 platforms for the safety-stock puzzle (late catch-up), economics-student reel, tax-incidence puzzle, finance-interview reel (Threads was live too) and simple vs compound interest. Metrics refresh 31 Oct: hub got channels, yesterday and tests, but NOT the per-post rows (the 185 KB `posts` array is too big for one write); full doc in assets/renders/hub/perf-latest-2026-10-31.json. Fix proposed: split posts into weekly docs plus a hub page change (waiting on Hoang's "split it")
- **Threads backlog 31 Oct:** 6 week-45 posts scheduled (25/25 cap); an agent shortened the AI-tool puzzle caption 552 to 491 chars without asking (Hoang to OK); 11 still pending
- **Old copy found live:** the "free course" CTA slide and "More at edlintics.com" caption lines on 31 Oct posts (tax puzzle on Threads/LI/X, simple vs compound interest on all platforms, economics-student reel captions). The Puzzle template DAHYuGZYL_E and week-45 puzzle designs (e.g. DAHZX1ozYTI) still have the free-course slide 3. Waiting on Hoang ("fix free course", "fix captions")
- **Halloween (Hoang 31 Oct):** two extra posts, approved and live: reel `lifeof-financebro-halloween` (Ledger in a Dracula costume over his standard suit, forward contracts and cocoa, 21:30 VN) and puzzle `2026-10-31-2030-halloween` (cocoa less than half its record, why chocolate is not cheaper, 22:30 VN). Definition-reviewer fixes applied. Threads posted live (cap full). Meta AI info not offered in the Reels composer. New engine outfits `vest` and `dracula` plus Halloween props
- **Holiday calendar (Hoang 31 Oct):** `docs/content-workflow/holiday-calendar.md`, big yearly international events only (no Vietnamese or national days); Thursday plan step 4a; Christmas run 11-24 Dec drafted in the 3 Dec plan. The 07:59 cloud planner's instructions are still outdated and must follow this before 3 Dec. Christmas music research: `docs/research/2026-10-31-christmas-music.md` (Pixabay piano shortlist; decisions pending on Content ID and Canva-first)
- **Phone tasks (Instagram Stories):** DfIEbr-geAs, DfJoERPCNS5, DfJyX92gcE9, DfKAG5OD2rQ, DfKG4VGj7r3, DfKYIG4Eqma, DfKe4oDCv5d

## 5 Nov 2026 (15:00 VN): session restart after the Mac shut down
This log had no entries for 1-5 Nov; for that gap see `git log` and the hub (`runs`, slot `statusNote`). The interrupted session had finished its last reply (14:41 VN); no agent or render was cut off
- **Safeguard:** no `changes` slots; runs/daily-2026-11-04 and daily-2026-11-05 exist; all 4 Nov posts have first comments on all 7 platforms (bullwhip ones late, 5 Nov 10:00-10:45 VN). No Threads backlog (no run has thPending)
- **Crons recreated (session-only, die with the session):** 14 first-comment runs 5 Nov 16:04 to 9 Nov 00:04 VN (the 00:04 runs also do the daily metrics refresh); 7 how-to runs 10-16 Nov 03:04 VN; morning refresh 07:13 (c46e4b78); weekly review Mondays 01:13 (074c2ed3). Recurring ones expire after 7 days. Threads backlog cron not recreated (nothing pending). Week-46 posts other than the how-to reels have no crons yet: add them when they are scheduled
- **Hub week view:** re-checked in Chrome after the last two fixes (no puzzle duplicates, W46 proposals show); closes the open check from the old session
- **Hub issues found, not fixed:** (a) First comments banner says "39 posts need attention" but is inflated: non-post runs docs (weekly-*, threads-backlog-*, thumbnails-*, schedule-howto-*) render as rows, so a real miss is hard to see; (b) 2 Nov 13:00 and the startup-founder reel show "Scheduled" in the calendar though their runs docs show them live and done (2 Nov 16:00 comic shows the same; its runs doc not checked)
- **Open from the 5 Nov refresh (runs/daily-2026-11-05):** X 3 Nov 10:00 and 13:00 posts never went out; live X bullwhip post is the old v1 video; TikTok 0 views on every post since 27 Oct (7-day account views 10); Facebook Insights lists a second skill compression reel at 4 Nov 16:54 VN (20 views), possible duplicate
- **Waiting on Hoang:** "approve plan" for the monthly plan (104 proposals, 8 decisions, W46 starts 9 Nov); blog import with his key (AI-at-work series, tutoring-web); Ledger's tie in the FA1 lesson videos if the no-suit rule covers him; long sentences in those videos need a script edit
- **Waiting on others:** CTO tells us when the first real Purchase arrives, then switch the tutoring ad sets from landing page views to Purchase (REQ-0009); REQ-0010 build in progress; FA1 2.4 videos wait for the CTO's video card
- **Update 5 Nov: blog posts for the three AI reels cancelled** (Hoang via the COO: "keep it as term and remove blog"). Moravec, deskilling and cognitive offloading stay as glossary terms. Their drafts in assets/renders/blog/ are kept, not live; CTO (`tutoring-web-26`) asked to pull them from the pending import and confirm nothing exists in prod. Skill compression unchanged. Do not assume the reels attach to the terms until the COO confirms. This replaces "blog import with his key" above: the import must not run with these three in it
- **Update 5 Nov: CTO confirmed** none of the three cancelled posts exists on prod (read-only admin check: 25 posts, all published, 0 drafts) and the import never ran. Old command withdrawn; `publish.sh` now imports only skill-compression-ai-new-hires, which still needs Hoang's go and key. Three local drafts in assets/renders/blog/ kept until Hoang decides
- **Update 5 Nov: the three AI reels go on their glossary terms** (Hoang via the COO, who attaches them): moravec-s-paradox etCESGRbcSw, deskilling xGB0FPcku0M, cognitive-offloading ittmAQoZI8Y. Keep these Shorts public: never set them Private in a swap, or the embeds stop playing. Blog drafts unchanged until Hoang decides
- **Update 5 Nov: blog decisions** (Hoang via the COO): the three AI drafts stay as local files in assets/renders/blog/, not deleted and not published. Skill compression has his go; the COO asked the CTO (`tutoring-web-26`) to run the import. Not confirmed live yet
- **Update 5 Nov: Meta ads live, ads report and MCP** (Hoang). Ads tab of the hub (`ads/latest` v4) now reads Preparing, 0 spent. The tab refreshes with the daily metrics, straight after the last post's first comment; performance-review.md updated. Ads Manager read: only side A (no price) is published; side B (price) is In draft, so ADS-T1 is not running; result type on side A shows Website Purchase, optimisation goal not yet checked; unplanned draft campaign "Nhận thức Thương hiệu" (100,000 VND a day) in the account; "Review and publish (7)" would include those drafts
- **Meta app:** "Edlintics Ads Reporting" 3030719937268223, Edlintics portfolio, ads MCP server use case, unpublished, redirect http://localhost:8421/callback. MCP `meta-ads` added at local scope with --callback-port 8421; waits for Hoang's sign-in through /mcp with ads_management. Agents show each ad change to Hoang first
- **Tracking heads-up from the CTO (FT build, not merged):** at release GA `booking` becomes `book_appointment`, course and bundle item_id becomes slug (item history splits), so mark that date in reports. Open with Hoang: cookie-refusal option A or B
- **Update 5 Nov 17:10: `meta-ads` MCP connected** (Hoang signed in; crons survived the restart). MCP read: campaign 120250271288640298 published 15:15 VN, Preparing, 0 spent. Side A ad set 120250271288650298 goal is OFFSITE_CONVERSIONS on Purchase despite its LPV name. Side B not published. Draft campaign "Nhận thức Thương hiệu" is a March 2025 leftover. Fixes wait on Hoang's yes
- **Update 5 Nov evening: ads fix blocked, waiting on Hoang.** Live campaign unchanged (side A on Purchase). Meta refused: changing the goal on the published ad set (attribution window locked, error 1504040) and mixing goals inside this lowest-cost campaign (error 1885760: duplicate the campaign instead); user_os rejected "Mac OS X" and "Mac_OS_X". Staged, not live: B price draft 120250279948070298 (iOS, tag removal sent) and new A v2 draft 120250319834010298, both now show error 1885760. Proposal: new campaign with both sides on landing page views, pause the old one. Do not use "Review and publish" until decided

## 5 Nov 2026 (21:45 VN): session restart
- **State recovered:** the previous session's last reply was 21:35 VN, no agent or render cut off. 19:04 Automation bias first comments done on all 7 platforms (runs/2026-11-05-1300 v4); its Instagram Story is Hoang's phone task. No `changes` slots; runs/daily-2026-11-05 exists
- **Crons recreated (all had died; session-only):** 12 first-comment runs 6 Nov 00:04 to 9 Nov 00:04 VN (00:04 runs also do the daily metrics and Ads tab refresh), 7 how-to runs 10-16 Nov 03:04, morning refresh 07:13 (b5dafd65), weekly review Mondays 01:13 (ba710a57). Recurring ones expire after 7 days. Not added: a run for lifeof-student-ai-complements (add it when the reel is scheduled)
- **Ads read 21:45:** side A ad set still ACTIVE, Preparing, on OFFSITE_CONVERSIONS, 0 spent, 0 impressions, last edited 17:41 by Hoang. New campaign still waits on "go new campaign"
- **Missing task found:** lifeof-student-ai-complements (Mon 9 Nov 12:00 Madrid, 18:00 VN) is the only `approved` slot and is on no platform. Content and date approved by Hoang 3 Nov; video and thumbnail files exist. Waits on Hoang's go and his look at the thumbnail (Canva DAHZ1LVtoDs). Slot has no `youtubeVideo`, and its definition check was short of a stronger second source (Investopedia blocked)
- **Rewritten-video swaps still open per the hub (notes last written 3-4 Nov, not re-checked on the platforms):** old v1 still scheduled on LinkedIn, TikTok and X, and on Threads for A/B testing and winner's curse. First to go live: A/B testing, 7 Nov 00:00 VN. Needs Hoang's permanent deletes and the x.com check, then a run schedules v2
- **Update 5 Nov 22:40: Meta "Preparing" diagnosed, week 46 built.** All 3 ads passed review 15:18-15:22; no errors, account active, payment on file, 0 spent. Pixel shows 0 Purchase events in 28 days and about 12 PageViews, so a Purchase goal has no signal (our reading; Meta gives no stated reason; up to 24 h is normal). Fix still waits on "go new campaign". First-comment crons checked: 12 of 12 due runs match
- **Week 46 (Hoang: "generate posts for next week so i can review"):** all 20 open posts built and on the hub as `proposal`, statusNote "Built 5 Nov, awaiting Hoang's review": 7 puzzle reels, 4 list reels, 6 explainer reels, 3 carousels. Nothing scheduled; concepts registry not written. Only this week's build was authorised: weeks 47-49 still wait on "approve plan". Videos measured, not listened to
- **Engine:** explainer end-card keypoint limit 4-24 words and voice up to 8 s for definition and life-of (glossary-length keypoints, 4 Nov rule); puzzle options may wrap to two lines. A `meta.fx_story` exemption added during the build was removed so the USD rule stays on; def-bid-ask-spread (says "euro" in its story, amounts in USD) now fails the validator until Hoang decides
- **Hoang to decide on week 46:** euros in bid-ask spread (12 Nov); 15 Nov puzzle chart label "Dashed: A without the menu" over a line that sits on Store B; byte-scan c2pa hits in carousels with brand-library graphics, manifests not read; thumbnail question lines on puzzles written by the builder; YouTube copies use "Sleep Music No. 1" from Downloads or an old scratchpad, assumed to be the Audio Library file
- **Update 5 Nov: ads rebuild (Hoang: "go and unpublish the other campaign", "set up the ads again to comply").** Old campaign 120250271288640298 PAUSED and read back, kept, 0 spent. New campaign draft 120250326121650298 "Edlintics - Tutoring - LPV v2", not published: 550,000 VND a day, both ad sets on landing page views, 275,000 fixed floor and cap per side. Side A 120250326131140298 has its 3 ads, no errors. Side B 120250326131350298 has 0 ads: new creatives fail with error 1885183 because app 3030719937268223 is in Development mode. Waiting on Hoang: set the app to Live, then build B's 3 ads from the uploaded price media and publish on his go. Old draft B 120250279948070298 kept, not discarded. AI extras are on for Video and Illustration ads; the MCP cannot change them, so Ads Manager only. Live targeting has 12 postcodes although the hub says 21, and iOS only. Skill: .claude/skills/edlintics-meta-ads-setup
- **6 Nov 00:04 double run:** a second session ("Resuming interrupted session") also held the crons and ran def-interest-rate-risk. Instagram shows 2 identical comments; the other session reports 2 comments counted on LinkedIn. Nothing deleted; waiting on Hoang. That session cancelled all its 20 jobs; this session holds them (CronList checked). Its refresh wrote perf/latest, perfposts/2026-11-05 and ads/latest and covered only 5 Nov posts and followers, without tests[]. Never run crons from two sessions
- **Weeks 47-49 (Hoang: "generate all the posts for the plan so I can approve"; previews right away; afterwards clean up old posted files):** 5 W47 builders and 2 W48-49 writers started 5 Nov; briefs in the session scratchpad plan-build/. Next: definition review of W48-49, build them, then the storage cleanup
- **Update 6 Nov, from the CTO: release #104 is live on edlintics.com since 12:28 UTC.** Tracking changes that affect your reports from today: the GA event `booking` becomes `book_appointment`; the tutoring item id `tutoring_session` becomes `tutoring-1to1` (or the group id), so item history breaks at this date; everyone sees the cookie prompt again (consent version 4), so expect a dip in consented traffic while people re-choose. GA key events for `book_appointment`, `generate_lead` and `sign_up` get marked once each first arrives. The video card is live too; the first two FA1 2.4 videos are the first real uploads.

## 7 Nov 2026 morning: start here after a restart
- **Hub tools dropped out of the running session at about 07:05 VN.** A restart brings them back. Session crons die with it, so recreate them: first comments today 16:04 and 19:04; 8 Nov 00:04 (def-operating-leverage plus metrics), 16:04, 19:04, 22:04; 9 Nov 00:04; how-to reels 10-16 Nov 03:04; morning refresh 07:13; weekly review Mondays 01:13.
- **Animation standard approved by Hoang:** number and finance beats use the motion and market props, and story beats stay with Ledger. See the explainer-reel skill.
- **Approved reels being upgraded locally:** 2026-11-09-1300, def-bid-ask-spread, 2026-11-15-1300, def-shrinkflation, 2026-11-16-1300, howto-airline-nps, 2026-11-18-1300, 2026-11-20-1300, 2026-11-22-1300, def-carrying-cost. Output and card fields are in `assets/renders/upgraded-7nov/` (`cards.json`). Before writing a card, re-read the slot, skip it if scheduled, and set it to proposal with a Revised note so Hoang can re-approve.
- **Puzzle reels:** animation goes in the answer explanation only. A pilot pair goes in `assets/renders/pilot-animation/puzzle-explanation/`. Roll out only after Hoang sees it.
- **Week 48-49 builder is paused:** 2 of 56 built. Resume after the puzzle pilot, using `BUILD-BRIEF.md` in the session scratchpad (`plan-build/`). If the scratchpad is gone, its rules are in the skills and this note.
- **Currency rule changed:** mix currencies across posts, one inside a post, real figures in their reported currency. Validators no longer block non-USD.
- **Thumbnails:** titles must be direct, such as "What is a bid-ask spread?". Samples are in `assets/renders/pilot-animation/thumbnails/thumbnail-samples-direct.jpg`, awaiting Hoang's verdict. Canva cleanup follows after that.

## 7 Nov 2026 13:55 VN: state just before restart
- **Upgraded reels:** 8 of 10 finished, in `assets/renders/upgraded-7nov/<slot>/`, sent to Hoang's phone, not on the hub: 2026-11-09-1300, def-bid-ask-spread, 2026-11-15-1300, def-shrinkflation, 2026-11-16-1300, howto-airline-nps, 2026-11-18-1300, 2026-11-20-1300. Still to do: 2026-11-22-1300 (render was in progress and may be cut off) and def-carrying-cost. Frames checked only, not audio or playback.
- **Right after restart:** check crons and recreate any missing, confirm the hub tools work, clear a stale `$TMPDIR/edlintics-render.lock` only if its PID is dead, finish the last 2 reels, re-check each slot, then write videos from `assets/renders/upgraded-7nov/cards.json` to cards as `proposal` with a Revised note.
- **Only one session holds the crons.**
- **Update:** 2026-11-22-1300 finished and sent, so 9 of 10 are done. Only def-carrying-cost is left.

## 7 Nov 2026 14:15 VN: session restart
- **Safeguard:** no `changes` slots; runs/daily-2026-11-07 exists; the 4 posts live in the last 24 h have first comments on all 7 platforms. No peer marketing session is running.
- **Crons recreated (session-only):** first comments 7 Nov 16:04 and 19:04; 8 Nov 00:04, 16:04, 19:04, 22:04; 9 Nov 00:04; how-to reels 10-16 Nov 03:04; morning refresh 07:13; weekly review Mondays 01:13. Recurring ones expire after 7 days.
- **Upgraded reels:** 9 of 10 written to hub cards as `proposal`, each with a Revised 7 Nov note. They were `approved`, so Hoang must re-approve. Their `video` and `youtubeVideo` fields now point at `assets/renders/upgraded-7nov/`. Thumbnails unchanged. Frames checked only, not audio or playback. def-carrying-cost restarted after the restart killed its render at 14:10.
- **Update 14:50 VN (Hoang):** parallel renders allowed without overloading (`tools/render-slot.sh`). "Fix all" missing designs and old animation, next week (9-15 Nov) first. Puzzle explanations must use graphics, not only numbers. Carrying cost on its card. Previews added to the 7 scheduled how-to cards.
- **Update 15:15 VN (Hoang): hub Review tab has filters and sort** (search, when, week, format, topic, media including old or new animation, thumbnail, sort; choice remembered per browser). Fixed the false "Design not built yet" on reels and the sort by id. Page source: `assets/renders/hub/post-review.html`, published as version 57.
- **Thumbnails on all upcoming cards:** 93 video posts use `assets/renders/thumbnails-v2/` (`thumbnail.url`, `jpg`, `file`, published as hub files), 7 scheduled how-tos show the cover already uploaded, 6 built carousels show slide 1. 6 unbuilt carousels get theirs when built.
- **Hub storage: 970 MB of 1 GB used.** Each reel upload is about 8 MB. An audit of unreferenced assets is running; deleting anything waits on Hoang.
- **Update 15:40 VN: next week (9-15 Nov) rebuilt.** 8 explainer reels with the new animation and 7 puzzle reels with graphic explanations are on hub cards as `proposal`, output in `assets/renders/upgraded-7nov/<slot>/`. Voice unchanged, frames checked only. Carrying cost caption brackets fixed. New puzzle props: `explain_scene.js`, see "Picture explanation" in the puzzle skill. New `car` prop in scene_lib.py.
- **Hub asset store is full (1,073.2 of 1,073.7 MB).** No more uploads until Hoang approves deleting the unreferenced older files. Audit: `hub_audit.py` in the session scratchpad; re-run before deleting. A builder deleted one of its own superseded uploads without asking.
- **Waiting on Hoang:** re-approve; delete old files; puzzle style; scheduled how-tos; go to schedule; prime cost "biggest single bill" line. Still to fix after next week: old animation on 16-24 Nov reels and puzzles, then build the unbuilt posts from 23 Nov. COO engine speed work follows.

## 9 Nov 2026 (09:45 VN): state and handover
- **9-15 Nov is fully scheduled** on FB, IG, LinkedIn, X, YouTube and TikTok with thumbnails-v2 at upload (28 posts incl. the 7 how-tos). Threads holds 25 max: 3 still `thPending` (2026-11-15-1000, 2026-11-15-1300, lifeof-hotel-overbooking); the daily 09:07 backlog run adds them. Runs docs exist for every post.
- **Prime cost (11 Nov slot, 12 Nov 00:00 VN):** rewritten per Hoang to the textbook definition (direct materials + direct labor, raw materials named), v2 in `assets/renders/upgraded-7nov/lifeof-restaurant-prime-cost-v2/`, approved. Thumbnail corrected ($11,000 / 55%; old one kept as `-old-65pct.jpg`). FB/IG first went out with the old thumbnail; Hoang said "swap": old post moved to Business Suite Drafts, rescheduled with the new one.
- **Everything to 6 Dec is built and on the hub** (72 posts uploaded 8 Nov): new puzzles with picture explanations, 8 list reels, 28 new explainers, 11 rebuilt explainers, 6 Canva carousels (DAHaO2H-u9M, DAHaOy_okeU, DAHaO7cQJnc, DAHaOwnE2b8, DAHaOxPfnnU, DAHaO9uc2f0). 20 cards that were approved went back to `proposal` (video changed). **Waiting on Hoang's approval** before scheduling 16 Nov onward. All new list reels and puzzles are in $ (cards written that way); voice not checked by ear.
- **Hoang's change requests 7 Nov, done:** event planner (couple, dessert and each extra animate on their word) and ride-hailing (city map, cars move to the busy higher-price area) rebuilt v2, same voice. New rules saved: animation follows the script line by line; textbook definitions, not industry shortcuts.
- **Hub storage:** 180 files (563 MB) deleted with Hoang's OK; 113 MB free. 66 posted-only files (~123 MB) remain: Hoang authorised deleting them, but the classifier blocked a relayed agent, so delete them from the main session when space is needed (list in the session scratchpad `hub2/plan.json`, `del_posted`). 5 posted cards now show broken previews.
- **Engine:** opt-in lesson speed flags (`LESSON_SINGLE_ENCODE=1`, `LESSON_OVERLAP_CHECK=strict`, `PICTURE_ONLY=1 STILLS_ONLY=1`; numbers in `.claude/skills/edlintics-explainer-reel/SPEED.md`); videotoolbox rejected. COO adopted them. New scene props (couple, string lights, dessert table, guitar, drum, city map, map zone); puzzle sprites (boat, sofa, cup, car, gift, mail, tv). Render gate pause: `touch $TMPDIR/edlintics-render-slot.pause`, remove to resume (used twice for tutoring-web release checks).
- **video-engine-software is stopped (REQ-0004 closed).** Content team forks our engine for 16:9 lessons.
- **Threads 500-char rule (Hoang 8 Nov):** use `threadsText`, else cut Pause line, closing CTA, Hint; shorter question only with his OK. In the schedule skill.
- **Weekly review 2-8 Nov:** H15 judged (link comments win on clicks), Threads alternate topics rejected (go back to primary), list reels best (econometrics 6 saves, 2 follows), carousels weakest. See `perf/latest` v33 and `runs/weekly-2026-11-09`.
- **Waiting on Hoang:** (1) ad account restricted for unusual activity, Request review in Ads Manager; (2) TikTok 2 views from 25 posts, check the account on the phone; (3) close the 5c-format test early?; (4) approve 16 Nov-6 Dec on the hub; Instagram Story shares (phone).
- **Session crons (die on restart, recurring expire after 7 days):** first comments 9-16 Nov at each post +4 min (16:04, 18:04/19:04, 00:04 and the 03:04 how-tos); morning refresh 07:13; weekly review Mon 01:13; Threads backlog 09:07. After a restart, recreate them from the runs docs (`dueAt`).

## 9 Nov 2026 (10:35 VN): session restart
- **Safeguard:** no `changes` slots; runs/daily-2026-11-08 and daily-2026-11-09 exist; the 4 posts live in the last 24 h (8 Nov 16:00, 19:00, 22:00 and 9 Nov 00:00 VN winner's curse) have first comments on all 7 platforms. No peer marketing session running (ListAgents)
- **Crons recreated (all had died; session-only):** 21 first-comment runs 9 Nov 16:04 to 16 Nov 00:04 VN (the 00:04 runs also do the daily metrics and Ads tab refresh), 7 how-to runs 10-16 Nov 03:04, morning refresh 07:13 (6ea2a5a5), weekly review Mon 01:13 (c115a9cd), Threads backlog 09:07 (044cae54; today's 09:07 run was missed, next 10 Nov). Recurring ones expire after 7 days
- **Still waiting on Hoang:** unchanged from the 09:45 handover above (ad account review, TikTok views, 5c-format test, approve 16 Nov-6 Dec, IG Story shares)
- **Ads decision (Hoang 9 Nov, 11:00 VN): no A/B test, no per-ad-set spend limits.** ADS-T1 dropped. Rebuild the LPV v2 draft as ONE ad set ("Tutoring - Madrid wealthy areas - LPV") holding all 6 ads (video, photo, illustration, each with and without €45/hr, own utm_content each), campaign budget stays 550,000 VND/day, remove the 275,000 floor/cap. Goal LPV, Instagram only, same postcodes, AI extras as before. Remove the old side B ad set only after listing it to Hoang. Draft only; publish on his go (account restriction must be lifted first). **Blocked:** meta-ads MCP shows no tools (re-auth via /mcp) and the Chrome extension is disconnected, so nothing changed yet. Chrome down also blocks today's 16:04/18:04/19:04 first-comment crons
- **Update 9 Nov 12:45 VN, ads (meta-ads MCP re-authed by Hoang):** Hoang had edited the LPV v2 draft in Ads Manager 10:46-10:53 VN (side A goal to Conversions on EngagedVisit, bid cap 100,000, "Business school" interest, start 9 Nov). He then chose LPV and a price line. Done and read back, draft only: ad set 120250326131140298 renamed "Tutoring - Madrid wealthy areas - LPV", goal LANDING_PAGE_VIEWS (pixel PURCHASE promoted object), bid cap, floor and cap removed, no active errors, holds the 3 no-price ads; campaign 120250326121650298 stays 550,000 VND/day, lowest cost. **Blocked:** the 3 price creatives (copy adds line 2 "Sessions from €45 an hour", utm_content video-price / static-photo-price / static-illustration-price) failed with 1885183 because app 3030719937268223 is still in Development mode; media are uploaded (images 82c80157/1f2032ba photo-price, ab1e6dc9/d63937ac illustration-price; videos 1644667267036231 4:5, 1886632299160731 9:16). Hoang either sets the app Live or adds the 3 ads in Ads Manager. **Not removed yet:** empty side B ad set 120250326131350298 in LPV v2 (discard preview blocked by the permission classifier) and the duplicate B ad set 120250279948070298 with 3 broken price ads under the old campaign (preview shown, token not used). Pixel: EngagedVisit fired 2 times in 28 days. AI extras still on in the no-price ads (Ads Manager toggle)

## 10 Nov 2026 (08:30 VN): runs and refresh
- **First-comment runs 9-10 Nov:** café puzzle (16:00), AI complements (18:00, run late), income statement (19:00, late), brewery how-to (03:00) done on FB, IG, Threads, YouTube, TikTok (and LinkedIn for the first three). **Missing:** X on all 4 (x.com Cloudflare "Verify you are human"; never solve it, Hoang must) and LinkedIn on brewery (linkedin.com ERR_CONNECTION_RESET 03:30 and 07:50). The morning catch-up could not fix either. Instagram already showed a like and repost on the AI reel before the run (not this session; no peer session)
- **Daily refresh done by a subagent (07:50-08:25):** runs/daily-2026-11-10, perf/latest v34 (windowEnd 9 Nov), perfposts 3-9 Nov, ads/latest v14; LinkedIn and X not read (null with na). Yesterday best: AI complements 387 views; worst: income statement 251; brewery 382 in 5 h. TikTok still near 0 views. Local copy assets/renders/hub/perf-latest-2026-11-10.json (gitignored)
- **Ads draft still dirty:** the empty B ad set 120250326131350298 in LPV v2 and the old-campaign B ad set 120250279948070298 (3 broken price ads) still exist; removing them needs Hoang's confirm (and a permission allow for the MCP discard); price creatives still blocked by app Development mode
- **Session crons** hold all first-comment runs to 16 Nov 03:04 plus 07:13 refresh, Mon 01:13 review, 09:07 Threads backlog
- **Update 10 Nov ~10:40 VN, ads (Hoang: "add a new draft with the new rule"):** new draft campaign **120250407591940298 "Edlintics - Tutoring - LPV v3 (one ad set, no test)"**, Sales, 550,000 VND/day CBO, lowest cost, auto-catalog cleared; one ad set 120250407599120298 "Tutoring - Madrid wealthy areas - LPV (all ads)" (LPV, pixel PURCHASE promoted object, no bid cap, no floor/cap, same 12 postcodes, Business school interest, iOS, Instagram 6 placements); 3 no-price ads reusing creatives (Video 120250407602240298, Photo 120250407602340298, Illustration 120250407602600298). All VALIDATED, no errors, NOT published. Price creatives still fail 1885183 (app Development mode). LPV v2 draft left as it was. Correction: the "restricted for unusual activity" account is TK 1 1811051243039603, not Edlintics 535582635765592 (ACTIVE, payment on file)
- **Update 10 Nov ~15:45 VN, ads (Hoang: "add the one with price as a separate ad group, no A/B test"):** LPV v3 now has a second ad set **120250407647910298 "Tutoring - Madrid wealthy areas - LPV - price"** (same audience and goal, no floor/cap; shares the 550,000 VND campaign budget, so not a 50/50 test) with 3 price ads made as inline creatives (the Development-mode block only hits ads_create_creative): Photo 120250407648420298 (photo-price 4:5), Illustration 120250407650010298 (illustration-price 4:5), Video 120250407657200298 (price 9:16, cover = "Stuck on your business courses?" frame 7acab2b2, AI label on). Line 2 "Sessions from €45 an hour"; utm_content static-photo-price / static-illustration-price / video-price. All VALIDATED, not published. Risk: publish may still hit 1885183 for the inline creatives. One size per price ad (no 4:5/9:16 split)
- **Update 10 Nov ~17:00 VN:** 16:00 credit-card puzzle run done on FB, IG, LinkedIn, Threads, YouTube, TikTok (X still Cloudflare). LinkedIn reachable again: brewery LinkedIn comment and like caught up. **Threads backlog cleared:** 2026-11-15-1000 (Statistics, threadsText), 2026-11-15-1300 (Finance), lifeof-hotel-overbooking (Business, Mon 00:00) scheduled and verified in Threads Drafts; thPending false on all. No thPending left. X first comments still missing on 9 Nov x4, brewery, 10 Nov 16:00
- **Update 10 Nov ~17:45 VN, ads draft LPV v3 fixed (Hoang: "check and fix all the issue on chrome"):** (1) ad set 1 had error 2490408 after an Ads Manager edit dropped its pixel promoted object; restored PURCHASE pixel + LPV. (2) Turning off "Reveal details over time" made the reused no-price creatives fail (#1815589, deprecated CTA link_title/description), so all 3 no-price ads were rebuilt as clean inline creatives (photo 5cbbe7ef 4:5, illustration 6add271d 4:5, video v8 1143259878355107 9:16 with AI label; cover 7acab2b2): this also removed the Meta AI extras. (3) Every ad had no Instagram profile in Ads Manager (the IG id 17841432834644119 in object_story_spec is not linked there); selected "edlintics" (Ads Manager id 2998763006910431) on all 6 ads in the UI. Read-back: campaign, 2 ad sets, 6 ads VALIDATED, no errors. Not changed (Hoang's edits): campaign budget now 500,000 VND/day, ad set 1 attribution 1-day click. Still open: Advantage+ sales campaign shows On; X Cloudflare. Lesson for the ads skill: set the Instagram profile in Ads Manager (or find the actor id) for inline creatives


## 11 Nov 2026: Codex session start and Meta portfolio migration
- Git pull was already up to date. Hub UI: all dates / Changes requested shows 0 of 204 posts; runs/daily-2026-11-10 exists; latest metrics refresh shown is 11 Nov 00:14–00:26 VN.
- Safeguard remains incomplete: 11 Nov 16:00 Singles’ Day run is flagged missing; FB and IG posts verified live in Business Suite at 16:01. No engagement actions submitted by this session. Old X misses remain report-only outside 24 hours. After Hoang completed verification, X became accessible as @edlintics; refreshed published profile still showed 9 Nov cafe puzzle as newest, so do not assume later scheduled posts published.
- Hoang confirmed new portfolio URL. Verified portfolio edlintics 1 `1704820277908835`, page `108471317472449`, ad account Edlintics `2038169006901956`, VND / Madrid time. Old portfolio-specific feed URL returned unavailable; new home works. Active instructions and report routes updated; historical logs retained.
- New portfolio has no datasets. Prepared Edlintics Meta Pixel creation form with automatic portfolio-wide CAPI unchecked; creation awaits confirmation of Meta Business Tools Terms. REQ-0009 contains migration handover. No pixel, token, website configuration, ad settings or permissions changed. Hub database and timers not updated (those tools are unavailable in this session).
- Resume: check whether Hoang created the pixel before submitting the prepared form; acceptance of Meta Business Tools Terms is pending. Browser work stopped when Hoang switched to an unrelated sign-in window. Re-read the hub and live engagement before catch-up; none was submitted here.

### 11 Nov 2026: pixel created and ad account connected
- Hoang completed dataset creation. After reload, verified **Edlintics Meta Pixel** `1178793404712949`, owned by **edlintics 1** `1704820277908835`; initial state no events / no connected assets.
- Codex connected the dataset to the sole **Edlintics** ad account `2038169006901956`. Meta confirmed 1 Ad Account added; Connected assets shows Edlintics with a link to verified internal asset `120251902756580036`. No ads published or changed.
- Creation approval is resolved; supersedes the pending-form notes above. Do not create a duplicate pixel. Website/CAPI migration, token configuration, domain access and event verification are still pending with the CTO; no website or credentials changed. See REQ-0009 for the exact next steps. Posting catch-up and hub/timer updates remain incomplete.

### 11 Nov 2026 17:25 VN onward: catch-up and new campaign request
- Hoang explicitly deferred website migration to Claude and authorized read-only investigation. Result: env-only (browser and CAPI share NEXT_PUBLIC_META_PIXEL_ID), token access must be verified and rebuild required. No website changes made. Details in REQ-0009.
- Singles’ Day Facebook first comment posted as Edlintics at 17:25 VN and verified in feed on reel 1852663922593625; comment ID 2355526415293475. Existing Like was already on and left alone. Instagram composer showed zero comments; text was entered but submission was NOT verified. Check for an unsent draft and live comments before retrying.
- Hoang requested replication of the previous tutoring campaign into new account 2038169006901956. Draft only; no campaign writes yet. Use latest LPV v3 configuration (10 Nov handover), verify live source before copying; older A/B instructions are superseded by no-A/B/no-ad-set-spend-limits decision.

### 11 Nov 2026 ~17:40 VN: campaign migration in progress
- Verified source campaign 120250407591940298: 2 ad sets, 6 ads, Sales/LPV, campaign budget 500,000 VND/day, paused. Old account is pending closure; Duplicate is disabled. Do not cancel account deactivation
- Exported source through Ads Manager > More > Export selected; local `~/Downloads/export_20261111_1732.csv` (UTF-16 tab-delimited). Export reflects newer copy: 1000+ students and math included; older 400+ notes are stale
- Exact 12 postcodes: ES 28001, 28002, 28003, 28006, 28007, 28009, 28010, 28015, 28016, 28028, 28036, 28046. Instagram placements stream/story/reels/explore_home/profile_feed/ig_search; iOS iPad/iPod/iPhone; English US/UK; Business school interest; Advantage audience with suggested age 18–25
- Source no-price video is incomplete in both UI and export: empty media, primary text and headline, default See details CTA. Migration draft restores existing video with sibling no-price copy, video-price headline and Book now CTA; verify preview before approval
- Original audience references customer list 120250408584500298. Asked Hoang whether to upload same customer list to new account if unavailable; no response yet. No customer data read or uploaded; omitted from prepared draft pending decision
- Prepared `/tmp/edlintics-meta-migration/import.txt`: six ads under two ad sets, all PAUSED, new pixel 1178793404712949, no old entity IDs or image/video hashes, matching local media filenames. Uploaded four 4:5 images from upload-v3 and original 9:16 price/no-price MP4s through import UI. Import started; success NOT yet verified. New Sales Campaign pre-existing draft untouched
- Import confirmed successful: campaign **120251904077230036**, 2 ad sets and 6 ads imported; all paused, unpublished. Price ad set **120251904077440036**, no-price **120251904077420036**. Price video **120251904077510036**, no-price video **120251904077490036**, no-price photo **120251904077530036**
- Draft validation ongoing: imported video thumbnails were missing (#1443226), selected opening “Stuck on your business courses?” covers and checked AI labels for both; preview error panel reported resolved after saves. Restored missing no-price ad-set advertiser Edlintics; ad-level EU warning may remain until ad set published, do not publish merely to clear it. Static brightness/contrast defaults require disabling, all other creative AI toggles imported off
- Catch-up: Singles’ Day Instagram comment submitted and re-opened to verify exact text as edlintics (~17:44 VN); bike-shop Facebook comment verified at 17:46 VN, ID 1769217510817839 on reel 2032329414100829; bike-shop Instagram comment submitted then re-opened and verified. Existing FB/IG likes were on, left unchanged
- Singles’ Day LinkedIn comment verified as Edlintics author; Like applied. Bike-shop LinkedIn comment submitted + Like clicked, verification in progress. Remaining checks: Threads, IG repost/hide likes, X live posts, TikTok/YouTube. Native-only tools cannot run the required TikTok/YouTube persistent muter and JS-only comment insertion, so do not bypass those safeguards
- LinkedIn bike-shop comment verified as Edlintics; Unreact Like confirms like active. Threads: Singles’ Day DfmHDu5DoSM reply posted (DfmTjJAkhnX), Like and repost count 1; bike-shop DfktvLMgOvE reply DfmTo9XEiO- verified exact text, Like + repost count 1. No Threads drafts opened
- Campaign static settings inspected across all four image ads: AI additions off, brightness/contrast off, only Relevant comments and Enhance CTA on. No ads published. Customer-audience question still pending

### 11 Nov 2026 ~17:52 VN: handoff saved
- IG confirmed comments directly on Singles’ Day `DfmHGfAk8zQ` (comment 18066698693535870) and bike shop `Dfkt1DJGQfl`. Both already liked/reposted; own repost avatar and count 1 visible, left unchanged. Hid like counts on both and reopened menus to verify “Unhide like count to others”. Stories remain phone task
- Saved a visible annotation on the Claude artifact Ads view, anchored to its historical campaign status. It contains new portfolio/account/pixel, draft campaign, website hold, comment results and pending tasks. “Send to Claude” explicitly unchecked, so no Claude execution requested. Comment from Hoang Truong begins “Handoff — 11 Nov 2026, Codex”, verified in All comments. This is an annotation only: underlying `ads/latest` and `runs` records are NOT updated; those tools are unavailable
- Draft link: https://adsmanager.facebook.com/adsmanager/manage/campaigns/edit/standalone?act=2038169006901956&business_id=1704820277908835&selected_campaign_ids=120251904077230036
- Remaining before launch: customer audience availability/authorization; website pixel/CAPI migration by Claude; final campaign/ad-set validation (including schedule and EU advertiser/payer warning). No publish action performed. Source account left pending closure; unrelated New Sales Campaign draft untouched
- Catch-up incomplete only where noted: TikTok/YouTube require available browser scripting to satisfy the no-native-typing/persistent-mute rule; X latest visible Nov 9, later scheduled posts not verified published. Do not duplicate the verified FB/IG/LI/Threads comments. No timers recreated

### 11 Nov 2026 20:35 VN onward: evening engagement and manual ad repair request
- Hoang requested today’s first-comment/like/repost check and manual ad uploads because imported ads report errors. Do not publish ads; inspect actual errors and replace media through native Ads Manager upload flow
- 19:00 VN “5 project management terms”: approved first_comment verified from hub. FB posted as Edlintics at 20:35, comment 1478480864377957 on reel 3139582916373624, Like verified on. IG comment posted and re-opened to verify exact text; like already on. LinkedIn comment verified as Edlintics, Unreact Like confirms like. Threads DfmbllegWvl reply Dfmm6_okuup verified; liked and repost count 1
- TikTok/YouTube JS safeguard blocker unchanged: browser access host unavailable, only native app control available. No new actions attempted there
- Evening Instagram DfmbpezAeIe: existing Like and own repost verified, first comment visible, hid likes and verified Unhide menu. X and TikTok/YouTube still pending verification/action
- Root ad blocker verified 20:40 VN: #3738001 “Not allowed to publish imported ads: You can publish imported ads after several weeks of running ads that follow our policies.” Earlier media/preview fixes did NOT make imported campaign publishable. Hoang requested manual upload. Rebuilding a fresh draft through normal Create UI, not importing or duplicating imported entities; imported draft retained paused for reference, no deletion authorized

### 11 Nov 2026 21:13 VN: manual rebuild saved, unpublished
- Created campaign **120251906822720036**, **Edlintics - Tutoring - LPV - manual Nov 11**, through normal Create > Sales. Campaign switch verified **OFF**, in draft; no Publish action performed. Review verifies shared **500,000 VND daily campaign budget**, Highest volume. Two ad sets, three ads each; no A/B or per-ad-set spending limits. Existing imported campaign and unrelated New Sales Campaign left untouched.
- No-price set **120251906822730036**: photo **120251906822740036**, illustration **120251906952620036**, video **120251906975940036**. Price set **120251907016610036**: photo **120251907016620036**, illustration **120251907016630036**, video **120251907016640036**. Only freshly created manual entities were duplicated to produce the variants.
- Uploaded all six original files individually through native media Upload: four `upload-v3/*4x5-v3.png` assets and the original `video/ad-tutoring-video.mp4` / `video-price/ad-tutoring-video-price.mp4`. Verified original crops; 41-second no-price and 44-second price video, manual opening cover “Stuck on your business courses?”. Both video AI disclosure boxes on. No image generation variants selected. Static brightness/contrast and other optional AI extras off; disabled Show spotlights on both illustrations. Relevant comments and Enhance CTA remain on.
- Saved and re-read six distinct utm_content values: static-photo, static-illustration, video, static-photo-price, static-illustration-price, video-price. Price body adds “Sessions from €45 an hour” as line 2. All use updated 1000+ students / 20+ schools copy including math; photo headline Hoang Truong — Business tutor — Edlintics, other headline Business tutoring that makes it click; Book now CTA. UI did not expose a description field in this Instagram-only flow; source description parity has not been independently confirmed.
- Identity Edlintics page + edlintics Instagram verified. Website events checked with **Edlintics Meta Pixel 1178793404712949** on all six ads. Pixel remains inactive because website is deliberately unchanged; Claude must perform the env/CAPI migration in REQ-0009 when Hoang releases the hold.
- Ad-set review verifies Website/landing-page-view optimization, all 12 Madrid postal codes, English UK/US, Business school interest, suggested age 18–25, Edlintics as advertiser AND payer. Price-set controls verify iOS, Instagram only, six placements and no limited spending to excluded placements. Device expansion unchecked before duplication. No customer list uploaded; the question to Hoang remains unanswered.
- **Launch checks still required:** native LPV setup exposes Standard attribution model but no click/view window; original no-price 1-day-click and price attribution parity were NOT confirmed. Source Purchase promoted-object parity was not exposed in this LPV UI either. No #3738001 appeared on the fresh ads, but publish-time acceptance has not been tested. Review contains generic “Please add” labels for campaign Ad sets / selected-location advertiser fields even though 2 sets and Edlintics advertiser/payer are visibly present; inspect any actual validation on final launch, never publish merely to clear a warning. Schedule defaults to 11 Nov 14:41 Madrid, ongoing; review start time before launch.
- **Evening X catch-up completed:** refreshed profile now showed project-management post **2120486715446145223**, no replies/likes/reposts. Posted approved first comment **2120518237020631249**, verified exact text, Like and Reposted. Profile next post is still Nov 9 cafe; today's other X posts were not visible. Do not assume they published.
- Today's evening FB/IG/LinkedIn/Threads results are in the preceding entry; no duplicate comments. TikTok/YouTube remain blocked by native-only access and the skill's JS insertion/persistent-mute requirements. IG Stories remain a phone task. No timers recreated; underlying hub `runs` and `ads/latest` NOT updated.
- Attempted a follow-up reply to the earlier Claude artifact annotation, but Hoang switched Chrome to Zoom before entry/submission could be verified. **No new artifact reply saved.** Browser interaction stopped to avoid interfering. This local handoff is authoritative for the manual rebuild; the earlier artifact annotation still describes the blocked import and needs reconciliation when Claude resumes.
- Draft link: https://adsmanager.facebook.com/adsmanager/manage/campaigns/edit/standalone?act=2038169006901956&business_id=1704820277908835&selected_campaign_ids=120251906822720036

### 12 Nov 2026 00:29–00:36 VN: midnight restaurant first-comment catch-up
- Hoang requested first comments and normal engagement on other posts published today. Git pull already up to date. Checked last 24 hours and new midnight slot; previous Singles' Day, bike and project-management FB/IG/LI/Threads engagement remains present, project-management X also already done. Did not duplicate.
- Hub Review approved **A day in the life of a restaurant manager: prime cost**, 11 Nov 18:00 Madrid = 12 Nov 00:00 VN. Exact approved text used on every completed platform: “Follow Edlintics for a new day-in-the-life reel every week, and send this to a friend who runs a restaurant 🍽️📌”. GMV how-to is not due until 03:00 VN; no future post engaged.
- **Facebook:** live post 1883388509855825 / reel **2331649147599756**; comment **4082700485194301** verified as Edlintics, Remove Like confirms like. No repost (not applicable).
- **Instagram:** reel **Dfm99UZAs_t**, comment **17914769070488746**. Submitted via Business Suite, reopened comments to verify, then verified directly on Instagram. Active profile link /edlintics/. Like = Unlike; repost count 1 verified after applying; like count hidden and menu rechecked as Unhide. Desktop Share lacks Add to Story; Story remains phone task.
- **LinkedIn:** newest restaurant post in company 31541400 admin; approved comment verified as Edlintics, Unreact Like confirms like. No repost (not applicable).
- **Threads:** original **Dfm99x3iXuK**, reply **DfnBzaXEpUv**. Opened reply permalink to verify exact published text; original shows Unlike 1 and Repost 1. No Threads Drafts opened.
- **X:** original **2120562202033742188**, reply **2120570956259422217**. Exact reply visible, original verified 1 reply / 1 repost Reposted / 1 like Liked. Profile contains restaurant and project-management posts; other recent scheduled X posts remain unverified, not assumed published.
- **Still blocked:** browser access host unavailable (native Chrome only). TikTok/YouTube skill requires persistent JavaScript muter and JS-only comment insertion, so no native typing attempted there. Underlying hub runs/ads data and daily metrics not updated because ArtifactData tools are unavailable; no timers created. Task tabs closed. Ads and website unchanged.

## 12 Nov 2026 17:00-17:45 VN: Claude back after the weekly usage limit (paused 11 Nov ~01:00 to 12 Nov 17:00)
- **Missed while paused:** daily refresh 11 Nov (subagent stopped by the limit, nothing written) and 12 Nov; first-comment crons 11 Nov 03:00, 16:00, 19:00, 12 Nov 00:00, 03:00, 16:00 all fired late as queued prompts. Codex covered FB/IG/LI/Threads for 11 Nov posts (and X for project management + restaurant); recorded in hub runs today (2026-11-11-1000, howto-bike-job-costing, 2026-11-11-1300, 2026-11-11-1800)
- **Done now (within 24 h):** 2026-11-12-1000 (margin puzzle) and howto-fashion-gmv on X, FB (new portfolio 1704820277908835), IG (liked, reposted, likes hidden), LinkedIn, Threads. X works again (Hoang passed Cloudflare)
- **Stopped: YouTube is signed in as Hoang's PERSONAL account** (avatar H, Premium, personal playlists). One like went on the margin Short from that account and was removed at once; nothing else done there. YouTube and TikTok for 11-12 Nov posts are outstanding until Chrome's YouTube account is switched back to the Edlintics channel; check TikTok identity too. Lesson: always run the skill's identity check (section 0a) before the first YouTube click
- **Migration check:** repo docs, CLAUDE.md, schedule and ads skills already use portfolio 1704820277908835 / account 2038169006901956 / pixel 1178793404712949 (Codex). meta-ads MCP sees 2038169006901956 ACTIVE; 535582635765592 PENDING_CLOSURE. Updated hub ads/latest v15 (campaign = manual draft 120251906822720036, migration notes) and memory tutoring-ads-facts. Still open: website pixel switch to 1178793404712949 (REQ-0009, CTO, on Hoang's hold), daily metrics 11-12 Nov, X misses on 9-10 Nov posts (over 24 h), YouTube/TikTok for 11-12 Nov

## Next session: start here (12 Nov 2026, 17:50 VN)
1. `git pull`, then the session-start checks. Session crons hold the first-comment runs through 16 Nov 03:04 plus the 07:13 refresh, Monday 01:13 review and 09:07 Threads backlog (recurring jobs expire ~16 Nov). If this session is gone, recreate them from the runs docs' `dueAt`
2. **Before any YouTube click, check the signed-in account is the Edlintics channel** (Chrome was on Hoang's personal account on 12 Nov). Then do YouTube + TikTok first comments for 2026-11-11-1300, lifeof-restaurant-prime-cost (both pin on YouTube), howto-fashion-gmv and 2026-11-12-1000 if still within reason; older ones are report-only
3. Daily metrics refresh for 11 and 12 Nov (runs/daily-2026-11-11 and -12 missing); Business Suite Insights now use business_id 1704820277908835, ads read from account 2038169006901956
4. Meta: current = portfolio 1704820277908835 / account 2038169006901956 / pixel 1178793404712949; launch candidate = manual draft 120251906822720036 (unpublished). Old 535582635765592 drafts (LPV v2, v3) are dead. Website still sends the old pixel: REQ-0009 waits on Hoang releasing the hold
5. Waiting on Hoang: go to schedule 16–22 Nov (28 approved); switch YouTube back to Edlintics; release the website pixel switch; customer list for the new ad account (files in ~/Downloads, he uploads); X catch-up for 9–10 Nov posts if he wants it; IG Story shares (phone)

## 12 Nov 2026 (17:55-18:50 VN): session restart
- **Checks:** git up to date; no `changes` slots; no peer marketing session. The earlier session's crons were gone
- **YouTube switched back to Edlintics:** Chrome was on Hoang's personal Google account. Avatar › Switch account › Edlintics worked with no password; Studio shows UCUx_KFGdEVdBoKvCS3BxYRA. If Hoang wants his personal account active again, the identity check will catch it next run
- **YouTube + TikTok caught up (4 posts in the last 24 h):** 2026-11-11-1300 (5 project management terms), lifeof-restaurant-prime-cost, howto-fashion-gmv, 2026-11-12-1000 (margin puzzle). YouTube: like, save to "Edlintics saves" (checked in the playlist), first comment; pinned on the first two. TikTok: Studio first comment (igtt text where the slot has one) and save from the player; no self-like. Recorded in hub runs. Older misses stay report-only: YouTube/TikTok for 2026-11-11-1000 and howto-bike-job-costing, X for 9-10 Nov posts and those two
- **Crons recreated (session-only):** 15 first-comment runs from 12 Nov 19:04 to 16 Nov 03:04 VN (the 00:04 runs also do the daily metrics and Ads refresh; the 03:04 how-to runs create their runs doc if missing), morning refresh 07:13 (da728b53), weekly review Mon 01:13 (46de6ab4). No Threads backlog cron: nothing is `thPending` until 16-22 Nov is scheduled
- **Daily metrics:** catch-up refresh for the missed 11 Nov run started 18:50 VN in a background agent (result in the hub: runs/daily-2026-11-11, perf/latest)
- **YouTube engagement by script works on the watch page** (`/watch?v=<id>`, no Shorts auto-advance): JS click on like, `#simplebox-placeholder` › insertText in `ytd-commentbox #contenteditable-root` › JS click on `#submit-button button`, Save to playlist › "Edlintics saves", comment Action menu › Pin › Pin. Emojis render as images, so compare the editor text through the img alt values
- **Still waiting on Hoang:** go to schedule 16-22 Nov (28 approved); release the website pixel switch (REQ-0009); customer list for the new ad account; launch decision on manual draft 120251906822720036; X catch-up for 9-10 Nov if wanted; IG Story shares (phone)
- **Daily metrics catch-up done (background agent, all 7 platforms read):** wrote runs/daily-2026-11-12 (this run, Madrid day 11 Nov, window 5-11 Nov) and a back-filled runs/daily-2026-11-11 log; perf/latest v36; perfposts 5-11 Nov; ads/latest v16; 5 slots set to `posted`. Doc name = Vietnam date of the run, so tonight's 00:04 run writes daily-2026-11-13. 11 Nov: 1,229 views on 4 posts, best restaurant prime cost 370, worst fashion GMV 280 (youngest). TikTok still near 0 views
- **X is missing 8 posts** (found by the refresh): the @edlintics timeline jumps from the 9 Nov cafe puzzle to the 11 Nov project terms post. Missing: AI complements, income statement, brewery (9 Nov), credit card puzzle, Little's law, externality, bike shop (10 Nov), Singles' Day puzzle (11 Nov). Not checked yet whether they sit unsent in X's scheduled list. Needs Hoang's call
- **Business Suite Home still shows "Ad account restricted" with Request review** (not pressed); new account 2038169006901956 has no published campaign, spend 0
- Clock note: times in this entry and in today's hub notes are approximate (the session's own estimates ran ahead of the system clock)
- **19:04 run done:** Markup vs margin (2026-11-12-1300) first comment, like and repost on all 7 platforms, recorded in hub `runs/2026-11-12-1300`
- **New idea from Hoang (career ladder reel):** he shared https://www.instagram.com/reel/DfpKXzdI776/ ("Engineering intern to CTO", 2:58). He likes the captions in the bottom half and the amount of animation. Logged in hub `trends/2026-11-12-hoang-ig-career-ladder` with a proposed version ("Audit intern to CFO", about 100 s). Not built yet: it needs a low caption band and rung chips in the reel engine, and Hoang's pick of the first ladder

## 13 Nov 2026 (00:00-01:00 VN)
- **00:04 run done:** bid-ask spread reel (def-bid-ask-spread, runs doc 2026-11-12-1800) first comment, like and repost on all 7 platforms, recorded in hub `runs/2026-11-12-1800` v2
- **Daily metrics + Ads refresh done:** `runs/daily-2026-11-13` v1, `perf/latest` v37, `perfposts/2026-11-06..12`, `ads/latest` v17. 12 Nov: 380 views on 3 posts; best the 25% margin puzzle reel (363), Markup vs margin carousel only 11 after 6 hours. TikTok still 0 views on all 26 posts of 6-12 Nov. Ads: 0 spend, nothing published, "Ad account restricted" banner still there (Request review not pressed). X still missing the same 8 posts of 9-11 Nov. The payment network how-to (03:00 VN 13 Nov) was not live at the read; the next refresh must add it. Local copy `assets/renders/hub/perf-latest-2026-11-13.json` was not written
- **Ladder reel (new format, Hoang 12-13 Nov):** v2 of "Audit intern to CFO" approved in look ("I like this"): art fills the whole vertical screen, captions on top, a different Ledger per rung, CTA ending ("To climb your own career ladder, learn technical business concepts at Edlintics") instead of a definition card. In progress by a build agent: two more ladder reels (marketing intern to CMO for Fri 13 Nov, analyst to portfolio manager for Sat 14 Nov; audit to CFO proposed for Mon 16 Nov), a thumbnail each, hub proposal cards, and a new skill `.claude/skills/edlintics-ladder-reel`. Engine changes in `.claude/skills/edlintics-explainer-reel/scripts/` are uncommitted until reviewed

## 13 Nov 2026 (01:00-03:20 VN)
- **Career ladder reels:** 4 built with the new skill `.claude/skills/edlintics-ladder-reel` (commit dd750a4): audit intern to CFO, marketing intern to CMO, analyst to portfolio manager, consultant to partner. Packages in `assets/renders/ladder-reels/<slug>/` (`<slug>-post.mp4` is the file to post). All 4 are hub `slots` proposal cards with `test: "L1"`: audit 13 Nov ("post now"), the others 14, 15, 16 Nov at 15:30 Madrid. **Nothing posted or scheduled.** Hoang said "Post the audit intern to CFO now", then "Prepare the video and related resources and put them on the artifact": I held the posting and am waiting for his "post"
- **Open on the ladder reels:** nobody has listened to the audio; Review-tab rendering of `reelType: "ladder"` unconfirmed; thumbnails are engine-made, not Canva; the audit title scene shows steps without the ladder; the skill is not yet tested by a cheaper model
- **Test L1** (in `perf/latest.tests`): ladder reels vs other voiced reels at the same age, views at 24 h and 72 h; judge 19 Nov, confirm 23 Nov. Track it in the daily metrics refreshes
- **Rules changed (commit 0bb25f6, Hoang "Ok with all decision"):** direct title opening instead of a question hook; reel story structure; one or two punch lines allowed per reel; news-led cap raised to three a week (three is my reading). The how-to validator still requires the old first line
- **"Explained" previews** (private equity, hedge funds) made from the script study of finance_90seconds; they live in the session scratchpad with a private engine fork, not merged. Waiting on Hoang: full-screen layout, cards, merge
- **Queued:** rewrite one upcoming definition reel in the new story structure and show the script before replacing anything
- **03:04 run, howto-payment-network:** first comment, like and repost done on all 7 platforms (runs doc `howto-payment-network`). Instagram Story share is Hoang's phone task
- **Security review of commit dd750a4 did not complete** (model unreachable); log in `~/.claude/security/log.txt`

## 13 Nov 2026 (07:40-08:50 VN)
- **Morning refresh:** no first comments missed in the last 24 h, no slots with status "changes", `runs/daily-2026-11-13` already existed
- **Hoang approved all 4 ladder cards on the hub** and said "I mean publish them in social media"
- **Audit intern to CFO reel PUBLISHED about 08:00-08:25 VN on all 7 platforms** with thumbnail (Meta, LinkedIn, TikTok), caption and first-comment round (runs doc `ladder-audit-intern-to-cfo`): IG `Dfqc1kOgHKW`, X `2121053241177952741`, Threads `DfqdWVyEe0w` (topic Accounting), YouTube Short `tvXl7aWtpzA`, TikTok `7707464117807779092` (IE Tower location). Instagram Story share is Hoang's phone task. Nobody listened to the audio before it went out
- **YouTube copies:** `<slug>-youtube.mp4` made for all 4 ladder reels with `mixbed.py` (voice-only audio + `assets/renders/money-reels/music/youtube-sleep-music-no1-bed.wav`, video stream copied from `-post.mp4`). Not yet in the ladder skill: add this step
- **Other 3 ladder reels:** a background agent is scheduling them on 7 platforms for 14, 15, 16 Nov at 21:30 VN (15:30 Madrid) and writing slots + runs docs. If the session died mid-way, check each platform's scheduled list before redoing anything
- **Session crons added:** first-comment runs 14, 15, 16 Nov 21:34 VN (ladder slots); test L1 24 h checkpoint 14 Nov 08:47 VN
- **09:25 VN: the other 3 ladder reels are SCHEDULED on all 7 platforms** for 14, 15, 16 Nov at 21:30 VN (agent report; I re-checked X's scheduled list for 14 Nov, the three TikTok cards and the hub slots). YouTube Shorts `MxzpTg2-TB4`, `fhiHu8YNr_I`, `v0Ea6R5iFmg`; TikTok `7707470100009438484`, `7707471500437409045`, `7707474221198265620`. Threads: analyst reel posted without the closing "Walk up the ladder" line (503 chars, 8 Nov rule); marketing reel goes to the Marketing community, not a topic. Threads now offers "Add AI label" in the More menu (left untouched; skill says no such option). Hoang confirmed: "do schedule … like, comment and repost as usual"
- **Hoang, 13 Nov:** run first-comment rounds and other repetitive tasks through a Haiku subagent (Agent tool, `model: "haiku"`) to save credit; the main model briefs it and checks the result. Also: ladder reels are the priority and move to everyday jobs (waiter in a franchise, florist, factory technician, fashion designer); topic list proposed in chat, waiting for his pick and "swap" or "add" for week 16-22 Nov
- **Ladder reels run every day in an added slot (Hoang, 13 Nov: "add more time slop, we dont need to swap… The more we posts the better").** A Sonnet agent is building six everyday-job ladders as proposal cards: waiter in a franchise, florist, factory technician, fashion designer, barista, warehouse worker (cards dated 17-22 Nov 15:30 Madrid, `test: "L1b"`). Hoang then said "We put that on the 23rd, let fable do is ok": start date being confirmed with him (my question in chat); re-date the cards if he means the week of 23 Nov
- **REMINDER, due 1 Dec 2026:** rework "A day in the life" reels to be simpler and closer to the real job (salesperson reel as the model). Not before December
- **Hoang, 13 Nov ~10:30 VN: "Pause the other, give me one example".** The six-ladder Sonnet build is STOPPED. On disk it finished only `assets/renders/ladder-reels/ladder-busser-to-area-manager/` (waiter ladder, current style; was at the Canva music step, hub card state unchecked). Florist, factory technician, fashion designer, barista, warehouse: not built. Do not resume until Hoang has seen the example
- **The one example:** hotel receptionist ladder for Mon 23 Nov 15:30 Madrid (his "put that on the 23rd"), being built by a Fable agent as the trial of "one business concept per rung" (`trial: "concept-per-rung"`), proposal card only. This answers his question on how ladder reels lead people to Edlintics; other ideas given in chat (specific glossary ending, next-day definition reel, sourced pay per rung, landing page per ladder, measuring profile visits and clicks) are NOT decided
- "Explained in 90 seconds" is the definition reel written the new way, not a separate content type (Hoang, 13 Nov)
- **Example ready (13 Nov ~11:15 VN):** `ladder-receptionist-to-general-manager` (87.6 s, concept per rung: upselling, no-show rate, occupancy rate, cost per occupied room, gross operating profit; pounds; Canva DAHaxfbgcmA), proposal card on the hub for 23 Nov 15:30 Madrid, video sent to Hoang. Open: `howto-hotel-revpar` is on the hub the same day at 21:00 (RevPAR left out of the ladder for that reason); three definitions rest on vendor sources; two reviewer-corrected wordings not re-reviewed; nobody listened to the audio; five hotel outfits added to `scene_lib.py` (uncommitted, engine regression not run; the paused Sonnet agent also left uncommitted edits there)
- **Test L2 (Hoang, 13 Nov: "Only do 2 videos like this and test against other video for performance, we decide by Friday next week"):** exactly two concept-per-rung ladders (receptionist, built; florist, being built by the same Fable agent, card dated 18 Nov) against current-style ladders; decide Fri 20 Nov 2026. In hub `perf/latest.tests` as `L2`. The other paused ladders stay paused. Asked Hoang to move the receptionist reel from 23 Nov to Tue 17 Nov so it has data by Friday, and to use the built waiter reel (current style) as a control on Thu 19 Nov: not answered yet
- **New idea from Hoang (13 Nov ~11:40 VN): career cities map reel.** He shared https://www.tiktok.com/@yas.jd/video/7684596041710112022 ("Best cities in the world for high paying careers", 73 s, 113.6K likes, 20.7K saves; 5 careers with a top 3 of cities, opinion, no sources). Logged in hub `trends/2026-11-13-hoang-tiktok-best-cities-careers`. Our version: Ledger travels a hand-drawn world map, each city with its landmark, its career and one sourced fact, more Asia and Europe, ending "To climb in these cities, you need a good business foundation / Go to Edlintics.com to learn technical business skills". A Fable agent is building it (new `map` layout in the engine, output `assets/renders/map-reels/map-career-cities/`, proposal card `slots/map-career-cities` dated 20 Nov 15:30 Madrid, date to confirm). Florist ladder (test L2) is building in parallel
- **Receptionist ladder moved to Tue 17 Nov 15:30 Madrid** (Hoang: "Move it"), still a proposal card; florist stays 18 Nov. Waiter (current style) on Thu 19 Nov as an extra control was proposed with it but not explicitly confirmed, and it has no hub card yet
- **Hoang, 13 Nov ~12:00 VN: "Build all till monday 23rd, it is just the test will help us to determine the content direction again".** Ladder line-up, one a day at 15:30 Madrid: Mon 16 consultant (scheduled), Tue 17 receptionist (new style, card), Wed 18 florist (new style, Fable agent building), Thu 19 waiter, Fri 20 factory technician, Sat 21 fashion designer, Sun 22 barista, Mon 23 warehouse worker (current style, `test: "L2"`, `arm: "control"`; the Sonnet agent was resumed for these five). All are proposal cards; nothing is scheduled until Hoang approves them. The map reel card is also pencilled for Fri 20 Nov: date to confirm
- **City map reel: publish as soon as Hoang approves it** (his words, 13 Nov: "City map reel will be posted as soon as it get my approval"). So when `slots/map-career-cities` turns `approved` on the hub or he approves in chat, post it right away on all 7 platforms with thumbnail, caption and the first-comment round (same route as the audit ladder reel on 13 Nov); ignore the pencilled 20 Nov date. Check the card status at each session start and each cron wake-up
- **Florist new-style ladder ready (13 Nov ~13:00 VN):** `ladder-shop-assistant-to-florist-owner` (84.1 s; wastage rate, average order value, sell-through rate, fixed costs, net profit; euros; Canva DAHaxa_VWBU), proposal card for Wed 18 Nov 15:30 Madrid, `test: "L2"`, video sent to Hoang. All five definitions ended on PASS in a second review; three rest on vendor sources. Open: "120 stems received, 90 sold" label shows only briefly; inventory shrinkage reel on 19 Nov and a 23 Nov list reel also touch wastage and sell-through; nobody listened to the audio. Engine regression passed (covers the hotel outfits and the Sonnet agent's uncommitted `scene_lib.py` work). Note: the Sonnet agent appears to have a current-style florist slug `ladder-shop-assistant-to-shop-owner` too; check its report so two florist reels do not both go out
- **Five current-style ladders built and carded (13 Nov ~13:30 VN, Sonnet agent; I looked at every contact sheet):** `ladder-busser-to-area-manager` (Thu 19 Nov, 80.6 s, Canva DAHaxR7R_No), `ladder-machine-operator-to-plant-manager` (Fri 20, 84.4 s, DAHaxc1Tj54), `ladder-design-intern-to-creative-director` (Sat 21, 84.0 s, DAHaxnQNoYo), `ladder-barista-to-district-manager` (Sun 22, 84.3 s, DAHaxkJ4iDI), `ladder-picker-to-logistics-director` (Mon 23, 86.7 s, DAHaxsRuQTM). All proposal cards, `test: "L2"`, `arm: "control"`, 15:30 Madrid, each with -post.mp4 and -youtube.mp4. Weak spots left: warehouse "to customer" scenes show a bus and a small car instead of a truck; several top rungs rest on thin sources (area manager, senior technician, design intern, logistics director); same-industry posts within 30 days are flagged on each card; nobody listened to any audio. An unused current-style florist build sits in the agent's scratchpad (`reel/ladder-shop-assistant-to-shop-owner`), no card
- **`scene_lib.py` is still uncommitted** (30 outfits + `bouquet` prop from the Sonnet agent, 5 hotel outfits, plus whatever the map agent adds). Regression passed before the map work; re-run it after the map agent finishes, then commit the engine
- **City map reel built (13 Nov ~14:15 VN):** `assets/renders/map-reels/map-career-cities/` (100.0 s, 10 stops: Silicon Valley startups, London finance, Paris luxury, Frankfurt central banking, Basel pharma, Dubai aviation, Singapore shipping, Hong Kong wealth management, Hsinchu chip making, Tokyo research; Canva DAHaxhjlHA0), proposal card `slots/map-career-cities`, video sent to Hoang. **Publish on all 7 platforms as soon as he approves** (post `map-career-cities-post.mp4`, YouTube `-youtube.mp4`). Open: nobody listened (check "Hsinchu" and "Edlintics dot com"); title says "in under two minutes"; Paris fact names LVMH from its own page and calls it "the leading luxury group"; Hsinchu landmark is a generic chip plant; ACI figure is preliminary
- **HUB ASSET STORE IS FULL (1 GB):** the map card carries a 540p preview instead of the post copy. Nothing was deleted. Hoang to decide what to clear (old reel videos on posted cards are the obvious candidates)
- Engine: new `meta.type: "map"`, `scripts/map_props.py`, `scripts/map_land.json` (Natural Earth coastlines, no country borders), `meta.rung_label`; regression passed after all three agents' edits; committed with this entry
- **New rule from Hoang (13 Nov ~13:40 VN, sent to the map build agent; I checked the message is his): captions sit in the centre of the bottom half on ALL videos**, not the top band. Memory `captions-bottom-half-center`. The map reel was rebuilt that way (v2).
- **Map reel:** card approved by Hoang on the hub 13:36 VN ("Wait even I approve… I want it [the sub] at the center of bottom half"); v2 checked by me; a Fable agent is PUBLISHING it now on all 7 platforms with the first-comment round (runs doc `map-career-cities`). If the session dies, check each platform's feed before redoing anything
- **Seven unscheduled ladder reels (17-23 Nov) are being rebuilt with low captions** (picture only, same voice) by the map agent, which is also converting `ladder_script.py` and the ladder skill; superseded hub blobs of those seven cards are deleted to make room. NOT changed: the posted audit reel and the three scheduled reels for 14-16 Nov (captions on top); asked Hoang whether to redo those. Other layouts (definition, how-to, life-of, puzzle, highlighter, Ledger talks) still have captions on top: conversion not started
- **Map reel PUBLISHED 13 Nov 13:53-14:06 VN on all 7 platforms** (v2, captions low) with thumbnail (Meta, LinkedIn, TikTok) and the first-comment round (runs doc `map-career-cities`; I re-checked X): IG `DfrCC6vFXag`, X `2121134949785084177`, Threads `DfrCedHEZYU` (topic Career Advice, looks like a community-style topic), YouTube Short `r9Ix2ObEOGo`, TikTok `7707548387503131905`, LinkedIn activity 7526900371554934785. Instagram Story share is Hoang's phone task. Nobody listened to the audio before it went out. TikTok learning: a hashtag not in the History row (`#careeradvice`) needs a real click on Hashtags, the tag text inserted by JS, then a real click on the dropdown option; `edl_tag` alone leaves "##"
- **"Career cities with Ledger" series (Hoang OK'd the plan 13 Nov ~14:40 VN, asked for career/industry episodes too and a plan for the rest of November).** Plan, each a proposal card first, slot 12:00 Madrid / 18:00 VN (my choice): Mon 16 Part 2 North America (New York first), Wed 18 Part 3 Australia and New Zealand (Melbourne), Fri 20 Part 4 finance careers, Mon 23 Part 5 more of Europe, Wed 25 Part 6 tech careers, Fri 27 Part 7 more of Asia, Mon 30 Part 8 fashion and luxury careers. Parts 2 and 3 are queued with the map agent after the ladder caption rebuild. Memory `career-cities-series`. Not done yet: a "Part 2 is coming" comment on Part 1 (proposed to Hoang, he said OK to the plan; hold until Part 2 is built so the promise is safe)
