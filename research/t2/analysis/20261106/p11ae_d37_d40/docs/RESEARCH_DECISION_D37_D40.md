# T2 — 2026-11-06 / D37–D40 Research decision

## Objective and evidence hierarchy

Objective: reproduce real intersection congestion at **one known signalized intersection** in independently executed T2 and SUMO, then assess whether detector error can reverse fixed-time versus actuated signal policy rankings. The intended result is not the count of features written; it is **coincident, observable, independently checkable real-world evidence**.

**Current status: not completed.** The single-intersection primary reference is [DLR Urban Traffic v1.3.1](https://zenodo.org/records/20919480), AIM Braunschweig research intersection. Dataset description includes 32,296 tracked road-user trajectories and 30 signal heads. Large original ~463.4MB archive **not downloaded, not hashed, not replayed**. [CityArtery v1](https://doi.org/10.17632/ftzzmh2cmt.1) is backup (signal timings + trajectories + SUMO calibration metadata; raw unacquired). These claims are metadata-level, not raw observational results.

## Actual external observation achieved now

GitHub app directly read 16 **original source CSV texts** from [CATS-Lab Data-AV-Traffic-Light-Stop-Sign](https://github.com/CATS-Lab/Data-AV-Traffic-Light-Stop-Sign): 8 published preselected 'stop' and 8 published 'straight through' segments. Per-source Git blob SHA-1, source URL, raw 91-row count, arithmetic mean speed, frame-level stationary (`AV_speed < 0.5 m/s`), circular/arrow red/green state-frame counts were derived in the connected app. **Only derived statistics and provenance are included in local/Drive artifacts**. The original copyrighted or licensed underlying CSVs were not stored locally. The 16 observations have 1,456 frames at 10Hz but there are only 16 *preselected episodes*, not 1,456 independent drivers or one crossing. Observable stop fractions: stops 328/728 (45.05%), straight-through 87/728 (11.95%). This is descriptive and the group labels were chosen *in advance by original dataset organizers*, so it is not an independent classification performance validation. Some 'through' episodes have red-light codes in some frames; no violation, route control, or signal-program effect is inferred. README code map includes 4=red circle, 6=green circle; undocumented -1 in observed CSV must remain unknown.

Separate SinD Changchun Pudong source map (connector read, no local raw copy) 409 nodes, 59 ways, 37 lanelet relations; `lat/lon` near zero should not be used as real GPS or metres. Signal file and vehicle trajectories exist as Git LFS *pointers*, original bytes not acquired: SHA256 and LFS size recorded in `data/source_registry.json`.

## Verification artifacts

`src/trajectory_gate.py`: fail-closed original CSV parser, nonfinite/unknown state handling, deterministic matching of actual file content against derived observations; never treat -1 as red/green. `src/empirical_summary.py`: episode-level descriptive summaries and source uniqueness tests. `src/queue_observation.py`: explicit lane-specific stopped-vehicle window count, distinct from true queue length or spillback, requiring calibrated stopline. `src/parity_contract.py`: blocks T2-SUMO comparisons if geometry/demand/signal/units/vehicle ids/queue definition or raw output provenance differ; incomplete trip records cannot be silently omitted. Tests use small synthetic schemas and the 16 independently sourced metadata rows.

## Before any scientific award-level claim

1. Obtain and SHA-256-pin DLR UT version 1.3.1 raw archive, signal phases, signal head to movement mapping, signal-control status; reject if misaligned or unavailable.
2. Declare one intersection, observation interval, exact approach stopline, lane geometry, vehicle dimensions, stopped-speed threshold and queue-length operationalization *before analysis*.
3. Independently execute pinned SUMO binary on the same geometry/demand/vehicle types/signals, preserve raw `tripinfo`, fcd and queue output, source hashes, version, and calibration/holdout separation. A proposed `sumo` XML is NOT a run.
4. Run core T2 with time-step refinement, validate no event backdating and no overlap, compare queue onset, discharge, tail and occupancy to **observed** records and SUMO. Report failed conditions.
5. Freeze comparison policies **after** baseline fits. Pre-register a not-previously-inspected holdout day/interval and control for detector error distribution, queue censoring, demand and independent simulation.

## Policy status

Offline policy research is open; real-world traffic control use or recommendations are out of scope. D36's +0.3625s mean difference at 40 cars / 20% dropout / 1-tick delay came from 4 synthetic seeds, 3 slower and 1 much faster; its exploratory 95% bootstrap interval includes zero. No general policy ranking follows.

## Verdict

**D37 raw observational metadata achieved; D38 single-intersection observation missing; D39 independent SUMO missing; D40 observed-noise policy evaluation missing.** Do not elevate trajectory metadata into complete intersection data or source-directory inspection into raw-byte acquisition. Next work targets a single verifiable Braunschweig AIM observation window rather than writing another uncalibrated simulator feature.
