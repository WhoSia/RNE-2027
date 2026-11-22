# P37 — Same-ID nighttime connector and receiver check

Use all five east crossings from the frozen P34 ledger, including any without downstream detections. Keep the daytime holdout sealed. Check the publisher trajectory CSV and OpenDRIVE against the P34 SHA-256 values before analysis.

Reuse the daytime quarter-meter masks and direct vehicle observations. For straight candidates require the five ordered connector bands followed by west receiver entry. For left candidates require a hit on connector 300015 followed by the south receiver. Remove cells shared across competing routes before scoring. Start strictly after the crossing bracket and test 10, 20, and 40 seconds. Report alternative route hits and retain incomplete observations in the denominator.
