# 2026-11-21 — Which unconventional traffic sensor deserves an R&E exhibition?

This is a **comparative research judgment**, not a patent novelty
search, field trial, procurement decision or empirically rated score.

## Comparison using the same criteria

| Candidate | School tabletop demonstrability | Mechanism specificity for short left-pocket vs downstream | External precedents | Key fatal risk | Decision |
|---|---|---|---|---|---|
| Multi-link Wi-Fi CSI RF-CURTAIN | Conditional on available CSI-enabled device; no new purchase yet | Hypothesis specific to *two* longitudinal queue sections | 2017/2019 WiTraffic, 2025 ESP32 CSI congestion, 2026 WiCrossing | Multipath and static metal may erase spatial attribution | **Proceed only to paper design and local feasibility gate** |
| mmWave radar without camera | Conditional on existing school radar hardware | Can potentially measure position/movement; must separately prove queue cause | 2021 roadside mmWave, 2026 radar/UWB VRU studies | Module cost, weak static target/occlusion and substantial prior art | Backup if accessible hardware exists |
| Magnetometer/structural vibration | Often simple demonstration but sensor placement matters | Metal vehicle passage is not a queue cause label | Long-established roadside detection; literature review still needed | Needs physical placement near moving vehicles to sense occupancy | Classroom baseline only, not road implantation |
| Camera + AI signal timing | Common in schools if consent/safe lab | Ground truth easiest, but no visual novelty | 2026 LTRC vehicle/queue/pedestrian analysis; extensive prior art | Privacy/occlusion and generic project scope | Use only as controlled truth reference |
| Scanning public Wi-Fi probe requests | Superficially simple | Counts phones, not vehicles or mechanism | 2025 single-intersection Wi-Fi probe study | Device bias, identifier privacy, no CSI | **Reject** |

## Preferred concept and tightly scoped research claim

**RF-CURTAIN — A camera-free RF diagnostic of *why*
a model intersection loses green-time discharge.**

Specific hypothesis that can genuinely fail:
Two longitudinal Wi-Fi channel links convey enough independent
information to distinguish **short-pocket entrance blockage**
versus **downstream receiving blockage** across new placements,
better than a simple RSSI link. If not, reject the sensor
or pivot to a physically more localized modality.

The **special part must be the new experimental evidence about
which blocking causes are observable**; the phrase 'Wi-Fi
vision' by itself has no originality. We do not claim broad
'privacy preserving': some RF systems can infer human
presence/pose and still require consent and a privacy review.

## Why no purchase today

The user requested an unusual science-fair direction, not to
buy hardware. Inventory school equipment, official chips and
publicly redistributable datasets first. Even a photograph or
tweet of a Wi-Fi skeleton does not establish detector quality
at an intersection.

A safe indoor model, openly documented negative outcomes and
the connection to traffic decision observability make a
stronger experimental story than a weak 'AI optimizes traffic
lights by Wi-Fi' demonstration.

## Single strongest falsification

Keep original and RF sensor mounting geometry locked, train
on early lab sessions and one placement, and reserve a new
placement/day entirely blind. If the two links cannot
distinguish pocket from downstream in that blind set, the
core proposed RF novelty does not survive. Report it openly.
