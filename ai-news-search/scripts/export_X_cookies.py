#!/usr/bin/env python3
"""Export X/Twitter cookies from a local browser (Chrome/Edge) into cookies.json.

The cookie file is used by the X collection track (xgo.ing RSS bridges or
browser automation). Cookies are decrypted with the macOS Keychain, so the
script only works on macOS with the same user account that owns the browser
profile.

Usage:
    python3 scripts/export_X_cookies.py [--browser chrome|edge] [--profile Default]
"""

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path


CHROME_COOKIES = Path.home() / "Library/Application Support/Google/Chrome/Default/Cookies"
EDGE_COOKIES = Path.home() / "Library/Application Support/Microsoft Edge/Default/Cookies"
KEYCHAIN_SERVICE = "Chrome Safe Storage"
OUTPUT = Path(__file__).resolve().parent.parent / "x_cookies.json"


def get_keychain_password(service):
    """Read the cookie decryption key from the macOS Keychain."""
    try:
        out = subprocess.check_output(
            ["security", "find-generic-password", "-w", "-s", service],
            stderr=subprocess.DEVNULL,
        )
        return out.decode().strip()
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"Keychain read failed for '{service}': {exc}", file=sys.stderr)
        return None


def decrypt_value(encrypted, key):
    """Decrypt a Chrome cookie value (AES-128-CBC with 'v10' prefix)."""
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    if not encrypted.startswith(b"v10"):
        return encrypted.decode("utf-8", errors="replace")
    payload = encrypted[3:]
    nonce, ciphertext = payload[:12], payload[12:]
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce))
    dec = cipher.decryptor()
    return dec.update(ciphertext) + dec.finalize()


def export_cookies(db_path, key, output_path):
    """Copy the locked DB to a temp file, read X cookies, write JSON."""
    if not db_path.exists():
        print(f"Cookie DB not found: {db_path}", file=sys.stderr)
        return False

    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    shutil.copy2(db_path, tmp.name)

    cookies = []
    try:
        con = sqlite3.connect(tmp.name)
        cur = con.execute(
            "SELECT host_key, name, path, expires_utc, encrypted_value "
            "FROM cookies WHERE host_key LIKE '%x.com%' OR host_key LIKE '%twitter.com%'"
        )
        for host, name, path, expires, enc in cur.fetchall():
            try:
                value = decrypt_value(bytes(enc), key)
            except Exception:
                continue
            cookies.append(
                {
                    "domain": host,
                    "name": name,
                    "value": value,
                    "path": path,
                    "expires": expires,
                }
            )
        con.close()
    finally:
        os.unlink(tmp.name)

    if not cookies:
        print("No X cookies found in the selected browser profile.", file=sys.stderr)
        return False

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(cookies, indent=2, ensure_ascii=False))
    print(f"Exported {len(cookies)} X cookies to {output_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Export X cookies from local browser")
    parser.add_argument("--browser", choices=["chrome", "edge"], default="chrome")
    parser.add_argument("--output", default=str(OUTPUT))
    args = parser.parse_args()

    db = CHROME_COOKIES if args.browser == "chrome" else EDGE_COOKIES
    key = get_keychain_password(KEYCHAIN_SERVICE)
    if not key:
        print("Cannot decrypt cookies without the Keychain password.", file=sys.stderr)
        sys.exit(1)

    # Chrome derives the AES key from PBKDF2-HMAC-SHA1 of the Keychain secret.
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes

    kdf = PBKDF2HMAC(algorithm=hashes.SHA1(), length=16, salt=b"saltysalt", iterations=1003)
    aes_key = kdf.derive(key.encode())

    ok = export_cookies(db, aes_key, Path(args.output))
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()

