# D27 — Longitudinal micro motion and finite lane storage: PROTOTYPE PASS

A new, independent reference simulates the rear position (m), velocity (m/s) and acceleration limit (m/s²) of each vehicle on fixed-length lanes. It enforces an explicit constant minimum intervehicle gap and checks no overlapping vehicle footprints at each full-second sample. Source admission is capacity constrained by actual longitudinal vehicle lengths and gap. Synchronous snapshot updates are used; source space freed during [t,t+1) cannot authorize entry at t.

The vehicle dynamics are **not the original T2 engine**, not a calibrated IDM, not continuous collision-free trajectories and not an emergency braking model. Discretization is fixed at **1 second**; the model throws an error for other grids. Phase transitions to a downstream link are simplified instantaneous link reassignments, not finite intersection crossing times. These are critical HOLD gates.

Verification: tests cover single trip conservation, 7 queued cars with no snapshot footprint overlap, bus/car storage, fixed red signal, crosswalk blocking, a 2-link upstream effect, curved road and grade bounded speed, invalid geometry and deterministic lane change. See `tests/test_micro_world.py`.

Next: vehicle state crosswalk and geometry refinement, IDM and Gipps references, independent SUMO FCD with matched car length and speed, multiple dt convergence and event causal trace for all transfers.
