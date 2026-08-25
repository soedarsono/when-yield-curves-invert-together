# v0.3 result and reproduction ledger

Audit date: 2026-08-26
Release target: `Alt_JMP_v0.3.pdf`
Reader-facing locations refer to the 38-page main paper and 27-page Online Appendix.

## Purpose

This ledger separates three objects that must not be conflated.

1. **Baseline evidence** is reported in `AI JMP.pdf` and rewritten in v0.3. The absent author panel prevents independent regeneration of those estimates.
2. **Source-derived synthesis** recombines exact entries already reported in `AI JMP.pdf` to expose economics that the longer draft underused. Code can audit the transcription and presentation, but it cannot turn those entries into regenerated estimates.
3. **Independent public analysis** is computed from OECD, BIS, FRED, CFTC, and other declared public files. It is executable through the documented downloader and one-command workflow, but it uses proxy tenors, rates, and returns and therefore is a challenge exercise rather than a replication of the baseline 10Y--2Y state. The manifest freezes the exact input hashes; reproducing the exact numerical snapshot later requires matching those bytes because the providers can revise current-vintage series.

The companion machine-readable file, `v03_novel_result_reproduction_ledger.csv`, maps each displayed result to inputs, code, output rows, paper assets, tests, and the appropriate evidentiary boundary.

## Source-derived economic additions

| ID | New use in v0.3 | Exact provenance | Economic payoff | Boundary |
|---|---|---|---|---|
| SRC-01 | The reported nine-rule neighborhood is shown as one ordered exhibit | `AI JMP.pdf`, reported tenor/breadth/release rows; configuration in `research_pipeline/config/source_reported_rule_neighborhood.csv` | Shows that eight of nine carry estimates are negative, while the baseline is second-most negative rather than the displayed optimum | Reported neighborhood, not a complete historical search universe |
| SRC-02 | Exact-one and exact-two indicator coefficients are interpreted separately | `AI JMP.pdf`, Table 3 | Shows opposite coefficient signs around the two-curve configuration | Each coefficient is relative to its own complement; this is not a direct exactly-one-minus-exactly-two test |
| SRC-03 | Carry income is separated from spot losses | `AI JMP.pdf`, Table 2 | Active-state carry income is 5.14 percent versus 3.60 percent outside the state, a 1.54-point increase that does not offset the 12.85-point spot gap | The income difference is imprecise (`p=0.260`) and is not identified compensation |
| SRC-04 | Portfolio composition is moved from a remote source table into the main argument | `AI JMP.pdf`, Table H.1, p. 91 | Persistent cores coexist with rotation: for example, Norway's carry-long share falls 62 to 34, while the pound's rises 43 to 70 | Selected exact entries; complete source table remains traceable in the external ledger |
| SRC-05 | Real-time and timing falsifications are restored | `AI JMP.pdf`, signal audit and timing checks | 435 truncation endpoints and 492 membership checks report no mismatch; an extra lag attenuates carry, and forward placebos destroy the association | Reported checks; original code is unavailable |
| SRC-06 | A flat average G10 money-market-rate path is stated as a mechanism null | `AI JMP.pdf`, Figure 6 | Separates synchronized easing delivery from a mechanical average-rate shift | Descriptive event-time evidence, not causal identification |

## Independently executable v0.3 results

The public 10Y--3M audit deliberately retains adverse evidence.

- Baseline-like estimate: **-3.20 annualized percentage points**, raw circular-shift reference value `0.335`, 99 active months, 18 episodes.
- Complete declared family: **41 of 64** estimates are negative; the baseline-like rule ranks 22nd from most negative; common-calendar max-|z| reference value `1.000`; no rule meets the 5-percent family reference criterion.
- Crisis-episode deletion: **-0.46**, complete-case rotation-reference value `0.826`.
- Calendar halves: **-5.73** (reference value `0.382`) and **-1.02** (`0.776`).
- Outcome-conditioned deletion of the five worst active months: **+0.94**; no inferential p-value is assigned.
- Joint currency deletion: all nine estimates remain negative, from **-5.08** after removing AUD to **-0.60** after removing GBP; none is conventionally detected.
- Geographically disjoint designs are asymmetric: European curves to AUD/CAD/JPY/NZD yield **-15.84** (complete-case rotation-reference value `0.062`), while non-European curves to CHF/EUR/GBP/NOK/SEK yield **-0.34** (`0.887`).

These facts discipline the paper. They document sign resemblance in a majority of nearby public rules but reject a claim that the public proxy validates a unique, family-robust state.

## One-command trace

`run_reproduction.ps1 -UseExistingData` executes the saved-data audit, public mechanism checks, country-combination screen, source-reported-neighborhood audit, complete public yield-proxy family, paper-table renderer, deterministic tests, PDF build, PDF preflight, and root release copy. The public-yield manifest records SHA-256 hashes for raw inputs, code/configuration inputs, machine outputs, and the four paper assets generated from those outputs.

The critical link is explicit:

`saved raw data` → `public_yield_proxy_v03.py` → machine-readable CSV files → `render_v03_public_tables.py` → three LaTeX tables plus one figure → main paper and Online Appendix.

The public analysis is therefore independently executable and its exact input bytes are auditable from the manifest. Exact numerical reproduction from a future download remains conditional on the providers returning those same current-vintage bytes. The baseline source estimates remain traceable but not independently reproducible until the author panel and code are recovered.

## Acceptance checks

- Every public number displayed in v0.3 appears in a machine-readable output row.
- All 64 declared rules use the same 1988-01--2025-10 complete-case calendar for family inference.
- The max statistic uses standardized coefficients and identical literal calendar shifts across the family; family-wise interpretation is conditional on simultaneous cyclic-shift exchangeability.
- Live-state entry is delayed: a crossing first observed in month `t-1` becomes live in `t`, and state `t` predicts return `t+1`.
- A missing slope comparison resets the consecutive-increase confirmation counter.
- Carry ties receive equal weight across all currencies at the cutoff, so realized legs can exceed their target sizes; an outcome is missing if any selected nonzero-weight currency return is missing.
- Joint deletion removes each currency from both signal and outcome.
- Disjoint designs identify their asymmetric basket sizes and do not share currencies across signal and outcome.
- Tests assert output schemas, timing, family size, common calendar, expanded cutoff ties, paper hashes, and every manifest file hash.

## Release interpretation

No v0.3 public result is labeled external validation, replication, or causal evidence. The source-derived additions improve the economic reading of the baseline evidence; the public audit shows exactly where a nearby, independently executable construction travels and where it fails.
