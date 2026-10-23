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

## 3. First comment, self-like, self-repost (a few minutes after each slot)
Run by one-shot CronCreate jobs, so this session and Chrome must stay open. Everything is done as the Edlintics page, never as Hoang personally. Comment text = `k<n>` in `posts/copy.json`. Never reveal the answer.

**Save tokens:** load all the Chrome tools in one ToolSearch call. Use `find` for buttons instead of full screenshots, take screenshots at `scale` 0.5, use `zoom` to check typed text, and put routine clicks in one `browser_batch`. Read `get_page_text` only to verify. Don't explore: the routes below are proven (23 Oct 2026).

**A. Facebook:** facebook.com is blocked for the extension, so use Business Suite.
1. Go to `https://business.facebook.com/latest/posts/feed_and_grid?business_id=110625140398351&asset_id=108471317472449`. The left column is the page feed.
2. `find` "Like, Comment, Share buttons under the first Facebook post". Click Comment. The box must read "Comment as Edlintics".
3. Type the paragraphs, with `shift+Enter shift+Enter` between them. Click the send arrow.
4. Click Like. Then Share › **Share now** (Feed, Public, as Edlintics). The toast "successfully shared" confirms it.

**B. Instagram:** use instagram.com.
1. Go to `https://www.instagram.com/`. The top-right account must be **edlintics**. If it isn't, click **Switch** and choose edlintics (Hoang is logged in on both accounts). Never type a password.
2. Go to `https://www.instagram.com/edlintics/` and `find` the first grid post link, then open `/p/<code>/`.
3. Comment: **Enter and shift+Enter both submit**, so type the whole `k<n>` as **one line** (paragraphs joined by a space), then press Enter.
4. Click the heart, then the Repost icon (next to the comment count). Leave "Add a thought" empty. Check that "Liked by edlintics" and the repost count show.

**C. LinkedIn**
1. Go to `https://www.linkedin.com/company/31541400/admin/page-posts/published/` and wait about 4 s. The first post is the newest.
2. `find` "Like, Comment, Repost buttons under the first post". The identity switcher must show the Edlintics logo and the box must read "Comment as Edlintics".
3. Type the paragraphs with `shift+Enter` between them. Click **Comment**.
4. Click Like. Then Repost › **Repost** (the instant one, not "with your thoughts"). The toast "Repost successful" confirms it.

**Report** one table: platform × comment, like, repost. Close the tabs you opened. If something can't be done as the page, skip it and say so. Don't substitute a story share.

## Never
- Boost, change page settings, choose "Always share stories", or post anything Hoang has not approved in chat.
