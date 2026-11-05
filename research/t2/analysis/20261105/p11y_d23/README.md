# T2 P11-Y / D23 — timetable and phased occupancy prototypes

Python 3.10+; no dependencies for computational core or tests; optional `matplotlib` for PNG rendering.

```
python -m unittest discover -s tests -v
python run_experiments.py
python visualize.py
```

- `src/transit_schedule.py` — immutable synthetic connection table and earliest-arrival query with trip-change transfer buffer; static shortest geometric distance only as comparator.
- `src/zone_phases.py` — integer-tick, zone-by-zone occupancy with blocking and explicit deadlock detection. NOT microscopic motion.
- `tests/test_models.py` — 17 tests, including comparison with independent brute enumeration across 150 randomized DAG schedules.
- `results/departure_sweep.csv` — 183 synthetic itinerary queries; `results/analysis.json` captures case evidence.
- `results/timetable_and_phases.html` — standalone offline adjustable schedule visualization. No live data requests or external JS dependencies.
- `results/*.png` — static graphics.

**P12 SIGNAL POLICY OPTIMIZATION FROZEN**. This is a modeling and representation experiment, not new transit optimization, road operations or field evidence. Do not confuse a timetable query with the scheduling of bus frequency or signal phase.
