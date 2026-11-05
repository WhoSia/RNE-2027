# T2 v6.10-E / P11-E / D3 — Road legality and descriptive completeness

Dated 2026-11-05, R&E 2027.

**Policy work is deliberately frozen.** This is an independent research-only source branch; no real traffic signal connection, policy deployment, or blanket legal-road compliance inference.

From this folder:

```bash
PYTHONPATH=src python -m unittest discover -s tests -q
PYTHONPATH=src python src/run_feature_audit.py
```

`road_ir.py` is an unchanged copied component from the sealed v6.10-D reference for reproducibility; rule and physical-limit modules are additive. Baseline v6.10-D and original v6.9-P2 regression suites were run independently on their untouched folders. These runs should be reproduced independently; the new ZIP includes only local new components, not earlier source ZIPs.

The synthetic example includes a locally conditional left turn, vehicle bridge-height restriction, and 2-link fixed-phase structural signal audit. No real road tags are parsed in this sample. Output `results/feature_audit.json` is fully synthetic.

See `docs/RESEARCH_DECISION.md` for provenance, limitations, and scientific rationale. Existing policy research P12-A/B is kept as a reference and was not modified.
