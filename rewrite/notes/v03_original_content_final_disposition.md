# Final original-paper content disposition

Audit date: 2026-08-26
Source reviewed: all 94 pages of `AI JMP.pdf`
Comparison target: final 38-page v0.3 main paper and 27-page Online Appendix

## Verdict

No additional source-grounded result should be promoted into the v0.3 main paper. A final adversarial re-read corrected the raw-count tail interpretation and restored high-beta tail frequency, front-loaded carry timing, EM concentration, and the classifier-change boundary in the term-premium exercise. The remaining omissions are deliberate: they are either secondary to the cross-country-configuration contribution, selected after observing outcomes, statistically weak, non-executable, or impossible to reconstruct from displayed PDF cells.

## Economics recovered in v0.3

| Source content | Final use | Why it matters |
|---|---|---|
| Exact live-entry timing: crossing at `t-1`, live at `t`, return at `t+1` | Main Section 2; Online Appendix A | Prevents a one-month look-ahead error and gives path dependence a precise information-clock interpretation |
| 435 real-time truncation endpoints and 492 portfolio-membership checks with no reported mismatches | Online Appendix A | Strongest available evidence that the historical predictor and sorts use information available at formation |
| Extra-lag attenuation and forward-shift placebo failure | Online Appendix A | Shows the association is short-lived and does not arise when the signal is moved after returns |
| Conditional carry income: 3.60 outside versus 5.14 inside the state | Main Sections 4 and 7 | Shows interest income moves in a compensating direction but is too small, and too imprecisely different, to offset spot losses |
| Separate exactly-one and exactly-two indicator coefficients | Main Sections 1, 4, and 8; Online Appendix C | Supports a configuration interpretation while explicitly avoiding a false direct one-versus-two contrast |
| Reported breadth/release/tenor/current-count neighborhood | Main Figure 3 and Table 3 | Makes carry-magnitude sensitivity visible and shows freshness contains information |
| Portfolio-level horse race with average slope, slope change, U.S. inversion, and all nine own states | Main Table 4 | Establishes what the configuration adds relative to the transformations actually reported in the source |
| Bilateral own-curve specifications | Main Section 5; Online Appendix Table 7 | Shows that the cluster is not generally reproduced by a currency's own state, while admitting that this is not a leave-own-country-out signal |
| U.S.-inclusive state construction | Main Section 6 and Table 8 | Distinguishes excluding the dollar currency from treating U.S. curve information as irrelevant |
| S&P-versus-MSCI beta failure | Main Section 5 and Table 7 | Prevents a nine-dot S&P pattern from being mistaken for benchmark-invariant structural exposure |
| Panel state-by-beta interaction `p=0.210` | Main Section 5 and Table 5 | Makes clear that the portfolio and descriptive bilateral gradient—not currency-month count—carry the exposure evidence |
| Portfolio composition, including Norway 62/34 and pound 43/70 | Main Section 5 and Table 6; Online Appendix C | Shows persistent cores and state-dependent rotation coexist |
| U.S. ACM term-premium controls and classifier adjustment | Main Section 6 prose: lagged ACM control/spanning exercise; Main Table 9 and Online Appendix C: rebuilt classifier | Distinguishes predictive spanning, where lagged U.S. premium controls leave the state coefficients intact, from rebuilding the classifier, where beta remains negative but the carry coefficient attenuates materially |
| Average G10 money-market rate approximately flat for a year | Online Appendix C and Figure 1 | Rejects a simple uniform coordinated-easing account even though leading activity indicators weaken |
| G10 versus G10+EM spot/income/total decomposition | Main Section 7; Online Appendix C and Table 8 | Shows a similar spot-risk state can imply different total returns when predetermined interest income differs |
| Calendar halves, tail deletion, influence, NFCI/VIX/dollar/volatility controls | Main Section 6; Online Appendix C | Makes episode concentration and the distinction between predictive and contemporaneous controls visible |
| Raw-count versus live-state tail capture and concentration | Online Appendix C | Correctly separates absolute tail coverage from the live state's greater concentration and five-month extreme-tail capture |
| High-beta crash frequency with nearly unchanged variance | Online Appendix C | Shows that the beta portfolio's distributional result is a higher realized tail frequency rather than a general volatility increase |
| Front-loaded carry response and partial rebound | Online Appendix C | Locates the historical spot adjustment in months one through six without interpreting overlapping local projections causally |
| EM country precision and persistent portfolio concentration | Online Appendix C | Shows that pooled EM breadth is imprecise and the combined sort is effectively a persistent EM-versus-funding-bloc exposure |
| Conditional UIP interaction `p=0.340` | Main Section 7; Online Appendix C | Keeps the conditional-UIP result descriptive rather than converting an imprecise interaction into a mechanism |

## Material deliberately not restored

| Source content | Disposition | Economic reason |
|---|---|---|
| Downcurve regime as a coequal contribution | Omitted from main; limited sensitivity references retained | The split was motivated by observed false alarms, is concentrated in two inflation-era blocks, and does not identify an inflation-normalization regime |
| Trading overlays and anti-carry strategies | Omitted | No feasible forwards, basis, bid-ask costs, financing, frozen construction, or genuine holdout |
| S&P 500 return application | Omitted | Broadens the draft without sharpening the currency contribution or identifying the mechanism |
| Oil-beta sort | Omitted | No complete displayed table; source says the sort is spanned by carry and equity beta |
| EM-native downcurve result | Omitted | Seven-month cell and secondary selected regime do not improve the configuration result |
| Structural threshold-sufficiency and calibration apparatus | Omitted | Identical-loading/iid assumptions are too restrictive and do not identify two inversions as a structural cutoff |
| Strong disaster-probability language | Omitted | The design does not separately identify event probability, loss size, or the price of disaster risk |
| Structural delayed-compensation claim | Reduced to an accounting benchmark | Delayed compensation is an assumed restriction, not an estimated friction |
| Full strategy/asset-pricing interpretation of the carry proxy | Omitted | Money-market accounting and spot returns are not an executable one-month forward excess return |

## Valuable analyses that the original PDF cannot supply

The final audit also confirms that several decisive tests are genuinely missing rather than overlooked:

- exact 10Y--2Y state construction without country `i` when predicting currency `i`;
- the complete historical state-definition search universe and joint resamples;
- a 15-row core episode ledger with contributor curves, spot, income, total return, and all joint crisis deletions;
- executable forward returns with basis, spreads, and settlement conventions;
- comparable country-level expected-rate and term-premium decompositions;
- a genuinely unused historical or prospective evaluation sample.

None can be recovered reliably by digitizing the PDF. They remain future data/code requirements rather than silent omissions from v0.3.

## Final economic reading

The source contains one durable contribution once its excess claims are removed: a nonlinear cross-country configuration of fresh yield-curve inversions precedes exposure-ordered currency spot losses. The precise carry magnitude is sensitive to tenor and persistence; the S&P-based beta ordering is more stable across the reported state perturbations but fails one important full-sample benchmark. The source's underused income, composition, timing, and macro-null evidence now makes that narrower contribution more economically informative without manufacturing a mechanism.
