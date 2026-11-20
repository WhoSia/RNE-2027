# K047 movement and connector evidence, 2026-11-21

## Source correction

The November 13 Drive research decision already cited DLR-UT v1.3.1
documentation page 12, Figure 1. Rechecked the publisher's PDF held in
Drive against the Zenodo MD5 `fa7f80c57c85d58c02ac71a3c100e102`.
In the east-approach panel, group 3 includes westbound straight movement
and group 4 depicts the southbound left movement. Table 3 locates the
signal heads and Table 4 defines the raw state codes. The OpenDRIVE map
links approach lanes −3 and −4 to westbound road 300016, and −2 to the
left connector 300015. The map itself uses a static StVO-294 marker
rather than dynamic signal-controller assignments. The movement assignment
comes from Figure 1; the specific connection comes from the mapped lane links.
This supersedes the blanket mapping uncertainty in the first November 21
audit. The description of unknown sampled states still applies.

[Publisher dataset](https://doi.org/10.5281/zenodo.20919480) ·
[Documentation PDF, Figure 1](https://drive.google.com/file/d/1gUqUJEAGtXw06RjQCLbBoJ0k-pcee5Uq/view) ·
[November 13 research decision](https://docs.google.com/document/d/1RNRrUkM1jw4GZANtttmXSH6G79AsKPbCdfhr0Ucj9hg/edit)

## Registered analysis on previously opened files

1. Reuse the same three 15-minute blocks and the first forward center
   crossing per ID from the earlier audit. Keep the original straight
   gate and add lane −2 as a separately counted left-movement control.
2. Find two consecutive samples from the mapped signal group surrounding
   both vehicle samples of the crossing. Require equal raw codes and a
   maximum gap of 1.25 s. Retain missing/transition and steady
   red/yellow categories separately. Report the other group's codes as a
   control. Retain all lane-gate candidates, including tracks without
   downstream confirmation.
3. Use quarter-meter masks for full straight connector length
   (longitudinal bins 0–8, 8–24, 24–40, 40–52 and 52–60.381 m)
   and the existing west receiver entrance 0–8 m. At a shared raster
   cell between bins, withhold that cell from the ordered path.
   Within 20 s after the crossing bracket, use the same ID to test for
   detections in each consecutive band, and then the west receiver.
   For the left control count same-ID detections on the south receiver
   road at s=5–20 m. No link is inferred when the track ID changes.
4. Independently tally positive and slow (≤2 m/s) center detections
   for each straight corridor band on the original half-second frame
   grid. These are zone observations, irrespective of a center's
   eventual turn. Retain `all` and group-3 bracketed green counts.

These are exploration data. The diagnostic period is deliberately 20 s,
so a missing ordered sequence may reflect a slow vehicle, censoring,
detection failure, an ID split, a route mismatch, or center-mask geometry.
It is not a measured detection rate for slow and stationary vehicles.
The publisher explicitly reports fallible tracking and multi-second
interruptions on the western arm (pp. 24–25). The 18:00–18:30 UTC holdout
is outside this analysis.
