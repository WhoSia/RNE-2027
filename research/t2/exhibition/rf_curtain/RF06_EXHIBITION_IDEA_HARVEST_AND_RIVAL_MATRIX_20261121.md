# RF06 — Mechanism-first creative idea harvest, 2026-11-21

**Research state:** 20 primary academic PDF originals reviewed at abstract/selected-method level, all in Research OS 10_PAPERS. No 5 GB `CIM dataset.zip` touched. Ideas below are **UNBUILT HYPOTHESES**. An exciting sensor mechanism is not in itself a published novel invention; no real traffic-controller connection is authorized.

## 1. The "why green produced no vehicles" scientific exhibit

**Exhibit one-sentence:** A traffic light is asked not only to count cars, but to say **whether it knows why nothing moved during green**.

Use two physically staged obstructions, turn-pocket entrance P and downstream receiving space D, with the exact four hidden states P,D=(0,0),(1,0),(0,1),(1,1). Let the student demonstrate that a single overall queue-count or wireless disturbance cannot determine P vs D. A small magnetic/physical occupancy flag or controlled, *known-stable* RF link may reduce ambiguity. Show `UNRESOLVED` instead of claiming a fact absent evidence.

**Known prior art:** Hu & Fan (2024) network traffic observability [PDF](https://drive.google.com/file/d/18GmpK9i-5yfnXNZzL9MImxDjLOl8PYem/view); Bao et al. (2016) tailgating magnetic [PDF](https://drive.google.com/file/d/1TJSzVqvqVykKNHqztKgUeRan-l8Vkjk0/view); WiTraffic (2017) [PDF](https://drive.google.com/file/d/1hMMeALKst2WyQUGAw0EorCZG6ddSkdK4/view); existing T2 queue/receiver model.

**Strong falsifier:** equal full five-class, independently manual labeled test data at two placements and multiple sessions, but RF/magnetometer pair still confuses pocket-only versus downstream-only. This would refute the proposed dual-cause source classifier regardless of in-sample F1. Report negative result.

**Mechanism caution:** a staged obstruction is NOT a realistic traffic driver's cause for lost green; physical queue-source semantics must be separately tested with a traffic-state model. No real signal actuation.

## 2. "Traffic noise is missing" — paired acoustic & static magnetometer

**Exhibit:** A pair of microphones detects moving sound, magnetic occupancy detects a steel toy held still, and camera-only *manual truth* labels show whether either system can distinguish empty road from blocked road. The focus is the *absence-of-motion paradox*, not vehicle recognition novelty.

**Source:** Toyoda et al. (2014) [PDF](https://drive.google.com/file/d/1XQN1ekuwCOhLva7xKkVb3zp-7Zxdaxz4/view) uses asynchronous microphone synchronization and propagation-time lane differences; Na et al. (2015) [PDF](https://drive.google.com/file/d/1FHz8oPaT3cQ94brjVB_gL7WH6uDBKSdZ/view) uses cross-array acoustic processing. Marciniuk et al. (2018) [PDF](https://drive.google.com/file/d/1YMYD11ubUROv8PsqP8fQyASfU2kTlnpK/view) combines acoustic sensors and accelerometers. Culík et al. (2023) [PDF](https://drive.google.com/file/d/1LzpfR65R1-4Jqhf5BUjF4lHuOwgbn_wu/view) flags count versus vehicle-type/speed failures. **Traffic Ear 2023 includes camera: it does NOT establish acoustic-only performance** [PDF](https://drive.google.com/file/d/1oBl_7-hNZeQgACnj05GY97908sOXfAq8/view).

**Strong falsifier:** in a quiet tabletop, static magnetism or material cannot represent full-size real vehicles; external background voices and near-silent electric vehicles cause audio mistakes; a magnetometer signal may be dominated by nearby fixtures. Stop mechanism claims if so.

## 3. "Camera that sees only change" — event camera static-queue blind spot

**Exhibit:** compare motion event count (rather than full video) with actual occupancy truth during transition, static holding and departure. A stale event should never be substituted for a continuous count. Freeze event time bin before measuring.

**Prior art:** eTraM CVPR2024 [PDF](https://drive.google.com/file/d/1MiQ5sTcIdGMuYSeJzQ570P_RHciq-GCp/view), TUMTraf CrossVision (RGB+event cross-view) [PDF](https://drive.google.com/file/d/19YSXLEoTG80OAsYXuyCpbylQe8VnLhpw/view), Fu et al. 2017 thermal-vs-visible [PDF](https://drive.google.com/file/d/1v2qbvTVYrIPnh2R0sADWkgWClgdk80YY/view).

**Falsifier:** sensor noise and small camera/illumination changes produce events during a static toy; event counts may not separate stop vs empty robustly. Commercial event cameras are expensive and event-image recordings still require privacy review. No claim of invented event cameras.

## 4. "The fiber under the road is the loop detector" — institutional future lane

**Exhibit:** with an institutionally licensed DAS sensor *or pre-existing legal research datasets*, infer linear vehicle traces from time-distance vibration images, visualize why some traces disappear at low speed and poor mounting. No fiber interrogator = NO DAS measurement.

**Source chain:** Corera et al. 2023 [PDF](https://drive.google.com/file/d/1CubEikHNzN2F_LZIYc7eetfUudWtNcto/view) Hough-like time-distance transform; Thomas et al. 2024 [PDF](https://drive.google.com/file/d/1aGEr3gikM-lscX85EvKC492VRu2GESwf/view) mounting geometry (~10 dB signal quality variation) and phase vs intensity; Truong et al. 2024 [PDF](https://drive.google.com/file/d/1inKIoSzvnfjdEGBNlCoPJjewLg2aIfVW/view) Hough+DBSCAN; Deng et al. 2025 [PDF](https://drive.google.com/file/d/1CiLcB1RzAKsukMkBnlZipFH58DA_OqDy/view). A broader road engineering 2025 review is already held in another Drive project [PDF](https://drive.google.com/file/d/170xG64S_vUE28HC_JnFvHMK5GeGGWU2-/view), don't duplicate it.

**Falsifier:** tracking vehicles crossing a buried fiber may be possible for some coupling situations but still fail at stationary queue, adjacent lanes and traffic stopping causes. High instrument cost, cannot infer raw strain from a normal cable without laser/interrogator hardware.

## 5. "One sensor or one extra second?" — dynamical observability thought experiment

Two possible approaches to distinguish near-identical traffic congestion:
- A new physical measurement (e.g., known pocket bit) supplies an independent observation row now.
- If the **correct** traffic dynamics are known, two successive aggregate measurements may distinguish states because one obstruction dissipates faster than another.

Use a frozen two-state linear model x(t+1)=A x(t), y=C x(t). With A=I and C=[1,1], y=x_p+x_d is identical for states (1,0) and (0,1), forever; no amount of repeated aggregate measurement helps. With A=diag(a,b) and a≠b, two samples yield observability determinant (b-a) and make formal identification possible, **but estimation becomes ill-conditioned as |a-b|→0** and inflows/controllers invalidate the assumed autonomous dynamics. An independent pocket measurement can instead restore full rank immediately in a toy. This is a mathematical **transfer** of Hu & Fan (2024), not a reproduction of their nonlinear/graph road model.

**Falsifier:** vary the unmeasured inflow, change between A matrices or add small measurement noise, and ask whether the inferred cause remains unique. If not, issue `UNRESOLVED`. This is also a strong prior art reminder: observability theory already exists.

## 6. "Only two smart measurements" — information entropy versus decision value

Shannon information is not the same as task-specific utility. On a 4-state toy, `number of blocked zones` carries 1.5 bits under uniform prior but cannot tell pocket-only from downstream-only, while an ideal pocket-local flag carries just 1 bit and is sufficient to tell *whether the pocket* is occupied. **This strict counterexample must be reproduced exactly in code** and prevents our T2 from optimizing sensors by generic mutual information alone.

**Source:** Zhang et al. (2026) [PDF](https://drive.google.com/file/d/1OCDtJcGTh8Red2IlpwYFtTMnl8Bd1pBB/view), NMI/IGNNK network-reconstruction evaluation on synthetic Chicago flows and Hu & Fan 2024. Their NMI selector can be better than PCA in some sensor-budget ranges, but not universally; this is not our novelty.

**Falsifier:** task label is redefined from pocket occupancy to complete 4-class mechanism diagnosis: pocket flag alone is not enough. Sensor value must be reported for the stated target task, prior, costs and time.

## 7. "Traffic camera without a field camera" — reusable dataset source audit

The user has not authorized use of `CIM dataset.zip` and it remains ignored. Separate paper PDFs are HELD:
- Soom et al. (2024) [mmWave and RGB paper](https://drive.google.com/file/d/1LWujhwAvrgZEEZsnPkHXOJXqMTw3-V38/view) describes point clouds and >8000 annotated images.
- eTraM paper has ~10h published events and 2M labels by its authors.
- CrossVision paper has 23,128 images with 83,026 boxes, published by its authors.

**These paper PDFs are NOT proof that their datasets have been downloaded/licensed, and their labels are vehicle classes/boxes, NOT T2 causal blockage classes.** No data download, training, or external performance comparisons are claimed here.

## Research-pipeline direction

The immediately actionable work (no new hardware) is a **fully exact finite-state observability and decision-specific information baseline** with explicit assumptions, accompanied by a second linear observability rank/determinant example. Preregister this before implementing, prove expected results under a uniform and asymmetric prior, and expose no realistic controller safety claim. This is an academic toy bridge from T2 to novel sensing, not RF performance evidence.

The future physical priority is (i) stop/empty stationary contrast, (ii) blinded day × placement heldouts (RF05), (iii) real RF/chip or magnetic evidence under authorized lab equipment, (iv) only then sensor errors into traffic-policy regret. K047 sealed, no roadside installations, GitHub Actions/bot disallowed.
