# T2 v5.7 — reproducibility and constraints (20261103)

Historical baseline: v5.6 network and geometry preserved. New spatiotemporal gate stores half-open intersection intervals [entry, exit), filters conflicting movements from subsequent tick admissions and re-audits all admitted crossings after simulation. Same movement uses preexisting discharge headway, nonconflicting geometry movements may overlap in time. 

Recomputed retrospective v5.6 audit of 72 OD replicates: under hypothetical 2s occupancy intervals, 365 incompatible interval-overlap pairs (balanced 142, main 96, side 127); under hypothetical 5s, 2190 pairs (balanced 659, main 491, side 1040). In these synthetic cases this is a discovered omission in the old constraint checking, NOT empirical road collision data.

17 tests passing (7 historical +10 new). 216 new microscopic simulations = 108 exploration +108 independent holdout. In holdout under 5s compared to 0s, average accumulated vehicle-second exposure changes: balanced +973.58, main peak +764.46, side peak +1844.08; each 12/12 paired seed comparisons was positive. The 2s side-peak response CI includes zero. Longer occupancy mechanically reduces service opportunities; results are parameter sensitivity, not real-road travel-time effects.

Known limitations: 2/5s are user-defined constants, not measured or calculated from path geometry/speed. Movement conflict graph comes from synthetic lane centerlines; full-body swept trajectories and pedestrian conflicts absent. Same-stream following uses independent headway. Data neither field calibrated nor SUMO validated. Next per-vehicle occupancy inference and comparison to independent simulation/field sources.

Full reproducible ZIP T2_v57_temporal_occupancy_20261103.zip SHA256 b02ca2e692243f1e7e0be3b9bb1f7ba346f2c557e52496411c0707a5b29e984c.