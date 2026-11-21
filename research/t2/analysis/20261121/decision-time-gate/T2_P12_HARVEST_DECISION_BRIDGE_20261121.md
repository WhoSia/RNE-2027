# T2 P12 — Harvest-to-research bridge: three source-backed transfers

Date 2026-11-21. Sources inspected at accessible online documentation level. None establishes calibration of the R&E model.

| Source | Transfer into T2 | Scientific failure mode | Implementation boundary |
|---|---|---|---|
| FHWA Traffic Signal Timing Manual Chapter 5 | Distinguish green, yellow change, red clearance and pedestrian considerations in a phase specification | A permissive 4-tick service may be physically possible yet not admissible when clearance obligations are omitted | A **configurable abstract validator**, not copied US law |
| SUMO Simulation/Randomness | Distinguish deterministic equispaced departures, random fixed-count time allocations, Poisson-style departures | Distinct random seeds with deterministic timestamps are not independent temporal samples | Keep independent clock-family evidence separate; don't claim SUMO run |
| Espressif esp-csi get-started | Real first-party CSI send/receive and subcarrier visualization are plausible under approved hardware | Seeing Wi-Fi subcarrier changes is not equivalent to camera images, vehicle localization or congestion diagnosis | E-track prototype only; never feed synthetic RF performance as physical probabilities |

Sources:
- https://ops.fhwa.dot.gov/publications/fhwahop08024/chapter5.htm
- https://sumo.dlr.de/docs/Simulation/Randomness.html
- https://github.com/espressif/esp-csi/blob/master/examples/get-started/README.md

## Cross-axis experiment
T2 tests whether an action is *meaningfully defined* before judging it, E tests whether a measured physical observation exists before using it. Both are an evidence-interface test: an attractive display cannot substitute for latent-state labels or admissible control actions.

The core claim remains *process validity under stated assumptions*, NOT real-road safety or novel field policy performance.
