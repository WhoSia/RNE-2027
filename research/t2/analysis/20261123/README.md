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

- [P88 post-tick spatial conservation replay](p88_spatial_audit.py): 192 matched comparisons, five locations (outside, approach A/B, turn pocket, receiver), 30s−60s costs and representative crossing order. **Committed, not yet replayed in an executable Python environment.**
- [P89 startup-lost-green intervention](p89_startup_loss.py): additional 0/1/2/3 seconds of unavailable receiver service at every downstream green onset; separately reports nominal displayed and effective service-eligible seconds. **Committed, not yet replayed in an executable Python environment.**
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

Important limitation: P88 and P89 *full* T2 simulations remain pending. Source-derived P90/P91 and separately checked toy P92 cannot assert 192/192 full spatial reconstruction. The full-window green-seconds discrepancy at 1440 is not by itself a proven mechanism when all test vehicles have cleared. `github-actions[bot]` is not used.
