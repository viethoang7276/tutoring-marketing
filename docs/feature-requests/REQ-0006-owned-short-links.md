# REQ-0006  ·  Owned short links (edlintics.com/go/<code>) for social posts

- **Status:** proposed
- **Date:** 2026-10-28
- **Source:** Hoang ("these tags are quite long and some platforms don't work with it, like Instagram")
- **Targets metric:** acquisition attribution (site sessions and waitlist signups per post and platform)
- **Priority (CMO view):** medium
- **Effort guess (CMO, non-binding):** S

## Summary
First comments carried full UTM links such as `edlintics.com/?utm_source=instagram&utm_medium=social-post&utm_campaign=explainer-reel&utm_content=def-break-even`. They look messy, and on Instagram and TikTok links in comments are not clickable at all. On 28 Oct 2026 Hoang approved removing the tags from first comments (plain `edlintics.com`, and "link in bio" on Instagram and TikTok). We lose per-post attribution until a short, clean link on our own domain exists

## Proposal
A redirect route on edlintics.com: `edlintics.com/go/<code>` answers with a 302 to a stored target URL that carries the full UTM tags. Example: `edlintics.com/go/fb-breakeven` goes to `/?utm_source=facebook&utm_medium=social-post&utm_campaign=explainer-reel&utm_content=def-break-even`

## Proposed requirements (CTO owns the final design)
- The system shall resolve `/go/<code>` (lowercase letters, digits, hyphens, max 32 characters) to a stored target and redirect with 302, keeping any extra query parameters
- Targets shall be limited to edlintics.com paths (no open redirect)
- An unknown code shall redirect to the home page with `utm_campaign=unknown-go-link`, never a 404
- The system shall count hits per code (a counter or a GA/PostHog event `go_link_hit`), and expose counts per code and day through `/api/v1` for the marketing daily metrics refresh. No personal data
- Admins (and marketing, through the admin screen in Chrome, as content is published) shall create a code with its target. No write API is needed; a bulk paste of several codes at once would help, because each post needs one code per platform (up to 4: Facebook, LinkedIn, X, Threads)
- Social preview (Open Graph) shall show the target page's card, so the redirect must work for crawlers (Facebook, LinkedIn, X, Threads)
- Bots and crawler hits should be excluded from the counts where possible

## Success signal
Per-post site sessions and waitlist signups readable again for Facebook, LinkedIn, X and Threads first comments, with links under 35 characters

## Out-of-scope check
Marketing reads only through `/api/v1` and enters codes through the admin screen; no app code is imported. No third-party shortener (bit.ly and similar hide our domain and look spammy). Schema work, if any, stays in the CTO lane. Related: REQ-0003 (waitlist stores UTM on signups)

## Decision log
- 2026-10-28 — proposed by CMO after Hoang approved the plan: no tags in first comments now, owned short links next
- _(Hoang / CTO: approve / defer / reject + reason here.)_
