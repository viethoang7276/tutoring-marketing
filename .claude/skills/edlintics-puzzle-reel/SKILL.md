---
name: edlintics-puzzle-reel
description: Turn one Edlintics puzzle into a 9:16 puzzle reel (up to 2 minutes) with the Kokoro voice reading the question, a silent 5-second ticking countdown, a hand that taps the right option, the answer reveal on the same diagram, a 3-sentence explanation and an end card. Code-rendered (no AI images or clips). Approved by Hoang 27 Oct 2026 (bottleneck v2 with voice). Also the reference for the future interactive puzzle exercise (REQ-0005)
---

# Edlintics puzzle reel

Reference build: `examples/bottleneck/` (bottleneck puzzle, 26 Oct). Worked-steps reference: `examples/tax-steps/puzzle.json` (tax bracket, 2 Nov). Hoang approved the voiced v2 on 27 Oct 2026. The video is in `docs/feature-requests/assets/REQ-0005/`

## Flow (voiced cut, up to 2 minutes from 4 Nov 2026; the explanation and worked steps are full sentences with transitional words)
1. **Question:** the slot's full question, word for word as in the caption (one `*key word*` in blue), and the diagram drawing in. The voice reads all of it, about 7-20 s
2. **Pause:** the voice says "Pause and think before the timer ends", then a silent 5-second countdown ring (5, 4, 3, 2, 1, one full second each) with a soft tick. On screen: "Pause and think, then comment your answer"
3. **Hand tap (about 1.9 s, added 27 Oct 2026 for v3):** when the countdown ends the ring fades and a flat line-art pointing hand (ink outline, white fill, blue cuff, about 155 px long, drawn in `render.html`) comes up from below. It points up, tilted 20 degrees to the right, with the fingertip on the option's letter circle and the hand body below and left of the circle, so the option text stays fully readable. It hovers briefly over a wrong option, moves to the right one and taps it: a press-down scale, a blue ripple ring from the circle and a soft generated tap sound. The tapped option fills blue with a white check. The hand slides back down and out before the explanation. On the lower rows (C, D) the cuff dips slightly below y 1250
4. **Reveal:** a chime 0.35 s after the tap, then the same diagram changes (highlight, new values) and the other options dim
5. **Explanation:** 2-3 full sentences, one at a time, read by the voice. The last one is the takeaway in blue
5b. **Worked steps (opt-in, Hoang 2 Nov 2026):** when the puzzle JSON has `steps`, the 2-3 sentence explanation is replaced by the calculation itself. About 1.4 s after the reveal the options, logo and diagram fade out and the steps appear one line at a time (x 372-960, y 230-1440, the block centred and spaced to fill it), each read by the voice. Main lines are 70 px bold; a line too wide for one row breaks before its last "=" (formula, then "= result") and shrinks only if still too wide. The current line is ink with a yellow highlighter swipe; earlier lines dim to grey. **The guide Ledger (Hoang picked option F of 6 on 2 Nov 2026):** the standard suit Ledger in the hand-drawn pencil style with round glasses and a thin wooden pointer, about 250 px tall (transparent PNG `assets/renders/cover-templates/ledger/ledger-guide-point.png`, drawn by `scene_lib.ledger(outfit="suit", arm="point", glasses=True, pointer=True)` with the pencil filter), stands left of the lines and glides line to line with his pointer tip on the current one. **4-5 steps at most** (the build prints a WARN above 5) and short voice lines (about 3-5 s each), so the reel stays under about 60 s with the full question. The explanation line with `"style": "takeaway"` comes last, in blue serif. Use steps for any puzzle with a calculation (percentages, tax, margins, interest, averages); keep the short explanation for logic-only puzzles
6. **End card:** "Follow Edlintics to learn business concepts interactively" (serif, 86 px, 3 lines) under the large logo, read by the voice, then a fade to white so it loops

The tap timing comes from `build.py` (`cd_end`, `tap_t` = countdown end + 1.55 s, reveal = countdown end + 1.9 s). The decoy option is B, or A when the answer is B

The voice-free cut (`novoice`) uses a 6-second countdown and is quieter (about -20 LUFS) because music is added later

## The question is written out in full (Hoang, 6 Nov 2026)
Hoang on the 10 Nov credit card puzzle: "Why it is so short, give the full context ... It needs to precise and cannot cut the words short. We can extent the the text limit". Then, on every puzzle: "it is not fully written like the caption, make watchers confused. It is best to write all out like in the caption where you state the full context".

**Why:** a shortened question drops who, where, the conditions and the units. Without them the viewer cannot solve it, or solves a different puzzle.

**Rule:**
- `question` in `puzzle.json` is the slot's `question`, word for word: the same words as the caption. The only change is one `*key word*` in blue.
- `caption` in `puzzle.json` is the slot's `caption`. The build stops unless the question appears in the caption word for word.
- `reel.question_short` is retired. Do not write it on new slots, and never build from it. `reel.options_short` stays, because the options are the same answers without the letters.
- The voice reads the whole question. Never give the question a shorter `say`.
- If a question is too long to read comfortably, fix the question in the slot, so the caption and the video stay the same. Do not cut it only in the video.

**Layout (v5, set by the text):** the question sits from y 190 and fits itself from 74 px down to 46 px within 440 px. Past four lines it reads left-aligned. The diagram takes the space left, down to y 1062, so keep diagram labels at 28 px or more in a 900-wide viewBox. Below 46 px the block may run to 560 px; past that the build stops. Do not shorten the question then: widen the limit in `render.html` and check the diagram still reads. Explanation lines fit the same block.

**Before showing Hoang, check on the contact sheet:** the question matches the caption, the text is readable at phone width, and the diagram labels are readable under it.

## Build
```
.claude/skills/edlintics-puzzle-reel/scripts/build.sh <puzzle.json> <outdir> [voice|novoice|both]
STILLS_ONLY=1 ...   # timeline, audio and contact sheet only, for a quick layout check
```
Uses the explainer-reel tools: Kokoro `af_heart` at 1.08 in `tools/tts/.venv`, the bundled ffmpeg, puppeteer-core from `.claude/skills/edlintics-explainer-reel/scripts/node_modules` and the installed Chrome. Output: `puzzle-reel-<slug>.mp4`, `-novoice.mp4` and contact sheets, 1080x1920, 24 fps, under 10 MB

## Puzzle JSON (see examples/bottleneck/puzzle.json)
`question` (the slot's full question with one `*key*`), `caption` (the slot's caption, checked against the question), `diagram` (SVG in the question state, element ids for the reveal), `options` A-D, `answer`, `prompt_text` / `prompt_say`, `countdown` {voice, novoice}, `reveal` (list of `{sel, attr}` or `{sel, text}` changes), optional `pulse`, `explanation` (list of `{text, say?, style?}`), optional `steps` (list of `{text, say?, label?, hl?}`: 3-5 worked lines such as "20% × $29,000 = $5,800"; `label` is a short grey heading above the line ("Tax at $29,000", "Extra tax"), under about 28 characters; `say` reads the line in words, short; `hl` is a diagram selector (the diagram is faded during the steps, so it rarely shows); keep each side of the "=" under about 15 characters so it stays at 70 px). Reference: the v2 demo, 4 steps (tax at $29,000, tax at $31,000, extra tax, take-home change) plus the takeaway, 50.4 s, `end_text` / `end_say` (default end card: "Follow Edlintics to learn business concepts interactively")

## Animated explanation (opt-in pilot, 7 Nov 2026, not yet a standard)
Hoang: "yes, in the answer explaination", with "arrow green red illustation with graph, number inside with people trading action and supplement info" where it fits, and objects that move with the voice. Add `explain_anim` to a puzzle that has `steps`. Without it the reel renders exactly as before. The hook, question, countdown, tap, reveal, end card and all timing stay the same, and no voice line changes. Worked example: `assets/renders/pilot-animation/puzzle-explanation/puzzle.json`. Code: `scripts/explain_anim.js`.

**Layout:** the current line sits beside Ledger at the top (one at a time, y 200-450), and the items use y 460-1520, x 60-960, in screen pixels.

**Time:** `"at": "step:N"` is the start of the voice on line N (the takeaway is the last line). `"word"` moves to a word in that line, estimated by character position, so it can be about 0.3 s out; adjust with `"delay"`. `"until"`, `"until_word"` and `"until_delay"` remove an item.

**Items** (`"p"`): `counter` (the diagram's blue bar with a ticking number: `start`, `keys` `[{at, to, dur}]`), `line_chart` (`min`, `max`, `grid`, `ref`, `points` `[{v, tone, label, at, dur, tag}]`), `arrow` (`dir`, `tone`, `text`; on debt, red rises and green falls), `chip` (a pill that travels: `to`, `arc`, `trail`), `split_bar` (`whole`, `parts`, each with `pulse`), `person` (`acts` `[{at, pose, mood}]`; poses down, give, take, raise, cheer, shrug), `note` (`text` or `lines`).

**The build stops** on text under 34 px, and on any number that is not in the puzzle. A worked-out number goes in `"derived": {"$1,020": "$1,000 + $20"}`. A made-up number needs `"example": true` on a note, which labels it on screen.

## Picture explanation (opt-in, 7 Nov 2026, awaiting Hoang's verdict)
Hoang: "even with the puzzle I feel like it is too dry with only number, may be we should use graphic to explain as well". Use the same `explain_anim` block, but tell the puzzle's situation as a picture: its people and objects act with the voice, with numbers as labels on them. At most 2 or 3 things to follow at once, so clear earlier items with `until`; text at 34 px or more. Code: `scripts/explain_scene.js`. Worked examples: `assets/renders/upgraded-7nov/<slot id>/puzzle.json` for 2026-11-09-1000 to 2026-11-15-1000. A puzzle with only an `explanation` needs `steps` for this: keep each voiced sentence as `say` and give it a shorter `text`, because the on-screen text may be shorter than the voice.

Items (`"p"`), on top of those in "Animated explanation". All take `x`, `y`, `at`, `until`, `fade`:
- `sprite`: one drawn object. `kind`: cafe, card, bank, note, tag, block, cart, shirt, pants, phone, jacket, wheat, bread, hat, store, clock, gauge, receipt, board, cross. Optional: `s`, `pop`, `moves` `[{at, to, dur, arc, scale, rot, ease}]`, `pulse` `[{at, dur, amp}]`, `text`, `texts` `[{at, text}]` to swap text, `value` `{prefix, start, keys: [{at, to, dur}]}` for a ticking number, `lines`, `fs`, `tc`, `tpos`, `label` `{text, dx, dy, fs, tone, pill, at, until}`. (x, y) is the centre, except top left for cafe and block and the middle of the ground for store. Kind extras: `w`, `h`, `tone`, `fill` (board), `sweep` `{at, to, dur}` (clock), `start` and `keys` (gauge), `wkeys` and `grow` (block), `sw` (cross)
- `walker`: the person prop with `moves`; bobs while moving. `name`, `nfs`, `color`, `s`, `acts`
- `flow`: people who enter, sit and leave. `grid` `{x, y, cols, rows, dx, dy}`, `enter` and `exit` point lists, `arrive` `[{at, n, dur}]`, `count` `{x, y, fs, suffix}`. Once every seat is taken, each arrival sends out the person in that seat, so the room stays full
- `dots`: a crowd. `n`, `cols`, `x`, `y`, `dx`, `dy`, `r`, `tone`, `mini`, `flips` `[{at, idx, tone, until}]`

Before showing Hoang, check mid-move frames as well as the stills: nothing covers a label, and the last frame has no more than 3 things to read.

## Rules
- Layout v4 (28 Oct 2026, Hoang: "use the height of the screen more"; applies from the 2 Nov puzzles, the 27 Oct-1 Nov reels keep v3): content from y ~190 to y 1560; only the bottom ~360 px (caption and username overlay) stays empty, and the right-hand buttons sit beside the options. The question and diagram follow layout v5 above (6 Nov 2026), "Pause and think" line at y 1075, options 54 px with 72 px circles from y 1190, timer beside them at x 680, logo under the timer at y 1488, explanation 70 px in the question block
- Diagrams: draw new puzzle diagrams taller, about 900x500-540 (viewBox), so the diagram fills the space down to the prompt line. The 27 Oct batch was 900x345, which leaves the frame looking flat
- House rules: one currency in the post and rotated across posts, full sentences, no exclamation points, no emoji, no full stop at the end of any line, brand blue #2960c7, ink #0d1523, white background
- Diagram style follows the edlintics-puzzle-visuals skill
- Sentences readable at 17 characters per second or slower
- No AI images or clips. Do not turn on Meta "AI info" for voiced reels (Hoang, 2 Nov 2026)
- The first comment never reveals the answer (the reel itself does)
- Check the contact sheet at phone width before showing Hoang
- Worked steps are full lines too: "Jordan pays $30", never a bare "$30"

## Shell rule: never let `$` amounts expand
When a shell command writes captions, JSON or hub docs that contain dollar amounts, quote the heredoc (`<<'EOF'`) and pass paths as arguments or env vars, or write the JSON from a file. An unquoted heredoc on 27 Oct turned "$3,000" into ",000" in two scheduled puzzle reels (found 29 Oct)
