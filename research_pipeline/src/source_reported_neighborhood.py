#!/usr/bin/env python3
"""Audit the rule neighborhood reported in the source paper's Appendix C.

The input is a transcription of source Tables C.1--C.3, not regenerated
estimates.  The script deliberately performs no search-adjusted inference:
the source PDF does not disclose the complete set of tried rules or joint
bootstrap draws.  It provides descriptive sign counts, baseline ranks, and a
figure ordered independently of coefficient magnitude.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT = PROJECT_ROOT / "research_pipeline" / "config" / "source_reported_rule_neighborhood.csv"
OUTPUT = PROJECT_ROOT / "research_pipeline" / "outputs" / "v03" / "source_reported_neighborhood"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def unique_core(frame: pd.DataFrame) -> pd.DataFrame:
    """Return the nine non-duplicated construction rows used in the audit."""
    core = frame.loc[frame["include_in_unique_core"]].copy()
    if core["rule_id"].duplicated().any():
        raise ValueError("Core rule identifiers must be unique.")
    if len(core) != 9:
        raise ValueError(f"Expected nine unique reported rules, found {len(core)}.")
    return core.sort_values(["active_months", "rule_family", "rule_id"]).reset_index(drop=True)


def summarize(core: pd.DataFrame) -> pd.DataFrame:
    baseline = core.loc[core["baseline"]]
    if len(baseline) != 1:
        raise ValueError("The unique core must contain exactly one baseline row.")
    rows = []
    for outcome in ("carry_spot_pp", "carry_total_pp", "high_beta_spot_pp", "high_beta_total_pp"):
        values = core[outcome].to_numpy(float)
        base = float(baseline.iloc[0][outcome])
        rows.append(
            {
                "outcome": outcome,
                "reported_rule_count": len(values),
                "negative_count": int((values < 0).sum()),
                "negative_share": float((values < 0).mean()),
                "baseline_coefficient_pp": base,
                "baseline_negative_rank": int(pd.Series(values).rank(method="min").loc[baseline.index[0]]),
                "most_negative_pp": float(np.min(values)),
                "least_negative_or_positive_pp": float(np.max(values)),
            }
        )
    return pd.DataFrame(rows)


def plot(core: pd.DataFrame, path: Path) -> None:
    labels = core["rule_label"].tolist()
    y = np.arange(len(core))
    colors = core["rule_family"].map({"breadth": "#2d6a9f", "release": "#a55b21", "tenor": "#5e7d3b"})
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 5.8), sharey=True)
    for ax, outcome, title in zip(
        axes,
        ("carry_spot_pp", "high_beta_spot_pp"),
        ("Interest-rate-sorted carry spot", "Predetermined-beta-sorted spot basket"),
    ):
        ax.axvline(0, color="#444444", linewidth=0.8)
        ax.scatter(core[outcome], y, c=colors, s=np.where(core["baseline"], 72, 42), zorder=3)
        for idx, row in core.iterrows():
            if bool(row["baseline"]):
                ax.scatter(row[outcome], idx, facecolors="none", edgecolors="black", s=125, linewidth=1.2, zorder=4)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("Annualized state coefficient (percentage points)")
        ax.grid(axis="x", color="#dddddd", linewidth=0.6)
    axes[0].set_yticks(y, labels)
    fig.suptitle("Reported state-definition neighborhood", fontsize=12, fontweight="bold")
    fig.text(
        0.5,
        0.01,
        "Rules are ordered by active-month count, not by estimated return. The black ring marks the baseline.\n"
        "The displayed specifications do not exhaust the search and do not use multiplicity-adjusted inference.",
        ha="center",
        fontsize=8.2,
    )
    fig.tight_layout(rect=[0, 0.075, 1, 0.94])
    fig.savefig(path, dpi=220)
    fig.savefig(path.with_suffix(".pdf"), metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(INPUT)
    for column in ("baseline", "include_in_unique_core"):
        frame[column] = frame[column].astype(str).str.lower().eq("true")
    core = unique_core(frame)
    summary = summarize(core)
    core_path = OUTPUT / "reported_rule_neighborhood_unique.csv"
    summary_path = OUTPUT / "reported_rule_neighborhood_summary.csv"
    figure_path = OUTPUT / "reported_rule_neighborhood.png"
    core.to_csv(core_path, index=False)
    summary.to_csv(summary_path, index=False)
    plot(core, figure_path)
    manifest = {
        "analysis": "descriptive audit of source Tables C.1--C.3",
        "input_status": "transcribed from AI JMP.pdf; estimates not regenerated",
        "search_adjusted_inference": False,
        "reason_search_adjustment_unavailable": "complete tried-rule set and joint resamples are absent",
        "input": {"path": INPUT.relative_to(PROJECT_ROOT).as_posix(), "sha256": sha256(INPUT)},
        "outputs": [
            {"path": p.relative_to(PROJECT_ROOT).as_posix(), "sha256": sha256(p)}
            for p in (core_path, summary_path, figure_path, figure_path.with_suffix(".pdf"))
        ],
    }
    (OUTPUT / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
