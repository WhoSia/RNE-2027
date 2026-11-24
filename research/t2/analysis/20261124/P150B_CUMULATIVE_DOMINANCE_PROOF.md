# P150B — cumulative-flow dominance and non-invariant policy ranking

## Claim and scope

For the P150A two-cell tandem, with fixed exogenous arrivals, upstream signal, downstream sink service, integer capacities, old-stock departures and upstream admission, enabling immediate reuse of downstream exit space weakly reduces the total stock integral at every common finite horizon. This is a theorem for the stated recurrences, not a theorem about all CTMs, movement sharing, realistic car-following, or real signals.

## Proof

Let A be the cumulative number of exogenous arrivals (including the new arrivals for the current step), E the cumulative entry into the upstream cell, F cumulative movement into the receiving cell, and Z cumulative exit. Start with the same empty state in both conventions; the old stocks are e=A_old-E, u=E-F, d=F-Z. Let U,D be positive capacities, s=min(sink,2), and g the binary upstream gate.

The stock updates of P150A give the equivalent cumulative recurrences:
- E' = min(A, E+2, U+F).
- Z' = min(F, Z+s).
- If g=0, F'=F.
- If g=1, old-space convention F'=min(E,F+2,D+Z); reuse convention F'=min(E,F+2,D+Z').

Admissible states satisfy Z<=F<=E<=A and Z' >= Z. Each right-hand side is coordinatewise nondecreasing in E,F,Z (A,s,g fixed). At the same admissible state the reuse map is coordinatewise no smaller than the old-space map: E',Z' agree and the F' supply term is no smaller. Starting from equal states, induction yields E_reuse>=E_old, F_reuse>=F_old, Z_reuse>=Z_old at every tick. All maps preserve admissibility by the stock conservation and capacity constraints. Total outstanding stock after each step equals A-Z'. Hence the reuse total stock integral is no greater for every common horizon. No clearance assumption is needed for the weak inequality; clearance is verified in the experiment.

## Why the policy ranking still changes

The dominance applies to one fixed signal and sink schedule, not to a comparison of different schedules. For policy a and b define cost reductions r_a=J_old(a)-J_reuse(a)>=0 and r_b likewise. Then Delta_reuse=Delta_old-r_a+r_b. No bound here forces r_a=r_b. Thus sign reversals are compatible with monotonicity for every fixed policy.

P150A witness: uniform tape, receiving capacity 2, 4-tick phase 0 versus 8-tick phase 6.
Old-space costs 372,336; reuse costs 196,336. Delta changes +36 to -140 vehicle-ticks. Both conventions conserve all 24 vehicles. The 98 strict cost decreases and 118 ties across 216 matched arms are consistent with the theorem, rather than independent proof of it.

## Evidence boundary

The proof relies on monotone scalar tandem flows, same exogenous input and fixed schedules. It does not apply automatically to movement-specific FIFO with interacting queues, adaptive state-dependent signal choices, or distinct physical travel times. The Go implementation uses cumulative flows and independently agrees with the Node stock implementation on 432 rows (native byte parity); agreement does not establish physical validity. This is a handwritten mathematical derivation, not a proof-assistant-checked theorem, and no novelty claim is made.
