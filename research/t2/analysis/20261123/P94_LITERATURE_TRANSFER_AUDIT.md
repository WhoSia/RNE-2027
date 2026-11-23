# P94 — Literature-transfer and capacity-aware selection audit (2026-11-23)

## Question and evidence levels
Does a queue-pressure or 'fewer blocked seconds' heuristic guarantee that usable green serves more vehicles when downstream road storage is finite? **No.** The archived P87 data already furnish 55 cost-increasing despite denial-decreasing pairs; P91 establishes that 51 of those also have fewer full-red seconds. P94 only provides **algebraic, single-tick feasibility counterexamples**, not an improved traffic signal controller or network stability proof.

## Paper 1 — Varaiya (2013), full text inspected
Pravin Varaiya. *Max pressure control of a network of signalized intersections.* Transportation Research Part C 36 (2013): 177–195. DOI: 10.1016/j.trc.2013.08.014.
Full text at https://www.researchgate.net/publication/259138901_Max_pressure_control_of_a_network_of_signalized_intersections

- Assumptions from abstract and Section 3: independent exogenous arrivals, fixed turn ratios, separate movement queues, stage-specific saturation rates and **initially unbounded point-queue storage**; prove mean queue stability (throughput optimality for admissible demands), not a guaranteed ordering of finite-horizon travel times for P87.
- Section 4.5 explicitly notes that the unbounded vertical-queue model excludes real downstream saturation that prevents upstream flow; introduces discussion and examples of bounded-link blocking and gridlock. This *does not* automatically validate the four-cell T2 model.
- Section 4.6 explicitly says the controller considered chooses **splits**, whereas **cycle length and offset are to be determined separately**. This is directly relevant: P85–P89 alter offset/period, so a bare max-pressure stability result does not answer P87 cycle ordering.
- Section 5 offers instability counterexamples to plausible local controls; one must compare mechanisms, not infer performance from controller name.

**T2 implication:** Existing P39 `pressure_proxy` is a local heuristic and must never be described as a fully implemented, theorem-backed Varaiya MP controller. The T2 receiver is physically bounded and admits only when cell zero is unoccupied.

## Paper 2 — Gregoire et al., accessible abstract/figure captions, NOT full-equation verification
Jean Gregoire, Xiangjun Qian, Emilio Frazzoli, Arnaud de La Fortelle, Tichakorn Wongpiromsarn. *Capacity-Aware Backpressure Traffic Signal Control.* IEEE Transactions on Control of Network Systems 2(2), 164–173. DOI: 10.1109/TCNS.2014.2378871.
https://www.researchgate.net/publication/257028475_Capacity-Aware_Backpressure_Traffic_Signal_Control

- Abstract/figures identify non-work-conservation and congestion propagation as failures of naive backpressure with **finite** capacities. Proposes a normalized pressure form and contrasts stable versus gridlocked examples.
- We have **not** verified the normalized pressure formula line-by-line in the full article. P94's simple capacity gate must NOT be presented as its implementation.

## Paper 3 — Han et al., abstract and accessible indexed summary, NOT full methods
Yu Han et al. *Field-tested signal controller to mitigate spillover using trajectory data.* Computer-Aided Civil and Infrastructure Engineering 39(9) (2024): 1354–1369. DOI 10.1111/mice.13144.
https://doi.org/10.1111/mice.13144

- Published study reports optimization with phase-duration/variation constraints, CV trajectory input and a field evaluation near Beijing Capital International Airport, including estimated CV penetration of roughly 5–10%. The exact before-after field performance, detector bias and intersection transfer cannot be independently audited from the accessible snippets here.
- T2 P80–P81 downstream-end observation gap means trajectory presence near an entry is not verified final downstream departure. A field study without the end-of-link events does not resolve this mechanism.

## Papers 4–5 — candidate constraints, abstract-level only
- *Estimation of Saturation Flow Rate and Start-Up Lost Time for Signal Timing Based on Headway Distribution* (2015), DOI 10.1155/2015/304823: field headways from 920 queues, evidence that startup loss and saturation behavior vary with queue position/length. Abstract-level review; reinforces why P89 2s service-mask is not a calibrated field discharge curve.
  https://onlinelibrary.wiley.com/doi/10.1155/2015/304823
- *A max pressure algorithm for traffic signals considering pedestrian queues* (2025 journal item): adds pedestrian waiting to control-state/pressure rather than treating vehicle delay as the complete objective. Abstract-level review; no numerical T2 implementation or validation.
  https://www.sciencedirect.com/science/article/abs/pii/S0968090X24003863

## P94 implementation and independently checked findings
Code: `p94_capacity_gate_screen.py`. Exact results: `P94_RESULT.json`.
Assume **two mutually exclusive stages** A and B, separate receiver capacities 4, upstream queues q, downstream occupancies o, pressure proxy `q-o`; one possible admitted vehicle per tick. Compare naive argmax pressure to argmax among **currently feasible** discharges (q>0 and o<4).

Six preregistered controller states: the naive selector attempts a physically impossible move in **two deliberately constructed cases** (`blocked_dominant`, `blocked_B_dominant`), whereas the gated selector admits one. Two cases both choose a useful stage, two cases have zero feasible service (both full/no demand). Aggregated one-tick feasible admissions are 2 for naive vs 4 for gated **over this purposely selected six-state unit suite**. A second event-free Python decision oracle independently matched all six stage choices and admissions.

This is **not** evidence for a 2x real-world throughput improvement. It lacks downstream release, arrivals over time, transition/lost times, fairness, safety, pedestrians, and feedback dynamics. The gated rule is not claimed to be any cited paper's exact controller.

## Scientific objections and next gate
1. **Confirmation-biased states:** P94 contains intentionally adversarial states, not a sampled prevalence; use a held-out state distribution and sequential transition model before any performance comparison.
2. **Competing users:** A movement blocked now might be valuable later; a feasible movement now can still cause downstream harm. Include conflicting-direction queues, pedestrian clearance and max wait as constraints before policy ranking.
3. **Controller definition leakage:** The present heuristic uses a one-step `q-o` score and independent downstream links. No stability theorem transfers from Varaiya/Gregoire to T2.
4. **External validity:** None of the above replaces P80/P81's missing observed downstream exits. Preserve missingness instead of imputing service.
5. **Full P88/P89 pending:** The previous code commits, one mini P93 fixture and P94 one-tick tests are **not** a run of the 384 full P88/P93 simulation arms or 768 P89 paired comparisons.

## Priority update after completed BFS P94
- **0.97** real simultaneous phase/turn/head/stopline/downstream exit observation (unchanged; missing identification).
- **0.96** P88/P93 actual 192-pair spatial and left/through accounting, including receiver discharge (unchanged; highest feasible synthetic mechanism test).
- **0.93** P89 0/1/2/3-second startup sensitivity with observed discharge headways (unchanged; requires complete simulation).
- **0.92** pedestrians/conflicting movement queues and explicit maximum-wait/clearance constraint (raised from .89; supported by full-user evaluation gap and pedestrian MP literature).
- **0.88** capacity-aware signal controller comparator under finite links (added after P94; defer until baseline and objective are validated).
- **0.86** detector-error-aware actuated gap-out and min-green control (deferred for measurement and safety constraints).
- **0.85** new seeded platoon/offset holdout and independent engine reconciliation (unresolved).
These are **ordinal research-resource allocations, not probabilities**; do not escalate controller comparison above reproduction until source-locked conservation passes.
