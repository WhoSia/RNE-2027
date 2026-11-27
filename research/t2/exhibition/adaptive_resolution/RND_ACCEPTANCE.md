# Adaptive Resolution Lab — software R&D acceptance, 2026-11-27

Status: executable offline laboratory prototype. Not a calibrated traffic simulator or real signal controller. The former exhibition and RF tracks are preserved. The H08H witness and T181 certificates motivated engineering, but no generic mathematical or algorithmic novelty is asserted.

## Implemented and checked

- Replaceable physical model, free-count erasure, stochastic service, exact finite posterior, paid head/full observation, stage schedule, hard pathwise integer-credit budget, and exact/rolling belief planning. Pocket counts remain exact and paid observations noiseless. FIFO and one binary arrival per stage remain deliberately simplified. Initial class known; only 4 stages in the prototype acceptance suite.
- Pure observation-only decision session: ordered request, reserve credits, optional measurement, decision, next observation. Unsupported/out-of-order observations cause terminal abstention; no subsequent action. No authenticated sensors, wall-clock freshness, recovery after mismatch, or live actuation.
- 32 witness contexts (2 erasure laws x 2 service laws x 2 schedules x 4 budgets), 192 policy evaluations (free, head-if, full-if, QMDP, depth2, exact). All pathwise budgets respected; depth2 exact and zero certificate gap in all 32. H08H first-only q=(2,2), S3L1: optimum 289/16, QMDP 1169/64, excess13/64, exactly reproduced. Exhaustive event-tree evaluator independently traverses 64 ideal or 8192 broad paths per depth and matches dynamic-policy evaluation for 3 depths each, but shares the model and planner, not a separately implemented solver.
- 24 model mismatch conditions (3 nominal x 4 actual laws x 2 depths), exact path mass. Fixed/no-erasure model under true service fluctuations aborts7/8, under true service fluctuations plus erasure1/4 aborts485/512. Erasure-only mismatch aborts37/64. Broad nominal model covers all 4 tested true laws with zero abort and zero observed excess cost on the witness. This is not arbitrary mismatch robustness. Aborted conditional costs are not used as unconditional policy comparisons.
- Eager anytime selection: 128 cap/epsilon/context combinations; at full cap, all 32 exact certificates found by depth2; epsilon1/64 certifies 8 at depth1, 24 at depth2. At cap1 and epsilon0 none of those witness cases certified. Never claim a capped result exact. Lazy incumbent-first selector: if the new lower bound already certifies a previously evaluated feasible upper bound, skip new policy evaluation. Same upper costs in all 128 comparisons; 48 evaluations skipped. The returned policy depth can differ from the explored lower-bound depth.
- 23 Python unit/integration tests pass, 232 Chromium DOM/interaction checks pass at desktop/mobile viewports. Initial local file navigation was blocked; exact generated HTML was loaded via set_content for tests. Initial mobile overflow corrected. Offline HTML is a viewer/replay using frozen evaluated cases, not an interactive fresh solver. The Python API is executable separately. No whole-repository regression or field trial.

## Cold timing and stronger acceptance

Seven randomized fresh-model runs per case and method, median wall-clock milliseconds, includes lower/upper work, fully observed tail and evaluation, excludes process startup and UI. Local Python only; no deployment speed guarantee.

| Case | Eager automatic | Lazy automatic | Exact |
|---|---:|---:|---:|
| ideal first-only | 9.593 | 9.829 | 11.308 |
| broad all stages | 187.033 | 91.538 | 265.629 |
| broad zero budget | 107.054 | 67.328 | 111.224 |

Lazy is slightly slower in first case. Broad all-stages is about 51.1% faster than eager, 65.5% faster than exact on this local timing. Do not cherry-pick it as a universal speed result.

Population acceptance: frozen 4 contexts, 27 classes each, 126 initial worlds each; length4 mixed queue only, all nine pocket occupations, three count pairs, uniform world prior. 108 class-contexts/504 world-contexts, 7 policies each, all exact lazy certificates (94 at lower-bound depth1, 14 at depth2), no depth2 regret, two QMDP positive-regret classes. Native rerun byte-identical. Strong classwise baseline chooses cheapest free/head-if/full-if policy for each known initial class using the exact model. Same hard budget4 for every policy, not equal realized expenditure. This is not an independently estimated classifier or a field sample.

| Law/schedule | Gain vs best global fixed | Gain vs classwise fixed | Positive classwise gain classes |
|---|---:|---:|---:|
| ideal first only | 0.219461% | 0% | 0/27 |
| ideal all | 0.179664% | 0.003636% | 1/27 |
| broad first only | 0.053074% | 0% | 0/27 |
| broad all | 0.073529% | 0.015655% | 6/27 |

The strong-baseline result is a **negative R&D gate for large traffic-cost improvement claims**. In these conditions adaptive policies mostly save information relative to over-observing fixed policies, and model-based certificates characterize decision sufficiency. Do not make a large cost-improvement headline. The next discriminating work must test independently observed conditions and multiple relevant objectives, not merely extend horizon or optimize the same rare witness. We need genuine independent physical model comparison, estimated sensing likelihood and temporal availability, student reproduction and teacher-approved tabletop paired trials. No K047, public-road actuation, RF collection, SUMO or whole-repo regression. No new Claude reply confirmed.

Source: `results.json`, `event_audit.json`, `mismatch_results.json`, `auto_results.json`, `lazy_results.json`, `population_results.json`, `tests.txt`, `browser_receipt.json`. Preserve the original prototype manifest and an expanded release manifest. Do not use a large generated HTML blob in Git.
