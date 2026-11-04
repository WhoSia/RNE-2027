# P7b: Common-cycle impossibility in practical experiment windows

Bologna-Pasubio source plan periods in seconds: [90,123,90,125,96,90,111,63].
Exact least common multiple: 382,284,000 s = 4,424.583333 days (~12.12 365-day years).
Source: GitHub DLR-TS/sumo-scenarios bologna/pasubio/pasubio_tls.add.xml, blob e58995742a551256ec2aa205788027593814a2b3.

A single practical observation interval cannot end at full multiples of every controller's fixed cycle. This is arithmetic only and does not mean the published scenario needs a 12-year simulation.

Instead, preregister paired common demand streams, choose multiple finite horizons, vary initial phases over held-out strata, retain incomplete-vehicle counts, and measure sensitivity of signal plan policy ranking. Random-phase averaging is unbiased for pure stationary green-permission time, not necessarily for queue or delay due to nonlinear interactions.

Original raw data not downloaded, SUMO executable unavailable, no vehicle performance validation claimed.
