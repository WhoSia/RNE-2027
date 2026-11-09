# D42 follow-up — publisher signal codebook and empirical head patterns, 2026-11-09

## Primary documentary evidence
Official DLR UT v1.3.1 documentation, **section 4.2.3 Table 4 (PDF page 14)**:
https://drive.google.com/file/d/1gUqUJEAGtXw06RjQCLbBoJ0k-pcee5Uq/view

Codes 0=unavailable; 1=off; 2=stop required before proceeding; 3=red; 4=red+yellow; 5=green; 6=green protected movement; 7=yellow; 8=yellow protected movement; 9=flashing yellow.

The same PDF **section 5.1** specifies that traffic volume is derived when a tracked object **center crosses the stopline** and that only detected movement columns are present. It warns in **section 6.2.1** of trajectory fragmentation, merges and cross-object ID switching. Official source codebook was read and PDF page visually checked; this supersedes the earlier explicitly provisional "enum not yet known" status, not the source CSV hashes.

## Observed state code occurrences (12:00–12:15 UTC)
0:0, 1:613, 2:0, 3:21,114, 4:133, 5:4,408, 6:0, 7:358, 8:0, 9:284. Total 26,910 rows.

Heads 1–13 have red/yellow phases and green. Heads 14–29 in this sample have only red/green observations. **Head 30 is atypical: OFF=613, FLASHING_YELLOW=284, never red/green in this sample.** Do not automatically label it a normal signal controlling one of the 32 volume movements.

Across 897 simultaneously observed 30-head timestamps, 60 distinct observed sets of heads in raw green state (code 5) were counted. These are **sample-level combinations**, not necessarily 60 controller phases, due to transitions and sample timing.

893 endpoint state changes seen across consecutive samples, 9 of which span gaps of ~2s and are interval censored. No finite list of observed state changes guarantees exact physical switch timing between 1Hz samples, even in the ordinary intervals.

## Next stronger empirical gate
Use official Table 3 UTM32U head coordinates plus the OpenDRIVE lane geometry and oriented stopline segments to establish each signal-to-movement mapping before any green-compliance count. Treat OFF/FLASHING_YELLOW separately. Reconstruct center-crossing event time as a closed interval between 20Hz observations, and preserve uncertainty at unsampled phase boundaries. Count 436 official metadata events as a comparison *target* only after movement mapping; never assume 636 track IDs correspond to 436 crossing events. External SUMO execution still not confirmed.

Raw triad QA release and checksum manifest:
https://drive.google.com/file/d/1IizRbVxb-M7RU3qP7twfY1qF0GnoLynA/view
