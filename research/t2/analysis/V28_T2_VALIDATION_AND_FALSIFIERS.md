# T2 — Validation hierarchy and falsification gates

1. **Source provenance:** GitHub HEAD versus archived v2.2 fixed source differ. Produce exact remote checkout hashes and patch audit before treating old experiments as current code evidence. Re-run all tests offline; no Actions.
2. **Conservation:** generated = outside + upstream + receiver + completed, tracked by vehicle ID and OD. Reject duplicates, impossible transitions or events not backed by state transitions.
3. **Independent simple baselines:** store-and-forward, CTM where applicable; analytically solve 1-link/2-link cases before simulation.
4. **Mechanism ablation:** finite versus unbounded storage, left-turn permission, different receiver lengths and lane counts; distinguish end-of-horizon effects from capacity.
5. **Model confrontation:** AIMSUN study findings by Taglieri et al. (2024) are literature claims; do not declare their numerical reproduction from a new toy model. Compare SUMO with matching geometry, route demand, gap acceptance and junction controls; document unavoidable discrepancies.
6. **World-contact:** observe de-identified turning counts, green splits, queue envelopes, saturated headways, bus stops and pedestrian phases in Korea; calibrate using one interval and hold out another independent interval.
7. **Counterexamples:** Seek scenarios where RB loses to TWL in multi-lane networks, where local delay improvement increases OD trip time, where signal coordination loses benefits under downstream spillback, and where a method overfits demand to a single date.

No claim of real-world signal optimization until independent predictive validity is demonstrated. No GitHub Actions or github-actions[bot].
