# When Yield Curves Invert Together

This repository contains an alternative job-market-paper edition of **“When Yield Curves Invert Together: Predicting Currency Carry Losses,”** its online appendix, the LaTeX source, external transformation/provenance ledgers, and reproducible public-data checks.

## Paper

- [Alt JMP v0.2 — main paper with online appendix](Alt_JMP_v0.2.pdf) — 44 pages
- [Main paper](output/pdf/When_Yield_Curves_Invert_Together_Main.pdf) — 26 pages, including 84 references
- [Online appendix](output/pdf/When_Yield_Curves_Invert_Together_Online_Appendix.pdf) — 18 pages, Appendices A--E

The paper reports a synchronized-inversion state formed from fresh 10-year/2-year inversions across the nine non-dollar G10 economies. In the source estimates, annualized carry-trade spot returns are 12.9 percentage points lower when the lagged state is active, with inference based on fifteen episodes. The cross-section is ordered by interest rates and predetermined equity-market betas.

The revision concentrates the economic argument around four distinctions:

1. synchronized breadth locates the predictive state;
2. rate and equity-beta exposure locate the loss-bearing currencies;
3. the inversion state precedes returns, whereas public policy easing records later delivery;
4. predetermined carry income determines whether similar spot losses produce negative total returns.

## Reproducibility boundary

The original yield-curve panel, currency panel, state dates, and estimation code are not present. The repository therefore does **not** independently regenerate the paper's core 1988--2026 estimates. Visible source estimates and copied exhibits are mapped in external ledgers.

The public-data layer is independently executable. It downloads or audits declared BIS, CFTC, New York Fed ACM, OECD, and FRED inputs; constructs a synchronized delivered-easing proxy; and regenerates event-study, inference, sensitivity, and country-combination outputs. This proxy is downstream of the yield-curve state and does not validate the paper's predictive classifier.

Current public-data results include:

- 15 synchronized delivered-easing onsets from 1988 through 2025;
- no outcome in the six-test primary mechanism family survives Holm adjustment;
- an exploratory screen of all 36 country pairs and 84 triples;
- one CHF--GBP result at the 5-percent family-wide level under a six-event minimum, which weakens after omitting October 2008 and disappears under stricter event-count rules.

The last result motivates a sensor-versus-risk-bearer hypothesis: countries whose policy rates help date a global episode need not be the currencies that absorb the losses.

## Audit trail

- [Original-to-revision transformation ledger](rewrite/notes/original_to_rewrite_transformation_ledger.md) — section-by-section moves, condensations, additions, and deletions
- [Copied-material ledger](rewrite/notes/copied_material_ledger.md) — source page, exhibit, asset hash, caption treatment, and final destination
- [Equation ledger](rewrite/notes/equation_provenance_ledger.md) — mapping from the original mathematical sequence to eight main-paper equations
- [Final page audit](rewrite/notes/page_by_page_audit.md) — visual and writing-style result for every page
- [Data-purpose ledger](research_pipeline/DATA_PURPOSE_LEDGER.md) — why every public dataset was acquired, what it interacts with, and its limitations
- [Reproducibility guide](REPRODUCIBILITY.md) — environment, commands, expected outputs, and exact boundary of reproducible claims

Original Appendices F and G remain external to both reader-facing PDFs. Their source assets and dispositions are recorded in the copied-material ledger. The synthetic path-dependence exercise is also repository-only and is not empirical evidence in either PDF.

## Rebuild

Requirements:

- Windows PowerShell
- Python 3.12 or newer
- MiKTeX with `pdflatex` and BibTeX
- Poppler with `pdftoppm`

Install the pinned Python layer and run the complete workflow:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
.\run_reproduction.ps1
```

For an already downloaded and hash-audited raw-data snapshot:

```powershell
.\run_reproduction.ps1 -UseExistingData
```

The workflow audits public inputs, rebuilds the mechanism and country-combination outputs, runs 21 deterministic tests, compiles the main and appendix PDFs, creates the combined edition, renders all pages, and runs automated PDF preflight.

## Repository map

- `rewrite/` — submission LaTeX, generated publication assets, and external provenance ledgers
- `research_pipeline/src/` — data acquisition, public mechanism checks, inference, and country-combination analysis
- `research_pipeline/config/` — declared sources, estimands, crosswalks, and data-purpose ledger
- `research_pipeline/outputs/` — machine-readable result tables, figures, and run manifests
- `research_pipeline/tests/` — deterministic timing, inference, manifest, and combination-screen tests
- `output/pdf/` — current standalone and combined PDFs

## Citation and reuse

Citation metadata are provided in [CITATION.cff](CITATION.cff). No software, text, data, or figure reuse license is granted by this repository. Provider terms and permissions for source-paper assets must be reviewed before redistribution in another archive or derivative work.
