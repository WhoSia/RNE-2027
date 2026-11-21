# Independent adversarial audit — T2 PHYS-01–11
2026-11-21 · second-pass internal critical review · NOT a new prospective field validation

## Top-line judgement

The matched-state checkpoint comparison and byte-identical code/results provide
strong evidence of **internal simulator implementation consistency**. They do
not establish realistic road dynamics, physical/controller feasibility, empirical
calibration, or general policy superiority. We should stop equating counts of
synthetic runs, self-authored tests and hashes with independent scientific
validation. The current most defensible research question is **whether
observations distinguish policy-relevant, physically feasible traffic worlds**
and how much additional information actually reduces minimax regret.

## A. Correct the PHYS-10 zero-distance claim

Existing outcome: evaluation seed76 (1800 vph, 45% left, receiver4,
bay14m, B share0) had the **exact same six count-feature values** as
training seed3 (1800 vph, 50% left). The k=5 learner estimated
ΔJ=-30.2; held-out true ΔJ=+306. Its cost decomposition:
outside -90, upstream +290, receiver -14, remaining +2 vehicles x60=+120.
With penalty0 it is still +186. This is a robust *realized cost effect*
within that synthetic world, **not** an intrinsically unsafe road event.

CRITICAL LOGIC CORRECTION: the matched training seed3 had actual ΔJ=0,
not a negative ΔJ. Thus it is **not** a strict opposite-optimal-policy
witness; baseline is a common weak optimum. The feature alias proves
that realized effect magnitude is not determined by the six counts,
not by itself that any additional sensor is essential for choosing a
common robust action.

An explicitly exploratory 2×2 splice tested two microscopic histories
(before t84) against two *future route tapes* (from t84 onward), keeping
the 1800-vph arrival timestamps fixed and branching each policy from
an identical world checkpoint:

| Prefix microstate | Future route tape seed3 | Future route tape seed76 |
|---|---:|---:|
| Seed3 (left share .50) | 0 | 0 |
| Seed76 (left share .45) | 0 | +306 |

Each prefix's frozen t84 state bytes were identical under either future
tape, so future observations were not leaked. This is a **joint
interaction of the microscopic history and future traffic tape** in a
known selected case, not a prospective discovery. The matrix itself
contains no negative policy ΔJ. Source:
\`research/t2/physical_checkpoint_alias_factorial_audit.py\`,
\`test_physical_checkpoint_alias_factorial_audit.py\`.
Local 2×2 JSON SHA-256
\`578515956482c250e8733054478b1542c9490fd4f1dce928e71fa7316403e32e\`.

A separate *exploratory re-scan* of PHYS-10 demand1650 found exact
counts matches at receiver2/B share .5/pockets14,28,70m:
seed73 ΔJ=+1 vs seed78 ΔJ=-179. The positive margin is **only
1 vehicle-second**, and the three rows share the same two demand
seeds, so this is one fragile independent contrast repeated at three
bay lengths, not three strong external policy-rank reversals. A
meaningful threshold ε and new independent seeds would be required.

## B. Much less arrival-time diversity than seed labels imply

\`spatial_v10.arrivals\` under \`arrival_pattern='uniform'\` chooses
arrival timestamps via deterministic integer floor counts. Across
seeds0–15 at 240s and each fixed 1350/1650/1800/1950/2250 vph,
there is **exactly one unique timestamp sequence**; only turn labels
vary with seed. The 1800-vph world always has 120 vehicles over
240s; 1650-vph always has 110. B-lane assignment uses further seeded
randomness, but there is no stochastic headway/platoon timing variation
inside the 'uniform' regime.

Therefore seed-block uncertainty is about a narrow pseudo-random route/
lane-allocation generator, not arbitrary real traffic arrivals. Even
disjoint test seeds do not validate unseen day-to-day timing patterns.
Report the true randomization level explicitly before promoting future
seed-based generalization claims.

## C. Operational feasible-action gate remains unclosed

The PHYS-04–11 intervention at tick84 substitutes a 3-tick red interval
and 4-tick L green. The baseline at t84..87 has through S green; the
baseline from 88..119 is red. Hence the treatment effectively exchanges
**four through-green ticks for four isolated left-green ticks** at
t87..90. The engine enforces red separation before conflicting active
movements, but does **not** implement yellow transitions, locally
applicable minimum phase green, pedestrian timing, conflicting
cross-street phases or controller actuation constraints.

The isolated 4s green may be inappropriate for an actual signal plan,
but no jurisdiction-specific minimum can be asserted without the
relevant standards and site layout. The FHWA signal timing manual
describes the missing parameters and calibration requirements; its US
guidance is not Korean operational authorization:
https://ops.fhwa.dot.gov/publications/fhwahop08024/chapter5.htm

The internal Notion T2 Harvest H06 (2026-11-02) had already shown a
previous non-identifiability witness disappeared under feasible signal
constraints: https://app.notion.com/p/40cef561cf928117bd9fcef033c79b33
This MUST be treated as a warning, not forgotten prior work.

## D. Novelty, effective sample size and internal validation

Notion H25 (2026-11-03) had previously documented aggregate-equivalent
states with different response to a synthetic controller guard:
https://app.notion.com/p/40def561cf9281a7923ef4542af30094
The new PHYS-10 case has different geometry, state, action and outcome,
but not a newly discovered general fact that aggregate matching can
hide mechanism-response differences. Prior-art positioning is OPEN.

For PHYS-10, across the 576 clean-observation cases, the counts-based
OOD-gated learner **treated 355**, among which **39 had positive
ΔJ, 225 negative ΔJ and 91 tied**. The training-support region
is not a nonharm certification. Across all four mild regime shifts,
OOD rejected 54 states but blocked 46 potentially beneficial candidate
treatments and just 2 harmful ones. These are synthetic retrospective
diagnostics, not calibrated risk probabilities.

For PHYS-11, 1-tick default confirmation had 15 beneficial versus
33 tied cases out of 48, but only **8 independent seed blocks**.
The 15 nonzero outcomes concentrate in seeds82/83/86, not 15
independent demand-day observations. Results under 2/3-tick confirmation
remain conditional on the same deterministic arrival-clock generator.

The repeated JSON SHA and internally generated test expectations
establish reproducibility and regression consistency, NOT physical
validation. A 5-file exact-core blob comparison does not equal a
full repository clone/integration acceptance.

## E. Confirmed software bug and minimal regression repair

\`dual_lane_v11.run\` accepted \`checkpoint_at=0\` but rejected
\`resume_from\` of that very snapshot because of \`0<first_tick\`.
Additionally, Python booleans were accepted as integer checkpoint
ticks. Both issues were reproduced with a failing test and repaired:
- initial tick0 is now a valid resume boundary,
- \`checkpoint_at=True/False\` and forged boolean ticks are rejected,
- existing t1/t84/t239 checkpoint replay, trace/no-trace and
  confirmation1/2/3 were tested.

GitHub engine blob after fix: \`a7c9aa6954402e12894d1d5b722e8a474b0bd58f\`.
New regression-test blob:
\`30103a6faa216ae5fcc76cc4f091c175763ae3e5\`.
Local latest PHYS-specific test suite **41/41 passed** plus separate
local core-contract tests **8/8**. **Full repo historical tests
remain unexecuted**. The bug is not evidence of an error in
the t84 matched-state results; do not overstate its impact.

## F. Program-level corrections and next falsification

1. **Freeze an operationally admissible action set first:** clearly
   distinguish abstract mathematical signal actions from candidate
   controller plans with minimum green, yellow, red, pedestrian and
   movement-conflict constraints. Compare the existing t84 witness
   against feasible alternative plans, not more arbitrary 4-tick green.
2. **Restore stochastic demand timing:** vary independent time-headway
   and pulse patterns with route-composition seeds. Cluster inference
   by independently generated arrival histories and validate on
   unseen timing generators, not only unused integers at fixed timestamps.
3. **Replace approximate support proximity with identification sets:**
   given decision-time observation o, define a physically feasible
   compatible-world set W(o), then report
   L(o)=inf_w ΔJ(w), U(o)=sup_w ΔJ(w).
   A strict opposite-sign witness demands L<-ε and U>ε, with a
   prespecified meaningful ε. If all ΔJ≥0, baseline is a common weak
   optimum and no extra sensor is needed for that simple decision.
   Distinguish policy ranking identification from predicting individual
   realized treatment magnitude.
4. **Connect to field evidence:** use only legally available, unsealed
   DLR/CityArtery evidence to validate route, clearance, movement and
   queue features. A few signal-head-linked trajectories are NOT yet
   a verified positive sample of left-turn spillback. Keep K047
   18:00–18:30 UTC sealed.
5. **Reduce artificial research churn:** consolidate the PHYS series
   into a single reproducible evidence map and 2–3 decisive experiments,
   including negative results and original literature comparison,
   rather than multiplying test counts or simulator knobs.
6. **Clean document authority:** \`START HERE\` contained historic
   references declaring \`research/t2-spatial-fig2-v02\` active and
   \`main\` unmerged; a 2026-11-21 dated correction was inserted at
   its beginning without deleting historical content. The README
   \`main\` instruction takes precedence.

This is a critical internal review and exploratory numerical audit, not
an independent paid-model replication, a new blinded holdout, a
clinically/legally certified controller, or an empirical finding.
