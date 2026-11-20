# T2-SF-01 — fixed synthetic experiment contract
Date 2026-11-21; status: PREDECLARED, not field data.
- Worlds: published eight arrival-order bit patterns × the **two whole-simulator** bypass modes 0/1. Delta is left-first cost minus through-first cost.
- Policy: for each reported sensor label, choose left-first with probability between 0 and 1; right comparator is through-first.
- Mode channel: binary noisy label for the **structural simulation mode**, NOT a camera detecting a legal/safe gap.
- Arrival channel: 8-category hypothetical forecast of 3-bit future order. With error q, correct label gets 1−q; each of the 7 other patterns gets q/7.
- Given a true world, both channels' errors are modeled **conditionally independent**, with arbitrary world-specific q_mode in [0, ε_mode] and q_arrival in [0, ε_arrival]. Independence and symmetric wrong-label distribution are strong modeling choices, not learned traffic properties.
- Regret: loss relative to the best of two permitted phase orders in the same world. No empirical improvement fraction, population frequency, prior distribution, or risk guarantee under model mis-specification is inferred.
- Report timing: a forecast of future arrivals may be issued before the commitment tick. A realized future value, even if known to the simulator at runtime, is NOT an admissible input.
- Held-out K047 18:00–18:30 UTC remains sealed. Retired K047-review.html remains retired.
**Decision gate:** look for conditional complementarity, but measure its fragility to small mode-observation error and observation cost.
