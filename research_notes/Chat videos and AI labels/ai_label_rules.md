# AI-generated content labelling rules (TikTok, Meta, YouTube, LinkedIn, X, Threads, EU AI Act) for Edlintics explainer reels, as of Oct 2026

Context: Edlintics formats under review are (a) a hand-drawn cartoon mascot (Ledger) with a realistic-sounding Kokoro text-to-speech voiceover, and (b) code-rendered chat "text story" videos (HTML, headless browser, ffmpeg) with fictional characters, typed messages, music and no voice.

## 1. What each platform requires creators to label, and whether synthetic voice or animated content counts

### Takeaway
All three big platforms tie *mandatory* creator labels to **realism**: content that looks or sounds real, shows real people, or shows events that did not happen. YouTube explicitly exempts animation, clearly unrealistic content and voiceovers in your own cloned voice. Meta's written rule is the only one that names **realistic-sounding audio** as its own trigger, so a realistic AI voice is the one grey area for format (a). Format (b) uses no generative AI and falls under none of these rules.

### Cited Findings

**YouTube (Help: "Disclosing use of altered or synthetic content", current page, ©2026, no last-updated date)**
- Creators must disclose content that "Makes a real person appear to say or do something they didn't do", "Alters footage of a real event or place", "Generates a realistic scene that didn't actually occur", or "Creates music that's the main focus of the video". — [YouTube Help](https://support.google.com/youtube/answer/14328491)
- Not required: clearly unrealistic content ("Someone riding a unicorn through a fantastical world"), and animation ("Using an AI-generated or altered animation of a missile in a fully animated video"). — [YouTube Help](https://support.google.com/youtube/answer/14328491)
- Also not required: "minor" or "primarily aesthetic" edits such as beauty filters, colour or lighting filters, caption creation, voice or audio repair, and "Cloning one's own voice to create voice overs or dubs". — [YouTube Help](https://support.google.com/youtube/answer/14328491)
- YouTube may put a lighter label in the expanded description for "non-music AI-generated audio or AI content that is non-photorealistic or animated". So a disclosure is possible for these but not required. — [YouTube Help](https://support.google.com/youtube/answer/14328491)

**TikTok (Community Guidelines, Integrity and Authenticity section; version released 25 Aug 2026, in effect 24 Sep 2026)**
- "we require creators to label AI-generated or significantly edited content that shows realistic-looking scenes or people" — [TikTok Community Guidelines](https://www.tiktok.com/community-guidelines/en/integrity-authenticity)
- The current section does not mention synthetic audio or voice. It names no explicit exemptions and does not define AIGC. — [TikTok Community Guidelines](https://www.tiktok.com/community-guidelines/en/integrity-authenticity)
- Earlier TikTok wording (AP, May 2024) required labels on AI content "that contains realistic images, audio, or video", and TikTok said it had "required creators to label realistic AIGC for over a year". This wording is older than 2025 and may be outdated; the 2026 guidelines say "realistic-looking scenes or people". — [AP via WJLA](https://wjla.com/news/nation-world/tiktok-answer-social-media-video-growing-amount-technology-universal-artificial-intelligence-ai-generated-content-label); [TechCrunch, 9 May 2024](https://techcrunch.com/2024/05/09/tiktok-automatically-label-ai-generated-content-created-other-platforms)
- Even labelled content is restricted if it is "misleading about matters of public importance or harmful to individuals". — [TikTok Community Guidelines](https://www.tiktok.com/community-guidelines/en/integrity-authenticity)

**Meta: Facebook and Instagram (Transparency Center, Manipulated Media community standard; change log runs to 7 Apr 2025 plus an undated "Today" entry)**
- "We require people to disclose, using our AI-disclosure tool, whenever they post organic content with photorealistic video or realistic-sounding audio that was digitally created or altered". — [Meta Transparency Center](https://transparency.meta.com/policies/community-standards/manipulated-media/)
- The policy has no explicit exemption for animation or parody in AI disclosure. Satire and humour come up only in the general misinformation context. — [Meta Transparency Center](https://transparency.meta.com/policies/community-standards/manipulated-media/)
- Meta "may place an informative label on the face of content", a more prominent one, when photorealistic or realistic-sounding content "creates a particularly high risk of materially deceiving the public". — [Meta Transparency Center](https://transparency.meta.com/policies/community-standards/manipulated-media/)

**LinkedIn**
- LinkedIn reads C2PA metadata and shows a "CR" badge. It runs no AI detector of its own, and coverage is incomplete. I found no rule requiring creators to self-label. — [Fortune, 26 Nov 2024](https://fortune.com/2024/11/26/linkedin-content-credentials-labeling-challenges-c2pa); [MediaPost](https://www.mediapost.com/publications/article/396225/linkedin-begins-labeling-ai-generated-content.html) (both from 2024, may be outdated)

**X**
- The Synthetic and Manipulated Media policy (April 2023 version) targets media that is "significantly and deceptively altered", shared deceptively, and likely to cause widespread confusion or harm. X may label or remove such media. — [X Help (help.twitter.com)](https://help.twitter.com/en/rules-and-policies/manipulated-media) (older than 2025; help.x.com returned 403 when fetched)
- A "manipulated media" warning reportedly began appearing in Nov 2025. In Mar 2026 X reportedly added a *voluntary* "Made with AI" creator disclosure. Both come from news reports, not X statements. — [exchange4media](https://www.exchange4media.com/digital-news/x-rolls-out-ai-content-labels-as-it-seeks-to-stabilise-advertising-revenue-152469.html)

**Threads**
- Meta's 2024 labelling announcement covered Facebook, Instagram and Threads together, so Threads follows the same Meta "AI info" approach. — [Meta newsroom](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/); [IANS](https://ianslive.in/meta-to-label-ai-generated-content-on-fb-instagram-threads-in-election-year--20240206184205)

### Inferences
- **Format (a), cartoon plus Kokoro voice:**
  - **YouTube:** no disclosure required. The video is "fully animated" and the narration does not make a real person say anything. The cartoon makes it clearly unrealistic.
  - **TikTok:** under the 2026 wording ("realistic-looking scenes or people") a hand-drawn mascot does not trigger the duty. The older "realistic ... audio" wording made the voice a grey area.
  - **Meta (Facebook, Instagram, Threads):** this is the real grey area. The written trigger is "realistic-sounding audio that was digitally created". A natural-sounding Kokoro narrator arguably meets it, even on an obviously animated video, because Meta's text has no animation exemption.
  - **Practical read:** the intent across Meta's policy is to stop *deception*. A narrator voice over a cartoon mascot, which does not imitate a real person, is low-risk. But turning on the "AI info" toggle on Meta, and optionally on TikTok, costs little and removes the ambiguity.
- **Format (b), code-rendered chat story with no voice:** no platform rule applies, because there is no generative-AI output and nothing photorealistic. A label is not required. Adding one would also be inaccurate unless the script or images were AI-generated. Exception: if a chat video presented fictional messages as a real screenshot from a real person or brand, that could fall under deceptive or misleading-content rules (TikTok's "misleading ... harmful to individuals", X's "shared deceptively"). Keep characters plainly fictional.
- AI-written *scripts or text* do not trigger a label on any of these platforms. All the rules are about images, video and audio.

### Gaps
- I could not retrieve Instagram's or Facebook's current Help Centre article on the "AI info" toggle (the Facebook help URL I tried returned "page does not exist"). Meta's examples of what counts as "realistic-sounding audio" (for example, whether a generic TTS narrator counts) are not published in the sources I found.
- The TikTok Support article on AIGC labels redirected to a JavaScript-only page and could not be read, so TikTok's current list of exemptions (such as animation or minor edits) is unconfirmed.
- I found no platform statement that directly addresses "AI voice over an animated cartoon".

## 2. Code-rendered or programmatic video, and how auto-labelling works (C2PA, IPTC, watermarks, classifiers)

### Takeaway
Auto-labels fire mainly on **embedded provenance signals**: C2PA Content Credentials, IPTC "digital source type" metadata, and invisible watermarks from AI tools or the platform's own AI features. YouTube and TikTok also use internal detection. A locally rendered Kokoro WAV and an ffmpeg or headless-browser MP4 carry none of these signals by default, so they are very unlikely to be auto-labelled through metadata. Classifier false positives remain possible on YouTube.

### Cited Findings
- **YouTube** may apply an AI label automatically for content made with its own GenAI tools, content with C2PA metadata, or content "its systems detect as AI-generated or altered". Creators are notified in Studio and can usually reverse a mistaken label by answering "No". Labels from C2PA metadata, YouTube's AI tools or manual review cannot be changed. — [YouTube Help](https://support.google.com/youtube/answer/14328491)
- **TikTok** has auto-labelled content carrying C2PA Content Credentials from other platforms since May 2024. It began with images and video, with audio "planned later". — [TechCrunch, 9 May 2024](https://techcrunch.com/2024/05/09/tiktok-automatically-label-ai-generated-content-created-other-platforms)
- On 24 Nov 2025 TikTok said it is adding invisible watermarks, readable only by TikTok, to AI content made with its own tools (for example, AI Editor Pro) and to uploads carrying C2PA. Labels have covered "over 1.3 billion videos to date". — [TikTok Newsroom, 24 Nov 2025](https://newsroom.tiktok.com/more-ways-to-spot-shape-and-understand-ai-generated-content); [TechSpot](https://www.techspot.com/news/110315-sick-ai-slop-feed-tiktok-finally-you-turn.html)
- **Meta** labels content through self-disclosure or "industry-shared signals". On 1 Jul 2024 Meta renamed "Made with AI" to "AI info" because minor AI retouching had been triggering the label. On 12 Sep 2024 Meta moved the label into the post menu for content that was only *edited* by AI. Content *generated* by AI still shows the label, with a note on whether it came from industry signals or self-disclosure. The page was last updated 23 Oct 2025. — [Meta newsroom](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/)
- Meta's 2024 coverage says its signals are C2PA and IPTC metadata plus invisible watermarks, though Meta has not detailed its detection method. — [Axios, Feb 2024](https://www.axios.com/2024/02/06/meta-ai-labeling-fix-oversight-board); [Slashdot/The Verge summary](https://tech.slashdot.org/story/24/04/05/187205/meta-will-require-labels-on-more-ai-generated-content) (2024, may be outdated in detail)
- **LinkedIn** relies on C2PA alone: no CR badge appears without embedded credentials. A Synthesia avatar video without C2PA carried no label. — [Fortune, Nov 2024](https://fortune.com/2024/11/26/linkedin-content-credentials-labeling-challenges-c2pa)
- C2PA metadata is often lost when files are re-encoded or re-uploaded. This is why TikTok is adding watermarks. — [TechSpot](https://www.techspot.com/news/110315-sick-ai-slop-feed-tiktok-finally-you-turn.html)
- **Kokoro-82M** is an open-weight, Apache-licensed TTS model (StyleTTS 2 / ISTFTNet). The sources I found describe no built-in watermark. — [DeepInfra model page](https://deepinfra.com/hexgrad/Kokoro-82M); [Together AI](https://together.ai/models/kokoro-82m)
- **Canva:** I found no Canva source confirming whether Dream Lab, Magic Media or exports attach C2PA Content Credentials. — [Canva Dream Lab help](https://www.canva.com/help/generate-with-dreamlab/) (no provenance mentioned)

### Inferences
- **ffmpeg and headless browser output:** ffmpeg writes only basic container tags (encoder name and similar). It has no C2PA signing, so an MP4 rendered this way carries no AI provenance signal. Even if a Kokoro track carried a watermark, ffmpeg re-encoding into AAC would likely degrade fragile marks. This is a technical inference and not verified by test here.
- **Main auto-label risks for Edlintics:**
  - **Canva AI features:** if the reels pass through Canva for music and Canva adds C2PA to AI-assisted exports (unconfirmed), every platform that reads C2PA would auto-label the video. On YouTube that label cannot be reversed.
  - **Platform AI tools:** using TikTok's or YouTube's in-app AI tools (AI voice, AI Editor, Dream Screen and similar) applies labels automatically.
  - **Classifiers:** YouTube's detection could flag a synthetic voice. The label could then be reversed by answering "No", unless it was applied after manual review.
- Recommended test: upload one Canva-exported reel to the Content Authenticity Initiative checker (contentcredentials.org/verify) before scaling.

### Gaps
- Whether Canva exports carry C2PA, and whether that applies only when Canva AI features are used, is unconfirmed. Check Canva's own trust or help pages, or test an export.
- None of the sources says whether any platform runs an audio-specific synthetic-voice classifier on uploads.
- I did not verify Kokoro's absence of a watermark against the official hexgrad repository. No local Kokoro install was found to inspect.

## 3. Penalties for not labelling

### Takeaway
Across platforms, penalties for a missing label are discretionary and escalate with harm or repetition: a label added by the platform, restricted reach, removal, and on YouTube possible loss of Partner Program status. None of the sources describes an automatic strike for one unlabelled, harmless video.

### Cited Findings
- **YouTube:** creators who "consistently" fail to disclose "may be subject to manual application of a label, or penalties from YouTube", including "removal of content or suspension from the YouTube Partner Program". — [YouTube Help](https://support.google.com/youtube/answer/14328491)
- **TikTok:** "Unlabeled content may be removed, restricted, or labeled by our team, depending on the harm it could cause." For You feed ineligibility appears separately, for misinformation that may cause moderate harm. — [TikTok Community Guidelines](https://www.tiktok.com/community-guidelines/en/integrity-authenticity)
- **Meta:** "we may apply penalties if they fail to" disclose. Repeat misinformation sharers can get "decreased distribution, limitations on their ability to advertise, or be removed". — [Meta Transparency Center](https://transparency.meta.com/policies/community-standards/manipulated-media/)
- **X:** misleading media may be labelled or removed. — [X Help](https://help.twitter.com/en/rules-and-policies/manipulated-media)

### Inferences
- For an education brand making harmless, non-deceptive cartoon explainers, the realistic worst case on Meta or TikTok is a platform-added label or some lost reach. Removal is reserved for harmful or misleading content.

### Gaps
- No platform publishes exact distribution penalties (for example, the percentage of reach lost) for a missing AI label. None states whether its own AI label itself lowers distribution. TikTok's AIGC slider suggests labelled content may be shown less to users who opt down (see section 4).

## 4. What changed in 2025-2026 (TikTok AIGC controls, Meta "AI info", YouTube, EU AI Act Article 50)

### Takeaway
The labelling duties in 2025-2026 stayed realism-based. What changed is that **labels now affect distribution**: TikTok's "Manage topics" slider lets viewers see less AIGC. The EU AI Act's deployer deepfake-disclosure duty applies from **2 Aug 2026**. The provider watermarking duty in Art 50(2) moved to **2 Dec 2026**. Neither EU duty plausibly covers a cartoon mascot or a code-rendered chat story.

### Cited Findings
- **TikTok, Nov 2025:** an AI-generated content control in "Manage topics" "to empower people to choose how much AIGC they want to see in their For You feeds". It was in testing at announcement. It has five levels and reduces AIGC rather than removing it. — [TikTok Newsroom, 24 Nov 2025](https://newsroom.tiktok.com/more-ways-to-spot-shape-and-understand-ai-generated-content); [TechSpot](https://www.techspot.com/news/110315-sick-ai-slop-feed-tiktok-finally-you-turn.html); [eWeek](https://www.eweek.com/news/tiktok-ai-transparency/)
- **TikTok, Aug-Sep 2026:** a new Community Guidelines version (released 25 Aug 2026, effective 24 Sep 2026) keeps the "realistic-looking scenes or people" label duty. — [TikTok Community Guidelines](https://www.tiktok.com/community-guidelines/en/integrity-authenticity)
- **Meta:** "Made with AI" became "AI info" on 1 Jul 2024. The label moved to the menu for AI-edited content on 12 Sep 2024. The page was updated 23 Oct 2025. — [Meta newsroom](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/)
- **YouTube:** the current help page keeps the March 2024 framework (realistic content must be disclosed; animation, unrealistic content and own-voice cloning are exempt). It adds auto-labels from C2PA and detection that cannot be reversed when applied from C2PA or manual review. — [YouTube Help](https://support.google.com/youtube/answer/14328491)
- **X:** a "manipulated media" warning was reported in Nov 2025, and a voluntary "Made with AI" disclosure was reported in Mar 2026. — [exchange4media](https://www.exchange4media.com/digital-news/x-rolls-out-ai-content-labels-as-it-seeks-to-stabilise-advertising-revenue-152469.html)
- **EU AI Act Art 50(2):** providers of systems "generating synthetic audio, image, video or text content" must mark outputs "in a machine-readable format and detectable as artificially generated or manipulated". This does not apply to systems that "perform an assistive function for standard editing or do not substantially alter the input data". — [AI Act Art 50](https://artificialintelligenceact.eu/article/50/)
- **EU AI Act Art 50(4):** deployers of AI that creates "image, audio or video content constituting a deep fake" must disclose it. For "evidently artistic, creative, satirical, fictional or analogous" works, the duty is limited to disclosure "in an appropriate manner that does not hamper the display or enjoyment of the work". AI-generated *text* on matters of public interest is exempt where there is "human review or editorial control" and a person holds "editorial responsibility". Disclosure must happen "at the latest at the time of the first interaction or exposure" (Art 50(5)). — [AI Act Art 50](https://artificialintelligenceact.eu/article/50/)
- **AI Act timeline:** Article 50 applies from 2 Aug 2026. The Digital Omnibus agreement (provisional deal 7 May 2026) postpones the Art 50(2) watermarking obligations for providers "until December 2, 2026". "All other transparency obligations, including those that apply to deployers, will continue to apply from August 2, 2026." — [Hogan Lovells, 7 May 2026](https://www.hlc.com/en/publications/eu-legislators-agree-to-delay-for-highrisk-ai-rules); [FEDIL](https://fedil.lu/en/publications/ai-act-update-enforcement-begins-as-the-digital-omnibus-reshapes-the-timeline/?pdf=1) (names it Regulation (EU) 2026/1744 and gives the end of the grace period for pre-existing GenAI systems as 2 Dec 2026). One source, Kennedys, gives 2 Feb 2027 for some Art 50(2) steps, which likely reflects an earlier draft. — [Kennedys](https://www.kennedyslaw.com/en/thought-leadership/article/2026/the-2025-european-commission-eu-digital-omnibus-package-the-eu-ai-act)
- **Deep fake definition (Art 3(60)):** AI-generated or manipulated image, audio or video content "that resembles existing persons, objects, places, entities or events and would falsely appear to a person to be authentic or truthful". — [AI Act Art 3](https://artificialintelligenceact.eu/article/3/) (wording from the Act; not re-fetched in this session)

### Inferences
- **Art 50(4) and Edlintics:** a hand-drawn mascot narrated by a generic synthetic voice does not "resemble existing persons" and would not "falsely appear ... authentic", so it is not a deep fake and the deployer disclosure duty does not apply. A Kokoro voice imitating a real, identifiable person would change this, and so would a photoreal AI presenter. Code-rendered chat videos involve no AI system at all.
- **Art 50(2)** binds *providers* of generative systems (here, Kokoro's developers and hosted TTS vendors), not a brand that uses the output. If Edlintics self-hosts Kokoro, it might arguably be treated as putting an AI system into service. The open-source exemption in the AI Act does not cover Art 50. This point is legally uncertain; get advice if it matters.
- **Distribution:** a voluntary label on TikTok may slightly reduce reach among users who turned the AIGC slider down. This is a trade-off with transparency, not a legal question.
- **Recommendation:**
  - **Format (a):** turn on Meta's "AI info" toggle, where it is a grey area, to stay on the safe side. Optionally add a caption line such as "voice: AI narrator" if Hoang wants consistent transparency across platforms. No label is needed on YouTube. On TikTok it is optional under the 2026 wording.
  - **Format (b):** no label anywhere.

### Gaps
- I did not fetch the Official Journal text of Regulation (EU) 2026/1744 to confirm the final dates. These rest on law-firm summaries.
- The EU Code of Practice on marking and labelling AI-generated content (Art 50(7)) and any final Commission guidelines were not reviewed. They may set specific label formats.
- Exact rollout status of TikTok's AIGC slider and invisible watermarks after testing (general availability, regions) was not confirmed.

## Local file check (coordinator, 27 Oct 2026): which of OUR videos carry C2PA
Method: scanned the exported MP4s in the scratchpad (posts/*/music8/) for C2PA/JUMBF manifests.
- The five-concepts videos (economics, statistics, marketing, management and their clips 2-6, Canva exports with AI-generated Ledger clips) DO carry a signed C2PA manifest: softwareAgent "Canva AI", digitalSourceType http://cv.iptc.org/newscodes/digitalsourcetype/compositeWithTrainedAlgorithmicMedia. Platforms that read C2PA (Meta, TikTok, YouTube, LinkedIn) can auto-label these as AI.
- The explainer reels with the Kokoro voice (accruals, break-even, salesperson, working capital, marginal utility, diminishing returns, deskilling, Moravec), also exported from Canva, carry NO C2PA manifest (0 hits for c2pa.claim). Clips 1 and 7 of the five-concepts sets (title/end cards) also have none.
- Inference: Canva attaches the "AI" manifest when the design contains Canva AI or AI-generated media, not on every export. An auto-applied AI label is therefore most likely coming from the five-concepts videos' AI-generated clips, not from the TTS voice. Code-rendered chat videos exported the same way as the reels would carry no manifest.
