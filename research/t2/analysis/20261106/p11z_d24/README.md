# R&E 2027 / T2 P11-Z / D24 — 2026-11-06

Research-only finite-slot phase network and a GTFS Schedule **intake gate**. It is not a full transport simulation or an agency feed validation claim. Policy P12 remains frozen.

## Reproduce (Python 3.10+, standard library, matplotlib only for figures)

```bash
python -m unittest discover -s tests -v
python run_experiments.py
python visualize.py
```

From a clean extracted folder: the 18 tests and 100-case X baseline comparison must pass; `results/D24_results.json` can be regenerated. `raw/synthetic_gtfs_fixture.zip` is created by `run_experiments.py`; it is **synthetic**. Prior Y tests separately passed 17/17 and are documented, not bundled as extra test suites.

## Core design

- `src/phase_network.py`: positive integer-tick durations, per-resource finite capacity, atomic handoff and upstream occupancy while blocked, blocked wait graph and detected cycle. Independent synthetic model.
- `src/gtfs_gate.py`: reads an already-downloaded GTFS ZIP and checks active `calendar`/`calendar_dates` dates, timezone, >24h clock, transfer minimum, no silent frequency expansion, and source byte SHA-256. Missing real feed is a documented blocker.
- `baselines`: byte-copied sealed X and Y scripts for compatible-domain reference tests.
- `tests`: 18 tests, including legacy comparisons, malformed GTFS and random occupancy.
- `results`: synthetic outcomes, plots and interactive offline HTML.

The actual US agency GTFS feed could not be downloaded during this execution; use the acquisition ledger under `docs/` rather than claiming agency timetable results. Do not use this code for vehicle safety, signals, policy optimization or navigation advice.
