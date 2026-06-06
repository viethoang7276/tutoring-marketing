#!/usr/bin/env python3
"""
Post a CMO weekly report to Slack: a concise summary message, with the full report
rendered to a Word (.docx) and attached in that message's thread.

Reads secrets from this repo's `.env` (gitignored):
    SLACK_BOT_TOKEN=xoxb-...        (required; bot scopes: chat:write, files:write)
    SLACK_CHANNEL_ID=C0123456789    (required; the channel the bot is invited to)
    SLACK_PARENT_TS=1700000000.0001 (optional; reply under one standing thread instead
                                     of starting a new thread each week)

Usage:
    python3 scripts/post_report_to_slack.py [docs/reports/2026-W23-cmo-weekly.md] [--send]

Safety:
    Without --send (or without a token) it DRY-RUNS: prints the summary it would post and
    the docx it would attach, and sends nothing. Posting a real message requires --send AND
    a token in .env. Nothing is posted by importing this module.
"""
import sys, re, json, os
from pathlib import Path

import requests
from render_report_docx import render

REPO = Path(__file__).resolve().parents[1]
SLACK_API = "https://slack.com/api"


def load_env():
    env = {}
    # .env first, then .env.local overrides it (both gitignored). Real shell env wins last.
    for name in (".env", ".env.local"):
        f = REPO / name
        if not f.exists():
            continue
        for raw in f.read_text(encoding="utf8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("SLACK_BOT_TOKEN", "SLACK_CHANNEL_ID", "SLACK_PARENT_TS"):
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def latest_report():
    reports = sorted((REPO / "docs" / "reports").glob("*-cmo-weekly.md"))
    if not reports:
        sys.exit("No weekly report found in docs/reports/")
    return reports[-1]


def build_summary(md_path):
    """Parent message = title + metadata + the 'Decisions needed' section, in Slack mrkdwn."""
    lines = Path(md_path).read_text(encoding="utf8").splitlines()
    title = next((l[2:].strip() for l in lines if l.startswith("# ")), "CMO weekly report")
    week = next((re.sub(r"^- \*\*Week:\*\*\s*", "", l).strip()
                 for l in lines if l.startswith("- **Week:**")), "")
    source = next((re.sub(r"^- \*\*Data source[^:]*:\*\*\s*", "", l).strip()
                   for l in lines if l.startswith("- **Data source")), "")

    # extract the "Decisions needed" section
    decisions = []
    grab = False
    for l in lines:
        if l.startswith("## ") and "Decisions needed" in l:
            grab = True; continue
        if grab and l.startswith("## "):
            break
        if grab and l.strip():
            decisions.append(l.rstrip())

    def to_mrkdwn(s):
        s = re.sub(r"\*\*(.+?)\*\*", r"*\1*", s)           # **bold** -> *bold*
        s = re.sub(r"^\s*-\s+\[ \]\s+", "☐  ", s)       # - [ ] -> ☐
        s = re.sub(r"^\s*-\s+\[x\]\s+", "☑  ", s, flags=re.I)
        s = re.sub(r"^\s*[-*]\s+", "•  ", s)            # - bullet -> •
        return s

    parts = [f"*{title}*"]
    if week:
        parts.append(f"_{week}_")
    if source:
        parts.append(f"_Data source: {source}_")
    if decisions:
        parts.append("")
        parts.append("*Decisions needed from you*")
        parts.extend(to_mrkdwn(d) for d in decisions)
    parts.append("")
    parts.append(":paperclip: Full report attached in this thread.")
    return "\n".join(parts)


def slack(method, token, **kwargs):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{SLACK_API}/{method}"
    if kwargs.get("_json"):
        headers["Content-Type"] = "application/json; charset=utf-8"
        r = requests.post(url, headers=headers, data=json.dumps(kwargs["_json"]), timeout=30)
    else:
        r = requests.post(url, headers=headers, data=kwargs.get("data"), timeout=30)
    out = r.json()
    if not out.get("ok"):
        sys.exit(f"Slack {method} failed: {out.get('error')}  ({out})")
    return out


def upload_docx_to_thread(token, channel, thread_ts, docx_path, title):
    size = Path(docx_path).stat().st_size
    up = slack("files.getUploadURLExternal", token,
               data={"filename": Path(docx_path).name, "length": str(size)})
    upload_url, file_id = up["upload_url"], up["file_id"]
    with open(docx_path, "rb") as fh:
        r = requests.post(upload_url, files={"file": (Path(docx_path).name, fh)}, timeout=60)
        r.raise_for_status()
    slack("files.completeUploadExternal", token, _json={
        "files": [{"id": file_id, "title": title}],
        "channel_id": channel,
        "thread_ts": thread_ts,
        "initial_comment": "Weekly CMO report (Word).",
    })


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    send = "--send" in sys.argv
    md = Path(args[0]) if args else latest_report()
    if not md.exists():
        sys.exit(f"Report not found: {md}")

    summary = build_summary(md)
    docx_path = render(md, str(md.with_suffix(".docx")))
    env = load_env()
    token = env.get("SLACK_BOT_TOKEN", "")
    channel = env.get("SLACK_CHANNEL_ID", "")
    parent_ts = env.get("SLACK_PARENT_TS", "")

    if not send or not token or not channel:
        why = "no --send flag" if not send else "SLACK_BOT_TOKEN/SLACK_CHANNEL_ID not set"
        print(f"--- DRY RUN ({why}) ---\n")
        print(f"[token  ] {'present' if token else 'MISSING'}")
        print(f"[channel] {channel or '(unset)'}")
        print(f"[thread ] {parent_ts or '(new thread per post)'}")
        print(f"[attach ] {docx_path}\n")
        print("[parent message]\n" + summary)
        print("\nTo actually post: set the keys in .env and re-run with --send")
        return

    # Post parent (or reply under a standing thread), then attach the docx in that thread.
    post_kwargs = {"channel": channel, "text": summary}
    if parent_ts:
        post_kwargs["thread_ts"] = parent_ts
    msg = slack("chat.postMessage", token, _json=post_kwargs)
    thread_ts = parent_ts or msg["ts"]
    upload_docx_to_thread(token, channel, thread_ts, docx_path, title=md.stem)
    print(f"Posted to Slack channel {channel}, thread {thread_ts}. Attached {Path(docx_path).name}.")


if __name__ == "__main__":
    main()
