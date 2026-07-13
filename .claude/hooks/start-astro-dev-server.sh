#!/usr/bin/env bash
# SessionStart hook: ensures the Astro dev server is running.
# Vite HMR means edits show up in the browser automatically - no refresh,
# no restart needed.
set -uo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-/home/saps/projects/hksaperstein.github.io}"
PORT=4321
PIDFILE="/tmp/astro-hksaperstein-site.pid"
LOGFILE="/tmp/astro-hksaperstein-site.log"
URL="http://127.0.0.1:${PORT}/"

# System node is too old for Astro; use the local node 22 install.
export PATH="$HOME/.local/node22/bin:$PATH"

json_message() {
  printf '{"systemMessage": "%s"}\n' "$1"
}

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; then
  json_message "Astro dev server already running at ${URL} (pid $(cat "$PIDFILE")). HMR is on - edits appear in the browser automatically."
  exit 0
fi

cd "$PROJECT_DIR" || exit 0

if (exec 3<>"/dev/tcp/127.0.0.1/${PORT}") 2>/dev/null; then
  exec 3<&- 3>&-
  json_message "Port ${PORT} is already in use by another process (likely ${URL}); not starting a new Astro dev server."
  exit 0
fi

setsid nohup npm run dev -- --port "${PORT}" --host 127.0.0.1 > "${LOGFILE}" 2>&1 < /dev/null &
disown

PID=""
for _ in 1 2 3 4 5 6; do
  sleep 1
  PID=$(pgrep -f "astro dev.*--port ${PORT}" | head -1)
  [ -n "$PID" ] && break
done

if [ -n "$PID" ]; then
  echo "$PID" > "$PIDFILE"
  json_message "Started Astro dev server: ${URL} (pid ${PID}). HMR is on - edits appear in the browser automatically. Log: ${LOGFILE}"
else
  json_message "Tried to start the Astro dev server (expected ${URL}) but couldn't confirm it came up. Check ${LOGFILE}."
fi
