# P137 prereg — Independent new-time-tape benchmark versus learned offset-only calendar policy
2026-11-24 KST. P136 outcomes were observed before this prereg. P136 had 35/64 30s wins and 29/64 60s wins overall, but EACH OFFSET PAIR overwhelmingly favored the same period, revealing an offset-stratum confound. The previous 35:29 balance is pooled mixture balance, NOT within-offset treatment equipoise.

**Frozen offset-only rule, trained on P136 and now LOCKED:**
- (phi30,phi60)=(0,30) -> period60;
- (15,0) -> period30;
- (7,15) -> period60;
- (23,45) -> period30.
This is legitimate out-of-sample evaluation ONLY if timing seeds 88701/88702 are not used to tune this mapping. (The sign by offset was observed on P136 seeds88601/88602.) Report it as a trained reference, not a zero-fit original design.

**Frozen new demand/time:** label seeds86001/86002; entirely unseen timestamp seeds **88701/88702**; families stochastic_uniform/stochastic_platoon4; left-turn share .5/.75. 16 route/time/share tapes (8 unique timestamp vectors per share, reused across shares), each 60 matched IDs.

**Topology/arms:** exact P136 S-first shared-global-exit split2+2 T2 fork, 2s exit clock, common t84 checkpoint, t4800 all-ID clearance. Four P136 offset packages frozen as above; period30/period60 per package. 16 tapes ×4 offsets×2 periods = **128 new T2 trace arms**, 64 policy comparisons.

**Proxies:** 3 untouched P136 rules (fewer receiver_denied_seconds, fewer refused attempts, fewer unique denied IDs; ties choose60). Evaluate total J, full regret to ex-post oracle, covered decisions, and compare with (a) P136-trained calendar-only lookup; (b) fixed period30; (c) fixed period60. Required subgroup reporting by offset, share, arrival family. Emphasize policy selection using post-treatment local proxy observed on BOTH alternative policy rollouts is *not operational online control*: at best a diagnostic comparing objective surrogates under full counterfactual simulation, unless a deployable predictor is developed.

**Primary falsifier:** if the best P136 local proxy rule fails to reduce regret below the **frozen calendar lookup** on the unseen P137 tapes by >=10%, reject the claim that that local proxy offers *additional* useful policy selection beyond the offset label in this T2 world. Do not hide failure in pooled balanced statistics; full prespecified cohort. No statistical independence from shared route seeds; no external SUMO/field transport.

**Integrity:** 60-ID complete for each arm, same tape within each pair, exact service refusal counts and denied seconds match trace events. If any fails, P137 run invalid.
