# T2 20261106 · five-unit research ledger

**D26 original archival P10 replay: GO (narrow).** Archived ZIP receipts verified, untouched P2 Python code loaded and 8/8 original tests pass, 8 dt traces and selected gate ablation regenerated, 3 archival outputs byte-identical.

**D27 micro motion and finite storage: GO for toy reference / HOLD for empirical fidelity.** Position/speed/accel, footprint, lane-order and signal gate tests pass. No real IDM/observed acceleration calibration; 1-s step only.

**D28 junction/road interactions: GO for limited demo / HOLD for full complex road network.** Lane change, merges, bus dwell, pedestrian block, grade/curve, OD and interconnected links in synthetic model. No OpenDRIVE polygon/roundabout yield calibration.

**D29 reproduction: GO for strict interface / HOLD for true independent data.** GTFS fixture from earlier D25, SUMO tripinfo parser, field queue schema strict. SUMO binary, NGSIM/inD trajectories and observed road queue not available in the runtime.

**D30 policy: reopened as OFFLINE exploratory only.** Three fixed two-approach candidates evaluated across separate development and holdout synthetic seeds. No traffic-control recommendation, optimization convergence, field validation or safety proof.

The user requested all 10 missing factors completed in one response. A scientifically valid claim of full implementation would require continuous trajectories, validated lane changes, detailed geometric movement, real road priority, actual transit/field data, SUMO parity and strong evaluation. The delivered work spans all ten topics to varying degrees but **does not fulfill those external/physical gates**. Do not conflate code coverage with empirical completeness.

For all code: WhoSia commits manual only; no GitHub-Actions bot. Store bytes and visualizations under `20261106 김우준의 사유`, and record semantic truth in native Google Docs.
