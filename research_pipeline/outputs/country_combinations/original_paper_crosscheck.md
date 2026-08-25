# Cross-check against the original paper's country evidence

## Source and scope

- Source: `AI JMP.pdf`
- SHA-256: `C1E770925DE84B1CC50F35B2A2FB7F015B6D250072B2F18F9EAC994489D1A043`
- Visually checked pages: 31--33 (mechanism, Table 2, Figure 5) and 47--49 (portfolio horse race and bilateral own-curve comparison, Tables 7--8).
- This note compares the new *delivered-easing proxy* with reported author-data results. It does not merge the two designs or claim to replicate the original yield-curve state.

## What the original already establishes

1. The currencies bearing the original state's losses are principally Australia and New Zealand, not Switzerland and the United Kingdom. In Table 2, Australia and New Zealand have the largest average rate differentials and high equity betas; their full-state spot coefficients are -13.21 and -13.28 percent per year, with episode-bootstrap p-values 0.013 and 0.012. The Swiss franc and pound have near-zero equity betas (-0.03 and +0.02) and much smaller, imprecise full-state spot coefficients (-0.89, p=0.868; -3.00, p=0.563).

2. A country's own curve is not generally a forecast of its own currency once the synchronized state is considered. Table 8 reports that own-state coefficients are insignificant conditional on the cluster for all nine currencies. The original text interprets the cross-country configuration, rather than the identity of one inverted country, as the informative object.

3. Table 7 points in the same direction at the portfolio level. Adding all nine country states makes the synchronized-state coefficient more negative while the country-state coefficients are mainly positive. The original interpretation is that individual states absorb benign one-country episodes and leave the synchronized configuration to identify the adverse ones.

## How the public combination result should be read

The public proxy's leading pair is CHF+GBP: six joint-cut onsets, a mean cumulative shadow carry spot return of -4.63 percentage points in months 0--1, raw rotation p=0.009, and all-combination max-statistic p=0.042. Its dates are 1992-09, 1993-01, 1995-12, 1999-04, 2001-09, and 2008-10. The result is fragile: the 90% episode-resampling interval is [-9.52, 0.26], deleting October 2008 raises the mean to -2.62, and the family contains no 5% result when eligibility requires at least eight rather than six events.

The pair's identity does **not** mean that francs and pounds are the currencies driving the original losses. The source evidence rejects that reading: both have low measured equity betas and weak bilateral responses. A more coherent candidate interpretation is a distinction between **where a global stress state is revealed** and **where the resulting currency exposure is borne**. Joint Swiss--U.K. easing may act as a calendar marker for broad stress or coordinated policy response, while the carry loss falls on persistently high-rate, high-beta currencies such as Australia and New Zealand. That sensor-versus-bearer distinction is compatible with the original paper's own-curve horse race.

This is a potentially useful economic insight, but not yet a paper result. Establishing it requires the author yield panel: enumerate the countries contributing to each original synchronized-inversion onset, test combination-specific predictive effects with episode-level multiplicity control, and compare those signal-contributor identities with the currencies' predetermined beta and carry-leg exposures. Until that is done, the public result belongs in a robustness appendix or future-work note, not in the abstract or headline contribution.

If this interpretation is discussed using literature, the relevant citations are already in the original bibliography: Chen and Tsang (2013) for own-curve information, Verdelhan (2018) for common bilateral currency components, and Ranaldo and Soderlind (2010) for safe-haven behavior. No new reference is needed.
