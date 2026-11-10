# D42 × D44 — 2026-11-10 route evidence and physical feasibility gate

## Status: HOLD (research prototypes, NOT validated traffic-policy claims)

### D42: field trajectory continuation through OpenDRIVE junction
- Exact field inputs: three consecutive DLR UT v1.3.1 trajectory 15-minute CSVs 12:00–12:45 UTC and an unmodified OpenDRIVE source; input byte SHA256 recorded in the release manifest.
- Frozen candidate 1,449 approach-crossing events from the previous D42 lane-strip detector.
- Actual junction topology: 16 connecting roads, 44 laneLinks; 346 candidates lie in six lanes with >1 legal outgoing road, while 1,103 lie in lanes with only one possible outgoing road.
- **New test:** candidate track's 0.5–14s postgate noninterpolated positions compared against only laneLink-permitted connector road **reference centerlines** sampled at ≤0.4m spacing. Default exploratory criteria: ≥3 nearest observations within 3.5m, median nearest-reference distance ≤3.5m, and a 1.4m advantage against second possible connector.
- Outcomes: 175/346 multi-option lane candidates classified as **ROUTE_EVIDENCE**; 171/346 remained UNKNOWN. Among 1,103 single-outgoing candidates, 621 showed geometric supporting evidence and 482 remained UNKNOWN. Overall 621 SINGLE_TOPOLOGY, 175 ROUTE_EVIDENCE, 648 UNKNOWN_OVERLAP_OR_NO_VISIBILITY, 5 UNKNOWN_TRACK_END = 1,449.
- Sensitivity: proximity bound 2.5/3.5/4.5m resulted in 171/175/187 multi-option classifications. With separation margin 2.5m, only 155 classifications at 3.5m proximity. Thus these are evidence candidates, **not publisher-confirmed turns**.
- Important weakness: centerlines are *road reference curves*, not physical lane centerlines; a vehicle close to a connector reference line is not proven to have followed its permitted lane. No origin-to-destination publisher movement scoring or signal-head map has been verified.

### D44: sealed-original braking parameter-grid audit
- Sealed original D27 `micro_world.py` from archived `T2_D26_D30_20261106_RELEASE.zip`, **unchanged**; separate D44 constrained-braking reference.
- Grid: road lengths 8/10/12/14/16/20m × maximum deceleration .25/.5/1/2/3m/s² = 30 synthetic cases. One car (length 4.5m), same 1-second signal timetable and acceleration 1.5m/s².
- **24/30** original-engine test cases violate their own per-tick configured deceleration ceiling; reported collision violations = 0 in all 30. The separate reference rejects **one** of the 30 as physically infeasible under its assumptions.
- This is a deliberately selected **synthetic stress grid**, not 80% of real vehicles or road situations. D27 is still not patched. A collision-free count cannot certify physical realizability.
- Prior witness: from 3 to 0 m/s within 1s with declared max deceleration .25m/s² (12×). An admissible engine must detect infeasible stop states rather than teleport velocity to zero.

### Evidence, executed tests, and open gates
- **80/80 locally executed tests**: 58 frozen D42 regressions, 8 route-classifier synthetic checks, 10 independent braking-reference tests, 4 new D44 stress-grid tests. These tests do not validate real traffic or a repaired policy engine.
- Byte-verified, source-included small reproducibility ZIP: https://drive.google.com/file/d/1iR5-QsiPdP6r4vkY7Xm_10vHmGDtZOpz/view
- ZIP SHA256 `b5905b5f6ffa2cccc48607be8c5045bc5269158b8b042de4f28c0d5603fa27c7`; exact executed files include `d42_route_evidence.py`, `d42_route_sensitivity.py`, `d44_physical_gate.py`, tests, original D27 engine and original input SHA manifest. Large raw DLR CSVs not duplicated.
- Existing 2026-11-10 reasoning Google Doc: https://docs.google.com/document/d/1fkzetvDIyGTho0wyccceYvFhUvB5ZPtPAMhjmJK9DH8/edit
- **Next empirical gate**: build physical lane centerlines and finite stoplines, use observed outbound trajectories to audit each assigned connector, quantify UNKNOWN, and independently compare route-by-route DLR movement counts without fitting to them.
- **Next physical gate**: implement a viability-aware successor of D27 that checks feasible deceleration, vehicle conservation, stopline, collision, and dt-refinement invariants. Preserve sealed D27, and only then reassess policy rankings using independent SUMO.
- No actual field-policy improvement, actual queue-tail-wave identification, or independent SUMO run is claimed.

**Executable source provenance:** exact locally executed Python files are in the Drive ZIP. This GitHub Markdown is the committed scientific verdict; some full Python sources remain to be synced individually to GitHub, so do not claim exact source mirroring already completed.
