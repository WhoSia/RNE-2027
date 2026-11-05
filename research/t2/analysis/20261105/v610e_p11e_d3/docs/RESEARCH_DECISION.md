# T2 2026-11-05 — v6.10-E / P11-E / D3: policy feature freeze

## Research decision

**No new policy optimization or adaptive controller work in this unit.** Existing P12-A/B prototypes are kept as immutable research references. Our goal is to expand the descriptive domain before selecting a policy: changes to physical movements, local regulations, time windows, bridge/underpass access and observed signal programs can change the feasible policy space and therefore the argmin.

## Implemented

- `src/road_rules.py`: explicit modal permissions, prohibition windows with weekday/overnight semantics and timezone-aware instants, multi-step route audits. `UNKNOWN` is distinct from `DENY`, never silently `ALLOW`.
- `src/physical_limits.py`: vehicle height/width/length/gross mass versus sourced lane-specific maximum values. Missing values stay `UNKNOWN`. `PASS_DECLARED_ONLY` is not a legality or safety certificate.
- `src/signal_binding.py`: read-only SUMO `tlLogic` static phase program structural parsing. Tests uniform signal-state widths, positive phase durations, and binding of `linkIndex` to RoadIR's declared connections; runtime active program stays unknown.
- 29 newly implemented unit tests, independent 62/62 prior v6.10-D and 28/28 original v6.9-P2 regression tests passed. Total 119 passed across separately executed suites, **not** 119 independent proofs of overall engine correctness.

## Source and data boundary

- OSM `restriction:conditional` syntax is richer than the manual overlay in this version, including vehicle hierarchy, time conditions and exemptions; the importer **does not** parse arbitrary OSM restrictions and must not claim that it does. Relevant documentation: https://wiki.openstreetmap.org/wiki/Conditional_restrictions and https://wiki.openstreetmap.org/wiki/Turn_Restriction
- SUMO `tlLogic` is read as source representation; additional file program override/WAUT and runtime active program are not inferred: https://eclipse.dev/sumo/docs/Simulation/Traffic_Lights.html
- Utah SPaT 1,000 queried observations for intersection 5502 from the prior D2 remain `derived`, not raw byte-sealed original. Jinju source CSV and SUMO vehicle benchmark remain missing. No new external data release is claimed in this unit.

## Scientific implications

A later signal optimization problem must not be viewed as a fixed abstract feasible set. The road model, regulatory model, vehicle classes and observation data jointly define the constraints and cost. If new evidence changes lane access, turns or clearance, this changes the optimization domain or objective. A previous optimum only qualifies for the old conditional model. This is a research decision, not a theorem of policy instability.

## Next functionality and validation

1. Strict importer from real OSM relation data with permitted exceptions and temporal restrictions; preserve raw source bytes + license, parsed derived model separately.
2. Link geometries (stoplines, conflict polygons, elevation/levels, reversible lanes and dedicated turn pockets) and a verification suite with clear unknown states.
3. Bind `tlLogic` actual active-state programs to movements and detect contradictory/disconnected or incomplete signal map; independently compare with SUMO read-only outputs.
4. Data D3: acquire longer, timestamp-sealed observed SPaT/BSM records with grounded spatial mapping and observed-data holdout. No field response modeling until correspondence established.
5. Policy P12 remains frozen until the descriptive road engine and validation gates have materially progressed.

Prior ZIP and GitHub artifacts are untouched; manual author only; `github-actions[bot]` must not be a contributor.
