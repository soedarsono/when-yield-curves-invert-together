# Data-purpose ledger

## Rule

No dataset enters this project merely because it is available. Every download must have:

1. a named hypothesis or credibility gate;
2. a specific interaction with the author panel, signal, or another public source;
3. a merge key and information-timing rule;
4. a target table, figure, or diagnostic;
5. a keep/drop criterion;
6. a documented limitation and redistribution status.

The machine-readable ledger is [`config/data_purpose_ledger.csv`](config/data_purpose_ledger.csv). The download-level provenance and hashes are stored in `data/download_manifest.jsonl` after the acquisition program runs.

## Official access routes verified

The acquisition routes were checked against the providers' own documentation on 2026-08-25. These links document access and interpretation; they are repository metadata, not additions to the paper's bibliography.

| Provider | Official route | Use in this project |
|---|---|---|
| BIS | [BIS Stats SDMX API](https://stats.bis.org/api-doc/v1/), [policy-rate documentation](https://www.bis.org/statistics/dataportal/cbpol.htm), and [bilateral-exchange-rate documentation](https://www.bis.org/statistics/dataportal/exr.htm) | Policy-rate event construction, lagged rate ranks, and bilateral spot returns |
| CFTC | [Historical compressed COT files](https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm) | Currency-futures positioning and open-interest shares |
| Federal Reserve Bank of New York | [ACM Treasury term-premia downloads](https://www.newyorkfed.org/research/data_indicators/term-premia-tabs) | Expected-rate/term-premium decomposition around public events |
| OECD | [Composite leading indicators](https://www.oecd.org/en/data/datasets/oecd-composite-leading-indicators-clis.html) and its SDMX Data Explorer | Current-vintage leading-activity diagnostic |
| Federal Reserve Bank of St. Louis | [FRED series-observations API](https://fred.stlouisfed.org/docs/api/fred/series_observations.html) | NFCI, VIX, and declared secondary controls |

The official pages confirm that BIS and OECD expose SDMX-compatible programmatic access, CFTC publishes annual machine-readable historical files, the New York Fed supplies monthly ACM expected-rate and term-premium estimates, and FRED exposes observations and real-time parameters through its API. The pipeline uses direct structured downloads; general web scraping is neither necessary nor authorized for these sources.

## Current acquisition decisions

| Dataset | Why it was acquired | What it must interact with | Intended evidentiary use | Current status |
|---|---|---|---|---|
| CFTC legacy currency futures | Test whether carry-aligned speculative positions unwind | Public synchronized-easing proxy, documented contract crosswalk, lagged policy-rate carry membership | Directional public-proxy mechanism evidence | `retained_online`; seven contracts match, but episode randomization is imprecise and release lag is assumed |
| New York Fed ACM | Compare expected-rate and term-premium movements | Public synchronized-easing proxy | Alternative-state diagnostic | `retained_online`; 10-year expected-rate component moves directionally, but family-adjusted inference is not decisive |
| BIS policy rates | Define delivered synchronized easing, lagged public carry ranks, and pair/triple sensor events | BIS FX, CFTC, ACM, OECD CLI, FRED, country-combination screen | Event proxy, sample construction, and exploratory sensor-country test | `retained_online`; explicitly downstream of and not a replacement for the IYC signal; combination inference uses maxT and event-count sensitivity |
| BIS bilateral FX rates | Measure the spot return on a public policy-ranked high-minus-low basket and score pair/triple events | Lagged BIS policy-rate rank and combination onsets | Shadow spot association and sensor-versus-risk-bearer check, not tradable carry or replication | `retained_online`; quote direction normalized, spot-only limitation recorded, and crisis sensitivity disclosed |
| OECD CLI | Measure current-vintage G7 leading activity around public easing onsets | Public synchronized-easing proxy | Secondary mechanism evidence | `retained_online`; revised and potentially financially contaminated |
| FRED controls | Measure financial-condition and volatility responses | Public synchronized-easing proxy | Alternative-state diagnostics | NFCI and VIX `retained_online`; broad-dollar, high-yield, and oil series rejected and removed from the declared source configuration and analytical panel |
| OECD industrial activity | Could provide a realized-activity outcome | Signal dates and country aggregation | Stronger macro mechanism test than CLI alone | **Deferred:** exact sector and transformation must be fixed first |

## Interaction graph

```text
Author signal dates and baseline analytical panel
    |
    +-- BIS FX ----------------> public spot-return reconciliation
    |       +-- policy rates --> public shadow carry sort
    |       +-- country subsets -> pair/triple sensor screen with maxT correction
    |
    +-- CFTC positioning ------> crowding and unwind mechanism
    |       +-- BIS FX --------> whether position changes mediate depreciation
    |
    +-- NY Fed ACM ------------> common term-premium robustness
    |       +-- foreign slopes -> rebuild or partial-out signal
    |
    +-- OECD CLI/policy rates -> growth and easing response
    |
    +-- FRED controls ---------> symmetric forecast and spanning benchmarks
```

The author signal dates and processed analytical panel are not currently present in this workspace. The completed exercises under `outputs/mechanism/` and `outputs/country_combinations/` therefore use a separately constructed synchronized-policy-easing proxy. Their outputs are downstream public-proxy associations, not headline regressions, signal validation, or replication.

## Completed public-proxy wave

The frozen mechanism run is documented in `reports/mechanism_checks.md` and `outputs/mechanism/run_manifest.json`. It produces a 1988--2025 currency panel, a 15-onset delivered-easing episode ledger, CFTC/ACM/OECD/FRED response checks, threshold and leave-one-currency sensitivities, circular-shift inference, episode-bootstrap intervals, and Holm adjustment for six primary outcomes. The separate country screen enumerates all 36 pairs and 84 triples, applies common-rotation maxT correction, and reports event-count, leave-one-event, and crisis sensitivity in `outputs/country_combinations/`. The fixed-seed simulation remains a repository diagnostic and does not enter either paper PDF.

## No-orphan review

At the end of each research wave, every row in the machine-readable ledger must be marked one of:

- `retained_main`: supports a main-text result;
- `retained_online`: supports a documented appendix result;
- `reconciliation_only`: validates public versus licensed inputs;
- `deferred`: purpose is valid but prerequisites are missing;
- `rejected`: failed its prespecified keep rule;
- `remove`: no longer has an evidentiary role and should not ship in the public release.

Raw public files may remain in a local cache for audit, but only legally redistributable and purpose-linked inputs belong in the eventual GitHub or archival release.
