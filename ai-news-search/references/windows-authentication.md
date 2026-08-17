# Windows authentication paths

Use this reference when Folo or X authentication fails on Windows.

## Folo CLI

1. Confirm `node`, `npm`, and `npx` are discoverable.
2. Run `npx --yes folocli@latest login --timeout 600` in a visible, persistent PowerShell window. The browser callback listener must remain alive until authorization finishes.
3. Treat browser account login and CLI authorization as separate states. Completion requires both a successful callback page and `~/.folo/config.json`.
4. Verify with `npx --yes folocli@latest whoami --format json` before collecting data.
5. Use `timeline`, `subscription list`, and `search trending` as the primary collection surfaces. On CLI 0.0.5, `opml export` can fail with an internal serialization error while the other commands remain healthy.
6. Keep callback tokens out of chat, logs, commits, and report artifacts.

## X cookies

1. Run `scripts/open_X_login_cdp.ps1` to start an isolated Edge/Chrome profile with a local debugging port and the required `--remote-allow-origins` value.
2. Let the user enter passwords, MFA, and CAPTCHA in the visible browser window.
3. Run `scripts/export_X_cookies_cdp.py`; it exports only X/Twitter-domain cookies and does not print values.
4. Require `scripts/validate_X_cookies.py` to confirm `auth_token` and `ct0` before starting the X worker.
5. Treat expiry warnings as a refresh signal. If validation fails, report the authenticated coverage gap and use the public-index fallback.

## Secret handling

- Keep `x_cookies.json`, Folo config, OPML, and subscription exports out of version control.
- Never include credential values in worker returns, terminal summaries, reports, slides, or videos.
- Prefer isolated browser profiles so collection setup does not inspect the user's daily browser profile.
