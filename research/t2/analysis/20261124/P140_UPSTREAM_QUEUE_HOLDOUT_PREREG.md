# P140 — pre-decision upstream-queue threshold, fresh 88901–88902 holdout

Timestamp (KST): 2026-11-24. Locked BEFORE inspecting new P140 demand tape outcomes, checkpoint features or simulator costs.

## Motivation / what has changed from P139
P139 was preregistered with an offset-specific guard requiring receiver_vehicles >=3. Actual no-outcome preflight of its 16 frozen t=84 checkpoints found receiver_vehicles=0 in **16/16**, so the guard never fires. This is `P139_UNINFORMATIVE_NO_TRIGGERS_PREFLIGHT`, not evidence for or against state-conditioned control. Its original protocol and code stay unchanged, and its result file explicitly reports no 128-arm P139 simulation completion (two initial debug arms were run separately).

P140 must use an observed **pre-treatment** variable with nonzero support, without retroactively tuning P139. The P139 *checkpoint-only* sample has combined upstream/pocket stock between 8 and 19 vehicles; no P139 post-policy reward was used to select the cutoff.

## Locked hypothesis and zero-fit queue guard
Keep the P136→P137 frozen calendar-only policy map:
- (phi30,phi60)=(0,30): choose period60;
- (15,0): period30;
- (7,15): period60;
- (23,45): period30.

For only (7,15), override **60→30 if and only if** at t=84
`Q=outside_A+outside_B+approach_A+approach_B+pocket_vehicles >=14`.
No override at other offsets. Threshold14 is an *a priori heuristic informed only by P139 prestate feature support* (8–19) and not a fitted optimum. Do not change it after looking at P140 performance.

## New independent timing seeds, same synthetic environment
Use time seeds **88901 and 88902**, which are disjoint from P136 88601/88602, P137 88701/88702, P139 88801/88802, XR1/P135 88401–88408. Label seeds86001/86002, left shares 0.50/0.75 and timestamp generators stochastic_uniform/stochastic_platoon4 are reused; this is NOT independent geometry or independent route label sampling. 16 label/share/time/family tapes, four frozen phase packages, period30 and60 arms = **128 complete T2 simulations, 64 paired decisions** planned.

Topology unchanged: P130 movement-separated L/S 2+2-cell downstream links, **single global 2-second exit headway, S-first** exit tie. Same checkpoint t84 for both arms within tape, complete60-ID terminal exit by t4800, full denial event logs and integrity checks. The only features read by the decision rule are the six basic integer counters from `checkpoint_observation(cp)`, before either arm runs; no future arrivals or post-intervention denial time.

## Primary endpoint and gates (preregistered)
- Compare **P140 upstream guard versus frozen calendar map** on identical 64 matched policy choices; regret is `J_selected - min(J30,J60)`, where J sums whole-network vehicle-seconds.
- Report total regret, accuracy, number of *activated guards*, guard helpful/harmful/tied decisions, and the (7,15) stratum separately; also fixed30 and fixed60 benchmarks. Only four offsets per same tape; report aggregated regret comparison on 16 original tapes, by share/family, not naive 64 independent real intersections.
- Favorable primary gate: guard activated at least 4/16 cases of the target offset, total P140 regret **at least 10% lower** than calendar-only; AND guard regret in each left-share stratum <= calendar stratum regret (zero-calendar-regret stratum must stay zero). If no activations, mark `UNINFORMATIVE`, and on any unit/integrity failure mark `INVALID`.
- If gate fails, retain result as a genuine falsification of **this frozen threshold**, not evidence that no pre-treatment state can ever improve phase decisions.

## Adversarial limitations
P136/P137 have already revealed near-pure offset-stratum policy rankings. 30 versus60 arms also differ by **phase origin**, not only cycle period. Calendar map trained on P136; on P140 it is an out-of-sample comparator. This test measures the value of a very simple queue guard *inside the same uncalibrated T2 simulator*, not a real traffic controller. Never transport without SUMO E0e exit parity.
