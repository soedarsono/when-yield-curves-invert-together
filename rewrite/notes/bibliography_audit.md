# Bibliography-universe audit

Audit date: 2026-08-25  
Source reference section: `AI JMP.pdf`, pp. 64-71 (PDF pages), cross-checked against `tmp/orchestration/source_full.txt`  
Target: `rewrite/references.bib`

## Result

- Source-PDF reference universe: **84 entries**.
- Pre-audit BibTeX universe: **77 entries**.
- Pre-audit extras relative to the source PDF: **none**.
- Pre-audit missing entries: **7**.
- Post-audit BibTeX universe: **84 entries**.
- Post-audit extras: **none**.
- Post-audit missing entries: **none**.
- Duplicate BibTeX keys after the additions: **none**.
- Uncertain source-to-entry identity matches: **none**. Every target entry can be matched on author, year, and title.

The audit is a bibliography-universe audit, not a citation-usage audit. Both current PDF entry points use `\nocite{*}` or the complete bibliography file, so the intended universe is the source paper's full reference list rather than only keys cited in rewritten prose.

## Added entries

| BibTeX key | Source-PDF reference | Publication metadata added |
|---|---|---|
| `baekLeeOhLee2020` | Baek, Lee, Oh, and Lee (2020), “Yield Curve Risks in Currency Carry Forwards” | *Journal of Futures Markets* 40(4), 651-670; DOI `10.1002/fut.22091` |
| `bansalDahlquist2000` | Bansal and Dahlquist (2000), “The Forward Premium Puzzle: Different Tales from Developed and Emerging Economies” | *Journal of International Economics* 51(1), 115-144; DOI `10.1016/S0022-1996(99)00039-2` |
| `dreherGrabKostka2020` | Dreher, Gräb, and Kostka (2020), “From Carry Trades to Curvy Trades” | *The World Economy* 43(3), 758-780; DOI `10.1111/twec.12877` |
| `engstromSharpe2019` | Engstrom and Sharpe (2019), “The Near-Term Forward Yield Spread as a Leading Indicator: A Less Distorted Mirror” | *Financial Analysts Journal* 75(4), 37-49; DOI `10.1080/0015198X.2019.1625617` |
| `ilzetzkiReinhartRogoff2019` | Ilzetzki, Reinhart, and Rogoff (2019), “Exchange Arrangements Entering the Twenty-First Century: Which Anchor Will Hold?” | *Quarterly Journal of Economics* 134(2), 599-646; DOI `10.1093/qje/qjy033` |
| `jotikasthiraLeLundblad2015` | Jotikasthira, Le, and Lundblad (2015), “Why Do Term Structures in Different Currencies Co-Move?” | *Journal of Financial Economics* 115(1), 58-83; DOI `10.1016/j.jfineco.2014.09.004` |
| `moench2012` | Mönch (2012), “Term Structure Surprises: The Predictive Content of Curvature, Level, and Slope” | *Journal of Applied Econometrics* 27(4), 574-602; DOI `10.1002/jae.1220` |

The new keys are ASCII, surname-explicit, year-stable, and collision-free. Diacritics in author fields are BibTeX-encoded (`Gr{\"a}b`, `M{\"o}nch`). No reference absent from the source PDF was added.

## Field-level fidelity notes on pre-existing entries

These do **not** create universe-level extras, omissions, or uncertain matches. They are pre-existing metadata-normalization issues that remain visible when the `.bib` is compared literally with the source list:

1. `estrellaMishkin1997` omits the source title's subtitle, “Implications for the European Central Bank.” Author, year, journal, volume, issue, and pages match.
2. `rey2013` identifies the correct chapter and volume, but the source reference also names the “Jackson Hole Economic Policy Symposium”; the current entry stores the volume title and Federal Reserve Bank of Kansas City publisher without that event phrase.
3. Several pre-existing author fields transliterate rather than encode source diacritics, including Jordà (`berge2011`, `jordaTaylor2012`), Söderlind (`christiansen2011`, `ranaldoSoderlind2010`), Rancière (`farhi2015`), Hélène Rey (`mirandaRey2020`, `rey2013`), and Örebro in the institutional note for `kaebiMartins2025`.
4. `mackinnon2023` records “Morten O. Nielsen”; the source rendering shows the middle initial as “Ø.” This is an orthographic fidelity issue, not an identity ambiguity.
5. The source list itself dates Brunnermeier, Nagel, and Pedersen's *NBER Macroeconomics Annual* contribution as 2008. Some publisher/catalog records distinguish the 2008 volume from a 2009 publication date. The existing entry follows the source PDF, which is correct for this source-universe reconstruction.

No changes were made to those 77 pre-existing entries because the requested operation was to reconstruct the missing source-PDF universe and report residual uncertainty, not to globally normalize the existing bibliography.

## Audit method

1. Isolated the source reference section from the local full-text extraction and counted entries by author-year-title boundaries across PDF pages 64-71.
2. Parsed the BibTeX file by entry boundary and compared normalized author/title/year identities.
3. Confirmed that the seven unmatched source entries were exactly the seven requested omissions.
4. Added journal, volume, issue, page, and DOI fields for those seven entries.
5. Re-counted entries and checked for duplicate keys.

