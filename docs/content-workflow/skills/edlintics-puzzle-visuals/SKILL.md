---
name: "edlintics-puzzle-visuals"
description: "Design rules for Edlintics two-slide puzzle carousels in a clean, diagram-first style (inspired by Brilliant's clarity, never copied). Use before building or reviewing any puzzle slide in Canva or SVG."
---

# Edlintics puzzle visuals

Goal: the picture IS the puzzle. A student should understand the question from the diagram in 3 seconds, with almost no reading. Use Brilliant only as a reference for clarity and restraint. Never copy its problems, illustrations, layouts or assets.

## Frame (both slides)
- 1080x1350, white background, Edlintics logo small at the bottom (template position). No category kicker like "OPERATIONS QUIZ". If a topic label is needed, keep it tiny and grey.
- Question at the top in the template serif, centred, max 2 lines, about 40px.
- Diagram centred, occupying at least 60% of the canvas. Leave generous white space around it.

## Diagram style
- Thin ink line art: #0d1523 strokes, 3-4px. Flat fills only.
- Max 2 accent colours plus ink (template blue #2960c7 first; one warm accent only if it carries meaning, e.g. the unknown).
- Numbers and labels sit ON the geometry (on a bar, beside an edge, inside a box). No separate legend when a label can sit on the shape.
- Mark the unknown clearly, e.g. a single highlighted shape or a "?".
- Forbidden: rounded tinted panels holding text, drop shadows, gradients, decorative icon rows, bold everywhere, emoji, stock art, mascots unless the brief asks for one.

## Text budget
- Slide 1: at most about 25 words outside the diagram. Do not restate the question as a big coloured headline.
- Max 3 font sizes per slide. Bold only for the single most important label.
- Optional answer options: a small row of circled letters (A) (B) (C) under the diagram.

## Assumptions (Edlintics rule: essential ones must be on the card)
1. Encode visually first: arrows for sequence (print -> pack), the word OR between alternatives, the number of stations shown as the number of boxes, a clock axis for time.
2. Whatever cannot be drawn goes in ONE footnote of max 2 lines, 26-28px, grey #5b6475, at the bottom above the logo.
3. Non-essential context goes in the caption, not on the card.

## Answer slide
- Reuse the same diagram so the eye recognises it. Reveal by changing it: highlight, fill in the timeline, mark the winner.
- One answer sentence (max 2 lines) and one takeaway line. No paragraphs.

## Anti-slop review (fail the slide if any is true)
- Text covers more than about 30% of the canvas.
- Any tinted rounded box exists only to hold text.
- The question appears twice.
- More than 3 font sizes or more than 3 colours (plus ink and grey).
- A legend explains something a label could show.
- The answer is readable on slide 1.
- The diagram would still be confusing with the text removed.

## Canva build notes
- The Canva connector cannot set fonts: added text uses Canva's default sans. Prefer reusing the template's own serif text boxes; ask the person to add spare serif label boxes to the template, or flag the font gap.
- Build the diagram with native shapes (insert_shape paths) and native text, never a flattened image.
- Workflow: sketch as SVG first, render and run the anti-slop review, then build in Canva, then preview both slides at phone width before asking for approval.