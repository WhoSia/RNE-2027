# T2 Research — 2026-11-23

**New day, new research and Drive log.** Historical `20261122/` remains immutable reference; all new work is on GitHub `main`, no extra branches and no GitHub Actions/bot.

- [20261123 dated Research Log folder](https://drive.google.com/drive/folders/1HGigW9JfBuIuG-mx6gK3GjTHAA5XhDZC)
- [20261123 research diary](https://docs.google.com/document/d/1ySC3KhATJ2VyGt4w7Jq77gvatKKcpuVZv7aPskRHUxw/edit)
- [Source-backed P35 scientific findings](P35_FORWARD_ONLY_FIELD_TIMING_FINDINGS_20261123.md)
- [P35 prospective protocol](P35_OBSERVATION_TIMING_PREREG_20261123.md)
- [Python time-bracket and tolerance runner](p35_observation_timing.py)
- [15 source-locked adversarial tests](test_p35_observation_timing.py)
- [Independent Node 22 microsecond oracle (13 parity checks)](p35_independent_node_oracle.mjs)
- [Full per-crossing output JSON](P35_FORWARD_ONLY_TIMING_FULL_20261123.json)
- [Node independent receipt](P35_NODE_INDEPENDENT_PARITY_20261123.json)
- [P35 original input/code/test/log ZIP in dated Drive folder](https://drive.google.com/file/d/1tkVOwNtvGIuTDH2IYoLkKK7DbufkE6NU/view)
- [Notion Harvest N](https://app.notion.com/p/420ef561cf9281ef8b9af3c4198f85b4)

## P35 finding

From the frozen P34-OBS **17** directly bracketed 50ms real geometric stopline-center vehicle crossing candidates and the exact original **30-ID/26,970-row** DLR-UT signal CSV, **11/17** candidates would be paired with a **future** signal sample by retrospective nearest-time matching; **10/17** nearest samples occur even after the entire vehicle crossing bracket. One crossing bracket **straddles** an actual signal sample timestamp and required an interval-aware correction during development. **5/17** events have at least one head with different sampled states on the sides of its interval (8 head×event pairs); the controlling signal head remains **UNKNOWN**. No crossing candidate overlaps P33's 2.004s shared signal gap, although P33 recorded 40 samples of one tracked object in that gap.

P34's publisher-derived 1Hz route-counter agreement depends on the declared allowed timestamp error: **4/17 at ±0.25s, 7/17 at ±0.5s, 10/17 at ±0.75s, 16/17 at ±1s, 16/17 at ±1.5s**. The original **16/17** is *same producer, same origin arm, within ±1s*, not a validated physical lane, vehicle destination or independently measured ground truth.

Latest signal sample available at or before the *start* of the 50ms vehicle bracket has age assessed at the bracket's *end*: ≤0.25s for 3/17, ≤0.5s for 6/17, ≤1.0s for 16/17, ≤1.5s for 17/17. A prior code remains a **sample**, not a continuous guarantee of physical red/green in the intervening second.

## Verified reproduction

P35 main source/test Git blobs:
- Python runner `5e2bc07db32d22474f9c5d9096087c2a82145cfb`.
- Portable Python tests `ed6a563f62e397e5268246806e6b2c219e92cf13`.
- Independent Node oracle `981601f54c42e36e33752e94ea905b415c0afe71`.
- Full results `877c80866acb4c792d448e08007b19764068a88b`.

**15/15 P35 tests PASS, 13/13 independent Node checks PASS, inherited P34 23/23 + P24b 7/7 PASS.** The clean-extracted ZIP re-ran P35 to a byte-identical JSON and all P35 tests/Node checks passed, using exact raw source hashes and unchanged original P34 ZIP. ZIP 112,932 bytes, SHA256 `0080df298e90ea6ab9c0b70eccf3af34598676520e586e41cf7650e8185e8a0d`, uploaded into the new date folder and fetched back with identical SHA.

To reproduce from the exact ZIP, extract and follow its README. The Python runner uses the **original P34 exact matcher** with a temporarily set tolerance restored in `finally`; Node independently parses microsecond UTC and reconstructs max-cardinality/minimum-error matching.

Scientific ceiling: **field-time observation quality**. No 2023 active head-to-lane mapping, no signal timing actuation, no causal queue discharge or validated independent SUMO. Next mainline stage should address actual geometry/head ownership or physically test the receiver model; **avoid another metadata-only stage without returning to the problem of observed discharge blockage and an actionable school-science-fair demonstrator**.

## P36 nighttime crosswalk transfer

[Protocol](P36_CROSSWALK_PROTOCOL.md) · [Findings and reproduction](P36_CROSSWALK_FINDINGS.md) · [Counts](P36_CROSSWALK_RESULT.json)

## P37 nighttime route evidence

[Protocol](P37_NIGHT_ROUTE_PROTOCOL.md) · [Findings and reproduction](P37_NIGHT_ROUTE_FINDINGS.md) · [Aggregate results](P37_NIGHT_ROUTE_RESULT.json)

## P38 breadth and evidence review

[Research scorecard](P38_RESEARCH_SCORECARD.md) · [Green-window observation counts](P38_GREEN_OBSERVATION_RESULT.json) · [Burst-arrival pilot](P38_BURST_PILOT.json)

## P39 model comparison and policy holdout

[Protocol](P39_DECISION_PROTOCOL.md) · [Decision review](P39_DECISION_REVIEW.md) · [Engine results](P39_ENGINE_RESULT.json) · [Policy results](P39_POLICY_RESULT.json)

## P40–P51 finite-link, sampling and individual-impact review

[Protocol](P40_PROTOCOL.md) · [Decision log and priorities](P40_P51_DECISION_LOG.md) · [Finite-link results](P40_RESULT.json) · [Individual impacts](P47_RESULT.json)

## P52–P53 event boundaries and lane allocation

[Stage decomposition](P52_RESULT.json) · [Lane allocation sensitivity](P53_RESULT.json)

The short closed receiver benchmark localizes the through phase-order disagreement to the admitted-to-stopline interval. Changing the T2 through-B share changes the result; intermediate assignment uses the existing seeded allocator. Unobserved boundaries are censored at the horizon. SUMO receiver release is the first downstream sample, while T2 release is the tick at which the vehicle leaves its receiver cells.

## P54–P55 individual crossings and downstream offsets

[Vehicle-level evidence](P54_RESULT.json) · [Clock-offset sweep](P55_RESULT.json)

In the 10 m closed-receiver comparison, the four largest vehicle gaps account for 255.5 of 341.125 vehicle-seconds (0.749, signed contribution). Three of those four vehicles have no direct T2 receiver-denial event. This does not rule out indirect queue effects. At six downstream offsets, changing the T2 through-lane share between 0 and 1 reverses the admitted-to-stop-line contrast at only two offsets (0.333). Therefore compare lane allocation jointly with the downstream clock.

Updated priorities use the P38 weights. Match lane path and downstream clock jointly (.99, .96, .87, .77 → .924); maintain independent field annotation (.99, .93, .67, .75 → .872). The clock sweep is T2-only. A SUMO horizon value of 180 for an unobserved crossing is censoring, not an observed crossing at t=180.

## P56 common downstream calendars

[Findings](P56_FINDINGS.md) · [Paired results](P56_RESULT.json)

## P57 cutoff and vehicle sensitivity

[Findings](P57_FINDINGS.md) · [Vehicle results](P57_RESULT.json)

## P88–P89 follow-up (2026-11-23; execution status explicit)

- [P88 post-tick spatial conservation replay](p88_spatial_audit.py): 192 matched comparisons, five locations (outside, approach A/B, turn pocket, receiver), 30s−60s costs and representative crossing order. **Executed and source-locked: P88 192/192 exact spatial and movement-by-zone identities; see P88_RESULT.json.**
- [P89 startup-lost-green intervention](p89_startup_loss.py): additional 0/1/2/3 seconds of unavailable receiver service at every downstream green onset; separately reports nominal displayed and effective service-eligible seconds. **Executed: P89 768 paired cycle comparisons at 0/1/2/3s loss; see P89_RESULT.json.**
- [Independently recomputed P87 cohort counts and deterministic P89 service-clock arithmetic](P88_P89_PREFLIGHT_RESULT.json): checked JSON reaggregation, **not** P88 or P89 full simulation output.
- [Shared Drive evidence ledger (20261123 dated project folder)](https://docs.google.com/document/d/1wPs7DMY_SL9rV0iUGTEzLQpSE8JXI2tYU5LGynlPos4/edit)
- [Existing Google Docs running diary](https://docs.google.com/document/d/1ySC3KhATJ2VyGt4w7Jq77gvatKKcpuVZv7aPskRHUxw/edit)

The P87 score is the post-movement, post-admission occupancy integral outside + A + B + pocket + receiver (terminal penalty 0 at clearance). Do not interpret receiver-denied seconds as a vehicle-seconds measure. P88 requires all 192 exact signed spatial totals to equal the source P87 cost delta. Neither an unexecuted script nor a clean import can substitute for this test.

For P89, the finite observation window [84,1440) is 1356 seconds, so even with the same 50% *asymptotic* green fraction, observed displayed seconds differ by period and start condition. For green-onset 2s lost time, 30s cycle has 681 displayed/589 effective seconds and 60s has 690 displayed/644 effective seconds. In the red-onset comparison they are 675/585 and 666/620. This is *clock arithmetic*, not a measured travel-time outcome.

## P90–P92 matched-onset audit, multi-metric falsification and BFS control

- [P90 exact matched-onset analyzer](p90_onset_interaction.py) · [P90 matched source-JSON audit](P90_RESULT.json): among 96 common demand tapes, 12 paradox cases occur only with green onset, 43 only with red onset, 0 with both and 41 with neither; 192 experiments are **not** 192 independent arrival tapes.
- [P91 dual-blockage falsification](p91_multi_metric_falsification.py) · [P91 full source-data reaggregation](P91_RESULT.json): 51/55 cost-increasing yet denied-reducing paired cases also have lower full-red seconds. This does not reveal **where** additional vehicle-seconds occur.
- [P92 director-reviewed adversarial procedure](P92_RESEARCH_REVIEW_LOOP.md) · [P90 methodological findings and FHWA references](P90_FINDINGS_AND_ADVERSARIAL_GATES.md): evidence grading, source invariants, counterexamples, twice-DFS-then-BFS discipline, required blocked-state labeling.
- [P92 independent FIFO control code](p92_exposure_negative_control.py) · [P92 saved independent output](P92_RESULT.json) · [event-driven Python oracle](test_p92_independent_oracle.py). For a *toy* FIFO over 600 seconds with 2s startup mask: both 30s and 60s cycles show 300s displayed green but 260s/280s eligible green; sparse arrivals produce equal departure counts **and equal delay**; 80 simultaneous arrivals produce equal 80 departures yet 608 more queue vehicle-seconds for the 30s clock. The event-based Python oracle independently matched these results. **This is NOT a replacement for the pending P89 T2 simulation or field data.**

Historical status before the later full replay: P88 and P89 full simulations were then pending; this has been **superseded by the P88_RESULT.json and P89_RESULT.json validated full runs**. Source-derived P90/P91 and separately checked toy P92 cannot assert 192/192 full spatial reconstruction. The full-window green-seconds discrepancy at 1440 is not by itself a proven mechanism when all test vehicles have cleared. `github-actions[bot]` is not used.

## P93 movement-level trace reconstruction (fully validated in P88/P101)

- [Extended P88 mechanism script](p88_spatial_audit.py) now reconstructs outside waiting **by immutable vehicle ID and movement**, not just counts, and uses native traced A/B/pocket/receiver identities for exact left-versus-through zone contributions. It also reconstructs and checks actual downstream-network departure IDs against network-out count increments.
- [P93 accounting tests](test_p93_spatial_movement_identity.py) · [isolated fixture result](P93_FIXTURE_RESULT.json). A separate Python implementation of the exact accounting function passed one hand-built three-frame positive fixture and two intentionally corrupted negative fixtures. These fixtures predate the full P88/P101 execution; P88 now has 192/192 exact decomposition and P101 128/128 held-out decomposition.
- Acceptance: 192/192 exact signed deltas for P87 cost/denied/full-red, 192/192 five-zone cost identities, 192/192 movement-by-zone identities, event order & network-out consistency, zero remaining on all 384 full runs. Do not print P93 left/through performance estimates until these gates pass.

## P94 literature-backed finite-capacity BFS control

- [Six counterexample states and naive vs capacity-gated one-tick decisions](P94_RESULT.json) · [standalone Python code](p94_capacity_gate_screen.py). The naive pressure proxy `q_up−n_receiver` chooses an infeasible discharge in two intentionally chosen states; a simple feasibility gate avoids these. Independent Python decision evaluation agreed. **These six constructed states do not establish a traffic network benefit or a published capacity-aware algorithm reproduction.**
- [Varaiya (2013), Gregoire et al. and field/CV/pedestrian transfer appraisal](P94_LITERATURE_TRANSFER_AUDIT.md). Source access levels are explicitly separated: full text inspected for Varaiya, abstract/figure-level for other studies. Varaiya's point-queue stability theorem does not transfer to a 4-cell finite receiver, and his MP split analysis does not by itself optimize offset/cycle length.
- New post-BFS priority balance (non-probabilistic): independent simultaneous field exit observation 0.97; full P88/P93 reconstruction 0.96; P89 startup sensitivity 0.93; competing pedestrian/conflicting user cost 0.92; held capacity-aware controller 0.88; actuated/detector error 0.86; independent new arrivals 0.85.

## Latest verified milestone — P88 through P101 (2026-11-23)

**Current evidence status: FULL SIMULATOR REPLAY PASSED; EXTERNAL TRANSPORT STILL OPEN.**

- [P101 director's complete scientific synthesis](P101_VERIFIED_SYNTHESIS_AND_NEXT_GATES.md) is the current interpretation and priority source; previous P88/P89 'pending' notes are historical pre-execution records.
- [P88 full spatial, left/through and downstream-exit results](P88_RESULT.json): 192/192 matches to P87, 384 fully cleared simulator arms; paradox red-onset 43 pairs left +46,853, through −9,248, total +37,605 vehicle-seconds. Four-cell downstream occupancy reductions do not establish reductions for each road user.
- [P89 full startup-loss study](P89_RESULT.json): 768 pairs / 1,536 arms with no remaining vehicles, and 192 loss-zero source matches.
- [P95 seed-block robustness](P95_RESULT.json) · [P96 representative ID/event trace](P96_RESULT.json) · [P97 absolute cost monotonicity screen](P97_RESULT.json) · [P98 two exceptions traced by ID](P98_RESULT.json).
- [P99 fully aligned observation horizon](P99_RESULT.json): [84,1464) exactly 23×60 seconds, 690 displayed green seconds for all period/onset combinations at loss zero, 768/768 signed P89 pairs reproduced, no rank changes.
- [P100 prospective new seed protocol](P100_HOLDOUT_PREREG.md) · [P100 32-seed synthetic holdout](P100_RESULT.json): red onset at 75% left share paradox 64/64, baseline original 32/32; green onset at 25% left share 29/64, 0/192 both-onset paradox.
- [P101 preregistered heldout movement mechanism](P101_MECHANISM_PREREG.md) · [P101 verified 128 spatial pair result](P101_RESULT.json): held-out red onset 64/64 higher left delay, 64/64 A increase, B decrease and outside increase, green onset 0/64 higher left delay.
- Source audit: 8/8 original core-module Git blob SHA match to remote main and 14/14 local core and P93 tests pass. No GitHub Actions bot.
- Google Docs [running diary](https://docs.google.com/document/d/1ySC3KhATJ2VyGt4w7Jq77gvatKKcpuVZv7aPskRHUxw/edit) and [dated reproducibility folder](https://drive.google.com/drive/folders/1HGigW9JfBuIuG-mx6gK3GjTHAA5XhDZC).

**Next non-negotiable boundary**: synthetic seed repetition cannot validate field operations. Independent engine with matched storage geometry, measured simultaneous two-stopline signal/vehicle events, and pedestrian/conflicting user cost are the top scientific gaps. Do not claim real corridor performance from P101.

## P102 external validity veto (historical SUMO evidence)

[Python source-only audit](p102_historical_engine_disagreement.py) · [exact source reaggregation JSON](P102_RESULT.json) · [Drive copy](https://drive.google.com/file/d/1MS74R0AbKs43nIrGraOQRdYLDGvpMOQp/view).

P71 had 64 pre-existing seed cohorts comparing **6s/10s upstream left-green allocations** (not P87/P100 downstream cycle-length intervention) with downstream offset 0s and 15s. On the exact historical P71 signed costs, T2/SUMO ranks agreed in **13/64** at offset 0s and **2/64** at offset 15s; strict opposite ranks were **16/64** and **40/64**, respectively. P71 included unmatched lane/link geometry, and P102 was only a new *audit of archived results*, not a fresh SUMO run. This warning reinforces the external validity stop gate: P100/P101 synthetic seed replication **cannot** substitute for independent-engine geometry-matched tests and actual field outlet observations.
