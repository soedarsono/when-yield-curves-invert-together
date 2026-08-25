# Research-pipeline reproducibility status

The public acquisition and mechanism-check layers are executable. They do not reproduce the unavailable IYC signal or inherited carry-return estimates.

## Current commands

```powershell
python research_pipeline/src/download_public_data.py
python research_pipeline/src/audit_public_data.py
python research_pipeline/src/run_mechanism_checks.py
python research_pipeline/src/country_combination_proxy.py
python -m unittest discover -s research_pipeline/tests -v
```

The top-level `run_reproduction.ps1` composes these steps and optionally builds and verifies both PDFs.

## Deterministic checks

The current suite passes 21 tests covering downloader and manifest integrity, event-window timing, live-state entry and release, exact enumeration of circular assignments, same-valid-event-count conditioning, doubled-tail rank inference, Holm adjustment, HAC regression calculations, hashed run-manifest records, joint-cut quiet windows, and country-screen rotation enumeration.

## Output contract

The mechanism run writes derived panels, all-rotation audit data, event dates, empirical and simulation ledgers, metadata, tables, figures, and a run manifest below `research_pipeline/outputs/mechanism/`. The country screen writes tested combinations, common-rotation maxT references, event-count sensitivities, leave-one-event diagnostics, a report, and a separate manifest below `research_pipeline/outputs/country_combinations/`. Publication-ready assets are mirrored to `rewrite/generated/`.

## Boundary

Exact reproduction of the original paper still requires the author yield panel, portfolio inputs, signal dates, transformations, code, seeds, and inference implementation. Until those arrive, every source-PDF result remains labeled `inherited - not independently regenerated`, and the public synchronized-easing exercise remains a downstream mechanism proxy.

See the project-root `REPRODUCIBILITY.md` for environment, release, and legal-data requirements.
