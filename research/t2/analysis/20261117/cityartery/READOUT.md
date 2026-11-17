# 17 November — CityArtery observations and daypart decisions

The origin of the work is a choice between feasible plans before the vehicle
state is fully observed. The time-of-day programme makes the distribution of
vehicle and pedestrian arrivals part of that choice. The D46 positive-travel
and FIFO work, D49 phase competition, and D51 phase-order comparisons supply
the mechanisms tested in the existing protected-stage queue simulator.

For model input, the synthetic daypart replay uses separate through and left
bays, a shared FIFO per approach, finite link storage, positive travel and a
downstream service calendar. A site's absolute offset reference would be set by
a verified signal or clock alignment. Here offsets are relative to the
synthetic common clock. The study holds the cycle (84 s) and candidate catalogue
(18 plans) fixed across policies.

| Policy | Worst cost | Worst regret | Sum over 12 worlds |
|---|---:|---:|---:|
| Fixed baseline | 34,818 | 5,501 | 166,021 |
| Pooled minimax cost | 32,583 | 3,340 | 149,172 |
| Pooled minimax regret | 35,414 | 3,096 | 151,494 |
| Band-specific minimax regret | 33,371 | 879 | 135,962 |

The frozen band-specific policy beats pooled minimax regret on all three
reported measures across 12 additional seeds. It beats pooled minimax cost on
worst regret and sum cost in 12/12 seeds. Pooled minimax cost beats it on worst
absolute cost in 12/12. These are perturbations of one synthetic scenario
family, with a known band and no switch/transient charges. In the original
evaluation, the band policy has no pedestrians remaining at the horizon in
all 12 worlds, with a maximum pedestrian waiting area of 1,960 person-seconds.
This exceeds pooled minimax regret's maximum of 1,441 person-seconds. Separate
weights or explicit pedestrian guarantees can therefore change the judgement.

## Next implementation

1. Use spatial lane/stop-line geometries and a clock registry to admit a
   recording per the CityArtery intake README. A verified signal clock makes
   queue and discharge alignment testable.
2. Exercise a two-junction feedback case by letting the downstream queue
   consume link space and block upstream service. The current receiving
   calendar is exogenous. Reuse D46's travel and finite-storage checks for the
   coupled Python/SUMO comparison.
3. Add a maximum pedestrian wait based on per-person waiting times and test
   tied costs under that constraint, then perturb saturation service and
   misclassified or missing observation at a band change. Preserve the
   difference between a demand forecast and a current-state measurement.

The field axis still needs independent evidence. Preserve the DLR held-out
period and reserve the field comparison until the observable join is validated.

## Reference candidates

- Ashqer et al., “Estimating Queue Length, Spillback, and Delay Using
  Trajectories of Probe Vehicles,” [journal](https://doi.org/10.1080/19427867.2023.2204249),
  [open preprint](https://arxiv.org/abs/2207.08025). Validate proxy and queue definitions against trajectories.
- Christofa, Argote and Skabardonis, “[Arterial Queue Spillback Detection and Signal
  Control Based on Connected Vehicle Technology](https://doi.org/10.1177/0361198113235600108).”
  Compare receiving-link observables and policy triggers.
- Wan et al., “[Signal optimization at an isolated intersection under cyclic
  vehicle arrivals using spatially sparse trajectory data](https://doi.org/10.1016/j.trc.2024.104643).”
  Compare reconstruction assumptions for platooned arrivals.
- Wang, Yu and Ma, “[Intelligent decision framework for person-based signal
  control: A generalised signal scheme](https://doi.org/10.1016/j.ins.2025.122309).”
  Compare vehicle/pedestrian conflict and phase options.
