# P11-V / D20 · Research-only lane FIFO audit

Python 3.10+; standard library for model/tests; matplotlib only to regenerate the optional figure.

From this directory:

```bash
python -m unittest discover -s tests -v
python run_audit.py
```

The original S-stage source is sealed in `baseline/`. The modified version is in `src/`. The archived S source's SHA-256 is recorded in `docs/AUDIT_DECISION_V.md`; its original ZIP was independently checked during this D20 audit. `run_audit.py` makes the comparison and writes `results/audit_results.json`.

Important: simulated requests are abstract synthetic resources, not field traffic, actual safety recommendations, or signal control. P12 remains frozen.
