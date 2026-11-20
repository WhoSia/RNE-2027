# SF-01 validation receipt · 2026-11-21

Status: **LOCAL EXECUTION VERIFIED**, **REMOTE BYTE AUDIT ON SOURCE**, **PHYSICAL 192 RUNS UNEXECUTED**.

## Source behavior (not a browser demonstration)

```sh
cd research/t2/efficiency_loop
python -m unittest -v test_regret_sensor_policy test_finite_sensor_information test_sensor_fusion_decision test_sensor_cost_policy test_sensor_fusion_frontier test_two_stage_queue_estimator
python sensor_fusion_decision.py ../analysis/20261121/sensor-fusion/robust_value_grid.json
python sensor_fusion_frontier.py ../analysis/20261121/sensor-fusion/sensor_frontier.json

cd ../
python -m unittest -v test_physical_transfer_screen
# DO NOT present this design test as 192 actual simulator executions.
# A separate execution of physical_transfer_screen.py is needed.
```

Local Python 3.13.5, SciPy 1.17.0: **43/43 tests passed** across seven units (including the two earlier finite-world calculation suites); `py_compile` passed for all five new executable modules. Running the two CLI generators produced parseable JSON in local scratch storage. Local generator output SHA-256 values:
- baseline robust grid: `3c02801135d250a0efc6ef5a27f1eab5b36ef9b89483e7fc931efd3951409878`
- sensor/frontier cost and timing: `e98c702e3ed01a81c968e7174163e3a7007f3dc9f0f29caf4976cc3f5a7b7270`.

The two GitHub JSON files intentionally preserve the same numerical contents in a shared version-control format. These local SHA-256 values refer specifically to the locally generated serialization; no claim of exact remote-output byte equality is made until regenerated and compared from a clean HEAD checkout.

## Hard test boundaries
- `test_physical_transfer_screen` uses a fully deterministic *fake simulator* to verify that all 192 planned condition keys, pairing, conservation and sign-reversal summarization work. It does **not** execute the canonical physical simulator, and is not an independent physics validation.
- `two_stage_queue_estimator.py` is an illustrative Kalman-style scalar adaptation to eight synthetic cycles. It does not reproduce published performance, estimate real penetration rates, or provide live signal control.
- Future-arrival reports are hypothetical **forecast messages**, never observed outcomes. Report provenance and latency are explicitly checked but cannot prove that a separate external prediction pipeline is leakage-free.
- The reported 2.897% error-bound transition is a **numerical** boundary for this 16-world, conditionally independent, uniformly confused reporter. It is not a universal sensor specification.
- No K047-review.html is used, and 18:00–18:30 UTC K047 remains sealed.

## Verification of GitHub edits
The new source files were mirrored to GitHub with coherent stage-by-stage commits. Nine checked source files had identical Git blob SHA-1 values to the locally executed copies; the remaining frontier script is adjusted in this commit to match the one blank-line difference, not to alter logic. No GitHub Actions or bot-author commit was used.

## Next gate: actual source-level physics check

Execute `research/t2/physical_transfer_screen.py` against `dual_lane_v11.py`, `spatial_v10.py`, `receiving_cells_v15.py`. Generate and preserve all 192 complete run rows and 96 matched phase-order differences, then independently run `test_physical_invariants_v22.py`. Any discrepancy in geometry, vehicle ID conservation, pre-decision state or terminal objective blocks claims that the information-value counterexample has survived physically permissible lane changes.
