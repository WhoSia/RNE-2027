# T2 P11-AA / D25 — physical link-packing audit + GTFS integrity gate

**2026-11-06 (KST).** Policy P12 remains **FROZEN**. Research paths: development/validation active; policy design ideas only. All traffic requests in this deliverable are **synthetic**.

## Source & exact scope

- Original D24 `phase_network.py` and `gtfs_gate.py` sealed byte-for-byte under `baselines/` before editing.
- `src/phase_network.py`: adds an **optional** `StorageGeometry(zone_lengths_mm, vehicle_lengths_mm, gap_mm)` parameter. Existing `simulate(...,capacity)` semantics remain the default. The extra gate checks whether the sum of the admitted vehicles' representative lengths and (n-1) equal gaps fits within each named zone, while retaining the old integer slot caps.
- `src/gtfs_gate.py`: rejects duplicate ZIP members and active `trip_id`s with zero or one `stop_times` row. Previously they could silently disappear from the emitted connection list.
- New tests: 6 geometry tests, 4 GTFS integrity tests. Existing D24 tests: 18. **Total: 28/28 pass**. Additional randomized single-zone FIFO model vs independently written event-based packing oracle: 100 cohorts, valid-fit cohorts cross-checked.

## Model witness: a declared capacity of two slots is not two physically fitting vehicles

At zone length L=15.0m, representative car length 4.5m, bus length 11.0m and declared gap 2.0m:

- 2 cars: 4.5+2.0+4.5=**11.0m**, fits.
- Bus + car: 11.0+2.0+4.5=**17.5m**, does not fit.
- D24 baseline capacity(A)=2 grants the follower car at t=1 in either case.
- D25 additional geometry check grants second car at t=1 in the car+car case, but the follower car behind the bus at **t=4**, after bus release. At L=17.5m the bus+car follower can enter at t=1.
- 17 geometry lengths × 5 desired gaps = **85** synthetic scenarios, with CSV and visualization. No field calibration and no recommendation of real-world safe vehicle gaps.

### Important physical caveats

This is a **one-dimensional aggregate packing bound**, not vehicle following: no longitudinal position, queue ordering within zone beyond pre-existing per-lane FIFO, acceleration, turning geometry, slope, braking, collision detection, or actual occupied lane boundaries. Gap is an illustrative model input, not a physical or safety prescription. `capacity` remains independent; it may still impose a stricter upper bound than geometry. Multiple intersecting zones reserve full representative length in each zone; no partial vehicle-body geometry. Does not turn D24 into a microscopic traffic simulation.

## GTFS integrity witness

The previous loader required base records but did not reject an **active trip with no timed stops**, nor an active trip with only one stop. These could make a timetable appear to provide less service than the source declared without any error. Repeated ZIP member names could be silently overridden by the ZIP reader. D25 fails closed on these cases, while permitting inactive trips without stop_times for the selected service date. This is still **not a general GTFS validation implementation**. Real GTFS original ZIP not acquired, no official timetables evaluated; synthetic fixture only.

## Prior P10 original-provenance breakthrough, not a run

Located **actual P10 source directory** in GitHub: `research/t2/analysis/20261104/v69p10` with `code/p10_boundary_trace.py`, `code/p10_capacity_ablation.py`, `code/p10_fine_refinement.py`, `tests/test_p10_mechanism.py`, and `derived/capacity_time_safe.patch` plus four original reports. This is a meaningful improvement over referencing P10 only from later memory summaries. The primary witness described by the archived report: `upstream_peak`, 18m link, seed 223, (24,24,24) signal, car storage footprint 6.5m, last possible side entry 47.1625s, dt-dependent vehicle 8 connector entry. The archived source itself imports P2 `dt_convergence`, `vehicle_schema` and an immutable reference. These dependencies are not yet mounted/executed in the local test. **No direct original P10 replay completed in D25.** Historical outcomes are reported only as the previous source's claims.

## Exhibit versus paper

- Student science exhibition: finite turn pocket and pedestrian-zone occupancy observed in an actual intersection, with queue length and delay measured against independent SUMO and matched fixed demand. Packing bound is only an input-model audit.
- Journal research: event-causal state semantics, finite geometric storage, overflow invariants, phase boundary convergence, and strong comparison to CTM/LTM/discrete-event state transitions. Novelty not yet established.
- Next hard gate: retrieve immutable P2/P10 archive, verify full byte hashes and execute exact vehicle 1/8 regression; then match SUMO and observation definitions. No optimized signal comparisons.

## Sources / evidence types

- D24 primary source: GitHub `research/t2/analysis/20261106/p11z_d24`, branch `research/t2-spatial-fig2-v02`.
- Historical P10 original (not re-run): GitHub `research/t2/analysis/20261104/v69p10`.
- Official GTFS schema: https://gtfs.org/documentation/schedule/reference/ .
- Results: local Python unit tests, `results/D25_results.json`, `results/length_gap_sweep.csv`, visual PNG and offline HTML. The original D24 GTFS fixture remains **synthetic**.
