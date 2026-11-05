# T2 P11-V / D20 — Discrete event semantics code audit

2026-11-05 · R&E 2027 · Research branch `research/t2-spatial-fig2-v02` · P12 **FROZEN**.

## Source custody

Read the byte-for-byte P11-S / D17 `lane_fifo.py` contained in previously sealed archive `T2_P11S_D17_20261105.zip`. SHA-256 of source `be12e18f44d80a86b0360b14c8a80b511653fd4e1ae4f564305076dcad4626cc`. Preserve unchanged under `baseline/lane_fifo_S_original.py`; independently patch `src/lane_fifo.py`. No claim of Ponytail execution or untouched P10 original engine replay.

## Reproduced defects

1. **Silent zero-duration occupancy:** `at=1e16 s`, `duration=.25 s` gives `at+duration==at` as IEEE-754 binary64. Former engine logs entry and exit at identical time though declared duration is positive.
2. **Nonfinite event:** `at=1e308`, `duration=1e308` makes exit `Infinity`, not checked by former engine.
3. **Peak waiting metric:** On an uncontended lane with instant admission, old `max_waiting` is 1 because the arrival was counted before grant. New definition measures end-of-event-batch pending vehicles, yielding 0. This is a **measurement definition correction**; for the old metric, retain a different explicit name if needed later.

## Surgical patch

- Guard each new exit timestamp `end=t+d.duration`: require `math.isfinite(end)` and `end>t`. On failure raise `ValueError` instructing clock rescaling or integer-tick time instead of silently modifying a physical parameter.
- Move the `max_waiting` update after the event batch's eligible admissions. No vehicle source/sink, conflict graph, admission order or wait-time accumulation modified.
- A representative normal-event trace is byte-for-byte structurally identical before and after the patch; no all-input equivalence claim.

## Verification

- 8 archived original tests + 8 newly constructed tests pass (16/16) locally.
- 100 deterministic random scenario trials × 32 synthetic requests = 3,200 generated admissions under bounded positive times, checked conservation and finite strictly future exit.
- Independent original-source loading in `run_audit.py` records both old outputs and patched outputs in `results/audit_results.json`.
- Tests are synthetic. Legacy full v6.10-N project and original P10 case NOT replayed. InD/NGSIM/Jinju real data and SUMO matching remain HOLD.

## Known remaining limitations

- Inputs are floating seconds. Rejecting unrepresentable times is a fail-fast guard, not a full numerical time semantics solution. Integer nanoseconds or rational ticks are candidates but need verified time-horizon and overflow bounds.
- Same-kind conflicts are declared global by `kind`, which may **over-block physically unrelated intersections**. Spatial conflict zone identity and movement graph are needed; a kind-only global conflict graph is not a realistic network validator.
- Current queues have unlimited pre-entry upstream waiting storage; there is no spatial propagation of spillback in this discrete-event engine. D18 CTM is a separate continuous vehicle-equivalent model and **not integrated**.
- Queue lengths are counts of not-yet-admitted requests after batch processing, not positions in physical lanes or measured bumper-to-bumper queues.
- The same-time release-before-admission tie-break is explicit but not calibrated to any real signal phases; event near-equality under floating time is unresolved.
- Research outputs and controls never actuate real-world signals; P12 remains frozen per user's earlier doctrine.

## Next acceptance criteria (P11-W)

1. Define clock abstraction: `Timestamp` and positive `Duration` with integer-tick canonical representation and explicit conversion from sensor nanoseconds. Prove/order/test no overflow and positive interval.
2. Build per-intersection **spatially scoped** conflict graph instead of conflict by global pedestrian/vehicle kinds.
3. Verify a finite-lane storage/queue ingress contract between event-driven P11 and continuous D18 CTM without equating continuous vehicle-equivalents and integers.
4. Reconstruct and replay untouched original P10 trajectory/time event from source with provenance.
5. Only afterward run same-demand SUMO and real observations; no policy optimization.
