# REQ-0007  ·  Early-bird free access for new sign-ups (financial accounting course)

- **Status:** proposed (Hoang asked for it, 29 Oct 2026; offer terms still open)
- **Date:** 2026-10-29
- **Source:** Hoang ("the post should lead users to the platform so they can sign up, and sign up for the early bird deal of free access"; "the CTO needs to set up that system")
- **Targets metric:** acquisition (sign-ups from social), then activation (course started) and the V1 validation target (paying customers)
- **Priority (CMO view):** high, needed before the financial accounting course opens (about 5 Nov 2026)
- **Effort guess (CMO, non-binding):** M

## Summary
The financial accounting course is ready in about a week. Social posts will send people to `edlintics.com/en/sign-up` (live on prod, checked 29 Oct) with the promise of early-bird free access. Today a new account gets nothing special, so the promise can't be kept automatically. The waitlist page (`/en/waitlist`, REQ-0003) still returns 404 on prod, so sign-up replaces it as the CTA

Evidence: 7,243 views in the last 7 days across 7 platforms, 0 new followers, 0 comments from others. Attention exists but nothing turns it into an account. A concrete, honest reason to sign up now is the missing step

## Proposed requirements (CTO owns the final design)
- An account created during the early-bird window shall get free access to the financial accounting course automatically, with no code to type
- The offer terms shall be settings an admin can change without a deploy, because Hoang has not fixed them yet: course(s) covered, window start and end date, an optional cap (first N accounts), and access length (lifetime or N days)
- The sign-up page and the course page shall show the offer while it runs (a short banner: what you get, until when) and hide it when the window closes or the cap is reached
- After sign-up the user shall land on the course (or see a clear "Your free access is active" message), so the promise is visible at once
- Each early-bird grant shall be recorded with the sign-up source: UTM parameters or `ref`, plus the `/go/<code>` from REQ-0006 if that exists by then
- `/api/v1` shall expose daily counts for marketing: sign-ups, early-bird grants, and course starts, split by source/platform. Counts only, no personal data
- When the window closes, accounts that already have free access shall keep it on the stated terms. Nothing is taken back
- Accounts that existed before the window: Hoang decides whether they qualify (a setting is enough)

## Success signal
Sign-ups per platform become readable in the daily metrics refresh, and the posts' CTA ("sign up free and get early-bird access") is true for every visitor who acts on it. Later: how many early-bird users start lessons and how many convert at €99

## Out-of-scope check
Not a subscription, not gamification, not a certificate: it is a time-boxed free grant of an existing paid course. Marketing reads results only through `/api/v1` and never imports app code. Any schema change stays in the CTO lane (serial schema rule). Related: REQ-0003 (waitlist with UTM), REQ-0006 (owned short links)

## Open decisions (Hoang)
1. What free access covers: the whole financial accounting course, or the first lessons
2. Access length: lifetime, or a fixed number of days
3. Who qualifies: everyone who signs up before a date (which), or the first N accounts
4. Whether existing accounts qualify
5. Which currency posts show if a price is mentioned (posts use USD; the course is priced at €99)

## Decision log
- 2026-10-29 — written by CMO at Hoang's request; Hoang confirmed the CTO must build it. Terms open (see above)
- _(Hoang / CTO: approve / defer / reject + reason here.)_
