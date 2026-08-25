param(
    [ValidateNotNullOrEmpty()]
    [string]$OutputName = 'dissertation_reviewed.pdf'
)

$ErrorActionPreference = 'Stop'
$project = $PSScriptRoot
$build = Join-Path $project '_build'

if ([System.IO.Path]::GetFileName($OutputName) -ne $OutputName) {
    throw 'OutputName must be a file name without a directory path.'
}

$toolDirectory = [System.IO.Path]::GetFullPath(
    [System.IO.Path]::Combine($project, '..', '_tools', 'tectonic')
)
$bundledCandidates = @(
    (Join-Path $toolDirectory 'tectonic.exe'),
    (Join-Path $toolDirectory 'tectonic')
)
$tectonic = $bundledCandidates |
    Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } |
    Select-Object -First 1

if (-not $tectonic) {
    $cmd = Get-Command tectonic -ErrorAction SilentlyContinue
    if ($cmd) {
        $tectonic = $cmd.Source
    }
}

if (-not $tectonic) {
    $architecture = [System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString()
    if ($architecture -ne 'X64') {
        throw "Automatic Tectonic installation is unavailable for Windows architecture $architecture. Install Tectonic in PATH."
    }

    Write-Host 'Tectonic was not found. Downloading the latest official Windows release...'
    New-Item -ItemType Directory -Force -Path $toolDirectory | Out-Null

    [System.Net.ServicePointManager]::SecurityProtocol =
        [System.Net.ServicePointManager]::SecurityProtocol -bor
        [System.Net.SecurityProtocolType]::Tls12

    $headers = @{ 'User-Agent' = 'dima-phd-build' }
    $release = Invoke-RestMethod `
        -Uri 'https://api.github.com/repos/tectonic-typesetting/tectonic/releases/latest' `
        -Headers $headers
    $asset = $release.assets |
        Where-Object { $_.name -match 'x86_64-pc-windows-msvc\.zip$' } |
        Select-Object -First 1

    if (-not $asset) {
        throw 'The latest official Tectonic release has no Windows x64 archive.'
    }

    $archive = Join-Path $toolDirectory '.tectonic-download.zip'
    try {
        Invoke-WebRequest `
            -Uri $asset.browser_download_url `
            -Headers $headers `
            -OutFile $archive `
            -UseBasicParsing
        Expand-Archive -LiteralPath $archive -DestinationPath $toolDirectory -Force
    } finally {
        Remove-Item -LiteralPath $archive -Force -ErrorAction SilentlyContinue
    }

    $tectonic = Join-Path $toolDirectory 'tectonic.exe'
    if (-not (Test-Path -LiteralPath $tectonic -PathType Leaf)) {
        throw 'The downloaded Tectonic archive did not contain tectonic.exe.'
    }
}

New-Item -ItemType Directory -Force -Path $build | Out-Null

Push-Location $project
try {
    & $tectonic 'main.tex' --outdir $build --keep-logs
    if ($LASTEXITCODE -ne 0) {
        throw "Build failed with exit code $LASTEXITCODE"
    }
    $output = Join-Path $project $OutputName
    Copy-Item -LiteralPath (Join-Path $build 'main.pdf') -Destination $output -Force
    Write-Host "Ready: $output"
} finally {
    Pop-Location
}
