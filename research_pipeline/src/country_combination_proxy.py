#!/usr/bin/env python3
"""Country-pair and country-triple diagnostics for the public easing proxy.

This module deliberately does not attempt to recreate the paper's yield-curve
state.  It asks a narrower question with already-downloaded BIS public data:
do joint delivered policy-rate cuts by particular country combinations line up
with especially weak policy-ranked currency returns?

The script writes only to ``outputs/country_combinations`` so the established
mechanism-check outputs remain untouched.
"""

from __future__ import annotations

import hashlib
import json
import platform
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

from mechanism.inference import episode_bootstrap_ci, leave_one_range
from mechanism.panel import at_least_rate_cut, build_public_panel, load_spec


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PIPELINE_ROOT = PROJECT_ROOT / "research_pipeline"
OUTPUT_ROOT = PIPELINE_ROOT / "outputs" / "country_combinations"
MINIMUM_TEST_EVENTS = 6
HORIZON_MONTHS = 1


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()


def _artifact(path: Path) -> dict[str, str | int]:
    return {"path": _relative(path), "bytes": path.stat().st_size, "sha256": _sha256(path)}


def build_country_cut_panel(currency: pd.DataFrame, spec: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return monthly cut indicators and their nonmissing-data coverage."""
    changes = currency.pivot(index="month", columns="currency", values="policy_change_pp").sort_index()
    coverage = changes.notna()
    cuts = changes.apply(
        lambda series: at_least_rate_cut(series, spec["synchronized_easing"]["minimum_cut_pp"])
    )
    cuts = cuts.where(coverage, False).astype(bool)
    return cuts, coverage


def joint_cut_onsets(
    cuts: pd.DataFrame,
    coverage: pd.DataFrame,
    combo: tuple[str, ...],
    quiet_months: int,
) -> pd.Series:
    """Flag joint-cut months preceded by ``quiet_months`` without that joint cut."""
    columns = list(combo)
    jointly_observed = coverage[columns].all(axis=1)
    joint_cut = cuts[columns].all(axis=1) & jointly_observed
    recent = pd.concat(
        [joint_cut.shift(lag, fill_value=False) for lag in range(1, quiet_months + 1)], axis=1
    ).any(axis=1)
    return (joint_cut & ~recent).astype(bool)


def rotation_reference(outcome: np.ndarray, events: np.ndarray) -> np.ndarray:
    """Mean outcomes for every circular rotation of an event indicator."""
    outcome = np.asarray(outcome, float)
    events = np.asarray(events, bool)
    if len(outcome) != len(events) or not events.any() or not np.isfinite(outcome).all():
        raise ValueError("Rotation inputs must be equal-length, finite, and contain an event.")
    return np.asarray([outcome[np.roll(events, shift)].mean() for shift in range(len(events))], float)


def doubled_tail_rank(reference: np.ndarray, observed: float) -> float:
    """Two-sided inclusive finite-reference p-value."""
    lower = float(np.mean(reference <= observed))
    upper = float(np.mean(reference >= observed))
    return min(1.0, 2.0 * min(lower, upper))


def _standardized_reference(reference: np.ndarray) -> np.ndarray:
    scale = float(np.std(reference, ddof=1))
    if not np.isfinite(scale) or scale <= 0:
        return np.full(len(reference), np.nan)
    return (reference - float(np.mean(reference))) / scale


def _max_t_adjust(results: pd.DataFrame, references: dict[str, np.ndarray], mask: pd.Series, column: str) -> pd.DataFrame:
    """Add a common-rotation max-|z| reference value to eligible rows."""
    keys = results.loc[mask, "combination"].tolist()
    if not keys:
        results[column] = np.nan
        return results
    z_refs = np.column_stack([_standardized_reference(references[key]) for key in keys])
    max_abs = np.nanmax(np.abs(z_refs), axis=1)
    results[column] = np.nan
    for key in keys:
        observed_z = float(_standardized_reference(references[key])[0])
        adjusted = float(np.mean(max_abs >= abs(observed_z)))
        results.loc[results["combination"] == key, column] = adjusted
    return results


def analyze_combinations(currency: pd.DataFrame, monthly: pd.DataFrame, spec: dict) -> dict[str, pd.DataFrame]:
    cuts, coverage = build_country_cut_panel(currency, spec)
    monthly_indexed = monthly.set_index("month").sort_index()
    response = monthly_indexed["shadow_carry_spot_pct"] + monthly_indexed["shadow_carry_spot_pct"].shift(-1)
    valid = response.notna()
    response = response.loc[valid]
    inference_months = response.index
    quiet = int(spec["synchronized_easing"]["quiet_months_before_onset"])
    minimum = int(MINIMUM_TEST_EVENTS)

    rows: list[dict] = []
    references: dict[str, np.ndarray] = {}
    all_combinations = [
        combo for size in (2, 3) for combo in combinations(sorted(spec["currencies"]), size)
    ]
    for combo in all_combinations:
        onset = joint_cut_onsets(cuts, coverage, combo, quiet).reindex(inference_months, fill_value=False)
        event_series = response.loc[onset]
        event_values = event_series.to_numpy(float)
        key = "+".join(combo)
        eligible = len(event_values) >= minimum
        ci_low, ci_high = (np.nan, np.nan)
        loo_low, loo_high = (np.nan, np.nan)
        reference_mean = np.nan
        reference_sd = np.nan
        observed_z = np.nan
        raw_p = np.nan
        if eligible:
            reference = rotation_reference(response.to_numpy(float), onset.to_numpy(bool))
            references[key] = reference
            reference_mean = float(reference.mean())
            reference_sd = float(reference.std(ddof=1))
            observed_z = float(_standardized_reference(reference)[0])
            raw_p = doubled_tail_rank(reference, float(event_values.mean()))
            seed_offset = sum((position + 1) * sum(map(ord, code)) for position, code in enumerate(combo))
            ci_low, ci_high = episode_bootstrap_ci(
                event_values,
                int(spec["bootstrap_draws"]),
                int(spec["random_seed"]) + seed_offset,
            )
            loo_low, loo_high = leave_one_range(event_values)
        rows.append(
            {
                "combination_size": len(combo),
                "combination": key,
                "eligible_for_inference": eligible,
                "event_count": len(event_values),
                "mean_shadow_carry_h0_h1_pp": float(event_values.mean()) if len(event_values) else np.nan,
                "rotation_mean_pp": reference_mean,
                "excess_vs_rotation_mean_pp": (
                    float(event_values.mean() - reference_mean) if eligible else np.nan
                ),
                "rotation_sd_pp": reference_sd,
                "rotation_z": observed_z,
                "p_rotation_two_sided_raw": raw_p,
                "p_maxT_within_size": np.nan,
                "p_maxT_all_combinations": np.nan,
                "ci90_episode_bootstrap_low": ci_low,
                "ci90_episode_bootstrap_high": ci_high,
                "leave_one_event_low": loo_low,
                "leave_one_event_high": loo_high,
                "mean_excluding_2008_10_pp": float(event_series.drop(pd.Period("2008-10", "M"), errors="ignore").mean()),
                "mean_excluding_2020_03_pp": float(event_series.drop(pd.Period("2020-03", "M"), errors="ignore").mean()),
                "mean_excluding_2008_10_and_2020_03_pp": float(
                    event_series.drop(
                        [pd.Period("2008-10", "M"), pd.Period("2020-03", "M")], errors="ignore"
                    ).mean()
                ),
                "event_months": ";".join(map(str, inference_months[onset])),
            }
        )

    results = pd.DataFrame(rows)
    eligible = results["eligible_for_inference"]
    results = _max_t_adjust(results, references, eligible, "p_maxT_all_combinations")
    for size in (2, 3):
        size_mask = eligible & results["combination_size"].eq(size)
        keys = results.loc[size_mask, "combination"].tolist()
        if not keys:
            continue
        z_refs = np.column_stack([_standardized_reference(references[key]) for key in keys])
        max_abs = np.nanmax(np.abs(z_refs), axis=1)
        for key in keys:
            observed_z = float(_standardized_reference(references[key])[0])
            results.loc[results["combination"] == key, "p_maxT_within_size"] = float(
                np.mean(max_abs >= abs(observed_z))
            )

    results = results.sort_values(
        ["combination_size", "eligible_for_inference", "mean_shadow_carry_h0_h1_pp"],
        ascending=[True, False, True],
    ).reset_index(drop=True)

    eligible = results["eligible_for_inference"]
    max_t_frames = []
    for family, family_mask in {
        "all_pairs_and_triples": eligible,
        "pairs": eligible & results["combination_size"].eq(2),
        "triples": eligible & results["combination_size"].eq(3),
    }.items():
        keys = results.loc[family_mask, "combination"].tolist()
        if not keys:
            continue
        z_refs = np.column_stack([_standardized_reference(references[key]) for key in keys])
        max_t_frames.append(
            pd.DataFrame(
                {
                    "family": family,
                    "rotation": np.arange(len(response)),
                    "max_abs_rotation_z": np.nanmax(np.abs(z_refs), axis=1),
                    "combination_count": len(keys),
                }
            )
        )
    max_t_reference = pd.concat(max_t_frames, ignore_index=True)

    threshold_rows = []
    for threshold in (6, 8, 10):
        keys = results.loc[results["event_count"] >= threshold, "combination"].tolist()
        z_refs = np.column_stack([_standardized_reference(references[key]) for key in keys])
        max_abs = np.nanmax(np.abs(z_refs), axis=1)
        adjusted = {
            key: float(np.mean(max_abs >= abs(float(_standardized_reference(references[key])[0]))))
            for key in keys
        }
        leading_key = min(adjusted, key=adjusted.get)
        leading_row = results.loc[results["combination"] == leading_key].iloc[0]
        threshold_rows.append(
            {
                "minimum_event_threshold": threshold,
                "eligible_combination_count": len(keys),
                "adjusted_5pct_hit_count": sum(value < 0.05 for value in adjusted.values()),
                "smallest_adjusted_p": adjusted[leading_key],
                "combination_with_smallest_adjusted_p": leading_key,
                "its_event_count": int(leading_row["event_count"]),
                "its_mean_shadow_carry_h0_h1_pp": float(leading_row["mean_shadow_carry_h0_h1_pp"]),
            }
        )
    eligibility_threshold_sensitivity = pd.DataFrame(threshold_rows)

    baseline_onsets = monthly_indexed["easing_onset"].fillna(False).astype(bool)
    baseline_rows = []
    for month in monthly_indexed.index[baseline_onsets]:
        cut_currencies = sorted(cuts.columns[cuts.loc[month]].tolist())
        baseline_rows.append(
            {
                "month": str(month),
                "cut_count": len(cut_currencies),
                "cut_currencies": "+".join(cut_currencies),
                "shadow_carry_h0_h1_pp": float(response.loc[month]) if month in response.index else np.nan,
            }
        )
    baseline_composition = pd.DataFrame(baseline_rows)

    baseline_combo_rows = []
    for combo in all_combinations:
        key = "+".join(combo)
        contains = baseline_composition["cut_currencies"].str.split("+").apply(
            lambda values: set(combo).issubset(set(values))
        )
        in_values = baseline_composition.loc[contains, "shadow_carry_h0_h1_pp"].dropna()
        out_values = baseline_composition.loc[~contains, "shadow_carry_h0_h1_pp"].dropna()
        baseline_combo_rows.append(
            {
                "combination_size": len(combo),
                "combination": key,
                "baseline_onset_occurrences": int(contains.sum()),
                "mean_h0_h1_when_present_pp": float(in_values.mean()) if len(in_values) else np.nan,
                "mean_h0_h1_when_absent_pp": float(out_values.mean()) if len(out_values) else np.nan,
                "present_minus_absent_pp": (
                    float(in_values.mean() - out_values.mean()) if len(in_values) and len(out_values) else np.nan
                ),
                "months_present": ";".join(baseline_composition.loc[contains, "month"]),
                "status": "descriptive_only_sparse_baseline_composition",
            }
        )
    baseline_combination_summary = pd.DataFrame(baseline_combo_rows).sort_values(
        ["combination_size", "baseline_onset_occurrences", "combination"],
        ascending=[True, False, True],
    )

    country_rows = []
    for code in sorted(spec["currencies"]):
        contains = baseline_composition["cut_currencies"].str.split("+").apply(lambda values: code in values)
        values = baseline_composition.loc[contains, "shadow_carry_h0_h1_pp"].dropna()
        country_rows.append(
            {
                "currency": code,
                "baseline_onset_occurrences": int(contains.sum()),
                "mean_h0_h1_when_present_pp": float(values.mean()) if len(values) else np.nan,
                "months_present": ";".join(baseline_composition.loc[contains, "month"]),
            }
        )
    country_summary = pd.DataFrame(country_rows).sort_values(
        ["baseline_onset_occurrences", "currency"], ascending=[False, True]
    )

    cut_long = cuts.stack(future_stack=True).rename("cut").reset_index()
    observed_long = coverage.stack(future_stack=True).rename("policy_change_observed").reset_index()
    country_cut_panel = cut_long.merge(observed_long, on=["month", "currency"], how="left")
    country_cut_panel["month"] = country_cut_panel["month"].astype(str)
    return {
        "tested_combination_results": results,
        "baseline_onset_composition": baseline_composition,
        "baseline_combination_summary": baseline_combination_summary,
        "country_baseline_summary": country_summary,
        "country_cut_panel": country_cut_panel,
        "maxT_rotation_reference": max_t_reference,
        "eligibility_threshold_sensitivity": eligibility_threshold_sensitivity,
    }


def _fmt(value: float, digits: int = 3) -> str:
    return "--" if not np.isfinite(value) else f"{value:.{digits}f}"


def write_latex_table(results: pd.DataFrame, path: Path) -> None:
    eligible = results.loc[results["eligible_for_inference"]].copy()
    selected = eligible.groupby("combination_size", group_keys=False).head(5)
    lines = [
        r"\begin{table}[H]",
        r"\centering",
        r"\caption{Country combinations in the public delivered-easing proxy}",
        r"\label{tab:public-country-combinations}",
        r"\small",
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Combination & Events & Mean $[0,1]$ & Raw ref. & Max-$|z|$ ref. \\",
        r"\midrule",
    ]
    for row in selected.itertuples(index=False):
        lines.append(
            f"{row.combination.replace('+', '--')} & {row.event_count:d} & "
            f"{_fmt(row.mean_shadow_carry_h0_h1_pp, 2)} & "
            f"{_fmt(row.p_rotation_two_sided_raw)} & {_fmt(row.p_maxT_all_combinations)} \\\\"
        )
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\begin{minipage}{0.94\textwidth}\footnotesize",
            r"\textit{Notes:} The table reports the five most negative eligible pairs and triples. An event requires every listed country to cut its BIS policy rate by at least 10 basis points after three months without the same joint cut. The outcome is the cumulative policy-ranked log spot-return proxy in event months 0 and 1, in percentage points. Portfolio legs target three currencies per side and expand to include all cutoff ties with equal weight. Combinations require at least six valid events. Raw reference values use every circular timing rotation. The final column is the common-rotation maximum absolute standardized reference across every eligible pair and triple. Under simultaneous cyclic-shift exchangeability it controls the declared family; otherwise it is a finite family diagnostic. The family was not preregistered. This is a delivered-easing proxy, not a replication of the yield-curve state.",
            r"\end{minipage}",
            r"\end{table}",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_report(outputs: dict[str, pd.DataFrame], path: Path) -> None:
    results = outputs["tested_combination_results"]
    baseline = outputs["baseline_combination_summary"]
    eligible = results.loc[results["eligible_for_inference"]].copy()
    strongest = eligible.sort_values("mean_shadow_carry_h0_h1_pp").head(8)
    adjusted_hits = eligible.loc[eligible["p_maxT_all_combinations"] < 0.05]
    recurring = baseline.loc[baseline["baseline_onset_occurrences"] > 0].head(10)
    sparse = results.loc[~results["eligible_for_inference"]]
    threshold_sensitivity = outputs["eligibility_threshold_sensitivity"]

    finding = (
        f"{len(adjusted_hits)} combination(s) meet the 5% common-rotation max-|z| reference criterion across all eligible pairs and triples."
        if len(adjusted_hits)
        else "No pair or triple meets the 5% common-rotation max-|z| reference criterion across all eligible combinations."
    )
    lines = [
        "# Public-data country-combination diagnostic",
        "",
        "## Evidentiary boundary",
        "",
        "This is not a reconstruction of the paper's synchronized yield-curve-inversion state. The public repository does not contain the nine-country yield-slope panel. The diagnostic instead uses the existing BIS policy-rate files to study synchronized *delivered easing*, then asks whether particular joint-cut combinations coincide with unusually weak policy-ranked currency spot returns.",
        "",
        "## Design",
        "",
        "For each of the 36 country pairs and 84 country triples, a joint-cut onset occurs when every member cuts its BIS policy rate by at least 10 basis points and the same joint cut did not occur in the previous three months. The outcome is the cumulative policy-ranked log spot-return proxy in months 0 and 1. It targets three currencies per side using lagged policy-rate differentials and includes all cutoff ties with equal weight, so realized legs can be larger. It is a public mechanism proxy rather than a feasible excess return. Reference values require at least six valid events.",
        "",
        "Every eligible combination is shifted through every possible circular calendar rotation. The raw reference value is the doubled smaller inclusive tail rank. A common-rotation maximum absolute standardized reference is computed jointly across all eligible pairs and triples; size-specific values are also reported. Under simultaneous cyclic-shift exchangeability, this construction controls the declared family; otherwise it is a finite family diagnostic. The family was declared in code and exhaustively reported but was not preregistered. Event-resampling intervals and leave-one-event ranges expose small-sample sensitivity.",
        "",
        "## Result",
        "",
        finding,
        "A low raw reference value should therefore not be read as evidence that a specific country set uniquely drives the mechanism. The estimates are contemporaneous event-window associations and cannot distinguish policy response from the stress that prompted it.",
        "",
        "Most negative eligible combination estimates:",
        "",
        "| Combination | Size | Events | Mean pp | Raw ref. | Within-size max-|z| ref. | All-combination max-|z| ref. | Leave-one range |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in strongest.itertuples(index=False):
        lines.append(
            f"| {row.combination} | {row.combination_size} | {row.event_count} | "
            f"{_fmt(row.mean_shadow_carry_h0_h1_pp, 2)} | {_fmt(row.p_rotation_two_sided_raw)} | "
            f"{_fmt(row.p_maxT_within_size)} | {_fmt(row.p_maxT_all_combinations)} | "
            f"[{_fmt(row.leave_one_event_low, 2)}, {_fmt(row.leave_one_event_high, 2)}] |"
        )
    lines.extend(
        [
            "",
            f"Eligible combinations: {len(eligible)}. Sparse combinations retained descriptively but not tested: {len(sparse)}.",
            "",
            "The family result is sensitive to the minimum event-count rule:",
            "",
            "| Minimum events | Eligible combinations | 5% max-|z| hits | Smallest max-|z| ref. | Leading combination |",
            "|---:|---:|---:|---:|---|",
        ]
    )
    for row in threshold_sensitivity.itertuples(index=False):
        lines.append(
            f"| {row.minimum_event_threshold} | {row.eligible_combination_count} | "
            f"{row.adjusted_5pct_hit_count} | {_fmt(row.smallest_adjusted_p)} | "
            f"{row.combination_with_smallest_adjusted_p} |"
        )
    lines.extend(
        [
            "",
            "## Composition of the 15 baseline synchronized-easing onsets",
            "",
            "The next rows count combinations contained in the existing threshold-three onset dates. They are descriptive: the same crisis month contributes many overlapping pairs and triples, so treating these rows as separate tests would manufacture precision.",
            "",
            "| Combination | Size | Onset occurrences | Mean pp when present | Present-minus-absent pp | Months |",
            "|---|---:|---:|---:|---:|---|",
        ]
    )
    for row in recurring.itertuples(index=False):
        lines.append(
            f"| {row.combination} | {row.combination_size} | {row.baseline_onset_occurrences} | "
            f"{_fmt(row.mean_h0_h1_when_present_pp, 2)} | {_fmt(row.present_minus_absent_pp, 2)} | "
            f"{row.months_present} |"
        )
    lines.extend(
        [
            "",
            "## What this check can and cannot reveal",
            "",
            "A persistently negative combination would identify a useful target for a future author-data decomposition: one could ask whether the same countries also contribute disproportionately to the forward-looking inversion state. Failure to meet the family reference criterion instead favors the more cautious interpretation that the public easing proxy is broad and episode-driven rather than uniquely tied to a stable country bloc.",
            "",
            "The exercise cannot determine whether any country pair or triple drives the original result. Policy cuts occur after decisions are delivered, while yield-curve inversions are forward-looking. The shadow carry outcome omits interest income, observes the event contemporaneously, and can be influenced by the same global shock that induced policy easing. Country combinations overlap heavily, the event counts remain small, and BIS policy-rate definitions differ across countries and over time.",
            "",
            "## Reproduction",
            "",
            "Run `python research_pipeline/src/country_combination_proxy.py` from the project root. All outputs are isolated under `research_pipeline/outputs/country_combinations/`.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    spec = load_spec()
    currency, monthly = build_public_panel(spec)
    outputs = analyze_combinations(currency, monthly, spec)
    data_dir = OUTPUT_ROOT / "data"
    table_dir = OUTPUT_ROOT / "tables"
    data_dir.mkdir(parents=True, exist_ok=True)
    table_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for name, frame in outputs.items():
        path = data_dir / f"{name}.csv"
        frame.to_csv(path, index=False, lineterminator="\n")
        written.append(path)
    table_path = table_dir / "public_country_combination_proxy.tex"
    write_latex_table(outputs["tested_combination_results"], table_path)
    written.append(table_path)
    report_path = OUTPUT_ROOT / "country_combination_report.md"
    write_report(outputs, report_path)
    written.append(report_path)
    original_crosscheck_path = OUTPUT_ROOT / "original_paper_crosscheck.md"
    if original_crosscheck_path.is_file():
        written.append(original_crosscheck_path)

    input_paths = [
        PIPELINE_ROOT / "config" / "mechanism_spec.json",
        *sorted((PIPELINE_ROOT / "data" / "raw" / "bis_policy_rates").glob("M_*.csv")),
        *sorted((PIPELINE_ROOT / "data" / "raw" / "bis_exchange_rates").glob("*.csv")),
    ]
    manifest = {
        "status": "complete",
        "evidentiary_boundary": "delivered-easing public proxy; not replication of the yield-curve state",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "specification": {
            "joint_cut_threshold_percentage_points": spec["synchronized_easing"]["minimum_cut_pp"],
            "quiet_months": spec["synchronized_easing"]["quiet_months_before_onset"],
            "outcome": "policy-ranked log spot-return proxy, cumulative months 0 and 1; target three per side with equal inclusion of cutoff ties",
            "minimum_events_for_inference": MINIMUM_TEST_EVENTS,
            "raw_inference": "all circular timing rotations, two-sided inclusive reference rank",
            "multiplicity": "common-rotation max absolute standardized reference; family interpretation conditional on simultaneous cyclic-shift exchangeability",
        },
        "inputs": [_artifact(path) for path in input_paths if path.is_file()],
        "contextual_sources_not_used_in_computation": [
            _artifact(PROJECT_ROOT / "AI JMP.pdf")
        ] if (PROJECT_ROOT / "AI JMP.pdf").is_file() else [],
        "code": [
            _artifact(Path(__file__)),
            _artifact(PIPELINE_ROOT / "src" / "mechanism" / "panel.py"),
            _artifact(PIPELINE_ROOT / "src" / "mechanism" / "inference.py"),
        ],
        "outputs": [_artifact(path) for path in written],
    }
    manifest_path = OUTPUT_ROOT / "run_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "output_root": str(OUTPUT_ROOT),
                "eligible_combinations": int(outputs["tested_combination_results"]["eligible_for_inference"].sum()),
                "adjusted_5pct_hits": int(
                    (outputs["tested_combination_results"]["p_maxT_all_combinations"] < 0.05).sum()
                ),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
