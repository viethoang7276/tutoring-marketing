# Social publishing infrastructure — build vs buy
# Platform-API reality check and commodity-provider survey

_Prepared 2026-06-23 by the market researcher for the CMO strategy session._
_All web sources accessed 2026-06-23 unless noted. Claims with no verifiable primary source are
flagged [UNVERIFIED]. Nothing here is a recommendation — that is the CMO's call._

---

## TL;DR — five things that matter before the strategy call

1. **DIY direct-platform APIs carry a gatekeeping tax of 4–12 weeks per platform before you can
   post publicly.** TikTok requires a manual audit (2–6 weeks, multiple rounds, strict UX
   requirements). Meta App Review for Instagram publishing permissions takes 2–6 weeks per
   permission, with screencast evidence required. YouTube quota increases take 1–6 weeks and may
   come back lower than requested. Facebook page publishing is the most accessible but still needs
   `pages_manage_posts` app review. That is roughly a quarter of calendar time before launch.

2. **Ayrshare is the most mature API-first commodity layer.** It covers all four target platforms
   (TikTok, Instagram, YouTube, Facebook), ships an official MCP server and SDK, and its pricing
   starts at $149/month for a single brand. Critical unknown: whether Ayrshare's TikTok integration
   uses a shared audited app on the customer's behalf, or whether each customer still needs their
   own TikTok audit. This is the single most important unresolved question for build-vs-buy.

3. **Postiz (self-hostable, AGPL-3.0) ships a native MCP server and a postiz-agent CLI that speaks
   to Claude/OpenClaw out of the box.** It is the only option in scope that is free at infrastructure
   cost and purpose-built for AI-agent control planes. However, self-hosted Postiz requires each
   customer (or operator) to register their own OAuth developer app per platform — the platform
   gatekeeping is not abstracted away. TikTok public posting still requires the operator to pass
   TikTok's own audit.

4. **Metricool and Buffer both have APIs but are not designed as infrastructure layers for wrapping.**
   Metricool's API gates behind its Advanced plan ($53+/month annual) and does not publicly
   document rate limits. Buffer's developer API is GraphQL, in beta, and primarily designed for
   individual-workflow automation, not programmatic multi-account publishing at scale.

5. **No provider fully absorbs all four-platform gatekeeping.** Every option — including commodity
   providers — still exposes the operator to some version of platform app review for at least one
   of the four target platforms. The question is how much of that burden is pre-absorbed vs
   delegated back.

---

## Strand 1 — Direct platform-API reality

### 1.1 TikTok Content Posting API

**Product page:** https://developers.tiktok.com/products/content-posting-api/ (accessed 2026-06-23)
**Get-started guide:** https://developers.tiktok.com/doc/content-posting-api-get-started (accessed 2026-06-23)

#### Registration and app setup
- Register at developers.tiktok.com; account registration is instant.
- Add the "Content Posting API" product to the app; request the `video.publish` scope.
- This triggers manual review.

#### Approval timeline
- Manual review of the `video.publish` scope takes 2–6 weeks; multiple feedback rounds are common.
- Required submission materials: a demo video or screenshots of the OAuth and upload flow end-to-end,
  a real privacy policy page (a placeholder fails), a clear data-handling description, and a working
  Terms of Service URL.

Source: https://zernio.com/blog/tiktok-developer-api (accessed 2026-06-23);
https://developers.tiktok.com/doc/content-sharing-guidelines (accessed 2026-06-23)

#### Unaudited client restrictions
Before passing TikTok's additional "Direct Post Audit":
- Posts are forced to `SELF_ONLY` visibility — they are private by default regardless of user intent.
  The account owner must manually change account visibility to public, then change each post to
  "Everyone" after the fact.
- Only 5 users can post via the app in any 24-hour window.

Source: https://developers.tiktok.com/doc/content-posting-api-get-started (accessed 2026-06-23);
https://postproxy.dev/blog/how-to-post-to-tiktok-via-api/ (accessed 2026-06-23)

#### Audit requirements to lift restrictions
TikTok's "Direct Post Audit" is a separate compliance review on top of scope approval. Key hard
requirements verified during audit:
- The app must display the creator's username and avatar before every post (non-negotiable UX
  requirement TikTok verifies).
- Users must be able to configure duet, stitch, and comment settings per post — these controls
  must be exposed in the UI.
- Audit timeline: 2–4 weeks, multiple rounds of feedback typical.

Source: https://www.postpeer.dev/blog/best-tiktok-posting-api (accessed 2026-06-23);
https://docs.mixpost.app/services/social/tik-tok/direct-post-audit/ (accessed 2026-06-23)

#### Rate limits (post-audit)
- 6 POST requests/minute to initiate posts.
- Approximately 15 posts per day per creator across all API clients.
- Video must be MP4/H.264; chunked upload 5–64 MB per chunk, final chunk up to 128 MB.
- TikTok is video-only via API — no image or carousel posting via the Content Posting API.

Source: https://postproxy.dev/blog/social-media-platform-api-rules-rate-limits-media-specs/
(accessed 2026-06-23)

#### Known gotchas
- An unaudited client posting even one video publicly is a terms violation, not just a restriction.
- Media files must be publicly reachable over HTTPS; localhost or private network routes fail the
  pull-from-URL flow.
- The scope `video.create` referenced in some third-party docs appears to no longer exist in
  TikTok's console; the correct scope is `video.publish`.

Source (scope issue): GitHub issue #1161, gitroomhq/postiz-app (accessed 2026-06-23)

---

### 1.2 Meta Graph API — Instagram and Facebook publishing

**Overview:** https://developers.facebook.com/docs/instagram-platform/overview/ (accessed 2026-06-23)
**Rate limits:** https://developers.facebook.com/docs/graph-api/overview/rate-limiting/ (accessed 2026-06-23)

#### Instagram publishing requirements
- Only Instagram Business or Creator accounts can authorize the Graph API. Personal accounts
  cannot be used at all.
- The Business/Creator account must be linked to a Facebook Page — permissions flow through the
  Page. An unlinked account cannot publish.
- Required permissions: `instagram_business_basic` (prerequisite) and
  `instagram_business_content_publish`. Each requires a separate app review submission with a
  screencast.

Source: https://www.getphyllo.com/post/instagram-api-integration-101-for-developers-of-the-creator-economy
(accessed 2026-06-23); https://zernio.com/blog/instagram-graph-api (accessed 2026-06-23)

#### Access levels
- Standard Access: the default; limits app to accounts the developer owns or manages. Sufficient
  if Edlintics only publishes to its own channels. No formal app review required beyond basic app
  registration to stay in Standard Access.
- Advanced Access: required if the app serves Instagram accounts the developer does not own.
  Requires formal Meta App Review, approximately 2–6 weeks per permission.

Source: https://developers.facebook.com/docs/instagram-platform/overview/ (accessed 2026-06-23)

#### Instagram publishing rate limits
- 200 API calls per hour per user account.
- 100 posts published per rolling 24-hour window per account (all content types combined).
- Reels publishing is a three-step process: create container → poll until `status_code: FINISHED`
  → publish. A video 5–90 seconds at 9:16 aspect ratio appears in the Reels tab; outside that
  range it publishes as a regular video post.

Source: https://postproxy.dev/blog/social-media-platform-api-rules-rate-limits-media-specs/
(accessed 2026-06-23); https://postproxy.dev/blog/instagram-reels-api-publishing-guide/
(accessed 2026-06-23)

#### Facebook page publishing
- Core permission required: `pages_manage_posts`. Requires app review before use on pages the
  developer does not own.
- App review timeline: 5–10 business days for initial review; 3–5 business days for second reviews.
  Total first-submission cycle plan: 1–4 weeks.
- Current API version as of mid-2026: Graph API v21.0 (v20.0 sunsets September 24, 2026).
- Rate limit: 200 API calls per user per hour; 25 posts per Page per 24 hours.
- Non-expiring Page tokens are available through a multi-step token exchange, which makes
  automation more stable.

Source: https://posteverywhere.ai/blog/post-to-facebook-api (accessed 2026-06-23);
https://developers.facebook.com/docs/graph-api/overview/rate-limiting/ (accessed 2026-06-23);
https://zernio.com/blog/facebook-api (accessed 2026-06-23)

#### Meta gotchas
- Each permission (`pages_manage_posts`, `instagram_business_content_publish`,
  `instagram_business_basic`) is a separate app review submission — three rounds minimum for full
  IG + FB coverage.
- The reviewer requires a screencast showing exactly how data is used for each permission.
- Advanced Access enforcement tightened in 2026; apps serving accounts the developer does not own
  that lack Advanced Access will be blocked.

Source: https://storrito.com/resources/instagram-api-2026/ (accessed 2026-06-23)

---

### 1.3 YouTube Data API v3 — video upload

**Quota and compliance:** https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits
(accessed 2026-06-23)
**Quota calculator:** https://developers.google.com/youtube/v3/determine_quota_cost (accessed 2026-06-23)

#### Default quota
- 10,000 units per day per Google Cloud project.
- One video upload (`videos.insert`) costs 1,600 units.
- Default ceiling: 6 videos uploaded per day maximum.

Source: https://www.getphyllo.com/post/youtube-api-limits-how-to-calculate-api-usage-cost-and-fix-exceeded-api-quota
(accessed 2026-06-23); https://postproxy.dev/blog/social-media-platform-api-rules-rate-limits-media-specs/
(accessed 2026-06-23)

#### Quota increase process
- Submit the "YouTube API Services — Audit and Quota Extension Form" in Google Cloud Console.
- Provide: project ID, use case description, expected volume, business justification, privacy policy
  URL, and terms of service URL.
- Timeline: 1–6 weeks per developer reports; public community threads document delays of up to
  five months. Google's own guidance says 3–5 business days, which does not match reported
  experience.
- Approval may come in below what was requested; scraping or bulk-harvesting use cases are
  routinely rejected.
- Failed uploads still consume quota units.

Source: https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits (accessed 2026-06-23);
https://codivupload.com/blog/youtube-api-quota (accessed 2026-06-23)

#### Gotchas
- Phone-verified YouTube channels bypass some upload blocks that otherwise surface as opaque
  errors; Ayrshare's changelog explicitly notes phone verification as the primary fix for blocked
  thumbnail uploads as of June 2026.
- YouTube Shorts via API require the video to be ≤60 seconds and have a vertical aspect ratio
  (9:16); the Shorts shelf assignment is not guaranteed and depends on algorithmic classification.
- API access is free; quota is the binding constraint, not price.

Source: https://www.ayrshare.com/docs/whatsnew/latest (accessed 2026-06-23);
https://www.getphyllo.com/post/is-the-youtube-api-free-costs-limits-iv (accessed 2026-06-23)

---

## Strand 2 — Commodity publishing/analytics providers

### 2.1 Ayrshare

**Homepage:** https://www.ayrshare.com/ (accessed 2026-06-23)
**Pricing:** https://www.ayrshare.com/pricing/ (accessed 2026-06-23)
**Changelog:** https://www.ayrshare.com/docs/whatsnew/latest (accessed 2026-06-23)

#### Platform coverage
TikTok, Instagram, YouTube, Facebook, X/Twitter, LinkedIn, Pinterest, Reddit, Telegram, Snapchat,
Threads, Bluesky, Google Business Profile — 13+ platforms as of 2026-06-23.

#### Does it handle the platform app-review burden?
This is the critical unknown. Ayrshare markets itself as "an alternative to integrating the TikTok
API directly and seeking approval" (from their own blog post), and they describe a partnership with
TikTok for direct publishing. However, no publicly accessible Ayrshare documentation page
retrieved on 2026-06-23 explicitly states whether customers use Ayrshare's own audited TikTok app
(no customer-side audit required) or whether each customer must still register and audit their own
TikTok developer app. The third-party comparison site postpeer.dev states that for any API
provider, "direct (non-draft) public posting requires TikTok app audit on your account," which
suggests the burden is not fully abstracted. This claim requires verification directly with
Ayrshare support before the CMO can rely on it.

For Instagram: Ayrshare likely uses Meta's approved app infrastructure internally, and Standard
Access (publishing only to accounts one manages) does not require customer-side app review. This
is the more tractable integration and Ayrshare's changelog shows it is actively maintained.

Source: https://www.ayrshare.com/introducing-tiktok-direct-publishing-analytics-and-commenting/
(accessed 2026-06-23); https://www.postpeer.dev/blog/best-tiktok-posting-api (accessed 2026-06-23)

#### API quality and completeness
- REST API with SDKs across major languages.
- Covers scheduling, publishing, pulling analytics, comment management, webhook callbacks.
- As of June 2026 changelog: TikTok photo posts supported (not just video); Instagram Trial Reels
  supported; YouTube custom thumbnail failures now surface as warnings (non-blocking); LinkedIn
  personal profile analytics expanded.
- Rate limits: "expanded" on Launch plan vs Premium; specific unit numbers not published publicly.

Source: https://www.ayrshare.com/docs/whatsnew/latest (accessed 2026-06-23);
https://github.com/ayrshare/social-media-api (accessed 2026-06-23)

#### Pricing (accessed 2026-06-23 from ayrshare.com/pricing)

| Plan | Monthly price | Social profiles | Notes |
|---|---|---|---|
| Premium | $149/month ($1,548/yr) | 1 | Basic analytics, API access, email support |
| Launch | $299/month | Up to 10 | Advanced analytics, expanded API rate limits, webhooks, custom branding, 28-day free trial |
| Business | $599/month ($5,988/yr) | 30 included, scalable to 5,000 | Unlimited team members |
| Enterprise | Custom | Thousands | Dedicated account manager, real-time webhooks, advanced security |

Pricing note: "You pay only for active profiles." At scale, per-profile cost falls — enterprise
can reach ~$1/profile/month.

For Edlintics (one operator, own channels only): the Premium tier at $149/month covers the use
case if the single-brand limit applies cleanly. The CMO should verify that "1 social profile"
means one brand's connected accounts (TikTok + IG + YT + FB counted as one profile) vs one
individual platform account.

#### MCP server and SDK
Ayrshare ships an official MCP server documented at https://www.ayrshare.com/docs/additional/mcp-server
(accessed 2026-06-23). The official page serves a read-only documentation-search MCP. A separate
"Action MCP" for executing API calls also exists. There is also a community FastMCP server
(github.com/vanman2024/ayrshare-mcp) with 75+ tools covering all 15 API categories, built by a
third party. Composio hosts an additional MCP integration. Multiple integration paths exist;
the Action MCP appears to be the one needed for an agent-driven control plane.

Source: https://www.ayrshare.com/docs/additional/mcp-server (accessed 2026-06-23);
https://github.com/vanman2024/ayrshare-mcp (accessed 2026-06-23)

---

### 2.2 Postiz

**GitHub:** https://github.com/gitroomhq/postiz-app (accessed 2026-06-23)
**MCP page:** https://postiz.com/mcp (accessed 2026-06-23)
**Agent CLI:** https://github.com/gitroomhq/postiz-agent (accessed 2026-06-23)
**Pricing:** https://postiz.com/pricing (accessed 2026-06-23)
**TikTok provider docs:** https://docs.postiz.com/providers/tiktok (accessed 2026-06-23)

#### Is it genuinely self-hostable?
Yes. The repository provides Docker and docker-compose configurations. The tech stack is:
Next.js (frontend), NestJS (backend), Prisma + PostgreSQL, Temporal (workflow engine), Resend
(email). The documentation states "there is no difference between the hosted version and the
self-hosted version." A single Docker host is sufficient for single-operator use.

Deployment platforms with documented one-click templates include Railway, Coolify, Hetzner, AWS,
Azure, GCP.

Source: https://github.com/gitroomhq/postiz-app (accessed 2026-06-23);
https://railway.com/deploy/deploy-postiz (accessed 2026-06-23)

#### License
AGPL-3.0. This means the software can be used and self-hosted freely, but if you modify and
expose it as a service, you must release modifications. For a single-operator internal control
plane (not a service sold to third parties), AGPL-3.0 is permissive enough in practice — but the
CMO should note this for Hoang's review.

Source: https://github.com/gitroomhq/postiz-app (accessed 2026-06-23)

#### Platform coverage
Instagram, YouTube, TikTok, LinkedIn, Facebook, Pinterest, Threads, X, Bluesky, Mastodon,
Discord, Slack, Reddit, Dribbble, and more — 30+ platforms total as documented.

Source: https://github.com/gitroomhq/postiz-app (accessed 2026-06-23)

#### Does self-hosted Postiz handle platform app-review?
No. This is the critical limitation of the self-hosted path. Self-hosted Postiz requires the
operator to provide their own OAuth developer app credentials per platform in Settings > Providers.
This means:
- TikTok: operator must register their own TikTok developer app, obtain `video.publish` scope
  approval, and pass TikTok's Direct Post Audit before posts can be public. The unaudited
  5-user/private-only restrictions apply to the operator's own app.
- Instagram/Facebook: operator must register a Meta app, obtain `instagram_business_content_publish`
  and related permissions through Meta App Review.
- YouTube: operator's Google Cloud project is subject to the 10,000 unit/day default quota.

Source: https://docs.postiz.com/providers/tiktok (accessed 2026-06-23); GitHub issue #1161
gitroomhq/postiz-app (accessed 2026-06-23)

#### Does the cloud-hosted Postiz (postiz.com) abstract the platform review?
The cloud-hosted version likely uses Postiz's own registered developer apps, which would mean
customers connect their social accounts via OAuth without needing their own developer apps.
However, the TikTok public-posting audit restriction may still apply at the operator level.
This was not confirmed in sources retrieved on 2026-06-23 and is flagged as unverified.

#### MCP server
Postiz ships a native MCP server. It is accessible via a single URL:
`https://api.postiz.com/mcp/<api-key>`. The MCP server is included at no extra cost with any
Postiz account (cloud or self-hosted). It is documented to work with Claude, ChatGPT, Cursor, and
any MCP-compatible AI agent.

For self-hosted instances, the POSTIZ_BASE_URL environment variable points the CLI/MCP to the
operator's own server.

Source: https://postiz.com/mcp (accessed 2026-06-23); https://github.com/gitroomhq/postiz-agent
(accessed 2026-06-23)

#### postiz-agent CLI
An official npm CLI (`npm install -g postiz`) enables AI agents (specifically Claude and
"OpenClaw") to schedule, publish, and manage posts from the command line. Capabilities include:
create/schedule/draft/delete posts, upload media, list integrations, pull analytics, manage
threading (Twitter threads, Reddit replies), and trigger platform-specific dynamic tools (e.g.
fetch YouTube playlists, Reddit flairs). Supports self-hosted instances via POSTIZ_AUTH_SERVER
environment variable.

Source: https://github.com/gitroomhq/postiz-agent (accessed 2026-06-23)

#### Activity level
As of 2026-06-23: v2.21.10 released June 22, 2026 (previous day). 29,839+ GitHub stars, 5,403
forks, 223 open issues. Active development confirmed.

Source: https://github.com/gitroomhq/postiz-app (accessed 2026-06-23)

#### Pricing — cloud hosted

| Plan | Monthly price | Channels | Posts/month | API + Webhooks |
|---|---|---|---|---|
| Standard | $29/month | 5 | 400 | Yes |
| Team | $39/month | 10 | Unlimited | Yes |
| Pro | $49/month | 30 | Unlimited | Yes |
| Ultimate | $99/month | 100 | Unlimited | Yes |

Self-hosted: free (infrastructure cost only). No permanent free cloud tier; 7-day free trial.

Source: https://postiz.com/pricing (accessed 2026-06-23)

#### Rate limits
Postiz API: 30 requests per hour on the cloud-hosted API.

Source: https://github.com/gitroomhq/postiz-agent (accessed 2026-06-23)

---

### 2.3 Metricool

**API guide:** https://tygartmedia.com/metricool-api-guide/ (accessed 2026-06-23)
**Help center API:** https://help.metricool.com/en/category/api-integrations-dc0snw/ (accessed 2026-06-23)

#### Platform coverage for publishing
LinkedIn, Facebook, Instagram, X/Twitter, Google Business Profile, TikTok, YouTube, Pinterest,
Threads, Bluesky — 10+ platforms. Direct publishing via API (`autoPublish: true`) is supported.

#### Does it handle platform app-review burden?
Not separately documented. Metricool is primarily an end-user SaaS tool, not an infrastructure
API layer. Users connect their own social accounts via Metricool's UI and Metricool's own
registered developer apps handle the OAuth flow. For an AI-agent control plane wrapping, this
is a softer API surface than Ayrshare.

#### API quality
- REST API with token-based authentication (X-Mc-Auth header, userId + blogId query params).
- Full CRUD on scheduled posts across all supported platforms; auto-publish flag supported.
- Rate limits not publicly documented; community guidance suggests a 1-second delay between
  calls prevents throttling at typical volumes.
- Official API documentation as a PDF: https://static.metricool.com/API+DOC/API+English.pdf
  Interactive docs: https://app.metricool.com/resources/apidocs/index.html

#### Plan requirement
API access requires the Advanced plan or above. Pricing for Advanced starts at approximately
$53/month on annual billing as of 2026.

Source: https://checkthat.ai/brands/metricool/pricing (accessed 2026-06-23)

#### MCP and CLI
No dedicated MCP server or CLI from Metricool was found. Integrations are via Zapier, Make.com,
and a Metricool-specific node for Make. One source mentioned an MCP server for Metricool but
this was not confirmed by primary sources; flagged as unverified.

#### Summary assessment
Metricool is a capable analytics + scheduling tool for manual/semi-automated workflows. It is not
designed as a headless infrastructure API layer. Its API docs are less developer-forward than
Ayrshare's. The undisclosed rate limit and PDF-only docs are weaknesses for a programmatic control
plane.

---

### 2.4 Buffer

**Developer API:** https://buffer.com/developer-api (accessed 2026-06-23)

#### Platform coverage
Instagram, TikTok, YouTube, LinkedIn, X, Facebook, Pinterest, Threads, Bluesky, Mastodon, Google
Business Profile — 11 platforms. Buffer is an official API partner with all four target platforms.

#### API type and quality
- GraphQL API (not REST). Currently in beta.
- Supports: post creation, scheduling, content ideas, channel management, account metadata.
- Analytics and community/inbox features are on the roadmap but not available as of 2026-06-23.
- Rate limits per API key: 100 requests/15-min window (all plans); 24-hour limits vary by plan
  (100 Free, 250 Essentials, 500 Team); 30-day limits (3,000 Free, 7,500 Essentials, 15,000 Team).

Source: https://buffer.com/developer-api (accessed 2026-06-23)

#### Plan requirement and pricing
API access is available on all plans including Free. Pricing:
- Free: 1 API key, 1 OAuth client.
- Essentials: 3 keys, 3 clients (pricing not confirmed on 2026-06-23 from primary source).
- Team: 5 keys, 5 clients.

Partners can contact Buffer for higher rate limits.

#### Does it handle platform app-review burden?
Likely yes for Instagram/Facebook (Buffer is an official Meta partner). TikTok public posting
audit status unclear.

#### Summary assessment
Buffer's developer API is the most accessible entry point (free tier exists) but is explicitly
in beta, GraphQL-only (adds client complexity), and currently missing analytics pull. It is more
appropriate as a scheduling layer for human-operated workflows than as a headless AI-agent
infrastructure layer. For wrapping behind a custom control plane, it is the weakest option of
the four evaluated here.

---

## Strand 3 — MCP servers and CLIs

| Provider | MCP server | CLI | Notes |
|---|---|---|---|
| Ayrshare | Yes — official (docs-search MCP at ayrshare.com/docs/mcp) + Action MCP for API execution; also a community FastMCP server with 75+ tools | No official CLI found | Action MCP needed for agent control plane; docs-only MCP is read-only |
| Postiz | Yes — native, built-in, included at no extra cost; single URL endpoint; works with self-hosted instances | Yes — postiz-agent CLI (npm install -g postiz), purpose-built for Claude and AI agents | The most complete AI-agent-native stack; self-hosted POSTIZ_BASE_URL wires it to own server |
| Metricool | Not confirmed by primary sources | No | Make.com and Zapier integrations only; not headless-agent-native |
| Buffer | No official MCP or CLI | No | No-code integrations (IFTTT, Make, Zapier) only; developer API is GraphQL beta |

Source: https://www.ayrshare.com/docs/additional/mcp-server (accessed 2026-06-23);
https://postiz.com/mcp (accessed 2026-06-23); https://github.com/gitroomhq/postiz-agent
(accessed 2026-06-23); https://lobehub.com/mcp/antoniolg-postiz-mcp (accessed 2026-06-23)

---

## Summary comparison table

| Dimension | DIY direct APIs | Ayrshare | Postiz (self-hosted) | Postiz (cloud) | Metricool | Buffer |
|---|---|---|---|---|---|---|
| **TikTok coverage** | Yes, post-audit | Yes | Yes, post-audit (own app) | Likely yes [UNVERIFIED] | Yes | Yes |
| **Instagram coverage** | Yes, post-review | Yes | Yes, post-review (own app) | Likely yes | Yes | Yes |
| **YouTube coverage** | Yes, post-quota-approval | Yes | Yes (own GCloud quota) | Yes | Yes | Yes (beta) |
| **Facebook coverage** | Yes, post-review | Yes | Yes, post-review (own app) | Likely yes | Yes | Yes |
| **Platform app-review absorbed by provider** | N/A — fully on operator | Likely yes for Meta; TikTok audit status UNVERIFIED | No — operator registers own apps | Likely yes [UNVERIFIED] | Likely yes for Meta | Likely yes (official partner) |
| **MCP server** | None (build own) | Yes — official + community | Yes — native, included | Yes — native, included | Not confirmed | No |
| **CLI for AI agents** | Build own | No official CLI | Yes — postiz-agent | Yes — postiz-agent | No | No |
| **Pricing (operator, single brand)** | Dev time + maintenance only | $149/month | $0 + infra (~$5–20/month on Hetzner) | $29/month (Standard) | ~$53/month (Advanced) | $0 (Free plan) |
| **Analytics pull via API** | Per-platform (build each) | Yes — all platforms | Yes — all platforms | Yes — all platforms | Yes (Advanced+) | Not yet (roadmap) |
| **Self-hostable** | N/A | No | Yes (AGPL-3.0) | N/A | No | No |
| **License** | N/A | Commercial SaaS | AGPL-3.0 | Commercial SaaS | Commercial SaaS | Commercial SaaS |
| **Time-to-first-public-post** | 4–12 weeks (gating) | Days to 2 weeks (onboarding + OAuth) | 4–12 weeks (same platform gating as DIY) | Days [UNVERIFIED] | Days | Days |
| **Ongoing maintenance burden** | High (API versioning, token refresh, quota, deprecations across 4 platforms) | Low (Ayrshare absorbs) | Medium (platform OAuth + own infra) | Low | Low | Low |

---

## What I could not verify

1. **Whether Ayrshare uses a shared audited TikTok developer app that lets customers post publicly
   without their own TikTok audit.** This is the most important open question. Ayrshare's public
   blog implies they abstract the integration but does not confirm audit status on the customer's
   behalf. Multiple third-party sources suggest the TikTok audit is still required "on your
   account." Recommend: email Ayrshare support directly (support@ayrshare.com) before strategy call.

2. **Whether cloud-hosted Postiz (postiz.com) absorbs the TikTok audit and Meta app review on
   behalf of customers.** The cloud-hosted version likely uses Postiz's own registered apps, but
   TikTok's per-app audit could still restrict posting to private. Not confirmed on 2026-06-23.

3. **Ayrshare's definition of "1 social profile" on the Premium plan.** It is unclear whether
   one profile means one connected channel (e.g. one TikTok account) or one brand (e.g. all
   of Edlintics' connected accounts across TikTok, Instagram, YouTube, Facebook). This determines
   whether Premium ($149/month) is the right tier or Launch ($299/month) is needed.

4. **Postiz API rate limit for self-hosted instances.** The 30 requests/hour figure is confirmed
   for the cloud API. For self-hosted, no published limit was found; it may be uncapped or
   set in configuration.

5. **Metricool MCP server.** One search result referenced a Metricool MCP server but this was not
   confirmed by primary Metricool documentation on 2026-06-23.

6. **Buffer's roadmap timeline for analytics pull via API.** Listed as "upcoming" but no date
   given.

7. **TikTok's "15 posts per day per creator" shared-quota claim.** Sourced from a third-party
   guide (postproxy.dev), not from TikTok's official documentation. Should be treated as
   directionally accurate but not precise.

---

## Sources

- https://developers.tiktok.com/products/content-posting-api/ — TikTok Content Posting API product page
- https://developers.tiktok.com/doc/content-posting-api-get-started — TikTok Content Posting API get-started
- https://developers.tiktok.com/doc/content-sharing-guidelines — TikTok content sharing guidelines
- https://zernio.com/blog/tiktok-developer-api — TikTok developer API guide 2026
- https://postproxy.dev/blog/how-to-post-to-tiktok-via-api/ — TikTok API posting guide 2026
- https://postproxy.dev/blog/social-media-platform-api-rules-rate-limits-media-specs/ — cross-platform rate limits 2026
- https://www.postpeer.dev/blog/best-tiktok-posting-api — TikTok API provider comparison 2026
- https://docs.mixpost.app/services/social/tik-tok/direct-post-audit/ — TikTok Direct Post Audit requirements
- https://developers.facebook.com/docs/instagram-platform/overview/ — Meta Instagram Platform overview
- https://developers.facebook.com/docs/graph-api/overview/rate-limiting/ — Meta Graph API rate limits
- https://www.getphyllo.com/post/instagram-api-integration-101-for-developers-of-the-creator-economy — Instagram API integration guide 2026
- https://zernio.com/blog/instagram-graph-api — Instagram Graph API open questions 2026
- https://postproxy.dev/blog/instagram-reels-api-publishing-guide/ — Instagram Reels API guide 2026
- https://storrito.com/resources/instagram-api-2026/ — Instagram API changes 2026
- https://posteverywhere.ai/blog/post-to-facebook-api — Facebook page publishing via API 2026
- https://zernio.com/blog/facebook-api — Facebook API guide 2026
- https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits — YouTube API quota and compliance audits
- https://www.getphyllo.com/post/youtube-api-limits-how-to-calculate-api-usage-cost-and-fix-exceeded-api-quota — YouTube API limits 2026
- https://codivupload.com/blog/youtube-api-quota — YouTube API quota 2026
- https://www.getphyllo.com/post/is-the-youtube-api-free-costs-limits-iv — YouTube API pricing 2026
- https://www.ayrshare.com/pricing/ — Ayrshare pricing (accessed 2026-06-23)
- https://www.ayrshare.com/docs/whatsnew/latest — Ayrshare changelog (accessed 2026-06-23)
- https://www.ayrshare.com/introducing-tiktok-direct-publishing-analytics-and-commenting/ — Ayrshare TikTok blog post
- https://www.ayrshare.com/blog/tiktok-api-how-to-post-and-get-analytics/ — Ayrshare TikTok API guide
- https://www.ayrshare.com/docs/additional/mcp-server — Ayrshare MCP server documentation
- https://github.com/ayrshare/social-media-api — Ayrshare SDK GitHub
- https://github.com/vanman2024/ayrshare-mcp — Community FastMCP server for Ayrshare
- https://github.com/gitroomhq/postiz-app — Postiz GitHub repository
- https://github.com/gitroomhq/postiz-agent — Postiz agent CLI GitHub
- https://postiz.com/mcp — Postiz MCP server page
- https://postiz.com/pricing — Postiz pricing (accessed 2026-06-23)
- https://docs.postiz.com/providers/tiktok — Postiz TikTok provider documentation
- https://railway.com/deploy/deploy-postiz — Postiz Railway deployment template
- https://tygartmedia.com/metricool-api-guide/ — Metricool API guide
- https://help.metricool.com/en/category/api-integrations-dc0snw/ — Metricool API help center
- https://checkthat.ai/brands/metricool/pricing — Metricool pricing 2026
- https://buffer.com/developer-api — Buffer developer API page
- https://lobehub.com/mcp/antoniolg-postiz-mcp — Postiz MCP on LobeHub
