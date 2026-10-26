# REQ-0004  ·  Video engine software: a standalone, AI-drivable engine for chat-story and explainer videos

- **Status:** relayed (Hoang asked the CMO to relay it to the tutoring-web CTO session on 27 Oct 2026)
- **Date:** 2026-10-27
- **Source:** research (`reports/Chat videos and AI labels.md`) and Hoang's request
- **Targets metric:** acquisition (reach, watch time and saves per reel without AI labels)
- **Priority (CMO view):** high
- **Effort guess (CMO, non-binding):** M (MVP with one template about 1-2 days, then about half a day per template)

## Summary
Edlintics needs voice-free chat-story reels (fictional characters chatting in a work chat, phone messenger, AI assistant or email screen) to teach business concepts. These reels need no AI label. No ready-made tool fits: every one copies iMessage or WhatsApp, several add AI voices, and none takes a script file from an agent. Today the reel engine lives inside a marketing skill folder (`edlintics-marketing/.claude/skills/edlintics-explainer-reel/scripts`). Hoang wants a proper software project for it: `tutoring/video-engine-software/`, with the same engineering setup as tutoring-web (session start, coding rules, status file, harness)

## Evidence (lead with this)
- **The labels come from Canva AI clips, not the voice.** Canva exports that contain AI-generated clips carry a signed C2PA manifest ("Canva AI", `compositeWithTrainedAlgorithmicMedia`), and platforms auto-label from it. Code-rendered video carries no manifest (local scan, 27 Oct 2026, in the report)
- **The model reel is** @orbi_the_alien "Corporate Life in 2026 · part 2": a voice-free, Slack-style work chat with a mascot as one user, a fixed title band, a cursor, file cards and an AI-assistant screen. About 369 comments and 1,265 reposts
- **Legal and platform limits:** fictional skits are fine. The engine must not reproduce real apps' trade dress (names, logos, signature colours, icons), because of WhatsApp's brand rules and Apple's rules against mimicking its interface. Avatars must be illustrated, not photorealistic AI faces (EU AI Act Art. 50, applies from Aug 2026)
- **Build vs buy:** subscriptions cost $72-240 a year with no branding or automation. The existing frame-by-frame renderer (`window.render(t)`, Puppeteer screenshots, ffmpeg) already avoids frame-timing bugs

## Hypothesis
We believe that **a template-driven chat-story engine that an agent can run from a script file** will let marketing ship 2-3 voice-free reels a week for **business students and young professionals**. Reach and saves per reel should then match or beat the explainer reels with no AI label, because the format is native, relatable office satire and carries no AI provenance

## Job to be done
"When I have a business concept and a joke, I want to write the conversation once as a script and get a finished 9:16 reel with music, sound and an end card, so that I can post daily without AI labels or manual editing"

## Proposed requirements (CTO owns the final design)

**Project setup (replicate tutoring-web's discipline)**
- A new repo or folder `tutoring/video-engine-software/` with its own `CLAUDE.md` and `AGENTS.md`, `docs/session-start.md`, `docs/STATUS.md`, coding rules, a `docs/specs/` pipeline, lint, typecheck and tests, and a dev harness on the same pattern as tutoring-web
- Add it to the root `AGENTS.md` divisions table and to `BOARD.md`
- Marketing consumes it as a tool (CLI or package). It never imports tutoring-web app code

**Rendering core**
- Deterministic, time-driven rendering: every frame is a pure function of `t`, with no CSS transitions or requestAnimationFrame. Frames are captured headless and encoded with ffmpeg. Output is 1080x1920 at 30 fps H.264, plus a cover PNG
- Port the existing explainer-reel engine into the new project (scenes, captions, end card, cover) so there is one engine, not two

**Chat-story templates (themes)**
Each template copies a layout convention, never a brand. There are no real app names, logos, signature colours or icons, and no iOS status bar
- `work-chat`: sidebar with #channels, threaded messages, names with roles, timestamps, reactions (Slack or Teams layout)
- `messenger`: phone bubbles left and right, read ticks, typing dots (WhatsApp or iMessage layout)
- `assistant`: a prompt box and an answer streaming in (ChatGPT layout)
- `email`: an inbox and a reply thread
- Each theme ships with Edlintics colours by default. A light and a dark variant are optional

**Screen inserts and overlays**
- A file card (pptx, xlsx, pdf), a spreadsheet snippet, an invoice, a small chart, a notification banner and a sticker or reaction burst
- A moving mouse cursor with clicks, scroll and a zoom-to-message camera move
- A fixed title band ("part N · <series>") and an end card (term and key point)
- Safe areas: keep text inside about x 120-840 and y 240-1500 of 1080x1920, and clear the bottom 320 px for the Reels and TikTok UI

**Background sound (required)**
- A music bed from a licensed library folder (Canva-licensed tracks exported by Hoang, or royalty-free tracks with the licence recorded). The default level is very quiet, matching marketing's "volume 8" rule (about -30 to -26 LUFS under the sound effects), with a fade in and out
- Sound effects: our own generated sounds for message pop, send, typing, notification and click, timed to events from the script. Never copies of Apple or WhatsApp system sounds
- Optional voiceover track, human recording or TTS, with ducking under the voice. If TTS is used, the manifest marks the video `ai_voice: true` so the uploader knows to switch on the Meta "AI info" label
- Final loudness normalised to about -14 LUFS integrated, true peak no higher than -1 dBTP

**AI accessibility (agent-drivable, required)**
- Input is one JSON (or YAML) episode file validated against a published JSON Schema: cast, theme, messages with sender, text, delay and reactions, inserts, music and end card
- A CLI that takes the episode file and returns the mp4, cover, srt and manifest, with machine-readable errors and non-zero exit codes. A `validate` command checks the script without rendering, and a `preview` command renders a still at time t
- A manifest JSON per render: inputs hash, duration, assets and licences used, `ai_generated: false` unless a TTS or AI asset was used
- No C2PA "AI" manifest is ever written. A post-render check scans the output and fails if any AI provenance is found
- An optional MCP server or Claude skill wrapper, so Claude sessions (marketing) can list themes, validate and render

**Viewer accessibility**
- Burned-in text sized for phones (at least 36 px at 1080 width) with high contrast (WCAG AA). Reading pace no faster than about 17 characters per second
- A sidecar `.srt` and alt text in the manifest
- Respect the "no full stop at the end of a paragraph" house rule in the defaults

**Hand-off**
- Drop the outputs where marketing's Canva and upload flow picks them up. Optional: upload to Canva through the existing connector

## Success signal
- Marketing can produce a 30-40 s chat reel from a script file in under 10 minutes of agent time
- The rendered files carry no AI manifest
- The first 4-6 episodes reach at least the explainer-reel median views and saves within 4 weeks

## Out-of-scope check
- No fake accounts or automated posting from fictional users. Characters exist only inside videos
- No real customer names or quotes, and no outcome claims by fictional students
- No imitation of a specific real app's trade dress
- Posting stays manual or through the existing Chrome upload skills, with Hoang's approval

## Decision log
- 2026-10-27: Hoang asked for a standalone `video-engine-software` project under `tutoring/`, built by the tutoring-web CTO session using its development discipline, with templates like Slack and WhatsApp, screen inserts, background sound and AI accessibility. The CMO relayed this request; trade-dress limits were explained to Hoang
