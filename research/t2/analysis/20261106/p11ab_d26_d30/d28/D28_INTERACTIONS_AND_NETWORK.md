# D28 — Network interactions and heterogeneous traffic: LIMITED INTEGRATION

The reference `src/micro_world.py` runs multi-link OD paths; parallel lane vehicles; a gap-based **instantaneous** lane change when a target lane is free; limited merge across lane-count reductions; fixed signals; pedestrian blocking windows; bus-specific length/acceleration and stop dwell; grade and curvature speed modifiers. `src/od_and_policy.py` generates reproducible time-varying OD arrivals with local random seeds.

In-scope regression: parallel lane cars finish, no immediate simultaneous opposite lane swaps, congested downstream road delays upstream insertion, bus stop increases travel time, pedestrian window delays discharge.

Not implemented as realistic models: longitudinal car-following calibration, finite-duration lateral trajectory, conflict polygons from OpenDRIVE, turn yield rules, roundabout yielding, pedestrian kinematics, detailed bus passenger counts, stochastic validated OD inference, per-lane toll/speed-limit maps, signal clearance with all pedestrian phases. Multi-road graph is abstract; adding edges is NOT evidence of an entire realistic urban network. This file sets explicit feature-level PASS/HOLD status and does not falsely declare ten physical factors fully completed.
