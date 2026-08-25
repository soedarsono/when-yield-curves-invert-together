"""Attach the standalone online appendix to the main-paper PDF."""

from __future__ import annotations

import argparse
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("main", type=Path)
    parser.add_argument("appendix", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    writer = PdfWriter()
    main_reader = PdfReader(args.main)
    appendix_reader = PdfReader(args.appendix)

    for page in main_reader.pages:
        writer.add_page(page)
    appendix_start = len(main_reader.pages)
    for page in appendix_reader.pages:
        writer.add_page(page)

    writer.add_outline_item("Main paper", 0)
    writer.add_outline_item("Online appendix", appendix_start)
    writer.add_metadata(
        {
            "/Title": "When Yield Curves Invert Together: Predicting Currency Carry Losses — Main Paper and Online Appendix",
            "/Author": "Alfredo Effendy",
            "/Subject": "Synchronized international yield-curve inversions and currency carry returns",
        }
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("wb") as handle:
        writer.write(handle)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
