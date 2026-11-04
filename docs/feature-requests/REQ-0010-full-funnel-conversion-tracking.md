# REQ-0010  ·  Full-funnel conversion tracking for Meta, GA4 and Google Ads

- **Status:** spec drafted by tutoring-web (feature FT, `docs/specs/conversion-tracking/`, commit 7a829ebda on feat/ft-conversion-tracking); build waits for Hoang's sign-off of decisions D1-D12
- **Date:** 2026-11-04
- **Source:** Hoang ("set that up properly so every campaign can track proper funnel sale and conversion. Work with the CTO on the Meta Conversions API setup and the Google Analytics/Ads event setup")
- **Targets metric:** paid acquisition: cost per booking, cost per purchase and return on ad spend (ROAS) per campaign and per ad, on Meta and Google
- **Priority (CMO view):** high. The tutoring Meta campaign is about to run and course ads follow; today no sale can be tied to the campaign or ad that brought it
- **Effort guess (CMO, non-binding):** L (schema, consent, server events, a new Google sink, a reporting endpoint)
- **Builds on:** REQ-0009 (Meta Pixel and CAPI, live on prod 4 Nov 2026 with PR #102), REQ-0003 (waitlist UTMs), REQ-0006 (short links)

## Summary
Every ad platform reports clicks, but none of our sales can be tied back to a campaign. The tutoring-web event inventory (4 Nov 2026) shows five gaps:
1. **UTMs and click IDs are not kept.** `lib/attribution.ts` reads UTMs from the current URL only. Orders and bookings have no UTM or click-ID columns, so a visitor who browses one page before booking is unattributed. This is the biggest blocker
2. **No Google Ads tracking at all.** There is no AW- tag, no conversion action and no enhanced conversions, and gclid, gbraid and wbraid are never captured
3. **GA4 purchase is browser-only.** There is no Measurement Protocol, so an ad blocker or a closed tab loses the sale. `user_id` is not sent, and bookings use a custom `booking` event that is not set up as a key event
4. **Google Consent Mode v2 is missing.** GA is hard-gated, which is compliant, but Google Ads cannot use the consent signals it now requires in the EEA (`ad_user_data`, `ad_personalization`)
5. **Marketing cannot read sales per campaign.** `/api/v1/marketing` has waitlist and email stats but no purchases or bookings by `utm_campaign` and `utm_content`

## Proposal
One funnel and one set of event names, sent to every sink that the visitor has consented to. Each sale is stored with the campaign and ad that brought it. Server-side copies of the money events go to Meta and Google, so ad blockers do not lose them. Marketing gets one read-only endpoint to report revenue per campaign and per ad.

## Proposed requirements (the CTO owns the final design)

### 1. Attribution capture and storage (the core)
- On every landing, capture `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`, `ref`, the click IDs `fbclid`, `gclid`, `gbraid` and `wbraid`, the landing path and `document.referrer` (host only)
- Persist them in a first-party cookie with **first touch** (never overwritten) and **last touch** (overwritten by any new UTM or click ID), with a 90-day lifetime. The cookie lives under the `marketing` consent purpose. Without consent, keep the values for the current session only, in memory or sessionStorage, so that a same-session order is still attributed. The CTO and security review decide whether session-only storage without consent is acceptable
- Store both touches on **Order** and **Booking** (and keep `SignupAttribution`): source, medium, campaign, content, term, click-ID type and value, landing path and touch time. Schema change, `cto` lane only
- Private paths keep being redacted as now

### 2. One funnel, the same names everywhere
| Funnel step | Product event | GA4 | Meta | Google Ads conversion |
|---|---|---|---|---|
| Landing | page view | `page_view` | PageView | none |
| Product view | course.viewed / tutor_viewed | `view_item` | ViewContent | none |
| Lead | waitlist_joined, brief_signup, waitlist_signup | `generate_lead` (lead_type) | Lead (**add the course waitlist**, missing today) | Lead (secondary) |
| Sign-up | signup_completed (**all methods, including Google OAuth**) | `sign_up` | CompleteRegistration | Sign-up (secondary) |
| Add to cart | add_to_cart_clicked, tutor_slot_added | `add_to_cart` | AddToCart | none |
| Checkout | checkout_started | `begin_checkout` | InitiateCheckout | Begin checkout (secondary) |
| Booking | booking_completed | **`purchase` with `item_category: tutoring`** (or a key event `book_appointment`; CTO's call), value and currency EUR | Schedule (+ CAPI) | **Booking (primary)** |
| Purchase | purchase_completed | `purchase` (transaction_id = orderId) | Purchase (+ CAPI) | **Purchase (primary)** |
| Abandoned at Stripe | new: checkout_abandoned (Stripe session expired) | `checkout_abandoned` (custom) | none | none |

- `content_ids` and `item_id` stay stable: the course slug, `tutoring-1to1` or `tutoring-group`
- `value` is always the net paid amount in EUR. Paid tutoring bookings carry their value, so tutoring ROAS can be measured

### 2b. Custom events (Hoang, 4 Nov 2026: "we should create custom events tracking as well")
The standard events above cover the big steps. Custom events cover the small steps between them. They show where an ad's visitors drop off, and they give Meta and Google an earlier signal to optimise for while sales are still few (Meta needs about 50 conversions a week per ad set). Each one shall be sent to PostHog and GA4 (custom event, parameters registered as custom dimensions), and the ones marked **M** to Meta as a custom event (`fbq('trackCustom', …)`, also usable for custom conversions and retargeting audiences). All of them follow the same consent rules as the rest.

| Custom event | Trigger | Key parameters | M |
|---|---|---|---|
| `cta_click` | any primary CTA (Book, Start, Join waitlist) | `cta_id`, `location` (hero, sticky, pricing, footer), `page_type` | |
| `pricing_viewed` | price block or pricing section is 50% in view | `product` (tutoring-1to1, course slug), `price_shown` | M |
| `booking_calendar_opened` | the tutor booking calendar opens | `tutor`, `source` (ad, profile, course page) | M |
| `slot_selected` | a time slot is picked (before add to cart) | `tutor`, `days_ahead`, `session_length` | M |
| `booking_form_started` | first field of the booking/checkout details touched | `product` | |
| `lesson_preview_started` | a free/preview lesson opens | `course`, `lesson` | M |
| `lesson_preview_completed` | the preview lesson reaches its end | `course`, `lesson`, `seconds` | M |
| `exercise_attempted` | first answer submitted on a free exercise or puzzle | `course` or `puzzle_id`, `correct` | |
| `video_progress` | tutor intro or lesson video reaches 25 / 50 / 75 / 100% | `video_id`, `percent` | |
| `scroll_depth` | 50% and 90% of tutor and course pages | `page_type`, `percent` | |
| `faq_opened` | an FAQ item expands | `question_id`, `page_type` | |
| `contact_click` | email / WhatsApp / message tutor click | `channel`, `location` | M |
| `outbound_click` | link to another domain | `host` | |
| `engaged_visit` | 45 s active on a tutor or course page plus a scroll past 50% (fires once per session) | `page_type`, `product` | M |

**Both product lines (Hoang, 4 Nov 2026: "for both the courses in the future and tutoring").** Every standard and custom event shall carry `product_line` (`tutoring` or `course`) and `product_id` (`tutoring-1to1`, `tutoring-group` or the course slug), so each funnel can be read on its own and new courses need no new tracking work. Funnel-specific additions:

| Product line | Custom event | Trigger | M |
|---|---|---|---|
| Tutoring | `tutor_profile_viewed` | tutor profile page (with `tutor`, `source`) | M |
| Tutoring | `booking_calendar_opened`, `slot_selected` | as above | M |
| Tutoring | `session_rebooked` | a second or later paid booking by the same student (server) | M |
| Course | `syllabus_viewed` | course outline section in view or expanded | M |
| Course | `lesson_preview_started` / `_completed` | as above | M |
| Course | `course_started` | first lesson opened after purchase or enrolment (server) | |
| Course | `course_progress` | 25 / 50 / 75% of lessons completed (server) | |
| Course | `course_completed` | already a server event in PostHog; mirror to GA4 | M |
| Both | `waitlist_joined` | coming-soon course waitlist, or the tutoring waitlist if one exists | M |

- The post-purchase events (`session_rebooked`, `course_started`, `course_progress`, `course_completed`) measure which campaigns bring students who stay, not just buyers. They are joined to the order's stored first- and last-touch campaign, so the read endpoint (requirement 6) can report repeat bookings and completion per campaign
- `engaged_visit` is a strong early optimisation signal for Meta (a custom conversion) while bookings are scarce. The CTO can tune its exact rule
- Every custom event carries the last-touch `utm_campaign`, `utm_content` and the click-ID type from requirement 1, so drop-off can be compared per ad
- The names and parameters live in one typed registry (as `lib/ga-events.ts` and `lib/meta-events.ts` already do), so a new event cannot be sent to one sink and missed in another
- No personal data in parameters. Private paths stay redacted

### 3. Server-side money events
- **GA4 Measurement Protocol** for `purchase` (and the booking event), sent from the Stripe webhook or Inngest with the same `transaction_id` and the visitor's `client_id` (`_ga`) captured at checkout. Server and browser are de-duplicated by `transaction_id` (GA dedupes purchases with the same id). Send only when analytics consent was given at checkout
- **Meta CAPI**: already live for Purchase and Schedule. Add Lead (course waitlist) and CompleteRegistration if cheap
- **Google Ads offline / enhanced conversions** (see 4)

### 4. Google Ads sink (new, under the `marketing` purpose)
**Phase 2 (Hoang, 4 Nov 2026: Google Ads is planned for the future, no account yet).** Phase 1 still builds what keeps Google ready: click-ID capture (`gclid`, `gbraid`, `wbraid`) and storage on orders and bookings (requirement 1), Consent Mode v2 (requirement 5), GA4 key events and the GA4 Measurement Protocol, so past sales can be uploaded as conversions later. The tag and conversion actions below are built when Hoang opens the account
- Load the Google tag with the Ads ID (`AW-…`, from an env var) through the same consent-gated loader. Linker and auto-tagging so `gclid` lands in the URL
- **Conversion actions:** Purchase and Booking as primary (value in EUR, transaction_id for dedupe); Lead, Sign-up and Begin checkout as secondary. Import them from GA4 key events or tag them directly (the CTO decides; direct tags with enhanced conversions are more accurate)
- **Enhanced conversions:** a SHA-256 hashed email (and phone when present) on Purchase and Booking, only with `marketing` consent
- **Server-side upload** (Google Ads API offline conversion import with `gclid`, `gbraid` or `wbraid` from the stored attribution) can come in phase 2
- Privacy and cookie pages: add Google as a recipient for ads measurement and list the `_gcl_*` cookies. Update the cookie audit script

### 5. Google Consent Mode v2
- Before any Google tag runs: `gtag('consent','default', {analytics_storage, ad_storage, ad_user_data, ad_personalization: 'denied', wait_for_update: 500})`
- On choice: `update` with analytics_storage set from the `analytics` purpose, and the other three set from the `marketing` purpose
- Keep hard gating as it is (basic mode). Advanced mode (cookieless pings) is a legal decision for Hoang and is not assumed here

### 6. Marketing read endpoint
- `GET /api/v1/marketing/conversions?from&to&groupBy=day,product_line,product_id,utm_source,utm_campaign,utm_content&touch=last|first`, returning per group: orders, bookings, revenue (EUR), sign-ups, leads, repeat bookings and course completions. Aggregates only, no personal data, behind the existing marketing API key
- The hub Ads tab and the daily ads refresh (`docs/content-workflow/performance-review.md`) read it to fill `bookings` and revenue per ad, replacing the current `null`

### 7. UTM convention (marketing owns this; the site only stores what arrives)
- `utm_source`: meta, google, linkedin, newsletter, organic platform names
- `utm_medium`: paid, social, email, referral
- `utm_campaign`: `<product>-<yyyy-mm>`, e.g. `tutoring-2026-11` or `course-fa-2026-12`
- `utm_content`: the creative id, e.g. `video`, `video-price`, `static-photo-price`
- `utm_term`: the keyword (Google Search) or the audience name
- Meta ads may use dynamic values (`{{ad.name}}`); Google uses auto-tagging plus the same UTMs

### 8. Bugs to fix before scaling spend
- Signed-out cart checkout shows "Something went wrong starting checkout" instead of a sign-in redirect (pre-existing, offered to Hoang)
- Make sure Google OAuth sign-ups fire `signup_completed`

## What Hoang does (outside the code)
1. **Google Ads (later):** when Hoang opens the account, give its ID and link it to GA4 property 263808863. Until then phase 1 runs without it
2. In Google Ads: turn on auto-tagging, accept the enhanced conversions terms, and create the conversion actions the spec names (or let the CTO/CMO do it with his OK)
3. Meta: run the MP022 test purchase (browser + server dedupe), rotate `META_CAPI_ACCESS_TOKEN`, accept the Business Tools Terms, add `NEXT_PUBLIC_META_PIXEL_ID` to Preview
4. Approve the privacy and cookie page wording for Google Ads

## Success signal
For any campaign, one hub row shows spend (from the ad platform) next to bookings, purchases and revenue (from our own DB through the endpoint), split by `utm_content`. Meta Events Manager and Google Ads show Purchase and Booking from browser and server, de-duplicated. GA4 shows `purchase` revenue matching Stripe within 5% for consented visitors

## Out-of-scope check
Marketing never imports app code: it reads `/api/v1` and the ad platforms only. No product catalog or feed. No cross-device identity graph. Session replay is out of scope

## Platform audit (read-only, 4 Nov 2026)
Read only. Nothing was changed. Figures are for 7 Oct to 3 Nov 2026

**Meta (dataset 1000075088350707)**
- Only **PageView** arrives (2 events, Pixel + Conversions API, Event Match Quality 6.1). No Lead, CompleteRegistration, InitiateCheckout, Schedule or Purchase yet (expected: #102 went live today and the MP022 test purchase has not run)
- **Automatic advanced matching is Off** in Settings, although REQ-0009 assumed it was on. Hoang to turn it on (email, phone, name), since the code relies on it
- **Conversions API shows "Web-only, Business connected", opted in 29 Oct from Events Manager.** This looks like Meta's no-code web CAPI, separate from our server CAPI in #102. CTO to confirm the two do not double-count Purchase and Schedule (event_id dedupe), and decide whether to keep the no-code one
- Used by 0 ad sets and 0 audiences; dataset category None; no custom conversions; domain edlintics.com Verified; allowlist edlintics.com added 4 Nov; first-party cookies On; "Measure conversions on customer devices" starts 12 Nov (On)
- Shared with ad accounts 535582635765592 (Edlintics) and 1811051243039603 ("TK 1"). Hoang to check whether TK 1 should keep access

**GA4 (property 263808863 "Website", G-KT16RP1WLE, account 190808750)**
- 28 days: 266 events, 19 users, 34 sessions. Events seen: page_view, session_start, scroll, user_engagement, first_visit, view_item_list (2) and view_item (1). **No** add_to_cart, begin_checkout, sign_up, generate_lead or purchase
- Key events: `purchase` and a legacy `ads_conversion_Book_appointment_1`, both "No stream data". €0 revenue
- **App and admin traffic pollutes the property.** The top page is the course "Cockpit" (65 views in 7 days), plus Admin and Sign-in pages. Requirement: exclude admin and app routes from GA page views (or tag `page_type` and filter), and define internal traffic (Hoang, staff, agents) as a data filter
- **`accounts.google.com / referral` is the top source (12 of 34 sessions).** These are Google sign-in redirects. Requirement: add unwanted referrals for `accounts.google.com` and `checkout.stripe.com`, so sign-in and payment do not steal the ad's attribution
- Consent signals for analytics_storage, ad_storage, ad_user_data and ad_personalization are all **inactive**, which confirms Consent Mode v2 is missing
- Google signals Off, user-provided data collection Off, Enhanced measurement on (form interactions off). Attribution is data-driven, with 30 / 90-day windows
- One Measurement Protocol secret already exists ("Squarespace scheduling", 2022). The CTO should create a fresh secret for the server-side purchase and booking events; Hoang can then revoke the old one
- The UTMs work: campaign `tutoring-2026-11` shows 4 meta/paid sessions and `explainer-reel` 2
- Old property 405129152: no data in 48 hours (switched off as planned)

**Google Ads**
- No live account. 622-861-8576 (linked to GA4) is Closed, 116-786-5935 is Closed, and 393-090-6286 is Cancelled with outstanding charges shown. Phase 2 starts with a new account or a reopened one. Hoang to settle or ignore the old one's balance notice himself
- GA4 still links to the closed 622-861-8576. Unlink it when the new account is linked

## Decision log
- 2026-11-04 — requested by Hoang; tutoring-web supplied the event inventory from main at 67adbdaf (PR #102 live on prod 4 Nov); CMO drafted this request
- 2026-11-04 — tutoring-web drafted the FT spec (36 tasks, 12 decisions for Hoang). CMO review: agreed with all 12 defaults; asked for a ready Phase 2 list (Google Ads 622-861-8576, edlintics@gmail.com, closed, Hoang plans to reactivate; keep its GA4 link), a test path given staff exclusion (a non-staff test account Hoang creates, FT097), groupBy utm_term and click_id_type, and pricing_viewed + booking_calendar_opened in the first batch (FT029). All four accepted in 7a829ebda
