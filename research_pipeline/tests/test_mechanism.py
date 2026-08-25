from pathlib import Path
import importlib.util
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mechanism.inference import circular_shift_reference_value, event_values, hac_intercept_slope, holm_adjust
from mechanism.panel import aggregate_shadow_spot, assign_carry_weights, at_least_rate_cut
from mechanism.simulation import live_state
import run_mechanism_checks


class MechanismInferenceTests(unittest.TestCase):
    def test_rate_cut_threshold_is_stable_at_exact_ten_basis_points(self):
        changes = pd.Series([-0.10, -0.09999999999999964, -0.0999999, -0.1000001, np.nan])
        classified = at_least_rate_cut(changes, 0.10).tolist()
        self.assertEqual(classified, [True, True, False, True, False])

    def test_policy_rate_cutoff_ties_expand_and_are_equally_weighted(self):
        panel = pd.DataFrame(
            {
                "month": [pd.Period("2000-01", "M")] * 9,
                "formation_policy_diff": [-2.0, -1.0, -1.0, -1.0, 0.0, 1.0, 1.0, 1.0, 2.0],
            }
        )
        spec = {"carry_sort": {"long_count": 3, "short_count": 3}}
        weighted = assign_carry_weights(panel, spec)
        self.assertEqual(int(weighted["carry_weight"].ne(0).sum()), 8)
        self.assertAlmostEqual(weighted["carry_weight"].clip(lower=0).sum(), 1.0)
        self.assertAlmostEqual(weighted["carry_weight"].clip(upper=0).sum(), -1.0)

    def test_shadow_spot_requires_every_selected_return(self):
        group = pd.DataFrame(
            {
                "carry_weight": [-0.5, -0.5, 0.0, 0.5, 0.5],
                "fx_usd_return_pct": [1.0, np.nan, np.nan, 2.0, 2.0],
            }
        )
        self.assertTrue(np.isnan(aggregate_shadow_spot(group, minimum_target_count=4)))
        group.loc[1, "fx_usd_return_pct"] = 1.0
        self.assertAlmostEqual(aggregate_shadow_spot(group, minimum_target_count=4), 1.0)

    def test_event_change_uses_pre_event_baseline(self):
        values = np.array([1.0, 2.0, 5.0, 8.0, 13.0])
        events = np.array([False, False, True, False, False])
        self.assertEqual(event_values(values, events, 1, "change").tolist(), [6.0])

    def test_event_sum_includes_onset_month(self):
        values = np.array([1.0, 2.0, 5.0, 8.0])
        events = np.array([False, True, False, False])
        self.assertEqual(event_values(values, events, 1, "sum").tolist(), [7.0])

    def test_holm_is_monotone_in_sorted_pvalues(self):
        adjusted = holm_adjust({"a": 0.01, "b": 0.04, "c": 0.20})
        self.assertAlmostEqual(adjusted["a"], 0.03)
        self.assertAlmostEqual(adjusted["b"], 0.08)
        self.assertAlmostEqual(adjusted["c"], 0.20)

    def test_hac_recovers_exact_slope(self):
        x = np.arange(20, dtype=float)
        y = 2.0 + 3.0 * x
        result = hac_intercept_slope(y, x, lags=3)
        self.assertAlmostEqual(result["estimate"], 3.0, places=10)

    def test_circular_reference_enumerates_all_rotations_when_complete(self):
        values = np.arange(12, dtype=float)
        events = np.zeros(12, dtype=bool)
        events[[2, 7]] = True
        estimate, p, event_count, reference_count = circular_shift_reference_value(values, events, 0, "sum")
        self.assertEqual(event_count, 2)
        self.assertEqual(reference_count, 12)
        self.assertTrue(0.0 <= p <= 1.0)
        self.assertAlmostEqual(estimate, 4.5)

    def test_circular_reference_conditions_on_observed_valid_event_count(self):
        values = np.arange(10, dtype=float)
        values[5] = np.nan
        events = np.zeros(10, dtype=bool)
        events[[1, 4]] = True
        _, _, event_count, reference_count = circular_shift_reference_value(values, events, 0, "sum")
        self.assertEqual(event_count, 2)
        self.assertLess(reference_count, 10)
        self.assertGreaterEqual(reference_count, 1)

    def test_doubled_tail_rank_is_not_abs_zero_statistic(self):
        values = np.array([10.0, 11.0, 12.0, 13.0, 14.0, 40.0])
        events = np.array([True, False, False, False, False, False])
        _, p, _, reference_count = circular_shift_reference_value(values, events, 0, "sum")
        self.assertEqual(reference_count, 6)
        # The observed value is the minimum: doubled inclusive lower-tail rank.
        self.assertAlmostEqual(p, 2.0 / 6.0)


class StateMachineTests(unittest.TestCase):
    def test_latch_survives_one_month_uninversion_and_releases_after_two(self):
        inverted = np.array([[False], [True], [True], [False], [False], [False]])
        live = live_state(inverted, confirmation=2).ravel().tolist()
        self.assertEqual(live, [False, True, True, True, False, False])

    def test_reentry_requires_fresh_inversion(self):
        inverted = np.array([[False], [True], [False], [False], [True]])
        live = live_state(inverted, confirmation=2).ravel().tolist()
        self.assertEqual(live, [False, True, True, False, True])


class RunManifestTests(unittest.TestCase):
    def test_artifact_record_includes_size_and_hash(self):
        with tempfile.TemporaryDirectory(dir=run_mechanism_checks.PROJECT_ROOT) as directory:
            path = Path(directory) / "sample.bin"
            path.write_bytes(b"abc")
            record = run_mechanism_checks.artifact_record(path)
            self.assertEqual(record["bytes"], 3)
            self.assertEqual(record["sha256"], "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
            self.assertNotIn("\\", record["path"])

    def test_dependency_versions_are_explicit(self):
        self.assertEqual(set(run_mechanism_checks.dependency_versions()), {"matplotlib", "numpy", "pandas"})


if __name__ == "__main__":
    unittest.main()
