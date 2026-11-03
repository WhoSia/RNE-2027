# T2 v5.8 — geometry-provenance and path-duration research (20261103)

This is synthetic three-junction microscopic traffic simulation research; it is **not** a calibrated operational traffic model or a real-world collision safety certificate.

## Reproduce

From this directory with Python 3.11+ (no third-party dependencies needed for core simulation):

```bash
python -m unittest test_v57.py test_v58.py -v
python experiment_v58.py
```

Expected: 20 tests pass. Experiment generates 192 exploratory runs and 96 untouched-seed holdout runs in CSV and JSON files. Full experiment output, SHA-256 manifest and source snapshot: [T2 v5.8 Drive reproducibility ZIP](https://drive.google.com/file/d/1I6Uf9T6f_C0IPl1NlDpc_iWM9g9lWuhF/view).

## Source lineage and fidelity warning

`geometry.py` and `network_v56.py`/`network_v57.py` are frozen historical test dependencies. `geometry_v58.py` corrects four right-turn synthetic polylines and `network_v58.py` adds optional path-derived movement occupation reservations, with the geometry conflict-graph pair set preserved at the tested 2.5m clearance threshold. The historical engine is *not* overwritten. `path_occupancy.py` uses exact line-segment clipping in a synthetic square junction; it estimates traversal as length divided by a clamped entry-speed proxy. It does not dynamically simulate turning speed, lateral acceleration, car width, or pedestrian conflicts.

Run modes: `zero`, `fixed3`, `path_floor4`, `path_floor6`. Comparing these modes is a sensitivity test, not evidence of model accuracy; results depend materially on the unmeasured minimum-speed assumption. Published claims must not state that the path-duration mode was field-calibrated or SUMO-validated.

## Research artifacts

- `RESEARCH_AUDIT_20261103.md`: implementation and empirical audit
- `EXHIBITION_20261103.md`: microscopic construction and internal verification narrative
- `PAPER_20261103.md`: policy-identifiability hypothesis, still not established
- `test_v57.py` and `test_v58.py`: independent regressions, accounting and geometry tests
- `experiment_v58.py`: matched-OD three-cohort independent-seed experiments

Next research gate: actual Korean lane geometry, measured signal phases/turning trajectories and held-out queue counts, followed by independent SUMO with internal lanes and physics of turning movement.
