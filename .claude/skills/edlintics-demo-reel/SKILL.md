---
name: edlintics-demo-reel
description: Make one Edlintics "platform demo" reel (9:16, 25-45 s, voice only) from a real, scripted screen recording of a PUBLIC edlintics.com page, where a finger does one interactive card while the ElevenLabs voice explains the concept. Covers the spec, voice, headless recording with a tap indicator, take picking, the composition (phone frame, title, bottom-half captions, push-in zoom, Ledger end card), the checks and the hub card. Pilot: journal-entry glossary card, 18 Nov 2026.
---

# Edlintics demo reel

Hoang, 18 Nov 2026: "focus on demo with screen recording and interaction, showing how easy learning business concepts on our platform is"

The pilot's output and notes are in `assets/renders/demo-reels/pilot-journal-entry/NOTES.md`. That file lists what is demo-able and the full script.

## Hard rules
- **Public pages only, signed out.**
  - Never sign in, create accounts, type personal data or submit forms.
  - Tapping a card's own answer button is fine.
  - `record_demo.cjs` logs every non-GET request and every main-frame navigation, and exits with code 2 if one happens. If that happens, stop and check.
  - The cookie banner is hidden with CSS. Never click it.
- **Marketing never imports app code.** Playwright, from the tutoring-web install, is only the browser driver.
- **Only real interactions.**
  - The homepage hero and story cards are mock-ups (`pointer-events: none`). Never fake a tap on them.
  - Demo-able now: glossary "Check yourself" cards, calculators, chart of accounts, markets/bonds.
- **No price, sale date or "course open" claims.**
  - Do not film course pages: they show "Add to cart".
  - Never mention tutoring.
  - CTA: "Try it free on edlintics.com"; on Instagram, "link in bio".
- **Copy and captions.**
  - Full sentences, no exclamation marks.
  - No trailing full stop on screen text or caption paragraphs.
  - Textbook-correct: run the definition-reviewer agent on every line.
- **Video.**
  - Captions sit in the bottom-half centre (y 1320-1530) and never cover the UI.
  - Nothing may be cut by the frame. The push-in zoom ends at the sticky header's bottom edge (`zoom_top_css`), so the header never shows half-cut.
- **Output is voice only.** Music is added in Edits; the reel goes up as an Instagram trial reel.
- Renders stay in `assets/renders/` (gitignored), and Ledger v2 art stays in `assets/brand-handoff/` (gitignored).

## Steps (repo root, `S=.claude/skills/edlintics-demo-reel`, `W=assets/renders/demo-reels/<slug>/work`)
1. **Find the card.**
   - Probe the page at a 410-430 px mobile viewport. Check that the card has real `<button>`/`<input>` elements and `pointer-events` is not `none`.
   - Tap it once in a throwaway run and watch the network (only GETs allowed).
2. **Write the spec.** Copy `examples/pilot-journal-entry.json`. Fields:
   - `url`
   - `viewport`: `[410, 500]` fits a question plus 3 options under the header. The screen shows 2.0 px per CSS px.
   - `title`: direct, true to the reel's length or to "one tap".
   - `lines[]`: `say` (spoken, numbers in words), `caption` (on screen, numerals, no final stop), `actions`.
   - `zoom`: a tagged target `id`.
   - `end: true` on the CTA line.
3. **Actions.** `t` is seconds from the line start, or `"end-0.2"` from its end.
   - `finger`: the dot glides to the target and stays.
   - `swipeTo`: a scroll with a visible dragging finger.
   - `scrollTo`: an eased scroll with no finger.
   - `tap`: glide, then ripple, then a real touch tap. `id` tags the element for the zoom.
   - Targets are `{text: "starts with"}` or `{buttonText: "contains"}`.
   - `top` is where the target lands, in CSS px from the viewport top. The header is about 77.
   - `fx`/`fy` set where on the target the finger rests. Keep key words uncovered, e.g. 0.75/0.8 = the blank corner of an option.
4. **Voice:** `tools/tts/.venv/bin/python $S/scripts/demo_voice.py SPEC $W`
   - Default voice is ElevenLabs `vChnJZ1Cu89g2XXumPfT`, tempo 1.0, tag `[calm]`.
   - Clips are cached, so re-runs are free.
5. **Record 2-3 takes:** `node $S/scripts/record_demo.cjs SPEC $W/timings.json $W/take-1`
   - Runs headless; Hoang's screen is not used.
   - The `--force-device-scale-factor` launch flag is what makes the frames crisp: without it, screencast frames come out at CSS px.
6. **Pick and compose.**
   - `tools/tts/.venv/bin/python $S/scripts/compose_demo.py --pick $W/take-*`: lowest motion gap wins, and it must show 0 non-GET and 0 navs.
   - `tools/tts/.venv/bin/python $S/scripts/compose_demo.py SPEC $W $W/take-N OUT.mp4 --thumb thumbnail.jpg`
   - The compose needs the take's `frames/`. Delete them only when the reel is final, and keep `raw-take-N-screen.mp4`.
7. **Check.**
   - `tools/tts/.venv/bin/python $S/scripts/tiles.py OUT.mp4 DIR --at <tap time>,<zoom time>,...`
   - Look at `tile-1fps.jpg` and `contact-sheet.jpg`:
     - UI text readable;
     - nothing cut;
     - captions at most 2 lines and off the UI;
     - finger and ripple visible;
     - the end card does not overlap.
   - Also look at the take's frames around the tap: the ripple lasts 0.85 s, so the 1-fps tile can miss it.
8. **Deliver.**
   - Copy the master to `~/Movies/Edits/Imports/<slug>-voice-only.mp4`.
   - Upload the video, poster and thumbnail to the hub (Artifact publish, `asset: true`).
   - If the 1 GB hub store is full, upload a 720p preview and say so. Never delete hub assets without Hoang's OK.
   - Write the slot as `status: "proposal"`, `format: "demo-reel"`, `igTrial: true`.
   - Do not post.

## Files
- `scripts/demo_voice.py`: voice clips laid end to end, plus timings.json.
- `scripts/record_demo.cjs`: the scripted headless recording, with the finger dot, ripple, eased scroll, network guard and frames.json/events.json.
- `scripts/compose_demo.py`: the 1080x1920 composition, take picker and thumbnail.
- `scripts/tiles.py`: the 1-fps tile and the contact sheet.
- `examples/pilot-journal-entry.json`: the pilot spec.
