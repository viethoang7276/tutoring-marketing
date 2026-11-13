---
name: edlintics-ladder-reel
description: Make one Edlintics career-ladder reel (9:16, 90 seconds or a little under, 2-minute cap), such as "From audit intern to CFO, the career ladder explained with Ledger in 90 seconds", end to end. Ledger climbs five rungs and wears a different outfit on each; every rung shows what the job is, with duty chips, moving props and a recurring slider. Covers the career and its sources, the registry check, the script from the generator, the full-bleed layout, the build, the checks, the thumbnail, the Canva draft with music and its export, and the hub proposal card. Written step by step for a cheaper model. Engine: edlintics-explainer-reel.
---

# Edlintics career-ladder reel

You produce one reel, its thumbnail, a Canva draft with music (exported), and one `status: "proposal"` card in the hub. Nothing is posted or scheduled; Hoang approves on the Review board.
- **Worked example:** `example-audit-intern-to-cfo.py` (the generator) and `example-audit-intern-to-cfo.json` (the script it writes; 23 beats, 84 s).
- **Helpers:** `ladder_script.py` draws everything that is the same in every ladder reel (room, title scene, climbs, payoff, closing scene, title and closing beats); `thumbnail_spec.py` writes the thumbnail spec; `make_card.py` builds the hub card document.
- **Blank to fill, if you prefer JSON:** `template.json` (the example with every text replaced by `<...>`). The generator is easier: use it.
- **Engine:** `.claude/skills/edlintics-explainer-reel/scripts/` (called `$E` below). Reels built with this skill: audit intern to CFO, marketing intern to CMO, junior analyst to chief investment officer, consulting analyst to partner (13 Nov 2026; folders in `assets/renders/ladder-reels/`).

Set these first:
```
REPO=/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing
E=$REPO/.claude/skills/edlintics-explainer-reel/scripts
K=$REPO/.claude/skills/edlintics-ladder-reel
PY=$REPO/tools/tts/.venv/bin/python
SLUG=ladder-<from>-to-<to>            # for example ladder-audit-intern-to-cfo
W=<scratchpad>/reel/$SLUG             # one work folder per reel
D=$REPO/assets/renders/ladder-reels/$SLUG   # the finished package (gitignored)
```

## What Hoang asked for (his words)
- 12 Nov 2026, on the reference reel "Engineering intern to CTO": "I like they move sub to the bottom half, more animation". Then: "Use Ledger as the storyline, generate different version of Ledger. Give me a video preview".
- 13 Nov 2026, on the first preview: "make the video take up the whole vertical screen, the sub will be on top as usual, at the end dont show the definition but show to climb your career ladder, learn technical business cocept at Edlintics".
- 13 Nov 2026, on the second preview: "I like this, generate two more ladder climb ... Generate thumbnail for each following our style, put it on the artifact for approval. Save this as a new skill so cheaper model can perform like opus".
- 13 Nov 2026, on the opening: "I think we should avoid the hook and go directly to the point like these video? Like Bid-Ask Spread explained with Ledger in 90s, Understand a day in the life of a manager in ..., avoid the hook just go directly to the point".
- 13 Nov 2026: "We will post 3 more ladder career next 3 days. Design a test to check effectiveness" (test L1).

What that means for every ladder reel:
1. **One hero.** Ledger is the only main character. He climbs five rungs and looks different on each (clothes and accessories), still clearly Ledger.
2. **Full-bleed art.** The wall and floor fill 1080x1920. No panel, no empty paper band.
3. **Captions in the middle of the bottom half** (y 1320-1530), on a soft paper backing. Hoang, 13 Nov 2026, after approving the first reels with captions on top: "I want it to be at the center of bottom half rather than at the top", then "make it the rule for all videos now". `write()` in `ladder_script.py` does this by default (`meta.caption_pos: "low"`); `write(..., caption_pos="top")` keeps the old band (y 228-438) and is only for reproducing reels rendered before the rule (audit, marketing, analyst, consulting).
4. **Direct opening, no hook.** Beat 1 is a title card that says what the video is. Beat 2 starts the first rung.
5. **No definition card at the end.** The reel ends on the call to action "To climb your own career ladder, learn technical business concepts at Edlintics".
6. **More animation.** Every voice line has its own prop that moves on the word.
7. **Only claim a length the video has.** "In 90 seconds" needs a video of 90 s or less.

## Steps
1. **Pick the career and its five rungs.** Use real job titles, bottom rung first (for example intern, senior, manager, controller, CFO). Find at least 2 reputable sources (WebSearch, then WebFetch to open them) for the rung names and for what each rung does. Keep the URLs. Only list a source you opened; mark a source seen only as a search snippet.
2. **Registry check.** Read the hub `concepts` collection (rules in `docs/content-workflow/concept-registry.md`). A ladder reel teaches no named concept, so:
   - do not name or define a concept that was a main idea in the last 90 days, or that is scheduled (describe the duty in plain words instead, for example "decides which numbers are big enough to test" and never "materiality");
   - theme `career-ladder` plus one career theme (`audit`, `marketing-careers`, ...); the theme cap is 2 posts in any 7 days unless Hoang clears more, as he did for 13-16 Nov 2026;
   - write the result in `meta.registry_check` ("registry check: clear ..." or the conflict), and set `meta.concept_id` (`career-ladder-<from>-to-<to>`) and `meta.themes`.
3. **Write the script with the generator.** `mkdir -p $W && cp $K/example-audit-intern-to-cfo.py $W/gen.py`, then change the parts marked CHANGE and the scenes, beats and meta. In the copy, set the `sys.path.insert` line to `$K` and the last line to `write(os.path.dirname(os.path.abspath(__file__)), meta, S, beats)`. Run `$PY $W/gen.py` to write `$W/script.json`.
4. **Dress Ledger** (section "Ledger per rung").
5. **Compose the rung scenes** (section "Scenes").
6. **Build:** `VO_TAIL=1.3 STILLS_ONLY=1 $REPO/tools/render-slot.sh $E/make_reel.sh $W $SLUG` first (voice and one still per beat), read the stills, fix, then the full build `REUSE_AUDIO=1 $REPO/tools/render-slot.sh $E/make_reel.sh $W $SLUG`. One render at a time.
7. **Checks** (section "Checks"). Fix and rebuild until they pass.
8. **Thumbnail, package, Canva draft and export, hub card** (sections below).
9. **Report** (last section).

## Script rules
- **meta:** `type: "ladder"`, `layout: "ladder"`, `ladder_style: "bleed"` (the helper `write()` sets these three), `rungs` (five header titles, 17 characters at most, for example "THE INTERN"), `term: "Career ladder"`, `title` (the direct title, see below), `slug`, `family_or_category`, `concept_id`, `themes`, `caption`, `caption_x`, `first_comment`, `first_comment_igtt`, `hashtags`, `threadsTopic`, `threadsReason`, `maths_check`, `sources`, `definition_check`, `registry_check`.
- **Beat roles, in order:**

| Role | How many | What it is |
|---|---|---|
| `title` | 1, beat 1 | The title card. Use `L.title_beat("<first role>", "<top role>")`. Voice: "From audit intern to CFO, the career ladder explained with Ledger in ninety seconds." Card: the same sentence without the length; the pill says "IN 90 SECONDS" |
| `rung` | 2-4 per rung | What the job is on that rung. Each carries `rung` (1-5) and, on most beats, one or two duty `chips` |
| `climb` | 4, one between rungs | One short line that names the next role: "After that, he climbs to senior." |
| `payoff` | 1 | The arc in one line over the ladder with all five Ledgers: "So with each rung, Ledger counted less, and decided more." |
| `cta` | 1, last | `L.cta_beat()`. Never change its sentence |

- **Beat 2 is the first rung.** Start it with "First, Ledger is the <role>, ...". No question, no teaser, no "did you know".
- **The arc.** Choose two verbs for the slider, what he does at the bottom and what he does at the top: Counts / Decides (audit), Makes / Decides (marketing), Researches / Decides (investment), Analyzes / Advises (consulting). Say it on the first rung ("On this rung, he counts everything himself"), once in the middle ("So he counts a little less, and starts to decide"), on the top rung ("He hardly counts anything himself, yet he answers for every number") and in the payoff.
- **Voice lines:** full sentences, 6-13 words, one idea each. Start most with a linking word (First, Then, Now, And, So, As manager, Next, Finally); the validator WARNs under 60%. Never mock a role. No exclamation points, no emoji, no tutoring, no exams. US spelling.
- **Numbers:** state none unless 2 sources back it; a ladder reel needs none. If money appears, one currency per reel; `coin_stream` with `kind: "coin"` draws a $ sign, `kind: "chip"` draws plain coloured pieces with no currency.
- **Caption chunks:** 1-4 words, each makes sense alone, taken from the voice line in order; one `key` per beat (a word inside its chunk); no full stop at the end.
- **Chips:** 1-3 words, 17 characters at most, capitals, 1-4 per rung (two rows at most). `("LABEL", n)` shows the chip on chunk n of that beat, the chunk that names the duty.
- **Length:** aim for 200-225 words in all, which gives 80-88 s with the default voice. The title may say "ninety seconds" only if `timing.json` `duration` is 90 or less. If it is longer, cut a line (a mid-rung arc line or a payoff line first), or use `L.title_beat(a, b, seconds_word="under two minutes", tag="IN UNDER 2 MINUTES")`. Hard cap 120 s.
- **Title (meta.title, the card title and the YouTube title):** "From <first role> to <top role>, the career ladder explained with Ledger in 90 seconds".

## Ledger per rung
One outfit per rung, bottom rung first, in `OUT = [...]`. Existing sets in `scene_lib.py` (`_ladder_wear`):

| Career | Outfits, bottom to top |
|---|---|
| Audit to CFO | `intern` (blue top, lanyard, orange backpack), `senior` (white shirt, rolled sleeves, tie, brown bag), `manager` (navy suit, pocket square), `controller` (grey suit, glasses, pen), `cfo` (black suit, gold pocket square, glasses, grey temples) |
| Marketing to CMO | `mk_intern` (coral tee, cap, lanyard), `mk_specialist` (teal hoodie, headphones), `mk_manager` (navy blazer, open shirt), `mk_director` (plum blazer, roll neck, coral glasses), `mk_cmo` (black blazer, gold pocket square, coral glasses, grey temples) |
| Analyst to CIO | `inv_junior` (shirt and tie, lanyard, teal backpack), `inv_analyst` (grey fleece vest), `inv_senior` (navy suit, pen), `inv_pm` (grey pinstripe suit, glasses), `inv_cio` (black suit, gold, glasses, grey temples, watch chain) |
| Consulting to partner | `con_analyst` (shirt and tie, lanyard, blue backpack), `con_consultant` (mid-blue blazer), `con_manager` (navy suit), `con_principal` (burgundy suit, glasses), `con_partner` (black suit, gold, glasses, grey temples) |

A new career may reuse a set, or add one:
1. In `scene_lib.py` add the five names to `OUTFITS` and `LADDER_OUTFITS`.
2. In `_ladder_wear`, add one `elif outfit == "<name>":` per look inside the last `else:` block. Build it from the parts already there: `bandp(colour)` (the clothes band), `shirt` (collar and blue tie), `opensh`, `tee`, `lany` (lanyard and badge), `lapels(colour)`, `psq(colour)` (pocket square), `pack(colour)` (backpack), `GL` or `glc(colour)` (glasses), `tufts` and `gbrow` (grey temples and brows, top rung only), and `sleeve = (colour, length)` (13 = rolled, 26 = jacket).
3. Rules: the body, face, bookmark, arms and hands never change. Each rung must differ at thumbnail size, so change the band colour on every rung and add one clear accessory. Bottom rung looks young (backpack, lanyard, cap), top rung looks senior (dark suit, glasses, grey temples).
4. Check: `$PY -c "import sys; sys.path.insert(0,'$E'); import scene_lib as L; [L.ledger(0,0,1,outfit=o) for o in L.LADDER_OUTFITS]"` must not fail, then look at the first stills.

## Scenes
Art coordinates are screen pixels (frame `[0, 0, 1080, 1920]`). Import everything from `ladder_script.py`.

**Safe areas**
| Zone | Where |
|---|---|
| Platform UI, nothing important | top 220 px, bottom 380 px (y over 1540), right 140 px (x over 940) |
| Rung title and logo (you compose with) | y 452-522 |
| Duty chips (you compose with) | y 534-670 (two rows) |
| Rung scenes: faces, text, props (you compose with) | x 30-940, y 690-1500 |
| On screen, after `write()` lifts every scene except the title and closing scenes by 220 px | header y 240-310, chips y 322-458, content y 470-1280, ground line y 1280, captions y 1320-1530 |
| Ladder scenes (no header) | x 30-940, y 450-1500 |
| Ground line | y 1500 (`GY`); Ledger's feet y 1496 (`FEET`) |

**Helpers** (`L = Ladder(OUT, TAGS, brackets=[...], dial=("Counts", "Decides"))`)
| Call | Gives |
|---|---|
| `scene(k, *items)` | A scene with the full-bleed room in wall colour k (1-5 = the rung, 0 = ladder shots) and the floor decoration. Every scene goes through it |
| `led(x, s, outfit, mood=..., arm=...)` | Ledger on the ground. `s` 3.0-3.4 alone, 2.2-2.6 with small props, 1.9-2.0 beside a big prop |
| `L.title()`, `L.title_beat(frm, to)` | Scene and beat 1 |
| `L.climb(k, go=0, name=1)` | The climb from rung k to k+1 (k 0-3). `go` = the chunk he starts on, `name` = the chunk that names the next role. `pulses={bracket index: "chunk:N"}` pulses a bracket |
| `L.all(slide_chunk=1)` | The payoff: five Ledgers on the ladder, all tags ticked, the slider runs to the far end |
| `L.cta()`, `L.cta_beat()` | Closing scene and beat |
| `L.dial_item(490, 770, 720, start=0.06, slide={"at": "chunk:1", "to": 0.3})` | The slider in a rung scene. Positions: 0.06 bottom rung, about 0.3-0.4 in the middle, 0.95 top rung |
| `B(role, img, text, chunks, rung, chips, **extra)` | One beat |

`Ladder(...)` options: `brackets=[("AUDIT FIRM", 0, 2, "ink"), ("COMPANY", 3, 4, "blue")]` groups rungs (first rung, last rung); leave it out when the whole career is in one kind of firm. Tags are 440 px wide with brackets and 540 px without. A long tag such as "PORTFOLIO MANAGER" needs `tag_w=540, tag_fs=36`; the build stops with a message when a tag does not fit.

**Rung scenes: one moving prop per line.** Patterns that work (copy them from the example and the four reels):
| Line says | Use |
|---|---|
| Who he is on this rung | Ledger alone at `s` 3.2-3.4 with two `arrow` items popping in on the chunks that name his badge, cap or bag (list the arrows AFTER Ledger) |
| Matches or checks things line by line | `match_rows` (`left`, `right` titles, `link`, `tick`, `flag` timings; `bad: None` when every row agrees) |
| Chooses what is worth it | `test_picker` (`labels`, `sizes`, `note`, `pick`) |
| Plans time | `cal_fill` (`title`, `fills`) |
| Keeps a budget, a risk or a target | `meter` (`label`, `limit`, `to`, `fill`, `color`) |
| Works through steps | `checklist` (`title`, `lines`, `tick`) |
| Owns one thing out of several | four `order_chip` pills, swapped on a chunk for a copy with one pill blue (`until` / `at` + `pop: "cut"`) |
| Splits money or effort | three `pot` items and three `coin_stream` items aimed at them |
| Leads a team | three `person` items with `appear` and a stagger |
| Presents to a board or clients | `board_table` (`seat` timing) with an `order_chip` label on its front, a `chart` with `reveal` |
| Runs several teams | `org_chart` (`heads`, `team`, `rows`, `show`) with a small Ledger standing on its top point |
| The arc line | `L.dial_item(...)` with Ledger alone at `s` 3.0 |

**Timing keys on any item:** `"at": "chunk:N"` (pop in on chunk N of the scene's run of beats), `"until": "chunk:N"`, `"pop": "cut"`, `"appear": {"at": "chunk:N", "delay": s}` (pop in after a delay, for staggers), `"move"`, `"pulse"`, `"shake"`, `"reveal"`, `"out"` (see the engine skill). Chunks count from 0 over the consecutive beats that share the scene.

**Rules**
- Ledger is never hidden: list tables, cards, desks and bursts BEFORE him.
- Text in props stays at 34 px or more; the props stop the build when a label does not fit.
- Every person and object the voice names is drawn and appears on that word.
- Keep Ledger's pointing hand clear of prop text: with `led(218, 2.0, ..., arm="point")` his hand reaches x 430, so props start at x 450.

## Checks (every build)
1. **Validator:** `$PY $E/validate.py $W/script.json` prints OK. One WARN is expected, the reminder about the 90 seconds. Fix every other WARN you can.
2. **Length:** `timing.json` `duration` is 90 or less if the title says ninety seconds; never over 120.
3. **Scene build:** no WARN lines from `build_scenes.py` (an item outside the art box, a chunk number past the end).
4. **Frame-fill** (printed at the end): "ui-zone ink" under about 2% on every beat (the ground line and floor lines run to the edges, which is fine).
5. **Read the stills and frames yourself.** Make a sheet of the stills, then extract 8-10 frames from the MP4 (first frame, a mid-climb frame, one per rung, payoff, closing card). Pass criteria:
   - frame 1 shows the finished title card in the right font;
   - the five Ledgers differ at thumbnail size and are all clearly Ledger;
   - captions sit in the middle of the bottom half, on the floor, and are readable; they never cover Ledger's face, a number, a concept tag or a ladder label; title, chips and logo do not collide;
   - nothing important in the UI zones; nothing covers Ledger; hands proportional;
   - in a mid-climb frame Ledger is between two rungs;
   - the slider's two words do not touch each other or the logo;
   - the closing card shows the full sentence in about four lines with the logo.
6. **Other layouts unchanged** (only after changing the engine): section "After an engine change".

## Thumbnail
One per reel, style "v2" (`$E/make_thumbnail.py`, see the memory notes thumbnails-at-upload and creative-context-thumbnails).
1. Write the spec: `$PY $K/thumbnail_spec.py $SLUG "From *<first role>* to *<top role>*" <five outfits, comma separated> <BOTTOM TAG> <TOP TAG> assets/renders/thumbnails-v2/specs/$SLUG.json`. It draws a four-rung ladder with Ledger in outfits 1, 2, 4 and 5, the bottom tag ticked, the top tag yellow and a dashed arrow up, with the pill "CAREER LADDER IN 90 SECONDS" (change the pill in the JSON if the reel is longer than 90 s). Keep the tags short ("ANALYST", not "JUNIOR ANALYST").
2. `$PY $E/make_thumbnail.py assets/renders/thumbnails-v2/specs/$SLUG.json --out assets/renders/thumbnails-v2 --png-dir <scratchpad>/thumbs`. It must print "0 check(s) to fix". Look at the JPG.
3. Copy the JPG and PNG into `$D` as `$SLUG-thumbnail.jpg` and `.png`.

## Package, Canva draft with music, export
1. Copy from `$W` into `$D`: `$SLUG.mp4`, `-canva-upload.mp4`, `-voice-only.mp4`, `-poster.jpg`, `-contact-sheet.png`, `script.json`, `timing.json`.
2. **Canva draft** (Chrome, your own new tab; never touch other tabs):
   1. `copy-design` on the latest ladder draft (`DAHauSOcnH4`, audit intern to CFO; its music "Light Minimal Ambient" is already at volume 8). Open `https://www.canva.com/design/<id>/edit` and wait 8 s.
   2. `find` the "Uploads" tab and click its ref (do not click by coordinate: the side bar moves with the window height). `find` "file-input element for Upload files" and `file_upload` `$D/$SLUG-canva-upload.mp4` (under 10 MB). If the call reports a connection error, run `find` again before retrying: the upload has often started anyway.
   3. Wait until the new thumbnail shows its length (for example 1:22). Click the video on the page, click **Replace** in the toolbar, then click the new thumbnail (first in the list; check the length).
   4. The total at the bottom right must equal the video length. If it is shorter, click the scissors length in the toolbar, triple-click the length field, type the full length (for example 84.1), press Return, click Done.
   5. Click the music track, open its volume, and check it says 8 (type 8 and press Return if not). The video stays at 100.
   6. Click the design title, select all, type "Ladder reel - <From> to <To> (Ledger) v1", press Return. `move-item-to-folder` to `FAHYcHrS5PE`. Close your tab.
3. **Export:** `export-design` with `{"type": "mp4", "quality": "vertical_1080p"}`, download the URL with `curl -sL -o $D/$SLUG-canva-export.mp4 "<url>"`. Check with ffmpeg: 1080x1920, the same length as `timing.json` (within 0.2 s), an audio stream. It is about 21 MB.
4. **Post copy under 10 MB** (the Chrome upload cap): `ffmpeg -i $D/$SLUG-canva-export.mp4 -c:v libx264 -preset slow -tune animation -b:v 740k -maxrate 1000k -bufsize 2000k -pix_fmt yuv420p -c:a copy -movflags +faststart $D/$SLUG-post.mp4`. Extract five frames from it and look at them.
5. If Canva or Chrome blocks you for more than about 15 minutes, stop, keep `$SLUG.mp4` as the file to post, and say so plainly in the report and in the card's `music` field.

## Hub card
1. **Upload** with the Artifact tool (`asset: true`, url `https://claude.ai/artifact/HbKxzWUcWhaBaaNb9buZM6`): `$SLUG-post.mp4`, `$SLUG-poster.jpg`, `$SLUG-thumbnail.jpg`. Keep the three `/_blob/` ids.
2. **Time:** read the slots on the date. Use 12:00 Madrid if no post is within 2 hours; otherwise the nearest time at least 2 hours from every other post (13-16 Nov 2026 used 15:30). Vietnam is Madrid + 6 h in winter.
3. **Card:** build the document with `cd $REPO && $PY $K/make_card.py assets/renders/ladder-reels/$SLUG $SLUG <YYYY-MM-DD> <HH:MM> <video blob id> <poster blob id> <thumbnail blob id> <scratchpad>/card.json <canva id>` (it stops when a copy limit is broken), then ArtifactData `set` on `slots/$SLUG` with `file_path` (get it first; if it exists, `update` with `if_version`). The fields it writes:
   - `id`, `reviewId` (= the slug), `format: "life-of-reel"`, `reelType: "ladder"`, `kind: "video"`, `status: "proposal"`, `image: "draft"`, `text: "ready"`, `version: 1`, `approvals: {}`;
   - `title`, `term`, `family_or_category`, `concept_id`, `concept`, `themes`, `registry_check`, `rungs`, `cta`, `duration_s`;
   - `date`, `time`, `time_madrid` ("15:30"), `time_vietnam` ("YYYY-MM-DD 21:30"), `week`;
   - `caption`, `caption_x` (280 characters at most), `first_comment`, `first_comment_igtt`, `firstCommentType: "question"`, `hashtags`;
   - `threadsTopic`, `threadsTopicKind: "topic"`, `threadsTopicVariant: "primary"`, `threadsReason`;
   - `youtubeTitle` (= title + " #Shorts", 100 characters at most), `youtubeDescription` and `tiktokCaption` (= caption);
   - `videoUrl` and `videoAssetId` (the post copy), `posterUrl`, `video` and `postVideo` (the local post copy), `canvaExport`, `canva`, `canvaFolder`, `music`, `postNote`;
   - `thumbnail: {style: "v2", template: "ladder", title, pill, file, jpg, url (the /_blob/ URL), png, spec}`;
   - `script` (each beat's role, start, text, captions with `t`, rung and chips, from `timing.json`), `sources`, `maths_check`, `definition_check`, `text_check`;
   - `test: "L1"`, `testNote: "L1 ladder format: views at 24 h and 72 h vs the platform median of our other voiced reels"`;
   - `statusNote`: what the reel is, its length, and what has not been checked (for example that nobody has listened to the audio).
4. **Copy rules** (`docs/content-workflow/weekly-content-process.md`): caption of three short paragraphs plus 4 hashtags (`#edlintics`, `#businessstudents` and 2 more); full sentences with linking words; no full stop at the end of any paragraph; no exclamation points; no emoji; no link; general audience; no tutoring. Use "Walk up the ladder with Ledger and note which rung you are on", never "swipe". First comment: one question, under 150 characters, ending with 1-2 emojis, no link; `first_comment_igtt` is the same ending ", link in bio" before the emojis.
5. Do not create `runs` documents and do not set any slot to approved or scheduled. Log the use in hub `concepts` only after Hoang approves.

## After an engine change
Every other reel type must come out the same. Before you change `$E`, and again after:
1. `$PY $E/validate.py` on `edlintics-life-of-reel/example-accountant.json`, `edlintics-howto-reel/example-hr-turnover.json` and `edlintics-explainer-reel/example-lesson.json`: the printed lines must be identical.
2. Copy the first two into two scratch folders as `script.json`, run `$PY $E/build_scenes.py <dir>`, `$PY $E/picture_timing.py <dir> <dir>/_picture 165`, `$PY $E/make_scenes_json.py <dir>/_picture <dir>/_picture`: `scenes.json` and `beats.json` must be byte-identical (`cmp`).
3. Render three stills of each (`cd $E && SCENES=<dir>/_picture/scenes.json OUT=<out> node render.js stills 3.87,20.37,35.25`) with the old engine (`git stash`, render, `git stash pop`, never while another render runs) and the new one: the maximum pixel difference must be 0.
Gate every new behaviour behind `meta.layout: "ladder"`, a new outfit name, a new prop or a new item key.

## Caption position (13 Nov 2026)
- **Compose as before:** write scenes with the ground at y 1500 (`GY`) and the safe areas in the table above. `write()` then lifts every scene except the title and closing scenes by `LIFT` (220 px) and sets `meta.caption_pos: "low"`, so the header, chips and logo move to the top and captions land on the floor below the ground line.
- **Keep the floor clear:** nothing important may hang below the ground line (a label under a prop at y 1500 or lower would sit under the captions).
- **Ladder shots:** the top Ledger of the payoff shot reaches about y 235, just inside the top safe line, and the right slider word ends close to the corner logo; keep slider words short.
- **Rebuilding a reel with captions low:** run its generator again (same text, so `REUSE_AUDIO=1` keeps the voice and timing), build, look at every still, then replace the video in the same Canva design and export again.

## Pitfalls (what went wrong on 12-13 Nov 2026)
- **Hidden parent, visible children.** Hiding the header with `visibility: hidden` left the chips on screen over the ladder shots; the header is switched with `display`.
- **First frame in the wrong font.** Headless Chrome drew frame 0 before Inter 900 had loaded. The ladder layout now waits for the font; if you add another layout, do the same, and never trust one baseline run for a regression check (render the first still twice).
- **A burst over Ledger.** The level-up flash was listed after Ledger and covered him. Bursts go before Ledger in the item list (the helper does this).
- **Outfit swap by chunk came too early or late.** The climb takes about 1 s, so the swap uses `out` and `appear` with a delay on the same chunk as the move, not `at` and `until`.
- **Seven-line closing card.** A card beside the ladder was too narrow. The closing and title cards are full width (x 60-920), with the five Ledgers on steps below them.
- **Slider words colliding.** "Researches" and "Decides" touched on the short payoff slider. Check every slider; widen it or shorten the words.
- **Thumbnail title on three lines** pushed the title into the art (two CHECK lines). Add `"title_fs": 78` for a long title; a long tag such as "JUNIOR ANALYST" may not fit a 430 px tag, so use the short role ("ANALYST").
- **Chips and titles too long.** A chip is 1-3 words and 17 characters; a header title is 17 characters. "ANSWER TO THE CEO" (4 words) failed; "REPORT TO CEO" passed.
- **A 5-word caption chunk** fails (the ladder limit is 1-4 words). When you add a linking word to a line, re-split its chunks and re-number the chip and `at` chunks of that scene.
- **Claiming 90 seconds on a 98-second video.** The first version ran 97.6 s. Cutting the question hook, one arc line and the team shot brought it to 84 s. Measure, then claim.
- **A number in the opener.** "It can take about twenty years" needed two sources and was then dropped with the hook. A ladder reel needs no career number.
- **zsh does not split `$VAR` into words** and treats `=====` oddly. Pass file lists through Python, and print separators with words.
- **`cat > file` with no input hangs the shell.** Never leave a bare `cat >` in a command.
- **`git stash` while a render runs** swaps the engine under it. Only stash when nothing is rendering.
- **A background render dies quietly when its last step fails.** `package`-style scripts with `set -e` stop at a failed thumbnail and skip the copies; read the log, not only the MP4.
- **Canva side bar by coordinate.** The Uploads button moved when the window height changed and the click opened Text instead. Click by `find` ref.
- **The Canva export is about 21 MB.** It cannot go through the Chrome upload (10 MB), so always make the post copy.
- **Listing a source that was not opened.** Only list what you opened, and mark snippet-only sources.

## Report
- slot id, date and time used, length;
- absolute paths: post copy, Canva export, engine MP4, contact sheet, thumbnail JPG and PNG;
- Canva draft id, hub card version, the three `/_blob/` ids;
- sources (opened or snippet-only), the registry line;
- WARN lines left;
- what was not verified, always including whether anybody has listened to the audio.
