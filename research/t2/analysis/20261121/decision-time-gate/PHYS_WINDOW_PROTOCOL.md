# T2-PHYS-02 — Pre-registered timing-window extension (2026-11-21)

**Status: DESIGN BEFORE RUN.** Primary PHYS-01 evidence remains unchanged. This is an independently labeled exploratory extension designed after we learned that 16/48 original physical scenarios reverse phase preference under all-day lane-change permission.

## Fixed physical model
Keep original `dual_lane_v11.py` cellular motion, 7m cells, same 8 demand seeds, 720s horizon, 1800 veh/h, 50% left turns, original lane preassignment, fixed B occupancy rules, 4-cell downstream receiving link, the same 70m allowable lateral-movement zone. Introduce one **explicit parameter** `lane_change_windows`: an ordered tuple of half-open absolute time intervals. The empty tuple preserves original behavior. When provided and `allow_lane_changes=True`, A→B may occur only if t lies in one of these intervals **and** the existing spatial/effective gap eligibility rules pass. An interval being open never guarantees a lane change.

Four prespecified window conditions per paired geometry/arrival stream:
- `never`: `allow_lane_changes=False`.
- `always`: `allow_lane_changes=True`, no time restriction.
- `early`: 15 ticks per 120-tick signal cycle, half-open [20+120c, 35+120c) for cycles c=0..5.
- `late`: 15 ticks per 120-tick signal cycle, half-open [70+120c, 85+120c) for cycles c=0..5.

Equal counted openings across `early` and `late`: 90 permitted ticks each over the 720-tick horizon. Keep fixed the **number** of windows, the permitted time, the lane geometry, demand and the 2 signal orders; vary only window timing.

## Grid and analysis
8 seeds × 3 pockets (14m/28m/70m) × 2 B-lane preassignments (0 and 0.5) × 4 window regimes × 2 signal orders = **384 runs**, 192 matched phase-order comparisons and 48 matched `early` vs `late` pairs. The `never` and `always` subsets should reproduce all 192 original primary runs to the original objective and motion counters, without a changed-in-default simulator result.

Primary outcome: sign reversal in Δ=C_left−C_through between the `early` and `late` opportunity schedules at p=60 terminal penalty, reporting all 48 matched cells. Secondary: p=0 and 120 sign stability, actual successful lane changes and count of conditions where early/late are observationally identical in total bypass count. **Zero case exclusions.** Do not move this gate after seeing results.

## Constraints and interpretation
- This model has spatial target/front/rear cell clearance but **not** a speed- or acceleration-based safe-gap acceptance model; do not label all windows safe real-world gaps. An open window is an exogenous research gate for a *potentially admissible* lateral movement.
- Both worlds start at an identical empty state at t=0 and use the same arrival stream. However their trajectories can diverge before the first signal commitment and do **not** satisfy the 84-tick same-prefix equivalence claim. This is a timing sensitivity experiment, not yet a prospective causal sensor experiment.
- Preserve the 70m pocket/70m change-zone degenerate stratum. Its zero bypass should remain explained by geometry, not driver behavior. A separate, explicitly exploratory >70m zone screen may be performed afterward.
- If **no** early/late phase reversal appears, do not shift windows to search for a post-hoc witness; conclude that the larger static switch result does not transfer to this timed schedule. If reversals exist, inspect actual A→B events and two full phase cost terms, and do not claim field causality.
- K047 18:00–18:30 UTC remains sealed. No K047 HTML recreation.

## Failure modes
Tick windows must be ordered, nonnegative, in horizon, half-open and nonoverlapping; invalid windows should reject before simulation state mutation. The default tuple must exactly reproduce all PHYS-01 numerical outputs. The v2.2 one-dimension-per-tick invariant and vehicle conservation are non-negotiable gates.

Use prior work constructively: Hidas (2005) motivates distinguishing window availability from accepted movement, Huang et al. (2025) motivates separating the structural traffic allocation rule from timing decisions, and Long et al. (2026) motivates stating exactly which future information a decision could actually possess.
