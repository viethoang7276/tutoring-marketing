# Slack delivery for the weekly CMO report

The weekly report can post to Slack: a short **summary message** as the thread parent, with the full
report rendered to **Word (.docx)** and attached in that thread. Script:
`scripts/post_report_to_slack.py` (renders via `scripts/render_report_docx.py`).

## Which path

Connecting Slack as a **claude.ai connector** does NOT make it available to this local Claude Code
(CLI) session — that connector is for the cloud `/schedule` routines, a different environment. For
local + unattended weekly delivery (and for attaching a Word file, which connectors often cannot do),
use the **bot-token script** below. It needs no MCP and runs from cron/`launchd`.

## One-time setup (your hands — I cannot create the app or authorise OAuth)

1. Go to <https://api.slack.com/apps> → **Create New App** → **From scratch**. Name it (e.g.
   "Edlintics CMO"); pick your workspace.
2. **OAuth & Permissions** → **Scopes** → **Bot Token Scopes** → add:
   - `chat:write`
   - `files:write`
3. **Install to Workspace** (top of the same page) → authorise → copy the **Bot User OAuth Token**
   (starts `xoxb-`).
4. In Slack, pick/create the channel for reports (e.g. `#edlintics-cmo`) and **invite the bot**:
   type `/invite @Edlintics CMO` in that channel.
5. Get the **channel ID**: click the channel name → scroll to the bottom of the About tab → copy the
   ID (starts `C`). (Or right-click the channel → Copy link; the ID is the `C…` in the URL.)
6. In this repo's **`.env.local`** (or `.env` — both gitignored; do not commit, do not paste the
   token in chat) set:
   ```
   SLACK_BOT_TOKEN=xoxb-...
   SLACK_CHANNEL_ID=C0123456789
   ```
   Optional: `SLACK_PARENT_TS=` to keep every week under one standing thread.

## Test

```bash
# dry run — renders the docx, prints the summary, sends nothing:
python3 scripts/post_report_to_slack.py

# real post (latest weekly report) once the keys are set:
python3 scripts/post_report_to_slack.py --send
```

The script posts the summary, then uploads the Word doc into that message's thread. Without `--send`
(or without the keys) it always dry-runs. Nothing posts until you set the keys and pass `--send`.

## Two-way loop: reply in Slack → trigger a CMO session

You reply in the weekly-report thread; a local watcher sees it and triggers a headless CMO session
that acts on your answer and replies in-thread. Components:

- `scripts/slack_watch.py` — polls the report thread (`conversations.replies`), keeps only new
  replies from you, and spawns one `claude -p` session per batch. State in `.slack-watch-state.json`.
- `scripts/slack_say.py` — how the triggered session replies in-thread.
- `scripts/run-slack-watch.sh` + `launchd/com.edlintics.cmo-slack-watch.plist` — run it every 15 min.

**Extra setup (one-time):**
1. **Read scope + reinstall.** The bot needs `channels:history` + `groups:history` (already added to
   the app manifest). After adding scopes you must **reinstall** the app (Install App → Reinstall →
   Allow) or reads fail with `missing_scope`.
2. **(Optional) Lock to your user.** Set `SLACK_OWNER_USER_ID=U...` in `.env.local` so only your
   replies trigger sessions (otherwise any non-bot user in the thread does).
3. **Go live (your call).** Test once supervised, then:
   ```bash
   cp launchd/com.edlintics.cmo-slack-watch.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.edlintics.cmo-slack-watch.plist
   ```
   Stop with `launchctl unload ~/Library/LaunchAgents/com.edlintics.cmo-slack-watch.plist`.

**Guardrails (built in):** only your messages are acted on; the triggered session is instructed to
stay human-gated — it applies internal, reversible decisions (calendar, feature-requests, the
report checklist) and replies in-thread, but does not post publicly elsewhere, send email, or write
into the `tutoring-web` repo. The headless run has a hard timeout so it cannot hang. It uses budget
each trigger, and only fires while the Mac is awake.

## How it ties into the cycle

When `.env` has the Slack keys, the CMO cycle's step 5 can finish by running the poster, so each
weekly report lands in Slack automatically. Wired with the local `launchd` schedule (optional), the
full chain is: local cron → CMO generates the report → posts the summary + Word doc to your thread.
