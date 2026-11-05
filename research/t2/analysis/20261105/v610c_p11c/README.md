# T2 v6.10-C / P11-C + Data D1 + Policy P12-A (2026-11-05)

Four tracks, derived only; historical research sources untouched.

## Track 1: capability
- `src/multihop.py` is a derived fork of v6.10-B with **bounded external source-lane storage** and per-lane outside backlog; lane occupancy is accounted separately from downstream link reservations.
- A shared source lane enforces physical FIFO between mutually exclusive turn requests. No second car on the shared lane can overtake the first just because another signal is green.
- `source_enter` occurs when footprint fits; `source_freed` is logged when the vehicle legally enters a connector. A source can free and new arrival can enter at the same *timestamp*, but connector exclusion still prevents simultaneous passages.
- Limit: virtual boundary outside remains unbounded, and source occupancy uses footprint slots without longitudinal geometry/wave propagation. A car entering the intersection is modeled as freeing its source footprint immediately; no stopline geometry.

## Track 2: verification
- v6.10-C 34/34 tests PASS; v6.10-B historical tests 37/37 PASS; v6.9-P2 historical test suite 28/28 PASS in an untouched extracted copy.
- Tests cover waiting outside the network, full source storage, shared FIFO, progress, conservation, timestamp monotonicity, route continuity, saturation and negative cases.
- This **does not** imply calibrated traffic dynamics, complete P9/P10 bug repair, or any actual SUMO runs.

## Track 3: real observed data
- Verified Utah SPaT query for `intersection_id=5502` with `$order=tmstp_utc ASC` and `$limit=500`. Actual public source response HTTP 200; 500 **parsed/normalized derived** observations kept in shared Drive dataset `40_DERIVED` and GitHub. 49.913-second observed time window, 7 adjacent observation state changes. **Not complete cycle identification, not an exact transition log, and not raw byte-sealed original.**
- Utah BSM 3-record schema probe successful. Jinju official 10,000-row CSV metadata and defined columns verified, original CSV not downloaded in this container.
- `src/spat_observations.py` fail-closed timestamp/state parser. The 500-row derived sample is separate and not bundled here to avoid implying source-byte provenance.

## Track 4: policy search
- 16 evaluation cells: demand 2 × source storage 2 × link storage 2 × travel time 2, eight J1 offset candidates each: 128 unique simulations, all 20 cars complete within 180 s.
- Compare fixed-0 (1 evaluation), 4-candidate even grid, sequential 4, shifted 4, and all-8 oracle. 80 algorithm-by-cell results, but only 128 unique physical simulations (cached); no invented additional traffic runs.
- Mean synthetic regret vs all-8 oracle in vehicle-s: fixed-0 74.6875; even-grid-4 0; sequential-4 49.625; shifted-grid-4 61; oracle 0. Even-grid always finds the finite candidate-space best in 16/16 cells, **NOT proof of general optimality**.
- Changing source storage 6.5→13m did **not** alter best offset in the 8 paired configurations. This is an explicitly reported negative result, reflecting current network's limited topology and shared-lane exposure.
- The 'controller' is **offline static offset search**, not a real actuated signal controller, MPC, or on-road policy.

## Replay
`cd T2_20261105_v610C_P11C && PYTHONPATH=src python -m unittest discover -s tests -q`
`PYTHONPATH=src python src/run_4track.py`

## Next gate
Build multi-lane shared/turn-pocket physical source storage, phase transition semantics (yellow/all-red), traffic-responsive control on a sensor contract, and independent SUMO two-junction benchmark. Keep matched budgets/holdouts and separate simulated from observed metrics.
