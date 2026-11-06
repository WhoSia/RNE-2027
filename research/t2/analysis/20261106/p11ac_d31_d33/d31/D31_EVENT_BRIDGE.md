# D31 — Source-pinned P10 event-causality bridge

Date: 2026-11-06. **ORIGINAL-REPLAYED for P10; not equivalent-microphysics validation.**

Source-of-truth is the sealed D26 release, extracted unchanged to `upstream` for this development. `references/p10_replay.json` retains the P10 replay receipt from the previous output. Independently, the original `p10_boundary_trace.run_trace` was executed again with the actual P2 `corridor.py`, P9 `dt_convergence.py` and original P10 script. Reproduced vehicle 8 entries at dt .5/.4/.25/.2/.125/.1/.0625/.05: 47,87.6,87.25,87.4,47.125,47,47.0625,47 s. These are the archived source's own mechanistic scenario, not a universal proof.

`src/event_bridge.py` defines only a common event representation `(time, actor, action, location)` for original P10 and D27 micro reference. It rejects out-of-order logging, malformed IDs, negative or nonfinite times, and identifies the *source-qualified* capacity backdating for the original vehicle 1/8 occupancy/phase witness. In dt=.5, vehicle 8's t=47 admission is 0.5 s before car1's link receipt at 47.5, an invalid use of freed capacity under the known 18m two-vehicle storage state. No claim of direct physical equivalence or complete P10 patch correctness.

**Major remaining issue:** D27 still has dt=1 only. This bridge does not establish time-grid convergence, continuous trajectories, or the microscopic model's parity with original P10. Explicitly next: port the corridor event source into D27's state contract while matching geometries and per-vehicle event semantics.
