# RF06-D — Pre-registered task-relevant observation value under a purely invented action-cost table

Date 2026-11-21. Status: PROSPECTIVE_MATH_TOY_ONLY / ZERO_TRAFFIC_CONTROLLER_EVIDENCE.
This commits the exact outcome and anti-leakage expectations BEFORE implementation.

### Why this unit
RF06-B proved a 1-bit pocket probe can beat the 1.5-bit total blockage count at classifying P. The **T2 policy research** requires a separate question: which observation changes a preference among *admissible actions*, and by how much? We cannot import measured cause/error probabilities (none collected) or claim any real-world signal plan is feasible. We therefore construct a transparently **arbitrary diagnostic cost table**.

### Locked synthetic world, observations and action family
Exactly four states P,D∈{0,1}, uniform prior1/4. All sensor mappings are the RF06-B ideal functions, without RF hardware or class ambiguity. Two **purely abstract** actions: `baseline` cost 0, `hypothetical_treatment` cost difference from baseline **+3 if P=0**, **-2 if P=1**, regardless of D. The sign and magnitudes are invented **dimensionless illustrative costs**, NOT travel delay or PHYS ΔJ. In particular this action is not a left-green length, not a viable field signal phase and not an intervention plan.

The policy observes only the fixed sensor signature and chooses the action minimizing **conditional expected toy cost**. If tied, choose baseline. Freeze decision rule, no fitting and no parameter adjustments in response to results.

### Mathematical expectations
- `none` / the stationary motion-only sensor: baseline for all; expected toy cost 0. Perfect information oracle expected cost -1, hence risk regret **1**.
- `aggregate_count=P+D`: treat only (P,D)=(1,1) where Y=2; expected cost **-1/2**, regret **1/2**, even though entropy1.5 bits.
- `pocket_probe=P`: treat both states P=1; expected cost **-1**, regret **0**, even though entropy1 bit.
- `any_rf_change=P∨D`: treat the three states with OR1 due to average treatment cost -1/3 in that group; expected global cost **-1/4**, regret **3/4**.
- `downstream_probe=D` only: P marginal remains equiprobable; always baseline and regret1.
- `any_rf_change+pocket_probe` has 4-class state Bayes error1/4 (cannot tell 10 from11), yet **zero regret for this cost**, because perfect D identification is not needed to choose action.
- `aggregate_count+pocket_probe` has full state identification and zero policy regret.
- The zero-information baseline is explicitly allowed as `()`; one cannot confuse having no sensor with an invalid external API state.
- Nonuniform prior (7,1,1,1) normalized to /10: perfect oracle expected cost -2/5; base no-sensor cost0; regret2/5. No uniform-prior shortcuts allowed.

### Inference boundaries
This is an exact finite table and an exercise in Bayes decision theory, NOT an empirical sensor information benefit, causal policy improvement, minimum green legality, proven T2 six-count alias or field signal controller result. The `CIM dataset.zip` hold is absolute. No physical CSI, K047, public roads or GitHub Actions.
