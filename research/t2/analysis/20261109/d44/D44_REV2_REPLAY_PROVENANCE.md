# D44-REV2 — 2026-11-09 sealed-original replay and physical braking audit

## Provenance

Original Drive ZIPs downloaded to the execution container **without editing** and SHA-256 verified:

- D26–D30 original: `60b6d6c5c6cf65044d0c13ee653adf9e75d6c59584fe73458558854dc6dc6a7a` — https://drive.google.com/file/d/1O_-JoZt-ii7vYZq3uy34qISpeDWnlx0Q/view
- D34–D36 original: `0844af4be9f5304a1abba7a13d52a95e193e9622a9f6ea83fdc69fd0a1cdc261` — https://drive.google.com/file/d/1Ppa4h-GZ44v9Her_wEoUW-Oih7Mh34VE/view
- Actual D27 source member `src/micro_world.py`: Git blob SHA-1 `63b571fda723d86e88fd24edd8a5d84334f5e25b`; byte SHA-256 `83c3f3fc5fe8bf6b8418fe7a48ebc6e3f3c09fbe725d94802d7b5120ca58fdde`. The Git blob agrees with the independent GitHub file readback.

## Executed tests, not merely inferred

- Original D25 tests: 28/28 PASS.
- Original D27/D30 tests: 22/22 PASS.
- Original archived P10 mechanism tests: 8/8 PASS, including the previously sealed backdating witness.
- Original D34/D36 tests: 10/10 PASS.
- **New D44 original-engine witness:** eight passing behavior tests and two `expectedFailure` physical invariants, total 10 executed.
- New **independent** constrained-braking reference: 10/10 PASS (not integrated into T2).
- Total executed: 88 tests; 86 pass and two expected failures. These tests come from different code systems and do not establish field validity.

## Reproduced physical counterexample

On one road (12 m), one car (4.5 m), red after initial one-second green, configured acceleration 1.5 m/s² and deceleration limit 0.25 m/s²: unchanged sealed D27 `run` produces tick-end speed 1.5, 3.0, 3.0, 0.0, 0.0 m/s at t=1..5 s; rear position 1.5, 4.5, 7.5, 7.5, 7.5 m. Thus a one-second speed drop of 3.0 m/s exceeds the configured deceleration magnitude by a factor of 12. Changing `decel_mps2` from .25 to 3 leaves trajectories identical in this witness. The original model reports zero collision violations; that is not a proof of physical feasibility.

## Modeling lesson and fix strategy

An engine can be internally overlap-free yet physically inconsistent. The appropriate fix is not to substitute `speed=max(speed_old-b*dt,0)` blindly: it may cross the stopline or hit a leader. Instead design a viability-aware advance that checks boundary stopping distance and forecast signal movement before admitting an accelerated state. The separate trapezoidal kinematic reference enforces finite acceleration and fails closed on an infeasible stopline; it is **not** an integrated or calibrated repair.

## External evidence status

DLR UT v1.3.1 official record: https://zenodo.org/records/20919480 ; the required original archive is `DLR-Urban-Traffic-dataset_v1-3-1.zip` (463.4 MB, publisher MD5 `401da7fbc1739c565c366e86fc116473`). Shared Drive search returned no original archive matching the filename. Container external network DNS did not resolve github.com and Zenodo direct web fetch encountered 429. The requested original DLR bytes have NOT been acquired or SHA-256 verified. SUMO and netconvert binaries are NOT installed locally, and no independent SUMO run occurred.

## Durable artifact

Drive release with source receipts, tests, execution logs, reference prototype and 13 manifest/verification files:
https://drive.google.com/file/d/1V4gaX_dVwFzOQzrA4VlxO4r3j4zm3W4Q/view
SHA-256 `f9f894022a5e492e414c87fe243456352bdbb95a200120dfd95e790e6be1c1d5`.

## Next gate

(1) Obtain and SHA-256 pin original DLR raw ZIP. (2) Derive exact observed head-to-movement and stopline geometry. (3) Independently execute pinned SUMO against matched inputs. (4) Integrate physically feasible braking and time-step refinement into the true D27 source, preserving the sealed original. (5) Reassess policy rankings only after field and numerical gates.

Human action requested: download the official original DLR ZIP and upload it into the verified 20261109 shared Drive `20_DLR_RAW_ACQUISITION` folder: https://drive.google.com/drive/folders/1MgVtPHh8UKMuv0hNhUQLRSmP_oNLN_FX . Do not rename or recompress; record original checksum.
