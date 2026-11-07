# Economic calendar (added 6 Nov 2026, Hoang)

Hoang's decision (6 Nov 2026): the content also follows scheduled economic events with global impact. This widens the 31 Oct holiday scope for these events only, so US inflation data and US Federal Reserve decisions count even though they are US releases. Other national days and national data stay out.

## Which events count

- US Federal Reserve rate decisions
- European Central Bank (ECB) rate decisions
- US CPI inflation releases
- Euro area flash inflation releases
- Big earnings weeks

Jobs reports, other central banks and smaller data releases are not on the list. Add one only if Hoang asks.

## How the planner uses this file

Every Thursday run checks this file, in both the monthly plan and the weekly refresh (step 4b in `weekly-content-process.md`).

- **What to look for:** every event whose "plan by" date falls in the next 3 weeks.
- **Limit:** at most one economic post in any Monday-to-Sunday week. It uses a normal slot and counts toward the weekly refresh's limit of about a third of the slots. It is never an extra post.
- **More than one event in a week:** choose in this order: rate decision, then US CPI, then euro area flash inflation, then earnings. One post may cover two decisions that fall in the same week.
- **Timing:** the post goes out 1 to 3 days before the event.
- **Holiday overlap:** Black Friday, the Christmas run and other big holiday runs keep their slots. The economic post takes a free slot or is skipped that week.
- **No forced posts:** if no idea passes the normal checks and scores 70 or more, skip the event and say so in the plan's "what changed and why" note. An economic post is optional, not a quota.

## Rules for the post

- **Teach the concept, not the result.** Explain what the event means and how it works, such as what a rate cut does to a loan. The post must stay true whatever the outcome, so it can be built and approved ahead of time.
- **No forecasts and no investment advice.** Never predict the result, a market move or a stock price, and never suggest buying or selling anything.
- **Currency.** Worked examples follow the mix-currencies rule, and a post about an event may use that economy's currency. Any real figure comes from the official source, is checked, and is dated.
- **One concept, normal format.** It is a normal puzzle, reel or carousel that passes the benchmark, full-sentence and definition checks. Number-based reels get a chart or table.
- **Concept registry still applies.** A concept used before may return only with a new angle and when the old post is more than 30 days old. Log it with `exception: "news"` and one line of reason.
- **Record the hook.** Set `meta.hook_reason` or the plan note to the event and its date.

## Check before relying on a date

Open the official source when an event first enters the 3-week view, and again 7 days before the post. Dates can move, and each Federal Reserve date stays tentative until confirmed at the meeting before it. If a date has moved, correct this file.

- Federal Reserve: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
- ECB meetings: https://www.ecb.europa.eu/press/calendars/mgcgc/html/index.en.html
- US CPI: https://www.bls.gov/schedule/news_release/cpi.htm
- Euro area inflation: https://ec.europa.eu/eurostat/en/news/euro-indicators and https://www.ecb.europa.eu/events/calendar/statscal/html/index.en.html

## Dates, December 2026 to December 2027

Checked on 6 Nov 2026 against the Federal Reserve, ECB and US Bureau of Labor Statistics pages above. The event date is the day of the decision or release. The two euro area dates come from a search summary of the ECB statistical calendar, so confirm them on the official page first.

"Plan by" is the Thursday before the week that holds the last posting day. A date in the posting window that falls in an earlier week needs an earlier plan.

| Event date | Event | Detail | Posting window | Plan by (Thursday) |
|---|---|---|---|---|
| Tue 1 Dec 2026 | Euro area flash inflation | Nov 2026 | 28 to 30 Nov | 26 Nov 2026 |
| Wed 9 Dec 2026 | Federal Reserve decision | Meeting 8-9 Dec, with projections | 6 to 8 Dec | 3 Dec 2026 |
| Thu 10 Dec 2026 | US CPI | Nov 2026 | 7 to 9 Dec | 3 Dec 2026 |
| Thu 17 Dec 2026 | ECB decision | Meeting 16-17 Dec | 14 to 16 Dec | 10 Dec 2026 |
| Wed 6 Jan 2027 | Euro area flash inflation | Dec 2026 | 3 to 5 Jan | 31 Dec 2026 |
| Wed 13 Jan 2027 | US CPI | Dec 2026 | 10 to 12 Jan | 7 Jan 2027 |
| Wed 27 Jan 2027 | Federal Reserve decision | Meeting 26-27 Jan | 24 to 26 Jan | 21 Jan 2027 |
| Thu 4 Feb 2027 | ECB decision | Meeting 3-4 Feb | 1 to 3 Feb | 28 Jan 2027 |
| Thu 11 Feb 2027 | US CPI | Jan 2027 | 8 to 10 Feb | 4 Feb 2027 |
| Wed 10 Mar 2027 | US CPI | Feb 2027 | 7 to 9 Mar | 4 Mar 2027 |
| Wed 17 Mar 2027 | Federal Reserve decision | Meeting 16-17 Mar, with projections | 14 to 16 Mar | 11 Mar 2027 |
| Thu 18 Mar 2027 | ECB decision | Meeting 17-18 Mar | 15 to 17 Mar | 11 Mar 2027 |
| Tue 13 Apr 2027 | US CPI | Mar 2027 | 10 to 12 Apr | 8 Apr 2027 |
| Wed 28 Apr 2027 | Federal Reserve decision | Meeting 27-28 Apr | 25 to 27 Apr | 22 Apr 2027 |
| Thu 29 Apr 2027 | ECB decision | Meeting 28-29 Apr | 26 to 28 Apr | 22 Apr 2027 |
| Wed 12 May 2027 | US CPI | Apr 2027 | 9 to 11 May | 6 May 2027 |
| Wed 9 Jun 2027 | Federal Reserve decision | Meeting 8-9 Jun, with projections | 6 to 8 Jun | 3 Jun 2027 |
| Thu 10 Jun 2027 | ECB decision | Meeting 9-10 Jun | 7 to 9 Jun | 3 Jun 2027 |
| Thu 10 Jun 2027 | US CPI | May 2027 | 7 to 9 Jun | 3 Jun 2027 |
| Wed 14 Jul 2027 | US CPI | Jun 2027 | 11 to 13 Jul | 8 Jul 2027 |
| Thu 22 Jul 2027 | ECB decision | Meeting 21-22 Jul | 19 to 21 Jul | 15 Jul 2027 |
| Wed 28 Jul 2027 | Federal Reserve decision | Meeting 27-28 Jul | 25 to 27 Jul | 22 Jul 2027 |
| Wed 11 Aug 2027 | US CPI | Jul 2027 | 8 to 10 Aug | 5 Aug 2027 |
| Thu 9 Sep 2027 | ECB decision | Meeting 8-9 Sep | 6 to 8 Sep | 2 Sep 2027 |
| Tue 14 Sep 2027 | US CPI | Aug 2027 | 11 to 13 Sep | 9 Sep 2027 |
| Wed 15 Sep 2027 | Federal Reserve decision | Meeting 14-15 Sep, with projections | 12 to 14 Sep | 9 Sep 2027 |
| Thu 14 Oct 2027 | US CPI | Sep 2027 | 11 to 13 Oct | 7 Oct 2027 |
| Wed 27 Oct 2027 | Federal Reserve decision | Meeting 26-27 Oct | 24 to 26 Oct | 21 Oct 2027 |
| Thu 28 Oct 2027 | ECB decision | Meeting 27-28 Oct | 25 to 27 Oct | 21 Oct 2027 |
| Wed 10 Nov 2027 | US CPI | Oct 2027 | 7 to 9 Nov | 4 Nov 2027 |
| Wed 8 Dec 2027 | Federal Reserve decision | Meeting 7-8 Dec, with projections | 5 to 7 Dec | 2 Dec 2027 |
| Fri 10 Dec 2027 | US CPI | Nov 2027 | 7 to 9 Dec | 2 Dec 2027 |
| Thu 16 Dec 2027 | ECB decision | Meeting 15-16 Dec | 13 to 15 Dec | 9 Dec 2027 |

**Euro area flash inflation after January 2027:** these dates are not listed yet. Read them from the official calendars each time a new monthly plan starts, and add them here.

**Earnings weeks:** companies set their own dates, so none are listed here. The busiest periods are usually mid-January to February, mid-April to May, mid-July to August and mid-October to November. When planning inside one of these periods, confirm the date on the company's investor relations page and use only figures from its own reports. Use a globally known company, and teach how to read the report, such as revenue versus profit or what guidance means.
