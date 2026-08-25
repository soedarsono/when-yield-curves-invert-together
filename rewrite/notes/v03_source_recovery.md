# v0.3 source-recovery memorandum

> **Historical source-audit record; public-proxy values superseded.** The source-paper recovery findings remain current, but older public 10-year-minus-3-month values in the audit trail (`-6.58`, `45/64`, `108` active months, `20` episodes, raw `p=0.062`, family value `0.562`) predate the final implementation. The final public values are `-3.2016`, raw `p=0.3348`, maximum-$|z|$ reference `1.000`, `41/64` negative, rank `22/64`, `99` active months, and `18` episodes. See the final-release addendum.

Audit date: 2026-08-26
Source papers: `AI JMP.pdf` (94 PDF pages) and `Alt_JMP_v0.2.pdf` (26-page main paper plus an 18-page online appendix in the combined file)
Current rewrite reviewed: all main and online-appendix LaTeX sources, source crops, source-claim ledger, copied-material ledger, equation ledger, transformation ledger, identification audit, and page-by-page audit
Method: full text extraction by PDF page, visual inspection of the decisive source exhibits, and cross-checking every recommended number against the existing provenance ledgers
Machine-readable companion: `v03_source_recovery_mapping.csv`

## Bottom-line editorial judgment

Alt v0.2 remains the correct architectural spine. The longer paper contains several pieces of source evidence that should be recovered, but the recovery must be asymmetric:

1. **Promote the evidence that directly distinguishes a cross-country configuration from nearby alternatives.** The strongest omitted objects are source Tables 7 and 8 (PDF pp. 47 and 49), the displayed state-definition grids in Tables C.1--C.3 (p. 79), the current-count repair in Table D.2 (p. 84), and the U.S.-inclusive construction in Table F.1 (p. 88).
2. **Disclose adverse robustness instead of claiming a uniformly robust rule.** The exact carry coefficient is concentrated near the baseline 10Y--2Y, two-curve, two-month-release rule. The equity-beta exposure ordering travels better than the carry estimate. This difference should be a finding in v0.3.
3. **Keep the mechanism modest.** The source establishes prediction and exposure ordering. It does not identify a global-growth shock, disaster probability, term-premium channel, delayed compensation friction, or causal effect of inversions.
4. **Do not represent missing new analyses as completed.** Leave-one-country-out states, a full multiverse, search-adjusted inference, executable forward returns, country-level term-premium decompositions, and a true external holdout cannot be recovered from the PDFs or current public-data files.

The most defensible source-grounded v0.3 claim is:

> In the reported 1988:01--2026:02 sample, a path-dependent state built from synchronized non-U.S. G10 yield-curve inversions predicts lower next-month carry spot returns. The result is not spanned by the reported U.S.-curve, average-slope, or own-curve specifications, and the bilateral losses are ordered by a predetermined equity-beta proxy. The exact carry magnitude is sensitive to reasonable state definitions, whereas adverse exposure ordering is more persistent across the reported perturbations.

That claim is stronger than Alt v0.2 because it makes the cross-country-configuration comparison explicit. It is more credible than AI JMP because it states the state-definition sensitivity and does not convert exposure ordering into structural identification.

## What the two drafts actually contain

Alt v0.2 already preserves the main reported return difference, the exact-one/exact-two contrast, the U.S. and average-slope comparisons, beta ordering, selected controls, term-premium asymmetry, calendar stability, emerging-market breadth, the compensation comparison, and the main limitations. Its reader-facing weakness is not absence of claims. It is absence of the source exhibits that let a skeptical reader inspect the most important comparisons.

AI JMP's useful reservoir is concentrated in a small number of places:

- **State construction and timing:** Figure 1 (p. 5), Figure 2 (p. 18), Tables C.1--C.3 (p. 79), Figure D.1 and Table D.1 (pp. 81--82), and Table D.2 (p. 84).
- **Cross-country configuration:** Tables 7--8 (pp. 47 and 49) and Table F.1 (p. 88).
- **Exposure ordering:** Table 2 and Figure 5 (pp. 32--33), Table G.1 (p. 89), and Table H.1 (p. 91).
- **Distribution and stability:** Tables 4--5 (pp. 39--40) and Table E.1 (p. 86).
- **Alternative explanations:** Table 14 (p. 59) and Table K.1 (p. 94).
- **Breadth, with weak independent variation:** Tables 9--12 (pp. 50--55).

The remainder is either exploratory, duplicative, or outside the central contribution.

## Conflicts and overclaims in the proposed v0.3 plan

### 1. The proposed signal-extraction equations have a sign and identification problem

The plan writes `z_i,t = g_t + u_i,t`, defines inversion as `z_i,t < c_i`, and then writes currency depreciation as `Delta s_i,t+1 = -lambda_i g_t+1 + e_i,t+1`. If an adverse common component is a low value of `g`, the last equation predicts appreciation for positive exposure. The normalization must be reversed or the factor must be defined as an adverse state with the inversion inequality adjusted.

More fundamentally, the statement that several inversions make a common component more likely relies on cross-country restrictions on the idiosyncratic terms. The original paper's iid/identical-loading threshold apparatus (original equations 6--7, Appendix B pp. 77--78) was correctly removed from Alt because it is restrictive and its calibration can imply a threshold other than two. A short qualitative framework can motivate the tests, but it should not present the threshold's posterior interpretation as established. The safe formulation is:

> Several fresh inversions are more consistent with shared information than one inversion under a common-plus-country-specific signal interpretation; the return tests evaluate that conjecture without identifying the underlying shock.

### 2. “Individual-country states do not reproduce the result” is too categorical

Source Table 8 (p. 49) shows that only the Australian own-state coefficient is marginally detectable alone (`-8.76`, bootstrap `p=0.044`), and all nine own-state coefficients become imprecise conditional on the cluster. That supports the cluster comparison. But source Table 7 (p. 47) reports the nine own signals as jointly informative (`p=0.005` for carry spot and `<0.001` for carry total) when added to the cluster, and the original text says many individual coefficients are positive. The defensible claim is that own states do not **span** the synchronized configuration or reproduce its adverse portfolio pattern, not that individual curves contain no information.

### 3. “Smooth global yield factors” exceeds the reported evidence

The source reports an average G10 slope and its one-month change in Table 7. It does not report the proposed first principal component, slope dispersion, or a comprehensive smooth-factor family. Until those are estimated, use “the reported average-slope measures,” not “smooth global yield factors” in general.

### 4. The reported specification neighborhood is unfavorable for a broad carry-robustness claim

Source Tables C.1--C.3 (p. 79) show:

- exactly one live inversion: carry spot `+8.33`, `p=0.005`;
- baseline at least two: `-12.85`, `p=0.001`;
- exactly two: `-15.72`, `p=0.001`;
- at least three: `-6.77`, `p=0.405`;
- at least four: `-0.75`, `p=0.879`;
- one-month release: `-12.14`, `p=0.059`;
- two-month release: `-12.85`, `p=0.001`;
- three-month release: `-3.59`, `p=0.161`;
- 10Y--3M: `-4.68`, `p=0.146`.

The signs are not uniformly adverse across the breadth grid, and precision is concentrated at the baseline release rule. The correct conclusion is not “most reasonable versions work.” It is that the exact-one/exact-two sign change supports nonlinear configuration information, while the carry magnitude is sensitive to how the state is persisted and which short maturity defines inversion.

The high-beta coefficients are more stable: `-4.62` (`p=0.008`) for any live inversion, `-10.43` (`p=0.012`) for exactly two, `-10.35` (`p=0.035`) under one-month release, `-4.23` (`p=0.001`) under three-month release, and `-5.25` (`p=0.011`) under 10Y--3M. This asymmetry is one of the most useful source-grounded facts for v0.3.

### 5. The beta result fails an important full-sample alternative benchmark

The plan proposes robustness to MSCI World. Source Table G.1 (p. 89) already reports that test. Over the maximal full sample, the S&P-beta portfolio has a spot coefficient of `-7.93` (`p=0.005`), while the MSCI-beta portfolio has `-2.93` (`p=0.319`); the corresponding total coefficients are `-7.19` (`p=0.009`) and `-4.00` (`p=0.162`). MSCI estimates become detectable only after 1999. The source attributes the early failure to Japan's large MSCI weight, which is plausible but not an exogenous resolution of benchmark selection.

V0.3 must disclose this result. It should say that the exposure ordering is robust across several **state definitions using the S&P-based beta**, but not across all equity benchmarks over the full sample. It should not promise MSCI robustness as if it were untested.

### 6. The term-premium statement must preserve the carry/beta asymmetry

Source Table K.1 (p. 94) reports that the U.S.-ACM-stripped state leaves the high-beta spot coefficient at `-6.17` (`p=0.004`) but attenuates the carry spot coefficient to `-5.42` (`p=0.107`). The state also broadens from 92 months/15 runs to 125 months/18 runs and overlaps the baseline in 83 months. “Results persist after removing a common term-premium component” is too broad. Only the exposure result remains statistically detectable; the carry estimate becomes smaller and imprecise. The adjustment also removes only fitted exposure to a U.S. common proxy, not foreign country-specific term premia.

### 7. Leave-one-country-out evidence does not exist in the source

Source Table 8 conditions on each currency's own state and own slope variables, but its cluster still includes that country's curve. It is not a leave-own-curve-out state. Any sentence saying that other countries' curves predict the excluded country's currency must wait for a genuine reconstruction of the panel.

### 8. The public-data easing analysis is downstream, not validation of the inversion state

The current online appendix's synchronized delivered-easing exercise uses a different event definition and public inputs. The pair/triple screen gives a CHF--GBP common-rotation maximum-$|z|$ reference of `0.0352` under the stated simultaneous-shift exchangeability assumption and six-event eligibility threshold. Its interval includes zero, the pattern weakens when October 2008 is omitted, and stricter event-count thresholds yield no family crossing. This belongs in an exploratory online appendix or repository note, not in the main v0.3 robustness section. Its conditional reference cannot be transferred to the unavailable inversion-state multiverse.

### 9. Emerging markets add breadth, not independent shocks

All seven EM bilateral coefficients are negative in source Table 9 (p. 50), and the pooled spot coefficient in Table 10 (p. 51) is `-14.37` with `p=0.104`. This is useful directional evidence because EM currencies do not construct the state. It shares the same global dates and only about twelve relevant runs in the shorter sample. “External validation” or “replication” is too strong.

### 10. A page target is not evidence

The proposed 30--35 pages can be sensible only if the extra pages carry the configuration horse race, the specification neighborhood, and exposure robustness. The paper should not restore weak applications to hit a page count. A 26--30 page main paper with the decisive source evidence would be preferable to a 35-page paper padded by downcurve, UIP, equity, or trading material.

## Exact source recovery recommendations

### Priority A: restore or promote in the main paper

#### A1. A compact cross-country-configuration horse race from source Table 7 (p. 47)

**Destination:** Main Section 4, immediately after the exact-one/exact-two dose response; main Table 4, “Synchronization versus nearby curve states.”
**Form:** Native LaTeX transcription of the carry spot/total columns, with high-beta columns if space permits. Keep both specifications: average G10 slope/change plus U.S. inversion, and the same specification plus nine own states.
**Numbers to retain:**

- Cluster with global slope, slope change, and U.S. inversion: carry spot `-13.45` (`p=0.003`), carry total `-12.44` (`p=0.012`).
- Cluster after adding nine own signals: spot `-26.79` (`p<0.001`), total `-27.52` (`p<0.001`).
- U.S. inversion coefficients in the joint columns are positive and imprecise (`+2.95`/`+2.23` for spot; `+2.42`/`+1.63` for total).
- Nine own signals are jointly informative (`p=0.005` and `<0.001` for carry spot and total).
- U.S. inversion alone: spot `-1.90` (`p=0.484`), total `-1.34` (`p=0.637`).

**Epistemic status:** Source-reported and unreplicated.
**Interpretation:** The configuration contributes information beyond these reported transformations; the more-negative coefficient after adding own states is not a causal purification.

#### A2. The bilateral cluster-versus-own-curve comparison from source Table 8 (p. 49)

**Destination:** Main Section 5, after the beta scatter, as a concise panel or a short main-text summary with the full table in the online appendix.
**Form:** Preserve the columns “own signal alone,” “cluster alone,” “cluster + own,” and the full own-curve-control specification. If the full nine-row table is too large, main text should report the pooled and two high-beta currencies, while the appendix carries all rows.
**Numbers/text to retain:**

- Australia cluster-alone `-13.21` (`p=0.015`); New Zealand `-13.28` (`p=0.011`).
- Australia own-state alone `-8.76` (`p=0.044`), the only marginal own-state result; conditional own-state estimates are imprecise for all nine.
- Full-specification cluster estimates remain negative for Australia (`-12.92`) and New Zealand (`-8.56`) but bootstrap precision weakens (`p=0.262` and `0.220`).
- Pooled currency-fixed-effect cluster coefficient `-4.74` with Newey--West `t=-2.34`; pooled own-state coefficient `-0.01`, `t=-0.01`.
- Own-curve joint tests reject only for Japan (`p=0.006`), not the other eight (`p>=0.115`).

**Epistemic status:** Source-reported; cluster includes own country's curve.
**Boundary:** This is the closest available source evidence to a leave-one-country-out design, but it is not that design.

#### A3. A transparent reported state-definition neighborhood from Tables C.1--C.3 (p. 79) and D.2 (p. 84)

**Destination:** Main Section 4.4 or Section 6; one main table and, if desired, a coefficient plot constructed only from the reported cells. Full source rows in the online appendix.
**Form:** Do not call it a “full multiverse.” Label it “Reported state-definition neighborhood.” Mark the baseline and group rows by breadth, release, tenor, and current-count repair. Do not rank rows by estimated return.

**Essential cells:** all breadth and release rows listed under conflict 4; 10Y--3M; current count; reciprocal-age current count; baseline. Table D.2 adds:

- raw current count: carry spot `-3.18` (`p=0.047`), high-beta spot `-4.73` (`p=0.005`);
- reciprocal-age current count: carry spot `-10.43` (`p=0.040`), high-beta spot `-14.87` (`p=0.001`);
- under NFCI/VIX controls, reciprocal-age carry `-7.55` (`p=0.084`) and high-beta `-13.82` (`p=0.008`).

**Epistemic status:** Source-reported, in-sample, per-specification inference only.
**Interpretation:** The cross-country threshold/nonlinearity is visible, but the precise carry rule is selection-sensitive. The exposure sort travels more consistently.

#### A4. U.S.-inclusive construction from source Table F.1 (p. 88)

**Destination:** Main Section 6, one sentence and selected cells in the alternative-explanations table; full table in the online appendix.
**Numbers to retain:**

- Baseline G10 carry: spot `-12.85` (`p=0.001`), total `-11.31` (`p=0.003`).
- Add U.S. curve to signal: spot `-11.72` (`p=0.001`), total `-10.20` (`p=0.006`).
- Dollar-inclusive portfolio with baseline signal: spot `-13.11` (`p<0.001`), total `-11.54` (`p=0.009`).
- Dollar-inclusive portfolio plus U.S. curve: spot `-12.10` (`p=0.001`), total `-10.57` (`p=0.013`).
- Ten-curve state: 101 months; all 92 baseline months are included; the dollar is in the funding leg 31 percent of months.

**Epistemic status:** Source-reported and unreplicated.
**Interpretation:** Excluding the U.S. is not load-bearing for the reported result. This does not imply the U.S. curve is irrelevant to global conditions.

#### A5. Full-sample beta-benchmark failure from source Table G.1 (p. 89)

**Destination:** Main Section 5 or Section 6 as an explicit limitation; full table in the online appendix.
**Numbers to retain:** full-sample S&P beta spot `-7.93` (`p=0.005`) versus MSCI beta spot `-2.93` (`p=0.319`); totals `-7.19` (`p=0.009`) versus `-4.00` (`p=0.162`). Post-1999 S&P and MSCI spot effects are `-11.10` (`p=0.003`) and `-7.67` (`p=0.030`).
**Epistemic status:** Source-reported adverse robustness.
**Interpretation:** The beta proxy is benchmark-sensitive over the full sample; the post-1999 agreement is a subsample result, not a repair of the full-sample failure.

#### A6. Preserve the accounting decomposition and report the return object accurately

**Destination:** Main Section 2 and headline table.
**Source:** Original equations 1--4 (pp. 11--13), Table 1 (p. 24), and Table 4 (p. 39).
**Numbers:** income leg averages `3.91` percent/year; no-signal spot/total `2.85`/`6.45`; state spot/total `-10.00`/`-4.86`; state-minus-no-state spot/total `-12.85` (`p=0.001`) and `-11.31` (`p=0.003`).
**Boundary:** These are money-market-differential return proxies, not executable forward returns after basis, spreads, and timing costs.

### Priority B: retain or recover in the online appendix, with concise main-text use

#### B1. Full distribution evidence: Tables 4--5 (pp. 39--40)

Retain the headline mean table in the main paper. Add a compact distribution table or appendix panel with median (`0.35` to `-0.76` percent/month), 25th percentile (`-0.93` to `-1.98`), 10th percentile (`-2.35` to `-3.94`), and the bottom-decile-deletion coefficients (`-7.24`, `p=0.006` spot; `-5.50`, `p=0.024` total). Keep the high-beta fixed `-4` percent/month hazard result (`4.6` to `9.8` percent, `p=0.033`) supporting, because the source does not document that the cutoff was frozen ex ante.

#### B2. Current-count anatomy: Figure D.1 and Table D.1 (pp. 81--82)

Recover in the online appendix. These objects make the path dependence inspectable: current count 165 months versus live state 92; the live state contains all five worst carry-total months whereas the current count contains two. But tail capture is outcome-selected and partly reflects the historical motivation for the latch. It is a classifier diagnostic, not independent validation.

#### B3. State incidence and input series: Tables A.1--A.3 and Figures A.1--A.2 (pp. 72--75)

Keep compact data summary and state-incidence cells. Restore the rate and beta time-series figures only if they remain readable and directly support persistent rankings. The central incidence fact is 33 active months out of 84 in 1988--94 versus 3 of 120 in 2010--19. Figure A.2 uses S&P-based betas and should be accompanied by the Table G.1 benchmark limitation.

#### B4. Portfolio persistence: Table H.1 (p. 91)

Place the full table in the online appendix and retain the concise main-text interpretation. Key carry-long shares are New Zealand `85` percent overall/`91` percent in state and Australia `71`/`73`; Japan is short `83`/`97` and Switzerland `96`/`100`. For the high-beta sort, Canada is long 100 percent, Australia `97`/`92`, and New Zealand `77`/`76`. This supports standing exposure rather than state-month resorting; it does not identify why those currencies have those exposures.

#### B5. Calendar and influence evidence: Table E.1 (p. 86) and source text pp. 85--87

Retain the split table in the appendix and its asymmetric interpretation: carry spot is negative in both halves (`-11.41`, `p=0.037`; `-15.85`, `p=0.010`), but high-beta is weak before 2005 (`-4.01`, `p=0.287`) and strong later (`-11.91`, `p=0.010`). The leave-one-episode result exists only as a source textual summary: carry coefficients remain within about one-third of baseline; high-beta worst bootstrap `p=0.006`. Do not invent an episode forest or exact deletion coefficients.

#### B6. Risk controls: Table 14 (p. 59)

Use selected cells in a main alternative-explanations table and put the full staircase online. Carry spot is `-12.84` (`p<0.001`) with NFCI and `-13.18` (`p=0.004`) with NFCI and VIX; high-beta spot is `-8.38` (`p=0.011`) and `-8.24` (`p=0.025`). Call these spanning diagnostics. The source's statement that VIX and credit measures cannot span a first-moment state “by construction” is wrong; lack of spanning is an empirical result in these regressions, not a mathematical implication.

#### B7. Common term-premium diagnostic: Table K.1 (p. 94)

Restore the full table in the online appendix and preserve the asymmetric main-text summary described above. The table is useful precisely because it weakens the carry result while preserving the high-beta result.

#### B8. Emerging-market breadth and compensation: Tables 9--12 (pp. 50--55)

Retain the current condensed treatment. All seven EM bilateral coefficients are negative, but pooled inference is weak. The common-sample G10 and G10+EM active-state spot means are similar (`-12.79` and `-12.51`), while total means differ (`-8.67` and `+2.51`) because implied income is about `4.12` versus `15.02`. This is a useful accounting contrast and a warning against calling the state a universal negative-total-return rule. Do not restore the trading overlays built on these portfolios.

#### B9. Local-projection timing: Figure 6 (p. 37) and Figure J.1 (p. 93)

Keep online as supporting chronology. The leading indicator falls about `0.6` percent at six months and is similar in onset/controlled designs; industrial production becomes imprecise under full controls. Figure J.1 is not the episode-onset cumulative-return event study proposed for v0.3. Do not relabel it as one.

### Priority C: demote to exploratory appendix material

- **Downcurve regime:** Table 1 and Figures 3--4 (pp. 24--26), filtered rows in Tables 2--6, and related equations 16--17. The `+16.75`-point within-state total-return wedge (`p=0.053`) is concentrated in the 1988--91 and 2023--24 inflation blocks and was found by inspecting false alarms. It should not compete with the configuration contribution.
- **Conditional Fama regressions:** Table 3 (p. 36). The slope moves from `+0.50` to `-1.33`, but the episode-bootstrap interaction has `p=0.340`. Keep as a descriptive image of the carry loss, not a headline UIP reversal.
- **Oil-beta sort:** original discussion p. 34. It is reportedly spanned by carry and equity-beta portfolios and has no displayed source table. Keep only as a brief appendix note if code/output becomes available; otherwise omit.
- **EM-native downcurve regime:** Table I.1 (p. 92). It addresses a secondary regime, uses a seven-month cell, and does not sharpen the configuration result.
- **Public synchronized-easing and country-combination checks:** current online Appendices D--E. Preserve for transparency, but remove the CHF--GBP screen from the main paper. These analyses concern delivered policy easing, not the source inversion state.

### Priority D: reject from reader-facing v0.3

- **Trading overlays and anti-carry rules:** Table 6 and Figure 7 (pp. 42--43), and G10+EM overlays in Figure 8 (p. 56). They lack executable forwards, transaction costs, financing, frozen construction, and a genuine holdout.
- **S&P 500 application:** Table 13 (p. 57). It broadens the paper without identifying the currency mechanism and does not sharpen the cross-country configuration contribution.
- **Strong disaster-probability statements:** abstract and introduction pp. 1--10 and mechanism prose pp. 31--38. The source does not separately identify event probability, loss size, or price of risk.
- **Structural delayed-compensation claims:** original equations 10--14 (pp. 19--21) beyond the compact accounting benchmark. The timing restriction is assumed, not estimated.
- **Threshold sufficiency/calibration apparatus:** original equations 6--7 and Appendix B propositions (pp. 13--17 and 77--78). The iid/identical-loading assumptions are too restrictive and the illustrative calibration does not uniquely support two.
- **Claims that the downcurve is an inflation-normalization regime:** the co-occurrence in two eras is descriptive and selected after inspecting false alarms.
- **“Conventional confirmation” language:** no source citation establishes two consecutive steepening months as a convention in this application.

## Complete exhibit disposition

The companion CSV maps every recovered source figure and table. The summary is:

| Source object | PDF page | v0.3 disposition | Exact destination |
|---|---:|---|---|
| Figure 1 | 5 | Retain main | Introduction, signal timeline |
| Figure 2 | 18 | Retain main, shorten | Measurement, release-rule example |
| Figures 3--4 | 25--26 | Demote | Exploratory downcurve appendix only |
| Figure 5 | 33 | Retain main with caveat | Exposure ordering |
| Figure 6 | 37 | Demote | Macro-timing appendix |
| Figures 7--8 | 43, 56 | Reject | No reader-facing destination |
| Tables 1--3 | 24, 32, 36 | Split | Table 2 main; Tables 1 and 3 appendix/exploratory |
| Tables 4--5 | 39--40 | Retain/condense main | Headline and distribution evidence |
| Table 6 | 42 | Reject | No strategy table |
| Tables 7--8 | 47, 49 | Restore/promote | Configuration and bilateral tests |
| Tables 9--12 | 50--55 | Condense | Exposure breadth/compensation, full online |
| Table 13 | 57 | Reject | No stock application |
| Table 14 | 59 | Condense | Alternative-explanations table; full online |
| Figures A.1--A.2; Tables A.1--A.3 | 72--75 | Restore selected online | Data and predetermined characteristics |
| Tables C.1--C.3 | 79 | Restore/promote | Main reported-neighborhood exhibit; full online |
| Figure D.1; Table D.1 | 81--82 | Restore online | Static-count and tail diagnostic |
| Table D.2 | 84 | Restore/promote | Main neighborhood; full online |
| Table E.1 | 86 | Retain online | Calendar stability |
| Table F.1 | 88 | Restore | Main sentence/cells; full online |
| Table G.1 | 89 | Restore adverse result | Main limitation; full online |
| Table H.1 | 91 | Restore online | Portfolio persistence |
| Table I.1 | 92 | Demote | Exploratory EM regime or omit |
| Figure J.1 | 93 | Retain online | LP design sensitivity |
| Table K.1 | 94 | Restore online | Common-term-premium asymmetry |

## Exact text that can be recovered safely

The following source ideas are worth restoring in rewritten form, not verbatim:

1. **Cross-country configuration as the unit of observation (pp. 45--49):** one live inversion and two live inversions have opposite return signs; the cluster retains an adverse coefficient after the reported U.S., average-slope, and own-curve variables enter.
2. **Standing exposure (pp. 31--34 and Table H.1 p. 91):** the carry and S&P-beta portfolios hold persistent currency blocs, so the conditional loss is not created by wholesale state-month resorting.
3. **Entry versus delivery (pp. 3--5, 18, and 81--84):** fresh entry reduces stale-current-inversion months, while confirmed release retains months after curves begin to re-steepen. State exactly that this design was motivated with knowledge of historical crash timing.
4. **Spot risk versus compensation (pp. 11--13 and 53--55):** similar state-dependent spot losses can produce different total returns when predetermined interest income differs.
5. **Asymmetric robustness (pp. 79, 84, 89, and 94):** beta-sorted losses persist across several state perturbations, while carry and beta-benchmark estimates are more sensitive. This is a more credible result than a blanket “robustness” claim.

Do not restore the source's phrases “the likelier cause is a global shock,” “two is the smallest count at which a systemic explanation is more likely than a coincidence,” “the conventional confirmation of a turning point,” “currencies without growth exposure do not crash,” “the signal identifies moments when global growth exposure is about to be repriced,” or “the signal contains the currency market's disaster risk.” Each exceeds the design.

## Recommended v0.3 exhibit sequence using currently available evidence

This sequence does not pretend the missing new work exists:

### Main figures

1. **Signal construction and carry returns:** source Figure 1 (p. 5), retained.
2. **Live versus current state:** source Figure 2 (p. 18), retained or moved online if main space is tight.
3. **Reported state-definition neighborhood:** a new native plot made only from source Tables C.1--C.3 and D.2; label every point source-reported and show active months.
4. **Exposure ordering:** source Figure 5 (p. 33), with the S&P-beta definition and Table G.1 caveat.

There is no source-grounded episode-onset carry event study, specification curve over a full multiverse, or leave-one-country-out scatter. Those should remain explicit missing exhibits.

### Main tables

1. Data, timing, and state incidence: source pp. 28--30 and Table A.2.
2. Headline carry accounting and distribution: source Tables 4--5.
3. Reported state-definition neighborhood: Tables C.1--C.3 and D.2.
4. Synchronization versus reported nearby states: Table 7, with Table F.1 selected cells.
5. Exposure ordering and own-curve comparison: Table 2, Table 8, Figure 5 statistics, and the beta portfolio/panel interaction.
6. Alternative explanations and adverse robustness: Table 14, Table G.1, and Table K.1.

This is a more source-grounded six-table architecture than mixing unavailable forward returns, unavailable leave-one-country-out estimates, and unavailable search-adjusted p-values into promised tables.

## Epistemic labels v0.3 should enforce

| Label | Meaning | Examples |
|---|---|---|
| Source-reported | Visible in AI JMP but not regenerated | Headline state coefficients, Tables 7--8, C.1--C.3, F.1, G.1, K.1 |
| Derived from source-reported | Arithmetic using visible source cells | Implied income in G10 versus G10+EM comparison |
| Independently generated public check | Produced from declared public inputs but not the source state | Delivered-easing and pair/triple screens |
| Editorial interpretation | Organizes evidence without adding an estimate | Prediction versus mechanism boundary |
| Missing decisive test | Cannot be produced from the current workspace | LOO state, full multiverse, feasible forwards, data-vintage audit, holdout |

No source-reported estimate should be called replicated, reproduced, verified, or executable. No public-data easing result should be called validation of the inversion classifier.

## 90-point internal editorial checklist

The paper cannot earn a genuine 90/100 empirical-design assessment from source recovery alone. It can earn roughly 90/100 for **source discipline and editorial architecture** if every item below is satisfied:

- [ ] The abstract says “reported historical association” or equivalent and distinguishes spot from proxy total return.
- [ ] The title avoids crash, disaster, systemic risk, and causal language.
- [ ] The state algorithm and `t -> t+1` timing are code-exact.
- [ ] The main paper shows, rather than merely narrates, the exact-one/exact-two contrast.
- [ ] Source Table 7's configuration horse race is reader-facing.
- [ ] Source Table 8 is not mislabeled leave-one-country-out.
- [ ] The reported-neighborhood exhibit includes all rows of Tables C.1--C.3 and the age-weighted alternative from D.2.
- [ ] The paper states that carry is sensitive to tenor and release choice.
- [ ] The paper states that S&P-based beta fails full-sample MSCI-benchmark robustness.
- [ ] The U.S.-ACM result reports both the surviving high-beta coefficient and attenuated carry coefficient.
- [ ] The U.S.-inclusive construction in Table F.1 is disclosed.
- [ ] Bottom-decile deletion is labeled outcome-conditioned.
- [ ] Fifteen episodes, not 92 months, are treated as the independent common-state variation.
- [ ] EM evidence is called breadth, not replication.
- [ ] The panel beta interaction (`p=0.210`) and conditional Fama interaction (`p=0.340`) are reported.
- [ ] The pre-2005 high-beta weakness is reported.
- [ ] The compensation model is labeled a candidate restriction, not an estimated mechanism.
- [ ] The main paper excludes strategies, equities, and downcurve as coequal contributions.
- [ ] The public delivered-easing screen is not used as main evidence for the inversion state.
- [ ] Every numerical claim resolves to a source page/table or executable public ledger.
- [ ] No new academic citation is added beyond the original 84-entry bibliography.
- [ ] Missing analyses are listed as missing, not written prospectively as if completed.
- [ ] A dated frozen signal specification is included for future prospective evaluation.

The remaining empirical points require data and code, not editing: a true leave-one-country-out construction, a prespecified comprehensive multiverse with search-adjusted inference, executable forward returns, foreign term-premium decomposition, and a frozen prospective or independent historical validation sample.

## Final recommendation to the v0.3 editor

Recover Tables 7, 8, C.1--C.3, D.2, F.1, and G.1 before recovering anything else. Together they turn the paper from a polished summary of a chosen state into a transparent paper about what the cross-country configuration adds, where the loss lands, and how sensitive the result is to measurement.

The key editorial move is to make the unfavorable evidence do intellectual work. The carry coefficient's sensitivity and the beta proxy's benchmark sensitivity prevent a 90/100 identification claim. But openly reporting them reveals a sharper and more durable source-grounded result: **the precise trading-state return is fragile, while the configuration/exposure pattern is the more stable empirical object.** That is the v0.3 paper the available evidence can honestly support.

## Final post-rewrite missed-content audit

Audit date: 2026-08-26
Comparison: full `AI JMP.pdf` and page-delimited source text against the inputs currently included by `rewrite/main.tex` and `rewrite/online_appendix.tex`

### Overall support for the new framing

The revised **cross-country-configuration** framing is supported as a reduced-form description. The source reports an exact-one/exact-two sign reversal, a cluster coefficient that survives the displayed U.S./average-slope horse race, and own-state controls that do not span the cluster. It does not establish that two curves reveal a structural common shock or that the state measures “common risk.” The present main paper generally observes that boundary.

The **rate ordering** is supported as a long-minus-short relative-return fact and by the large Australian/New Zealand bilateral coefficients. It should not be read as every high-rate currency depreciating absolutely: several country coefficients are small and imprecise, and a negative carry spread can also reflect funding-currency appreciation.

The **beta ordering** is supported by a nine-currency descriptive gradient and a separate S&P-beta-sorted portfolio. It is not a precise structural cross-sectional estimate: the monthly interaction has `p=0.210`, the full-sample MSCI sort fails, and Australia/New Zealand have substantial leverage. The current main paper discloses these limitations, but two statements still use stronger inferential language than the evidence permits.

The **compensation** framing is supported as accounting, not mechanism. The interest differential is known and partly offsets the state-dependent spot loss. Delayed compensation remains an assumed benchmark restriction. The current paper mostly preserves that distinction, but it omits the most direct conditional-income comparison and occasionally calls interest income “compensation.”

### Actionable findings

#### 1. Critical: the reader-facing state recursion enters a curve one month earlier than the source definition

Source equation (9) and text on PDF p. 16 define entry at `t` from a fresh inversion observed at `t-1`:

`L_i,t = 1` when `I_i,t-1 = 1` and `I_i,t-2 = 0`.

The source says explicitly that an inversion “becomes live the month after it is first observed.” The current `appendix/A_signal_algorithm.tex` instead defines a crossing from `q_i,t-1 >= 0` to `q_i,t < 0` and sets `L_i,t=1` at that same month-end. The main measurement section likewise says a curve enters when it freshly crosses. With the maintained statement that `S_t` positions the return in `t+1`, this is not a harmless relabeling: it moves entry and potentially the 92 state months one month earlier than the source-reported classifier.

**Required action:** reconcile the index convention before release. Either restore the source recursion—crossing observed at `t-1`, live status at `t`, return at `t+1`—or demonstrate that all source tables use a relabeled same-month state. Figure 2 and the source prose support the former. The appendix cannot be called code-exact until this is resolved.

#### 2. High priority: restore the source-reported real-time and decay falsification checks

The current paper explains the information timing but omits the strongest source evidence that it was implemented historically. Source pp. 87 reports:

- a truncation audit at 435 month-ends in which no prior signal, inversion count, or own-state classification changes when later observations are added;
- 492 portfolio-membership checks with zero mismatches when conditioning series and sorts are recomputed from truncated data;
- one additional month of lag attenuates carry spot from `-12.9` to `-6.3` and high-beta spot from `-7.5` to `-4.7`, with loss of precision;
- forward-shift placebos destroy the results.

These are source-reported rather than independently regenerated, but they materially sharpen the predictive-timing claim and are more relevant than another mechanism discussion. Add a concise appendix paragraph and, if space permits, one main-text sentence. Do not claim a vintage audit: the source checks truncation of the available market series, not vendor timestamps or historical-data revisions.

#### 3. High priority: the current recursion/accounting discussion omits that conditional carry income rises in the state

Source Table 1 (p. 24) reports annualized carry income of `3.60` percent outside the state and `5.14` percent inside it, a `+1.54`-point difference with bootstrap `p=0.260`. The paper currently reports only the unconditional `3.91` mean and `0.7` minimum.

This conditional comparison is the cleanest accounting fact for the compensation section: income moves in the compensating direction but not enough to offset the `-12.85` spot gap, leaving a `-11.31` total-return gap. It also prevents the reader from thinking the negative total proxy arises because carry income collapses during state months.

**Required action:** report `3.60` versus `5.14` once in the main compensation/accounting discussion, call the difference imprecise, and reserve “compensation” for an interpretation rather than treating the differential as identified risk compensation.

#### 4. High priority: the online algorithm's same-month entry error also contaminates the claimed “fresh” public comparison unless the two classifiers are kept visibly distinct

The public 10Y--3M audit may intentionally use a same-month crossing and its own code-exact rule. That is permissible as a nearby proxy, but it cannot be described as implementing the original source recursion if the source waits one month before live entry. The current appendix abstract and robustness section correctly call the public exercise a nearby proxy; preserve that distinction after fixing the original algorithm.

**Required action:** state separately the source 10Y--2Y entry clock and the public proxy's implemented entry clock. If they differ, include entry timing among the reasons the public estimate is not a replication.

#### 5. Medium priority: replace two overstrong claims about cross-sectional “establishment”

Current Section 5 says the nine-point beta fit “does establish a cross-sectional restriction,” and Section 3 says the evidence “rejects” the possibility of no exposure relation. The source provides no uncertainty for the nine-point second-stage fit; the panel interaction has `p=0.210`; and the full-sample MSCI portfolio is weak.

**Required action:** use “documents a descriptive cross-sectional restriction supported by the S&P-beta portfolio” and “runs counter to no exposure ordering in the reported S&P-based tests.” The abstract's “losses ... grow with predetermined equity-market beta” is defensible only if read as the reported S&P-based pattern; naming S&P or “reported coefficients” would remove ambiguity.

#### 6. Medium priority: persistent membership does not mean the carry portfolio does not rotate

The current main and conclusion say the state reprices standing exposure “rather than” rotating the sort. Source Table H.1 supports persistent core members, but it also shows economically meaningful composition shifts. Norway is in the carry long leg in 62 percent of all months but only 34 percent of state months; Britain is long 43 percent overall and 70 percent in the state. Sweden, the euro, and other funding shares also change materially across cells.

**Required action:** say that persistent AUD/NZD and JPY/CHF membership shows the result is **not created solely** by state-month resorting, while acknowledging that the portfolio continues to re-sort and some memberships change. “Standing exposure rather than rotation” is too exclusive.

#### 7. Medium priority: restore the flat post-state money-market-rate response as a mechanism-relevant null

Source pp. 35--36 and Figure J.1 report that the average G10 money-market rate does not move over the year after a state month under the baseline, onset, or controlled projection. This null is absent from the current prose even though the figure remains online.

It materially constrains the interpretation: the state pools episodes followed by easing with high-rate normalization episodes and therefore is not simply a predictor of subsequent average policy-rate cuts. The leading-indicator decline can support expected-slowdown language, but the flat rate response weakens a uniform coordinated-easing story.

**Required action:** add the null to the online local-projection discussion and cite it when listing competing expected-rate, inflation, and term-premium interpretations.

#### 8. Medium priority: distinguish interest income from identified compensation in the EM comparison

Current Section 7 says similar G10 and G10-plus-EM spot repricing need not imply a universal negative total return “when predetermined compensation differs.” The underlying `4.12` versus `15.02` numbers are mechanically implied interest-income legs. They do not establish that the additional EM differential compensates the same risk.

**Required action:** replace “predetermined compensation” with “predetermined interest income” in the empirical comparison. The next sentence may say this is consistent with differential compensation, provided it remains interpretive.

#### 9. Medium priority: “a lone inversion often belongs to one country's rate cycle” is not directly shown

The exact-one months have positive carry returns, but the source does not display an attribution of those months to national rather than regional/common shocks. Current Section 4 turns the common-plus-country-specific framework into a historical statement: “A lone fresh inversion often belongs to one country's rate cycle.”

**Required action:** write “is consistent with a national rate cycle” or “can arise from” instead of “often belongs.” The sign contrast establishes different return associations, not the shock composition of exact-one months.

#### 10. Medium priority: avoid “identifies when” in the compensation conclusion

Current Section 6 says the configuration “identifies when” exposures subsequently lose. In an otherwise careful paper, “identifies” risks conflating historical classification with econometric identification.

**Required action:** use “historically predicts” or “classifies months before” and retain the existing statement that neither the shock nor the compensation friction is identified.

#### 11. Lower priority: qualify the public-proxy synthesis

The final public family has 41 of 64 negative estimates, a finite common-calendar maximum-$|z|$ reference of `1.000`, crisis-deletion `p=0.826`, and an asymmetric disjoint-geography result. These results do not support language that the family “confirms” the original state or establishes “recurring directional information.” A non-independent majority of negative rules with no family-threshold crossing is a descriptive sensitivity result.

**Required action:** say the public family “shows a recurring negative direction across related rules without adjusted statistical detection.” This preserves its value as transparency about sensitivity without converting sign counts into confirmation.

#### 12. Lower priority: remove “complete” from the original specification-neighborhood description

The introduction says it shows the “complete state-definition neighborhood reported in the underlying analysis.” The source contains the displayed C.1--C.3 grid, D.2 repairs, U.S. inclusion, extra-lag and timing checks, and additional replication-package variants. The present main figure itself correctly says it is not the complete set examined.

**Required action:** use “complete displayed C.1--C.3 neighborhood” or, more simply, “the reported local neighborhood.”

### Material that remains appropriately omitted

No additional trading overlay, stock-market application, downcurve strategy, EM-native regime, or conditional-UIP headline should be restored. The current paper already discloses the MSCI failure, implied-volatility beta null, pre-2005 beta weakness, term-premium carry attenuation, EM imprecision, and absence of true leave-one-country-out 10Y--2Y evidence. Those are the principal adverse cells needed for a fair evaluation.

## Final-release addendum: public audit after implementation fixes

The corrected nearby public proxy reports `-3.2016` annualized percentage points with raw circular reference `p=0.3348`, using `99` active months and `18` episodes. The finite common-calendar maximum-$|z|$ reference is `1.000`; `41/64` rules are negative, no rule crosses the 5-percent family threshold, and the baseline ranks `22/64`. Deleting the three named crisis episodes gives `-0.46` (`p=0.826`), while deleting the five worst active months produces `+0.94` and is deliberately reported without a p-value. European curves paired with non-European currencies give `-15.84` (`p=0.062`); the reverse split gives `-0.34` (`p=0.887`). These findings strengthen the case for treating the exercise as an adverse nearby-measurement audit rather than as validation of the original 10-year-minus-2-year state.
