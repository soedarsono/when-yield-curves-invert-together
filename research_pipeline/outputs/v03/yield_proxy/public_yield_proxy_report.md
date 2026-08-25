# V0.3 independent public yield-curve proxy audit

## Evidentiary boundary

This exercise is **not a replication of the paper's synchronized-inversion state**. It uses current-vintage OECD monthly 10-year government yields minus 3-month interbank rates delivered through FRED rather than the baseline end-of-month 10Y-minus-2Y panel. The public outcome is a BIS policy-ranked log spot-return proxy, not an executable forward excess return.

## Main result

The baseline-like public rule (fresh entry, two-curve breadth, two consecutive steepening months for release, a target of three currencies per side with all cutoff ties equally weighted, and a next-month outcome) has an annualized active-minus-inactive log spot-return-proxy difference of **-3.20 percentage points** across 99 active months and 18 episodes. Its inclusive circular-shift reference value is 0.335; its common-calendar maximum-standardized-coefficient reference value across the declared 64-rule family is 1.000.

Across all 64 rules, 64% have a negative coefficient and 0 meet the 5% common-calendar maximum-standardized-coefficient reference criterion. The baseline-like estimate ranks 22 of 64 from most negative to most positive. Under simultaneous cyclic-shift exchangeability, the maximum reference controls the declared family; otherwise it is a finite rotation-reference diagnostic.

## Same-universe concern

When each currency is jointly deleted from signal construction and the public carry outcome, 9 of 9 influence estimates are negative. Each state requires five of the remaining eight curves. These are sensitivity checks, not nine independent tests: the samples and event calendars overlap heavily.

| Excluded | Annualized pp | Raw rotation ref. | Active months | Episodes |
|---|---:|---:|---:|---:|
| AUD | -5.08 | 0.133 | 69 | 16 |
| CAD | -1.96 | 0.554 | 92 | 17 |
| CHF | -4.51 | 0.204 | 92 | 17 |
| EUR | -2.90 | 0.391 | 88 | 18 |
| GBP | -0.60 | 0.827 | 88 | 16 |
| JPY | -2.33 | 0.404 | 98 | 18 |
| NOK | -1.32 | 0.655 | 70 | 14 |
| NZD | -1.93 | 0.538 | 82 | 14 |
| SEK | -1.95 | 0.591 | 91 | 16 |

The geographically disjoint checks are stronger conceptually because no currency supplying the curve signal appears in the outcome basket. The European sensor requires four of five curves; the non-European sensor requires three of four:

| Split | Annualized pp | Raw rotation ref. | Active months | Episodes |
|---|---:|---:|---:|---:|
| European curves -> non-European currencies | -15.84 | 0.062 | 38 | 10 |
| Non-European curves -> European currencies | -0.34 | 0.887 | 44 | 9 |

The disjoint evidence is asymmetric: European curves precede losses in the non-European basket, but the reverse direction is approximately zero. This is not a general two-way validation of common information. The deletion and disjoint references rotate each complete-case sequence after missing observations are dropped, so internal calendar gaps are compressed.

## Concentration and calendar sensitivity

| Check | Annualized pp | Raw rotation ref. | Active months | Episodes |
|---|---:|---:|---:|---:|
| full_sample | -3.20 | 0.335 | 99 | 18 |
| exclude_episodes_containing_1998_09_2008_10_2020_03 | -0.46 | 0.826 | 88 | 15 |
| first_calendar_half_1988_2004 | -5.73 | 0.382 | 49 | 9 |
| second_calendar_half_2005_2025 | -1.02 | 0.776 | 50 | 10 |
| delete_five_worst_active_months_outcome_conditioned_diagnostic | 0.94 | -- | 94 | 20 |

The five-worst-month deletion is deliberately labeled outcome-conditioned and receives no p-value. It is a concentration diagnostic, not a preferred estimator.

## Interpretation rule for v0.3

- A broadly negative family with a non-extreme baseline is descriptive sign resemblance, not independent confirmation, when no rule exceeds the common-calendar family reference threshold.
- If only a few rules are negative or the baseline-like rule is an extremum, the public proxy should be reported as sensitive to state definition.
- Disjoint results can support a common-information interpretation only as associations. Monthly current-vintage data, small episode counts, and the spot-only outcome prevent a claim of implementable predictability or structural identification.

## What remains impossible in this repository

The absent author 10Y-minus-2Y panel still prevents an audit of the original fifteen episodes, the exact 92 active months, the headline carry and beta portfolios, author-data leave-one-country-out states, and search-adjusted inference for the actual state family. No result here should be substituted for those missing tests.

The baseline public proxy contains 18 contiguous episodes; the complete episode ledger is supplied as a machine-readable output.
