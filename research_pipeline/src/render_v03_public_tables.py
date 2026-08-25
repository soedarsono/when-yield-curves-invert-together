#!/usr/bin/env python3
"""Render the v0.3 public-yield-proxy paper tables from machine outputs."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = PROJECT_ROOT / "research_pipeline" / "outputs" / "v03" / "yield_proxy" / "data"
TABLE_ROOT = PROJECT_ROOT / "rewrite" / "generated" / "tables"


def signed(value: float) -> str:
    return f"{value:+.2f}"


def pvalue(value: float) -> str:
    return "---" if pd.isna(value) else f"{value:.3f}"


def ordinal(value: int) -> str:
    suffix = "th" if 10 <= value % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(value % 10, "th")
    return f"{value}{suffix}"


def save(name: str, lines: list[str]) -> None:
    TABLE_ROOT.mkdir(parents=True, exist_ok=True)
    (TABLE_ROOT / name).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def file_record(path: Path) -> dict[str, object]:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "path": path.relative_to(PROJECT_ROOT).as_posix(),
        "sha256": digest,
        "bytes": path.stat().st_size,
    }


def render_summary(specs: pd.DataFrame, sensitivities: pd.DataFrame) -> None:
    baseline = specs.loc[specs["baseline_like"].astype(str).str.lower().eq("true")].iloc[0]
    labels = {
        "full_sample": "Baseline-like rule",
        "exclude_episodes_containing_1998_09_2008_10_2020_03":
            "Exclude episodes containing 1998:09, 2008:10, or 2020:03",
        "first_calendar_half_1988_2004": "First calendar half, 1988--2004",
        "second_calendar_half_2005_2025": "Second calendar half, 2005--2025",
        "delete_five_worst_active_months_outcome_conditioned_diagnostic":
            "Delete five worst active months",
    }
    rows = [
        f"Baseline-like rule & ${signed(baseline['annualized_active_minus_inactive_pp'])}$ & "
        f"{pvalue(baseline['p_circular_raw'])} & {int(baseline['active_months'])} & {int(baseline['episodes'])} \\\\"
    ]
    for row in sensitivities.itertuples(index=False):
        if row.sensitivity == "full_sample":
            continue
        displayed_episodes = (
            "---"
            if row.sensitivity == "delete_five_worst_active_months_outcome_conditioned_diagnostic"
            else str(int(row.episodes))
        )
        rows.append(
            f"{labels[row.sensitivity]} & ${signed(row.annualized_active_minus_inactive_pp)}$ & "
            f"{pvalue(row.p_circular_raw)} & {int(row.active_months)} & {displayed_episodes} \\\\"
        )
    negative = int((specs["annualized_active_minus_inactive_pp"] < 0).sum())
    save("v03_public_proxy_summary.tex", [
        "% EXECUTABLE PUBLIC OUTPUT: generated from the declared v0.3 10Y--3M proxy family.",
        r"\begin{table}[H]",
        r"\centering",
        r"\caption{Independent public 10Y--3M proxy audit}",
        r"\label{tab:v03-public-proxy}",
        r"\small",
        r"\begin{tabularx}{\textwidth}{>{\raggedright\arraybackslash}Xrrrr}",
        r"\toprule",
        "Public-data specification & Log spot difference & Raw rotation ref. & Active months & Episodes " + "\\\\",
        r"\midrule",
        *rows,
        r"\bottomrule",
        r"\end{tabularx}",
        "",
        r"\begin{minipage}{0.94\textwidth}",
        r"\footnotesize\emph{Notes:} Annualized percentage-point active-minus-inactive differences in a BIS policy-ranked log spot-return proxy. Each leg targets three currencies; all currencies tied at a cutoff enter with equal weight, so realized leg size can exceed three. The baseline-like rule uses current-vintage OECD monthly 10-year government yields minus 3-month interbank rates distributed through FRED, fresh entry, breadth two, two consecutive increases for release, and a one-month return lag. It is distinct from the baseline 10Y--2Y state and is not an executable forward return. Across the complete declared family, "
        f"{negative} of {len(specs)} coefficients are negative, the baseline ranks "
        f"{ordinal(int(baseline['estimate_rank_of_64_low_to_high']))} from most negative to most positive, and the common-calendar max-$|z|$ rotation-reference value is {baseline['p_maxT_family']:.3f}. "
        r"The crisis-deletion reference rotates the resulting complete-case sequence after excluded episodes are removed. The last row is outcome-conditioned and intentionally has neither a $p$-value nor an episode count, because deleting realized months mechanically splits state runs.",
        r"\end{minipage}",
        r"\end{table}",
    ])


def render_exclusions(loo: pd.DataFrame, disjoint: pd.DataFrame) -> None:
    loo_rows = [
        f"{row.excluded_from_signal_and_outcome} & ${signed(row.annualized_active_minus_inactive_pp)}$ & "
        f"{row.p_circular_raw:.3f} & {int(row.active_months)} & {int(row.episodes)} \\\\"
        for row in loo.itertuples(index=False)
    ]
    labels = {
        "European curves -> non-European currencies":
            r"European curves $\rightarrow$ AUD/CAD/JPY/NZD",
        "Non-European curves -> European currencies":
            r"Non-European curves $\rightarrow$ CHF/EUR/GBP/NOK/SEK",
    }
    split_rows = [
        f"{labels[row.split]} & ${signed(row.annualized_active_minus_inactive_pp)}$ & "
        f"{row.p_circular_raw:.3f} & {int(row.active_months)} & {int(row.episodes)} \\\\"
        for row in disjoint.itertuples(index=False)
    ]
    save("v03_public_loo_disjoint.tex", [
        "% EXECUTABLE PUBLIC OUTPUT: leave_one_country_out.csv and geographically_disjoint.csv",
        r"\begin{table}[H]",
        r"\centering",
        r"\caption{Public proxy exclusions and disjoint signals}",
        r"\label{tab:v03-public-exclusions}",
        r"\small",
        r"\begin{tabularx}{\textwidth}{>{\raggedright\arraybackslash}Xrrrr}",
        r"\toprule",
        "Excluded from curve state and outcome & Log spot difference & Raw rotation ref. & Active months & Episodes " + "\\\\",
        r"\midrule",
        *loo_rows,
        r"\midrule",
        r"\multicolumn{5}{l}{\emph{Geographically disjoint curve state and outcome}} " + "\\\\",
        *split_rows,
        r"\bottomrule",
        r"\end{tabularx}",
        "",
        r"\begin{minipage}{0.94\textwidth}",
        r"\footnotesize\emph{Notes:} Annualized active-minus-inactive differences in the log spot-return proxy. Each joint deletion removes a currency from both the public curve state and the public spot basket and requires five of the remaining eight curves. The resulting influence estimates overlap heavily and are not independent tests. Disjoint rows use no curve from a currency in the outcome basket. The European sensor requires four of five curves and targets one currency per side over four outcomes; the non-European sensor requires three of four curves and targets two per side over five. All cutoff ties are included and equally weighted. Reference values use inclusive circular shifts of each complete-case sequence after missing observations are dropped, compressing internal calendar gaps. They are not adjusted as an eleven-test family.",
        r"\end{minipage}",
        r"\end{table}",
    ])


def render_episodes(episodes: pd.DataFrame) -> None:
    rows = []
    for row in episodes.itertuples(index=False):
        rows.append(
            f"{int(row.episode_id)} & {str(row.onset_month).replace('-', ':')} & "
            f"{str(row.end_month).replace('-', ':')} & {int(row.duration_months)} & "
            f"${signed(row.cumulative_next_month_shadow_carry_spot_pct)}$ & "
            f"${signed(row.worst_next_month_shadow_carry_spot_pct)}$ \\\\"
        )
    save("v03_public_episode_ledger.tex", [
        "% EXECUTABLE PUBLIC OUTPUT: baseline_episode_ledger.csv",
        r"\begin{table}[H]",
        r"\centering",
        r"\caption{Public 10Y--3M proxy episode ledger}",
        r"\label{tab:v03-public-episodes}",
        r"\scriptsize",
        r"\begin{tabular}{rrrrrr}",
        r"\toprule",
        "Episode & Onset & End & Months & Sum of log spot proxy & Worst month " + "\\\\",
        r"\midrule",
        *rows,
        r"\bottomrule",
        r"\end{tabular}",
        "",
        r"\begin{minipage}{0.94\textwidth}",
        r"\footnotesize\emph{Notes:} Episodes use the baseline-like public 10Y--3M live state. The reported episode total is the sum of monthly percentage-point observations of the next-month BIS policy-ranked log spot-return proxy. Each side targets three currencies, with all cutoff ties included and equally weighted. The public "
        f"{len(episodes)}-episode ledger is specific to this exercise and is distinct from the baseline 15-episode 10Y--2Y state.",
        r"\end{minipage}",
        r"\end{table}",
    ])


def main() -> int:
    specs = pd.read_csv(DATA_ROOT / "specification_family.csv")
    sensitivities = pd.read_csv(DATA_ROOT / "baseline_sensitivities.csv")
    loo = pd.read_csv(DATA_ROOT / "leave_one_country_out.csv")
    disjoint = pd.read_csv(DATA_ROOT / "geographically_disjoint.csv")
    episodes = pd.read_csv(DATA_ROOT / "baseline_episode_ledger.csv")
    render_summary(specs, sensitivities)
    render_exclusions(loo, disjoint)
    render_episodes(episodes)
    figure_source = PROJECT_ROOT / "research_pipeline" / "outputs" / "v03" / "yield_proxy" / "figures" / "specification_curve.png"
    figure_mirror = PROJECT_ROOT / "rewrite" / "generated" / "v03_public_specification_curve.png"
    shutil.copyfile(figure_source, figure_mirror)
    paper_outputs = [
        TABLE_ROOT / "v03_public_proxy_summary.tex",
        TABLE_ROOT / "v03_public_loo_disjoint.tex",
        TABLE_ROOT / "v03_public_episode_ledger.tex",
        figure_mirror,
    ]
    manifest_path = PROJECT_ROOT / "research_pipeline" / "outputs" / "v03" / "yield_proxy" / "run_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["paper_outputs"] = [file_record(path) for path in paper_outputs]
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
