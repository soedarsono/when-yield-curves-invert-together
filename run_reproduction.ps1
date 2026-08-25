param(
    [switch]$UseExistingData,
    [switch]$SkipPdf
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonCommand = Get-Command python.exe -ErrorAction Stop | Select-Object -ExpandProperty Source

Push-Location $ProjectRoot
try {
    if (-not $UseExistingData) {
        & $PythonCommand 'research_pipeline/src/download_public_data.py'
        if ($LASTEXITCODE -ne 0) { throw 'Public-data download failed.' }
    }

    & $PythonCommand 'research_pipeline/src/audit_public_data.py'
    if ($LASTEXITCODE -ne 0) { throw 'Public-data audit failed.' }

    & $PythonCommand 'research_pipeline/src/run_mechanism_checks.py'
    if ($LASTEXITCODE -ne 0) { throw 'Mechanism-check pipeline failed.' }

    & $PythonCommand 'research_pipeline/src/country_combination_proxy.py'
    if ($LASTEXITCODE -ne 0) { throw 'Country-combination analysis failed.' }

    & $PythonCommand -m unittest discover -s 'research_pipeline/tests' -v
    if ($LASTEXITCODE -ne 0) { throw 'Unit tests failed.' }

    if (-not $SkipPdf) {
        & '.\rewrite\build.ps1'
        if ($LASTEXITCODE -ne 0) { throw 'PDF build failed.' }

        & $PythonCommand 'rewrite/verify_pdfs.py'
        if ($LASTEXITCODE -ne 0) { throw 'PDF preflight failed.' }

        Copy-Item -LiteralPath 'output/pdf/When_Yield_Curves_Invert_Together_With_Online_Appendix.pdf' -Destination 'Alt_JMP_v0.2.pdf' -Force
    }
}
finally {
    Pop-Location
}

Write-Host 'Reproduction run completed successfully.'
