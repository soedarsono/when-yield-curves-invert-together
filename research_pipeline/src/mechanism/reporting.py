"""Write publication-ready figures, LaTeX fragments, and evidence ledgers."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .inference import event_values


PROJECT_ROOT = Path(__file__).resolve().parents[3]
PIPELINE_ROOT = PROJECT_ROOT / "research_pipeline"
OUTPUT_ROOT = PIPELINE_ROOT / "outputs" / "mechanism"
PUBLICATION_ROOT = PROJECT_ROOT / "rewrite" / "generated"


def _latex_escape(value: object) -> str:
    text = str(value)
    for old, new in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("_", r"\_"), ("#", r"\#")]:
        text = text.replace(old, new)
    return text


def _fmt(value: float, digits: int = 2) -> str:
    return "--" if not np.isfinite(value) else f"{value:.{digits}f}"


def write_tables(results: pd.DataFrame, sensitivity: pd.DataFrame, simulation: pd.DataFrame) -> list[Path]:
    table_dir = OUTPUT_ROOT / "tables"
    table_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        r"\begin{table}[!htbp]", r"\centering", r"\caption{Outcomes around synchronized delivered-easing onsets}",
        r"\label{tab:public_mechanism_checks}", r"\small", r"\begin{tabular}{>{\raggedright\arraybackslash}p{4.6cm}rrrrr}",
        r"\toprule", r"Outcome & Estimate & 90\% CI & RI $p$ & Holm $p$ & Rotations \\", r"\midrule",
    ]
    for row in results.itertuples(index=False):
        ci = f"[{_fmt(row.ci90_episode_bootstrap_low)}, {_fmt(row.ci90_episode_bootstrap_high)}]"
        lines.append(
            f"{_latex_escape(row.label)} & {_fmt(row.estimate)} & {ci} & {_fmt(row.p_randomization_raw, 3)} & {_fmt(row.p_holm_primary_family, 3)} & {int(row.rotation_reference_count_including_observed)} \\\\"
        )
    lines.extend([
        r"\bottomrule", r"\end{tabular}",
        r"\begin{minipage}{0.96\linewidth}\footnotesize Notes: Events are synchronized delivered-easing onsets constructed from public BIS policy rates. They are a downstream policy-rate state, distinct from the paper's predictive IYC state. RI $p$-values enumerate every circular rotation, condition on the observed number of valid episode outcomes, include the observed assignment, and double the smaller inclusive tail rank. Rotations reports the resulting finite reference count. The CFTC reference is small because missing contract coverage makes most rotations change the valid event count; its RI result is correspondingly coarse. With irregular missingness, the same-count rotations need not form a transformation group, so these are conditional finite-rotation references rather than exact causal randomization tests. Intervals resample onset episodes. Holm $p$-values adjust the six prespecified primary outcomes. Currency returns and CFTC positioning are percentage points, with CFTC positions measured as a share of open interest; ACM components are percentage points; CLI, NFCI, and VIX are index points.\end{minipage}",
        r"\end{table}", "",
    ])
    main = table_dir / "public_mechanism_checks.tex"
    main.write_text("\n".join(lines), encoding="utf-8")

    sim_summary = simulation.groupby("state").agg(
        crash_capture_rate=("crash_capture_rate", "mean"), state_month_share=("state_month_share", "mean"),
        false_positive_months=("false_positive_months", "mean"), mean_carry_on_pct=("mean_carry_on_pct", "mean"),
    ).reset_index()
    sim_lines = [
        r"\begin{table}[!htbp]", r"\centering", r"\caption{Path-dependent and static rules across synthetic paths}",
        r"\label{tab:synthetic_latch}", r"\small", r"\begin{tabular}{lrrrr}", r"\toprule",
        r"State rule & Capture & On share & False months & Return on (\%) \\", r"\midrule",
    ]
    labels = {"static_state": "Static count", "latched_state": "Path-dependent latch"}
    for row in sim_summary.itertuples(index=False):
        sim_lines.append(f"{labels[row.state]} & {_fmt(row.crash_capture_rate, 3)} & {_fmt(row.state_month_share, 3)} & {_fmt(row.false_positive_months, 1)} & {_fmt(row.mean_carry_on_pct, 3)} \\\\ ")
    capture_path_count = int(simulation.loc[simulation["crashes"] > 0, "simulation"].nunique())
    sim_lines.extend([
        r"\bottomrule", r"\end{tabular}",
        rf"\begin{{minipage}}{{0.93\linewidth}}\footnotesize Notes: Results use 2,000 illustrative 456-month paths. Capture averages the {capture_path_count:,} paths containing at least one delayed-crash month; all other columns average all 2,000 paths. Capture is the share of delayed-crash months in which the rule is active; on share is the fraction of all months active; false months counts active non-crash months; and return on is the mean carry return while active. Delivered easing mechanically re-steepens simulated curves after stress begins.\end{{minipage}}",
        r"\end{table}", "",
    ])
    sim_path = table_dir / "synthetic_path_dependence.tex"
    sim_path.write_text("\n".join(sim_lines), encoding="utf-8")

    sens_lines = [
        r"\begin{table}[!htbp]", r"\centering", r"\caption{Public-proxy sensitivity: shadow carry spot return}",
        r"\label{tab:public_proxy_sensitivity}", r"\small", r"\begin{tabular}{lrrrr}", r"\toprule",
        r"Construction & Estimate & RI $p$ & Events & Rotations \\", r"\midrule",
    ]
    sensitivity_labels = {
        "cut_count_threshold_2": "At least two countries easing",
        "cut_count_threshold_3": "At least three countries easing",
        "cut_count_threshold_4": "At least four countries easing",
    }
    for row in sensitivity.itertuples(index=False):
        label = sensitivity_labels.get(row.sensitivity)
        if label is None and row.sensitivity.startswith("leave_event_currency_"):
            label = f"Exclude {row.sensitivity.rsplit('_', 1)[-1]} from event rule"
        if label is None:
            label = row.sensitivity
        sens_lines.append(f"{_latex_escape(label)} & {_fmt(row.estimate)} & {_fmt(row.p_randomization, 3)} & {int(row.event_count)} & {int(row.rotation_reference_count_including_observed)} \\\\ ")
    sens_lines.extend([
        r"\bottomrule", r"\end{tabular}",
        r"\begin{minipage}{0.92\linewidth}\footnotesize Notes: Each threshold definition recomputes its own three-month quiet window. Onset counts therefore need not be monotone in the number of countries required to cut. Leave-one-currency rows omit that currency from the event rule.\end{minipage}",
        r"\end{table}", "",
    ])
    sens_path = table_dir / "public_proxy_sensitivity.tex"
    sens_path.write_text("\n".join(sens_lines), encoding="utf-8")
    return [main, sim_path, sens_path]


def _event_path(values: pd.Series, events: pd.Series, horizons: range, mode: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    means, lows, highs = [], [], []
    v = values.to_numpy(float)
    e = events.fillna(False).to_numpy(bool)
    rng = np.random.default_rng(13010)
    for h in horizons:
        x = event_values(v, e, h, mode)
        means.append(x.mean() if len(x) else np.nan)
        if len(x) >= 2:
            boot = np.array([rng.choice(x, size=len(x), replace=True).mean() for _ in range(1999)])
            low, high = np.quantile(boot, [0.05, 0.95])
            lows.append(low)
            highs.append(high)
        else:
            lows.append(np.nan); highs.append(np.nan)
    return np.asarray(means), np.asarray(lows), np.asarray(highs)


def write_empirical_figure(panel: pd.DataFrame) -> list[Path]:
    figure_dir = OUTPUT_ROOT / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    horizons = range(0, 13)
    events = panel["easing_onset"]
    series = [
        ("shadow_carry_spot_pct", "sum", "Shadow carry spot return", "Cumulative percentage points"),
        ("cftc_carry_crowding_pct_oi", "change", "CFTC carry-aligned crowding", "Change, pp of open interest"),
        ("acm_expected_path_10y_pct", "change", "ACM expected-rate component", "Change, percentage points"),
        ("acm_term_premium_10y_pct", "change", "ACM 10-year term premium", "Change, percentage points"),
        ("oecd_g7_cli", "change", "OECD G7 leading indicator", "Change, index points"),
        ("NFCI", "change", "Chicago Fed financial conditions", "Change, index points"),
    ]
    fig, axes = plt.subplots(3, 2, figsize=(10.5, 10.2), sharex=True)
    color = "#5B2C6F"
    for ax, (column, mode, title, ylabel) in zip(axes.flat, series):
        mean, low, high = _event_path(panel[column], events, horizons, mode)
        ax.axhline(0, color="#666666", linewidth=0.8)
        ax.fill_between(list(horizons), low, high, color=color, alpha=0.16, linewidth=0)
        ax.plot(list(horizons), mean, color=color, marker="o", markersize=3.2, linewidth=1.7)
        ax.set_title(title, loc="left", fontsize=10, fontweight="bold")
        ax.set_ylabel(ylabel, fontsize=8)
        ax.grid(axis="y", color="#dddddd", linewidth=0.5)
    for ax in axes[-1]:
        ax.set_xlabel("Months from synchronized-easing onset")
    fig.suptitle("Public proxies around synchronized delivered easing", x=0.07, ha="left", fontsize=14, fontweight="bold")
    fig.text(0.07, 0.008, "Means across onset episodes; bands are 90% episode-bootstrap intervals. The delivered-easing state is downstream of, and distinct from, the predictive IYC state.", fontsize=8)
    fig.tight_layout(rect=(0.04, 0.035, 1, 0.96))
    paths = []
    for suffix in ["pdf", "svg", "png"]:
        path = figure_dir / f"public_mechanism_event_study.{suffix}"
        fig.savefig(path, dpi=300 if suffix == "png" else None, bbox_inches="tight")
        paths.append(path)
    plt.close(fig)
    return paths


def write_simulation_figure(example: pd.DataFrame, simulation: pd.DataFrame) -> list[Path]:
    figure_dir = OUTPUT_ROOT / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    crash_idx = np.flatnonzero(example["crash"].to_numpy(bool))
    center = int(crash_idx[len(crash_idx) // 2]) if len(crash_idx) else len(example) // 2
    lo, hi = max(0, center - 24), min(len(example), center + 24)
    window = example.iloc[lo:hi]
    summary = simulation.groupby("state")["crash_capture_rate"].agg(["mean", lambda x: x.quantile(0.05), lambda x: x.quantile(0.95)])
    summary.columns = ["mean", "p05", "p95"]
    fig, axes = plt.subplots(2, 1, figsize=(10.5, 7.2), gridspec_kw={"height_ratios": [1.5, 1]})
    ax = axes[0]
    x = window["month"].to_numpy()
    ax.plot(x, window["inversion_count"], color="#999999", linewidth=1.4, label="Static inversion count")
    ax.plot(x, window["live_count"], color="#5B2C6F", linewidth=2.0, label="Latched live count")
    ax.axhline(2, color="#333333", linestyle="--", linewidth=0.8, label="Cluster threshold")
    for t in window.loc[window["crash"], "month"]:
        ax.axvline(t, color="#C0392B", alpha=0.55, linewidth=1.2)
    ax.set_ylabel("Curves counted")
    ax.set_title("One synthetic path: re-steepening can turn off a static state before losses arrive", loc="left", fontsize=11, fontweight="bold")
    ax.legend(frameon=False, ncol=2, fontsize=8)
    ax.grid(axis="y", color="#dddddd", linewidth=0.5)
    ax = axes[1]
    order = ["static_state", "latched_state"]
    labels = ["Static count", "Path-dependent latch"]
    means = summary.loc[order, "mean"].to_numpy()
    errors = np.vstack([means - summary.loc[order, "p05"].to_numpy(), summary.loc[order, "p95"].to_numpy() - means])
    ax.bar(labels, means, color=["#9E9E9E", "#5B2C6F"], width=0.55)
    ax.errorbar(range(2), means, yerr=errors, fmt="none", color="#222222", capsize=4)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Crash-month capture rate")
    ax.set_title("2,000 illustrative paths", loc="left", fontsize=11, fontweight="bold")
    ax.grid(axis="y", color="#dddddd", linewidth=0.5)
    fig.text(0.07, 0.01, "Synthetic illustration only. Parameters are not estimated or calibrated to the paper; red lines mark simulated crash months.", fontsize=8)
    fig.tight_layout(rect=(0.04, 0.035, 1, 1))
    paths = []
    for suffix in ["pdf", "svg", "png"]:
        path = figure_dir / f"synthetic_path_dependence.{suffix}"
        fig.savefig(path, dpi=300 if suffix == "png" else None, bbox_inches="tight")
        paths.append(path)
    plt.close(fig)
    return paths


def write_ledgers(results: pd.DataFrame, onsets: pd.DataFrame, spec: dict, sample: pd.DataFrame, simulation: pd.DataFrame) -> list[Path]:
    ledger_dir = OUTPUT_ROOT / "ledgers"
    ledger_dir.mkdir(parents=True, exist_ok=True)
    result_ledger = ledger_dir / "mechanism_result_ledger.csv"
    results.to_csv(result_ledger, index=False)
    onsets_path = ledger_dir / "synchronized_easing_onsets.csv"
    onsets.to_csv(onsets_path, index=False)
    sim_summary = simulation.groupby("state").agg(
        simulations=("simulation", "nunique"), crash_capture_rate=("crash_capture_rate", "mean"),
        state_month_share=("state_month_share", "mean"), false_positive_months=("false_positive_months", "mean"),
        mean_carry_on_pct=("mean_carry_on_pct", "mean"),
    ).reset_index()
    sim_summary.insert(0, "evidence_type", "simulation")
    sim_summary["interpretation"] = "Illustrates how confirmed exit can retain crash-state coverage after contemporaneous inversions re-steepen."
    sim_summary["limitation"] = "Synthetic parameters are neither fitted nor calibrated; higher crash capture also uses more state months and is not an empirical performance estimate."
    sim_path = ledger_dir / "simulation_result_ledger.csv"
    sim_summary.to_csv(sim_path, index=False)
    metadata = {
        "design_status": "Prespecified public proxy; not an IYC signal replication",
        "sample_start": spec["sample_start"], "sample_end": spec["sample_end"],
        "monthly_rows": len(sample), "onset_count": len(onsets),
        "policy_event_definition": spec["synchronized_easing"],
        "multiple_testing_family": spec["primary_tests"],
        "inference": "Episode bootstrap; all circular rotations conditional on the observed valid-event count with doubled smaller-tail inclusive ranks; disclosed Newey-West association check",
        "simulation_status": "Synthetic illustration; parameters neither fitted nor calibrated to paper estimates",
    }
    metadata_path = ledger_dir / "mechanism_run_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return [result_ledger, onsets_path, sim_path, metadata_path]


def write_report(results: pd.DataFrame, sensitivity: pd.DataFrame, hac: pd.DataFrame, onsets: pd.DataFrame, simulation: pd.DataFrame, spec: dict) -> Path:
    report_dir = PIPELINE_ROOT / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / "mechanism_checks.md"
    primary = results.loc[results["result_id"].isin(spec["primary_tests"])]
    lines = [
        "# Independent public-data mechanism checks", "",
        "## Evidentiary boundary", "",
        "This exercise does **not** reproduce the paper's IYC signal, episode ledger, carry returns, or licensed panel. It asks whether public proxies display associations consistent with parts of the proposed mechanism. The event is synchronized **delivered easing**, constructed from BIS policy rates. It is downstream of the paper's expected-easing signal and cannot validate the paper's timing claim.", "",
        "## Frozen construction", "",
        f"- Sample: {spec['sample_start']} through {spec['sample_end']}.",
        f"- Onset: at least {spec['synchronized_easing']['baseline_country_count']} of nine policy rates fall by at least {spec['synchronized_easing']['minimum_cut_pp']:.2f} percentage point after {spec['synchronized_easing']['quiet_months_before_onset']} months without another synchronized cut.",
        "- Currency return: negative log change in BIS local-currency-per-USD exchange rate; positive means foreign-currency appreciation against USD.",
        "- Public carry proxy: equal-weight long the three highest and short the three lowest policy differentials, ranked with a one-month lag; spot leg only.",
        f"- Events found: {len(onsets)}. Exact dates and country counts are in `outputs/mechanism/ledgers/synchronized_easing_onsets.csv`.",
        "- Inference: every circular rotation preserves the complete event sequence. The reference set retains only rotations with the observed number of valid episode outcomes, includes the observed assignment, and doubles the smaller inclusive tail rank. This is a conditional finite-rotation reference rather than a causal exact test because irregular missingness can make the same-N subset fail to form a transformation group. Every retained and rejected rotation is recorded in `outputs/mechanism/data/rotation_audit.csv`. Ninety-percent intervals resample episodes; leave-one-episode ranges report influence. A monthly HAC regression is secondary.",
        "- Multiplicity: the six outcomes in `mechanism_spec.json` form one primary family and receive Holm adjustment. Other horizons and VIX are descriptive.", "",
        "## Primary estimates", "",
        "| Outcome | Estimate | Unit | Events | Rotations | RI p | Holm p | Leave-one-event range |", "|---|---:|---|---:|---:|---:|---:|---:|",
    ]
    for row in primary.itertuples(index=False):
        lines.append(f"| {row.label} | {_fmt(row.estimate)} | {row.unit} | {int(row.event_count)} | {int(row.rotation_reference_count_including_observed)} | {_fmt(row.p_randomization_raw,3)} | {_fmt(row.p_holm_primary_family,3)} | [{_fmt(row.leave_one_episode_low)}, {_fmt(row.leave_one_episode_high)}] |")
    lines.extend([
        "", "## Secondary diagnostics", "",
        f"The monthly HAC regression of the shadow carry spot return on the synchronized-easing state gives {hac.iloc[0]['estimate']:.3f} percentage point per month (Newey-West SE {hac.iloc[0]['se']:.3f}, t={hac.iloc[0]['t']:.2f}, normal-reference p={hac.iloc[0]['p']:.3f}). The episode randomization result is the preferred small-event inference.", "",
        "Threshold and leave-one-currency constructions are reported in `outputs/mechanism/tables/public_proxy_sensitivity.tex` and the machine-readable sensitivity CSV. These checks vary the event proxy, not the unavailable IYC signal. Onset counts need not be monotone in the cut threshold because every threshold definition applies its own three-month quiet-window rule.", "",
        "## Simulation boundary", "",
        "The synthetic exercise makes one structural point: if delivered easing re-steepens curves after a latent stress state begins, a static contemporaneous inversion count can switch off before delayed losses, while a fresh-entry/confirmed-exit latch can remain on. The simulation is deliberately not calibrated. It cannot establish that the historical latch was chosen independently, that the paper's episodes are correct, or that its return estimates generalize.", "",
        "## Interpretation limits", "",
        "- Synchronized policy easing is partly a response to stress, so all empirical results are associations around a downstream event, not causal effects or predictive tests.",
        "- Policy-rate ranks are an imperfect substitute for money-market or forward rates. Spot returns omit the carry income leg and transaction costs.",
        "- CFTC coverage is limited to directly matchable futures contracts. NOK and SEK are absent, and the DEM/EUR splice is a documented proxy. Only the same-N rotations enter its finite reference, so its p-value is discrete and low-powered; the exact reference count is reported beside the estimate.",
        "- ACM describes the U.S. Treasury curve. It cannot remove country-specific or regional term premia from foreign curves.",
        "- OECD CLI and FRED graph histories are current-vintage. The CLI may include financial information and therefore is secondary mechanism evidence.",
        "- Holm adjustment covers the declared primary family, but specification search in the original paper remains outside this public-proxy exercise.", "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def mirror_publication_assets(paths: list[Path]) -> list[Path]:
    PUBLICATION_ROOT.mkdir(parents=True, exist_ok=True)
    mirrored = []
    for path in paths:
        target = PUBLICATION_ROOT / path.name
        shutil.copy2(path, target)
        mirrored.append(target)
    return mirrored
