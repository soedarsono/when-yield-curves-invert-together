# Figure and recovered-exhibit provenance

Final audit date: 2026-08-26
Source: `AI JMP.pdf` (94 pages)
Reader builds: `main.pdf` (38 pages) and `online_appendix.pdf` (27 pages), 65 pages combined
Machine-readable companion: `figure_provenance.csv`

## Evidentiary classes

- **Source-reported, not independently replicated:** recovered source crops and any new visualization whose cells are transcribed from `AI JMP.pdf`.
- **Independently reproduced public proxy/challenge:** graphics generated from the public-data pipelines. These do not reproduce the original 10Y--2Y panel or return construction and are not baseline replications.
- **External audit asset:** recovered material retained for provenance but excluded from both reader PDFs.

## Figures in the final reader PDFs

| Final object | Final page | Asset | Provenance |
|---|---:|---|---|
| Main Figure 1 | Main 3 | `assets/original/figure_01_main.png` | Flattened 400-DPI crop of original Figure 1, p. 5; source-reported |
| Main Figure 2 | Main 9 | `assets/original/figure_02_main.png` | Flattened 400-DPI crop of original Figure 2, p. 18; source-reported; native caption states delayed live entry |
| Main Figure 3 | Main 16 | `generated/v03_reported_rule_neighborhood.pdf` | Newly composed visualization of original Tables C.1--C.3, p. 79, and D.2, p. 84; source-reported cells, not a replication; no search adjustment |
| Main Figure 4 | Main 20 | `assets/original/figure_05_main.png` | Flattened 400-DPI crop of original Figure 5, p. 33; source-reported |
| Appendix Figure 1 | Appendix 14 | `assets/original/figure_06_main.png` | Flattened 400-DPI crop of original Figure 6, p. 37; source-reported supporting temporal associations |
| Appendix Figure 2 | Appendix 18 | `generated/v03_public_specification_curve.png` | Independently reproduced complete 64-rule public 10Y--3M proxy family; not original replication |
| Appendix Figure 3 | Appendix 23 | `generated/public_mechanism_event_study.pdf` | Independently reproduced delivered-easing event study; downstream contemporaneous proxy, not inversion-state prediction |

## Recovered source inventory

The 94-page source contains 12 numbered figures and 28 numbered tables. All 40 were recovered as one-page PDF/PNG asset pairs. Only original Figures 1, 2, 5, and 6 enter the final reader PDFs. Every source table crop is excluded; numerical cells are instead rendered as native LaTeX and mapped in `copied_material_ledger.csv`. In particular, Table H.1 (original p. 91) appears as a seven-country selection in Main Table 6 (p. 23) and a complete nine-country/two-portfolio transcription in Appendix Table 8 (p. 12).

Recovered vector masters preserve source fidelity. The four source figures used in the reader builds are flattened to raster before inclusion so clipped or hidden source-page text cannot enter semantic extraction. Reader captions contain economic descriptions and limitations only; production labels stay in this ledger.

## Timing note for original Figure 2

The authoritative caption and text use the source equation-(9) clock: a crossing observed at `t-1` makes the curve live at `t`; `S_t` then positions/predicts the return in `t+1`. The crop itself is inherited, but the native v0.3 caption prevents the earlier same-month-entry interpretation.
