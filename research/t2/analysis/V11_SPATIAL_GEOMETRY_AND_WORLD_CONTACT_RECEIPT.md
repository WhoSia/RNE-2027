# T2 v1.0–v1.1 — Spatial Pocket, Multi-Lane & World-Contact Experiment Receipt
Date: 2026-10-31. Status: **LOCAL EXECUTION COMPLETE / EXACT GITHUB SOURCE EXECUTION NOT VERIFIED / NO FIELD CALIBRATION**.

## Executed engineering increments
1. **spatial_v10.py**: one full through lane and a physically located, finite turn pocket. Every car advances ≤1 7m cell/s; L vehicles must reach and enter the real pocket fork, unlike virtual admission-cap K in v0.5. Two exclusive protected phases plus clearance; conservation, uniqueness and pocket occupancy checked at every time step.
2. **test_spatial_v10.py**: 11 local tests pass (geometry, protected phasing, route correctness, zero-bay negative control, all-through placebo, deterministic arrival pairing, cycle residuals, arrival pattern, trace frames, no teleport, update policies).
3. **factorial_v10.py**: 384 paired synthetic simulations, 2 arrival patterns × 3 L fractions × 8 seeds × 2 protected phase sequences × 4 pocket lengths. At 30% L, uniform arrivals and leading L, through-exit marginal gain (1800s): +100.75 for 14→28m, +66.0 for 28→42m, +48.625 for 42→70m.
4. **update_sensitivity_v10.py**: 768 runs with sequential vs parallel movement. With same conditions and 70m pocket, parallel minus sequential through exits averaged −45.375 over eight seeds; shorter 14m case had 0 difference. A concrete numerical-algorithm-dependent result, not a field phenomenon.
5. **demand_sweep_v10.py**: 384 runs from 300 to 2100 veh/h. At 300 veh/h, 14m and 70m had identical mean 101.875 through exits in 1800s; at 1500 veh/h, these were 151.625 and 367.0, respectively. Hence physical-pocket benefit is conditional on demand and the shared-lane model.
6. **dual_lane_v11.py**: add two full through lanes A/B plus turn pocket, fixed upstream destination-lane assignment and an optional simplistic A→B lateral move permitted only with free adjacent, front and rear cells, only in an upstream change zone. It does NOT implement realistic velocity-dependent gap acceptance.
7. **test_dual_lane_v11.py**: 7 local tests pass (mass conservation, cell occupancy, no-through-left exit, all-through independent lane negative control, deterministic replay, invalid settings, cycle field-telemetry schema).
8. **dual_lane_factorial_v11.py**: 384 paired runs, L ratio .30/.45, B-lane share 0/.5/1, lateral move on/off, four pocket lengths, eight seeds. At 30% L, 14→70m through exits (8-seed means): all S initially A no change 151.625→367.0; A/B 50/50 no change 355.625→505.875; A/B 50/50 with change 439.125→506.625; all S on independent B 369.5→369.5.
9. **separation_court_v11.py**: 150 checked runs (10 seeds × 3 L fractions × 5 pocket lengths). Conditional theorem: if all straight cars are on independent B, all left cars on A, lateral movement disabled and no shared downstream resource, B's state update does not reference pocket geometry; induction implies identical B exit times/counts for fixed S input. Computational checks passed including every cycle's cumulative S exits. This is a model-conditional property, NOT an empirical theorem about actual roads.
10. **site_v11.py + fixtures + run_site_v11.py**: preserve per-input provenance and reject unlabeled non-synthetic geometric/control/demand inputs; never infer field calibration. Six local schema tests and one local site-execution test pass.
11. **Visual deliverables**: two labeled synthetic plots and standalone browser-based lane animation available in local reproducibility bundle.

## Execution totals / hashes
- **25 locally passing unit tests** across v1.0, v1.1, site and site-run suites.
- **1,920 scenario runs** (384+768+384+384), plus **150 conditional-separation runs**.
- Locally executed source SHA256: `spatial_v10.py` = `05cc8215c72cf57054fb7782d9191af2deb32cd391ffe1439ffdb5a082190dfe`; `dual_lane_v11.py` = `33a091460ee1027816f4f79ab31dcaa815627fbeaef37235192e55db5058ea0a`.
- CSV SHA256: v10 factorial `3844932bf0114359e91248e89300979f79b37cef61d27f6f688c807f419ce15d`; v10 update `12426248be257546c61c24369f14ff93e577a6eaf7020e579ba7b974960ce211`; v10 demand `d46a7097a9f51fdebcc7a4619220ce9b05599a633ae3ba3261b617a11180d2ef`; v11 two-lane `84aae059eb6e3ab40591405b8a5d4ff722e936fc7e52932c15b09e972d87bdf6`.
- Separation court JSON SHA256 `ea117cd5eff09bc25b7abc8927ecfdb98c16891f6137cf7802cc58ca34451d72`.
- The local bundle has a per-file SHA256 inventory and complete original CSVs, JSON outputs, plots, HTML demos and test code.

## Major assumptions and boundaries (not optional)
- Vehicle advances one 7m cell/s (25.2 km/h); no calibrated speed distribution, acceleration, reaction delay, vehicle-type mix or headway distribution.
- Only protected L and S phases, 3s clearance. Actual Korean intersection phases may overlap or have additional movements.
- Pocket extension changes fork position and storage simultaneously, so these are **geometric package interventions**, not isolated effects of storage count.
- The B-lane share is an upstream assignment assumption. Lane-change action is deterministic free-cell reallocation, not MOBIL/Hidas forced/cooperative gap acceptance.
- No shared downstream blocking, pedestrian priority, buses, nearby intersection offsets, real field calibration or actual weather/visibility variations.
- The local Python files and GitHub connector-authored source use corresponding logic but have **not** been shown byte-identical. The GitHub HEAD has not been checked out and executed; this is **not** a remote-repository execution seal. The environment had no installed SUMO executable. All outputs are synthetic.

## Practical near-term targets
A) Freeze one real approach geometry and signal phase plan with provenance, while not claiming generality from a single site.
B) Observe anonymous, safely acquired per-cycle movement discharge and queue length, compare to v11 cycles; use different periods for calibration vs validation.
C) Add velocity/gap-acceptance (e.g. source-grounded MOBIL safety and incentive conditions) only if needed to explain measured differences.
D) Make the exhibition model, animated demo and one bounded engineering recommendation with visible source and uncertainty controls.

## Credits and research scope
Based on established traffic modeling ideas: Zhang & Tong (2008), Osei-Asamoah et al. (2010), Liu et al. (2019), Emtenan & Day (2021); lane-change methodological guidance Kesting et al. (2007) MOBIL and Hidas (2005). Implementation and adaptations are T2 educational research, not a claim to have newly invented short-turn-pocket modeling.
