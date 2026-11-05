# R&E 2027 — T2 v6.10-D / P11-D / D2 / P12-B

**Four-track, independent additive research prototype** dated 2026-11-05.

## Reproduce

Python 3.11+, optionally `networkx` for the OSMnx adapter test.

```bash
PYTHONPATH=src python -m unittest discover -s tests -q
PYTHONPATH=src python src/run_prototype.py
```

The code fixtures do not require internet or SUMO. Tests of prior immutable P2 require the original ZIP outside this package; it is **not modified**. No claim of running SUMO or external vehicle trajectories.

## Files

- `src/road_ir.py`: loss-aware CityFlow/SUMO/OSMnx adapters. Output is structural, not a calibrated simulation-ready road model.
- `src/controllers.py`: guarded fixed, actuator proxy and simple queue-pressure signal control on **synthetic** observations.
- `src/spat_intervals.py`: uncertainty-preserving interval bracketing of actual public time-stamped SPaT data.
- `src/run_prototype.py`: same synthetic 121-observation stream, three policy state traces, two road format synthetic fixtures.
- `tests/test_road_ir.py`, `tests/test_controllers.py`, `tests/test_spat_intervals.py` plus previous independent v6.10-C tests.
- `results/summary.json`, `results/controller_traces.csv`: outputs from new synthetic fixtures only.
- `docs/RESEARCH_REVIEW.md`: evidence, source reference and no-go criteria.
- `provenance/references.json`: official links, exact external evidence level and immutable prior source SHA-256.

## What has NOT been implemented

Not a worldwide import service; no full native OSM/OSMnx downloads, OpenDRIVE parser, actual signal link-state loader, automatic geometry conflict inference, lane-changing dynamics, complete yellow/all-red application in the vehicle RouteEngine, closed-loop controller-to-vehicle coupling, independent SUMO run, or field prediction benchmark. All policies are simulation-only. Real-world improvement is not claimed.
