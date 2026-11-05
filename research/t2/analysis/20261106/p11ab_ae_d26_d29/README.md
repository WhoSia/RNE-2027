# T2 2026-11-06 D26–D29: Experimental integrated road network + P10 original replay

Research only. No calibrated traffic safety, deployment, or signal optimization claims.

## Standalone reproduction
```bash
python -m unittest discover -s tests -v
python replay_provenance.py
python run_study.py
```

`replay_provenance.py` verifies original raw ZIP SHA-256 and original P2 `corridor.py` hash before executing the unchanged P10 test and 8-grid trace. It compares the outputs to its archived `boundary_mechanism.json`.

`run_study.py` uses a **synthetic** 22-vehicle demand in a fixed 2-link road; generates CSV/PNG/HTML, timestep sensitivity and SUMO XML inputs. `sumo` and `netconvert` are not installed in the current environment. Files in `independent_sumo_input/` are inputs, not execution proof. No actual GTFS or road trajectory files were used here.

`src/micro_network.py` is a simplified per-vehicle, longitudinal-lane reference with finite space, fixed-time signals, pedestrian occupancy and bus dwell. Lane-change choices and grade/curvature ceilings are experimental kinematic approximations and have no real-world safety standing.

## Evidence sources
- D25 unchanged source ZIP: `baselines/D25_sealed.zip`.
- P9/P10 raw preserved ZIPs: `baselines/P9_v69_original.zip`, `baselines/P10_v69_original.zip`.
- Real-world validation still open; see `docs/03_D28_DATA_REPRODUCTION.md`.
- Original P10 code remains unmodified. Historical policy P12 remains sealed; policy research restart is **NEXT** stage only, in a separate sandbox after explicit gate review.
