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

The primary head bracket has a 1.25 s maximum sample gap. As a separate
sensitivity calculation, relax only that limit to 2.05 s and retain the
unchanged neighboring-state and transition checks. The wider bracket
can mask an unobserved transition if the head changed twice between
samples. Its counts measure rule sensitivity, without validated coverage.

## Observed counts

| Observable | All retained frames | Head 3 green, 1.25 s | Head 3 green, 2.05 s |
| --- | ---: | ---: | ---: |
| Frames | 5,400 | 866 | 878 |
| Slow center near stop reference | 2,077 | 96 | 98 |
| Slow center near stop with no positive crossing bracket in slot | 2,060 | 82 | 84 |
| Slots with a positive crossing bracket | 165 | 97 | 97 |
| Both sides of adjacent taper detected | 71 | 23 | 23 |
| Center detected in west entry (0–8 m) | 565 | 120 | 122 |
| Center detected in shifted west strip (2–24 m) | 1,078 | 228 | 232 |
| Slow center in west entry (0–8 m) | 2 | 0 | 0 |
| Slow center in shifted west strip (2–24 m) | 0 | 0 | 0 |
| Slow center at connector entry | 0 | 0 | 0 |
| Positive co-detections in all five primary zones | 0 | 0 | 0 |

A slow detection uses a velocity magnitude of at most 2 m/s. Counts are
frames or slots, as indicated, and repeat detections can involve the same
vehicle. The entrance strip and shifted strip overlap, so their counts
cannot be summed. The two non-green-or-unknown west-entry slow detections
occurred in the 13:00 block and both coincided with a slow near-stop center.

The primary bracket leaves head 3 unknown in 2,322 frames. Of its 866
green frames, head 4 is green in 135, non-green in 696 and unknown in 35.
The 2.05 s bracket leaves head 3 unknown in 2,289 frames. The stricter
primary exposure remains the basis of the field audit. There were 188
positive first-center-crossing candidates across the three blocks
(56, 68 and 64). Of those, 18 straddled slot boundaries and 170 fit in 165
retained slots. Report crossings and frame counts as different denominators.

## Research decision

Keep both blocking mechanisms in simulation. In this open K047 sample we
can compare independently detected motion and retained signal-head
readings. Leave field labels unresolved for pocket blocking versus
spillback and for true zero discharge. The map represents the 60.381 m
straight connector as a separate road. An outlet probe does not locate the
queue tail anywhere along that connector.

For a field test, document which head authorizes the tested movement and
register view coverage along the taper, the stop reference, the connector
and its receiving lanes. Track the queue tail from the receiving link
towards the stop line and record visible gaps, demand and crossings over the
same green interval. A second observer should label events independently
from the simulation. Keep the later holdout unopened until these
requirements can be tested on an open block.

## Reproduction

From `research/t2/efficiency_loop`, run:

```sh
python dlr_joint_observability.py "$DLR_ROOT" /tmp/joint_observability.json
cmp /tmp/joint_observability.json ../analysis/20261121/joint_observability.json
```

[Aggregated output and input hashes](joint_observability.json).
[DLR Urban Traffic v1.3.1, publisher record](https://zenodo.org/records/20919480).
