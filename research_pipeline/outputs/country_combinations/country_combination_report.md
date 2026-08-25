# Public-data country-combination diagnostic

## Evidentiary boundary

This is not a reconstruction of the paper's synchronized yield-curve-inversion state. The public repository does not contain the nine-country yield-slope panel. The diagnostic instead uses the existing BIS policy-rate files to study synchronized *delivered easing*, then asks whether particular joint-cut combinations coincide with unusually weak policy-ranked currency spot returns.

## Design

For each of the 36 country pairs and 84 country triples, a joint-cut onset occurs when every member cuts its BIS policy rate by at least 10 basis points and the same joint cut did not occur in the previous three months. The outcome is the cumulative shadow carry spot return in months 0 and 1. It ranks all nine currencies using lagged policy-rate differentials, so it is a public mechanism proxy rather than a feasible excess return. Inference requires at least six valid events.

Every eligible combination is shifted through every possible circular calendar rotation. The raw p-value is the doubled smaller inclusive tail rank. A common-rotation maximum absolute standardized statistic adjusts jointly across all eligible pairs and triples; size-specific adjusted p-values are also reported. Event-resampling intervals and leave-one-event ranges expose small-sample sensitivity.

## Result

1 combination(s) pass a 5% family-wise threshold across all eligible pairs and triples.
A low unadjusted p-value should therefore not be read as evidence that a specific country set uniquely drives the mechanism. The estimates are contemporaneous event-window associations and cannot distinguish policy response from the stress that prompted it.

Most negative eligible combination estimates:

| Combination | Size | Events | Mean pp | Raw p | Within-size maxT p | All-combination maxT p | Leave-one range |
|---|---:|---:|---:|---:|---:|---:|---:|
| CHF+GBP | 2 | 6 | -4.63 | 0.009 | 0.026 | 0.042 | [-6.16, -2.62] |
| CAD+NOK+NZD | 3 | 7 | -4.29 | 0.013 | 0.037 | 0.055 | [-4.89, -2.57] |
| AUD+EUR | 2 | 6 | -4.06 | 0.009 | 0.057 | 0.088 | [-5.57, -1.94] |
| NOK+NZD+SEK | 3 | 6 | -3.62 | 0.026 | 0.160 | 0.279 | [-4.43, -1.42] |
| CAD+GBP+NOK | 3 | 6 | -3.58 | 0.022 | 0.156 | 0.277 | [-4.92, -1.37] |
| GBP+NZD+SEK | 3 | 8 | -3.52 | 0.018 | 0.081 | 0.143 | [-4.54, -1.93] |
| GBP+SEK | 2 | 9 | -3.28 | 0.018 | 0.086 | 0.152 | [-4.15, -1.86] |
| AUD+NOK+NZD | 3 | 6 | -3.11 | 0.044 | 0.255 | 0.440 | [-4.29, -0.81] |

Eligible combinations: 42. Sparse combinations retained descriptively but not tested: 78.

The family result is sensitive to the minimum event-count rule:

| Minimum events | Eligible combinations | Adjusted 5% hits | Smallest adjusted p | Leading combination |
|---:|---:|---:|---:|---|
| 6 | 42 | 1 | 0.042 | CHF+GBP |
| 8 | 25 | 0 | 0.105 | GBP+NZD+SEK |
| 10 | 15 | 0 | 0.224 | GBP+NZD |

## Composition of the 15 baseline synchronized-easing onsets

The next rows count combinations contained in the existing threshold-three onset dates. They are descriptive: the same crisis month contributes many overlapping pairs and triples, so treating these rows as separate tests would manufacture precision.

| Combination | Size | Onset occurrences | Mean pp when present | Present-minus-absent pp | Months |
|---|---:|---:|---:|---:|---|
| CAD+NZD | 2 | 7 | -3.82 | -5.10 | 1989-05;1990-08;1995-07;1998-09;2008-10;2015-07;2020-03 |
| NOK+NZD | 2 | 6 | -2.10 | -1.66 | 1988-05;1988-12;1989-05;1990-08;2008-10;2020-03 |
| AUD+NOK | 2 | 5 | -2.91 | -2.71 | 1988-12;1990-08;2008-10;2011-12;2020-03 |
| AUD+NZD | 2 | 5 | -3.27 | -3.25 | 1988-12;1990-08;2008-10;2016-08;2020-03 |
| AUD+CAD | 2 | 4 | -5.33 | -5.77 | 1990-08;1996-07;2008-10;2020-03 |
| AUD+GBP | 2 | 4 | -4.28 | -4.33 | 2001-02;2008-10;2016-08;2020-03 |
| CAD+NOK | 2 | 4 | -5.65 | -6.20 | 1989-05;1990-08;2008-10;2020-03 |
| GBP+NZD | 2 | 4 | -2.79 | -2.30 | 1988-05;2008-10;2016-08;2020-03 |
| AUD+SEK | 2 | 3 | -4.52 | -4.28 | 1996-07;2008-10;2011-12 |
| CAD+CHF | 2 | 3 | -3.17 | -2.58 | 1995-07;2008-10;2024-06 |

## What this check can and cannot reveal

A robustly negative combination would identify a useful target for a future author-data decomposition: one could ask whether the same countries also contribute disproportionately to the forward-looking inversion state. A null adjusted result instead favors the more cautious interpretation that the public easing proxy is broad and episode-driven rather than uniquely tied to a stable country bloc.

The exercise cannot determine whether any country pair or triple drives the original result. Policy cuts occur after decisions are delivered, while yield-curve inversions are forward-looking. The shadow carry outcome omits interest income, observes the event contemporaneously, and can be influenced by the same global shock that induced policy easing. Country combinations overlap heavily, the event counts remain small, and BIS policy-rate definitions differ across countries and over time.

## Reproduction

Run `python research_pipeline/src/country_combination_proxy.py` from the project root. All outputs are isolated under `research_pipeline/outputs/country_combinations/`.
