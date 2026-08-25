#!/usr/bin/env python3
"""Small SDMX access probe for BIS, OECD, ECB, or another declared endpoint.

This utility helps a research agent inspect an unfamiliar official dataflow before
adding it to sources.json. It downloads a URL with a caller-specified Accept header,
prints response metadata, and optionally saves the body. It does not guess series
codes or scrape rendered webpages.
"""

from __future__ import annotations

import argparse
import hashlib
import ssl
import urllib.request
from pathlib import Path


DEFAULT_ACCEPT = "application/vnd.sdmx.data+csv;version=1.0.0"
USER_AGENT = "IYC-research-replication/0.1 (academic research)"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("--accept", default=DEFAULT_ACCEPT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--preview-bytes", type=int, default=1200)
    args = parser.parse_args()

    request = urllib.request.Request(
        args.url,
        headers={"Accept": args.accept, "User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=90, context=ssl.create_default_context()) as response:
        body = response.read()
        print(f"status={response.status}")
        print(f"content_type={response.headers.get('Content-Type')}")
        print(f"bytes={len(body)}")
        print(f"sha256={hashlib.sha256(body).hexdigest()}")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(body)
        print(f"saved={args.output.resolve()}")
    preview = body[: args.preview_bytes].decode("utf-8", errors="replace")
    print("--- preview ---")
    print(preview)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
