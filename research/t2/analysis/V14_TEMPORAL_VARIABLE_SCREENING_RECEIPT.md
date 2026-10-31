# T2 v1.4 — temporal coordination, screening and world-contact receipt

2026-10-31. WhoSia/RNE-2027 branch research/t2-spatial-fig2-v02.
**NO GitHub Actions, no workflow changes, no main merge.**

## Executed local work (NOT yet byte-identical GitHub checkout)
v1.3 historical artifact unzipped locally. Prior 44 tests passed.
- Added integer signal_offset_s (default 0) to the signal scheduler.
- Implemented ArrivalProfile with complete-period budgets, time-varying
  arrival rates and turn shares, and modulo-period upstream platoon offsets.
  Rotating an arrival schedule preserves number and route composition.
- 576 matched-synthetic runs: 2 demand histories x 2 turning histories x
  2 arrival offsets x 3 signal offsets x 4 pocket lengths x 6 seeds.
  Same second/route arrival list reused across pocket and signal policies.
- 162 synthetic 9-lever one-factor screens: 3 levels x 6 seeds each.
- Per-seed pocket x signal-offset difference-in-differences (8 strata).
- Vehicle-seconds are tracked separately for external queues,
  internal approach/pocket, and downstream receiver.
- **61/61 local unit tests passed**, including original 44.
- Total newly run: **738 simulation cells**. All outputs synthetic and
  field-uncalibrated. GitHub exact HEAD did not run in the container.

## Results and scope
Baseline geometry: two 140m through lanes, 7m cells, 28m pocket,
B-lane share 50%, protected L/S greens 35s/50s, cycle 120s,
receiver capacity 2 vehicles, receiver discharge headway 4s,
720-second horizon, six seeded route draws.
Representative demand rate 1,500 veh/h, left share 30%.
- Steady demand, platoon offset 0, signal offset 0, 28m pocket:
  mean downstream (S,L) completions=(86.833,42.333).
- Exactly matched demand but platoon offset 30, signal offset 40:
  (S,L)=(73.667,42.000). Not a measured signal coordination effect.
- OAT total-completion ranges under preselected levels:
  receiver headway (2,4,8s): 138; through green (40,50,60s): 32.833;
  receiver slots (1,2,4): 19.0; pocket (14,28,70m): 18.667;
  B share (.2,.5,.8): 13.667; left green (25,35,45s): 11.167;
  signal offset (0,20,40s): 2.5; permitted change zone (35,70,110m):
  0.667; model stopline headway (1,2,3s): 0.333.
  These ranges are NOT normalized and cannot establish universal rank.
- Under steady arrival volume and turn share, platoon offset 0:
  pocket length effect (70-14m) on total network completions changes
  from +19 (signal phase offset 0) to +22 (phase offset 40).
  Matched finite-difference interaction = +3 vehicles; with a
  time-variable turn share, the corresponding interaction is +5.333.
  Some other demand/arrival strata yield negative interactions.

## Main engineering interpretation
The downstream exit headway is dominant in this selected *severely
receiver-limited* synthetic configuration. This is **not** a finding
that downstream headway always dominates pocket length in real roads.
Green timing, upstream platoon phase, turning share history and pocket
storage interact. A short pocket might not be the principal bottleneck.

## World-contact gates
Important unmodeled or undervalidated factors: observed lane geometry,
actual signal plans including pedestrian/overlapping phases, car-following
velocity distributions, heavy vehicles and standing pitch, bus stops,
lane-changing reachability and safety, downstream signal offsets and
receiving densities, cycle-specific turn ratios, upstream platoon
arrival timestamps, weather. Do not add all as independent controls
without data; rank by expected model impact and measurement feasibility.

Local archive T2_v14_temporal_engineering_bundle.zip contains sources,
tests, CSVs, JSON summaries, charts, and per-file SHA256 manifest.
Archive SHA256:
0c6b358f1ca2ee98b54043fe776375e07831de89e58d399d993e20c2649807a7

## Code and reproducibility
arrival_design_v14.py, temporal_factorial_v14.py, screen_v14.py,
interaction_v14.py, plot_temporal_v14.py, and matching regression tests.
The original local execution source and the GitHub connector-written
files have NOT been proven byte identical. Exact GitHub checkout
execution remains pending. GitHub Actions shall not be used.

## Final v1.4 local extension (supersedes provisional counts above)
Additional robust_policy_v14.py and test_robust_policy_v14.py:
12 paired (bay length, signal phase offset) policies aggregated over eight
predeclared synthetic arrival/turn contexts; report context mean, finite
worst-case total, mean through and left completions separately.
In these particular conditions, bay 70m/phase offset 0 has the
largest *minimum total network completion* among the 12 tested policies:
minimum 126.667 vehicles in 720s across eight synthetic contexts;
mean across contexts 131.3125. This is NOT a real-world recommendation.
No land-take costs, signal safety constraints, actual observed traffic
or generalized downstream physical geometry were included.

**Final local test status: 63 PASS (not the earlier 61).**
New simulation calls remain 576+162=738; robust screening is postprocessing,
not additional traffic simulations.
Final bundle now contains **77 files**, and archive SHA256 is
fcbab7ee16368a6f8b5ba69d197fcee80433c1dc7cf87d9486442ed87c381235.
Earlier archive hash and 74-file count above refer to a superseded local
snapshot. The user-visible downloadable bundle is the latest version.
No GitHub Actions or main merge. Exact GitHub checkout source execution
continues to be **unverified**.
