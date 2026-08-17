$ErrorActionPreference = 'Stop'
$host.UI.RawUI.WindowTitle = 'Folo CLI Login (local only)'

Write-Host 'Copy only the value after token= from the Folo callback URL.'
Write-Host 'Paste it below. The value will not be displayed.'
$secureToken = Read-Host 'Folo session token' -AsSecureString
$ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureToken)

try {
    $token = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
    $env:npm_config_loglevel = 'error'
    & npx --yes folocli@latest login --token $token
    if ($LASTEXITCODE -ne 0) {
        throw "Folo CLI login failed with exit code $LASTEXITCODE"
    }
    Write-Host 'Folo CLI login completed. You may close this window.' -ForegroundColor Green
} finally {
    $token = $null
    $secureToken = $null
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
}

Read-Host 'Press Enter to close'
