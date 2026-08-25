# Public-data country-combination diagnostic

## Evidentiary boundary

This is not a reconstruction of the paper's synchronized yield-curve-inversion state. The public repository does not contain the nine-country yield-slope panel. The diagnostic instead uses the existing BIS policy-rate files to study synchronized *delivered easing*, then asks whether particular joint-cut combinations coincide with unusually weak policy-ranked currency spot returns.

## Design

For each of the 36 country pairs and 84 country triples, a joint-cut onset occurs when every member cuts its BIS policy rate by at least 10 basis points and the same joint cut did not occur in the previous three months. The outcome is the cumulative policy-ranked log spot-return proxy in months 0 and 1. It targets three currencies per side using lagged policy-rate differentials and includes all cutoff ties with equal weight, so realized legs can be larger. It is a public mechanism proxy rather than a feasible excess return. Reference values require at least six valid events.

Every eligible combination is shifted through every possible circular calendar rotation. The raw reference value is the doubled smaller inclusive tail rank. A common-rotation maximum absolute standardized reference is computed jointly across all eligible pairs and triples; size-specific values are also reported. Under simultaneous cyclic-shift exchangeability, this construction controls the declared family; otherwise it is a finite family diagnostic. The family was declared in code and exhaustively reported but was not preregistered. Event-resampling intervals and leave-one-event ranges expose small-sample sensitivity.

## Result

1 combination(s) meet the 5% common-rotation max-|z| reference criterion across all eligible pairs and triples.
A low raw reference value should therefore not be read as evidence that a specific country set uniquely drives the mechanism. The estimates are contemporaneous event-window associations and cannot distinguish policy response from the stress that prompted it.

Most negative eligible combination estimates:

| Combination | Size | Events | Mean pp | Raw ref. | Within-size max-|z| ref. | All-combination max-|z| ref. | Leave-one range |
|---|---:|---:|---:|---:|---:|---:|---:|
| CHF+GBP | 2 | 6 | -4.54 | 0.009 | 0.024 | 0.035 | [-6.21, -2.52] |
| AUD+EUR | 2 | 6 | -4.26 | 0.004 | 0.042 | 0.055 | [-5.63, -2.18] |
| CAD+NOK+NZD | 3 | 7 | -4.09 | 0.013 | 0.040 | 0.066 | [-4.66, -2.33] |
| GBP+NZD+SEK | 3 | 8 | -3.71 | 0.018 | 0.057 | 0.086 | [-4.76, -2.14] |
| NOK+NZD+SEK | 3 | 6 | -3.62 | 0.026 | 0.141 | 0.235 | [-4.43, -1.42] |
| CAD+GBP+NOK | 3 | 6 | -3.33 | 0.031 | 0.191 | 0.321 | [-4.62, -1.07] |
| GBP+SEK | 2 | 9 | -3.32 | 0.013 | 0.064 | 0.119 | [-4.19, -1.90] |
| AUD+NOK+NZD | 3 | 6 | -2.87 | 0.048 | 0.292 | 0.519 | [-3.99, -0.51] |

Eligible combinations: 42. Sparse combinations retained descriptively but not tested: 78.

The family result is sensitive to the minimum event-count rule:

| Minimum events | Eligible combinations | 5% max-|z| hits | Smallest max-|z| ref. | Leading combination |
|---:|---:|---:|---:|---|
| 6 | 42 | 1 | 0.035 | CHF+GBP |
| 8 | 25 | 0 | 0.064 | GBP+NZD+SEK |
| 10 | 15 | 0 | 0.229 | GBP+NZD |

## Composition of the 15 baseline synchronized-easing onsets

The next rows count combinations contained in the existing threshold-three onset dates. They are descriptive: the same crisis month contributes many overlapping pairs and triples, so treating these rows as separate tests would manufacture precision.

| Combination | Size | Onset occurrences | Mean pp when present | Present-minus-absent pp | Months |
|---|---:|---:|---:|---:|---|
| CAD+NZD | 2 | 7 | -3.64 | -4.83 | 1989-05;1990-08;1995-07;1998-09;2008-10;2015-07;2020-03 |
| NOK+NZD | 2 | 6 | -1.88 | -1.36 | 1988-05;1988-12;1989-05;1990-08;2008-10;2020-03 |
| AUD+NOK | 2 | 5 | -2.70 | -2.46 | 1988-12;1990-08;2008-10;2011-12;2020-03 |
| AUD+NZD | 2 | 5 | -2.75 | -2.53 | 1988-12;1990-08;2008-10;2016-08;2020-03 |
| AUD+CAD | 2 | 4 | -5.11 | -5.52 | 1990-08;1996-07;2008-10;2020-03 |
| AUD+GBP | 2 | 4 | -3.90 | -3.87 | 2001-02;2008-10;2016-08;2020-03 |
| CAD+NOK | 2 | 4 | -5.32 | -5.80 | 1989-05;1990-08;2008-10;2020-03 |
| GBP+NZD | 2 | 4 | -2.14 | -1.47 | 1988-05;2008-10;2016-08;2020-03 |
| AUD+SEK | 2 | 3 | -4.80 | -4.68 | 1996-07;2008-10;2011-12 |
| CAD+CHF | 2 | 3 | -3.17 | -2.63 | 1995-07;2008-10;2024-06 |

## What this check can and cannot reveal

A persistently negative combination would identify a useful target for a future author-data decomposition: one could ask whether the same countries also contribute disproportionately to the forward-looking inversion state. Failure to meet the family reference criterion instead favors the more cautious interpretation that the public easing proxy is broad and episode-driven rather than uniquely tied to a stable country bloc.

The exercise cannot determine whether any country pair or triple drives the original result. Policy cuts occur after decisions are delivered, while yield-curve inversions are forward-looking. The shadow carry outcome omits interest income, observes the event contemporaneously, and can be influenced by the same global shock that induced policy easing. Country combinations overlap heavily, the event counts remain small, and BIS policy-rate definitions differ across countries and over time.

## Reproduction

Run `python research_pipeline/src/country_combination_proxy.py` from the project root. All outputs are isolated under `research_pipeline/outputs/country_combinations/`.
