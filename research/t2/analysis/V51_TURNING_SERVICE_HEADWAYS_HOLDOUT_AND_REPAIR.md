# T2 v5.1 — Movement delay, spurious policy flips and invariant repair (2026-11-02)

## Results that survive scrutiny
- Existing 26 tests + 11 new tests = **37/37 PASS**.
- Stress exploration: 3 demand conditions × 3 uncalibrated turn service-headway models × 4 seeds × 6 policies = **216 synthetic runs**.
- Predeclared additional seed range 101–148: balanced demand × 2 turn headway models × 2 offset policies = **192 new synthetic runs**.
- Source code: `research/t2/microscopic/v51/`. All 17-file reproduction artifacts, CSVs, summary and SHA manifest: [Google Drive ZIP](https://drive.google.com/file/d/1yUAgtzaJyggd9HuibNEG2XHb42EtOBxk/view). ZIP SHA256: `3aa37ac7efd7820a7121a58564f72649f1fd22f59564fd5a8a4076621faf1aab`.

## Counterexample / correction
A longer side-merge headway exposed a *software invariant violation* at S1 during the main_peak seed11 g38+progression scenario, t≈475.5s. A downstream transfer was rejected after followers had advanced, and force-resetting the leading vehicle to an arbitrary stopline position reduced gap below 4.5+2.0=6.5m. Fixed with transaction-like lane follower reconciliation from pre-tick positions, no negative longitudinal movement; added regression test. Not proof of physical collision avoidance.

## Exploratory optimum flip, then negative replication
In the original **four** discovery seeds, the balanced demand g38 policy favored progression under equal 2s headways and favored zero offset under severe synthetic side_merge=7s and main_exit=5s. **The reversal failed to replicate** under independent synthetic seeds 101–148:
- equal 2s: progression minus zero mean −305.865 veh-s; approximate 95% paired t interval [−400.648, −211.081], progression favored in 39/48 seeds.
- severe turns: mean −150.792 veh-s; interval [−306.369, +4.785], progression favored in 26/48.
- matched interaction: (severe turn effect on progression minus zero) = +155.073 veh-s, interval [+26.605, +283.541].
Thus severe turn delays attenuate the effect of progression in this model; they do not give demonstrated evidence for a reliably opposite best controller. Field calibration not attempted.

In the four-seed exploratory parameter grid, minimax normalized regret selected g38 progression for balanced demand (max regret 0.7003%) rather than g38 zero (2.144%). This ranking is exploratory and should not be interpreted as a statistically certified traffic policy.

## Movement fidelity limits
New legal-successor OD validation and four connection types: main_through, main_exit, side_merge, side_exit; their staged control and movement-specific interdeparture headways are now explicit. This is still a FIFO single-lane-per-incoming-link 3-signal corridor. Although conflict exclusion is enforced via conservative mutually exclusive main/side stages, there is NO geometric turning conflict matrix, protected left-turn bay, lane change model, signal yellow handling, bus stop or pedestrian safety model.

SUMO links are controlled at the **lane-to-lane connection** level (linkIndex), not merely by source lane: [SUMO Traffic Lights](https://eclipse.dev/sumo/docs/Simulation/Traffic_Lights.html); [SUMO Intersection Dynamics](https://sumo.dlr.de/docs/Simulation/Intersections.html). This is a design target, not a SUMO matching test.

## Next scientific gates
1. Construct geometry-aware directed connection graph with conflict/foe matrix and multi-lane turns, in independently reproducible SUMO network.
2. Measure/estimate discharge headways, queue lengths and turning ratios in safe, supervised, non-identifying Gyeongnam intersection observation; no unauthorized modification of actual signals.
3. In a fixed and blinded OD/observation split, test whether these micro headway measurements improve prediction of independent-day *queues and policy regrets*.
4. Report policy rankings as intervals and distinguish model parameter ambiguity, observation indistinguishability and robust policy recommendation.
5. No SUMO executable and no sumolib were available in this execution environment; no independent SUMO verification has been performed.
