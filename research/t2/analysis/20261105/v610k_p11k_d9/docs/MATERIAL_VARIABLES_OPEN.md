# Road-pavement variables still not modeled (K follow-up)

**Observed versus inferred:** None of these quantities has been measured in K. They are implementation priorities, not a dataset.

1. Aggregate microtexture (polishing, exposed aggregate, micro-roughness).
2. Macrotexture / mean profile depth MPD and drainage channels.
3. Different pavement mix specifications, additives and binders.
4. Surface aging, raveling, rutting and pothole geometry.
5. Patch/hot-mix boundaries and lane marking surface differences.
6. Water film thickness and drainage rate / cross slope.
7. Rainfall intensity and elapsed time since precipitation.
8. Snow, ice, salt, sand and surface contamination.
9. Tire compound, tread depth, tire wear and inflation pressure.
10. Tire temperature, pavement temperature and seasonal variation.
11. Friction-speed curves, slip ratio/slip angle, anisotropy and load transfer.
12. Speed-dependent aquaplaning and water evacuation.
13. Field measurement procedure and uncertainty; test tire/vehicle calibration.
14. OpenCRG high-resolution friction surface inheritance and override rules.
15. Pavement roughness spectra and rolling resistance / vibration.
16. Road surface wetness and vehicle observation sensor errors.
17. Spatial mixing within lane, lane boundary transitions, object patches.
18. Time-variable pavement maintenance, repairs and degradation.
19. Vehicle-specific drivetrain/braking/traction systems and brake thermal effects.
20. Independent empirical pavement friction calibration and withheld validation sites/dates.

Do not infer specific pavement friction coefficients from a material name. The source XODR `friction` is application-dependent; actual effective grip and the model's assumed μ must remain distinguishable.
