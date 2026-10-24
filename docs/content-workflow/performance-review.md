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
