param(
    [switch]$SkipRender,
    [string]$PdfLatexPath = $env:IYC_PDFLATEX,
    [string]$BibtexPath = $env:IYC_BIBTEX,
    [string]$PdfToPpmPath = $env:IYC_PDFTOPPM,
    [string]$PythonPath = $env:IYC_PYTHON
)

$ErrorActionPreference = 'Stop'
$RewriteRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$WorkspaceRoot = Split-Path -Parent $RewriteRoot
$OutputRoot = Join-Path $WorkspaceRoot 'output\pdf'
$RenderRoot = Join-Path $WorkspaceRoot 'tmp\pdfs'

function Resolve-ToolPath {
    param(
        [string]$ExplicitPath,
        [string]$CommandName,
        [string[]]$CandidatePaths = @()
    )
    if ($ExplicitPath) {
        if (-not (Test-Path -LiteralPath $ExplicitPath -PathType Leaf)) {
            throw "Configured path for $CommandName does not exist: $ExplicitPath"
        }
        return (Resolve-Path -LiteralPath $ExplicitPath).Path
    }
    $Command = Get-Command $CommandName -ErrorAction SilentlyContinue
    if ($Command) { return $Command.Source }
    foreach ($CandidatePath in $CandidatePaths) {
        if ($CandidatePath -and (Test-Path -LiteralPath $CandidatePath -PathType Leaf)) {
            return (Resolve-Path -LiteralPath $CandidatePath).Path
        }
    }
    return $null
}

$MiKTeXRoots = @(
    (Join-Path $env:LOCALAPPDATA 'Programs\MiKTeX\miktex\bin\x64'),
    (Join-Path $env:ProgramFiles 'MiKTeX\miktex\bin\x64')
)
$PopplerRoots = @(
    (Join-Path $env:ProgramFiles 'poppler\Library\bin'),
    (Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin')
)
$PdfLatex = Resolve-ToolPath $PdfLatexPath 'pdflatex.exe' ($MiKTeXRoots | ForEach-Object { Join-Path $_ 'pdflatex.exe' })
$Bibtex = Resolve-ToolPath $BibtexPath 'bibtex.exe' ($MiKTeXRoots | ForEach-Object { Join-Path $_ 'bibtex.exe' })
$PdfToPpm = Resolve-ToolPath $PdfToPpmPath 'pdftoppm.exe' ($PopplerRoots | ForEach-Object { Join-Path $_ 'pdftoppm.exe' })
$Python = Resolve-ToolPath $PythonPath 'python.exe'

if (-not $PdfLatex -or -not $Bibtex) {
    throw 'pdflatex.exe or bibtex.exe was not found. Add both to PATH, pass -PdfLatexPath/-BibtexPath, or set IYC_PDFLATEX/IYC_BIBTEX.'
}

New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
New-Item -ItemType Directory -Force -Path $RenderRoot | Out-Null

Push-Location $RewriteRoot
try {
    foreach ($Document in @('main', 'online_appendix')) {
        & $PdfLatex -interaction=nonstopmode -halt-on-error -file-line-error "$Document.tex"
        if ($LASTEXITCODE -ne 0) {
            throw "LaTeX build failed for $Document.tex"
        }

        $AuxPath = Join-Path $RewriteRoot "$Document.aux"
        if (Select-String -LiteralPath $AuxPath -Pattern '\\citation\{' -Quiet) {
            & $Bibtex $Document
            if ($LASTEXITCODE -ne 0) {
                throw "BibTeX build failed for $Document.tex"
            }
        }

        foreach ($Pass in 1..2) {
            & $PdfLatex -interaction=nonstopmode -halt-on-error -file-line-error "$Document.tex"
            if ($LASTEXITCODE -ne 0) {
                throw "LaTeX build pass $Pass failed for $Document.tex"
            }
        }

        $BuiltPdf = Join-Path $RewriteRoot "$Document.pdf"
        $FinalName = if ($Document -eq 'main') {
            'When_Yield_Curves_Invert_Together_Main.pdf'
        } else {
            'When_Yield_Curves_Invert_Together_Online_Appendix.pdf'
        }
        Copy-Item -LiteralPath $BuiltPdf -Destination (Join-Path $OutputRoot $FinalName) -Force

        if (-not $SkipRender) {
            if (-not $PdfToPpm) {
                throw 'pdftoppm.exe was not found; cannot perform required visual-render step.'
            }
            $DocumentRenderRoot = Join-Path $RenderRoot "rewrite_$Document"
            New-Item -ItemType Directory -Force -Path $DocumentRenderRoot | Out-Null
            Get-ChildItem -LiteralPath $DocumentRenderRoot -File -Filter 'page-*.jpg' -ErrorAction SilentlyContinue |
                Remove-Item -Force
            & $PdfToPpm -jpeg -r 110 $BuiltPdf (Join-Path $DocumentRenderRoot 'page')
            if ($LASTEXITCODE -ne 0) {
                throw "PDF rendering failed for $BuiltPdf"
            }
        }
    }

    if (-not $Python) {
        throw 'python.exe was not found; cannot attach the online appendix. Add it to PATH, pass -PythonPath, or set IYC_PYTHON.'
    }
    $CombinedPdf = Join-Path $OutputRoot 'When_Yield_Curves_Invert_Together_With_Online_Appendix.pdf'
    & $Python (Join-Path $RewriteRoot 'combine_pdfs.py') (Join-Path $RewriteRoot 'main.pdf') (Join-Path $RewriteRoot 'online_appendix.pdf') $CombinedPdf
    if ($LASTEXITCODE -ne 0) {
        throw 'Failed to attach the online appendix to the main paper.'
    }
    if (-not $SkipRender) {
        $CombinedRenderRoot = Join-Path $RenderRoot 'rewrite_combined'
        New-Item -ItemType Directory -Force -Path $CombinedRenderRoot | Out-Null
        Get-ChildItem -LiteralPath $CombinedRenderRoot -File -Filter 'page-*.jpg' -ErrorAction SilentlyContinue |
            Remove-Item -Force
        & $PdfToPpm -jpeg -r 110 $CombinedPdf (Join-Path $CombinedRenderRoot 'page')
        if ($LASTEXITCODE -ne 0) {
            throw "PDF rendering failed for $CombinedPdf"
        }
    }
}
finally {
    Pop-Location
}

Write-Host "Built paper PDFs in $OutputRoot"
