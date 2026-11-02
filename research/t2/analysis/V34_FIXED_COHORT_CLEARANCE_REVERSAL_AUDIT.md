# T2 v3.1 — SAME COHORT clearance falsification (executed 2026-11-02)

Original v3.0 engine unmodified. Fixed arrival cohort generated only for t=0..449; each policy uses same arrivals for 450, 900 or 1800 seconds of simulation. Seeds 0-3, link capacity 4/12, main arrival probabilities .35/.7, side .15/.4 = 32 scenarios × 3 horizons × 2 policies = **192 runs**. ID conservation and generated count held in every run; no new arrivals after 449s.

Mean completed trips fixed vs pressure heuristic: 450s 185.1875 / 188.875; 900s 331.28125 / 351.65625; 1800s 451.46875 / 462.3125. Mean unfinished: 450s 296.4375 / 292.75; 900s 150.34375 / 129.96875; 1800s 30.15625 / 19.3125. Mean total vehicle-in-system-seconds across horizon: 450s 69220.25 / 67402.625; 900s 167636.1875 / 159691.375; 1800s 232355.3125 / 210880.28125.

**Crucial correction:** The earlier v3.1 horizon sweep regenerated demand throughout each horizon and showed a fixed/pressure mean ranking reversal at 900 and 1800s; this matched-cohort clearance test does NOT show that reversal. Instead pressure heuristic wins on mean completed and vehicle seconds under this cohort, demonstrating strong sensitivity to demand-generation protocol. Neither result establishes formal Max-pressure optimality or field effect. Fixed signal's nonexistent origin0 side green and unmatched service semantics remain serious confounding factors. No bootstrap/CIs yet.

Reproduction source and CSV in local v3.1 bundle; GitHub source synchronization and Drive upload of v3.1 bundle pending. Next repair invalid phase action set and compare under fixed and streaming arrivals separately.
