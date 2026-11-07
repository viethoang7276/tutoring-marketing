# Edlintics marketing: notes for Claude

## Social content workflow
Read these before any Edlintics social content work:
- `docs/content-workflow/weekly-content-process.md`: the Thursday plan, caption and first-comment rules, and approvals.
- `docs/content-workflow/brand-graphics.md`: reusable icons and illustrations. Check it before generating anything.
- `docs/content-workflow/holiday-calendar.md`: every holiday with its content window. Make content fit upcoming holidays; Christmas content starts 1–2 weeks before 25 Dec.
- `docs/content-workflow/economic-calendar.md`: scheduled economic events with global impact (Federal Reserve and ECB decisions, US CPI, euro area flash inflation, big earnings weeks). At most one post a week, published before the event, teaching a concept that stays true whatever the result.
- `docs/content-workflow/concept-registry.md`: the hub `concepts` registry of every concept already used. Query it before proposing any post; same concept blocked 90 days, related concept or same industry 30 days, a theme at most 2 posts a week.
- Skills `edlintics-concept-carousel` and `edlintics-puzzle-visuals`: copies in `docs/content-workflow/skills/` (to load them as project skills, copy that folder to `.claude/skills/`).

## Systems
- **Content Desk** (approvals, system of record): https://claude.ai/artifact/RV9TtccfdAkHVQX3zpkv61
- **Canva templates:** Definition DAHYuPFDiDU, This vs That DAHYuGf21MI, Puzzle DAHYuGZYL_E. Always copy them; never edit the originals.
- **Claude Design templates:** canvas "Edlintics Post Templates", https://claude.ai/artifact/7yg3KS9LosoEoZEqEP2GAp
- **Canva brand graphics folder:** FAHYugebSqU
- **Canva thumbnail templates:** Edlintics › Thumbnail template `FAHZvEuoTWo`, one 9:16 cover template per reel type (Definition DAHZsFwGa8k, A day in the life DAHZsDp1sEM, How-to DAHZsPspd34, Puzzle DAHZsM7lYrQ, List DAHZsMn_9zo, Ledger talks DAHZsCwNlJQ, Highlighter DAHZsFzww28). Copy them; never edit the originals. Guide: assets/renders/cover-templates/README.md
- **Canva post folder:** Edlintics › Social media posts `FAHYcHrS5PE`. File every saved post design here.
- **Posting (option A, Chrome):** Meta Business Suite, business_id 110625140398351, asset_id 108471317472449 (Facebook + Instagram). LinkedIn company page admin: https://www.linkedin.com/company/31541400/admin/
- **X and Threads (added 23 Oct 2026):** https://x.com/edlintics and https://www.threads.com/@edlintics. Chrome is logged in as Edlintics on both. Schedule with each site's own web composer.
- **Scheduled task:** "Edlintics weekly content plan", Thursdays 07:59 Vietnam time. It plans content only.

## Hard rules
- Mix currencies across posts (Hoang, 7 Nov 2026): rotate dollars, euros, pounds and others instead of defaulting to one ($1.80, €3,000, £45). Keep one currency inside a post unless the concept is about exchange rates, and keep real-world figures in the currency they were reported in.
- Show planned external writes before making them.
- Canva designs: always save (commit) a draft as soon as it is built and file it in the post folder, so Hoang can open and fix it in Canva. Never leave edits in an open transaction; they expire. If Hoang rejects a design, delete it in Canva. (Agreed 23 Oct 2026; replaces "save only after approval".)
- Content, design and publishing approval are separate. Publishing and scheduling stay off until Hoang explicitly authorises them.
- Never put secrets in chat, code or logs. Ask before creating credentials, OAuth access, installs or permission changes.
- A timeout is not proof that nothing happened.
