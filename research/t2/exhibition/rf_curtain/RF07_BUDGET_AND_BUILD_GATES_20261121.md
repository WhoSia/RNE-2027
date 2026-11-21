# RF07 — Budget-first build/no-build decision gates

No hardware purchase or permission is granted by this design note. Prices deliberately NOT asserted without local quotations. First identify available equipment and implementation constraints.

## Tier 0 — no purchase, robust scientific control
- Desktop Python exact noisy-channel model (RF07); printed cards/tabletop labels; optionally an existing webcam for **independent ground truth only**.
- Existing laptop microphone produces activity amplitudes, but quiet stationary occupancy vs empty is likely fundamentally ambiguous.
- Existing webcam frame-difference can simulate an event sensor, but stationary occupancy cannot be inferred from events without state/memory assumptions.

## Tier 1 — inexpensive electronics, only if inventory/approval
- Own ESP32 board(s) with firmware-supported CSI, and separated fixed transmitter/receiver observation links. Do not assume a phone/laptop Wi-Fi indicator is CSI.
- Magnetic sensor for model cars ONLY if a steel/magnet marker and mounting are specified; separately note that marker recognition is not ordinary vehicle detection.
- Infrared break-beam pair and photodiode control for empty/occupied distinctions; may work better than RF at small scale.

## Tier 2 — publicly available data or institutional loan
- Event-based camera, mmWave radar, optical fiber DAS. Use verified dataset licensing or institutionally loaned equipment. A regular glass fiber with no interrogator is not an operating DAS sensor.

## Go/no-go matrix
A candidate can become the **flagship exhibit** only if it passes ALL:
1. Building and operation can be safely supervised indoors using owned or properly approved devices.
2. It detects at least one scientifically stated contrast under unseen-session controls.
3. Its result is independently checked and errors are displayed, including abstention.
4. It beats or meaningfully complements a cheaper baseline on the stated task.
5. The apparatus, latency, per-unit economics and placement limitations can be explained to judges without claiming first-in-world novelty.

Fallback: A striking counterexample is itself a working exhibit — explain scientifically why a moving-object detector fails on a stationary queue, and demonstrate a cheap independent sensor that resolves that ambiguity.

## Measurement plan for the next lab session
Collect a signed inventory (model of chips and antenna configuration, lab network approval, manual truth channel, mounts, number of movable objects). Freeze P1/S1–S3 and P2 placements before any RF recording. Preserve raw source with provenance but no personal device identifiers. The unapproved 5GB CIM dataset stays untouched.
