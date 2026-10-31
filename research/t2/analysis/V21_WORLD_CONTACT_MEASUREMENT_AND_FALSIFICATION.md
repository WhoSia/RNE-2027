# T2 v2.1 — World Contact, Observables, and Falsification Gates
Date: 2026-10-31. Scope: synthetic model verification, **not field validation**.

## Question
Can a queue simulation be wrong about physical blocked-pocket entrance
even when its total exit counts and vehicle-conservation tests pass?
Yes: stopline discharge, blocked-entry cycle, bay-full frame,
and downstream-refused *attempt* are four different observables.

## Direct public evidence
FHWA Traffic Signal Timing Manual chapter 3:
https://ops.fhwa.dot.gov/publications/fhwahop08024/chapter3.htm
Queue length is physical storage; back-of-queue can grow during green.
Chapter 6:
https://ops.fhwa.dot.gov/publications/fhwahop08024/chapter6.htm
Left-turn bay overflow AND through-queue blockage of bay access
are separate mechanisms. A blocked bay may cause detector-driven
premature gap-out.
Chapter 7:
https://ops.fhwa.dot.gov/publications/fhwahop08024/chapter7.htm
In oversaturation, observed stopline counts are departures, not
necessarily the total incoming demand.
Tageldin, Sayed & Ismail 2018 DOI 10.1016/j.aap.2018.07.029:
3 treated approaches and 3 matched controls; blocked-entry signal
cycles and travel time are relevant field targets. Reported 63.2%
was a traffic-conflict surrogate effect, not an accident-count effect.

## Executed v2.1 local study
Core from preserved v1.6 local trace. Its original configuration uses
7m cells, one vehicle/cell, 1-second updates, 120s signal cycle,
protected separated phases and a **shared** physical downstream receiver.
Default lane changing disabled. No field recordings were used.

8 paired seeds × 3 pocket lengths (14/28/70m) × 3 downstream offsets
(0/20/40s) × 2 downstream greens (15/30s) =
**144 independently simulated scenarios**, each 720s.
End-of-step frame records were sampled systematically every
1/2/5/10/15s for **720 observational reductions**, not 720
independent traffic simulations. Nine new local unit tests PASS.

Observable proxy for 'blocked entrance': after-step bay first cell
occupied + a left car at the immediately upstream lane cell. This
simultaneous occupancy **does not prove a denied access attempt**.
Actual downstream receiving refusals were taken from separately logged
pre-movement service events with vehicle IDs, not inferred from frames.
The diagnostic reconciles exact event counts with core counters
and S/L crossings with stopline departure counters.

Mean number of 120s cycles containing proxy (maximum six):
1s 5.3403; 2s 5.1736; 5s 4.9583;
10s 4.8403; 15s 4.8611.
Scenario fraction with >=1 missed flagged cycle relative to 1s:
1s 0%; 2s 13.19%; 5s 27.08%;
10s 30.56%; 15s 30.56%.
The sampling grid was anchored at t=0. Phase/random-offset sampling
remains a follow-up sensitivity test. A high snapshot sampling rate
is NOT ground truth for actual obstruction or human-visible video.

## World-contact acceptance gates
P: certified geometry (pocket usable length/taper, actual route-lane
access and whether S/L downstream receiving space is shared).
O: independent legally acquired, anonymized cycle annotations:
entrance blocked, bay overflow, queue tail position, actual signal phase,
separate S/L stopline departures. UNKNOWN is not zero.
C: small training calibration versus held-out time/date validation,
including per-cycle prediction errors and an independent observable.
H: initial residual queue, generated versus discharged demand, final
unserved queue and horizon sensitivity.
F: reject a throughput-matched model if it systematically predicts no
blocked entrance cycles where annotated video repeatedly shows them.

This is an **identifiability gate**, not a post-hoc software score.
Even perfect counter reconciliation cannot certify field geometry.
No covert data collection, personally identifying footage, or roadside
field work is necessary or proposed.

## Artifact receipt
Local executed bundle: T2_v21_world_contact_repro.zip,
15 members, 144 simulations/720 sampling reductions,
raw CSV, JSON, trace extractor, 9 tests, schema, protocol and chart.
SHA256 caad9f365182da801aa9d7a31c5f53ff9e9e28c5012a060fbbbbf955522530e9.
Archive ZIP CRC check PASS. The GitHub record is a source-of-truth
narrative; local code and remote GitHub execution are not byte-parity
certified in this version.
No GitHub Actions, no workflows, no main merge.

## New identifiability counterexample from the executed sweep
Two simulated scenarios finish **exactly 59 vehicles** in 720s but
have radically different proxy-blocked bay entrance signatures:
- seed 0, pocket 70m, offset 40s, downstream green 15s:
  proxy seen in **1/6** cycles.
- seed 6, pocket 14m, offset 40s, downstream green 15s:
  proxy seen in **6/6** cycles.
The arrival stream AND geometry differ. This is not a causal matched
intervention; it is a non-identifiability demonstration that aggregate
throughput alone does not determine blocked-entrance prevalence.
Therefore fit/validate not just exits but independently annotated
blocked-entrance cycles and queue-tail measurements. Appendix
IDENTIFIABILITY_V21.md is included in the final ZIP.
