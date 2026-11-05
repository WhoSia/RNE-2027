# T2 v6.10-M / P11-M / D11 — Differential road geometry and field-data contact

2026-11-05 · R&E 2027. **Policy P12 remains frozen**. This is a research package, not a traffic-control or road-safety tool.

## Reproduce

```bash
python -m unittest discover -s tests -q
python src/run_m_audit.py
```

Read `docs/RESEARCH_DECISION_M.md`, `results/M_geometry_independent_audit.json`, and `data/external_field_source_registry.json` before interpreting numerical values. The package contains inherited L source files and original P2 reference copy only for read-only regression. It does **not** contain DTU friction CSV source bytes, FHWA measurement rows, complete OpenDRIVE field models, or fresh BSM data. No raw road-friction results were fabricated.

The 188 tests include 173 inherited L tests + 15 new geometry tests. The separate original P2 28 tests run under `reference/P2_original/T2_v69_P2`. Older artifacts are not overwritten. The synthetic curvature estimate is not evidence of safe driving speed, physical tire grip, or legal road connectivity.
