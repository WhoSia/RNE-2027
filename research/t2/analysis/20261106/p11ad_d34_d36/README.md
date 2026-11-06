# T2 — 20261106 D34-D36: numerical refinement reference, real sensor data quality and sensor-error policy court

Synthetic code, not a traffic-control system or safety-qualified model.

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python run_study.py
```

D34: *independent* single-car dt reference, NOT existing micro_world convergence.
D35: direct published real winter sensor CSV read; derived summary only and source SHA-1; no SUMO or queue data.
D36: fixed vs actuated, matched synthetic holdout, sensor drop/miss/delay; no real policy efficacy inference.

All experiment outputs use integer-fixed seeds, source files maintained without unnecessary comments, and fail-closed completion report. Shared Drive folder is canonical for bytes. GitHub manual commits only.
