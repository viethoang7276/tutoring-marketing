# REQ-0009  ·  Meta Pixel and Conversions API for tutoring and course ads

- **Status:** live on prod since 2026-11-04 09:12 UTC; only PageView received so far (5 Nov); Purchase/Schedule and CAPI unverified until the first consented order (no test purchase, Hoang 5 Nov: wait for the first real customer)
- **Date:** 2026-11-03
- **Source:** Hoang ("we should set meta pixel for tutoring and all the course to track the ads")
- **Targets metric:** paid acquisition (cost per tutoring booking, cost per course purchase, cost per waitlist lead)
- **Priority (CMO view):** high (the tutoring ads campaign is being set up now)
- **Effort guess (CMO, non-binding):** S for the Pixel, M with the Conversions API

## Summary
Hoang is launching Meta ads for tutoring (4 static variants, each with and without the €45/hr price) and later for the courses. Meta can only optimise for bookings and purchases if edlintics.com reports them. There is no Meta Pixel in tutoring-web today (checked 3 Nov 2026: no `fbq`, no pixel ID). Until it exists, the ads run on the Traffic objective (landing page views) and bookings are judged by hand from the `utm_content` split

The site already has a clean event layer: `lib/analytics.ts` events are mapped to GA4 in `lib/ga-events.ts`, consent-gated, with URL redaction for private paths. The Pixel should be one more consumer of the same events, not a parallel tracking setup

## Proposal
Add Meta as a second sink of the existing analytics events, behind the same cookie consent as GA and PostHog, plus a server-side Conversions API (CAPI) call for the money events so they still count when the browser blocks the Pixel

## Proposed requirements (CTO owns the final design)
- **Consent option (new purpose).** Today `lib/consent.ts` has one optional purpose, `analytics`. Meta ad tracking with Advanced Matching is advertising, not analytics, so it needs its own opt-in. Add a second purpose `marketing` (label e.g. "Advertising: measure our ads on Meta"), off by default, as its own toggle in the cookie banner and the footer cookie settings, with Accept all / Reject all still one click. Bump `CONSENT_VERSION` so returning visitors are asked again. GA and PostHog keep using `analytics`; the Meta Pixel and the Conversions API use `marketing` only
- **Automatic Advanced Matching is ON** (Hoang turned it on in Events Manager, 2026-11-03). With it, the Pixel reads email, phone and name fields that visitors type into site forms, hashes them in the browser and sends the hashes to Meta. It shall only run after `marketing` consent (it can, because the Pixel itself only loads after consent). Password, payment and card fields are never read by Meta's matching, but the CTO shall confirm no other sensitive field (e.g. student notes) is named like an email/phone field
- The privacy policy and cookies page shall say, in plain words: Meta Platforms Ireland is a joint controller for ad measurement; with advertising consent the site shares page visits, bookings, purchases and hashed contact details (email, phone, name) with Meta to measure and improve our ads; visitors can withdraw consent at any time in cookie settings; Meta cookies `_fbp` and `_fbc`, up to 90 days. Update the cookie table in the cookies page and the cookie audit script
- The system shall load the Meta Pixel (ID `1000075088350707`, dataset "Edlintics Meta Pixel" created 2026-10-29; from an env var, e.g. `NEXT_PUBLIC_META_PIXEL_ID`) only after the visitor accepts marketing/analytics cookies, and shall clear `_fbp`/`_fbc` cookies when consent is withdrawn (extend `lib/consent-cookies.ts` and the cookie audit)
- The cookies page and privacy policy shall list Meta as a processor
- The system shall send these standard events, mapped from the existing analytics events:

| Existing event | Meta standard event | Parameters |
|---|---|---|
| page view | `PageView` | none |
| course page view / tutor page view | `ViewContent` | content_ids (course slug or `tutoring-1to1`), content_type `product` |
| `cart_item_added`, `tutor_slot_added` | `AddToCart` | value, currency EUR, content_ids |
| `checkout_started` | `InitiateCheckout` | value, currency EUR, num_items |
| `booking_completed` | `Schedule` | sessions, booking_source |
| `purchase_completed` (courses and paid tutoring) | `Purchase` | value, currency EUR, content_ids, content_type `product` |
| `waitlist_signup`, `brief_signup_submitted` | `Lead` | lead_type |
| `signup_completed` | `CompleteRegistration` | none |

- `content_ids` shall be stable: one per course slug and `tutoring-1to1` / `tutoring-group` for tutoring, so ads can be reported per product
- `Purchase` and `Schedule` shall also be sent server-side through the Conversions API (from the Stripe webhook / booking confirmation), with the same `event_id` as the browser event so Meta de-duplicates them. The CAPI access token lives in Vercel env vars only, never in code or logs. Server events only fire for visitors who gave consent (pass the consent state with the order)
- The site shall not add email or name to Pixel event parameters by hand; Advanced Matching handles matching. For CAPI, send SHA-256 hashed email (and `fbp`/`fbc`, client IP and user agent) only for orders made with `marketing` consent, so server events match as well as the browser ones
- Private paths stay redacted as in `sanitizeUrlForGa` (claim, booking links, pay/seat)
- Do not paste Meta's base code snippet into the root layout `<head>` as Meta suggests: it fires PageView before consent. Load `fbevents.js` from the consent-gated analytics loader instead, and keep the `<noscript>` image out (it cannot respect consent)
- Test with Meta Events Manager "Test events" on a preview deploy before production

## What Hoang does (outside the code)
1. Dataset: use "Edlintics Meta Pixel" 1000075088350707 (business 110625140398351), already created 2026-10-29
2. Generate a Conversions API access token for that dataset and put it in Vercel env vars himself (not in chat)
3. Verify the domain edlintics.com in Business Settings › Brand safety › Domains, then set the 8 events priority (Aggregated Event Measurement): Purchase, Schedule, InitiateCheckout, Lead, AddToCart, CompleteRegistration, ViewContent, PageView

## Success signal
Events Manager shows Schedule and Purchase from both browser and server, de-duplicated, within a day of a test booking. The tutoring ad set can then switch from Traffic to Sales, optimised for `Schedule`

## Out-of-scope check
Marketing never imports app code and only reads results in Meta Ads Manager. No product catalog is needed for tutoring: Commerce Manager / catalog ads stay off. Related: REQ-0003 (waitlist UTMs), REQ-0006 (short links), `assets/renders/ads/tutoring-2026-10/ad-copy.md` (switch the ad set to the booking event once this is live)

## Decision log
- 2026-11-03 — requested by Hoang while setting up the tutoring conversion campaign; CMO wrote the request
- 2026-11-03 — Hoang created a second dataset 1054697157584785 by mistake; he chose to keep the original 1000075088350707 (already has the CAPI token in Vercel). The 2026-11-03 dataset is not used. Domain verification tag sent to tutoring-web as a hotfix. Hoang then turned Automatic Advanced Matching on; consent requirements updated to a separate `marketing` purpose
- 2026-11-04 — domain verification tag live on edlintics.com (PR #101); Hoang approved REQ-0009 and tutoring-web is building it (per tutoring-web session). Marketing switches the tutoring ad set to Purchase optimisation once events show on prod
- 2026-11-04 — tutoring-web: Pixel + CAPI built, reviewed, on env-dev; release PR #102 (development → main) open for Hoang. Not live until Hoang sets NEXT_PUBLIC_META_PIXEL_ID on env-dev and prod. Server events deduped by event_id purchase.<orderId> / schedule.<orderId>; content_ids course slugs or tutoring-1to1 / tutoring-group; advertising consent is its own switch, off by default. Known funnel gap: a signed-out visitor checking out from the course cart sees a generic error instead of a sign-in prompt (pre-existing, follow-up with Hoang)
- 2026-11-05 — tutoring-web (Events Manager, 5 Nov): PageView active (8 events, EMQ 6.1, integration "Multiple" = browser Pixel plus probably the no-code connection). No ViewContent, AddToCart, InitiateCheckout, CompleteRegistration, Lead, Schedule or Purchase yet: no consented visitor has done those steps. CAPI needs the rotated META_CAPI_ACCESS_TOKEN (Hoang); dedupe against the no-code connection unverified. Domain verified, diagnostics clean. Next: Hoang's go for test purchase MP022
- 2026-11-05 — Hoang: no test purchase (MP022 dropped); wait for the first real customer. tutoring-web watches Events Manager and tells marketing when Purchase arrives (browser + server, deduped); the ad sets stay on landing page views until then
