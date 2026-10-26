# Chat and text-message story videos: ready-made tools vs a custom pipeline

Research date: 27 Oct 2026. About 17 web calls. Where a primary page could not be fetched (Pixabay licence page returned HTTP 429, Mixkit licence text not rendered), this is marked. Context checked locally: the existing Edlintics reel engine at `.claude/skills/edlintics-explainer-reel/scripts/render.js` is a 50-line Puppeteer-core 23.11 script. It loads `render.html` at 1080x1920, calls `window.render(t)` for each frame at `k / FPS`, screenshots JPEG q92 and pipes the frames to ffmpeg with libx264, CRF 20 and AAC audio. In other words, it already uses a deterministic seek-per-frame model, not real-time capture.

## Ready-made tools (2025-2026): pricing, quality, customisation, watermarks, TTS/AI, licence, iMessage imitation

### Takeaway
Dedicated chat-story generators are cheap: $0-$20 a month for the basic ones, and $29-$99 a month for the AI "brainrot" suites. They are built around imitating iMessage, WhatsApp and Instagram DM skins, often with AI voices bundled in. None found offers a custom, brand-owned chat UI, and none publishes clear commercial-use terms on its pricing or comparison pages. Open-source options are tiny, unmaintained demos, and no Remotion-based chat-story template of note exists.

### Cited Findings
**Web apps**
- **texting.video:** The Free Maker is $0 with "all 13 themes", unlimited MP4/WebM export and a small watermark ("made with texting.video" pill below the chat header). A 24-hour pass is $4.99 once and removes the watermark for 24 h. Creator Pro is $9/month, with annual billing described as "2 months free". Free exports have the same resolution as Pro, so the watermark is the only difference. The pricing page lists themes and member photos but says nothing about AI voices or commercial-use terms. — [texting.video pricing](https://texting.video/pricing)
- **GhostShorts:** Starter is $19.99/mo ($16.66/mo annual), Creator+ $39.99/mo and GhostMode $79.99/mo, plus a $9.99 one-time credit pack. The free tier is only a silent browser preview with no download, and paid exports have no watermark. It includes AI voices (one per side). Skins are iMessage, WhatsApp, Instagram and Tinder, in light or dark. Output is 1080x1920 MP4 at 30 fps. The comparison is published by GhostShorts itself (vendor bias, disclosed), with prices checked 2026-09-27. — [GhostShorts comparison](https://ghostshorts.com/best-texting-story-makers)
- **Chatimator:** Pro is $5.99/mo. The free tier allows one 720p watermarked export a month, and Pro exports 1080p60. Skins are iMessage, WhatsApp and Instagram DM, in dark or light. No voices are mentioned. — [GhostShorts comparison](https://ghostshorts.com/best-texting-story-makers) (secondary, vendor-written)
- **ConvoClip:** $15/mo or a $15 one-time credit pack. Watermark, voices and skins are not stated. — [GhostShorts comparison](https://ghostshorts.com/best-texting-story-makers)
- **Brainrot Shorts:** Lite $29/mo, Creator $49/mo, Pro $99/mo, with 240 free credits and "40+ character voices". Uploading your own background is paid-only. — [GhostShorts comparison](https://ghostshorts.com/best-texting-story-makers)
- The comparison states: "We did not test output quality and nothing here is a ranking." No tool listing in it mentions avatars or custom branding beyond preset skins, and none states commercial-use terms. — [GhostShorts comparison](https://ghostshorts.com/best-texting-story-makers)
- **Crayo AI:** Described as a texting-video maker with typing animations, sound effects and export presets for TikTok, Instagram and YouTube Shorts, mimicking WhatsApp, iMessage or Instagram DM interfaces. The source is a CapCut marketing article. — [CapCut: texting video makers](https://www.capcut.com/resource/texting-video-maker)
- **FakeMessenger:** Listed as a free browser tool for fake chat conversation videos (August 2026). No pricing or licence detail was found. — [PeerPush listing](https://peerpush.com/p/fakemessenger)
- **AlternativeTo listing for texting.video:** Shows "from $9 per month + free version", which is consistent with the primary pricing page. — [AlternativeTo](https://alternativeto.net/software/texting-video/about/)

**Mobile apps**
- **TextingStory:** A free phone app with "unlimited video creations". Free output is watermarked, and removal is an in-app purchase (per third-party sources). It exports video or GIF, square or vertical. Prices are not published. — [GhostShorts comparison](https://ghostshorts.com/best-texting-story-makers)

**Editor templates**
- **CapCut:** A free editor with no chat generator, so you build the chat by hand. Pro is $19.99/mo (US web price from a 2026-09-23 article, not a pricing page). Free exports are reported by third parties to carry a watermark, which CapCut has not confirmed. — [GhostShorts comparison](https://ghostshorts.com/best-texting-story-makers)
- CapCut and Pippit host "fake iMessage screen" and "iMessage text template animation" templates, and Premiere Pro text-message templates with customisable fonts, colours and animations. — [Pippit fake iMessage screen](https://pippit.capcut.com/templates/fake-imessage-screen); [Pippit iMessage animation](https://pippit.capcut.com/templates/imessage-text-template-animation); [CapCut Premiere templates](https://www.capcut.com/explore/text-message-template-premiere-pro)
- **Kapwing:** Has a text-story video template (edit the text in each bubble to re-create an iMessage conversation). It also has a tutorial that builds a dark-mode iMessage look by hand: black background, gray top bar, contact photo and name, timed pauses. — [Kapwing template](https://www.kapwing.com/explore/text-story-video-template); [Kapwing tutorial](https://www.kapwing.com/resources/how-to-make-a-fake-texting-story-video/)
- **Canva:** No Canva template page specifically for animated chat or iMessage video was found in search. Canva hits were only spam or off-topic. — (search returned nothing reliable; see Gaps)

**Open source (GitHub)**
- **samkwak188/Fake-Text-Video-Generator-Demo:** Python/Flask with Selenium + Chrome, FFmpeg and the ElevenLabs API (key required). It makes iMessage-style conversations with TTS voices (Adam, Natalie, Brian, Laura), sound effects ("Vine boom, notification, rizz") with no stated source or licence, background videos hosted on Google Drive with no licence stated, and custom profile images and names. The repo has 0 stars, 1 fork and 15 commits, and no licence is stated. The author notes free-tier hosts lacked the memory to render. — [GitHub repo](https://github.com/samkwak188/Fake-Text-Video-Generator-Demo)
- **AmirPhenomenal/fake-chat:** A React fake-chat generator with WhatsApp styling and video export. Stars, licence and recency were not checked. — [GitHub repo](https://github.com/AmirPhenomenal/fake-chat)
- GitHub topic pages "fake-chat" and "fake-message-generator" list more small projects, mostly screenshot generators. — [fake-chat topic](https://github.com/topics/fake-chat); [fake-message-generator topic](https://github.com/topics/fake-message-generator)
- **Remotion's official "prompt-to-video" template:** Creates short vertical videos from a story title using OpenAI (script, images) and ElevenLabs (voiceover). It has no chat-bubble layout. A search for a Remotion chat or text-story generator found no dedicated project. — [remotion-dev/template-prompt-to-video](https://github.com/remotion-dev/template-prompt-to-video)

### Inferences
- Every off-the-shelf tool is built around platform skins (iMessage, WhatsApp, IG, Tinder). That works against a brand that wants its own UI and risks Apple trade-dress or "fake screenshot" associations. Custom Edlintics branding (fonts, blue, Ledger avatar) is not offered by any tool found.
- Tools that bundle AI voices (GhostShorts, Brainrot Shorts, Crayo, the samkwak188 demo with ElevenLabs) put synthetic voice into the output. That can push a post into platform AI-disclosure territory, which is covered by the AI-labels research lane. Silent tools with music only (texting.video, Chatimator) avoid this.
- The cheapest watermark-free path is texting.video at $9/mo, or $4.99 per 24 h for a batch day. It is still locked to its 13 themes, and its commercial terms are unverified.
- The open-source projects are not usable foundations: no licence (which legally means all rights reserved), no maintenance, and unlicensed sound and background assets.

### Gaps
- No tool's Terms of Service was read directly for commercial-use or output-ownership clauses. The pricing pages and the comparison do not state them. Read the ToS before paying.
- Chatimator, ConvoClip, Brainrot Shorts and TextingStory prices come from a competitor's comparison page, not their own pricing pages.
- No Canva-native animated chat template was found. Canva's template library could not be searched directly.
- Output quality was not tested by any source found.
- Star counts, licence and last commit for AmirPhenomenal/fake-chat were not verified.

## Building our own: best technical approach, effort and pitfalls

### Takeaway
The best fit is to extend the existing Puppeteer + ffmpeg engine with a chat "scene" in HTML/CSS/JS, driven by the same `window.render(t)` seek function. It already sidesteps the main frame-timing pitfall and needs no new licence. Remotion would need a paid Company License once Edlintics passes 3 employees, and Motion Canvas would need a second toolchain. Neither adds anything the current engine lacks for a 2D chat UI.

### Cited Findings
**Remotion licensing**
- The Free License covers individuals, non-profits, people evaluating it, and "a for-profit organization with up to 3 employees". It allows commercial video creation. Anyone else must buy a Company License. The licence "will change slightly in Remotion 5.0". — [Remotion LICENSE.md](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md)
- Company License pricing:
  - "Remotion for Automators" is $0.01 per render with a $100/month minimum, and automation developers don't need a seat.
  - "Remotion for Creators" is $25/month per seat.
  - Enterprise starts at $500/month.

  — [remotion.pro/license](https://www.remotion.pro/license)
- Remotion ships a "social safe zones" overlay element. Its TikTok path clears the search bar to about y=132, the action rail from about x=949/y=803, and captions from about y=1749. — [Remotion social safe zones](https://www.remotion.dev/elements/overlays/social-safe-zones/)

**Motion Canvas**
- Motion Canvas is MIT-licensed, with about 18.2k stars (AlternativeTo snapshot). Rendering is driven from its editor UI. FFmpeg export is a separate MIT package (`@motion-canvas/ffmpeg`). — [AlternativeTo](https://alternativeto.net/software/motion-canvas/about); [package.json mirror](https://dev.ncot.uk/NCOT-Videos/agon-video-3-animations/blame/commit/69b66abda9709d4893e6ffec6235a1a5044960ae/node_modules/@motion-canvas/ffmpeg/package.json)
- Revideo is a fork that adds headless rendering, because Motion Canvas "requires you to press a button in its UI to render". — [Best of JS: Revideo](https://bestofjs.org/projects/revideo)
- Remotion publishes its own comparison page with Motion Canvas (vendor perspective). — [Remotion vs Motion Canvas](https://www.remotion.dev/docs/compare/motion-canvas)

**Headless browser frame timing**
- timesnap/timecut overwrite page time functions and capture at virtual times. Their README warns that "transitions/animations from CSS rules will likely not render as intended". — [timecut README](https://cdn.jsdelivr.net/npm/timecut@0.3.3/README.md); [timesnap](https://github.com/tungs/timesnap)
- puppeteer-capture uses the HeadlessExperimental CDP domain to capture deterministically. It requires injected replacements for setTimeout/setInterval, requestAnimationFrame, Date.now and performance.now before the page loads, and `waitForTimeout` cannot work in deterministic mode. — [puppeteer-capture](https://github.com/alexey-pelykh/puppeteer-capture)
- HeyGen's HTML-to-video write-up reports that rAF doesn't fire in BeginFrame mode, and that `<video>` decoders skip or fail in headless BeginFrame mode, so embedded video should be composited offline. — [HeyGen research](https://www.heygen.com/research/html-to-video)

**Safe areas (1080x1920)**
- TikTok publishes safe zones only for ads (In-Feed Ads template, 720x1280). Socialync scales it to a clear area of 840x1020 px, starting 120 px from the left and 240 px from the top, with the right button column about 180 px wide from y≈840. — [Socialync TikTok safe zones](https://www.socialync.io/tools/safe-zones/tiktok)
- Other third-party figures:
  - Vidpros puts the TikTok text-safe area at about 840x1280 centred, with 250-320 px kept clear at the bottom.
  - Vidpros puts the Reels safe area at 996x1400, with about 320 px at the bottom and about 84 px on the right.
  - AI Carousels (2025 layout) gives 131 px top, 367 px bottom and 120 px sides.
  - AdMake says its 2026 values were reverse-engineered from the live UI.

  — [Vidpros](https://vidpros.com/vertical-video-safe-zone/); [AI Carousels checker](https://www.aicarousels.com/free-tools/tiktok-safe-zone-checker); [AdMake](https://www.admakeai.com/blog/vertical-video-dimensions-2026)

**Emoji rendering**
- Noto Color Emoji is SIL OFL 1.1 (font) per Fontsource, and an Arch bug report clarifies that the tools are Apache while the fonts are OFL. — [Fontsource](https://fontsource.org/fonts/noto-color-emoji/about); [Arch bug 53452](https://bugs.archlinux.org/task/53452)
- Twemoji's licence is reported inconsistently across secondary sources (CC BY 4.0, MIT, mixed). — [Emojipedia licences](https://shop.emojipedia.org/pages/licenses); [Gentoo ebuild](https://gpo.zugaina.org/media-fonts/twemoji)

### Inferences
**Recommended approach.** Add a `chat` scene type to the existing engine: `render.html`, `scene_lib.py` and the scenes JSON. Each message gets an appear time. `render(t)` computes the state purely from t: which bubbles are visible, the typing-dots phase, the scroll offset, and each bubble's pop-in scale via an easing function. Because the engine already seeks with `window.render(k/FPS)` rather than letting CSS animations play, it avoids the CSS-transition and rAF problems documented for timecut and puppeteer-capture. The one rule is: no CSS `transition`/`@keyframes` and no `<video>` in the chat scene; compute everything in JS from t.

**Pitfalls and fixes**
- **Frame timing:** The engine already solves this. Keep all motion as a function of t.
- **Typing indicator:** Three dots with a sine phase per dot (`opacity = 0.4 + 0.6*max(0, sin(2π(t·1.4) − i·0.6))`). Show it for about 0.6-1.2 s before each incoming bubble, with duration scaled to message length so it feels natural.
- **Scroll physics:** Don't simulate physics. Measure bubble heights once at init (getBoundingClientRect), compute the target offset when a new bubble would overflow, and tween translateY with an ease-out (about 250-350 ms). Read heights before the first frame to avoid layout thrash. Fonts must be loaded before measuring (`document.fonts.ready`).
- **Emoji:** Headless Chrome on macOS picks up Apple Color Emoji from the system. That is a proprietary Apple font, and its licence for redistributed video was not verified. Bundle Noto Color Emoji (OFL) as a webfont and force it in `font-family` so renders are consistent and licence-clean. This fits the brand's "no emoji in content" rule anyway; emoji would mostly appear only inside story characters' messages.
- **Sound effects:** Mix them in the existing `mix_audio.py` with ffmpeg `adelay` at each message's appear time. Use self-made or royalty-free sounds, never iOS system sounds (see next section).
- **Safe areas:** Keep the chat panel inside about x 120-840 (right rail) and y 240-1500 at 1080x1920, so it clears the TikTok search bar, action rail, captions and username. Reels needs about 320 px at the bottom. Add a debug overlay toggle, as Remotion's safe-zone element does.
- **UI design:** Build an Edlintics-branded chat (brand blue for one side, neutral gray for the other, Ledger as avatar, brand fonts) rather than an iMessage clone. This avoids Apple trade-dress imitation and reads as a brand format, not a "fake text".

**Effort estimate** (inference, based on the existing 50-line render.js and 144-line render.html)
- **Minimal chat scene:** Bubbles, typing dots, auto-scroll, header with Ledger avatar, a JSON script format, a validator check and SFX placement in the mix. About 1-2 focused dev days, or 1-3 agent sessions plus a review.
- **Polished version:** Read receipts, reactions, an image-message bubble, light and dark themes, per-platform safe-zone presets and a skill doc for cheaper models. About 3-5 days in total.
- **Buy option:** texting.video at $9/mo, about $108 a year, or Chatimator at $5.99/mo. These are cheaper in raw cash but give no brand control and add manual per-video work in a web UI, plus unknown commercial terms. They are also outside the existing JSON → build → Canva hand-off pipeline.
- **Break-even:** For a brand already running its own renderer and producing many reels a week, break-even favours building within months, and the build has zero recurring licence cost.

**Remotion vs staying put.** Remotion is free only up to 3 employees, then at least $25/seat/mo or $100/mo for automation. Migrating means rewriting the engine in React. That is not justified for a chat format. Motion Canvas is free (MIT) but UI-driven, unless you use the Revideo fork, and it would be a second stack.

### Gaps
- Exact current Remotion 5.0 licence changes were not checked (the PR is only referenced).
- No developer blog post benchmarking chat-animation effort specifically was found. The estimate above is an inference.
- The Apple Color Emoji licence for use in rendered video was not found.
- Twemoji's authoritative licence (repo LICENSE file) was not fetched.

## Sound effects: royalty-free notification and typing sounds, avoiding Apple iMessage sounds

### Takeaway
Mixkit (free licence, attribution optional) and Pixabay (Content License, no attribution required) both allow commercial use of sound effects in social videos. Neither allows redistributing the files on their own. Apple's iOS system sounds (tri-tone, the iMessage "swoosh") have no licence found that permits their use in videos, so they should be replaced with original or stock sounds that do not copy them.

### Cited Findings
- **Mixkit:** Its official info page says: "Yes, you can use Mixkit Sound Effects for commercial and personal projects… YouTube, Social Media and Online Marketing ads", and "Attribution is appreciated but not required". Music and SFX are under separate free licences. Its terms bar selling unaltered copies and sublicensing, and some items are under a separate "Free Restricted" tier. — [Mixkit official info](https://mixkit.co/llm-info/); [Cinevva guide](https://app.cinevva.com/guides/free-sound-effects-music); [Newcastle Uni list](https://www.newcastle.edu.au/__data/assets/pdf_file/0007/875995/Suggested-sound-effects-sites.pdf)
- **Mixkit licence page:** Says each item type has its own licence, and the user must check which applies. The licence text itself was not rendered in the fetch. — [Mixkit license](https://mixkit.co/license/)
- **Pixabay:** Grants a "worldwide, perpetual, non-exclusive, royalty-free" right to use and modify content commercially, with no attribution required. Prohibited uses include selling or distributing content on its own, and trademark or logo issues. The user bears responsibility for third-party rights, and audio samples may need clearance. Pixabay hosts "message" notification SFX searches. — [Pixabay Terms](https://pixabay.com/service/terms/); [Pixabay FAQ](https://pixabay.com/service/faq/); [Pixabay message SFX](https://pixabay.com/sound-effects/search/message/)
- **Apple bundled audio:** Apple licenses the audio bundled with iMovie and Final Cut Pro for royalty-free commercial use, per Apple community docs. This does not address iOS system sounds. YouTube Content ID may still flag bundled Apple audio. — [Apple Community DOC-4201](https://discussions.apple.com/docs/DOC-4201); [Apple Community DOC-4532](https://discussions.apple.com/docs/DOC-4532)
- **Stock alternatives:** A commercial guide recommends royalty-free "cell phone alert" sounds "that evoke the vibe without copying Apple's specific tones". This is not a legal source. — [Voxbooster](https://voxbooster.com/blog/iphone-calling-sound)

### Inferences
- **Safest option:** Make or commission an original Edlintics "pop" and "typing tick" (for example, synthesised in a few lines with ffmpeg `sine` or `aevalsrc`, or recorded). This gives a brand-owned sonic signature with zero licence risk and no Content ID matches.
- **Second option:** Mixkit or Pixabay SFX, logged with source URL and download date in the asset folder, since Pixabay puts clearance responsibility on the user.
- Avoid any pack titled "iPhone/iMessage sound". These are often rips of Apple's system sounds, uploaded by users, regardless of the host's licence.
- Keep SFX quiet under the music and voice, consistent with the existing music-at-volume-8 rule.

### Gaps
- Pixabay's full Content License text (including any audio-specific clause) was not retrieved (HTTP 429).
- No primary Apple source (iOS SLA) on the use of system sounds in videos was found.
- Freesound (CC0 or CC-BY per file) and Zapsplat terms were not checked in this pass.

## Effort: minimal custom version vs tool subscriptions

### Takeaway
A minimal branded chat scene inside the existing engine is about 1-2 dev days (inference) with no recurring cost. Tools cost $5.99-$19.99 a month for watermark-free 1080p output, or $29-$99 a month for AI-voice suites. Tools win only for a one-off test; building wins for a repeatable, on-brand weekly format.

### Cited Findings
- **Tool costs:**
  - texting.video: $9/mo, or $4.99 per 24 h pass. — [texting.video pricing](https://texting.video/pricing)
  - Chatimator Pro: $5.99/mo. GhostShorts: $19.99-$79.99/mo. Brainrot Shorts: $29-$99/mo. CapCut Pro: $19.99/mo. — [GhostShorts comparison](https://ghostshorts.com/best-texting-story-makers)
- **Remotion (if chosen instead):** Free at 3 or fewer employees. Otherwise $25/seat/mo, or $0.01/render with a $100/mo minimum. — [Remotion LICENSE.md](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md); [remotion.pro/license](https://www.remotion.pro/license)
- **Existing engine:** Already does deterministic seek-per-frame capture at 1080x1920 with Puppeteer and ffmpeg (local file `.claude/skills/edlintics-explainer-reel/scripts/render.js`, observed 27 Oct 2026). Of the build pieces, only the chat scene, script schema and SFX cues are new. — (local codebase, not a web source)

### Inferences
- **Recommendation:** Build. Spend about 1-2 days adding a chat scene and a one-command build, matching the existing reel skills. If a format test is wanted before committing, a single $4.99 texting.video day pass could validate audience response first. Note that this would publish an imitation-skin, watermark-free video with unverified commercial terms.
- **Hidden costs of buying:** Manual per-video UI work, no JSON or agent automation, skins that imitate Apple or Meta, possible bundled AI voice (AI-label risk), and ToS uncertainty.

### Gaps
- No real time-to-produce-per-video figure for the tools was found. The comparison does not measure it.
