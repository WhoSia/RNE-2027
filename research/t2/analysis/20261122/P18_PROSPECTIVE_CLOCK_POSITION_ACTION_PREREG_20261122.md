# T2 P18 — Canonical-PHYS replication followed by prospective arrival-clock, position and abstract-feasibility study

Date 2026-11-22 KST. **Prospective design written after successful exact-source PHYS-04 replay but before executing the new P18 cohort.**

## Exact canonical gate already completed

Five source files were fetched from GitHub WhoSia/RNE-2027 at explicit `main`, moved through a byte-preserving percent-encoded Google Docs source manifest, exported locally and restored. Every restored file's `git hash-object` matches the connector's original Git blob:
- `dual_lane_v11.py` a7c9aa6954402e12894d1d5b722e8a474b0bd58f
- `spatial_v10.py` ffbf3fc3f8b9a64a819d4f73ce70b264b877e84e
- `receiving_cells_v15.py` b078cf215c74b76ace6dffcbcbacab6ae22c3673
- `physical_transfer_screen.py` 8d75745053ff720db6c8af0001aaaf13ba1f295e
- `physical_checkpoint_capacity_screen.py` 220aeafb492fa41c8a9908f215e393f15fdfb22b

Standalone Python 3.13.5 `physical_checkpoint_capacity_screen.py` regenerated all 144 records; **144/144 `pairs` entries are exactly equal** to historical SHA-sealed `canonical_local_capacity144.json`. Top-level formats differ (summary label names and metadata), so *whole JSON hashes differ*. This is exact-source replay of five dependencies, not a full Git checkout or proof of field validity. Historical seal: ZIP SHA256 7f7eff90b83cfe5e1f071bb02d5880face9c0e047abcd17349cd3fb06392758e; old result SHA256 0d91beab746b8e67bf1fa5ea327e3c982d10e39b57cd5cf2fef020ad328e1001.

## Pre-fixed research question
When vehicle count and **ordered movement-label tape** are exactly fixed, does changing only timestamp allocation alter the synthetic 84-second policy effect, once predecision positions are audited and abstract action-feasibility conditions are declared separately?

## Cohort, independent unit, outcomes
- Fresh seed labels: 104–111 inclusive; two regimes (1800 vehicles/h with left fraction .45; 1650 vehicles/h with left fraction .50).
- Duration 240s; decision tick 84; terminal penalty 60; same base `leading` 120s schedule and `clearance_s=3`.
- Pocket 14 or 28m; receiver 2 or 4 cells; through-B assignment 0 or .5; lane changes enabled, target clearance default 1.
- Two clock types: canonical `spatial_v10.arrivals` (deterministic tick spacing), versus seeded sorted-random timestamp reassignment using `random.Random(seed+1_000_003)` in slots [0,239], retaining *each original request's route label in index order*. Verify same ordered labels and total requests.
- This makes 2 regimes×8 seeds×2 clocks×2 pockets×2 receivers×2 B shares = **256 unique worlds**. Each world has a baseline and two **abstract** candidate modifications (4s and 8s left-green) from an exact shared checkpoint.
- Old 4s action: `((84,87,'-'),(87,91,'L'),(91,120,'-'))`. 8s action: `((84,87,'-'),(87,95,'L'),(95,120,'-'))`. Both use the simulator's native 3s no-service clearance and no extra physical period; later baseline phase resumes. **Neither models real amber/red rights or pedestrian clearance**. They are not controller programs.
- The 'illustrative minimum green 6s' policy screen marks the 4s action INELIGIBLE under this **invented parameter**, and 8s potentially eligible **only on that minimum-green criterion**. This is not a jurisdictional safety verdict; do not silently use 4s as an operational recommendation.

## Pairing and leakage gates
1. Same-world baseline/treatment must share byte-equivalent predecision checkpoint (copy and pickle hash before/after) and same full arrival tape. Verify generated vehicles, conservation, and direct vs resumed baseline.
2. Retain SHA256 of each complete `(timestamp, movement)` tape; neither a new seed ID nor a route-label match proves independent traffic histories. Also record arrival count *before* tick84.
3. Treat cross-clock worlds as **different predecision states** even when total and ordered movement labels match. Their policy deltas are not same-state causal effects.
4. Compare state information at three levels: six counts, then six counts plus four occupied-cell position tuples, then full checkpoint identity; do not treat equal counts as equal microstate.
5. Match regime, receiver, pocket length, B-share and identical action definition before searching delta opposition. Threshold epsilon=5 model vehicle-seconds, **strict >**.
6. Report the total number of signature collisions, opposite-effect pairs and **distinct actual arrival-tape SHA256 values per group**. One timestamp tape copied across seeds cannot masquerade as independent.
7. Publish zero strong aliases as **NO_WITNESS**; compare against invalid ablation dropping B share only as labeled negative control.

## Exploratory analysis quarantined
After primary figures, possible conditional comparisons by 4 vs 8s green, source of pocket block in event traces and departure-time distribution can be performed only with explicit exploratory labeling. Do not tune the cohort or epsilon to produce a preferred conclusion.

No external traffic signal actuation; K047 remains sealed; 5GB CIM dataset untouched; no GitHub Actions or bot. This is an uncalibrated synthetic model experiment. 
