# RF-CURTAIN — Seeing the reason for green-time non-discharge without images

**2026-11-21 / R&E 2027 / exhibition exploratory track / stage: DESIGN, NOT PHYSICAL DEMONSTRATION**

## The audience-facing idea
"Could a traffic light use the disturbance of ordinary Wi-Fi radio signals as a
non-imaging sensor to distinguish a short left-turn-bay queue from a full
downstream link, before recommending any change to signal timing?"

A camera asks *where do the vehicles appear?* Our experiment first asks
*which physically located radio paths change, and can the pattern distinguish
two causes of unused green?* It also asks explicitly when the answer is NO.

## Not one project with everything bolted on

Track **E** (Exhibition, apparatus + truth labels):
- An authorized indoor, tabletop intersection with vehicle stand-ins.
- A few fixed, known transmitter/receiver radio links across named
  observation zones, each using **our own packets and hardware**.
- Conditions: no demand, moving through traffic, pocket entrance blocked,
  downstream occupied, and both blocked.
- Detect both **stationary occupancy** and motion; when possible, compare
  RF CSI amplitude/phase aggregates to a simple RSSI-only baseline.
- Keep source labels from manually documented model traffic state, not
  the same RF features being evaluated. Optional ground-truth video stays
  offline and is never presented as a Wi-Fi-derived image.
- Main score: held-out-layout and held-out-session diagnosis, false causes,
  abstentions and inference latency; include a negative result if metal
  vehicles/adjacent lanes cannot be separated.

Track **T** (Existing T2 physics, parallel):
- Preserve all current PHYS and arrival-clock result tapes; never
  claim they measure radio propagation.
- Only after **measured** confusion probabilities become available
  evaluate if sensor observations reduce conditional policy regret
  against an admissible signal-action set.
- A traffic signal on a real road is not modified in this project.

## Distinct hypotheses (not accomplished results)
H1: In a controlled small intersection, two spatially separated *authorized, regulation-compliant Wi-Fi CSI observation links using only our own packets* can discriminate pocket-entry
obstruction from downstream congestion across unseen sessions better
than one RSSI link.

H2: The possible improvement does **not** automatically transport when
the link mounting locations, reflective environment or vehicle scale change.
The out-of-placement failure is a central outcome, not an optional note.

H3: Under measured source-classification error, adding a detector may
fail to change any admissible signal-policy choice. Thus sensor diagnostic
accuracy and **decision value** must be reported separately.

## Hard stop/no-go
- We do NOT yet know if any currently owned devices expose CSI; ordinary
  laptop/router RSSI alone is not interchangeable with CSI.
- Public published Wi-Fi CSI vehicle and outdoor crossing research makes
  'Wi-Fi used for traffic detection' prior art.
- First-Fresnel-zone geometry is a *potentially sensitive region*, not a
  pixel grid or a guarantee of lane recognition.
- Target outside school/lab: only after supervising institution approvals;
  no transmitters near active roadway, controller wiring, signal
  modification or third-party device interception.
- Never collect identifiable passenger trajectories, Wi-Fi device addresses,
  unrelated network traffic or human pose data.
- Hardware procurement: **none authorized by this research plan**.
  Start with source review, geometric audit, and existing available gear.
  A public pedestrian Wi-Fi dataset cannot validate vehicle congestion.

## Proposed exhibit
A transparent tabletop junction, labeled model vehicles, two isolated
radio corridors, a display showing each *measured channel-quality trace*
and an honest diagnostic: 'pocket', 'downstream', 'both', 'unresolved'.
A visual camera may be used solely to check the truth labels.
An on-screen virtual traffic light illustrates potential signal
information value; it never operates a real signal controller.

See PRIOR_ART_AND_ALTERNATIVES.md, GEOMETRY_GATE.md, PILOT_PREREG.md.

## RF04 — 2026-11-21 intake and math study (newest stage)

- [Seven papers formally moved from 00_INTAKE to canonical 10_PAPERS; one SHA-pending text duplicate quarantined](RF04_INTAKE_00_LITERATURE_RECEIPT_20261121.md).
- [OpenCSI-inspired known-empty baseline hypotheses locked before code](RF04_OPENCSI_MATH_STRESS_PREREG_20261121.md).
- [Scalar known-empty Welford implementation](open_csi_quiet_calibration_analogue.py), [unit tests](test_open_csi_quiet_calibration_analogue.py), [small artificial numerical fixture](rf04_open_csi_math_fixture.json).
- [Validation receipt: 31/31 local RF unit tests](RF04_INTAKE_AND_CALIBRATION_VALIDATION_RECEIPT_20261121.md); two new source/test files matched local GitHub blobs and JSON local SHA. **Not CSI measurements; no school equipment trial; not author algorithm source-replicated.**
- The 2025 embedded-sensing paper's EMD is **Empirical Mode Decomposition**, not WiTraffic's **Earth Mover's Distance**. Avoid acronym-matching algorithms.
- Research direction: actual measured CSI, separate across-day and across-placement holdouts, correct known-empty calibration, source-of-blockage truth labels. No real road controller or third-party wireless capture.


## RF05 — idea-farming literature and crossed collection design

- [17 new cross-modal paper/dataset candidates + five carried missing originals](RF05_DIVERSE_IDEA_FARMING_MISSING_LEDGER_20261121.md) span fiber-optic DAS, magnetic sensing, audio, mmWave, event vision, thermal, traffic state observability and queue shockwaves. Each includes an experiment and disconfirming control. This is a literature **discovery queue**, not a list of demonstrated inventions.
- [Preregistered 3×2 crossed time/placement evaluation](RF05_CROSSED_HOLDOUT_PREREG_20261121.md), [runnable evaluator](rf_crossed_holdout_evaluator.py), [nine additional tests](test_rf_crossed_holdout_evaluator.py), [synthetic comparison JSON](rf05_crossed_synthetic_suite_summary.json), [verification receipt](RF05_CROSSED_HOLDOUT_VALIDATION_RECEIPT_20261121.md).
- Training uses P1/S1+S2 only. P2/S2 tests placement, P1/S3 tests session, P2/S3 tests joint transfer. Reserve P2/S1 not used. **No tuning on holdout.**
- New RF05 tests **9/9**; combined existing RF01–RF04 **31** + RF05 **9** = **40/40** local RF-only, exact committed Git blobs. All test feature values are artificially class-encoded, **NOT measured CSI**; every synthetic scenario is `NOT_APPLICABLE_SYNTHETIC_FIXTURE`.
- Even a working two-link detector does not imply causally identified traffic queue mechanisms or a safe/controller-admissible action. Real sensor calibration, consented capture, physical validation and context-specific field data remain OPEN.
