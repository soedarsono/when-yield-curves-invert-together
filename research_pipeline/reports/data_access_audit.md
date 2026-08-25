# Public-data access audit

Generated: 2026-08-25T19:27:54+00:00

This report verifies acquisition and basic parseability. Analytical use still requires the purpose-ledger gates.

## Acquisition summary

- Files audited: 38
- Download size excluding extracted CFTC duplicates: 58.8 MB
- Unresolved failures among currently configured downloads: 0
- Configured downloads missing locally: 0
- Raw files with missing or mismatched manifest hashes: 0
- Extracted CFTC analytical inputs verified: 11 of 11

- `bis_exchange_rates`: 9 file(s)
- `bis_policy_rates`: 10 file(s)
- `cftc_legacy_futures`: 11 file(s)
- `fred_controls`: 5 file(s)
- `nyfed_acm`: 2 file(s)
- `oecd_cli`: 1 file(s)

## Date coverage

| Source | File | Rows | Start | End |
|---|---|---:|---|---|
| bis_exchange_rates | `M_AU_AUD_E.csv` | 835 | 1957-01-01 | 2026-07-01 |
| bis_exchange_rates | `M_CA_CAD_E.csv` | 979 | 1945-01-01 | 2026-07-01 |
| bis_exchange_rates | `M_CH_CHF_E.csv` | 875 | 1953-09-01 | 2026-07-01 |
| bis_exchange_rates | `M_GB_GBP_E.csv` | 876 | 1953-08-01 | 2026-07-01 |
| bis_exchange_rates | `M_JP_JPY_E.csv` | 835 | 1957-01-01 | 2026-07-01 |
| bis_exchange_rates | `M_NO_NOK_E.csv` | 872 | 1953-12-01 | 2026-07-01 |
| bis_exchange_rates | `M_NZ_NZD_E.csv` | 835 | 1957-01-01 | 2026-07-01 |
| bis_exchange_rates | `M_SE_SEK_E.csv` | 875 | 1953-09-01 | 2026-07-01 |
| bis_exchange_rates | `M_XM_EUR_E.csv` | 626 | 1974-06-01 | 2026-07-01 |
| bis_policy_rates | `M_AU.csv` | 604 | 1976-04-01 | 2026-07-01 |
| bis_policy_rates | `M_CA.csv` | 793 | 1960-07-01 | 2026-07-01 |
| bis_policy_rates | `M_CH.csv` | 967 | 1946-01-01 | 2026-07-01 |
| bis_policy_rates | `M_GB.csv` | 967 | 1946-01-01 | 2026-07-01 |
| bis_policy_rates | `M_JP.csv` | 851 | 1946-01-01 | 2026-07-01 |
| bis_policy_rates | `M_NO.csv` | 485 | 1986-03-01 | 2026-07-01 |
| bis_policy_rates | `M_NZ.csv` | 499 | 1985-01-01 | 2026-07-01 |
| bis_policy_rates | `M_SE.csv` | 967 | 1946-01-01 | 2026-07-01 |
| bis_policy_rates | `M_US.csv` | 865 | 1954-07-01 | 2026-07-01 |
| bis_policy_rates | `M_XM.csv` | 331 | 1999-01-01 | 2026-07-01 |
| cftc_legacy_futures | `deacot1986_2016.zip` |  |  |  |
| cftc_legacy_futures | `deacot2017.zip` |  |  |  |
| cftc_legacy_futures | `deacot2018.zip` |  |  |  |
| cftc_legacy_futures | `deacot2019.zip` |  |  |  |
| cftc_legacy_futures | `deacot2020.zip` |  |  |  |
| cftc_legacy_futures | `deacot2021.zip` |  |  |  |
| cftc_legacy_futures | `deacot2022.zip` |  |  |  |
| cftc_legacy_futures | `deacot2023.zip` |  |  |  |
| cftc_legacy_futures | `deacot2024.zip` |  |  |  |
| cftc_legacy_futures | `deacot2025.zip` |  |  |  |
| cftc_legacy_futures | `deacot2026.zip` |  |  |  |
| fred_controls | `BAMLH0A0HYM2.csv` | 793 | 2023-08-25 | 2026-08-21 |
| fred_controls | `DCOILWTICO.csv` | 10599 | 1986-01-02 | 2026-08-18 |
| fred_controls | `DTWEXBGS.csv` | 5385 | 2006-01-02 | 2026-08-21 |
| fred_controls | `NFCI.csv` | 2902 | 1971-01-08 | 2026-08-14 |
| fred_controls | `VIXCLS.csv` | 9560 | 1990-01-02 | 2026-08-24 |
| nyfed_acm | `acmPlot_data.csv` | 782 | 1961-06-30 | 2026-07-31 |
| nyfed_acm | `ACMTermPremium.xls` |  |  |  |
| oecd_cli | `oecd_cli_1988_present.csv` | 9877 | 1988-01-01 | 2026-06-01 |

## Failed requests

- None.

## Integrity issues

- None.

## Completed checks and remaining limitations

- Completed: all configured raw downloads and extracted CFTC analytical inputs have locally verified SHA-256 hashes and acquisition statuses.
- Completed: BIS exchange-rate quote direction is normalized to the USD return on foreign currency; EUR is used as a documented proxy, not an asserted Deutsche-mark splice.
- Completed: the ACM CSV fields used by the mechanism checks, the CFTC contract crosswalk, and the assumed CFTC release lag are documented in the analytical pipeline.
- Remaining limitation: the OECD CLI and FRED histories are current-vintage, and the CLI can overlap with financial inputs.
- Remaining limitation: the author signal dates and licensed analytical panel are unavailable, so the public exercise remains a proxy analysis rather than a replication.
