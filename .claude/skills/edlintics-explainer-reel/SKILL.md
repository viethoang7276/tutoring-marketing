---
name: edlintics-explainer-reel
description: Make an Edlintics definition explainer reel (9:16, 30–40 s, short-form): a Ledger picture story drawn in a hand-drawn pencil style with draw-on and line boil, Kokoro voiceover, short captions, the Canva logo, and free Canva music. Covers script, scene layout, build commands, the Canva upload and the hub proposal. Written so a cheaper model can follow it. First used for "Sunk cost" (25 Oct 2026).
---

# Edlintics explainer reel

Output: a 1080x1920, 24 fps MP4 of 30–40 s and a Canva draft with Canva music, plus a `status: "proposal"` slot in the hub. Nothing is published until Hoang approves.
Reference build: the sunk-cost reel v4, hub slot `explainer-sunk-cost`, Canva `DAHZAC3sKDI`, script `scripts/script_example.json`.

## 1. Script (write this first; Hoang approves the words)
Short-form defaults (Hoang, 25 Oct 2026: "make it bigger and optimise for short form"):
- **Length 30–40 s**, about 100–115 words, voice at speed 1.08.
- **10–12 beats of 2–4 s.** A beat is one voice line on one framing. A cut or strong visual change every 2–3 s; split a long scene into 2 beats with a reframe.
- **Hook in the first 1–2 s:** open on the most striking image of the story (not an intro), with the hook question on screen from frame 1.
- **Loop:** the last beat reuses the hook image and framing and ends on a line that leads back into the hook question, so the replay feels continuous.

Structure:
1. **Hook:** a question the viewer has felt. Example: "Why do smart people keep paying for bad decisions?"
2. **Everyday story (3–4 beats):** Ledger in a concrete situation with US dollar amounts.
3. **Definition (1 beat):** the term in one plain sentence.
4. **Business example (3–4 beats):** the same idea in a company, with dollar amounts.
5. **Takeaway (1–2 beats)** and the loop line.

Write it the Feynman way: explain to a smart 15-year-old, no jargon without a plain meaning, and no formulas on screen.

Voice rules (house rules, all apply):
- Calm and expert, full sentences.
- No exclamation points and no emoji.
- US dollars only.
- General audience; no exam-only framing.
- Never mention tutoring.

Caption rules:
- **On-screen captions follow the voice in chunks of 2–5 words**, one chunk at a time, with one key word or amount per beat marked `key` (it gets a yellow highlighter). The chunks are the voice's own words, so together they form its full sentences.
- **No paragraph ends with a full stop** (Hoang, 25 Oct 2026). This covers on-screen captions, the post caption, caption_x and the first comment. Full stops between sentences inside a paragraph are fine; only the last one in each paragraph goes. Question marks stay.
- **First comment:** a reply prompt plus a bonus question. It **never reveals the answer**; store the maths in `maths_check`.

`<work>/script.json` (example: `scripts/script_example.json`):
`[{"img": "s1", "focus": [x, y, w, h], "focus_end"?: [x, y, w, h], "text": "voice line", "chunks": [{"text": "Ledger paid $60", "key"?: "$60"}, …]}, …]`
- `focus` is the part of the 1080x1920 scene art to frame, in art coordinates. The renderer fits it into the box x 40–1040, y 530–1310, so a box about 600–700 wide makes Ledger fill 60–70% of the frame. Frame the action, not the whole room.
- `focus_end` (optional): where the camera ends. Use it for a strong push-in from a wide establishing frame to the subject. Without it, the camera pushes in 7% with a small pan.
- Reusing the same `img` in the next beat gives a quick reframe instead of a cut.

## 2. Scenes (art)
Copy `scripts/scenes_example.py` into the work folder and edit the scene list. Its `ledger(x, y, scale, mood, tilt, arm)` helper draws the real mascot from `assets/brand/ledger.svg`:
- moods: smile, frown, sad, flat, o;
- arms: hold, up.

It writes `s1.svg … sN.svg` (1080x1920).

Art rules:
- No text inside the art (captions are separate layers).
- Brand colours from config/brand.ts: ink #0F172A, blue #467DE3, navy #222C3D, gold #C2922F.
- One clear action per scene. Ledger is always recognisable.
- Draw the ground line at y=1480. Any art scale works: each beat's `focus` box decides the framing. To pick boxes, render the scene PNGs on a 100 px grid and read the coordinates.

## 3. Layout and safe zones (1080x1920)
- **Clear areas:** Reels, Shorts and TikTok cover the bottom ~670 px (name, caption, audio) and the right ~120 px (buttons). Keep everything that matters between y 262 and y 1360, and x 70 to 960.
- **Caption:** a 236 px band from y 262. Inter 900 at 92 px, 2 lines at most, ink #0F172A, with a yellow highlighter on the key word. Each chunk pops in (scale 0.88 to 1 in 0.16 s).
- **Art:** each beat's focus box fills x 40–1040, y 530–1310. Art fades out above y ~490, so it never runs under the caption.
- **Logo:** the Canva template logo, `scripts/logo/edlintics-logo.png`, 210 px wide at y 1338, opacity 0.72, small and quiet. It's the same logo as on the post templates (DAHYuGZYL_E). To refresh it, export page 1 of that template as a transparent PNG at 3240 px wide and crop the bottom logo.

## 4. Hand-drawn style (what the renderer does, and why)
The reference (evanbode, "TIME FLIES") gets its feel from:
- graphite strokes drawn several times, loose and slightly off each other;
- frame-by-frame line boil at about 12 drawings a second;
- strokes that appear as if drawn;
- visible paper grain;
- a mostly locked camera.

`scripts/render.html` imitates that in the browser:
- **Line boil:** an SVG displacement filter whose noise seed changes every 2 frames (12 fps boil), cycling through 3 seeds.
- **Pencil grain:** a high-frequency noise mask that knocks small gaps out of strokes and fills.
- **Ghost pass:** a second copy of the art at 30% opacity, offset 2.5 px with its own wobble, so lines look drawn twice.
- **Draw-on:** on every new scene, each shape's stroke draws in order through `stroke-dashoffset`; the whole scene is drawn in about 0.5 s, so it never delays information. Fills fade in behind the lines. Beat 1 opens fully drawn, so the hook frame reads at once.
- **Paper:** an off-white base with fibre and grain noise.
- **Camera:** each beat frames its `focus` box and pushes in (7% with a small pan, or to `focus_end`). A new scene cuts in with a quick pop (scale 0.9 to 1 with overshoot, 0.32 s). The same scene in the next beat reframes in 0.35 s.
- **Captions:** 2–5 word chunks at the times vo.py estimates. The key word gets a highlighter sweep.
- **Sound:** mix_audio.py adds a soft generated whoosh on each new scene and a light tick on each reframe, about 20 dB under the voice. No licensed audio.

Considered but not used:
- **rough.js and perfect-freehand:** they would mean redrawing the Ledger art as generated strokes, losing the exact mascot shape.
- **Remotion's official agent skills** (`npx skills add remotion-dev/skills`): a heavier React toolchain with no gain for still-based scenes.
- **The whiteboard-animation skill** (yangagent): it turns photos into whiteboard sketches, which isn't our look.

## 5. Build
Tools (no system installs):
- Kokoro and imageio-ffmpeg in `tools/tts/.venv`;
- Node with puppeteer-core in `scripts/`, which uses the installed Google Chrome.
```
cd tools/tts && .venv/bin/python ../../.claude/skills/edlintics-explainer-reel/scripts/vo.py <work> 1.08 0.2   # speed, gap between lines -> voiceover.wav + timing.json (beat and chunk times)
tools/tts/.venv/bin/python .claude/skills/edlintics-explainer-reel/scripts/mix_audio.py <work>        # audio-voice.wav + audio.wav
python3 <work>/scenes.py                                                                             # s1..sN.svg
python3 .claude/skills/edlintics-explainer-reel/scripts/make_scenes_json.py <work> .claude/skills/edlintics-explainer-reel/scripts
cd .claude/skills/edlintics-explainer-reel/scripts && node render.js stills 2,10,25                 # check stills in out/
./build.sh <work> <slug>     # <slug>.mp4 (voice + pad), <slug>-voice-only.mp4, <slug>-canva-upload.mp4 (<10 MB)
```
Rendering takes about 1 minute for 40 s. If you change a `focus` box after vo.py, copy it into timing.json too (or rerun vo.py).

Check before moving on:
- the stills show the subject at 60–70% of the frame width and no art behind the caption;
- the first frame already shows the hook image and question, and the last frame matches it (loop);
- the logo is clear in every scene;
- the duration matches timing.json;
- the video stream is `yuv420p(tv)`.

## 6. Canva (music and the draft)
The Canva connector rejects video uploads, so use the editor in Chrome:
1. Copy the last reel design with `copy-design` (for example DAHY_xGsGFc) so the music track comes with it. Then open it in a new tab.
2. Uploads › `find` the file input › `file_upload` `<slug>-canva-upload.mp4`. The bridge limit is 10 MB.
3. Uploads › Videos › drag the new video onto the page. Then the element's ⋯ menu › **Replace background**.
4. Music: keep the free track "Light Minimal Ambient" (makesoundmusic, volume 15), or pick another free Canva track. Never use a paid (crown) track.
5. Rename it with File › title: "Explainer reel - <Term> (Ledger) vN".
6. `move-item-to-folder` to FAHYcHrS5PE. Close your tab.

## 7. Hub proposal
Create or update the slot (ArtifactData `slots`, artifact HbKxzWUcWhaBaaNb9buZM6, pin writes with `if_version`):
- **Basics:** `format: "explainer-reel"`, `status: "proposal"`, `kind: "video"`, `test: "H12"`.
- **Copy:** `caption`, `caption_x`, `first_comment`, `hashtags`, `maths_check`.
- **Threads:** `threadsTopic` and `threadsReason`.
- **Links:** `utm.template` = `https://edlintics.com/?utm_source=<platform>&utm_medium=social-post&utm_campaign=explainer-reel&utm_content=<slot id>`.
- **Media and script:** `canva`, `video`, `music`, `script` (captions with start times).
- **Status note:** a `statusNote` saying what is new.

Leave the date empty for Hoang. Show Hoang the MP4 and a contact sheet.
