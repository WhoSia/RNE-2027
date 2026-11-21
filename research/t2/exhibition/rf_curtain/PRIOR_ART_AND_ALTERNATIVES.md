# RF-CURTAIN — Prior art, precision of claims, and competing exhibit concepts

Audit date: 2026-11-21. This is a bounded web/source-landscape scan, NOT
a systematic literature review. Text was read from abstracts, project
pages or official documentation unless full text is explicitly noted.

## We cannot claim these inventions

| Work | What was already attempted | Consequence for our claim |
|---|---|---|
| Won et al., **WiTraffic**, ~2017, https://digitalcommons.memphis.edu/facpubs/3343/ | CSI patterns of passing vehicles for classification, lane detection and speed | 'Vehicle detection with ordinary Wi-Fi' is clearly old |
| Won, Sahu & Park, **DeepWiTraffic**, MASS 2019, DOI 10.1109/MASS.2019.00062, https://digitalcommons.memphis.edu/facpubs/2683/ | Two Wi-Fi transceivers and CSI amplitude/phase for vehicle-type detection | CSI vehicle sensing and simple portable apparatus already exist |
| **ESP32-Based Wi-Fi CSI for Traffic Monitoring and Congestion Detection**, QPAIN 2025, IEEE document 11172128, https://ieeexplore.ieee.org/document/11172128/ | ESP32 CSI for traffic-monitoring/congestion and signal-automation concept; limited evidence from accessible abstract | Cannot claim 'ESP32 Wi-Fi traffic lights' as original; independently inspect full methodology before novelty assertion |
| **A Traffic Information Detection Method at Single Intersection Based on Wi-Fi Data**, Applied Sciences 2025, DOI 10.3390/app15105407, https://www.mdpi.com/2076-3417/15/10/5407 | Wi-Fi **probe requests and MAC association/space-time** rather than CSI RF obstruction | Do NOT merge passive handset probe sensing with device-free CSI sensing; privacy and sampling biases differ |
| Dharmaraj, Dias & Hemachandra, **Enabling Scalable, Privacy-Preserving Smart Pedestrian Crossings with CSI-Based Sensing on COTS Hardware**, ITSC 2025 (IEEE online Mar 2026), https://ieeexplore.ieee.org/document/11423151/ | Outdoor pedestrian movement detection in 4 sites and 7 people; reported 96.9% movement detection but **up to 62% direction classification** | Outdoor CSI direction inference is not a solved problem; no transfer to vehicles warranted |
| Niu et al., **WiCrossing**, IEEE IoT Journal 2026, https://researchportal.ip-paris.fr/en/publications/wicrossing-the-first-fresnel-zone-crossing-detection-using-commod/ | First Fresnel zone crossing detection using commodity Wi-Fi | Even 'RF curtain' crossing trigger is prior art |
| Guo et al., **Optimal Sensing Boundary Identification for Adaptive Signal Timing via Bayesian Online Learning**, Sustainability 2026, DOI 10.3390/su18179194, https://www.mdpi.com/2071-1050/18/17/9194 | Selection of upstream observation boundary for adaptive signal timing | 'Where should a sensor go?' alone is not original |
| **IEEE 802.11bf-2025**, https://standards.ieee.org/ieee/802.11bf/11574/ | IEEE amendment for WLAN sensing, published 2025-09-26 | Mature standards context, not an invention by this project |
| Espressif ESP-IDF Wi-Fi CSI documentation, https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/wifi-driver/wifi-vendor-features.html | CSI callback APIs and ESP32 hardware caveats | Hardware availability/driver support must be checked, not assumed from a generic router |

## Alternative innovations assessed

**Candidate A — RF-CURTAIN (first experimental gate).**
Wi-Fi CSI through *known* tabletop locations to diagnose the **cause**
of wasted green when turning-pocket entrance and downstream receiving link
are separately blocked. Strong connection to T2, high public demonstration
value and possible reuse of existing Wi-Fi equipment, but high
multipath/static-occupancy/adjacent-lane confounding; no measured
vehicle classification yet. Novelty must be in **tested decision-relevant
mechanism distinguishability and the refusal-to-infer boundary**, not
in inventing Wi-Fi traffic sensing.

**Candidate B — mmWave radar + optional UWB crossing monitor.**
Already demonstrated in 2026 road VRU tracking:
https://www.mdpi.com/1424-8220/26/5/1690
and in older roadside intersection work:
https://rosap.ntl.bts.gov/view/dot/60935.
This is engineering-realistic but comparatively less surprising and
not free without existing institutional hardware; static target handling
and weather/occlusion need independent proof.

**Candidate C — camera-free geomagnetic/vibration lane proxy.**
Cheap in concept if existing educational magnetic sensors exist, but
detecting moving metal does not itself identify *pocket-induced*
blocking, and road surface installation/permissions are nontrivial.
This is a backup laboratory control signal, not a claimed invention.

**Candidate D — passive handset probe / Bluetooth counts.**
Rejected as a primary route: it measures discoverable *devices* rather
than all vehicles, is biased by handset ownership/randomization and
may collect network identifiers. Contrasts with device-free CSI and
is ill-suited to privacy-preserving school demonstration.

**Candidate E — optical camera + traffic AI.**
Strong measurement baseline for laboratory truth, but prior methods
and proprietary/dataset video labeling are established; a camera
alone is less unusual and road surveillance/privacy add constraints.
See 2026 Louisiana Transportation Research Center report:
https://rosap.ntl.bts.gov/view/dot/92000.

## Claimed gap, carefully phrased

Hypothesis for a science fair, not established novelty:
"A **camera-free**, fixed multi-link CSI instrument, optimized
specifically to tell *left-turn-pocket obstruction from downstream
receiving-link blocking*, can achieve **useful out-of-placement
source attribution** compared with an RSSI link."

Publication novelty and freedom-to-operate are **unverified**.
A fair prior-art review must later compare exact feature extraction,
sensing link layout, training split and real field baselines, including
the 2025 ESP32 CSI intersection work and 2017 WiTraffic.

## Data source caveat

WiPCI (https://github.com/LiuSjia/WiPCI) describes an *outdoor
pedestrian* CSI dataset, not metal vehicle queues. WiSe4Car
(https://ieeexplore.ieee.org/document/11125778/) concerns Wi-Fi CSI
**inside** vehicles. Neither is a substitute for independent
pocket/downstream ground-truth scenes. A released dataset must
be license-checked before redistribution or reuse. We have not
downloaded, licensed, trained on, or validated such a dataset.
