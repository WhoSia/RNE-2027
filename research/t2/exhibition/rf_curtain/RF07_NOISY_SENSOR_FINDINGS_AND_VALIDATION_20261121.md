# RF07 — Noisy sensor selection and costs: findings / evidence boundary

Date 2026-11-21. **Invented exact four-state mathematics, not CSI performance, measured traffic, or real policy advice.**

## Model
P,D each in {0,1}, uniform prior, baseline cost 0. Hypothetical treatment cost delta -2 if P=1, otherwise +3 (invented dimensionless units). Exact conditional Bayes minimum vs omniscient state oracle. Errors of multiple channels are assumed conditionally independent GIVEN the hidden state. This assumption can fail in real correlated RF/environmental noise. Sensors are NOT calibrated measurements.

Toy channels:
- Exact total blocked P+D (aggregate)
- 80% binary pocket-specific bit, 80% downstream-specific bit
- 90% logical-OR blockage bit
- Motion-only channel with zero static-state information

## Exact Fraction arithmetic results

| Sensors | Expected hypothetical cost | Regret vs full state | Net cost with fee 1/5 per channel |
|---|---:|---:|---:|
| None | 0 | 1 | 0 |
| Aggregate | -1/2 | 1/2 | -3/10 |
| Noisy pocket | -1/2 | 1/2 | -3/10 |
| Noisy downstream | 0 | 1 | 1/5 |
| Noisy OR | -3/20 | 17/20 | 1/20 |
| Motion-only | 0 | 1 | 1/5 |
| Aggregate + noisy pocket | -3/4 | 1/4 | -7/20 |
| Noisy pocket + noisy downstream | -1/2 | 1/2 | -1/10 |
| Noisy OR + noisy pocket | -57/100 | 43/100 | -17/100 |

**Interpretation:** A sensor that supplies no decision-relevant information provides zero benefit before cost, and actively harms net value when observations have a fee. Adding an independent informative channel cannot increase the exact ideal Bayes regret when fees are zero, but may increase total cost once fee is charged. This is a property of the invented distribution and perfect Bayesian optimizer, not a guarantee for an estimated model or actual acquisition.

## Execution and custody
- A semantically equivalent local prototype and its 12 Python unittest checks ran successfully in Python with exact fractions (12/12 PASS). An initial local printout was generated.
- Four separate GitHub main commits preserved protocol, cross-domain matrix, implementation, and 12-test source. These four canonical blobs were independently read back from GitHub main.
- **Important open gate:** The final GitHub-committed Python contents were compacted from the equivalent locally tested version; the exact fetched GitHub source and test pair were NOT run together in a fresh authenticated checkout in this work unit. Therefore we do NOT claim a full exact-blob 12/12 verification of the uploaded pair. Run `python -m unittest -v test_rf07_noisy_sensor_value.py` in `research/t2/exhibition/rf_curtain` and hash/freeze that result before upgrading the claim.
- No field measurements, no Wi-Fi equipment capture, no project hardware inventory, no random person tracking and no live controller. No GH Actions/bot. K047 sealed; CIM dataset.zip hold.

## Future falsification gate
Replace artificial likelihoods with verified blinded manual labels and measured approved tabletop observations. Examine correlated error (violates conditional independence), across-session drift, changed placement, stationary metal/nonmetal differences and uncertain action constraints. Compete against a trivial optical/marker baseline. A negative result should be preserved.
