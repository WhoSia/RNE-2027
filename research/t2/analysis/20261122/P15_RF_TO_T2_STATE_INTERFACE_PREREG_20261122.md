# P15 — RF tabletop labels are not automatically sufficient for T2 decisions

Date 2026-11-22 KST. Prospective *interface-level* plan, before any RF physical experiment or new T2 simulator result. Motivated by [김세호 independent audit](https://docs.google.com/document/d/15CFAM0QsRQkYNGUvf3VEyISxG9Pxyz-I_4WX32CAQp8/edit) and existing RF protocol. This is an untested hypothesis, not a discovered PHYS counterexample.

## What the RF label actually means
The RF laboratory labels are `no_demand`, `free`, `pocket`, `downstream`, `both`. They mean **manually staged tabletop conditions**. No label entails that real turning vehicles backed up, that an actual stopline could discharge, or that the physical receiver capacity matches a model variable.

## Projection contract — MUST define before connecting a measured classifier
Let `x` be a PHYS simulator state containing at least the upstream and pocket occupancies, pocket entrance availability, downstream storage, turn-route composition, and decision-time arrival/future-action assumptions. Let `z=h(x)` be an experiment-specific manually defined RF class. One class may map to many distinct states `W(z) = {x : h(x)=z}`; a physically realizable `h` has not been established.

A hypothetical perfect observation of `z` is **decision-sufficient for cost J and admissible action set A** only if
`intersection_{x in W(z)} argmin_{a in A} J(a,x)` is nonempty for all observed classes `z`.
For two abstract actions baseline vs treatment, let `delta(x)=J(treatment,x)-J(baseline,x)` and pre-fix a meaningful tolerance epsilon. A strict opposing-sign witness exists only when `inf_{x in W(z)} delta(x)<-epsilon` AND `sup_{x in W(z)} delta(x)>epsilon`, with the **same action definition** and genuinely compatible worlds.

This is a condition for common optimal actions across a compatibility set, not proof that all real road systems are identifiable/unidentifiable. It is also not equivalent to mutual information maximizing all state coordinates.

## Test ladder
1. Define `h` operationally using manually labelled physical occupancy, route and time. Do not equate a staged toy obstruction with observed queue spillback.
2. Independently produce illustrative pairs with identical `z` but different `x` (e.g. modest versus full pocket occupancy) and first report only state aliasing.
3. For any claim that **policy preference differs**, use *same abstract action*, P12-style declared action feasibility, P13 same-observation + epsilon test, and freshly sampled independent arrival groups. Different labels or route tapes cannot be silently equated.
4. Determine whether the learned RF signal `Y` depends on finer nuisance aspects of `x` even given `z`. A single pooled confusion matrix `P(Y|z)` may not transfer across changed mounting, material or within-class queue length.
5. Train only on designated placements/sessions; test empty vs moving vs stationary and pocket vs downstream with blinded independent truth. Compare RSSI and a cheap simple sensor against CSI. Report abstention and error.
6. Only then calculate conditional policy value, incorporating acquisition costs and *measured* errors instead of arbitrary RF07 percentages. An improved 5-class F1 score does not imply changed optimal signal action.

## Strong falsifiers and legitimate null findings
- The same `z` may always lead to a common optimal abstract action in the admissible PHYS cohort: then extra RF subclass information was not useful for that cohort and task.
- A static object may be indistinguishable from empty across unseen sessions: RF stationary occupancy claim fails.
- Two links may be confounded by position/metal volume rather than blockage source: source localization claim fails.
- A simple optical or marked magnetic sensor may outperform CSI: still a successful negative-control result.
- Even when RF infers a class correctly, an inadmissible intervention must never be counted as a benefit.

## Boundaries
All formal claims are conditional on a named model, admissible action set and observation mapping. Not an authorized physical test, a measured Wi-Fi camera, or a traffic-signal controller. No third-party Wi-Fi packet interception, live roads, K047 unsealing or handling the held CIM dataset.

Next step: implement a minimal exact mathematical fixture distinguishing **label aliasing** from **strict policy-opposition**, then use P13's existing screening contract as the comparator; do not inflate results with synthetic numerical examples disguised as field evidence.
