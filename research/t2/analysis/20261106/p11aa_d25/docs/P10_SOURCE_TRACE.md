# P10 source lineage — located, not independently replayed

- Original source path: `research/t2/analysis/20261104/v69p10` in `WhoSia/RNE-2027`, branch `research/t2-spatial-fig2-v02`.
- Archive document `01_FIRST_CAUSAL_DIVERGENCE.md` SHA-1 Git blob `ddbeffa75bfa39df844dbeefb1ab62565aee3d1a` reports original P2 scenario `upstream_peak`, 18m, seed 223, signal plan `(24,24,24)`. Clearance ends at last green entry 47.1625s. dt=0.5: vehicle 8 connector entry 47.0s; vehicle 1 receiving-link release 47.50s. dt=0.25: vehicle 8 connector entry 87.25s. This is a source-derived historical result, **not computed this turn**.
- `code/p10_boundary_trace.py` Git blob SHA-1 `65c4fb9b083b900c14cefd7dcc0d4605dfb99e79` imports historical `dt_convergence` and `vehicle_schema`, which must be resolved to original immutable P2 source before a reproducible replay. `tests/test_p10_mechanism.py` blob `4feb3a63b444aec66729074a7cb3dcf347160a09` contains 8 mechanism tests; these were not executed in D25.
- `derived/capacity_time_safe.patch` blob `18a87bfe4f5678c0a23280ea9e1154c26f413052` freezes link occupancy at tick start to avoid spending end-of-tick receipt on tick-start admission; it is a historical candidate fix, not verified here.
- Historical P10 archive Drive URL https://drive.google.com/file/d/11rq7hbnvRaJwKzM6OwQUwTiajCShwipJ/view, archived claim SHA256 `9fa06146b781bcbbd1f5e19dc25b277e1e98c695b13e61fc0b291b58cd53b59c` (not independently validated in D25).

**Before claiming a P10 rerun:** fetch complete original ZIP; verify byte hash and imported P2 modules; preserve unmodified baseline; run original eight traces and eight mechanism tests, then evaluate experimental patch separately. Do not alter historical original files.
