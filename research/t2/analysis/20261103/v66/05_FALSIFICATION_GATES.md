# v6.6-P0 — Special researcher review gates
Decision: promote the demonstrated theoretical counterexample and tested synthetic factor interactions, but HOLD real-safety and signal-control efficacy claims.
P0: measure queue discharge headway and admissible stopline crossing; audit signal green gate against actual free-acceleration reachability. Vary dt before trusting discrete collision checker.
P1: per-vehicle dimensions/accelerations and mixed fleet, geometry and car-following together (not an isolated scalar). Explicit downstream storage/supply, spillback, pedestrian and cyclist crossing conflict phases.
P2: lateral lane-changing (decision / initiation / insertion / completion), turn-specific paths and multi-vehicle compatible conflict occupancy.
Validation: field geometry+signal+turn flow; split day into calibration vs untouched holdout; match SUMO and T2 OD; report queue, movement flow, and travel time independently. Freeze pre-registered comparison metrics and check 800s incomplete vehicles.
Two goals: exhibition needs empirical trajectory and queue prediction; academic paper needs observation sufficiency and policy regret not conflated with simulator artifacts.
