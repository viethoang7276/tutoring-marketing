---
name: edlintics-tiktok-upload
description: Upload and schedule approved Edlintics posts to the Edlintics TikTok account (@edlintics) through TikTok Studio web in Claude in Chrome, then like, save and first-comment them once live. Reels and five-concepts videos go up as videos; puzzles, definitions and comics go up as photo posts with a free sound. Written so a cheaper model can follow it step by step. Proven 25 Oct 2026 (42 posts).
---

# Upload Edlintics posts to TikTok

Account: **Edlintics Organization, @edlintics** (user id 7599269275379876881).
Upload page: `https://www.tiktok.com/tiktokstudio/upload?from=creator_center&tab=video` (photos: `&tab=photo`).
Posts list: `https://www.tiktok.com/tiktokstudio/content`. Public profile: `https://www.tiktok.com/@edlintics`.
Hub: ArtifactData, url `https://claude.ai/artifact/HbKxzWUcWhaBaaNb9buZM6`, collection `slots`.
Only run on slots that are approved (`status` "scheduled" or already "posted" elsewhere).

## Hard rules
- Act only as @edlintics. Hoang's restaurant account is also logged in to this Chrome. Never type a password; if a switch needs one, stop and report.
- Never Boost, Promote or buy anything. Leave the "Promote video" button alone.
- Captions exactly as stored in the hub (slot `caption`), with no paragraph or line ending in a full stop. The build script strips them.
- **Location (Hoang, 25 Oct 2026):** posts that go out **now** (past slots) get **"IE University - IE Tower"** (Paseo de la Castellana 259, 28046 Madrid; the closest exact match to "IE Tower - IE University"). **Scheduled posts get NO location.** The `edl_go` guard enforces both. Hoang can change this rule.
- **Scheduled posts cannot be edited** ("Scheduled posts cannot be edited."). Check everything before clicking Schedule. To fix one, Hoang must delete it in Studio (the agent does not delete posts) and the next run re-schedules it.
- Use your own new tab (`tabs_create_mcp`); other agents use Chrome at the same time. Close your tab at the end.

## 0. Identity check (before every upload and every like, save or comment)
Run on any tiktok.com page:
`const r=await fetch('/passport/web/account/info/?aid=1988').then(r=>r.json()); r.data.username`
It must return `edlintics`. If not: avatar (top right) › Switch account › Edlintics. Re-check after any reload or login prompt. The batches below throw `WRONG ACCOUNT` and stop if it changes.

## 1. What TikTok Studio web can do (tested 25 Oct 2026)
| Topic | Finding |
|---|---|
| Scheduling | Yes, "When to post › Schedule". Up to **30 days** ahead (the calendar allowed up to 24 Nov on 25 Oct), at least about 15 min ahead, 5-minute steps. Times are the browser's time zone (Asia/Saigon), so use `time_vietnam`. First use shows "Allow your video to be saved for scheduled posting?" › Allow. |
| Photo posts | Yes, the **Photos** tab: up to 35 images, JPG/PNG/WebP, max 50 MB each. 4:5 slides work. Photo posts have a **title** (90 characters) plus the description. |
| Videos | Up to 30 GB / 60 min. Our MP4s are 3–10 MB. |
| Caption | 4,000 characters. Hashtags only become links when picked from the suggestion list (type `#tag`, wait 2 s, press Return). Pasted hashtags stay plain text. |
| Sound (photo posts) | "Add sound" opens the TikTok library. We use **"Lofi Study" by Lofi Studies & FASSounds** on every photo post. Videos keep their own audio (Canva music). |
| Location | Field under Cover. Search "IE Tower" › pick **IE University - IE Tower**. |
| Checks | Music copyright check and Content check lite run automatically. All 42 uploads passed. Content check lite can take about 10 minutes; if it is still running, TikTok asks "Continue to post?" › "Post now" keeps the schedule. |
| Rate limits | 42 uploads in about 2.5 hours on 25 Oct with no throttling. Likes did throttle: after 8 quick likes, the 9th reverted silently (request 200, UI back to unliked). |
| Other settings | Who can see: Everyone. Allow comments and reuse: on. "AI-generated content" and "Disclose post content" toggles exist under Show more; we leave them off unless Hoang decides otherwise. |

## 2. Prepare (no browser)
1. Read the hub: `ArtifactData list`, collection `slots`, `query.limit` 200, `out_dir` `<scratchpad>/tt/db`.
2. Media in `<scratchpad>/posts/`: `<slot id>/fixed/01.png…` or `<slot id>/fixed/<subject>.mp4` (corrected exports), reels in `<slot id>/*.mp4`, older posts as `<MMDD>-<HHMM>-<slug>-<n>.png|mp4`. If an old post's media is missing, export it from the slot's `canva` design with the Canva connector (`export-design`, PNG 1080x1350 or MP4) and save it with that naming.
3. Run `python3 .claude/skills/edlintics-tiktok-upload/scripts/build_items.py <scratchpad>/tt/db/slots <scratchpad>/posts <scratchpad>/tt`.
   It prints the queue (`index slot type when files tags chars`), writes `items.json` (file paths) and `inject.js`. It skips slots whose `tiktok.status` is scheduled or published, takes old captions from `posts/copy.json` (c1–c5) and turns "This carousel"/"Swipe through and note" into "Ledger walks you through"/"Walk through them with Ledger and note" for five-concepts videos. `when` is the slot's `time_vietnam`, or `now` if that is less than 20 minutes away or past.
4. Check TikTok's own list for duplicates before uploading: open Posts (`tiktokstudio/content`) and compare captions with the queue (step 6 shows how to list all rows).

## 3. One-time setup in your tab
1. `tabs_create_mcp`, navigate to the upload page, run the identity check.
2. Run the whole of `inject.js` with `javascript_tool` (stores the queue as `edl_tt`), then the whole of `scripts/helpers.js` (stores `edl_fill`, `edl_loc`, `edl_snd`, `edl_sched`, `edl_chk`, `edl_go`, `edl_eng`). Both survive reloads on tiktok.com.
3. Each step below runs a helper with: `const R=n=>new (Object.getPrototypeOf(async function(){}).constructor)('I',localStorage.getItem(n)); await R('edl_fill')('<index>')`

## 4. Upload one item = ONE browser_batch
Replace `<i>`, the file paths and the hashtags (from the queue's `tags`, in order). The `find` ref is `ref_89` on the photo tab and `ref_90` on the video tab; if `file_upload` fails, use the ref that `find` returned.

**Photo post (puzzle, definition, comic):**
1. `navigate` upload page `&tab=photo` › wait 4 › identity check (throw if not edlintics) › `find` "photo file input type=file" › `file_upload` all slides in order, in ONE call › wait 4.
2. `edl_fill('<i>')` (title + body; expect `counter N/4000` = body + 2).
3. For each tag: `type` `#tag` › wait 2 › `key` Return.
4. **Only if `when` is now:** location (step 4c).
5. `javascript_tool`: click "Add sound", wait 2.5 s, focus `input[placeholder="Search sounds"]` › `type` `lofi study` › Return › wait 3.
6. `edl_snd`, then (scheduled only) `edl_sched`, then `edl_go`, in one javascript call: `(await R('edl_snd')('<i>'))+' || '+(await R('edl_sched')('<i>'))+' || '+(await R('edl_go')('<i>'))`.
   Expected: `sound set || sched set 16:00 2026-10-27 (want 2026-10-27 16:00) htrue mtrue || CLICKED Schedule -> /tiktokstudio/content | … OK | loc  | sound true | …`.

**Video (explainer reel, five-concepts):**
1. `navigate` upload page `&tab=video` › wait 4 › identity check › `find` "video file input type=file" › `file_upload` the MP4 › wait 8–10.
2. `javascript_tool`: `document.querySelector('.public-DraftEditor-content').focus()` and read "Uploaded (x MB)" › `key` cmd+a › `key` Delete (the editor starts with the file name).
3. `edl_fill`, then the tags as above. **Now** posts: location (4c).
4. One javascript call: run `edl_sched` (scheduled only), read the Checks text, and only if it contains "Music copyright check No issues found" run `edl_go`; otherwise return `HOLD` and look.

**4c. Location (now posts only):** `javascript_tool` scrolls `input[placeholder="Search locations"]` into view (`scrollIntoView({block:'center'})`) › `left_click` at (440, 417) (the input sits at y 402–434 after centring; check the returned top if it misses) › `key` cmd+a › `type` `IE Tower` › wait 3 › `edl_loc`. Expect `location IE University - IE Tower`. A JS `focus()` alone does not open the dropdown.

**Read the result:** `NOT POSTED: …` means the guard stopped it: fix what the check shows (tags mismatch, location, sound, time) and run `edl_go` again. `CLICKED … -> /tiktokstudio/content` means done. Past posts: about one every 3 minutes is fine.

## 5. After a post is live: like, save, first comment (Hoang, 25 Oct 2026)
**Studio first (Hoang, 27 Oct 2026; proven on 2026-10-26-1800).** Work from TikTok Studio, not the public post or feed pages, so nothing plays sound and nothing auto-advances. No self-likes (26 Oct), so only the comment and the save remain:
- **Live check:** `tiktokstudio/content` row shows "Public" with a date. The list is virtualised and starts at the latest scheduled rows; scroll its container by script to reach the row.
- **First comment:** click the row's comment icon to open `/tiktokstudio/comment/<id>`. Its "Reply to comment" box at the top posts a TOP-LEVEL comment on our post (150 characters). Check the thread for an existing Edlintics comment first. Focus the textarea, insert the text with `document.execCommand('insertText', false, text)`, and click the red send arrow. Expect the toast "Comment posted". Studio has no pin.
- **Save:** Studio cannot save, and its save count does not say who saved. Check the profile's Favourites tab (`tiktok.com/@edlintics`, muter on). Only if our post is missing there, open that single public post URL with the muter on, check `location.href`, and click the bookmark. No keystrokes.
- **Recognise what is ours (Hoang, 27 Oct 2026):** before any comment or save, confirm the post is by @edlintics (URL id and caption match the slot). Likes on other creators' videos are fine and need no undo or report; the no-like rule is only for our own posts.
- Steps 2, 3 and 5 below are the old public-site fallback; use them only when Studio cannot do a step.
Do this for every post once it is live (now posts straight away; scheduled posts in the first-comment run after their time). Identity check first.
1. **Confirm it is live:** `tiktokstudio/content` shows the row as "Public" with a date (no blue clock badge).
2. **Photo posts:** `navigate` `https://www.tiktok.com/@edlintics/photo/<id>` and run `edl_eng('<i>')` straight away (the photo page auto-advances to other people's posts after the slides; `edl_eng` finds our post by its caption). Expect `like false->true … | fav [Add to Favourites …]`.
3. **Videos:** direct `/video/<id>` URLs open a Chrome error page in this setup. Open `https://www.tiktok.com/@edlintics`, then `javascript_tool`: `document.querySelector('a[href*="/video/<id>"]').click()` (scroll the grid until it exists). The video opens in a player with the actions at the top right. Check `location.href` contains the id, then real `left_click` on the heart (about 1007, 225) and the bookmark (about 1137, 225). Do not use JS clicks there: one moved the player to the next video and un-liked it.
4. **Verify** with zoom on the action row: red heart, yellow bookmark, counts +1. A like that reverts to grey within seconds is TikTok's soft limit: stop liking for an hour and record `like: false`.
5. **First comment = the slot's `first_comment`** (new format: 1–2 sentences, under 150 characters, ending with 1–2 emojis). Read it fresh from the hub. If it is still the old long format, skip the comment and note it. TikTok caps comments at 150 characters; links are not clickable, so use `first_comment_igtt` when the slot has it, or drop the link and end with "link in bio" (28 Oct 2026). Type it into "Add comment…" (`data-e2e=comment-input`), click the red send arrow, and check it appears under Comments as Edlintics.
6. **Never** click "Promote video" or "View Analytics" by accident; they sit on the player.

## 6. Record it (hub, pinned with if_version)
- After uploading: `tiktok: {status: "published"|"scheduled", type: "photo"|"video", url, at: "<YYYY-MM-DD HH:MM> Vietnam", location: "IE University - IE Tower (Madrid)"|"none", note}`. URL: `https://www.tiktok.com/@edlintics/photo/<id>` or `/video/<id>`.
- After engaging: `tiktok.engaged: {like, save, comment, at, note}`. Updates deep-merge, so writing `{tiktok: {engaged: …}}` keeps the other fields.
- Batch all slots in one `ArtifactData batch` with `file_path` per entry and `if_version` from a fresh list.
- **Getting the ids:** the Posts list is virtualised (only about 7 rows exist at a time). Scroll the list's scroll container 250 px at a time and collect `a[href*="/video/"]` into a Map (href id → caption start) until you have them all. Photo posts also show as `/video/<id>` there; the public URL is `/photo/<id>`.

## Pitfalls (learned 25 Oct 2026)
- The Draft.js caption editor ignores `execCommand('selectAll')`; clear it with real cmd+a and Delete. Paste with a synthetic `ClipboardEvent('paste')` (that is what `edl_fill` does).
- Blank lines between paragraphs show as three newlines in `innerText` but count correctly (counter = caption length).
- Typing `IE Tower` without first clicking the search box sends the keys nowhere, or puts a stray letter in the box (we saw `rIE Tower`); always cmd+a before typing.
- `edl_go` waits for the "Continue to post?" dialog and confirms it; without that the page stays on the upload form.
- The schedule pickers list only valid hours for today; pick the date first, then the time (`edl_sched` does).
- A photo post's "Favourites" label always reads "Add to Favourites…"; it does not flip when saved. Judge by the yellow icon, the toast "Added to Favourites" or the count. Never click save twice (it un-saves).
- 25 Oct: the free-rider test reel was scheduled with the IE location before the no-location rule; it cannot be edited (see Hard rules).

## Pitfalls from the first engagement run (25 Oct 2026)
- Photo posts auto-advance. Click the image to pause before commenting, and check `location.href` and focus on the comment box before typing. Stray keys trigger shortcuts ("L" toggles the like) or move to other creators' videos.
- Likes are soft-limited after about 8 quick likes: a like looks red, then reverts on reload. Space likes 20–30 s apart and verify each one after a reload.
- Never click a like or save that is already active, because a second click undoes it.
- Comment pinning may not be offered on our own posts (the menu shows only Delete). If so, record pin: false and move on.
- New-account soft limit: on 25 Oct, likes on @edlintics kept reverting for hours. Retry at most once, several hours later. If a like reverts twice, skip self-likes for that day; the save and comment matter more. Clicking during an auto-advancing slideshow can land a like on another creator's video, so always pause first.
- Check likes on the profile's Liked tab (tiktok.com/@edlintics → Liked), not by reloading the post. On 26 Oct it showed 8 of our posts liked and no other creators' posts. Opening a /photo/ link can drop you into the For You feed after a few seconds, so take a screenshot right before any click.
- Studio and the player show 0 comments even when our first comment exists. Check comments in Studio → Comments.
- **No self-likes from 26 Oct 2026.** After repeated reverts, and a stray like that landed on another creator's video during an auto-advance, TikTok runs only save and first-comment. Hoang likes from his phone if he wants a like. Never click a heart on TikTok.

**Always mute (Hoang, 26 Oct 2026):** on TikTok and YouTube (and any page that plays video), mute every time a page loads or auto-advances, because the sound plays on Hoang's computer while he works. Right after every navigate or reload, run this persistent muter with javascript_tool (it also pauses playback and keeps working through auto-advance): `const m=()=>document.querySelectorAll('video,audio').forEach(v=>{v.muted=true;v.volume=0;v.pause&&v.pause()}); m(); if(!window.__mute){window.__mute=setInterval(m,300);new MutationObserver(m).observe(document.documentElement,{childList:true,subtree:true});}`. Never leave a tab sitting on the For You feed; close your tab as soon as you are done. Never press the "m" key or other keys on the page. **No typing on TikTok or YouTube (27 Oct 2026):** never use computer `type` or `key` actions there; photo posts auto-advance and keystrokes land on strangers' videos (75 did on 26 Oct). Insert comment text with javascript_tool (focus the editor, then `document.execCommand('insertText', false, text)`), check the URL is still our post, and click Post instead of pressing Enter. Tip for Hoang: right-click a tiktok.com and a youtube.com tab and choose "Mute site" so the first half-second before the muter runs is silent too
