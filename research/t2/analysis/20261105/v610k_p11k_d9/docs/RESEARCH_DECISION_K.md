# T2 v6.10-K / P11-K / D9 — Geometry × Pavement Material × Friction, 2026-11-05

## Decision and evidentiary boundary

**GO:** Implement an ASAM OpenDRIVE 1.8.1 **lane material subset** and a separate **hypothetical tire–surface friction-demand model**. Continue limited road geometry audits with an independent G2 curvature-jump test. **NO-GO:** Claim that a material label establishes actual skid resistance; claim a measured tire–surface coefficient; produce a field-safe vehicle speed; certify collision/traction safety; promote policy P12; or assert fully compliant OpenDRIVE parsing.

## New functionality

- `src/pavement_material.py` parses laneSection-lane `material` records, `sOffset`, required nonnegative `friction`, optional `surface` and `roughness`. Rejects unsorted, invalid, nonfinite, negative values. Missing records stay UNKNOWN; no material defaults are invented. A road OpenCRG surface or object material patch yields UNKNOWN because lane material may be overridden.
- `src/friction_demand.py` models a *hypothetical quasi-static contact force budget* for a road tangent frame, not a real tire. Variables: vehicle speed **v** (m/s), signed reference-line curvature **κ** (1/m), bank **φ** (radian), grade **α** (radian), longitudinal acceleration **a_x** (m/s²). Define q=v²κ; normal force per mass n=g cosα cosφ+q sinφ; lateral required contact force per mass f_y=q cosφ−g cosα sinφ; longitudinal contact force per mass f_x=a_x+g sinα. When n>0, μ_required=sqrt(f_x²+f_y²)/n. The contact model assumes a locally banked smooth rigid surface, aligned vehicle trajectory, quasi-static projections, no load transfer/detailed tire dynamics. The numerical comparison with an assumed effective μ is a **scenario**, not an estimate of actual grip.
- `src/road_physics_bridge.py` samples declared line/arc/spiral curvature, cubic elevation slope and declared roll at station s; combines them with independently supplied v and a_x. **Crucially, it does not transfer OpenDRIVE's application-dependent source `friction` to the physical effective μ slot.**
- `src/curvature_seams.py` reports G2 curvature discontinuities between geometry fragments; inherited source parser already checks G0/G1 within its restricted geometry subset.

## Synthetic counterexamples and tests

A fully synthetic 100m OpenDRIVE road declares a 50m line followed by a 50m arc κ=0.02/m; lane material asphalt with source friction 0.8 at s=0 and concrete with source friction 0.5 at s=60. Both labels/values are **invented test input, not field-derived typical coefficients**. At s=60 the new source record supersedes the earlier material, correctly selecting `concrete`. A G2 curvature jump is flagged at 50m. A synthetic parametric suite uses curvature 0.02/m, speed 5/10/15 m/s, bank 0/0.08 radians and longitudinal acceleration −1 m/s². Assumed effective μ=0.8/0.5/0.35 **only as explicitly declared numerical hypotheses**. There are 18 comparisons; the highest computed μ demand in this declared suite is about 0.47007 (dimensionless). These outputs cannot establish actual tire-road traction. In a flat 0-bank example with 15m/s and a_x=−1, μ_required≈0.47007; if assumed μ=0.35, model margin is negative; that is a model scenario, **not a roadway safety finding or a real-world speed advisory**.

`python -m unittest discover -s tests -q` → 149/149 PASS (parent J 113 + new 36). Separate read-only P2 original regressions `test_corridor test_optimizer test_coordinate test_robust` → 28/28 PASS. Source P2/J ZIP hashes preserved separately. No policy execution. No real-world XODR raw-file run; no SUMO vehicle simulation; no observed friction measurements.

## Literature and external definitions

- ASAM OpenDRIVE 1.8.1 [Lane material](https://simulation.pages.asam.net/opendrive-group/opendrive-antora-gen/ASAM_OpenDRIVE_Specification/v1.8.1/specification/11_lanes/11_07_lane_properties.html): application-dependent surface/friction/roughness profiles.
- ASAM OpenDRIVE 1.8.1 [Road CRG surface](https://simulation.pages.asam.net/opendrive-group/opendrive-antora-gen/ASAM_OpenDRIVE_Specification/v1.8.1/specification/10_roads/10_06_road_surface.html): OpenCRG with purpose=friction can override lane material.
- FHWA [Pavement Friction for Road Safety Primer](https://highways.fhwa.dot.gov/safety/rwd/keep-vehicles-road/pavement-friction/pavement-friction-road-safety-primer-friction): field friction measurement, micro/macro texture and friction demand. Source-specific measured pavement friction is essential for empirical calibration.
- FHWA [Surface Texture Advisory](https://www.fhwa.dot.gov/pavement/t504036.cfm): microtexture and macrotexture both affect wet pavement friction; asphalt and concrete categories alone do not determine wet grip.
- SUMO [Friction device](https://sumo.dlr.de/docs/Simulation/Friction.html): lane friction input to a device-specific speed factor. **Its fitted speed factor must not be conflated with the quasi-static friction budget implemented here.**

## Next research gates

1. Field and source data: genuine friction measurement with test speed, equipment/protocol, pavement location/time, precipitation/water film, texture and uncertainty. Original source bytes and provenance.
2. Geometry: lane-level **signed curvature** rather than just road reference curvature, and normal-direction/grade/roll consistency; frame and direction sign audit, superelevation across laneSection knots, G2 seam evidence.
3. Physics: tire slip, friction-speed relation, longitudinal/lateral anisotropy, aquaplaning, ice/snow, load transfer and tire temperature/pressure; do not assume one constant μ is a real full tire model.
4. Independent SUMO friction-device matched tests only after an executable SUMO instance and identical input semantics are established.
5. Compare OpenDRIVE lane material inheritance/overrides and OpenCRG data when properly licensed source files become available. **Policy track remains frozen.**
