from pathlib import Path
import importlib.util
import json
import sys
import tempfile
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "audit_public_data.py"
SPEC = importlib.util.spec_from_file_location("audit_public_data", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class AuditPublicDataTests(unittest.TestCase):
    def test_normalizes_windows_manifest_key(self):
        self.assertEqual(
            MODULE.normalize_manifest_key(r"research_pipeline\data\raw\sample.csv"),
            "research_pipeline/data/raw/sample.csv",
        )

    def test_latest_manifest_rows_reports_only_latest_failures(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "manifest.jsonl"
            rows = [
                {"output_path": r"research_pipeline\data\raw\a.csv", "status": "failed"},
                {"output_path": "research_pipeline/data/raw/a.csv", "status": "cached", "sha256": "abc"},
                {"output_path": "research_pipeline/data/raw/obsolete.csv", "status": "failed"},
                {"output_path": "research_pipeline/data/raw/current.csv", "status": "failed"},
            ]
            manifest.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
            latest, failures = MODULE.latest_manifest_rows(
                manifest,
                active_keys={"research_pipeline/data/raw/a.csv", "research_pipeline/data/raw/current.csv"},
            )
            self.assertEqual(latest["research_pipeline/data/raw/a.csv"]["status"], "cached")
            self.assertEqual([row["output_path"] for row in failures], ["research_pipeline/data/raw/current.csv"])

    def test_sha256_file_hashes_local_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.bin"
            path.write_bytes(b"abc")
            self.assertEqual(
                MODULE.sha256_file(path),
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            )


if __name__ == "__main__":
    unittest.main()
