# Shared brief: script proposals, 17 Nov 2026

Hoang asked (17 Nov 2026, 01:xx VN): "Propose ... Script the other career ladder videos, city hub map video and then I want a new video idea on explain the difference in the department inside the big 4 accounting firms (we can use their logo)". He reviews tomorrow.

**This is SCRIPT ONLY.** Do not render, do not run make_reel.sh or render-slot.sh, do not generate voice, do not touch Canva, the hub `slots`, any social platform or the browser for posting. Do not download logo files. Research with WebSearch / WebFetch is expected. Do not commit to git (the lead does that).

## Read first (all writers)
Repo: `/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing`
- `edlintics-marketing/CLAUDE.md` hard rules and `docs/brand-guidelines.md` (voice: calm, expert, direct; no exclamation points; no emoji except at the end of first comments; no hype)
- `docs/content-workflow/weekly-content-process.md`: "Rules learned so far", "Reel story structure", "Rules from our own Instagram results"
- `docs/content-workflow/concept-registry.md`, then query the hub `concepts` collection (ArtifactData, url https://claude.ai/artifact/HbKxzWUcWhaBaaNb9buZM6, action "list", collection "concepts", query.limit 1000; load the tool with ToolSearch "select:ArtifactData"; READ ONLY)
- The skill for your format (named in your task)

## House rules that every script must follow
- Every voice line and on-screen line is a full sentence; captions and comments too. No full stop at the end of any paragraph, caption, comment or on-screen line.
- Direct opening: beat 1 says what the video is ("From X to Y, the career ladder explained with Ledger in 90 seconds" / "... in under 2 minutes"). Only state a length the script really fits (about 2.5 words per second with the default voice). Hard cap 120 s; never state exact seconds other than "90 seconds" when it truly fits, otherwise "in under 2 minutes".
- Start most lines with a linking word (First, Then, Now, So, Next, But, Finally). One story, not a list.
- Every person, object and move the voice names is something the animation can draw at that word: write a short `visual` note per beat.
- Mix currencies across posts; one currency inside a post; real-world figures stay in their reported currency. Numbers only with 2 sources.
- No tutoring, no exams, no "swipe", no investment advice, no "best"/"highest paying" unless a source says it.
- Sources: only list a URL you actually opened (WebFetch); mark snippet-only sources `"opened": false`. At least 2 sources for each career ladder and for each Big 4 claim; at least 1 opened source per map stop fact.
- Registry check: state "registry check: clear ..." or name the conflict.
- First comments: 1-2 sentences, under 150 characters, end with 1-2 emojis (the only place emojis are allowed), no links/UTM in `first_comment`; `first_comment_igtt` (Instagram and TikTok) may say "link in bio".
- Threads destination: `threadsTopic` + `threadsReason`.

## Output: one JSON file per reel in this folder
`docs/proposals/2026-11-17/<slug>.json` with exactly these keys:
```
{
  "slug": "...", "group": "ladder" | "map" | "big4",
  "title": "...", "proposedSlot": "e.g. Tue 24 Nov 21:30 VN (to confirm)",
  "estSeconds": 88, "wordCount": 214,
  "summary": "one sentence on why this reel, for Hoang",
  "beats": [ {"n": 1, "role": "title|rung|climb|payoff|stop|hop|intro|dept|compare|cta|...", "label": "rung 1 / stop 3 Seoul / Audit", "voice": "full sentence", "onScreen": ["chips or card text"], "visual": "what is drawn and what moves"} ],
  "caption": "...", "first_comment": "...", "first_comment_igtt": "...",
  "hashtags": ["#edlintics", "..."], "threadsTopic": "...", "threadsReason": "...",
  "logos": [ {"brand": "...", "city": "...", "why": "based there, source url"} ],   // [] if none
  "sources": [ {"claim": "...", "url": "...", "opened": true} ],
  "registry_check": "...",
  "openQuestions": ["anything Hoang must decide"]
}
```
Finish with a short report (under 200 words): files written, anything weak or unsourced, open questions.
