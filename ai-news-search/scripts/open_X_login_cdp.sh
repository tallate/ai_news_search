#!/usr/bin/env bash
# Open X login in a browser with Chrome DevTools Protocol (CDP) enabled so
# that cookies can later be exported programmatically.
#
# Usage:
#   ./scripts/open_X_login_cdp.sh [chrome|edge|chromium]
set -euo pipefail

BROWSER="${1:-chrome}"
PORT="${CDP_PORT:-9222}"
PROFILE_DIR="${XDG_RUNTIME_DIR:-$TMPDIR}/x-login-profile-${USER}"
mkdir -p "$PROFILE_DIR"

case "$BROWSER" in
  chrome)
    APP="Google Chrome"
    EXEC="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ;;
  edge)
    APP="Microsoft Edge"
    EXEC="/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
    ;;
  chromium)
    APP="Chromium"
    EXEC="/Applications/Chromium.app/Contents/MacOS/Chromium"
    ;;
  *)
    echo "Unknown browser: $BROWSER" >&2
    exit 2
    ;;
esac

if [[ ! -x "$EXEC" ]]; then
  echo "$APP not found at $EXEC" >&2
  exit 2
fi

echo "Starting $APP with CDP on port $PORT and opening https://x.com"
"$EXEC" \
  --remote-debugging-port="$PORT" \
  --user-data-dir="$PROFILE_DIR" \
  --no-first-run \
  "https://x.com/login" >/dev/null 2>&1 &

echo "Log in to X in the opened window, then run:"
echo "  python3 scripts/export_X_cookies.py"

