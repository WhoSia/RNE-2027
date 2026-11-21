# T2 P22 — Adversarial reality gate: block dependence and observed stopline counts

Preregistered 2026-11-22 KST **before fetching the new DLR day-time windows**.

## BFS lineage restored from direct November archive bytes
- 2026-10-27: the traffic problem was a study of missing observations and efficient signal decisions, not a data-collection project.
- 2026-11-11: DFS+BFS included physical queue geometry, sensing and worst-case decision regret; warnings included signal clearance, post hoc study design and independent simulation checks.
- 2026-11-17: domestic Jinju traffic aggregates for coarse inputs, DLR for independent trajectory/signal validation, Monaco MoST/SUMO for independent simulation; lane-bypass rules erased one flagship simulated paradox; Seho questioned post hoc 2.05s gaps, DLR exit-selected cohort and SUMO step-size sign flips.
- 2026-11-21: PHYS causal synthetic mechanism first; RF-CURTAIN's physical occupancy measurement second; value-of-information policy effect third. All three tracks must be maintained, without conflating each other's evidence.
- P18-P21: exact-source replay/event audit succeeded within synthetic law, but legitimate signal phases, stopline map, empirical headway, independent SUMO remain unverified. P21's 23:30 UTC DLR window has 37 object IDs; it was not selected to represent congestion.

## Freeze 1: check artificial sample size and block dependence
Primary data P19 exact frozen JSON, source: `research/t2/analysis/20261122/p19_receiver_service_opportunity.py`; 256 worlds generated from 16 unique timestamp+tape fingerprints and 8 geometries × 2 downstream offsets per tape. Distinguish 16 tape blocks, 32 tape×offset blocks, 128 offset pairs, and 256 outcome rows. Count strict positive `model_delta>0` for offset 15 at all three levels, including any positive among 8 geometries per tape; also report >5 threshold. Do not use a 128/128 binomial calculation. For 0 adverse among 16 independent exchangeable tape blocks, calculate the illustrative one-sided 95% Clopper-Pearson bound `1-0.05^(1/16)`. This is **not** a field generalization or confidence statement if IID tape exchangeability fails.

## Freeze 2: observed DLR-UT 1-second stopline count source
The published dataset README describes `meta_data/traffic_volume` as counting traffic-participant **center crossings of approach stoplines**, provided as CSV in 15-minute blocks. This is a *different observation modality* from trajectory IDs and raw signal code series. The pre-existing 2023-09-24 23:30–23:45 UTC volume file is known to contain 893 rows × 12 movement columns, binary 0/1 entries and 17 reported center-crossing bins across all movements. This is too sparse for credible congested queue or left-pocket blocking inference.

**Before inspecting new counts, freeze two additional windows:**
- `2023-09-24 12:00–12:15 UTC` (**calibration-candidate**), prechosen calendar-noon window irrespective of actual observed counts.
- `2023-09-24 18:00–18:15 UTC` (**independent temporal sensitivity**), prechosen 6h separation.
Do not promote either to positive-example status based only on a large count. The published recording day 2023-09-24 is Sunday; avoid commuter weekday/peak assumptions.

Measure number of valid timestamp rows, per-movement crossing bin totals, nonzero per-second bins, count outside {0,1}, exact duplicate timestamps, and union intersection with nominal signal/trajectory file intervals. **Do not** claim exact vehicle-level headways from whole-second bins, full sample independence, an identified controlling phase, or real spillback. Movement names are dataset column identifiers, not independently confirmed physical lane geometry.

## Frozen review-panel role separation
- BUILDER: execute exact-source calculations and preserve raw hashes.
- SKEPTIC: construct counterexamples to strong P19 'never harmful' narrative; check pseudoreplication and transfer of source assumptions.
- EMPIRICAL: independently audit 1-second stopline-count semantics and signal/trajectory time alignment; reject selection on observed outcomes.
- METHODS: check aggregation levels, nonidentical world comparisons, phase legality and any unwarranted causal claims.

These are **explicit internal adversarial review roles**, not four independently called LLMs. MCP_Hub tools currently advertise bounded utilities and public scientific metadata tools, not a callable general-purpose independent reasoning-model endpoint; external peer-review execution must be reported separately if ever performed. This panel's final verdict must report *evidence*, *objection*, *possible falsification*, *status* and *next repair* on each claim.

## Gates
- Gate A: synthetic block dependence and exchangeability analyzed, not hidden.
- Gate B: two preregistered DLR count windows audited byte-exactly.
- Gate C: confirm signal code mapping and stopline geometry before any actual headway/cause claim.
- Gate D: independent SUMO execution with matched road, arrival tape and action legality.
- Gate E: RF sensor discrimination and decision-value tests separately, not inferred from PHYS math.

Do not open K047 sealed data, move or extract CIM unverified ZIP, actuate real controllers, collect unauthorized WiFi data, use GitHub Actions/bot, or create proliferation branches.
