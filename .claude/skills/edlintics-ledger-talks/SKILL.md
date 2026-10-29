---
name: edlintics-ledger-talks
description: Make one "Ledger talks" reel, Edlintics' face-free version of the creator talking-to-camera format. Ledger faces the viewer holding a small mic, lip-synced to the Kokoro voice, on a campus backdrop, with big 1-3 word karaoke captions and jump cuts between gestures. The end card shows the term and the key point. Used for advice, opinion and "here is an idea" posts. Written step by step for a cheaper model. Engine: edlintics-explainer-reel.
---

> Hoang rejected this format on 25 Oct 2026. Don't use it unless he asks for it again; use the illustrated definition or life-of style.

# Ledger talks (test format T1, 25 Oct 2026)

**What it copies from the reference:** the format only, never the words or visuals. The reference is a creator outdoors with a lapel mic, captions of 1-2 words at a time low on screen, no music and a high save rate.
- **Ledger stands in for the face**, because Hoang never appears.
- **Worked example:** `example-moravec.json` ("The skills that pay are flipping", Moravec's paradox; 36 s, slot `test-ledger-talks-moravec`).
- **Blank to fill:** `template.json`.
- **Engine:** `.claude/skills/edlintics-explainer-reel/scripts/` (`$E`). Set REPO, E, PY and W as in edlintics-life-of-reel.

## What the engine does for `meta.type: "ledger-talks"`
- **Frame:** the art fills the whole 9:16 screen, and Ledger is framed the same in every scene:
  - he is about 80% of the screen width with his arms;
  - his feet are at screen y 1360 and his mouth at about y 1010;
  - the frame never moves (no camera moves).
- **Lip sync:** mood `talk` has an open and a closed mouth. The renderer opens it whenever the voice is loud, at 12 fps.
- **Jump cuts:** a new beat may switch scenes to change the gesture. There's no fade and no draw-on after the first beat, like a talking-head edit.
- **Captions:**
  - white Inter 900 at 112 px with a navy outline, the key word in yellow;
  - centred at y 1110-1340, over Ledger's chest, never his face;
  - the logo sits small at the top (y 262).
- **Sound:** voice only, with no whoosh and no music bed (the reference has none). The Canva copy also has no music.

## Steps
1. **Topic:**
   - an argument or a list with one clear idea per beat, true and useful for a general audience;
   - from one of Hoang's references, paraphrase the argument in our own words with a business angle. Never reuse the creator's sentences. Check every fact (dates, names) and record the source in `maths_check` and the slot `sources`;
   - don't name the creator in the public caption unless Hoang decides to; put the credit in the slot `sources`.
2. **Script:** `cp template.json $W/script.json` and fill it.
   - **Roles, in order:** hook (1), point (3-10), takeaway (1), optional loop, endcard (always last).
   - **Voice:** full sentences, US dollars spelled out, about 80-105 words in total (validator target; 25-36 s at speed 1.12). Keep each beat to 12 words or fewer.
   - **Caption chunks:** **1-3 words** each, one `key` per beat, no full stop.
   - **End card:** `term` is the idea's name or the list title; `keypoint` is 4-12 words with no full stop; the voice says the term.
   - **Definition check (Hoang, 29 Oct 2026):** before you build, run the `definition-reviewer` agent (`.claude/agents/definition-reviewer.md`) on `script.json`: the any beat that says what a term is or means, the end card `term` and `keypoint`, and the caption. Every term must PASS against at least 2 online sources; apply each FIX wording and run it again. The end card must show a real definition or a key point that follows one, never only a takeaway. Put the source URLs in the slot `sources` and the result in `definition_check`.
3. **Scenes:** every scene uses `bg: "campus"` and Ledger at x 540, y 1470, s 2.4, `mood: "talk"`, `arm: "mic"`, outfit `casual` (or the outfit that fits the speaker).
   - **Vary the left arm (`larm`) each beat** for natural gestures: `open_l` (explaining), `point_l` (pointing), `up_l` (an idea or number one), `shrug_l` (a surprise), `down`.
   - **Optional props:** one small prop per scene at x 800, y 860-880, s 0.45-0.8 (beside his head, top right): `laptop`, `books`, `check`, `speech`, `invoice` (stamp), `price_tag`, `chart`. No other props: they get cut off.
4. **Build:** run `$E/make_reel.sh $W <slug> 1.12`. Fix any FAIL and rebuild. If only the pictures changed, add `REUSE_AUDIO=1` (about 3 min).
5. **Check by eye, on the contact sheet:**
   - the mouth is visible above the captions;
   - hands are in proportion and the mic sits at his mouth, not his eye;
   - props aren't cut off;
   - the end card reads well.
6. **Canva:** follow edlintics-definition-reel step 6, with one difference: after Replace, select the music track in the timeline and delete it (this format has no music). Rename it "Test format - Ledger talks - <topic> v1" and file it in FAHYcHrS5PE.
7. **Hub:** upload the video and poster, and create the slot, as in edlintics-definition-reel steps 7-8:
   - `format: "explainer-reel"`, `reelType: "ledger-talks"`, `status: "proposal"`;
   - `test: "T1-ledger-talks"` with its hypothesis;
   - a free time slot (an extra post), checked against the day's slots.

## Hypothesis T1
An advice or opinion reel by Ledger gets a higher save rate (saves per 1,000 views) than our definition reels. Judge it in the weekly review after 3 posts.
