# Original-paper visual provenance map

Source: `AI JMP.pdf` (94 pages), inspected page by page on 2026-08-25.

Every numbered figure and table in the source PDF is catalogued below. The canonical, machine-readable ledger with captions, crop methods, resolutions, placement, recommendations, limitations, and evidentiary labels is `figure_provenance.csv` in this directory.

## Evidentiary rule

All recovered material has the status **inherited—not independently replicated**. A recovered crop is evidence of what the original PDF reported; it is not evidence that the underlying result has been reproduced. The rewrite may use these assets temporarily, but empirical claims should retain this inherited status until the rewrite's independent checks reproduce them.

## Extraction and quality summary

- The PDF contains no embedded raster-image objects on any of its 94 pages.
- Figures are composed of vector paths and live PDF text. Each was clipped to a one-page vector PDF and rendered to a 400-DPI PNG companion.
- Figure crops retain titles, axes, ticks, legends, annotations, panel labels, and shading, while excluding the original typeset caption so that the rewrite can supply a native LaTeX caption.
- Tables are live PDF text plus vector rules. Each table crop includes its original caption, full body, and any table-specific footer or note.
- Vector-PDF crops are the fidelity master. PNGs are convenience copies and should not replace the PDF in final typesetting.
- Rerender checks passed for all 40 one-page PDF crops. The rendered dimensions differ from the direct source clips by at most one pixel because the PDF clip edges fall on fractional device pixels.

## Figures

| Label | PDF p. | Panels / content | Asset stem | Intended placement | Recommendation |
|---|---:|---|---|---|---|
| Figure 1 | 5 | Three stacked outcomes: carry total, carry spot, inversion counts | `figure_01_main` | Main paper | Temporary copy; recreate from verified data |
| Figure 2 | 18 | (a) Australian slope; (b) naive/live counts; (c) carry under traded states | `figure_02_main` | Main paper | Temporary copy; recreate from verified data |
| Figure 3 | 25 | Yield and CPI time series with signal/regime bands | `figure_03_main` | Main paper | Temporary copy; recreate from verified data |
| Figure 4 | 26 | Average yield curves in four signal-by-regime cells | `figure_04_main` | Main paper | Temporary copy; recreate from verified data |
| Figure 5 | 33 | Currency spot effect against real-time equity beta | `figure_05_main` | Main paper | Temporary copy; recreate from verified data |
| Figure 6 | 37 | 2x2 local projections: industrial production, leading indicator, rates, carry spot | `figure_06_main` | Main paper | Temporary copy; recreate from verified data |
| Figure 7 | 43 | Cumulative returns of five G10 carry strategies | `figure_07_main` | Main paper | Temporary copy; recreate from verified data |
| Figure 8 | 56 | Cumulative returns of five G10+EM strategies | `figure_08_main` | Main paper | Temporary copy; recreate from verified data |
| Figure A.1 | 73 | G10 and U.S. money-market rates | `figure_a01_appendix` | Online appendix | Temporary copy; recreate from verified data |
| Figure A.2 | 74 | Real-time expanding-window equity betas | `figure_a02_appendix` | Online appendix | Temporary copy; recreate from verified data |
| Figure D.1 | 81 | Naive-count and IYC-signal timelines | `figure_d01_appendix` | Online appendix | Temporary copy; recreate from verified data |
| Figure J.1 | 93 | 2x2 local projections under three designs | `figure_j01_appendix` | Online appendix | Temporary copy; recreate from verified data |

Each figure stem has both `.pdf` and `.png` files under `rewrite/assets/original/`.

## Main-paper tables

| Label | PDF p. | Panels / content | Asset stem | Intended placement | Recommendation |
|---|---:|---|---|---|---|
| Table 1 | 24 | Panel A means; Panel B gaps | `table_01_main` | Main paper | Rebuild in native LaTeX |
| Table 2 | 32 | Currency mechanism; three state groups | `table_02_main` | Main paper | Rebuild in native LaTeX |
| Table 3 | 36 | Per-currency Fama slopes and pooled row | `table_03_main` | Main paper | Rebuild in native LaTeX |
| Table 4 | 39 | Carry/high-beta spot/total conditional moments and effects | `table_04_main` | Main paper | Rebuild; consider landscape or appendix |
| Table 5 | 40 | Conditional quantiles, volatility, and skewness | `table_05_main` | Main paper | Rebuild in native LaTeX |
| Table 6 | 42 | Carry and high-beta strategy panels | `table_06_main` | Main paper | Rebuild in native LaTeX |
| Table 7 | 47 | Four-portfolio horse race | `table_07_main` | Main paper | Rebuild in native LaTeX |
| Table 8 | 49 | Bilateral currency specifications | `table_08_main` | Main paper | Rebuild; strong appendix candidate |
| Table 9 | 50 | EM spot result by currency | `table_09_main` | Main paper | Rebuild in native LaTeX |
| Table 10 | 51 | EM pooled panel | `table_10_main` | Main paper | Rebuild in native LaTeX |
| Table 11 | 53 | Panel A G10; Panel B G10+EM conditional moments | `table_11_main` | Main paper | Rebuild in native LaTeX |
| Table 12 | 55 | Panel A G10; Panel B G10+EM state regressions | `table_12_main` | Main paper | Rebuild in native LaTeX |
| Table 13 | 57 | Panel A moments; Panel B regressions/hazard; Panel C overlays | `table_13_main` | Main paper | Rebuild in native LaTeX |
| Table 14 | 59 | Panels A-D for carry/high-beta spot/total | `table_14_main` | Main paper | Rebuild; do not use the PNG at print scale |

Each table stem has both `.pdf` and `.png` files under `rewrite/assets/original/`. Table crops are provided for audit and temporary visual reuse; native LaTeX is preferable because copied table text cannot reflow and becomes too small quickly.

## Appendix tables

| Label | PDF p. | Panels / content | Asset stem | Intended placement | Recommendation |
|---|---:|---|---|---|---|
| Table A.1 | 72 | Money-market rates by country | `table_a01_appendix` | Online appendix | Rebuild in native LaTeX |
| Table A.2 | 75 | Economic-regime summary | `table_a02_appendix` | Online appendix | Rebuild in native LaTeX |
| Table A.3 | 75 | Currency summary statistics | `table_a03_appendix` | Online appendix | Rebuild in native LaTeX |
| Table C.1 | 79 | Cluster-size grid | `table_c01_appendix` | Online appendix | Rebuild in native LaTeX |
| Table C.2 | 79 | Exit-confirmation grid | `table_c02_appendix` | Online appendix | Rebuild in native LaTeX |
| Table C.3 | 79 | Slope-definition grid | `table_c03_appendix` | Online appendix | Rebuild in native LaTeX |
| Table D.1 | 82 | Tail capture at 1%, 5%, and 10% | `table_d01_appendix` | Online appendix | Rebuild in native LaTeX |
| Table D.2 | 84 | Naive-count repairs and controls | `table_d02_appendix` | Online appendix | Rebuild in native LaTeX |
| Table E.1 | 86 | Two sample halves | `table_e01_appendix` | Online appendix | Rebuild in native LaTeX |
| Table F.1 | 88 | U.S.-inclusive signal/portfolio checks | `table_f01_appendix` | Online appendix | Rebuild in native LaTeX |
| Table G.1 | 89 | Panel A maximal samples; Panel B post-1999 | `table_g01_appendix` | Online appendix | Rebuild in native LaTeX |
| Table H.1 | 91 | Panel A carry composition; Panel B high-beta composition | `table_h01_appendix` | Online appendix | Rebuild; consider landscape |
| Table I.1 | 92 | EM-native cells and wedge regression | `table_i01_appendix` | Online appendix | Rebuild in native LaTeX |
| Table K.1 | 94 | Term-premium-stripped signal | `table_k01_appendix` | Online appendix | Rebuild in native LaTeX |

## QA material

The temporary recovery folder contains:

- Eight contact sheets covering all 94 original PDF pages: `tmp/figure_recovery/contact_sheets/all_pages_*.jpg`.
- One contact sheet for all recovered figures: `tmp/figure_recovery/contact_sheets/recovered_figures_qa.jpg`.
- Four contact sheets for all recovered tables: `tmp/figure_recovery/contact_sheets/recovered_tables_qa_*.jpg`.
- Direct text extraction with PDF-page boundaries: `tmp/figure_recovery/all_pages_text.txt`.
- Page metadata (dimensions, image-object count, vector-drawing count, detected labels): `tmp/figure_recovery/page_metadata.json`.
- Asset dimensions and vector-PDF rerender audit: `tmp/figure_recovery/asset_dimensions.csv` and `tmp/figure_recovery/vector_verification.csv`.

## Visual-quality warnings

1. Table 14 is nearly a full page and is not realistically readable as a raster insertion at normal journal scale. The vector PDF remains sharp, but a native LaTeX reconstruction is required for a polished rewrite.
2. Figures 6 and J.1 use translucent confidence bands. They render correctly, but different PDF engines can produce small antialiasing differences at band overlaps.
3. Figure 2 contains dense annotations across three panels. Do not shrink it aggressively.
4. Figures A.1 and A.2 have many series and compact legends; use full text width in the appendix.
5. Tables 4, 8, 11, 14, and H.1 are especially dense. Their crops are reliable archival references, not recommended final-layout solutions.
6. Caption equations in Tables 3 and 13 are visually intact, but the source PDF's text extraction splits some mathematical glyphs across blocks. Re-type equations from the visual PDF, not from raw extracted text.
