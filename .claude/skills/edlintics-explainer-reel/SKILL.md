---
name: edlintics-explainer-reel
description: Shared engine for Edlintics explainer reels (9:16, up to 2 minutes, hand-drawn Ledger picture stories with Kokoro voice, chunked captions, an end card and Canva music). Holds the scene library, validator, renderer and the one build command used by the edlintics-definition-reel and edlintics-life-of-reel skills. To make a reel, use one of those two skills; read this file only to change the engine.
---

# Edlintics explainer reel engine

To make a reel, use one of these skills:
- **edlintics-definition-reel:** hook, everyday story, definition, business example, takeaway, end card.
- **edlintics-life-of-reel:** "A day in the life of a [role]", relatable moments, the turning moment, the concept, the lesson, end card.
- **edlintics-howto-reel:** "How [role] in [industry] deals with [problem]" (60-90 s, 2-minute cap): hook question, the problem, 3-4 steps, the concept with its equation, a 4-box summary diagram, takeaway, end card with term, definition and equation. `meta.type: "howto"`; it opts in to the full-frame layout with `meta.layout: "full"` (see "Full-frame layout" below).
- **In-lesson videos:** `meta.type: "lesson"`, for course lessons in the app, not social posts (see "In-lesson videos (type lesson)" below). Examples: `example-lesson.json` (defcards inline) and `example-lesson-grouped.json` (defcards at the end).
- **edlintics-ladder-reel:** "From audit intern to CFO, the career ladder explained with Ledger in 90 seconds" (13 Nov 2026): Ledger climbs five rungs in a different outfit on each. `meta.type: "ladder"`, `meta.layout: "ladder"`, `meta.ladder_style: "bleed"` (see "Ladder layout" below).
- **edlintics-ledger-talks:** Ledger talks to camera with a mic (test format T1). `meta.type: "ledger-talks"` switches the engine to the talk layout: full-screen art, a fixed frame, lip sync (mood `talk`), jump cuts, 1-3 word karaoke captions over his chest, voice only. New presets: mood `talk`, arm `mic`, `larm` (`up_l`, `point_l`, `open_l`, `shrug_l`) and background `campus`.

Both write a `script.json` and build it with this engine:
```
.claude/skills/edlintics-explainer-reel/scripts/make_reel.sh <workdir> <slug> [speed=1.08]
```
Reference build: sunk cost v5 (hub slot `explainer-sunk-cost`, Canva `DAHZALJdKoM`). It was built from `.claude/skills/edlintics-definition-reel/example-sunk-cost.json`.

## Standing rules (Hoang, 25 Oct 2026). The validator enforces them.
1. **No camera moves.** There is no zoom, push-in, pan or reframe. Each beat shows its scene as one steady frame. By default the frame auto-fits (see Layout); a scene may override it once with `"frame"`. A new scene comes in with a 0.15 s fade and a fast draw-on (0.5 s). Line boil and objects drawing in are the only motion.
2. **End card last.** The final beat has role `"endcard"`, with `"term"` and `"keypoint"`. It shows the term large, a one-line key point with a highlighter, and the logo, for about 3-4 s while the voice says both. A loop-back line before it is optional (role `"loop"`).
3. **Captions** are chunks of 2-5 words in time with the voice, with one `key` word highlighted per beat.
4. **No full stop at the end of any paragraph.** This covers captions, the key point, the post caption, caption_x and the first comment. Full stops between sentences are fine.
5. **House rules:** mixed currencies across posts (one inside a post), no exclamation points, no emoji, no tutoring, general audience. The first comment never reveals the answer.
6. **Length** is up to 2 minutes for every reel type (Hoang, 4 Nov 2026: "Put all of video to 2 mins cap"). Use the time the story needs: about 2.4-3 spoken words a second, beats of 2-4 s.
7. **Full sentences with transitions** (Hoang, 4 Nov 2026). The script, its description and every voice line are full sentences joined by strong transitional words (because, so, however, as a result, this means, for example). No fragments or keyword lists. The definition line is a full sentence that matches the glossary entry, and the end-card `keypoint` is a full sentence too, never a clipped phrase. The voice is Kokoro `af_heart` at speed 1.08.

8. **Say out loud when the example starts, and when the reel goes back to it (Hoang, 6 Nov 2026).** See "Context transitions" below. The validator fails a script that drops the viewer into an example unannounced.
9. **Show the real thing (Hoang, 6 Nov 2026: "real excel refernece and equation").** When a concept lives in a tool or a formula, draw the tool with its real contents, not a generic picture of it. See "Real artefacts" below.

10. **Direct opening, no hook (Hoang, 13 Nov 2026).** See "Direct opening" below. It applies to NEW reels; reels already scheduled are not changed.

## Direct opening (Hoang, 13 Nov 2026)
Hoang, after sharing two "X, explained in 90 seconds" reels: "I think we should avoid the hook and go directly to the point like these video? Like Bid-Ask Spread explained with Ledger in 90s, Understand a day in the life of a manager in ..., avoid the hook just go directly to the point".

**Rule for new reels:** beat 1 says what the video is, as one full sentence on screen and in the voice, and the story starts in beat 2. No verdict question, no teaser, no "did you know". This replaces the "beat 1 is a verdict question" and "hook question" guidance in the definition, life-of and how-to skills for new reels.
- **Example openings:** "Bid-ask spread, explained with Ledger in 90 seconds", "A day in the life of a manager, in 90 seconds", "From audit intern to CFO, the career ladder explained with Ledger in 90 seconds".
- **Only claim a length the video has.** "In 90 seconds" needs a `timing.json` duration of 90 or less; otherwise say "in under two minutes".
- **Thumbnail, card title and YouTube title** use the same direct title.
- **Where it works today:**
  - ladder reels: beat 1 has role `title` (a title card with a tag pill, complete on frame 1); the validator requires it;
  - definition and life-of reels: beat 1 keeps role `hook` and may be a title-style sentence. The validators accept it as long as the first `story` beat (definition) or the first `moment` (life-of) still opens the example out loud ("Let's imagine ...", "Let's follow ..."), and a life-of beat 1 or 2 still says "a day in the life of";
  - how-to reels: NOT yet. The how-to validator still requires "How does <a role> ... deal with <a problem>?" in beat 1 (or in hook beat 2-3 with `hookStyle: "B"`), so a title-style beat 1 fails. Until the validator is updated, how-to reels keep the question opening.

## Context transitions (Hoang, 6 Nov 2026)
Hoang: "when ever you start the context explaine, please give the transitional context like Let's imagine ..., for this let's use the example of ... so user understand, continue from the last example, ..., continue the story".

**Why:** a viewer who starts mid-scroll, or who has just heard a definition, cannot tell whether a new person or number belongs to a new example or the same one. One spoken phrase fixes that.

**Three moments need a spoken signpost:**
| Moment | Say | Instead of |
|---|---|---|
| The example starts | "Let's imagine a toy shop that ...", "For this, let's use the example of a cafe's order sheet", "To see why, picture ..." | Starting cold: "Last January, he bought ..." |
| The reel returns to the same example, after a definition or a step away | "Continuing the story, ...", "Back to our toy shop, ...", "Continuing from the last example, ...", "Staying with the same sheet, ..." | "At twenty-five percent, Ledger's toys ..." |
| A different example starts | "Now let's use a business example. Imagine a bank that ...", "Let's take a second example ..." | Changing the setting with no warning |

**By reel type (the validator enforces the first two columns):**
| Type | Must open the example | Must signal the return | Pattern |
|---|---|---|---|
| Definition | first `story` beat | first `example` beat | hook, "Let's imagine ...", definition, "Continuing the story, ..." or "Now let's use a business example ...", takeaway |
| A day in the life | a `hook` beat or the first `moment` | first `lesson` beat | "Let's follow a day in the life of ...", moments, turn, concept, "Back to the wedding, ..." |
| How-to | first `problem` beat | none, the steps already run First, Then, Next, Finally | hook question, "Let's imagine an airline where ...", steps, concept, "Let's revise the process" |
| List | the `story` beat after the hook, naming the running example | at least two later terms: "Back in our cafe, ...", "On the same sheet, ..." | "Let's use a cafe's order sheet as our example", then each term on that same example |

**Writing it:**
- Keep it short. The signpost adds 3-5 words to a line; it never gets its own sentence unless the example needs setting up.
- Vary the phrase inside a reel. "Let's imagine" once, then "Continuing the story", then "Back to our toy shop".
- Name the thing you return to ("Back to our toy shop"), so a viewer who looked away can rejoin.
- Put the signpost in the captions too, as its own chunk where it fits ("Let's imagine a toy shop").
- Hooks stay as they are: a hook asks the question first, and the signpost comes straight after it.
- Lessons (`meta.type: "lesson"`), Ledger talks and ads are not checked, but the same idea helps in lessons.

**Example, carrying cost:**
- Before: "Ledger's toys sit unsold on a shelf, so why do they keep costing him money? Last January, he bought ten thousand dollars of toys ..."
- After: "Ledger's toys sit unsold on a shelf, so why do they keep costing him money? Let's imagine he bought ten thousand dollars of toys last January ..."
- Before: "That is carrying cost ... Many businesses estimate it at twenty to thirty percent ..."
- After: "That is carrying cost ... Continuing the story, many businesses estimate it at twenty to thirty percent ..."

## Real artefacts (Hoang, 6 Nov 2026)
A reel about formulas or a tool shows that tool with real contents. For anything in a spreadsheet use `sheet_grid`, never `laptop` with `screen: "sheet"`. The numbers in the cells must be the ones the voice says, and the formula bar must hold the formula exactly as a viewer would type it. Work the sheet's sums out and add them to `meta.maths_check`.

**`sheet_grid`, full layout, no Ledger:**
```json
{"bg": "none", "frame": "wide", "items": [
  {"p": "sheet_grid", "x": 490, "y": 945, "w": 860, "h": 900, "cols": ["A", "B", "C", "D"],
   "rows": [["Item", "Price", "Cups", "Total"], ["Latte", "$3.00", "3", "$9.00"], ["", "", "", ""]],
   "name_box": "D2", "formula": "=B2*C2", "selected": [1, 3],
   "refs": [{"cell": [1, 1], "color": "blue", "label": "B2"}, {"cell": [1, 2], "color": "red", "label": "C2"}]}
]}
```
- `rows` shows cells as given. Pad with empty rows so the grid fills the frame and looks like a real sheet. `start_row` sets the first row number.
- `selected` is `[row, col]` from 0, with the green cell border and fill handle. `name_box` should name the same cell.
- `refs` tints and outlines the cells a formula uses, as Excel does. `label` colours that text in the formula, so `B2` in the bar matches the blue `B2` box. Colours: blue, red, green, violet, amber.
- `popup: {"title", "text"}` draws an error box over the grid, for data validation.
- **Animate with states, never with camera moves:** stack two `sheet_grid` items, the first with `"until": "chunk:N"` and the second with `"at": "chunk:N", "pop": "cut"`. Copying a formula down is the selection and the formula moving one row. Check the state change lands on the right word on the contact sheet.
- Text below 30 px, or a formula too long for the bar, stops the build at the scenes step with a message saying what to shorten.
- Worked example: `assets/renders/explainer-reels/w47/2026-11-16-1300/script.json`.

## Files (scripts/)
| File | What it does |
|---|---|
| `make_reel.sh` | The one command: validate, scenes, voice, audio mix, scene data, stills, video, then the checks and contact sheet |
| `validate.py` | Checks script.json against the rules above and the beat structure for `meta.type` |
| `scene_lib.py` | The scene library (spreadsheets: `sheet_grid`, numbers: `data_chart`, `data_table`): Ledger (`mood`, `arm`, `outfit`, `flip`, `tilt`), about 35 props and 6 backgrounds. Run `python scene_lib.py --list` |
| `build_scenes.py` | Turns scene presets into `s*.svg` and resolves each scene's optional `frame` (default `auto`) into `beats.json` |
| `vo.py` | Makes the Kokoro voiceover (`voiceover.wav`) and `timing.json` with beat and chunk times |
| `mix_audio.py` | Makes `audio-voice.wav` (voice plus soft generated whoosh and tick) and `audio.wav` (adds a quiet pad for preview) |
| `make_scenes_json.py` | Packs the art, beats and end card into `<work>/scenes.json` |
| `render.html`, `render.js`, `build.sh` | The headless Chrome renderer at 24 fps, plus the H.264 encode, the voice-only cut and the Canva upload copy under 10 MB |
| `render_range.sh` | Renders one time range of a built reel with its audio, for pilots and quick checks |
| `postcheck.py` | Checks resolution, audio, length and the 10 MB limit (not for lessons), and makes `<slug>-contact-sheet.png` |
| `lesson_files.py` | Lessons only, run by `make_reel.sh`: `<slug>.vtt` (WebVTT from the caption chunk times) and `<slug>-transcript.txt` (the "Read instead" text) |
| `canva_kit.py` | After the build: the editable kit (per-beat clean clips, voice and per-line files normalised to -14 LUFS, SRT, end-card PNGs, previews, README) for Canva or CapCut |
| `cutcheck.py` | Frame checks after the build: ink coverage on the first frames after every cut, plus the 4 fps and cut ±2-frame review sheets |
| `logo/edlintics-logo.png` | The logo from the Canva post template DAHYuGZYL_E |

Tools, with no system installs:
- Kokoro, imageio-ffmpeg and Pillow in `tools/tts/.venv`;
- Node with puppeteer-core in `scripts/` (installed on first run) and the installed Google Chrome.

Each reel builds in its own work folder, so several can build at once.

## Layout (1080x1920)
- **Caption band:** y 262-498, Inter 900 at 92 px, 2 lines at most.
- **Art box:** x 40-1040, y 530-1310.
- **Ledger-first framing (the default, 25 Oct 2026):** in any scene with Ledger, `build_scenes.py` sizes the frame from Ledger's own height, so he fills 74-88% of the art-box height (about 74% in a busy scene) whatever his `s`. Props that would fall outside are nudged in, then scaled down if still too big; Ledger is never shrunk or moved. Wide "bleed" props (`desk`, `building`, `whiteboard`, `window`, `people_group`) may run off the left and right edges instead of shrinking. Nothing goes above the frame top, so nothing sits under the caption band. Scenes without Ledger fall back to the renderer's fit (the drawn subject at ~70% of the width).
- **Override:** set `"frame"` on the scene to `content` (old fit-everything), `ledger`, `ledger-close`, `wide`, `item:<id>`, `items:<id>,<id>` or `[x, y, w, h]`. Use it only for a deliberate close-up or crop.
- **Hands and arms:** every arm pose in `scene_lib.ARM_POSES` keeps the brand proportions (shoulder-to-hand 38-48 units, hand r 9 against a 136-wide body). `validate.py` fails the build if a pose drifts (`check_proportions()`), and `build_scenes.py` WARNs when a prop at Ledger's hand is out of scale with it. The contact-sheet review always includes "hands proportional".
- **Rebuild pictures only:** `REUSE_AUDIO=1 make_reel.sh <workdir> <slug>` keeps voiceover.wav, the mix and the timings, and only redraws scenes.
- **Poster:** make_reel.sh writes `<slug>-poster.jpg` from the first still by time.
- **Logo:** 210 px wide at y 1338, opacity 0.72.
- **Clear areas:** the bottom ~670 px and right ~120 px are covered by the Reels, Shorts and TikTok buttons.
- **End card:** the term at 132 px, a blue rule, the key point at 64 px, and the logo at 330 px.

## Hand-drawn look
It is modelled on the pencil reference (evanbode, "TIME FLIES"):
- **Line boil:** the displacement noise seed changes every 2 frames, so lines move at 12 fps.
- **Pencil grain:** a noise mask breaks up strokes.
- **Ghost pass:** a second copy at 30% opacity, so lines look drawn twice.
- **Paper:** grain and fibre texture.
- **Draw-on:** strokes draw in with stroke-dashoffset.

We don't use rough.js, perfect-freehand or Remotion: they would mean redrawing Ledger and lose the exact mascot.

## Data charts and tables (Hoang, 6 Nov 2026)
Hoang: "For the reel, if it is a numerical concept, we can add graph and table to explain clearly as well".

**Rule:** in explainer, how-to and list reels, a concept that rests on numbers gets at least one `data_chart` or `data_table` beat where it explains the idea more clearly than a picture. Put the same numbers as the voice line on screen, and never show a number the voice or slot does not support.

The props compute nothing but the scale: every value shows as given, so the script owns the maths and the currency. Pass values as strings to keep zeros and commas (`"0.40"`, `"3,000"`); the JSON number `0.40` would show as `0.4`.

**Bar chart, full layout, no Ledger:**
```json
{"bg": "none", "frame": "wide", "items": [
  {"p": "data_chart", "kind": "bars", "x": 490, "y": 945, "w": 860, "h": 940, "values": ["0.40", "0.44"], "labels": ["Before the deal", "After the deal"], "unit": "$", "y_title": "Price per ounce", "highlight": 1}
]}
```
**Line chart, full layout, Ledger below:**
```json
{"bg": "none", "frame": "wide", "items": [
  {"p": "data_chart", "kind": "line", "x": 490, "y": 755, "w": 860, "h": 610, "values": [100, 80, 64, 51], "labels": ["1", "2", "4", "8"], "y_title": "Hours to build one boat", "x_title": "Boats built so far", "highlight": 3},
  {"p": "ledger", "x": 170, "y": 1430, "s": 1.55, "mood": "smile", "arm": "point", "outfit": "suit"}
]}
```
**Table, full layout, no Ledger:**
```json
{"bg": "none", "frame": "wide", "items": [
  {"p": "data_table", "x": 490, "y": 945, "w": 860, "h": 800, "headers": ["Cost", "Boat 1", "Boat 2"], "rows": [["Materials", "$1,200", "$1,200"], ["Labor", "$2,500", "$2,000"], ["Overhead", "$600", "$480"], ["Total", "$4,300", "$3,680"]], "highlight": -1}
]}
```
**Other layouts (art box 1000x780):** no Ledger: `"x": 500, "y": 920, "w": 860, "h": 700` (table `"h": 640`). With Ledger beside it: `"x": 640, "y": 920, "w": 620, "h": 740` (table `"y": 880, "h": 620`) and Ledger at `"x": 165, "y": 1290, "s": 1.15`.

**`data_chart` options:**
- `kind`: `bars` (always from zero, negatives go below the axis) or `line` (from zero unless `"zero": false`; use that only when a line from zero would look flat, and let the value labels carry the numbers).
- `values` and `labels`: 1-8 of each, equally spaced in the order given. A line over 1, 2, 4, 8 is therefore spaced by doubling, so the voice must say "each time the number doubles".
- `unit`: `$` and other currency signs go in front, `%` and words go behind. A word unit makes labels long, so prefer it in `y_title`.
- `y_title`, `x_title`: optional axis titles.
- `highlight`: an index or a category label, drawn in amber.

**`data_table` options:**
- `headers`: up to 5 columns. `rows`: up to 6 rows, shown as given.
- Number columns align right and text wraps.
- `highlight`: a body row (`2`, `-1` or `{"row": 2}`) or a cell (`{"cell": [row, column]}`), counted from 0.
- `h` is optional; rows stretch to fill it.

**Fit and legibility:**
- Text shrinks and wraps down to a 34 px minimum at `s` 1, the smallest size of the existing prop labels. Category labels that still do not fit drop to two staggered rows. Line values move to a clear spot off the line.
- If text still cannot fit, the build stops at the scenes step with a message saying what to shorten. Keep `s` at 1 and size the prop with `w` and `h`.
- A scene with a data prop and a frame of auto or `wide` shows the whole scene inside the safe area, so it does not use Ledger-first sizing. The 70% Ledger check does not apply to these beats. `build_scenes.py` WARNs if an item overlaps the numbers or the prop shows under 85% of its size.
- Use `"bg": "none"`, and pop the prop in with `"at": "chunk:N"` when the voice reaches the numbers.

## Motion and market props (standard from 7 Nov 2026)
Hoang: "any way we can improve the animation to be more finance oriented ... arrow green red illustation with graph, number inside with people trading action and supplement info". Hoang approved this after watching the bid-ask pilot on 7 Nov 2026. **Every beat in an organic reel that explains a number or a finance idea uses these props:** a real graph, table or order book, green and red direction, numbers inside the graphic, people acting, a short supporting note, and motion timed to the voice. Story beats stay hand-drawn with Ledger, so the reel does not turn into an infographic. Lessons and scripts that do not use the props render exactly as before.

Flaws to avoid, seen in the pilots: a counter must not sit on its starting value such as "$0.00" for more than about a second, so start the count when the voice reaches it; check the frames either side of each scene change for a near-empty frame; a flying chip must not cross a face or stay on a label.

**Time.** Every `at` is `"chunk:N"`, counted over the consecutive beats that share the scene, as for pop-ins. Add `"delay"` in seconds and `"dur"` for the length. A scene may run over several beats (give them the same `img`), so a chart keeps building across lines. Frames are rendered by seeking, so all motion is computed from the time.

**Frame.** Use an explicit frame so coordinates equal screen pixels: full layout `"frame": [40, 450, 900, 990]` (safe x 40-940, y 460-1440), other layouts `"frame": [40, 530, 1000, 780]` (safe x 40-960, y 535-1305). Do not use the auto frame with Ledger: it moves items after you place them. `build_scenes.py` WARNs about that, about a chunk number past the end of the run, and about items outside the box.

**Keys on any item** (a dict, or a list of dicts played in order for `move`):
| Key | Fields | What it does |
|---|---|---|
| `move` | `at, delay, dur, to: [x, y], arc, ease, scale, rot, trail` | Travels to `to`. `arc` bows the path upward in pixels. `ease`: inout (default), out, linear, back. `trail`: `"green"` or `{"color", "fade", "width"}` |
| `pulse` | `at, delay, dur, amp` | Grows and settles once, for emphasis |
| `shake` | `at, delay, dur, amp, hz` | Trembles, for panic |
| `bob` | `amp, hz` | A slow idle float |
| `out` | `at, delay, dur` | Fades away |
| `reveal` | `at, delay, dur, dir` | Wipes in: right, left, up or down. Add `"at"` and `"pop": "cut"` on the same item so nothing shows before it. On a `flow_box` over a ghost box, this is a process step that fills |

**New props** (`python scene_lib.py --list` prints every option):
| Prop | Use |
|---|---|
| `order_book` | Ladder with red asks, green bids, numbers inside and a spread band. Rows are best price first. `show` times the parts, `states` move the prices so the spread narrows or widens, and the band's text follows. Give two books the same `spread_range` to compare them |
| `live_chart` | `candles` or `line` that draw themselves. `stops` sets how far the chart has reached by each chunk, `marks` adds green and red arrows with short text, and a price tag follows the latest price |
| `waterfall` | Bars build one by one (`total`, `down`, `up`) while the numbers tick. `rider` puts a small Ledger on the newest bar. With `connect: false` it is two bars growing side by side |
| `fill_grid` | People or squares that fill one by one (`fills`) or empty out and leave a red outline (`fades`). `capacity` puts the excess on its own red row |
| `counter` | A number that ticks with money formatting: `$1,234.50`, `−$0.05`, `$500K` (`comp`), `+20%` (`plus`, `unit`) |
| `trader` | A person with arms. `acts` are poses on chunks: raise, both, point, point_l, cheer, shrug, down, and an optional `mood`. A small hop plays on each |
| `order_chip` | A pill, such as "Bid $50.00", to send with `move`. `plain: true` draws only the coloured words, for a name |
| `coin`, `coin_stream` | One coin to `move`, or several pieces flowing from (x, y) to `to` (`kind`: coin, chip or dot) |
| `burst` | A short flash when something happens, such as a trade matching |
| `note_card` | A pinned note with supporting information. `mark` highlights the last line |
| `trend_arrow` | A chunky green up or red down arrow. Grow it with `reveal` |

**Small example, a trade (full layout):**
```json
"tags": {"bg": "none", "frame": [40, 450, 900, 990], "items": [
  {"p": "order_book", "x": 490, "y": 822, "w": 640, "asks": [["50.05", 300], ["50.06", 500]], "bids": [["50.00", 400], ["49.99", 600]],
   "show": {"bids": "chunk:1", "asks": "chunk:2", "band": "chunk:3"}},
  {"p": "trader", "x": 790, "y": 1385, "s": 1.15, "side": "sell", "name": "Seller", "acts": [{"at": "chunk:2", "pose": "raise", "mood": "happy"}]},
  {"p": "order_chip", "x": 760, "y": 1098, "label": "Ask $50.05", "color": "red", "at": "chunk:2", "until": "chunk:3",
   "move": {"at": "chunk:2", "dur": 0.8, "to": [490, 750], "arc": 70, "trail": {"color": "red", "fade": 0.5}}, "out": {"at": "chunk:2", "delay": 0.7, "dur": 0.15}},
  {"p": "note_card", "x": 490, "y": 1285, "w": 390, "fs": 38, "title": "Spread", "lines": ["$50.05 − $50.00", "= 5 cents"], "mark": true, "at": "chunk:3"},
  {"p": "burst", "x": 862, "y": 822, "s": 0.85, "at": "chunk:3"}
]}
```

**Numbers.** Every number comes from the script. Voiced numbers can appear as they are. Anything else, such as candle prices and ladder depth, must be plainly labelled: `order_book` and `live_chart` write "Example prices" by default, and `"example": false` is only for a scene where the voice says every number or another item carries the label. Use the post's own currency. Text stays at 34 px or more, and a prop stops the build with a message if its labels cannot fit.

**Colour.** Blue stays the main colour (headers, total bars, the numbers that matter). Green and red mean market direction only.

**Check.** Rebuild with `REUSE_AUDIO=1 STILLS_ONLY=1 make_reel.sh`, then look at frames in the middle of a move, not only the stills at the end of each beat: `SCENES=<work>/scenes.json OUT=<dir> node render.js stills 12.5,13.0,13.5`. A flying item may pass over a label for under a second, but must not rest on one. To render part of a reel: `render_range.sh <work> <t0> <t1> <out.mp4>`.

**Worked examples:** the four pilots in `assets/renders/pilot-animation/` (`script.json` in each folder).

## Changing the engine
- **New prop:** add a function to `scene_lib.py`, register it in `PRESETS` (and `HALF` for its size), give it a one-line docstring, and test with the two examples.
- After any engine change, rebuild both examples and look at the contact sheets.

## Contact-sheet review checklist (every reel, every build)
- Ledger is accurate to assets/brand/ledger.svg and fills at least 70% of the art-box height in every scene
- **Hands proportional:** Ledger's hands and arms match the brand proportions (hand about the size of his eye-to-eye gap, arms no longer than his body is tall), and anything he holds is in scale with his hand (Hoang, 25 Oct 2026: check this every time)
- No text inside the art, and nothing sits under the caption band
- The end card shows the term and the key point
- A spoken signpost opens the example, and another marks each return to it (read the voice lines, not only the frames)
- Formulas and tables on screen show the same numbers as the voice, and state changes land on the right word

## Notes from batch runs (25 Oct 2026)
- `people_group` doesn't work under Ledger-first framing: it gets cropped or hidden behind Ledger. Use one `person` (plus a `check`, `bills` and so on) to show "the others".
- Canva Replace keeps the old clip's trim. If the new video is longer, extend the clip: click its duration and type the new length. Then check that the page total equals the video length.
- Study Threads is already joined (24 Oct), so study-pain reels can go there.

## Ledger is not required in every scene (Hoang, 25 Oct 2026)
Use scenario graphics that show the idea directly: a computer, code on a screen, a robot arm, a chessboard, a toddler with blocks, a meeting table, a store, a chart. Ledger appears where a character helps the story, typically the hook, a story beat and the takeaway, but scenes without Ledger are welcome. Scenes without Ledger use the renderer's content fit and still keep the art big. Add simple hand-drawn presets when a scenario needs one.

New scenario presets (25 Oct 2026): `code_screen` (trend none/down/up), `chessboard`, `robot_arm` (hold none/block/piece, drop, flip), `toddler`, `meeting_table` (deal), `whiteboard_team`; `laptop` has `screen: "filled"`. For scenes without Ledger, set `"frame": "wide"` and `"bg": "none"` (or `"paper"` when something stands on the ground) so the art fills the frame.

## Cover (thumbnail), added 26 Oct 2026
Every reel gets a cover: `SCENES=$W/scenes.json node $E/make_cover.js <t> $W/<slug>-cover.png "<kicker>" "<title with one *keyword*>"`.
- Kicker: "Explained in 40 seconds" (definition reels) or "A day in the life" ("life of…" reels).
- Title: 3-6 words, a question or a claim that matches the reel's hook, with one keyword in *stars* (highlighted in yellow). No full stop at the end.
- `<t>`: a time inside a scene whose art matches the title (usually the hook, about 2 s).
- The layout is centred for the 3:4 grid crop (y 240-1680), which Instagram and TikTok profiles show.
- Use the cover wherever the platform allows: the Instagram and Facebook reel cover, the YouTube Short thumbnail, the TikTok cover (choose it at upload) and the LinkedIn video thumbnail.
- **Editable Canva template (26 Oct 2026):** "Shorts cover template - explainer reels", design `DAHZGJ1m_8E` (folder FAHYcHrS5PE). It has one 1080x1920 page per reel: the art PNG as the background (made by `make_cover.js <t> art.png "" ""`), with the kicker (40 px bold #467DE3) and the title (100 px bold #0F172A) as editable text boxes at top 372 and 430, left 60, width 960. For a new reel, upload the art with create-upload-url, add_page, update_fill the background and add the two texts. Hoang may edit the covers in Canva; export them from there when he has.

## Voice engine: ElevenLabs v3 (Hoang, 29 Oct 2026)
- Hoang picked ElevenLabs **eleven_v3** with voice `gPiEpcKoaZywgOzc0Zn9` over Kokoro (round-3 blind test, `assets/renders/voicetest/round3/`)
- Switch: `TTS_ENGINE` (default `eleven`) read by `make_reel.sh` / the puzzle-reel `build.sh`. Code: `scripts/eleven_tts.py` (pcm 24 kHz, cached per line in `tools/tts/cache-eleven/`, key `ELEVEN_LABS_TOKEN` from env, repo `.env` or `../tutoring-content/.env.local`, never printed)
- **ElevenLabs is the default since 29 Oct 2026** (Hoang: Creator plan, "use elevenlab"). `TTS_ENGINE=kokoro` brings back the old Kokoro af_heart voice. If ElevenLabs returns 401/402/429, stop and report; don't fall back silently
- v3 sets its own pace, so the SPEED argument does nothing with ElevenLabs

## Paid ads: `meta.type: "ad"` (29 Oct 2026)
- For paid Meta ad creatives only (first use: `assets/renders/ads/tutoring-2026-10/video/script.json`). The other types are unchanged
- Roles in order: `hook` (1-4, short questions work as a problem montage), `point` (2-3), `cta` (exactly 1), `endcard` (required, last). 5-10 beats, 22-30 s, 45-95 words, caption chunks 2-5 words. A point may run 5-7 s (one line, one scene)
- Only `type`, `term`, `title` and `slug` are required in meta: the ad text lives in Ads Manager, not in caption or first comment
- Tutoring and "book a session" are allowed in ads (the organic no-tutoring rule stays for every other type). No price, no outcome promises, no exclamation points, no trailing full stops, US dollars
- End card: optional `"footnote"` (1-2 lines split by `\n`, at most 90 characters each, no closing full stop), shown small under the logo, for example the IE independence line or "Interactive courses opening soon"
- Layout `ad`: the caption band moves down to y 300-520 so the captions, art and end card all sit inside the central 4:5 safe area (y 285-1635) that Meta's feed crop keeps
- Pace: build with `ELEVEN_TEMPO=1.24 VO_GAP=0.1 make_reel.sh ...` (`VO_GAP` is the pause between beats, default 0.2). At the default 1.12 the 80-word tutoring ad ran 34.8 s
- New presets: Ledger mood `dizzy` (spiral eyes, wavy mouth, a ring of three stars over his head; body and arms unchanged), `chip` (labelled pill; the one prop with text in the art, for subject chips), `exam_sheet`, `cost_pools` (ABC costing), `scatter_plot` (regression), whiteboard drawing `shift` (supply curve moves), laptop screens `call` (generic online lesson: a student tile and a shared board, no real app UI) and `lesson` (interactive lesson card)
- Wide props next to Ledger got cropped by Ledger-first framing; set `"frame": "wide"` on those scenes and check the contact sheet
- **Pace (29 Oct 2026, Hoang):** cut words rather than speeding up; keep `ELEVEN_TEMPO` at 1.15 or lower. The ad voice is `ELEVEN_VOICE=dfeOmy6Uay63tNhyO99j` (set it only for ads; the reel default stays). It speaks about 2.3 words a second at 1.15 and reads lists slowly (a colon costs about a second), so an ad holds about 65 spoken words. Measure first: build the voice at `ELEVEN_TEMPO=1.0` (cached, so later tempos cost nothing) and pick the tempo from timing.json
- **End-card CTA pill:** an ad's end card may carry `"cta": "Start at edlintics.com"` (32 characters at most). It shows as a blue button under the logo from 0.7 s, and the end card's voice line may then be the CTA ("Start at edlintics dot com") instead of the term, so no separate cta beat is needed. Tutoring ad: `VO_GAP=0.1 VO_TAIL=0.6` (`VO_TAIL` is the silence after the last line, so the card stays up about 3 s)
- **Ad scenes are complete on their first frame (reviewer, 29 Oct 2026):** the ad layout skips the part-by-part draw-in and the fill fade; a new scene (and the end card) gets only a 0.12 s whole-group settle (scale 0.97 to 1), captions are fully visible on their first frame. Check it with `tools/tts/.venv/bin/python scripts/cutcheck.py <workdir> <slug> 4`: it measures the ink of the art box on the three frames after every cut against a steady frame (FAIL under 85%) and writes `review/cuts-pm2.png` (every cut at -2..+2 frames) and `review/fps-4.png`
- **Voice tails:** every line gets a 30 ms fade in and out, ElevenLabs clips keep 150 ms after the last voiced sample, and `VO_GAP` is at least 0.23 for ads (the cut sits 0.08 s before the next line, so 0.15 s stays after the last word). A beat may set `"gap": 0.45` for more room after a short hook
- **Loudness:** `canva_kit.py` normalises voice.wav, voice.mp3, voice-with-fx.wav and the previews to -14 LUFS integrated, -1.5 dBTP (two-pass loudnorm) and prints the measured values; Canva and CapCut do not normalise
- **Sound-off rules (Hoang, 29 Oct 2026):** frame 1 is the hook (beat 1 opens fully drawn with its caption; no fade from blank, no logo intro), captions big and high-contrast, and nothing important in the Reels UI zones (bottom 20%, y over 1536, and the right 120 px). The ad layout keeps captions at y 300-520, the art at y 530-1310, the logo at y 1338 and the end card at y 330-1330, all inside the 4:5 safe area (y 285-1635)
- **Ledger `tilt` rotates his arms with the body** (fixed 29 Oct 2026: a tilted body with untilted arms left a hand floating off the corner). `"anim": "wobble"` on an item (with optional `amp` degrees, default 4, and `hz`, default 1.1) sways it about its own feet from 0.2 s into the scene; used for the dizzy beat. Not a camera move
- **Dizzy mood** has eye-sized spirals (readable on a phone) and the ring of stars; pair it with a small `tilt` and the wobble
- **Ad end card box:** y 300-1360 with 36 px gaps and the term at 120 px (the reel card is y 330-1330), so term + key point + logo + cta pill + footnote fit without the flex column squashing the rule. Verified boxes for the tutoring ad: term y 307, rule 710, key point 756, logo 1038, cta 1160, footnote 1302

## Story ads (emotional arc, 29 Oct 2026)
The tutoring ad v4 follows a struggle → turn → help → joy → CTA arc (Hoang's reference: the Tutorful TV ad). Engine pieces added for it, all ad-only unless noted:
- **Scene `tint`:** `"tint": {"color": "#17315F", "opacity": 0.4}` washes the whole scene (dim cool night; `#FFD27A` at 0.08-0.18 for warm scenes). Drawn over the content, inside the art
- **Pop-in on a caption chunk:** `"at": "chunk:N"` on any item shows it (0.2 s fade, small overshoot) when chunk N starts, where N counts chunks across the consecutive beats that share the scene (a scene used by two beats keeps counting). Used for the chat bubbles, the proof cards and the lightbulb
- **Beat `fx: "wipe"`:** a #467DE3 sweep that covers the frame at that beat's cut (0.28 s in, 0.28 s out), the light switching on at the turn
- **Per-beat voice:** `"tempo"` (1.05 for the struggle lines, 1.12 elsewhere) and `"say"` (the text sent to the voice when it must differ from the caption line: v3 audio tags like `[softly]`, `[sighs]`, `[warmly]`, `[cheerfully]`, or the spelling `Ed-lin-tics` so the name is read ED-lin-tiks). The validator checks `text`; `say` may add at most two words. Ellipses in `say` cost about a second each with this voice; use commas for short pauses
- **New props:** `bubble` (chat bubble with text; `"Course|problem"` makes two lines, course bold-blue; side left/right/down), `lamp` (on/off, with a glow), `stat_card` (big blue number + label), `lightbulb`. `window` has weather night/clear, `clock` takes a float hour (0.5 = just past midnight)
- **Pronunciation listen-check:** no local Whisper and the ElevenLabs key has no speech-to-text permission, so variants are generated into `video/pronunciation/` and put in `preview.html` for Hoang to hear
- **Pause-aware captions (reviewer, 29 Oct 2026):** `vo.py` splits each line's audio into speech segments (pauses of 0.15 s or more; bursts under 0.45 s such as a sigh are dropped, extra pauses inside a sentence are merged). When the segments match the chunks grouped by sentence end (`? . ! …`), each group's first caption starts at its measured onset (minus 0.08 s) and the group's chunks spread inside that segment. Otherwise the old spread by word length applies. Check: the caption-vs-onset table in the report of 29 Oct 2026 was exact to 0.01 s
- **`"lit": true`** on an item draws it above the scene tint (chat bubbles stay bright at night)
- **Ad caption box** is x 120-960 and the end-card key point 840 px wide, so no caption passes the right 120 px Reels zone; the art mask is off in the ad layout so a tint reaches the top of the frame (keep ad frames with their art below y 530)
- **State swaps inside one beat (tutoring ad v5, 30 Oct 2026):** `"until": "chunk:N"` hides an item from the start of chunk N, and `"pop": "cut"` makes an `"at"` item appear at once (no fade, no scale, so its own `anim` keeps working). Several Ledgers at the same (x, y), each with `at`/`until`, change his mood on the caption chunks without a cut or a new voice line. The first state has no `at`, so frame 1 is complete
- **Ledger `gaze`:** `right`, `left`, `down`, `up` shift his eyes and brows (`down` also lowers the mouth: head-down sad). Omitted = unchanged
- **Prop `swirl`:** numbers and symbols (`"symbols": "$ % ? 7"`, space-separated) on a flat ellipse (`rx`, `ry`) round (x, y); with `"anim": "orbit"` (and `hz`, default 0.45) they circle, front ones larger. Used over the dizzy Ledger's head. `chip` labels are now HTML-escaped, so `&` is safe
- **Camera keyframes, paid ads only (Hoang, 30 Oct 2026, tutoring ad v6):** the one exception to standing rule 1. A scene may carry `"cam": [{"at": "chunk:N", "delay": s, "dur": s, "frame": <box, item:<id>, ledger, ledger-close, wide>}, ...]`. The first keyframe is the opening frame; each later one moves there at chunk N + delay over dur seconds (cubic ease in and out, zoom in log scale; `dur` 0 = a cut). Chunks count over the beats sharing the scene. A camera scene's art is clipped to y 530-1336 (never under the captions or the logo) and the pencil noise is scaled against the zoom, so close-ups boil like a normal frame. Scenes without `cam` render pixel-identical to before
- **Zone scenes:** for several rooms in one beat (one voice line), lay the rooms side by side in one wide scene (`bg: "none"`, a `backdrop` item per room: wall colour, floor, ground line, 1080 wide) and cut the camera between them
- **Course visuals (ads):** `balance_sheet` (Assets vs Liabilities + Equity, totals that do not match, red not-equal), `abc_tangle` (Overhead → Setups, Orders, Inspection → Product A, Product B, crossing arrows, "?"), `regression_guess` (scatter on x and y with three dashed candidate lines, "?"), `supply_shift` (Price/Quantity, D, S shifting right to S′, old equilibrium dot, new one marked "?")
- **Renderer fix (30 Oct 2026):** when a scene is first drawn mid-run (out-of-order stills, `canva_kit` clips that start on the 2nd beat of a scene), chunk counting now starts at the scene's first beat. Before, `at`/`until`/`cam` chunk numbers shifted by that beat's chunks in such renders; sequential video renders were never affected
- **No exams anywhere** in this ad (voice, captions, bubbles, props); courses are named as on the students' timetable, never the school

## Editable kit for Canva and CapCut (29 Oct 2026)
Hoang assembles ads as layers, not as one flat MP4. After `make_reel.sh`, run
```
tools/tts/.venv/bin/python .claude/skills/edlintics-explainer-reel/scripts/canva_kit.py <workdir> <slug> <outdir>
```
It writes the building blocks (see the docstring in `canva_kit.py`): `clips/clip-NN-<scene>.mp4` (art only, no captions or logo, cut on the same frames as the full video, so clip NN = that beat's voice line plus its gap), `clips-4x5/` (the same cropped to y 285-1635), `clean-9x16.mp4` and `clean-4x5.mp4` (clips joined with the voice), `voice/voice.wav|mp3`, `voice/line-NN.wav` (one window per beat, for re-voicing one line), `captions.srt` (the chunks as shown) and `lines.srt` (one line per beat), `endcard/endcard-*.png` (term, kp, rule, logo, cta, fn, all; transparent), `logo/`, the previews with burned-in captions, `kit.json` (times, boxes and the caption style) and `README.md`.
- Engine side: `CLEAN=1 node render.js clips <dir>` and `node render.js cardparts <dir>`; `CLEAN=1` hides captions, logo and end-card text in any render mode
- Canva build (needs Chrome for the timeline and audio): one 1080x1920 page per clip, the clip as the page's background video, the caption as an editable text layer (Inter 900, 92 px, #0F172A, centred in x 60-1020, y 300-520, key word on a #FFD45C highlight), the logo PNG 210 px wide at y 1338 with opacity 72%, the end card from editable text and the PNG parts, the voice track once at the start of the timeline, a free Canva track at volume 8. Page durations must equal the clip lengths in `clips/clips.json`; check the total against `kit.json` duration
- CapCut: import the clips in order, then `voice/voice.wav`, then `captions.srt`; `README.md` in the kit has the beat table and the caption style

## Full-frame layout and how-to pieces (1 Nov 2026, opt-in)
Hoang (1 Nov 2026): the first how-to sample left the bottom half of the phone empty. `meta.layout: "full"` (used by edlintics-howto-reel; every other reel type is unchanged) puts captions at y 228-438 (x 60-920, 84 px), the art box at x 40-940, y 450-1440, the logo at y 1462 (190 px) and the end card at y 228-1518, all inside the platform safe zones (top 220, bottom 380, right 140 px). `build_scenes.py` uses the 900:990 frame shape there and sizes Ledger at 66-78% of the box height. `make_cover.js` fits the art under the title for this layout.
- **Equation:** prop `equation` (`mode` formula or numbers, `lhs`, `num`, `den`, `result`, `note`, `w`), drawn in the art with a wavy fraction bar and a highlighter swipe on the result. End card: optional `"equation": {"lhs", "num", "den", "example"}` on the endcard beat shows a formula card under the definition (any layout; `canva_kit` card part `eq`).
- **Summary diagram:** `flow_box` takes `w`, `h` (text grows with `h`, shrinks to fit `w`) and `ghost: true` (a grey dashed placeholder under a box that pops in later); `flow_arrow` joins boxes.
- **framefill.py:** frame-fill and caption-sync report, run at the end of `make_reel.sh` (also with `STILLS_ONLY=1`); it FAILs only for the full layout (mean safe-area share under 75%, more than 2% ink in the UI zones, a caption chunk outside its voice line). Sample: 63.6% (old layout) to 80.1%.
- **Long reels and 10 MB:** `build.sh` lowers the Canva copy's video bitrate for reels over ~48 s so it stays near 9 MB (shorter reels keep 1500k), and re-encodes `<slug>.mp4` at that bitrate only if it is 10 MB or more.
- `REUSE_AUDIO=1` now also carries end-card fields (`term`, `keypoint`, `equation`, `footnote`, `cta`) from beats.json, and `STILLS_ONLY=1` no longer exits 1 because the MP4s are missing.

## Ladder layout and career-ladder pieces (12-13 Nov 2026, opt-in)
`meta.type: "ladder"` with `meta.layout: "ladder"` (used by edlintics-ladder-reel; every other reel type is unchanged). Two styles:
- **`meta.ladder_style: "bleed"` (the one Hoang approved, 13 Nov 2026):** the art fills 1080x1920 and scenes use the frame `[0, 0, 1080, 1920]`, so art coordinates are screen pixels. Captions y 228-438 (84 px) on a soft paper backing, rung title with its "n/5" pill at y 452-522, logo top right at y 468, duty chips at y 534-670. Keep faces, text and props in x 30-940, y 690-1500 (ladder shots, which have no header: from y 450); the ground line is at y 1500.
- **Left out or `"panel"` (the first preview):** art in a rounded panel x 40-940, y 456-1294 (frame `[40, 460, 900, 830]`), captions low at y 1304-1520.
- **Roles:** `title` (beat 1: a scene plus a card with `message` and an optional `tag` pill, no captions), `rung` (carries `rung` 1-5 and `chips: [{label, at}]`, where `at` is the chunk index in that beat), `climb`, `payoff`, `cta` (last: a scene plus a full-width card with `message` and the logo). `hook` and `endcard` are still accepted for the older style. `meta.rungs` lists the header titles (17 characters at most). Caption chunks are 1-4 words.
- **Ledger outfits per rung:** `intern`, `senior`, `manager`, `controller`, `cfo`; `mk_intern` to `mk_cmo`; `inv_junior` to `inv_cio`; `con_analyst` to `con_partner` (`scene_lib._ladder_wear`; the body, face and hands never change, and a short sleeve colours the first part of each arm).
- **Props:** `career_ladder`, `rung_tag` (state todo, now, done), `side_bracket`, `steps`, `floor_deco`, `dial` (the two-word slider), `match_rows`, `test_picker`, `meter`, `cal_fill`, `checklist`, `pot`, `board_table`, `org_chart`. `backdrop` takes `up` and `down` for a full-bleed room.
- **Item key `appear`:** `{"at": "chunk:N", "delay": s}` pops an item in after a delay, for staggers (the ladder props use it inside themselves).
- **Helpers:** `.claude/skills/edlintics-ladder-reel/ladder_script.py` writes the title, climb, payoff and closing scenes.
- The ladder layout waits for Inter 900 before frame 0, so the title card is in the right font on the first frame.

## Map reels and city props (13 Nov 2026, opt-in)
`meta.type: "map"` with `meta.layout: "ladder"` and `meta.ladder_style: "bleed"` (first reel: `assets/renders/map-reels/map-career-cities/`, with its generator `gen.py` and card builder `make_card.py`). Every other reel type is unchanged.
- **Roles:** `title` (beat 1, a card with `message` and `tag`), `stop` (carries `rung` = the stop number and `chips`; each stop needs a scene with a `landmark`), `summary` (after the last stop), then one or two `cta` cards. `meta.rungs` lists the 8-12 stop titles (15 characters at most), `meta.rung_label: "STOP {n} OF {N}"` sets the header pill, and `meta.cities` holds one `{city, career, fact, source, figureDate}` per stop. The validator fails "best" and "highest paying" unless `meta.superlative_source` is set, and fails a scene without Ledger.
- **Props (`scripts/map_props.py`, installed into `scene_lib`):** `world_map` (coastlines only, from `map_land.json`, Natural Earth public domain; no country borders, no labels; `lon`, `lat`, `k` pixels per degree, optional `box`), `map_pin` (state done, now, todo), `map_dot` (numbered badge for the summary map), `map_label`, `map_plate`, `flight_path` (dots that `grow` with a mover), `suitcase`, `cloud`, `plane`, `cargo_ship` and `landmark` (`kind`: golden_gate, big_ben, eiffel, erasmus, euro, minster, burj, mbs, hk, fab, tokyo_tower, empire). Place pins with `map_props.map_xy(lon, lat, view)`.

## In-lesson videos (type lesson, 5 Nov 2026)
Hoang (5 Nov 2026): "no time cap for in lesson video (ideal time is 2-3 minutes), vertical design, script need to be in full sentence with transitional words, using the same drawing style like what we have with the explainer reels". Set `meta.type: "lesson"`; `meta.layout: "full"` is recommended. Same scenes, Ledger, pencil look, voice and captions as the reels.
- **Roles:** an optional `hook` (beat 1 only, a direct question to the learner ending in `?`, never a social tease), then `story`, `definition`, `example`, `defcard` and `takeaway` in any order. At least one `defcard`; no `endcard`, `loop` or `cta`
- **Defcard:** `{"role": "defcard", "term", "definition", "text", "equation"?}`. It renders like the end card without the logo: the term large, the full-sentence definition (6-30 words, no closing full stop) with the highlighter, and an optional `equation {lhs, num, den}` card. The voice `text` must read the term and then the definition word for word. It has no `img` and no caption chunks. Defcards may come after a section (inline) or all at the end (grouped, as in FA1 2.4), more than once, and may be the last beat
- **Nothing promotional:** no end card, logo (corner logo and card logo are off: `nologo` in scenes.json, set from the type), follow line, loop-back or edlintics.com. The validator FAILs follow, subscribe, link-in-bio, brand-name and tease lines
- **Length:** 60 s to about 4 minutes (177-708 words at 2.95 words a second); the 354-531 word target (2-3 minutes) is a WARN only. Beats may run to about 12 s. Captions are 2-5 word chunks with no closing full stop
- **Kept checks:** full sentences ending in `.` or `?` with transitions (story-flow WARN, with however, for example, as a result, in other words and the like), no exclamation points or emoji, no tutoring. Money may be in any currency; a lesson follows its course's currency, and more than one currency sign in a post gives a WARN
- **Not required:** caption, caption_x, first comment, Threads fields, follow CTA, logo end card, how-to hook question. Meta needs only `type`, `title` and `slug`
- **FA1 cast and lesson props (5 Nov 2026, first used by FA1 2.4 cards 2 and 10):** `plot` (the bar-chart character, owner of the clothes store) and `tempo` (the hourglass, at the till) are the EdCharacter cast, drawn from `tutoring-web/public/mascot/plot.svg` and `tempo.svg` in Ledger's frame and arm poses. They are no-suit: never add a collar or tie. Moods `smile, happy, focused, surprised, worried, thinking, sigh`; `arm`, `larm`, `flip`, `tilt` and `gaze` work as on Ledger. Props: `till` (counter and register; list the character before it and raise them about 150 x s so the counter hides the legs), `label` (title / amount / note card, "/" breaks the title), `icon_tile` and `big_icon` (13 small icons: bags, key, shield, invoice, box, poster, mirror, bank, wallet, payslip, percent, bulb, shelf, jacket), `months`, `block` (bar pieces and trays), `t_account`, `letter_tiles` (DEAD CURLS; swap labelled and glow states with `at`/`until`), `shopfront`, `shopping_bag` and `bank_app`. Lesson scenes in FA1 2.4 use one explicit frame `[40, 490, 900, 990]` with the full layout, so art coordinates map to the screen 1:1 (minus 40 in y)
- **Outputs (next to the MP4):** `<slug>.mp4` (crf 20, no 10 MB re-encode; postcheck skips the size check), `<slug>.vtt`, `<slug>-transcript.txt` (spoken `text`, never `say`, `[tags]` dropped, paragraphs per role run, each defcard as a term line and a definition line, no full stop closing a paragraph), and `<slug>-poster.jpg` at 1080x1920 from the first frame (the hook). `make_cover.js` is not used for lessons because its kicker and title are social cover copy
