#!/usr/bin/env python3
"""Independent public 10Y-3M yield-curve proxy audit for v0.3.

This module does not reproduce the paper's unavailable 10Y-2Y author panel.
It uses current-vintage OECD monthly 10-year government yields and 3-month
interbank rates delivered through FRED, applies a deterministic version of the
paper's fresh-entry/live-state recursion, and relates the resulting proxy to
next-month BIS currency log spot-return proxies.  The complete declared rule family is
reported, including unfavorable results.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SRC_ROOT = Path(__file__).resolve().parent
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from mechanism.panel import load_fx_panel, load_policy_panel, load_spec


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PIPELINE_ROOT = PROJECT_ROOT / "research_pipeline"
RAW_ROOT = PIPELINE_ROOT / "data" / "raw" / "oecd_yield_curve_proxy"
OUTPUT_ROOT = PIPELINE_ROOT / "outputs" / "v03" / "yield_proxy"
SAMPLE_START = pd.Period("1988-01", "M")
SAMPLE_END = pd.Period("2025-12", "M")

COUNTRY_SERIES = {
    "AUD": ("IRLTLT01AUM156N", "IR3TIB01AUM156N"),
    "CAD": ("IRLTLT01CAM156N", "IR3TIB01CAM156N"),
    "CHF": ("IRLTLT01CHM156N", "IR3TIB01CHM156N"),
    "GBP": ("IRLTLT01GBM156N", "IR3TIB01GBM156N"),
    "JPY": ("IRLTLT01JPM156N", "IR3TIB01JPM156N"),
    "NOK": ("IRLTLT01NOM156N", "IR3TIB01NOM156N"),
    "NZD": ("IRLTLT01NZM156N", "IR3TIB01NZM156N"),
    "SEK": ("IRLTLT01SEM156N", "IR3TIB01SEM156N"),
}
EURO_PRE = ("IRLTLT01DEM156N", "IR3TIB01DEM156N")
EURO_POST = ("IRLTLT01EZM156N", "IR3TIB01EZM156N")
EURO_SPLICE = pd.Period("1999-01", "M")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_fred_series(series_id: str) -> pd.Series:
    path = RAW_ROOT / f"{series_id}.csv"
    frame = pd.read_csv(path)
    if frame.shape[1] != 2:
        raise ValueError(f"Expected two columns in {path}, found {frame.columns.tolist()}")
    dates = pd.to_datetime(frame.iloc[:, 0], errors="coerce").dt.to_period("M")
    values = pd.to_numeric(frame.iloc[:, 1], errors="coerce")
    series = pd.Series(values.to_numpy(float), index=dates, name=series_id)
    return series.loc[~series.index.isna()].sort_index().groupby(level=0).last()


def _slope(long_id: str, short_id: str) -> pd.DataFrame:
    frame = pd.concat(
        [load_fred_series(long_id).rename("long_yield_pct"), load_fred_series(short_id).rename("short_rate_pct")],
        axis=1,
    )
    frame["slope_pct"] = frame["long_yield_pct"] - frame["short_rate_pct"]
    frame["long_series_id"] = long_id
    frame["short_series_id"] = short_id
    return frame


def load_yield_panel() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for currency, pair in COUNTRY_SERIES.items():
        frame = _slope(*pair).assign(currency=currency)
        frames.append(frame.reset_index(names="month"))
    pre = _slope(*EURO_PRE).loc[lambda x: x.index < EURO_SPLICE]
    post = _slope(*EURO_POST).loc[lambda x: x.index >= EURO_SPLICE]
    euro = pd.concat([pre, post]).sort_index().assign(currency="EUR")
    frames.append(euro.reset_index(names="month"))
    panel = pd.concat(frames, ignore_index=True)
    return panel.loc[panel["month"].between(SAMPLE_START, SAMPLE_END)].sort_values(["currency", "month"])


def live_curve_recursion(slopes: pd.Series, release_months: int) -> pd.DataFrame:
    """Apply delayed entry and the documented steepening/release update order.

    A crossing observed at month t-1 becomes live at month t.  Release uses
    information through t.  This matches the baseline recursion's timing rather
    than activating the curve in the crossing month itself.
    """
    values = pd.to_numeric(slopes, errors="coerce").to_numpy(float)
    live = False
    eligible = False
    counter = 0
    records: list[dict[str, object]] = []
    for idx, value in enumerate(values):
        previous = values[idx - 1] if idx else np.nan
        pre_previous = values[idx - 2] if idx >= 2 else np.nan
        fresh = False
        released = False
        observed_pair = np.isfinite(value) and np.isfinite(previous)
        lagged_crossing = np.isfinite(previous) and np.isfinite(pre_previous) and pre_previous >= 0 and previous < 0
        if not live and eligible and lagged_crossing:
            live = True
            eligible = False
            counter = 0
            fresh = True
        elif live:
            counter = counter + 1 if observed_pair and value > previous else 0
            if counter >= release_months:
                live = False
                released = True
                counter = 0
                eligible = bool(value >= 0)
        if not live and not eligible and np.isfinite(value) and value >= 0:
            eligible = True
        records.append(
            {
                "fresh_entry": fresh,
                "live": live,
                "steepening_counter": counter,
                "released": released,
                "eligible": eligible,
                "inverted": bool(value < 0) if np.isfinite(value) else False,
                "observed": bool(np.isfinite(value)),
            }
        )
    return pd.DataFrame(records, index=slopes.index)


def build_state(
    yield_panel: pd.DataFrame,
    *,
    state_type: str,
    threshold: int,
    release_months: int,
    excluded_currencies: set[str] | None = None,
    minimum_coverage: int = 6,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    excluded_currencies = excluded_currencies or set()
    work = yield_panel.loc[~yield_panel["currency"].isin(excluded_currencies)].copy()
    audit_frames = []
    for currency, group in work.groupby("currency", sort=True):
        group = group.sort_values("month").set_index("month")
        audit = live_curve_recursion(group["slope_pct"], release_months)
        audit = group.join(audit).reset_index()
        audit["currency"] = currency
        audit_frames.append(audit)
    audit_panel = pd.concat(audit_frames, ignore_index=True)
    monthly = audit_panel.groupby("month").agg(
        observed_curves=("observed", "sum"),
        current_inversions=("inverted", "sum"),
        live_inversions=("live", "sum"),
        fresh_entries=("fresh_entry", "sum"),
    )
    count_column = "live_inversions" if state_type == "live" else "current_inversions"
    monthly["state"] = (monthly[count_column] >= threshold).where(monthly["observed_curves"] >= minimum_coverage)
    monthly["state_type"] = state_type
    monthly["threshold"] = threshold
    monthly["release_months"] = release_months
    return monthly.reset_index(), audit_panel


def equal_tie_carry_weights(group: pd.DataFrame, leg_count: int) -> pd.Series:
    """Allocate each leg equally across all currencies tied at its cutoff."""
    valid = group["formation_policy_diff"].dropna().sort_values()
    out = pd.Series(0.0, index=group.index)
    if len(valid) < 2 * leg_count:
        return out.where(group["formation_policy_diff"].notna(), np.nan)
    low_cutoff = float(valid.iloc[leg_count - 1])
    high_cutoff = float(valid.iloc[-leg_count])
    if low_cutoff >= high_cutoff:
        return pd.Series(np.nan, index=group.index)
    low = group.index[group["formation_policy_diff"] <= low_cutoff]
    high = group.index[group["formation_policy_diff"] >= high_cutoff]
    out.loc[low] = -1.0 / len(low)
    out.loc[high] = 1.0 / len(high)
    return out.where(group["formation_policy_diff"].notna(), np.nan)


def build_currency_panel(leg_count: int, included: set[str] | None = None) -> tuple[pd.DataFrame, pd.Series]:
    spec = load_spec()
    spec = json.loads(json.dumps(spec))
    spec["carry_sort"]["long_count"] = leg_count
    spec["carry_sort"]["short_count"] = leg_count
    policy = load_policy_panel(spec)
    fx = load_fx_panel()
    panel = policy.merge(fx, on=["month", "currency"], how="left")
    panel = panel.loc[panel["month"].between(SAMPLE_START, SAMPLE_END)].copy()
    if included is not None:
        panel = panel.loc[panel["currency"].isin(included)].copy()
    panel = panel.drop(columns=["carry_weight", "carry_leg"], errors="ignore")

    panel["carry_weight"] = panel.groupby("month", group_keys=False).apply(
        lambda group: equal_tie_carry_weights(group, leg_count), include_groups=False
    )
    panel["carry_leg"] = np.select(
        [panel["carry_weight"] > 0, panel["carry_weight"] < 0],
        ["long_high", "short_low"],
        default="middle",
    )

    def aggregate(group: pd.DataFrame) -> float:
        selected = group["carry_weight"].notna() & group["carry_weight"].ne(0)
        if selected.sum() < 2 * leg_count or group.loc[selected, "fx_usd_return_pct"].isna().any():
            return np.nan
        if not np.isclose(group.loc[selected & group["carry_weight"].gt(0), "carry_weight"].sum(), 1.0):
            return np.nan
        if not np.isclose(group.loc[selected & group["carry_weight"].lt(0), "carry_weight"].sum(), -1.0):
            return np.nan
        return float(np.sum(group.loc[selected, "carry_weight"] * group.loc[selected, "fx_usd_return_pct"]))

    outcome = panel.groupby("month").apply(aggregate, include_groups=False).rename("shadow_carry_spot_pct")
    return panel, outcome


def active_difference(state: pd.Series, future_return: pd.Series) -> tuple[float, int, int, int]:
    joined = pd.concat([state.rename("state"), future_return.rename("return")], axis=1).dropna()
    active = joined.loc[joined["state"].astype(bool), "return"]
    inactive = joined.loc[~joined["state"].astype(bool), "return"]
    if active.empty or inactive.empty:
        return np.nan, len(active), len(inactive), 0
    state_values = joined["state"].astype(bool).to_numpy()
    if isinstance(joined.index, pd.PeriodIndex):
        starts_after_gap = np.r_[True, np.diff(joined.index.asi8) != 1]
    else:
        starts_after_gap = np.r_[True, np.zeros(max(len(joined) - 1, 0), dtype=bool)]
    follows_inactive = np.r_[True, ~state_values[:-1]]
    episode_count = int(np.sum(state_values & (starts_after_gap | follows_inactive)))
    return 12.0 * float(active.mean() - inactive.mean()), len(active), len(inactive), episode_count


def circular_reference(state: pd.Series, future_return: pd.Series) -> np.ndarray:
    """Rotate the joined complete-case sequence, including its observed assignment.

    The declared 64-rule family passes one contiguous common calendar. Auxiliary
    deletions can contain internal gaps; for those diagnostics this function
    rotates the compressed complete-case sequence rather than literal calendar
    time. Paper tables disclose that distinction.
    """
    joined = pd.concat([state.rename("state"), future_return.rename("return")], axis=1).dropna()
    events = joined["state"].astype(bool).to_numpy()
    outcomes = joined["return"].to_numpy(float)
    refs = []
    for shift in np.arange(len(joined)):
        rotated = np.roll(events, shift)
        refs.append(12.0 * (outcomes[rotated].mean() - outcomes[~rotated].mean()))
    return np.asarray(refs, float)


def two_sided_rank(reference: np.ndarray) -> float:
    observed = float(reference[0])
    return min(1.0, 2.0 * min(float(np.mean(reference <= observed)), float(np.mean(reference >= observed))))


def specification_family(yield_panel: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, np.ndarray]]:
    outcomes = {leg: build_currency_panel(leg)[1] for leg in (2, 3)}
    state_cache: dict[tuple[str, int, int], pd.Series] = {}
    for state_type in ("live", "raw"):
        releases = (1, 2, 3) if state_type == "live" else (0,)
        for release in releases:
            for threshold in (1, 2, 3, 4):
                state_frame, _ = build_state(
                    yield_panel,
                    state_type=state_type,
                    threshold=threshold,
                    release_months=max(release, 1),
                )
                state_cache[(state_type, release, threshold)] = state_frame.set_index("month")["state"]

    # Every family statistic uses the same literal calendar and the same shift.
    # The two-month return horizon determines the common endpoint.
    calendar = pd.period_range(SAMPLE_START, SAMPLE_END, freq="M")
    complete = pd.Series(True, index=calendar)
    for state in state_cache.values():
        complete &= state.reindex(calendar).notna()
    for leg_count in (2, 3):
        for return_lag in (1, 2):
            complete &= outcomes[leg_count].shift(-return_lag).reindex(calendar).notna()
    common_calendar = calendar[complete.to_numpy()]
    if common_calendar.empty:
        raise ValueError("The declared specification family has no common complete-case calendar.")

    rows: list[dict[str, object]] = []
    references: dict[str, np.ndarray] = {}
    for state_type in ("live", "raw"):
        releases = (1, 2, 3) if state_type == "live" else (0,)
        for release in releases:
            for threshold in (1, 2, 3, 4):
                state = state_cache[(state_type, release, threshold)].reindex(common_calendar)
                for return_lag in (1, 2):
                    for leg_count in (2, 3):
                        future = outcomes[leg_count].shift(-return_lag).reindex(common_calendar)
                        estimate, active, inactive, episodes = active_difference(state, future)
                        key = f"{state_type}_b{threshold}_r{release}_lag{return_lag}_leg{leg_count}"
                        ref = circular_reference(state, future)
                        references[key] = ref
                        rows.append(
                            {
                                "specification": key,
                                "state_type": state_type,
                                "breadth_threshold": threshold,
                                "release_months": release,
                                "return_lag_months": return_lag,
                                "carry_leg_count": leg_count,
                                "active_months": active,
                                "inactive_months": inactive,
                                "episodes": episodes,
                                "annualized_active_minus_inactive_pp": estimate,
                                "p_circular_raw": two_sided_rank(ref),
                                "baseline_like": key == "live_b2_r2_lag1_leg3",
                                "common_calendar_start": str(common_calendar.min()),
                                "common_calendar_end": str(common_calendar.max()),
                                "common_calendar_months": len(common_calendar),
                            }
                        )
    results = pd.DataFrame(rows)
    standardized = []
    keys = results["specification"].tolist()
    for key in keys:
        ref = references[key]
        scale = float(np.std(ref, ddof=1))
        if not np.isfinite(scale) or scale == 0:
            raise ValueError(f"Degenerate common-calendar reference for {key}.")
        standardized.append((ref - float(np.mean(ref))) / scale)
    max_abs = np.max(np.abs(np.column_stack(standardized)), axis=1)
    results["p_maxT_family"] = [float(np.mean(max_abs >= abs(z[0]))) for z in standardized]
    results["estimate_rank_of_64_low_to_high"] = results["annualized_active_minus_inactive_pp"].rank(method="min").astype(int)
    return results.sort_values(
        ["state_type", "return_lag_months", "carry_leg_count", "breadth_threshold", "release_months"]
    ), references


def leave_one_country_out(yield_panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    all_currencies = set(yield_panel["currency"].unique())
    for excluded in sorted(all_currencies):
        state_frame, _ = build_state(
            yield_panel,
            state_type="live",
            threshold=2,
            release_months=2,
            excluded_currencies={excluded},
            minimum_coverage=5,
        )
        _, outcome = build_currency_panel(3, included=all_currencies - {excluded})
        state = state_frame.set_index("month")["state"]
        future = outcome.shift(-1)
        estimate, active, inactive, episodes = active_difference(state, future)
        ref = circular_reference(state, future)
        rows.append(
            {
                "excluded_from_signal_and_outcome": excluded,
                "sensor_currency_count": len(all_currencies) - 1,
                "minimum_curve_coverage": 5,
                "annualized_active_minus_inactive_pp": estimate,
                "p_circular_raw": two_sided_rank(ref),
                "active_months": active,
                "episodes": episodes,
            }
        )
    return pd.DataFrame(rows)


def geographically_disjoint(yield_panel: pd.DataFrame) -> pd.DataFrame:
    groups = {
        "European curves -> non-European currencies": (
            {"CHF", "EUR", "GBP", "NOK", "SEK"}, {"AUD", "CAD", "JPY", "NZD"}, 1
        ),
        "Non-European curves -> European currencies": (
            {"AUD", "CAD", "JPY", "NZD"}, {"CHF", "EUR", "GBP", "NOK", "SEK"}, 2
        ),
    }
    rows = []
    all_currencies = set(yield_panel["currency"].unique())
    for label, (sensors, bearers, leg_count) in groups.items():
        minimum_coverage = max(3, len(sensors) - 1)
        state_frame, _ = build_state(
            yield_panel,
            state_type="live",
            threshold=2,
            release_months=2,
            excluded_currencies=all_currencies - sensors,
            minimum_coverage=minimum_coverage,
        )
        _, outcome = build_currency_panel(leg_count, included=bearers)
        state = state_frame.set_index("month")["state"]
        future = outcome.shift(-1)
        estimate, active, inactive, episodes = active_difference(state, future)
        ref = circular_reference(state, future)
        rows.append(
            {
                "split": label,
                "sensor_currencies": "+".join(sorted(sensors)),
                "outcome_currencies": "+".join(sorted(bearers)),
                "outcome_leg_count": leg_count,
                "sensor_currency_count": len(sensors),
                "minimum_curve_coverage": minimum_coverage,
                "annualized_active_minus_inactive_pp": estimate,
                "p_circular_raw": two_sided_rank(ref),
                "active_months": active,
                "episodes": episodes,
            }
        )
    return pd.DataFrame(rows)


def baseline_ledgers(yield_panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    state, audit = build_state(yield_panel, state_type="live", threshold=2, release_months=2)
    _, outcome = build_currency_panel(3)
    monthly = state.set_index("month").join(outcome.shift(-1).rename("next_month_shadow_carry_spot_pct"))
    monthly["episode_onset"] = monthly["state"].fillna(False).astype(bool) & ~monthly["state"].fillna(False).astype(bool).shift(1, fill_value=False)
    monthly["episode_id"] = monthly["episode_onset"].cumsum().where(monthly["state"].fillna(False).astype(bool))
    episodes = []
    for episode_id, group in monthly.dropna(subset=["episode_id"]).groupby("episode_id"):
        episodes.append(
            {
                "episode_id": int(episode_id),
                "onset_month": str(group.index.min()),
                "end_month": str(group.index.max()),
                "duration_months": len(group),
                "cumulative_next_month_shadow_carry_spot_pct": group["next_month_shadow_carry_spot_pct"].sum(min_count=1),
                "worst_next_month_shadow_carry_spot_pct": group["next_month_shadow_carry_spot_pct"].min(),
            }
        )
    return monthly.reset_index(), audit, pd.DataFrame(episodes)


def baseline_sensitivities(monthly: pd.DataFrame) -> pd.DataFrame:
    work = monthly.set_index("month").copy()
    state = work["state"].astype("boolean")
    outcome = work["next_month_shadow_carry_spot_pct"]
    # Match the literal common calendar used by the two-horizon family.
    valid = state.notna() & outcome.notna() & (work.index <= SAMPLE_END - 2)
    named_crisis_months = {pd.Period("1998-09", "M"), pd.Period("2008-10", "M"), pd.Period("2020-03", "M")}
    crisis_episode_ids = set(work.loc[work.index.isin(named_crisis_months), "episode_id"].dropna().astype(int))
    masks = {
        "full_sample": valid,
        "exclude_episodes_containing_1998_09_2008_10_2020_03": valid & ~work["episode_id"].isin(crisis_episode_ids),
        "first_calendar_half_1988_2004": valid & (work.index <= pd.Period("2004-12", "M")),
        "second_calendar_half_2005_2025": valid & (work.index >= pd.Period("2005-01", "M")),
    }
    rows = []
    for label, mask in masks.items():
        estimate, active, inactive, episodes = active_difference(state.loc[mask], outcome.loc[mask])
        ref = circular_reference(state.loc[mask], outcome.loc[mask])
        rows.append({
            "sensitivity": label,
            "annualized_active_minus_inactive_pp": estimate,
            "p_circular_raw": two_sided_rank(ref),
            "active_months": active,
            "inactive_months": inactive,
            "episodes": episodes,
        })
    active_valid = work.loc[valid & state.astype(bool), "next_month_shadow_carry_spot_pct"].nsmallest(5).index
    trimmed_mask = valid & ~work.index.isin(active_valid)
    estimate, active, inactive, episodes = active_difference(state.loc[trimmed_mask], outcome.loc[trimmed_mask])
    rows.append({
        "sensitivity": "delete_five_worst_active_months_outcome_conditioned_diagnostic",
        "annualized_active_minus_inactive_pp": estimate,
        "p_circular_raw": np.nan,
        "active_months": active,
        "inactive_months": inactive,
        "episodes": episodes,
    })
    return pd.DataFrame(rows)


def plot_specification_curve(results: pd.DataFrame, path: Path) -> None:
    ordered = results.sort_values(
        ["active_months", "state_type", "breadth_threshold", "release_months", "return_lag_months", "carry_leg_count"]
    ).reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(10, 5.6))
    colors = np.where(ordered["baseline_like"], "#b22222", np.where(ordered["state_type"].eq("live"), "#315f8a", "#929292"))
    ax.scatter(np.arange(len(ordered)), ordered["annualized_active_minus_inactive_pp"], c=colors, s=np.where(ordered["baseline_like"], 55, 25), alpha=0.9)
    ax.axhline(0, color="black", linewidth=0.8)
    baseline_index = int(np.flatnonzero(ordered["baseline_like"].to_numpy())[0])
    baseline_value = float(ordered.loc[baseline_index, "annualized_active_minus_inactive_pp"])
    ax.annotate("baseline-like public proxy", (baseline_index, baseline_value), xytext=(8, 12), textcoords="offset points", fontsize=9)
    ax.set_xlabel("Declared specifications ordered by active-state frequency (then rule fields)")
    ax.set_ylabel("Annualized active-minus-inactive log spot-return proxy (pp)")
    ax.set_title("Public 10Y-3M proxy: complete 64-rule specification family")
    ax.text(0.01, 0.02, "Blue: live-state rules   Gray: raw inversion rules   Red: baseline-like rule", transform=ax.transAxes, fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_report(specs: pd.DataFrame, loo: pd.DataFrame, disjoint: pd.DataFrame, episodes: pd.DataFrame, sensitivities: pd.DataFrame) -> str:
    baseline = specs.loc[specs["baseline_like"]].iloc[0]
    negative_share = float((specs["annualized_active_minus_inactive_pp"] < 0).mean())
    max_hits = int((specs["p_maxT_family"] <= 0.05).sum())
    loo_negative = int((loo["annualized_active_minus_inactive_pp"] < 0).sum())
    lines = [
        "# V0.3 independent public yield-curve proxy audit",
        "",
        "## Evidentiary boundary",
        "",
        "This exercise is **not a replication of the paper's synchronized-inversion state**. It uses current-vintage OECD monthly 10-year government yields minus 3-month interbank rates delivered through FRED rather than the baseline end-of-month 10Y-minus-2Y panel. The public outcome is a BIS policy-ranked log spot-return proxy, not an executable forward excess return.",
        "",
        "## Main result",
        "",
        f"The baseline-like public rule (fresh entry, two-curve breadth, two consecutive steepening months for release, a target of three currencies per side with all cutoff ties equally weighted, and a next-month outcome) has an annualized active-minus-inactive log spot-return-proxy difference of **{baseline['annualized_active_minus_inactive_pp']:.2f} percentage points** across {int(baseline['active_months'])} active months and {int(baseline['episodes'])} episodes. Its inclusive circular-shift reference value is {baseline['p_circular_raw']:.3f}; its common-calendar maximum-standardized-coefficient reference value across the declared 64-rule family is {baseline['p_maxT_family']:.3f}.",
        "",
        f"Across all 64 rules, {negative_share:.0%} have a negative coefficient and {max_hits} meet the 5% common-calendar maximum-standardized-coefficient reference criterion. The baseline-like estimate ranks {int(baseline['estimate_rank_of_64_low_to_high'])} of 64 from most negative to most positive. Under simultaneous cyclic-shift exchangeability, the maximum reference controls the declared family; otherwise it is a finite rotation-reference diagnostic.",
        "",
        "## Same-universe concern",
        "",
        f"When each currency is jointly deleted from signal construction and the public carry outcome, {loo_negative} of 9 influence estimates are negative. Each state requires five of the remaining eight curves. These are sensitivity checks, not nine independent tests: the samples and event calendars overlap heavily.",
        "",
        "| Excluded | Annualized pp | Raw rotation ref. | Active months | Episodes |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in loo.itertuples(index=False):
        lines.append(f"| {row.excluded_from_signal_and_outcome} | {row.annualized_active_minus_inactive_pp:.2f} | {row.p_circular_raw:.3f} | {row.active_months} | {row.episodes} |")
    lines.extend([
        "",
        "The geographically disjoint checks are stronger conceptually because no currency supplying the curve signal appears in the outcome basket. The European sensor requires four of five curves; the non-European sensor requires three of four:",
        "",
        "| Split | Annualized pp | Raw rotation ref. | Active months | Episodes |",
        "|---|---:|---:|---:|---:|",
    ])
    for row in disjoint.itertuples(index=False):
        lines.append(f"| {row.split} | {row.annualized_active_minus_inactive_pp:.2f} | {row.p_circular_raw:.3f} | {row.active_months} | {row.episodes} |")
    lines.extend([
        "",
        "The disjoint evidence is asymmetric: European curves precede losses in the non-European basket, but the reverse direction is approximately zero. This is not a general two-way validation of common information. The deletion and disjoint references rotate each complete-case sequence after missing observations are dropped, so internal calendar gaps are compressed.",
        "",
        "## Concentration and calendar sensitivity",
        "",
        "| Check | Annualized pp | Raw rotation ref. | Active months | Episodes |",
        "|---|---:|---:|---:|---:|",
    ])
    for row in sensitivities.itertuples(index=False):
        p = "--" if pd.isna(row.p_circular_raw) else f"{row.p_circular_raw:.3f}"
        lines.append(f"| {row.sensitivity} | {row.annualized_active_minus_inactive_pp:.2f} | {p} | {row.active_months} | {row.episodes} |")
    lines.extend([
        "",
        "The five-worst-month deletion is deliberately labeled outcome-conditioned and receives no p-value. It is a concentration diagnostic, not a preferred estimator.",
        "",
        "## Interpretation rule for v0.3",
        "",
        "- A broadly negative family with a non-extreme baseline is descriptive sign resemblance, not independent confirmation, when no rule exceeds the common-calendar family reference threshold.",
        "- If only a few rules are negative or the baseline-like rule is an extremum, the public proxy should be reported as sensitive to state definition.",
        "- Disjoint results can support a common-information interpretation only as associations. Monthly current-vintage data, small episode counts, and the spot-only outcome prevent a claim of implementable predictability or structural identification.",
        "",
        "## What remains impossible in this repository",
        "",
        "The absent author 10Y-minus-2Y panel still prevents an audit of the original fifteen episodes, the exact 92 active months, the headline carry and beta portfolios, author-data leave-one-country-out states, and search-adjusted inference for the actual state family. No result here should be substituted for those missing tests.",
        "",
        f"The baseline public proxy contains {len(episodes)} contiguous episodes; the complete episode ledger is supplied as a machine-readable output.",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / "data").mkdir(exist_ok=True)
    (OUTPUT_ROOT / "figures").mkdir(exist_ok=True)
    yield_panel = load_yield_panel()
    specs, _ = specification_family(yield_panel)
    loo = leave_one_country_out(yield_panel)
    disjoint = geographically_disjoint(yield_panel)
    monthly, audit, episodes = baseline_ledgers(yield_panel)
    sensitivities = baseline_sensitivities(monthly)

    artifacts = {
        "specifications": OUTPUT_ROOT / "data" / "specification_family.csv",
        "leave_one_out": OUTPUT_ROOT / "data" / "leave_one_country_out.csv",
        "disjoint": OUTPUT_ROOT / "data" / "geographically_disjoint.csv",
        "monthly": OUTPUT_ROOT / "data" / "baseline_monthly_state.csv",
        "curve_audit": OUTPUT_ROOT / "data" / "baseline_curve_recursion_audit.csv",
        "episodes": OUTPUT_ROOT / "data" / "baseline_episode_ledger.csv",
        "sensitivities": OUTPUT_ROOT / "data" / "baseline_sensitivities.csv",
        "figure": OUTPUT_ROOT / "figures" / "specification_curve.png",
        "report": OUTPUT_ROOT / "public_yield_proxy_report.md",
    }
    for frame, key in [
        (specs, "specifications"), (loo, "leave_one_out"), (disjoint, "disjoint"),
        (monthly, "monthly"),
        (audit[["month", "currency", "long_series_id", "short_series_id", "fresh_entry", "live", "steepening_counter", "released", "eligible", "inverted", "observed"]], "curve_audit"),
        (episodes, "episodes"), (sensitivities, "sensitivities"),
    ]:
        frame.to_csv(artifacts[key], index=False, lineterminator="\n")
    plot_specification_curve(specs, artifacts["figure"])
    artifacts["report"].write_text(write_report(specs, loo, disjoint, episodes, sensitivities), encoding="utf-8", newline="\n")

    spec = load_spec()
    policy_files = [
        PIPELINE_ROOT / "data" / "raw" / "bis_policy_rates" / f"M_{country}.csv"
        for country in [*spec["country_to_currency"].keys(), "US"]
    ]
    fx_files = sorted((PIPELINE_ROOT / "data" / "raw" / "bis_exchange_rates").glob("*.csv"))
    raw_files = sorted(RAW_ROOT.glob("*.csv")) + policy_files + fx_files
    code_and_config = [
        Path(__file__).resolve(),
        PIPELINE_ROOT / "src" / "render_v03_public_tables.py",
        PIPELINE_ROOT / "src" / "mechanism" / "panel.py",
        PIPELINE_ROOT / "config" / "mechanism_spec.json",
        PIPELINE_ROOT / "config" / "sources.json",
    ]
    run_head = os.environ.get("IYC_RUN_HEAD")
    run_started_clean = os.environ.get("IYC_RUN_STARTED_CLEAN")
    if run_head and run_started_clean in {"true", "false"}:
        git_head = run_head
        git_dirty = run_started_clean != "true"
    else:
        try:
            git_head = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT, check=True,
                capture_output=True, text=True,
            ).stdout.strip()
            git_dirty = bool(subprocess.run(
                ["git", "status", "--porcelain"], cwd=PROJECT_ROOT, check=True,
                capture_output=True, text=True,
            ).stdout.strip())
        except (FileNotFoundError, subprocess.CalledProcessError):
            git_head, git_dirty = None, None
    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python": platform.python_version(),
        "environment": {
            "platform": platform.platform(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "matplotlib": __import__("matplotlib").__version__,
        },
        "git": {"head_at_run": git_head, "worktree_dirty_at_run": git_dirty},
        "sample": [str(SAMPLE_START), str(SAMPLE_END)],
        "evidentiary_boundary": "independent current-vintage 10Y-3M public proxy; not author-state replication",
        "raw_inputs": [{"path": str(path.relative_to(PROJECT_ROOT)).replace("\\", "/"), "sha256": sha256_file(path), "bytes": path.stat().st_size} for path in raw_files],
        "code_and_config_inputs": [
            {"path": str(path.relative_to(PROJECT_ROOT)).replace("\\", "/"), "sha256": sha256_file(path), "bytes": path.stat().st_size}
            for path in code_and_config
        ],
        "outputs": [{"path": str(path.relative_to(PROJECT_ROOT)).replace("\\", "/"), "sha256": sha256_file(path), "bytes": path.stat().st_size} for path in artifacts.values()],
    }
    manifest_path = OUTPUT_ROOT / "run_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(artifacts["report"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
