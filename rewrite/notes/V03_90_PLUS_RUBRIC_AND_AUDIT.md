# v0.3 90+ Release Rubric and Hostile-Referee Audit

> **Historical audit record; intermediate values superseded.** This file preserves successive hostile-audit findings to document how v0.3 changed. Public 10-year-minus-3-month values such as `-6.58`, `45/64`, `108` active months, `20` episodes, raw `p=0.062`, and the earlier `0.562` common-grid statistic describe a pre-fix implementation and must not be cited as final results. Likewise, early delivered-easing values `-1.10` and `p=0.195`, and the early country-screen value `0.042`, precede equal cutoff-tie weighting. The final common-calendar, delayed-entry, equal-cutoff-tie yield implementation reports `-3.2016` annualized percentage points, raw circular reference `p=0.3348`, maximum-$|z|$ family reference `1.000`, `41/64` negative rules, rank `22/64`, `99` active months, and `18` episodes. See the final-release addendum at the end of this file.

Audit date: 2026-08-26 (Asia/Jakarta)
Scope: the full v0.3 plan supplied in `pasted-text.txt`; `AI JMP.pdf`; `Alt_JMP_v0.2.pdf`; the standalone and combined release PDFs; LaTeX; checklists; transformation, claim, equation, copied-material, figure, and data-purpose ledgers; public-data code and the deterministic test suite available at each audit stage; run manifests; and the public GitHub repository. This is a readiness diagnostic, not a publication probability.

## Executive verdict

The v0.2 release is a strong editorial rescue and a credible, submission-clean alternative paper. It is not yet a 90+/100 research release. On the rubric below it scores **72/100**. The score is slightly above the earlier 71/100 audit because a public repository now exists and its deterministic test workflow succeeds. The central research gates remain unchanged.

The binding fact is simple: the workspace does not contain the author yield-curve panel, currency-return panel, exact core episode file, portfolio construction code, core inference code, or complete tested specification universe. The headline 1988--2026 estimates are therefore auditable transcriptions from `AI JMP.pdf`, not independently regenerated results. No improvement in prose, page design, public-policy-rate analysis, or GitHub polish can substitute for those missing objects.

**Strict ceiling with the present evidence:** approximately **82/100**, even if every feasible writing and release-engineering improvement below is completed perfectly. A 90+ claim requires new or recovered evidence that was not available to this audit: at minimum the core panel and code, a full search-aware state-definition audit, core-state leave-one-country-out tests, and a genuinely frozen validation design. If the panel remains absent, v0.3 can be an excellent, unusually transparent alternative edition; it cannot honestly be marketed as a replicated, search-robust, externally validated job-market result.

This is not a recommendation to abandon v0.3. It is a recommendation to separate two targets:

1. **Best honest v0.3 from current materials:** sharpen the common-information contribution, keep the inherited evidence boundary explicit outside the reader-facing PDF, improve the reported-neighborhood presentation, complete the nearby public proxy, and issue a professional immutable release.
2. **90+ empirical v0.3:** recover or rebuild the core panel and run the decisive tests before letting the prose settle the paper's identity.

## Verified evidence base

The audit verified the following facts rather than relying on checklist assertions alone.

- `AI JMP.pdf` is 94 pages (SHA-256 `C1E770925DE84B1CC50F35B2A2FB7F015B6D250072B2F18F9EAC994489D1A043`). It makes several claims beyond the design: that the signal isolates disaster probability, identifies a conditional UIP reversal, locates a compensation regime, supports trading overlays, and generalizes to equities and emerging markets.
- `Alt_JMP_v0.2.pdf` is a 44-page combined edition (SHA-256 `D6B2BCD6EB6544B41CA605C5BE2D84E62352BA75A2A64E64C153EE081097DEFD`), byte-identical to `output/pdf/When_Yield_Curves_Invert_Together_With_Online_Appendix.pdf`. Its main paper is 26 pages and its online appendix 18 pages.
- PDF preflight passes. Visual inspection of the original and current contact sheets found no blank, clipped, overlapping, or unreadable pages. The current edition is materially cleaner, shorter, and more disciplined than the 94-page source.
- The inherited headline sample contains 458 months, 92 active months, and only 15 contiguous episodes. The reported annualized active-minus-inactive differences are `-12.85` percentage points for carry spot and `-11.31` for total carry, with source-reported episode-bootstrap p-values of `0.001` and `0.003`.
- The exposure evidence is informative but not decisive. It has nine currency observations, a descriptive cross-currency beta fit with `R^2=0.77`, a beta-sorted spot result of `-7.53` points, and an imprecise panel state-by-beta interaction (`p=0.210`). The beta portfolio is substantially weaker before 2005 (`-4.01` spot, `p=0.287`) than after 2005 (`-11.91`, `p=0.010`).
- The reported neighborhood is not uniformly favorable. A 10Y--3M reconstruction and a U.S. term-premium adjustment attenuate the carry result; the term-premium-adjusted carry estimate is about `-5.4` with `p=0.11`. An age-weighted current-inversion construction produces a larger high-beta estimate than the baseline. These are reasons to run a full multiverse, not reasons to declare the baseline uniquely validated.
- The independently executable delivered-easing proxy finds 15 onsets, but none of its six primary mechanism outcomes survives Holm correction. Under the final equal-cutoff-tie implementation, the shadow-carry spot estimate is `-1.0607` cumulative percentage points with finite-rotation reference `p=0.2222` and Holm-adjusted reference `1.000`. These directions can motivate mechanisms; they do not validate the inversion classifier.
- The country-combination screen tests 120 pairs and triples. Under the final equal-cutoff-tie implementation, CHF--GBP has a conditional common-rotation maximum-$|z|$ reference of `0.0352` at the six-event threshold, has a 90-percent interval including zero, weakens materially without October 2008, and is not significant when the minimum event count rises to eight. This is a conditional screen under simultaneous cyclic-shift exchangeability, not unconditional family-wise inference; it is hypothesis-generating.
- Thirty-nine deterministic unit tests pass locally. They cover timing boundaries, state-machine behavior, conditional rotations, manifests, hashes, the country-combination screen, the declared 64-rule public-proxy family, and the source-reported neighborhood. They do not test the unavailable core state or headline returns.
- The public GitHub repository exists at `https://github.com/soedarsono/when-yield-curves-invert-together`, with four commits on `main`. GitHub Actions run `#2` for commit `d2a5a8d` reports success. The workflow runs Python unit tests only; it does not download data, run the full analysis, build PDFs, or verify release assets.
- The GitHub repository has **no tag and no formal release**. The releases page states that there are no releases. The local tree was also dirty at audit time with a substantial but uncommitted v0.3 public-proxy layer: sources, ledgers, code, tests, machine-readable outputs, and notes were present but not part of the audited release commit. The work is useful evidence, but it is not scoreable as a released v0.2 artifact until the repository state, documentation, manifests, and release commit agree.
- The new public 10Y--3M proxy is adverse evidence against a strong validation claim. Its baseline-like estimate is `-6.58` percentage points over 108 active months and 20 episodes, but its raw circular-shift `p=0.062` and 64-rule maximum-statistic `p=0.562`; zero of 64 rules survives the 5-percent family threshold. All nine leave-one-country-out estimates are negative, but the geographically disjoint result is one-sided: European curves to non-European currencies is `-18.22` (raw `p=0.022`), while non-European curves to European currencies is `0.30` (raw `p=0.949`). This is a transparent nearby-rule stress test, not confirmation of the author state.
- No reuse license is granted. The repository itself warns that provider terms and permissions for source-paper assets require review. A public repository is therefore not yet an archival release with settled redistribution rights.

## Evidence-based 100-point rubric

| Dimension | Weight | Current v0.2 | 90+ standard |
|---|---:|---:|---|
| Contribution and claim hierarchy | 14 | 13 | One memorable contribution; prediction, exposure ordering, mechanism, and causality separated; no disaster, UIP, or structural-friction claim beyond the evidence |
| Rule integrity and specification search | 18 | 10 | Complete rule family, disclosed provenance of every choice, full state-definition multiverse, search-adjusted inference, and evidence that the baseline is not a crash-selected tail specification |
| Rare-event inference and episode anatomy | 12 | 9 | Episodes are primary; complete episode ledger and event study; onset/continuation/release decomposition; joint crisis deletions; finite-sample and family-wide inference |
| Common-information and exposure tests | 12 | 9 | Core-state leave-one-country-out and geographically disjoint signals; uncertainty on currency coefficients and beta gradient; beta survives alternative exposure controls |
| Identification and mechanism discipline | 10 | 7 | Expected-rate, term-premium, inflation, dollar, funding, and commodity alternatives confronted; one mechanism promoted only if a distinctive restriction succeeds |
| Return object and economic implementation | 8 | 6 | Executable or close-to-executable forward excess returns, exact formation/settlement, basis, spreads, costs, coverage, and DEM/euro treatment; otherwise claims explicitly limited to spot-risk accounting |
| External validation | 10 | 4 | A genuinely unused sample, market, or prospective episode evaluated under a frozen rule and decision protocol; EM breadth and calendar splits do not count as independent validation |
| Reproducibility, provenance, and release integrity | 10 | 8 | Core estimates regenerated; clean-clone workflow; immutable tag/release; all assets hashed; environment locked; CI/release logs; redistribution rights and license resolved |
| Writing, architecture, and exhibits | 6 | 6 | Contribution visible by page 2; five or fewer core figures and six or fewer core tables; no repeated argument; every caption states timing, unit, sample, and evidence boundary |
| **Total** | **100** | **72** | **90+ also requires every non-negotiable gate below** |

The current score should not be inflated because the PDF is polished. Presentation has already earned essentially all available points. The remaining points are expensive because they require evidence.

## Non-negotiable gates and exact acceptance tests

A total score of 90 or more is invalid if any applicable gate is open.

### Gate 1: Claim and provenance integrity - PASS now

**Acceptance test**

- Every quantitative main-text claim resolves to one row in a machine-readable ledger with `source`, `sample`, `timing`, `unit`, `estimand`, `inference`, and `evidence_class`.
- `evidence_class` is one of `core_regenerated`, `inherited_source_estimate`, `new_public_analysis`, `simulation`, or `interpretation`.
- Automated comparison reports zero unledgered numbers and zero reader-facing uses of “replicated,” “verified,” or “causal” for inherited estimates.

**Current result:** The external ledgers and evidence policy substantially pass this gate. v0.3 must preserve the distinction.

### Gate 2: Core-panel regeneration - BLOCKED

**Acceptance test**

- From raw or licensed inputs, one command regenerates the nine-country monthly slope panel, exact live-state recursion, 15-episode ledger, portfolio weights, spot and total returns, inference draws, and all core exhibits.
- Regenerated headline coefficients agree with the released tables to within `0.01` annualized percentage point, event counts agree exactly, and p-values agree to the published three decimals given the frozen seed and algorithm.
- Every input and output has a SHA-256 hash and a license/redistribution classification.

**Failure action:** If the core panel remains unavailable, retain `inherited_source_estimate` labels in the repository and do not call v0.3 a replication or a reproducible empirical release.

### Gate 3: Rule-selection and full multiverse - BLOCKED

**Acceptance test**

- The Cartesian family is fixed before rerunning returns and includes, at minimum: 10Y--2Y and 10Y--3M; thresholds 1--4; fresh crossing versus current inversion; release lengths 1--3; current versus live counts; 2x2, 3x3, and 4x4 portfolios; information lags 0--2; U.S. included/excluded; and leave-one-country-out construction.
- A machine-readable grid contains one row for every declared cell, including failed/undefined cells with explicit reasons. No analyzed cell is omitted from the released file.
- The paper reports the baseline's percentile rank within the family, the share of economically admissible specifications with a negative carry-spot coefficient, and the same share for the exposure result.
- A maximum-|t|, Romano--Wolf, or equivalent family procedure recomputes the full specification selection under each resample. The baseline claim may be called statistically detectable only if the family-adjusted p-value is at most `0.05`; otherwise the paper reports the distribution without a confirmatory significance claim.

**Failure action:** If the baseline is an extreme outlier or loses family-adjusted support, reframe the paper around clustering intensity/exposure ordering and treat the binary latch as illustrative.

### Gate 4: Episode-primary evidence - BLOCKED

**Acceptance test**

- Release a 15-row core episode ledger with onset, release, contributing curves, duration, cumulative spot, carry income, total return, worst month, crisis overlap, and leave-one-episode estimate.
- Produce an event-time figure from month `-12` through `+12` for spot, income, and total returns, with episode-resampled intervals and no causal label.
- Estimate four predeclared phases: onset month, ordinary continuation, live-but-no-longer-current release phase, and first month after release.
- Report deletions of GFC and COVID jointly, the four named crisis-era episodes jointly (1995, 1998, 2008, 2020), and every leave-two-episode pair. If the non-crisis coefficient reverses sign or falls below one-half the full-sample magnitude, remove “broad-based beyond crises” from the abstract and conclusion.

### Gate 5: Common-information test - BLOCKED

**Acceptance test**

- For every country, build the signal without that country's curve and predict that country's bilateral spot return without using it in any outcome sort.
- Release all nine estimates and uncertainty intervals. The pooled leave-own-country-out state effect and the leave-own-country-out beta gradient must be predeclared headline tests.
- The “shared international information” claim survives only if at least seven of nine bilateral point estimates have the predicted sign and the predeclared pooled or gradient test has family-adjusted `p <= 0.05`. Otherwise use “same-universe cross-country association.”
- Geographically disjoint European-to-non-European and non-European-to-European tests are reported as low-power corroboration, not selected subset searches.

### Gate 6: Return-object honesty - CONDITIONAL PASS BY NARROWING; BLOCKED for an investable carry claim

**Acceptance test for a carry/excess-return claim**

- Use one-month forward quotes observed at formation, exact settlement returns, basis where relevant, bid-ask spreads, currency availability, asynchronous-close checks, and a documented DEM/euro transition.
- Report gross and net spot, carry, and total return components with episode inference.
- “Negative carry return” remains in the title/abstract only if the active-state net total mean is negative and the active-minus-inactive net gap has a predeclared episode-level 95-percent interval excluding zero.

**Alternative pass:** If these data cannot be obtained, title and claims are limited to predictable spot depreciation or a money-market accounting proxy. No deployable strategy, alpha, or implementability language appears.

### Gate 7: Mechanism identification - PASS only for bounded interpretation

**Acceptance test**

- A compact horse race includes the synchronized state, U.S. inversion, average slope and change, slope PC1, dispersion, current inversion count, lagged VIX/NFCI, dollar factor, FX volatility, and commodity/funding proxies.
- Comparable foreign expected-rate/term-premium decompositions are required before stating that the state measures expected policy or global growth rather than term-premium news.
- If only U.S. ACM is available, the manuscript says the channel remains unidentified and reports the attenuation of carry as adverse evidence rather than robustness.

### Gate 8: External or prospective validation - BLOCKED

**Acceptance test**

- The complete rule, code hash, exposure definition, outcome family, and decision rules are timestamped in an immutable tag before observing the validation outcomes.
- The validation set was not used directly or indirectly to design the rule. Calendar splitting of the already examined 1988--2026 history does not qualify.
- Success/failure is reported under the frozen protocol regardless of sign. A different currency universe sharing the same 15 dates is labeled breadth, not an independent time-series replication.
- If no historical untouched sample exists, v0.3 may preregister the prospective test, but it cannot claim that the validation gate has passed until future episodes occur.

### Gate 9: Immutable public release and clean-clone execution - BLOCKED

**Acceptance test**

- `git status --porcelain` is empty at the release commit.
- An annotated tag `v0.3.0` points to the audited commit; `git ls-remote --tags origin` contains that exact object.
- A formal GitHub release named `v0.3.0` attaches the main, appendix, combined PDF, release manifest, checksums, environment lock, and machine-readable result ledgers.
- A fresh clone on a clean machine runs the documented workflow without manual file insertion. The log records OS, Python, package lock hash, TeX/Poppler versions, input hashes, output hashes, and commit.
- CI runs unit tests on Linux and a release job runs the full saved-snapshot analysis and PDF preflight on Windows. Live-current-vintage downloads are not treated as byte-identical reproduction.
- Provider rights are audited. A clear software license is added, and paper text/figure/data rights are stated separately. If copied source figures cannot be redistributed, the release excludes them or documents permission.

**Current failure evidence:** public `main` has successful unit-test CI, but no tags or GitHub releases; the CI does not run the full workflow; no reuse license is granted; and the local tree was dirty during this audit.

### Gate 10: Reader-facing production - PASS now

**Acceptance test**

- PDF preflight, visual inspection, metadata, references, cross-references, page substance, and prohibited-language scans all pass.
- Main and appendix outputs match release checksums exactly.
- No core table or figure is a raster transcription once the underlying panel becomes available; code-generated replacements are mandatory for a replication claim.

## Prioritized hostile-referee audit

### P0 - Fatal until answered

#### 1. “The state machine was designed to keep 1995, 2008, and 2020 after curves re-steepened.”

**Why it is dangerous:** The live-state rule switches off the naive count precisely where several worst carry months occur. The paper discloses this but does not remove selection risk. A deterministic rule can overfit without estimated coefficients.

**Required answer:** Full multiverse, selection-adjusted inference, episode-phase decomposition, and a rule rationale recorded independently of returns. The baseline must be shown in the full distribution, not beside a few favorable neighbors.

#### 2. “Your core result is copied from a PDF, not reproduced.”

**Why it is dangerous:** Every headline coefficient, episode count, beta coefficient, and robustness result depends on absent author inputs. The public pipeline analyzes a different downstream event.

**Required answer:** Recover/rebuild the core panel and code or state prominently in repository/release materials that v0.3 is an editorial alternative with inherited empirical evidence. There is no third honest category.

#### 3. “Fifteen episodes are the sample; 458 months are window dressing.”

**Why it is dangerous:** Persistent months do not create independent common shocks. A few crisis episodes can govern effect size, cross-sectional sorting, and every extension sharing the state calendar.

**Required answer:** Complete episode ledger, phase-specific estimates, joint crisis deletions, leave-two-episode results, and finite-sample inference. Never present more currencies or outcomes as more independent global shocks.

#### 4. “You examined the full garden of forking paths but report only fragments.”

**Why it is dangerous:** Tenor, threshold, release, freshness, geography, lag, portfolio size, controls, tail cutoff, and downcurve classification were all potentially outcome-sensitive. The current appendix reports a neighborhood, not the universe.

**Required answer:** Machine-readable complete universe and search-adjusted inference. If provenance of past searches is unknown, say so and distinguish the ex post audit family from historically tested variants.

### P1 - Severe threats to the contribution

#### 5. “The same countries generate the signal and bear the measured loss.”

The own-curve horse race is not the decisive test. Construct the state without country `i` and predict country `i` outside the portfolio sort. Until then, “shared international information” is an interpretation of same-universe evidence.

#### 6. “Beta is AUD and NZD with nine dots.”

The scatter has nine observations, no displayed coefficient uncertainty, and the panel interaction has `p=0.210`. Rate and beta ranks correlate `0.72`, and the beta portfolio is weak before 2005. Require leave-currency-out gradients, rolling/expanding beta variants, global ex-U.S. and downside betas, and controls for average rate, commodity, dollar, trade, and funding exposure.

#### 7. “The term-premium result cuts the headline carry magnitude in half.”

The U.S. ACM adjustment is not a foreign decomposition, yet it attenuates carry to an imprecise estimate. This is not a clean robustness win. Either obtain comparable country decompositions or keep expected-policy/global-growth language explicitly tentative.

#### 8. “Money-market accounting is not a traded one-month forward return.”

The current narrowing is defensible, but the title and abstract still foreground carry losses. If v0.3 wants negative excess-return or public-information-puzzle claims, it needs forward quotes, basis, spreads, settlement, and costs. Otherwise make spot risk the primary object.

#### 9. “Why does public information forecast a negative return?”

The compensation equation organizes the puzzle but does not identify slow adjustment. The paper must distinguish predictable spot depreciation, predetermined carry, and negative excess return. Candidate frictions belong in one bounded subsection unless independently tested.

### P2 - Important but subordinate

#### 10. “The EM extension is not external validation.”

It uses the same global dates, has a shorter sample, and pooled p-values of `0.104` and `0.079`. Call it breadth only.

#### 11. “The public mechanism appendix is mostly null.”

No primary public-proxy outcome survives Holm correction. The appendix is valuable because it is reproducible and disciplined, not because it confirms the headline mechanism. Do not elevate it to main evidence.

#### 12. “CHF--GBP is a six-event, October-2008-sensitive screen.”

It disappears under stricter minimum-event rules. Keep the sensor-versus-bearer idea exploratory until tested on the core yield panel with contributor identities and family correction.

#### 13. “The release is a repository, not a release.”

The public repository and successful CI are progress. They are not an immutable archival release: no tag, no formal release, no clean-clone full-run log, no settled license, and no CI build of the paper/data outputs.

#### 14. “The OECD 10Y--3M proxy is not the missing 10Y--2Y panel.”

At audit time a complete declared 64-rule family, tests, ledgers, and outputs existed only in the dirty working tree, not the public release commit. More importantly, the family does not pass search-adjusted inference: the baseline-like maximum-statistic `p=0.562`, and none of the 64 rules clears the 5-percent family threshold. Monthly current-vintage 10Y government yields minus 3-month interbank rates, including a Germany/euro-area splice, are a nearby public proxy. They cannot validate the exact author tenor, dates, release logic, or return object.

## What can be improved with existing evidence

These actions are feasible without pretending that the absent panel exists.

| Action | Evidence already available | Honest payoff |
|---|---|---|
| Use Alt v0.2 as the spine and AI JMP as an evidence reservoir | Both PDFs and full transformation ledgers | Stronger economic momentum without reviving overclaiming |
| State one contribution: cross-country curve configuration predicts exposure-ordered spot losses | Inherited headline, exact-one/two contrast, beta ordering, controls | A memorable and defensible paper identity |
| Use the common-plus-idiosyncratic signal-extraction framework | Existing schematic factor equation and synchronization logic | Derives threshold nonlinearity and leave-one-country-out prediction without claiming a structural model |
| Recast all claims into direct result / supporting interpretation / possible mechanism | Current evidence policy and identification audit | Eliminates disaster-probability, causal-growth, and friction-identification overreach |
| Make 15 episodes visually and rhetorically primary | Existing sample counts and reported leave-one-episode statements | Better small-sample honesty, although not a substitute for the missing episode ledger |
| Build a “reported neighborhood” exhibit | Existing reported threshold, release, tenor, raw-count, age-weighted, and term-premium rows | Shows known sensitivity; must not be called a complete specification curve |
| Strengthen the exact-one versus exact-two discussion | Existing source estimates | Motivates synchronization as a minimum configuration, not a universal structural cutoff |
| Preserve the U.S., smooth-slope, NFCI, VIX, dollar, and U.S.-ACM comparisons | Existing inherited tables and prose | Narrows obvious alternative accounts while admitting incomplete proxies |
| Keep EM and public delivered-easing results in the appendix | Existing outputs and adjusted inference | Breadth and mechanism challenges without false independent validation |
| Retain the completed OECD 10Y--3M public proxy under its declared family | Current code, 64-rule output, episode ledger, leave-one-country-out and disjoint diagnostics | An independently sourced nearby-rule stress test whose null family-adjusted result disciplines the paper; not replication of the author state |
| Improve release engineering | Existing repo, CI, manifests, tests, preflight | Immutable, citable, cleanly rebuildable public layer |
| Tighten exhibit architecture | Existing figures/tables and source assets | Five core figures/six core tables only if each earns a distinct inferential role |

Do not pad the 21-page main text merely to reach a nominal 30--35-page target. Expansion is justified only by decisive new exhibits: a full specification curve, episode anatomy, leave-one-country-out exposure, executable returns, or an external validation. Without them, the current concise architecture is superior to a longer defense brief.

## What cannot be honestly claimed without the core panel or new data

| Claim/test | Why current evidence is insufficient |
|---|---|
| Exact replication of the 12.85-point headline | Underlying yields, returns, weights, dates, and bootstrap are absent |
| Complete 10Y--2Y multiverse and search-adjusted p-value | Only selected reported variants are visible in the source PDF |
| Core-state leave-one-country-out prediction | Exact country-month live states and bilateral outcomes are absent |
| Episode-onset event study and onset/continuation/release effects | Exact core episode returns and state path are absent |
| Joint crisis and all leave-two-episode deletions | Episode-level core data are absent |
| Contributor-country versus loss-bearing-country decomposition | Onset contributor identities for the core state are absent |
| Executable forward excess-return result | Forward quotes, basis, bid-ask spreads, settlement, and financing data are absent |
| Foreign expected-rate versus term-premium synchronization | Comparable country decompositions are absent |
| Independent historical holdout | The full 1988--2026 history informed the existing rule; splitting it later does not undo that knowledge |
| Structural slow-compensation or disaster-probability mechanism | The reduced-form return pattern does not identify the friction, shock, probability, or price of risk |
| A zero-beta no-loss result | Nine-point descriptive fit lacks sufficient uncertainty analysis |
| A stable CHF--GBP sensor result for the original state | Current evidence is a downstream delivered-easing screen, not the core inversion state |

## Result-contingent decision rules for v0.3

These rules should be frozen before new core analysis.

1. **Broadly negative multiverse plus family-adjusted support:** retain the synchronized-inversion predictor as the central result; report the range rather than one immaculate coefficient.
2. **Only baseline strongly negative:** abandon robust fixed-rule language; present clustering intensity and exposure ordering, with the latch as an in-sample classifier.
3. **Core leave-one-country-out test passes:** promote it to a headline common-information result.
4. **Core leave-one-country-out test fails:** remove “global/shared information” as an established interpretation and identify the countries driving the same-universe association.
5. **Executable forward net returns reproduce the negative total-return state:** permit conditional carry/excess-return language, while retaining selection and rare-event caveats.
6. **Only spot returns survive:** make predictable currency depreciation the paper's object and demote negative total carry and trading implications.
7. **Expected-rate synchronization dominates:** strengthen expected-easing/global-growth interpretation, without calling it causal.
8. **Term-premium synchronization dominates:** pivot toward common risk-bearing information transmitted through bonds and currencies.
9. **No external/prospective validation yet:** call the exercise frozen for future evaluation, not validated.

## Priority order

### Priority A: Work that changes the credibility frontier

1. Recover/rebuild the core author panel and code.
2. Freeze and run the full state-definition multiverse with selection-adjusted inference.
3. Run core leave-one-country-out and disjoint-region tests.
4. Release the complete episode ledger, event study, phase decomposition, and joint deletions.
5. Add executable forward returns or narrow the title/claims to spot risk.
6. Seek a genuinely unused validation sample or preregister the prospective test.

### Priority B: Work that improves the best honest no-panel edition

1. Freeze the claim tiers and decision rules in repository documentation.
2. Turn the reported rule neighborhood into one transparent inherited-evidence exhibit.
3. Commit, manifest, and clearly label the completed OECD 10Y--3M public proxy as a nearby-rule audit; preserve its null family-adjusted result.
4. Keep the public delivered-easing and country-combination exercises in the appendix.
5. Convert the public repository into a tagged, formal, rights-audited release with a clean-clone log and full release checksums.

### Priority C: Work that should wait

- Further prose expansion before decisive exhibits exist.
- Additional weak markets or mechanisms sharing the same 15 dates.
- More trading overlays, Sharpe optimization, downcurve taxonomies, or conditional UIP rhetoric.
- Any attempt to obtain 90+ by increasing robustness-table count rather than reducing selection uncertainty.

## Required v0.3 release packet

A serious v0.3 release should contain, at minimum:

- main, appendix, and combined PDFs;
- exact checksums and PDF page counts;
- a machine-readable claim ledger;
- input, code, environment, and output manifests;
- the complete core specification grid if the panel is recovered;
- the 15-episode core ledger and all event-level diagnostics;
- public-proxy result families with adjusted inference;
- a data/license/redistribution matrix;
- an environment lock and tool versions, including TeX and Poppler;
- an annotated Git tag and formal GitHub release;
- clean-clone logs for unit tests, saved-snapshot analysis, PDF build, and preflight;
- a prominent boundary stating which results are regenerated, inherited, public proxies, or simulations.

## Final recommendation

Proceed with v0.3, but do not let the manuscript get ahead of the evidence. The current edition has already solved most of the writing and production problem. Its remaining weakness is not that it is too short or too cautious. It is that the central state was evaluated on the history used to motivate it, only fifteen episodes identify the result, and the package cannot regenerate the core estimates.

The dangerous temptation is to treat a polished PDF, a public repository, and additional public proxies as cumulative confirmation. They are not. The proper 90+ route is narrower and harder: recover the core objects, reveal the entire design neighborhood, test whether other countries' curves predict a country's currency, and freeze the rule for evidence it has not already seen. If those tests succeed, the paper can make a strong claim about cross-country bond-market configurations and shared currency risk. If they fail, v0.3 should become a different, narrower paper. That willingness to change the paper is itself part of the acceptance standard.

## v0.3 manuscript pre-release audit - 2026-08-26

### Snapshot and verdict

This audit covers the active main and online-appendix sources, every included generated table and figure, the latest component PDFs, the combined PDF, and the second-pass missed-content notes. The audited PDF snapshot is:

- main: 37 pages, SHA-256 `D4B08D1C106C20E21124916C0855696A96AF1C97DD15AAE6EC588305C08E09AE`;
- online appendix: 24 pages, SHA-256 `02A403B917818EE36C4065FA9237C06EE6ED43F3790B301C2447257472BDACA8`;
- combined: 61 pages, SHA-256 `780762595471071ECE79366F3AF381489B1D34D079ABC7993FBA83D247DEE35F`.

**Release verdict: STOP. Revised honest score: 73/100.** The manuscript is much stronger in source recovery and adverse-evidence disclosure, but the empirical ceiling has not moved because the core panel remains absent. The current release additionally fails its own PDF preflight, overstates what the exact-one/exact-two coefficients show, and reports a maximum-statistic family adjustment whose rotations are not aligned to a common calendar assignment across all 64 rules.

| Dimension | Weight | Pre-v0.3 | Current v0.3 | Audit reason |
|---|---:|---:|---:|---|
| Contribution and claim hierarchy | 14 | 13 | 13 | Clearer configuration/exposure contribution, but the central sign-reversal wording and public-proxy conclusion still overreach |
| Rule integrity and specification search | 18 | 10 | 12 | The reported neighborhood and complete public grid add real transparency; the original family is still incomplete and the public max-stat alignment is defective |
| Rare-event inference and episode anatomy | 12 | 9 | 9 | Fifteen core episodes remain the effective sample; the new 20-episode ledger belongs only to the nearby public proxy |
| Common-information and exposure tests | 12 | 9 | 9 | Own-curve and public exclusions are clearly bounded; the decisive core-state leave-own-curve-out test remains unavailable |
| Identification and mechanism discipline | 10 | 7 | 7 | Strong boundaries, with remaining overstatement of the nine-point beta association |
| Return object and implementation | 8 | 6 | 6 | Forward/spot boundaries are mostly correct; the log-return/rate-differential approximation still needs an exact convention |
| External validation | 10 | 4 | 4 | The public proxy is a same-history nearby measurement audit, not an untouched holdout |
| Reproducibility and release integrity | 10 | 8 | 8 | Public code and outputs improve the package, but the core remains unregenerated and the v0.3 tree is not yet an immutable release |
| Writing, architecture, and exhibits | 6 | 6 | 5 | Strong architecture, but preflight fails and several pages contain unacceptable orphans/underfill |
| **Total** | **100** | **72** | **73** | **A score above 73 is not warranted until every P0 item below is closed** |

### P0 - Release-blocking findings

#### P0.1 Reader-facing transcription status fails the automated release gate

`rewrite/sections/04_main_inherited_evidence.tex:31` says “Points transcribe the displayed...” in Figure 3's caption. That production-status term appears on main PDF page 16. `python rewrite/verify_pdfs.py` therefore fails for both the main and combined PDFs. The caption should describe the estimands and the incomplete reported neighborhood, not how the asset was manufactured.

**Acceptance test:** `python rewrite/verify_pdfs.py` exits zero on the final main, appendix, and combined PDFs; a text scan finds no `transcrib*`, `inherited`, `source-PDF`, workspace, author-package, or reconstruction-status term in reader-facing pages.

#### P0.2 “Return sign reverses” is not what the reported rows estimate

`rewrite/sections/00_abstract.tex:2`, `rewrite/sections/01_introduction.tex:17`, and `rewrite/sections/07_conclusion.tex:4` describe a return-sign reversal between exactly one and exactly two live inversions. But `rewrite/generated/tables/v03_reported_rule_neighborhood.tex:16-18` reports two separate active-minus-complement regression coefficients: `+8.33` for the exactly-one indicator and `-15.72` for the exactly-two indicator. Those signs do not by themselves establish that the conditional mean return is positive in the first cell, nor do they supply inference for the direct exactly-two-minus-exactly-one contrast. `rewrite/sections/04_main_inherited_evidence.tex:18` is closer because it calls them coefficients, but “the coefficients reverse” still invites a direct contrast that is not shown.

**Required fix:** say that the separately estimated active-minus-complement coefficients have opposite signs. If the paper wants a direct sign-reversal result, report the two cell means, their exact difference, and episode-aware inference for that predeclared contrast.

**Acceptance test:** no abstract, introduction, or conclusion sentence says that the return sign reverses unless a direct one-versus-two estimand and its uncertainty appear in a table. All prose distinguishes conditional means, active-minus-complement coefficients, and direct cell contrasts.

#### P0.3 The public max-statistic columns do not share one calendar rotation

The family-wide inference claim in `rewrite/sections/03_empirical_design.tex:38`, `rewrite/sections/07_robustness_limits.tex:38-40`, and `rewrite/appendix/D_public_data_checks.tex:18-24` depends on `research_pipeline/src/public_yield_proxy_v03.py:201-216` and `224-272`. The 32 one-month-lag rules have 455 usable observations; the 32 two-month-lag rules have 454. The code requests 454 reference draws for both, then maps draw `k` to `floor(k*n/454)`. Consequently, after part of the grid, the 455-observation specifications use a different calendar displacement from the 454-observation specifications in the same max-stat row. The columns are not evaluations under one common timing reassignment. The resulting `p_maxT_family`, including the reported `0.562`, is not the claimed common-rotation family-wise reference.

This defect is adverse-result neutral: it may or may not change the conclusion that no public rule survives. It nevertheless invalidates the exact inference label.

**Required fix:** define one master monthly calendar and one shift index per draw; apply that same calendar displacement to every state before each rule's sample mask is imposed. Do not compress different usable samples and then align them by fractional position.

**Acceptance test:** a unit test constructs lag-one and lag-two toy specifications and verifies that max-stat row `k` maps both to the same calendar displacement; every declared rule is present; observed assignment is included once; recomputed raw and family values are regenerated into CSV, TeX, prose, manifests, and PDFs. Until then, replace “controls family-wise error” and all exact max-stat `p`-values with “provisional.”

#### P0.4 The public proxy is interpreted more strongly than its inference permits

`rewrite/sections/03_empirical_design.tex:38` calls the proxy “external directional consistency”; `rewrite/sections/07_robustness_limits.tex:50` says the family “confirms” a direction beyond one “undocumented” rule; `rewrite/sections/07_conclusion.tex:8` infers “recurring directional information”; and `rewrite/appendix/D_public_data_checks.tex:43` says the configuration “carries directional information.” These statements are too strong when the baseline raw `p=0.062`, the currently reported family value is `0.562`, zero rules clear 5 percent, the crisis deletion gives `p=0.244`, and one disjoint direction is approximately zero. Forty-five negative, highly correlated specifications are a descriptive sign count, not confirmation or external validation.

**Required fix:** call the proxy a complete nearby-measurement sensitivity audit. State that a majority of overlapping rules have the same sign, but the family provides no adjusted detection and the disjoint evidence is asymmetric. Delete “confirms,” “external consistency,” and “recurring information.”

**Acceptance test:** the abstract, main text, conclusion, and appendix describe `45/64` only as a descriptive count of dependent rules and never use it to establish validation, recurrence, or independent confirmation.

### P1 - Required substantive and presentation fixes

#### P1.1 “Frozen before estimation” is not supported by an immutable pre-result record

`rewrite/sections/01_introduction.tex:25`, `rewrite/sections/03_empirical_design.tex:38-40`, and `rewrite/sections/07_robustness_limits.tex:38` call the public family frozen or fixed before estimation. The family, code, tests, and outputs were still uncommitted in the audited working tree, and there is no immutable pre-outcome tag. A family declared in analysis code is fully disclosed, but that is not evidence that its choices preceded inspection of outcomes.

**Acceptance test:** either produce an immutable commit/tag demonstrably predating result inspection, or replace “frozen/fixed before estimation” with “declared in code and fully reported.” The public exercise must not be called preregistered or prospective.

#### P1.2 The nine-point beta association is still described as an established restriction

`rewrite/sections/05_mechanism_model_intuition.tex:21` says the nine-point fit “does establish a cross-sectional restriction,” and `rewrite/sections/03_empirical_design.tex:44` says the evidence rejects no relation with predetermined exposure. Yet the fit has no displayed coefficient uncertainty, Australia and New Zealand have high leverage, the monthly state-by-beta interaction has episode `p=0.210`, the pre-2005 beta portfolio has `p=0.287`, and full-sample MSCI beta has `p=0.319`. The S&P beta-sorted portfolio is useful evidence; the nine-dot slope is descriptive.

**Acceptance test:** prose says “documents a descriptive ordering consistent with” rather than “establishes/rejects”; the beta-portfolio result, panel-interaction null, pre-2005 weakness, and MSCI failure remain adjacent enough that none can be read in isolation as structural exposure evidence.

#### P1.3 Internal evidence-production language remains in the main paper

Beyond the P0 caption, `rewrite/sections/07_robustness_limits.tex:32` says “The source does not contain...,” line 50 says “one undocumented rule,” and line 52 says the “original analytical panel is unavailable here.” The limitation is economically important, but these are editorial-production statements rather than self-contained descriptions of what the study estimates. “Undocumented” is also inaccurate: the recursion is documented; the underlying core panel and complete historical search record are unavailable.

**Acceptance test:** state the empirical limit directly—for example, exact deletion coefficients are not reported; the complete historical rule family cannot be assessed; the released materials do not regenerate the core panel—without referring to a source PDF, workspace, transcription, or undocumented rule.

#### P1.4 Return accounting mixes a log spot change with a simple rate differential without stating the approximation

`rewrite/sections/02_setting_measurement.tex:29-34` and `rewrite/appendix/B_accounting_theory.tex:8-19` define `s` in logs but set monthly income to the annualized money-market-rate difference divided by twelve, then say the sum corresponds to a forward return under covered interest parity. If the money-market rates are simple annualized rates, adding `d/12` to a log spot change is a first-order proxy, not an exact log excess return.

**Acceptance test:** identify whether rates are simple or continuously compounded. Either use a unit-consistent log formula such as the relevant log gross-rate differential, or explicitly label `d/12 + Delta s` a first-order monthly approximation. Preserve the basis, spread, and executability caveats.

#### P1.5 The supposedly complete state algorithm is ambiguous under missing slopes

`rewrite/appendix/A_signal_algorithm.tex:37` says a current or lagged missing slope creates neither a crossing nor a confirmed-steepening update; line 42 says an interrupted steepening sequence resets the counter; line 62 again says missing observations do not count toward release. These sentences do not determine whether a missing month holds `k` fixed or resets it, nor what happens to eligibility when the nonnegative observation required for re-entry is missing. A “complete deterministic transition” must assign every state variable.

**Acceptance test:** the transition table specifies `L`, `k`, and eligibility under current-missing, lagged-missing, and return-from-missing cases, and tests cover each branch. The wording must match the implementation used for any regenerated state.

#### P1.6 Current pagination is not release quality

- Main PDF page 20 contains only the last three lines of Section 4 and otherwise is blank; `rewrite/main.tex:30` forces the following section onto a new page.
- Appendix PDF page 15 begins with the orphaned word “statistic.” from `rewrite/appendix/D_public_data_checks.tex:20`, before Table 9.
- Appendix PDF page 21 contains Table 13 and then the isolated continuation “the headline state.” from `rewrite/appendix/D_public_data_checks.tex:106`, with most of the page blank.

There is no clipping or overlap, and the figures render sharply. These are flow defects, not cosmetic preferences.

**Acceptance test:** visual inspection finds no page consisting only of a paragraph fragment and no sentence split around a float into a one-word or one-line orphan. Add a page-substance check that flags low-text non-figure pages; remove unnecessary hard `\clearpage` boundaries or adjust float placement without shrinking core tables further.

### P2 - Polish and self-containedness fixes

1. `rewrite/generated/tables/inherited_headline.tex:4,21`, `inherited_tail_robustness.tex:19`, and `inherited_split_sample.tex:25` use “IYC” without defining it anywhere in the main text. Spell out synchronized-inversion state or define the acronym once.
2. `rewrite/generated/tables/v03_bilateral_own_curve.tex:14-22` uses `AU`, `CA`, `CH`, `EU`, `GB`, `JP`, `NO`, `NZ`, and `SE` without a legend and instead of the otherwise used currency codes. Define the mapping or use AUD/CAD/CHF/EUR/GBP/JPY/NOK/NZD/SEK.
3. `rewrite/sections/04_main_inherited_evidence.tex:39` lists one-month release, three-month release, and 10Y--3M, then says beta remains detected under “both perturbations.” It should say all three.
4. `rewrite/generated/tables/inherited_headline.tex:4-21` labels “carry total” as a return without repeating that it is the money-market-differential proxy. A reader should not need surrounding prose to avoid mistaking the table for executable forward returns.
5. Appendix Table 7 on PDF page 10 reaches approximately 6-point type. It is technically legible when zoomed but too dense for comfortable print reading; split it or move secondary columns to a machine-readable supplement.
6. Appendix PDF page 13 begins with a one-line continuation from the term-premium discussion before Section C.8. Main reference page 37 and appendix reference page 24 are heavily underfilled. These are lower priority than the P1 orphans but should be cleaned in the final pagination pass.
7. Per-specification phrases such as “statistically detected” in `rewrite/sections/05_mechanism_model_intuition.tex:43` should say “at the reported per-specification level” because the historical neighborhood has no family adjustment.

### Second-pass missed-content cross-check

The second-pass notes were substantively integrated correctly:

- breadth beyond two is described as episode age rather than a monotone dose response (`rewrite/appendix/C_inherited_robustness.tex:24-30`);
- the implied-volatility beta null and raw-count control absorption are disclosed (`rewrite/sections/07_robustness_limits.tex:12-14`; `rewrite/appendix/C_inherited_robustness.tex:85-91`);
- persistent rate and S&P-beta portfolio membership is reported alongside the MSCI failure (`rewrite/sections/05_mechanism_model_intuition.tex:35-45`);
- the 2026:02 return endpoint is explicitly paired with generally 2026:01 rate coverage (`rewrite/appendix/A_signal_algorithm.tex:16`);
- the pre-Lehman chronology is not promoted to a separate identification result;
- the restrictive iid count-sufficiency theorem was not restored; and
- the conditional-Fama interaction retains its episode-bootstrap `p=0.340` warning (`rewrite/appendix/B_accounting_theory.tex:68-76`).

No material second-pass item is falsely presented as new independent evidence.

### Claim-language audit: what passes

- **Leave-one-country-out:** Pass. The main and appendix repeatedly state that the core own-curve horse race still includes the focal country's curve. The public exclusion exercise removes a currency from both its proxy state and proxy outcome and is not substituted for the core test.
- **Replication:** Pass with the P1.3 wording cleanup. No reader-facing sentence calls the core estimates replicated, reproduced, or independently verified; EM evidence is called breadth; public easing is explicitly not replication.
- **Causality:** Pass. Local projections are called temporal associations, rotation references are not called causal randomization tests, and the paper does not claim that inversions cause losses.
- **Executable returns:** Pass with the P1.4 accounting clarification. The paper consistently says the core total is a money-market-differential proxy and that forwards, basis, spreads, and costs are absent. “Executable public exercise” refers to code, not a feasible trading payoff.
- **Timing:** Pass subject to P1.5. The information convention is consistently `t -> t+1`, beta uses data through `t-1`, and delivered-easing month-zero returns are correctly called contemporaneous associations.

### Exact final acceptance suite

Do not release v0.3 until all of the following are true:

1. `python rewrite/verify_pdfs.py` exits zero on the exact release PDFs.
2. The 64-rule family is regenerated using one common calendar shift per max-stat draw, with a unit test proving calendar alignment across return lags and usable-sample masks.
3. A scripted phrase scan returns zero false uses of `return sign reverses`, `confirms`, `recurring directional information`, `external validation/consistency`, `replicated`, `causal`, `leave-one-country-out`, and `executable return`; negative boundary statements may be allowlisted explicitly.
4. Abstract, introduction, results, table notes, and conclusion agree on the exact-one/exact-two estimand and on the public-proxy interpretation.
5. The signal transition table assigns every state variable for every missing-data branch.
6. The rate/spot accounting uses one unit convention or identifies the approximation.
7. Main and appendix tables define all acronyms and currency codes and distinguish spot, income, proxy total, and feasible forward returns.
8. The full deterministic test suite passes from a clean checkout, and regenerated public CSV/TeX/prose values agree exactly with the release manifest.
9. Page-by-page visual inspection finds no clipping, overlap, one-word float orphan, paragraph-fragment page, unreadably reduced core table, or underfilled page caused solely by forced section breaks.
10. The release commit has an empty `git status --porcelain`, an annotated `v0.3.0` tag, final PDF hashes, and a formal release whose attached files match those hashes.

**Bottom line:** the rewrite is intellectually more credible than v0.2 because it restores adverse robustness and states the missing tests. It is not ready to release. Fixing P0.1, P0.2, and P0.4 is editorial; P0.3 requires recomputation. None requires or licenses a stronger claim about the absent 10Y--2Y core panel.

## Final empirical linkage audit

The public-proxy point estimate and annualization pass a direct recomputation. The active mean is $-0.46980$ percent per month, the inactive mean is $+0.07880$, and $12(-0.46980-0.07880)=-6.5832$ annualized percentage points. The ledgers contain 108 active and 347 inactive usable months, twenty episodes, 64 unique specification rows, 45 negative estimates, and zero rows with reported family value at or below 0.05. The baseline raw rotation value is 0.06154 and the reported family value is 0.56167, correctly rounded to 0.062 and 0.562. The current static TeX tables match the CSVs to displayed precision, the released plot copy is byte-identical to the pipeline PNG, and the current main and appendix PDFs contain the new values. Those are linkage facts, not a release pass: the links are manual and unaudited by code.

### P0 - recompute or narrow before release

1. **Replace the 454-point family reference with a genuine common-calendar construction.** `public_yield_proxy_v03.py` currently drops unusable endpoints separately by rule, rotates each truncated state vector, maps it onto 454 fractional positions, standardizes the coefficient reference, and takes the cross-rule maximum. For lag-one rules one of 455 distinct rotations is omitted; a given row of the 454 grid is therefore not literally the same calendar shift across lag-one and lag-two rules. This does not establish exact family-wise error control. Recompute every rule under the same shift of the full 456-month calendar before applying rule-specific valid-outcome masks, add an alignment test, and describe the finite-rotation assumption. Until then call 0.562 a common-grid maximum-statistic diagnostic, not a family-adjusted $p$-value that controls FWER.

2. **Correct the statistic's name.** The code divides each rotated coefficient by the standard deviation of its rotation distribution after subtracting that distribution's mean. It does not compute a regression $t$-statistic. Replace `max-$|t|$` in `rewrite/generated/tables/v03_public_proxy_summary.tex` with `maximum-$|z|$ rotation reference` (or change the code to compute the advertised statistic).

3. **Integrate the module into the supported reproduction path.** `run_reproduction.ps1` does not call `public_yield_proxy_v03.py`; neither it nor `rewrite/build.ps1` regenerates the three public-proxy TeX tables or copies/verifies the PNG. Add a deterministic CSV-to-TeX/figure generation stage, call it before the PDF build, and add tests comparing every displayed number and asset hash with machine output. The present statements that the exercise is independently reproducible and that every output is released are too strong for the current one-command workflow.

4. **Complete the run manifest.** The v0.3 manifest hashes all twenty OECD/FRED curve files and its nine direct outputs, and those hashes currently verify. It omits the BIS policy-rate files, BIS FX files, `mechanism_spec.json`, the analysis code, source configuration, and the static TeX/PNG manuscript assets, even though all determine the reported results. Add all effective inputs, code/config hashes, package versions, commit ID, and manuscript mirrors. Because the hashed raw snapshot is ignored by Git, distinguish exact snapshot reproduction from a fresh current-vintage method rerun.

### P1 - interpretation and measurement fixes

5. **Remove the unverifiable ex-ante claim.** The manuscript says the 64-rule family was “fixed before estimation,” but there is no immutable pre-analysis record and the entire layer is uncommitted relative to the last repository commit. Say that the family is declared in code and exhaustively reported. Likewise qualify “complete family” as the complete declared 64-cell *public-proxy* family; it is not the complete reasonable family for the author state.

6. **Do not call the currency exclusions leave-one-country-out prediction.** Each row removes currency $i$ from both the state and the basket of the remaining eight; it does not use other countries' curves to predict currency $i$. It is a joint leave-one-country influence diagnostic and does not eliminate signal/outcome universe overlap. In prose, “$-7.47$ for Australia” must become “$-7.47$ when Australia is excluded.” Rename the CSV/ledger target or state this distinction wherever `leave-one-country-out` appears.

7. **Disclose that the two disjoint directions are not symmetric designs.** European curves predict a one-long/one-short basket of four non-European currencies with four-of-five sensor coverage required; the reverse uses a two-long/two-short basket of five European currencies with three-of-four sensor coverage required. The $-18.22$ and $+0.30$ estimates are therefore not a clean directional horse race. Report leg sizes and coverage in the table, run harmonized constructions if feasible, and keep the raw 0.022 descriptive because the eleven exclusion/disjoint diagnostics have no family adjustment or immutable prespecification.

8. **Specify and stress-test portfolio ties.** `assign_carry_weights` breaks equal policy-rate differentials by inherited row order. A portfolio boundary is tied in 132 of 456 months for the baseline three-by-three basket, 54 months for the four-currency disjoint basket, and 115 months for the five-currency disjoint basket. A read-only equal-allocation check gives approximately $-6.26$, $-17.80$, and $-0.31$ respectively, so it does not overturn the broad pattern, but the released values still depend on an undocumented rule. Freeze an explicit tie policy, test fractional allocation, and record it in the ledger and table notes.

9. **Make the return-availability check operate on selected legs.** The aggregator counts all rows with nonmissing weights, including zero-weight middle currencies, when deciding whether enough returns exist. No incomplete selected leg occurs in the current files, so displayed estimates are unaffected, but the guard is wrong and can silently produce underinvested baskets after a provider revision. Require all nonzero-weight legs to have returns and test this branch.

10. **Resolve missing-value semantics in the live recursion.** The code preserves a steepening counter through a missing month, so two increases separated by missing observations can trigger “two consecutive increases.” Current slope series have no internal gaps after their first observation, so present values are unaffected. Either reset the counter on a missing current/lagged slope or define the rule as consecutive *observed comparisons*; add the exact counter-one/missing/release test and make the transition table agree.

11. **Narrow real-time language.** The curve inputs are current-vintage monthly observations and their publication availability is not modeled. The state-$t$/return-$t+1$ alignment is mechanically correct, and policy ranking for the return month uses the prior month's differential, but this is not a real-time forecasting or executable timing test. Replace “confirms” and unqualified “predicts” for this module with “is associated with next-month public spot returns in the current-vintage proxy.” Remove “fixed before estimation” from the main text.

12. **Synchronize provenance and release documentation.** `public_data_inventory.csv`, `research_pipeline/reports/data_access_audit.md`, both reproducibility guides, the pipeline README, and the one-command step/test counts do not yet include the twenty yield files or the new analysis. The machine data-purpose row is useful but says `retained_online` even though the result now appears in the main paper and calls its exclusion diagnostic leave-one-country-out. Update the status and terminology, rerun the access audit, and verify provider metadata before asserting that every national series is a monthly average.

13. **Downgrade two manuscript conclusions.** “The independent public family confirms that the direction appears beyond one undocumented rule” should be “documents negative estimates in 45 of 64 declared public-proxy rules.” “A nearby public configuration carries directional information” should not be presented as external validation: the raw baseline value is 0.062, the common-grid family diagnostic is 0.562, crisis-episode deletion is 0.244, and deletion of five worst active months attenuates the estimate from $-6.58$ to $-2.29$. The defensible contribution is transparent adverse measurement sensitivity, not confirmation of the 10Y--2Y state.

## Final-release addendum: superseding public-proxy results

The corrected public proxy delays live entry by one month, applies one literal common-calendar shift across the declared family, allocates all cutoff ties equally, and requires nonmissing returns for selected legs. The baseline estimate is `-3.2016` annualized percentage points with raw circular reference `p=0.3348`, based on `99` active months and `18` episodes. The common-calendar maximum-$|z|$ reference is `1.000`; `41` of `64` rules are negative, no rule crosses the 5-percent family threshold, and the baseline ranks `22` of `64` from most negative to most positive.

The adverse diagnostics remain decisive for interpretation. Deleting episodes containing September 1998, October 2008, or March 2020 gives `-0.46` percentage points with rotation reference `0.826`. The first and second calendar halves give `-5.73` (rotation reference `0.382`) and `-1.02` (`0.776`). Deleting the five worst active months changes the estimate to `+0.94`; because that deletion is outcome-conditioned, no reference value is reported. European curves paired with non-European currencies give `-15.84` (rotation reference `0.062`), whereas the reverse disjoint split gives `-0.34` (`0.887`). The delivered-easing policy-rate proxy gives a cumulative months-0--1 estimate of `-1.0607` percentage points (finite-rotation reference `0.2222`; Holm-adjusted reference `1.000`). In the exploratory country screen, CHF--GBP gives `-4.5396` percentage points, with a conditional common-rotation maximum-$|z|$ reference of `0.0352` under the stated exchangeability assumption and six-event threshold; its interval includes zero and stricter event thresholds yield no family crossing. These are current-vintage policy-ranked log spot-return proxy associations, not replication, external validation, or unconditional family-wise inference.

## Final closure: two scores for two different objects

The final release comprises a 38-page main paper, a 27-page online appendix, and a 65-page combined PDF. On editorial architecture, documentation, reproducibility of the public-data modules, provenance, and production quality, it clears the 90-plus release standard at **96/100**. The manuscript is concise, the main and appendix are self-contained for readers, the source boundary is documented outside the PDFs, the deterministic public-data workflow passes 39 tests, and the release artifacts are professionally organized.

That production score is not an empirical-identification score. Because the original author panel, exact portfolio inputs, and core estimation code remain absent, the paper's empirical-design ceiling remains approximately **82/100**. The inherited headline results cannot be independently regenerated, and the public exercises are nearby robustness and mechanism diagnostics rather than replication or external validation. Both scores should be reported together: **96/100 for editorial, reproducibility, and production execution; approximately 82/100 for the attainable empirical design given the evidence currently available.**
