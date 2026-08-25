from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT = PROJECT_ROOT / "research_pipeline" / "outputs" / "v03" / "yield_proxy"
TABLES = PROJECT_ROOT / "rewrite" / "generated" / "tables"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class V03PaperLinkageTests(unittest.TestCase):
    def test_summary_table_matches_common_calendar_family_and_sensitivities(self):
        specs = pd.read_csv(OUTPUT / "data" / "specification_family.csv")
        baseline = specs.loc[specs["baseline_like"].astype(str).str.lower().eq("true")].iloc[0]
        sensitivities = pd.read_csv(OUTPUT / "data" / "baseline_sensitivities.csv")
        tex = (TABLES / "v03_public_proxy_summary.tex").read_text(encoding="utf-8")
        self.assertIn(
            f"Baseline-like rule & ${baseline['annualized_active_minus_inactive_pp']:+.2f}$ & "
            f"{baseline['p_circular_raw']:.3f} & {int(baseline['active_months'])} & {int(baseline['episodes'])}",
            tex,
        )
        self.assertIn(f"{int((specs['annualized_active_minus_inactive_pp'] < 0).sum())} of {len(specs)}", tex)
        self.assertIn(
            f"common-calendar max-$|z|$ rotation-reference value is {baseline['p_maxT_family']:.3f}",
            tex,
        )
        crisis = sensitivities.loc[
            sensitivities["sensitivity"].eq("exclude_episodes_containing_1998_09_2008_10_2020_03")
        ].iloc[0]
        self.assertIn(f"${crisis['annualized_active_minus_inactive_pp']:+.2f}$ & {crisis['p_circular_raw']:.3f}", tex)

    def test_exclusion_and_episode_tables_match_machine_ledgers(self):
        loo = pd.read_csv(OUTPUT / "data" / "leave_one_country_out.csv")
        disjoint = pd.read_csv(OUTPUT / "data" / "geographically_disjoint.csv")
        episodes = pd.read_csv(OUTPUT / "data" / "baseline_episode_ledger.csv")
        exclusion_tex = (TABLES / "v03_public_loo_disjoint.tex").read_text(encoding="utf-8")
        episode_tex = (TABLES / "v03_public_episode_ledger.tex").read_text(encoding="utf-8")
        self.assertEqual(set(loo["sensor_currency_count"]), {8})
        self.assertEqual(set(loo["minimum_curve_coverage"]), {5})
        self.assertEqual(
            set(zip(disjoint["sensor_currency_count"], disjoint["minimum_curve_coverage"])),
            {(5, 4), (4, 3)},
        )
        for row in loo.itertuples(index=False):
            self.assertIn(f"{row.excluded_from_signal_and_outcome} & ${row.annualized_active_minus_inactive_pp:+.2f}$", exclusion_tex)
        for row in disjoint.itertuples(index=False):
            self.assertIn(f"${row.annualized_active_minus_inactive_pp:+.2f}$ & {row.p_circular_raw:.3f}", exclusion_tex)
        self.assertIn(f"The public {len(episodes)}-episode ledger", episode_tex)
        last = episodes.iloc[-1]
        self.assertIn(str(last["onset_month"]).replace("-", ":"), episode_tex)

    def test_manifest_covers_raw_code_config_and_paper_outputs(self):
        manifest = json.loads((OUTPUT / "run_manifest.json").read_text(encoding="utf-8"))
        raw_paths = {item["path"] for item in manifest["raw_inputs"]}
        self.assertTrue(any("oecd_yield_curve_proxy" in path for path in raw_paths))
        self.assertTrue(any("bis_policy_rates" in path for path in raw_paths))
        self.assertTrue(any("bis_exchange_rates" in path for path in raw_paths))
        code_paths = {item["path"] for item in manifest["code_and_config_inputs"]}
        self.assertIn("research_pipeline/src/public_yield_proxy_v03.py", code_paths)
        self.assertIn("research_pipeline/src/render_v03_public_tables.py", code_paths)
        self.assertIn("research_pipeline/config/mechanism_spec.json", code_paths)
        for section in ("raw_inputs", "code_and_config_inputs", "outputs", "paper_outputs"):
            self.assertTrue(manifest.get(section), f"Manifest section {section} is missing or empty")
            for record in manifest[section]:
                path = PROJECT_ROOT / record["path"]
                self.assertRegex(record["sha256"], r"^[0-9a-f]{64}$")
                self.assertGreater(record["bytes"], 0)
                if section == "raw_inputs" and not path.is_file():
                    # Raw provider files are intentionally untracked. A clean-clone CI
                    # run verifies the immutable manifest records; a saved-snapshot or
                    # release run additionally verifies the local bytes below.
                    continue
                self.assertTrue(path.is_file(), f"Missing manifest path: {record['path']}")
                self.assertEqual(record["sha256"], sha256(path), f"Stale hash: {record['path']}")
                self.assertEqual(record["bytes"], path.stat().st_size, f"Stale size: {record['path']}")

    def test_public_figure_mirror_is_byte_identical(self):
        source = OUTPUT / "figures" / "specification_curve.png"
        mirror = PROJECT_ROOT / "rewrite" / "generated" / "v03_public_specification_curve.png"
        self.assertEqual(sha256(source), sha256(mirror))


if __name__ == "__main__":
    unittest.main()
