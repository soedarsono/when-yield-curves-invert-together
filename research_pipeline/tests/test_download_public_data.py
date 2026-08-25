from pathlib import Path
import importlib.util
import sys
import tempfile
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "download_public_data.py"
SPEC = importlib.util.spec_from_file_location("download_public_data", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class DownloadPublicDataTests(unittest.TestCase):
    def test_safe_name_from_url(self):
        self.assertEqual(
            MODULE.safe_name_from_url("https://example.org/a/file.csv?x=1", "fallback"),
            "file.csv",
        )
        self.assertEqual(
            MODULE.safe_name_from_url("https://example.org/", "fallback.dat"),
            "fallback.dat",
        )
        self.assertEqual(
            MODULE.safe_name_from_url("https://example.org/.M.LI...", "fallback.csv"),
            "fallback.csv",
        )


    def test_iter_jobs_expands_keys_and_series(self):
        config = {
            "example": {
                "api_template": "https://example.org/{key}",
                "accept": "text/csv",
                "keys": ["M.AU"],
                "series": {"CONTROL": "https://example.org/control.csv"},
            }
        }
        jobs = list(MODULE.iter_jobs(config, {"example"}))
        self.assertEqual(len(jobs), 2)
        self.assertTrue(jobs[0][1].endswith("M.AU"))
        self.assertEqual(jobs[0][2].name, "M_AU.csv")
        self.assertEqual(jobs[1][2].name, "CONTROL.csv")


    def test_sha256_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.bin"
            path.write_bytes(b"abc")
            self.assertEqual(
                MODULE.sha256_file(path),
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            )

    def test_manifest_path_is_platform_independent(self):
        path = MODULE.PROJECT_ROOT / "research_pipeline" / "data" / "raw" / "example.csv"
        self.assertEqual(
            MODULE.manifest_path(path),
            "research_pipeline/data/raw/example.csv",
        )


if __name__ == "__main__":
    unittest.main()
