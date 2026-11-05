# T2 20261106 — D26..D30 five-unit integrated reference

**Research prototype; not a real-road control system.**

## Unit inventory
- D26 `d26_p10/`: unchanged historical P10 source, original vehicle 1/8 replay and ablation. P9/P2 original dependency in `d26_p9/`; ZIP receipts in `sources/`.
- D27 `src/micro_world.py`: 1-s discrete time microscopic longitudinal reference with car positions and finite road length, signal, crosswalk and transfer.
- D28 same engine + `src/od_and_policy.py`: gap-constrained instantaneous lane changes, multi-road demand, bus dwell, simplified curve/grade.
- D29 `src/validation.py`: independent SUMO output and field observation fail-closed parser. **No SUMO executable or field data actually used.**
- D30 `src/od_and_policy.py` `court`: offline candidate signal comparison on synthetic demand, 4 train + 2 holdout seeds, not traffic-control advice.

## Test independently
```
python -m unittest discover -s tests -v
python -m unittest discover -s baseline_d25/tests -v
PYTHONPATH="$PWD/d26_p9/code:$PWD/d26_p9/reference/T2_v69_P2:$PWD/d26_p10" python -m unittest discover -s d26_p10 -p test_p10_mechanism.py -v
python produce_results.py
```

`produce_results.py` regenerates CSV/JSON/PNG/standalone HTML. For exact P10 origin, first execute the unchanged archived P10 programs with PYTHONPATH as above and verify output against ZIP, then run script.

IMPORTANT: The micro reference is a standalone comparison artifact, **not** a replacement for all existing T2 `research/t2` code. Implementation scope, empirical missing-data blockers, and policy validity caveats are in five documents under `research/`.
