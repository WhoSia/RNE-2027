# T2 v1.2–v1.3 — Shared Downstream World-Contact Audit

Date: 2026-10-31. Repository: WhoSia/RNE-2027.
Branch: research/t2-spatial-fig2-v02.

**Safety of repository:** NO GitHub Actions, no workflows, no push to
main, no automated background execution. Individual GitHub connector
commits were made on the established research branch only.

## Engineering mechanism
In v1.1 the straight B lane is independent of left-turn A and pocket
storage. A finite downstream receiving resource may re-couple them.
Two *optional* mechanisms were implemented, both disabled by default:

- `downstream_conflict_gap_s`: intentionally simple common minimum
  interval between different movement exits (NOT a real merge model).
- `receiver_slots` and `receiver_headway_s`: finite FIFO receiving
  reservoir after the stopline, drained by a headway rule regardless of
  signal color. If full, a stopline discharge is blocked. The simulator
  explicitly distinguishes movement stopline exits from final network
  completions and checks **generated = network completed + all queues
  including downstream receiver** every second.

Both mechanisms are hypothesis-generating approximations. They do not
implement longitudinal car following, physical junction conflict zones,
the friction of actual weaving, downstream signal progression, or a
calibrated receiving-link fundamental diagram.

## Tests actually executed locally
- 26 inherited spatial/site/separation tests
- 5 optional shared-exit tests
- 5 finite receiver conservation/backpressure tests
- 4 downstream site/provenance tests
- 4 movement-specific Pareto integrity tests
= **44 local PASS**; no failed assertions.

`check_checkout_v13.py` executes tests and hashes source files
**offline**. Local run reported 44 PASS but no Git worktree/commit ID,
so it correctly recorded `exact_checkout_tested=false`.
Internet name resolution prevents cloning GitHub in this container.
Neither checkout SHA parity nor GitHub HEAD tests have been claimed.

## Experiments: 1,920 additional synthetic runs
- 768 optional common exit interval combinations:
  3 left-turn shares x 8 matched seeds x 4 downstream intervals
  x 2 B lane allocations x 4 pockets.
- 1,152 finite receiver combinations:
  2 left shares x 8 matched seeds x 4 pockets
  x 3 reservoir capacities x 3 downstream headways x 2 B allocations.

Every comparison reuses the same time-stamped generated arrivals for
each seed; all cases are virtual 720-second horizons. Seeds model
within-simulator variation, **not** observed statistical uncertainty.

### Preselected representative comparison
Left share 30%; B lane allocation 50%; receiver capacity 2 vehicles,
receiver discharge headway 4 seconds; 1,500 veh/h synthetic demand;
8 seeds; 720-second horizon.

| Pocket | S network completed | L network completed | Total network |
|---|---:|---:|---:|
| 14 m | 88.125 | 26.750 | 114.875 |
| 28 m | 86.375 | 41.625 | 128.000 |
| 70 m | 83.125 | 52.250 | 135.375 |

Matched 70 m minus 14 m outcomes:
- S: −5.0 vehicles mean; every seed negative, range −8 to −1.
- L: +25.5 mean; every seed positive, range +19 to +31.
- Total: +20.5 mean; 8/8 positive, range +12 to +26.
- Time receiver full and discharge attempted: +185 seconds mean,
  with paired seed differences +123 to +224 seconds.

This model shows a true tradeoff **inside the specified model**: a
longer pocket increases total movements served by admitting left-turn
vehicles, yet left traffic competes with straight vehicles for a
shared receiving resource. These numbers are **not** real-world
pocket-widening effects.

**Boundary warning:** 0 m pockets forbid left turns in this simulator
and are an extreme falsification control, not a credible live site
intervention. Common gap 40s is also a deliberately extreme stress
parameter, not a recommended discharge headway.

## Decision structure
`pareto_receiver_v13.py` identifies nondominated alternatives using
**final network S and L exits**, grouped only within otherwise
identical traffic/network assumptions. For the representative case,
14, 28 and 70 m are non-dominated; 0 m is dominated.
The existence of multiple Pareto choices indicates that a single
`maximum total exits` objective loses movement-specific information.

## Evidence and next world-contact gates
1. Site provenance schema now distinguishes optional receiver capacity,
   headway and conflict interval; absent fields remain explicit
   synthetic defaults for backward compatibility, never become a
   "field calibrated" claim.
2. Validate the actual receiving-link length, lane count, outlet
   signal/demand, and lane-change reachability at one representative
   intersection from independent sources before making decisions.
3. Replace the virtual receiving reservoir with actual spatial receiving
   cells and calibrated discharge dynamics when real observations
   justify the added complexity.
4. Split real data into separate calibration and withheld validation
   windows. Stopline detectors and downstream exit detectors estimate
   different observables; never conflate them.

## Files
Core: `dual_lane_v11.py`; tests: `test_downstream_v12.py`,
`test_receiver_v13.py`, `test_site_downstream_v13.py`,
`test_pareto_receiver_v13.py`.
Experiments: `downstream_sweep_v12.py`,
`receiver_sweep_v13.py`, `pareto_receiver_v13.py`.
Visuals: `plot_pareto_v13.py`, `make_demo_v13.py`.
Verification: `check_checkout_v13.py`.
All local raw run CSV/summary JSON and the standalone HTML are included
in the supplied artifact bundle; raw results are not claimed to have
been executed directly on GitHub infrastructure.
