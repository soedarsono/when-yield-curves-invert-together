# Public 10-year-minus-3-month yield-proxy outputs

This directory contains the v0.3 current-vintage nearby-measurement and specification-search audit. It does not reproduce the original paper's 10-year-minus-2-year state or forward excess returns.

## Estimand and timing

The outcome is a **policy-ranked log spot-return proxy**. For a one-month-lag rule, policy-rate differentials available by formation month `t` rank the non-dollar G10 currencies and the outcome is the basket's BIS log spot return in `t+1`. For a two-month-lag rule, the basket is re-sorted with rates available by `t+1` and its return is measured in `t+2`; it is not a month-`t` basket held for two months. The target long and short leg sizes are two or three currencies; all currencies tied at a cutoff receive equal weight, so an actual leg can contain more than its target number. The proxy is not interest-inclusive carry, a forward return, or a trading return net of costs.

The public state uses current-vintage OECD monthly 10-year government-bond yields less 3-month interbank rates delivered through FRED. Germany supplies the euro-area curve through 1998 and EA19 supplies it from 1999. The change in geographic concept, tenor, short-rate instrument, monthly timing, and data vintage prevents interpreting this exercise as replication or external validation of the source-paper state.

## Output schema

| File | Unit | Purpose |
|---|---|---|
| `baseline_curve_recursion_audit.csv` | currency-month | Inputs and every transition of the baseline public state recursion |
| `baseline_monthly_state.csv` | calendar month | Baseline state, breadth, episode membership, and next-month policy-ranked log spot-return proxy |
| `baseline_episode_ledger.csv` | contiguous baseline episode | Onset, end, duration, cumulative proxy return, and worst monthly proxy return |
| `baseline_sensitivities.csv` | declared sensitivity | Baseline, crisis-episode deletion, calendar halves, and outcome-conditioned worst-month deletion |
| `specification_family.csv` | declared rule | Complete 64-rule nearby public family, raw rotation reference, common-calendar maximum-standardized-coefficient reference, and coefficient rank |
| `leave_one_country_out.csv` | jointly excluded currency | Joint delete-one influence diagnostic: the named currency is removed from both state construction and the outcome universe |
| `geographically_disjoint.csv` | sensor/outcome split | Diagnostics in which no signal currency appears in the outcome basket |
| `figures/specification_curve.png` | figure | Coefficients for the declared 64-rule family |
| `public_yield_proxy_report.md` | report | Human-readable summary generated from the machine outputs |
| `run_manifest.json` | run | Environment information and SHA-256 records for raw inputs, code/configuration, machine outputs, and paper-facing outputs |

## Rotation-reference fields

`p_circular_raw` is a finite circular-shift reference for one displayed rule. For the main 64-rule family, the same shift is applied to the full common calendar before each rule's valid-outcome mask is imposed.

`p_maxT_family` is a legacy machine-field name. It records the **finite common-calendar maximum-$|z|$ rotation reference**, where each rule's rotated coefficient is centered and scaled by its own rotation distribution before the cross-rule maximum is formed. Interpreting this value as family-wise error control requires simultaneous cyclic-shift exchangeability of the state relative to the return outcomes under the maintained null. Without that assumption, it is a specification-family diagnostic, not an unconditional FWER guarantee and not a regression maximum-$|t|$ statistic.

The filename `leave_one_country_out.csv` is also retained for compatibility. Its estimand is joint delete-one influence, not a leave-one-country-out reconstruction of the original state. The exclusion and geographically disjoint raw references circularly shift each complete-case sequence; months missing from a sequence are compressed rather than treated as literal intervening calendar positions. These overlapping diagnostics are sensitivity checks, not independent tests.

The outcome-conditioned deletion of the five worst active months receives no p-value by design. It measures concentration and is not a preferred estimator.
