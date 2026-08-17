$ErrorActionPreference = 'Stop'
$host.UI.RawUI.WindowTitle = 'Folo CLI Official Login'
$env:npm_config_loglevel = 'error'

Set-Location -LiteralPath 'L:\WORKSPACE\ai_news_search\ai-news-search'
Write-Host 'Starting the official Folo CLI browser login...'
& npx --yes folocli@latest login --timeout 600 --verbose

$configPath = Join-Path $env:USERPROFILE '.folo\config.json'
if ($LASTEXITCODE -eq 0 -and (Test-Path -LiteralPath $configPath)) {
    Write-Host 'VERIFIED: Folo CLI config created.' -ForegroundColor Green
} else {
    Write-Host "FAILED: exit=$LASTEXITCODE; config exists=$(Test-Path -LiteralPath $configPath)" -ForegroundColor Red
}

Read-Host 'Press Enter to close'
