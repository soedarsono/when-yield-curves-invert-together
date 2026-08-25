"""Synthetic illustration of why a path-dependent latch differs from a static state."""

from __future__ import annotations

import numpy as np
import pandas as pd


def live_state(inverted: np.ndarray, confirmation: int = 2, steepening: np.ndarray | None = None) -> np.ndarray:
    """Apply fresh-entry and confirmed-release rules to country inversions.

    ``steepening`` marks a positive month-to-month change in the underlying
    slope. When omitted, an un-inverted month is used only as a small unit-test
    fixture; the simulation passes the actual slope-change indicator.
    """
    t_count, n_country = inverted.shape
    if steepening is None:
        steepening = ~inverted
    if steepening.shape != inverted.shape:
        raise ValueError("steepening and inverted arrays must have the same shape")
    live = np.zeros_like(inverted, dtype=bool)
    active = np.zeros(n_country, dtype=bool)
    steepening_run = np.zeros(n_country, dtype=int)
    eligible = np.ones(n_country, dtype=bool)
    for t in range(t_count):
        previous_inverted = inverted[t - 1] if t else np.zeros(n_country, dtype=bool)
        fresh = inverted[t] & ~previous_inverted & eligible & ~active
        active[fresh] = True
        eligible[fresh] = False
        if t:
            steepening_run[active] = np.where(steepening[t, active], steepening_run[active] + 1, 0)
            release = active & (steepening_run >= confirmation)
            active[release] = False
            steepening_run[release] = 0
        eligible[~inverted[t] & ~active] = True
        live[t] = active
    return live


def simulate_path(seed: int, months: int = 456, countries: int = 9) -> pd.DataFrame:
    """Generate one illustrative latent-stress path, not a fitted or calibrated model."""
    rng = np.random.default_rng(seed)
    stress = np.zeros(months, dtype=bool)
    age = np.zeros(months, dtype=int)
    for t in range(1, months):
        if stress[t - 1]:
            stress[t] = rng.random() > 0.18
            age[t] = age[t - 1] + 1 if stress[t] else 0
        else:
            stress[t] = rng.random() < 0.025
            age[t] = 1 if stress[t] else 0
    common = np.zeros(months)
    for t in range(1, months):
        common[t] = 0.75 * common[t - 1] + rng.normal(0, 0.12) - 1.80 * (stress[t] and age[t] == 1)
        # Delivered easing re-steepens curves late in stress episodes.
        if stress[t] and age[t] >= 4:
            common[t] += 0.55
    slope = 1.05 + common[:, None] + rng.normal(0, 0.35, size=(months, countries))
    inverted = slope < 0
    steepening = np.vstack([np.zeros((1, countries), dtype=bool), np.diff(slope, axis=0) > 0])
    live = live_state(inverted, steepening=steepening)
    static = inverted.sum(axis=1) >= 2
    latched = live.sum(axis=1) >= 2
    crash = stress & (age >= 4) & (age <= 5) & (rng.random(months) < 0.55)
    carry = 0.35 + rng.normal(0, 1.25, months) - crash * rng.uniform(5.0, 9.0, months)
    return pd.DataFrame(
        {
            "month": np.arange(months), "stress": stress, "stress_age": age,
            "inversion_count": inverted.sum(axis=1), "live_count": live.sum(axis=1),
            "static_state": static, "latched_state": latched, "crash": crash,
            "carry_return_pct": carry,
        }
    )


def simulation_metrics(seed: int, simulations: int = 2000) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    rows = []
    example = simulate_path(int(rng.integers(0, 2**31 - 1)))
    for simulation in range(simulations):
        path = simulate_path(int(rng.integers(0, 2**31 - 1)))
        crash_n = int(path["crash"].sum())
        for state in ["static_state", "latched_state"]:
            on = path[state].to_numpy(bool)
            capture = float(path.loc[path["crash"], state].mean()) if crash_n else np.nan
            false_months = int((on & ~path["crash"].to_numpy(bool)).sum())
            rows.append(
                {
                    "simulation": simulation, "state": state,
                    "crash_capture_rate": capture, "state_month_share": on.mean(),
                    "false_positive_months": false_months,
                    "mean_carry_on_pct": path.loc[on, "carry_return_pct"].mean() if on.any() else np.nan,
                    "crashes": crash_n,
                }
            )
    return example, pd.DataFrame(rows)
