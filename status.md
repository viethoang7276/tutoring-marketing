# STATUS — living state

The cross-session memory for this repo. Read after `session-start.md`. Update it at the end of any
session that changes state (append to the session log; revise "Now" / "Next").

_Last updated: 2026-10-28_

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
- **Video engine software (REQ-0004):** Hoang wants a REUSABLE video editor app, not one-off videos. The tutoring-web CTO session owns it, in `tutoring/video-engine-software/` (spec on branch spec/editor, `docs/specs/video-engine/`).
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
