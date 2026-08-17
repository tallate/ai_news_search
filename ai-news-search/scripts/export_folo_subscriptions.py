#!/usr/bin/env python3
"""Export authenticated Folo subscriptions through the official Folo CLI."""

import json
import shutil
import subprocess
import sys
from pathlib import Path


def export_subscriptions(output_path=None):
    npx = shutil.which("npx.cmd") or shutil.which("npx")
    if not npx:
        raise RuntimeError("npx is unavailable; install Node.js and npm first")

    command = [npx, "--yes", "folocli@latest", "subscription", "list", "--format", "json"]
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "Folo CLI failed")

    payload = json.loads(completed.stdout)
    if not payload.get("ok"):
        error = payload.get("error") or {}
        raise RuntimeError(f"Folo CLI {error.get('code', 'ERROR')}: {error.get('message', '')}")

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Exported authenticated Folo subscriptions to {path}")
    else:
        print(json.dumps(payload, indent=2, ensure_ascii=False))

    return payload


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    export_subscriptions(path)
