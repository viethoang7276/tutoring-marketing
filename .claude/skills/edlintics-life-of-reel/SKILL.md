---
name: edlintics-life-of-reel
description: Make one Edlintics "A day in the life of a [role]" reel (9:16, 30-40 s) end to end. Covers the script from the template, the scene presets, a one-command build, the checks, the Canva draft with music and the hub proposal card. Structure is a hook, 3-4 relatable moments, the turning moment, one named concept, the business lesson and an end card. Written step by step for a cheaper model. Engine: edlintics-explainer-reel.
---

# Edlintics "life of" reel

You produce one reel and one `status: "proposal"` card in the hub. Nothing is posted; Hoang approves on the Review board.
- **Worked example:** `example-accountant.json` ("An accountant at month-end", teaching accruals; validates with no WARN, 38 s).
- **Blank to fill:** `template.json`.
- **Engine:** `.claude/skills/edlintics-explainer-reel/scripts/` (called `$E` below).

Set these first:
```
REPO=/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing
E=$REPO/.claude/skills/edlintics-explainer-reel/scripts
PY=$REPO/tools/tts/.venv/bin/python
W=<scratchpad>/reel/<slug>          # one folder per reel
```

## What makes it work
- **People recognise their own day.** Use real, specific details: the 8 a.m. coffee, 200 invoices, a group chat at midnight. That's why viewers tag a friend.
- **Situational humour only.** The joke is the situation, never the person or the job. Never mock accountants, salespeople, students or any role.
- **One named concept is the payoff.** Every episode teaches exactly one, shown on the end card.

## Steps
1. **Pick the role and concept.** Take them from the topic bank below, or use the ones you were given. One concept per episode. If the hub already has a slot on the same concept, stop and report.
2. **Write the script.** Run `mkdir -p $W && cp template.json $W/script.json` and fill every `<...>`. Copy the patterns in `example-accountant.json`.
   - **Beat roles, in order:** hook (1), moment (3-4), turn (1), concept (1), lesson (1-2), optional loop (1), endcard (1, always last).
   - **The hook** must say "A day in the life of <a role>", plus when: at month-end, before the exam, on launch day.
   - **Moments:** short, specific and relatable, ideally with a number. The last moment is where the problem appears, often someone suggesting the wrong move.
   - **Turn:** Ledger explains why the wrong move is wrong.
   - **Concept:** "That is <concept>. <It in one plain sentence>."
   - **Lesson:** what it changes in business.
   - **End card:**
     - `"term"` is the concept; `"keypoint"` is one line to remember (4-12 words, no full stop);
     - `"text"` is "<Concept>. <Key point as a sentence>.";
     - the voice must say the term.
   - **Voice `text`:**
     - full sentences, with amounts spelled out ("twelve hundred dollars");
     - US dollars only; no exclamation points, emoji or tutoring.
   - **Caption `chunks`:**
     - 2-5 words each, with numbers as "$1,200";
     - one `key` per beat;
     - no full stop at the end.
   - **Totals:** about 100-115 words, 9-13 beats, and 12 words or fewer per beat.
3. **Compose the scenes.** Use presets only (`$PY $E/scene_lib.py --list`).
   - **Dress Ledger for the role** with `outfit`:
     - `suit` for an accountant, analyst or manager;
     - `sales` for a salesperson (with headset);
     - `student` for a student (hoodie and backpack);
     - `casual` for a founder or intern.
   - **Useful backgrounds:** `office`, `classroom`, `lecture` (lecture hall), `home` and `street`.
   - **Useful props:**
     - `person` (a colleague, customer or classmate; `color` sets their shirt), `people_group` (a group project; `busy` = how many do all the work);
     - `speech`, `thought` (with `inner`), `phone` (screen `call`/`chat`), `laptop` (screen `sheet`);
     - `calendar` (`mark` circles a day), `clock` (`hour`), `invoice`, `coffee`, `bed`, `school_desk`, `whiteboard`, `funnel` (`top`/`bottom` dots); never `handshake` next to Ledger (its small drawn hands never match his; show a deal with `invoice` `stamp: true` or a `check`);
     - `chart` (`trend`), `check` and `cross`.
   - **Placement:** Ledger's (x, y) is between his feet, and the ground is at y 1480. Every other prop's (x, y) is its centre. Give an `id` to anything the frame should show.
   - **Ledger size is automatic (Ledger-first framing, 25 Oct 2026):** stand Ledger anywhere on the ground (y 1470) at any `s`; the build sizes the frame from Ledger so he fills 74-88% of the frame height, then nudges or shrinks props that would fall outside. You do not need to hand-tune `s` or y. A `desk` (set `w`, default 880; 360 = a short desk) may run off the frame edges as a cropped desk edge. Props never go under the caption band.
   - **Held props:** put a prop at Ledger's hand at about 0.5-1.2x his body width (for Ledger `s` 2.3: prop `s` 0.6-0.8). The build WARNs if a held prop would make the hand look tiny or the prop a speck.
   - **Food and everyday props:** `pizza` (`slices` left, 0-8), `pizza_slice` (`bite`, `rot`), `sandwich`, `burger`, `plate` (`item` none/slice/crumbs), `lemonade_cup`, `lemonade_stand`, `groceries_bag`, `receipt`, `gym`, `bus` (`flip`).
   - **`frame`:** leave it out (Ledger-first is the default). Overrides: `content` (fit everything, Ledger may get small), `ledger-close`, `item:<id>`, `items:<id>,<id>`, `wide`, `ledger` or `[x, y, w, h]`. There are no camera moves.
4. **Validate and build.** Run `$E/make_reel.sh $W <slug>`. Fix any `FAIL` line and run it again. Output: `<slug>.mp4`, `<slug>-voice-only.mp4`, `<slug>-canva-upload.mp4` and `<slug>-contact-sheet.png`.
5. **Check by eye.** Use the contact sheet:
   - the role is clear from the first frame;
   - Ledger is big and recognisable;
   - **hands proportional:** in every scene Ledger's hands and arms match the brand proportions (hand about the size of his eye-to-eye gap, arms no longer than his body is tall), and anything he holds is in scale with his hand (Hoang, 25 Oct 2026: check this every time);
   - no art sits under the captions;
   - the end card reads well.
   If a prop hides under the captions or a hand looks off, fix the scene (see Compose) and rebuild (about 2 min; add `REUSE_AUDIO=1` before the command when only the pictures changed).
6. **Canva draft with music:** follow edlintics-definition-reel step 6 exactly:
   - `copy-design` `DAHZALJdKoM`, open `/design/<id>/edit`, click Uploads, then `find` "file input button" (the first `find` may return the search box; ask again) and upload `<slug>-canva-upload.mp4` (10 MB cap), open the Videos tab, wait for the thumbnail to show its length, then click the old video on the page, **Replace**, and your thumbnail. The upload library is shared, so pick the thumbnail whose length matches your video;
   - Edit as video, delete any old video layer, and check the total equals the video length;
   - if the total is short, extend the clip with the scissors trim; set the music Volume to 8 (video stays at 100);
   - rename it "Explainer reel - Life of <role> (Ledger) v1" (File menu, the name field at the top), check "All changes saved", then `move-item-to-folder` to `FAHYcHrS5PE`.
7. **Upload the video to the hub:** follow edlintics-definition-reel step 7 (Artifact publish, `asset: true`, the MP4 plus a poster JPEG). Make the poster from the still with the lowest time in `$W/stills/` (sort numerically, not alphabetically) and name it `<slug>-poster.jpg`.
8. **Hub proposal card:** follow edlintics-definition-reel step 8, with these differences:
   - slot id = the slot id you were given (else `lifeof-<slug>`); also set `id`, `reviewId` (= slot id), `image: "draft"`, `text: "ready"`;
   - `reelType: "life-of"`;
   - `test: "H14"`, plus `test2: "H12"`;
   - `title` "A day in the life of <role>: <concept>".
9. **Report:**
   - the slot id, Canva id and length;
   - the contact sheet path;
   - any WARN lines left.

Threads topic: use the primary arm in week 1 (mapping in `docs/research/2026-10-24-threads-topics-communities.md`). A sales or marketing reel maps to the Marketing community, which needs Hoang's approval to join, so use the topic Business and say so in `threadsReason`.

## Topic bank (one concept each; none duplicates a carousel, puzzle or definition reel up to 1 Nov 2026)
| Role and moment | Concept | The turning moment |
|---|---|---|
| An accountant at month-end | Accruals | The October bill arrives in November (worked example) |
| A salesperson on a Monday | Conversion rate | 40 calls, 8 meetings, 2 deals, so 5% |
| A business administration student in a group project | Free-rider problem | Five names on the slide, one person did the work |
| An economics student at the pizza night | Diminishing marginal utility | The fourth slice is worth less than the first |
| A startup founder checking the bank account | Burn rate and runway | $60,000 a month and $300,000 left means 5 months |
| A shop owner pricing a new mug | Markup vs margin | A 50% markup is only a 33% margin |
| An auditor at year-end | Materiality | A $3 error in $40 million of sales |
| A supply chain manager before the holidays | Lead time | The order needs 6 weeks, not 6 days |
| An HR manager after a resignation | Cost of employee turnover | Hiring and training cost a year's salary |
| A financial analyst building a portfolio | Diversification | Not all eggs in one basket |
| A marketing intern testing two emails | A/B testing | Change one thing at a time |
| A café owner looking at the electricity bill | Fixed vs variable costs | Rent stays, milk grows with sales |
| A data analyst at a team meeting | Correlation vs causation | Ice cream sales and sunburn |

## Ledger is not required in every scene (Hoang, 25 Oct 2026)
Use scenario graphics that show the idea directly: a computer, code on a screen, a robot arm, a chessboard, a toddler with blocks, a meeting table, a store, a chart. Ledger appears where a character helps the story, typically the hook, a story beat and the takeaway, but scenes without Ledger are welcome. Scenes without Ledger use the renderer's content fit and still keep the art big. Add simple hand-drawn presets when a scenario needs one.
