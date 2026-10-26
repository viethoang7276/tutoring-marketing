---
name: edlintics-youtube-upload
description: Upload and schedule approved Edlintics posts to the Edlintics YouTube channel through Claude in Chrome. Five-concepts videos go up as Shorts (Studio); puzzles, definitions, comics and image carousels go up as channel Posts (multi-image). Written so a cheaper model can follow it step by step. Proven 24 Oct 2026.
---

# Upload Edlintics posts to YouTube

Channel: Edlintics, `UCUx_KFGdEVdBoKvCS3BxYRA` (handle `@edlinticsorganization8151`).
Studio: https://studio.youtube.com/channel/UCUx_KFGdEVdBoKvCS3BxYRA
Posts page (composer): https://www.youtube.com/channel/UCUx_KFGdEVdBoKvCS3BxYRA/posts
Only run on posts that are already approved and scheduled on the other platforms (slot `status: "scheduled"`).

## 0. Identity check (before EVERY upload, schedule or post)
- Studio: the URL contains `UCUx_KFGdEVdBoKvCS3BxYRA`, the left panel says "Your channel / Edlintics" with the blue tie avatar.
- Posts page: the composer header shows "Edlintics" with the tie avatar.
- If another channel shows: avatar (top right) › Switch account › Edlintics. Never type a password. If the switch asks for one, stop and report.
- Re-check after any reload, logout prompt or account switch.

## 1. Which format
| Slot | YouTube format | Media |
|---|---|---|
| `format: five-concepts` (video carousel) | **Short** | the long MP4 `<MMDD>-<HHMM>-<subject>.mp4` (not the `clip-n` files) |
| puzzle, definition, comic, image carousel | **Post** with images | the PNG slides in page order, max 10 |

Text: Posts use the approved caption unchanged (YouTube image posts swipe, so "Swipe for the answer" is fine). Shorts: title = slot title without the bracket part + ` #Shorts`; description = caption with "This carousel" → "This short" and "Swipe through and note" → "Watch and note", ending with `#Shorts`.
Time: use the slot's `time_vietnam` (that is the slot's Madrid time converted: CEST +5 h until 25 Oct, CET +6 h after; e.g. Madrid 13:00 on 27 Oct = 19:00 Vietnam). The browser and YouTube both use local time GMT+0700; the schedule pickers say "(GMT+0700) Local Time". Check this.

## 2. Prepare (no browser)
1. Query the hub `slots` (ArtifactData, artifact HbKxzWUcWhaBaaNb9buZM6) with `out_dir` = `<scratchpad>/yt/db`.
2. Media must be in `<scratchpad>/posts/` (exported from Canva per the schedule-posts skill, step 0b).
3. Run `python3 .claude/skills/edlintics-youtube-upload/scripts/build_items.py <scratchpad>/yt/db/slots <scratchpad>/posts <scratchpad>/yt --from <YYYY-MM-DD>`.
   It prints the queue (index, slot, type, date, time, slide count), writes `items.json` (with file paths) and `inject.js`. It skips slots whose `youtube.status` is already scheduled or published.
4. Open the Posts page in a new tab and run the whole content of `inject.js` once with `javascript_tool`. It stores the captions in `localStorage` (`edl_items`) so each later step only needs the index. Re-run it whenever you rebuild the queue. If you will only post a few items this run, rebuild with `--only 0,1,2` (queue indices keep their numbers) instead of trimming `inject.js` by hand (it is about 8–9 KB for 15 items). Queue filter: slot `status` must be "scheduled" and `youtube.status` not scheduled or published ("pending" counts).

## 3. Post path (images), 2 browser calls per post
Scripts are in `scripts/`. Replace the `__I__` placeholder with the queue index.
1. One `browser_batch`: `navigate` to the Posts page → `javascript_tool` with `post-compose.js` (expects `item I len … img true`) → `find` "file input labeled YT_DROPZONE_INPUT".
2. `file_upload` ALL slide paths of that item **in one call** to that ref. (Uploading one file at a time through other inputs replaces the previous image.)
3. `javascript_tool` with `post-schedule.js`. Expected: `item I uploads N sched Oct 27, 2026 4:00 PM result [200]`.
   - `[200]` = scheduled. Write the slot's `youtube` field now (section 5).
   - `[429 … rateLimitExceeded]` = YouTube soft rate limit on posts. Nothing was created. Stop posting at once; do not retry in the same run (see pitfalls).
   - `MISMATCH` = date or time did not set. Reload and redo the item.
   - Old posts that go out now: use `post-now.js` (replace `__N__`) instead of `post-schedule.js`.
4. To save calls, put the next item's step 1 in the same batch as this item's step 3.

## 4. Short path (Studio), 3 browser calls per Short
1. `browser_batch`: `navigate` to `https://studio.youtube.com/channel/UCUx_KFGdEVdBoKvCS3BxYRA/videos/upload?d=ud` → wait 4 s → `javascript_tool`: `document.querySelector('input[type=file][name=Filedata]').setAttribute('aria-label','YT_VIDEO_INPUT')` → `find` "file input labeled YT_VIDEO_INPUT".
2. `file_upload` the MP4.
3. One `browser_batch`: `javascript_tool` with `short-details.js` (fill `__TITLE__`, `__DESC__` as JSON strings, `__DATE__` like `Oct 28, 2026`) → `computer` key `Return` (the REAL key; a script Enter does not commit the date) → wait 1 s → `javascript_tool` with `short-schedule.js` (`__DATE__`, `__TIME__` like `7:00 PM`).
   Expected: `https://youtube.com/shorts/<id> | Video scheduled | … 7:00 PM`. "nodialog" can still be fine: check Studio › Content › Shorts, the row says "Scheduled" with the date.
- Copyright check "Claimed content found" is the Canva library music. It does not block visibility; carry on.
- Videos are 4:5 and under 3 minutes, so YouTube files them as Shorts automatically.

## 5. Record it
Right after each success, `update` the slot in the hub: `youtube: {status: "scheduled"|"published", type: "short"|"post", url, at: "<YYYY-MM-DD HH:MM> Vietnam", note}`. Posts' URLs: Posts page › Scheduled tab (`?pvf=CAE%253D`); each post card links to `/post/<id>`. Shorts: the link from step 4.3.
Check at the end: Scheduled tab count and Studio › Content › Shorts.

## Pitfalls (learned 24 Oct 2026)
- **Rate limit on Posts.** After about 14 posts in about 1.5 hours, `create_post` returned HTTP 429 `posts_soft_rate_limit`, and it was still in force 45+ minutes later (24 Oct). The UI shows NO error for this, so only trust the status from the fetch hook in `post-compose.js`. The reset window is unknown: it was still active more than 1 hour later on 24 Oct. Pace posts: schedule about 5 at a time, then wait an hour or more. **Probe first:** start each run with the pending item that has the fewest slides; if that returns 429, stop and report, so you don't waste uploads. If the probe returns 200, continue with the rest in date order (the probe rule only picks the first item). The 429 lasted more than 24 hours on 24-25 Oct (probably a daily or weekly cap on Posts for a new channel). After a 429, probe at most once a day. better, schedule YouTube posts in the daily run, 2–3 days ahead. Shorts use a different endpoint and were not limited.
- The composer placeholder text changes ("What's on your mind?", "Share a sneak peek…"). Always click `#commentbox-placeholder`, never by text.
- Typing into the posts page before the editor is focused triggers YouTube keyboard shortcuts. Use `post-compose.js`.
- The first click on Post right after `file_upload` failed with 400 when the images had not finished uploading. The scripts wait for 2 upload requests per image.
- Times in pickers use a narrow no-break space ("7:00 PM"); scripts normalise whitespace.
- Links (edlintics.com) in post text are allowed.
- Community "Turn on my Community" banner: leave it alone (it is a channel setting).
- After a YouTube item goes live: like, save and first comment (see the section at the end)

- **Caption length check:** `post-compose.js` may report a few characters more than expected (for example 405/402) because the editor counts line breaks differently. A difference under 10 is fine; a big difference means the caption was cut or doubled.
- **Work in your own new tab**, never in tabs other sessions left open.
- **Comics have 6 images:** the 4-panel comic posts are 6-page carousels in Canva (the PNGs `-comic-1` to `-comic-6` all belong to the post, matching the slot's `previews`). Upload all of them, in order.
- **Slot files:** `ArtifactData` list files keep fields either at the top level or under `data`; `build_items.py` handles both.
- **Navigate between items** (reload the Posts page) before each compose: `post-compose.js` installs a fetch hook, and running it twice on one page stacks hooks and double-counts.
- **Reading a 429:** the response body in `window.__cp` is base64 (`cG9zdHNfc29mdF9y…` = `posts_soft_rate_limit`); rely on the status number 429.
- **Captions:** use the slot's `caption` exactly as stored. UTM tags are added in the slot caption at approval time, never by this skill.
- **After a 429:** close your tab without saving the draft. Nothing was created, and the hub slot stays `pending`.
- **Placeholders:** `__I__` in the scripts is replaced with the queue index before each run (for example with `sed 's/__I__/3/'`).
- **429 cleared on 25 Oct 2026** (after YouTube approved advanced features): the probe returned 200 and 10 posts went through in about 25 minutes with no 429. Stopped at 10 on purpose, to stay under the ~14 that tripped it before. Pace: about 10 per run, then wait.
- **Speed-up:** store `post-compose.js` and `post-schedule.js` in `localStorage` (`edl_c`, `edl_s`, bodies using `return`, index as parameter `I`) and run them with `new (Object.getPrototypeOf(async function(){}).constructor)('I', localStorage.getItem('edl_c'))(idx)`. Eval is allowed on the Posts page. Each batch then ends one item (schedule) and starts the next (navigate, compose, find), so it is 2 calls per post.
- **Post URLs:** on `?pvf=CAE%253D` the cards are lazy-loaded (about 10 at a time) and listed newest first; read `a[href*="/post/"]` and match by the "Scheduled for" text inside `ytd-backstage-post-thread-renderer`.
- **Second run 25 Oct 2026:** the 5 remaining posts (including a 6-image comic) all returned 200, no 429, so 15 posts in one day is fine after the advanced-features approval. Store the scripts in `localStorage` as `edl_c`/`edl_s` (see Speed-up) by wrapping the bodies with `return` on their final expression; `build_items.py` writes `edl_items` as an object keyed by index, which works with `[I]`. The first row on the Scheduled tab can belong to another agent's post, so match by the "Scheduled for" text, not by position. Slot hub writes succeeded with `if_version` taken from the list read.

## After it goes live: like, save, first comment (Hoang, 25 Oct 2026)
This replaces any earlier note that YouTube comments are skipped. As the Edlintics channel: like the Post or Short; save Shorts to the playlist "Edlintics saves" (Posts can't be saved); post the slot's first_comment exactly as stored (replace SOURCE with youtube); pin it if pinFirstComment is true. Record it in the runs doc as yt: {like, save, comment, pin}.

**Always mute (Hoang, 26 Oct 2026):** on TikTok and YouTube (and any page that plays video), mute every time a page loads or auto-advances, because the sound plays on Hoang's computer while he works. Run `document.querySelectorAll('video,audio').forEach(v=>{v.muted=true;v.volume=0})` with javascript_tool. Never press the "m" key or other keys on the page.
