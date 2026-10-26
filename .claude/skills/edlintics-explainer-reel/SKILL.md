---
name: edlintics-explainer-reel
description: Shared engine for Edlintics explainer reels (9:16, 30-40 s, hand-drawn Ledger picture stories with Kokoro voice, chunked captions, an end card and Canva music). Holds the scene library, validator, renderer and the one build command used by the edlintics-definition-reel and edlintics-life-of-reel skills. To make a reel, use one of those two skills; read this file only to change the engine.
---

# Edlintics explainer reel engine

To make a reel, use one of these skills:
- **edlintics-definition-reel:** hook, everyday story, definition, business example, takeaway, end card.
- **edlintics-life-of-reel:** "A day in the life of a [role]", relatable moments, the turning moment, the concept, the lesson, end card.
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
5. **House rules:** US dollars, no exclamation points, no emoji, no tutoring, general audience. The first comment never reveals the answer.
6. **Length** is 30-40 s, about 100-115 words, with 9-13 beats of 2-4 s. The voice is Kokoro `af_heart` at speed 1.08.

## Files (scripts/)
| File | What it does |
|---|---|
| `make_reel.sh` | The one command: validate, scenes, voice, audio mix, scene data, stills, video, then the checks and contact sheet |
| `validate.py` | Checks script.json against the rules above and the beat structure for `meta.type` |
| `scene_lib.py` | The scene library: Ledger (`mood`, `arm`, `outfit`, `flip`, `tilt`), about 35 props and 6 backgrounds. Run `python scene_lib.py --list` |
| `build_scenes.py` | Turns scene presets into `s*.svg` and resolves each scene's optional `frame` (default `auto`) into `beats.json` |
| `vo.py` | Makes the Kokoro voiceover (`voiceover.wav`) and `timing.json` with beat and chunk times |
| `mix_audio.py` | Makes `audio-voice.wav` (voice plus soft generated whoosh and tick) and `audio.wav` (adds a quiet pad for preview) |
| `make_scenes_json.py` | Packs the art, beats and end card into `<work>/scenes.json` |
| `render.html`, `render.js`, `build.sh` | The headless Chrome renderer at 24 fps, plus the H.264 encode, the voice-only cut and the Canva upload copy under 10 MB |
| `postcheck.py` | Checks resolution, audio, length and the 10 MB limit, and makes `<slug>-contact-sheet.png` |
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

## Changing the engine
- **New prop:** add a function to `scene_lib.py`, register it in `PRESETS` (and `HALF` for its size), give it a one-line docstring, and test with the two examples.
- After any engine change, rebuild both examples and look at the contact sheets.

## Contact-sheet review checklist (every reel, every build)
- Ledger is accurate to assets/brand/ledger.svg and fills at least 70% of the art-box height in every scene
- **Hands proportional:** Ledger's hands and arms match the brand proportions (hand about the size of his eye-to-eye gap, arms no longer than his body is tall), and anything he holds is in scale with his hand (Hoang, 25 Oct 2026: check this every time)
- No text inside the art, and nothing sits under the caption band
- The end card shows the term and the key point

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
