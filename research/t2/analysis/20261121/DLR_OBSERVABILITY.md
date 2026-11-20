# K047 joint observability audit, 2026-11-21

## Fixed inputs and meaning of the probes

Use the three already-open 15-minute blocks beginning at 12:00, 12:30 and
13:00 UTC on 2023-09-24. Use the native DLR-UT v1.3.1 trajectories, signal
samples and hash-verified OpenDRIVE map. Record input hashes. No input from
the 18:00–18:30 UTC holdout is part of this audit.

For each 0.5 s slot, select a single actual trajectory timestamp within 26 ms
of the slot start. Never combine rows from adjacent raw frames. At that time
log non-interpolated motor-vehicle center detections in independent zones:

- through approach, road 100000 lanes -3/-4 at s=135–155 m;
- inner through lane and adjacent left bay at s=80–105 m, road 100000;
- connector entry, road 300016 lanes -1/-2 at s=0–8 m;
- west receiving entry, road 101000 lanes -1/-2 at s=0–8 m.

Use the StVO-294 reference at s=155.566906348012 m for positive crossing
evidence. A center crossing requires the same ID in two consecutive usable
observations at most 100 ms apart, signed displacement through the line in
the driving direction, and a lateral crossing within mapped lanes -3/-4.
Keep each track's first accepted candidate per block. Count a crossing in a
0.5 s slot only when both bounding observations are inside that slot. This
does not recover front-bumper service time or detect every crossing.

Reuse the existing 20 Hz signal bracketing rule for approach heads 3 and 4.
Report head 3 green results and the 3/4 state contingency separately.
No documented mapping from these heads to the specific through movement has
been verified, so the exposure is labelled head-3 bracketed green.

## Evidence gate

The masks are map geometry and carry no information about sensor coverage.
Absence of a detected center leaves vehicle presence unresolved. A slow
observed center at the west receiving entry neither proves a full link nor
places a queue at the stop line. The through connector and west receiving
entry are spatially separate. Positive co-detections establish simultaneous
observations. Spillback claims and counterfactual signal effects require
additional evidence. Zero detected crossings leave actual discharge unknown.

## Post-run sensitivity check

The first run produced sparse slow detections in the 0–8 m west entry
mask. Keep that mask as the primary probe. Add the earlier work's 2–24 m
west strip as a descriptive sensitivity check and retain center detections
at any speed in both masks. Record whether near-stop slow detections
coincide with a contained crossing candidate. This guards against calling
a missing crossing candidate a measured zero.
