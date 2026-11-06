# R&E 2027 / T2 — D37–D40: real signal-encounter evidence and independence gate

Research date: 2026-11-06. Canonical location: Shared Drive `20261106 김우준의 사유`.

**Evidence honesty**: we have reviewed real external original CSVs through a linked GitHub app, but only derived episode-level statistics and Git object references are saved here. The full multi-road-user original dataset from a *single* intersection has **not** been acquired. SUMO **has not run**. T2 independent field validation and real policy ranking are **not complete**.

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python run_analysis.py
PYTHONDONTWRITEBYTECODE=1 python visualize.py
```

The tests exercise fabricated *small fixtures*, fail-closed empirical validators, 16 source-derived episode metrics, and experiment parity contracts. No test fakes real road data or an external SUMO result.

- `data/cats_16_derived.json`: 16 directly examined published Waymo-derived sample episode summaries with per-CSV Git blob SHA1 (not raw CSV content).
- `data/source_registry.json`: one-intersection target and source-data availability states. DLR AIM Braunschweig primary; CityArtery backup; SinD map/LFS source; CATS motor-behavior-only.
- `src/trajectory_gate.py`: validate any future downloaded raw sample and compare content to recorded derived metrics.
- `src/queue_observation.py`: explicitly defined stopped-vehicle counts in a measured lane-local observation window.
- `src/parity_contract.py`: independent SUMO/T2 comparison fail-closed contract.
- `results/`: source-derived visualizations and a standalone HTML exploration interface.
- `docs/EXECUTION_GATES.md`, `docs/RESEARCH_DECISION_D37_D40.md`: judgment, missing evidence, and next acceptance gates.

The true target: match a **single observed signalized intersection** across raw data, a pinned SUMO execution, and physically interpretable T2 output. Offline policies should only be compared after this gate. Do not use any code here to actuate street signals.
