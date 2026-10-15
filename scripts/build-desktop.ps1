# Full desktop build: sidecar -> frontend -> tauri build (NSIS installer).
# Usage: pwsh scripts/build-desktop.ps1 [-Placeholder] [-SkipSidecar] [-SkipFrontend]
#   -Placeholder   use desktop/placeholder-dist instead of app/dist (smoke tests only)
param([switch]$Placeholder, [switch]$SkipSidecar, [switch]$SkipFrontend)
$ErrorActionPreference = 'Continue'  # native tools write progress to stderr; we check $LASTEXITCODE explicitly
$Root    = Split-Path -Parent $PSScriptRoot
$Desktop = Join-Path $Root 'desktop'
$App     = Join-Path $Root 'app'

if (-not $SkipSidecar) { & (Join-Path $PSScriptRoot 'build-sidecar.ps1') }

$useDist = 'app'
if (-not $Placeholder -and -not $SkipFrontend -and (Test-Path (Join-Path $App 'package.json'))) {
    if (-not (Test-Path (Join-Path $App 'node_modules'))) {
        npm --prefix $App install
        if ($LASTEXITCODE -ne 0) { throw 'npm install (app) failed' }
    }
    npm --prefix $App run build
    if ($LASTEXITCODE -ne 0) { throw 'frontend build failed' }
}
if ($Placeholder -or -not (Test-Path (Join-Path $App 'dist\index.html'))) {
    Write-Warning 'app/dist not found (or -Placeholder): bundling desktop/placeholder-dist (NOT the real game UI).'
    $useDist = 'placeholder'
}

if (-not (Test-Path (Join-Path $Desktop 'node_modules\.bin\tauri.cmd'))) {
    npm --prefix $Desktop install
    if ($LASTEXITCODE -ne 0) { throw 'npm install (desktop) failed' }
}

Push-Location $Desktop
try {
    if ($useDist -eq 'placeholder') {
        npx tauri build --config src-tauri/tauri.placeholder.conf.json
    } else {
        npx tauri build
    }
    if ($LASTEXITCODE -ne 0) { throw "tauri build failed ($LASTEXITCODE)" }
} finally { Pop-Location }

$Bundle = Join-Path $Desktop 'src-tauri\target\release\bundle\nsis'
Get-ChildItem $Bundle -Filter *.exe | ForEach-Object {
    Write-Host ("installer: {0}  ({1} MB)" -f $_.FullName, [math]::Round($_.Length / 1MB, 1))
}
Write-Host "frontend bundled: $useDist"
