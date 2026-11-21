# T2 signal-action and arrival-clock robustness — frozen protocol
Date 2026-11-21 · **REGISTERED BEFORE SEED 88–95 RESULTS ARE INSPECTED**

## Why this experiment exists

The preceding internal audit found two structural risks:
1. The proposed t84 policy uses 3 seconds of no-through/no-left service
   followed by only 4 seconds of protected left service. Although
   `dual_lane_v11` checks active-phase red separation, it cannot
   represent real yellow transitions, pedestrians, other approaches,
   controller minimum-green commitments or local legal plans.
2. `spatial_v10.arrivals(..., arrival_pattern="uniform")` deterministically
   fixes every arrival timestamp once demand_vph is fixed. Different seeds
   only change route labels and later lane allocations. Prior seeded
   'generalization' was not validation under new temporal headways.

## Lock before outcomes

Experiment cohort: **novel synthetic seeds 88–95**, eight independent
route/timing RNG seeds, no overlap with prior PHYS-01–11 or exploratory
seed76 audits.

- Regimes: (1800 vehicles/hour, left fraction 0.45) and
  (1650 vehicles/hour, left fraction 0.50).
- Downstream receiving capacity: **4 cells**.
- Bay lengths: **14, 28, 70m**.
- B-lane straight-assignment shares: **0, 0.5**.
- Duration 240 seconds; decision boundary t84.
- Three arrival-clock generators:
  (a) `legacy_deterministic`: exact `spatial_v10.arrivals`;
  (b) `fixed_count_uniform`: draw N=floor(duration*demand/3600)
       timestamps independently in [0,duration), integer-floor and sort;
       sample movement independently with a second seeded PRNG stream;
  (c) `poisson_exponential`: exponential waiting times rate demand/3600
       across the 240-second window, integer-floor the times, sample
       movements from a separate seeded PRNG stream.
  No truncation to at most one attempted upstream arrival per second,
  since arrivals are requests queued by the physical engine.
- There are **2 regimes × 3 generators × 8 seeds × 3 bays × 2 B
  shares = 288 distinct state-and-tape worlds**.
- In each world run one baseline and four prospective phase plans from
  the **same pre-t84 complete checkpoint**:
  A. existing baseline signal,
  B. 3s red at t84–87 and left green **4** ticks from t87,
  C. identical except left green **8** ticks,
  D. identical except left green **12** ticks,
  E. identical except left green **20** ticks.
  Each plan has red until t120 after its left-green window. The plans
  preserve at least the model's 3s separation between opposing active
  phases. These are abstract **green-duration sensitivity envelopes**;
  *none is certified as an implementable traffic signal plan*. In
  particular, this simulator cannot represent amber/yellow phases,
  concurrent pedestrian intervals, cross-street conflicting stages, or
  real controller legal minima. Do NOT label green≥8, 12 or 20 'safe'.
- Every comparison uses the same frozen t84 microscopic state and
  arrival tape; **worlds with different generator/seed/regime have
  different predecision states** and are not matched-state effects.
- Endpoint: `J = outside_vehicle_seconds + upstream_vehicle_seconds
  + receiver_vehicle_seconds + 60*remaining` at t240. Report
  `ΔJ = J_plan - J_baseline`, negative is lower model cost.

## Prespecified analyses and no-tuning rules

Primary:
1. For seed88–95/each generator, count strict ΔJ<0, ΔJ>0, ties
   separately by plan duration and demand regime.
2. Compare whether the known +306 seed76 failure's sign remains
   unchanged when green width is lengthened (explicitly labeled
   *exploratory known-seed pilot*; do not mix into novel cohort).
3. Record direct vs restarted baseline equality, vehicle conservation
   under every treatment, unchanged route tape, initial prefix identity.
4. Inspect arrival timestamp uniqueness across eight seeds at fixed
   demand. For the two random families, check mean generated count,
   minimum/maximum, and a tail measure of per-second arrival bursts.
5. Compare the distribution of ΔJ across arrival families and width,
   emphasizing any **strict sign differences for corresponding labels
   that occur in different states**. Do not interpret those as a
   same-state causal arrival-time effect.
6. Calculate per-seed savings aggregations; if showing uncertainty
   use whole-seed resampling, with only eight seed blocks. No
   interpretation as field confidence limits.
7. Keep baseline demand generator behavior unchanged; add a separate
   experimental arrival module rather than changing the original
   `spatial_v10.arrivals` with retroactive effects.

Decision criteria:
- **REJECT** robustness of the old 4s finding if strict sign or material
  scale depends on the arrival-clock family.
- **HOLD** signal feasibility and field performance regardless of
  whether green-duration sign is stable, because yellow/pedestrian
  and opposing stages are unmodeled.
- If strict signs do not change, report the null result; do not add
  other settings opportunistically to manufacture a reversal.
- Do not use retrospective optimal actions as decision-time policies.

## Reproducibility and preservation

Record Python version, GitHub main commit and exact five-core blob
identities, the new generator/runner/test blob SHA, all paired
full-precision JSON, seed/config/tape hashes and output SHA-256.
Run two byte-identical replays. Preserve source and outputs in the
shared Drive research evidence area; keep executable script, tests
and concise failure report in GitHub main. Do not use GitHub Actions
or the `github-actions[bot]` contributor. K047 holdout stays sealed.
