# RF07 — Low-cost cross-modal sensing: post-hoc scope and next prospective protocol

Date: 2026-11-21. This document was written **after** the first RF07 toy implementation and 12 local tests. It is NOT a retrospective preregistration.

## Motivation
A high-quality exhibition should show why a *motion-only* sensor cannot identify an occupied stationary lane, and why a small additional measurement might change the best decision. Candidate mechanisms: ESP32 Wi-Fi CSI, magnetic occupancy, microphone activity, light interruption, and hand-labelled tabletop ground truth. No real sensor data are yet collected.

## Exact toy study, tested locally
- Hidden pocket P and downstream D, each binary: four equally likely states.
- Invented action cost: hold=0; imaginary treatment=-2 if P=1, +3 if P=0. Units are artificial.
- Aggregate sensor reveals P+D perfectly; noisy pocket and downstream probes each report their target bit correctly with probability 4/5; an OR probe reports P OR D correctly with probability 9/10; motion-only emits the same signal for all four stationary states.
- Channel errors assumed conditionally independent given P,D. This is a modeling hypothesis, not a measured radio property.
- Exact Fraction arithmetic enumerates all joint signals; for each observation the Bayes optimal action minimizes expected hypothetical cost; report oracle regret and per-channel fee.

## Future *prospective* physical gate
1. Separate construction and measurement equipment. Only school-approved, owned transmitter/receiver devices, on a small tabletop model with consent and teacher supervision.
2. Freeze zone layout, manually observed labels and time/session holdout **before** recording.
3. Compare empty, moving, pocket stationary, downstream stationary, jointly stationary, with fixed train/test sessions.
4. Compare motion/activity versus occupancy; include no-sensor and simple optical or magnetic baselines.
5. For each channel report confusion matrix, coverage, false-source classification, abstention, delay and installation costs.
6. Pass empirically measured likelihoods into RF07 only after independent verification. Do not call artificial 80/90% assumptions RF accuracies.
7. If no known-bounded sensor placement or repeatable signal: NO-GO for causal diagnosis; a negative result is valid.

## Stop conditions
No human pose, bystander monitoring, other people's Wi-Fi packets/MACs, roadside hardware, traffic control, or unapproved RF setup. The ~5GB CIM dataset.zip stays on HOLD. K047 remains sealed.

## Prior art and caution
- Official Espressif esp-csi https://github.com/espressif/esp-csi has actual sensing examples but does not make Wi-Fi a pixel camera.
- Wi-Fi DensePose repositories show ambitious visualizations; claims need a measured held-out pose benchmark. This project does not reproduce them.
- RF06 exact four-state information results are earlier synthetic science. RF07 adds deliberately noisy sensors, fees and conditional independence assumptions; real efficacy is untested.
