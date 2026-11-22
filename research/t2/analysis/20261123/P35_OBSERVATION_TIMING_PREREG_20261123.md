# T2 P35 — Forward-only field observation timing versus hindsight: frozen 2026-11-23 protocol

## Origin and scope

P34-OBS reconstructed **17 directly bracketed 20Hz geometric stopline center crossings** in an exact DLR-UT v1.3.1 15-min observation; the publisher's same-source 1Hz route counter also had 17 records and **16/17** approach+±1s matches. P33 found a **2.004s common gap** in all 30 signal-head observations. The current question is narrow but consequential: **how often does assigning an observed signal state to a crossing by selecting the temporally nearest sample use a signal record from the future?** Such hindsight must not be presented as available to a live policy at the crossing.

This is OBSERVATIONAL TIMING QA only. No signal-head→approach/lane control map, experimental signal intervention, or external microsimulation exists. No red-light-running, green-without-discharge, or safety violation inference is licensed.

## Immutable input gates
- P34 archive ZIP SHA256 `bb8701db35578951e82202845c5fa9b65d5ee55afb31c1afed22292e65a3c679`; inside it the 17-event ledger `p34_result.json`, SHA256 `ea0eaae72afd8e82547a5f0b278765e27a871d86cdabeb34a2e4bf4e0a646c72`. A P34 re-execution using map+trajectory+volume is the stronger upstream validation and is preferred when accessible.
- Exact original signal CSV SHA256 `95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c`.
- Verify **17** P34 crossing entries, 16 matched publisher events, 30 signal IDs and **26,970** signal rows. Hard reject hash, timestamp, ID, duplicate head/time or object-bracket corruption.
- All 17 event brackets are direct 50ms vehicle observations, *not exact physical crossing instants*. Each crossing's estimated interpolated timestamp must lie within its bracket.

## Predesignated metrics

For each crossing bracket `[start,end]` and EACH of the 30 signal heads, compute:
- `latest_seen_by_bracket_start`: most recent sample at or before **start**; this is the conservative causal signal observation. Compute its *age at bracket end* (the worst observed time staleness over the 50ms candidate event interval).
- `first_sample_after_bracket_end`: the first sample strictly after **end**; hindsight, not a causal observation.
- `closest_sample_to_estimated_crossing`: the timestamp minimizing absolute difference (tie broken toward earlier), explicitly labeled HINDSIGHT if later than the bracket start. Compare whether this differs from the last causal sample. **No linear interpolation of discrete signal codes.**
- For each event, flag whether any of the 30 heads changes *sampled state* between conservative before and next after; only establishes observational ambiguity, never actual instantaneous phase.
- Bounded 1Hz freshness thresholds **0.25 / 0.5 / 1.0 / 1.5 / 2.5 sec**, all measured against *bracket end*. At stricter thresholds stale means no sufficiently fresh verified preceding observation; treat as unknown rather than use future data.
- Explicit P33 common-gap overlap predicate between event bracket and `23:31:44.010Z–23:31:46.014Z`; report zero if actual evidence supports zero.
- Re-evaluate approach/time matching counts at time thresholds **0.25 / 0.5 / 0.75 / 1.0 / 1.5 sec**, using the exact P34 ordered global max-cardinality/min-error dynamic-programming matcher with its original P34 source (not greedy nearest neighbor). Reconstruct official route-count source from the **actual volume CSV**, and compare the ±1.0s baseline with P34 **16**.

## Falsifiers and independent check

The main finding must be allowed to be null. A detected lack of future-sample use would be recorded, not optimized away. If any fresh causal observation also differs from the state later reported, no instant controller change is inferred. An independent Node.js stdlib reference should recompute one core temporal claim from raw CSV rather than merely copy Python counts. At least one artificial 2.004s counterexample must show a stale/no-future observation gate.

## RAVEL and return edge

Explanandum: signal/vehicle timing information actually available at the time of observed stopline crossing. Selected: Observer-First Drift Audit, Exact-Runtime Certification, Bridge Intent ≠ Bridge Closure. Rival: nearest-time interpolation is harmless because signal codes rarely change; attack by counting source timestamps in the future and sampled state discordance. Authority ceiling: same-source timing fidelity, *not* traffic-phase-to-lane causality. Stage CORE for observation-boundary identification, ENABLING for field congestion mechanism. Return edge P36: independent movement/approach mapping or live junction geometry; do not add another metadata-only stage otherwise. No GitHub Actions/bot; `main` only, old-day source immutable.
