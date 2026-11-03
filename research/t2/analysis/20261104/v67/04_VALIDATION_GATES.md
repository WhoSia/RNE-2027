# v6.7-P0 — Special research review
Verdict: ACCEPT isolated mixed-fleet/spillback/pedestrian-phase mechanism exploration; HOLD physical simulation validation and safety.
P1 integrate vehicle-class length/width/min-gap/accel/brake/headway into v6.6 upstream IDM and 2D connector with rear-clearance state, conserving each vehicle at each tick.
P2 represent downstream receiving vehicle positions in space, blocking connector if no room and avoiding double occupancy.
P3 represent pedestrian trajectories and actual legal crossing phases rather than an arbitrary first-12s blockage.
P4 collect field turning movements, heavy-vehicle fractions, exact signal phases, crosswalk geometry, discharge headway, queues and completion traces; validate independent SUMO and holdout field days.
Scientific standard: retain a simple model if more complicated physics does not improve held-out prediction. No Github Actions bot contributions.