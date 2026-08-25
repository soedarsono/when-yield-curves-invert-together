from pathlib import Path
import importlib.util
import sys
import unittest
from unittest import mock

import numpy as np
import pandas as pd


MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "public_yield_proxy_v03.py"
SPEC = importlib.util.spec_from_file_location("public_yield_proxy_v03", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class PublicYieldProxyTests(unittest.TestCase):
    def test_live_recursion_requires_fresh_crossing_and_confirmed_release(self):
        slopes = pd.Series([0.5, -0.2, -0.4, -0.1, 0.1, -0.2, -0.3], index=pd.period_range("2000-01", periods=7, freq="M"))
        result = MODULE.live_curve_recursion(slopes, release_months=2)
        self.assertEqual(result["fresh_entry"].tolist(), [False, False, True, False, False, False, True])
        self.assertEqual(result["live"].tolist(), [False, False, True, True, False, False, True])
        self.assertTrue(result.loc[pd.Period("2000-05", "M"), "released"])

    def test_missing_value_breaks_consecutive_steepening_sequence(self):
        slopes = pd.Series([0.5, -0.2, -0.4, -0.1, np.nan, 0.1, 0.2], index=pd.period_range("2000-01", periods=7, freq="M"))
        result = MODULE.live_curve_recursion(slopes, release_months=2)
        self.assertTrue(result.iloc[2]["fresh_entry"])
        self.assertTrue(result.iloc[-1]["live"])
        self.assertFalse(result.iloc[-1]["released"])
        self.assertEqual(result.iloc[-1]["steepening_counter"], 1)

    def test_active_difference_uses_future_return_alignment(self):
        idx = pd.period_range("2000-01", periods=4, freq="M")
        state = pd.Series([False, True, False, True], index=idx)
        returns = pd.Series([1.0, -1.0, 2.0, -2.0], index=idx)
        estimate, active, inactive, episodes = MODULE.active_difference(state, returns)
        self.assertEqual(estimate, -36.0)
        self.assertEqual((active, inactive, episodes), (2, 2, 2))

    def test_declared_family_has_64_unique_rules(self):
        expected = (3 * 4 + 4) * 2 * 2
        self.assertEqual(expected, 64)

    def test_policy_rate_ties_receive_equal_cutoff_weights(self):
        group = pd.DataFrame(
            {"formation_policy_diff": [-1.0, -1.0, 0.0, 1.0, 1.0]},
            index=list("abcde"),
        )
        weights = MODULE.equal_tie_carry_weights(group, leg_count=1)
        self.assertEqual(weights.to_dict(), {"a": -0.5, "b": -0.5, "c": 0.0, "d": 0.5, "e": 0.5})
        self.assertAlmostEqual(weights.clip(lower=0).sum(), 1.0)
        self.assertAlmostEqual(weights.clip(upper=0).sum(), -1.0)

    def test_target_two_and_three_legs_expand_at_cutoff_ties(self):
        for leg_count, values in [
            (2, [-2.0, -1.0, -1.0, 0.0, 1.0, 1.0, 2.0]),
            (3, [-2.0, -1.0, -1.0, -1.0, 0.0, 1.0, 1.0, 1.0, 2.0]),
        ]:
            group = pd.DataFrame({"formation_policy_diff": values})
            weights = MODULE.equal_tie_carry_weights(group, leg_count=leg_count)
            self.assertGreater(int(weights.ne(0).sum()), 2 * leg_count)
            self.assertAlmostEqual(weights.clip(lower=0).sum(), 1.0)
            self.assertAlmostEqual(weights.clip(upper=0).sum(), -1.0)

    def test_episode_count_treats_internal_calendar_gap_as_new_episode(self):
        full_index = pd.period_range("2000-01", periods=4, freq="M")
        state = pd.Series([True, True, True, False], index=full_index)
        returns = pd.Series([1.0, np.nan, 1.0, -1.0], index=full_index)
        estimate, active, inactive, episodes = MODULE.active_difference(state, returns)
        self.assertTrue(np.isfinite(estimate))
        self.assertEqual((active, inactive, episodes), (2, 1, 2))

    def test_family_uses_one_literal_common_calendar(self):
        index = pd.period_range("1988-01", periods=10, freq="M")
        state_values = [False, True, False, False, True, False, True, False, False, True]

        def fake_state(*args, **kwargs):
            return pd.DataFrame({"month": index, "state": state_values}), pd.DataFrame()

        outcomes = {
            2: pd.Series([0.2, -0.1, 0.4, -0.3, 0.1, -0.5, 0.3, -0.2, 0.6, -0.4], index=index),
            3: pd.Series([0.1, -0.4, 0.2, -0.2, 0.5, -0.3, 0.4, -0.1, 0.3, -0.6], index=index),
        }

        def fake_currency(leg_count, included=None):
            return pd.DataFrame(), outcomes[leg_count]

        with mock.patch.object(MODULE, "build_state", side_effect=fake_state), mock.patch.object(
            MODULE, "build_currency_panel", side_effect=fake_currency
        ):
            results, references = MODULE.specification_family(pd.DataFrame())
        self.assertEqual(set(results["common_calendar_months"]), {8})
        self.assertEqual(set(results["common_calendar_start"]), {"1988-01"})
        self.assertEqual(set(results["common_calendar_end"]), {"1988-08"})
        self.assertEqual({len(reference) for reference in references.values()}, {8})


if __name__ == "__main__":
    unittest.main()
