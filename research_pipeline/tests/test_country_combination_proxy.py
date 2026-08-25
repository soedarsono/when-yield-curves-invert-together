import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from country_combination_proxy import doubled_tail_rank, joint_cut_onsets, rotation_reference


class CountryCombinationProxyTests(unittest.TestCase):
    def test_joint_cut_onset_respects_quiet_window(self):
        months = pd.period_range("2000-01", periods=7, freq="M")
        cuts = pd.DataFrame(
            {
                "AUD": [True, False, True, False, False, False, True],
                "CAD": [True, False, True, False, False, False, True],
            },
            index=months,
        )
        coverage = pd.DataFrame(True, index=months, columns=cuts.columns)
        result = joint_cut_onsets(cuts, coverage, ("AUD", "CAD"), quiet_months=3)
        self.assertEqual(result.tolist(), [True, False, False, False, False, False, True])

    def test_rotation_reference_enumerates_every_calendar_shift(self):
        outcome = np.array([1.0, 2.0, 3.0, 4.0])
        events = np.array([True, False, True, False])
        reference = rotation_reference(outcome, events)
        np.testing.assert_allclose(reference, [2.0, 3.0, 2.0, 3.0])
        self.assertEqual(doubled_tail_rank(reference, reference[0]), 1.0)

    def test_publication_table_mirror_is_byte_identical(self):
        project = SRC.parents[1]
        source = project / "research_pipeline" / "outputs" / "country_combinations" / "tables" / "public_country_combination_proxy.tex"
        mirror = project / "rewrite" / "generated" / "public_country_combination_proxy.tex"
        self.assertTrue(source.is_file())
        self.assertTrue(mirror.is_file())
        self.assertEqual(source.read_bytes(), mirror.read_bytes())


if __name__ == "__main__":
    unittest.main()
