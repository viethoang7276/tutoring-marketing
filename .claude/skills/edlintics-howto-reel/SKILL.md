---
name: edlintics-howto-reel
description: Make one Edlintics "How [role] in [industry] deals with [problem]" reel (9:16, 60-90 s; every video is capped at 2 minutes from 3 Nov 2026) end to end. Covers research and topic choice (holiday hooks, the concepts registry, authoritative sources), the script from the template, content safeguards, the full-frame layout, the equation scene, the 4-box summary diagram, a one-command build, the checks (contact sheet, frame fill, file size, caption sync) and the hub proposal card. Structure is hook question, the problem with one number, 3-4 steps, the named concept with its definition and equation, the summary diagram, the takeaway and an end card with term, definition and equation. Written step by step for a cheaper model. Engine: edlintics-explainer-reel.
---

# Edlintics "how to" reel

You produce one reel and one `status: "proposal"` card in the hub. Nothing is posted; Hoang approves on the Review board.
- **Worked example:** `example-hr-turnover.json` ("How does a department store's HR team deal with staff who keep quitting?", teaching employee turnover rate; 21 beats, 68 s; output in `assets/renders/howto-reels/w46/howto-hr-turnover/howto-hr-turnover-v3.mp4`).
- **Blank to fill:** `template.json`.
- **Engine:** `.claude/skills/edlintics-explainer-reel/scripts/` (called `$E` below).
- **Topic bank:** `assets/renders/industry-series/proposals.md` and `assets/renders/howto-reels/w46/proposals.md`.

Set these first:
```
REPO=/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing
E=$REPO/.claude/skills/edlintics-explainer-reel/scripts
PY=$REPO/tools/tts/.venv/bin/python
W=<scratchpad>/reel/<slug>          # one folder per reel
```


## Story rules for every reel (Hoang, 3 Nov 2026)
Hoang rejected the posted founder-runway reel because it "doesn't have flow". Read `.claude/skills/storytelling-and-narrative` (the BEATS framework) before you write any script.
1. **One story, not a list of facts.** Use setup, then tension, then the turn, then the payoff. One hero (Ledger in the role) wants something, a problem appears, and the concept resolves it.
2. **Link every beat to the one before.** Start most beats with a linking word: First, Then, So, But, That means, Now. The turn always starts with "But" (or Yet, Still, Instead). The validator warns if fewer than 60% of story beats link.
3. **Tell the story on the timescale of the numbers.** Monthly numbers get a monthly story, such as "today he checks the month", never clock times through one day. Yearly numbers get a year. The validator warns when clock times appear next to per-month or per-year numbers.
4. **Never hide Ledger.** Items draw in list order, so put desks, whiteboards, stands and tables BEFORE Ledger in `items`. The validator fails otherwise. Check the contact sheet: nothing crosses his face.
5. **Each caption chunk makes sense on its own.** Avoid fragments like "just arrived" or "for years".
6. **Length:** every video is 2 minutes or less (Hoang, 3 Nov 2026; this replaces the 1-minute cap). Keep it as short as the story allows.
7. **Full sentences (Hoang, 3 Nov 2026: "Always write full sentence").** Every voice line is a full sentence with a subject and a verb. No fragments like "Eighty out, twenty in." or "Five months, not years." Write "Eighty thousand goes out and twenty thousand comes in." Caption chunks split a full sentence; they never replace it.
8. **Say when the example starts (Hoang, 6 Nov 2026).** The first `problem` beat opens with "Let's imagine an airline where ..." or "For this, let's use the example of ...", straight after the hook question. The validator fails the script otherwise. Full guide: "Context transitions" in the engine skill.

**Direct opening (Hoang, 13 Nov 2026).** New reels open by saying what the video is and then go straight to the point, with no question or teaser hook: see "Direct opening" in the engine skill (`edlintics-explainer-reel`). It does NOT yet apply to how-to reels: the validator still requires the "How does <a role> ... deal with <a problem>?" question in beat 1 (or beat 2-3 with hookStyle B), so keep the question opening until the validator is updated. Reels already scheduled are not changed.

## What makes it work
- **A real job, a real problem.** Viewers see how a named role in a named industry handles something that actually happens: a ransomware attack at a hospital, staff quitting at a store, a restricted donation at a charity.
- **A process they can screenshot.** The 3-4 steps come back as a 4-box diagram that fills the screen.
- **One named concept with its formula.** The concept, its one-sentence definition and (when it has one) its equation with the story's real numbers are the payoff, on screen and on the end card.

## A. Research and topic selection
1. **Pick a role.** Finance, accounting, IT, audit, marketing, HR, procurement, compliance, operations, supply chain, customer experience, risk.
2. **Pick an industry** different from every how-to and industry-series post of the last 30 days (hospital, bus operator, fashion marketplace, airline, department store, charity, bank, football club, drug company, coffee chain…).
3. **Pick a real problem or process** that role handles there, with one number that shows the size of it.
4. **Prefer a holiday or news hook.** Open `docs/content-workflow/holiday-calendar.md`. If a holiday's content window covers the post date, use it (Singles' Day: returns and GMV; Black Friday: loss leaders). Only international events; no national days. Then check `docs/content-workflow/economic-calendar.md`: if the post date falls in an event's posting window and the plan assigns the week's economic post to this reel, follow that file's rules (teach the concept, no forecasts or investment advice). Record the hook in `meta.hook_reason` (or "none").
5. **Registry check.** Read the hub `concepts` collection (rules and queries in `docs/content-workflow/concept-registry.md`; offline, the mirror `docs/content-workflow/concept-registry.json`). The concept is blocked if:
   - the same concept was a main idea in the last 90 days (planned posts count, in both directions);
   - a `related` concept was a main idea in the last 30 days;
   - the same industry ran in the industry or how-to series in the last 30 days;
   - its theme already has 2 posts in the 7 days around the date.
   Write `"registry_check": "registry check: clear"` in meta, or name the conflict and pick another topic. Set `meta.concept_id` (the registry slug), `meta.themes`, `meta.industry` and `meta.role`.
6. **Source every step.** Each step must come from an authoritative source for that process, for example:
   - security incidents: NIST SP 800-61 (Rev. 3 is current; do not call the four-phase cycle "NIST's current lifecycle"), CISA;
   - money laundering and KYC: FinCEN, 31 CFR 1020;
   - labor data and turnover: BLS (JOLTS), SHRM;
   - accounting rules: FASB (ASC) or IFRS; charities: FASB ASU 2016-14 and IRS;
   - prices and market data: a dated official or company filing.
   The definition needs at least 2 reputable sources (CFI, Investopedia, a regulator, a textbook). Put every URL in `meta.sources`.
7. **Write the numbers so they obey the real rule behind the story.** Check each number against the source, not only the arithmetic (lesson from the KYC check: "30 deposits in a month" broke the structuring example; a cash deposit story must stay under or over the real $10,000 reporting line as the story needs). Write every sum and the benchmark that makes it realistic in `meta.maths_check` (example: "120 / 200 = 60%; BLS JOLTS retail separations about 45-48% a year, so 60% is high").

## B. Script
Run `mkdir -p $W && cp template.json $W/script.json` and fill every `<...>`. Copy the patterns in `example-hr-turnover.json`. Keep `"type": "howto"` and `"layout": "full"` in meta.
- **Beat roles, in order:** hook (1; 2-3 for hookStyle B), problem (1-2), step (4-8: each step gets a short "First, …" beat and a detail beat), concept (2-3), summary (4: one per box), takeaway (1), optional loop (1), endcard (1, always last).
- **Hook:** "How does <a role> at <a company type> deal with <a problem>?" The validator checks the wording "How does … deal with". Give it `"gap": 0.35`. Set `meta.hookStyle`:
  - `"A"`: beat 1 is the question;
  - `"B"` (hook test, 1 Nov 2026): beat 1 is a `hook` beat that opens on the problem and its number ("Price a custom bike below cost, and the shop loses money on it."), and the question follows in hook beat 2 or 3. The validator checks both.
- **Problem:** the setting and one number ("This store averages about two hundred staff. Last year, a hundred and twenty left.").
- **Steps (3-4):** "First, …", "Then …", "Next, …", "Finally, …", each followed by a detail line with the numbers in the post's currency.
- **Concept:** "That is <term>." then "It is <one-sentence definition>." Then, when the definition has an equation, one more beat on the `equation` scene that says it in words ("You find it by dividing the people who left by average headcount.") with `"gap": 1.1` so the filled-in numbers stay on screen.
- **Summary (Hoang, 2 Nov 2026):** the voice walks the diagram as a recap: "Let's revise the process. Step 1, measure it." then "Step 2, price it.", "Step 3, find the cause.", "Step 4, fix it and track it." One beat per box, `"gap": 0.45` each, 1.5 on the last. Say "the process" when the boxes are steps the role takes, and "the concept" when they explain how the idea works (the gas-station prisoner's dilemma: map the profits, see the trap, notice the cost, compete on something else). Chunks: `"Let's revise the process"` or `"Let's revise the concept"` (beat 1 only, no full stop), `"Step N"`, then the short step (2-5 words, lower case). Write `"say"` with the number in words ("Step one, …") and `text` with the digit. The validator FAILs a how-to summary without this.
- **Takeaway:** one business lesson. No absolute words: "never", "always", "only", "every", "all", "guarantee" (the validator WARNs). Use rarely, usually, often, can.
- **End card:** only the term, the one-sentence definition and the equation (Hoang, 1 Nov 2026). `"term"`, `"keypoint"` = the one-sentence definition, a full sentence matching the glossary entry (no full stop at the end), `"text"` = "<Term>. <Definition as a sentence>." and, when there is one, `"equation": {"lhs", "num", "den"}` (each 34 characters at most; `den` empty for a one-line equation such as "Profit = Revenue − Costs"). No worked example or numbers line: the validator FAILs an `"example"` or an "=" inside lhs, num or den. The story's numbers stay in the equation scene. When the concept has no equation, set `meta.equation` to "none (...)" and leave `"equation"` out.
- **Length:** about 60-90 s, never over 2 minutes (Hoang, 3 Nov 2026), about 140-220 words, 12-40 beats. The voice is ElevenLabs `eleven_v3`, voice `gPiEpcKoaZywgOzc0Zn9`, tempo 1.12 (the defaults; never set another voice, never print the key).
- **House rules:**
  - One currency in the post, rotated across posts ("four thousand euros" in the voice, "€4,000" in captions); US spelling (labor, analyze, center);
  - voice lines are full sentences; caption chunks are 2-5 words with one `key` per beat and no full stop at the end;
  - no full stop at the end of any on-screen line, caption paragraph or first comment;
  - no exclamation points; emojis only at the end of the first comment; no tutoring.
- **meta:** fill `hookStyle`, `caption` (3 short paragraphs and 4 hashtags), `caption_x` (under 280 characters), `first_comment`, `threadsTopic`, `threadsReason`, `maths_check`, `sources`, `definition_check`, `registry_check`, `equation`.

## C. Content safeguards (before Hoang sees anything)
1. **Definition review gate.** Run the `definition-reviewer` agent (`.claude/agents/definition-reviewer.md`) on `$W/script.json`: the definition, the equation (formula and the filled-in numbers), every step against its process source, every number, the takeaway and the end card. Every item must PASS. Apply each FIX wording and run it again. File the verdicts next to the reel (for example `assets/renders/howto-reels/<week>/definition-check.md`) and point `meta.definition_check` at them.
2. **No absolute claims** in the takeaway or the caption ("never has its own line" became "rarely gets its own line").
3. **Numbers obey the real rule** (A.7). An example that breaks the rule it teaches is a FAIL even when the sum is right.
4. **Sensitive topics** (security, crime, fraud, money laundering, health, safety): describe what the organization does to detect, respond and report, as the official guidance says. Never show how to evade a control (no "stay under $10,000" tricks, no attack steps), and give no advice beyond the official guidance. Name the authority (FBI, FinCEN) only as the guidance does. A ransom is "a demand"; never imply paying.
5. **No real company named** unless a source in `meta.sources` backs the fact. Use a company type ("a department store", "a hospital").
6. **Invented findings stay inside the story** ("exit interviews show schedule changes top the list" is this store's finding, not a general fact).
7. **Music is copyright-safe:** the final track is the free Canva track at volume 8 added in the Canva draft (see edlintics-life-of-reel step 6). For the local preview, `MUSIC_BED` may only point to a track we have the rights to (the Canva "Light Minimal Ambient" export in `assets/renders/money-reels/music/`); holiday reels use only `docs/research/2026-10-31-christmas-music.md`.

## D. Build
### The full-frame layout (Hoang, 1 Nov 2026: "use more of the phone screen")
`meta.layout: "full"` (opt-in; other reel types are unchanged) puts everything inside the platform safe zones (top 220 px, bottom 380 px, right 140 px):
- captions y 228-438 in x 60-920, Inter 900 at 84 px;
- art box x 40-940, y 450-1440 (900x990);
- logo 190 px wide at y 1462;
- end card y 228-1518 in x 60-920: term, rule, definition, equation card, logo.

### Scene presets for how-to reels
Use presets only (`$PY $E/scene_lib.py --list`).
- **Ledger plays the role.** `outfit` `suit` (finance, HR, audit, compliance, manager), `casual` (IT, startup), `sales` (marketing, sales). `lanyard: true` adds a staff ID badge (store, hospital, airline staff).
- **Backgrounds:** `store` (department store floor), `office`, `street`, `home`, `classroom`, `none`, `paper`.
- **Week 46 props** (1 Nov 2026): `brew_tanks` (`n`, `new` adds a dashed tank), `pint`, `share_pie` (`share`, `r`, `mine`, `other` labels), `bike` (`frame_only`), `tool_wall` (overhead), `parcel` (`n`, `ret` return arrow), `network` (`n` users with every pair joined, `color`), `school` (`roof` leak, build, new), `money_jar` (`lock`, `tag`), `gas_station` (`price`, `color`), `payoff_grid` (2 x 2 game, profit a day; `circle` the both-low box, `ch` 300 fills a full-frame scene, `cells` to reveal it row by row), and the phone screen `pay`. The `equation` prop also takes `terms` (a stacked sum, in formula and numbers mode).
- **How-to props:** `name_board` (staff tags, `filled` of `n`), `clothes_rack`, `calculator` (`display` "60%", the one number allowed in the art), `job_ad`, `manual`, `clipboard`, `headcount` (`n` figures, `left` leaving, with a split bar), `door` (`ajar`), `person` (`carry: "box"`, an employee leaving), `speech` (`inner` preset), `calendar` (`weeks` filled), `chart` (`trend`, `color`), `coins`, plus every explainer prop.
- **Framing in the full layout:**
  - leave `frame` out on scenes with Ledger: Ledger-first framing sizes him at 66-78% of the 990 px box height; put props ABOVE him (y 650-900) and beside him, not only beside him;
  - for a designed scene, set `"frame": [40, 450, 900, 990]`: then art coordinates equal screen pixels, so place items directly in the box x 40-940, y 450-1440;
  - for a designed scene with a ground (a `bg` other than `none`, whose ground line is at y 1480), use `"frame": [40, 530, 900, 990]` so the ground lands at screen y 1400, above the logo;
  - Ledger's (x, y) is between his feet; every other prop's (x, y) is its centre; `s` 2.3-2.6 for Ledger in a designed scene.
- **State changes inside a scene:** `"at": "chunk:N"` pops an item in on caption chunk N (chunks count over the beats that share the scene); `"until": "chunk:N"` hides it; `"pop": "cut"` swaps at once (the calculator going from "120÷200" to "60%").

### The equation scene
Two `equation` items on a scene with `"bg": "none"` and `"frame": [40, 450, 900, 990]`:
```
{"p": "equation", "id": "f", "x": 490, "y": 660, "mode": "formula", "lhs": "Turnover rate", "num": "People who left", "den": "Average headcount", "w": 860},
{"p": "equation", "id": "n", "x": 490, "y": 1170, "mode": "numbers", "num": "120", "den": "200", "result": "60%", "note": "in one year", "w": 800, "at": "chunk:2"}
```
- `formula` writes "lhs =" over a hand-drawn fraction (num over a wavy bar over den). With `"den": ""` it writes one line, "lhs = num". For a sum too long for one line, give `"terms": ["Materials", "+ Labor", "+ Overhead rate × hours"]`: "lhs =" with one term per line (num and den are then ignored).
- `numbers` writes the story's numbers as a fraction, "=", and the result with a yellow highlighter swipe; `note` states the period. It pops in on the chunk that says the denominator.
- Both shrink to fit `w`. They are drawn in the art, so they boil and draw on like the rest of the picture.

### The summary diagram
A scene with `"bg": "none"`, `"frame": [40, 450, 900, 990]`, `"pointer"` and four `flow_box` items, w 700, h 200, at x 580, y 555, 815, 1075, 1335:
- boxes 1-4 have a `"ghost": true` copy (grey dashed outline with the number) under them and a `flow_arrow` (x 580, y = box y − 156, dy 40) with no `at`, so the whole diagram fills the screen from the first summary beat;
- **the pointer** (Hoang, 1 Nov 2026): `"pointer": true` or `{"outfit": "suit", "lanyard": true}` (match the reel's Ledger) adds a small Ledger (s 0.8) left of the boxes who points at each box while the voice names it. The engine (`scene_lib.summary_pointer`) places one Ledger per real box with his hand on the box's left edge, shown from that box's `at` chunk to the next box's (a cut), so he steps box to box in sync with the voice. He stands in x 60-200, inside the safe area and off the box text; the validator FAILs a pointer scene whose boxes start left of x 220 (so keep w 700 at x 580). Without `pointer` the old full-width layout (w 880 at x 490) still works;
- the real boxes pop in on their "Step N" chunk as the voice names each step: with the recap chunks above that is box 1 `"at": "chunk:1"`, box 2 `"chunk:3"`, box 3 `"chunk:5"`, box 4 `"chunk:7"` (chunk 0 is "Let's revise the process");
- `title` 1-3 words, `sub` the key point in 2-4 words; text grows with h and shrinks to fit w.
Copy the block from `template.json`.

### Commands
Set `MB=$REPO/assets/renders/money-reels/music/light-minimal-ambient-bed.wav` (the preview music; the audio mix is made only when the voice is made, so pass it from the first run).
1. **Stills first (cheap check):** `MUSIC_BED=$MB STILLS_ONLY=1 $E/make_reel.sh $W <slug>`. This validates, voices every line (ElevenLabs caches each line in `tools/tts/cache-eleven/`, so an unchanged line costs nothing), renders one still per beat, the contact sheet and the frame-fill report. Fix any `FAIL` line and run again.
2. **Pictures only after a scene change:** `REUSE_AUDIO=1 STILLS_ONLY=1 $E/make_reel.sh $W <slug>`. Use it whenever the voice text is unchanged; it keeps the voice and timings. If you add, remove or reword a beat, run without `REUSE_AUDIO` and with `MUSIC_BED=$MB` (only the changed lines are voiced again).
3. **Full build:** `REUSE_AUDIO=1 $E/make_reel.sh $W <slug>` (or `MUSIC_BED=$MB $E/make_reel.sh $W <slug>` if the voice changed). Output: `<slug>.mp4` (voice and preview music), `<slug>-voice-only.mp4`, `<slug>-canva-upload.mp4`, `<slug>-poster.jpg`, `<slug>-contact-sheet.png`.
4. **Cover:** `cd $E && SCENES=$W/scenes.json node make_cover.js 2.0 $W/<slug>-cover.png "How <role> deals with it" "<3-6 word title with one *keyword*>"`. The cover fits the full layout under the title.

## E. Checks (every build)
1. **Contact sheet** (`<slug>-contact-sheet.png`), by eye:
   - the role and the problem are clear from the first frame;
   - Ledger is big, accurate to `assets/brand/ledger.svg`, and his hands are proportional (hand about his eye-to-eye gap, arms no longer than his body; held props in scale);
   - no art under the captions, nothing over the logo, no prop cut off at the frame edge;
   - the equation beat shows the formula and the filled-in numbers with the period;
   - the summary shows all 4 boxes (ghosts first) and they fill the screen, with the small Ledger pointing at the box being named and not covering any text;
   - the end card shows the term, the definition and the equation card, with no worked example.
2. **Frame fill** (printed at the end of `make_reel.sh`, or run `$PY $E/framefill.py $W`): the mean share of the safe area covered by the content must be at least 75% (FAIL under), and no beat may put more than 2% of its ink in the UI zones. The sample went from 63.6% (old layout) to 80.1%. If it FAILs, make the scenes bigger: raise `s`, move props up into the empty band, or use a designed frame.
3. **Under 10 MB:** `postcheck.py` FAILs if the Canva upload copy is 10 MB or more. `build.sh` lowers the bitrate for long reels so both the Canva copy and `<slug>.mp4` stay under 10 MB.
4. **Caption sync:** `framefill.py` FAILs if any caption chunk starts outside its own voice line. Also play `<slug>-voice-only.mp4` once and check that each key word lights up as it is said, and that the equation numbers appear as the denominator is spoken.
5. **Validator WARNs:** fix every WARN you can; report the rest.

## F. Hub proposal card
Upload the video and poster (edlintics-definition-reel step 7), then make the Canva draft with music (edlintics-life-of-reel step 6) only when Hoang asks. Then write `slots/<slot id>` as in edlintics-definition-reel step 8, with these differences:
- slot id = the slot id you were given (else `howto-<slug>`); also `id`, `reviewId` (= slot id), `image: "draft"`, `text: "ready"`;
- `format: "explainer-reel"`, `reelType: "howto"`, `kind: "video"`, `status: "proposal"`;
- `title` "How <role> at <company type> deals with <problem>: <term>";
- `concept` (the registry slug), `themes`, `industry`, `role`, `equation` (from meta), and the line `registryCheck: "registry check: clear"`;
- `script` (each beat's role, start, text and captions with `t`, from `$W/timing.json`) and `endcard: {term, keypoint, equation}`;
- `caption`, `caption_x`, `hashtags`, `maths_check`, `sources`, `definition_check`;
- **Threads:** `threadsTopic` (or `threadsCommunity`), `threadsTopicKind`, `threadsTopicVariant` and `threadsReason`, a one-line reason (map in `docs/research/2026-10-24-threads-topics-communities.md`; a community not yet joined needs Hoang's approval, so use the closest topic and say so);
- **First comment:** 1-2 sentences, under 150 characters, a question that does not give the answer away, ending with 1-3 emojis (the only place emojis are allowed), no UTM tags; if it mentions edlintics.com, add `first_comment_igtt` ending "link in bio";
- `test: "H12"`, plus `statusNote` "New <date>: how-to reel on <term>, <N> s";
- after Hoang approves or schedules it, log the use in hub `concepts` (concept-registry.md, "Log the use").

## Report
- the slot id, length and file paths (video, contact sheet, cover);
- the frame-fill mean;
- the definition-reviewer verdict;
- any WARN lines left.
