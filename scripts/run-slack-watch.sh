#!/bin/zsh
# launchd entrypoint for the Slack watcher. Sets PATH so `claude` + node resolve in a
# non-interactive context (launchd does not source your shell profile), then runs one poll.
export PATH="/Users/hoangtruong/.nvm/versions/node/v22.16.0/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
cd /Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing || exit 1
mkdir -p logs
exec python3 scripts/slack_watch.py >> logs/slack-watch.log 2>&1
