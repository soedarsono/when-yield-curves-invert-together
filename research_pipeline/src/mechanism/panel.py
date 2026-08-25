"""Construct transparent monthly public-data proxies for mechanism checks."""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
PIPELINE_ROOT = PROJECT_ROOT / "research_pipeline"


def load_spec() -> dict:
    return json.loads((PIPELINE_ROOT / "config" / "mechanism_spec.json").read_text(encoding="utf-8"))


def _period(values: pd.Series) -> pd.PeriodIndex:
    return pd.to_datetime(values, errors="coerce").dt.to_period("M")


def load_policy_panel(spec: dict) -> pd.DataFrame:
    frames = []
    mapping = spec["country_to_currency"]
    for country, currency in mapping.items():
        path = PIPELINE_ROOT / "data" / "raw" / "bis_policy_rates" / f"M_{country}.csv"
        frame = pd.read_csv(path, usecols=["REF_AREA", "TIME_PERIOD", "OBS_VALUE", "COMPILATION", "TITLE"])
        frame = frame.assign(month=_period(frame["TIME_PERIOD"]), currency=currency)
        frame["policy_rate"] = pd.to_numeric(frame["OBS_VALUE"], errors="coerce")
        frames.append(frame[["month", "currency", "policy_rate", "COMPILATION", "TITLE"]])
    us = pd.read_csv(
        PIPELINE_ROOT / "data" / "raw" / "bis_policy_rates" / "M_US.csv",
        usecols=["TIME_PERIOD", "OBS_VALUE"],
    )
    us = us.assign(month=_period(us["TIME_PERIOD"]), us_policy_rate=pd.to_numeric(us["OBS_VALUE"], errors="coerce"))
    panel = pd.concat(frames, ignore_index=True).merge(us[["month", "us_policy_rate"]], on="month", how="left")
    panel["policy_diff_us"] = panel["policy_rate"] - panel["us_policy_rate"]
    panel = panel.sort_values(["currency", "month"])
    panel["policy_change_pp"] = panel.groupby("currency")["policy_rate"].diff()
    panel["formation_policy_diff"] = panel.groupby("currency")["policy_diff_us"].shift(
        int(spec["carry_sort"]["formation_lag_months"])
    )
    return panel


def load_fx_panel() -> pd.DataFrame:
    frames = []
    for path in sorted((PIPELINE_ROOT / "data" / "raw" / "bis_exchange_rates").glob("*.csv")):
        frame = pd.read_csv(path, usecols=["TIME_PERIOD", "CURRENCY", "OBS_VALUE", "TITLE"])
        frame = frame.assign(month=_period(frame["TIME_PERIOD"]), fx_lcu_per_usd=pd.to_numeric(frame["OBS_VALUE"], errors="coerce"))
        frame = frame.sort_values("month")
        # BIS WS_XRU files here are local-currency units per USD for every currency.
        # A fall is foreign-currency appreciation; negate the log change to express
        # the return on one unit of foreign currency in USD.
        frame["fx_usd_return_pct"] = -100.0 * np.log(frame["fx_lcu_per_usd"]).diff()
        frames.append(frame[["month", "CURRENCY", "fx_lcu_per_usd", "fx_usd_return_pct", "TITLE"]].rename(columns={"CURRENCY": "currency", "TITLE": "fx_title"}))
    return pd.concat(frames, ignore_index=True)


def assign_carry_weights(panel: pd.DataFrame, spec: dict) -> pd.DataFrame:
    long_count = int(spec["carry_sort"]["long_count"])
    short_count = int(spec["carry_sort"]["short_count"])

    def weights(group: pd.DataFrame) -> pd.Series:
        valid = group["formation_policy_diff"].dropna().sort_values()
        out = pd.Series(0.0, index=group.index)
        if len(valid) < long_count + short_count:
            return out.where(group["formation_policy_diff"].notna(), np.nan)
        low_cutoff = float(valid.iloc[short_count - 1])
        high_cutoff = float(valid.iloc[-long_count])
        if low_cutoff >= high_cutoff:
            return pd.Series(np.nan, index=group.index)
        low = group.index[group["formation_policy_diff"] <= low_cutoff]
        high = group.index[group["formation_policy_diff"] >= high_cutoff]
        out.loc[low] = -1.0 / len(low)
        out.loc[high] = 1.0 / len(high)
        return out.where(group["formation_policy_diff"].notna(), np.nan)

    out = panel.copy()
    monthly_weights = [weights(group) for _, group in out.groupby("month", sort=False)]
    out["carry_weight"] = pd.concat(monthly_weights).reindex(out.index) if monthly_weights else np.nan
    out["carry_leg"] = np.select([out["carry_weight"] > 0, out["carry_weight"] < 0], ["long_high", "short_low"], default="middle")
    return out


def aggregate_shadow_spot(group: pd.DataFrame, minimum_target_count: int) -> float:
    """Aggregate selected currency returns, rejecting incomplete realized legs."""
    selected = group["carry_weight"].notna() & group["carry_weight"].ne(0)
    if selected.sum() < minimum_target_count:
        return np.nan
    if group.loc[selected, "fx_usd_return_pct"].isna().any():
        return np.nan
    long_weight = group.loc[selected & group["carry_weight"].gt(0), "carry_weight"].sum()
    short_weight = group.loc[selected & group["carry_weight"].lt(0), "carry_weight"].sum()
    if not np.isclose(long_weight, 1.0) or not np.isclose(short_weight, -1.0):
        return np.nan
    return float(np.sum(group.loc[selected, "carry_weight"] * group.loc[selected, "fx_usd_return_pct"]))


def at_least_rate_cut(changes: pd.Series, minimum_cut_pp: float) -> pd.Series:
    """Classify cuts at the stated threshold without binary-float boundary loss."""
    numeric = pd.to_numeric(changes, errors="coerce")
    threshold = -abs(float(minimum_cut_pp))
    at_boundary = np.isclose(
        numeric.to_numpy(dtype=float),
        threshold,
        rtol=0.0,
        atol=1e-12,
        equal_nan=False,
    )
    return numeric.lt(threshold) | pd.Series(at_boundary, index=numeric.index)


def synchronized_easing(policy: pd.DataFrame, spec: dict, threshold: int | None = None, drop_currency: str | None = None) -> pd.DataFrame:
    cfg = spec["synchronized_easing"]
    threshold = int(threshold or cfg["baseline_country_count"])
    work = policy.copy()
    if drop_currency:
        work = work.loc[work["currency"] != drop_currency]
    work["cut"] = at_least_rate_cut(work["policy_change_pp"], cfg["minimum_cut_pp"])
    monthly = work.groupby("month").agg(cut_count=("cut", "sum"), country_coverage=("policy_change_pp", "count"))
    monthly["synchronized_easing"] = (monthly["cut_count"] >= threshold) & (
        monthly["country_coverage"] >= int(cfg["minimum_country_coverage"])
    )
    quiet = int(cfg["quiet_months_before_onset"])
    recent = pd.concat([monthly["synchronized_easing"].shift(i, fill_value=False) for i in range(1, quiet + 1)], axis=1).any(axis=1)
    monthly["easing_onset"] = monthly["synchronized_easing"] & ~recent
    monthly["easing_episode"] = monthly["easing_onset"].cumsum().where(monthly["synchronized_easing"])
    monthly["threshold"] = threshold
    return monthly.reset_index()


def build_public_panel(spec: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    policy = assign_carry_weights(load_policy_panel(spec), spec)
    fx = load_fx_panel()
    currency = policy.merge(fx, on=["month", "currency"], how="left")
    start, end = pd.Period(spec["sample_start"], "M"), pd.Period(spec["sample_end"], "M")
    currency = currency.loc[currency["month"].between(start, end)].copy()
    monthly = synchronized_easing(currency, spec).set_index("month")
    minimum_target_count = int(spec["carry_sort"]["long_count"]) + int(spec["carry_sort"]["short_count"])
    shadow = currency.groupby("month").apply(
        lambda g: pd.Series(
            {
                "shadow_carry_spot_pct": aggregate_shadow_spot(g, minimum_target_count),
                "mean_policy_rate": g["policy_rate"].mean(),
                "mean_policy_change_pp": g["policy_change_pp"].mean(),
                "currency_coverage": g["fx_usd_return_pct"].notna().sum(),
            }
        ),
        include_groups=False,
    )
    monthly = monthly.join(shadow, how="left")
    return currency, monthly.reset_index()


def load_cftc_monthly(currency_panel: pd.DataFrame, spec: dict) -> pd.DataFrame:
    crosswalk = pd.read_csv(PIPELINE_ROOT / "config" / "cftc_contract_crosswalk.csv", dtype={"contract_code": str})
    crosswalk["contract_code"] = crosswalk["contract_code"].str.zfill(6)
    crosswalk["start"] = pd.to_datetime(crosswalk["start"])
    crosswalk["end"] = pd.to_datetime(crosswalk["end"])
    frames = []
    columns = [
        "Market and Exchange Names", "As of Date in Form YYYY-MM-DD", "CFTC Contract Market Code",
        "Open Interest (All)", "Noncommercial Positions-Long (All)", "Noncommercial Positions-Short (All)",
    ]
    sample_end_year = pd.Period(spec["sample_end"], "M").year
    cftc_paths = sorted((PIPELINE_ROOT / "data" / "raw" / "cftc_legacy_futures" / "extracted").glob("*.txt"))
    for path in cftc_paths:
        years = [int(value) for value in re.findall(r"(?:19|20)\d{2}", path.name)]
        if years and max(years) > sample_end_year:
            continue
        frame = pd.read_csv(path, usecols=columns, low_memory=False, dtype={"CFTC Contract Market Code": str})
        frames.append(frame)
    raw = pd.concat(frames, ignore_index=True)
    raw["contract_code"] = raw["CFTC Contract Market Code"].str.extract(r"(\d+)", expand=False).str.zfill(6)
    raw["report_date"] = pd.to_datetime(raw["As of Date in Form YYYY-MM-DD"], errors="coerce")
    selected = []
    for row in crosswalk.itertuples(index=False):
        keep = (raw["contract_code"] == row.contract_code) & raw["report_date"].between(row.start, row.end)
        part = raw.loc[keep].copy()
        part["currency"] = row.currency
        part["position_direction"] = row.position_direction
        selected.append(part)
    data = pd.concat(selected, ignore_index=True)
    for col in columns[3:]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    # Transition weeks can contain exchange-name duplicates. The row with the
    # greatest open interest is the economically relevant continuous contract.
    data = data.sort_values("Open Interest (All)").drop_duplicates(["currency", "report_date"], keep="last")
    data["release_date_assumed"] = data["report_date"] + pd.to_timedelta(int(spec["cftc_release_lag_calendar_days"]), unit="D")
    data["month"] = data["release_date_assumed"].dt.to_period("M")
    data["net_noncommercial_share_pct"] = data["position_direction"] * 100.0 * (
        data["Noncommercial Positions-Long (All)"] - data["Noncommercial Positions-Short (All)"]
    ) / data["Open Interest (All)"].replace(0, np.nan)
    monthly = data.sort_values("release_date_assumed").groupby(["month", "currency"], as_index=False).tail(1)
    ranks = currency_panel[["month", "currency", "carry_leg"]].drop_duplicates()
    monthly = monthly.merge(ranks, on=["month", "currency"], how="left")

    def crowding(group: pd.DataFrame) -> pd.Series:
        high = group.loc[group["carry_leg"] == "long_high", "net_noncommercial_share_pct"].dropna()
        low = group.loc[group["carry_leg"] == "short_low", "net_noncommercial_share_pct"].dropna()
        if not len(high) or not len(low):
            return pd.Series({"cftc_carry_crowding_pct_oi": np.nan, "cftc_contracts": len(group), "cftc_high": len(high), "cftc_low": len(low)})
        return pd.Series({
            "cftc_carry_crowding_pct_oi": high.mean() - low.mean(),
            "cftc_contracts": group["net_noncommercial_share_pct"].notna().sum(),
            "cftc_high": len(high),
            "cftc_low": len(low),
        })

    aggregate = monthly.groupby("month").apply(crowding, include_groups=False).reset_index()
    return monthly, aggregate


def load_external_monthly(spec: dict) -> pd.DataFrame:
    start, end = pd.Period(spec["sample_start"], "M"), pd.Period(spec["sample_end"], "M")
    acm = pd.read_csv(PIPELINE_ROOT / "data" / "raw" / "nyfed_acm" / "acmPlot_data.csv")
    acm["month"] = pd.to_datetime(acm["RunDates"], errors="coerce").dt.to_period("M")
    acm["acm_term_premium_10y_pct"] = pd.to_numeric(acm["TERMYld"], errors="coerce")
    acm["acm_expected_path_10y_pct"] = pd.to_numeric(acm["ACMFITYld"], errors="coerce") - acm["acm_term_premium_10y_pct"]
    out = acm[["month", "acm_term_premium_10y_pct", "acm_expected_path_10y_pct", "ACMFITYld", "GSWYld"]].copy()

    cli = pd.read_csv(PIPELINE_ROOT / "data" / "raw" / "oecd_cli" / "oecd_cli_1988_present.csv", low_memory=False)
    cli = cli.loc[(cli["REF_AREA"] == "G7") & (cli["MEASURE"] == "LI") & (cli["METHODOLOGY"] == "H")].copy()
    cli["month"] = _period(cli["TIME_PERIOD"])
    cli["oecd_g7_cli"] = pd.to_numeric(cli["OBS_VALUE"], errors="coerce")
    cli = cli.sort_values("month").drop_duplicates("month", keep="last")[["month", "oecd_g7_cli"]]
    out = out.merge(cli, on="month", how="outer")

    for series in ["NFCI", "VIXCLS"]:
        frame = pd.read_csv(PIPELINE_ROOT / "data" / "raw" / "fred_controls" / f"{series}.csv")
        frame["month"] = pd.to_datetime(frame["observation_date"], errors="coerce").dt.to_period("M")
        frame[series] = pd.to_numeric(frame[series], errors="coerce")
        frame = frame.sort_values("observation_date").groupby("month", as_index=False)[series].last()
        out = out.merge(frame, on="month", how="outer")
    out = out.loc[out["month"].between(start, end)].sort_values("month")
    return out
