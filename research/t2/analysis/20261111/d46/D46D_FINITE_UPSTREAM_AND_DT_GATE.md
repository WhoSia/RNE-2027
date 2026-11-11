# D46-D — finite upstream supply spillback and numerical-delay interaction

**2026-11-11 | SYNTHETIC ACCOUNTING PASS / FIELD AND POLICY HOLD**

## Model with strict causal synchronization
Define outside backlog B, first-link occupancy U, second-link occupancy N, cumulative external demand C_d and cumulative sink outflow C_o. Each discrete tick uses only **start-of-tick** inventory and free spaces:

```
admitted   = min(B, gate_cap, K_u-U)
transferred= min(U, transfer_cap, K_d-N)
discharged = min(N, exit_cap)
B' = B + new_demand - admitted
U' = U + admitted - transferred
N' = N + transferred - discharged
C_d - C_o == B + U + N
```

B is outside **unbounded queue**, not deleted demand. U and N have finite storage K_u and K_d (vehicles). This is a synchronous two-link *fluid* model; no actual geometry, lane, integer cars, signal heads, wave speed or DLR field calibration.

## Frozen A/B synthetic case
40 ticks, 75 total input demand (3/tick for first25), gate/transfer potential 4/tick, K_u=8, K_d=6.

- Free downstream (exit cap 4 throughout): 75 entered, 75 exited, final stocks (B,U,N)=(0,0,0).
- Downstream restriction exit cap [0]×10, [1]×20, [4]×10: 58 entered, 50 exited; ending (B,U,N)=(17,4,4), so **75-50=17+4+4**. First downstream full at step index3, upstream full index5, accumulated waiting beyond new arrivals index5.

## Capacity × discrete-time interaction is substantial
Holding dt=1 and same input/outlet schedule, vary K_u=3/6/8/12/24/48/96. Total outflow=38/50/50/50/50/50/50. At K_u=3 the final (B,U,N)=(34,1,2).

This is **not solely a physical buffer-capacity effect**: keeping the same physical rates and 40 physical time units, with K_u=3, dt=1/.5/.25/.125/.0625 gives 38/53/60/60/60 outflows; K_u=6 gives 50/60/60/60/60. A hard synchronous boundary rule delays admission/reuse and biases sink discharge when a finite upstream buffer is small. The plateau at 60 is not a proof of true continuous-time dynamics, but equals the integral upper bound on scheduled sink service.

The exploratory assertion 'all upstream capacities yield the same final discharge' **failed**, so it was replaced by measured case-specific assertions; preserved in the study note as a falsified hypothesis.

## Tests, reproducibility, limitation
- 32 old D46 contract tests plus 19 D46-C tests plus 28 D46-D tests = **79/79 successfully re-executed**.
- The exact executed Python modules (`d46d_finite_cascade.py`, `d46d_experiment.py`, `d46d_storage_sweep.py`, `d46d_dt_sweep.py`), tests, CSV/JSON, logs and SHA256 manifest are byte-preserved in:
  https://drive.google.com/file/d/1tysAmjPeZBuqEEys1CPE9dcDOKS9JaHs/view
- ZIP SHA256: `474a71a0e9749658f0f8d2589465b9828e6d59429a1742412e14a4d244ba9b77`.
- 11/11 scientific reasoning Google Doc: https://docs.google.com/document/d/1ZZPfPZXyHazuLiSqOowHQfSRecseZtzSY1gn1EEOhqc/edit
- No independent SUMO or event-driven reference, physical DLR spatial queue/tail, actual measured upstream demand/supply, D44 viability repair, or empirically validated policy ranking is claimed.

**Next gate:** A genuinely independent event-time update with same upstream/downstream storage and demand/sink schedules, alongside spatial lane length/vehicle occupancy and D44's physical braking constraints. Do not report 38 vs 50 as demonstrated field improvement or intrinsic buffer effect.