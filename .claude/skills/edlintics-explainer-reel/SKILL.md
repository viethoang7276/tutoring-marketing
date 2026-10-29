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
