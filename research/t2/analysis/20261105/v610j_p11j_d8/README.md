# T2 v6.10-J / P11-J / D8 — Lane Boundary & 3D Geometric Seam Audit

This independent continuation develops conditional 3D lane boundary sampling and explicit junction seam counterexamples. Policy code is retained as reference only.

## Reproduce

From this directory:

```bash
python -m unittest discover -s tests -p 'test_*.py' -q
python src/run_boundary_audit.py
```

SciPy needed only for inherited independent 2D spiral test comparisons. 113 tests pass in the sealed local environment. Original P2 regression executed separately from original ZIP: 28 passed.

## Interpretation

- The 5-case experiment is entirely synthetic. `UNKNOWN` is intended even when source-declared boundaries agree.
- `SAMPLED_STRIP_NOT_EXACT_SURFACE` is **not** a source-authorized intersection, an exact polygon, or an engineering road clearance certificate.
- Reference road point proximity and laneLink element presence **do not** prove permitted drivable lane-to-lane movement; direction and legal data are unverified.
- Original J parent: v6.10-I derived snapshot (do not overwrite).
- Original papers are in Research OS 10_PAPERS only; no duplicate source PDFs in ZIP.

## Matched diagnostic

The runner records prior I and new J outcomes for five identical synthetic fixtures. Prior I flags 1/5; J flags 4/5 as geometry failures, deliberately leaving the continuous reference as UNKNOWN. **This is not a source dataset benchmark or a general detector performance claim.**
