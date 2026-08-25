# Alternative JMP v0.3 release manifest

Release date: 2026-08-26

## Reader-facing PDFs

| Artifact | Pages | SHA-256 |
|---|---:|---|
| `Alt_JMP_v0.3.pdf` | 65 | `F6FBB17B919DEBB964E13B9C3DA4FA7BDFA45A2085EEC256C84BEF81E51F601C` |
| `output/pdf/When_Yield_Curves_Invert_Together_Main.pdf` | 38 | `C0649352C586028751BFAEA59C180393B6B84CF713BC6D18905007C76A81068E` |
| `output/pdf/When_Yield_Curves_Invert_Together_Online_Appendix.pdf` | 27 | `8340A9E7AF3EEBAF3A564E583DA9E1D548A217473D92CE71C323F1C4B8BE633E` |
| `output/pdf/When_Yield_Curves_Invert_Together_With_Online_Appendix.pdf` | 65 | `F6FBB17B919DEBB964E13B9C3DA4FA7BDFA45A2085EEC256C84BEF81E51F601C` |

The root release PDF is byte-for-byte identical to the combined PDF in `output/pdf/`.

## Release gates

- PDF preflight: passed.
- Automated tests: 39 passed under `unittest` discovery.
- Main-paper length: 38 pages.
- Online appendix: 27 pages, Appendices A--E.
- Combined release: 65 pages.
- Main numbered equations: 10; online-appendix numbered equations: 11.
- References: the original 84-entry bibliography is retained; no new academic references were added.
- Production-language scan: no self-assessment, scoring language, source-PDF labels, or drafting markers occur in either reader-facing PDF.
- Transformation, copied-material, equation-provenance, claim, and data-purpose ledgers are included outside the reader-facing PDFs.

## Executable public checks

The one-command workflow runs the public-input audit, delivered-easing mechanism analysis, country-combination screen, descriptive source-reported rule neighborhood, current-vintage public 10-year-minus-3-month challenge, generated-table renderer, 39 tests, PDF build, page rendering, and PDF preflight:

```powershell
.\run_reproduction.ps1
```

For an existing hash-audited raw-data snapshot, use `.\run_reproduction.ps1 -UseExistingData`.

The public 10-year-minus-3-month result is adverse sensitivity evidence, not validation. The baseline-like rule produces a -3.20-percentage-point annualized active-minus-inactive log spot-return-proxy difference (raw circular-shift reference value 0.335; common-calendar maximum-$|z|$ reference value 1.000 across the declared 64-rule family). Forty-one of 64 estimates are negative, no rule meets the 5-percent family reference criterion, and the public-proxy state contains 18 episodes. Family-wise interpretation is conditional on simultaneous cyclic-shift exchangeability.

## Generated-table and manifest linkage

`research_pipeline/src/render_v03_public_tables.py` converts the public-proxy CSV outputs into the `rewrite/generated/tables/v03_*.tex` files included by the LaTeX sources and mirrors the specification-curve figure. The public-proxy run manifest hashes those paper-facing outputs together with the raw inputs, code, configuration, and machine-readable results.

Run manifests:

- `research_pipeline/outputs/mechanism/run_manifest.json`
- `research_pipeline/outputs/country_combinations/run_manifest.json`
- `research_pipeline/outputs/v03/source_reported_neighborhood/run_manifest.json`
- `research_pipeline/outputs/v03/yield_proxy/run_manifest.json`

## Verification boundary

The declared public-data analyses are executable. The 10-year-minus-3-month audit uses current-vintage public series and a spot-only outcome; it is not an executable forward-return replication. The core 10-year-minus-2-year yield-curve and currency estimates remain auditable transcriptions of the original PDF because the original analytical panel and code were not available. The repository does not represent those transcribed estimates as independently reproduced results.
