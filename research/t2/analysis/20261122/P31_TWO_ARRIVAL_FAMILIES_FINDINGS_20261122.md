# T2 P31 — Falsification of 6s/10s score plateau under new arrival-clock families

2026-11-22 KST. [Preregistered design](P31_TWO_ARRIVAL_FAMILIES_PREREG_20261122.md) was committed `f5e92bb0f5b8cd22ab083b28450912f621adc7d7` **before** P31 execution. The hypothesis is exploratory because the motivating P26/P30 plateau was already observed.

## Question, sources and method
Does the earlier 64/64 matched-world equality of abstract model-left-stage 6s vs10s scores generalize beyond the random-reclocked arrival tapes? The previously frozen P30 sample has only four arrival tapes and gives exact+4 refused attempts in each world; the P31 cohort uses fresh seed labels124–127, hence eight complete new time-and-route sequences.

The exact original `dual_lane_v11.py`, `spatial_v10.py`, `receiving_cells_v15.py`, `physical_transfer_screen.score` core remains unchanged. [P31 runner](p31_two_arrival_families.py), SHA Git blob `d53eb9c1b04a162f39866c4ae5627600288bf9d9`, constructs:
- `uniform`: vehicles are spread at evenly spaced integer timestamps within the same 240s horizon.
- `platoon4`: the same ordered route labels are regrouped into four arrival clusters of 15s each, anchored at t20,80,140,200. Route sequence and total vehicle number are preserved, but clock dynamics differ sharply.
- 4 fresh regime/seed pairs ×2 clock families ×2 receiver capacities(2/4) ×2 downstream offsets(0/15) ×2 pocket lengths(14/28m) ×2 B shares(0/.5) = **128 model worlds, eight distinct complete arrival tapes**.
- Every 6s/10s intervention starts from its **own identical within-world tick84 physical checkpoint**, not from checkpoints shared across clock families. Identity-based event metrics use P30's exact trace validator, fail on missing or duplicate crossings or inconsistent refusal counts.

## Falsification, including null results

| Clock mechanism | Worlds | 6s =10s score | Different score | 10s−6s denial count exactly +4 | Other denial deltas |
|---|---:|---:|---:|---:|---:|
| Uniform | 64 | 63 | **1** | 52 | 12 |
| Four platoons | 64 | 56 | **8** | 56 | 8 |
| **Total** | **128** | **119** | **9** | **108** | **20** |

All nine **non-equal** pairs show `score(10s)−score(6s) = −189`, simultaneously with changed simulated network departure and terminal remaining count. The earlier universal generalization **“6s and10s always have the same final model cost” is falsified**. Exactly-four refusal-increment universality is also falsified in **20/128** new model worlds; neither exact increment nor aggregate cost equality is an invariant of the unchanged physical model across arrival processes.

The 9 counterexample worlds are *not* 9 independent traffic days. All nine happen with downstream capacity4 and offset15s; five share seed126 or repeated geometry. Clock mechanism and offset alter traffic already before tick84. These results therefore support the narrower claim that **arrival process and downstream service opportunities moderate the synthetic policy response**; they do not establish how a real intersection should alter green time.

## Provenance and tests
- [P31 tests](test_p31_two_arrival_families.py), exact Git blob `1d2b5957bd7cc86fb99764339a8b496a57576427`, **11/11 PASS**, test log SHA256 `31a01e4e3face47e6e4834357ebd8dbb0d9708d555fe3b2f99b08fbded6b1ed0`.
- Complete P31 JSON SHA256 `ff0452b4b37174b17bf91228722209de0f26ac60730ef9ef673b08d50c0f4915`.
- [P31 machine summary](P31_TWO_ARRIVAL_FAMILIES_RESULTS_20261122.json); full 128 rows in separate reproduction ZIP. All original historical P19–P29 JSON files unchanged.
- Paired event audit P30 [results](P30_UNIQUE_VEHICLE_EVENT_AUDIT_RESULTS_20261122.json) and [findings](P30_UNIQUE_VEHICLE_EVENT_AUDIT_FINDINGS_20261122.md) show same score can hide changed distinct rejected vehicles; P31 shows even score equality itself fails across more diverse arrival time distributions.

## Next falsifiable step
Instead of lengthening model-left-stage beyond 24s, measure which candidate future arrivals and receiver occupied-cell patterns are necessary for action cost inequality. Build a **minimal sufficient decision-state test** conditioned on predecision queues, arrival clock descriptors, and downstream occupancy, with family-held-out scoring. Avoid using future arrival tapes as sensor-visible control inputs. Better yet, independently replay equivalent road geometry in SUMO or other genuine microsimulator and compare physical queue travel time. Neither empirical calibration, real timing clearance, pedestrian service nor live controller interface is established by T2.
