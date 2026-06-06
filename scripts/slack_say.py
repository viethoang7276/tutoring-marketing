#!/usr/bin/env python3
"""Post a plain-text message to the Slack report thread (or channel).

Used by triggered CMO sessions to reply in-thread. Usage:
    python3 scripts/slack_say.py "your message"        # replies in the report thread
    python3 scripts/slack_say.py "msg" --no-thread     # posts to channel top-level
Thread = SLACK_PARENT_TS if set, else the ts in .slack-last-thread (written by the report poster).
"""
import sys
from pathlib import Path
from _slack_common import load_env, slack_api, REPO


def main():
    argv = sys.argv[1:]
    no_thread = "--no-thread" in argv
    text = None
    if "--file" in argv:
        text = Path(argv[argv.index("--file") + 1]).read_text(encoding="utf8")
    else:
        pos = [a for a in argv if not a.startswith("--")]
        text = pos[0] if pos else None
    if not text:
        sys.exit('usage: slack_say.py "text" | --file PATH [--no-thread]')
    env = load_env()
    token, channel = env.get("SLACK_BOT_TOKEN", ""), env.get("SLACK_CHANNEL_ID", "")
    if not token or not channel:
        sys.exit("SLACK_BOT_TOKEN / SLACK_CHANNEL_ID not set in .env.local")
    thread = env.get("SLACK_PARENT_TS", "")
    if not thread:
        f = REPO / ".slack-last-thread"
        thread = f.read_text().strip() if f.exists() else ""
    body = {"channel": channel, "text": text}
    if thread and not no_thread:
        body["thread_ts"] = thread
    out = slack_api("chat.postMessage", token, json_body=body)
    print("posted ts", out["ts"])


if __name__ == "__main__":
    main()
