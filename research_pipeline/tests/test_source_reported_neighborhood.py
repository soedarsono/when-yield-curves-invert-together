import sys
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research_pipeline" / "src"))

from source_reported_neighborhood import summarize, unique_core


class SourceReportedNeighborhoodTests(unittest.TestCase):
    def setUp(self):
        frame = pd.read_csv(ROOT / "research_pipeline" / "config" / "source_reported_rule_neighborhood.csv")
        for column in ("baseline", "include_in_unique_core"):
            frame[column] = frame[column].astype(str).str.lower().eq("true")
        self.core = unique_core(frame)

    def test_core_has_one_baseline_and_nine_rules(self):
        self.assertEqual(len(self.core), 9)
        self.assertEqual(int(self.core["baseline"].sum()), 1)

    def test_reported_sign_counts_are_reproducible(self):
        summary = summarize(self.core).set_index("outcome")
        self.assertEqual(int(summary.loc["carry_spot_pp", "negative_count"]), 8)
        self.assertEqual(int(summary.loc["high_beta_spot_pp", "negative_count"]), 7)

    def test_baseline_is_not_the_most_negative_carry_rule(self):
        summary = summarize(self.core).set_index("outcome")
        self.assertEqual(float(summary.loc["carry_spot_pp", "most_negative_pp"]), -15.72)
        self.assertEqual(float(summary.loc["carry_spot_pp", "baseline_coefficient_pp"]), -12.85)


if __name__ == "__main__":
    unittest.main()
