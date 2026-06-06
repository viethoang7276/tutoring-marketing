#!/usr/bin/env python3
"""Watch the weekly-report Slack thread for new replies from Hoang and trigger a CMO session.

Loop: read the report thread's replies via conversations.replies since the last-seen ts (state in
.slack-watch-state.json), keep only NEW messages from the owner (not the bot), and if any exist,
spawn ONE headless CMO session (`claude -p`) to act on them. The triggered session reads the reply
plus docs/cmo-cycle.md, applies Hoang's internal/reversible decisions, and replies in-thread.

Guardrails: only messages from the owner are acted on (SLACK_OWNER_USER_ID if set; otherwise any
non-bot user in this private thread). The triggered session is told to stay human-gated — no public
posts beyond the report thread, no email, no writing into the tutoring-web repo. The subprocess has
a hard timeout so a stuck session cannot hang the watcher.

Env (.env / .env.local): SLACK_BOT_TOKEN, SLACK_CHANNEL_ID, plus the thread to watch
(SLACK_PARENT_TS or .slack-last-thread). Optional: SLACK_OWNER_USER_ID, CLAUDE_BIN, CLAUDE_TOOLS,
CLAUDE_PERMISSION_MODE, CLAUDE_TIMEOUT.

Usage: python3 scripts/slack_watch.py [--dry-run]
"""
import sys, os, json, subprocess
from pathlib import Path
from _slack_common import load_env, slack_api, REPO

STATE = REPO / ".slack-watch-state.json"
DEFAULT_BIN = str(Path.home() / ".nvm/versions/node/v22.16.0/bin/claude")


def watched_thread(env):
    ts = env.get("SLACK_PARENT_TS", "")
    if ts:
        return ts
    f = REPO / ".slack-last-thread"
    return f.read_text().strip() if f.exists() else ""


def build_prompt(messages):
    return (
        "You are the Edlintics CMO, triggered by Hoang's reply in the weekly-report Slack thread. "
        "Follow docs/cmo-cycle.md and session-start.md. Hoang replied:\n\n" + messages + "\n\n"
        "Read the latest docs/reports/*-cmo-weekly.md, then act on his answers: apply his internal, "
        "reversible decisions — update calendar/calendar.json (validate with `npm run calendar`), "
        "docs/feature-requests/, and tick the report's decisions checklist. "
        "STAY HUMAN-GATED: do not post publicly anywhere except this report thread, do not send "
        "email, and never write into the ../tutoring-web repo (only Hoang relays approved feature "
        "requests). When done, post a short summary of exactly what you changed by running: "
        "python3 scripts/slack_say.py \"<summary>\"  (it replies in this thread). "
        "Brand voice: calm, direct, no exclamation points, no emoji."
    )


def main():
    dry = "--dry-run" in sys.argv
    env = load_env()
    token, channel = env.get("SLACK_BOT_TOKEN", ""), env.get("SLACK_CHANNEL_ID", "")
    thread = watched_thread(env)
    owner = env.get("SLACK_OWNER_USER_ID", "")
    if not (token and channel and thread):
        sys.exit("Need SLACK_BOT_TOKEN, SLACK_CHANNEL_ID, and a thread (SLACK_PARENT_TS or "
                 ".slack-last-thread). Post a weekly report first, or set SLACK_PARENT_TS.")

    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    last = state.get(thread, thread)  # default: the thread root (process replies after it)

    replies = slack_api("conversations.replies", token,
                        data={"channel": channel, "ts": thread, "oldest": last, "limit": "100"})
    bot_user = slack_api("auth.test", token).get("user_id")

    new = []
    for m in replies.get("messages", []):
        ts = m.get("ts", "0")
        if float(ts) <= float(last):
            continue
        if m.get("bot_id") or m.get("subtype") == "bot_message" or m.get("user") == bot_user:
            continue
        if owner and m.get("user") != owner:
            continue
        if m.get("text", "").strip():
            new.append(m)

    if not new:
        print("No new owner replies.")
        return

    combined = "\n".join(f"- {m['text']}" for m in new)
    max_ts = max(m["ts"] for m in new)
    print(f"{len(new)} new reply(ies):\n{combined}")

    if dry:
        print("\n[DRY RUN] would trigger one headless CMO session. State not advanced.")
        return

    bin_ = env.get("CLAUDE_BIN", DEFAULT_BIN)
    tools = env.get("CLAUDE_TOOLS", "Bash Read Write Edit WebSearch WebFetch Glob Grep").split()
    mode = env.get("CLAUDE_PERMISSION_MODE", "acceptEdits")
    timeout = int(env.get("CLAUDE_TIMEOUT", "900"))
    cmd = [bin_, "-p", build_prompt(combined), "--permission-mode", mode, "--allowedTools", *tools]
    run_env = dict(os.environ)
    run_env["PATH"] = str(Path(bin_).parent) + ":" + run_env.get("PATH", "")

    print(f"Triggering headless CMO session (timeout {timeout}s)...")
    try:
        r = subprocess.run(cmd, cwd=str(REPO), env=run_env, timeout=timeout,
                           capture_output=True, text=True)
        print((r.stdout or "")[-2000:] or "(no stdout)")
        if r.returncode != 0:
            print("session exit", r.returncode, (r.stderr or "")[-1000:])
    except subprocess.TimeoutExpired:
        print("session timed out — advancing state to avoid a reprocessing loop")

    state[thread] = max_ts  # advance even on failure: never reprocess the same reply forever
    STATE.write_text(json.dumps(state))


if __name__ == "__main__":
    main()
