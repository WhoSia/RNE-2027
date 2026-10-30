# T2 v0.5 — audited factorial experiment & numerical-method sensitivity
Date: 2026-10-30. Status: **RUN locally; reproducibility tests PASSED; field validity NOT ESTABLISHED**.
Branch: `research/t2-spatial-fig2-v02`. PR #1 remains draft. Do not merge without review.
All commits are manual. No GitHub Actions are required.

## Source and exact commands

From the repository root (Python >=3.10, standard library only):

```bash
python -m unittest discover -s research/t2 -p "test_spatial_v05.py" -v
python research/t2/experiment_v05.py
python research/t2/update_sensitivity_v05.py
```

The first experiment regenerates `research/t2/results/paired_runs.csv`
(80 rows) and `research/t2/results/summary.json`; the second generates
`update_sensitivity_runs.csv` (160 rows) and `update_sensitivity_summary.json`.
The generated data files are **not** committed because they are regenerable;
the output digests below are an exact local-run seal.

| Result | SHA-256 of locally generated file |
| --- | --- |
| paired_runs.csv | `1fcc7ebf1b6f3c5e785d3c69fb461a898431791f6f891d95b06ff819529cab73` |
| summary.json | `ad4e791e5014d714e46cd46ba38a92ad403a6e76c9b35ca7b0dc711ea73c6603` |
| update_sensitivity_runs.csv | `46a392dd5498e82441b82b878958b22ffe28ee4f26ce4cd204aed7e9e018b1e5` |
| update_sensitivity_summary.json | `5c162d59616d329e2948a6756c05a074061ea2d24e1480023331ebd761a9f884` |

A preliminary 6-test suite passed locally; the extended 7-test suite
including parallel auditing also passed locally. GitHub does not run CI.

## Model and design

Each cell is 25 ft and each time step is 1 s.
Approach length 2000 ft; duration 4200 s; cycle 150 s;
through green 60 s and protected left green 54 s.
Demand 3000 veh/h, left fraction 0.4, outer-lane straight fraction 0.55.
Arrival timestamps are deterministically spaced by integer arithmetic;
turning and lane assignments use the documented Python RNG seed
0..9; **arrivals are not a Poisson process**.
Paired runs reuse the identical time-stamped arrival stream in all four
counterfactuals for each seed and signal mode.

Fixed factors:
- `fork_cells=-21` versus `-13`, measured from stop line: the physical
  bay has 10 or 6 packed vehicle slots with gap=1 cell.
- `bay_limit=2` versus `4`: a **virtual admission constraint** in an
  unchanged geometric pocket. Both limits fit within each geometry.
- `signal_mode=leading` versus `lagging`: nonoverlapping protected
  greens, in contrast to the historical overlapping v0.3 default.
- `update_mode=sequential` versus `parallel`: sequential front-to-back
  sweep uses updated leader position; synchronous parallel uses the
  prior time-step leader position.

**Important identification boundary:** changing physical fork position
necessarily changes travel distance and queue formation, while changing
K is an abstract gate, not an independently constructible real-world
storage expansion. Thus the 2x2 difference-in-differences tests a toy
transition system, not a physically identified civil-engineering effect.

For each signal, seed, update rule:
`I=[Q(-13,K4)-Q(-13,K2)]-[Q(-21,K4)-Q(-21,K2)]`.

## Results: original sequential update (80 audited simulations)

Mean exited vehicles, seeds 0..9:

| Signal | f=-21,K2 | f=-21,K4 | f=-13,K2 | f=-13,K4 | Mean I |
| --- | ---: | ---: | ---: | ---: | ---: |
| Leading left | 1356.8 | 1707.3 | 1417.8 | 1558.5 | **-209.8** |
| Lagging left | 1346.2 | 1701.4 | 1414.2 | 1551.1 | **-218.3** |

At K2, moving the fork from -21 to -13 increased exits by
61.0 (leading) / 68.0 (lagging). At K4, the same fork movement
decreased exits by 148.8 / 150.3, respectively.
**The sign reversal of the fork effect is observed in all ten tested
seeds for both protected signal orders.** This is an observed
ordinal interaction within the simulator, not a theorem for roads.

## Results: update-rule sensitivity (160 audited simulations)

| Update rule | Leading mean I | Lagging mean I |
| --- | ---: | ---: |
| Sequential | -209.8 | -218.3 |
| Parallel | -154.4 | -157.6 |

All 10 per-seed interactions were negative for each of the four
(signal, update-rule) combinations. Nevertheless, effect magnitudes
changed substantially. In one seed-0 condition, leading/f=-21/K4
changed from 1696 exits (sequential) to 1603 (parallel), delta -93.
We have **not** proven sign robustness for other demands, discretizations,
time steps, geometry, headway laws, or independent simulators.

## Constructive order-of-arrival witness

For a single 150-s leading-phase horizon, 120 arrivals at identical
timestamps t=0..119, all assigned to upstream, exactly 60 L and 60 S:
- A = `L*60 + S*60`: 7 exits (7 L, 0 S).
- B = `(L,S)*60`: 18 exits (7 L, 11 S).

Same timing and movement totals, different order => different **finite
horizon** throughput. This is a concrete counterexample to sufficiency
of demand totals for THIS transition system, not a counterexample to any
published general theorem.

## Demand screen (not full factorial, seed=0; 1800-s horizon)

Leading phase, `demand_vph=600`: Q=285 in all four K/f cells, I=0.
Leading phase, `demand_vph=900`: I=-42.
Leading phase, `demand_vph=1200`: I=-98.
Lagging phase, `demand_vph=600`: I=+2.
Lagging phase, `demand_vph=1200`: I=-75.
This shows **no universal sign** is established across demand levels.
Low-demand finite-horizon arrivals not exiting are partly due to travel
time to stopline rather than congestion. Investigate long-run/warm-up
metrics before declaring a capacity phenomenon.

## Validation and literature boundaries

- All tested steps assert unique ownership of vehicle IDs, nonnegative
  coordinate motion, physical spacing in each lane, correct exits,
  route-correct transfer, and count conservation including waiting
  vehicles. These are implementation **invariants under tested inputs**,
  not empirical behavioral validity.
- Sequential front-to-back movement is not the parallel four-step
  Nagel–Schreckenberg (1992) update.
- Reconcile early v0.3's simultaneous L and S greens with actual
  protected phase timing; v0.3 throughput figures cannot be directly
  contrasted against v0.5 without matching the signal plan.
- Osei-Asamoah et al. (2010) identify cycle-to-cycle queue dependence;
  Wei et al. (2021) restrict their analytical results to undersaturation.
  A valid next test should explicitly retain queues and scan stable
  undersaturation regimes.
- SUMO official documentation lists Krauss as default car-following
  model and LC2013 as default lane-change model. Model changes can be
  parameterized; compare against SUMO only after matching geometry,
  signal plan, vehicle lengths and detector definitions.
  https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html

## Next falsification gates

1. Construct **spatially synchronous** occupancy update using old
   positions and compare collision/throughput to the parallel mode here.
2. Change discretization (cell=5 m vs 25 ft), step 0.5 s and realistic
   headway distribution; check whether I maintains sign.
3. Compare identical demand permutations under other phase plans.
4. Independent implementation in SUMO and matched approach geometry;
   log per-lane stopline counts and queue profiles, not merely totals.
5. Field-site candidate in Changwon/Gyeongnam: verify geometry, signal
   head sequences and anonymized aggregate counts; no field claims yet.

## Explicit 3-second clearance (additional 160 audited simulations)

The earlier independent phase module `signal_phases_v05.py` has now been
reused by `spatial_v05.py` when `clearance_s=3`. This is a SECOND
factorial test, not an undocumented change to the original results.
Default remains `clearance_s=0`, preserving the numerical output digests
in the first sections. New command:

```bash
python research/t2/clearance_sensitivity_v05.py
```

| 3-s clearance | Leading mean I | Lagging mean I |
| --- | ---: | ---: |
| Sequential | -209.8 | -218.3 |
| Parallel | -154.4 | -157.6 |

All 40 per-seed interactions (2 update modes × 2 signal orders × 10 seeds)
are **identical** to their zero-clearance counterparts. Comparing
all 160 individual exit counts, clearance changes the 0-s values by:
0 vehicles in 96 cells, +1 in 32 cells, +2 in 32 cells. For any one
seed and signal order, the clearance-induced shift is the SAME across
all four fork/K cells and hence cancels in the interaction. This is a
specific invariant of the tested conditions, NOT a general law of
phase clearance effects or validation of the phase schedule.

Regenerated `clearance3_runs.csv` SHA256:
`274433cc2d4c6729ef345d06ebb372b00e3ca615af6780416b69c29f38fca988`.
Regenerated `clearance3_summary.json` SHA256:
`6ee737d465d2fa32b7d588fdf40af907d5686000273c18cd8491281881d5ec45`.

The 3-second clearance introduces a genuine phase gap between protected
left and through. A full movement-level validation is still needed:
amber/all-red timings and conflict rules are intersection-specific, and
the present simulator omits pedestrians and opposing movements.
