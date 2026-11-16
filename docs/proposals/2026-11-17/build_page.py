"""Build the local HTML proposal page for the 17 Nov 2026 script proposals.

Run: python3 docs/proposals/2026-11-17/build_page.py  (writes index.html next to this file)
"""
import glob
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

ORDER = {"ladder": 0, "map": 1, "big4": 2}
GROUP_NAME = {"ladder": "Career ladder reels", "map": "Career cities map reels", "big4": "New idea: Big 4 departments"}

# Lead review notes (Claude, 17 Nov 2026): what Hoang should look at first on each reel
LEAD = {
    "team-big4-departments": "Needs your call on the 30-day related rule: the audit ladder (13 Nov) and consultant ladder (16 Nov) are close, so 26 Nov needs a waiver, or it moves to 14 Dec or later. PwC's current department names could not be opened (pwc.com blocked the reader), so the script only uses names confirmed on every firm",
    "ladder-pharmacy-technician-to-operations-manager": "Weakest ladder: no source names the top rung. My suggestion is to swap it for a backlog career, such as flight attendant to head of cabin services",
    "ladder-bank-teller-to-regional-manager": "Only one source covers the manager rungs; one more is needed before the build",
    "ladder-apprentice-electrician-to-electrical-contractor": "The owner rung rests on two government career pages, and neither describes the owner's daily work in detail",
    "ladder-hr-assistant-to-chief-people-officer": "Skips the HR director rung to keep five rungs; titles vary a lot by company size",
    "ladder-sales-associate-to-regional-manager": "Sources say 'several stores across a region' but never 'regional manager' as a title",
    "ladder-salon-apprentice-to-salon-owner": "The team leader rung is really a senior stylist role in most salons",
    "ladder-trainee-property-agent-to-agency-owner": "Two rungs are not named on the source pages; fine for a ladder, flagged for honesty",
    "map-career-cities-6-asia-1": "Nine stops. Haier, Hisense and Huawei head offices are only 'home to' on Wikipedia; Hyundai is a plant, not a head office. Ulaanbaatar has no company logo",
    "map-career-cities-7-asia-2": "Nine stops; four facts are country or sector figures (Phnom Penh, Rayong, Singapore, Manila). Kuala Lumpur is a second Malaysian stop next to Penang",
    "map-career-cities-8-asia-3": "Tiruppur sources disagree on the export figure. Ras Laffan: snippets report 2026 strike damage to the gas trains, so the script uses QatarEnergy's own capacity figure; check the news before the build",
    "map-career-cities-9-south-america": "Shorter, about 99 seconds. Two Brazil stops. Only Medellín has three logos; São José dos Campos has Embraer only",
    "map-career-cities-10-africa": "Ends with 'Part 11: finance careers', please confirm. Two South Africa stops. Only Lagos meets the three-logo rule; Debswana and Suez Canal Authority bases are unconfirmed",
}


def esc(s):
    return html.escape(str(s or ""))


def load():
    items = []
    for f in glob.glob(os.path.join(HERE, "*.json")):
        d = json.load(open(f))
        items.append(d)

    def key(d):
        m = re.search(r"cities-(\d+)", d["slug"])
        return (ORDER.get(d["group"], 9), int(m.group(1)) if m else 0, d.get("proposedSlot", ""))

    return sorted(items, key=key)


def words(d):
    return len(" ".join(b.get("voice", "") for b in d["beats"]).split())


def card(d):
    rows = []
    for b in d["beats"]:
        chips = " ".join('<span class="chip">%s</span>' % esc(c) for c in (b.get("onScreen") or []))
        rows.append(
            "<tr><td class='n'>%s</td><td class='lab'>%s</td><td><div class='voice'>%s</div>%s<div class='vis'>%s</div></td></tr>"
            % (esc(b.get("n")), esc(b.get("label") or b.get("role")), esc(b.get("voice")),
               ("<div class='chips'>%s</div>" % chips) if chips else "", esc(b.get("visual")))
        )
    srcs = "".join(
        "<li>%s <a href='%s' target='_blank' rel='noopener'>%s</a>%s</li>"
        % (esc(s.get("claim")), esc(s.get("url")), esc(re.sub(r"^https?://(www\.)?", "", s.get("url", ""))[:70]),
           "" if s.get("opened") else " <span class='warn'>not opened</span>")
        for s in d.get("sources", [])
    )
    logos = "".join("<li><b>%s</b>, %s: %s</li>" % (esc(l.get("brand")), esc(l.get("city")), esc(l.get("why"))) for l in d.get("logos", []))
    oq = "".join("<li>%s</li>" % esc(q) for q in d.get("openQuestions", []))
    tags = " ".join(esc(h) for h in d.get("hashtags", []))
    lead = LEAD.get(d["slug"])
    return """
<article class="card" id="{slug}">
  <header>
    <div class="meta"><span class="pill">{slot}</span><span class="pill soft">{w} words, about {sec} s</span><span class="pill soft">{n} beats</span></div>
    <h3>{title}</h3>
    <p class="sum">{summary}</p>
    {lead}
  </header>
  <details open><summary>Script</summary>
    <table class="beats"><thead><tr><th>#</th><th>Beat</th><th>Voice, on screen and animation</th></tr></thead><tbody>{rows}</tbody></table>
  </details>
  <details><summary>Caption and first comments</summary>
    <p class="pre">{caption}</p>
    <p><b>First comment:</b> {fc}</p>
    <p><b>Instagram and TikTok comment:</b> {fcig}</p>
    <p><b>Hashtags:</b> {tags}</p>
    <p><b>Threads:</b> {th} ({thr})</p>
  </details>
  {logos_block}
  <details><summary>Sources ({ns})</summary><ul class="src">{srcs}</ul><p class="reg">{reg}</p></details>
  {oq_block}
</article>""".format(
        slug=esc(d["slug"]), slot=esc(d.get("proposedSlot")), w=words(d), sec=esc(d.get("estSeconds")), n=len(d["beats"]),
        title=esc(d["title"]), summary=esc(d.get("summary")),
        lead=("<p class='lead'><b>My review:</b> %s</p>" % esc(lead)) if lead else "",
        rows="".join(rows), caption=esc(d.get("caption")), fc=esc(d.get("first_comment")), fcig=esc(d.get("first_comment_igtt")),
        tags=tags, th=esc(d.get("threadsTopic")), thr=esc(d.get("threadsReason")),
        logos_block=("<details><summary>Logos (%d)</summary><ul>%s</ul></details>" % (len(d.get("logos", [])), logos)) if logos else "",
        ns=len(d.get("sources", [])), srcs=srcs, reg=esc(d.get("registry_check")),
        oq_block=("<details open><summary>Questions for you</summary><ul class='oq'>%s</ul></details>" % oq) if oq else "",
    )


def main():
    items = load()
    sched = "".join(
        "<tr><td>%s</td><td><a href='#%s'>%s</a></td><td>%s</td><td>about %s s</td></tr>"
        % (esc(d.get("proposedSlot")), esc(d["slug"]), esc(d["title"]), esc(GROUP_NAME[d["group"]].split(":")[0]), esc(d.get("estSeconds")))
        for d in items
    )
    sections = []
    for g in ["ladder", "map", "big4"]:
        cards = "".join(card(d) for d in items if d["group"] == g)
        sections.append("<section><h2>%s</h2>%s</section>" % (esc(GROUP_NAME[g]), cards))
    backlog = ""
    bp = os.path.join(HERE, "ladder-backlog.md")
    if os.path.exists(bp):
        lines = [l[3:].strip() for l in open(bp) if re.match(r"^\d+\. ", l)]
        backlog = "<section><h2>Ladder backlog for December</h2><p class='sum'>Not scripted yet; each needs two opened sources first</p><ol>%s</ol></section>" % "".join(
            "<li>%s</li>" % esc(l) for l in lines)

    page = TEMPLATE.replace("{SCHED}", sched).replace("{SECTIONS}", "".join(sections)).replace("{BACKLOG}", backlog)
    out = os.path.join(HERE, "index.html")
    open(out, "w").write(page)
    print(out)


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Script proposals 17 Nov</title>
<style>
:root{--blue:#2960c7;--ink:#14213d;--muted:#5b6478;--line:#e3e7ef;--bg:#f6f8fc;--card:#fff;--warn:#b45309;--soft:#eaf0fb}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--ink:#e8ecf4;--muted:#a3abbd;--line:#2a3142;--bg:#0f131b;--card:#171c27;--soft:#1e2a44;--warn:#f59e0b}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif}
main{max-width:1040px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:26px;margin:0 0 4px}h2{font-size:20px;margin:40px 0 12px;color:var(--blue)}h3{font-size:17px;margin:6px 0}
.sum{color:var(--muted);margin:4px 0}.lead{background:var(--soft);border-left:3px solid var(--blue);padding:8px 12px;border-radius:6px;margin:10px 0 0}
.box{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:16px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:14px 0}
.pill{display:inline-block;background:var(--blue);color:#fff;border-radius:999px;padding:2px 10px;font-size:12px;margin-right:6px}
.pill.soft{background:var(--soft);color:var(--ink)}
details{margin-top:10px;border-top:1px solid var(--line);padding-top:8px}summary{cursor:pointer;font-weight:600}
table{width:100%;border-collapse:collapse;font-size:14px}td,th{border-bottom:1px solid var(--line);padding:6px 8px;vertical-align:top;text-align:left}
.beats .n{width:28px;color:var(--muted)}.beats .lab{width:170px;color:var(--muted);font-size:13px}
.voice{font-weight:500}.vis{color:var(--muted);font-size:13px;margin-top:2px}
.chip{display:inline-block;border:1px solid var(--blue);color:var(--blue);border-radius:4px;font-size:11px;padding:0 5px;margin:3px 4px 0 0;font-weight:600}
.pre{white-space:pre-wrap;background:var(--bg);padding:8px;border-radius:6px}.warn{color:var(--warn);font-size:12px}
.src li,.oq li{margin:3px 0}.reg{color:var(--muted);font-size:13px}a{color:var(--blue)}
.decide li{margin:6px 0}
@media (max-width:640px){.beats .lab{width:90px}}
</style></head><body><main>
<h1>Script proposals, 17 Nov 2026</h1>
<p class="sum">Scripts only: nothing is rendered, scheduled or posted. Approve, change or drop each one, and the builds start after your OK</p>

<div class="box"><h2 style="margin-top:0">Decisions for you</h2><ol class="decide">
<li><b>Big 4 reel date:</b> waive the 30-day related rule for 26 Nov (audit ladder 13 Nov, consultant ladder 16 Nov), or move it to 14 Dec or later</li>
<li><b>Big 4 caption:</b> no non-affiliation line, as on the map reels, or add one because four firm logos are shown</li>
<li><b>Pharmacy ladder:</b> keep it, or swap it for flight attendant to head of cabin services from the backlog</li>
<li><b>Map Part 10 ending:</b> "Part 11: finance careers" as the next episode, or another topic</li>
<li><b>Map lengths:</b> Parts 6-8 run about 107 seconds, Parts 9 and 10 about 100 seconds, all under 2 minutes; nine stops each instead of ten to twelve to stay under the cap</li>
<li><b>Instagram route:</b> new reels go to Instagram as trial reels from Edits (your 15 Nov rule), but the Edits connector is not connected in this session; run /mcp before the builds</li>
</ol></div>

<div class="box"><h2 style="margin-top:0">Proposed schedule (all to confirm)</h2>
<table><thead><tr><th>Slot</th><th>Reel</th><th>Type</th><th>Length</th></tr></thead><tbody>{SCHED}</tbody></table></div>
{SECTIONS}
{BACKLOG}
</main></body></html>"""

if __name__ == "__main__":
    main()
