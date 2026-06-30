#!/usr/bin/env bash
# SessionStart hook: ensures a Jekyll dev server is running with --watch,
# so editing files + Ctrl+R in the browser is enough to see changes
# (no need to stop/restart the server).
set -uo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-/home/saps/projects/hksaperstein.github.io}"
PORT=4000
PIDFILE="/tmp/jekyll-hksaperstein-site.pid"
LOGFILE="/tmp/jekyll-hksaperstein-site.log"
BASEURL=$(grep -oP '(?<=^baseurl: ").*(?=")' "$PROJECT_DIR/_config.yml" 2>/dev/null)
URL="http://127.0.0.1:${PORT}${BASEURL}/"

json_message() {
  printf '{"systemMessage": "%s"}\n' "$1"
}

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; then
  json_message "Jekyll dev server already running at ${URL} (pid $(cat "$PIDFILE")). Edit + Ctrl+R in the browser, no restart needed."
  exit 0
fi

cd "$PROJECT_DIR" || exit 0

if (exec 3<>"/dev/tcp/127.0.0.1/${PORT}") 2>/dev/null; then
  exec 3<&- 3>&-
  json_message "Port ${PORT} is already in use by another process (likely ${URL}); not starting a new Jekyll server."
  exit 0
fi

setsid nohup bundle exec jekyll serve --watch --port "${PORT}" > "${LOGFILE}" 2>&1 < /dev/null &
disown

PID=""
for _ in 1 2 3 4 5 6; do
  sleep 1
  PID=$(pgrep -f "jekyll serve.*--port ${PORT}" | head -1)
  [ -n "$PID" ] && break
done

if [ -n "$PID" ]; then
  echo "$PID" > "$PIDFILE"
  json_message "Started Jekyll dev server: ${URL} (pid ${PID}). Auto-rebuilds on save — refresh the browser (Ctrl+R) to see changes, no restart needed. Log: ${LOGFILE}"
else
  json_message "Tried to start the Jekyll dev server (expected ${URL}) but couldn't confirm it came up. Check ${LOGFILE}."
fi
