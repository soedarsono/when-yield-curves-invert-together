# Public-data mechanism pipeline

This directory acquires official public data and runs a mechanism exercise around synchronized delivered policy easing. It does not reproduce the paper's unavailable author yield panel, any licensed carry-return inputs, fresh-inversion IYC state, episodes, or headline estimates.

## Design boundary

The distinction is substantive, not merely a data substitution. The paper's IYC state uses fresh yield-curve inversions and a confirmed-release latch to classify the next month's return. This pipeline identifies an onset only after at least three BIS policy rates have fallen by at least 0.10 percentage point following three quiet months. Delivered easing is downstream of expected easing and stress, so results from this pipeline are event-response associations and cannot validate the paper's predictive signal.

The [data-purpose ledger](DATA_PURPOSE_LEDGER.md) records the hypothesis, merge rule, timing, intended output, limitation, and redistribution status for each source. Provenance for material copied into the rewritten paper is separate in the [copied-material ledger](../rewrite/notes/copied_material_ledger.md).

## Source groups

- `cftc_legacy_futures`: currency-futures positioning, 1986 onward.
- `nyfed_acm`: U.S. ACM expected-rate and term-premium estimates.
- `bis_policy_rates`: monthly G10 and U.S. policy rates.
- `bis_exchange_rates`: monthly end-of-period bilateral USD exchange rates.
- `oecd_cli`: OECD harmonised composite leading indicators.
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

With the current audited snapshot, the mechanism run finds 15 delivered-easing onsets over 1988–2025 and no Holm-significant result in the declared six-outcome primary family. The country screen enumerates 120 pairs/triples and finds one family-adjusted result under the six-event rule, but none under stricter event-count thresholds. These are public-proxy results, not estimates of the paper's IYC state. See the root [reproducibility guide](../REPRODUCIBILITY.md) for exact results and the snapshot-versus-fresh-download distinction.

## Data and legal limits

Do not edit raw files. Current-vintage FRED and OECD downloads can be revised, and a fresh provider download need not match the audited snapshot. The CFTC Deutsche-mark/euro transition is a documented proxy; NOK and SEK lack directly matched CFTC contracts. BIS quote conventions are normalized before return construction, and policy-rate ranks remain an imperfect substitute for money-market or forward rates.

Raw downloads are ignored by version control. Before a public release, review provider terms and distribute only material for which redistribution is permitted. Availability through an official endpoint is not itself a license to republish the downloaded file.
