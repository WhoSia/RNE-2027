# T2 v6.10-F / P11-F / D4 — Complex road constraints, policy frozen

Research dated 2026-11-05. Derived branch, pre-existing v6.10-E source copied unchanged. New modules: `osm_relations.py`, `grade_geometry.py`, `variable_lanes.py`, plus 31 new tests and a synthetic structural audit. Earlier 29 tests are included in this local package. The previously sealed code/ZIP is not modified. **No policy optimizer code is changed or run.**

```bash
PYTHONPATH=src python -m unittest discover -s tests -q
PYTHONPATH=src python src/run_feature_matrix.py
```

P11-F scope: OSM simple node-via restrictions (`no_*`, `only_*`, mode-qualified, `except`, a narrow fixed weekday window) with unsupported syntax reported `UNRESOLVED_NOT_AUTHORIZED`; 2D strict segment intersections and declared layer classification (`UNKNOWN_3D_RELATION` if unverified); turn pocket length/footprint **upper bound only**; reversible-lane time-window states with overlap/gap detection, not live occupancy clearance.

Not yet implemented: complete OSM relation geometry or via-way restrictions, holiday conditional grammar, tested global jurisdiction rules, actual elevation/clearance and polygons, real route simulation integrated with new restrictions, real-world source OSM extraction, SUMO run, full vehicle dynamics, real held-out data validation.

All newly added results are synthetic. No actual traffic signal hardware, real road access certification, or field safety effect is claimed. The 120-item capability-gap catalogue is in `docs/UNHANDLED_VARIABLES.md`.

References: OSM turn restriction relation https://wiki.openstreetmap.org/wiki/Turn_Restriction ; ASAM OpenDRIVE v1.8.1 junction lanes https://publications.pages.asam.net/standards/ASAM_OpenDRIVE/ASAM_OpenDRIVE_Specification/v1.8.1/specification/12_junctions/12_04_connecting_roads.html ; SUMO pedestrians https://sumo.dlr.de/docs/Simulation/Pedestrians.html .
