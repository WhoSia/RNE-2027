# T2-PHYS-01 — Fixed-geometry transfer of the information counterexample (preregistered)
Date: 2026-11-21. Status: PROTOCOL, NOT RUN.

## Decision that follows the 16-world synthetic audit

The 16-world result compared different whole-simulator bypass settings. That uncertainty is artificial if geometry and lane-change rules are known to the controller, and a large value-of-information score is not an engineering finding. **Next, freeze one geometry and vehicle motion law and vary only a physical, time-local maneuver opportunity, without exposing future events to the controller.** If the effect does not survive, report the negative result instead of constructing another K047 HTML demonstration.

## Existing executable starting point

- `research/t2/dual_lane_v11.py`, in particular `DualConfig`, `run`, `changes_A_to_B`, `pocket_block_seconds`, `receiver_denied_seconds`, and exact `service_events`/`access_events` when trace=True.
- `research/t2/test_physical_invariants_v22.py` tests vehicle ID conservation, one-dimension-per-tick displacement, access-denial event lineage and receiver-denial attempts-versus-ticks. This is an existing mesoscopic **cell** simulation, not observed driver behavior.
- `research/t2/spatial_v10.py` supplies `Config`, signal phase and matched arrival sequences.

The spatial model permits A→B for a straight vehicle only in a designated upstream lane-change zone if the adjacent target and neighboring cells are unoccupied and the vehicle was not advanced longitudinally that tick. There is no actual speed-dependent safety-gap acceptance law. The first check must preserve this physical invariant, not relax it.

## Screened matched design, no tuning after observing outcomes

Primary paired grid (all synthetic, no empirical calibration):
- 8 fixed seeds 0–7
- 3 pocket lengths: 14, 28, 70 m
- two through-B assignment shares: 0, 0.5
- A→B lane change allowed or disallowed
- two protected phase orders: leading or lagging
- `Config(duration_s=720,demand_vph=1800,left_fraction=0.5)`; equal upstream arrival stream for each seed
- `DualConfig(change_zone_m=70,receiver_mode="cells",receiver_slots=4)`, all other parameters fixed at recorded defaults.

Total: 8×3×2×2×2 = **192 simulation runs**, paired by seed/pocket length/B share with only phase order and lane-change permission changed. This is a physics sensitivity **screen**, not a randomized physical intervention. No spatial nor temporal detector data comes from the K047 HTML.

Primary output: completed S and L vehicle counts, accumulated upstream/outside/receiving vehicle-seconds, terminal remaining, successful A→B changes, pocket entry denials, and receiver denials by count and distinct time. Compute signed left-first-minus-through-first differences; retain every negative, positive and tie. Do not select only reversal-producing seeds.

### Gates

**G1 — physical invariant:** all v2.2 tests pass; traceable vehicle conservation and 1-cell/1-dimension per tick hold for every sampled run. Fail → repair before interpreting results.

**G2 — same-input comparison:** match actual arrival events, route assignment rule, initial occupancy, phase duration, receiving conditions and simulation horizon. Record that changing lane-change permission alters pre-decision internal microstate if it does; do not call such worlds observationally equivalent merely because aggregate queue counts match.

**G3 — action availability:** from each tick just before a hypothetical commitment, record only states available by then. Existing `frames` represent end-of-tick state; reconstructing earlier state requires explicit semantics for input timing and must not be assumed. For a strict 84-tick counterexample, an added full-state snapshot **before policy intervention** is necessary.

**G4 — mechanistic value:** characterize physically blocked and successful A→B transitions, denied pocket entry and receiver full events. Stop after the fixed screened design unless a new physical parameter is justified. If all phase-order differences have the same sign for physically admissible opportunities, report that the earlier witness was generator-specific.

**G5 — operational claims:** do not suggest changing actual signals or controlling vehicle lane changes. Minimum greens, pedestrians, intergreen clearance and observed acceptance are separate prerequisites for any operational recommendation.

## 4-week delivery priority

Week 1: run matched 192-run physics screen and present every condition, not just the largest improvement. Week 2: add explicit tick-boundary snapshot and select a feasible observation rule before the action. Week 3: exact information partition + forecast error on the resulting finite collection, holding geometry fixed. Week 4: poster and scientific limitations emphasizing what survives vs fails across the three models. If the screen cannot be executed, mark the physics transfer **UNVERIFIED** in the submission rather than fabricating a validation figure.

Prior literature: [Zhang & Tong (2008)](https://doi.org/10.3141/2071-09), [Liu & Chang (2011)](https://www.sciencedirect.com/science/article/pii/S0968090X10000720), [Huang et al. (2025)](https://doi.org/10.1080/21680566.2025.2474656), and the [Long (2026)](https://arxiv.org/abs/2610.06992) preprint already restrict generic novelty claims. The physical experiment must isolate a genuinely narrower mechanism.
