---
name: edlintics-schedule-posts
description: Schedule approved Edlintics posts to Facebook, Instagram (Meta Business Suite), the LinkedIn company page, X and Threads through Claude in Chrome, then post first comments after they go live. Use when Hoang says "go" on an approved batch.
---

# Schedule Edlintics posts (Meta + LinkedIn)

Only run on an approved batch: content, design and time approved, and Hoang said "go" in chat.


## 0a. Identity check before every automated action (Hoang, 24 Oct 2026)
Before posting, scheduling, commenting, liking, reposting or editing on any platform, confirm the active identity is Edlintics. If it isn't, switch to it. Never type a password. If switching would need one, stop for that platform and tell Hoang.
- **Meta Business Suite:** the top-left asset is "Edlintics" (Facebook page and edlintics Instagram), and comment boxes read "Comment as Edlintics".
- **Instagram web:** the left-nav Profile link points to `/edlintics/`. It often switches back to `hoang.vtrg`; use Switch › edlintics.
- **LinkedIn:** you are on the page admin `/company/31541400/admin/`, the identity switcher shows the Edlintics logo, and boxes read "Comment as Edlintics".
- **X:** the account menu at bottom left shows `@edlintics`.
- **Threads:** the profile is `@edlintics`, and the composer header starts "edlintics".
- **YouTube:** Studio shows the channel `UCUx_KFGdEVdBoKvCS3BxYRA` (Edlintics). See `.claude/skills/edlintics-youtube-upload/SKILL.md`.
- **Canva:** the Edlintics team, with posts in folder FAHYcHrS5PE.
Re-check after any account switch, reload or logout prompt. Record the identity in `runs` notes if anything was off.

## 0b. Prepare (no browser)
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

## 2b. X (@edlintics) (proven 23 Oct 2026)
1. Go to `https://x.com/compose/post` and wait 3 s.
2. **Images first:** `find` "file input inside the open compose dialog (modal), not the home timeline composer", then `file_upload` up to 4 slides. A file input from the home timeline composer attaches the images to the wrong box.
3. Click the text box at about (720,105) and type the caption. Enter makes a line break.
   - No trailing space after the hashtags, because X counts it.
   - **Never press Escape and never click outside the text**: either closes the composer.
   - The limit is 280 characters, and the ring at the bottom shows what's left.
4. Post now: click **Post** twice. The first click only closes the hashtag suggestion list.
5. To schedule instead: `find` "Schedule post button in the compose dialog toolbar" and click it (click again if the hashtag list swallowed the first click). Set the selects with `form_input`: day, hour (1–12), minutes (`0`), AM/PM (`pm`). The times are Indochina Time. Zoom on "Will send on …" to check, click **Confirm** at (979,57), then `find` the "Schedule" submit button and click it, twice if needed. The toast "Your post will be sent on …" confirms it.
6. A notice "Unlock more on X" can appear (the account is new). `find` "Got it" and click it.

## 2c. Threads (@edlintics) (proven 23 Oct 2026)
1. Go to `https://www.threads.com/@edlintics`, `find` "New thread button in main navigation", click it and wait 3 s.
2. Click the text box at about (640,308), **wait 1 s** (typing straight away loses the first words), then type. Use `shift+Enter` for line breaks.
3. **Choose where the thread goes (every post, from 24 Oct 2026).** Never end with `#edlintics`, and put no hashtags in the Threads text.
   - **Topic:** use the slot's `threadsTopic`. If it is empty, use `docs/research/2026-10-24-threads-topics-communities.md` for the subject, and the current test arm (primary or alternate) in weekly-content-process.md. Then write the chosen topic and `threadsTopicVariant` back to the slot.
     - Click "Add a topic" in the composer header, type the topic (for example `Accounting`) and click the exact match.
     - The header must read "edlintics › <Topic>". If the exact topic doesn't exist, pick the closest real one and note it in the slot's statusNote.
   - **Community:** if the slot has `threadsCommunity` (for example "Study Threads" for study-pain comics), choose that community in the composer's audience or post-to selector instead of a topic. Edlintics must already be a member (Study Threads joined 24 Oct).
   - A topic or community cannot be changed after posting, so check the header before scheduling.
4. `find` "file input in the new thread composer dialog" and `file_upload` the slides.
5. Post now: click **Post**. To schedule: `find` the "More" button in the dialog header › **Schedule…**. Click the day in the calendar, then triple-click the `hh` and `mm` fields and type a 24-hour time, e.g. `23` and `00`. Click **Done** and check the banner ("Posting tomorrow at 15:00 GMT+7"). Then `find` the "Schedule" submit button and click it once. If the dialog stays open, check again before clicking a second time.
6. Check: New thread › **Drafts** lists the scheduled posts with their times.

## 3. First comment, self-like, self-repost (a few minutes after each slot)
**24 Oct 2026: no reshare or repost on Facebook or LinkedIn.** Comment and like only there; Instagram, X and Threads still get a repost. In `runs`, record `repost: null` (not applicable) for fb and li.
Run by one-shot CronCreate jobs, so this session and Chrome must stay open. Everything is done as the Edlintics page, never as Hoang personally. Comment text = `k<n>` in `posts/copy.json`. Never reveal the answer.

**Save tokens:** load all the Chrome tools in one ToolSearch call. Use `find` for buttons instead of full screenshots, take screenshots at `scale` 0.5, use `zoom` to check typed text, and put routine clicks in one `browser_batch`. Read `get_page_text` only to verify. Don't explore: the routes below are proven (23 Oct 2026).

**A. Facebook:** facebook.com is blocked for the extension, so use Business Suite.
1. Go to `https://business.facebook.com/latest/posts/feed_and_grid?business_id=110625140398351&asset_id=108471317472449`. The left column is the page feed.
2. `find` "Like, Comment, Share buttons under the first Facebook post". Click Comment. The box must read "Comment as Edlintics".
3. Type the paragraphs, with `shift+Enter shift+Enter` between them. Click the send arrow.
4. Click Like. **No share/repost on Facebook** (Hoang stopped it on 24 Oct 2026).

**B. Instagram:** use instagram.com.
1. Go to `https://www.instagram.com/`. The top-right account must be **edlintics**. If it isn't, click **Switch** and choose edlintics (Hoang is logged in on both accounts; the active account can revert to his personal one between runs, so check every time). Never type a password. If switching logs the browser out and Instagram shows "Continue as hoang.vtrg" or a login page, stop: don't continue as Hoang, skip Instagram and ask him to log edlintics back in (seen 23 Oct 2026).
2. Go to `https://www.instagram.com/edlintics/` and `find` the first grid post link, then open `/p/<code>/`.
3. Comment: **Enter and shift+Enter both submit**, so type the whole `k<n>` as **one line** (paragraphs joined by a space), then press Enter.
4. After commenting, the layout shifts, so reload the post and `find` "Like button and Repost button in the action row" before clicking (clicking by position opened Insights once). Click the heart, then the Repost icon (next to the comment count). Leave "Add a thought" empty. Check that "Liked by edlintics" and the repost count show.
   **Check before clicking (24 Oct 2026):** Instagram labels the repost button "Repost" whether or not edlintics has already reposted, and an already-liked post shows "Unlike". If the repost count already shows 1, or the heart is red, the action is probably done: zoom on the action row first. Clicking again undoes it.
5. **Hide the like count (Hoang, 24 Oct 2026):** on the post page, open the three-dot menu at the top right of the caption panel and choose "Hide like count to others". Check that the menu now reads "Unhide like count to others". Record `done.ig.hideLikes = true`.
6. **Instagram Story share (Hoang, 24 Oct 2026):** share the post to the edlintics Story every time, as the page, once per post. First try the post's Share (paper plane) menu on instagram.com for "Add post to your story". The desktop web often lacks it. If so, use Meta Business Suite › Create story › Instagram only, with slide 1 of the post (export from Canva as PNG), and publish the story. If neither route works as the page, record `story: false` with a note, and ask Hoang to share it from the phone. Seen 24 Oct: the Business Suite story composer's "Add photo/video" opens the Mac file picker, which Claude in Chrome cannot use, so on desktop this step usually falls back to Hoang's phone. Never turn on any automatic "always share" setting.

**C. LinkedIn**
1. Go to `https://www.linkedin.com/company/31541400/admin/page-posts/published/` and wait about 4 s. The first post is the newest.
2. `find` "Like, Comment, Repost buttons under the first post". The identity switcher must show the Edlintics logo and the box must read "Comment as Edlintics".
3. Type the paragraphs with `shift+Enter` between them. Click **Comment**.
4. Click Like. **No repost on LinkedIn** (Hoang stopped it on 24 Oct 2026).
5. **Never open Hoang's personal pages (27 Oct 2026).** Layout shifts twice sent a click to his personal Notifications. Use `find` refs or the post's own URL, never coordinate clicks near the top bar, and if a personal page opens, navigate straight back to the admin URL without reading or clicking anything

**D. X:**
1. Open `https://x.com/edlintics` and `find` "Reply, Repost and Like buttons of the newest post". Click Like, then Repost › **Repost**. Dismiss the "Got it" notice if it appears.
2. For the reply, **open the post's own page**: `find` its timestamp link, then go to `/edlintics/status/<id>`. The Reply button on the timeline can open a new standalone post instead of a reply.
3. On the post page, `find` the inline "Post text" reply box, click it, wait 1 s, and type with Enter Enter between paragraphs.
4. X counts edlintics.com as 23 characters. If the ring turns red, drop the final full stop or shorten the reply. `find` "Reply submit button" and click it. Check that the post shows 1 reply, 1 repost and 1 like.

**E. Threads:**
1. Open `https://www.threads.com/@edlintics` and `find` "Like, Reply, Repost buttons of the newest thread". Click Like, then Repost › **Repost** (the toast says "Reposted").
2. Click Reply. It opens the thread page with a "Reply to edlintics…" box. Click it, wait 1 s, type with `shift+Enter` between paragraphs, then click the round send arrow. Our own reply appears as part 2 of 2 of the thread.

**F. TikTok (added 25 Oct 2026):** after each TikTok post goes live, follow section 5 of `.claude/skills/edlintics-tiktok-upload/SKILL.md`: confirm it is live on the Edlintics profile, then like, save (Favourites) and comment with the slot's `first_comment` (short, emoji ending). Record `tiktok.engaged` on the slot.

**Record (safeguard, 23 Oct 2026):** after each platform, write the result to the hub database (ArtifactData, url https://claude.ai/artifact/HbKxzWUcWhaBaaNb9buZM6, collection `runs`, doc `<YYYY-MM-DD-HHMM>` in Madrid time): `done.<fb|ig|li|x|th> = {comment, like, repost}` as booleans, plus `done.ig.story` and `done.fb.story` (true once the post is on the Story), plus `at` and a `note` for anything skipped. When a batch is scheduled, create one `runs` doc per slot with `title`, `dueAt` (UTC ISO), `platforms` and `igManual` (true when Instagram is posted by hand from the phone), so the hub can flag misses.

**Catch-up (safeguard):** the per-slot timers die when the Mac sleeps, shuts down or the session closes. So at the start of every session, read the `runs` collection. For any doc whose `dueAt` is in the last 24 hours and has a platform missing a comment, like or repost, run this section for it now, late. Anything older than 24 hours: report it to Hoang, don't act. If `igManual` is true and `igPosted` is not, remind Hoang first that the Instagram post is still due.

**Daily metrics refresh (24 Oct 2026):** if this run is for the day's last post (the 18:00 Madrid slot), straight after the first comment run the "Daily metrics refresh" in docs/content-workflow/performance-review.md for the last 7 days of posts, then add its summary under the report table.

**Report** one table: platform × comment, like, repost. Close the tabs you opened. If something can't be done as the page, skip it and say so. A story share never replaces the comment, like or repost.

## Platform limits and gotchas (learned 24 Oct 2026)
- **Threads topic:** never let `#edlintics` become the topic. Remove all hashtags from the Threads text, then set the topic chip from the slot's `threadsTopic`. If it is empty, use the subject mapping in docs/research/2026-10-24-threads-topics-communities.md and the current test arm in weekly-content-process.md. A topic cannot be changed after posting.
- **Threads** holds at most 25 scheduled threads. Schedule the nearest posts first. For the rest, leave a session cron (or a note in status.md) to add them once earlier ones go live.
- **X** takes at most 4 images per post. Carousels with more pages go to X with pages 1 to 4, and the slot's statusNote says so.
- **5-concepts format test (Instagram only, until 21 Nov):** on carousel days, export each Canva page as its own MP4 and post the clips as an Instagram carousel. Facebook, LinkedIn, X and Threads get the full MP4. If Business Suite creates the Instagram copy of the long video, move it to Drafts.
- **Instagram** often switches back to hoang.vtrg between runs: always check the account first.
- **Speed:** batch predictable clicks in one browser_batch, use find instead of screenshots, export a day's media at once, and update `slots` and `runs` right after each slot so a stopped run can resume.

## Never
- Boost, change page settings, choose "Always share stories", or post anything Hoang has not approved in chat.

## 2d. YouTube (added 24 Oct 2026)
After the other platforms, add each scheduled slot to YouTube with `.claude/skills/edlintics-youtube-upload/SKILL.md`: five-concepts videos as Shorts, everything else as channel Posts. Record the result in the slot's `youtube` field. Mind the posts rate limit (about 5 per hour).

**Threads Drafts are off limits during first-comment runs (28 Oct 2026):** confirm a Threads post is live from the @edlintics profile only. Never open New thread › Drafts or a scheduled draft in a first-comment run; on 28 Oct the R-squared thread fell back to an unscheduled draft around the time a run was looking there. If the post is missing from the profile, report it and stop for Threads.

**First comment format (25 Oct 2026):** post the slot `first_comment` exactly as stored on every platform, including X and TikTok. It is 1–2 sentences ending with emojis, so no separate versions are needed. **Links (28 Oct 2026):** no UTM tags in first comments. On Instagram and TikTok post `first_comment_igtt` when the slot has it; if `first_comment` contains a link and there is no `first_comment_igtt`, drop the link and end with "link in bio" before the emojis. On the other platforms, if a stored link still contains `?utm_`, strip everything from `/?` on so it reads plain `edlintics.com`. If the slot has `pinFirstComment: true`, pin the comment wherever the platform allows (Instagram, Facebook, TikTok, YouTube, X profile pin is not needed).

**YouTube engagement (25 Oct 2026, Hoang):** after each YouTube Post or Short goes live, as the Edlintics channel, like it, save it (Shorts and videos: Save to playlist, using a playlist named "Edlintics saves", created once if missing; channel Posts have no save, so skip and note it), and post the slot `first_comment` as the first comment. Pin it when `pinFirstComment` is true, because the channel owner can pin. This is part of every first-comment run.

## 2e. TikTok (added 25 Oct 2026)
TikTok (@edlintics) is scheduled from TikTok Studio web with `.claude/skills/edlintics-tiktok-upload/SKILL.md`: reels and five-concepts videos as videos, puzzles, definitions and comics as photo posts with a free sound. Scheduled posts carry no location; posts that go out now carry "IE University - IE Tower". Record the slot's `tiktok` field. Scheduled TikTok posts cannot be edited, so check everything before clicking Schedule.

**Always mute (Hoang, 26 Oct 2026):** on TikTok and YouTube (and any page that plays video), mute every time a page loads or auto-advances, because the sound plays on Hoang's computer while he works. Right after every navigate or reload, run this persistent muter with javascript_tool (it also pauses playback and keeps working through auto-advance): `const m=()=>document.querySelectorAll('video,audio').forEach(v=>{v.muted=true;v.volume=0;v.pause&&v.pause()}); m(); if(!window.__mute){window.__mute=setInterval(m,300);new MutationObserver(m).observe(document.documentElement,{childList:true,subtree:true});}`. Never leave a tab sitting on the For You feed; close your tab as soon as you are done. Never press the "m" key or other keys on the page. **No typing on TikTok or YouTube (27 Oct 2026):** never use computer `type` or `key` actions there; photo posts auto-advance and keystrokes land on strangers' videos (75 did on 26 Oct). Insert comment text with javascript_tool (focus the editor, then `document.execCommand('insertText', false, text)`), check the URL is still our post, and click Post instead of pressing Enter. Tip for Hoang: right-click a tiktok.com and a youtube.com tab and choose "Mute site" so the first half-second before the muter runs is silent too

## Week-45 learnings (29 Oct 2026, scheduling 2 Nov on all 7 platforms)
**Meta (Business Suite)**
- 9:16 videos: use the Reels composer directly, `https://business.facebook.com/latest/reels_composer/?asset_id=108471317472449&business_id=110625140398351&context_ref=POSTS`. The post composer's "Go to Reels composer" link sticks at 0%, and it flags 9:16 as "Wrong aspect ratio" for Instagram
- Reels flow: file-input patch, Add Video, wait for 100%, caption, click a blank area to close the hashtag list, Next, Next. Story switch: its dialog preselects **Always**, so choose "Share this story" and check with zoom before Confirm. Schedule tab, date and time per row, Schedule, Done
- Five-concepts carousel day = two posts: Instagram-only (untick Edlintics in "Post to", upload clips p1–p7 in one call) and Facebook-only (the long MP4). In Scheduled the IG row shows "Your reel" but the caption is there. Never click **Publish now** in the side panel
- Files over 10 MB (the Chrome upload cap): re-encode first with the same audio
**LinkedIn** video works in the normal composer. Wait for "Your upload is complete" before navigating. Verify via clock › "View all scheduled posts" (the /admin/page-posts/scheduled/ URL redirects)
**X** video uses the same modal file input. The first Schedule-post click and the first Schedule-submit click are swallowed by the hashtag list: click each twice. Set date/time with form_input. Verify at https://x.com/compose/post/unsent/scheduled
**Threads** set the topic by typing it and `find`ing the exact option. Check the chip text via the `input[type=search]` value (it can render as full-width letters). "Financial Literacy" only exists as lowercase "financial literacy". With 6 images attached the date picker sits about 18 px lower. No AI-info option exists
**YouTube** after short-schedule.js a "We're still checking your content" box needs **Got it**. Trust Studio › Content › Shorts "Scheduled", not the dialog text. For a channel Post write `edl_items` by hand as `{"0":{text,n,date,time,ap}}`
**TikTok** (no keystrokes): clear the filename caption once with a DOM Range selectNodeContents + `execCommand('delete')`, check 0/4000, then `edl_fill`; doing it twice doubles the text (reload and re-upload). Hashtags: click the `.suggest-item` matches, don't type. Turn the music copyright check on by script and wait for "No issues found" before `edl_go`. Photo sound: Add sound › **Recent** › "Lofi Study". Helpers live in localStorage on tiktok.com (`edl_fill`, `edl_sched`, `edl_go`, `edl_snd`); overwrite `edl_tt` with the day's queue
**Captions for puzzle reels**: use the reel card's caption (it has no "Swipe for the answer" line). Check `caption_x` for slide wording before using it on a video
