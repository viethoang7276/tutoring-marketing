# Posting safeguard

Agreed with Hoang on 23 Oct 2026, after a first-comment run nearly failed because the Mac was going to shut down.

## The problem
First comments, self-likes and self-reposts are done by Claude in Hoang's logged-in Chrome. The per-slot timers are one-shot jobs inside a Claude Code session, so they are lost when the Mac sleeps, shuts down or the session closes. A cloud agent cannot take over, because it has no access to those logins. Posts scheduled in Meta, LinkedIn, X and Threads still publish on their own; Instagram posts made by hand from the phone can be forgotten.

## The five parts
1. **Run log in the hub.** The Schedule tab has a "First comments and Instagram" table, fed by the `runs` collection. Each live post shows comment, like and repost per platform. A row turns red 15 minutes after the slot if anything is missing.
2. **Catch-up at every session start.** `session-start.md` and the scheduling skill (section 3) tell Claude to read `runs` first and finish anything missed in the last 24 hours. Older misses are reported, not acted on.
3. **Timers that survive the terminal closing.** Use the Claude desktop app's scheduled tasks for the per-slot runs instead of CronCreate jobs. The prompt for each task is below. They still need the Mac awake with Chrome open.
4. **Mac available at slot times (Hoang's setting).** System Settings › Battery (or Energy) › Options: turn on "Prevent automatic sleeping on power adapter when the display is off", keep the Mac plugged in, and leave Chrome open. Or schedule the Mac to wake shortly before 16:00 and 00:00 Vietnam time with `sudo pmset repeat wakeorpoweron MTWRFSU 15:55:00` (one daily wake; add the second slot in Energy settings if needed). If the Mac is shut down, parts 1 and 2 catch the miss later.
5. **"Forgot to post" check for Instagram.** When Instagram is posted by hand, the runs doc gets `igManual: true`. Hoang presses "I posted it" in the hub table. If it is still unticked 30 minutes after the slot, the row turns red, and the next Claude run reminds him before anything else.

## Desktop-app scheduled task prompt (one per slot, a few minutes after it)
> Edlintics first comment for slot <YYYY-MM-DD-HHMM> (Madrid): follow section 3 of .claude/skills/edlintics-schedule-posts/SKILL.md in /Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing. Post first comment k<n> from the approved copy, then self-like and self-repost as Edlintics on every platform in the slot's `runs` doc, record each result in `runs`, and also catch up any other slot from the last 24 hours with missing steps. Never type passwords; if a site is logged out, skip it and note it.
