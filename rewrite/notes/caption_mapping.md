# Caption mapping for reused source-PDF images

Source: `AI JMP.pdf`. Destination audit date: 2026-08-26.

This memo covers every source-PDF crop that is referenced by a manuscript or external-only appendix source file: four main-PDF figures and eleven Appendix G images (four figures and seven tables). It does not edit or prescribe manuscript text. Original captions below are transcribed from the PDF/source text with OCR line-break hyphenation repaired and mathematical symbols normalized for readability. Table crops retain their source captions inside the crop; figure crops omit the source caption and therefore receive a native LaTeX caption at the destination.

## Included in the main PDF

### Source Figure 1 (PDF p. 5)

**Original caption**

> Figure 1: The carry trade and the IYC signal. Top to bottom: the carry portfolio's cumulative total return, its cumulative spot return, and two counts of inverted G10 curves (the nine non-dollar members) - the naive count (light), curves with the 10-year yield below the 2-year this month, and the IYC signal count (dark), the inversions the signal counts, entered fresh and not yet confirmed re-steepened - with the cluster threshold of two dotted. IYC signal episodes are shaded throughout; triangles mark each return series' own bottom-5% months, the crash months (the two sets share 22 of their 23), and black stars its bottom-1% months, the five worst of the sample, all of which fall inside the signal's lagged state (three of them - March 1995, October 2008, and March 2020 - are the first month after a shaded band, when the lagged state is still on). The shading is, by construction, the months in which the signal count is at least two, and the gap between the two bars is the signal's discipline in both directions. Standing naive inversions with no fresh entry are not counted (1991-92, 2023-24), and counted inversions persist through the delivery phase after the naive count has receded (early 1995, late 2008, early 2020) - the latch at work. Shading is the information-time state; every regression uses it lagged one month.

**Destination mapping**

- Submission asset: `rewrite/assets/original/figure_01_main.png` (flattened 400-DPI crop; vector recovery master retained externally)
- Destination: `rewrite/sections/01_introduction.tex`
- Label: `fig:inherited_overview`
- Native caption: “The carry trade and the IYC signal. Top to bottom: the carry portfolio's cumulative total return, its cumulative spot return, and two counts of inverted G10 curves (the nine non-dollar members)---the naive count (light), curves with the 10-year yield below the 2-year this month, and the IYC signal count (dark), the inversions the signal counts, entered fresh and not yet confirmed re-steepened---with the cluster threshold of two dotted. IYC signal episodes are shaded throughout; triangles mark each return series' own bottom-5-percent months (the two sets share 22 of their 23), and black stars mark its bottom-1-percent months, all five of which fall inside the signal's lagged state. Standing naive inversions with no fresh entry are not counted, whereas counted inversions persist through the delivery phase after the naive count has receded. Shading is the information-time state; every regression uses it lagged one month.”
- Mapping assessment: adapted from the longer source caption; preserves the panel ordering, visual encodings, timing convention, and core latch interpretation while omitting date-specific examples.

### Source Figure 2 (PDF p. 18)

**Original caption**

> Figure 2: One live inversion and what it buys, 2005:07-2008:12. (a) The Australian 10Y-2Y slope. The naive inversion is the grey bar (slope below zero); the live period under the paper's rule is shaded, from the month after the inversion is observed (▼) to the release (×) after two consecutive steepening months (circles). The curve is released in January 2007 while still inverted and stays naively inverted for another eighteen months. (b) Across the nine curves, the naive inversion count and the IYC live count N_t against the cluster threshold of two. (c) The carry trade's cumulative total return (solid) and its spot component (dashed), with the months in which each traded state is on shaded (states lagged one month). From January to June 2007 the naive state is on and the IYC state is off, and the carry trade earns +9.7%; in October 2008 the naive state is off (the count had fallen to one in September and falls to zero in October) while the IYC state is still on, and the carry trade loses 11.6%.

**Destination mapping**

- Submission asset: `rewrite/assets/original/figure_02_main.png` (flattened 400-DPI crop; vector recovery master retained externally)
- Destination: `rewrite/sections/02_setting_measurement.tex`
- Label: `fig:inherited_latch`
- Native caption: “One live inversion and what it buys, 2005:07--2008:12. Panel (a) shows the Australian 10Y--2Y slope. The naive inversion is the grey bar; the live period under the paper's rule is shaded from the month after entry is observed to release after two consecutive steepening months. The curve is released in January 2007 while still inverted and stays naively inverted for another eighteen months. Panel (b) plots the naive inversion count and the IYC live count across the nine curves against the cluster threshold of two. Panel (c) plots the carry trade's cumulative total return (solid) and spot component (dashed), with each traded state lagged one month. From January to June 2007 the naive state is on and the IYC state is off, and carry earns 9.7 percent; in October 2008 the naive state is off while the IYC state remains on, and carry loses 11.6 percent.”
- Mapping assessment: closely adapted from the source caption; retains the panel definitions, release rule, state timing, and two numerical episode comparisons.

### Source Figure 5 (PDF p. 33)

**Original caption**

> Figure 5: On-signal spot effect against equity beta, one point per currency. Circles and solid fit are for the full signal (slope -60, R^2 = 0.77), squares and dashed fit for the non-downcurve months (slope -106, R^2 = 0.84). Both intercepts are economically zero, so currencies without growth exposure do not crash on the signal.

**Destination mapping**

- Submission asset: `rewrite/assets/original/figure_05_main.png` (flattened 400-DPI crop; vector recovery master retained externally)
- Destination: `rewrite/sections/05_mechanism_model_intuition.tex`
- Label: `fig:inherited_beta_gradient`
- Native caption: “On-signal spot effect against equity beta, one point per currency. Circles and the solid fit use the full signal (slope $-60$, $R^2=0.77$); squares and the dashed fit use non-downcurve signal months (slope $-106$, $R^2=0.84$). Both fitted intercepts are economically near zero. With nine currencies, the fitted lines should be read as descriptive exposure gradients.”
- Mapping assessment: closely tracks the source's visual encodings and fitted statistics while replacing the overstrong “do not crash” conclusion with descriptive language.

### Source Figure 6 (PDF p. 37)

**Original caption**

> Figure 6: What follows a signal month. Local projections of the cumulative change from t - 1 to t - 1 + h on the lagged signal state, for h = 1 to 12 months, 1988:01-2026:02, of the G10 activity proxies of Section 3 - industrial production for the seven currency countries that publish it monthly and the OECD composite leading indicator for the five it covers, each the cumulated average of the countries' monthly log changes (100 × log) - the average G10 one-month money-market rate (percentage points), and the carry trade's spot leg (cumulative %). Bands are 90% Newey-West intervals with h + 1 lags; red markers have a wild cluster bootstrap p below 0.10 with signal runs as clusters. Appendix J repeats the projections on the onset month of each run and with lagged controls.

**Destination mapping**

- Submission asset: `rewrite/assets/original/figure_06_main.png` (flattened 400-DPI crop; vector recovery master retained externally)
- Destination: `rewrite/sections/05_mechanism_model_intuition.tex`
- Label: `fig:inherited_local_projections`
- Native caption: “What follows a signal month. The panels report local projections of the cumulative change from $t-1$ to $t-1+h$ on the lagged signal state for horizons $h=1,\ldots,12$ over 1988:01--2026:02. Outcomes are G10 industrial production, the G10 composite leading indicator, the average G10 one-month money-market rate, and the carry trade's spot leg. Bands are 90-percent Newey--West intervals with $h+1$ lags; colored markers denote a wild-cluster-bootstrap $p$-value below 0.10 with signal runs as clusters.”
- Mapping assessment: closely tracks the source design while retaining the full horizon, sample, outcome, interval, and bootstrap-marker definitions.

## Native table transcriptions in current PDFs

These destination captions are synchronized directly from the three generated LaTeX files. The underlying rows are selected and reformatted from source Table 4 or Table E.1, as recorded in `copied_material_ledger.csv`.

| Source | Destination file and label | Current destination caption | Inclusion |
|---|---|---|---|
| Table 4, p. 39 | `rewrite/generated/tables/inherited_headline.tex`, `tab:inherited-headline` | “The carry trade in and out of the IYC signal” | Main PDF only |
| Table 4, p. 39 | `rewrite/generated/tables/inherited_tail_robustness.tex`, `tab:inherited-excrash` | “State effects after removing bottom-decile months” | Main PDF and online appendix PDF |
| Table E.1, p. 86 | `rewrite/generated/tables/inherited_split_sample.tex`, `tab:inherited-halves` | “The headline estimates in two halves of the sample” | Main PDF and online appendix PDF |

## External-only rewrite Appendix G (excluded from both current PDFs)

`rewrite/appendix/G_additional_inherited_exhibits.tex` is not input by `rewrite/main.tex` or `rewrite/online_appendix.tex`. Every mapping in this section is therefore external-only. Rewrite Appendix F (`rewrite/appendix/F_data_provenance.tex`) is likewise excluded but contains no reused image.

### Source Figure A.1 (PDF p. 73)

**Original caption**

> Figure A.1: One-month money-market rates, 1988-2026, for the nine G10 currencies (warm colors for the persistent high-rate bloc AU, NZ, NO, SE, GB; cool colors for EU, CH, JP; green for CA) and the U.S. (black, dashed).

**Destination mapping**

- Asset: `rewrite/assets/original/figure_a01_appendix.pdf`
- Destination label: `fig:recovered-rates`
- Native caption: “Money-market rates in the inherited construction (source Figure A.1)”
- Mapping assessment: adapted and substantially shortened; the source color/line key remains visible in the crop.

### Source Figure A.2 (PDF p. 74)

**Original caption**

> Figure A.2: Real-time equity betas, the expanding-window estimates beta-hat_i,t from (3), with the same color scheme as Figure A.1. The commodity currencies stay at the top of the ranking and the funding currencies at the bottom throughout the sample.

**Destination mapping**

- Asset: `rewrite/assets/original/figure_a02_appendix.pdf`
- Destination label: `fig:recovered-betas`
- Native caption: “Real-time expanding-window equity betas (source Figure A.2)”
- Mapping assessment: adapted and shortened; omits the source's substantive ranking claim from the caption.

### Source Tables C.1-C.3 (PDF p. 79)

**Original captions**

> Table C.1: Cluster-size grid: the state defined by the number of live inversions - at least n (n = 1, 2, 3, 4) and exactly n (n = 1, 2) - with the identical per-curve entry and exit rules. State regressions y_t = a + b 1{state}_{t-1} + e_t as in Table 4 (bare, 1988:01-2026:02; wild bootstrap p on the respective state's episodes).

> Table C.2: Exit-confirmation grid: the signal rebuilt with the exit requiring K consecutive re-steepening months (K = 1, 2, 3), identical entry rule. Specification as in Table C.1.

> Table C.3: Slope-definition robustness: the signal rebuilt on 10Y-3M slopes instead of 10Y-2Y, identical entry and exit rules. Specification as in Table C.1.

**Destination mapping**

- Assets: `table_c01_appendix.pdf`, `table_c02_appendix.pdf`, and `table_c03_appendix.pdf`
- Destination: three unlabeled centered images in `rewrite/appendix/G_additional_inherited_exhibits.tex`
- Caption handling: the original caption is embedded verbatim in each table crop; no replacement LaTeX caption or label is supplied. Nearby prose describes them as the cluster-size, exit-confirmation, and slope-definition variants.
- Mapping assessment: visual content and caption are verbatim crops; the surrounding interpretation is adapted and explicitly calls the set a local specification neighborhood.

### Source Figure D.1 (PDF p. 81)

**Original caption**

> Figure D.1: How long each classifier is on. The naive count (at least 2 of 9 inverted, 165 months, top) is shown against this paper's signal (92 months, bottom), 1988-2026. The raw count stays on through long stretches in which nothing happens - most visibly 1988-93, 2006, and 2022-24 - while the signal's episodes are shorter and end with the re-steepening confirmation.

**Destination mapping**

- Asset: `rewrite/assets/original/figure_d01_appendix.pdf`
- Destination label: `fig:recovered-counts`
- Native caption: “Naive-count and latched-state timelines (source Figure D.1)”
- Mapping assessment: adapted and substantially shortened; the counts and episode interpretation remain visible in the crop.

### Source Table D.1 (PDF p. 82)

**Original caption**

> Table D.1: Tail capture per classifier. The table reports how much of the carry trade's worst months each state contains, against how much calendar it occupies. Concentration = capture share / time share; tail months are the full-sample worst 1%, 5%, and 10% of carry total returns, 1988:01-2026:02; all states lagged one month.

**Destination mapping**

- Asset: `rewrite/assets/original/table_d01_appendix.pdf`
- Destination: unlabeled centered image in `rewrite/appendix/G_additional_inherited_exhibits.tex`
- Caption handling: original caption remains embedded in the crop; the destination adds the note “Tail capture at the 1, 5, and 10 percent thresholds, source Table D.1.”
- Mapping assessment: verbatim table/caption crop with an adapted source note.

### Source Table D.2 (PDF p. 84)

**Original caption**

> Table D.2: Repairing the naive count. State regressions y_t = a + b 1{state}_{t-1} + e_t as in Table 4, with the conditioning variable the naive count, the count restricted to non-downcurve months, the count weighted by 1/age of the standing cluster, and the paper's signal (with and without the same filter); bare, 1988:01-2026:02. Wild bootstrap p on the respective state's episodes.

**Destination mapping**

- Asset: `rewrite/assets/original/table_d02_appendix.pdf`
- Destination: unlabeled centered image in `rewrite/appendix/G_additional_inherited_exhibits.tex`
- Caption handling: original caption remains embedded in the crop; the destination adds the note “Naive-count repairs and controls, source Table D.2.”
- Mapping assessment: verbatim table/caption crop with an adapted source note.

### Source Table E.1 (PDF p. 86)

**Original caption**

> Table E.1: The headline in the two halves of the sample. State regressions y_t = a + b 1{signal}_{t-1} + e_t (%/yr; no controls) estimated separately on 1988:01-2004:12 and 2005:01-2026:02, with the episode-clustered t and the wild cluster bootstrap p on the half's signal episodes (B = 9,999); stars by the wild p. The footer reports each half's months, signal months, episodes, and how many of its three worst carry months fall inside the lagged state.

**Destination mapping**

- Asset: `rewrite/assets/original/table_e01_appendix.pdf`
- Destination: unlabeled centered image in `rewrite/appendix/G_additional_inherited_exhibits.tex`
- Caption handling: original caption remains embedded in the crop; the destination adds a source note that characterizes the split as conditional on a full-sample-designed rule rather than historical out-of-sample validation.
- Mapping assessment: verbatim table/caption crop with an adapted cautionary note. A separate selected native transcription is mapped in the copied-material ledger.

### Source Figure J.1 (PDF p. 93)

**Original caption**

> Figure J.1: Three designs for the local projections of Figure 6. Circles are the baseline state design, squares the onset design (the first month of each signal run, fifteen events), and triangles the controlled design (the state with its own lag and three lags of the outcome's monthly change); 1988:01-2026:02. Bands are 90% Newey-West intervals with h + 1 lags, and red markers have a wild cluster bootstrap p below 0.10 with signal runs as clusters.

**Destination mapping**

- Asset: `rewrite/assets/original/figure_j01_appendix.pdf`
- Destination label: `fig:recovered-lp-variants`
- Native caption: “Local projections under three inherited designs (source Figure J.1)”
- Mapping assessment: adapted and shortened; the destination source note says the confidence bands and markers have not been regenerated.

### Source Table K.1 (PDF p. 94)

**Original caption**

> Table K.1: The signal rebuilt on term-premium-stripped slopes. Each country's 10Y-2Y slope is stripped of its fitted exposure to the U.S. ACM slope term premium, the IYC rule is rebuilt on the stripped slopes and lagged one month, and the rebuilt state is split by the downcurve regime. Cells are state regressions y_t = a + b 1{state}_{t-1} + e_t of the carry and high-beta portfolios' spot and total returns (annualized, %/yr) against all other months; the wedge row is the within-signal regression of the return on the downcurve dummy on the rebuilt state's months. Wild cluster bootstrap p on the state's runs in brackets (B = 9,999), stars by that p; 1988:01-2026:02.

**Destination mapping**

- Asset: `rewrite/assets/original/table_k01_appendix.pdf`
- Destination: unlabeled centered image in `rewrite/appendix/G_additional_inherited_exhibits.tex`
- Caption handling: original caption remains embedded in the crop; the destination adds the note “Term-premium-stripped signal, source Table K.1” and cautions that a common U.S. ACM component does not remove country-specific foreign term premia.
- Mapping assessment: verbatim table/caption crop with an adapted cautionary note.

## Excluded source Appendix F/G audit crops

The original PDF's Table F.1 (`table_f01_appendix.*`, p. 88) and Table G.1 (`table_g01_appendix.*`, p. 89) were recovered and hashed but are not referenced by any rewrite source file. They are external audit assets and are excluded from both current PDFs. Their improved captions, crop rectangles, filenames, and hashes are recorded in `copied_material_ledger.csv`.
