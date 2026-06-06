#!/usr/bin/env python3
"""
Generate the CMO -> CEO marketing proposal as a Word (.docx) document.
Brand voice: calm, direct, no exclamation points, no emoji (per config/brand.ts).
Output: docs/research/Edlintics-Marketing-Proposal-Fall-2026.docx
"""
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ---- Brand tokens (mirror config/brand.ts) -------------------------------
BLUE      = RGBColor(0x46, 0x7D, 0xE3)   # primary - edlintics blue
BLUE_DK   = RGBColor(0x36, 0x69, 0xCC)   # primary hover
INK       = RGBColor(0x02, 0x08, 0x17)   # foreground
MUTED     = RGBColor(0x64, 0x74, 0x8B)   # secondary text
ACCENT    = RGBColor(0x60, 0xA5, 0xFA)   # gradient terminus
EMERALD   = RGBColor(0x10, 0x98, 0x81)   # accounting / money accent
SANS = "Calibri"   # clean sans fallback for Inter

doc = Document()

# Base style
normal = doc.styles["Normal"]
normal.font.name = SANS
normal.font.size = Pt(10.5)
normal.font.color.rgb = INK
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.line_spacing = 1.15

def _shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)

def _set_cell_text(cell, text, bold=False, color=INK, size=9.5, white=False):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    r = p.add_run(text)
    r.font.name = SANS
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if white else color

def heading(text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14 if level == 1 else 9)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.font.name = SANS
    r.font.bold = True
    if level == 1:
        r.font.size = Pt(15)
        r.font.color.rgb = BLUE
        # blue rule under H1
        pPr = p._p.get_or_add_pPr()
        pbdr = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "6")
        bottom.set(qn("w:space"), "2")
        bottom.set(qn("w:color"), "467DE3")
        pbdr.append(bottom)
        pPr.append(pbdr)
    elif level == 2:
        r.font.size = Pt(12)
        r.font.color.rgb = INK
    else:
        r.font.size = Pt(10.5)
        r.font.color.rgb = BLUE_DK
    return p

def para(text, italic=False, color=INK, size=10.5, bold=False, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text)
    r.font.italic = italic
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.size = Pt(size)
    r.font.name = SANS
    return p

def bullet(text, bold_lead=None):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    if bold_lead:
        r = p.add_run(bold_lead)
        r.font.bold = True
        r.font.size = Pt(10.5)
        r.font.name = SANS
        r.font.color.rgb = INK
    r2 = p.add_run(text)
    r2.font.size = Pt(10.5)
    r2.font.name = SANS
    r2.font.color.rgb = INK
    return p

def table(headers, rows, widths=None, header_fill="467DE3"):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Table Grid"
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        _set_cell_text(hdr[i], h, bold=True, white=True, size=9.5)
        _shade(hdr[i], header_fill)
    for r_i, row in enumerate(rows):
        cells = t.add_row().cells
        for i, val in enumerate(row):
            _set_cell_text(cells[i], val, size=9.5)
            if r_i % 2 == 1:
                _shade(cells[i], "F1F5F9")
    if widths:
        for i, w in enumerate(widths):
            for cell in t.columns[i].cells:
                cell.width = Inches(w)
    return t

# ============================ TITLE BLOCK =================================
title = doc.add_paragraph()
title.paragraph_format.space_after = Pt(2)
r = title.add_run("Edlintics")
r.font.size = Pt(30); r.font.bold = True; r.font.name = SANS; r.font.color.rgb = INK
r2 = title.add_run("  -  Marketing Strategy Proposal")
r2.font.size = Pt(18); r2.font.bold = True; r2.font.name = SANS; r2.font.color.rgb = BLUE

sub = doc.add_paragraph()
sub.paragraph_format.space_after = Pt(2)
rs = sub.add_run("Fall 2026 Launch  -  Direction, Pillars, and the First 12 Weeks")
rs.font.size = Pt(12); rs.font.color.rgb = MUTED; rs.font.name = SANS

meta = doc.add_paragraph()
meta.paragraph_format.space_after = Pt(2)
for line in [
    "Prepared by: Marketing Manager",
    "For: Hoang Truong, Founder and CEO",
    "Date: 6 June 2026",
    "Status: Proposal for decision  -  nothing is locked until you approve",
]:
    rl = meta.add_run(line + "\n")
    rl.font.size = Pt(10); rl.font.color.rgb = MUTED; rl.font.name = SANS

# rule
hr = doc.add_paragraph()
pPr = hr._p.get_or_add_pPr()
pbdr = OxmlElement("w:pBdr")
bottom = OxmlElement("w:bottom")
bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), "12")
bottom.set(qn("w:space"), "1"); bottom.set(qn("w:color"), "467DE3")
pbdr.append(bottom); pPr.append(pbdr)

# ========================= 1. EXECUTIVE SUMMARY ===========================
heading("1.  Executive summary")
para("We launch on 1 September 2026, twelve weeks from now. Our buyer is a business "
     "undergraduate at a prestige European school who is quietly afraid of failing a specific "
     "exam. Demand for what we sell is not steady. It spikes hard with the autumn exam cycle: a "
     "midterm wave in mid-October to early November, a finals wave in early-to-mid December.")
para("The recommendation in one line: spend June to August building a library of worked, "
     "on-screen exam-problem content so that by the time the October panic arrives, we already "
     "rank and already have an audience. The binding constraint is time, not money. Content that "
     "is published in October is too late, because reach and search ranking take weeks to compound.")
para("Three content pillars carry the plan: (1) Worked, Not Watched, the flagship format that is "
     "itself a demonstration of our paid session; (2) The Concept You Will Be Tested On, a "
     "seasonal series timed to each exam wave; (3) What AI Gets Wrong, the differentiator that "
     "turns ChatGPT from a competitor into the reason our product exists.")
para("The market scan confirms the wedge is real. The exact-concept lane on TikTok is nearly "
     "empty (the financial-accounting hashtag holds roughly 4,000 videos against 4.2 million on "
     "the broad study hashtag), and the few creators who own it teach abstract concepts for a US "
     "professional audience, not exam-specific problems for European undergraduates. Nobody owns "
     "the thing our product already is.")
para("What I need from you is on the last page: five decisions and a green light to start "
     "filming the flagship problems in June.", bold=True)

# ========================= 2. THE SITUATION ===============================
heading("2.  The situation")
heading("Where we are", 3)
bullet("until launch. The product is built; this is the demand-generation gap.", "Twelve weeks ")
bullet("the European autumn exam cycle. The IE University calendar (our persona's school) starts "
       "31 August, clusters midterms in mid-to-late October, and ends classes 18 December with "
       "finals concentrated before it. LSE, HEC, ESCP and Bocconi follow the same shape.",
       "Demand is dictated by ")
bullet("a documentation product, not a tutoring product. So marketing has to sell the live "
       "session, not just the notes. Our north-star metric is session completion before the exam.",
       "The moat is the live screen-share session. Without it we sell ")
heading("What the market looks like right now", 3)
bullet("learn finance from TikTok and YouTube, but that is personal finance (budgeting, investing). "
       "Our buyer has the opposite intent: pass an academic exam. Same platforms, different universe.",
       "76 percent of Gen Z ")
bullet("the first three seconds drive about 80 percent of completion, completion matters more than "
       "length, and saves and shares (not likes) are what the algorithm rewards. A calm, useful, "
       "no-hype voice is an asset here, not a handicap.", "Short-form mechanics in 2026 reward usefulness: ")
bullet("a search engine for revision. Students type a concept they are stuck on and watch the top "
       "result. This rewards evergreen, concept-named content, which compounds in our favour over time.",
       "YouTube is functioning as ")

# ========================= 3. THE INSIGHT ================================
heading("3.  The strategic insight")
para("Three facts combine into one wedge that only Edlintics can occupy.")
bullet("the broad study hashtag has 4.2 million videos; the exact financial-accounting hashtag "
       "has about 4,000. The closer a concept is to an actual exam, the less competition exists.",
       "The exact-concept lane is open. On TikTok, ")
bullet("the leaders (for example the dominant financial-accounting creator on TikTok) teach "
       "concepts in the abstract for a US, CPA, finance-professional audience. None of them teach "
       "the specific kind of problem a European Year-1 undergraduate will face on a midterm.",
       "The incumbents aim elsewhere. ")
bullet("on accounting assessments, students still beat ChatGPT (roughly 77 percent against 47 "
       "percent). Accounting is a domain where AI is unreliable enough to be dangerous to lean on. "
       "That makes our message honest: AI gives you an answer; it cannot watch you try and stop you "
       "at the moment your reasoning breaks. That is the session.", "AI raises our value, it does not lower it: ")
para("The wedge: be the person who solves the exact problem your exam will ask, on screen, in the "
     "calm voice of someone who has done it, and who will then get on a call and watch you do it. "
     "That is not a content idea bolted onto the product. It is the product, filmed.", bold=True)

# ========================= 4. TARGET & POSITIONING ========================
heading("4.  Target and positioning")
heading("Who we are talking to", 3)
para("Sofia, 19, first-year business student at a prestige European school, studying in English, "
     "anxious about one specific exam in the next three to six weeks. She reads carefully, dislikes "
     "videos over ten minutes, studies on her phone between classes, and her priority order is: "
     "pass the exam, not feel stupid in front of a tutor, not waste her parents' money.")
heading("How we position", 3)
bullet("a concept is always the headline (T-accounts, cash-flow statements, consolidation, deferred "
       "tax). A university is named only as secondary context, never in the headline. This protects "
       "the brand on trademark and independence.", "Topic-led: ")
bullet("calm, expert, direct, practical, slightly serious. No exclamation points, no emoji, no hype. "
       "We earn attention with the idea. This voice is rare in the niche and it reads as the adult in "
       "the room.", "Voice: ")
bullet("we are not affiliated with any university, and we say so. The names appear as factual "
       "context for who the content is built for.", "Independent: ")

# ========================= 5. THE PILLARS ================================
heading("5.  The three content pillars")
para("Each pillar is a durable theme, not a campaign. Together they cover the full job: get found, "
     "build trust, and convert. Pillar 1 is the spine, Pillar 2 is the schedule it runs on, Pillar 3 "
     "is the sharpest differentiator.", italic=True, color=MUTED, size=10)

heading("Pillar 1  -  Worked, Not Watched", 2)
para("Calm, screen-recorded walk-throughs in which Hoang solves one exam-style problem in "
     "Excel or Sheets, narrating the reasoning and naming the exact point where students lose marks. "
     "The content is a direct preview of the paid session.")
table(
    ["Dimension", "Detail"],
    [
        ["Thesis", "Show the problem being solved, do not talk about solving problems."],
        ["Native format", "5-8 min worked example on YouTube (evergreen anchor), cut into 30-50s hooks for TikTok, Reels, Shorts."],
        ["Why it wins", "It is the moat, filmed. No competitor in the EU-undergraduate lane does on-screen worked problems in this voice."],
        ["Example", "\"The one consolidation step that costs you the marks\" - solved live, not described."],
        ["Primary KPI", "Saves and watch-through on short form; watch time and search impressions on YouTube."],
    ],
    widths=[1.4, 5.1],
)

heading("Pillar 2  -  The Concept You Will Be Tested On", 2)
para("A concept-per-week series reverse-engineered from the autumn exam cycle and front-loaded so "
     "each concept already ranks when its exam arrives. October carries the accounting-midterm "
     "concepts; December carries the finals concepts.")
table(
    ["Dimension", "Detail"],
    [
        ["Thesis", "Be the top result for the concept at the moment the student searches it."],
        ["Native format", "Short concept explainer plus a one-page reference; the explainer points to the Pillar 1 worked example."],
        ["Why it wins", "Demand is violently seasonal and ranking has lag. This is the mechanism that converts the season into pipeline."],
        ["Example", "Cash-flow statement, T-accounts, accruals vs deferrals, consolidation, deferred tax, CVP break-even."],
        ["Primary KPI", "Search impressions and ranking on named-concept queries; click-through to the offer."],
    ],
    widths=[1.4, 5.1],
)

heading("Pillar 3  -  What AI Gets Wrong", 2)
para("A recurring series that takes a concept where ChatGPT confidently misleads, shows the wrong "
     "answer, then the correct reasoning, and closes on why someone watching you try is the thing "
     "AI cannot replace.")
table(
    ["Dimension", "Detail"],
    [
        ["Thesis", "Reframe the student's default tool (ChatGPT) into the reason to buy."],
        ["Native format", "Short, punchy: the AI answer on screen, the error circled, the fix, the takeaway."],
        ["Why it wins", "AI is top of mind, accounting is where AI is measurably weak, and few finance creators run this angle credibly."],
        ["Example", "\"ChatGPT got this deferred-tax question wrong. Here is why, and why it matters in the exam.\""],
        ["Primary KPI", "Shares and comments (debate-driving); branded-search lift over time."],
    ],
    widths=[1.4, 5.1],
)

# ========================= 6. CHANNELS ===================================
heading("6.  Channel strategy")
para("Lead on YouTube, net with short form, support with communities and owned channels. The brand "
     "voice fits YouTube far better than TikTok hype culture, and YouTube captures the high-intent "
     "moment when Sofia is stuck and searching.")
table(
    ["Channel", "Role", "Why"],
    [
        ["YouTube", "Spine (primary)", "Search intent plus evergreen ranking plus a calm, longer voice. Captures the moment of need."],
        ["TikTok", "Net (discovery)", "Reaches Sofia before she searches. Saves are the currency. TikTok now rewards search-optimised teaching."],
        ["Instagram Reels", "Repurpose", "Shares to study groups (sends per reach). Treat as a repurpose target; it no longer reports hashtag size."],
        ["Reddit / Discord", "Helpfulness", "Course-specific communities where intent is explicit and reach is not algorithm-gated. Answer, do not sell."],
        ["Blog / email (owned)", "Capture and hold", "SEO concept articles and a list we own, not rented from an algorithm. Reinforces the seasonal push."],
        ["LinkedIn", "Defer", "Right for the alumni and employer story later, wrong for the anxious-undergraduate persona now."],
    ],
    widths=[1.5, 1.4, 3.6],
)
heading("Hashtag stack (TikTok / Reels)", 3)
para("Stack one tag per tier so a post gets both reach and intent: a big reach tag (study, "
     "accounting-student), a topic tag (accounting, business-school), the exact concept tag "
     "(financial-accounting plus the named concept), and a search tag (creator-search-insights, "
     "learn-on-tiktok). Avoid leaning on the personal-finance and corporate-finance tags for reach: "
     "the audience there has the wrong buying intent.", size=10)

# ========================= 7. CALENDAR ===================================
heading("7.  The seasonal plan (build now, harvest in the autumn)")
table(
    ["Window", "Student state", "Our posture"],
    [
        ["Jun - Aug", "Off for summer", "Build and plant. Film the worked-example library and the concept set. No selling. Goal: a ranked back-catalogue before anyone panics."],
        ["September", "New syllabi, low panic", "Awareness. Introduce the concept series gently. Establish the calm voice."],
        ["Mid-Oct - early Nov", "Midterm spike", "Harvest. Push accounting-midterm concepts hard. This is the primary conversion window."],
        ["Nov - mid-Dec", "Finals build then finals", "Bridge to finals concepts, then push through to about 18 December."],
        ["Late Dec - early Jan", "Winter break (dead air)", "Stop selling. Reflect-and-plan content only."],
        ["Mid-January", "Spring term starts", "Restart the cycle; the back-catalogue now compounds."],
    ],
    widths=[1.4, 1.7, 3.4],
)
para("This is the single most important slide. Reach and ranking take 8-plus weeks to build and "
     "three to six months to reach a working following. If we begin in October we miss the autumn "
     "entirely and wait a year for the next one.", bold=True, color=BLUE_DK, size=10.5)

# ========================= 8. FLAGSHIP TOPICS ============================
heading("8.  What to film first")
para("The research on where students struggle most points to a clear flagship set. These are the "
     "highest-pain, highest-search concepts and they map directly onto the five launch courses.")
table(
    ["Flagship topic", "Why it leads"],
    [
        ["Cash-flow statement (indirect method)", "Universally taught, universally feared; the classic Year-1 wall."],
        ["T-accounts and double-entry", "The foundation; high search volume; ideal first worked example."],
        ["Consolidation", "Named repeatedly as one of the hardest topics; little good undergraduate content exists."],
        ["Deferred tax", "High-difficulty, high-confusion; the natural anchor for the What-AI-Gets-Wrong pillar."],
        ["CVP / break-even analysis", "Management-accounting staple; quick to demonstrate on screen."],
    ],
    widths=[2.5, 4.0],
)

# ========================= 9. FUNNEL & TARGETS ==========================
heading("9.  Funnel and targets")
para("The company's own V1 success bar (vision.md) is 15 net-new paying customers within eight "
     "weeks of launch, spread across at least three of the five courses, with most completing their "
     "session. Marketing's job is to feed that. Working backwards with published benchmarks gives an "
     "honest sense of the reach required.")
table(
    ["Funnel stage", "Benchmark", "Implication for the autumn window"],
    [
        ["Course-page to purchase", "About 2-5% for a priced course page", "To net ~15 buyers, we need roughly 400-700 qualified course-page visits."],
        ["Content to course page", "Short form sends ~1-2% of engaged viewers to a link", "That implies tens of thousands of engaged views routed toward the offer across the season."],
        ["Audience build", "3-6 months to a working following; 4-6 posts/week; 8+ weeks before traction", "Confirms the build-now mandate. A standing start in October cannot clear the bar."],
        ["Owned capture", "Course landing pages convert far higher (13-18% median) than cold sales pages", "Email and SEO that pre-warm the visitor materially lift the final number."],
    ],
    widths=[1.7, 1.9, 2.9],
)
para("These figures are benchmark-based and illustrative, not a forecast. The point is directional: "
     "the target is reachable for a niche-fit account over a full season, and only if the catalogue "
     "is built before the season starts.", italic=True, color=MUTED, size=10)

# ========================= 10. RISKS & SCENARIOS ========================
heading("10.  Risks and scenarios")
table(
    ["Scenario / risk", "Response"],
    [
        ["Content build slips into September", "Triage to the October-critical accounting concepts only; narrow to one or two courses; accept a thinner net."],
        ["One worked example over-performs early", "Make that concept's course the launch hero; reorder the build queue around proven demand."],
        ["Low reach through September", "Shift weight to YouTube search and Reddit/Discord helpfulness, where intent is explicit and reach is not gated."],
        ["Cannibalisation without net-new buyers (4 wks)", "Treat as a signal the message or audience is off, per vision.md; re-test the hook before scaling effort."],
        ["Topic-led rule forfeits the highest-intent hook", "Accepted trade-off (see decision 2). We win the concept search and keep the school as secondary context."],
        ["One-operator bandwidth", "Engineer for fewer, deeper pieces; batch-film in June; repurpose one asset across every platform."],
    ],
    widths=[3.0, 3.5],
)
para("The honest headline risk: this is a single-operator, organic, build-ahead strategy. It trades "
     "speed for durability. It will not produce a viral spike in week one; it is designed to own a "
     "niche by October and compound from there.", color=MUTED, size=10)

# ========================= 11. DECISIONS NEEDED =========================
heading("11.  What I need from you")
para("Five decisions gate the plan. None require new spend; they require your judgement and a "
     "green light to start filming.", bold=True)
table(
    ["#", "Decision", "My recommendation"],
    [
        ["1", "Channels in scope", "YouTube primary; TikTok and Reels as repurpose; Reddit/Discord light-touch; defer LinkedIn."],
        ["2", "The trademark trade-off", "Accept staying strictly topic-led, forfeiting the branded-exam hook for legal safety and independence."],
        ["3", "Sustainable cadence", "Commit to a realistic, fewer-but-deeper cadence you can hold through the summer build."],
        ["4", "Lead courses", "Choose the one or two surest October converters to build the flagship worked examples around."],
        ["5", "Filming setup", "Confirm the screen-recording and clean-audio setup, or flag it as a gap to close before June filming."],
    ],
    widths=[0.4, 2.3, 3.8],
)

# ========================= 12. RECOMMENDATION ===========================
heading("12.  Recommendation")
para("Approve the three pillars, lead on YouTube with short form as the net, and begin filming the "
     "flagship worked examples in June. Build the catalogue through the summer so it is ranking and "
     "trusted before the October midterm panic. The product is already differentiated; the only "
     "question is whether we are visible at the moment the student is most afraid. With a twelve-week "
     "head start, we can be. Without it, we wait a year.", bold=True)
para("Nothing here is locked. On your approval, the surviving directions go into the content "
     "calendar as dated, trackable commitments, and we begin.", color=MUTED, size=10)

# ========================= APPENDIX =====================================
doc.add_page_break()
heading("Appendix A  -  Live TikTok hashtag scan (6 June 2026)")
para("Read live off each hashtag page; counts are TikTok's own and approximate. Public pages only; "
     "no account actions taken.", italic=True, color=MUTED, size=9.5)
table(
    ["Hashtag", "Videos", "Relevance"],
    [
        ["#studytok", "4.2M", "Reach (generic, much non-English)"],
        ["#accounting", "376K", "Mid reach"],
        ["#contabilidad", "354K", "Low (LatAm SMB / CPA, not EU exams)"],
        ["#fintok", "161.1K", "Low (personal finance, wrong intent)"],
        ["#accountingstudent", "70.6K", "High (struggle + how-to-pass)"],
        ["#businessschool", "43.9K", "Mid"],
        ["#corporatefinance", "5.6K", "Mid (careers, not coursework)"],
        ["#financialaccounting", "4.0K", "Highest (exact concept lane)"],
    ],
    widths=[2.2, 1.2, 3.1],
)
para("Instagram no longer publishes hashtag post counts, so it cannot be sized quantitatively; "
     "treat it as a repurpose target.", size=10)

heading("Appendix B  -  Sources")
sources = [
    "IE University 2026-2027 Academic Calendar (PDF)",
    "Gen Z financial-media behaviour: GOBankingRates; Fast Company; YR Media",
    "Short-form mechanics 2026: ALM Corp; JoinBrands (YouTube Shorts); Digital Applied",
    "Creator landscape: FeedSpot finance YouTubers and TikTok influencers",
    "AI and study: ScienceDaily; ScienceDirect (ChatGPT and student engagement)",
    "Hardest accounting topics: Brainscape; UWorld; PassAccountingClass; Research.com",
    "Growth and conversion benchmarks: Stackmatix; SeoSherpa; Acceleroi; Unbounce; Teachfloor",
    "Live hashtag scan: TikTok hashtag pages, 6 June 2026",
    "Full working notes: docs/research/2026-06-05-fall-launch-market-research.md and "
    "docs/research/2026-06-06-tiktok-instagram-hashtag-stats.md",
]
for s in sources:
    bullet(s)

para("")
para("Edlintics is independent and not affiliated with, endorsed by, or sponsored by any university.",
     italic=True, color=MUTED, size=9)

out = Path(__file__).resolve().parents[1] / "docs" / "research" / "Edlintics-Marketing-Proposal-Fall-2026.docx"
out.parent.mkdir(parents=True, exist_ok=True)
doc.save(str(out))
print("Saved:", out)
