# External copied-material ledger

Audit date: 2026-08-26  
Source: `AI JMP.pdf` (94 pages)  
Machine-readable record: `copied_material_ledger.csv`

This ledger is deliberately external to the main paper and online appendix. It records which visible objects and numerical cells come from the 94-page source, where each object appears in the revised package, and which recovered items were excluded.

## Inventory

The CSV contains 48 provenance events:

- 40 recovered source crops: 12 figures and 28 tables;
- 8 native-LaTeX adaptations of source numbers: seven reader-facing tables and one external beta-benchmark audit table.

Every crop row records the source page and exhibit number, crop rectangle, PDF/PNG asset pair, SHA-256 hash, reuse mode, destination, and inclusion status. Every numerical adaptation records the source exhibits, generated LaTeX file, hash, destination label, and transformation note.

## Reader-facing inclusion

| Final location | Source material retained | Form in final document |
|---|---|---|
| Main Figure 1, p. 3 | Source Figure 1, p. 5 | Flattened 400-DPI crop; caption states timing and distinguishes current from live inversions |
| Main Figure 2, p. 8 | Source Figure 2, p. 18 | Flattened 400-DPI crop; caption centers the path-dependent release rule |
| Main Figure 3, p. 15 | Source Figure 5, p. 33 | Flattened 400-DPI crop; caption reports the baseline beta slope and identifies the downcurve fit as exploratory |
| Main Table 2, p. 12 | Source Table 4, p. 39 | Selected headline cells transcribed into a native table |
| Main Table 3, p. 16 | Source Table 2, Figure 5, and Table 3, pp. 31--36 | Rate-beta alignment, cross-currency gradient, beta-sort, panel interaction, and conditional-Fama estimates synthesized into one native table |
| Online Appendix Table 2, p. 4 | Source Table A.2, p. 75 | Era counts transcribed; active shares recomputed from counts |
| Online Appendix Table 3, p. 7 | Source Table 4, p. 39 | Bottom-decile-deletion rows transcribed into a native table |
| Online Appendix Table 4, p. 8 | Source Table E.1, p. 86 | Calendar-half cells transcribed into a native table |
| Online Appendix Table 5, p. 9 | Source Tables C.3 and K.1, pp. 79 and 94 | Baseline, tenor, and term-premium-adjusted estimates placed on one scale |
| Online Appendix Table 7, p. 10 | Source Tables 11--12, pp. 53--55 | G10 and G10-plus-EM spot/total cells combined; carry income computed as total minus spot |
| Online Appendix Figure 1, p. 11 | Source Figure 6, p. 37 | Flattened 400-DPI crop; caption limits the panels to supporting temporal associations |

The public-data tables, public event-study figure, and pair/triple country screen are new executable analyses and are not copied material.

## External-only material

- Source Figures 3--4, 7--8, A.1--A.2, D.1, and J.1 and all unused source tables remain under `rewrite/assets/original/` for audit.
- Source Appendix F, including Table F.1, is excluded from both PDFs.
- Source Appendix G, including Table G.1, is excluded from both PDFs. The separate native transcription of Table G.1 is also excluded because the full-sample MSCI result does not support a general beta-benchmark robustness claim.
- `rewrite/appendix/F_data_provenance.tex` and `rewrite/appendix/G_additional_inherited_exhibits.tex` remain external archival source files and are not input by either PDF entry point.
- The synthetic path-dependence exercise remains repository-only and is not part of either reader-facing PDF.

## Caption and binary-safety rule

Recovered PDF clips can retain hidden source-page text even when only the crop is visible. Every reused figure therefore enters the final PDFs as a flattened PNG containing visible pixels only. Captions are native LaTeX text and contain the economic description without production labels such as “copied,” “recovered,” or “source PDF.” Automated preflight checks reject hidden PTEX metadata, personal filesystem paths, and production terminology.

## Interpretation

A transcription or crop reproduces the visible source object; it does not independently regenerate the underlying estimate. The revised paper presents the estimates as reported results, while the repository separately identifies which claims can and cannot be reproduced from public inputs.
