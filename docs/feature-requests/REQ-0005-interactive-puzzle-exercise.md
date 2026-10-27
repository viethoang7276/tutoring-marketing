# REQ-0005  ·  Interactive puzzle exercise (inspired by the puzzle reel)

- **Status:** proposed
- **Date:** 2026-10-27
- **Source:** research (our own social format)
- **Targets metric:** north-star session completion; acquisition (social puzzles that lead into the product)
- **Priority (CMO view):** medium
- **Effort guess (CMO, non-binding):** M

## Summary
Hoang approved a "puzzle reel" format on 27 Oct 2026: a question with a diagram, a short ticking timer to think, the answer revealed on the same diagram, a 2-3 sentence explanation and the concept it teaches. He wants it as inspiration for a future interactive exercise in the app, so the daily social puzzles and the product can share one experience. There is no such exercise in the app yet

Reference video and frames: `docs/feature-requests/assets/REQ-0005/puzzle-reel-bottleneck-v2.mp4` and `-contact-sheet.png`. Source data format: `.claude/skills/edlintics-puzzle-reel/examples/bottleneck/puzzle.json`

## Evidence
- Our 7-day numbers (perf/latest, 27 Oct): video posts get 2-3x the views of image puzzles (Facebook median 31-181 vs 15; Instagram 61-85 vs 33). Puzzles are our most frequent format (8 in 7 days) and get comments
- The puzzle reel was built because of this; its structure (think, commit, reveal, explain) is also a standard active-recall pattern
- Hypothesis only: no first-party product data yet

## Hypothesis
We believe that **an interactive puzzle exercise that mirrors the social puzzle reel** for **business students and professionals who meet us through social puzzles** will raise **session completion and sign-ups from social** because **the same question they saw in a reel can be answered for real, with feedback and the concept behind it**

## Job to be done
"When I see a business puzzle, I want to try it myself and see right away why the answer is right, so that I learn the concept, not just the fact"

## Proposed requirements (CTO owns the final design)
- The system shall show a puzzle question with a diagram, with one key word highlighted
- The system shall offer an optional think timer (e.g. 5 s, skippable, accessible: no time limit enforced, reduced-motion respected)
- The system shall let the student commit an answer (multiple choice first; numeric later) before anything is revealed
- The system shall reveal the answer by changing the same diagram (highlight, new values) rather than showing a new picture
- The system shall show a short explanation (2-3 sentences) and link to the concept it teaches (Key concepts)
- The system shall let authors (COO, admin editor) create these from a small data structure similar to the puzzle JSON: question, diagram, options, answer, reveal changes, explanation lines, concept
- Nice to have: the same data can render the social puzzle reel (via the video engine, REQ-0004), so one authored puzzle feeds both the app and social

## Success signal
Once live: completion rate of puzzle exercises vs other exercise kinds; later, sign-ups attributed to social puzzle posts that link to a public puzzle

## Out-of-scope check
Marketing does not import app code; the reel pipeline stays in the marketing repo and only shares a data shape. Not a request to change the schema now; the CTO decides if and when (schema work is serial and CTO-only). Related: REQ-0002 (daily puzzle page), REQ-0004 (video engine)

## Decision log
- 2026-10-27 — proposed by CMO after Hoang's note: "the video is an inspiration for the team to create the exercise later, we can use it for the exercise engine"
- _(Hoang: approve / defer / reject + reason here.)_
