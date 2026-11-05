# T2 v6.10-N / P11-N / D12 — 3D lane geometry and real MARWIS observations

2026-11-05 · Research-only, P12 policy development frozen.

## Reproduction

`python -m unittest discover -s tests -q` (211 tests on this snapshot).
`cd reference/P2_original/T2_v69_P2 && python -m unittest test_corridor test_optimizer test_coordinate test_robust -q` (28 separate tests).

New `lane_3d_differential.py`: five-point derivative geometry for curvature and torsion of source-declared OpenDRIVE lane-center approximations. Explicitly refuses source knots and unresolvable lane/section geometry. The finite-difference convergence diagnostic is not an error certificate and no safe-speed calculation exists.

New `marwis_frame_audit.py`: parses real-source frame CSVs *if obtained*, distinguishes rows from consecutive constant sensor blocks; tests use transparent SYNTHETIC CSV fixtures. Actual raw GitHub CSV bytes were inspected via GitHub connector for six upstream files, NOT transferred into this ZIP. Their upstream blob hashes, row counts and derived aggregate evidence are recorded in `data/michigan_marwis_six_runs_derived.json`. The expanded full audit including timestamps and weather is in GitHub at `research/t2/analysis/20261105/v610n_p11n_d12/data/michigan_marwis_six_trajectories_derived_audit.json`.

Unresolved: real ground-truth friction, independent device frequency, physical/causal asphalt-versus-concrete attribution, DTU original CSV bytes, FHWA field records, field OpenDRIVE, SUMO simulation. Do not interpret instrument optical estimates as actual road grip or speed guidance. Policy frozen.
