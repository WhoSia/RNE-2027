# P11-S / D17 — Lane-queue independence counterexample
**2026-11-05.** P12 signal-policy search FROZEN. Source-of-truth full local-test package: Drive [T2 P11-S/D17 ZIP](https://drive.google.com/file/d/1XGPfBXIvw2fBM88V3dHQ0U6hgZwFiA3w/view) SHA256 `80f984ff257c7bde93974c345b8a78cfa44ddf27c6df63c55f9775ce72169b78`.

## What is genuinely reproduced?
Prior P11-R global FIFO blocks the entry of a vehicle into an independent road resource when an earlier waiting vehicle requests another, occupied resource. New source `src/lane_fifo.py` (in Drive ZIP) maintains independent FIFOs for each lane while preserving atomic resource acquisition, capacities, movement-kind conflicts, deterministic time-ordered exit/entry, and conservation.

Minimal synthetic request times: A occupier 0s until 10s; second A request .1s; independent B request .2s. Prior P11-R global pending queue starts B at 10s; per-lane FIFO starts B at .2s. Difference **9.8s** due solely to algorithm design. Parameter sweep 4 occupier durations × 3 B demand sizes = 12 cases. At 20s occupancy and 7 B requests, global FIFO induces 138.6 vehicle·seconds of aggregate extra wait on B.

## Verification
Local Python: 8/8 new tests + 8/8 old P11-R tests passed; random tests 20 × 120 = 2400 synthetic vehicle requests; checked time monotonicity, capacity and exits/entries. Baseline exact local version copied into ZIP. `experiment.py`, scenario records and SHA256 per-file manifest included. This is NOT P10 untouched original replay, NOT an inD/Jinju validation and NOT SUMO run.

## Critical validity boundaries
- Unlimited *upstream* waiting storage, thus **not a genuine finite link spillback model**.
- Fixed occupation durations, not actual IDM or car-following; no speed, real longitudinal position or lane changes.
- The new per-lane queue still has within-lane head-of-line blocking where overtaking may be physically possible; 0s wait on B is a synthetic independent-link consequence, not prediction of field traffic.
- No numerical error certificate; float event timestamps subject to roundoff and near-equality corner cases.
- No calibrated vehicle demand or signal phases. P12 optimizers and control policy experiments remain untouched.
- SUMO already has `--meso-lane-queue` and mesoscopic LTM, so changing global FIFO to lane FIFO is **NOT a novelty claim**. https://sumo.dlr.de/docs/Simulation/Meso.html

## Decision
Exhibition: keep narrowly testable question about finite turn-pocket storage and intersection queues, using matched real observations and SUMO. Journal: causal event semantics and finite capacity with precise assumptions, formal counterexamples and numerical convergence. Next D18 add upstream finite length, physically grounded gap propagation; restore actual legacy P10 proof-of-failure and obtain raw Jinju CSV with integrity and observational unit check.
