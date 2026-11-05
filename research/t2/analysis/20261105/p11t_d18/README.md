# T2 P11-T / D18 — Finite-cell backpressure reference and evidence map

Research-only synthetic CTM. P12 policy optimization FROZEN. NOT a field traffic-control model or individual-car microsimulator.

### Reproduce
```bash
python -m unittest discover -s tests -v
python run_experiments.py
```

- `src/cell_link_model.py`: finite storage CTM; CFL and conservation checks.
- `tests/`: 10 tests including 100 deterministic randomized configurations.
- `results/`: scenario snapshots, Δt sensitivity, backlog traces, time series PNG, interactive HTML (offline).
- `docs/RESEARCH_DECISION_T.md`: evaluated claims and precise limitations.
- `docs/EVIDENCE_GATES.md`: achievements vs unresolved bottlenecks.

Data are SYNTHETIC, no original Jinju/NGSIM/inD/SUMO data incorporated. No original legacy P10 engine test or policy optimization performed.

Check official CTM reference https://its.berkeley.edu/node/4777 and SUMO mesoscopic documentation https://sumo.dlr.de/docs/Simulation/Meso.html. SUMO already has lane queues and meso-LTM; neither CTM nor backpressure is newly invented here.
