# Weekly performance review

How to refresh the "Edlintics Channel Performance" dashboard (https://claude.ai/artifact/2QsDUdLpSPuzWrzn7AznSa) and how to judge a post. First built on 24 Oct 2026, one day after the relaunch.

## When

Every Monday morning, before the Thursday content plan. Read figures for every post that is at least 48 hours old, plus follower counts.

## Rules

- Read only. Never like, comment, follow, post, change settings or press Boost while collecting.
- Copy what each platform shows. Never estimate. Leave a missing metric blank and note "not shown".
- If a platform is logged out or asks for a password or 2FA, stop for that platform and tell Hoang.
- Record when you read the figures (date and Vietnam time). Every number on the dashboard names its page and that time.

## Where each metric lives

| Channel | Page | Metrics there |
|---|---|---|
| Facebook and Instagram | Meta Business Suite › Insights › Content (`business.facebook.com/latest/insights/content?business_id=110625140398351&asset_id=108471317472449`). Scroll the table; it loads more rows as you go. | Views, reach, viewers (Facebook only), interactions, likes, comments, shares, saves, link clicks, follows, watch time. Facebook rows say "Multi media" or "Photo"; Instagram rows say "Carousel" with the lowercase account name. Facebook reach is removed from 31 Oct 2026; use viewers after that. |
| Facebook account | Insights › Results | 28-day views, viewers, content interactions, link clicks, visits, follows. Followers for both accounts are on the Business Suite home page. |
| Instagram followers | instagram.com/edlintics (profile description) | Exact follower and post counts. |
| LinkedIn | `linkedin.com/company/31541400/admin/analytics/updates/` › Content engagement table | Impressions, clicks, CTR, reactions, comments, reposts, engagement rate. Rows showing only dashes are duplicates; use the row with numbers. Followers and new followers are under the Followers tab. Don't copy follower names. |
| X | Open each post and add `/analytics` to its URL. | Impressions, engagements, detail expands, profile visits. Followers are on the profile. |
| Threads | `threads.com/insights` | Views per latest post, then 30-day views, viewers, interactions, net followers and follower vs non-follower viewers. |

## Refreshing the dashboard

1. Update `posts.json` (one row per post per channel; stories and self-reshares have `kind` `story` or `reshare`) and `channels.json` in the scratchpad, using the fields already there.
2. Upload each file to the dashboard as a new asset, then update its dataset's `url`, `name` and `updated`.
3. Rewrite `suggestions.json` from the new figures, and keep each suggestion's evidence and confidence.

## How to judge a post

- **Engagement from others comes first.** Every post carries our own like, first comment and reshare (see the `runs` collection in the hub). Subtract them before comparing posts. The rate from others is engagements from others divided by reach.
- **Compare within a channel.** Reach means different things: reach on Facebook and Instagram, impressions on LinkedIn and X, views on Threads.
- **Saves and shares by others matter most** for puzzles and carousels. Comments count next, and likes last.
- **Don't decide anything on fewer than 10 posts of a format or time slot.** Until then, label a finding as a hypothesis and name the test that would settle it.
- **Watch the funnel:** profile visits, link clicks and new followers per channel are what turn views into students.

## Weekly review in the hub (added 24 Oct 2026)

The hub's first tab, Performance (https://claude.ai/artifact/HbKxzWUcWhaBaaNb9buZM6), reads the document `perf/latest` in the hub database. After each weekly refresh, write the whole document with ArtifactData using the current version as if_version. It has these fields:
- `readAt`, `channels`, `posts`, `suggestions`, `fullUrl`: the figures and the dashboard link.
- `review.week`: the week covered.
- `review.text`: one short paragraph covering what happened, which channel and format did best, and what is still uncertain. Use engagement from other people, not totals.
- `review.next`: 4 to 6 concrete changes for next week, each one sentence and each tied to a number above.

Do not republish the page for a data refresh.

## Hypotheses and tracking (added 24 Oct 2026)

Every running test is listed in weekly-content-process.md with numbered hypotheses (H1, H2...) and a judge date. In each weekly review:
- Record the numbers per test in `perf/latest.tests`, as `{id, hypothesis, metric, baseline, current, n, verdict: pending|supported|rejected, note}`.
- Write the verdicts into the review paragraph.
- Turn supported results into rules in "Rules learned so far".

Do not call a verdict before the judge date, or with fewer than 4 posts per arm.

Running now:
- **5c-format:** Instagram carousel vs long video, until 21 Nov.
- **threads-topic:** H1 to H6, until 8 Nov.

Per Threads post, track views, the share of views from non-followers (Threads Insights), replies, reposts and follows, with `threadsTopic` and `threadsTopicVariant`.

## Daily metrics refresh (added 24 Oct 2026)

Run this every day straight after the first-comment run of the day's last post (the 18:00 Madrid slot, about 00:04 Vietnam). The first-comment skill triggers it.

1. **Scope:**
   - every post that went live in the last 7 days (Madrid dates);
   - every older post that belongs to a running test (slot fields such as `test`, `threadsTopicVariant`, or listed in `perf/latest.tests`). Keep re-reading it until that test's judge date, so each hypothesis is measured on data up to the moment it is checked;
   - any post a hypothesis or measurement names explicitly (for example "30-day saves").

   All other older posts keep their last figures; don't re-read them. When a test is judged, do one last full read of all its posts that day before writing the verdict.
2. **Read** (read only) each post's metrics per platform, from the sources listed above:
   - Business Suite Insights › Content for Facebook and Instagram;
   - LinkedIn page analytics › Updates;
   - X post analytics;
   - Threads Insights.
   Record views, reach, likes, comments, shares or reposts, saves, link clicks, follows, the share of views from non-followers where shown, and video watch time where shown. Record only what the platform shows: `null` = not shown.
3. **Update** `perf/latest` in the hub (ArtifactData, if_version from a fresh read):
   - replace or add those posts' rows in `posts`, keeping the own like, comment and repost counts so "engagement from others" stays correct;
   - refresh `channels` follower counts;
   - set `readAt`;
   - update each `tests[].current` and `n`.
   Leave `review` alone except on the weekly review day.
4. **Update** each slot that went live today to `status: "posted"`, with a one-line `statusNote` (for example "Posted 25 Oct; 24 h: IG 31 reach, Threads 40 views").
5. **Website traffic (once GA events are live):** in analytics.google.com, read sessions, engaged sessions and key events for the last 7 days by session source, medium, campaign and manual ad content (utm_content). Use the property that matches the date (see "Website analytics"). Add `site: {sessions, engaged, keyEvents, byEvent}` to each post row whose utm_content matches, plus a `siteTotals` block by channel. Untagged visits stay under their channel group.
6. **Log the refresh** in `runs/daily-<YYYY-MM-DD>` with `{at, postsUpdated, problems}`.

If the Mac was asleep and the refresh was missed, the next session's start check runs it once for the missed days.

## Website analytics (GA4) and UTM links (agreed with tutoring-web, 25 Oct 2026)

**Two GA4 properties, split by date (Hoang's decision, 25 Oct 2026; GA4 cannot merge properties):**
- **Before the switch date:** property 405129152 ("Edlintics", G-3XS7G1QBFT, account 190808750, authuser=1). About 134 days of history, with page views and enhanced measurement only, and no custom events.
- **From the switch date** (the first prod deploy after release PR #95; tutoring-web will send the exact date): property 263808863 ("Website", G-KT16RP1WLE, stream 2345294407).
- **Combining them in the Performance tab:**
  - Join by date.
  - Week-over-week across the switch compares sessions, users and channel or source figures only, because key events exist only in the new property.
  - Mark the switch date with a "property switch" annotation.
- **Data API:** if it is approved later, the service account needs Viewer on both properties. Do not add GA to the Performance tab until tutoring-web confirms the events are live on prod.

**UTM convention (every link we post):** lowercase, hyphens, no spaces.
- `utm_source` = platform: instagram, facebook, linkedin, x, threads, youtube, tiktok, newsletter, email, or partner-<name>.
- `utm_medium` = where the link sits: social-post (caption or first comment), social-bio, social-story, email, referral, or paid-social (reserved).
- `utm_campaign` = content stream or named campaign: puzzle, definition, this-vs-that, five-concepts, comic, explainer-reel, bio, or a named campaign such as oct-exam-2026 or launch-v1.
- `utm_content` = hub slot id (for example 2026-10-24-1800); bio links use "bio".

Example: `https://edlintics.com/?utm_source=instagram&utm_medium=social-post&utm_campaign=puzzle&utm_content=2026-10-24-1800`

**What the Performance tab will read from GA4:**
- Sessions, engaged sessions, engagement rate and new users by source, medium, campaign, utm_content and channel group.
- Key events (generate_lead, sign_up, begin_checkout, purchase, booking) on the same dimensions, plus conversion rate.
- Sessions and key events per landing page.
- purchaseRevenue in EUR by source and campaign.

**How:** read analytics.google.com in Chrome for now. The GA4 Data API with a service account is pending Hoang's decision.
