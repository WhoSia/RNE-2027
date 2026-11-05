# T2 v6.10-G / P11-G / D5 — OpenDRIVE 3D Reference Geometry

Date 2026-11-05, R&E 2027. Policy (P12) intentionally frozen.

## Reproduce

```bash
PYTHONPATH=src python -m unittest discover -s tests -q
PYTHONPATH=src python src/run_opendrive_audit.py
```

- Adds `src/opendrive_ir.py`: explicit **ASAM OpenDRIVE XML subset** for line and arc reference-line geometry, 3D elevation polynomial segments, lane-section widths, and explicit junction laneLink reference existence. Geometry `s` and XY joins must be continuous. All geometric values in SI units, heading radians.
- New 16 tests plus 60 inherited tests: **76/76 passing**. Independently re-tested unmodified v6.9-P2: 28/28 passing.
- Unsupported road geometries (`spiral`, `paramPoly3`, `poly3`), full lateral surface physics, laneOffset, superelevation, actual turn direction, priority, geometry conflict and region law cannot be inferred. OpenDRIVE `junction laneLink` does NOT imply that all real-world traffic regulations permit the movement.
- Synthetic two-road/one-connection fixture is **not real road geometry**. No SUMO vehicle runs, no OSM raw acquisition or real-world validation.
- External source registry confirms `esmini/esmini` public `straight_500m.xodr` 7080-byte text, Git blob SHA1, one line / one road / one lane section. Its raw bytes could not be transferred to this container and were **not parsed here**. Retrieval was metadata + public GitHub connector text inspection only. License is not verified for redistribution, so its content is not included.

The aim is a reusable road-world representation, not deploying or selecting traffic policies. Previous v6.10-F source modules are copied byte-identically into this package for test reproducibility; original ZIP is unchanged.
