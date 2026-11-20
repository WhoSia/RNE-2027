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

## Results

Of 188 center-crossing candidates in mapped east straight lanes, all
188 were detected in the first connector band. 182 had ordered hits in all
five connector bands and 179 had those hits followed by a same-ID hit in
the west entry. 180 had a same-ID west hit when the intervening-band
requirement was dropped. The sample window starts just after the earlier
gate sample. A hit in every band is not a statement that tracking was
continuous between hits.

| Candidate cohort | N | Mapped green (5) | Mapped yellow (7) | Mapped red (3) | Missing or transition | Other group green (5) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Straight lanes −3/−4 at gate (group 3) | 188 | 170 | 3 | 1 | 14 | 22 |
| Left lane −2 at gate (group 4) | 96 | 57 | 12 | 3 | 24 | 23 |

All 96 left-lane candidates were detected at the south receiver within
the window. Positive same-ID detections support the external map
assignment. Neither the steady-red nor yellow **center** brackets can
establish the vehicle's entry time or driving compliance. They stay in
the denominator without being relabeled.

| Region | Any center, all frames | Slow center, all frames | Any center, group-3 green | Slow center, group-3 green |
| --- | ---: | ---: | ---: | ---: |
| Connector 0–8 m | 285 | 0 | 153 | 0 |
| Connector 8–24 m | 487 | 0 | 238 | 0 |
| Connector 24–40 m | 934 | 3 | 260 | 0 |
| Connector 40–52 m | 812 | 1 | 178 | 0 |
| Connector 52–60.381 m | 666 | 0 | 126 | 0 |
| West entry 0–8 m | 565 | 2 | 120 | 0 |

All exposure denominators are 5,400 and 866 respectively. The band counts
are marginal, may involve repeated vehicles, and cannot be summed into
distinct occupied frames. They include any detected motor-vehicle center
in the mask, even in shared parts of different movement paths. The slow
hits in the interior bands are detections, not queue events. The moving
cohort is a positive tracking control. The resulting 179/188 is neither
complete observation of the connector nor detector sensitivity for a queue.

## Research direction

Keep T2 on the east approach of K047 for discharge timing and for student
annotation of positive controls and ambiguous cases. Stop tuning this set
of exploration blocks to find an example of physical blocking. The field
branch should first screen another viewing angle or an independently
observable approach using the same tuple of movement, waiting through
demand, pocket entrance and receiving storage, then manually label whether
the queue grows continuously from the downstream link. Do not open the
timed holdout merely to look for a positive case.

On the modeling branch, hold fixed the initial queue, complete ordered
arrival stream, green times, clearance and horizon when comparing lead
with lag. Compare (i) separate unlimited through and receiving lanes,
(ii) a finite pocket alone, (iii) finite receiving storage alone, and
(iv) both limits. Compare distinct vehicles discharged and time with
through demand and lost service, and record what a policy actually knows
at decision time. Report the sign and range of paired differences over
all arrival orders compatible with the same observed aggregates.
This retains the original physical question while preserving established
prior work on short pockets and phase-design throughput effects. The
exhibition needs a positive event with a visible queue tail and an
independently labeled discharge. The model may still produce falsifiable
claims about the sufficiency of pre-decision observations.

## Reproduction

From `research/t2/efficiency_loop`:

```sh
python dlr_route_evidence.py "$DLR_ROOT" /tmp/route_evidence.json
cmp /tmp/route_evidence.json ../analysis/20261121/route_evidence.json
```

[Block-level aggregate and input hashes](route_evidence.json).
Documentation SHA-256
`94fd9ebd32d04a9c35b02be526fbd11a8d5a613933d7961fde800386853b34f3`.

### Follow-up window sensitivity

After the primary run, repeated the same path criterion with 10 s and 40 s.
All three windows recover the ordered path in 179 of 188 candidates.
The block end falls inside the potential follow-up for 4 candidates at
10 s and 10 at both 20 s and 40 s. These counts measure potential
administrative censoring, including cases where the path was already
observed in time. They cannot attribute the nine unmatched cases.
