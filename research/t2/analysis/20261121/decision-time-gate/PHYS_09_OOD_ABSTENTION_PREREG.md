# PHYS-09 — Training-support abstention: locked synthetic prospective test

Date 2026-11-21 · **pre-registration before observing seed56–71 outcomes**

## Research question

PHYS-08 rejected a blanket 12s geometry fallback because it worsened the
low-turn regime. Could a purely decision-time, label-free out-of-training
support check reduce the policy's harm under a changed demand mix?
This is an *abstaining intervention selector*, not a certified safe
traffic controller. It defaults to the existing baseline phase plan,
without claiming the baseline is field-safe or optimal.

## Data splits and locked procedure

- Fitted 5-nearest-neighbor delta predictor from PHYS-04 original seeds
  **0–7**, demand 1800 vph, 50% left, only.
- A leave-one-**seed**-out nearest-feature distance is computed for each
  of the 144 training rows against the other seven seed groups.
- For a feature map (counts or occupied positions), set OOD radius to
  the **95th percentile of those 144 leave-seed-out squared Euclidean
  nearest distances**, nearest-rank quantile
  `sorted(distances)[ceil(0.95*n)-1]`.
- At runtime, compute the minimum squared distance from test feature
  to **any** training example. If it exceeds its training radius,
  **abstain / maintain the baseline phase plan**. Otherwise use the
  unchanged 5-NN sign-of-mean-delta decision.
- Geometry, receiver capacity, pocket length and B-share are known
  design parameters; counts and positions are privileged perfect
  simulator observations at the decision tick. The model may not
  have corresponding real-world detectors. Future arrivals, labels,
  random state, and actual demand-rate/left-share parameters are NEVER
  fed to either policy.
- Newly held-out seeds **56–71**, distinct from PHYS-04 (0–7),
  PHYS-05 (8–31), PHYS-07 (32–39), PHYS-08 (40–55).
- Two regimes: uniform 1800 vph/left 50% and uniform 1350 vph/left 30%.
  At each regime 16 seeds × (2,4,8 receiver cells) ×
  (14,28,70m pockets) × (0,.5 B-shares) = **288 same-state policy pairs**.
  Two regimes total 576 pairs, but across regimes initial traffic
  microstates differ.
- Tick-84 checkpoint and unchanged arrival tape, control vs the prior
  future left-green intervention; identical 240-tick objective and
  terminal penalty 60. Require direct/resumed baseline identity and
  vehicle conservation for every paired case.
- Compare always control, always treat, unchanged k=5 learned
  counts/positions, OOD-abstaining counts/positions, and hindsight
  oracle (retrospective only). Record coverage, disagreements,
  per-seed savings/regret and 16-seed-block percentile uncertainty.
- Check two byte-identical output runs and SHA-256 before making any
  claims. Do not optimize the OOD percentile after seeing new seeds.

## Risks and falsification

OOD distance in a high-dimensional feature map may not detect changes
in vehicle behavior or policy effects; a genuinely different demand
regime can produce apparently familiar queues. Abstention may cause
false negatives and lose potential savings, or fail to catch harmful
interventions. There is no universal assurance of nonnegative
benefits, legal signal timing, or real-world safety. Report full
counterexamples rather than selecting only aggregate favorable cases.
K047 real holdout remains sealed.
