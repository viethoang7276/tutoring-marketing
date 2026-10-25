---
name: edlintics-definition-reel
description: Make one Edlintics definition explainer reel (9:16, 30-40 s) end to end. Covers the script from the template, the scene presets, a one-command build, the checks, the Canva draft with music and the hub proposal card. Structure is hook, everyday story, one-sentence definition, business example, takeaway and end card. Written step by step for a cheaper model. Engine: edlintics-explainer-reel.
---

# Edlintics definition reel

You produce one reel and one `status: "proposal"` card in the hub. Nothing is posted; Hoang approves on the Review board.
- **Worked example:** `example-sunk-cost.json` (sunk cost v5).
- **Blank to fill:** `template.json`.
- **Engine:** `.claude/skills/edlintics-explainer-reel/scripts/` (called `$E` below).

Set these first:
```
REPO=/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing
E=$REPO/.claude/skills/edlintics-explainer-reel/scripts
PY=$REPO/tools/tts/.venv/bin/python
W=<scratchpad>/reel/<slug>          # one folder per reel
```

## Steps
1. **Pick the topic.** Take it from the topic bank below, or use the one you were given. If the hub already has a slot on the same term (check `slots` titles), stop and report.
2. **Write the script.** Run `mkdir -p $W && cp template.json $W/script.json` and fill every `<...>`. Copy the patterns in `example-sunk-cost.json`.
   - **Beat roles, in order:** hook (1), story (2-4), definition (1), example (2-3), takeaway (1), optional loop (1), endcard (1, always last).
   - **Voice `text`:**
     - full sentences, calm and plain, as if to a smart 15-year-old;
     - amounts spelled out ("sixty dollars"), so Kokoro reads them right;
     - US dollars only; no exclamation points, emoji or tutoring.
   - **Caption `chunks`:**
     - 2-5 words each, taken from the voice line, with numbers as "$60";
     - one chunk per beat has `key` (a word inside that chunk);
     - no full stop at the end; a question mark is fine.
   - **End card:**
     - `"term"` is the term; `"keypoint"` is one line to remember (4-12 words, no full stop);
     - `"text"` is "<Term>. <Key point as a sentence>.";
     - the voice must say the term.
   - **Totals:** about 100-115 words, 9-13 beats, and 2-4 s of voice per beat (12 words or fewer).
3. **Compose the scenes.** Each scene is `{"bg", "items": [...]}` (an optional `"frame"`), built from presets only. Never write SVG.
   - Run `$PY $E/scene_lib.py --list` to see every preset and option.
   - **Ledger:** `{"p": "ledger", "id": "led", "x": 540, "y": 1470, "s": 2.2, "mood": "smile", "arm": "down", "outfit": "suit"}`. (x, y) is between his feet, and the ground is at y 1480. Use `"flip": true` to make him face left.
   - **Other props:** (x, y) is the centre. Give an `id` to anything the frame should show.
   - **`frame`:** leave it out. The default auto-fits the drawn scene to about 70% of the frame width without clipping Ledger. Only add one (`ledger-close`, `item:<id>`, `items:<id>,<id>`, `wide`, `ledger` or `[x, y, w, h]`) for a deliberate close-up. There are no camera moves.
   - **Keep Ledger big:** auto-fit sizes the whole drawing to 70% of the width, so wide props (desk, scale, `people_group`, `building`) shrink him. Use Ledger `s` 2.4-2.6 with one or two small props (scale `s` 0.7 with its pivot y about 1270, `person` `s` 1.5), not a desk or `people_group`.
   - **One clear action per scene, and no text inside the art.** Reuse a scene for two beats if it fits; it stays the same frame.
4. **Validate and build.** Run `$E/make_reel.sh $W <slug>`. It stops at the first problem with clear `FAIL` lines; fix the script and run it again. WARN lines are advice.
   - Output in `$W`:
     - `<slug>.mp4` (for preview);
     - `<slug>-voice-only.mp4`;
     - `<slug>-canva-upload.mp4` (under 10 MB);
     - `<slug>-contact-sheet.png`.
   - The build takes about 75 s.
5. **Check by eye.** Open the contact sheet and check each of these:
   - Ledger is recognisable and big in every scene, and nothing important is cut off at the frame edge;
   - no art sits under the caption;
   - the end card reads well;
   - each caption matches its picture.
   If a scene looks wrong, move the items (x, y, s), or add a `frame` override, then rebuild.
6. **Canva draft with music.** In Chrome, in your own new tab:
   1. Run `copy-design` on the latest reel design, `DAHZALJdKoM` (sunk cost v5, which carries the free Canva track "Light Minimal Ambient"). Open the copy at `https://www.canva.com/design/<id>/edit`.
   2. Uploads › `find` the "file input" › `file_upload` `<slug>-canva-upload.mp4`. The Chrome bridge takes at most 10 MB. The copy opens already in timeline view, with the old video and the music on it; other agents' uploads share the Videos list, so pick the thumbnail whose length matches yours. Wait until the thumbnail shows its length.
   3. Click the video on the page (the old background) to select it, click **Replace** in the toolbar, then click the new thumbnail. The background swaps in place and the music stays. Do NOT click the thumbnail with nothing selected: that appends a second clip and doubles the length (if it happens, press cmd+z).
   4. **Remove any old video.** If the timeline is not already showing, use the page ⋯ menu › **Edit as video**. The timeline must show only the new video and the music. Delete any other video layer (an old reel left on top) and any extra clip after the new one. The total at the bottom right must equal the video length (for example 0:36); the music trims itself to the page.
   5. Rename it: File › pencil › "Explainer reel - <Term> (Ledger) v1". Check it says "All changes saved".
   6. Run `move-item-to-folder` with the design id to `FAHYcHrS5PE`. Close your tab.
7. **Upload the video to the hub so it plays on Hoang's phone.** Use the Artifact tool, publish with `asset: true`:
   - `url` `https://claude.ai/artifact/HbKxzWUcWhaBaaNb9buZM6`;
   - `file_paths`: `<slug>.mp4` and a poster JPEG (make it from the first still by time, `ls $W/stills | sort -V | head -1` (plain `ls` sorts 11.37 before 2.17): `$PY -c "from PIL import Image; Image.open('<first still>').convert('RGB').resize((540,960)).save('$W/poster.jpg', quality=85)"`).
   - Keep the returned `/_blob/...` URLs.
8. **Hub proposal card.** Use ArtifactData `set` on `slots/<slot id>`. The slot id is `reel-<slug>`, or the date-time id Hoang gives. Copy the field names of `explainer-sunk-cost`:
   - **Basics:** `format: "explainer-reel"`, `reelType: "definition"`, `kind: "video"`, `status: "proposal"`, `title`, `family_or_category`.
   - **Time:** `date` (YYYY-MM-DD), `time` and `time_madrid` (for example "08:30"), and `time_vietnam` (Madrid +6 in winter, so 08:30 becomes 14:30).
   - **Copy:** `caption`, `caption_x`, `first_comment`, `hashtags` and `maths_check`, from `meta`.
   - **Threads:** `threadsTopic`, `threadsTopicKind: "topic"`, `threadsTopicVariant` and `threadsReason`.
   - **Link:** `utm.template` with `utm_content=<slot id>`.
   - **Media:**
     - `videoUrl` and `posterUrl` (the `/_blob/` URLs) and `videoAssetId`;
     - `canva` (the design id);
     - `video` (the local path) and `music`.
   - **Script and end card:** `script` (each beat's role, start, text, captions with `t`, from `$W/timing.json`) and `endcard: {term, keypoint}`.
   - **Tests and note:** `test: "H12"`, plus `statusNote` "New <date>: definition reel on <term>, <N> s".
   The Review tab then shows the video with the voiceover lines, the end card, the caption, the first comment and the Threads destination, with Approve and Request changes buttons.
9. **Report:**
   - the slot id, Canva id and length;
   - the contact sheet path;
   - any WARN lines left.

## Topic bank (none duplicates a carousel or puzzle up to 1 Nov 2026)
| Term | Everyday story | Business example |
|---|---|---|
| Break-even point | A lemonade stand covering its $40 stall fee | A café's monthly rent against coffees sold |
| Working capital | Paying rent before payday | A shop paying suppliers in 30 days, collected in 60 |
| Depreciation | A $1,200 laptop losing value each year | A delivery van spread over five years |
| Inflation | The same $5 buying less lunch | Raising prices when costs rise |
| Marginal cost | Baking one more batch of cookies | One more unit off a running line |
| Economies of scale | Buying in bulk | A factory's cost per unit falling as volume grows |
| Fixed vs variable costs | Phone plan vs pay-as-you-go | Rent vs ingredients in a restaurant |
| Liquidity | Owning a house but having no cash for dinner | A profitable firm that cannot pay wages |
| Diminishing returns | The fourth hour of studying | Adding staff to a small kitchen |
| Comparative advantage | Flatmates splitting cooking and cleaning | Countries trading what they make best |
| Sampling bias | Asking only friends if your app is good | A survey sent only to happy customers |
| Moral hazard | Driving carelessly with full insurance | Banks taking risks they expect to be bailed out of |
| Accounts receivable | A friend who owes you $50 | Sales on credit that are not cash yet |
