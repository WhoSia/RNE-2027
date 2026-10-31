# T2 v2.2 — World Contact: one-step vehicle motion and exact access-denial genealogy

Date: 2026-10-31. Project branch: research/t2-spatial-fig2-v02.
Scope: synthetic simulation **physics audit**, not empirically validated traffic dynamics.

## Research priority
World contact requires that an internal event correspond to a measurable
physical event. The existing v2.1 local model claimed "only one cell per
vehicle per second; lateral changes do not also move forward." Its
forward movement loop happened before lateral-change loop, which could
change the lane of an already-advanced vehicle during the same update.

## v2.2 correction and observables
- Track vehicle IDs moved longitudinally within each time step; prohibit
  those IDs from also switching lanes in that same step.
- Movement from fork to pocket is a separate movement step.
- If the pocket entrance is already occupied, emit an **exact internal
  access-denial event** with `vehicle_id`, `blocker_id`, second and
  reason. This event arises within the programmed service rule.
- Record successful pocket-entry events.
- Record both `receiver_denied_attempts` (per attempted movement) and
  `receiver_denied_seconds` (distinct simulation ticks with >=1 denial).
  Preserve legacy `receiver_full_denied_s` as a **misnamed attempts
  alias** for backward compatibility.

These are internal model state transitions. They are **not observations
of a real vehicle failing a pocket entry**; frame co-occupancy remains
a different and weaker observational signature.

## Verified archived-v2.1 vs local-v2.2 experiment
48 paired parameter conditions x 2 executable source versions = **96
synthetic 720-second runs**. Each condition used identical demand seeds
and conditions: 8 seeds x bay length 14/28/70m x lane changes on/off,
1,800 veh/h nominal approach demand, 50% left turns, 4-cell downstream
shared receiving link and through-B allocation 0.

A physical-displacement violation was recorded for the same continuing
vehicle if the sum of longitudinal cell movement and lateral lane-change
indicator exceeded 1 between end-step frames:
- Archived v2.1: **888 violation occurrences** over 48 runs.
- Fixed local v2.2: **0 violation occurrences** over 48 runs.
- Network exit totals differ in **7/48 paired scenarios**.
- Of 24 lane-change-disabled pairs, **0** changed throughput.
- Of 24 lane-change-enabled pairs, **7** changed throughput.
- Mean revised-minus-original exits over the 24 lane-change-enabled
  conditions: **+0.333 vehicles in 720 s**.

888 is a number of **model motion-invariant failures**, not unique
vehicles or traffic accidents. A corrected discrete motion invariant
does not by itself validate acceleration, gap acceptance, queue waves,
or real-world lane-change decisions.

## Tests and implementation gate
**23/23 selected local Python tests pass** on the patched local source:
18 tests retained from archived v2.1 plus 5 new v2.2 invariant and event
lineage tests. The local new test checks exact pocket denial event count
equals the existing simulation fork-refusal count, and receiver refusal
attempts/seconds reconcile with vehicle-specific service events.

Corresponding GitHub branch source change:
`79f6fcba30c33682b5cb5c57d12ef0ebfa6d6be1`.
New regression test commit:
`ffd9e15f2909486cc41a87de8b12fa1f523e5633`.
The GitHub remote source uses a different historical code dialect
from the locally executed source, and **exact remote HEAD checkout
execution remains unverified**. Do not overstate code parity or full
historical-suite coverage.

## Reproducibility and cross-version impact
The executed baseline+fixed source files, paired raw data,
paired differences, 23-test log, patch and SHA256 manifest are in
`T2_v22_world_contact_physics_repro.zip`: 11 members, local CRC PASS,
SHA256 `131ed0e08f0a75519aae9c33457babc23a97919a6ca09a9a79f2a9865f5f5b3b`.

Older lane-change-enabled findings must be treated as contingent until
recomputed. Scenarios with lane changes off in this comparative grid
are invariant under the repair.

## Shared Drive archive hygiene
Prior outputs were NOT all present in Drive. In this turn the
project-shared-drive folder `01_ACTIVE_T2/02_REPRO_ARTIFACTS — T2 Chat
Outputs (2026-10-31)` was created at
https://drive.google.com/drive/folders/1dOUedBcOxb5HPQoJWLdur_6jFF2ni5rV.
13 historical reproducibility ZIPs (v0.8-v2.1 and related), plus a
separate ZIP of 60 accessible loose generated assets, and a JSON
SHA256 inventory were uploaded through Google Drive. The folder
inventory was read back to verify 15 file names at that point.
The latest v2.2 files are separately deposited afterwards.
Canonical paper PDFs remain in the Research OS 10_PAPERS shelf.

## Remaining world-contact requirements
- Identify the exact physical geometry and shared/independent
  receiving lanes with street plans or approved observations.
- Quantify observed blocked-entrance *cycles* in an independently
  annotated, legally obtained field record, not only co-occupancy.
- Measure actual initial queue, back-of-queue position and signal
  phase by movement before calibration.
- Evaluate multiple observed outcomes on a held-out period,
  separating bias from sampling aliasing.
- Acknowledge unmodeled heterogeneity in vehicle length, response
  time and lane-change decisions.

No GitHub Actions/workflow changes and no main merge.
