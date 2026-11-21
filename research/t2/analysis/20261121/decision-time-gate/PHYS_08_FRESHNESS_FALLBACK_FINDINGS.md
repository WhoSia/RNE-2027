# PHYS-08 — Prospective age-aware fallback falsified by turn-share shift

2026-11-21 · R&E 2027 / T2 · **SYNTHETIC_UNCALIBRATED**

## Protocol lock and evidence provenance

The 12-second freshness threshold and seed 40–55 evaluation were
pre-registered *before* reading those new seed outcomes:
[PHYS-08 pre-registration](PHYS_08_FRESHNESS_FALLBACK_PREREG.md).
The model and k=5 predictor were fixed on seeds 0–7; intermediate
PHYS-07 results on seeds 8–39 were used to choose the proposed cutoff,
not to re-fit the learner. Geometry fallback substitutes an estimated
action when observation age is at least 12 seconds. **It is not a
traffic-signal safety fallback**.

Each of two new regimes evaluates 16 seeds × 3 capacities × 3 bays × 2
B-assignments = **288 paired policy worlds**, 576 control-versus-policy
pairs total. Within each pair, both futures share exactly the same tick-84
microscopic state and arrival tape. The observed information is captured
from tick 84, 78, 72 or 60 for ages 0, 6, 12, 24 seconds.
The retrospective per-case oracle is NOT a deployable control.

## Results: 24s old detector feed

| Demand regime | Never intervene | Always intervene | Stale counts | Stale positions | Geometry fallback | Retrospective oracle |
|---|---:|---:|---:|---:|---:|---:|
| Uniform 1800 vph / left 0.5 | 0 | 14,519 | 8,431 | 9,419 | **13,758** | 14,901 |
| Uniform 1350 vph / left 0.3 | 0 | −71,042 | −16,704 | −15,599 | **−57,852** | 9,881 |

Values are the sum of model-cost savings versus always maintaining
the baseline, with penalty 60. Positive is a model benefit, negative
is an increased model cost. For 24s telemetry, the fallback increases
savings by **5,327** versus stale counts in the original regime,
but **decreases** savings by **41,148** versus stale counts under the
low-turn shift. The corresponding positions comparisons are
+4,339 and −42,253.

For the low-turn shift, even *fresh* counts/positions policies had
negative savings (−8,665/−10,680). This is a previously unseen
synthetic demand regime, not simple detector staleness.

## Age response (each regime is 288 cases)

| Regime | Age | Counts | Positions | Age-aware counts fallback |
|---|---:|---:|---:|---:|
| Original | 0 | 14,688 | 14,683 | 14,688 |
| Original | 6 | 13,961 | 13,962 | 13,961 |
| Original | 12 | 11,548 | 12,339 | 13,758 |
| Original | 24 | 8,431 | 9,419 | 13,758 |
| Low-turn | 0 | −8,665 | −10,680 | −8,665 |
| Low-turn | 6 | −12,021 | −5,578 | −12,021 |
| Low-turn | 12 | −11,999 | −6,671 | −57,852 |
| Low-turn | 24 | −16,704 | −15,599 | −57,852 |

## Uncertainty and heterogeneity across seeds

Bootstrap resampling 16 seed blocks (18 correlated road configurations
per seed), 10,000 seeded draws, age-24 **fallback minus stale-counts**
per-case average difference:

- Original demand: +18.50, 95% seed-block percentile interval
  **[+2.56, +38.23]**.
- Low-turn demand: −142.88, interval **[−210.48, −74.16]**.

Despite a positive aggregate improvement in the original demand,
the fallback was individually *worse in 12 of 16 seed blocks*
(only four seed blocks generated larger positive gains). This
tail-concentration makes unconditional average effects unsuitable as
a safety argument.

## Event-level explanatory witness: seed 53, receiver 2 cells, pocket 14m, B share 0

The same geometric setting and random seed under two *different demand
regimes* gave **opposite intervention preference**. The within-regime
control and intervention were branched from identical tick-84 state
and matched all 84 predecision frames.

| Quantity | 1800 vph / left 50% | 1350 vph / left 30% |
|---|---:|---:|
| Generated vehicles | 120 | 90 |
| Intervention ΔJ (treatment minus baseline) | **−281** | **+781** |
| Baseline downstream straight / left out | 26 / 17 | 30 / 15 |
| Intervention downstream straight / left out | 27 / 19 | 29 / 11 |
| Baseline remaining | 77 | 45 |
| Intervention remaining | 74 | 50 |

At tick 84 the high-demand case has outside-A queue 5 and
approach-A/B 18/2, while the low-turn case has outside-A queue 0
and approach-A/B 10/5. Both have two pocket cars and two receiver
cars. Their microscopic states are **not the same** across regimes,
so the sign flip is a physical-world *sensitivity witness* rather
than a same-state causal effect of demand. Within each demand world,
the counterfactual signal intervention begins after the common prefix.

A total of **18 of the 288 matching seed/geometry combinations**
had a strict sign reversal when comparing the two demand regimes
(note: again, these are different predecision states).

## Reproducibility and open gates

- The full PHYS-08 local output was independently replayed with
  identical SHA-256 **`8994b32bcd4011d776ac222bd42922136d7acf1b6398a65fa544b1c3a29363f2`**.
- Event witness JSON SHA-256
  **`47ed567d3d9fdb27d66473d7bcb3a6ed4746646faa24fc7f610ea8aafb94d452`**.
- PHYS-08 main runner's exact local Git blob equals the current
  connector-fetched GitHub file SHA
  **`887acba7146b10c68ffcbee51764f668325968b0`**.
- Prospectively locked age-gate regression tests **5/5** passed in
  the source-derived local runtime; exploratory trace witness tests
  **3/3** passed; PHYS-07 tests **7/7** passed.
- The isolated Python runner imports simulator helper code copied
  from earlier source inspections, **not** a clean exact-blob checkout
  of all GitHub `main` dependencies. This remains an open
  reproducibility qualification, despite exact equality of the
  experiment script's own Git blob.
- The observational features are privileged simulator states, not
  verified detector readings; this is no validation of a legal,
  safe, or generally optimal signal controller. K047 remains sealed.

## Technical verdict

**Reject the current 12-second geometry fallback as a generally
reliable safety or performance rule.** It is only a conditional
model heuristic, helpful in one synthetic regime and strongly harmful
in another. A next experiment may compare a conservative
*no-intervention/abstention* policy under established detection
of observation age and regime uncertainty. That policy requires
new out-of-sample evaluation; do not optimize its threshold on this
PHYS-08 prospective set and re-label the same set as confirmation.

The decisive engineering issue is not merely a richer car-following
simulation: reliable policy decisions require valid decision-time
measurement, distribution-shift detection, and explicit abstention.
