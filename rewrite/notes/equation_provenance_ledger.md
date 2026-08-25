# Equation provenance and simplification ledger

Final audit date: 2026-08-26
Source: `AI JMP.pdf` (94 pages)
Reader builds: 38-page main paper and 27-page online appendix, 65 pages combined
Machine-readable companion: `equation_provenance_ledger.csv`

The final main paper has ten numbered equations. The online appendix has seven numbered equations in Appendix B and four in Appendix D. Appendix A implements the state as a transition table rather than another numbered recursion.

## Main-paper equations

| No. | Label | Page | Purpose | Provenance |
|---:|---|---:|---|---|
| (1) | `eq:slope_information` | 6 | Country level + shared curve information + idiosyncratic component | Editorial signal-extraction formalization motivated by original pp. 14--17; not an estimated structural factor |
| (2) | `eq:inversion_threshold` | 6 | Curve-level inversion indicator | Editorial formalization of the indicator inside original equation (9), p. 16 |
| (3) | `eq:factor_decomposition` | 6 | Shared/idiosyncratic currency return exposure | Schematic restatement of original equation (5), p. 13 |
| (4) | `eq:currency_return` | 7 | Monthly currency return proxy | Direct restatement of original equation (1), p. 11 |
| (5) | `eq:carry_return` | 7 | Three-by-three carry and income/spot decomposition | Combined restatement of original equation (2), p. 12 |
| (6) | `eq:signal` | 8 | Live-count aggregation and at-least-two state | Aggregation part of original equation (9), p. 16; transition is in Appendix A |
| (7) | `eq:currency_beta` | 10 | Predetermined expanding-window equity beta | Direct restatement of original equation (3), p. 12, with returns ending at `t-1` |
| (8) | `eq:state_regression` | 11 | General next-month predictive regression | Editorial formalization of source Tables 4, 7, and 14 |
| (9) | `eq:bilateral_state` | 12 | Currency-specific next-month spot regression | Editorial formalization of source Table 2/Figure 5 and Table 8 |
| (10) | `eq:predetermined_compensation` | 31 | Condition for current expected loss after predetermined compensation | Compression of original equations (10)--(13), pp. 19--21 |

## Appendix equations

Appendix B equations (1)--(7), on pp. 6--7, restate the accounting, schematic exposure, adverse-payoff, compensation, negative-mean, and conditional-Fama objects from original equations (1)--(5) and (10)--(14). Appendix D equations (8)--(11), on pp. 20--21, are new code-exact definitions for the independently reproduced public delivered-easing proxy: country cuts, synchronized onsets, endpoint changes, and cumulative return flows.

## Timing correction and information clock

The authoritative v0.3 clock is:

1. A fresh crossing is observed at month-end `t-1`: `I_{i,t-2}=0` and `I_{i,t-1}=1`.
2. That curve first becomes live at `t`: `L_{i,t}=1`.
3. The cross-country count and state are formed at `t`.
4. `S_t` positions/predicts the payoff realized during `t+1`.

This is the source equation-(9) timing on original p. 16. Merely setting a live state in the crossing month would be one month too early. Tables indexed by payoff month may equivalently write the predetermined regressor as `S_{t-1}`.

## Simplification decisions

- Original equations (6)--(7) and the iid/identical-loading sufficiency apparatus were removed because they impose structure not identified by nine-currency descriptive evidence.
- Original equation (8), the expectations/term-premium discussion, is retained in cautious prose because the displayed source expression is schematic without full maturity-specific definitions.
- Original strategy equation (15) was removed with the trading overlays.
- Original equations (16)--(17) are retained only as inline exploratory curve-shape definitions in Appendix B/C.
- The compensation benchmark preserves earlier-information-set compensation through `E_{t-1}[p_t]`; replacing it with `p_{t-1}` would add a transition/martingale assumption.
- Public Appendix D equations are independent proxy definitions. They are not source equations and do not replicate the original 10Y--2Y state.
