# Edlintics Marketing Engine

An automated marketing department for **Edlintics** (the tutoring SaaS at `../tutoring-site`).
Independent, local-first project. Reads Edlintics data over its public `/api/v1`; never imports app code.

Audience for all content: **finance/accounting university students**. Topic-led — a university is named
only as *secondary* context, never as the headline (trademark/independence reasons).

Brand voice: calm, expert, direct, practical, slightly serious. **No exclamation points. No emoji.**

---

## The two loops

This runs as **two loops at different cadences** — a strategy conversation you drive, and a daily
production cron that executes what you decided.

### Tier 1 — Strategy loop (you ⇄ Marketing Manager, weekly / on-demand)

The Manager is an agentic assistant. It comes to each session prepared with a data-grounded briefing,
proposes 2-3 directions, and argues them out with you. You bring domain judgment; it brings the data.

```
 ┌──────────────────────────────────────────────────────────────────┐
 │  MARKETING MANAGER arrives with:                                 │
 │   PERFORMANCE DIGEST   what posted, what landed, the funnel      │
 │     <- PostHog (catalog->course->enrol), platform stats         │
 │   TREND SCAN           what finance/acct students care about     │
 │     <- WebSearch + seasonality (exam periods) + format trends   │
 │   FIRST-PARTY SIGNAL   YOUR data, not generic                    │
 │     <- onboarding "wanted-it-didn't-enrol" demand gaps          │
 │     <- feedback / survey campaign answers                       │
 │   2-3 PROPOSALS        pillars / campaigns, each with rationale  │
 └───────────────────────────────┬──────────────────────────────────┘
                                 v
        ┌──────────────────────────────────────────────┐
        │   BACK-AND-FORTH                             │
        │   You: domain expertise + gut                │
        │   Manager: data + options                    │
        │   ("students don't care about X, they're     │
        │    stressed about Y" -> it re-proposes)      │
        └───────────────────────────┬──────────────────┘
                                    v
        ┌──────────────────────────────────────────────┐
        │   LOCKED DECISIONS                           │
        │   - content pillars for the period           │
        │   - active campaign(s) + angle               │
        │   - what to film next session                │
        └───────────────────────────┬──────────────────┘
                                    │ writes
                            CONTENT CALENDAR
                                    │ drives
```

### Tier 2 — Production loop (daily cron, autonomous)

```
 ┌─ YOU (2 days/week) ──────────────────────────────────────────────┐
 │  Film 1 long video, talk naturally through 2-3 concepts          │
 │  -> drop the file in assets/raw-footage/                         │
 └───────────────────────────────┬──────────────────────────────────┘
                                 v   (daily cron from here)
        [1] INGEST + TRANSCRIBE       Whisper -> every word timestamped
        [2] EDIT DECISION LIST (LLM)  cut ums/dead air; pick 3-5 short
                                      windows; mark animation beats
        [3a] FLUENCY CUT (ffmpeg)  ┐
        [3b] CONCEPT ANIM (Remotion)├ run in parallel, then merge
        [3c] CLIP + REFRAME 9:16   ┘
        [4] ATOMIZE                   1 video -> ~10 assets:
                                      1 hero, 3-5 shorts, 2-3 carousels,
                                      1 blog, 1 newsletter
        [5] QUALITY GATE              brand voice + uni-trademark check
                                      + virality check on video
        [6] APPROVAL (you, ~5 min)    daily content drop; nothing posts
                                      until you OK it
        [7] SCHEDULE + PUBLISH        IG / LinkedIn / TikTok via scheduler;
                                      blog + newsletter reuse Edlintics
        [8] ANALYST                   pull results -> back to the calendar
                                                    -> shapes next session
```

One filmed concept atomizes into ~10 assets, so **2 filming days/week, filmed ahead, build a content
bank** that keeps the calendar full even on a bad week.

---

## Why a separate repo (not inside tutoring-site)

- Different runtime (local agent, not Next.js), different deps, different secrets, different cadence.
- Edlintics was designed so external clients consume `/api/v1` ("a future native client is a packaging
  task, not a rewrite") — this engine is exactly such a client. Loose coupling, no shared build.
- Clean security boundary: its own `.env`; Canva/Ayrshare keys never touch the app's Vercel env.
- Reusable across Hoang's other businesses (any `/api/v1`).
- Reversible: durable slices (calendar, approval queue) can graduate into the Edlintics admin later.

---

## Folder layout

```
manager/    Tier 1: the strategy agent (briefing builder, proposal loop)
pipeline/   Tier 2: ingest -> edit -> atomize -> publish
remotion/   animated concept templates (T-account, DCF, CVP, ratios...)
calendar/   the content calendar (system of record)
config/     brand tokens (mirrored from tutoring-site/app/globals.css), settings
assets/     raw-footage/ (you drop here) + renders/ (output)
docs/       design notes, decisions
```

---

## Tooling (local-first)

- **Brain:** Claude (Claude Code session + Anthropic API).
- **Creative:** Canva (brand templates), Higgsfield (cinematic AI video / clips).
- **Render:** local `ffmpeg` + **Remotion** (data-accurate animated graphs) + Whisper (transcription).
  None installed yet — `brew install ffmpeg`, plus Whisper, when the pipeline slice starts.
- **Publish:** a social scheduler API (Ayrshare / Metricool / self-host Postiz) — TBD.
- **Newsletter:** reuse Edlintics' existing broadcast system (E048).

---

## Open decisions (not yet locked)

- Channels in scope (IG / LinkedIn / TikTok / blog+newsletter).
- Strategy-session cadence (weekly ritual vs on-demand) and where the briefing is delivered.
- Publishing scheduler choice.
- Approval-gate strictness (review-before-publish vs hybrid by channel).

## Proposed first build slice

**Tier 1 only:** the Manager strategy chat + the content calendar. Lowest new infra (just the LLM +
data Edlintics already collects, read via `/api/v1`). No video/publish pipeline yet. Build from the
brain outward.

---

## Build log

- 2026-06-05 — Repo scaffolded. Design captured (two-tier engine, local-first, independent).
  Decision: separate repo, reads Edlintics over `/api/v1`. First slice = Tier 1 manager + calendar.
