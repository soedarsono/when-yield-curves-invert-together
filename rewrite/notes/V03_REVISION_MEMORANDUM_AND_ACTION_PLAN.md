# V0.3 revision memorandum and execution record

> **Historical execution record; superseded values are retained only as process evidence.** Any public 10-year-minus-3-month result below that reports `-6.58`, `45/64`, `108` active months, `20` episodes, raw `p=0.062`, or family value `0.562` predates the corrected delayed-entry, common-calendar, and equal-tie implementation. The final values are `-3.2016`, raw `p=0.3348`, maximum-$|z|$ reference `1.000`, `41/64` negative, rank `22/64`, `99` active months, and `18` episodes. See the final-release addendum.

Date: 2026-08-26
Edition: `Alt JMP v0.3`
Purpose: editorial judgment, empirical decision record, manuscript architecture, reproducibility standard, and release acceptance criteria

## Executive judgment

The right v0.3 uses Alt v0.2 as the architectural spine and the 94-page source paper as an evidence reservoir. It does not split the difference between the two drafts. Alt v0.2 solved the main problems of scope, tone, and claim discipline; the source paper contains several decisive exhibits that Alt v0.2 summarized too aggressively. V0.3 should recover those exhibits without reviving the source paper's structural overclaims, trading overlays, secondary asset classes, or post-hoc regime taxonomy.

The paper's one durable contribution is:

> The cross-country configuration of yield curves contains predictive information about currency spot losses that is not reproduced by the reported U.S.-curve, average-slope, or own-curve specifications, and the subsequent losses are ordered by predetermined currency exposure.

The paper can state the source-reported historical association confidently. It cannot claim that the core estimate has been independently reproduced, that the state identifies a primitive global shock, that the carry return is executable, that the original state survives a complete specification search, or that public proxy exercises validate the missing author state.

The main editorial insight from the full audit is unfavorable but useful: the exact carry coefficient is sensitive to tenor and release design, while the cross-country configuration and S&P-beta exposure ordering travel more consistently across the reported state perturbations. The beta interpretation is itself benchmark-sensitive over the full sample. V0.3 should make these asymmetries visible. A paper that reports where its strongest number weakens is more credible than one that calls a selected neighborhood uniformly robust.

## 1. What v0.3 should establish

### Tier 1: directly reported historical results

V0.3 may state these as source-reported results:

1. The month-end synchronized-inversion state precedes the next month's return.
2. In the reported 1988:01--2026:02 sample, the state is active for 92 months in fifteen contiguous episodes.
3. Annualized carry spot returns are 12.85 percentage points lower in active than inactive months; the corresponding money-market-differential total-return proxy is 11.31 points lower.
4. The distribution shifts beyond the five worst months: the monthly median and lower quantiles decline, and the outcome-conditioned bottom-decile deletion leaves a negative mean difference.
5. Exactly one live inversion and exactly two live inversions have opposite carry-return signs.
6. The cluster retains predictive content in the reported horse race with the U.S. inversion, the average G10 slope and its change, and the nine own live states.
7. Bilateral losses are larger for currencies with higher predetermined S&P 500 betas; the S&P-beta-sorted portfolio also loses in the state.
8. The U.S.-inclusive signal and dollar-inclusive portfolio produce similar source-reported return differences.

Every one of these statements must be labeled in the repository as source-reported and unreplicated because the original analytical panel and estimation code are absent.

### Tier 2: evidence supporting an interpretation

The following evidence supports a shared-information interpretation without identifying the shared shock:

- one live inversion is a different state, not simply a weaker version of two;
- the reported cluster is not spanned by the displayed average-slope, U.S.-curve, and own-state variables;
- the pooled bilateral cluster coefficient is negative while the pooled own-state coefficient is approximately zero;
- spot losses are ordered by a predetermined exposure measure;
- all seven emerging-market bilateral signs are negative even though those currencies do not construct the state;
- the independently sourced public 10Y--3M proxy has a broadly negative rule family and nine negative leave-one-currency-out estimates, although neither result supplies independent core-state inference.

Preferred phrases are “supports a shared-information interpretation,” “is consistent with,” and “adds information beyond the reported comparison.” Avoid “identifies a global shock,” “isolates disaster risk,” and “proves common rather than national risk.”

### Tier 3: candidate mechanisms

Global growth news, coordinated expected easing, common inflation news, term-premium shocks, intermediary constraints, slow portfolio adjustment, and time-varying disaster exposure remain candidate mechanisms. The reduced-form design does not select among them. The compensation benchmark may state why public predictability is economically interesting, but it must remain a benchmark, not a recovered friction.

## 2. Decisions forced by the source recovery

The following source objects materially improve v0.3 and should be reader-facing:

| Source exhibit | Recovery decision | Reason |
|---|---|---|
| Figure 1, source p. 5 | Main paper | Best compact timeline of returns, counts, state, and timing |
| Figure 2, source p. 18 | Online appendix or compact main use | Makes entry and release path dependence inspectable |
| Table 7, source p. 47 | Main paper | Direct configuration horse race |
| Table 8, source p. 49 | Main summary; full online | Closest available own-curve comparison; explicitly not leave-one-out |
| Tables C.1--C.3, source p. 79 | Main paper and full online | Reveals threshold, release, and tenor sensitivity |
| Table D.2, source p. 84 | Online, selected main discussion | Compares raw, age-weighted, and live-state constructions |
| Table F.1, source p. 88 | Online, selected main discussion | Shows exclusion of the U.S. and dollar is not load-bearing |
| Table G.1, source p. 89 | Main limitation and full online | Required adverse beta-benchmark result |
| Table K.1, source p. 94 | Main summary and full online | Required adverse carry/term-premium asymmetry |

The following material should not compete for the main-paper contribution:

- downcurve regimes and their trading overwrite;
- anti-carry and exit strategies;
- S&P 500 timing;
- conditional UIP reversal rhetoric;
- Sharpe ratios and cumulative trading overlays;
- oil-beta sorting without a displayed source table;
- emerging-market-native curve regimes;
- the public delivered-easing pair/triple screen.

Original Appendices F and G remain external to the reader-facing PDFs as requested. Numerical cells from their source tables may be natively transcribed into newly organized v0.3 evidence tables, with every transfer recorded in the external ledgers. No caption in the paper will say “inherited from the source PDF.”

## 3. Mathematical framework

The proposed common-plus-idiosyncratic framework is useful only after correcting its sign and identification problems. Define the country slope as

\[
q_{i,t}=\mu_i+f_t+u_{i,t},
\]

where a lower common component \(f_t\) tends to flatten curves. Inversion is the threshold event \(I_{i,t}=1\{q_{i,t}<0\}\). Several crossings can be more consistent with shared information than one crossing under restrictions on the cross-country distribution of \(u_{i,t}\), but those restrictions are not estimated and regional shocks may also synchronize curves.

Use a separate adverse return innovation:

\[
\Delta s_{i,t+1}=-\lambda_i h_{t+1}+e_{i,t+1}.
\]

The empirical interpretation is that the synchronized state may raise \(E[h_{t+1}\mid S_t=1]\). Do not equate the yield-slope factor \(f_t\) with the currency-return shock \(h_{t+1}\). Do not derive the two-country threshold from iid country shocks or identical loadings. The framework organizes tests; it is not a structural model and is not calibrated.

The framework yields four comparisons:

1. exactly one versus at least two live inversions;
2. the cluster versus smooth average-slope and U.S.-curve measures;
3. the cross-sectional return gradient in predetermined exposure;
4. a genuine leave-country-out signal predicting the excluded currency.

The source contains the first three. The fourth does not exist for the original 10Y--2Y state and remains a decisive missing test. Source Table 8 must never be relabeled as leave-one-country-out because its cluster includes the predicted country's curve.

## 4. What the reported neighborhood says

The displayed source neighborhood contains nine non-duplicated rules across breadth, release, and tenor. It is not the complete set of rules examined by the author and cannot support search-adjusted inference.

- Carry spot coefficients are negative for eight of nine displayed rules, but the positive exactly-one rule is economically important.
- The baseline carry coefficient is the second most negative displayed value, behind exactly two live inversions.
- Carry precision is concentrated near the two-month release rule and the 10Y--2Y tenor.
- Releasing after three increases dilutes the carry coefficient to -3.59 points; a 10Y--3M reconstruction attenuates it to -4.68 points.
- S&P-beta-sorted spot coefficients remain negative in seven of nine displayed rules and survive the 10Y--3M perturbation.
- Raw and reciprocal-age current-count repairs show that freshness contains information, but the path-dependent latch also uses historical timing that catches major delivery months.

The paper should therefore say that the cross-country nonlinearity is visible and that exposure ordering travels more consistently than the precise carry magnitude. It should not say that “most reasonable versions work” or call the displayed grid a full multiverse.

## 5. New independent public-data work

V0.3 adds a frozen, executable audit based on current-vintage OECD monthly yields distributed through FRED. The public slopes are 10-year government yields minus 3-month interbank rates. The outcome is a BIS policy-rate-ranked long-three/short-three currency spot basket. These inputs differ from the unavailable author 10Y--2Y end-of-month panel, money-market carry sort, and total-return proxy.

The declared family contains 64 combinations of:

- live versus raw inversion states;
- breadth thresholds of one through four;
- one-, two-, and three-month release rules for live states;
- one- and two-month return lags;
- long/short leg sizes of two and three.

The final baseline-like public rule yields a `-3.2016` percentage-point annualized policy-ranked log spot-return difference across `99` active months and `18` episodes. Its raw circular reference is `p=0.3348`; the finite common-calendar maximum-$|z|$ family reference is `1.000`. Forty-one of 64 rules are negative, none clears the 5-percent family threshold, and the baseline-like estimate ranks 22nd from most negative to most positive.

The same-universe checks are directional but not decisive. Excluding each currency from both the signal and outcome produces nine negative estimates, but the calendars and samples overlap heavily. A disjoint European-curve signal paired with the non-European basket gives `-15.84` points across ten episodes (raw rotation reference `0.062`), while the reverse split gives `-0.34` across nine episodes (reference `0.887`). Removing episodes containing September 1998, October 2008, or March 2020 attenuates the public baseline to `-0.46` points (complete-case rotation reference `0.826`); the outcome-conditioned deletion of the five worst active months changes it to `+0.94` and receives no p-value.

This is transparent adverse evidence. The nearby public family shares the source result's direction more often than not, but it does not validate the author state, produce family-adjusted rejection, or establish a symmetric shared-information channel. The complete public state, episode, recursion, specification, leave-one-out, disjoint, sensitivity, and manifest files belong in the reproducibility package.

## 6. Manuscript architecture

The intended main-paper structure is:

1. **Introduction.** State the cross-country-configuration problem, construction, three findings, source-reported status, and identification boundary.
2. **Economic framework, returns, and measurement.** Separate the slope signal from the adverse currency innovation; define spot, income, proxy total return, state recursion, data, timing, and predetermined beta.
3. **Empirical design.** Make fifteen episodes primary; distinguish headline inference from unavailable search adjustment; define the exposure and horse-race tests.
4. **The cross-country configuration.** Present headline conditional returns, distribution shift, exact-one/exact-two contrast, reported rule neighborhood, and Table 7 horse race.
5. **Where the losses fall.** Present rate and beta ordering, Table 8 without leave-one-out language, standing portfolio composition, and the full-sample MSCI failure.
6. **Alternative explanations and independent stress tests.** Present U.S. inclusion, risk controls, term-premium attenuation, calendar/influence evidence, EM breadth, and the public 10Y--3M audit.
7. **Why can a public state forecast poor carry returns?** Keep the compensation benchmark short and explicit about non-identification.
8. **Conclusion.** State one result, one interpretation, and the decisive missing validation step; no self-assessment.

The online appendix should attach:

- exact signal algorithm and edge cases;
- accounting and compensation derivations;
- full source-reported robustness and adverse results;
- the independent public 10Y--3M audit and episode ledger summary;
- the downstream delivered-easing mechanism checks;
- the exploratory country-combination screen, clearly separated from core evidence.

## 7. Figure and table discipline

The main paper should use exhibits only when each performs a distinct inferential job.

### Main figures

1. Source-reported full-sample signal and carry-return overview.
2. Source-reported rule neighborhood, ordered by active months rather than coefficient.
3. Source-reported bilateral loss against predetermined S&P beta.

The public 64-rule curve belongs in the online appendix because it measures a different state and outcome. The original live-state construction example also fits naturally online once the main algorithm is clear in text.

### Main tables

1. Notation, timing, and state summary.
2. Headline carry and beta-sorted returns.
3. Reported state-definition neighborhood.
4. Synchronization versus reported nearby curve states.
5. Exposure ordering and own-curve comparison.
6. Alternative explanations and adverse robustness.

Large source tables should be transcribed natively, not inserted as screenshots. Main tables may select decisive cells; the online appendix must carry the complete transcription and provenance note.

## 8. Writing rules

Use the sequence **result → comparison → interpretation → boundary**. A qualification appears once where it changes interpretation and once in the consolidated design boundary; do not qualify every sentence.

Prefer:

- “shared across currencies” for the statistical component;
- “common international conditions” for the interpretation;
- “source-reported historical association” for the unavailable core estimates;
- “money-market-differential return proxy” for total carry;
- “reported state-definition neighborhood” for Tables C.1--C.3 and D.2;
- “independent public proxy audit” for the executable 10Y--3M work.

Avoid:

- systemic crash risk, disaster probability, causal shock, or structural beta;
- “replicated,” “reproduced,” or “verified” for source-PDF estimates;
- “leave-one-country-out” for source Table 8;
- “external validation” for EM observations sharing the same dates;
- “conventional confirmation” for the two-month release rule;
- “inherited from source PDF” anywhere in the reader-facing paper;
- self-assessment in the conclusion;
- statements that a null or adverse robustness result is merely due to low power.

## 9. Reproducibility standard

Every empirical object must fall into one of five classes:

| Class | Meaning |
|---|---|
| Source-reported | Visible in the source paper but not regenerated |
| Derived from source-reported | Transparent arithmetic on visible source cells |
| Independently generated public check | Executed from declared public inputs |
| Editorial interpretation | A claim organizing evidence without adding an estimate |
| Missing decisive test | Impossible with the present repository |

For each public download, the data-purpose ledger must record provider, series, exact hypothesis, interaction with other files, merge key, timing, target output, keep rule, limitations, and redistribution status. Raw data remain untracked; hashes, manifests, code, and result tables are tracked.

The release must include:

- main, online appendix, and combined PDFs;
- page counts and SHA-256 hashes;
- the v0.3 revision memorandum;
- claim, equation, copied-material, figure, transformation, and data-purpose ledgers;
- source and output manifests;
- deterministic tests;
- public-proxy episode and recursion audits;
- environment and rebuild instructions;
- a clean repository status at the release commit;
- a v0.3 tag and pushed remote commit if repository permissions permit.

## 10. Redundancy-removal hierarchy

V0.3 removes redundancy in four tiers.

### Tier 1: exact repetition

Delete repeated definitions, repeated headline numbers, duplicate caveats, and captions that restate the surrounding paragraph. The abstract, introduction, results, and conclusion may each state the headline once for different purposes, but no section should mechanically repeat the full set of numbers.

### Tier 2: duplicate empirical roles

If two exhibits answer the same question, retain the more transparent one. Use the reported-neighborhood plot rather than three main appendix grids; use the horse race rather than separate prose paragraphs on every comparator; use one exposure table plus the scatter rather than multiple beta narratives.

### Tier 3: secondary branches

Move conditional UIP, downcurve, local projections, public delivered easing, and country combinations online. These results may illuminate boundaries but do not establish the cross-country-configuration contribution.

### Tier 4: contribution-diverting material

Remove trading overlays, Sharpe-ratio optimization, equity timing, anti-carry strategies, strong disaster language, and structural delayed-compensation claims from both reader-facing PDFs when they cannot be supported by executable returns or identification.

The goal is not a short paper for its own sake. The goal is one inferential role per paragraph and one distinct question per exhibit.

## 11. Acceptance rubric and honest ceiling

The hostile audit scores the pre-v0.3 package at 72/100. With the absent original panel, an honest empirical ceiling is approximately 82/100. Editorial polish, public code, and source discipline cannot substitute for missing core-state regeneration.

The package can approach the no-panel ceiling if it:

- makes source status visible and internally consistent;
- restores the adverse robustness and configuration horse race;
- shows the reported rule neighborhood without calling it complete;
- incorporates the public 64-rule audit without calling it validation;
- removes all incorrect leave-one-out language;
- keeps spot and total-return-proxy claims distinct;
- treats fifteen episodes as the effective common-state variation;
- attaches a self-contained online appendix;
- reconciles every ledger and release hash;
- passes all tests and page-level visual checks.

A genuine 90+ empirical package still requires:

1. the original panel and code, with exact state and estimate regeneration;
2. a complete declared 10Y--2Y specification family with joint search-adjusted inference;
3. the fifteen-row original episode ledger, event-time paths, phase decomposition, and joint episode deletions;
4. true original-state leave-one-country-out and disjoint tests;
5. executable forward returns and implementation costs if total carry is central;
6. a genuinely unused or prospective validation sample;
7. an immutable, rights-audited archival release.

The release should report both scores: the achieved editorial/reproducibility score after final audit and the empirical-design ceiling imposed by missing inputs. It should never rename an 82 as a 90.

## 12. Final release decision rule

Release v0.3 only if all of the following are true:

- the abstract, introduction, tables, and conclusion describe the same estimand and claim tier;
- every source number resolves to a source page/table and every public number resolves to executable output;
- adverse 10Y--3M, MSCI, and U.S.-term-premium results are visible;
- the public yield audit is described as a nearby proxy with no maximum-$|z|$ family crossing;
- the paper contains no false leave-one-out, replication, causal, disaster, or executable-return claim;
- the main paper and online appendix are visually clean page by page;
- references remain within the original 84-entry universe;
- all deterministic tests and PDF preflight checks pass;
- transformation and copied-material ledgers map every moved, condensed, omitted, or transcribed object;
- the release files, manifest, commit, and remote state agree.

If one of these conditions fails, fix it before tagging. If the missing author panel prevents a requested empirical claim, omit or narrow the claim rather than filling the gap with prose.

## Final-release addendum: public-proxy interpretation

The final executable public audit reports a baseline association of `-3.2016` annualized percentage points (raw circular reference `p=0.3348`) over `99` active months and `18` episodes. Its finite common-calendar maximum-$|z|$ reference is `1.000`; `41/64` related rules are negative and the baseline ranks `22/64`. Crisis-episode deletion gives `-0.46` (`p=0.826`), and deleting the five worst active months gives `+0.94` without a p-value because the diagnostic is outcome-conditioned. The public evidence therefore documents measurement sensitivity and concentration. It does not validate the missing original state.
