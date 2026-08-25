param(
    [switch]$UseExistingData,
    [switch]$SkipPdf
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonCommand = Get-Command python.exe -ErrorAction Stop | Select-Object -ExpandProperty Source
$OriginalRunHead = [Environment]::GetEnvironmentVariable('IYC_RUN_HEAD', 'Process')
$OriginalRunStartedClean = [Environment]::GetEnvironmentVariable('IYC_RUN_STARTED_CLEAN', 'Process')
$GitCommand = Get-Command git.exe -ErrorAction SilentlyContinue
if ($GitCommand) {
    $env:IYC_RUN_HEAD = (& $GitCommand.Source -C $ProjectRoot rev-parse HEAD).Trim()
    $PendingAtStart = & $GitCommand.Source -C $ProjectRoot status --porcelain
    $env:IYC_RUN_STARTED_CLEAN = if ($PendingAtStart) { 'false' } else { 'true' }
}

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
    Copy-Item -LiteralPath 'research_pipeline/outputs/country_combinations/tables/public_country_combination_proxy.tex' -Destination 'rewrite/generated/public_country_combination_proxy.tex' -Force

    & $PythonCommand 'research_pipeline/src/source_reported_neighborhood.py'
    if ($LASTEXITCODE -ne 0) { throw 'Reported-rule-neighborhood audit failed.' }

    & $PythonCommand 'research_pipeline/src/public_yield_proxy_v03.py'
    if ($LASTEXITCODE -ne 0) { throw 'Public yield-curve proxy audit failed.' }

    & $PythonCommand 'research_pipeline/src/render_v03_public_tables.py'
    if ($LASTEXITCODE -ne 0) { throw 'Public v0.3 table rendering failed.' }

    Copy-Item -LiteralPath 'research_pipeline/outputs/v03/source_reported_neighborhood/reported_rule_neighborhood.pdf' -Destination 'rewrite/generated/v03_reported_rule_neighborhood.pdf' -Force
    Copy-Item -LiteralPath 'research_pipeline/outputs/v03/source_reported_neighborhood/reported_rule_neighborhood.png' -Destination 'rewrite/generated/v03_reported_rule_neighborhood.png' -Force

    & $PythonCommand -m unittest discover -s 'research_pipeline/tests' -v
    if ($LASTEXITCODE -ne 0) { throw 'Unit tests failed.' }

    if (-not $SkipPdf) {
        & '.\rewrite\build.ps1'
        if ($LASTEXITCODE -ne 0) { throw 'PDF build failed.' }

        & $PythonCommand 'rewrite/verify_pdfs.py'
        if ($LASTEXITCODE -ne 0) { throw 'PDF preflight failed.' }

        Copy-Item -LiteralPath 'output/pdf/When_Yield_Curves_Invert_Together_With_Online_Appendix.pdf' -Destination 'Alt_JMP_v0.3.pdf' -Force
    }
}
finally {
    Pop-Location
    if ($null -eq $OriginalRunHead) {
        Remove-Item Env:IYC_RUN_HEAD -ErrorAction SilentlyContinue
    } else {
        $env:IYC_RUN_HEAD = $OriginalRunHead
    }
    if ($null -eq $OriginalRunStartedClean) {
        Remove-Item Env:IYC_RUN_STARTED_CLEAN -ErrorAction SilentlyContinue
    } else {
        $env:IYC_RUN_STARTED_CLEAN = $OriginalRunStartedClean
    }
}

Write-Host 'Reproduction run completed successfully.'
