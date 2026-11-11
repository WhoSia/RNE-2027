# D46-E — 2026-11-11 independent event-time fluid reference

**Decision: SYNTHETIC ZERO-TRAVEL REFERENCE PASS; POSITIVE TRAVEL TIME / FIELD / POLICY HOLD.**

## Scientific objective
D46-D's beginning-of-tick update produced different sink discharges when upstream buffer and time step change. To distinguish finite-storage effects from time-grid/event-order artifacts, implement an **independent event-time continuous fluid comparator**. This is **not the same physical model**: D46-E permits zero internal travel time and same-instant throughflow across zero-occupancy links, whereas D46-D has a deliberate one-step availability delay.

## Event algorithm
With outside backlog B, finite upstream U<=Ku, finite downstream N<=Kd and piecewise-constant exogenous arrival rate λ, choose admissible boundary rates (a=admit, f=transfer, o=discharge) via three sequential linear programs maximizing o, then f, then a subject to physical capacities and stock-boundary viability:
- B=0 requires a<=λ.
- U=0 requires f<=a; U=Ku requires a<=f.
- N=0 requires o<=f; N=Kd requires f<=o.
- Rates nonnegative and bounded by prescribed gate/transfer/sink capacities.
- Interior dynamics dB/dt=λ-a, dU/dt=a-f, dN/dt=f-o.
Advance exactly to the first stock hitting zero/full or an exogenous rate-change time. Preserve cumulative identity demand - discharge = B+U+N.

This is a *synthetic, zero-travel-time piecewise-linear network-flow reference* without acceleration, lane geometry, intersection signal phase, vehicle length, or microscopic trajectories. No claims of complete Tampère (2011) or Newell (1993) reconstruction.

## Executed frozen test and comparison
Schedule: 40 time units, λ=3 during [0,25), zero afterward; gate/transfer ceilings 4; sink ceiling 0 during [0,10), 1 during [10,30), 4 during [30,40). Total desired arrivals = 75, sink service integral bound = 0*10+1*20+4*10=60; downstream buffer Kd=6.

|Ku|D46-D h=1 discharge|D46-D h=.25 discharge|Event-time zero-travel discharge|
|---:|---:|---:|---:|
|1|19|45|60|
|2|34|60|60|
|3|38|60|60|
|6|50|60|60|
|8|50|60|60|
|12|50|60|60|

For Ku=1, smaller h=.125 is needed to produce 60. Additional h=.5,.125,.0625,.03125 tested, **36 combinations** (six Ku x six h). Each model conserves its cumulative fluid vehicles; the reference reaches the schedule's theoretical sink service upper bound for each Ku. This does **not** prove 60 physically attainable with positive travel times.

Test log: new solver 20/20, comparison 7/7, frozen D46-D/prior D46 60/60, frozen D46-C 19/19 = **106/106 current-turn tests passed**. Fail-closed for invalid states, nonfinite input, mismatched schedules, zero/full boundary feasibility, and rate ceilings.

## Evidence/provenance
Verified reproducibility ZIP (full newly executed Python sources, frozen D46-D/D46-C scripts, tests, 36-case CSV+JSON, runtime versions and SHA256 manifest):
https://drive.google.com/file/d/1HfypuhXMx-1obNE7g5jZqB5UOK37Jycu/view
SHA256 `65c74a603323d67dcecca3151bf61d6b4a1608cee73c17e93d08a0647bdea4a7`.
Daily scientific reasoning document:
https://docs.google.com/document/d/1ZZPfPZXyHazuLiSqOowHQfSRecseZtzSY1gn1EEOhqc/edit

Exact runnable sources are in the SHA-verified Drive ZIP. This Markdown is the GitHub scientific decision record, not a claim the D46-E .py files were separately committed.

## Next gate
1. Construct independent event-time **positive travel-delay** link model, with no same-time time-travel, and compare matched conditions.
2. D44 braking viability, D42 lane-specific entry and exit with censoring; real downstream receiving space not independently observed yet.
3. Run actual SUMO binary matched on geometry/schedules before policy ranks.
