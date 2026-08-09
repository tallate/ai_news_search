#!/usr/bin/env bash
# Ensure X cookies exist and are valid for the X collection track.
#
# Flow:
#   1. If x_cookies.json is missing -> open browser login (CDP) and export cookies.
#   2. Validate the cookie file; if invalid/expired -> re-login and re-export.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
COOKIE_FILE="${PROJECT_DIR}/x_cookies.json"

python3 "$SCRIPT_DIR/validate_X_cookies.py" "$COOKIE_FILE" >/dev/null 2>&1 && {
  echo "X cookies are valid."
  exit 0
}

echo "X cookies missing or expired. Opening X login (Chrome DevTools Protocol)..."
"$SCRIPT_DIR/open_X_login_cdp.sh"

echo "Exporting cookies from browser profile..."
python3 "$SCRIPT_DIR/export_X_cookies.py" --output "$COOKIE_FILE"

if python3 "$SCRIPT_DIR/validate_X_cookies.py" "$COOKIE_FILE"; then
  echo "X cookies ready."
else
  echo "Cookie refresh failed. Log in to X in the opened browser, then re-run this script." >&2
  exit 1
fi

