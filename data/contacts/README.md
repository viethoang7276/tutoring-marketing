# Contacts — old tutoring platform client list

**Files in this folder are gitignored (PII). Only this README is tracked.** The GitHub remote of
this repo is public, so the CSVs must never be committed. Back them up outside git.

| File | What |
|---|---|
| `old-platform-clients-raw.csv` | Verbatim export from the old booking platform (2026-09-14). Columns: First Name, Last Name, Phone, Email, Notes, Days Since Last Appointment, Banned. |
| `old-platform-clients-clean.csv` | Deduplicated + normalized version (one row per person, phones in E.164, country guessed from prefix, recency bucket, `email_ok` flag). Regenerate from raw if the export is refreshed. |

Source of the export: Hoang's 1:1 tutoring bookings, 2019 → 2026 (IE University students and others).

## Snapshot analysis (2026-09-14)

**Size**
| | |
|---|---|
| Raw rows | 436 |
| Unique people (dedup by email, else name+phone) | 359 |
| Duplicate rows removed | 77 (62 people had 2–4 rows, e.g. same email with short vs full surname) |
| Usable email addresses | ~349 (7 rows had no email; 2 malformed; 3 obvious domain typos or placeholder) |
| Phone numbers | 383 rows |
| Banned | 2 |
| Notes column | empty on every row — nothing to mine |

**Recency (days since last appointment, per unique person)**
| Bucket | People |
|---|---|
| < 90 d | 2 |
| 90–180 d | 11 |
| 180–365 d | 25 |
| 1–2 y | 80 |
| 2–3 y | 76 |
| 3–5 y | 88 |
| > 5 y | 63 |
| no appointment recorded | 14 |

Median last contact ≈ 1,000 days (~2.8 y). Only ~38 people were active in the last 12 months.

**Where they are (from phone prefix)**
Spain 224 · France 29 · Germany 27 · Switzerland 13 · Italy 13 · Norway 6 · Austria 4 · UK 4 ·
Portugal 3 · US/CA 3 · a dozen others 1–2 each · 53 no phone · 42 unparseable (local numbers
without prefix). Heavily Madrid/IE-centred; the non-Spanish numbers are IE international students.

**Email domains**
gmail 223 · `student.ie.edu` 68 · icloud 21 · hotmail/outlook/yahoo ~15. IE student cohorts by
address (`ieuYYYY`): 2018: 7 · 2019: 11 · 2020: 16 · 2021: 7 · 2022: 15 · 2023: 10 · 2024: 2.
Student addresses for cohorts ≤ 2022 are probably dead (graduated) — prefer the personal
email where the same person has both.

## What this means for marketing

1. **It is an alumni list, not a warm list.** ~70 % last booked 2+ years ago; most have graduated.
   Treat it as a referral / testimonial / "tell a younger sibling or friend" audience, not as
   direct buyers of €99 exam-prep courses.
2. **The ~38 active-in-last-year people are the real launch wedge.** They are current IE students
   who already pay €45/h — the most likely first 15 paying customers (validation target). A
   personal, one-to-one message from Hoang beats any campaign here.
3. **Cohorts 2023–2024 (≈12 people) are still enrolled** — second-priority direct outreach.
4. **Country mix matters for channel choice:** Spanish numbers dominate → WhatsApp is the native
   channel; email for the rest. But see consent below.
5. **Never bulk-email or bulk-WhatsApp this list.** These people gave contact details to book
   tutoring, not to receive marketing (GDPR: Spain/EU). Acceptable uses: personal 1:1 messages
   from Hoang to former students; a one-time "I've launched Edlintics, want updates? reply YES"
   opt-in to recent contacts; suppression / lookalike seed audiences only with a lawful basis.
   Build the marketing list from the opt-ins, not from this file.
6. **Hygiene before any use:** drop the 2 banned, the placeholder/typo emails (`email_ok = N`),
   and prefer personal over `student.ie.edu` addresses for cohorts ≤ 2022.

## Suggested next steps (not done)

- Hoang sends a personal message to the `<180d` + `180-365d` group (~38 people) announcing the
  Sept 1 launch and asking who wants to be told when their course goes live.
- Ask the 2023–2024 cohort for one-line testimonials for the site / social proof.
- Log opt-ins in a separate consented list (e.g. `data/contacts/opt-in.csv`, also gitignored).
