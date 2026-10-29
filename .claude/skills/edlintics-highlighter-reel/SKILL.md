---
name: edlintics-highlighter-reel
description: Make one Edlintics "highlighter" reel (9:16, 30-40 s). A printed Edlintics infographic sheet lies on a wooden desk, and a drawn hand with a yellow highlighter traces the chart and highlights each label as the ElevenLabs voice reads it, with big 2-4 word karaoke captions under the sheet and an end card. Code-rendered (no AI images, no real hands or faces). Used for "watch the numbers" ideas such as compounding, break-even and margins. Written step by step for a cheaper model. First reel: compounding (30 Oct 2026, from Hoang's reference video)
---

# Edlintics highlighter reel

Reference build: `examples/compounding/` (`make_sheet.py` → `sheet.svg`, `script.json`). Output: `assets/renders/reels/2026-10-30-compounding/`.

## The format
- **Frame:** a wooden desk (an SVG noise texture) with a white sheet (960x1300, tilted -0.7 degrees) from y 96 to y 1400. The Edlintics logo sits at the top of the sheet. Brand blue #467DE3, ink #0F172A, Inter (headings), Lato (figures), Source Serif 4 (end-card line)
- **Hand:** flat line art (ink 5 px outline, white fill, blue cuff, light sleeve) holding a yellow highlighter, about 120 px across the fist. The nib tip is the point that moves. It rests low on the right in the opening frame, so the title is clear, and leaves before the end card
- **Highlights:** yellow (#FFD84A, 85%, multiply blend) and they stay on, like real ink. `mark` sweeps across a text element; `trace` follows a path (the chart curve) up to a dot
- **Captions:** 2-4 words, white Inter 900 at 98 px with a dark outline, one key word in yellow, on the desk at y 1425-1565. They are timed from the real word timings (ElevenLabs with-timestamps), not guessed
- **End card:** white, logo, the term (132 px), a blue rule, the key point with a highlighter sweep, and "Follow Edlintics to learn business concepts". It fades back to the clean opening frame, so the video loops
- **Sound:** the voice plus a soft felt-tip sound during each stroke, at -14 LUFS. There is no music in the file: add the Canva track at volume 8 later, as for every reel

## Steps
1. **Numbers first.** Write `examples/<slug>/make_sheet.py` (copy the compounding one). Compute every number in two independent ways (for example a loop and a closed formula) and `assert` that they agree, plus the rounded figures you print on the sheet. It writes `numbers.json`, which goes into the slot's `maths_check`
2. **Sheet.** The same script writes `sheet.svg` (viewBox 0 0 960 1300). Give an `id` to every element the hand will highlight (a `<text>` or `<tspan>`) and to the curve (`<path id="curve">`) and its dots (`<circle id="dot1">`). State the assumptions in small print (19 px or larger) at the bottom, and say the figures are an illustration, not advice or a promise. Keep slide lines as full sentences. Use US dollars
3. **Script.** Write `examples/<slug>/script.json`:
   - `beats`: 7-9 beats. Each has a `text` (a full spoken sentence), `chunks` (the captions) and `do` (the highlights)
   - A chunk is `{"text", "n"?, "key"?}`. `n` is how many spoken words it covers when the caption is written differently (for example "$500 a month" covers "five hundred dollars a month", so `n: 5`). The chunk word counts must add up to the beat's spoken words; the build checks this
   - A highlight is `{"mark": "#id", "at": "<spoken word>"}` or `{"trace": "#curve", "to": "#dotN", "at": "<word>", "until": "<word>"}`. `at` and `until` are words from that beat's text (first match), or seconds from the beat start. A trace continues from where the last trace on that path ended
   - `endcard`: `term`, `keypoint`, `follow` (no full stop at the end) and `say` (what the voice reads)
   - 80-95 spoken words in total give 33-38 s
4. **Quick check:** `STILLS_ONLY=1 .claude/skills/edlintics-highlighter-reel/scripts/build.sh examples/<slug>/script.json <workdir>`. Open `<workdir>/<slug>-contact-sheet.png` (one still just after each highlight)
5. **Full build:** the same command without `STILLS_ONLY`. It ends with `CHECK OK` (1080x1920, audio, length, under 10 MB)
6. **Cover:** `TIMELINE=<workdir>/timeline.json NODE_PATH=.claude/skills/edlintics-explainer-reel/scripts/node_modules node .claude/skills/edlintics-highlighter-reel/scripts/make_cover.js <t> <workdir>/<slug>-cover.png "Explained in 35 seconds" "<3-6 word title with one *keyword*>"`. Pick a `<t>` late in the reel, when the chart is highlighted
7. **Outputs:** copy the mp4, contact sheet, poster, cover, `script.txt`, `script.json`, `numbers.json` and `sheet.svg` to `assets/renders/reels/<date>-<slug>/`. Make 3-4 hub previews at 608x1080 (opening, mid-chart, stat, end card) in `assets/renders/hub/<week>/`
8. **Hub card:** a `slots` proposal like `reel-compounding-2026-10-30` (format `highlighter-reel`)

## Checklist (look at every still, every build)
- The highlight lands on the right label, and the label is still readable under it
- The hand keeps its size and shape, and never covers the label being highlighted
- Nothing sits under the captions; captions stay on one line (they shrink if longer than 1000 px)
- Text is readable at phone width (open a still at 360 px wide)
- Each highlight happens when the voice says that word (the build uses the real word times; WARN "actions too close" means two strokes are less than 0.22 s apart, which is fine if the still looks right)
- The first and last frames match (loop), and the hand is gone before the end card
- House rules: US dollars, no "!", no emoji, no full stop at the end of any caption or end-card line, no tutoring, general audience, numbers with stated assumptions

## Files (scripts/)
| File | What it does |
|---|---|
| `build.sh` / `build.py` | Validate, voice with word timings, caption and highlight times, audio mix, stills, contact sheet, poster, video, checks |
| `tts_align.py` | ElevenLabs v3 (voice gPiEpcKoaZywgOzc0Zn9, tempo 1.12 from the explainer engine's `eleven_tts.py`) with word timings; cached in `tools/tts/cache-eleven/*-ts.json`, so a rebuild is free. On 401/402/429 it stops; do not switch voices silently |
| `render.html` | Desk, sheet, highlight layer, hand, captions, end card, cover panel |
| `render.cjs` | Headless Chrome at 24 fps, frames piped to ffmpeg (same as the puzzle reel) |
| `make_cover.js` | Cover frame with the kicker and title panel inside the 3:4 crop |
| `edlintics-logo.png` | Logo, the same one the puzzle reel uses |

Uses the explainer engine's node_modules (puppeteer-core) and `tools/tts/.venv` (numpy, soundfile, imageio-ffmpeg, Pillow). No installs.
