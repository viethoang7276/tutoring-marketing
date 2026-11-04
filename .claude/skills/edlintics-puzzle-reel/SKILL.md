---
name: edlintics-puzzle-reel
description: Turn one Edlintics puzzle into a 9:16 puzzle reel (up to 2 minutes) with the Kokoro voice reading the question, a silent 5-second ticking countdown, a hand that taps the right option, the answer reveal on the same diagram, a 3-sentence explanation and an end card. Code-rendered (no AI images or clips). Approved by Hoang 27 Oct 2026 (bottleneck v2 with voice). Also the reference for the future interactive puzzle exercise (REQ-0005)
---

# Edlintics puzzle reel

Reference build: `examples/bottleneck/` (bottleneck puzzle, 26 Oct). Worked-steps reference: `examples/tax-steps/puzzle.json` (tax bracket, 2 Nov). Hoang approved the voiced v2 on 27 Oct 2026. The video is in `docs/feature-requests/assets/REQ-0005/`

## Flow (voiced cut, up to 2 minutes from 4 Nov 2026; the explanation and worked steps are full sentences with transitional words)
1. **Question (0-10 s):** the question block (serif, 66 px, max 4 lines, one `*key word*` in blue) and the diagram drawing in. The voice reads the question
2. **Pause (10-15 s):** the voice says "Pause and think before the timer ends", then a silent 5-second countdown ring (5, 4, 3, 2, 1, one full second each) with a soft tick. On screen: "Pause and think, then comment your answer"
3. **Hand tap (about 1.9 s, added 27 Oct 2026 for v3):** when the countdown ends the ring fades and a flat line-art pointing hand (ink outline, white fill, blue cuff, about 155 px long, drawn in `render.html`) comes up from below. It points up, tilted 20 degrees to the right, with the fingertip on the option's letter circle and the hand body below and left of the circle, so the option text stays fully readable. It hovers briefly over a wrong option, moves to the right one and taps it: a press-down scale, a blue ripple ring from the circle and a soft generated tap sound. The tapped option fills blue with a white check. The hand slides back down and out before the explanation. On the lower rows (C, D) the cuff dips slightly below y 1250
4. **Reveal:** a chime 0.35 s after the tap, then the same diagram changes (highlight, new values) and the other options dim
5. **Explanation:** 2-3 full sentences, one at a time, read by the voice. The last one is the takeaway in blue
5b. **Worked steps (opt-in, Hoang 2 Nov 2026):** when the puzzle JSON has `steps`, the 2-3 sentence explanation is replaced by the calculation itself. About 1.4 s after the reveal the options, logo and diagram fade out and the steps appear one line at a time (x 372-960, y 230-1440, the block centred and spaced to fill it), each read by the voice. Main lines are 70 px bold; a line too wide for one row breaks before its last "=" (formula, then "= result") and shrinks only if still too wide. The current line is ink with a yellow highlighter swipe; earlier lines dim to grey. **The guide Ledger (Hoang picked option F of 6 on 2 Nov 2026):** the standard suit Ledger in the hand-drawn pencil style with round glasses and a thin wooden pointer, about 250 px tall (transparent PNG `assets/renders/cover-templates/ledger/ledger-guide-point.png`, drawn by `scene_lib.ledger(outfit="suit", arm="point", glasses=True, pointer=True)` with the pencil filter), stands left of the lines and glides line to line with his pointer tip on the current one. **4-5 steps at most** (the build prints a WARN above 5) and short voice lines (about 3-5 s each), so the reel stays about 45-50 s. The explanation line with `"style": "takeaway"` comes last, in blue serif. Use steps for any puzzle with a calculation (percentages, tax, margins, interest, averages); keep the short explanation for logic-only puzzles
6. **End card:** "Follow Edlintics to learn business concepts interactively" (serif, 86 px, 3 lines) under the large logo, read by the voice, then a fade to white so it loops

The tap timing comes from `build.py` (`cd_end`, `tap_t` = countdown end + 1.55 s, reveal = countdown end + 1.9 s). The decoy option is B, or A when the answer is B

The voice-free cut (`novoice`) uses a 6-second countdown and is quieter (about -20 LUFS) because music is added later

## Build
```
.claude/skills/edlintics-puzzle-reel/scripts/build.sh <puzzle.json> <outdir> [voice|novoice|both]
STILLS_ONLY=1 ...   # timeline, audio and contact sheet only, for a quick layout check
```
Uses the explainer-reel tools: Kokoro `af_heart` at 1.08 in `tools/tts/.venv`, the bundled ffmpeg, puppeteer-core from `.claude/skills/edlintics-explainer-reel/scripts/node_modules` and the installed Chrome. Output: `puzzle-reel-<slug>.mp4`, `-novoice.mp4` and contact sheets, 1080x1920, 24 fps, under 10 MB

## Puzzle JSON (see examples/bottleneck/puzzle.json)
`question` (with `*key*`), `diagram` (SVG in the question state, element ids for the reveal), `options` A-D, `answer`, `prompt_text` / `prompt_say`, `countdown` {voice, novoice}, `reveal` (list of `{sel, attr}` or `{sel, text}` changes), optional `pulse`, `explanation` (list of `{text, say?, style?}`), optional `steps` (list of `{text, say?, label?, hl?}`: 3-5 worked lines such as "20% × $29,000 = $5,800"; `label` is a short grey heading above the line ("Tax at $29,000", "Extra tax"), under about 28 characters; `say` reads the line in words, short; `hl` is a diagram selector (the diagram is faded during the steps, so it rarely shows); keep each side of the "=" under about 15 characters so it stays at 70 px). Reference: the v2 demo, 4 steps (tax at $29,000, tax at $31,000, extra tax, take-home change) plus the takeaway, 50.4 s, `end_text` / `end_say` (default end card: "Follow Edlintics to learn business concepts interactively")

## Rules
- Layout v4 (28 Oct 2026, Hoang: "use the height of the screen more"; applies from the 2 Nov puzzles, the 27 Oct-1 Nov reels keep v3): content from y ~190 to y 1560; only the bottom ~360 px (caption and username overlay) stays empty, and the right-hand buttons sit beside the options. Question 74 px in a 390 px block from y 190, diagram 1000 px wide from y 620, "Pause and think" line at y 1075, options 54 px with 72 px circles from y 1190, timer beside them at x 680, logo under the timer at y 1488, explanation 70 px in the question block
- Diagrams: draw new puzzle diagrams taller, about 900x500-540 (viewBox), so the diagram fills the space down to the prompt line. The 27 Oct batch was 900x345, which leaves the frame looking flat
- House rules: US dollars, full sentences, no exclamation points, no emoji, no full stop at the end of any line, brand blue #2960c7, ink #0d1523, white background
- Diagram style follows the edlintics-puzzle-visuals skill
- Sentences readable at 17 characters per second or slower
- No AI images or clips. Do not turn on Meta "AI info" for voiced reels (Hoang, 2 Nov 2026)
- The first comment never reveals the answer (the reel itself does)
- Check the contact sheet at phone width before showing Hoang

## Shell rule: never let `$` amounts expand
When a shell command writes captions, JSON or hub docs that contain dollar amounts, quote the heredoc (`<<'EOF'`) and pass paths as arguments or env vars, or write the JSON from a file. An unquoted heredoc on 27 Oct turned "$3,000" into ",000" in two scheduled puzzle reels (found 29 Oct)
