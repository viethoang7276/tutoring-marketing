---
name: edlintics-puzzle-reel
description: Turn one Edlintics puzzle into a 9:16 puzzle reel (25-35 s) with the Kokoro voice reading the question, a silent 5-second ticking countdown, a hand that taps the right option, the answer reveal on the same diagram, a 3-sentence explanation and an end card. Code-rendered (no AI images or clips). Approved by Hoang 27 Oct 2026 (bottleneck v2 with voice). Also the reference for the future interactive puzzle exercise (REQ-0005)
---

# Edlintics puzzle reel

Reference build: `examples/bottleneck/` (bottleneck puzzle, 26 Oct). Hoang approved the voiced v2 on 27 Oct 2026. The video is in `docs/feature-requests/assets/REQ-0005/`

## Flow (voiced cut, about 34 s)
1. **Question (0-10 s):** the question block (serif, 66 px, max 4 lines, one `*key word*` in blue) and the diagram drawing in. The voice reads the question
2. **Pause (10-15 s):** the voice says "Pause and think before the timer ends", then a silent 5-second countdown ring (5, 4, 3, 2, 1, one full second each) with a soft tick. On screen: "Pause and think, then comment your answer"
3. **Hand tap (about 1.9 s, added 27 Oct 2026 for v3):** when the countdown ends the ring fades and a flat line-art pointing hand (ink outline, white fill, blue cuff, about 155 px long, drawn in `render.html`) comes up from below. It points up, tilted 20 degrees to the right, with the fingertip on the option's letter circle and the hand body below and left of the circle, so the option text stays fully readable. It hovers briefly over a wrong option, moves to the right one and taps it: a press-down scale, a blue ripple ring from the circle and a soft generated tap sound. The tapped option fills blue with a white check. The hand slides back down and out before the explanation. On the lower rows (C, D) the cuff dips slightly below y 1250
4. **Reveal:** a chime 0.35 s after the tap, then the same diagram changes (highlight, new values) and the other options dim
5. **Explanation:** 2-3 full sentences, one at a time, read by the voice. The last one is the takeaway in blue
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
`question` (with `*key*`), `diagram` (SVG in the question state, element ids for the reveal), `options` A-D, `answer`, `prompt_text` / `prompt_say`, `countdown` {voice, novoice}, `reveal` (list of `{sel, attr}` or `{sel, text}` changes), optional `pulse`, `explanation` (list of `{text, say?, style?}`), `end_text` / `end_say` (default end card: "Follow Edlintics to learn business concepts interactively")

## Rules
- Layout: content from y ~250 to y 1250; the bottom ~670 px and right ~120 px are covered by platform buttons. Question 64-72 px, diagram ~900 px wide, options 48 px, explanation 60-64 px
- House rules: US dollars, full sentences, no exclamation points, no emoji, no full stop at the end of any line, brand blue #2960c7, ink #0d1523, white background
- Diagram style follows the edlintics-puzzle-visuals skill
- Sentences readable at 17 characters per second or slower
- No AI images or clips. The Kokoro voice means Meta "AI info" may be needed (test H16)
- The first comment never reveals the answer (the reel itself does)
- Check the contact sheet at phone width before showing Hoang
