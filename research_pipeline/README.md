# Public-data audit pipeline

This directory acquires official public data and runs delivered-easing, country-combination, and current-vintage yield-curve sensitivity exercises. It does not reproduce the paper's unavailable author yield panel, licensed carry-return inputs, fresh-inversion IYC state, baseline episodes, or headline estimates.

## Design boundary

The distinction is substantive, not merely a data substitution. The paper's IYC state uses fresh 10-year-minus-2-year yield-curve inversions and a confirmed-release latch to classify the next month's return. The delivered-easing exercise identifies an onset only after at least three BIS policy rates have fallen by at least 0.10 percentage point following three quiet months. Delivered easing is downstream of expected easing and stress, so those results are event-response associations.

The separate public yield-curve exercise uses current-vintage OECD monthly 10-year government yields minus 3-month interbank rates distributed through FRED. It evaluates a declared 64-rule family against a BIS policy-ranked log spot-return proxy; target legs include all cutoff ties with equal weight. The maturity, vintage, coverage, and outcome differ from the paper's baseline, so the exercise is an adverse sensitivity or challenge test, not a validation or replication.

The [data-purpose ledger](DATA_PURPOSE_LEDGER.md) records the hypothesis, merge rule, timing, intended output, limitation, and redistribution status for each source. Provenance for material copied into the rewritten paper is separate in the [copied-material ledger](../rewrite/notes/copied_material_ledger.md).

## Source groups

- `cftc_legacy_futures`: currency-futures positioning, 1986 onward.
- `nyfed_acm`: U.S. ACM expected-rate and term-premium estimates.
- `bis_policy_rates`: monthly G10 and U.S. policy rates.
- `bis_exchange_rates`: monthly end-of-period bilateral USD exchange rates.
- `oecd_cli`: OECD harmonised composite leading indicators.
- `oecd_yield_curve_proxy`: current-vintage OECD/FRED monthly 10-year government yields and 3-month interbank rates.
- `oecd_industrial_activity`: deferred pending a fixed sector and transformation definition.
- `fred_controls`: NFCI, VIX, broad dollar, high-yield spread, and oil-price controls; only declared retained series enter reported results.

## Run

The project requires Python 3.12 or newer. From the repository root, the supported one-command path is:

```powershell
python -m pip install -e .
.\run_reproduction.ps1
```

For an existing hash-verified raw-data snapshot without a PDF build:

```powershell
.\run_reproduction.ps1 -UseExistingData -SkipPdf
```

The pipeline stages can also be run separately:

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

To fetch one declared group:

```powershell
python research_pipeline/src/download_public_data.py --source cftc_legacy_futures
```

## Output contract

- Local immutable downloads: `research_pipeline/data/raw/<source_group>/`.
- Retrieval records and SHA-256 hashes: `research_pipeline/data/download_manifest.jsonl`.
- Coverage and parseability inventory: `research_pipeline/data/public_data_inventory.csv`.
- Derived panels, finite-rotation audit, and sensitivities: `research_pipeline/outputs/mechanism/data/`.
- Event, empirical-result, simulation, and run-metadata ledgers: `research_pipeline/outputs/mechanism/ledgers/`.
- Tables and figures: `research_pipeline/outputs/mechanism/tables/` and `research_pipeline/outputs/mechanism/figures/`.
- Complete generated-artifact inventory: `research_pipeline/outputs/mechanism/run_manifest.json`.
- Pair/triple sensor screen, maxT references, sensitivities, report, and manifest: `research_pipeline/outputs/country_combinations/`.
- Descriptive source-reported rule neighborhood and manifest: `research_pipeline/outputs/v03/source_reported_neighborhood/`.
- Public 10-year-minus-3-month rule family, exclusions, sensitivities, episode ledger, report, figure, and manifest: `research_pipeline/outputs/v03/yield_proxy/`.
- Paper-facing v0.3 tables and mirrored figures: `rewrite/generated/tables/v03_*.tex` and `rewrite/generated/v03_public_specification_curve.png`.

With the current audited snapshot, the mechanism run finds 15 delivered-easing onsets over 1988–2025 and no outcome meeting the 5-percent Holm-adjusted rotation-reference criterion in the declared six-outcome primary family. The country screen enumerates 120 pairs/triples and finds one result meeting the common-rotation maximum-$|z|$ criterion under the six-event rule, but none under stricter event-count thresholds. Family-wise interpretation is conditional on simultaneous cyclic-shift exchangeability.

The baseline-like public 10-year-minus-3-month rule produces a -3.20-percentage-point annualized active-minus-inactive log spot-return-proxy difference, with raw circular-shift reference value 0.335 and 64-rule common-calendar maximum-$|z|$ reference value 1.000. Forty-one of 64 estimates are negative, no rule meets the 5-percent family reference criterion, and the public proxy contains 18 episodes. Family-wise interpretation is conditional on simultaneous cyclic-shift exchangeability. This is an adverse sensitivity result, not validation of the baseline state. See the root [reproducibility guide](../REPRODUCIBILITY.md) for full results, manifest locations, and the snapshot-versus-fresh-download distinction.

`render_v03_public_tables.py` reads the machine-readable public-proxy CSV files, writes the LaTeX tables included by the paper, mirrors the specification-curve figure, and records hashes for those paper-facing outputs in the yield-proxy run manifest.

## Data and legal limits

Do not edit raw files. Current-vintage FRED and OECD downloads can be revised, and a fresh provider download need not match the audited snapshot. The CFTC Deutsche-mark/euro transition is a documented proxy; NOK and SEK lack directly matched CFTC contracts. BIS quote conventions are normalized before return construction, and policy-rate ranks remain an imperfect substitute for money-market or forward rates.

Raw downloads are ignored by version control. Before a public release, review provider terms and distribute only material for which redistribution is permitted. Availability through an official endpoint is not itself a license to republish the downloaded file.
