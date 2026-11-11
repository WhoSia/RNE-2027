# D46 — 2026-11-11 FIFO node-supply boundary gate

## Scientific status
**Synthetic node conservation/supply acceptance: PASS (25/25 local tests).**
**Field-identified arrivals / downstream capacity / policy comparison: HOLD.**

Tampère et al. (2011) is a reference for physical node acceptance constraints, **not** a claim the full paper's SCIR, priority, invariance and traffic signal model were replicated.

An independent minimal fluid node uses incoming demands `D_i`, outgoing supplies `S_j`, fixed turn fractions `beta_ij` and strict incoming-link FIFO:
```text
max     Σ_i f_i
s.t.    0 <= f_i <= D_i
        Σ_i beta_ij*f_i <= S_j   (each exit j)
        f_ij = beta_ij*f_i
        Σ_j beta_ij = 1
```
Implemented using scipy HiGHS LP. No signal conflicts, time-varying finite buffer `K`, signal decision, queue-tail propagation or micro-vehicle motion is represented. Degenerate optima need explicit priority/fairness rules before model acceptance.

## Synthetic counterexample
One shared input link with D=10 split 50/50 into exits of receiving supplies (8,0): strict link FIFO gives throughput 0. A **different physical structure**, two separate inputs with D=(10,10) individually dedicated to the two exits, supplies (8,0), gives throughput 8. These two values are not comparable estimates of a signal policy improvement. At second exit supplies 0/0.5/2/5/10, shared FIFO throughput = 0/1/4/10/10 vs separately routed approaches = 8/8.5/10/13/18.

## Actual 45-minute DLR publisher counts
Original three 900-second traffic-volume CSVs (2023-09-24 12:00–12:45 UTC) have 32/27/28 active movement columns. Aggregated published movement-crossing **outflow**: East 372, South 397, West 378, North 262, total 1409. Not independent queue arrivals. This is D42's same-sensor-lineage observed count, not exogenous traffic demand `D`, outlet receiving supply `S`, or ground truth for vehicle trajectories.

## Test and executable sources
25/25 Python unit tests executed locally (20 node and cumulative-accounting contracts; 5 actual-volume-reader boundary contracts). All locally executed code, tests, actual 45-min file provenance SHA256, synthetic grid, JSON output and full research note in **byte-sealed ZIP**:
https://drive.google.com/file/d/1X4ofXd6CKhYi5U1heXpbCQjXwvrFVs44/view

ZIP SHA256 `de09ba7bd978a4328936a874b4d72c1549665df2ef194d7bb14e0d4e3c02709d`.
The original DLR CSVs are not duplicated in the ZIP. Exact execution and test output are in the ZIP; the GitHub commit of this note does not yet constitute a line-for-line source mirror.

Dated reasoning Google Doc:
https://docs.google.com/document/d/1ZZPfPZXyHazuLiSqOowHQfSRecseZtzSY1gn1EEOhqc/edit

## Next gates
1. Recover lane-specific finite stoplines and track-to-turn mapping with UNKNOWN/censored tracks.
2. Get **actual entrance arrivals** and **exit receiving capacity**, not observed crossing counts substituted as both.
3. Build a physically admissible D44 motion successor, then supply/blocking dynamics.
4. Independent actual SUMO run with matched demand, geometry and signals.
5. Only then quantify observability-induced signal-policy ranking reversals.

Provenance: original node theory in **Tampère et al. (2011)**, TRB 45(1) 289–309, DOI 10.1016/j.trb.2010.06.004, already canonical Drive file `1yEbxz7-us7MkMYmxULtItrwCgUy6Ojo_`.
