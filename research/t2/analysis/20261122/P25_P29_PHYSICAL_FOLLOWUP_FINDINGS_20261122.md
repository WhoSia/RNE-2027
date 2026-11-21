# T2 P25–P29 — Exact-main physical simulator follow-up series (2026-11-22)

**Research status: COMPLETE for executed synthetic experiments and regression gates; EXTERNAL PHYSICAL VALIDITY OPEN.** This series extends the old PHYS-04 / P18 / P19 simulator without silently altering historical cohorts or claiming deployable traffic control.

## Research genealogy and design commitments

- P17: archived PHYS-04 historical 144-world original ZIP recovered; strict six-count vs actual microstate aliases distinguished.
- P18: exact GitHub `main` T2 core replay agrees **144/144** with historical PHYS-04 *pairs*; not whole JSON bytes.
- P19: receiver capacity / downstream offset moderator, **256 worlds**, 16 complete arrival tapes; preserved frozen JSON SHA-256 **`0681f683acd549cb2d32cc8957038ce3e652819f47e8288c5a751b6acd7e2468`**.
- P22: already implemented terminal cost penalty sensitivity (0/60/120). **P25 is not relabeling this old sweep.**
- [P25/P26 preregistration](P25_P26_FOLLOWUP_PREREG_20261122.md) was committed **before** running these cohorts (`5f99a50d70e3ea95071b6b578f561dfe27e574f0`).
- [P27 exploratory longer-stage plan](P27_STAGE_OPPORTUNITY_EXTENSION_PLAN_20261122.md) explicitly discloses the diagnostic, outcome-informed pilot; P27 is **NOT an independently preregistered discovery**.
- [P28 posthoc metric-audit plan](P28_EVENT_METRIC_IDENTIFIABILITY_PLAN_20261122.md) labels measurement analysis as exploratory.
- [P29 fresh unused seed holdout preregistration](P29_FRESH_SEED_HOLDOUT_PREREG_20261122.md), committed `cc854e84425b0e301c4170a67a79a7d5f979f2a5` **before P29 run**.

All follow-ups use the exact original synthetic engine: `dual_lane_v11.py` blob `a7c9aa6954402e12894d1d5b722e8a474b0bd58f`, `receiving_cells_v15.py` blob `b078cf215c74b76ace6dffcbcbacab6ae22c3673`; model cost `score` from `physical_transfer_screen.py`. The 1D cells, 1-second timesteps, 7m cells and phase `-` label are not an empirically validated vehicle-following system or a legal traffic-signal clearance program.

## P25 — Finite downstream receiver exit headway

[Code](p25_p26_physical_followups.py), [machine manifest](P25_P26_HEADWAY_AND_DOSE_RESULTS_20261122.json), full output SHA `640ec195830abae2ab99d202d43d92aaf3cbbc5f875a0ddc6765fe82f20c19e4`.

Four new *selected* P19 arrival tapes, seeds 112/113 for 1650 vph turn .50 and 116/117 for 1800 vph turn .45, each repeated over capacities2/4, offsets0/15, pocket14/28m, B shares0/.5 and receiver headway **1/2/4s**. Exactly **192 worlds (64/headway), four unique timestamped tapes**. Within each world, baseline vs existing 8s treatment share a byte-identical tick84 checkpoint. Frozen P19 8s effects at headway2 reproduced **64/64**.

| Receiver exit headway | Lower model cost | Higher model cost | Tie | Summed treatment-minus-baseline cost |
|---|---:|---:|---:|---:|
| 1s | 47 | 0 | 17 | -17,194 |
| 2s | 18 | 12 | 34 | -6,960 |
| 4s | 0 | 0 | 64 | 0 |

With 4s exit headway, the objective response is **flat in these 64 worlds** even though the treatment changes attempted receiver entries: the total denied-attempt counts are 7,777 under baseline and 8,029 under treatment. This does **not** prove absence of physical state change. No strict opposite-sign reversal between headway1 and4 exists at epsilon5, since headway4 is entirely tied. Crucially, headway changes before tick84 produce *different checkpoint states*, so contrast across headways is synthetic effect modification, not a same-state causal effect of altering discharge capacity at the decision instant.

## P26 — Same-state 6/8/10-second stage duration plateau

Each of the 64 headway2 worlds has **one immutable checkpoint** and four branches: no intervention, plus model-left-stage durations **6, 8 and 10s** after 3s `-` from tick84. `8s` effects again reproduce P19 64/64. Under penalty60, every duration produces the **same model cost delta in all 64 worlds**, with 18 beneficial, 12 harmful and 34 tied vs baseline. Relative to including no action in the candidate set, 18 worlds favor all three actions equally, 12 favor no action, and 34 have all choices tied.

**Important corrective observation:** *score equivalence is not trajectory equivalence.* Every one of these 64 worlds has differing receiver-denial attempts between 6s and10s (`+4` attempts for 10s), while its terminal remaining-vehicle count is unchanged. Do not report these three interventions as the same physical path or use raw attempt frequency as unique congestion.

## P27 — Longer stage duration (exploratory, pilot-informed)

[Exploratory precommit](P27_STAGE_OPPORTUNITY_EXTENSION_PLAN_20261122.md), [event-traced code](p27_stage_opportunity_extension.py), [result manifest](P27_LONG_STAGE_EXPLORATORY_RESULTS_20261122.json), full output SHA `339a9aacc5f3539bbc65931ab9655f362a58ed19305debca53a25e1a6de9b962`.

Reused 64 geometry-tape classes but tested headway1/2 and durations **6/10/16/24s**, giving **128 worlds**, four complete unique arrival tapes. The 24s candidate was chosen **because a diagnostic pilot had already suggested an effect**. That disclosure is central: this is hypothesis-generating, not a new confirmatory causal claim.

| Exit headway | Duration | Beneficial | Harmful | Tie | Added modeled L crossings in ticks87–119 vs baseline |
|---|---|---:|---:|---:|---:|
| 1s | 6 | 47 | 0 | 17 | 121 |
| 1s | 10 | 47 | 0 | 17 | 137 |
| 1s | 16 | 47 | 0 | 17 | 137 |
| 1s | 24 | 64 | 0 | 0 | 217 |
| 2s | 6 | 18 | 12 | 34 | 111 |
| 2s | 10 | 18 | 12 | 34 | 127 |
| 2s | 16 | 18 | 12 | 34 | 127 |
| 2s | 24 | 41 | 12 | 11 | 207 |

Exactly **64/128** matched worlds have lower model cost under 24s than under 6s; other 64 tie, none becomes worse in this sample. The 64 worlds with changed cost also have different observed modeled left crossing events. The first *tested* longer duration to produce a nonidentical cost is 24s in those worlds; that is **not** identification of the actual threshold, as the intervals 17–23s were not tested.

## P28 — Event measurement non-invariance, not new vehicle congestion

[Source-locked posthoc runner](p28_event_metric_identifiability.py) and [8 tests](test_p28_event_metric_identifiability.py), [P28 result](P28_METRIC_INVARIANCE_RESULTS_20261122.json). The P25/P26 and P27 full output SHA checks **fail closed**, and the overlapping 64 headway2 worlds reproduce the same costs and event counts independently.

- In **64/64 P26 worlds**, model cost for 6 vs10s is identical, but `receiver_denied_attempts` increases by **exactly four** for 10s. The end vehicle remaining count is identical.
- In **128/128 P27 worlds**, 6→10s produces four additional receiver rejection attempts, and 10→16s produces six additional attempts. Yet the 6→10s model cost is the same across all 128.
- Among the 128 6→10s comparisons, **32 worlds change actual model L stopline crossing count** while their final model cost remains identical; **96 worlds change rejected-attempt count without changing L crossings or model cost**.

These are **attempt events conditional on when the candidate stage enables service**. The same blocked vehicle may be refused once per second repeatedly. It is methodologically false to treat denial-attempt frequencies as independently countable blocked vehicles, direct disutility or a policy-invariant measure of congestion. This metric audit does **not** prove that an intervention is physically beneficial, only that different operational traces can map to the same scalar objective.

## P29 — Newly frozen seed-label extension: partial transport, not empirical validation

[Before-running protocol](P29_FRESH_SEED_HOLDOUT_PREREG_20261122.md), [runner](p29_fresh_seed_holdout.py), [7 tests](test_p29_fresh_seed_holdout.py), [sealed compact result](P29_FRESH_SEED_HOLDOUT_RESULT_20261122.json), full output SHA `cb126997cd36c2cc1cec6d54ef7678d68f1ef4367101d46cec8a2ab693c278ec`.

Fresh seeds **120,121 (1650vph,.50 left)** and **122,123 (1800vph,.45 left)** did not appear in P18–P27. Across 2 receiver slots×2 downstream offset×2 pocket×2 B-share×2 exit headway = **128 worlds**, four actual complete arrival tapes, paired t84 baseline, 6s and 24s action.

| Receiver headway | Offset | 24s better than6s | Equal | 24s worse |
|---|---:|---:|---:|---:|
| 1s | 0s | 0/32 | 32/32 | 0 |
| 1s | 15s | 32/32 | 0 | 0 |
| 2s | 0s | 0/32 | 32/32 | 0 |
| 2s | 15s | 32/32 | 0 | 0 |

**HOLD:** This is new *synthetic seed* transport of a previously explored model hypothesis, not a new measured traffic intersection; the different offsets modify the state before tick84. A summary of 64 apparent benefit worlds does not establish broad efficacy across roads or stochastic arrival laws. Notice offset0 contains 16/32 additional L crossings at each headway yet 0 incremental cost improvement: more upstream stopline crossings alone need not improve this terminal cost when downstream reception is constrained.

## Exact code evidence, tests and output custody

- P25/P26/P27 [test suite](test_p25_p26_p27_physical_followups.py): **11/11 PASS** with original P19 JSON, physically executed P25 192, P26 64 and P27 128 cohorts, checkpoint identity, score conservation, forged reference veto. Main blob `b323f45bf74ad021e773138b041c8fc65687ab77`.
- P28 [tests](test_p28_event_metric_identifiability.py): **8/8 PASS**, main blob `eee35d19235daaedabbd52d5ecb056604c81b92f`; local log SHA `429db4d63bbd71016f3e06bd6edb6f168dba0d3c7da4b94f853fa1af414acab0`.
- P29 [tests](test_p29_fresh_seed_holdout.py): **7/7 PASS**, main blob `267a77565fb178262ca3d898f27e215517bded12`; local log SHA `af546caa7d52a912277501fab224f223f7c214d30b35ec71a434e8a529dffde7`.
- All runner/test code was fetched as exact bytes from remote `main`, transported through a read-only Google Docs text bridge, restored locally and verified with `git hash-object` against its GitHub Git blob before test runs.
- **26/26 tests PASS.** Rerun P25/P26, P27, P29 entire outputs produced byte-identical JSON files; P28 result independently SHA-pinned to the two input results. Full result JSON, code, test logs and source hash manifest reside in a local reproducibility ZIP, not invented GitHub raw-file paths. Four complete arrival tapes are shared within each cohort and no pseudo-independent standard errors are claimed.

## Conclusion, failure modes, and next hypotheses

The results strengthen the simulator's *internal* reproducibility but expose two important scientific constraints:

1. **Downstream receiving service opportunities**, not nominal duration alone, govern when an upstream stage extension can alter the scalar simulated outcome. This is conditional on the entire synthetic initial state and arrivals, not a known real-road scheduling law.
2. **Scalar objective blindness and event-measurement bias:** equal final cost can conceal different trajectory/denial histories; raw denials depend mechanically on service attempts and cannot be treated as unique jammed vehicles.

Strong next gates: construct per-vehicle receiver waiting time and distinct blocked-vehicle cardinality **from event IDs**, not event frequency; compare these with frozen penalty cost; repeat across qualitatively different arrival processes, not more geometries reusing four tapes; independently run a SUMO-matched geometry with proper signal constraints and real DLR reference. Do not increase intervention durations further simply to find a larger simulated gain.

K047 and large CIM archive remain sealed/untouched, INTERACTION TC and DR user-downloaded originals await connected Drive upload; no GitHub Actions/bot and no real road intervention.
