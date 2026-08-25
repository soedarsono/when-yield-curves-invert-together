# v0.3 native-table transcription checks

Audit date: 2026-08-26
Source: `AI JMP.pdf`
Scope: six new native LaTeX tables under `rewrite/generated/tables/`
Status: source transcription only; none of the underlying estimates has been regenerated

## Method

Each source table was checked in three representations:

1. the visible source-PDF crop under `rewrite/assets/original/`;
2. page-delimited text extracted from `AI JMP.pdf`;
3. the new native LaTeX file.

The audit checked coefficients, Newey--West or run-clustered statistics, displayed bootstrap or Wald `p`-values, sample counts, panel definitions, and source-specific qualifications. A static token audit checked 212 numeric and boundary tokens across the six files. All were present. Environment counts for every `table`, `tabular`, and `minipage` block balance. All six new labels are unique. `git diff --check` reports no whitespace errors.

A TeX engine is not installed in the current execution environment, so the standalone fragments were not rendered here. Their syntax follows the existing generated-table conventions and uses only packages already loaded by `rewrite/style/iyc-paper.sty` (`booktabs`, `float`, and standard tabular environments).

## 1. Configuration horse race

**Output:** `rewrite/generated/tables/v03_configuration_horse_race.tex`
**Source:** Table 7, PDF p. 47
**Label:** `tab:v03-configuration-horse-race`

### Cell-level checks

- Carry spot cluster: specification (2) `-13.45`, `t=-3.15`, `p=0.003`; specification (3) `-26.79`, `t=-4.88`, `p<0.001`.
- Carry total cluster: `-12.44`, `t=-2.86`, `p=0.012`; `-27.52`, `t=-4.92`, `p<0.001`.
- High-beta spot cluster: `-6.16`, `t=-1.72`, `p=0.102`; `-11.99`, `t=-2.02`, `p=0.040`.
- High-beta total cluster: `-5.66`, `t=-1.56`, `p=0.143`; `-12.37`, `t=-2.07`, `p=0.036`.
- Global-slope rows checked across all eight cells: `+0.21`, `+4.68`, `-0.64`, `+4.30`, `+2.40`, `+5.45`, `+2.40`, `+5.67`, with source `t`-statistics.
- One-month global-slope-change rows checked: `-14.97`, `-16.10`, `-15.14`, `-16.22`, `+11.87`, `+10.85`, `+11.41`, `+10.32`, with source `t`-statistics.
- U.S.-inversion rows checked across all eight joint specifications, including bootstrap `p`-values `0.465`, `0.605`, `0.581`, `0.696`, `0.450`, `0.667`, `0.308`, and `0.543`.
- Nine-own-state joint `p`-values checked: `0.005`, `<0.001`, `0.009`, and `0.004`.
- U.S.-inversion-alone footer checked: carry spot `-1.90 [0.484]`, carry total `-1.34 [0.637]`, high-beta spot `-3.01 [0.205]`, high-beta total `-2.03 [0.345]`.

### Interpretation check

The note says that source Table 7 does not display the nine own-state coefficients and that adding own states does not create a causal purification. No claim of a principal-component or comprehensive smooth-factor test is introduced.

## 2. Bilateral cluster and own-curve specifications

**Output:** `rewrite/generated/tables/v03_bilateral_own_curve.tex`
**Source:** Table 8, PDF p. 49
**Label:** `tab:v03-bilateral-own-curve`

### Row-level checks

All nine currencies and their own-state month counts were checked: AU 47, CA 40, CH 12, EU 25, GB 59, JP 22, NO 82, NZ 48, and SE 13.

For every currency, five coefficient cells were checked:

1. own state alone;
2. cluster alone;
3. cluster conditional on own state;
4. own state conditional on cluster;
5. full-specification cluster.

Each cell retains the source coefficient, Newey--West `t`, and state-specific wild-bootstrap `p`. The nine full-specification own-curve Wald `p`-values were checked in order: `0.408`, `0.801`, `0.115`, `0.488`, `0.486`, `0.006`, `0.233`, `0.373`, and `0.150`.

The pooled rows were checked: cluster-alone `-4.74 (t=-2.34)`; cluster with own state `-4.74 (t=-2.34)`; pooled own state `-0.01 (t=-0.01)`. The source does not display pooled bootstrap values or a pooled full-specification coefficient, so the transcription leaves those cells blank.

### Design-boundary check

The caption, source comment, and note all say explicitly that the cluster includes the focal country's curve. The table is not labeled or interpreted as leave-one-country-out evidence.

## 3. Reported rule neighborhood

**Output:** `rewrite/generated/tables/v03_reported_rule_neighborhood.tex`
**Sources:** Tables C.1--C.3, PDF p. 79; Table D.2, PDF p. 84
**Label:** `tab:v03-reported-rule-neighborhood`

### Panel A: breadth

All six active-month counts and all 24 coefficient/`p` pairs were checked:

- at least one: 180 months;
- exactly one: 88;
- at least two baseline: 92;
- exactly two: 48;
- at least three: 44;
- at least four: 22.

The sign change from exactly one (`+8.33 [0.005]` carry spot) to exactly two (`-15.72 [0.001]`) and the loss of the carry result at three/four were checked directly against the source crop.

### Panel B: release

All twelve coefficient/`p` pairs and counts were checked: one steepening month 39, baseline two-month confirmation 92, and three-month confirmation 191. In particular, one-month carry spot is `-12.14 [0.059]` and three-month carry spot is `-3.59 [0.161]`.

### Panel C: tenor and filter

All sixteen coefficient/`p` pairs and counts were checked. The unfiltered 10Y--3M row is carry spot `-4.68 [0.146]`, carry total `-4.02 [0.260]`, high-beta spot `-5.25 [0.011]`, and high-beta total `-5.00 [0.034]`. The source's `<0.001` for the filtered baseline high-beta spot row is preserved literally.

### Panel D: current-count repairs

All twenty coefficient/`p` pairs in source Table D.2 were checked. The reciprocal-age row is carry spot `-10.43 [0.040]`, carry total `-9.75 [0.057]`, high-beta spot `-14.87 [0.001]`, and high-beta total `-14.46 [0.002]`. The source does not display active-month counts in Table D.2; the transcription does not infer them.

The partially reported controlled estimates in the source footer were checked and retained in the note: raw count carry `-1.91 [0.576]` spot and `-0.63 [0.847]` total; reciprocal-age carry spot `-7.55 [0.084]` and high-beta spot `-13.82 [0.008]`; filtered current-count carry spot `-3.99 [0.269]` and high-beta spot `-7.04 [0.035]`.

### Multiplicity check

The caption calls this the **reported** neighborhood. The source comment and table note state that the source supplies per-rule inference only and no search-adjusted or family-wise inference. The table does not claim to enumerate the full specification search.

## 4. U.S. inclusion

**Output:** `rewrite/generated/tables/v03_us_inclusion.tex`
**Source:** Table F.1, PDF p. 88
**Label:** `tab:v03-us-inclusion`

All eight rows were checked at the coefficient, run-clustered `t`, and wild-`p` level:

- G10/baseline: spot `-12.85`, `-3.03`, `0.001`; total `-11.31`, `-2.40`, `0.003`.
- G10/add U.S. curve: spot `-11.72`, `-2.92`, `0.001`; total `-10.20`, `-2.34`, `0.006`.
- Dollar-inclusive/baseline: spot `-13.11`, `-2.69`, `<0.001`; total `-11.54`, `-2.15`, `0.009`.
- Dollar-inclusive/add U.S. curve: spot `-12.10`, `-2.68`, `0.001`; total `-10.57`, `-2.14`, `0.013`.

The 92 baseline months, 101 ten-curve months, complete 92-month overlap, and 31-percent dollar funding-leg share were checked. The note limits the inference to the non-load-bearing nature of U.S. exclusion; it does not declare the U.S. curve structurally irrelevant.

## 5. Beta benchmark

**Output:** `rewrite/generated/tables/v03_beta_benchmark.tex`
**Source:** Table G.1, PDF p. 89
**Label:** `tab:v03-beta-benchmark`

All 32 coefficient/`p` values were checked. The transcription restores both source panels rather than only the unfiltered signal:

- Maximal-sample S&P: signal spot/total `-7.93 [0.005]` and `-7.19 [0.009]`; filtered `-12.31 [0.001]` and `-11.97 [0.001]`.
- Maximal-sample MSCI: `-2.93 [0.319]`, `-4.00 [0.162]`; filtered `-2.30 [0.544]`, `-2.65 [0.446]`.
- Post-1999 S&P: `-11.10 [0.003]`, `-10.73 [0.004]`; filtered `-13.35 [0.001]`, `-13.09 [0.001]`.
- Post-1999 MSCI: `-7.67 [0.030]`, `-7.85 [0.019]`; filtered `-8.29 [0.014]`, `-8.67 [0.008]`.

The maximal-sample count of 443 and post-1999 count of 320 were checked. The note discloses that the maximal all-nine-beta sample excludes fifteen early months used by source Table 4 when seven or eight betas were available.

## 6. Common term-premium adjustment

**Output:** `rewrite/generated/tables/v03_term_premium.tex`
**Source:** Table K.1, PDF p. 94
**Label:** `tab:v03-term-premium`

All twenty coefficient/`p` pairs were checked. The source prints `0.000`, rather than `<0.001`, for both non-downcurve high-beta cells; the transcription preserves `0.000` exactly. Other boundary values are retained as displayed.

The source-text quantities in the note were also checked: baseline 92 months/15 runs; stripped state 125 months/18 runs; 83 shared months; 942 of 1,134 inversion curve-months remain after stripping. The note states that this is a fitted U.S.-proxy adjustment, not a foreign-country term-premium decomposition.

## File-integrity result

The new files are self-contained fragments and do not edit or input themselves into the current manuscript. No existing manuscript section, PDF, generated table, or appendix file was modified as part of this transcription task.

## Second-pass missed-content audit

A second page-by-page sweep of the longer source found no omitted exhibit that should displace the six transcribed tables. It did identify the following source-text facts that are economically material and were not fully itemized in the first recovery pass:

- **Breadth beyond two is mostly episode age, not a monotone dose response (pp. 15--16).** Months with at least three live curves have median episode age six months, versus three months for exactly-two months; eleven of fifteen episodes begin at exactly two. Conditional on being in the baseline state, a three-or-more indicator reportedly adds nothing (`p>=0.27`, with or without episode age). This is source prose referring to replication-package calculations, not a displayed table. It supports reporting exact-two as an onset/configuration contrast and rejects language implying that more inverted curves monotonically mean more return risk.
- **The alternative volatility benchmark contains an adverse beta null (p. 61).** Contemporaneous dollar and realized-FX-volatility controls leave carry spot at `-11.5 [0.002]` and high-beta spot at `-7.4 [0.009]`; stacking lagged NFCI/VIX gives `-12.0 [0.004]` and `-8.7 [0.011]`. But substituting G10 implied-volatility innovations leaves carry detectable (`p<=0.011`) while high-beta estimates retain their size and lose precision (`-7.7` and `-7.3`, `p=0.17--0.18`). Any mechanism table should preserve this adverse high-beta null rather than report only the favorable realized-volatility specification.
- **Control absorption differs for the crude count (p. 60).** NFCI level/change moves the raw current-count carry-spot `p` from `0.047` to `0.15`, while VIX alone leaves it at `0.015`; under all four controls the crude-count carry outcomes have `p>=0.58` and high-beta outcomes `p>=0.12`. This is useful evidence about stale-duration contamination, but it does not prove the live rule is uniquely correct.
- **Predetermined rankings are unusually persistent under the chosen inputs (pp. 72--74).** Australia or New Zealand occupies one of the top two G10 rate slots in 80 percent of months; both are in the top three in 64 percent. Under the S&P-based expanding beta, the smaller of the Australia/New Zealand betas exceeds the larger of the yen/franc betas in every month. These facts strengthen the standing-exposure interpretation, but the beta claim must remain paired with the full-sample MSCI failure in Table G.1.
- **The final return month uses rates whose coverage generally ends one month earlier (p. 72).** Seven of ten money-market-rate series end in 2026:01 and position the 2026:02 portfolio-return month; Australia, Canada, and Sweden continue further and are truncated. This is consistent with the stated formation timing, but v0.3's data appendix should say it explicitly so the 2026:02 endpoint is not mistaken for same-month rate coverage.
- **Pre-Lehman timing is suggestive, not a separate identification result (p. 60).** The source says the live state is active in seven of the fifteen months leading into September 2008, including July--September, while the U.S. curve is not inverted. This helps explain the U.S.-curve contrast but should not be used as a standalone event-study claim.

The sweep also reconfirmed two exclusions. The original count-sufficiency result relies on iid country errors and identical loadings (pp. 15--17 and 27), and the source's interpretation of the conditional Fama slope as an “independent estimate” of delayed compensation (pp. 21--22) is not supported by its episode-bootstrap interaction `p=0.340`. Neither should be restored as an established mechanism.
