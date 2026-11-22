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
