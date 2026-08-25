#!/usr/bin/env python3
"""Download official public datasets used by the IYC paper validation pipeline.

The downloader is deliberately conservative:

* it uses only source URLs declared in config/sources.json;
* it keeps immutable raw files rather than silently transforming them;
* it writes a SHA-256 manifest with retrieval time, status, and source URL;
* it retries transient failures but records permanent failures;
* it does not require third-party Python HTTP packages.

Run from the project root:

    python research_pipeline/src/download_public_data.py

Use ``--source bis_policy_rates`` to fetch only one source group and ``--force``
to replace an existing raw file after preserving the previous hash in the run log.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "research_pipeline" / "config" / "sources.json"
RAW_ROOT = PROJECT_ROOT / "research_pipeline" / "data" / "raw"
MANIFEST_PATH = PROJECT_ROOT / "research_pipeline" / "data" / "download_manifest.jsonl"
USER_AGENT = "IYC-research-replication/0.1 (academic research; contact author listed in paper)"


@dataclass
class DownloadRecord:
    source_group: str
    url: str
    output_path: str
    retrieved_at_utc: str
    status: str
    bytes: int | None = None
    sha256: str | None = None
    content_type: str | None = None
    error: str | None = None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_path(path: Path) -> str:
    """Return the project-relative, platform-independent manifest key."""
    return path.relative_to(PROJECT_ROOT).as_posix()


def safe_name_from_url(url: str, fallback: str) -> str:
    name = Path(urllib.parse.urlparse(url).path).name
    if not name or name.startswith("."):
        return fallback
    return name


def fetch(
    *,
    source_group: str,
    url: str,
    output_path: Path,
    accept: str | None,
    force: bool,
    retries: int = 4,
) -> DownloadRecord:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists() and not force:
        return DownloadRecord(
            source_group=source_group,
            url=url,
            output_path=manifest_path(output_path),
            retrieved_at_utc=utc_now(),
            status="cached",
            bytes=output_path.stat().st_size,
            sha256=sha256_file(output_path),
        )

    headers = {"User-Agent": USER_AGENT}
    if accept:
        headers["Accept"] = accept

    partial = output_path.with_suffix(output_path.suffix + ".part")
    last_error: str | None = None
    for attempt in range(1, retries + 1):
        try:
            request = urllib.request.Request(url, headers=headers)
            context = ssl.create_default_context()
            with urllib.request.urlopen(request, timeout=90, context=context) as response:
                content_type = response.headers.get("Content-Type")
                with partial.open("wb") as handle:
                    shutil.copyfileobj(response, handle)
            os.replace(partial, output_path)
            return DownloadRecord(
                source_group=source_group,
                url=url,
                output_path=manifest_path(output_path),
                retrieved_at_utc=utc_now(),
                status="downloaded",
                bytes=output_path.stat().st_size,
                sha256=sha256_file(output_path),
                content_type=content_type,
            )
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if partial.exists():
                partial.unlink()
            if attempt < retries:
                time.sleep(min(2 ** attempt, 15))

    return DownloadRecord(
        source_group=source_group,
        url=url,
        output_path=manifest_path(output_path),
        retrieved_at_utc=utc_now(),
        status="failed",
        error=last_error,
    )


def iter_jobs(config: dict, selected: set[str] | None) -> Iterable[tuple[str, str, Path, str | None]]:
    for group, spec in config.items():
        if selected and group not in selected:
            continue
        if not spec.get("enabled", True):
            continue
        group_dir = RAW_ROOT / group
        accept = spec.get("accept")

        for index, url in enumerate(spec.get("urls", []), start=1):
            declared_names = spec.get("filenames", [])
            fallback = declared_names[index - 1] if index <= len(declared_names) else f"download_{index}.dat"
            name = safe_name_from_url(url, fallback)
            yield group, url, group_dir / name, accept

        template = spec.get("api_template")
        for key in spec.get("keys", []):
            url = template.format(key=urllib.parse.quote(key, safe="."))
            yield group, url, group_dir / f"{key.replace('.', '_')}.csv", accept

        for series_id, url in spec.get("series", {}).items():
            yield group, url, group_dir / f"{series_id}.csv", accept


def extract_cftc_archives(records: list[DownloadRecord]) -> list[DownloadRecord]:
    extracted_records: list[DownloadRecord] = []
    output_dir = RAW_ROOT / "cftc_legacy_futures" / "extracted"
    output_dir.mkdir(parents=True, exist_ok=True)
    for record in records:
        if record.source_group != "cftc_legacy_futures" or record.status == "failed":
            continue
        archive = PROJECT_ROOT / record.output_path
        if archive.suffix.lower() != ".zip" or not archive.exists():
            continue
        try:
            with zipfile.ZipFile(archive) as bundle:
                for member in bundle.infolist():
                    member_name = Path(member.filename).name
                    if not member_name:
                        continue
                    destination = output_dir / f"{archive.stem}__{member_name}"
                    if not destination.exists():
                        with bundle.open(member) as source, destination.open("wb") as target:
                            shutil.copyfileobj(source, target)
                    extracted_records.append(
                        DownloadRecord(
                            source_group="cftc_legacy_futures_extracted",
                            url=record.url + "#" + member.filename,
                            output_path=manifest_path(destination),
                            retrieved_at_utc=utc_now(),
                            status="extracted",
                            bytes=destination.stat().st_size,
                            sha256=sha256_file(destination),
                            content_type="application/octet-stream",
                        )
                    )
        except (zipfile.BadZipFile, OSError) as exc:
            extracted_records.append(
                DownloadRecord(
                    source_group="cftc_legacy_futures_extracted",
                    url=record.url,
                    output_path=manifest_path(archive),
                    retrieved_at_utc=utc_now(),
                    status="failed",
                    error=f"{type(exc).__name__}: {exc}",
                )
            )
    return extracted_records


def append_manifest(records: list[DownloadRecord]) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("a", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(asdict(record), ensure_ascii=True, sort_keys=True) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--source", action="append", help="Source group to fetch; may be repeated.")
    parser.add_argument("--force", action="store_true", help="Replace existing raw downloads.")
    parser.add_argument("--no-extract", action="store_true", help="Do not extract downloaded CFTC ZIP files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    with args.config.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    selected = set(args.source) if args.source else None
    unknown = selected - set(config) if selected else set()
    if unknown:
        print(f"Unknown source group(s): {', '.join(sorted(unknown))}", file=sys.stderr)
        return 2

    records: list[DownloadRecord] = []
    for group, url, output_path, accept in iter_jobs(config, selected):
        print(f"[{group}] {url}")
        record = fetch(
            source_group=group,
            url=url,
            output_path=output_path,
            accept=accept,
            force=args.force,
        )
        records.append(record)
        print(f"  -> {record.status}: {record.output_path}")

    if not args.no_extract:
        records.extend(extract_cftc_archives(records))
    append_manifest(records)

    failures = [record for record in records if record.status == "failed"]
    downloaded = [record for record in records if record.status in {"downloaded", "cached", "extracted"}]
    print(f"Completed: {len(downloaded)} usable records, {len(failures)} failures")
    for failure in failures:
        print(f"FAILED {failure.source_group}: {failure.url}: {failure.error}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
