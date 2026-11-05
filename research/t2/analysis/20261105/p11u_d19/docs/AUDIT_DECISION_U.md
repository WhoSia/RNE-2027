# T2 P11-U / D19 — Evidence audit and counterfactual queue attribution

**2026-11-05 · R&E 2027 · research only · P12 optimization frozen.**

## Precisely scoped verified changes

1. Re-read the D18 Python CTM source (`src/cell_link_model.py`) and experimental runner. Re-ran **10/10 D18 tests** unchanged.
2. Removed one dead `if False` branch, unused imports, and a permissive JSON round-trip from a *copied* D18 experiment runner. Its generated `results/case_results.json` is **structurally identical** to the D18 version under Python `json.loads` comparison; the two files also have identical size, 131,542 bytes. This is a **refactor only**, not improved physical accuracy.
3. Identified that `first_source_blocked_end_s` in D18 means **first positive unadmitted external demand**, not necessarily **first downstream-caused spillback**. With the downstream gate fully open but arrivals set to 1.5 vehicle-equivalents/s versus 1 vehicle-equivalent/s saturation, the D18 source queue is positive from 1 second onward. Therefore interpreting that field universally as first spatial spillback is false.
4. Built independent `src/paired_backpressure.py`, which compares each tested closure run to the *same model with the downstream gate always open*, and reports both first any queue and first **excess** queue as separate metrics. The paired conservation identity was checked to numerical tolerance.
5. New D19 unit tests: **8/8 passed** across alternative inflows, time-step refinement, negative and non-finite tolerances, and immutable input. Existing D18 tests are separate, not silently counted as a combined test suite.

## Numerical witness — vehicle equivalents, synthetic CTM

| Demand (veh-equivalent/s) | Gate closed until (s) | First any source queue (s) | First closure-attributable excess queue (s) | Max closure-attributable excess (vehicle-equiv) |
|---|---:|---:|---:|---:|
| 0.5 | 12 | 11 | 11 | 2.3121811 |
| 1.5 | 0 | 1 | none | 0 |
| 1.5 | 12 | 1 | 9 | 3.2945028 |

For the default scenario with 0.5 arrivals and 12s closure, the open-gate reference never queues, so the two definitions coincide. But they are **not equivalent in general**, as the higher-demand counterexample proves. The paired result is model-counterfactual attribution, not a claim of field causal identification.

## More stringent terminology

- **Unadmitted source queue:** incoming demand that could not enter cell U, regardless of cause.
- **Extra source queue from gate closure (model counterfactual):** the difference between the closed-gate and open-gate models with all other inputs fixed.
- **Spatial spillback:** a physically specified downstream restriction propagates back through finite-capacity cells to restrict a spatial upstream movement. This requires tracing the actual mechanism, not just testing a nonzero external queue.
- **Individual vehicle queue:** not measured here; the CTM state is a continuous vehicle-equivalent amount.

## Code audit & known limits

- No Ponytail or custom MCP-Hub audit tool was exposed for execution in this conversation. Plugin Directory search for these exact names found no connected matching execution plugin. This is an **independent Python source audit**, not a Ponytail invocation.
- No architecture-breaking modifications were made to legacy T2 code, no GitHub Actions, no `github-actions[bot]`.
- `src/cell_link_model.py` was preserved unchanged in the D19 reproducibility package. Its `infinite_storage_baseline=True` is an **unphysical counterfactual** that must never be mistaken for a matched second real-road model.
- D18 / D19 time-step sensitivity remains; no theorem of convergence to a continuum traffic flow model is established.
- `run_audit.py` produces an offline HTML visualization, CSV, JSON and a static PNG; visualization labels explicitly say vehicle-equivalents and synthetic results.
- Prior Jinju / NGSIM / inD / SUMO independent traffic validation remains **HOLD**; original P10 engine replay also **HOLD**.
- **P12 signal-policy optimization remains FROZEN.** Abstract policy ideas only.

## Next gate

1. Audit temporal semantics and conditional conflicts in the earlier P11-S discrete event lane model, not just D18.
2. Reproduce the original P10 vehicle/clock counterexample on the actual sealed T2 engine, then integrate one validated physical invariant at a time.
3. Build same-condition three-link SUMO experiment with verified executable/version and linked demand/signal timing.
4. Treat Jinju traffic count as detector passage, not queue length; acquire queue length observations separately.
5. Design an independent split by **site/day/recording**, not repeated frames or derived blocks.

## Competition publication status

The exhibition-specific title and results remain tentative. Research code publication/contest overlap should be checked against exhibition organizers before definitive submission; no unpublished exhibit-specific measurements are presented as tested here.
