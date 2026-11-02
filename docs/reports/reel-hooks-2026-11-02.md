# Reel hooks: what worked and what failed, 25 to 31 Oct 2026

Prepared 2 Nov 2026 for Hoang. Read-only analysis. Nothing was written to the hub and Chrome was not used.

## Data mode and limits

- **Source: live platform stats, local copy.** `assets/renders/hub/perf-latest-2026-11-02-weekly.json` (a copy of hub `perf/latest`), platform readings taken 2 Nov 2026, 00:20 to 01:10 Vietnam time. Instagram and Facebook figures are Business Suite or profile readings; YouTube is Studio Content > Shorts; TikTok is Studio Posts.
- **Not loaded:** the hub `perfposts/<date>` collection and `slots`. The hub tools were not available in this session, so any reading taken after the local copy is not included. The local file already carries the per-post rows, so the table below is complete for what it holds.
- **Hooks:** the voiced first line is available for 5 of the 10 mature explainer-type reels (script files on disk: working capital, AI talks, compounding; skill example scripts for sunk cost and Moravec; the provisional Halloween reel also has one) and for all 7 mature puzzle reels (the voiced question comes from the puzzle JSON). For the other explainers (free-rider, accruals, break-even, deskilling, salesperson; provisionally the economics student and the list reel) the script files are not on disk, so only the **cover text** (from `assets/renders/thumbnails/w44-w45/map.tsv`) is known. Rows say which one is shown. The two skill-example scripts (sunk cost, Moravec) may differ from the cut that was posted.
- **Eligibility:** a reel is "mature" if posted at least 48 h before the 2 Nov 00:20 reading (posted on or before 31 Oct 00:00 VN). That gives **n = 17** (10 explainer-type, 7 puzzle). Four reels posted on 31 Oct after 00:20 are shown separately and not ranked. Reels from 1 Nov onward (diminishing returns, three puzzle reels, and the 5-term list reels) and all how-to reels (not live until 10 Nov) are excluded. The 5-concepts "Ledger walk" videos from 24 to 30 Oct are carousel-style videos with no voiced hook and are not in this analysis.
- **Retention:** only **Instagram** and **Facebook** give an average watch time (whole seconds). **YouTube** gives views only in this data (no average view duration or retention curve captured). **TikTok** shows 0 to 4 views per post and no skip rate was captured. **LinkedIn, X and Threads** give impressions or views only. No platform gives % watched or 3-second views in the data. Reel lengths are known for only some reels, so % watched is not computed.
- **Engagement columns** show interactions **from others**: the reading minus our own like, comment and share. Comments from others are 0 on every Instagram row in the mature set, so that column is left out.
- **Baselines (medians, mature reels, n = 17):** Instagram 157 views, Facebook 51, YouTube 54, TikTok 0. Ratios below are against these medians. Weekly platform shifts exist (see confounds), so a ratio is a guide, not a result.

## 1. Full table: mature reels (posted 25 to 31 Oct, at least 48 h before the reading)

### 1a. Hooks

| # | Posted (VN) | Type | Hook | Style | Source | Words in first line | Number in first line |
|---|---|---|---|---|---|---|---|
| 1 | 10-25 20:30 | definition | Sunk cost, explained by Ledger<br>Voiced: "Why do smart people keep paying for bad decisions?"; cover: "Already paid? That money is gone" | question to viewer / curiosity gap | skill example script | 9 | no |
| 2 | 10-26 14:30 | life-of | A day in the life of a business student: the free-rider problem<br>Voiced: not on disk; cover: "Five names, one grade, one does it all" | relatable situation | cover only | 8 (cover text) | yes |
| 3 | 10-27 14:30 | life-of | A day in the life of an accountant: accruals<br>Voiced: not on disk; cover: "Bill in November, cost in October" | curiosity gap (contrast) | cover only | 6 (cover text) | no |
| 4 | 10-27 18:00 | definition | Moravec's paradox: why soft skills are rising<br>Voiced: "The skills that pay are flipping."; cover: "Hard skills fall, soft skills rise" | contrarian claim | skill example script | 6 | no |
| 5 | 10-28 00:00 | puzzle | Same stock, same sales, different profit<br>Voiced question: "A shop buys 10 cases at $5, then 10 more at $7, and sells 10 at $10. Which method shows more gross profit?" | challenge (scenario + question) | puzzle JSON | 17 | yes |
| 6 | 10-28 14:30 | definition | Break-even point, explained by Ledger<br>Voiced: not on disk; cover: "When does a shop stop losing money?" | question to viewer | cover only | 7 (cover text) | no |
| 7 | 10-28 16:00 | puzzle | The extra variable that cannot hurt R-squared<br>Voiced question: "R-squared is 0.62. Adding a column of random coin flips lifts it to 0.63. Why is that no improvement?" | challenge (scenario + question) | puzzle JSON | 3 | yes |
| 8 | 10-28 18:00 | definition | Deskilling: is AI making you worse at your job?<br>Voiced: not on disk; cover: "AI makes you faster, and maybe worse" | contrarian claim | cover only | 7 (cover text) | no |
| 9 | 10-29 00:00 | puzzle | Three more people, how many more conversations?<br>Voiced question: "A team grows from 5 to 8 people, and every pair shares one line. How many extra lines are there now?" | challenge (scenario + question) | puzzle JSON | 14 | yes |
| 10 | 10-29 14:30 | life-of | A day in the life of a salesperson: conversion rate<br>Voiced: not on disk; cover: "40 calls 2 deals Awful or not?" | surprising number + question | cover only | 7 (cover text) | yes |
| 11 | 10-29 16:00 | puzzle | A beats B twice and still loses<br>Voiced question: "A store tests two product pages. The grid shows buyers out of visitors. Which page converts better overall?" | challenge (scenario + question), no digits | puzzle JSON | 6 | no |
| 12 | 10-30 00:00 | puzzle | Is a $300 customer worth acquiring?<br>Voiced question: "A customer costs $300 to win and brings $20 of profit a month. Each month, 5% cancel. Is one worth winning?" | challenge (scenario + question) | puzzle JSON | 13 | yes |
| 13 | 10-30 14:30 | definition | Working capital, explained by Ledger<br>Voiced: "Can you pay a bill before the money arrives?"; cover: "Can you pay before the money arrives?" | question to viewer | script.json | 9 | no |
| 14 | 10-30 16:00 | puzzle | Rank the loans by what they really cost<br>Voiced question: "Loan X charges 12.0% compounded monthly, Y 12.4% quarterly and Z 12.5% yearly. Rank them, cheapest first" | challenge (scenario + question) | puzzle JSON | 13 | yes |
| 15 | 10-30 18:00 | ledger-talks | Is AI making you worse at your job? What the studies say<br>Voiced: "AI can make you feel smarter while you think less."; cover: "AI can make you think less" | contrarian claim | script.json | 10 | no |
| 16 | 10-30 20:30 | highlighter | Compounding: why the first $100K is the slowest<br>Voiced: "Your first hundred thousand dollars is the slowest one."; cover: "Your first $100K is the slowest" | contrarian claim (number) | script.json | 9 | yes |
| 17 | 10-31 00:00 | puzzle | Two warehouses or one: how much safety stock?<br>Voiced question: "Two stores with independent demand each hold safety stock of 2 × SD = 200. What does one shared warehouse need?" | challenge (scenario + question) | puzzle JSON | 15 | yes |

Notes: "Words in first line" is the voiced first line where known, otherwise the cover text (marked). For puzzles it is the first sentence of the question; a puzzle's final sentence is the question the viewer is asked. "Number" means a digit, or a number word for voiced explainer hooks.

### 1b. Performance (views are platform views; LinkedIn and X are impressions)

| # | Reel | IG views | IG avg watch | IG likes / saves / shares (others) | FB views | FB avg watch | YT views | TikTok views | LinkedIn impr. | X impr. | Threads views |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Sunk cost, explained by Ledger | 149 | 8s | 3 / 0 / 0 | 51 | 3s | 78 | 3 | 75 | 9 | 10 |
| 2 | A day in the life of a business student: the f | 35 | 5s | 1 / 0 / 0 | 13 | 2s | 84 | 4 | 51 | 11 | 2 |
| 3 | A day in the life of an accountant: accruals | 191 | 7s | 3 / 0 / 0 | 16 | 6s | 173 | 0 | 21 | 8 | 9 |
| 4 | Moravec's paradox: why soft skills are rising | 1,442 | 12s | 25 / 10 / 1 | 38 | 3s | 140 | 0 | 36 | 8 | 3 |
| 5 | Same stock, same sales, different profit | 143 | 6s | 0 / 0 / 0 | 71 | 3s | 31 | 0 | - | - | - |
| 6 | Break-even point, explained by Ledger | 193 | 6s | 3 / 0 / 0 | 72 | 4s | 54 | 0 | 19 | 12 | 5 |
| 7 | The extra variable that cannot hurt R-squared | 216 | 7s | 0 / 1 / 0 | 35 | 4s | 104 | 0 | 16 | 8 | 15 |
| 8 | Deskilling: is AI making you worse at your job | 524 | 10s | 10 / 4 / 0 | 13 | 3s | 211 | 0 | 23 | 9 | 4 |
| 9 | Three more people, how many more conversations | 130 | 6s | 0 / 0 / 0 | 144 | 4s | 294 | 0 | 12 | 6 | 7 |
| 10 | A day in the life of a salesperson: conversion | 1,553 | 13s | 21 / 1 / 1 | 37 | 8s | 56 | 0 | 15 | 7 | 7 |
| 11 | A beats B twice and still loses | 47 | 4s | 1 / 0 / 0 | 52 | 2s | 47 | 0 | 8 | 8 | 2 |
| 12 | Is a $300 customer worth acquiring? | 142 | 7s | 1 / 0 / 0 | 11 | 1s | 15 | 1 | 4 | 5 | - |
| 13 | Working capital, explained by Ledger | 238 | 9s | 1 / 0 / 0 | 135 | 3s | 21 | 0 | 13 | 5 | 4 |
| 14 | Rank the loans by what they really cost | 157 | 3s | 2 / 2 / 0 | 95 | 2s | 10 | 0 | 5 | 4 | 12 |
| 15 | Is AI making you worse at your job? What the s | 164 | 7s | 4 / 0 / 0 | 126 | 3s | 24 | 1 | 3 | 4 | 9 |
| 16 | Compounding: why the first $100K is the slowes | 114 | 5s | 0 / 0 / 0 | 51 | 3s | 28 | 0 | 14 | 5 | 8 |
| 17 | Two warehouses or one: how much safety stock? | 111 | 5s | 0 / 1 / 0 | 80 | 3s | 24 | 0 | 6 | 5 | 2 |

## 1c. Provisional: posted 31 Oct after 00:20 VN (under 48 h old at the reading, not ranked)

| # | Posted (VN) | Type | Hook | Style | Source | Words in first line | Number in first line |
|---|---|---|---|---|---|---|---|
| 1 | 10-31 14:30 | life-of | A day in the life of an economics student: diminishing marginal utility<br>Voiced: not on disk; cover: "Why slice four is worth less than slice one" | question / curiosity gap | cover only | 9 (cover text) | no |
| 2 | 10-31 16:00 | puzzle | Who really pays a tax collected from sellers?<br>Voiced question: "Roasters sell cafés 50 bags a day at $20. The city taxes roasters $3 per bag. Using the slopes shown, how much more do cafés pay?" | challenge (scenario + question) | puzzle JSON | 9 | yes |
| 3 | 10-31 18:00 | list | 5 terms every finance interview expects you to know<br>Voiced: not on disk; cover: "5 finance terms for your next interview" | list (number in line) | cover only | 7 (cover text) | yes |
| 4 | 10-31 21:30 | life-of | A day in the life of a finance bro: forward contracts (Halloween)<br>Voiced: "A day in the life of a finance bro on Halloween night."; cover: "Cocoa fell, so why is candy not cheaper?" | relatable situation (voiced) / question (cover) | script.json | 12 | no |

| # | Reel | IG views | IG avg watch | IG likes / saves / shares (others) | FB views | FB avg watch | YT views | TikTok views | LinkedIn impr. | X impr. | Threads views |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A day in the life of an economics student: dim | 995 | 1m 6s | 26 / 4 / 12 | 40 | 4s | 57 | 0 | 6 | 4 | - |
| 2 | Who really pays a tax collected from sellers? | 192 | 7s | 1 / 0 / 0 | 19 | 2s | 37 | 0 | 11 | 3 | 13 |
| 3 | 5 terms every finance interview expects you to | 712 | 8s | 16 / 13 / 1 | 112 | 2s | 42 | 0 | 9 | 5 | 1 |
| 4 | A day in the life of a finance bro: forward co | 281 | 10s | 4 / 0 / 0 | 32 | 4s | 21 | 0 | 54 | 7 | 2 |

Anomaly: the economics-student reel shows an Instagram average watch of 1m 6s, far above every other reel (3 to 13 s). It may be a read error or a loop count; do not use it until re-read.

## 2. Top 5 and bottom 5 hooks

Ranked on Instagram views (the only platform with a usable spread; Facebook is shown alongside because it moves differently). n = 17, Instagram quartiles 130 / 157 / 216.

### Top 5 (top quartile, Instagram views at or above 216)

| Rank | Hook | Type | IG views (x median) | IG avg watch | FB views (x median) | YT views |
|---|---|---|---|---|---|---|
| 1 | Cover: "40 calls 2 deals Awful or not?" (voiced line not on disk) | life-of | 1,553 (9.9x) | 13s | 37 (0.7x) | 56 |
| 2 | "The skills that pay are flipping." | ledger-talks style (Moravec) | 1,442 (9.2x) | 12s | 38 (0.7x) | 140 |
| 3 | Cover: "AI makes you faster, and maybe worse" (voiced line not on disk) | definition | 524 (3.3x) | 10s | 13 (0.3x) | 211 |
| 4 | "Can you pay a bill before the money arrives?" | definition | 238 (1.5x) | 9s | 135 (2.6x) | 21 |
| 5 | "R-squared is 0.62." then the coin-flip question | puzzle | 216 (1.4x) | 7s | 35 (0.7x) | 104 |

Top on Facebook instead (top quartile, 80 or more): "Three more people, how many more conversations?" puzzle 144 (2.8x), working capital 135 (2.6x), AI talks "AI can make you feel smarter while you think less." 126 (2.5x), loans puzzle 95, warehouses puzzle 80. Working capital is the only reel in the top quartile on both Instagram and Facebook.

### Bottom 5 (bottom quartile, Instagram views at or below 130)

| Rank (worst first) | Hook | Type | IG views (x median) | IG avg watch | FB views (x median) | YT views |
|---|---|---|---|---|---|---|
| 1 | Cover: "Five names, one grade, one does it all" (voiced line not on disk) | life-of | 35 (0.2x) | 5s | 13 (0.3x) | 84 |
| 2 | "A store tests two product pages. The grid shows buyers out of visitors." (Simpson's paradox; no digits in the first line) | puzzle | 47 (0.3x) | 4s | 52 (1.0x) | 47 |
| 3 | "Two stores with independent demand each hold safety stock of two standard deviations, which is two hundred units." | puzzle | 111 (0.7x) | 5s | 80 (1.6x) | 24 |
| 4 | "Your first hundred thousand dollars is the slowest one." | highlighter | 114 (0.7x) | 5s | 51 (1.0x) | 28 |
| 5 | "A team grows from 5 to 8 people, and every pair shares one line." | puzzle | 130 (0.8x) | 6s | 144 (2.8x) | 294 |

Low hold regardless of views: the loans puzzle ("Loan X charges twelve percent compounded monthly, Y twelve point four percent quarterly...") has the lowest Instagram watch time (3s) and 2s on Facebook, at a median-sized 157 views. The "A beats B" puzzle is next at 4s and 2s. Both are long, number-heavy openings.

Row 5 of the bottom list is a split result: weak on Instagram, best on Facebook. Treat the bottom list as Instagram-specific.

## 3. Patterns found

| # | Pattern | n | Confidence |
|---|---|---|---|
| P1 | The three Instagram outliers (524 to 1,553 views, 3.3x to 9.9x median) were all explainer-type reels whose hook is a **claim or a number with a judgment** about work and AI: Moravec "The skills that pay are flipping.", salesperson "40 calls 2 deals Awful or not?", deskilling "AI makes you faster, and maybe worse". No puzzle and no plain definition question reached 500. | 3 of 10 explainers; 0 of 7 puzzles | Low. Topic is a confound (careers, AI and sales are broader subjects than R-squared or break-even). Claim style is not sufficient: the other two claim hooks were at or below median (AI talks "AI can make you feel smarter while you think less." 164, same topic as deskilling; compounding 114). That is 2 hits in 4 claims |
| P2 | Instagram views and average watch time move together: the three outliers hold 10 to 13s; every other mature reel holds 3 to 9s. Spearman rank correlation 0.81 (n = 17). | 17 | High that they are associated; no causal reading, since Instagram may show a reel more widely once early viewers hold, and the reverse |
| P3 | Puzzle reels are a tight, mediocre band on Instagram (47 to 216, median 142 vs 192 for explainers; without the 3 outliers explainers are 164). Hook wording differences inside puzzles do not separate them. The one puzzle opening without digits or money (Simpson's paradox) was the lowest, and the longest, number-heavy openings (loans, warehouses) had the lowest hold. | 7 | Low. One case per claim |
| P4 | Facebook behaves differently from Instagram: plain question hooks rank high (break-even 72 is the top of its 25 to 29 Oct window; working capital 135; the conversations puzzle 144), while the Instagram claim winners sit below the Facebook median (37, 38 and 13 vs 51). | 3 question hooks vs 3 claim hooks | Low. Facebook views drift upward over the week (rank correlation with order 0.44), so later reels have a head start; the 30 Oct to 31 Oct reels sit in a higher band |
| P5 | Life-of reels have the widest spread (35, 191, 1,553; provisional 995 and 281). The weakest cover (a list of names and a grade, no stake) is the lowest; the strongest names a count and asks a verdict. The provisional economics reel (995) also asks a concrete "why" question. | 3 mature (+2 provisional) | Low. Cannot separate hook from topic or post time |
| P6 | YouTube and TikTok carry no hook signal in this data. YouTube Shorts views fall with post date (rank correlation with order -0.67): the oldest reels have the most views, regardless of hook. TikTok shows 0 views on 13 of 17 reels. | 17 | High that these two platforms cannot be used to compare hooks now |

Confounds that apply to everything above: post time and day, platform distribution shifts over the week (Facebook up, YouTube down), the topic itself, music, a very small and mostly follower-limited Instagram audience, a single reading per post, and voiced hook text missing for 5 of the 10 mature explainers in the mature set (cover text is a stand-in). With n = 17 and one reel per hook, none of this is a statistical result.

## 4. Hook rules to test next

1. **Number plus a verdict question on life-of and definition reels.** Rule: open on a concrete count or amount and ask for a judgment ("40 calls, 2 deals: awful or not?"). The scheduled life-of covers already vary this: "$300,000 in the bank is 5 months" and "+10% demand becomes +150% at the factory" are number-led; "Email B won and nobody knows why" and "You won the bid That may be bad news" are story-led. Measure: Instagram views against the life-of median, average watch of 10s or more, and saves plus shares per 1,000 views, with each reel tagged number-led or story-led. Judge after at least 4 per arm; fits with H14.
2. **Same topic, two hook styles, one platform.** Rule: for the next AI or careers topic, publish one version with a claim hook and one with a plain "what is X" or question hook, on different days at the same time slot. Measure: Instagram and Facebook views as a ratio to that day's reel median. This separates topic from style, which P1 cannot.
3. **Short, money-first puzzle openings.** Rule: puzzle first sentence of 10 words or fewer, with a dollar amount or percentage in it, against the current 13 to 17 word number-heavy setups. Measure: Instagram average watch (target 6s or more, current median 6s on this set) and, once captured, 3-second views. Needs about 4 per arm.
4. **Question hook for Facebook.** Rule: where a reel has a plain question cover, check Facebook views against the Facebook median for that day. Measure: Facebook views as a ratio to the day's median across the 5 or so posts that day, with at least 6 question and 6 claim reels. This keeps the Facebook upward drift out of the comparison.
5. **Record the hook, so the next analysis is possible.** Rule: write the voiced first line, its word count and a style tag onto every reel slot at build time (a hub field or the script file kept after publishing). Measure: next analysis finds a voiced hook for 100% of reels instead of 12 of 17 here. Also capture, per reel, Instagram average watch and % watched, YouTube average view duration and "stayed to watch", and TikTok skip rate when TikTok views move above 0.

## Data gaps

- Voiced hook lines missing for 5 of 10 mature explainers (script files not retained on disk).
- No % watched, 3-second views, skip rate or YouTube retention captured anywhere.
- Hub `perfposts` and `slots` not loaded; the local `perf/latest` copy is dated 2 Nov 00:20 to 01:10 VN.
- Four provisional reels (31 Oct) and everything from 1 Nov need a re-read at 48 h before they can be ranked.
- Facebook audience is 65 followers and TikTok 1; their numbers are small enough that single posts can swing a ratio.
