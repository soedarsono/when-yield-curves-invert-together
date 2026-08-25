#!/usr/bin/env python3
"""Create a compact, reproducible audit of downloaded public data.

The audit is descriptive only. It verifies that files exist, records schemas and
date coverage where CSV parsing is unambiguous, and flags download failures. It
does not declare a dataset analytically valid; that decision belongs in the
data-purpose ledger after timing, units, and merge logic are reviewed.
"""

from __future__ import annotations

import csv
import hashlib
import json
import urllib.parse
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PIPELINE_ROOT = PROJECT_ROOT / "research_pipeline"
RAW_ROOT = PIPELINE_ROOT / "data" / "raw"
MANIFEST = PIPELINE_ROOT / "data" / "download_manifest.jsonl"
CONFIG = PIPELINE_ROOT / "config" / "sources.json"
INVENTORY = PIPELINE_ROOT / "data" / "public_data_inventory.csv"
REPORT = PIPELINE_ROOT / "reports" / "data_access_audit.md"

DATE_CANDIDATES = (
    "TIME_PERIOD",
    "DATE",
    "DATE.1",
    "observation_date",
    "RunDates",
    "As of Date in Form YYYY-MM-DD",
)


def normalize_manifest_key(value: str | Path) -> str:
    """Normalize old Windows and current POSIX-style manifest paths."""
    return str(value).replace("\\", "/")


def configured_output_keys(config_path: Path = CONFIG) -> set[str]:
    """Return raw-file keys for currently enabled acquisition jobs."""
    config = json.loads(config_path.read_text(encoding="utf-8"))
    keys: set[str] = set()
    for group, spec in config.items():
        if not spec.get("enabled", True):
            continue
        declared_names = spec.get("filenames", [])
        for index, url in enumerate(spec.get("urls", []), start=1):
            fallback = declared_names[index - 1] if index <= len(declared_names) else f"download_{index}.dat"
            name = Path(urllib.parse.urlparse(url).path).name
            if not name or name.startswith("."):
                name = fallback
            keys.add(f"research_pipeline/data/raw/{group}/{name}")
        for key in spec.get("keys", []):
            keys.add(f"research_pipeline/data/raw/{group}/{key.replace('.', '_')}.csv")
        for series_id in spec.get("series", {}):
            keys.add(f"research_pipeline/data/raw/{group}/{series_id}.csv")
    return keys


def latest_manifest_rows(
    manifest_path: Path = MANIFEST,
    active_keys: set[str] | None = None,
) -> tuple[dict[str, dict], list[dict]]:
    latest: dict[str, dict] = {}
    if not manifest_path.exists():
        return latest, []
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        key = normalize_manifest_key(row.get("output_path", ""))
        if key:
            row["output_path"] = key
            latest[key] = row
    failures = [
        row for key, row in latest.items()
        if row.get("status") == "failed" and (active_keys is None or key in active_keys)
    ]
    return latest, failures


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extracted_integrity_issues(manifest_rows: dict[str, dict]) -> tuple[int, list[str]]:
    """Verify the extracted CFTC inputs actually consumed by the analysis."""
    extracted_root = RAW_ROOT / "cftc_legacy_futures" / "extracted"
    expected: set[Path] = set()
    for archive_path in sorted((RAW_ROOT / "cftc_legacy_futures").glob("*.zip")):
        try:
            with zipfile.ZipFile(archive_path) as archive:
                for member in archive.infolist():
                    member_name = Path(member.filename).name
                    if member_name:
                        expected.add(extracted_root / f"{archive_path.stem}__{member_name}")
        except zipfile.BadZipFile:
            expected.add(extracted_root / f"INVALID_ARCHIVE__{archive_path.name}")

    issues = []
    for path in sorted(expected):
        relative = path.relative_to(PROJECT_ROOT).as_posix()
        if not path.is_file():
            issues.append(f"missing extracted input: {relative}")
            continue
        manifest = manifest_rows.get(relative, {})
        recorded = manifest.get("sha256")
        actual = sha256_file(path)
        if not recorded:
            issues.append(f"unmanifested extracted input: {relative}")
        elif recorded != actual:
            issues.append(f"modified extracted input: {relative}")
    return len(expected), issues


def csv_audit(path: Path) -> dict:
    frame = pd.read_csv(path, low_memory=False)
    date_column = next((name for name in DATE_CANDIDATES if name in frame.columns), None)
    start = end = None
    if date_column:
        parsed = pd.to_datetime(frame[date_column], errors="coerce")
        if parsed.notna().any():
            start = parsed.min().date().isoformat()
            end = parsed.max().date().isoformat()
    return {
        "rows": len(frame),
        "columns": len(frame.columns),
        "date_column": date_column,
        "start": start,
        "end": end,
        "column_names": " | ".join(map(str, frame.columns)),
    }


def zip_audit(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        members = [member for member in archive.infolist() if not member.is_dir()]
    return {
        "rows": None,
        "columns": None,
        "date_column": None,
        "start": None,
        "end": None,
        "column_names": " | ".join(member.filename for member in members),
    }


def file_audit(path: Path) -> dict:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return csv_audit(path)
    if suffix == ".zip":
        return zip_audit(path)
    return {
        "rows": None,
        "columns": None,
        "date_column": None,
        "start": None,
        "end": None,
        "column_names": "binary or non-CSV source; source-specific parser required",
    }


def main() -> int:
    active_keys = configured_output_keys()
    manifest_rows, failures = latest_manifest_rows(active_keys=active_keys)
    records: list[dict] = []
    for path in sorted(RAW_ROOT.rglob("*")):
        if not path.is_file() or "extracted" in path.parts:
            continue
        relative = path.relative_to(PROJECT_ROOT).as_posix()
        manifest = manifest_rows.get(relative, {})
        actual_sha256 = sha256_file(path)
        recorded_sha256 = manifest.get("sha256")
        if not manifest or not recorded_sha256:
            status = "local_unmanifested"
        elif recorded_sha256 != actual_sha256:
            status = "local_modified"
        else:
            status = manifest.get("status") or "local_verified"
        audit = file_audit(path)
        records.append(
            {
                "source_group": path.parent.name,
                "file": relative,
                "bytes": path.stat().st_size,
                "sha256": actual_sha256,
                "manifest_status": status,
                **audit,
            }
        )

    INVENTORY.parent.mkdir(parents=True, exist_ok=True)
    with INVENTORY.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = list(records[0]) if records else ["source_group", "file"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)

    counts = Counter(record["source_group"] for record in records)
    total_bytes = sum(record["bytes"] for record in records)
    present_keys = {record["file"] for record in records}
    missing_configured = sorted(active_keys - present_keys)
    local_integrity_issues = [
        record for record in records
        if record["manifest_status"] in {"local_unmanifested", "local_modified"}
    ]
    extracted_count, extracted_issues = extracted_integrity_issues(manifest_rows)
    healthy = not failures and not missing_configured and not local_integrity_issues and not extracted_issues
    lines = [
        "# Public-data access audit",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "This report verifies acquisition and basic parseability. Analytical use still requires the purpose-ledger gates.",
        "",
        "## Acquisition summary",
        "",
        f"- Files audited: {len(records)}",
        f"- Download size excluding extracted CFTC duplicates: {total_bytes / (1024 ** 2):.1f} MB",
        f"- Unresolved failures among currently configured downloads: {len(failures)}",
        f"- Configured downloads missing locally: {len(missing_configured)}",
        f"- Raw files with missing or mismatched manifest hashes: {len(local_integrity_issues)}",
        f"- Extracted CFTC analytical inputs verified: {extracted_count - len(extracted_issues)} of {extracted_count}",
        "",
    ]
    for group, count in sorted(counts.items()):
        lines.append(f"- `{group}`: {count} file(s)")
    lines.extend(["", "## Date coverage", "", "| Source | File | Rows | Start | End |", "|---|---|---:|---|---|"])
    for record in records:
        lines.append(
            f"| {record['source_group']} | `{Path(record['file']).name}` | "
            f"{record['rows'] if record['rows'] is not None else ''} | "
            f"{record['start'] or ''} | {record['end'] or ''} |"
        )
    lines.extend(["", "## Failed requests", ""])
    if failures:
        for failure in failures:
            lines.append(f"- `{failure['source_group']}`: {failure['url']} - {failure.get('error', 'unknown error')}")
    else:
        lines.append("- None.")
    lines.extend(["", "## Integrity issues", ""])
    integrity_messages = [
        *[f"missing configured download: {key}" for key in missing_configured],
        *[f"{record['manifest_status']}: {record['file']}" for record in local_integrity_issues],
        *extracted_issues,
    ]
    if integrity_messages:
        lines.extend(f"- {message}" for message in integrity_messages)
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Completed checks and remaining limitations",
            "",
            "- Completed: all configured raw downloads and extracted CFTC analytical inputs have locally verified SHA-256 hashes and acquisition statuses."
            if healthy else
            "- Incomplete: acquisition or integrity issues listed above must be resolved before analysis.",
            "- Completed: BIS exchange-rate quote direction is normalized to the USD return on foreign currency; EUR is used as a documented proxy, not an asserted Deutsche-mark splice.",
            "- Completed: the ACM CSV fields used by the mechanism checks, the CFTC contract crosswalk, and the assumed CFTC release lag are documented in the analytical pipeline.",
            "- Remaining limitation: the OECD CLI and FRED histories are current-vintage, and the CLI can overlap with financial inputs.",
            "- Remaining limitation: the author signal dates and licensed analytical panel are unavailable, so the public exercise remains a proxy analysis rather than a replication.",
        ]
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {INVENTORY.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {REPORT.relative_to(PROJECT_ROOT)}")
    return 0 if healthy else 1


if __name__ == "__main__":
    raise SystemExit(main())
