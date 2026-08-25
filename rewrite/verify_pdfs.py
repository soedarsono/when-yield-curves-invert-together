"""Automated preflight checks for the submission-facing paper PDFs.

Visual inspection remains mandatory. These checks catch page-count drift, blank pages,
placeholder text, unresolved references, and common LaTeX log defects before rendering QA.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

from pypdf import PdfReader


FORBIDDEN_TEXT = (
    "Section pending integration",
    "Missing source file",
    "[?]",
)

# These terms are valid in external audit ledgers but signal internal production
# status when they leak into either reader-facing PDF.
FORBIDDEN_META_PATTERNS = {
    "reconstruction label": r"\breconstruct(?:ion|ed|ing)\b",
    "inherited-evidence label": r"\binherited\b",
    "source-PDF label": r"\bsource[ -]pdf\b",
    "source-paper label": r"\bsource paper\b",
    "original-draft label": r"\boriginal draft\b",
    "evidence-status label": r"\bevidence status\b",
    "transcription label": r"\btranscribed\b",
    "workspace reference": r"\bworkspace\b",
    "author-package reference": r"\bauthor package\b",
    "removed Appendix F": r"\bAppendix F\b",
    "removed Appendix G": r"\bAppendix G\b",
}

# Included PDF figures can otherwise leak relative filenames, producer strings,
# and generation timestamps through pdfTeX's low-level PTEX dictionaries even
# when none of that material is visible or text-extractable.
FORBIDDEN_BINARY_MARKERS = {
    b"/PTEX.": "embedded PTEX provenance dictionary",
    b"C:\\\\Users\\\\": "absolute Windows user path",
    b"/Users/": "absolute macOS user path",
    b"Claude workFolder": "personal workspace path",
}

EXPECTED_APPENDICES = {
    "A_signal_algorithm.tex",
    "B_accounting_theory.tex",
    "C_inherited_robustness.tex",
    "D_public_data_checks.tex",
    "E_country_combinations.tex",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_pdf(
    path: Path,
    minimum: int,
    maximum: int | None,
    expected_title: str,
    expected_author: str,
) -> list[str]:
    errors: list[str] = []
    binary = path.read_bytes()
    for marker, label in FORBIDDEN_BINARY_MARKERS.items():
        if marker in binary:
            errors.append(f"{path.name}: contains {label}")
    reader = PdfReader(path)
    metadata = reader.metadata or {}
    if str(metadata.get("/Title", "")).strip() != expected_title:
        errors.append(f"{path.name}: incorrect PDF title metadata")
    if str(metadata.get("/Author", "")).strip() != expected_author:
        errors.append(f"{path.name}: incorrect PDF author metadata")
    count = len(reader.pages)
    if count < minimum:
        errors.append(f"{path.name}: {count} pages; minimum is {minimum}")
    if maximum is not None and count > maximum:
        errors.append(f"{path.name}: {count} pages; maximum is {maximum}")

    for index, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if len(text) < 80:
            errors.append(f"{path.name}: page {index} appears blank or materially underfilled")
        for marker in FORBIDDEN_TEXT:
            if marker in text:
                errors.append(f"{path.name}: page {index} contains placeholder {marker!r}")
        for label, pattern in FORBIDDEN_META_PATTERNS.items():
            if re.search(pattern, text, re.I):
                errors.append(f"{path.name}: page {index} contains {label}")
    return errors


def inspect_submission_sources(root: Path) -> list[str]:
    errors: list[str] = []
    appendix_tex = (root / "online_appendix.tex").read_text(encoding="utf-8")
    appendix_inputs = set(re.findall(r"\\inputsection\{appendix/([^}]+)\}", appendix_tex))
    if appendix_inputs != EXPECTED_APPENDICES:
        errors.append(f"online_appendix.tex: expected A--E only, found {sorted(appendix_inputs)}")
    if r"\nocite{*}" in appendix_tex:
        errors.append("online_appendix.tex: bibliography must remain restricted to cited entries")

    main_bbl = (root / "main.bbl").read_text(encoding="utf-8", errors="replace")
    bibitems = len(re.findall(r"\\bibitem", main_bbl))
    if bibitems != 84:
        errors.append(f"main.bbl: expected 84 source-universe references, found {bibitems}")

    main_sources = "\n".join(
        (root / relative).read_text(encoding="utf-8")
        for relative in (
            "sections/01_introduction.tex",
            "sections/02_setting_measurement.tex",
            "sections/05_mechanism_model_intuition.tex",
        )
    )
    appendix_sources = (root / "appendix/C_inherited_robustness.tex").read_text(encoding="utf-8")
    for figure_id in ("01", "02", "05"):
        if f"figure_{figure_id}_main.pdf" in main_sources:
            errors.append(f"submission sources: copied Figure {figure_id} must use its flattened PNG")
        if f"figure_{figure_id}_main.png" not in main_sources:
            errors.append(f"submission sources: flattened Figure {figure_id} is not included")
    if "figure_06_main.pdf" in appendix_sources:
        errors.append("submission sources: copied Figure 06 must use its flattened PNG")
    if "figure_06_main.png" not in appendix_sources:
        errors.append("submission sources: flattened Figure 06 is not included in the appendix")
    return errors


def inspect_mirrored_outputs(root: Path) -> list[str]:
    errors: list[str] = []
    pairs = {
        root / "main.pdf": root.parent / "output" / "pdf" / "When_Yield_Curves_Invert_Together_Main.pdf",
        root / "online_appendix.pdf": root.parent / "output" / "pdf" / "When_Yield_Curves_Invert_Together_Online_Appendix.pdf",
    }
    for source, mirror in pairs.items():
        if not mirror.exists():
            errors.append(f"Missing mirrored output: {mirror}")
        elif sha256_file(source) != sha256_file(mirror):
            errors.append(f"Mirrored output is stale: {mirror.name}")
    return errors


def inspect_log(path: Path) -> list[str]:
    if not path.exists():
        return [f"Missing LaTeX log: {path}"]
    text = path.read_text(encoding="utf-8", errors="replace")
    patterns = {
        "undefined references": r"There were undefined references",
        "undefined citations": r"Citation [`'].+?undefined",
        "multiply defined labels": r"multiply defined",
        "overfull boxes": r"Overfull \\hbox",
    }
    return [f"{path.name}: {name}" for name, pattern in patterns.items() if re.search(pattern, text, re.I)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    root = args.root.resolve()

    errors: list[str] = []
    title = "When Yield Curves Invert Together: Predicting Currency Carry Losses"
    errors.extend(inspect_pdf(root / "main.pdf", minimum=1, maximum=None, expected_title=title, expected_author="Alfredo Effendy"))
    errors.extend(inspect_pdf(root / "online_appendix.pdf", minimum=1, maximum=None, expected_title=f"Online Appendix to {title}", expected_author="Alfredo Effendy"))
    combined = root.parent / "output" / "pdf" / "When_Yield_Curves_Invert_Together_With_Online_Appendix.pdf"
    errors.extend(
        inspect_pdf(
            combined,
            minimum=1,
            maximum=None,
            expected_title=f"{title} — Main Paper and Online Appendix",
            expected_author="Alfredo Effendy",
        )
    )
    if combined.exists():
        combined_pages = len(PdfReader(combined).pages)
        component_pages = len(PdfReader(root / "main.pdf").pages) + len(PdfReader(root / "online_appendix.pdf").pages)
        if combined_pages != component_pages:
            errors.append(f"Combined PDF has {combined_pages} pages; expected {component_pages}")
    errors.extend(inspect_log(root / "main.log"))
    errors.extend(inspect_log(root / "online_appendix.log"))
    errors.extend(inspect_submission_sources(root))
    errors.extend(inspect_mirrored_outputs(root))

    if errors:
        print("PDF preflight failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PDF preflight passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
