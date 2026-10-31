# T2 v1.9 — Intake Literature Audit, Two-Movement Receiving Supply and Initial Queue

Date: 2026-10-31. Branch: research/t2-spatial-fig2-v02.
Policy: no GitHub Actions, no workflow edit, no main merge.

## 00_INTAKE complete name audit
The connected Drive folder 00_INTAKE — Literature Radar (ID
1MLtYh0pv8QUZDReYzRqjDrOjRkSJAD16) contained 28 files at the time of
enumeration. Three PDF objects with opaque short file names proved relevant:
- wei2016.pdf: Dali Wei, Wesley Kumfer, Dayong Wu & Hongchao Liu (2016),
  *Traffic queuing at unsignalized crosswalks with probabilistic priority*,
  Transportation Letters, DOI 10.1080/19427867.2016.1236069.
  Relevance is yielding/queue theory, NOT direct left-turn field evidence.
- jun-qiang2012.pdf: Leng Jun-qiang et al. (2012),
  *Travel Time Model of Left-Turning Vehicles at Signalized Intersection*,
  Mathematical Problems in Engineering 2012, 473847,
  DOI 10.1155/2012/473847. Investigates opposing headway M3 distributions.
- yang2018.pdf: Yang, Shi, Yu & Zhou (2018),
  *Analytical evaluation of the use of left-turn phasing for single
  left-turn lane only*, Transportation Research B 111, 266–303,
  DOI 10.1016/j.trb.2018.03.013.
  Models protected/permitted/mixed left-turn server vacations.

All three PDF bodies were fetched, title/author/DOI cross-checked,
then metadata-renamed and moved to the canonical 10_PAPERS folder
1D2M4LHcejREhlyp6vTd71xxLLx-6ldUP, preserving Drive IDs.
Some remaining opaque PDF source(s) have no available extracted text;
they remain on identification hold. No blanket claim of full binary
page inspection is made.

## Additional literature (not confirmed as owned)
Tageldin, Sayed & Ismail (2018), *Evaluating the safety and operational
impacts of left-turn bay extension at signalized intersections using
automated video analysis*, Accident Analysis & Prevention 120:13–27,
DOI 10.1016/j.aap.2018.07.029.
Before/after with matched controls, identifies blocked entrance cycles
and travel times as field-observable measures. Do not equate conflict
reduction with measured crash reduction.

Furth & Tabatabaei (2026), *Short Right-Turn Lanes and Auxiliary Through
Lanes: Intersection Capacity, Signal Timing, and Negative Lost Time*,
DOI 10.1177/03611981261424234 (publisher open access).
Relevant as a closely related but deliberately different short-lane
geometry; authors distinguish additional left-turn phase complexity.

## v1.9 independent receiving-group mechanism court
Standalone link_supply_v19.py (not the full physical pocket simulator):
2 movement-specific upstream queues, finite receiving inventories,
separate S/L phase and service headways, explicit initial queues,
2 receiver structures (shared vs independent), 3 admission priorities
(through-first, left-first, alternating). Conservation is asserted every
tick. Shared models use a common finite storage inventory with a
deterministic admission tie-break; this is not microscopic gap acceptance.

384 simple scenario runs: shared 2 × initial L queue 3 × L-offset 4 ×
L green durations 2 × paired seeds 8.
576 priority scenario runs: shared 2 × priority 3 × capacity 2 ×
initial L queue 3 × L green 2 × paired seeds 8.
**960 simulations total**. 10 local unit tests passed. No field calibration.

For a single-slot shared receiver, initial L queue=20, green L=20/60s,
green S=45/60s, horizon 360s (eight paired seeds):
- physically independent S and L receiving: (S 90,L 42) completed
  under all three admission-order rules;
- shared with S-first: (90,0);
- shared with L-first: (0,42);
- shared with alternating: (27,38).
Result is a **structural counterexample**: same demand and service
budgets, dramatically different outcomes due solely to shared storage
and tie-breaking. It is NOT measured impact or policy optimization.
Admitting to shared supply with S-first can starve L, and L-first
can starve S; simulated events depend on discrete update order.
A different access geometry would invalidate the shared-buffer setup.

## Reproducibility and historical defect
During remote branch source review we found an incorrectly-indented,
left-turn service-event logging statement inside the straight branch
of dual_lane_v11.py. Fixed on remote research branch in commit
eab9f9d6d8ec5c62db1fd0373aac2310d074369d.
A full exact-source legacy suite has NOT been run against this updated
remote file yet; prior local historical PASS counts cannot certify it.

For the newly built standalone engine, exact remote Git blob SHA
**e00cbb28e1017eea912745d049d69a372ab1d991** was equal to
git hash-object of the locally executed link_supply_v19.py.
The 576-run priority_sweep_v19.py also had exact remote/local blob
parity: **1a97aa57b9c475dc589aa9a4eea32415156d35c2**.
Other files do not carry the same parity claim.

Local reproducibility package:
T2_v19_supply_and_literature_bundle.zip, 15 members; ZIP CRC PASS;
SHA256 90dac3734927991b357a6261fef9fc4c712dc8e93685ab746c5c9da3bdc67276.
Contains source, unit tests, 960 raw scenario rows, summary JSON,
one plot, logs, README, per-file SHA256 manifest.
