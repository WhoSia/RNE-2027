# RF06-D — Ideal sensor information versus hypothetical policy regret

**Date:** 2026-11-21. **STATUS: EXECUTED EXACT MATH ON INVENTED COSTS — NOT A REAL T2 TRAFFIC POLICY.**

## Preregistration and provenance

[Pre-registered cost signs and all six expected conditional decisions](RF06_POLICY_INFORMATION_VALUE_PREREG_20261121.md) in GitHub commit `220ec3b1c03659feb07d62aa1ee41827ad8a0105` *before code/results*. The four equiprobable microscopic toy states are P,D bits. Observations are those same ideal/noiseless **conceptual** channels from [RF06-B](RF06_CAUSE_OBSERVABILITY_PREREG_20261121.md), including manufactured logical OR called `any_rf_change`; this is NOT CSI, wireless propagation or a real magnetometer. Two abstract actions have toy cost differences `+3` if P=0 (an invented harmful treatment), `-2` if P=1 (an invented beneficial treatment), and baseline 0 regardless of state. **These units are NOT seconds, vehicle delay, safety or PHYS ΔJ**.

The best action for each observed signature is frozen as the lower conditional expected cost, with a tie choosing baseline. The oracle is allowed the full microscopic P,D state and is the *in-sample theoretical lower bound*, not a usable controller.

## Exact results from the executed four-state source

| Information available | H(ideal observation) bits | Expected fake action cost relative baseline | Regret vs perfect-info oracle |
|---|---:|---:|---:|
| No sensor | 0 | 0 | 1 |
| Global static motion-only event bit | 0 | 0 | 1 |
| Ideal total blocked count Y=P+D | 1.5 | -1/2 | **1/2** |
| Ideal pocket probe P | 1.0 | -1 | **0** |
| Ideal global obstruction OR(P,D) | 0.811278... | -1/4 | 3/4 |
| Ideal downstream-only D | 1.0 | 0 | 1 |
| OR plus P | 1.5 | -1 | **0** |
| Y plus P | 2.0 | -1 | **0** |

The perfect full-information oracle cost is exactly **-1**. For the Y=P+D channel, observed `Y=1` aliases `(P,D)=(0,1)` and `(1,0)`; conditional invented treatment deltas are +3 and -2, so choose baseline and miss the pocket-only beneficial state, raising regret to 1/2. For the pocket probe, both `P=1` states receive the invented treatment, oracle regret0 despite lower H(Y). This demonstrates **task-relative information value ≠ overall state information**. The OR+P channel can have *nonzero four-state classification error* yet **zero policy regret**, since D identity is irrelevant to the made-up costs.

For nonuniform toy prior weights (7,1,1,1)/10, no-sensor regret is exactly 2/5, not the uniform1. This is a prior-dependent decision property, not a universal sensor ranking.

## Executed validation/integrity

- Python **3.13.5** local `python -m unittest -v test_rf_policy_information_value_toy.py test_rf_cause_observability.py`: **20/20** passed, 9 new policy-value tests and 11 RF06-B observability tests. This is a local RF06 mathematical-subset run only, not previous RF01–05/full T2 integration rerun.
- [Executable code](rf_policy_information_value_toy.py): local executed Git blob `469ba0d9b4632c4bffc5b94664f73ec44621892f` equals fetched GitHub main blob.
- [Tests](test_rf_policy_information_value_toy.py): executed Git blob `46ec6fe8ba31e0962e3466348dc31453a7370920` equals fetched GitHub main blob.
- [Deterministic exact JSON](rf06_policy_value_results.json): executed local SHA256 `1ed6814f57b5520cd4fcc9a318a5733832b6770ca7c73bfbcd8d6f40f8a06d7c`, local Git blob `a02c16605a83bb0a517907c675c1856b0705fbeb`, equal to remote GitHub main blob. The output explicitly marks `ARBITRARY_HYPOTHETICAL_COSTS_NOT_ACTUAL_T2_DELTAJ`.
- No hardware, road, dataset, unseen field holdout, external controller, package install, GitHub Actions or bot work. K047 sealed; `CIM dataset.zip` downloading on an external shared Drive is **unopened/unqueried/unmoved**.

## Correct relation to the old T2 traffic simulator

The old T2 PHYS policy assessment depends on microscopic predecision queues, arrival-time stochasticity, finite downstream reception, signal phase semantics and route tape, and lacks complete real-world controller constraints. This toy uses **NONE** of those policies, costs or physically real signal actions, and does not establish any compatible-world opposite optimum under the same six-count t84 T2 observation. Earlier arrival-clock stress showed 10 strict policy-sign differences only across **different** pre84 states/observations; that limitation remains.

**Direction:** in the actual traffic simulator, only after validating the source-specific sensor confusion and physically admissible actions should one measure `expected regret under P(real sensor observation | real cause)`. Treat sensor placement as a **task-specific design** with condition-on-action information, not a general classification/maximum-bit contest. Even an idealized low regret under a made-up policy table is no evidence of field safety or implementable timings.
