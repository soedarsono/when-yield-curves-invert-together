# Reproducibility guide

## Output classes

The repository separates three classes of output.

**Executable from declared public inputs**

- download manifests, file hashes, and access audit;
- 1988--2025 public monthly panel and synchronized delivered-easing onsets;
- policy-ranked log spot-return proxies;
- CFTC positioning, New York Fed ACM, OECD CLI, NFCI, and VIX checks;
- circular-rotation references, episode-bootstrap intervals, leave-one-event ranges, Holm adjustment, and sensitivity results;
- all 36 country pairs and 84 triples in the delivered-easing screen, including common-rotation maximum-$|z|$ references and event-count sensitivity;
- the current-vintage OECD/FRED 10-year-minus-3-month public proxy, its declared 64-rule family, circular-shift and common-calendar maximum-$|z|$ references, joint delete-one and geographically disjoint checks, sensitivities, and 18-episode ledger;
- paper-facing public-proxy tables and the specification-curve figure rendered from machine-readable outputs.

**Rebuildable from repository assets**

- the 38-page main paper;
- the 27-page online appendix;
- the 65-page combined `Alt_JMP_v0.3.pdf` edition.

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

The delivered-easing exercise instead identifies months in which at least three BIS policy rates fall by at least 10 basis points after a three-month quiet period. It measures responses around delivered policy easing. These events can test a stress-and-easing chronology but cannot reconstruct the inversion episodes or validate their predictive timing.

The country-combination screen uses the same delivered-easing definition for every pair and triple. Its event dates are defined by the tested policy-rate subset, while the shadow-carry portfolio continues to rank all nine currencies using lagged policy differentials. The screen is exploratory and multiple-tested.

The separate public yield-curve exercise uses current-vintage OECD monthly 10-year government yields minus 3-month interbank rates distributed through FRED. Its outcome is a BIS policy-ranked log spot-return proxy, not an executable forward excess return. Target portfolio legs expand to include all currencies tied at a cutoff. It is an adverse sensitivity or challenge test, not a validation or replication of the baseline 10-year-minus-2-year classifier.

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
5. rebuilds the descriptive source-reported rule neighborhood and the current-vintage public 10-year-minus-3-month audit;
6. renders the v0.3 public tables and figures into `rewrite/generated/` and records them in the public-proxy run manifest;
7. runs 39 deterministic tests;
8. builds the main paper and online appendix, combines them, renders every page, runs PDF preflight, and copies the combined edition to `Alt_JMP_v0.3.pdf`.

The expected final line is:

```text
Reproduction run completed successfully.
```

Expected PDFs:

- `output/pdf/When_Yield_Curves_Invert_Together_Main.pdf` — 38 pages
- `output/pdf/When_Yield_Curves_Invert_Together_Online_Appendix.pdf` — 27 pages
- `output/pdf/When_Yield_Curves_Invert_Together_With_Online_Appendix.pdf` — 65 pages
- `Alt_JMP_v0.3.pdf` — byte-identical release copy of the combined edition

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
- policy-ranked log spot-return proxy over months 0--1: -1.061 percentage points, conditional finite-rotation reference value 0.222;
- carry-aligned CFTC positioning through month 3: -6.417 percentage points of open interest, finite-rotation reference 0.568, Holm-adjusted reference 1.000;
- ACM expected-rate component through month 3: -0.130 percentage point, finite-rotation reference 0.202, Holm-adjusted reference 1.000;
- no outcome in the six-test primary family meets the 5-percent Holm-adjusted reference criterion.

Country screen:

- 120 enumerated combinations: 36 pairs and 84 triples;
- 42 eligible under the baseline six-event minimum;
- CHF--GBP: six events, mean cumulative months-0--1 log spot-return proxy -4.54 percentage points, raw rotation reference 0.0088, all-combination maximum-$|z|$ reference 0.0352;
- omitting October 2008 changes the CHF--GBP mean to -2.52 percentage points;
- no result meets the 5-percent family reference criterion under minimum event counts of eight or ten.

Public 10-year-minus-3-month challenge:

- baseline-like annualized active-minus-inactive log spot-return-proxy difference: -3.20 percentage points;
- raw circular-shift reference value 0.335 and common-calendar maximum-$|z|$ reference value 1.000 across the declared 64-rule family;
- 41 of 64 rule estimates are negative, but none meets the 5-percent family reference criterion;
- the baseline-like public state contains 18 episodes.

Family-wise interpretation of the maximum reference is conditional on simultaneous cyclic-shift exchangeability; otherwise it is a finite rotation-reference diagnostic. This is adverse sensitivity evidence. It does not independently validate the paper's unavailable baseline state, and the spot-only outcome is not an executable carry return.

Authoritative machine-readable records:

- `research_pipeline/outputs/mechanism/ledgers/mechanism_result_ledger.csv`
- `research_pipeline/outputs/mechanism/run_manifest.json`
- `research_pipeline/outputs/country_combinations/data/tested_combination_results.csv`
- `research_pipeline/outputs/country_combinations/run_manifest.json`
- `research_pipeline/outputs/v03/source_reported_neighborhood/run_manifest.json`
- `research_pipeline/outputs/v03/yield_proxy/data/specification_family.csv`
- `research_pipeline/outputs/v03/yield_proxy/data/baseline_episode_ledger.csv`
- `research_pipeline/outputs/v03/yield_proxy/run_manifest.json`

## Generated-table linkage and manifests

`research_pipeline/src/render_v03_public_tables.py` reads the public-proxy CSV outputs and writes `rewrite/generated/tables/v03_public_proxy_summary.tex`, `v03_public_loo_disjoint.tex`, and `v03_public_episode_ledger.tex`. It also mirrors the specification-curve PNG into `rewrite/generated/`. The active LaTeX sources include these files directly, so the tables in the PDFs are tied to the machine-readable results rather than maintained as separate transcriptions.

The manifests record scope-specific inputs, outputs, code, and provenance. The mechanism and public-yield manifests also record environment and dependency versions plus Git information when available; the public-yield manifest hashes the paper-facing generated tables and figure. A dirty-worktree marker or an `unavailable` Git value is a provenance fact, not a clean-release assertion. The source-reported-neighborhood manifest instead records its transcribed-input boundary and the reason search-adjusted inference is unavailable.

## Data and redistribution

The [data-purpose ledger](research_pipeline/DATA_PURPOSE_LEDGER.md) gives every dataset a named hypothesis, required interaction, merge key, timing rule, target output, keep rule, and limitation. Downloads without an analytical purpose are rejected or deferred.

Public availability does not automatically grant redistribution rights. Raw files remain local and ignored by Git. No reuse license is granted for the software, paper text, source PDF, or recovered exhibits. A separate archived release should review provider terms and source-asset permissions.

## Continuous integration

The GitHub Actions workflow installs the pinned Python layer and runs the same 39 deterministic unit tests. Because raw provider files are intentionally untracked, clean-clone CI validates their manifest paths, sizes, and SHA-256 syntax but verifies raw bytes only when a saved snapshot is present; all tracked code, output, and paper-asset hashes are always checked. CI excludes live downloads and the LaTeX build because provider revisions and TeX installation are unsuitable for a lightweight per-commit check.
