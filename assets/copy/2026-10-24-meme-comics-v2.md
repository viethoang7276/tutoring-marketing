# Meme-comic scripts v2, 2026-10-24

Status: draft for brand review. Nothing approved or scheduled. Replaces v1 direction after Hoang's feedback: C02 (divisible-by-9) dropped, more spreadsheet jokes, one-glance single-image comics.

Machine-readable copy: `/private/tmp/claude-501/-Users-hoangtruong-Desktop-WebDevelopment-tutoring-edlintics-marketing/b1cda27f-49e5-4898-b02c-508c299fe887/scratchpad/meme/comics-v2.json`.

## Format

- Carousel of 3 slides. Slide 1 is the whole comic as one image: either a 2x2 grid (4-panel) or two tall panels side by side (2-panel). Slide 2 is "the real lesson", matching the "THE RULE" slide (one or two rule sentences plus a one-line takeaway). Slide 3 is the standard CTA slide.
- Speech bubbles, few words, lettered text. The last bubble is very short and flat; the deadpan reaction is the punch.
- Cast: Ledger characters only (book-shaped, blue bookmark, blue tie). Senior: glasses and grey cardigan. Junior: blue hoodie. Other roles are told apart by clothes (colleague: green scarf). Each speaking character is tagged with one of the 8 states (idle, cheerful, focused, thinking, proud, surprised, stuck, resting).
- The word "Excel" and any real brand never appear on art or in copy. The spreadsheet is called a spreadsheet, and the small grid creature in D11 is generic.
- Mix: 6 two-panel, 6 four-panel. Visual metaphors: D12 (month-end close as a mountain) and D11 (circular reference as a creature chasing its tail).
- Jokes are our own. The reference style supplied the mechanics only (one-image layout, flat last line, visual metaphor, 2-panel contrast).

## Ranking

| Rank | ID | Format | Subject | Premise | R | C | D | P | Total |
|---|---|---|---|---|---|---|---|---|---|
| 1 | D06 | 2-panel | business | The report says $10,000 profit, the bank says $1,200, payroll is $6,000. | 5 | 5 | 4 | 5 | 19 |
| 2 | D09 | 2-panel | economics | Inflation fell from 5% to 2%, yet the receipt says $107.10. | 5 | 4 | 5 | 5 | 19 |
| 3 | D07 | 4-panel | statistics | Umbrella sales and late trains rise together, and rain sits behind both. | 5 | 5 | 5 | 4 | 19 |
| 4 | D01 | 2-panel | workplace | The lookup works until a colleague adds one column and the price says Blue. | 5 | 5 | 4 | 4 | 18 |
| 5 | D05 | 2-panel | workplace | The crash recovers a file from 9:02, a minute after it was opened. | 5 | 5 | 5 | 3 | 18 |
| 6 | D08 | 4-panel | workplace | A net-30 invoice pays on day 62, so the pain becomes a metric. | 5 | 5 | 4 | 4 | 18 |
| 7 | D02 | 2-panel | workplace | The file is locked by Dana, who is at lunch, and the file is not. | 5 | 5 | 4 | 3 | 17 |
| 8 | D03 | 4-panel | workplace | An export opens with IDs stripped of zeros and one turned into a date. | 5 | 4 | 4 | 4 | 17 |
| 9 | D04 | 4-panel | workplace | A dragged formula moves the tax rate cell and row two says $0. | 4 | 4 | 4 | 5 | 17 |
| 10 | D12 | 4-panel | accounting | Month-end close as a mountain, a $2,400 March invoice rolls down at the summit. | 4 | 4 | 5 | 4 | 17 |
| 11 | D10 | 4-panel | workplace | Two people hold "the latest export" from different dates: $48,000 and $52,500. | 5 | 4 | 4 | 3 | 16 |
| 12 | D11 | 2-panel | business | A debt model's circular reference drawn as a creature chasing its tail. | 3 | 4 | 5 | 4 | 16 |

Spreadsheet jokes: D01, D02, D03, D04, D05, D11 (six; D10 is a seventh adjacent theme). Subjects: business 2, economics 1, statistics 1, accounting 1, workplace 7 (most of them spreadsheet pain).

Suggested posting order, so D06 and D08 (receivables and profit) are never adjacent: D01, D06, D05, D09, D03, D07, D12, D04, D08, D02, D11, D10.

---

## D06 | 2-panel | business | Profit versus cash (from C01)

Layout: two tall panels side by side. Topic label: Business.

Panel 1 (grey label "The report"): Junior holds a printed report upright; laptop beside it shows "Profit: $10,000". Senior seated nearby. States: junior cheerful, senior idle.
- Junior: "We made $10,000 this month."

Panel 2 (grey label "The bank"): Same desk. Laptop shows "Balance: $1,200". Wall calendar has Friday circled and "Payroll: $6,000". Senior turns the laptop toward junior. States: junior stuck, senior focused.
- Senior: "Payroll is $6,000. The bank has $1,200."
- Junior: "Noted."

Punchline mechanism: two-panel contrast; the one-word "Noted." is the flat deadpan punch.

Lesson slide. THE RULE: Profit counts a sale when it is earned, but payroll is paid from cash. A $16,000 sale on 60-day terms is revenue today and $0 in the bank until day 60.
Takeaway: Check cash flow, not just profit.

Caption: A business can report a $10,000 profit and still be unable to cover a $6,000 payroll. Profit counts a sale when it is earned. The bank records it when the customer pays. Both numbers are true, and they answer different questions. Have you ever seen a profitable month with a thin bank balance?
#edlintics #edlinticsprofit #edlinticscashflow

First comment: When you read a statement, find operating cash flow before you judge the profit line. If profit rises while operating cash flow falls, ask where the money is stuck. Receivables and inventory are the usual answer.

Scores: R5 C5 D4 P5 = 19

---

## D09 | 2-panel | economics | Slower is not cheaper (from C09)

Layout: two tall panels side by side. Topic label: Economics.

Panel 1 (grey label "The headline"): Junior at the laptop showing a falling chart labelled "Inflation: 5% to 2%". A basket of bread and eggs on the desk. States: junior cheerful.
- Junior: "Inflation fell from 5% to 2%."

Panel 2 (grey label "The receipt"): Junior holds a receipt reading "$107.10" beside the basket. Senior at a notepad has drawn three rising steps labelled "$100", "$105", "$107.10". States: junior thinking, senior focused.
- Senior: "Prices still rose. Just more slowly."
- Junior: "Slower is not cheaper."

Punchline mechanism: two-panel contrast between the headline and the receipt; the junior's four-word summary is the punch.

Lesson slide. THE RULE: Inflation is the rate at which prices rise, so a falling rate means prices rise more slowly, not that they fall. A $100 basket becomes $105 at 5%, then $107.10 a year later at 2%.
Takeaway: A lower rate is still a higher price.

Caption: When inflation falls from 5% to 2%, prices have not gone down. They are rising more slowly, on top of the earlier increases. That is why the headline and the receipt can feel like they disagree. Which price do you check first to judge the cost of living?
#edlintics #edlinticseconomics #edlinticsinflation

First comment: For the price level itself to fall you need negative inflation, called deflation. Starting from the $105 basket, minus 1% would bring it to $103.95, still above the $100 starting point.

Scores: R5 C4 D5 P5 = 19

---

## D07 | 4-panel | statistics | Umbrellas and late trains (from C03)

Layout: 2x2 grid. Topic label: Statistics.

1. Junior at the laptop; screen shows a line chart with two rising lines labelled "Umbrella sales" and "Late trains". Senior seated behind. States: junior focused, senior idle.
   - Junior: "Umbrella sales and late trains rise together."
2. Junior leans toward the screen holding a closed umbrella like a pointer. States: junior thinking, senior idle.
   - Junior: "Should we ban umbrellas?"
3. Senior at a whiteboard draws a small rain cloud above both lines with an arrow down to each. States: junior idle, senior focused.
   - Senior: "Look behind both lines."
4. Junior hangs the umbrella on the chair and opens a weather forecast on the laptop. States: junior proud, senior idle.
   - Junior: "Checking the forecast."

Punchline mechanism: reversal; the flat two-word action replaces the wrong conclusion.

Lesson slide. THE RULE: Two lines that rise together do not show that one causes the other. A hidden third factor, such as rain, can drive both.
Takeaway: Before blaming one line, ask what could move both.

Caption: Two lines rising together is a pattern, not an explanation. Before you read a cause into a correlation, look for a third factor that could drive both. Here it is the rain. The same check works on sales reports, survey results and any chart that arrives in a meeting. What is the best false cause you have been shown?
#edlintics #edlinticsstatistics #edlinticscorrelation

First comment: If you wanted to test whether umbrellas really affect train delays, how would you design it? You would need to hold the weather fixed, or hand out umbrellas at random.

Scores: R5 C5 D5 P4 = 19

---

## D01 | 2-panel | workplace | The lookup and the new column

Layout: two tall panels side by side. Topic label: Workplace.

Panel 1: Junior at the laptop. Screen shows a row "Widget" with "Price: $40". States: junior cheerful.
- Junior: "The lookup finally works."

Panel 2: Same desk the next morning. Screen shows "Widget" with "Price: Blue". A colleague (green scarf) stands in the doorway holding a laptop. States: junior stuck, colleague idle.
- Junior: "Why does the price say Blue?"
- Colleague: "I added a column."

Punchline mechanism: reversal plus understatement; the colleague's four flat words explain everything.

Lesson slide. THE RULE: A lookup that finds its answer by counting columns breaks when someone inserts a column. A lookup that points at the answer column moves with it.
Takeaway: Point at the column, not at its position.

Caption: A spreadsheet lookup can be right on Monday and wrong on Tuesday without anyone touching it. If it counts columns by number, one inserted column changes the answer. Pointing at the answer column instead lets the formula follow it. What is the quietest spreadsheet break you have found?
#edlintics #edlinticsspreadsheets #edlinticslookup

First comment: After any structural change, test one row whose answer you can name from memory. If the Widget should cost $40 and the sheet says Blue, you will know in ten seconds.

Scores: R5 C5 D4 P4 = 18

---

## D05 | 2-panel | workplace | Recovered from 9:02

Layout: two tall panels side by side. Topic label: Workplace.

Panel 1: Wall clock reads 6:10. Junior at the laptop with a full sheet of numbers and a small box labelled "Not responding". Senior at the next desk. States: junior focused, senior idle.
- Junior: "Three hours of work. About to save."

Panel 2: Laptop shows a recovery pane labelled "Recovered version: saved 9:02 am" beside an empty grid. Junior slumps in the chair. Senior holds a mug. States: junior resting, senior idle.
- Junior: "The recovered file is from 9:02."
- Senior: "You opened it at 9:01."

Punchline mechanism: recognition and deadpan; the senior's single fact finishes the joke.

Lesson slide. THE RULE: A recovery copy is only as recent as the last save or autosave. Turn autosave on, and save by hand after any change you would hate to redo.
Takeaway: Save when the work is good, not when it is finished.

Caption: A crash does not take the file. It takes everything since the last save. Autosave narrows the gap, but only if it is switched on and the file lives somewhere that supports it. Saving by hand closes the rest. When did you last lose a few hours of work?
#edlintics #edlinticsspreadsheets #edlinticsproductivity

First comment: A quick audit: open the file you work in most, find the autosave setting, and read the time of the last save. If it says 9:02 and it is now 6:10, you have your answer.

Scores: R5 C5 D5 P3 = 18

---

## D08 | 4-panel | workplace | Day sixty-two (from C05)

Layout: 2x2 grid. Topic label: Workplace.

1. Junior at the laptop; screen shows "Invoice: $6,000, due in 30 days" beside a send button. States: junior cheerful, senior idle.
   - Junior: "Invoice sent. Due in thirty days."
2. Wall calendar with days crossed off and "Day 30" circled. Laptop shows an empty inbox. Senior stands with a coffee facing the calendar. States: junior idle, senior thinking.
   - Senior: "Day thirty. Bank balance unchanged."
3. Calendar reads "Day 47". Junior slumps over the keyboard. Three sent-mail icons on screen. States: junior stuck, senior idle.
   - Junior: "Three polite reminders so far."
4. Laptop shows "Payment received: $6,000". Calendar reads "Day 62". Junior leans back. Senior writes the number on a notepad. States: junior resting, senior proud.
   - Senior: "Day sixty-two. Now we measure it."

Punchline mechanism: recognition, then a dry pivot; the pain becomes a metric.

Lesson slide. THE RULE: Days sales outstanding is receivables divided by credit sales, multiplied by the days in the period. $60,000 of receivables on $120,000 of credit sales over 90 days is 45 days.
Takeaway: Measure how long customers take, not just whether they pay.

Caption: Net 30 is a term, not a guarantee of payment. When invoices arrive late, the delay is a number you can track. Days sales outstanding turns a vague frustration into a trend you can bring to a meeting. How long do your invoices usually take to get paid?
#edlintics #edlinticsreceivables #edlinticsfinance

First comment: At $120,000 of credit sales over 90 days, one day of DSO is about $1,333 of cash tied up. Cutting DSO from 45 days to 40 would free roughly $6,667. Which lever would you pull first, earlier invoices or firmer terms?

Scores: R5 C5 D4 P4 = 18

---

## D02 | 2-panel | workplace | Locked by Dana

Layout: two tall panels side by side. Topic label: Workplace.

Panel 1: Wall clock 12:40, sticky note "Report due 1:00". Junior at the laptop; screen shows a box "File in use. Locked for editing by Dana." States: junior stuck, senior idle.
- Junior: "Dana has the file locked."

Panel 2: Senior at the desk with a mug. A small inset shows Dana (green scarf) at a lunch table with a bowl of soup, laptop bag closed beside her. States: junior stuck, senior idle, colleague resting.
- Senior: "Dana is at lunch. The file is not."

Punchline mechanism: reversal; the file is more present than the person.

Lesson slide. THE RULE: A file left open on one computer stays locked for editing on every other until it is closed. Save shared work where several people can edit at once.
Takeaway: Close the file before you leave your desk.

Caption: A locked file is a small problem with a bad sense of timing. It stays locked as long as it stays open somewhere, including on a laptop in a bag. Co-editing in a shared location removes most of it. What is the worst moment a file has been locked on you?
#edlintics #edlinticsspreadsheets #edlinticsteamwork

First comment: When a file is locked, ask who holds it before making a copy. A second copy solves the next ten minutes and recreates the version problem for the next ten weeks.

Scores: R5 C5 D4 P3 = 17

---

## D03 | 4-panel | workplace | The helpful file

Layout: 2x2 grid. Topic label: Workplace.

1. Junior opens an export file; screen shows a column "ID" with "00417" in the first row. States: junior cheerful, senior idle.
   - Junior: "Opening the export now."
2. Same screen; the first row now shows "417". Junior leans forward. States: junior focused, senior idle.
   - Junior: "My IDs lost their zeros."
3. A second row with ID "3-12" now reads "12-Mar". Junior sits back. States: junior surprised, senior idle.
   - Junior: "And one became a date."
4. Senior stands beside the desk with a coffee, looking at the screen. States: junior stuck, senior idle.
   - Senior: "The file thinks it is helping."

Punchline mechanism: understatement; personifies the software as an overeager helper in six words.

Lesson slide. THE RULE: Opening a CSV file makes the program guess each column's type, so text IDs can turn into numbers or dates. Import the column as text and the zeros stay.
Takeaway: Tell the program the type. Do not let it guess.

Caption: An ID is a label, not a number, but a spreadsheet will not always agree. Opening a CSV file can strip leading zeros or turn an ID into a date. Importing the column as text keeps it exactly as it was exported. What is the strangest thing a file has done to your data on opening?
#edlintics #edlinticsspreadsheets #edlinticsdata

First comment: A check worth running after every import: sort the ID column and look at the first and last rows. If the shortest ID has fewer characters than the longest, something was stripped.

Scores: R5 C4 D4 P4 = 17

---

## D04 | 4-panel | workplace | Dollar signs

Layout: 2x2 grid. Topic label: Workplace.

1. Junior at the laptop; screen shows a sales column, a tax rate "8%" in a single cell, and the first row "$100" next to "$108". A drag handle sits at the corner of the cell. States: junior cheerful, senior idle.
   - Junior: "One formula, dragged down."
2. Same screen; the second row shows "$250" next to "$0". Junior leans toward the screen. States: junior stuck, senior idle.
   - Junior: "Row two says zero."
3. Senior at the whiteboard draws the tax rate cell with an arrow sliding down one row, off the cell. States: junior thinking, senior focused.
   - Senior: "The reference slid down with the formula."
4. Screen shows "$C$1" highlighted and both rows correct. Senior holds a coffee. States: junior proud, senior idle.
   - Junior: "Dollar signs. Of course."

Punchline mechanism: recognition; the junior's flat sign-off treats an hour of confusion as obvious.

Lesson slide. THE RULE: A relative reference shifts when you copy a formula, while an absolute reference written with dollar signs, such as $C$1, stays fixed. Lock any cell that every row should share.
Takeaway: Lock the rate, not the row.

Caption: When you drag a formula down, every reference moves with it unless you tell it not to. A tax rate in one cell needs dollar signs so every row keeps pointing at it. Without them, row two quietly multiplies by an empty cell. What is the first spreadsheet shortcut you wish you had learned sooner?
#edlintics #edlinticsspreadsheets #edlinticsformulas

First comment: A fast way to catch this: click into a formula three rows down and read which cell it points to. If the rate cell has changed from C1 to C3, the reference was not locked.

Scores: R4 C4 D4 P5 = 17

---

## D12 | 4-panel | accounting | The month-end mountain (visual metaphor)

Layout: 2x2 grid. Topic label: Accounting.

1. A tall mountain in simple outline, small flags labelled "Accruals", "Reconciliations", "Review". Label at the base: "Month-end close". Junior at the base wearing a ledger as a backpack; senior beside. States: junior cheerful, senior idle.
   - Junior: "It looks manageable from here."
2. Halfway up. Junior climbs past the "Accruals" flag; senior a step behind. States: junior focused, senior idle.
   - Junior: "Accruals done."
3. Near the summit a round boulder rolls down the slope labelled "Invoice: $2,400, dated March". Junior stands braced in front of it. States: junior surprised, senior focused.
   - Senior: "It belongs to this month."
4. Junior sits on the summit beside the "Review" flag, backpack off. Behind, a second mountain labelled "Next month" rises. States: junior resting, senior idle.
   - Junior: "Another mountain."

Punchline mechanism: visual metaphor with a flat three-word reaction; the close is a mountain that keeps reappearing.

Lesson slide. THE RULE: Accrual accounting records an expense in the month it is incurred, so a $2,400 supplier invoice for March services belongs in March even if it arrives in April.
Takeaway: Book it where it belongs, not when it arrives.

Caption: The month-end close is a climb with a fixed route: accruals, reconciliations, then review. A late invoice does not change which month it belongs to. It changes how much you have to move before you reach the top. Which step of the close takes the longest where you work?
#edlintics #edlinticsaccounting #edlinticsmonthend

First comment: If the $2,400 March invoice arrives after the books are closed, you can still record an accrual in March for an estimate and reverse it when the invoice is entered. Which would your team do, accrue or reopen the period?

Scores: R4 C4 D5 P4 = 17

---

## D10 | 4-panel | workplace | Two exports and a meeting (from C04)

Layout: 2x2 grid. Topic label: Workplace.

1. Junior at one laptop; screen shows "Budget export: Mar 3, total $48,000". States: junior focused, senior idle.
   - Junior: "This is the latest budget export."
2. Senior turns a second laptop toward the camera; screen shows "Budget export: Mar 10, total $52,500". States: junior idle, senior focused.
   - Senior: "So is this."
3. The two laptops face each other on the desk; a sticky note between them reads "$4,500". States: junior thinking, senior thinking.
   - Junior: "We exported on different days."
4. Both characters sit very still, laptops half closed; a wall calendar shows a meeting marked. States: junior stuck, senior stuck.
   - Senior: "One budget. Two totals. A meeting."

Punchline mechanism: recognition and understatement; the closing three-beat line summarises the whole office.

Lesson slide. THE RULE: Exports taken on different dates will disagree without anyone being wrong. Keep one master file and put the export date in every file name.
Takeaway: Date every export.

Caption: Two people can both hold the latest export and still disagree. When the exports come from different days, a $4,500 difference becomes a meeting about whose spreadsheet is right. One master file and dated exports reduce it. How many versions of your budget file exist right now?
#edlintics #edlinticsspreadsheets #edlinticsbudgeting

First comment: A small habit worth copying: put the date and the author's initials in the change log every time a total moves. It takes ten seconds and answers the question before anyone asks it.

Scores: R5 C4 D4 P3 = 16

---

## D11 | 2-panel | business | The model chasing its tail (from C10, visual metaphor)

Layout: two tall panels side by side. Topic label: Business.

Panel 1 (grey label "The model"): Junior at the laptop. On screen a small generic grid creature runs in a circle chasing its own tail, labelled "Circular reference". A highlighted cell reads "Interest: ?". States: junior stuck, senior idle.
- Junior: "Interest depends on debt. Debt depends on interest."

Panel 2 (grey label "The fix"): The grid creature sits still, tail beside it. The cell reads "Interest: $80,000". Senior points to a cell labelled "Opening debt". Junior leans back. States: junior resting, senior focused.
- Senior: "Use the opening balance."
- Junior: "One cell. One afternoon."

Punchline mechanism: visual metaphor, then a flat two-beat reaction that prices the mistake.

Lesson slide. THE RULE: A circular reference is a formula that depends on its own result. Charging interest on the opening balance breaks the loop: 8% on $1,000,000 of debt is $80,000.
Takeaway: Interest on the opening balance never needs its own answer.

Caption: A circular reference is a formula that depends on its own answer. In a debt model, it happens when interest depends on a balance that interest changes. Using the opening balance breaks the loop with one small change. Have you ever lost an afternoon to a single cell?
#edlintics #edlinticsmodelling #edlinticsspreadsheets

First comment: If you use the average balance instead, which direction does interest move when cash flow improves? Lower, because the average debt falls. That is why some models keep the loop on purpose, with a switch to turn it off.

Scores: R3 C4 D5 P4 = 16

---

## Notes for review

- The pivot-table and shrinking-pizza ideas were not used; twelve slots were taken by the five required spreadsheet jokes, the five v1 keepers and C10. The pizza budget metaphor is a good next candidate.
- Facts to verify: D12 accrual treatment (matches standard accrual accounting and reversing-entry practice); D03 text-import behaviour of CSV files (common across spreadsheet programs, not brand-specific); D05 and D02 describe general behaviour of autosave and file locking, which varies by program and storage location. Arithmetic checked: D06 numbers, D08 (60,000 / 120,000 x 90 = 45), D09 (100 x 1.05 x 1.02 = 107.10), D11 (8% of $1,000,000 = $80,000).
- Hashtags are the requested three-tag pattern, not the calendar's reach-tag stack.
- D07 uses a classic hidden-cause teaching pattern; the joke is our own.
