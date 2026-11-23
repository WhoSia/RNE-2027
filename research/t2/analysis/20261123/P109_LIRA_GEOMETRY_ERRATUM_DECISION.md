# P109 — LIRA adversarial review of pocket-geometry correction and P104–P108

2026-11-23. **LIRA (0–1) is current recommendation to RETAIN a precisely scoped claim, not probability of truth, policy success or paper acceptance.** Under the established project rubric, KEEP >=0.80. Assign severity P0 (invalidating logical/scientific inference), P1 (major conceptual/evidence defect), P2 (scope/qualification), P3 (wording). Every claim has a warrant, rival and revision trigger.

## P0 documentation erratum, retain scientific results with corrected physical meaning

Earlier P100/P101/P103 prose sometimes calls the original turn pocket a **"7-cell pocket"**. This is **wrong**: `build_config(...,7,4,...)` passes `pocket_length_m=7` meters, with `cell_m=7.0`, so `validate` returns `pocket_slots = floor(7/7)=1`. The receiving link is specified separately as `receiver_slots=4`, a 4-cell link, while a 140m approach is 20 approach cells. The wrong "7-cell" wording may misdirect external SUMO parity and mechanism interpretations, but does **not** change the original exact P87/P88/P100/P101 numeric model output. Correct source semantics and *preserve* the old original prereg documents as historical provenance; append explicit errata instead of silently altering historical text.

## New frozen pre-registered falsifier P106

[P106 pre-registration](P106_POCKET_GEOMETRY_PREREG.md) was committed at `cab02b203aad8312698ca6313993821472a32455` **before** the first P106 run. 8 new seed blocks 87001–87008 × uniform/platoon4 =16 demand tapes, 75% left-turn, red onset, pocket physical lengths 7/14/28/56m = 1/2/4/8 cells. Each has a common matched checkpoint and downstream 30/60s cycle; 64 matched pairs/128 simulation arms.

| Length (m) | Pocket slots | Denied lower and network cost higher | Signed network cost sum (vehicle-s) | Mean pair delta |
|---:|---:|---:|---:|---:|
| 7 | 1 | 15/16 | +18,289 | +1,143.0625 |
| 14 | 2 | 15/16 | +18,289 | +1,143.0625 |
| 28 | 4 | 15/16 | +18,289 | +1,143.0625 |
| 56 | 8 | 16/16 | +18,288 | +1,143.0000 |

All THREE preregistered 2/4/8-cell thresholds >=14/16 PASS. Exactly 15/16 demand tapes have the same signed 30s-60s total cost difference across **all four pocket lengths**; remaining one differs by just 1 vehicle-second at 8 slots. Therefore the hypothesis "a one-cell pocket is necessary for the red-onset paradox" is **falsified within these particular synthetic conditions**. The result does not prove pocket capacity is irrelevant at higher traffic pressure, other headways or different phase plans.

## P107 post hoc absolute-cost diagnostic

Executed another 128 simulator arms with post-tick trace and kept each policy's **absolute** network cost, maximum pocket occupancy and `pocket_block_seconds`. Compared to the 1-cell case:
- 2 slots: 16/16 tapes **both 30s and 60s absolute costs unchanged**.
- 4 slots: 16/16 tapes **both absolute costs unchanged**.
- 8 slots: 14/16 tapes both absolute costs unchanged; one further period matched; the other differs.
- Summed pocket blockage seconds over 32 policy arms: **1 slot 10,808; 2 slots 10,522; 4 slots 9,895; 8 slots 8,013** (but these counts are per-arm aggregated and must not be described as the 16-pair experiment total).
- All 32 4-slot-arm max pocket occupancies are exactly 4 (max occupancy sum 128); all 32 2-slot arms exactly 2. So **pocket geometry did change observed storage**, even when network cost didn't change.
- 4 slots versus 1: pocket-entry block seconds decrease by 913 seconds (8.45% of 10,808) over the 32 arms, **without changing network vehicle-seconds for any of the 32 arms**.

This directly illustrates *another* surrogate-metric problem: changing a **local pocket-blocking metric** need not change the global corridor vehicle-seconds under the fixed downstream supply.

## P108 ID-level downstream exit falsification

Compared 1-slot versus 4-slot pocket under 16 tapes × two downstream cycles = 32 geometry pairs, 64 fully cleared model arms. Source P107 absolute costs independently confirmed **32/32 equal**. Actual downstream network departure events `(tick,vehicle_ID,movement)` were **31/32 exactly equal**; per-vehicle total costs also **31/32 equal**. The single exception was seed 87002, platoon4, period60: six vehicle delays changed (+2s for five vehicles and −10s for one), summing **0**, so network total still equaled 6,606 vehicle-seconds in both geometries.

### Rival explanations to retain
- The 1-slot pocket is absolutely binding (maximum occupancy 1), whereas 4 slots fill to 4; movement A↔pocket occurs earlier with extra storage, but downstream release calendar and upstream phase may still dominate actual departures. **Do not assume the same event sequence** unless per-ID replay verifies it (the P108 exception falsifies universality).
- Different physical pocket lengths may alter human lane change and spillback in SUMO or the field. No independent microcalibration was done.
- Cost equality is partly a consequence of the **conservation definition** if all per-car exit times and initial arrival times are equal: moving the same car from lane A to pocket redistributes zone cost but leaves total residence time unchanged. Where per-car exit times differ, equal total still arises by cancellation.

## LIRA case-by-case panel

| ID | Precisely scoped claim | LIRA | Verdict | Severity / rival and upgrade gate |
|---|---|---:|---|---|
| GEOM-1 | Original `7` denotes 7 meters = **1** pocket cell at 7m/cell | **0.99** | KEEP | P0 correction; verified source `validate` and runtime `pocket_slots` |
| GEOM-2 | Original high-left red-onset paradox *requires* a 1-slot pocket | 0.12 | REJECT | P1: P106 at 2/4/8 slots 15/15/16 out of16; upgrade only with different factor conditions |
| GEOM-3 | Larger pocket reduces observed local pocket blocking under P107 conditions | **0.94** | KEEP | P2: 10,808→9,895 (1→4) on 32 synthetic arms; cannot extrapolate physical rates |
| GEOM-4 | Reduced pocket blocking therefore reduces **network** vehicle seconds in the same conditions | 0.06 | REJECT | P0: absolute costs identical 32/32; need new experiment with final departure differences |
| GEOM-5 | Increasing 1→4 pocket slots preserves per-ID downstream discharge history always | 0.18 | REJECT | P1: P108 31/32 identity; one exception with six individual shifts |
| GEOM-6 | Enlarging pocket 1→4 leaves *aggregate* network cost unchanged on P108 tested 32 arms | **0.96** | KEEP | P2: exact 32/32, but conditional on this load/stage/receiver |
| GEOM-7 | P106 is independent proof of road operations | 0.02 | REJECT | P0: same synthetic T2 engine, no physical lane/head mapping |
| FIELD-1 | P104 field candidate paths certify actual downstream terminal departures | 0.04 | REJECT | P0: 0 observed verified physical terminal exits; acquire real downstream crossing |
| ENGINE-1 | A geometry-matched independent engine and field exit audit should outrank more new T2 seeds | **0.96** | KEEP | P1: P102 mismatch, P104 coverage; redo decision after parity and field data |
| REPRO-1 | P106/P107/P108 exact numerical identities and physically differing pocket occupancy are source-locked | **0.94** | KEEP | P2: 128+128+64 arms, all actual engine replays, same engine |

**KEEP 5 / REJECT 5**. Decisions are claim adoption judgments, **not calibrations of certainty**.

## Revised research director ordering

The prior P103 objective-weighted action scores F01 .8930, E01 .8925, G01 .8745 still control operational portfolio; P106 has now executed a piece of G01 but **G01 is not complete**: receiver capacity and independent geometry are untouched. Repeated same-engine trials alone are no longer the bottleneck.

Next:
1. **F01** official field head→movement and downstream-terminal evidence ledger (must preserve P104's 0 official mapping, 0 terminal observations).
2. **E01** genuine geometry-matched T2 vs SUMO. **P0 geometry gate** `cell_m=7`, `approach_length_m=140`, original `pocket_length_m=7` (1 cell), `receiver_slots=4` (4 cells), `receiver_headway_s=2`, `through_B_share=.5`, `change_zone_m=100`, and exact phase/start semantics. None of these *synthetic values* is a surveyed physical geometry.
3. **U01** pedestrians and conflicting-demand objective, after true conflicting movements have been represented.
4. **G01 remainder** receiving slots 2/4/8/16, shorter/longer approach, lane assignment and downstream headway, with preregistered interaction holdout *only after independent engine work is attempted*.

**Stop condition:** no "real efficiency improvement" claim until exact corresponding intervention and comparable event definitions are assessed in physically matched independent engine and independently observed road data.
