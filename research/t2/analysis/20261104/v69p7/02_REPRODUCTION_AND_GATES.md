# P7 Independent Replay Gates

Derived source and tests: Drive T2_P7_Signal_Phase_Opportunity_Audit_20261104.zip.
ZIP SHA256 bec87deb1e1ef83fbf577f34624e53a67e30553aeb84037e44df4ad5d5e73852.
Standalone signal-window module tests 13/13 passed. Unmodified source P2 original regression tests 28/28 also passed in the current environment.

Next:
1. Obtain byte-exact SUMO scenario files incl network, signal, detector, complete routes; verify provenance/hash/license.
2. Run actual SUMO baseline and capture tripinfo, detector output, configuration, version, seeds; no field truth claim.
3. Crosswalk T2 links and movements to SUMO; compare fixed policies under identical routes, horizons, phase offsets.
4. Test OOD demand and models against measured data (NGSIM, Utah SPaT and/or Jinju) with source-date separation.
5. Retain unresolved P3/P5 stop-line viability and finite-horizon censoring as promotion blockers.

Keep upstream originals immutable. GitHub-Actions[bot] must never be used as contributor; manual commits only.
