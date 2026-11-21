# R&E 2027 T2 — Research genealogy before the 2026-11-21 exhibition reorientation

**Status: documentary critical synthesis**. Sources in this map were read from the GitHub main documents, connected historical Google Docs, and selected old Notion pages. This is not a claim to have read *every* archived chat line, all PDFs or every GitHub commit across months.

## A. Origin: green given but no discharge

The original research asks: why does a through movement fail to discharge during green even when upstream vehicles want to pass? At least three causal classes must remain distinguishable:
- **No demand**: no queue waiting to move, so zero discharge is expected.
- **Pocket-induced through blockage**: left-turn or channelized-section queue crosses the shared approach, suppressing through discharge.
- **Downstream occupancy**: receiving link lacks storage; discharge impossible or limited even though upstream is available.
- **Both at once** can coexist. Include uncertain label when trajectory/signal alignment is incomplete.

Compare [Wu2024 held](https://drive.google.com/file/d/155MVLQ8tpc1AhK5mo03Rz2w5MHBQUJ_r/view), [Qi2020 held](https://drive.google.com/file/d/110GFwIyMMN1cJc_iyeTMVeZCVFRYTVmP/view), [Emtenan&Day2021 held](https://drive.google.com/file/d/1DtGATNcUmPdLF8JTKbe7yoFy65v4yh-j/view) and the Nov13 team [Notion plan](https://app.notion.com/p/417ef561cf9281ab89c5e2514aad3575).

A real static blocker being present is insufficient evidence that it caused zero discharge. Movement need, permitted signal, downstream space, lane-specific trajectory and nonmeasurement must all be considered.

## B. Earlier model and field work was real work, not disposable

- **Pre-Nov21:** point queues, phase boundary/tau effects and adverse findings already existed; 2026-11-17 **김세호** independently audited the local 85-test suite against a historical SHA. His report identifies a stale contradictory SUMO text, posthoc 2.05s gap selection, outcome-based DLR cohort choice, small independent temporal samples and numerical time-step sensitivity. [His original independent Google Doc](https://docs.google.com/document/d/1vtBLTnL6S9m7VJPOmWnwQRVGCuwIUHewZ8SPGVFX2Bc/edit) and [discussion](https://docs.google.com/document/d/1tUkSfAj-vo-AOzfLc_A_TWInzztmXsf8-hOwk_kKqso/edit) are mandatory reading for the new Claude reviewer. Do not claim every historic SUMO action has been reexecuted in the current environment.
- **Notion H06 (2026-11-02):** an apparently dramatic control/nonidentifiability witness failed when physically feasible timing constraints were enforced. [Original negative result](https://app.notion.com/p/40cef561cf928117bd9fcef033c79b33).
- **Notion H25 (2026-11-03):** aggregate-alias observation under synthetic guard already reported; zero novelty for the generic statement that aggregate matching can hide mechanism-dependent policy effects. [Original H25](https://app.notion.com/p/40def561cf9281a7923ef4542af30094).
- **DLR / K047:** open three historical DLR 15min blocks yielded useful movement/route/signal alignment diagnostics. That does NOT identify a confirmed observed case of actual left-turn blockage. Explicitly **seal K047 18:00–18:30 UTC**. The existing Nov21 diary warns against ex-post destination cohort selection, and was updated following signal head mapping corrections.
- **SF-01:** a theoretical 16-world information–decision regret analysis and toy scalar Kalman training exercise *transfers method principles* from Long2026, Huang2025 and Shafik&Rakha2025. No complete original method or published field experiment was reproduced.
- **PHYS01–03:** 192+384+128 synthetic studies tested pocket geometry/time opportunities and restrictions; the apparently independent run total is not a measure of independent traffic days.
- **PHYS04–11:** matched same-t84-checkpoint signal branch comparisons, new limited observation heuristics, repeated determinism checks. PHYS10 count-feature zero-distance example seed76 was **+306 model cost**, but its matched training seed3 cost effect **0**, so this is NOT strict opposite optimal-action identification. PHYS11 gap-confirmation 1/2/3 ticks had 0 strict policy reversals on its prospective grid.
- **Independent adversarial audit:** fixed zero-time checkpoint boundary, characterized low arrival-time diversity; the canonical 240s uniform generator uses the exact same timestamp array for each same-demand seed. [Corrective audit](../decision-time-gate/CRITICAL_INDEPENDENT_REVIEW_AND_CORRECTIONS.md).
- **Arrival clock follow-up:** new route-matched alternative timestamp families (seed96–103) showed strict opposite policy-value signs across different pre-t84 microscopic worlds, despite equal total vehicle number and ordered left-turn/through labels; **not** a same-state or same-observation identification theorem. [Registered evidence](../decision-time-gate/T2_ARRIVAL_CLOCK_AND_GREEN_ENVELOPE_FINDINGS.md).
- **RF01:** two longitudinal camera-free Wi-Fi channel sections to diagnose pocket/downstream obstruction, five tabletop classes and held-out placement design. First-Fresnel midpoint geometry and 12 tests pass; measured CSI = **0**, no hardware demonstration. [RF01 receipt](../../../exhibition/rf_curtain/RF01_FEASIBILITY_RECEIPT_20261121.md).
- **RF02 (current document unit):** discipline the observation ontology before sensors are purchased: a P,D perfect two-bit *static occupancy* observation yields 4 signatures among 5 toy classes, leaving no_demand/free ambiguous. An independent approach-demand bit resolves it within the declared ideal toy model; 9 tests passed. [Code](../../../exhibition/rf_curtain/rf_observation_identifiability.py).

## C. Parallel scientific agenda, rather than replacing T2

**E-track: empirical sensing & exhibition**
1. Re-read exact WiTraffic, DeepWiTraffic, 2025 ESP32 CSI and 2024/2026 review papers; retrieve originals to canonical Research OS shelf only with DOI/version/byte checks.
2. Inspect available school-owned CSI-capable equipment, consent/privacy requirements and safe indoor test geometry. No real-road installation or public-controller access.
3. Pre-register independent *moving and stationary* model-scene tests, P1/S1–S2 training and P2/S3 holdout. RSSI baseline, CSI model if actual CSI accessible. Never label a synthetic feature fixture an RF measurement.
4. Evaluate distinguishability of pocket/downstream/no_demand/free/both vs 'unresolved', including missing sensors. Keep Wu10-type taxonomy separate from our toy labels.

**T-track: traffic dynamics & information causality**
1. Preserve and simplify the broad PHYS evidence graph, make numerical tests complete and explicitly source-constrained.
2. Build physically feasible **abstract** signal action set and evaluate arrival-rate sensitivity without inventing real legal controller authorization.
3. Validate state/demand clock with source papers, independent SUMO version/geometry and unsealed observed DLR evidence.
4. Only when **real** RF confusion/latency measurements exist, evaluate if they reduce worst-case regret conditional on compatible traffic worlds.

## D. Governance and preservation

Canonical GitHub working branch `main`. No GitHub Actions or bot author, no cherry-picked holdout, no claim full historical integration testing. Original papers stay in 10_PAPERS; source-grounded interpretation in date-stamped Google Docs, reproducible small code/figures and test fixtures in Git. Existing original artifacts and historical branch links remain intact, with dated corrections rather than retroactive deletion.

Scientific timeline is flexible. **Do not optimize for dozens of runs or 'paper novelty' before source reproduction and externally observed truth labels.**
