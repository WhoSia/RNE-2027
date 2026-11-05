# R&E 2027 — T2 P11-X / D22 — Multi-zone event conflict audit
Date: 2026-11-05. P12 optimization FROZEN.

## Verified original code and counterexample
- Base: `WhoSia/RNE-2027` branch `research/t2-spatial-fig2-v02`, `p11w_d21/src/lane_fifo.py`, Git blob `61580e48e24dd384f30792e9d91bc7e9a22e1545`.
- Old single-zone design checked `d.conflict_zone != a.conflict_zone`. Python tuple arguments with partially overlapping labels were accepted implicitly but incorrectly treated as entirely different zones.
- Synthetic events: car_A at t=0, duration 5s, zones north+shared; ped_B request t=1, duration 2s, zones shared+south; car_C independent at t=1, duration 1s, zone far.
- Old W: entries car_A=0, ped_B=1, car_C=1 (unsafe model inconsistency when tuple labels denote zone sets).
- New X: entries car_A=0, ped_B=5, car_C=1; same-zone conflict is respected, independent zone is not blocked. All times synthetic.

## Code change and tests
- `Demand.conflict_zone`: supports `str | tuple[str,...]`, legacy default `global` unchanged. Tuples validated nonempty, unique and containing only nonempty strings.
- Normalized zone label sets are computed once during input validation, then overlap-tested with `&`. Movement conflicts apply only if zones intersect and movement-kind pair is forbidden; occupancy capacities remain independent.
- Unit tests: 25 unchanged W tests + 9 new tests, 34/34 passed locally. `run_case.py` independently reruns archived W and new X and asserts the witness; PNG and interactive offline HTML emitted.

## Model-theoretic caution
- Multi-zone *atomic locking* throughout entire duration is conservative and **not** a vehicle's trajectory through zones. It may overestimate blocking relative to sequential zone occupancy and real car following. Spatial zone boundaries must be derived from independently verified map geometry and continuous trajectories before field claims.
- A 2-way zone conflict check is a resource semantics contract, not calibrated yield/right-of-way or SPaT. No actual road-safety or optimized signal claim.
- This standalone simulator is not integrated into untouched legacy P10/P11 main engine; no SUMO run and no Jinju/inD trajectory reconstruction this D22.

## Next evidence gates
1. Demonstrate sequential zone-occupancy timing: release Z1 prior to acquire Z2 only with collision-free transition, finite junction clearance and no retrospective resource release.
2. Audit resource transitions at same timestamp and multi-request fairness. Avoid deadlocks and physically impossible overlap.
3. Bind movement resources/zones to independently inspected inD OpenDRIVE map + trajectories, then compare matched SUMO.
4. Re-run original P10 vehicle 1/8 counterexample with actual archived engine; validate timeline with event-time monotonicity.
5. Split exhibition question (finite spatial queues with observational confirmation) vs journal claim (event-time & conflict graph semantics). Do not publish overlapping exhibition work before eligibility review.

## Operational
Drive is primary byte archive. GitHub is manual `WhoSia` commits, never `github-actions[bot]`. P12-A/B retained but policy code, tuning and performance search still frozen; policy ideas only.
