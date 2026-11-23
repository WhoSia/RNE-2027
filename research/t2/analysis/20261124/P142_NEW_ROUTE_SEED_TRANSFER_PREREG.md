# P142 — BFS route-label generalization holdout, rule frozen from P140 (preregistered before P141/P142 outcomes)

2026-11-24 KST. The conditional policy in P141 was fit to P140's SHARE-specific outcome sign, and all earlier P135–P141 T2 policies have primarily reused label seeds86001/86002. Repeated new timestamp vectors under the SAME movement labels do not test route-label generalization.

## Frozen intervention (unchanged regardless of P141 outcome)
- Calendar map (0,30)→60, (15,0)→30, (7,15)→60, (23,45)→30.
- At ONLY (7,15), choose30 instead of calendar60 iff **configured left share <=0.50** and t84 queue Q=outside_A+outside_B+approach_A+approach_B+pocket_vehicles **>=14**. Else calendar.
- Identical thresholds, same source logic and score, no tuning based on P141.

## New evidence universe, unseen movement identities and timestamp roots
- NEW label seeds **86101,86102** and NEW timing seeds **89101,89102**; two timing families stochastic_uniform/stochastic_platoon4; left-share0.50/0.75. Total 16 demand tapes, four fixed relative-offset policy packages and 30/60 period options => **128 new T2 arms / 64 matched policy decisions**.
- Exact same P130 receiver separation 2+2, single global 2-second exit headway, S-first tie, t84 common checkpoint, 4800s horizon; 60 vehicles complete and all IDs/refusal logs validated.
- Choose using only t84 queue snapshot and configured share, not the future tape or posterior denial proxies.
- New route seeds affect route label arrangement and left count; these are different movement-labeled traffic realizations from P141. Geometry and synthetic engine remain shared.

## Primary out-of-label-distribution audit
- Regret vs previously frozen calendar-only, correctness, triggers, and full 30/60 fixed baselines; report share, family, offset, per-original-tape differences.
- Primary pass: at least 1 trigger, overall >=10% lower regret than calendar-only with both shares nonworsening and <=25% activated choices harmful. If P141/P142 disagree, treat it as a transfer failure (not a motivation to retroactively select a subset).
- All 128 arms, 60 IDs, cost and denial conservation and exact policy/checkpoint parity must pass, else INVALID. If no triggers then UNINFORMATIVE.
- Report both P141 and P142; do not pool them to hide a failure or claim independent intersection network evidence.

## Limitations
Configured turn share is an experiment setting, not necessarily observable by road infrastructure; no real-sensor design or SUMO individual exit parity. Negative results are informative and should be kept intact. Same engine is not independent external verification.
