#!/usr/bin/env python3
"""Render the four quiz proofs. Requires CairoSVG; SVG sources are tracked, PNGs are generated."""
from pathlib import Path
from html import escape
import cairosvg
ROOT=Path(__file__).resolve().parent.parent
O=ROOT/'assets/quiz-samples'; O.mkdir(parents=True,exist_ok=True)
RASTER=ROOT/'assets/renders/quiz-samples'; RASTER.mkdir(parents=True,exist_ok=True)
B='#467DE3'; I='#0D1523'; M='#64748B'; E='#168768'; L='#EAF1FD'
def text(x,y,s,size=34,color=I,weight=600): return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(str(s))}</text>'
def box(x,y,w,h,fill=L): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="24" fill="{fill}"/>'
def line(x,y,a,b,color=B):return f'<path d="M{x} {y}L{a} {b}" stroke="{color}" stroke-width="5" fill="none"/>'
def choices(vals):
 s=''
 for j,v in enumerate(vals):
  x=30+j*310;s+=box(x,670,290,100,'#F4F6F9')+text(x+145,733,chr(65+j)+'  '+v,31)
 return s+text(490,823,'Choose your answer. Swipe for the reasoning.',25,M,400)
def save(name,body):
 s='<svg xmlns="http://www.w3.org/2000/svg" width="980" height="850" viewBox="0 0 980 850"><rect width="980" height="850" fill="white"/>'+body+'</svg>'
 (O/(name+'.svg')).write_text(s);cairosvg.svg2png(bytestring=s.encode(),write_to=str(RASTER/(name+'.png')))
# Accounting: parallel movements make the balance-sheet change visible.
s=text(490,65,'A business borrows €1,000 from a bank.',36)+text(490,110,'Ignore interest and fees.',27,M,400)
for x,title,label in [(40,'CASH','+ €1,000'),(520,'LOAN OWED','+ €1,000')]:
 s+=box(x,180,420,350)+text(x+210,250,title,28,M)+text(x+210,378,label,58,B)+text(x+210,455,'on the balance sheet',25,M,400)
s+=text(490,598,'What happens to profit?',38)
s+=choices(['Up €1,000','No change','Down €1,000']);save('accounting-question',s)
s=text(490,95,'B  ·  Profit does not change',48,E)+box(40,185,900,270)+text(490,260,'Assets = Liabilities + Equity',42)+text(490,365,'+ €1,000 = + €1,000 + €0',48,B)+text(490,550,'Borrowing creates an obligation to repay.',32)+text(490,605,'It is not income earned by the business.',32)+text(490,770,'Cash received ≠ revenue earned',37,E);save('accounting-answer',s)
# Finance: visible sequence, exact base values on reveal.
s=text(490,80,'Start with €100',44)+box(40,170,390,270)+text(235,242,'FIRST MOVE',27,M)+text(235,350,'+20%',78,B)+box(550,170,390,270)+text(745,242,'SECOND MOVE',27,M)+text(745,350,'−20%',78,B)+line(455,305,520,305)+text(490,555,'€100  →  ?  →  ?',60)+choices(['€96','€100','€104']);save('finance-question',s)
s=text(490,80,'A  ·  You finish with €96',48,E)+box(45,160,890,370)+text(490,250,'€100 × 1.20 = €120',51,B)+text(490,365,'€120 × 0.80 = €96',51,B)+text(490,465,'The loss is €24. The gain was €20.',32)+text(490,635,'Equal percentages use different bases.',33)+text(490,775,'+20% then −20% is a 4% loss.',37,E);save('finance-answer',s)
# Economics: either/or output possibilities with a common time budget.
s=text(490,60,'What each maker can produce in one day',34)+text(490,110,'Choose one product per day.',27,M,400)
for x,name,t,c in [(40,'MAYA',4,8),(520,'LEO',3,3)]:
 s+=box(x,170,420,380)+text(x+210,235,name,33,B)+text(x+210,330,str(t)+' tables',48)+text(x+210,390,'OR',25,M)+text(x+210,475,str(c)+' chairs',48)
s+=text(490,615,'Who gives up fewer chairs per table?',31)+choices(['Maya','Leo','Same cost']);save('economics-question',s)
s=text(490,80,'B  ·  Leo',51,E)+text(490,140,'Compare the chairs given up for one table.',31)
for x,name,a,b in [(40,'MAYA','8 ÷ 4','2 chairs'),(520,'LEO','3 ÷ 3','1 chair')]:
 s+=box(x,220,420,330)+text(x+210,280,name,30,M)+text(x+210,380,a,61,B)+text(x+210,470,b,44)
s+=text(490,660,'Leo has the lower opportunity cost.',35)+text(490,780,'That is comparative advantage.',37,E);save('economics-answer',s)
# Statistics: 1:3 visual weighting, figures are explicitly means.
s=text(490,60,'Two groups take the same test.',35)
for x,label,n,avg in [(40,'GROUP A',10,60),(520,'GROUP B',30,80)]:
 s+=box(x,130,420,440)+text(x+210,195,label,28,M)+text(x+210,275,str(n)+' students',42)+text(x+210,345,'Mean score: '+str(avg),34,B)
 for j in range(n):s+=f'<circle cx="{x+65+(j%10)*32}" cy="{410+(j//10)*48}" r="10" fill="{B}"/>'
s+=choices(['70','75','80']);save('statistics-question',s)
s=text(490,75,'B  ·  The combined mean is 75',45,E)+box(40,170,900,370)+text(490,245,'10 × 60 + 30 × 80',52,B)+line(170,275,810,275,I)+text(490,340,'10 + 30',52,B)+text(490,450,'3,000 ÷ 40 = 75',47)+text(490,635,'Group B has three times as many students.',31)+text(490,700,'Its mean needs three times the weight.',31)+text(490,800,'Do not average averages without weights.',32,E);save('statistics-answer',s)
print('Created 8 diagrams')
