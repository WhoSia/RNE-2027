# T2 v0.6 — Observability Court: inference ≠ traffic mechanism
Date: 2026-10-31. Status: CODE COMMITTED / WITNESS SEARCH NOT YET EXECUTED.
Research branch: research/t2-spatial-fig2-v02.

## External studies and distinct estimands
1. Reynolds, Rouphail & Zhou (2011) — *Turn Pocket Blockage and Spillback Models: Applications for Signal Timing and Capacity Analysis*. TRR 2259:112–122, DOI 10.3141/2259-10. Estimand: sustainable service rate after queue interactions.
2. Yang et al. (2022) — *Characterizing the dynamics and uncertainty of queues at signalized intersections with left-turn bay*. Physica A 599:127439, DOI 10.1016/j.physa.2022.127439. Estimand: signal-state-dependent queue distributions.
3. Qi, Dai, Tang & Hu (2020) — *Quasi-real time estimation of turning movement spillover events based on partial connected vehicle data*. TRC 120:102824, DOI 10.1016/j.trc.2020.102824. Estimand: triggering movement and spillover duration from partial trajectories.
4. Wu, Yao, Cao & Tang (2024) — *Left-turn queue spillback identification based on single-section license plate recognition data*. Transportmetrica B 12:2363273, DOI 10.1080/21680566.2024.2363273. Estimand: spillback type under single-section LPR/queue-inference information.

Their publication abstracts/academic records have been checked. The newly
uploaded four PDF files were **not found in the 00_INTAKE Drive listing or
global title/DOI search as of this inspection**. Thus no pdf was renamed,
moved, SHA-sealed, or page-read this session. Full-paper harvest pending
confirmed source file IDs; do NOT equate this abstract-level synthesis
with a full-paper reading.

## Exact mathematical question
Let H be a fully specified hidden traffic trajectory, E(H) an internal
mechanism event sequence, and O(H) a partial detector observation.
The event class is identifiable from O on an admissible history set
\\mathcal H only if

  for all H1,H2 in H: O(H1)=O(H2) => E(H1)=E(H2).

A witness to failure requires **both** histories to be realizable
under the same named simulator/config and input restrictions, plus a
common observation and distinct mechanism labels. Merely writing down
two arbitrary signatures with identical count vectors does NOT prove
these are realizable, and the tests explicitly guard this distinction.

## Implemented enumerator
`observability_court_v06.py` enumerates every C(n,l) permutation of
left/straight route letters at identical arrival timestamps, same
route totals, same protected phase, same fork and virtual K. Its
observation consists only of aggregate arrivals and movement-specific
stopline exit totals; hidden signature records capacity blockage and
both gap-blockage counters. It returns WITNESS_FOUND with two explicit
sequences if distinct signatures project to identical observation,
or NO_WITNESS_IN_ENUMERATED_DOMAIN otherwise. This is a **finite
computational search**, not a result and not a universal theorem.

```bash
python -m unittest discover -s research/t2 -p 'test_observability_court_v06.py' -v
python research/t2/observability_court_v06.py
```

Test cases are committed but **not yet run**; do not upgrade the
witness to verified status until the exact output and SHA are checked.
The named signatures are internal v0.5 counters and not automatically
equivalent to the ten categories used in Wu et al.

## Further scientific gates
- Replace coarse aggregate counts with per-cycle movement counts,
  then a single section’s movement-specific time stamps, then partial
  trajectories. Determine which observation addition distinguishes
  previously equivalent histories.
- Report an explicit 'unidentifiable' class for collisions of O,
  rather than assigning the most plausible mechanism as ground truth.
- Use two independent models (e.g., macroscopic CTM and SUMO), but
  distinguish model disagreement from measurement nonidentifiability.
- Determine whether the observation distinguishes fork blockage
  from bay saturation vs. upstream demand/insertion delay under
  identical stopping-time definitions.
- Avoid using real identifiable license plate data; synthetic,
  anonymized, or aggregated measurements suffice for a first study.

## Research judgment
The strongest possible result from this sequence is not a new
spillback classifier. It is a **demonstrated bound on what a chosen
sensor/observation process can logically infer**, with minimal
indistinguishable traffic histories and explicit conditions under
which added sensing breaks the equivalence. A theorem at the
observation-map level and measured relevance at an actual intersection
are separate proof obligations.
