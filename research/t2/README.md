# T2 — Spatial Traffic Dynamics
Current research: finite lane/pocket geometry, receiving-link behavior, observation cost and policy regret. **Synthetic, uncalibrated; not a real controller.**
## Current entry points
- [2026-11-28 index and current decision](analysis/20261128/README.md).
- [Dual-lane cellular engine](dual_lane_v11.py), [spatial configuration and phase](spatial_v10.py), [receiving link](receiving_cells_v15.py), [split receiver](split_receiver_v1.py).
- [Dual-lane model contract](README_SPATIAL_V11.md); [efficiency experiments](efficiency_loop/README.md).
- [Adaptive Resolution Lab](exhibition/adaptive_resolution/README.md), [RF-CURTAIN](exhibition/rf_curtain/README.md), [receiver observation lab](analysis/20261128/receiver_observation_lab.html).
## Scope and reproduction
Run specific source-pinned tests/runners from the relevant experiment receipt. For core regression use `python -m unittest discover -s research/t2 -p 'test_*.py'` only in an appropriate full checkout; the whole suite has not been validated in this session.
The initial v0.2 model and its counterintuitive 100ft vs 500ft result are historical calibration failures, not evidence of physical performance: [original README at pinned commit](https://github.com/WhoSia/RNE-2027/blob/8f8ae127f5a31d87578427f4008795aefa95f804/research/t2/README.md). Keep old paths unchanged until dependency audit and regression. Main only; no routine feature branches or Actions.
