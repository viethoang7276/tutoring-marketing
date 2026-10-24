# Meme-comic scripts v1, 2026-10-24 (revised after brand review)

Status: draft, brand review passed (0 HIGH), fixes applied. Nothing is approved or scheduled. Source: `docs/research/2026-10-24-meme-pain-point-bank.md`.

Format for every comic: white background, small grey topic label top-left, each line in a speech bubble from its speaker (Hoang, 24 Oct 2026: speech bubbles), Ledger characters at a desk with a laptop (senior: glasses, grey cardigan; junior: blue hoodie; both book-shaped with blue bookmark and blue tie), Edlintics logo at the bottom. Slides: 3 or 4 comic panels, one "the real lesson" slide, then the standard CTA slide. Each panel lists the Ledger state for both characters (idle, cheerful, focused, thinking, proud, surprised, stuck, resting); deadpan is carried by posture and props. Machine-readable copy: `/private/tmp/claude-501/-Users-hoangtruong-Desktop-WebDevelopment-tutoring-edlintics-marketing/b1cda27f-49e5-4898-b02c-508c299fe887/scratchpad/meme/comics-v1.json`.

Scores are 1 to 5 on: relatable to students and workers (R), clarity of pain (C), drawability in 3-4 panels (D), concept payoff (P).

## Ranking

| Rank | ID | Pain | Subject | Premise | R | C | D | P | Total |
|---|---|---|---|---|---|---|---|---|---|
| 1 | C01 | P17 | business | A $10,000 profit on screen, an empty till on payday. | 5 | 5 | 5 | 5 | 20 |
| 2 | C03 | P34 | statistics | Umbrella sales and late trains rise together, and rain sits behind both. | 5 | 5 | 5 | 4 | 19 |
| 3 | C02 | P03 | accounting | A $90 trial balance gap solved by a divisible-by-nine clue. | 4 | 5 | 4 | 5 | 18 |
| 4 | C05 | P16 | workplace | A net-30 invoice pays on day 62, so the pain becomes a metric. | 5 | 5 | 4 | 4 | 18 |
| 5 | C09 | P30 | economics | Inflation falls from 5% to 2%, yet the basket still costs more. | 5 | 4 | 4 | 5 | 18 |
| 6 | C04 | P20 | workplace | Two people hold "the latest export" from different dates: $48,000 vs $52,500. | 5 | 5 | 4 | 3 | 17 |
| 7 | C06 | P25 | economics | A price rise moves the dot on the curve, not the curve. | 3 | 4 | 4 | 5 | 16 |
| 8 | C07 | P32 | statistics | A p-value of 0.03 is read as "97% sure". | 4 | 4 | 3 | 5 | 16 |
| 9 | C08 | P07 | accounting | "Just adding things up" meets a $12,000 server receipt. | 4 | 4 | 4 | 4 | 16 |
| 10 | C10 | P23 | business | A debt model chases its own tail in one circular cell. | 3 | 4 | 4 | 4 | 15 |

Subjects covered: accounting (2), economics (2), statistics (2), business (2), workplace (2).

Suggested posting order, so P16 and P17 are never back-to-back: C01, C03, C02, C09, C04, C05, C07, C08, C06, C10.

---

## C01 | P17 | Business | The profitable empty till

Topic label: Business

1. Speaker: junior. State: junior cheerful, senior idle. Scene: Junior stands at the desk holding a printed report upright. Laptop screen shows "Profit: $10,000". Senior sits at the desk.
   Line: We made $10,000 in profit this month.
2. Speaker: senior. State: junior idle, senior focused. Scene: Close on a wall calendar, Friday circled and labelled "Payroll: $6,000". Senior turns toward an open cash drawer holding one coin.
   Line: Noted. Payroll is $6,000 on Friday.
3. Speaker: junior. State: junior stuck, senior idle. Scene: Junior stands by the laptop with the report lowered to hip height. Screen shows "Sale: $16,000, due in 60 days".
   Line: The customer pays in sixty days.
4. Speaker: senior. State: junior stuck, senior thinking. Scene: Both characters sit side by side, shoulders level, facing the empty drawer. The coin sits on the desk.
   Line: Then we are profitable and broke at the same time.

Punchline mechanism: understatement and reversal; the good news and the bad news are one sentence.

Lesson slide: Revenue is recorded when a sale is earned, not when the cash arrives. The whole $16,000 sale is recorded as revenue today, and $0 reaches the bank until day 60. Payroll of $6,000 is paid from cash, so a month can show a $10,000 profit and still leave the bank short on Friday.

Caption: A business can report a $10,000 profit and still be unable to cover a $6,000 payroll. Profit counts a sale when it is earned. The bank records it when the customer pays. Both numbers are true, and they answer different questions. Have you ever seen a profitable month with an empty account?
#edlintics #edlinticsprofit #edlinticscashflow

First comment: Bonus tip: when you read a statement, find operating cash flow before you judge the profit line. If profit is rising and operating cash flow is falling, ask where the money is stuck. Receivables and inventory are the usual answer.

Scores: R5 C5 D5 P5 = 20

---

## C03 | P34 | Statistics | Umbrellas and late trains

Topic label: Statistics

1. Speaker: junior. State: junior focused, senior idle. Scene: Junior at the laptop. Screen shows a line chart with two rising lines labelled "Umbrella sales" and "Late trains". A commuter pass lies on the desk.
   Line: Umbrella sales and late trains rise together.
2. Speaker: junior. State: junior thinking, senior idle. Scene: Junior leans toward the screen holding a closed umbrella like a pointer.
   Line: Should we ban umbrellas to fix the timetable?
3. Speaker: senior. State: junior idle, senior focused. Scene: Senior at a whiteboard draws a small rain cloud above both lines with arrows down to each, marker in hand.
   Line: Something else sits behind both lines.
4. Speaker: junior. State: junior proud, senior idle. Scene: Junior hangs the umbrella on the chair and opens a weather forecast on the laptop.
   Line: I will leave the umbrellas and check the forecast.

Punchline mechanism: reversal; the junior reaches the sensible conclusion through a small dry action.

Lesson slide: Two things that move together are correlated, but that alone does not show that one causes the other. A third factor, called a confounder, can drive both. A shop that sells 400 umbrellas on a wet day and 40 on a dry day will also see more late trains on the wet day, whether or not anyone owns an umbrella.

Caption: Two lines rising together is a pattern, not an explanation. Before you read a cause into a correlation, look for a third factor that could drive both. In this case it is the rain. The same check works on sales reports, survey results and any chart that arrives in a meeting. What is the best false cause you have been shown?
#edlintics #edlinticsstatistics #edlinticscorrelation

First comment: A follow-up question: if you wanted to test whether umbrellas really affect train delays, how would you design it? Hint: you would need to hold the weather fixed, or assign the umbrellas at random.

Scores: R5 C5 D5 P4 = 19

---

## C02 | P03 | Accounting | The ninety dollar hunt

Topic label: Accounting

1. Speaker: junior. State: junior focused, senior not in frame. Scene: Junior hunched over the laptop, three empty coffee cups on the desk, wall clock showing late. Screen shows "Debits $48,350" and "Credits $48,260".
   Line: The trial balance is off by $90.
2. Speaker: junior. State: junior stuck, senior not in frame. Scene: Junior sits behind a thick ledger bristling with sticky notes, bookmark askew, shoulders dropped.
   Line: I have checked all two hundred entries twice.
3. Speaker: senior. State: junior stuck, senior thinking. Scene: Senior walks in holding a mug and stops beside the desk, head tilted toward the screen.
   Line: Ninety divides by nine. Look for swapped digits.
4. Speaker: junior. State: junior surprised, senior resting. Scene: Junior holds the ledger open at a line reading "$540", with "$450" on the invoice beside it. Senior is already walking out with the mug.
   Line: Two hours, and it was one swap.

Punchline mechanism: recognition plus reversal; two hours of effort undone by one arithmetic clue.

Lesson slide: When a trial balance is off by an amount that divides evenly by 9, two digits have often been swapped. Posting $450 as $540 creates a $90 gap, and 90 divided by 9 is 10. That is a clue, not proof, so confirm it against the source document. If the gap is twice a single amount, that amount may have been posted to the wrong side, so halve the gap and search for that figure.

Caption: A trial balance that will not balance often has a pattern. A gap that divides evenly by 9 often points to two swapped digits. A gap that is exactly double an amount often points to a debit posted as a credit. Neither is proof, but each narrows the search. What is the longest you have spent hunting for a small gap?
#edlintics #edlinticsaccounting #edlinticstrialbalance

First comment: A warning to go with the tip: a balanced trial balance does not prove the books are right. An entry posted twice, or to the wrong account, keeps debits equal to credits. The test checks the arithmetic, not the accuracy.

Scores: R4 C5 D4 P5 = 18

---

## C05 | P16 | Workplace | Day sixty-two

Topic label: Workplace

1. Speaker: junior. State: junior cheerful, senior idle. Scene: Junior at the laptop. Screen shows "Invoice: $6,000, due in 30 days" with a send button.
   Line: Invoice sent. Payment is due in thirty days.
2. Speaker: senior. State: junior idle, senior thinking. Scene: Wall calendar with days crossed off and "Day 30" circled. Laptop shows an empty inbox. Senior stands with a coffee facing the calendar.
   Line: Day thirty has arrived. The bank balance has not changed.
3. Speaker: junior. State: junior stuck, senior idle. Scene: Calendar now reads "Day 47". Junior slumps over the keyboard. Three sent-mail icons sit on screen.
   Line: I have sent three reminders. Each one was very polite.
4. Speaker: senior. State: junior resting, senior proud. Scene: Laptop shows "Payment received: $6,000". Calendar reads "Day 62". Junior leans back in the chair. Senior writes the number on a notepad.
   Line: It arrived on day sixty-two. Now we measure it.

Punchline mechanism: recognition, then a dry pivot; the pain becomes a metric.

Lesson slide: Days sales outstanding shows how long customers take to pay, on average across all invoices. Divide receivables by credit sales, then multiply by the days in the period. If a business has $60,000 in receivables on $120,000 of credit sales over 90 days, its DSO is 45 days, which is 15 days slower than net-30 terms.

Caption: Net 30 is a term, not a guarantee of payment. When invoices arrive late, the delay is a number you can track. Days sales outstanding turns a vague frustration into a trend you can bring to a meeting. A rising DSO is often the first sign of a cash problem. How long do your invoices usually take to get paid?
#edlintics #edlinticsreceivables #edlinticsfinance

First comment: A quick check: at $120,000 of credit sales over 90 days, each day of DSO is worth about $1,333 of cash tied up. Cutting DSO from 45 days to 40 would free roughly $6,667. Which lever would you pull first, earlier invoices or firmer terms?

Scores: R5 C5 D4 P4 = 18

---

## C09 | P30 | Economics | Slower is not cheaper

Topic label: Economics

1. Speaker: junior. State: junior cheerful, senior idle. Scene: Junior holds a grocery basket with bread and eggs. Behind, the laptop shows a falling chart labelled "Inflation: 5% to 2%".
   Line: Inflation fell from 5% to 2%. That is good news.
2. Speaker: junior. State: junior thinking, senior idle. Scene: Junior holds up a receipt reading "$107.10", basket on the other arm.
   Line: Then why does my basket cost more than before?
3. Speaker: senior. State: junior idle, senior focused. Scene: Senior at a notepad draws three rising steps labelled "$100", "$105", "$107.10".
   Line: Prices still rose. They just rose more slowly.
4. Speaker: junior. State: junior proud, senior idle. Scene: Junior stands in front of the steps, basket in hand, posture upright and still.
   Line: Slower is not cheaper. I have noted it.

Punchline mechanism: understatement; one short sentence restates the whole concept.

Lesson slide: Inflation measures how fast prices rise, not whether they fall. A basket that costs $100 rises to $105 at 5% inflation, then to $107.10 at 2% inflation. The rate dropped from 5% to 2%, but the basket still costs $7.10 more than two years ago.

Caption: When inflation falls from 5% to 2%, prices have not gone down. They are rising more slowly. A lower rate still stacks on top of the earlier increases, so the price level stays higher. This is why the numbers and the receipt can feel like they disagree. Which price do you check first to judge the cost of living?
#edlintics #edlinticseconomics #edlinticsinflation

First comment: Bonus: for the price level to fall, you need negative inflation, called deflation. At 5% and then minus 1%, the $105 basket would cost $103.95. Even then, it is still above where it started.

Scores: R5 C4 D4 P5 = 18

---

## C04 | P20 | Workplace | Two exports and a meeting

Topic label: Workplace

1. Speaker: junior. State: junior focused, senior idle. Scene: Junior at one laptop. Screen shows "Budget export: Mar 3, total $48,000".
   Line: I am working from the latest budget export.
2. Speaker: senior. State: junior idle, senior focused. Scene: Senior turns a second laptop toward the camera. Screen shows "Budget export: Mar 10, total $52,500".
   Line: So am I. Mine is from last week.
3. Speaker: junior. State: junior thinking, senior thinking. Scene: The two laptops face each other on the desk. A sticky note between them reads "$4,500".
   Line: Neither of us is wrong. We exported on different days.
4. Speaker: senior. State: junior stuck, senior stuck. Scene: Both characters sit very still, upright, laptops closed halfway, a calendar on the wall with a meeting marked.
   Line: We now have two budgets and a meeting.

Punchline mechanism: recognition and understatement; the whole office knows this scene.

Lesson slide: When people work from exports taken on different dates, nobody can say which total is current. Keep one master file in a shared location, date every export, and log each change with an author. Then a difference such as $48,000 versus $52,500 becomes a $4,500 question you can trace, not an argument.

Caption: Two people can both hold the latest export and still disagree. When the exports come from different days, a $4,500 difference becomes a meeting about whose spreadsheet is right. One shared master file, dated exports and a simple change log reduce it. How many versions of your budget file exist right now?
#edlintics #edlinticsspreadsheets #edlinticsmodelling

First comment: A small habit worth copying: put the date and the author's initials in the change log cell every time a total moves. It takes ten seconds and answers the question before anyone asks it.

Scores: R5 C5 D4 P3 = 17

---

## C06 | P25 | Economics | The dot moved, the curve did not

Topic label: Economics

1. Speaker: junior. State: junior idle, senior idle. Scene: Cafe counter. A price board reads "Coffee $5" with "$4" crossed out above it. Junior holds a cup and faces the board. Senior sits at a nearby table.
   Line: The price of coffee rose from $4 to $5.
2. Speaker: junior. State: junior thinking, senior idle. Scene: Junior opens a small notebook and draws a downward-sloping line with a dot on it at "$4".
   Line: So demand for coffee fell.
3. Speaker: senior. State: junior idle, senior focused. Scene: Senior leans over the notebook. The dot has slid along the same line to "$5". Only one line is drawn.
   Line: The dot moved. The curve did not.
4. Speaker: junior. State: junior proud, senior idle. Scene: Junior writes in the notebook, cup in the other hand, posture upright and composed.
   Line: Quantity demanded fell. Demand stayed put. I will write that down.

Punchline mechanism: understatement; a one-word distinction delivered as a calm correction.

Lesson slide: A change in price moves you along the demand curve, which changes the quantity demanded. If coffee rises from $4 to $5 and daily sales fall from 100 cups to 80, that is a movement along one curve. Demand itself shifts only when something else changes, such as incomes, tastes or the price of tea.

Caption: When the price of a product rises, the curve does not move. The quantity demanded changes, and the point slides along the curve. Demand shifts only when something other than price changes. The wording matters, in a report and in a meeting. Which do people mix up more, demand or quantity demanded?
#edlintics #edlinticseconomics #edlinticsdemand

First comment: Try this: tea gets cheaper. Does the demand curve for coffee shift left, shift right, or stay put? Tea is a substitute, so people buy less coffee at every price. The curve shifts left.

Scores: R3 C4 D4 P5 = 16

---

## C07 | P32 | Statistics | Ninety-seven percent sure

Topic label: Statistics

1. Speaker: junior. State: junior proud, senior idle. Scene: Junior holds a report upright. Laptop screen shows "p = 0.03".
   Line: The test says p equals 0.03. We are 97% sure.
2. Speaker: senior. State: junior idle, senior thinking. Scene: Senior sets the mug down and removes the glasses, holding them at their side.
   Line: That is not what that number says.
3. Speaker: senior. State: junior idle, senior focused. Scene: Senior at a whiteboard sketches a bell curve with both tails shaded, together labelled "3%".
   Line: If nothing changed, results at least this extreme appear 3% of the time.
4. Speaker: junior. State: junior surprised, senior idle. Scene: Junior stands between the laptop and the whiteboard, report lowered to the side.
   Line: So it is a statement about the data, not the idea.

Punchline mechanism: reversal; confident certainty is quietly deflated by a precise definition.

Lesson slide: A p-value is the chance of seeing data at least this extreme if the null hypothesis were true. It is not the probability that your idea is true. If a new checkout raises the average order from $50 to $53 with p = 0.03, a result that large would show up about 3 times in 100 if the checkout changed nothing.

Caption: A p-value of 0.03 does not mean there is a 97% chance the idea works. It means that if nothing changed, data at least this extreme would appear about 3% of the time. That is a statement about the data under an assumption. It is useful, and it is narrower than it sounds. Where have you seen a p-value described loosely in a report?
#edlintics #edlinticsstatistics #edlinticspvalue

First comment: Follow-up: if a test shows p = 0.30, does that prove the checkout made no difference? Not quite. It means the data are not unusual under that assumption. A small sample can hide a real effect.

Scores: R4 C4 D3 P5 = 16

---

## C08 | P07 | Accounting | The adding is the easy part

Topic label: Accounting

1. Speaker: junior. State: junior idle, senior idle. Scene: Junior at the desk with a calculator and a long strip of receipt paper curling to the floor. Senior sits opposite.
   Line: Accounting is just adding things up, right?
2. Speaker: senior. State: junior idle, senior focused. Scene: Senior places one receipt on the desk. It reads "Server: $12,000".
   Line: Is this server an expense or an asset?
3. Speaker: junior. State: junior stuck, senior idle. Scene: Junior sits behind the receipt, calculator screen blank. Two small signs on the desk read "Expense this year" and "Asset over 4 years".
   Line: The calculator does not know either.
4. Speaker: senior. State: junior proud, senior thinking. Scene: Senior writes "$3,000 per year" on a sticky note and hands it across the desk. Junior takes it.
   Line: The adding takes four seconds. The deciding is the job.

Punchline mechanism: understatement; a hard question exposes the assumption without mocking anyone.

Lesson slide: Much of accounting is judgement about when and how to record a number, not the arithmetic itself. A $12,000 server that lasts 4 years, assuming no resale value, is recorded as an asset, then expensed at $3,000 a year through depreciation. Expensing the full $12,000 at once would understate profit this year and overstate it in the next three.

Caption: Accounting is often described as adding numbers. The arithmetic is the short part. The hard part is deciding what a number means and when it belongs. A $12,000 server is not an expense today. It is an asset that is used up over four years. What part of your job looks simple from outside?
#edlintics #edlinticsaccounting #edlinticsdepreciation

First comment: Question for the comments: a $12,000 server is expected to last 4 years and be worth $2,000 at the end. What is the yearly straight-line depreciation? Subtract the $2,000 first, then divide by 4.

Scores: R4 C4 D4 P4 = 16

---

## C10 | P23 | Business | The model chasing its tail

Topic label: Business

1. Speaker: junior. State: junior focused, senior idle. Scene: Junior at the laptop with a financial model open, a cell labelled "Interest: ?" highlighted. Three small linked boxes on screen: Interest, Debt, Cash.
   Line: Interest depends on debt, which depends on cash, which depends on interest.
2. Speaker: senior. State: junior stuck, senior thinking. Scene: Screen shows a warning triangle labelled "Circular reference". Junior sits back from the keyboard. Senior leans in, glasses catching the screen light.
   Line: The model is chasing its own tail.
3. Speaker: senior. State: junior thinking, senior focused. Scene: Senior stands at the screen beside a small looping arrow, and a straight arrow drawn next to it.
   Line: Charge interest on the opening debt instead.
4. Speaker: junior. State: junior resting, senior proud. Scene: Screen is clean and shows "Interest: $80,000". Both characters hold mugs, seated and relaxed.
   Line: That was one cell. I lost an afternoon.

Punchline mechanism: recognition and understatement; a large time cost traced to one cell.

Lesson slide: A circular reference appears when a formula depends on its own result, as when interest is calculated on a debt balance that the interest itself changes. Calculating interest on the opening balance removes the loop: 8% on $1,000,000 of debt is $80,000. Average-balance models are more precise, but they need iterative calculation switched on deliberately.

Caption: A circular reference is a formula that depends on its own answer. In a debt model, it happens when interest depends on a balance that interest changes. Using the opening balance breaks the loop with one small change. Have you ever lost an afternoon to a single cell?
#edlintics #edlinticsmodelling #edlinticsfinance

First comment: Question: if you use the average balance instead, which direction does interest move when cash flow improves? Lower, because the average debt falls. That is why some models keep the loop on purpose, with a switch to turn it off.

Scores: R3 C4 D4 P4 = 15

---

## Notes for review

- Dialogue format: each line sits in a speech bubble from its speaker (Hoang chose bubbles on 24 Oct 2026). The "Speaker" field tells the designer whose bubble it is.
- Facts to verify before publishing: C02 divisible-by-9 and halve-the-gap rules (standard bookkeeping rules, found in search summaries in the pain bank, S16); arithmetic checked for C05 (60,000 / 120,000 x 90 = 45), C09 (100 x 1.05 = 105; 105 x 1.02 = 107.10) and C08 (12,000 / 4 = 3,000).
- C07 panel 3 line is 13 words after the "at least" edit, one over the soft 12-word cap. It can be trimmed at design time if it will not fit.
- Hashtags are the requested three-tag pattern, not the calendar's reach-tag stack; the distribution lane may want to swap in reach tags.
