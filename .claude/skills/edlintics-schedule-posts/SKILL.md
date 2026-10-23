---
name: edlintics-schedule-posts
description: Schedule approved Edlintics posts to Facebook, Instagram (Meta Business Suite) and the LinkedIn company page through Claude in Chrome, then post first comments after they go live. Use when Hoang says "go" on an approved batch.
---

# Schedule Edlintics posts (Meta + LinkedIn)

Only run on an approved batch: content, design and time approved, and Hoang said "go" in chat.

## 0. Prepare (no browser)
- Export each Canva design as PNG 1080x1350 (`export-design`, all pages), download with curl into `<scratchpad>/posts/`. Name files `<MMDD>-<HHMM>-<slug>-<n>.png`.
- Claude Design posts: render each artboard with headless Chrome at 1080x1350 (replace `{{accent}}` with `#2960C7`, logo blob with the local copy of the canvas asset). Puzzles end with the CTA slide.
- Captions and first comments come from the hub page (`<pre id="c1..">`, `k1..`) into `posts/copy.json`.
- Times: the browser and both schedulers use the Mac's time zone (Asia/Saigon). Convert Madrid slots: CEST (until the last Sunday of Oct) is +5 h; CET is +6 h. 10:00 Madrid = 15:00 Vietnam in summer time, 16:00 in winter time.

## 1. Meta Business Suite (Facebook + Instagram in one post)
URL: `https://business.facebook.com/latest/composer/?asset_id=108471317472449&business_id=110625140398351&context_ref=POSTS`
Per post:
1. Navigate to the composer, wait about 5 s. "Post to" is already "Edlintics and edlintics" (FB + IG).
2. Run this JavaScript first so the file picker never opens natively:
   `if(!window.__claudeClickPatched){const o=HTMLInputElement.prototype.click;HTMLInputElement.prototype.click=function(){if(this.type==='file'){this.style.cssText='position:fixed;left:0;top:0;width:10px;height:10px;opacity:0.01;z-index:99999';if(!this.isConnected)document.body.appendChild(this);return;}return o.call(this)};window.__claudeClickPatched=true;}`
3. Click "Add photo/video", then `find` "file input (type=file)" and `file_upload` all slides in order (10 max).
4. Click the Text combobox and type the caption.
5. Click the "Share to Facebook Story" switch (find it, scroll to it). A dialog appears: choose **Share this story**, not "Always share stories", then Confirm.
6. Turn on "Set date and time". For each of Facebook and Instagram: triple-click the date and type `MM/DD/YYYY`, then Tab. Click the hours segment and type `03`, the minutes segment and type `00`, the AM/PM segment and type `P`. Zoom to verify both rows.
7. Verify the switches with JavaScript: `[...document.querySelectorAll('[role=switch]')].map(e=>[e.getAttribute('aria-label'),e.checked])`. Click one switch at a time; a double click toggles it back off.
8. Click Schedule, wait, then in the boost pop-up click **Maybe later** (never Boost).
9. Check: Posts & reels › Scheduled lists one FB and one IG row per post with the right time.

Meta's "Bulk schedule posts" (Create post ▾) uses a CSV upload. It is untested here; the per-post composer above is the proven path.

## 2. LinkedIn company page
URL: `https://www.linkedin.com/company/31541400/admin/page-posts/published/`
Per post:
1. Run the same file-input JavaScript, click "Start a post", then the image icon. `find` "file input", `file_upload` the slides, then click Next.
2. Click the clock icon. Click the Date field to open the calendar and pick the day (typing the date does not stick). Click the Time field, `find` the option, e.g. "3:00 PM", click it, then Next.
3. **Type the caption after setting the schedule.** Text typed before the schedule step is lost. Find "Text editor for creating content", click it, then type.
4. Click Schedule. Check the list via clock › "View all scheduled posts".

## 3. First comments (after each post is live)
- These need a running Claude session. Create one-shot CronCreate jobs a few minutes after each slot. Each job confirms the post is live, then on Facebook, Instagram and LinkedIn, acting as the Edlintics page (never as Hoang personally):
  1. **Post the first comment** with the matching `k<n>` text.
  2. **Self-like** the post (agreed 23 Oct 2026).
  3. **Self-repost** it (agreed 23 Oct 2026). LinkedIn: Repost › "Repost" (instant, no added text). Instagram: the Repost button if the app offers it on our own post. Facebook: Share › "Share now" to the page feed. If a platform doesn't offer a repost of our own post, skip it and say so in the report; don't substitute a story share or anything else without asking.
- Check the identity switcher before each click: a like, comment or repost made as Hoang's personal profile is the wrong one; undo it and redo as the page.
- First-comment rules: `docs/content-workflow/weekly-content-process.md`. Never reveal the answer.

## Never
- Boost, change page settings, choose "Always share stories", or post anything Hoang has not approved in chat.
