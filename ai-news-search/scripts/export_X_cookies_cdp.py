#!/usr/bin/env python3
"""Export X cookies from a user-controlled Windows browser opened with CDP."""

import argparse
import json
import sys
import urllib.request
from pathlib import Path


OUTPUT = Path(__file__).resolve().parent.parent / "x_cookies.json"
REQUIRED = {"auth_token", "ct0"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9222)
    parser.add_argument("--output", default=str(OUTPUT))
    args = parser.parse_args()

    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{args.port}/json/version", timeout=3
        ) as response:
            websocket_url = json.load(response)["webSocketDebuggerUrl"]
    except Exception as exc:
        print(f"Cannot connect to the local login browser: {exc}", file=sys.stderr)
        return 2

    try:
        from websocket import create_connection
    except ImportError:
        print("Missing dependency: pip install websocket-client", file=sys.stderr)
        return 2

    ws = create_connection(websocket_url, timeout=5)
    try:
        ws.send(json.dumps({"id": 1, "method": "Storage.getCookies"}))
        while True:
            message = json.loads(ws.recv())
            if message.get("id") == 1:
                cookies = message.get("result", {}).get("cookies", [])
                break
    finally:
        ws.close()

    cookies = [
        {
            "domain": item.get("domain"),
            "name": item.get("name"),
            "value": item.get("value"),
            "path": item.get("path", "/"),
            "expires": item.get("expires", 0),
            "secure": item.get("secure", True),
            "httpOnly": item.get("httpOnly", False),
            "sameSite": item.get("sameSite"),
        }
        for item in cookies
        if item.get("domain", "").lstrip(".") in {"x.com", "twitter.com"}
    ]
    names = {item["name"] for item in cookies}
    missing = REQUIRED - names
    if missing:
        print(f"X login is incomplete; missing required cookie names: {sorted(missing)}", file=sys.stderr)
        return 1

    output = Path(args.output)
    output.write_text(json.dumps(cookies, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Exported {len(cookies)} X cookies to {output} (values not displayed).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
