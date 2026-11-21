# PHYS-05b — decision-observation corruption / detector error falsification

**2026-11-21 · SYNTHETIC_DETECTOR_STRESS_NOT_CALIBRATED**

## Why

PHYS-05 found that a policy conditioned on decision-time aggregate occupancy
and occupied cell positions can outperform an unconditional phase action
on synthetic held-out demand seeds. However, the trained classifier
received perfectly measured simulator state. It was important to test
this assumption before treating high-resolution observation as a
practical engineering requirement.

## Frozen evaluation

The PHYS-05 k=5 rule trained only on seeds 0–7 is **not retrained**.
Existing 432 paired outcomes for held-out seeds 8–31 are **not
resimulated or changed**. At policy selection time only, independently
perturb the six count features by uniformly sampled integer errors
bounded by +/-1 or +/-2 and omit each occupied cell observation with
probability 0%, 10% or 30%.

The noise is generated with a reproducible arithmetic seed derived
solely from scenario identifiers, not from the policy outcome. It is
clipped to the configured physical count limit (20 upstream cells,
pocket length / 7, receiver capacity). The corrupted count and
occupancy arrays can disagree: this intentionally models unsynchronized
sensor channels and is **not a calibrated detector error distribution**.

Eight fixed noise realizations are evaluated for each noisy scenario.
The zero-noise control is one exact realization. Absolute cost units
remain sums of synthetic vehicle-seconds plus an endpoint penalty.

## Local source-derived results

| Observation corruption | Mean total savings, counts policy | Mean total savings, positions policy | Mean policy-decision changes vs clean, counts / positions |
|---|---:|---:|---:|
| Exact decision observation | 48449 | 49586 | 0 / 0 |
| Count ±1, positions complete | 48211.375 | 49790.25 | 26.375 / 14.75 |
| Count ±1, position omission 10% | 47983 | 49595.5 | 26 / 19.875 |
| Count ±2, position omission 30% | 47022.375 | 49304.875 | 46.625 / 39.125 |

Each trial scores the same 432 holdout conditions. The counts and
positions policies select treatment under different feature maps and
their performance is not guaranteed to be monotonic under random noise.
For instance, the positions policy's mean at count ±1 without
dropout was slightly higher than the clean result. This is **not
evidence that sensor noise improves traffic**; a finite-sample
classifier can change decisions in either direction.

Under the strongest tested corruption, the mean counts-policy
saving falls by 1426.625 compared with clean, while the mean
positions-policy saving falls by 281.125. Mean decisions differing
from the clean choice were 46.625/432 and 39.125/432,
respectively. No statistical uncertainty bound on these effects is
claimed from only eight randomized realizations.

## Controls, reproducibility and limits

- Outcomes for each case stay fixed; only the decision feature vector
  is mutated. The original record and outcome are preserved.
- Sensor noise is independent of future events, policy outcomes and
  any training labels.
- Double local execution generated exactly identical JSON bytes.
- Source-derived local Python output SHA-256:
  `309ad56f67946519127bdeb7cdca6b3b4883a6179058e4119ec40f4f2cf42a98`.
- Exact GitHub blob checkout and its full committed regression suite
  have **not** run in the isolated Python container.

These errors are illustrative not empirical; the real detector error
distribution, spatial measurement constraints, time delay,
correlated missingness, detector placement and demand shift remain
unmeasured. There is no claim of field policy safety or efficacy.

## Research decision

Observation and geometry interact with phase value, but current
controlled perturbations do not immediately destroy the synthetic
position-policy advantage. Next priority is **delayed information,
correlated missingness and external demand distribution shifts**.
Physical sensitivity PHYS-06 shows why that observation analysis must
be reported alongside explicit target-gap and receiving-capacity
assumptions. Continue to preserve the protected K047 holdout.
