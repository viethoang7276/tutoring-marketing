#!/bin/bash
# launchd entry for the weekly performance review (com.edlintics.weekly-performance-review)
cd /Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing || exit 1
echo "=== $(date) start"
/Users/hoangtruong/.nvm/versions/node/v22.16.0/bin/claude -p "$(cat ops/weekly-performance-review.md)" --chrome \
  --permission-mode acceptEdits \
  --allowedTools "mcp__claude-in-chrome__*" "mcp__claude-artifacts__db_get" "mcp__claude-artifacts__db_list" "mcp__claude-artifacts__db_query" "mcp__claude-artifacts__db_write" "Read" "Write" "Edit" "Glob" "Grep" "ToolSearch" "Bash(python3:*)" "Bash(ls:*)" "Bash(date:*)"
echo "=== $(date) end ($?)"
