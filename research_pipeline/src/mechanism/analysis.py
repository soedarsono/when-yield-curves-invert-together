"""Run prespecified public-proxy event checks and build machine-readable results."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .inference import circular_shift_pvalue, circular_shift_reference, episode_bootstrap_ci, event_values, hac_intercept_slope, holm_adjust, leave_one_range
from .panel import build_public_panel, load_cftc_monthly, load_external_monthly, synchronized_easing


def _full_month_grid(monthly: pd.DataFrame, spec: dict) -> pd.DataFrame:
    grid = pd.DataFrame({"month": pd.period_range(spec["sample_start"], spec["sample_end"], freq="M")})
    return grid.merge(monthly, on="month", how="left").sort_values("month").reset_index(drop=True)


def _result(
    result_id: str, label: str, series: pd.Series, events: pd.Series, horizon: int, mode: str,
    unit: str, evidence_type: str, interpretation: str, limitation: str, spec: dict,
) -> dict:
    values = series.to_numpy(float)
    indicator = events.fillna(False).to_numpy(bool)
    estimate, p, n_events, reference_count = circular_shift_pvalue(values, indicator, horizon, mode)
    per_event = event_values(values, indicator, horizon, mode)
    ci_low, ci_high = episode_bootstrap_ci(per_event, int(spec["bootstrap_draws"]), int(spec["random_seed"]) + 100 + horizon)
    loo_low, loo_high = leave_one_range(per_event)
    return {
        "result_id": result_id, "label": label, "evidence_type": evidence_type,
        "estimate": estimate, "unit": unit, "horizon_months": horizon,
        "event_count": n_events, "p_randomization_raw": p,
        "rotation_reference_count_including_observed": reference_count,
        "randomization_method": "all circular rotations; same valid-event count; doubled smaller-tail inclusive rank",
        "p_holm_primary_family": np.nan, "ci90_episode_bootstrap_low": ci_low,
        "ci90_episode_bootstrap_high": ci_high, "leave_one_episode_low": loo_low,
        "leave_one_episode_high": loo_high, "interpretation": interpretation,
        "limitation": limitation,
    }


def run_empirical(spec: dict) -> dict[str, pd.DataFrame]:
    currency, monthly = build_public_panel(spec)
    cftc_currency, cftc = load_cftc_monthly(currency, spec)
    external = load_external_monthly(spec)
    analysis = _full_month_grid(monthly, spec).merge(cftc, on="month", how="left").merge(external, on="month", how="left")
    events = analysis["easing_onset"]
    rows = [
        _result("fx_shadow_carry_h1", "Policy-ranked shadow carry spot return, months 0--1", analysis["shadow_carry_spot_pct"], events, 1, "sum", "percentage points cumulative", "empirical public proxy", "Whether currencies with high lagged policy rates depreciate relative to low-rate currencies around synchronized delivered easing.", "BIS spot rates and policy-rate ranks are not tradable forward excess returns; the event is delivered easing, not the paper's yield-curve signal.", spec),
        _result("cftc_carry_crowding_h3", "Carry-aligned CFTC non-commercial net share, change through month 3", analysis["cftc_carry_crowding_pct_oi"], events, 3, "change", "percentage points of open interest", "empirical public proxy", "Whether speculative futures positions aligned with the public carry rank unwind around synchronized easing.", "Only seven matchable currency contracts; legacy non-commercial categories are coarse; release is assumed three calendar days after report date.", spec),
        _result("acm_expected_path_h3", "ACM 10-year expected-rate component, change through month 3", analysis["acm_expected_path_10y_pct"], events, 3, "change", "percentage points", "empirical public proxy", "Whether the U.S. expected-rate component falls around synchronized easing.", "U.S. 10-year decomposition only; it is not a foreign-country slope decomposition and is current-vintage.", spec),
        _result("acm_term_premium_h3", "ACM 10-year term premium, change through month 3", analysis["acm_term_premium_10y_pct"], events, 3, "change", "percentage points", "empirical public proxy", "Whether a common term-premium movement is comparable to the expected-rate movement around synchronized easing.", "A 10-year U.S. term premium is an alternative-state diagnostic, not the 10Y-minus-2Y foreign slope premium used in the paper.", spec),
        _result("oecd_g7_cli_h6", "OECD G7 CLI, change through month 6", analysis["oecd_g7_cli"], events, 6, "change", "index points", "empirical public proxy", "Whether synchronized easing is followed by weaker current-vintage G7 leading activity.", "The amplitude-adjusted CLI is revised and partly constructed from forward-looking inputs; this is not a real-time outcome test.", spec),
        _result("fred_nfci_h3", "Chicago Fed NFCI, change through month 3", analysis["NFCI"], events, 3, "change", "index points", "empirical public proxy", "Whether U.S. financial conditions tighten around synchronized easing.", "U.S.-centric and current-vintage; it cannot establish that easing caused financial stress.", spec),
        _result("fred_vix_h1", "VIX, change through month 1", analysis["VIXCLS"], events, 1, "change", "index points", "empirical public proxy", "Whether equity-implied volatility rises around synchronized easing.", "VIX starts in 1990 and is an overlapping risk-state indicator, not independent identification.", spec),
    ]
    results = pd.DataFrame(rows)
    rotation_definitions = [
        ("fx_shadow_carry_h1", analysis["shadow_carry_spot_pct"], 1, "sum"),
        ("cftc_carry_crowding_h3", analysis["cftc_carry_crowding_pct_oi"], 3, "change"),
        ("acm_expected_path_h3", analysis["acm_expected_path_10y_pct"], 3, "change"),
        ("acm_term_premium_h3", analysis["acm_term_premium_10y_pct"], 3, "change"),
        ("oecd_g7_cli_h6", analysis["oecd_g7_cli"], 6, "change"),
        ("fred_nfci_h3", analysis["NFCI"], 3, "change"),
        ("fred_vix_h1", analysis["VIXCLS"], 1, "change"),
    ]
    rotation_frames = []
    for result_id, series, horizon, mode in rotation_definitions:
        audit = circular_shift_reference(series.to_numpy(float), events.fillna(False).to_numpy(bool), horizon, mode)
        audit.insert(0, "result_id", result_id)
        rotation_frames.append(audit)
    rotation_audit = pd.concat(rotation_frames, ignore_index=True)
    primary = set(spec["primary_tests"])
    adjusted = holm_adjust({r.result_id: r.p_randomization_raw for r in results.itertuples() if r.result_id in primary})
    for key, value in adjusted.items():
        results.loc[results["result_id"] == key, "p_holm_primary_family"] = value

    hac = hac_intercept_slope(
        analysis["shadow_carry_spot_pct"].to_numpy(float), analysis["synchronized_easing"].fillna(False).astype(float).to_numpy(), int(spec["hac_lags"])
    )
    hac_table = pd.DataFrame([{"series": "shadow_carry_spot_pct", "regressor": "synchronized_easing", **hac, "unit": "percentage points per month"}])

    sensitivity_rows = []
    for threshold in [int(spec["synchronized_easing"]["baseline_country_count"]), *map(int, spec["synchronized_easing"]["sensitivity_country_counts"])]:
        event_frame = synchronized_easing(currency, spec, threshold=threshold).set_index("month")
        indicator = analysis["month"].map(event_frame["easing_onset"]).fillna(False)
        estimate, p, n, reference_count = circular_shift_pvalue(
            analysis["shadow_carry_spot_pct"].to_numpy(float), indicator.to_numpy(bool), 1, "sum"
        )
        sensitivity_rows.append({"sensitivity": f"cut_count_threshold_{threshold}", "estimate": estimate, "p_randomization": p, "event_count": n, "rotation_reference_count_including_observed": reference_count, "unit": "percentage points cumulative, months 0--1"})
    for currency_code in spec["currencies"]:
        event_frame = synchronized_easing(currency, spec, drop_currency=currency_code).set_index("month")
        indicator = analysis["month"].map(event_frame["easing_onset"]).fillna(False)
        estimate, p, n, reference_count = circular_shift_pvalue(
            analysis["shadow_carry_spot_pct"].to_numpy(float), indicator.to_numpy(bool), 1, "sum"
        )
        sensitivity_rows.append({"sensitivity": f"leave_event_currency_{currency_code}", "estimate": estimate, "p_randomization": p, "event_count": n, "rotation_reference_count_including_observed": reference_count, "unit": "percentage points cumulative, months 0--1"})
    sensitivity = pd.DataFrame(sensitivity_rows)
    onsets = analysis.loc[analysis["easing_onset"].fillna(False), ["month", "cut_count", "country_coverage"]].copy()
    onsets["month"] = onsets["month"].astype(str)
    return {
        "currency_panel": currency, "monthly_panel": analysis, "cftc_currency": cftc_currency,
        "results": results, "rotation_audit": rotation_audit, "hac": hac_table, "sensitivity": sensitivity, "onsets": onsets,
    }
