#!/usr/bin/env python3
"""Validate the X cookie file used by the X collection track.

Checks that the file exists, contains the expected cookie names, and that
session cookies have not expired. Exits non-zero if validation fails.

Usage:
    python3 scripts/validate_X_cookies.py [path/to/x_cookies.json]
"""

import json
import sys
import time
from pathlib import Path


REQUIRED = {"auth_token", "ct0"}
SESSION_TTL_SECONDS = 30 * 24 * 3600  # ~30 days


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "x_cookies.json"
    if not path.exists():
        print(f"Cookie file missing: {path}", file=sys.stderr)
        print("Run scripts/export_X_cookies.py or scripts/open_X_login_cdp.sh first.", file=sys.stderr)
        sys.exit(2)

    try:
        cookies = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        print(f"Cookie file is not valid JSON: {exc}", file=sys.stderr)
        sys.exit(2)

    names = {c.get("name") for c in cookies}
    missing = REQUIRED - names
    if missing:
        print(f"Missing required cookies: {sorted(missing)}", file=sys.stderr)
        sys.exit(1)

    oldest_ts = None
    for c in cookies:
        if c.get("expires") and c["expires"] > 0:
            # Chrome-style microseconds epoch
            ts = c["expires"] / 1_000_000 if c["expires"] > 1e15 else c["expires"]
            if oldest_ts is None or ts < oldest_ts:
                oldest_ts = ts

    if oldest_ts and oldest_ts < time.time():
        print("Cookies have expired; re-run the login/cookie refresh flow.", file=sys.stderr)
        sys.exit(1)
    if oldest_ts and oldest_ts - time.time() < SESSION_TTL_SECONDS:
        print("Warning: cookies expire soon, consider refreshing.", file=sys.stderr)

    print(f"OK: {len(cookies)} cookies, required keys present.")
    sys.exit(0)


if __name__ == "__main__":
    main()

