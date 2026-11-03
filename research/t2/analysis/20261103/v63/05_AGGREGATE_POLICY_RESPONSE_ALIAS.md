# T2 v6.3-P0 — aggregate-observation alias / policy-effect counterexample
Study date 20261103; verified by replayable script alias_audit_v63.py and the v6.2 engine. Not real-world evidence.

Grid: 3 traffic demand labels × 3 brake strengths × 2 lateral acceleration constraints × 8 OD seeds × 2 green-end guards = 288 simulator executions. Hold demand, OD seed, and base policy (0-second guard) constant. Compare 6 motor parameter configurations in each 24 demand×seed stratum: 24 * C(6,2)=360 model pair comparisons.

Define aggregate observation O(theta)=(number generated, number completed, cumulative vehicle seconds), in finite 180-second run. 8 pairs agree exactly in these three observables.

One of the 8 equal-observation pairs has different *response to the same policy change*:
- demand balanced, seed 406, lateral acceleration cap 2.4m/s².
- theta_A: braking cap 2m/s²; theta_B: braking cap 3m/s².
- O_A = O_B = (37 vehicles, 12 vehicles, 3144.75 vehicle·seconds).
- switch guard from 0s to 1s: delta exposure theta_A = +137.0 vehicle·seconds, theta_B = 0.0.

**Careful formulation:** O_A=O_B does not imply ΔJ_A=ΔJ_B for this limited observation operator O. This is not proof of structural non-identifiability, universal equivalence, distributional equivalence, or a **policy ranking reversal**. All data are deterministic within fixed synthetic OD streams. It raises a falsifiable observation-design question: can richer queue/trajectory/entry-speed outputs distinguish the pair before a different policy is applied?

Next gate: prospectively fix the two parameter states and test multiple previously unseen OD seeds; then add observation channels sequentially with within-scenario holdout, rather than selecting a better-looking policy ex post. Distinguish better observational resolution from additional model assumptions.
