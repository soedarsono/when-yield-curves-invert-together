# Original-to-revision transformation ledger

Final audit date: 2026-08-26  
Original: `AI JMP.pdf`, 94 pages  
Final reader-facing documents: 26-page main paper, 18-page online appendix, and 44-page combined edition  
Machine-readable record: `original_to_rewrite_transformation_ledger.csv`

This ledger records where every original top-level section and Appendix A--K moved, what was condensed or deleted, and why. It also identifies new analyses and objects that have no source-paper antecedent. Figure/table-level copying is tracked separately in `copied_material_ledger.csv`; equation-level changes are tracked in `equation_provenance_ledger.csv`.

## High-level reorganization

| Original material | Final location | Disposition |
|---|---|---|
| Abstract and Introduction, pp. 1--10 | Main pp. 1--5 | Rewritten around one predictive measurement result, exposure ordering, and the in-sample specification risk |
| Accounting and model, pp. 11--27 | Main pp. 6--7 and 18--19; Appendix B, pp. 4--6 | Main mathematics reduced to the objects needed for measurement and one candidate compensation restriction; derivations moved online |
| Data, signal, and inference, pp. 28--30 | Main pp. 6--11; Appendix A, pp. 3--4 | Timing, fresh entry, confirmed release, missing data, notation, and episode inference made explicit |
| Beta, UIP, and macro mechanism, pp. 31--37 | Main pp. 14--18; Appendix C, pp. 10--12 | Exposure ordering promoted; imprecise conditional-UIP and production estimates reported as such; local-projection figure moved online |
| Headline return evidence, pp. 38--49 | Main pp. 12--14; Appendix C, pp. 7--9 | Main result, distribution shift, exact-one/exact-two contrast, U.S. benchmark, and timing condensed |
| Emerging-market results, pp. 50--55 | Main p. 17; Appendix C, pp. 9--10 | Directional out-of-construction evidence and compensation comparison restored; strategy overlays removed |
| Equity allocation, pp. 55--57 | No reader-facing destination | Removed as a separate application |
| Risk controls and robustness, pp. 58--61 | Main pp. 13--14 and 20; Appendix C, pp. 8--10 | Retained as spanning and measurement diagnostics; causal language removed |
| Original Conclusion and references, pp. 62--71 | Main pp. 21--26 | Conclusion rewritten without self-assessment; all 84 references retained |
| Original Appendices A--E, pp. 72--87 | Main pp. 6--20; Online Appendices A--C, pp. 3--12 | Essential definitions and diagnostics integrated; full source crops remain external |
| Original Appendices F--G, pp. 88--89 | External ledgers/assets only | Excluded from both PDFs as requested; no reader-facing MSCI robustness claim |
| Original Appendix H, p. 91 | Main pp. 16--17 | Portfolio persistence used to distinguish standing exposure from mechanical resorting |
| Original Appendix I, p. 92 | No reader-facing destination | Emerging-market-native regime removed |
| Original Appendices J--K, pp. 93--94 | Main pp. 13--20; Appendix C, pp. 9--12 | Local-projection timing and asymmetric term-premium results condensed |

## New material

| New object | Final location | Evidentiary status |
|---|---|---|
| Notation and timing table | Main p. 9 | Editorial clarification; no new empirical claim |
| Public synchronized delivered-easing check | Appendix D, pp. 12--16 | Executable downstream mechanism check; not a replication of the inversion state |
| Public pair/triple country screen | Main p. 20; Appendix E, pp. 17--18 | Exploratory sensor-versus-risk-bearer hypothesis with family-wide maxT correction |
| Synthetic path-dependence experiment | Repository only | Non-evidentiary diagnostic; removed from reader-facing PDFs |

## Material removed rather than merely moved

- Trading overlays, anti-carry rules, and overwrite strategies were removed because feasible forward returns, implementation costs, and frozen construction are unavailable.
- The stock-market allocation application was removed because it does not sharpen the international-finance contribution.
- Strong iid/identical-loading threshold propositions were removed because they are unnecessary for the empirical design and depend on restrictive calibration.
- Repetitive table narration, repeated roadmaps, generic literature catalogues, and duplicate limitation language were deleted.
- Full source crops that remain useful for audit but are not readable at publication scale were kept outside both PDFs.
- Original Appendices F and G remain external. Table G.1 is not used to claim general beta-benchmark robustness.
- Seven unreferenced rewrite scaffolds were deleted at release: three integration wrappers, one superseded public-data section, one duplicate conclusion wrapper, the reader-facing simulation appendix draft, and the appendix drafting bank. Their removal does not change either final PDF; executable simulation diagnostics remain repository-only.

## Economic spine after reorganization

The final ordering separates four objects that were previously dispersed:

1. **Breadth locates the state:** exactly one live inversion has positive carry returns, whereas synchronized live inversions predict losses.
2. **Exposure locates the losses:** high-rate and high-equity-beta currencies bear the larger depreciations.
3. **Timing distinguishes signal from delivery:** the yield-curve state is predictive; the public policy-easing exercise is downstream and contemporaneous.
4. **Compensation determines total returns:** G10 and G10-plus-EM portfolios can experience similar spot repricing but different total outcomes because predetermined interest income differs.

## Verification boundary

The public-data analyses and their ledgers are executable from declared inputs. The core yield-curve and currency estimates are visible-source transcriptions because the original analytical panel and code are absent. The final PDFs do not contain production labels; this external ledger preserves that evidentiary distinction.
