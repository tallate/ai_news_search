param(
    [ValidateSet('edge', 'chrome')]
    [string]$Browser = 'edge',
    [int]$Port = 9222
)

$ErrorActionPreference = 'Stop'
$profileDir = Join-Path $env:LOCALAPPDATA 'ai-news-search\x-login-profile'
New-Item -ItemType Directory -Force -Path $profileDir | Out-Null

$candidates = if ($Browser -eq 'edge') {
    @(
        "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
        "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
    )
} else {
    @(
        "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
        "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
    )
}

$exe = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $exe) {
    throw "$Browser executable not found."
}

Start-Process -FilePath $exe -WindowStyle Normal -ArgumentList @(
    "--remote-debugging-port=$Port",
    "--remote-allow-origins=http://127.0.0.1:$Port",
    "--user-data-dir=$profileDir",
    '--no-first-run',
    'https://x.com/i/flow/login'
)

Write-Host 'X login window opened.'
Write-Host 'Log in yourself, keep the window open, then run export_X_cookies_cdp.py.'
