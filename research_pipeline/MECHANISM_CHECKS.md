# Public mechanism-check pipeline

Run from the repository root:

```powershell
python research_pipeline/src/run_mechanism_checks.py
```

The command reads only the already downloaded official public files listed in the data-purpose ledger. It writes derived panels, results, LaTeX fragments, figures, and ledgers under `research_pipeline/outputs/mechanism/`, then mirrors publication-ready tables and figures to `rewrite/generated/`.

## What the run establishes

The empirical exercise measures associations around a public synchronized-policy-easing proxy. It does not reproduce the paper's IYC signal, licensed carry returns, episodes, or headline estimates. The synthetic exercise illustrates why a path-dependent latch can remain active after contemporaneous curves re-steepen; its parameters are not fitted or calibrated to the paper.

## Failure behavior

Missing raw files, absent required columns, too little cross-sectional coverage, or a broken CFTC mapping stops the command with an exception. Outputs are never silently relabeled as a replication. Empty event samples remain missing in machine-readable results instead of being replaced with zeros.

## Verification

```powershell
python -m unittest discover -s research_pipeline/tests -v
```

The tests cover event-window timing, exact enumeration and same-valid-count conditioning of circular rotations, the doubled-tail rank p-value, multiplicity adjustment, HAC slope calculation, and the live-state entry/release rules. The full run also records its design boundary and output inventory in `research_pipeline/outputs/mechanism/run_manifest.json`.
