# REQ-0008  ·  Course prelaunch mode (first use: Financial Accounting - Part 1)

- **Status:** proposed (Hoang asked for it, 29 Oct 2026)
- **Date:** 2026-10-29
- **Source:** Hoang ("we need to edit the course to coming soon for Financial Accounting Part 1 and users can sign up; propose a feature that we can prelaunch like this")
- **Targets metric:** acquisition (accounts created from social), prelaunch demand per course, then conversion at launch
- **Priority (CMO view):** high, the course is ready in about a week
- **Effort guess (CMO, non-binding):** M (builds on what exists)
- **Works with:** REQ-0007 (early-bird free access), REQ-0006 (owned short links), REQ-0003 (waitlist)

## What exists today (checked on prod 29 Oct)
`edlintics.com/en/courses/financial-accounting-part-1` shows "Coming soon", an email-only box ("Be first to know", "Notify me at launch", one email on launch day) and the full curriculum with "Unlocks with purchase". Every course except Managerial Accounting Part 1 shows "Coming soon" on `/en/courses`. Odd value: the Financial Accounting card says "8m Est. study time" for 8 lessons and 64 exercises (data or calculation issue, worth a check)

What is missing for a prelaunch: the email box doesn't create an account, there is no launch date, no reason to act now, nothing to try, and no numbers marketing can read

## Proposal
A per-course **prelaunch** state that sits between "coming soon" and "live", which admins switch on in the course editor. Every future course can reuse it

## Proposed requirements (CTO owns the final design)
- Admins shall set a course's state: coming soon (as today), prelaunch, or live. They can also set a launch date and an optional early-bird offer, linked to REQ-0007's settings
- On a prelaunch course page, the main button shall be "Sign up free and reserve early-bird access" (wording can be edited). It goes to sign-up and returns to the course page. A signed-in user reserves with one click. Keep the email-only "Notify me" as a secondary option, or merge it into the reserve flow
- The page shall show the launch date, what the early bird gets and until when, and the curriculum as today
- One or two lessons (chosen by admins) shall be open as a free preview in prelaunch, so visitors can try the format before launch. The content team picks them in the admin editor
- Reserved users shall get one email or in-app notice on launch day, saying the course is open and their free access is active (if REQ-0007 applies)
- On the courses list, a prelaunch course shall show "Opens <date>" instead of "Coming soon"
- Reservations shall store the sign-up source (UTM, ref, /go code). `/api/v1` shall expose daily counts per course: page views if available, reservations, preview-lesson starts, by source. Counts only, no personal data
- Switching a course to live shall need no data migration: reservations become access grants (REQ-0007) or plain launch notices

## Success signal
For Financial Accounting - Part 1: reservations per day and per platform readable in the marketing daily refresh from the first prelaunch post on. Later, the share of reservers who start the course in week 1 after launch

## Out-of-scope check
No subscription, no gamification, no certificates. Content stays in the admin editor (the COO picks preview lessons there). Marketing reads results only through `/api/v1` and never imports app code. Schema changes stay in the CTO lane

## Open decisions (Hoang)
1. Launch date for Financial Accounting - Part 1
2. Which 1–2 lessons are the free preview (suggest Unit 01 "Accounting - The language of business" and "The Balance Sheet")
3. The early-bird terms (see REQ-0007)

## Decision log
- 2026-10-29 — written by CMO at Hoang's request and relayed to the tutoring-web session
- _(Hoang / CTO: approve / defer / reject + reason here.)_
