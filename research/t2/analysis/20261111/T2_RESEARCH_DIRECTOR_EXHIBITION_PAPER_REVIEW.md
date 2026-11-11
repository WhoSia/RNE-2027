# T2 Research Director Review — 2026-11-11
## Exhibition track vs academic publication track: evidence-first decision

**Decision: CONTINUE T2, FREEZE NEW FEATURE EXPANSION. Field stopline/queue adjudication + true engine physical repair + independent SUMO are critical-path.** Do not claim field traffic-policy superiority or award likelihood.

### Evidence chain reviewed
Original archived conversations `20261027.md`, `20261030.md`, `20261101.md`, `20261104.md`, `20261105.md`; 20261105 D16 track split, 20261106 award review and D26~D40, 20261108 D42-D45, 20261109 DLR original contact, 20261110 D42/D44, 20261111 D46-A~I. Github branch `research/t2-spatial-fig2-v02` governance and independent gate notes directly checked.

- D42 actual 45-min 20Hz DLR UT v1.3.1 trajectories and 1Hz publisher counts: frozen approach candidate 1449 vs publisher 1409, temporal one-to-one greedy ±1s 1399; candidate/publisher shared sensor lineage is NOT external truth. 346 multi-turn candidates, only 175 geometric route evidence, 171 UNKNOWN. Lane centerlines, finite stoplines, source-confirmed signal head-turn mapping, arrival demand and downstream receiving supply remain unresolved.
- D44 original D27 24 of 30 synthetic braking ceiling violations. The original engine is **not repaired**. D46-H separate bounded-braking single-car oracle passes its test but uses different initial conditions.
- D46-C/D/E: finite-storage throughput varies with dt and zero- vs positive-travel assumptions; do not equate different models as proof of numeric error alone.
- D46-F/G: positive travel and vehicle footprint cause synthetic throughput changes under specified event calendars. Not observed queue-tail shockwave.
- D46-I: 29 local contract tests and 12 synthetic runs, deliberate 4/4 unsafe cases flagged; multi-car longitudinal diagnostic is NOT integrated into the D46-G admission system or original D27 engine.
- D36 exploratory fixed vs actuated policy ranks based on four holdout synthetic seeds: interval crosses 0; empirically supported reversal not established.
- SUMO independent actual run unverified; old XML/netconvert design is NOT an external execution.

### Exhibition: CONDITIONAL GO for a bounded observable claim
Retain one intersection and one auditable queue/spillback process. Aim for measured car arrivals, finite lane stoplines, observed queue onset/release/tail, same-condition baseline T2 vs **real executed independent SUMO**. A falsifying case under detector censoring is desirable but cannot replace the observation. Present one physical mechanism + independent raw plots + honest uncertainty. If actual queue ground truth remains inaccessible, retitle to a reproducible **physical/model error case study**, without real signal superiority claims.

Competition eligibility: 2026 National Science Exhibition official page excludes works already public/presented at similar competitions, and requires student-origin work and regional qualification. **2027 Gyeongnam/National requirements and dates are not confirmed; verify directly before publication/release**. Previous GitHub public branch should be reviewed for overlap; public code alone does not automatically settle eligibility.

### Paper: CONDITIONAL GO for rigorous methods / HOLD on empirical claims
Best intellectual spine: *When do event-time, finite storage, and observational error contaminate estimated queue dynamics and signal policy ranking?* Need (i) one nontrivial well-scoped statement/counterexample with precise assumptions (ii) consistent implementation not a bag of independent prototypes (iii) independent comparator and dt/event convergence (iv) literature comparisons including bounded backpressure and trajectory/shockwave inference (v) paired heldout experiments with proper correlated observation uncertainty. Known conservation, `v²/(2b)` and quadratic gap minima are acceptance checks, **not publishable novelty by themselves**.

Key prior art: Emtenan & Day 2021, LWR/Newell, Lo 2001, Aboudolas 2009/2010, Tampère 2011, Grégoire 2015, Wang/Huang/Lo 2020, Yang et al. 2024, Wang et al. 2024 sparse trajectories. Han 2024, You 2026 still original full-text acquisition/review candidates. Never claim first spillback/queue/uncertainty model.

### Mandatory GO/NO-GO gates
1. **G1 field event validity:** physical lane/stopline + trace movement/signal mapping, UNKNOWN/censoring; disjoint human-reviewed holdout; publisher movement count not used to fit/validate itself.
2. **G2 physical-integrated implementation:** D44 bounded braking fix in a *working coherent* finite-buffer micro world, car IDs, gap, redline, time order, dt and mass conservation tests; recover/compare unmodified D27 defect trace.
3. **G3 independent SUMO:** pin binary, netconvert geometry, identical demand/signal/vehicle attributes, actual run and raw per-vehicle/queue output.
4. **G4 observational model check:** onset, discharge, queue tail, downstream occupancy with uncertainty and censoring; held-out sequences.
5. **G5 policy (only after G1-4):** frozen fixed-time vs actuated baseline; paired seeds, measured error mechanisms, unserved-demand right-censoring, uncertainty on rank difference, no p-hacking.

**Current code tests ≠ integrated empirical validation.**

### Custody
Full Korean decision and detailed review:
https://docs.google.com/document/d/1VOANUPgQDt__rzvfhRbm5sfq3xEd7CXxhaJLlZH0Jlg/edit
Daily reasoning folder contains only native Google Docs.
No GitHub-actions[bot] commits. Preserve raw dataset bytes, versioned ZIP and prior failed hypotheses.
