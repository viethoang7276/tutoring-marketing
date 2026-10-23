# REQ-0002  ·  Daily puzzle page, with a teaser on the home page

- **Status:** proposed
- **Date:** 2026-10-23
- **Source:** competitor
- **Targets metric:** acquisition (social visitors who land on edlintics.com and sign up or enquire about tutoring)
- **Priority (CMO view):** medium
- **Effort guess (CMO, non-binding):** M

## Summary
Edlintics posts a business puzzle on social media twice a day, but the posts have nowhere useful to send people. A daily puzzle page on edlintics.com, with a small teaser on the home page, gives every post a landing page and turns puzzle viewers into site visitors.

## Evidence (lead with this)
- **Competitor (Brilliant):** read 23 Oct 2026 from Brilliant's Instagram (@brilliantorg, 323 posts, 473k followers).
  - **Daily challenges:** from 2019 to late 2020 they posted a daily challenge image almost every day, ending each caption with "Find out the answer to this Daily Challenge. Link in bio!" (66 of 129 captions sampled).
  - **Where the link went:** to puzzle pages on brilliant.org.
  - **Engagement:** 200 to 3,000 likes a post, peaking at about 14K during #100Problems in mid-2020.
  - **Then they stopped:** after 2020 they barely posted for about five years. Our hypothesis, not stated by Brilliant: the posts drew comments but few clicks, so organic Instagram did not pay back.
- **Our own setup:** the answer is already on slide 2, so a page must offer more than the answer:
  - an archive of past puzzles;
  - a fuller worked explanation;
  - a next step into a lesson or tutoring.
- **First-party data:** none yet (the /api/v1 read token is pending). This is a hypothesis, labelled as such.

## Hypothesis
We believe that **a shareable daily puzzle page linked from every post's first comment and from the bio** will cause **more social viewers to visit edlintics.com and start a lesson or ask about tutoring**. The reason is that Brilliant's puzzles drew strong engagement but had a weak path from the post to the product; we can give that path a destination.

## Job to be done (problem, not solution)
"When I see an Edlintics puzzle and want to check my reasoning or try another one, I want one place with today's puzzle, the full explanation and past puzzles, so that I keep practising without hunting through Instagram."

## Proposed requirements (CTO owns the final design)
- The system shall have a public route (for example `/puzzles`, with `/puzzles/<slug>` per puzzle) listing today's puzzle first and an archive of past ones by subject.
- Each puzzle page shall show the question, options, an answer reveal that the student chooses to open, the worked explanation, and a link to the related lesson or to tutoring.
- The home page shall have a small "Today's puzzle" section showing the current question and linking to its page.
- Puzzle content shall be enterable through the admin editor, like other content (no JSON import or schema coupling from the marketing repo).
- Each page shall be shareable with a stable URL and social preview image.
- Visits and clicks from each puzzle page to a lesson or tutoring shall be measurable and exposed to marketing through /api/v1.

## Success signal (how marketing will know it worked)
Within 8 weeks of launch: puzzle pages become a top-3 landing source from social, and at least 5% of puzzle-page visitors click through to a lesson or tutoring page. If that doesn't happen, drop the archive and keep only the home-page teaser.

## Out-of-scope check
To check against `tutoring-web/docs/{vision,product}.md` before relay. This adds no accounts, payments or community features. It is public content plus a link-out. No leaderboard or streaks are requested.

## Decision log
- 2026-10-23 — proposed by CMO after Hoang asked whether the daily challenge should be a route or a home-page section.
- _(Hoang: approve / defer / reject + reason here.)_
