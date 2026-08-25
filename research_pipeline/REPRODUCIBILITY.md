# Research-pipeline reproducibility status

The public acquisition, mechanism-check, source-reported-neighborhood, and v0.3 current-vintage yield-proxy layers are executable. They do not reproduce the unavailable original 10-year-minus-2-year state or its carry-return estimates.

## Current commands

```powershell
python research_pipeline/src/download_public_data.py
python research_pipeline/src/audit_public_data.py
python research_pipeline/src/run_mechanism_checks.py
python research_pipeline/src/country_combination_proxy.py
python research_pipeline/src/source_reported_neighborhood.py
python research_pipeline/src/public_yield_proxy_v03.py
python research_pipeline/src/render_v03_public_tables.py
python -m unittest discover -s research_pipeline/tests -v
```

The top-level `run_reproduction.ps1` composes these steps and optionally builds and verifies both PDFs.

## Deterministic checks

The current suite passes 39 tests covering downloader and manifest integrity, event-window timing, live-state entry and release, exact enumeration of circular assignments, same-valid-event-count conditioning, doubled-tail rank inference, Holm adjustment, HAC regression calculations, hashed run-manifest records, joint-cut quiet windows, country-screen rotation enumeration, equal cutoff-tie weights, selected-return completeness, generated-table mirroring, the declared 64-rule current-vintage family, common-calendar rotation alignment, gap-aware episode counting, source-reported-neighborhood outputs, and paper-output linkage. Clean-clone CI validates untracked raw-input manifest metadata and verifies raw bytes when a saved snapshot is present; tracked code, output, and paper records are always byte-checked.

## Output contract

The mechanism run writes derived panels, all-rotation audit data, event dates, empirical and simulation ledgers, metadata, tables, figures, and a run manifest below `research_pipeline/outputs/mechanism/`. The country screen writes tested combinations, common-rotation maxT references, event-count sensitivities, leave-one-event diagnostics, a report, and a separate manifest below `research_pipeline/outputs/country_combinations/`. The source-reported-neighborhood stage writes a descriptive, source-transcribed rule comparison below `research_pipeline/outputs/v03/source_reported_neighborhood/`; it does not regenerate the original estimates. The public yield-proxy stage writes its state, policy-ranked log spot-return proxy, declared 64-rule family, influence diagnostics, figure, report, and hashed manifest below `research_pipeline/outputs/v03/yield_proxy/`. The renderer converts those machine-readable outputs into the v0.3 LaTeX tables and figure under `rewrite/generated/`.

## Boundary

Exact reproduction of the original paper still requires the author yield panel, portfolio inputs, signal dates, transformations, code, seeds, and inference implementation. Until those arrive, the original-paper estimates remain source-reported rather than independently regenerated. The synchronized-easing exercise remains a downstream mechanism proxy. The source-reported boundary grid is a traceable transcription, and the current-vintage public 10-year-minus-3-month exercise is a nearby measurement and specification-search audit; neither is a replication of the original 10-year-minus-2-year design.

See the project-root `REPRODUCIBILITY.md` for environment, release, and legal-data requirements.
