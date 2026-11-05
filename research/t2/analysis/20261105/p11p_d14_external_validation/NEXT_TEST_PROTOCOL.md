# T2 D14 — test plan
## T1. Genuine local observations
Acquire Jinju CSV original, enumerate 10-day sample times and lanes; compare occupied queue vs movements; parse unknown/missing columns. Validate source SHA256 and license. Demand is latent without origin counts.
## T2. Car following
Select NGSIM Lankershim/Peachtree trajectories; split by recording session; fit simple IDM on training only; use constant-velocity and another car-following baseline; metrics MAE position [m], speed [m/s], headway [s], collision and physically impossible event counts. Compare calibration and holdout. Do not call camera reconstruction ground truth exact.
## T3. Map and turns
Use inD OpenDRIVE map and tracks; independent centerline 3D/2D coordinate reference, check knot and lane connection discontinuities, path deviation [m]. Germany and Korean intersections are separate cohorts.
## T4. Signal causality
Recreate P10's timestamp backward use minimal witness and new event scheduler; enforce event-effect timestamp monotonicity; vary dt. Only afterward test candidate policies.
## T5. Independent SUMO
Construct matched 2-intersection case and compare detailed queue discharge/vehicles; never compare unrelated network summary statistics.
## Hold
Actual phase-transition SPaT, ground-truth grip, Korea site-specific signal and traffic counts aligned at same time, real-world policy effects: NOT YET ACQUIRED.
