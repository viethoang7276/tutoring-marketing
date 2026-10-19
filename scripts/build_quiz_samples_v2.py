from pathlib import Path
import re, html
import cairosvg
R=Path(__file__).resolve().parent.parent
O=R/'assets/quiz-samples-v2';O.mkdir(exist_ok=True)
P=R/'assets/renders/quiz-samples-v2';P.mkdir(exist_ok=True)
def t(x,y,s,n=32,c='#020817'):
 return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Arial" font-size="{n}" fill="{c}">{html.escape(s)}</text>'
def rect(x,y,w,h,c='#EAF1FD'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{c}"/>'
def char(n,x,y,w=180):
 s=(R/f'assets/brand/{n}.svg').read_text();s=re.sub(r'<svg[^>]*>',f'<svg x="{x}" y="{y}" width="{w}" height="{w*270/240}" viewBox="0 0 240 270">',s,count=1);return s

def save(n,s):
 s=f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="900" viewBox="0 0 900 900"><rect width="900" height="900" fill="white"/>{s}</svg>'
 (O/(n+'.svg')).write_text(s);cairosvg.svg2png(bytestring=s.encode(),write_to=str(P/(n+'.png')))
for answer in [False,True]:
 s=rect(45,40,810,110)+t(450,88,'TICKET PRICE CAP',24,'#64748B')+t(450,133,'€10 per ticket',39,'#467DE3')
 s+=rect(45,180,810,350,'#F5F8FE')
 for i in range(6):
  x=105+(i%3)*260;y=220+(i//3)*135
  s+=f'<rect x="{x}" y="{y}" width="170" height="95" rx="10" fill="white" stroke="#467DE3" stroke-width="3"/>'+t(x+85,y+58,'TICKET',23,'#467DE3')
 s+=t(450,580,'6 tickets available · 10 buyers',36)
 s+=char('centi',65,620,170)+char('ledger',660,615,175)
 if answer:s+=t(450,690,'4 buyers miss out',36,'#467DE3')+t(450,747,'10 wanted − 6 available',26)+t(450,795,'Shortage = 4 tickets',28)
 else:s+=t(450,690,'Each buyer wants one.',28)+t(450,743,'How many miss out?',31)+t(450,805,'A  0     B  4     C  6',30,'#467DE3')
 save('ticket-shortage-'+('answer' if answer else 'question'),s)
for answer in [False,True]:
 s=char('centi',35,0,160)+char('ledger',700,0,160)+t(450,80,'TWO CAFÉS. ONE DECISION.',30,'#467DE3')+t(450,130,'Profit per café per day',26,'#64748B')
 s+=t(540,225,'CAFÉ B',30,'#467DE3')+t(405,285,'Keep price',27)+t(675,285,'Discount',27)
 s+=t(130,440,'CAFÉ A',27,'#467DE3')+t(130,490,'Keep price',24)+t(130,650,'Discount',24)
 vals=[(270,330,'€60 / €60'),(540,330,'€20 / €80'),(270,550,'€80 / €20'),(540,550,'€40 / €40')]
 for x,y,v in vals:s+=rect(x,y,250,190,'#DCE8FC' if answer and x==540 and y==550 else '#F0F5FD')+t(x+125,y+108,v,31)
 s+=t(450,800,'Each cell shows: Café A / Café B',25,'#64748B')
 s+=t(450,860,'Both discount: €40 each.' if answer else 'They choose once, without coordinating.',28,'#467DE3')
 save('cafe-pricing-'+('answer' if answer else 'question'),s)
print(P)
