# Reproducibility guide

## Output classes

The repository separates three classes of output.

**Executable from declared public inputs**

- download manifests, file hashes, and access audit;
- 1988--2025 public monthly panel and synchronized delivered-easing onsets;
- policy-ranked shadow-carry spot returns;
- CFTC positioning, New York Fed ACM, OECD CLI, NFCI, and VIX checks;
- circular-rotation references, episode-bootstrap intervals, leave-one-event ranges, Holm adjustment, and sensitivity results;
- all 36 country pairs and 84 triples in the delivered-easing screen, including common-rotation maxT correction and event-count sensitivity.

**Rebuildable from repository assets**

- the 26-page main paper;
- the 18-page online appendix;
- the 44-page combined `Alt_JMP_v0.2.pdf` edition.

The PDF build combines executable public exhibits with source-paper figures and numerical transcriptions whose underlying calculations are not available here.

**Not independently reproducible from this repository**

- the nine-country 10-year/2-year yield panel;
- fresh-inversion and live-state dates;
- money-market carry portfolios and feasible forward returns;
- core conditional-return, bilateral, and beta regressions;
- original episode-bootstrap calculations.

The paper reports those source estimates, but the repository must not be described as an exact replication. Provenance is recorded in the [copied-material ledger](rewrite/notes/copied_material_ledger.md), and editorial movement/deletion is recorded in the [transformation ledger](rewrite/notes/original_to_rewrite_transformation_ledger.md).

## Why the public event differs from the paper's state

The paper's state is known before the return it classifies. A non-dollar G10 curve enters after a fresh 10-year/2-year inversion, remains live until two consecutive months of steepening, and cannot re-enter without first becoming non-inverted. The aggregate state turns on when at least two curves are live.

The public exercise instead identifies months in which at least three BIS policy rates fall by at least 10 basis points after a three-month quiet period. It measures responses around delivered policy easing. These events can test a stress-and-easing chronology but cannot reconstruct the inversion episodes or validate their predictive timing.

The country-combination screen uses the same delivered-easing definition for every pair and triple. Its event dates are defined by the tested policy-rate subset, while the shadow-carry portfolio continues to rank all nine currencies using lagged policy differentials. The screen is exploratory and multiple-tested.

## Environment

- Windows PowerShell
- Python 3.12 or newer
- MiKTeX with `pdflatex` and BibTeX
- Poppler `pdftoppm`

Create an environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

Dependencies are pinned in `pyproject.toml`.

## One-command workflow

From the repository root:

```powershell
.\run_reproduction.ps1
```

The command:

1. downloads only sources declared in `research_pipeline/config/sources.json` and records retrieval status, byte count, and SHA-256 hash;
2. audits coverage and parseability;
3. rebuilds the public panel, delivered-easing events, mechanism results, inference references, sensitivities, figures, and ledgers;
4. rebuilds the pair/triple country screen and its maxT and threshold diagnostics;
5. runs 21 deterministic tests;
6. builds the main paper and online appendix, combines them, renders every page, and runs PDF preflight.

The expected final line is:

```text
Reproduction run completed successfully.
```

Expected PDFs:

- `output/pdf/When_Yield_Curves_Invert_Together_Main.pdf` — 26 pages
- `output/pdf/When_Yield_Curves_Invert_Together_Online_Appendix.pdf` — 18 pages
- `output/pdf/When_Yield_Curves_Invert_Together_With_Online_Appendix.pdf` — 44 pages
- `Alt_JMP_v0.2.pdf` — release copy of the combined edition

The main bibliography contains the complete 84-entry source reference universe. The appendix bibliography is restricted to works cited in that document.

## Snapshot and current-vintage runs

To reuse raw files already present under `research_pipeline/data/raw/`:

```powershell
.\run_reproduction.ps1 -UseExistingData
```

Raw downloads are ignored by version control. A fresh download reproduces the declared method and records the exact bytes received, but current-vintage FRED/OECD and other provider files can be revised.

To run the public-data and test layers without compiling PDFs:

```powershell
.\run_reproduction.ps1 -UseExistingData -SkipPdf
```

## Current public-data results

Mechanism run:

- 15 synchronized delivered-easing onsets from 1988 through 2025;
- shadow-carry spot return over months 0--1: -1.102 percentage points, conditional-rotation p = 0.195;
- carry-aligned CFTC positioning through month 3: -4.388 percentage points of open interest, p = 0.741;
- ACM expected-rate component through month 3: -0.130 percentage point, raw p = 0.202, Holm p = 0.975;
- no outcome in the six-test primary family survives Holm adjustment.

Country screen:

- 120 enumerated combinations: 36 pairs and 84 triples;
- 42 eligible under the baseline six-event minimum;
- CHF--GBP: six events, two-month shadow-carry spot return -4.63 percentage points, raw p = 0.0088, all-combination maxT p = 0.0418;
- omitting October 2008 changes the CHF--GBP mean to -2.62 percentage points;
- no 5-percent family-wide result remains under minimum event counts of eight or ten.

Authoritative machine-readable records:

- `research_pipeline/outputs/mechanism/ledgers/mechanism_result_ledger.csv`
- `research_pipeline/outputs/mechanism/run_manifest.json`
- `research_pipeline/outputs/country_combinations/data/tested_combination_results.csv`
- `research_pipeline/outputs/country_combinations/run_manifest.json`

## Data and redistribution

The [data-purpose ledger](research_pipeline/DATA_PURPOSE_LEDGER.md) gives every dataset a named hypothesis, required interaction, merge key, timing rule, target output, keep rule, and limitation. Downloads without an analytical purpose are rejected or deferred.

Public availability does not automatically grant redistribution rights. Raw files remain local and ignored by Git. No reuse license is granted for the software, paper text, source PDF, or recovered exhibits. A separate archived release should review provider terms and source-asset permissions.

## Continuous integration

The GitHub Actions workflow installs the pinned Python layer and runs the same 21 deterministic unit tests. It excludes live downloads and the LaTeX build because provider revisions and TeX installation are unsuitable for a lightweight per-commit check.
