# Alternative JMP v0.2 release manifest

Release date: 2026-08-26

## Reader-facing PDFs

| Artifact | Pages | SHA-256 |
|---|---:|---|
| `Alt_JMP_v0.2.pdf` | 44 | `D6B2BCD6EB6544B41CA605C5BE2D84E62352BA75A2A64E64C153EE081097DEFD` |
| `output/pdf/When_Yield_Curves_Invert_Together_Main.pdf` | 26 | `6D480731D9F477FC2D64DDC4FC8FD0371E41757285B211A220C5BAED79A2FFFF` |
| `output/pdf/When_Yield_Curves_Invert_Together_Online_Appendix.pdf` | 18 | `C8C73E18F0C6461672B1418CCA86784F51D65B03802E962486408BC746BDB2A2` |
| `output/pdf/When_Yield_Curves_Invert_Together_With_Online_Appendix.pdf` | 44 | `D6B2BCD6EB6544B41CA605C5BE2D84E62352BA75A2A64E64C153EE081097DEFD` |

The root release PDF is byte-for-byte identical to the combined PDF in `output/pdf/`.

## Release gates

- PDF preflight: passed.
- Automated tests: 21 passed under `unittest` discovery.
- Main-paper length: 26 pages, including five pages of references.
- Online appendix: 18 pages, Appendices A--E.
- Combined release: 44 pages.
- Main numbered equations: 8.
- References: the original 84-entry bibliography is retained; no new academic references were added.
- Title-page layout: the JEL and keyword lines remain adjacent near the bottom of the page and are visually separated from the abstract.
- Production-language scan: no self-assessment, scoring language, source-PDF labels, or drafting markers occur in either reader-facing PDF.
- Transformation, copied-material, equation-provenance, claim, and data-purpose ledgers are included outside the reader-facing PDFs.

## Verification boundary

The public-data analyses are executable from the declared inputs. The core yield-curve and currency estimates remain auditable transcriptions of the original PDF because the original analytical panel and code were not available. The repository does not represent those transcribed estimates as independently reproduced results.
