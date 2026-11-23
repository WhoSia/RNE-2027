# P141 — prospective demand-conditioned prestate guard (new timestamp holdout)

Registered on 2026-11-24 KST BEFORE P141 time seeds 89001,89002 are examined or any P141 cost is evaluated.

## Prior evidence and outcome dependence
P139 receiver>=3 gate never activated (0/16 t84 checkpoints). P140 (88901/88902) adopted a t84 upstream+outside+pocket stock >=14 guard at offset(7,15); across 64 policy pairs its calendar regret4035 vs guard regret21875 and 2 helpful/6 harmful activations. **Post-hoc analysis revealed** both helpful activations occurred in share0.50 (2/2) and six harmful activations in share0.75 (6/6). This is a training observation, not confirmation. P141 rule was SELECTED BASED ON P140 REWARDS. We now freeze it before previously unseen P141 tapes. No after-the-fact threshold tuning.

## Frozen policy rule
Unchanged calendar map trained P136: (phi30,phi60)=(0,30)→60, (15,0)→30, (7,15)→60, (23,45)→30.

P141 conditional guard overrides 60→30 ONLY when ALL:
- offset package (7,15);
- demand parameter left_share <= 0.50 (left_share is an a-priori configured demand scenario parameter; it is **not** a physical detector output and cannot be assumed known in real-road deployment);
- Q at t84 = outside_A + outside_B + approach_A + approach_B + pocket_vehicles >=14, drawn from the public checkpoint_observation before either policy.

No other features or parameters. The comparison remains between **period-and-offset policy packages**, not a pure cycle-length intervention.

## Fresh holdout, unchanged network
- Frozen route label seeds86001/86002, time seeds **89001/89002**, stochastic_uniform/stochastic_platoon4, share .50/.75. Time seeds disjoint from P136, P137, P139, P140 (88601–88902), and XR1/P135 (88401–88408).
- Synthetic T2 P130 movement separated 2+2 receiver, single global 2-second exit headway, S-first tie arbitration, checkpoint t84 and horizon t4800, 60 vehicles complete per arm.
- 16 label/share/time/family demand tapes ×4 locked offset packages×2 signal policies = **128 planned complete arms, 64 matched comparisons**. Each of the 16 independent label+timing configuration tapes is reused 4 times across offsets. Route labels and timing generators are shared with training cohorts: NO independent road-network validation.
- Both arms run from EXACT SAME checkpoint; no post-treatment local proxy enters rule; trace denial attempts and denied tick count fully cross-checked. Preserve t84 checkpoint from mutation.

## Locked primary analysis and gates
- Primary: calendar-only vs P141 share-conditioned guard total regret across 64 paired policy contrasts; regret defined from fully cleared network vehicle-seconds. Compare correct period counts and fixed30/fixed60 benchmarks.
- Guard triggers >=1 within .50 share, otherwise `P141_UNINFORMATIVE_NO_TRIGGERS`.
- Required improvement: overall total regret at least **10% lower** than calendar-only, AND zero increase in regret within either share, AND no more than 25% of activated decisions harmful. If calendar regret=0, require guard regret=0, and label not a demonstrated improvement.
- Report results by share, offset, arrival family, and original 16 tapes; treat 64 repeated-arm comparisons as dependent.
- If full 60-ID clearing, service-event denial accounting, the unmodified checkpoint, or seed uniqueness fails, STOP invalid. If P141 fails, revise claim rather than tuning on these seeds.

## Separate next BFS gate
P142 must change **route-label seeds** as well as timestamp seeds (the prior 86001/86002 route cohorts have remained nearly unchanged across P135–P141), using fresh route seeds86101/86102 and time seeds89101/89102, with *this P141 rule frozen regardless of P141 result*. Do not interpret similar timing seeds with identical route labels as independent demand generalization.

## Limitations
Same synthetic engine, not calibrated real intersection; demand share supplied by experiment configuration; real-world turn share estimation may be noisy. SUMO XR3 individual exit timestamp parity failed; forbid SUMO policy-sign transfer until the XR7 parity gate is actually passed.
