---
name: edlintics-explainer-reel
description: Make an Edlintics definition explainer reel (9:16, 40–50 s): a Ledger picture story drawn in a hand-drawn pencil style with draw-on and line boil, Kokoro voiceover, short captions, the Canva logo, and free Canva music. Covers script, scene layout, build commands, the Canva upload and the hub proposal. Written so a cheaper model can follow it. First used for "Sunk cost" (25 Oct 2026).
---

# Edlintics explainer reel

Output: a 1080x1920, 24 fps MP4 of 40–50 s and a Canva draft with Canva music, plus a `status: "proposal"` slot in the hub. Nothing is published until Hoang approves.
Reference build: the sunk-cost reel, hub slot `explainer-sunk-cost`, Canva `DAHY_xGsGFc`.

## 1. Script (write this first; Hoang approves the words)
Structure, one idea per scene, 8–10 scenes of 3–6 s, 85–120 words in total:
1. **Hook (0–3 s):** a question the viewer has felt. Example: "Why do smart people keep paying for bad decisions?"
2. **Everyday story (2–3 scenes):** Ledger in a concrete situation with US dollar amounts.
3. **Definition (1 scene):** the term in one plain sentence. Example: "That is a sunk cost: money already spent that no decision can recover."
4. **Business example (2–3 scenes):** the same idea in a company, with dollar amounts.
5. **Takeaway (1 scene):** the decision rule.

Write it the Feynman way: explain to a smart 15-year-old, no jargon without a plain meaning, and no formulas on screen.

Voice rules (house rules, all apply):
- Calm and expert, full sentences.
- No exclamation points and no emoji.
- US dollars only.
- General audience; no exam-only framing.
- Never mention tutoring.

Caption rules:
- **On-screen captions:** one per scene, 3–7 words, and a short full sentence ("It is pouring with rain", not "Pouring rain, feeling unwell"). The caption says the scene's point, not a transcript of the voice.
- **No paragraph ends with a full stop** (Hoang, 25 Oct 2026). This covers on-screen captions, the post caption, caption_x and the first comment. Full stops between sentences inside a paragraph are fine; only the last one in each paragraph goes. Question marks stay.
- **First comment:** a reply prompt plus a bonus question. It **never reveals the answer**; store the maths in `maths_check`.

Files in a work folder `<scratch>/reel/<slug>/`:
- `script.json` = `[{"text": voice line(s), "cap": caption, "img": "s1"}, …]`;
- optionally `hook.json` = `{"cap": "...", "until": <sec>}`, to show a hook caption before scene 1's caption.

## 2. Scenes (art)
Copy `scripts/scenes_example.py` into the work folder and edit the scene list. Its `ledger(x, y, scale, mood, tilt, arm)` helper draws the real mascot from `assets/brand/ledger.svg`:
- moods: smile, frown, sad, flat, o;
- arms: hold, up.

It writes `s1.svg … sN.svg` (1080x1920).

Art rules:
- No text inside the art (captions are separate layers).
- Brand colours from config/brand.ts: ink #0F172A, blue #467DE3, navy #222C3D, gold #C2922F.
- One clear action per scene. Ledger is always recognisable.
- Draw the ground line at y=1480. The renderer scales the art by 0.8 and moves that line to y=1215. If a scene reaches far below the ground (a pit, for example), add `"dy": -230` to that scene in timing.json so it clears the logo.

## 3. Layout and safe zones (1080x1920)
- **Clear areas:** Reels, Shorts and TikTok cover the bottom ~670 px (name, caption, audio) and the right ~120 px (buttons). Keep everything that matters between y 262 and y 1360, and x 70 to 960.
- **Caption:** top 262 px, Inter 800 at 74 px, ink, balanced line breaks, with a yellow highlighter sweep behind it.
- **Art:** about y 470–1215.
- **Logo:** the Canva template logo, `scripts/logo/edlintics-logo.png`, 300 px wide, centred at y≈1300. It's the same logo as on the post templates (DAHYuGZYL_E). To refresh it, export page 1 of that template as a transparent PNG at 3240 px wide and crop the bottom logo.

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
- **Draw-on:** each shape's stroke draws in order through `stroke-dashoffset` over the first ~1.2 s of the scene. Its fill fades in behind the line, and dashed shapes fade in.
- **Paper:** an off-white base with fibre and grain noise.
- **Camera:** a slow 4.5% push-in per scene, with a 0.18 s fade between scenes.
- **Captions:** a highlighter sweep for the caption, and a hook caption first if hook.json exists.

Considered but not used:
- **rough.js and perfect-freehand:** they would mean redrawing the Ledger art as generated strokes, losing the exact mascot shape.
- **Remotion's official agent skills** (`npx skills add remotion-dev/skills`): a heavier React toolchain with no gain for still-based scenes.
- **The whiteboard-animation skill** (yangagent): it turns photos into whiteboard sketches, which isn't our look.

## 5. Build
Tools (no system installs):
- Kokoro and imageio-ffmpeg in `tools/tts/.venv`;
- Node with puppeteer-core in `scripts/`, which uses the installed Google Chrome.
```
cd tools/tts && .venv/bin/python ../../.claude/skills/edlintics-explainer-reel/scripts/vo.py <work>   # voiceover.wav + timing.json
# add "cap" (and "dy" if needed) per scene in <work>/timing.json if not already in script.json
tools/tts/.venv/bin/python .claude/skills/edlintics-explainer-reel/scripts/mix_audio.py <work>        # audio-voice.wav + audio.wav
python3 <work>/scenes.py                                                                             # s1..sN.svg
python3 .claude/skills/edlintics-explainer-reel/scripts/make_scenes_json.py <work> .claude/skills/edlintics-explainer-reel/scripts
cd .claude/skills/edlintics-explainer-reel/scripts && node render.js stills 2,10,25                 # check stills in out/
./build.sh <work> <slug>     # <slug>.mp4 (voice + pad), <slug>-voice-only.mp4, <slug>-canva-upload.mp4 (<10 MB)
```
Rendering takes about 1 minute for 46 s.

Check before moving on:
- the stills show no caption overlapping the art;
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
