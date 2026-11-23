# P101 prospectively locked mechanism check on P100 held-out high-left-turn tapes

**Registered after P100 outcome, before P101 spatial replay.** This is a *second-stage mechanism audit on the already-tested same 64 tapes*; the outcome success 64/64 is known, so P101 must NOT be presented as a third independent replication.

## Fixed cohort and comparators
- Exact seeds 86001–86032 × clock families uniform and platoon4; left-turn share 0.75 fixed, 64 unique synthetic tapes.
- Recompute one checkpoint at t=84 with frozen P100 settings: 900s arrival tape, extended full model 1440s, receiver capacity 4 and left-first 6-second phase.
- For each tape, replay 30s and 60s downstream periods with both red-onset and green-onset. 64×2×2 = 256 arms. Compare all 128 onset pairs with `P100_RESULT.json` for exact signed cost, denied and full-red deltas.
- Reconstruct post-tick signed `outside/A/B/pocket/receiver` vehicle-seconds and separate left/through amounts. Verify **128/128 exact** five-zone and movement-by-zone conservation, plus receiver departure conservation and all 256 arms clear.

## Primary movement hypotheses (red-onset 64/64 confirmed cost paradox before this prereg)
1. At least **58/64** have *left-turn vehicle-seconds delta >0* (original P88 red paradox: 43/43).
2. At least **58/64** have *A-lane delta >0* and *B-lane delta <0*; count each separately and their conjunction.
3. Exploratory: fraction where through-vehicle delta <0 (original 39/43), and whether outside waiting delta >0 (original 35/43).
4. Green onset same 64 tapes is an internal paired comparator, not an independent sample. Report source P100 policy-cost signs and zone/movement deltas for both onsets.
5. Count any model/snapshot mismatch as FAIL, not missing or dropped case.

## Interpretation gate
These are only **mechanism repeatability tests within the same T2 synthetic engine**. Their success cannot establish a physical causal pathway at a real intersection. Next external evidence gate remains independent cross-engine and simultaneous field stopline/downstream discharge observations.
