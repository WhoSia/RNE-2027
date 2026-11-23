# P103 — 2026-11-23 T2 Research Director's Adversarial Decision Audit

**Status:** archival audit, NOT a new simulator run. Parent evidence: P35, P38, P71, P87–P102. Verified remote `main` before writing: `5a2dab0f0df5f936e2bbd83a8d989984f1b9464f`. Existing dated Google Docs running diary reviewed.

## Executive verdict: conditional discovery, not a traffic policy

**Retain** a rigorously reproducible **synthetic finite-storage delay-redistribution mechanism**: at fixed initial state and arrivals, a shorter downstream cycle can reduce receiver-entry refusal while shifting vehicle-seconds to left turners and the upstream A lane. Original P87 55/192 paradox pairs, all 192 paired metrics re-executed in P88; P100 pre-registered 32 newly chosen seeds (64 heldout tapes at high-turn red onset) yielded 64/64 red-onset paradoxes, P101 decomposed same tapes. This strongly establishes *internal conditional behavior* of this precise simulator and set of parameters.

**Do not assert** empirically optimal 30s/60s cycles, a physical 2023 intersection result, a measured startup loss, validated pressure stability, pedestrian safety, or an independent SUMO replication of the P100 condition. The most pressing remaining uncertainty is **transportability of a T2-specific mechanism to properly geometry-matched physical or independently modeled networks**.

## Recounted evidence ledger — distinct denominators

| Evidence | Exact counts / numerical result | Basis | What it proves | What it cannot prove |
|---|---|---|---|---|
| P35 actual data time join | 17 geometrically estimated stopline crossing brackets; naive nearest is future sample in 11/17, after full 50ms interval in 10/17; 16/17 source-derived counter match at ±1s vs 7/17 at ±0.5s | 30 head signals/26,970 rows; 17 geometric crossings | Synchronization, sampling and source consistency hazards | Physical controlling head→lane attribution, 2023 observed road stripe or downstream exit |
| P87 discovery | 192 paired cycle comparisons on **96 unique seed/share/family tapes**, with 55 denial-down/cost-up pairs (12 green onset, 43 red onset) | 16 seeds×3 shares×2 arrival families×2 onsets | Synthetic metric mismatch exists | 192 independent field trials |
| P88 reconstruction | 192/192 exact P87 signed delta reproduction; 384 arms, all vehicles cleared; 5 zone × 2 movement reconstruction; 43 red paradox sums left +46,853, through −9,248, network +37,605 vehicle-s | Source-locked T2 simulation | Exact model-level allocation of increased occupancy | Field causation or unique event-level causal mechanism |
| P89 | 768 paired comparisons, 1,536 arms with additional green-onset service blackout 0/1/2/3s; red-onset 30s victories 51/40/41/33 of 96 | Same T2 engine | Sensitivity to specified *additional* blackout | Measured saturation flow/headway/startup loss |
| P95 leave-one-seed-out | Onset interaction mean signs fixed in all 16 leave-one-seed-out subsets at shares .25/.50/.75; n=32 pairs per share across 16 seed blocks | Subsets of original P87 | Simple one-seed influence not enough to reverse sign in source panel | Independent out-of-sample performance |
| P96 | 5 selected representative ID replays; sample 85001/0.5/uniform/red earliest receiver exit 99s vs 114s, yet +126 network vehicle-s | Preselected synthetic cases | Earliest exit is not sufficient for total network-cost ordering | Global causal pathway across 55 cases |
| P97–P98 | Only 2/576 adjacent *absolute* cost comparisons show a decrease on extra blackout (−253 and −454 vehicle-s); two cases fully ID-reconstructed | Same engine, selected exceptions | Nonmonotonicity counterexample *inside model* | Benefit of wasting green at real signals; population incidence |
| P99 | Extended end from 1440 to 1464 for exact common 1380s postdecision window, 690s displayed green/arm at loss0. 768/768 signed results unchanged. | Same tape, same no-terminal-vehicle state | Previous unequal 1356s displayed-green totals not needed for observed comparison | An independent sensitivity to long-run demand; with full clearance before 1440, equality is largely forced |
| P100 pre-registered holdout | 32 new seeds ×3 share ×2 arrival families =192 tapes, 384 paired comparisons, 768 arms. Red onset high left-share 64/64 paradox; low left-share green onset 29/64. Both-onset paradox 0/192 | Same simulator, disjoint random seeds | Not confined to original 16 seeds | Independent model/site generalization; seed×arrival scenarios are not 384 independent clusters |
| P101 mechanism on P100 | Same **64 tapes** red onset left higher/A higher/B lower/outside higher 64/64 each; green left higher 0/64. 128/128 paired decomposition identities | Same P100 heldout tapes, not a second independent sample | Recurrence of movement and zone pattern conditional on P100 | Independent replication of P100 result |
| P71 / P102 adversarial external data | Historical 64-tape T2 vs SUMO on **different intervention** (10s−6s left green). At offset 0 signed rank exact 13/64, strict opposite 16/64; at offset15 exact 2/64, strict opposite 40/64 | Existing independent-engine data, unmatched geometry | Physical-semantic mapping between engines is unresolved and can reverse policy rank | P100's 30s−60s conclusion is directly refuted by P71; not same treatment |
| P80–P81 | No observed downstream end on relevant observed tracks; lane/head physical ownership unknown | Existing night field track screen | Incompleteness of physical exit observation | End-to-end real vehicle travel time |

## Three consequential methodological corrections

**1. Evidence independence.** A matched seed/share/arrival tape used for green and red onsets is one paired underlying arrival realization, **not** two independent samples. P100's 64 tapes are from 32 seed blocks; `uniform` and `platoon4` within one seed share seeded randomness and structural assumptions. A naive 64-out-of-64 i.i.d. confidence interval is unwarranted. P101 is a downstream nested diagnostic on exactly the same 64 records. No extra external replication count.

**2. Quantity definition.** `cost` is *network vehicle-seconds* (outside+A+B+pocket+receiver) through complete clearing, not field measured stopped delay or intersection control delay. `receiver_denied_seconds` counts blocked receiver *attempt-time*, not denied-vehicle-seconds. A reduction in this local rate is therefore not expected to imply reduced global occupancy without extra model constraints. `full_red` is full occupancy under red and does not establish observed network throughput. P89 masks further green availability; real startup lost time must be tied to measured discharge headways.

**3. Alternative explanation and weak negative control.** P99's equality after t=1440→1464 is compatible with all cars having exited before 1440; thus it is a sound *finite-boundary bookkeeping check* but has little power to distinguish physical timing mechanisms. The more decisive challenges are link capacity, lane geometry/turn handling, human or car-following discharge behavior and independent generator/engine.

## Research maturity grades, not probabilities

Use P38 anchors: 0 absent; .25 specification/toy; .50 direct repeatability within one domain; .75 independent reference or substantially different conditions within scope; 1 target-domain independent validation with quantified error. Proposed current **ordinal** status, with rationale:
- T2 execution and conservation **.90** (8/8 Git SHA, 14/14 module tests, 192/192 P87 replay and 128/128 heldout identity).
- Conditional synthetic mechanism **.85** (two distinct seed sets, source-locked per-ID accounting, but one simulator architecture).
- Physical parameter fidelity **.45** (unobserved critical downstream storage/headway and uncertain physical lane movements; prior P38 component baselines acceleration .45, startup .40, pedestrians .25).
- Cross-engine transported policy sign **.20** (existing independent P71 disagreeing and not geometry-matched; not P100-matched).
- Field identification of controlling head and complete downstream exit **.20** (17 candidate crossing brackets but head attribution and terminal exit unresolved).
- Real-world signal policy benefit and safety **.00** (no controlled real intervention, real counterfactual or pedestrian/hazard outcome).

Grades are planning judgments, **not observed success rates**, and changing grades does not replace actual experiment counts.

## Transparent decision scoring instead of ungrounded 0.98
Historical P38 criterion adopted: weighted priority = 0.35 relevance + 0.30 discrimination + 0.20 readiness + 0.15 one-week feasibility. Each column 0–1 is an explicit **subjective proposal**, not an empirical probability. Ranked for *next actionable work*, with field acquisition maintained as a mandatory strategic gate even though its readiness is low.

| Candidate | R | D | Ready | Week-feasible | Weighted |
|---|---:|---:|---:|---:|---:|
| F01 기존 현장자료 동기화·식별성 감사 | 0.96 | 0.90 | 0.82 | 0.82 | 0.8930 |
| E01 동형 T2–SUMO 독립 대조 | 0.99 | 0.98 | 0.72 | 0.72 | 0.8925 |
| G01 수용량·포켓 길이 구조적 반증 | 0.87 | 0.84 | 0.90 | 0.92 | 0.8745 |
| U01 보행자·교차 이동류 지체·제약 | 0.92 | 0.90 | 0.64 | 0.67 | 0.8205 |
| H01 실제 출발 차두간격 기반 손실 검정 | 0.88 | 0.85 | 0.65 | 0.60 | 0.7830 |
| F02 부족한 현장 출구/현시 동시 관측 | 0.99 | 0.97 | 0.40 | 0.40 | 0.7775 |
| A01 감응식·검지 오류 | 0.82 | 0.75 | 0.56 | 0.63 | 0.7185 |
| S01 기존 엔진 난수 시드만 추가 | 0.68 | 0.20 | 0.98 | 0.98 | 0.6410 |

**Interpretation:** near-tie between F01 (~.8930) and E01 (~.8925) is below subjective rating precision; treat as a **co-equal portfolio**, not a meaningful 0.0005 advantage. Geometry counterexample G01 (~.875) is ready but synthetic-only; schedule it **after** at least one genuine independent-engine or official data-identity attempt. Physical F02 field capture (~.778) ranks lower only because resources and downstream visibility are missing; field completeness remains **non-negotiable scientific gate**, regardless of numeric score. Additional seeds alone (~.641) are explicitly deprioritized.

## Two-week research plan with preregistered objective gates

### Days 1–2: F01 independent data/geometry identity audit
- Inspect original P33–P38 raw data (same-source route counter cannot become external ground truth), P80–P81 end-of-link visibility, time/head→approach map; classify every event as observed, bounded, imputed, or unavailable.
- Required artifacts: exact source SHA hashes, head→lane support matrix, downstream-entry vs downstream-end observation coverage per target movement, censoring indicator and a falsifiable statement of what cannot be inferred.
- **Gate F:** No false exact physical approach ownership; 17/17 candidate crossing intervals retain interval bounds, no uncontrolled future sample join; if downstream exit 0, write END_EXIT_UNOBSERVED instead of extrapolating time. If dataset cannot identify discharge, stop causal field policy inference and specify minimal extra sensors.

### Days 2–5: E01 geometry-matched T2 vs SUMO
- Reconstruct T2's A/B upstream lane widths, 7-cell pocket, finite four-cell receiver and independent fixed-time 30/60s calendars, green/red start and service headways in SUMO with explicit lane routes. Confirm clock phase conventions, 1s T2 vs SUMO time step, and vehicle ID/timestamp identity.
- **Prerequisite gate E0:** Both engines match demand tape SHA, ID counts, stage lengths, upstream split, 4-cell downstream storage *physical-equivalent length*, boundary delay semantics and terminal clearance. Otherwise classify `MODEL_MISMATCH`; do **not** publish policy-sign agreement as a validation metric.
- Reserve 8 original and 8 heldout seed blocks (both families; share .25/.5/.75; 2 onset comparisons) for a pilot after geometry is locked. Treat each seed block as the cluster.
- **Gate E1:** 100% route/arrival ID preservation, 100% terminal conservation; record median absolute exit-time error and 95th percentile by movement. Predeclare tolerance for exit-time error only *after checking SUMO physical resolution and before inspecting policy effect*.
- **Gate E2:** Report rank agreement by onset/share family with three categories `agree/opposite/tie` and paired cost effect; publish discordance matrix **even on failure**. No cherry-picked parameter fits.

### Days 6–8: G01 geometry falsification, conditional
- Lock four receiver capacities `2/4/8/16` and pocket slots `0/7/14` on the same seeded tape panel (capacity values are mathematical synthetic settings, not actual road lengths). First one-factor sweeps, then only preselected 2-way interactions.
- Primary outcome: red-onset share .75 paradox frequency, network and per-movement cost, max queue, network-out and phase score.
- **Gate G:** Every run clears, vehicle count conserves, no pressure/queue proxy used as surrogate for travel cost; count when 64/64 pattern fails. Demote conditional universality if sign reverses anywhere.

### Days 8–10: U01 competing road users
- Add minimal opposing queue plus pedestrian crossing only *with legally safe conflict/clearance semantics*, not an arbitrary zero-cost extra flow.
- Compare weighted network occupancy, worst-user delay, 95th-percentile vehicle travel time, pedestrian maximum wait, and risk/phase feasibility constraints separately rather than hiding competing users in one scalar.
- **Gate U:** No unsafe overlapping conflicts in generated schedules, all affected movement populations in objective, no unmeasured pedestrian delay described as improved.

### Days 11–14: independent review and manuscript freeze
- Roles: hypothesis proposer, adversarial falsifier, method/causal estimator, reproducibility auditor. Separate `SOURCE_OBSERVED / SIMULATOR_REPRODUCED / ENGINE_DISAGREES / MODEL_ASSUMPTION / UNKNOWN` lines.
- Freeze text only when references resolve to original raw inputs and source/test/result SHA, figures include denominator and paired unit, and every conclusion states its scope.
- **STOP** if independent engine cannot be made physically isomorphic, observed downstream endpoints are missing, or the scope relies on an unverifiable controller phase→lane mapping. Publish negative/missing results without masking.

## Concrete research thesis and alternative

Main defensible thesis: **“Finite downstream storage and movement-specific queues can make local signal spillback indicators non-order-preserving for total corridor vehicle-time under matched arrival and onset conditions.”** This is a *conditional result* in a discrete two-lane simulator, not a field-experiment finding.

Adversarial alternative: the high-share red-onset 64/64 pattern may be an artifact of fixed T2 lane assignment, 4-slot receiver, fixed upstream left-first schedule and perfect knowledge of arrival/turn choices. The experiment is valuable precisely if a physically consistent independent simulator or varying bay length falsifies it.

## Collaboration and bookkeeping
No new branches, only authorized main writes by WhoSia, never github-actions[bot]. New report must be entered in existing Nov 23 diary and archived in 01_ACTIVE_T2 dated folder. If a real independent SUMO cannot be installed/run, preserve prereg and an environment/incompatibility report, rather than upgrading a historical P71 reread to 'new independent validation'.
