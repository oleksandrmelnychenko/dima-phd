param(
    [string]$OutputName = 'dissertation.pdf'
)

$ErrorActionPreference = 'Stop'
$project = $PSScriptRoot
$build = Join-Path $project '_build'
New-Item -ItemType Directory -Force -Path $build | Out-Null

$bundled = Join-Path $project '..\_tools\tectonic\tectonic.exe'
if (Test-Path -LiteralPath $bundled) {
    $tectonic = $bundled
} else {
    $cmd = Get-Command tectonic -ErrorAction SilentlyContinue
    if (-not $cmd) {
        throw 'Tectonic was not found. Install it or add the executable to PATH.'
    }
    $tectonic = $cmd.Source
}

Push-Location $project
try {
    & $tectonic 'main.tex' --outdir $build --keep-logs
    if ($LASTEXITCODE -ne 0) {
        throw "Build failed with exit code $LASTEXITCODE"
    }
    Copy-Item -LiteralPath (Join-Path $build 'main.pdf') -Destination (Join-Path $project $OutputName) -Force
    Write-Host "Ready: $(Join-Path $project $OutputName)"
} finally {
    Pop-Location
}
