# T2 P11-AA / D25 — 2026-11-06

Synthetic physical-storage and GTFS provenance integrity audit; **P12 policy FROZEN**.

## Reproduction (Python 3.10+)

From this directory:

```bash
python -m unittest discover -s tests -v
python run_experiments.py
python visualize.py   # matplotlib for PNG only
```

Default `simulate(movements, capacity)` remains the exact D24 behavior. `StorageGeometry` adds an optional aggregate packing bound using **integer millimetres**, not a calibrated microscopic traffic physics model. Files in `baselines/` preserve the D24 sources verbatim. The archived D24 GTFS fixture in `results/` is **synthetic**, not an official transit feed.

Check `docs/RESEARCH_DECISION.md` for evidence boundaries; `docs/P10_SOURCE_TRACE.md` for P10 original archive discovery and missing replay dependency.
