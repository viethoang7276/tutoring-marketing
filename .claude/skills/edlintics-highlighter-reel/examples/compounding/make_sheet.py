"""Builds sheet.svg (960x1300 infographic) for the compounding highlighter reel and checks every number on it.
Run: python3 make_sheet.py   (writes sheet.svg and numbers.json next to this file)
Assumptions (stated on the sheet): $500 invested at the end of every month, 8% a year compounded monthly
(0.6667% a month), no fees, taxes or inflation. Milestones every $100K up to $1M.
"""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
P, i, STEP, K = 500.0, 0.08 / 12, 100_000, 10

# --- method 1: month-by-month loop
bal, m, bals, cross = 0.0, 0, [0.0], []
while len(cross) < K:
    m += 1; bal = bal * (1 + i) + P; bals.append(bal)
    while len(cross) < K and bal >= (len(cross) + 1) * STEP: cross.append(m)
# --- method 2: closed form for an ordinary annuity, n = ln(1 + FV i / P) / ln(1 + i), rounded up to whole months
cf = [math.ceil(math.log(1 + k * STEP * i / P) / math.log(1 + i)) for k in range(1, K + 1)]
assert cross == cf, (cross, cf)
steps = [cross[0]] + [cross[k] - cross[k - 1] for k in range(1, K)]
yrs = [round(s / 12, 1) for s in steps]
total = cross[-1]
share_first = steps[0] / total
deposits = P * total; final = bals[total]; growth_share = (final - deposits) / final
assert round(share_first * 100) == 32 and round(growth_share * 100) == 80, (share_first, growth_share)
assert steps[-1] == 14 and round(cross[0] / 12, 1) == 10.7
nums = {"months_to_milestone": cross, "years_to_milestone": [round(c / 12, 2) for c in cross], "step_months": steps,
        "step_years": yrs, "total_months": total, "first_step_share": round(share_first, 4), "deposits": deposits,
        "balance_at_end": round(final, 2), "growth_share": round(growth_share, 4),
        "share_of_time_per_step": [round(s / total, 4) for s in steps]}
json.dump(nums, open(f"{HERE}/numbers.json", "w"), indent=1)

# --- geometry (sheet coordinates)
X0, X1, YRS = 110, 900, 35
Y0, Y1 = 945, 470                  # $0 and $1M
sx = (X1 - X0) / YRS
def X(months): return X0 + sx * months / 12
def Y(b): return Y0 - (Y0 - Y1) * b / (K * STEP)
pts = [(X(k), Y(b)) for k, b in enumerate(bals[: total + 1])]
curve = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
dots = []
for k, c in enumerate(cross, 1):   # dot exactly where the balance crosses k x $100K (linear between months)
    target = k * STEP; b0, b1 = bals[c - 1], bals[c]; f = (target - b0) / (b1 - b0)
    dots.append((X(c - 1 + f), Y(target)))

INK, BLUE, MUTED, GRID = "#0F172A", "#467DE3", "#64748B", "#E2E8F0"
o = []
a = o.append
a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 1300" width="960" height="1300">')
a('<rect id="paper" x="0" y="0" width="960" height="1300" fill="#FFFFFF"/>')
a('<image href="edlintics-logo.png" x="370" y="34" width="220" height="57"/>')
a(f'<line x1="60" y1="118" x2="900" y2="118" stroke="{GRID}" stroke-width="3"/>')
# title
a(f'<text x="480" y="214" text-anchor="middle" font-family="Inter" font-weight="800" font-size="78" fill="{INK}" letter-spacing="-1.5">'
  f'The first <tspan id="t-100k">$100K</tspan></text>')
a(f'<text x="480" y="300" text-anchor="middle" font-family="Inter" font-weight="800" font-size="78" fill="{INK}" letter-spacing="-1.5">'
  f'is the <tspan id="t-slowest" fill="{BLUE}">slowest</tspan></text>')
# subtitle band
a(f'<rect x="60" y="338" width="840" height="76" rx="14" fill="#EEF4FD"/><rect x="60" y="338" width="10" height="76" rx="4" fill="{BLUE}"/>')
a(f'<text x="488" y="388" text-anchor="middle" font-family="Inter" font-weight="600" font-size="34" fill="{INK}">'
  f'You invest <tspan id="sub-500" font-weight="800">$500 a month</tspan> and earn <tspan id="sub-8" font-weight="800">8% a year</tspan></text>')
# chart: grid, axes, drop lines, curve, dots, labels
for k in range(1, K + 1):
    a(f'<line x1="{X0}" y1="{Y(k*STEP):.1f}" x2="{X1}" y2="{Y(k*STEP):.1f}" stroke="#F1F5F9" stroke-width="2"/>')
a(f'<line x1="{X0}" y1="{Y0}" x2="{X1+10}" y2="{Y0}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
a(f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1-30}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
for yr in (0, 10, 20, 30):
    a(f'<line x1="{X0+sx*yr:.1f}" y1="{Y0}" x2="{X0+sx*yr:.1f}" y2="{Y0+12}" stroke="{INK}" stroke-width="3"/>')
    a(f'<text x="{X0+sx*yr:.1f}" y="{Y0+46}" text-anchor="middle" font-family="Lato" font-weight="700" font-size="28" fill="{MUTED}">{yr}</text>')
a(f'<text x="{X1}" y="{Y0+46}" text-anchor="end" font-family="Lato" font-weight="700" font-size="28" fill="{MUTED}">years</text>')
a(f'<text x="{X0-14}" y="{Y0+8}" text-anchor="end" font-family="Lato" font-weight="700" font-size="26" fill="{MUTED}">$0</text>')
for k, (x, y) in enumerate(dots, 1):
    a(f'<line x1="{x:.1f}" y1="{y+10:.1f}" x2="{x:.1f}" y2="{Y0-4}" stroke="#94A3B8" stroke-width="2.5" stroke-dasharray="3 7" stroke-linecap="round"/>')
    a(f'<circle cx="{x:.1f}" cy="{Y0}" r="5" fill="{BLUE}"/>')
a(f'<path id="curve" d="{curve}" fill="none" stroke="{BLUE}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>')
for k, (x, y) in enumerate(dots, 1):
    lab = "$1M" if k == K else f"${k}00K"
    a(f'<circle id="dot{k}" cx="{x:.1f}" cy="{y:.1f}" r="9" fill="#FFFFFF" stroke="{BLUE}" stroke-width="5"/>')
    a(f'<text id="lab{k}" x="{x-18:.1f}" y="{y-10:.1f}" text-anchor="end" font-family="Lato" font-size="28" fill="{INK}">'
      f'<tspan font-weight="900">{lab}</tspan> <tspan id="yrs{k}" font-weight="700" fill="{BLUE}">+{yrs[k-1]:.1f} yrs</tspan></text>')
a(f'<text x="{X0+6}" y="{Y1-40}" font-family="Lato" font-weight="700" font-size="24" fill="{MUTED}">+ yrs is how long each $100K step takes</text>')
# stat cards: number on top, two lines of text under it
for j, (num, l1, l2, cx) in enumerate([("32%", "of the time goes to", "the first $100K", 60), ("80%", "of the $1M is growth,", "not your deposits", 495)], 1):
    a(f'<rect x="{cx}" y="1010" width="405" height="166" rx="18" fill="#F8FAFC" stroke="{GRID}" stroke-width="3"/>')
    a(f'<text id="s{j}num" x="{cx+202}" y="1076" text-anchor="middle" font-family="Inter" font-weight="800" font-size="64" fill="{BLUE}" letter-spacing="-1.5">{num}</text>')
    a(f'<text id="s{j}txt" x="{cx+202}" y="1116" text-anchor="middle" font-family="Inter" font-weight="600" font-size="26" fill="{INK}">{l1}</text>')
    a(f'<text x="{cx+202}" y="1150" text-anchor="middle" font-family="Inter" font-weight="600" font-size="26" fill="{INK}">{l2}</text>')
a(f'<text id="biz" x="480" y="1214" text-anchor="middle" font-family="Inter" font-weight="700" font-size="28" fill="{INK}">'
  f'A business that reinvests its profit compounds the same way</text>')
for k, line in enumerate(["Illustration only, not advice or a promise. Assumes $500 invested at the end of each month",
                          "and a steady 8% a year return, compounded monthly, with no fees, taxes or inflation",
                          "Real returns go up and down from year to year"]):
    a(f'<text x="480" y="{1244 + 23*k}" text-anchor="middle" font-family="Inter" font-weight="500" font-size="19" fill="{MUTED}">{line}</text>')
a('</svg>')
open(f"{HERE}/sheet.svg", "w").write("\n".join(o))
print("milestone months", cross); print("step years", yrs)
print(f"first step {share_first:.1%} of {total} months; deposits ${deposits:,.0f}; balance ${final:,.0f}; growth {growth_share:.1%}")
