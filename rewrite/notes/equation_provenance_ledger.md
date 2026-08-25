# Equation provenance and simplification ledger

This external ledger maps the mathematics in the 94-page original PDF to the simplified paper and attached appendix. The machine-readable companion is `equation_provenance_ledger.csv`.

## Outcome

The main paper now contains eight numbered equations rather than seventeen:

| Main equation | Purpose | Source relationship |
|---|---|---|
| (1) | Currency return proxy, $rx_{i,t+1}=d_{i,t}+\Delta s_{i,t+1}$ | Direct restatement of original equation (1) |
| (2) | Three-by-three carry portfolio and income/spot decomposition | Combined restatement of original equation (2); fixes the former double-numbered `align` block |
| (3) | Schematic shared-return exposure | Cautious restatement of original equation (5) |
| (4) | Live-curve count and synchronized state | Aggregation portion of original equation (9); exact recursion moved to Appendix A |
| (5) | Predetermined expanding equity beta | Direct restatement of original equation (3), with explicit one-month information buffer |
| (6) | General predictive regression | Editorial formalization of the regressions behind original Tables 4, 7, and 14 |
| (7) | Bilateral currency state regression | Editorial formalization of original Table 2 and Figure 5 |
| (8) | Conditional mean under earlier-information-set compensation | Compression of original equations (10)--(13) |

All predictive mathematics uses one convention: information observed at the end of $t$ predicts the return realized during $t+1$. Tables indexed by return month may equivalently describe the regressor as $S_{t-1}$.

## Important substantive corrections

1. The carry construction is one numbered `equation`/`aligned` block. The previous `align` environment silently consumed two numbers and attached its label only to the decomposition line.
2. Portfolio sets are $\mathcal H_t$ and $\mathcal F_t$, avoiding visual collision between the former $\mathcal L_t$ and the live-curve indicator $L_{i,t}$.
3. $\lambda_i$ denotes a latent shared-factor loading; $\widehat\beta_{i,t}$ denotes an estimated equity-beta proxy. The appendix no longer calls both objects beta.
4. $W_t$ denotes benchmarks and controls; $A_{t+1}$ denotes an adverse payoff event. The symbol $Z$ no longer performs two unrelated jobs.
5. The delayed-compensation expression uses $\mathbb E_{t-1}[p_t]$, matching the original earlier-information-set commitment. Replacing it by $p_{t-1}$ would require an additional transition or martingale assumption.
6. The conditional Fama regression and downcurve inequality are now appendix equations because their empirical evidence is supporting or exploratory.

## Removed mathematics

- Original equations (6)--(7) and the iid/sufficiency apparatus were removed because they impose stronger structure than the empirical contribution requires.
- The strategy payoff equation was removed with the trading overlays because executable forwards, costs, and frozen strategy construction are unavailable.
- The calibrated threshold proposition was removed because the illustrative parameters can imply a different threshold; the paper instead reports the exact-one/exact-two data contrast and clearly labels it in-sample.
- The synthetic simulation was removed from the reader-facing appendix. Its delayed-loss timing was built into its data-generating process, so it was a possibility illustration rather than robustness evidence. Code and outputs remain in the repository and are logged externally.

## Appendix mathematics

Appendix A gives the exact state transition and raw benchmark. Appendix B retains the full payoff accounting, Euler benchmark, compensation derivation, negative-mean condition, conditional Fama regression, and exploratory downcurve definition. Appendix D adds code-exact definitions for the public delivered-easing proxy and distinguishes endpoint-change estimands from summed return-flow estimands.

No equation in the rewritten paper is represented as newly estimated unless it belongs to the explicitly separate public-data analysis. The original author-panel equations and estimates remain source-derived because the author panel and code are unavailable.
