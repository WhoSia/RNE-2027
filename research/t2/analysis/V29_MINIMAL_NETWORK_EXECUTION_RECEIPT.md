# T2 v2.9 — Executed three-junction OD-conserving network

**Code/CSV/JSON/tests:** [Drive reproducibility ZIP](https://drive.google.com/file/d/1TPMtsBxlbq8cR8x--Su4WHJ_GilfTmRM/view). **20261102 Docs:** https://docs.google.com/document/d/1zaUc5dScw47gwm49UjxGF94dbtxWFa9h7igd6fvlzXU/edit

Implementation: standalone Python store-and-forward demonstration, 3 controlled junctions, main finite links, side access at junctions 1 and 2, explicit vehicle IDs, single exit destination, fixed link travel time. Each time step asserts generated=outside+links+completed and unique vehicle IDs. **Not** a merge of the pre-existing v2.2 engine, and **not** a calibrated physical microsimulation.

Local executed tests: 5/5 pass, including conservation across three policies and seeds; capacity=1 stress; deterministic replay; same exogenous arrivals; rejection of invalid events and configuration.

Experiment: seeds 0..3, capacity 4/12, main arrival probability .35/.70, each side arrival probability .15/.40, offset 0/10 seconds; 64 scenario inputs x 3 policies = 192 simulations, 900 simulation seconds each. Archived CSV was accidentally named experiment_384_v29.csv although it has 192 rows; the true count is 192. Mean completed OD trips: fixed 208.5; offset-coordinated 207.0; locally greedy pressure heuristic 183.953125. In 64/64 scenarios the heuristic completed fewer trips than fixed.

**Critical interpretation:** These are toy-model outcomes; the heuristic is not Varaiya's Max-pressure, and switching/lost time is not matched between policies. This is NOT a counterexample to an established Max-pressure stability theorem, and it is NOT an external empirical validation. Completed-trip mean time is survivorship-biased whenever some trips remain incomplete; vehicle_system_seconds counts occupancy time rather than pure delay. The isolated 3-junction model has only one exit destination and is not yet a general OD network.

Next gates: comparably constrained controllers, stage switching counts, physical headway and signal feasibility tests, actual max-pressure definition, event-level causal comparison, SUMO/field validation. No GitHub Actions or bot commits.
