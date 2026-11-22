# T2 P34 — Official stopline-bin co-occurrence baseline and timing-shift adversary

**2026-11-23 KST — preliminary raw-file inspection occurred BEFORE this protocol was committed. This is exploratory with transparent outcome-informed pilot, not preregistered confirmation.**

## Core question
Does naive tracked-object activity in the official DLR 1-second volume-bin interval identify actual published movement-specific stopline crossing bins, and what remains unidentified? P33 found a one-sample shared signal gap, but never proved a signal head-to-movement relation. This study adds a **third independent original DLR stream**, publisher `traffic-volume`, to field-side checks instead of extending synthetic simulator duration.

Exact raw inputs SHA256:
- `traffic-volume_230924-233000_230924-234500.csv`: `00f6f29b2be6c2fa517077de3b7accbbfc75edddc92332534f00ad6b62312798` (893 1Hz rows, 12 directed movement columns).
- `trajectories_230924-233000_230924-234500.csv`: `6ba8920caa839dc20e2fd7f2fe2dedd553aeb4c27e4be3ea453054de0b09af50` (8,624 rows, 37 tracked IDs).
- `traffic-lights_230924-233000_230924-234500.csv`: `95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c` (26,970 rows, 30 heads).

Freeze labels as **positive 1-second bins**, not unique vehicles; for each official timestamp t, positive iff any of 12 published movement indicators is 1; binary activity proxy iff any observed trajectory `timestamp` is in `[t,t+1s)` using UTC floor. Compute TP/FP/FN/TN over all 893 aligned bins, zero divisions safe, precision/recall/specificity, distribution of candidate tracked IDs in positive bins, number of movement indicators per bin, and timestamp coverage. No posthoc threshold selection.

**Explicit exploratory baseline timing adversaries:** shift the sample time bin associated with each tracked trajectory by `-2,-1,0,+1,+2` seconds relative to the official bin axis, with no tuning. These are *diagnostics of the alignment convention*, not randomization tests, not independent replications. Report complete confusion counts and emphasize any accidental changes in apparent precision.

**Negative control on event identity:** Within each positive bin, report candidate count as an *upper-bound candidate set* of tracked IDs. Do not claim any candidate is the actual crossing vehicle. No attempt to use unsupported ID-equality between signal, track and movement label. Count samples inside the known P33 common signal observation gap separately, but do NOT claim missing volume crossings (the official bin indicators are all zero during gap seconds). Do not impute signal states.

**Source/engine:** Python stdlib CSV is selected for simple exact time alignment; preserve existing Go P33 as an independent raw input time-quality gate. Adding a third runtime would not solve the lane geometry/movement association problem. The stage delivers one scientific discriminator rather than language count. Provide runnable CLI, exact SHA hard gate, malformed timestamp/duplicate bin/unknown indicator tests, and 1Hz bin fixture; deterministic output and reexecution.

## Falsification and authority
- If binary activity underperforms, claim only poor *naive baseline* discrimination, not insufficient information in actual geometry-aware tracking.
- If every published crossing has active tracks, temporal co-occurrence **does not** demonstrate matched identities or verify publisher stopline geometry.
- Since volumes may derive from same underlying tracking dataset, do not call them independent ground truth sensor modalities without publisher provenance confirmation. They are two different exports with possible **shared-source dependency**.
- Scientific next gate: obtain/pin the official movement line coordinates, then reconstruct path intersection of each ID trajectory with crossing line and evaluate official movement-bin agreement and source-dependent cases. Do not create fabricated stoplines.
- A gap with no positive official volume event cannot prove absence of true crossings.
- No SUMO execution, real intersection interventions, or signal law claims.
- RAVEL compressed: observer-first, source-dependence skeptic, external-discriminator test. **Return edge:** replace activity proxy by geometry-grounded stopline crossing or hold observational model validation; do not append another uninformative metadata stage.
