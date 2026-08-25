#!/usr/bin/env python3
"""One-command orchestrator for independent public-data mechanism checks."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from mechanism.analysis import run_empirical
from mechanism.panel import load_spec
from mechanism.reporting import (
    OUTPUT_ROOT, mirror_publication_assets, write_empirical_figure, write_ledgers,
    write_report, write_simulation_figure, write_tables,
)
from mechanism.simulation import simulation_metrics


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PIPELINE_ROOT = PROJECT_ROOT / "research_pipeline"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_path(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()


def artifact_record(path: Path) -> dict[str, str | int]:
    return {"path": relative_path(path), "bytes": path.stat().st_size, "sha256": sha256_file(path)}


def analytical_input_paths() -> list[Path]:
    raw = PIPELINE_ROOT / "data" / "raw"
    sample_end_year = pd.Period(load_spec()["sample_end"], "M").year
    cftc_paths = []
    for path in sorted((raw / "cftc_legacy_futures" / "extracted").glob("*.txt")):
        years = [int(value) for value in re.findall(r"(?:19|20)\d{2}", path.name)]
        if not years or max(years) <= sample_end_year:
            cftc_paths.append(path)
    paths = [
        PIPELINE_ROOT / "config" / "mechanism_spec.json",
        PIPELINE_ROOT / "config" / "cftc_contract_crosswalk.csv",
        *sorted((raw / "bis_policy_rates").glob("*.csv")),
        *sorted((raw / "bis_exchange_rates").glob("*.csv")),
        *cftc_paths,
        raw / "nyfed_acm" / "acmPlot_data.csv",
        raw / "oecd_cli" / "oecd_cli_1988_present.csv",
        raw / "fred_controls" / "NFCI.csv",
        raw / "fred_controls" / "VIXCLS.csv",
    ]
    return [path for path in paths if path.is_file()]


def code_paths() -> list[Path]:
    return [Path(__file__).resolve(), *sorted((Path(__file__).parent / "mechanism").glob("*.py"))]


def dependency_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for package in ("matplotlib", "numpy", "pandas"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = "unavailable"
    return versions


def git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT,
            capture_output=True, text=True, check=False,
        )
    except OSError:
        return "unavailable"
    return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else "unavailable"


def build_manifest(
    *,
    derived: list[Path],
    tables: list[Path],
    figures: list[Path],
    ledgers: list[Path],
    report: Path,
    publication: list[Path],
) -> dict:
    output_paths = [*derived, *tables, *figures, *ledgers, report, *publication]
    return {
        "status": "complete", "evidentiary_boundary": "public proxies and synthetic illustration; not replication",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "environment": {
            "python": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "dependencies": dependency_versions(),
        },
        "inputs": [artifact_record(path) for path in analytical_input_paths()],
        "code": [artifact_record(path) for path in code_paths()],
        "outputs": [artifact_record(path) for path in output_paths],
        "derived_data": [relative_path(p) for p in derived],
        "tables": [relative_path(p) for p in tables],
        "figures": [relative_path(p) for p in figures],
        "ledgers": [relative_path(p) for p in ledgers],
        "report": relative_path(report),
        "publication_assets": [relative_path(p) for p in publication],
    }


def main() -> int:
    spec = load_spec()
    outputs = run_empirical(spec)
    example, simulation = simulation_metrics(int(spec["random_seed"]), simulations=2000)
    data_dir = OUTPUT_ROOT / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    derived = []
    for name in ["currency_panel", "monthly_panel", "cftc_currency", "results", "rotation_audit", "hac", "sensitivity", "onsets"]:
        path = data_dir / f"{name}.csv"
        frame = outputs[name].copy()
        for column in frame.columns:
            if isinstance(frame[column].dtype, pd.PeriodDtype):
                frame[column] = frame[column].astype(str)
        frame.to_csv(path, index=False, lineterminator="\n")
        derived.append(path)
    example_path = data_dir / "synthetic_example_path.csv"
    simulation_path = data_dir / "synthetic_monte_carlo.csv"
    example.to_csv(example_path, index=False, lineterminator="\n")
    simulation.to_csv(simulation_path, index=False, lineterminator="\n")
    derived.extend([example_path, simulation_path])

    tables = write_tables(outputs["results"], outputs["sensitivity"], simulation)
    empirical_figures = write_empirical_figure(outputs["monthly_panel"])
    simulation_figures = write_simulation_figure(example, simulation)
    ledgers = write_ledgers(outputs["results"], outputs["onsets"], spec, outputs["monthly_panel"], simulation)
    report = write_report(outputs["results"], outputs["sensitivity"], outputs["hac"], outputs["onsets"], simulation, spec)
    publication = mirror_publication_assets(
        [*tables, *[p for p in empirical_figures + simulation_figures if p.suffix in {".pdf", ".svg", ".png"}]]
    )
    manifest = build_manifest(
        derived=derived,
        tables=tables,
        figures=empirical_figures + simulation_figures,
        ledgers=ledgers,
        report=report,
        publication=publication,
    )
    manifest_path = OUTPUT_ROOT / "run_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"manifest": str(manifest_path), "onsets": len(outputs["onsets"]), "results": len(outputs["results"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
