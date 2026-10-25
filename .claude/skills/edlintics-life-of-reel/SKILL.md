---
name: edlintics-life-of-reel
description: Make one Edlintics "A day in the life of a [role]" reel (9:16, 30-40 s) end to end. Covers the script from the template, the scene presets, a one-command build, the checks, the Canva draft with music and the hub proposal card. Structure is a hook, 3-4 relatable moments, the turning moment, one named concept, the business lesson and an end card. Written step by step for a cheaper model. Engine: edlintics-explainer-reel.
---

# Edlintics "life of" reel

You produce one reel and one `status: "proposal"` card in the hub. Nothing is posted; Hoang approves on the Review board.
- **Worked example:** `example-accountant.json` ("An accountant at month-end", teaching accruals).
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
     - `calendar` (`mark` circles a day), `clock` (`hour`), `invoice`, `coffee`, `bed`, `school_desk`, `whiteboard`, `funnel` (`top`/`bottom` dots), `handshake`;
     - `chart` (`trend`), `check` and `cross`.
   - **Placement:** Ledger's (x, y) is between his feet, and the ground is at y 1480. Every other prop's (x, y) is its centre. Give an `id` to anything the frame should show.
   - **`frame`:** one per scene: `ledger`, `ledger-close`, `wide`, `item:<id>` or `items:<id>,<id>`. There are no camera moves.
4. **Validate and build.** Run `$E/make_reel.sh $W <slug>`. Fix any `FAIL` line and run it again. Output: `<slug>.mp4`, `<slug>-voice-only.mp4`, `<slug>-canva-upload.mp4` and `<slug>-contact-sheet.png`.
5. **Check by eye.** Use the contact sheet:
   - the role is clear from the first frame;
   - Ledger is big and recognisable;
   - no art sits under the captions;
   - the end card reads well.
6. **Canva draft with music:** follow edlintics-definition-reel step 6 exactly:
   - copy `DAHZALJdKoM`, upload `<slug>-canva-upload.mp4` (10 MB cap), set it as background;
   - Edit as video, delete any old video layer, and check the total equals the video length;
   - rename it "Explainer reel - Life of <role> (Ledger) v1", then move it to `FAHYcHrS5PE`.
7. **Upload the video to the hub:** follow edlintics-definition-reel step 7 (Artifact publish, `asset: true`, the MP4 plus a poster JPEG).
8. **Hub proposal card:** follow edlintics-definition-reel step 8, with these differences:
   - `reelType: "life-of"`;
   - `test: "H14"`, plus `test2: "H12"`;
   - `title` "A day in the life of <role>: <concept>".
9. **Report:**
   - the slot id, Canva id and length;
   - the contact sheet path;
   - any WARN lines left.

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
