# REQ-0003  ·  Course waitlist signup on the home page, protected against bot signups

- **Status:** proposed
- **Date:** 2026-10-25
- **Source:** CMO (pre-launch audience capture), Hoang's request
- **Targets metric:** acquisition (an owned audience to reach on course launch day)
- **Priority (CMO view):** high (every social post from now on points somewhere; today there is nowhere to send people)
- **Effort guess (CMO, non-binding):** S to M

## Summary
The courses are not ready, so social media is building an audience before launch. Followers belong to the platforms and only a small share will see a launch post. A waitlist on edlintics.com gives Edlintics an email list it owns. Hoang's main worry is bot signups, so protection is part of the request, not an extra.

## Evidence (lead with this)
- **Our data:** posts reach 2 to 50 people each across six platforms (daily metrics refresh, 24 to 25 Oct). There is no link destination that captures anyone, and GA plus UTM tagging only starts with the next deploy.
- **Bot risk is real:** a newsletter owner had about 5,000 bot addresses added in one attack. Double opt-in kept them off the active list, but the provider still stored every pending address and sent every confirmation email, which hurts sender reputation. Lesson: protect the signup endpoint itself, and never let the form post straight to the email provider ([flaviocopes.com](https://flaviocopes.com/newsletter-spam-attack)).
- **Layered defence is standard practice:** honeypot field hidden with CSS, minimum time to submit, an invisible challenge (Cloudflare Turnstile or reCAPTCHA), rate limiting, and real-time email validation ([LaunchList docs](https://getlaunchlist.com/help/docs/tips/spam-protection), [Suped](https://suped.com/email-deliverability/answers/what-are-the-best-practices-for-minimizing-bot-signups-on-email-forms), [Elastic Email](https://elasticemail.com/blog/how-to-prevent-bots-from-spamming-your-sign-up-forms)).
- **Vercel option:** Vercel BotID is an invisible check for signup routes on apps deployed on Vercel (`checkBotId()` in the server action). Turnstile may show a checkbox when it detects risk; BotID never does ([Vercel docs](https://vercel.com/docs/botid), [BotID vs Turnstile](https://vercel.com/kb/guide/vercel-botid-vs-cloudflare-turnstile)). Check the current plan and pricing.
- **Conversion:** email-only forms convert best. One source reports about 15% fewer signups for each extra field. The patterns that convert are a specific outcome headline, one call to action above the fold, real social proof (never invented counts), and a referral or early-access perk ([LaunchList examples](https://getlaunchlist.com/blog/waitlist-landing-page-examples-that-convert), [Medium](https://medium.com/@soyzamudio/maximizing-waitlist-conversion-rates-data-driven-strategies-6856cb91f83b)). Vendor blogs, so treat the numbers as rough.

## Hypothesis
We believe that **an email-only course waitlist on the home page, linked from every bio and first comment**, will turn social viewers into **an owned list of a few hundred students before launch**, because a clear perk (weekly puzzle by email and early access or an early-bird price) gives a reason to sign up now.

## Job to be done
"When I like an Edlintics puzzle but the course I need is not out yet, I want to leave my email once, so that I hear the moment it opens and get a puzzle each week in the meantime."

## Proposed requirements (CTO owns the final design)
**Form and placement**
- The home page shall have a waitlist section above the fold with one email field and one button. Optionally there is a "Which course?" choice, but only after signup (on the thank-you step), never on the first form.
- A stable URL such as `/waitlist` (or `/#waitlist`) shall exist so social links can point to it, and it shall keep UTM parameters.
- The thank-you step shall say "check your inbox to confirm" and may offer a share link.
- The copy is about courses and learning business. No tutoring offer, no tutor photo, no personal branding (Hoang's instruction: tutoring is marketed separately).

**Bot protection (all server-side; layers, not one tool)**
- The form posts to our own server action or route, never directly to an email provider.
- An invisible challenge: Vercel BotID (preferred if the plan allows; no user interaction) or Cloudflare Turnstile, verified on the server.
- A honeypot field hidden with CSS, plus a minimum time to submit (for example 3 seconds). Failing either returns a fake success, so bots learn nothing.
- Rate limiting per IP (for example 5 per hour) through the Vercel firewall or middleware.
- Email validation: syntax, MX record, and a disposable-domain blocklist.
- Double opt-in. An address counts as on the list only after the confirmation link is clicked. Unconfirmed addresses expire after 7 days. Confirmation emails are throttled per address.

**Compliance (EU business)**
- A consent line under the button with a link to the privacy notice. The privacy notice says what is stored and why.
- An unsubscribe link in every email, and a way to delete the record.
- Store the minimum: email, confirmed-at, source UTM, created-at.

**Measurement for marketing (read through /api/v1)**
- The counts of confirmed and pending signups per day and per `utm_source` / `utm_campaign` / `utm_content`. No email addresses are exposed to the marketing repo.
- A GA4 event `waitlist_signup` on submit and `waitlist_confirmed` on confirm, carrying the UTM parameters.

**Storage and sending**
- The CTO decides: app database (a schema change, strictly in the cto lane) or the email provider's audience list (Resend, Loops or similar) behind our own endpoint.

## Part 2: weekly puzzle email to the confirmed list (added 25 Oct 2026, Hoang: keep the puzzle promise)
The waitlist promises "a weekly business puzzle", so the list needs a weekly send. The puzzle comes from what we already post daily.

**Who does what**
- **Marketing (this repo, weekly):** picks the week's best puzzle from the daily posts (by saves, shares and comments in perf/latest). Writes the email: subject, the question in full sentences, the options, one line of context, and a "See the answer" button. Hoang approves it, like the posts. Marketing then enters the draft through the app's admin screen in Chrome, the same way content is published. There is no import and no write API.
- **App (CTO lane):** an admin "Weekly puzzle email" composer with these parts:
  - fields for subject, image, body and an answer link;
  - a preview and a test send to Hoang;
  - scheduling;
  - a send through Resend to confirmed waitlist members only;
  - a one-click unsubscribe header and link;
  - per-send counts (sent, opened, clicked, unsubscribed) exposed through /api/v1 for the daily metrics refresh.

**The answer link:** "See the answer" goes to the puzzle page on edlintics.com (REQ-0002), so every email brings people to the site. Until REQ-0002 exists, the answer appears in the next week's email instead.

**Cadence:** one email a week, Tuesday morning Madrid time (marketing default; adjust from the data). If a week is missed, skip it; never send two.

**Success signal:** at least 40% open rate, at least 8% click to the answer, and unsubscribes under 1% per send.

## Part 3: /waitlist version B with interactive exercises, and a 50/50 test (added 25 Oct 2026, Hoang approved "build")
Mockups (layout and wording only): `assets/REQ-0003/versionB-desktop.png`, `versionB-phone.png`, `versionB-mockup.html`, `user-flow.png`.
- **Version A:** the plain /waitlist from the spec.
- **Version B:**
  - **Hero, left:** the headline "Learn the language of business by doing". The line under it reads "Accounting, mathematics, statistics and economics courses, built from short interactive exercises · Join the waitlist for early access and a weekly business puzzle". Then the email form and the consent line.
  - **Hero, right:** an interactive exercise card with subject tabs for Accounting, Mathematics, Statistics and Economics. Each tab loads one real exercise; the defaults come from the home page exercises (the balance-sheet equation, the break-even dial, and so on). Under the card: "Like this? Get one every week · Join the waitlist".
  - **"Courses opening soon":** four subject cards listing the real courses, with the real course cover images.
  - **Bottom:** a dark band, "Be first in when the courses open", with a second form.
- **Removed at Hoang's request:** the course badge, the stats row, the "Try a question" label, the lesson label, and the "?" in the empty slot. The page covers all courses, not one.
- **Real assets in the build:**
  - the real Ledger mascot;
  - the real interactive exercise components;
  - real course covers, and the site's own components and styles.
  - The mockup's drawings are placeholders.
- **Test:** split /waitlist visitors 50/50 between A and B, with the variant recorded on the signup row and in GA. Judge on confirmed signups per visitor after about 2 weeks.
- **Copy rule:** no full stop at the end of any sentence in page copy. Use " · " between phrases.
- **Also:**
  - On phones, the form comes before the exercise (home hero too).
  - A waitlist email that later creates an account merges into one record, with no second confirmation email.
  - The course pages' existing "Notify me at launch" form joins the same waitlist, with course interest set automatically.

## Success signal
Over the first 4 weeks: at least 5% of social visitors who land on the page confirm a signup, fewer than 2% of pending addresses look like bots, and the list reaches 300 confirmed signups by course launch.

## Out-of-scope check
No accounts, payments or community features. No referral leaderboard in v1; that is a possible v2 if signups are slow.

## Decision log
- 2026-10-25: proposed by the CMO after Hoang asked for a waitlist and raised bot signups. Relayed to the tutoring-web session for a homepage proposal.
- 2026-10-25: Hoang kept sign-up (needed to book tutoring). The hero shows the waitlist first, then "or Create a free account", and the header keeps "Get started". Hoang kept the weekly puzzle promise, which added Part 2.
- 2026-10-25: Hoang approved the build, including version B (all courses, interactive exercises) and the 50/50 test. tutoring-web's preview with real assets is still the sign-off step.
- _(Hoang: approve / defer / reject + reason here.)_
