"""Small-sample inference helpers with no statsmodels dependency."""

from __future__ import annotations

import math
from collections.abc import Callable

import numpy as np


def hac_intercept_slope(y: np.ndarray, x: np.ndarray, lags: int = 12) -> dict[str, float]:
    """OLS with Bartlett-kernel Newey-West covariance.

    Returns the slope, its HAC standard error, t statistic, and a normal-reference
    two-sided p-value. The normal reference is disclosed because the effective
    event count can be small; the event tests use randomization inference instead.
    """
    mask = np.isfinite(y) & np.isfinite(x)
    y = np.asarray(y, float)[mask]
    x = np.asarray(x, float)[mask]
    X = np.column_stack([np.ones(len(x)), x])
    if len(y) < 5 or np.linalg.matrix_rank(X) < 2:
        return {"n": float(len(y)), "estimate": np.nan, "se": np.nan, "t": np.nan, "p": np.nan}
    inv_xx = np.linalg.inv(X.T @ X)
    beta = inv_xx @ X.T @ y
    resid = y - X @ beta
    xu = X * resid[:, None]
    meat = xu.T @ xu
    max_lag = min(int(lags), len(y) - 1)
    for lag in range(1, max_lag + 1):
        weight = 1.0 - lag / (max_lag + 1.0)
        gamma = xu[lag:].T @ xu[:-lag]
        meat += weight * (gamma + gamma.T)
    cov = inv_xx @ meat @ inv_xx
    se = math.sqrt(max(float(cov[1, 1]), 0.0))
    t_stat = float(beta[1] / se) if se > 0 else np.nan
    p = math.erfc(abs(t_stat) / math.sqrt(2.0)) if np.isfinite(t_stat) else np.nan
    return {"n": float(len(y)), "estimate": float(beta[1]), "se": se, "t": t_stat, "p": p}


def event_values(
    values: np.ndarray,
    event_indicator: np.ndarray,
    horizon: int,
    mode: str,
) -> np.ndarray:
    """Return event-level outcomes using t-1 as the level baseline.

    ``mode='change'`` computes y[t+h]-y[t-1]. ``mode='sum'`` computes the
    sum from t through t+h, suitable for monthly returns.
    """
    values = np.asarray(values, float)
    events = np.flatnonzero(np.asarray(event_indicator, bool))
    out: list[float] = []
    for t in events:
        if mode == "change":
            if t < 1 or t + horizon >= len(values):
                continue
            pair = values[[t - 1, t + horizon]]
            if np.isfinite(pair).all():
                out.append(float(pair[1] - pair[0]))
        elif mode == "sum":
            if t + horizon >= len(values):
                continue
            window = values[t : t + horizon + 1]
            if np.isfinite(window).all():
                out.append(float(window.sum()))
        else:
            raise ValueError(f"Unknown event mode: {mode}")
    return np.asarray(out, float)


def circular_shift_pvalue(
    values: np.ndarray,
    event_indicator: np.ndarray,
    horizon: int,
    mode: str,
    draws: int | None = None,
    seed: int | None = None,
) -> tuple[float, float, int, int]:
    """Exact, same-N circular-rotation reference with a doubled-tail p-value.

    Every nonzero rotation is enumerated; ``draws`` and ``seed`` remain optional
    compatibility arguments and are ignored. Rotations are retained only when
    they produce the same number of valid event-level outcomes as the observed
    assignment. This matters when an outcome has missing history (especially
    CFTC) or a horizon removes edge events. The observed assignment is included
    in the finite reference distribution. The two-sided p-value is twice the
    smaller inclusive tail rank, capped at one. It therefore does not assume that
    zero, the placebo mean, or the placebo median is the null center.

    The conditional same-N set need not itself form a transformation group when
    missingness is irregular. We therefore describe the output as a conditional
    finite-rotation reference p-value, not a finite-sample exact causal test.
    """
    audit = circular_shift_reference(values, event_indicator, horizon, mode)
    observed_rows = audit.loc[audit["shift"] == 0]
    if observed_rows.empty or not bool(observed_rows.iloc[0]["retained_same_event_count"]):
        return np.nan, np.nan, 0, 0
    observed = float(observed_rows.iloc[0]["estimate"])
    observed_n = int(observed_rows.iloc[0]["event_count"])
    reference_array = audit.loc[audit["retained_same_event_count"], "estimate"].to_numpy(float)
    lower = float(np.mean(reference_array <= observed))
    upper = float(np.mean(reference_array >= observed))
    p = min(1.0, 2.0 * min(lower, upper))
    return observed, p, observed_n, len(reference_array)


def circular_shift_reference(
    values: np.ndarray,
    event_indicator: np.ndarray,
    horizon: int,
    mode: str,
):
    """Return all finite-rotation estimates and the same-N retention decision."""
    import pandas as pd

    observed_values = event_values(values, event_indicator, horizon, mode)
    if not len(observed_values):
        return pd.DataFrame(columns=["shift", "estimate", "event_count", "retained_same_event_count", "is_observed"])
    target_n = len(observed_values)
    n = len(event_indicator)
    rows = []
    for shift in range(n):
        shifted = np.roll(event_indicator, shift)
        draw_values = event_values(values, shifted, horizon, mode)
        rows.append(
            {
                "shift": shift,
                "estimate": float(draw_values.mean()) if len(draw_values) else np.nan,
                "event_count": len(draw_values),
                "retained_same_event_count": len(draw_values) == target_n,
                "is_observed": shift == 0,
            }
        )
    return pd.DataFrame(rows)


def episode_bootstrap_ci(values: np.ndarray, draws: int, seed: int) -> tuple[float, float]:
    values = np.asarray(values, float)
    values = values[np.isfinite(values)]
    if len(values) < 2:
        return np.nan, np.nan
    rng = np.random.default_rng(seed)
    means = np.empty(draws)
    for b in range(draws):
        means[b] = rng.choice(values, size=len(values), replace=True).mean()
    return tuple(map(float, np.quantile(means, [0.05, 0.95])))


def leave_one_range(values: np.ndarray) -> tuple[float, float]:
    values = np.asarray(values, float)
    values = values[np.isfinite(values)]
    if len(values) < 3:
        return np.nan, np.nan
    means = np.array([np.delete(values, i).mean() for i in range(len(values))])
    return float(means.min()), float(means.max())


def holm_adjust(pvalues: dict[str, float]) -> dict[str, float]:
    valid = sorted((p, key) for key, p in pvalues.items() if np.isfinite(p))
    adjusted: dict[str, float] = {key: np.nan for key in pvalues}
    running = 0.0
    m = len(valid)
    for rank, (p, key) in enumerate(valid):
        running = max(running, (m - rank) * p)
        adjusted[key] = min(1.0, running)
    return adjusted
