# T2 P23 — Official DLR-UT signal codebook and signal-purpose audit

2026-11-22 KST. **ACCEPT codebook interpretation and broad motor/VRU signal purpose; HOLD signal-to-movement/stopline identification, subsecond discharge headway and independent SUMO.**

## Actual primary evidence inspected

Original [DLR Urban Traffic v1.3.1 documentation PDF](https://drive.google.com/file/d/1gUqUJEAGtXw06RjQCLbBoJ0k-pcee5Uq/view), 27 pages, SHA256 3c733b677ee63fd2cb282946f415f649d23954ac420d5bc37e0af545f7293849. Printed page 14 **Table 4** defines all 10 light-state codes. Printed page 12 **Figure 1** maps the signal IDs and their broad participant purpose; both figures were actually rendered and visually inspected. Printed pages 12–13 **Table 3** gives UTM 32U physical head coordinates, not a verified lane controlling each detector movement.

Original [23:30–23:45 UTC signal CSV](https://drive.google.com/file/d/1TXma5bvw_M-NSfqO2LhW7JrEFqANxUOy/view), SHA256 95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c. There are 26,970 records, 30 signal IDs, 899 records per signal.

## Publisher state codes

| Code | Official semantic state |
|---|---|
| 0 | unavailable |
| 1 | off |
| 2 | stop required before proceeding |
| 3 | red, stop and wait |
| 4 | red and yellow simultaneously |
| 5 | green |
| 6 | protected green movement |
| 7 | yellow |
| 8 | protected yellow movement |
| 9 | yellow flashing |

The sampled night window shows 1/3/4/5/7/9, not 0/2/6/8. Absence in this window does not prove that other windows lack protected movement opportunities.

## What a vehicle signal actually is

The publisher Figure 1 identifies IDs 1–9 as motor-vehicle heads, IDs 10–29 as bicycle/pedestrian signal heads, and ID 30 as a special yellow-flashing warning for motor traffic concerning a vulnerable-road-user movement. These are broad group definitions, **not validated lane- or phase-specific control assignments**.

| Participant purpose | IDs | Rows | Red code 3 | Green code 5 | Other |
|---|---|---:|---:|---:|---|
| Motor vehicle | 1–9 | 8091 | 6105 | 1645 | red+yellow 86, yellow 255 |
| Bike/pedestrian | 10–29 | 17980 | 14819 | 3035 | red+yellow 42, yellow 84 |
| Special VRU warning | 30 | 899 | 0 | 0 | off 604, flashing yellow 295 |

Summing all 30 IDs into a single motor green fraction would mix incompatible signal purposes and count a special warning device as a conventional motor signal.

## Sampling, no invented green transitions

Across 26,940 within-ID adjacent recorded gaps: median 1.000 s; minimum 0.879 s; maximum 2.004 s; **30 gaps above 1.5 s**. Each observed state change only bounds a real transition between timestamps; it does not prove exact amber or all-red durations. The earlier 869 code changes are sample transitions across independent signal IDs, not 869 full controller program switches.

## Executed exact source tests

[Decoder](p23_dlr_official_signal_codebook.py) local Git blob 6866838ef5df68b761cb93e6ae837af1d66810ee and [5 tests](test_p23_dlr_official_signal_codebook.py) blob d0a33abe4788a8954c78a9b1f3a772f5fafe7ca4; both exactly match actual remote GitHub main blobs. **5/5 actual-source tests PASS**, including source mismatch detection and correct motor/VRU/warning grouping. Local full 30-signal JSON SHA256 32082768e667522f5b191dbc76fd0b92604844c4001dd30186b387ea54c85b10; test log SHA256 c40575e73f33b0b8db8267f9390e127a41d406b29e5755ef3b05f11a016d6fa9. [Structured result](P23_OFFICIAL_DLR_SIGNAL_CODEBOOK_RESULTS_20261122.json).

This upgrades P20–P21's historical codebook status without rewriting those earlier dated records. **OPEN:** physical signal-head ID → movement/stopline relationship; independently estimated vehicle crossing timestamps; real-world queue/blocked-pocket claim; legal phase/amber/VRU crossing safety; independent SUMO execution; actual RF CSI and decision-value measurement.

Next: use the original OpenDRIVE map, printed Figure 1 directional assignment and original one-second movement volume columns to verify a single selected lane's controlling head before comparing its discharge to T2/SUMO. No unauthorized traffic-signal intervention, GitHub bot, or opening K047/CIM.


## P24 exact-source reproducibility correction (2026-11-22, supersedes earlier SHA claim)

Original P23 document described publisher PDF SHA256 `3c733b677ee63fd2cb282946f415f649d23954ac420d5bc37e0af545f7293849`. But the actual official 2,383,435-byte PDF fetched again from connected Drive has SHA256 `94fd9ebd32d04a9c35b02be526fbd11a8d5a613933d7961fde800386853b34f3`. A replay of the original preserved P23 ZIP on this exact real PDF gives **4 PASS and 1 error due to byte-lock mismatch**, not 5/5. Source expected SHA was corrected on `main` (blob `f2363324a7a3c8aa2017901d9d2da1d9f4f5c1c1`) and **all 5 exact-source tests now PASS**. The corrected P23 results JSON and full [P24 erratum](P24_DLR_MAP_JOIN_AND_P23_CORRECTION_FINDINGS_20261122.md) record both failed and corrected replay. Historical P23 ZIP is unchanged, so its originally claimed full byte-acceptance should be treated as superseded. The *semantic Table4 state mapping* survives manual source inspection but is distinct from source-byte reproducibility.
