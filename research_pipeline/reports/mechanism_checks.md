# Independent public-data mechanism checks

## Evidentiary boundary

This exercise does **not** reproduce the paper's IYC signal, episode ledger, carry returns, or licensed panel. It asks whether public proxies display associations consistent with parts of the proposed mechanism. The event is synchronized **delivered easing**, constructed from BIS policy rates. It is downstream of the paper's expected-easing signal and cannot validate the paper's timing claim.

## Frozen construction

- Sample: 1988-01 through 2025-12.
- Onset: at least 3 of nine policy rates fall by at least 0.10 percentage point after 3 months without another synchronized cut.
- Currency return: negative log change in BIS local-currency-per-USD exchange rate; positive means foreign-currency appreciation against USD.
- Public carry proxy: equal-weight long the three highest and short the three lowest policy differentials, ranked with a one-month lag; spot leg only.
- Events found: 15. Exact dates and country counts are in `outputs/mechanism/ledgers/synchronized_easing_onsets.csv`.
- Inference: every circular rotation preserves the complete event sequence. The reference set retains only rotations with the observed number of valid episode outcomes, includes the observed assignment, and doubles the smaller inclusive tail rank. This is a conditional finite-rotation reference rather than a causal exact test because irregular missingness can make the same-N subset fail to form a transformation group. Every retained and rejected rotation is recorded in `outputs/mechanism/data/rotation_audit.csv`. Ninety-percent intervals resample episodes; leave-one-episode ranges report influence. A monthly HAC regression is secondary.
- Multiplicity: the six outcomes in `mechanism_spec.json` form one primary family and receive Holm adjustment. Other horizons and VIX are descriptive.

## Primary estimates

| Outcome | Estimate | Unit | Events | Rotations | RI p | Holm p | Leave-one-event range |
|---|---:|---|---:|---:|---:|---:|---:|
| Policy-ranked shadow carry spot return, months 0--1 | -1.10 | percentage points cumulative | 15 | 441 | 0.195 | 0.975 | [-1.77, -0.13] |
| Carry-aligned CFTC non-commercial net share, change through month 3 | -4.39 | percentage points of open interest | 12 | 81 | 0.741 | 1.000 | [-7.88, -1.67] |
| ACM 10-year expected-rate component, change through month 3 | -0.13 | percentage points | 15 | 396 | 0.202 | 0.975 | [-0.20, -0.08] |
| ACM 10-year term premium, change through month 3 | -0.03 | percentage points | 15 | 396 | 0.980 | 1.000 | [-0.08, 0.02] |
| OECD G7 CLI, change through month 6 | -0.34 | index points | 15 | 353 | 0.159 | 0.952 | [-0.42, -0.17] |
| Chicago Fed NFCI, change through month 3 | 0.03 | index points | 15 | 396 | 0.520 | 1.000 | [-0.01, 0.06] |

## Secondary diagnostics

The monthly HAC regression of the shadow carry spot return on the synchronized-easing state gives -0.238 percentage point per month (Newey-West SE 0.301, t=-0.79, normal-reference p=0.429). The episode randomization result is the preferred small-event inference.

Threshold and leave-one-currency constructions are reported in `outputs/mechanism/tables/public_proxy_sensitivity.tex` and the machine-readable sensitivity CSV. These checks vary the event proxy, not the unavailable IYC signal. Onset counts need not be monotone in the cut threshold because every threshold definition applies its own three-month quiet-window rule.

## Simulation boundary

The synthetic exercise makes one structural point: if delivered easing re-steepens curves after a latent stress state begins, a static contemporaneous inversion count can switch off before delayed losses, while a fresh-entry/confirmed-exit latch can remain on. The simulation is deliberately not calibrated. It cannot establish that the historical latch was chosen independently, that the paper's episodes are correct, or that its return estimates generalize.

## Interpretation limits

- Synchronized policy easing is partly a response to stress, so all empirical results are associations around a downstream event, not causal effects or predictive tests.
- Policy-rate ranks are an imperfect substitute for money-market or forward rates. Spot returns omit the carry income leg and transaction costs.
- CFTC coverage is limited to directly matchable futures contracts. NOK and SEK are absent, and the DEM/EUR splice is a documented proxy. Only the same-N rotations enter its finite reference, so its p-value is discrete and low-powered; the exact reference count is reported beside the estimate.
- ACM describes the U.S. Treasury curve. It cannot remove country-specific or regional term premia from foreign curves.
- OECD CLI and FRED graph histories are current-vintage. The CLI may include financial information and therefore is secondary mechanism evidence.
- Holm adjustment covers the declared primary family, but specification search in the original paper remains outside this public-proxy exercise.
