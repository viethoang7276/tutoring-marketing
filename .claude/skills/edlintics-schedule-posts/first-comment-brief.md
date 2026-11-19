# First-comment round: Haiku agent brief (template)

Fill the {PLACEHOLDERS} from the slot doc (first_comment, first_comment_igtt, youtube.id, threadsTopic, caption) and the runs doc, then pass the text as the agent prompt. Do not rebuild the brief from scratch each round.

You are running the Edlintics first-comment round for ONE reel that went live at {TIME_VN} Vietnam time on {DATE} ({DUE_UTC} UTC). Work in Claude in Chrome. Follow section 3 of /Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing/.claude/skills/edlintics-schedule-posts/SKILL.md (read lines 89-140 first) plus the rules below.

POST: {FORMAT} "{TITLE}". Caption starts "{CAPTION_START}". Hub runs doc id: {RUN_ID}.
Platforms: fb (reel), ig (reel), li (video), th (video thread, topic {TH_TOPIC}), yt (Short {YT_ID}, https://www.youtube.com/shorts/{YT_ID}). TikTok and X are PAUSED.

COMMENT TEXT (exactly, one line):
- Facebook, LinkedIn, Threads, YouTube: {FIRST_COMMENT}
- Instagram: {FIRST_COMMENT_IG}

RULES
- Load all Chrome tools in ONE ToolSearch call: select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__tabs_close_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__find,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__browser_batch,mcp__claude-in-chrome__javascript_tool. Call tabs_context_mcp first, then create your own new tab; close the tabs you opened at the end. Do not touch the other tabs.
- Identity check on every platform: act only as Edlintics (FB "Comment as Edlintics", IG top-right account "edlintics", LinkedIn identity Edlintics, Threads @edlintics, YouTube channel Edlintics UCUx_KFGdEVdBoKvCS3BxYRA). If wrong and not switchable without a password, skip and report. Never type a password.
- Confirm you are on the {SHORT_NAME} reel (check the caption) before commenting, and check that Edlintics has not already commented (no duplicates). On Instagram other recent reels and trial reels are NOT this post; make sure you open the {SHORT_NAME} reel.
- Facebook: Business Suite Feed & grid https://business.facebook.com/latest/posts/feed_and_grid?business_id=1704820277908835&asset_id=108471317472449 . The Facebook Page column is on the LEFT (Instagram on the right). Comment + Like only, no share.
- Instagram: instagram.com/edlintics, open the {SHORT_NAME} reel (/reel/<code>/ or /p/<code>/). Comment, reload, like the ACTION-ROW heart (left of the comment icon, not the heart on our own comment), repost, hide like count. Zoom before clicking so you don't undo something already done. Report the code.
- LinkedIn: https://www.linkedin.com/company/31541400/admin/page-posts/published/ ; comment + like, no repost. Never open Hoang's personal pages.
- Threads: https://www.threads.com/@edlintics ; like, repost, reply. If the thread for this post does not exist, record th pending and do not post one.
- YouTube: open https://www.youtube.com/shorts/{YT_ID} (or watch?v={YT_ID}), comment as Edlintics, like the Short, pin our comment. Do NOT type with key events: focus the comment box, then use document.execCommand('insertText', false, text) via javascript_tool, then click the Comment button. IMPORTANT: YouTube turns emojis into <img alt="EMOJI"> tags, so the box's innerText will NOT show them; check the img alt values instead. That is normal, so do not stop over it.
- TikTok PAUSED: do not open TikTok. X PAUSED: do not open x.com.
- No UTM tags; do not change the comment text.
- If Claude Code's permission check refuses an action, STOP that action and report it; do not try a workaround.
- Do NOT write to the hub; the lead records results.

REPORT: a table platform × comment/like/repost (true/false/null) with the post id/URL for each, the IG code and whether hide-likes worked, the YT pin status, and anything skipped and why.