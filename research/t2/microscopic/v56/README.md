# T2 v5.6 (20261103) — Geometry-gated concurrent microscopic crossing

Reproduce using Python 3.10+ with no third-party packages:

```bash
python -m unittest -v test_v56
python experiment_v56.py
```

- `geometry.py` original v5.5 synthetic 12-movement 4-way graph, unchanged.
- `network_v56.py` derived from v5.3 microscopic engine, with `ParallelSignalPlan`, geometry-matched movements, two-vehicle same tick crossing gating and independent graph audit.
- `test_v56.py` 7 integration tests.
- `experiment_v56.py` matched OD synthetic 3 demand scenarios ×24 seeds ×2 signal dispatch modes (144 runs).
- `holdout_paired.csv` reserved 12 different seeds per demand, 72 additional runs.
- `runs.csv`, `paired.csv`, `summary.csv` and `summary.json` are raw/summary experiments.

Crucial limitations: synthetic four-way `W>E/W>S/N>E/N>W` movements mapped to the corridor's main and side movements. A main green may also release conflict-free side-exit vehicles during a 12-second window; it adds service opportunity and thus is not an equal-time phase reallocation experiment. Geometric centerline separation is 2.5 m but true vehicle swept area, occupation intervals, lane geometry, signal intergreens, pedestrians, regulations and empirical calibration are absent. `next_junction_release` is bypassed only during the parallel window: same-lane minimum service headways still enforced. This is a mechanism proof-of-concept, not a field-safe controller.

Original v5.3 default-mode exact numeric regression: 48 combinations crosschecked by a separate script with source engine (3 demands ×4 seeds ×2 signal settings ×2 pocket lengths): all five output metrics matched.

The original v5.3 full test suite and v5.5 geometry tests are supplied in the historical artifacts. This version's seven tests are not a claim that all earlier 52/26 tests were rerun against the modified implementation.
