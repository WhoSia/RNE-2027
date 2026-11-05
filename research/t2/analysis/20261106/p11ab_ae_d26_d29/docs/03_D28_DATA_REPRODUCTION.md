# D28 — five source-to-reproduction gates

- [ ] G1 *Original raw provenance*: official source URLs, raw bytes, upstream checksums/SHA256, license, date of collection, immutable original and explicit transformations. **P2/P9/P10 historical source: PASS; independent GTFS/NGSIM/inD/Jinju: HOLD**.
- [ ] G2 *Matching observational units*: SI dimensions, lane vs link vs vehicle, time zone, GTFS service date + `25:15:00` time, detector counts vs standing queue length. **Contract functions: IMPLEMENTED; field schema audit: HOLD**.
- [ ] G3 *Independent SUMO execution*: same geometry, fixed signal phase, given OD/seed and time resolution; compare trajectory, queue, supply, and event timestamps. **XML input generator: PASS; external run: HOLD (no binary)**.
- [ ] G4 *Numerical convergence and adversarial tests*: source P10 direct replay PASS; new micro `dt=1,.5,.25,.125` sensitivity measured, but large drift means **CONVERGENCE FAIL/UNKNOWN**.
- [ ] G5 *Actual held-out predictions*: separate locations, distinct dates, held-out output comparisons and uncertainty with credible baselines. **Metrics/date split code: PASS; real prediction comparison: HOLD**.

Never label a planned feed as acquired. GTFS static schedule and actual real-time transit information must not be conflated. H3 indexes spatial units but is not by itself a route-time solver.

Official reference: https://gtfs.org/documentation/schedule/reference/
SUMO docs: https://sumo.dlr.de/docs/index.html
