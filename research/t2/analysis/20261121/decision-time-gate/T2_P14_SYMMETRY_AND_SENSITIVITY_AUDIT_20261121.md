# T2 P14 — Structural symmetry and post-hoc sensitivity audit

Date: 2026-11-21. Conducted **after** P14's first 100-world screen. Exploratory, not a registered confirmatory study.

## Key correction: 39 versus 39 is a label-exchange symmetry
For queues A,B with *identical capacity and cost coefficients*, let T(a,b)=(b,a). Let J_AABB(a,b) and J_BBAA(a,b) be the two abstract service costs. The implementation satisfies:

J_AABB(a,b) = J_BBAA(b,a), and J_BBAA(a,b) = J_AABB(b,a).

Therefore Δ(a,b)=J_AABB(a,b)-J_BBAA(a,b) = -Δ(b,a).

The 100-world cohort contains every pair (a,b) together with its swapped partner (b,a). Consequently, the numbers of strictly negative and positive Δ **must coincide**. Their equality is *not* an independent empirical finding, sample-frequency estimate, or strong evidence of controller robustness. An exact independent regression test was added to the final P14 test file and run across all 100 worlds: **14/14 local unit tests pass**.

## Post-hoc stress matrix
A grid of 3 queue capacities (1,2,3) × 3 invented lost-vehicle penalties (0,5,10) × 3 terminal-weight penalties (0,2,5) = 27 parameter worlds; each evaluates the same 100 arrival tapes. All 27 settings preserve the antisymmetric sign pairing.

- Capacity 1: 40–45 negative and equally many positive; 10–20 ties. Extreme |Δ| ranges 4–29 depending on weights.
- Capacity 2 or 3: 39 negative, 39 positive, 22 ties throughout the weight grid; |Δ| maximum 7,11,17 as terminal penalty is 0,2,5.
- The capacity2/3 equivalence arises because four total arrivals, two per lane, never produce more than two waiting in any lane under this miniature experiment; increasing capacity past two does not alter outcomes.
- The lost-vehicle penalty has zero effect at capacity>=2 in this particular cohort, as no arrivals are discarded.

All these results are model-dependent and selected after first findings. None is a T2 PHYS engine run or independent empirical validation.

## Reproducibility
Main source exact Git blob `65005b44e02998985597946956cbf1c3005ffb56`, source SHA256 `802e1b6de87efebb222136d7be9b2380905061e49d67a245135f1c19851c5cd6`.
Final 14-test exact Git blob `5e58d3b742a49ee9d71f8bceabab4608d9de6aef`, test SHA256 `f55e5ef46189868c6d1b47fa12009349a382877ed0e9364a9c51303539a42f9a`.
Results JSON Git blob `6c99b9cadcdaa96d650b32133c0d428fe56d4063`; SHA256 `b11fdb8bca7c320e5a20615c1b01ac36ab30984ae661c7be6c45389b5078faf5`.
Each exact Git blob was re-fetched from GitHub `main` and agrees with the locally executed file's git hash-object.

## What a stronger experiment needs
Break the uninformative symmetry using physically justified asymmetric storage, unequal movements, conflicts, or measured demand distributions — but **pre-register the mechanism**, don't manufacture novelty from artificial parameters. Then import into exact PHYS source and compare model-independent outputs. Preserve negative results and group on truly independent arrival histories.

No actions on real traffic infrastructure. K047 sealed, CIM dataset held, GitHub Actions unused.
