# PHYS-08 — Age-aware observation fallback (frozen prospective synthetic screen)

2026-11-21 · Pre-registration before examining any seed 40–55 results

## Motivation and epistemic status

PHYS-07 found that a frozen k=5 decision rule trained on seed 0–7
degraded when its simulated decision-time observation was 12–24 seconds
old. A static geometry-only rule is a possible *engineering fallback*
when the detector feed becomes stale. It is not a road-safety failsafe,
and the model is not calibrated to field traffic.

## Evaluation lock

- Training is the existing PHYS-04 144 rows from seeds **0–7** only.
- Previous exploratory observation study used seeds **8–31**; PHYS-07
  regime sensitivity used **32–39**. None of those outcomes are used to
  fit or adjust the following locked policy.
- New prospective synthetic evaluation set: seeds **40–55**;
  receiver capacities 2/4/8 cells, turn bays 14/28/70m,
  through B-share 0/0.5; **288 same-state policy pairs per regime**.
- Two exogenous demand regimes: (A) uniform 1800 vph and 50% left,
  (B) uniform 1350 vph and 30% left. The second regime probes the
  previously discovered fragility under reduced turning demand.
- Outcome model and action: identical pre-tick-84 state, unchanged
  baseline versus 3s clearance + 4s left-green intervention,
  cost integrated vehicle-seconds plus 60 times remaining vehicles.
- Decision telemetry age: **0, 6, 12, 24 seconds**, achieved by actually
  observing earlier states at ticks 84, 78, 72, 60.
- Frozen predictor: existing k=5 nearest-neighbor expected delta, with
  geometry, counts, or positions features and no test label lookup.
- Frozen comparison policies: always control, always intervention,
  geometry-only, stale counts, stale positions, and the **age-aware
  fallback** that uses counts or positions when age is *strictly less
  than 12 seconds*, otherwise switches to geometry-only. The 12s
  threshold is chosen from *prior* 8–31 exploration and is never
  optimized against seeds 40–55.

## Required audits

1. Direct uninterrupted baseline equals checkpoint-restarted baseline
   for every evaluated case. Exactly one arrival tape per pair.
2. Conservation for both alternative outcomes, plus no future tape or
   future RNG value in decision observations.
3. Four age-conditioned observations must be generated strictly from
   each case's own historical prefix; no 'future' imputation.
4. Evaluate the 576 cases once per distinct future plan; policy
   differences select between those two fixed outcomes only.
5. Count actual decisions and realized savings, regret against the
   *retrospective, nondeliverable* oracle, and paired **16-seed-block**
   intervals; do not treat the 18 geometric repeats per seed as iid.
6. Perform two byte-identical local runs; hash raw output. Compare
   exact GitHub file blob for the new script. Report known inability
   to clone a byte-for-byte full `main` runtime separately.
7. Report failure regimes even when the fallback reduces latency loss
   in the original demand regime. No tuning after seeing new results.

## Interpretation limits

This is a stress test of one synthetic vehicle cell simulator. A
fallback to geometry is a substitute decision heuristic, **not** an
actuator-safe controller. Neither minimum-green safety constraints nor
sensor calibration, mixed vehicles, network-wide queues or human
gap-acceptance are validated. K047 remains sealed.
