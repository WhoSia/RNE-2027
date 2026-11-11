# D46-B — throughput uncertainty envelope (2026-11-11)

**Scientific status: synthetic formal/LP tests PASS (32/32); field receiving capacity NOT identified.**

For fixed turning fractions beta and strict incoming-link FIFO, maximizing sum of incoming flows under `0<=f_i<=D_i` and `Σ_i beta_ij f_i <= S_j` has a feasible region monotonically expanding as any component of upstream demand or downstream supply grows. Consequently the LP's **optimal total throughput** for uncertain componentwise intervals is bounded by the solution with all lower bounds and the solution with all upper bounds.

This is a deterministic feasible-set monotonicity result. It **does not** imply movement-by-movement monotonic allocation when the optimal LP solution is degenerate, nor create any empirical confidence intervals for DLR sensor/traffic states.

## Synthetic sensitivity
Single shared upstream approach: D=10 vehicles/step, turn fractions 50/50, outlet 1 supply 8. When outlet 2 supply is *assumed* in [0,2], optimum total throughput ∈[0,4]. When outlet 2 supply *assumed* in [1,3], optimum total throughput ∈[2,6]. No such supply interval has been measured in the DLR UT v1.3.1 field observations.

The official 45-minute (2023-09-24 12:00–12:45 UTC) 1 Hz published movement counts sum to 1409 (E=372,S=397,W=378,N=262). They represent **observed flow at stopline crossings**, not upstream arrival demand or downstream receiving supply. Do not substitute them for both D and S.

## Provenance
Original 25 executed node/field schema tests + 7 newly executed uncertainty envelope tests = **32/32 PASS**. V1 sealed Drive ZIP includes 25 tests: https://drive.google.com/file/d/1X4ofXd6CKhYi5U1heXpbCQjXwvrFVs44/view (SHA256 `de09ba7bd978a4328936a874b4d72c1549665df2ef194d7bb14e0d4e3c02709d`).
V2 full locally executed source + 32 tests + synthetic uncertainty outputs: `RNE_T2_20261111_D46_FIFO_NODE_UNCERTAINTY_V2.zip`, SHA256 `3b291b8d96882209ef04ed4db1028e2a6adc4f8d67e3576d26c77858a8766d42`. The V2 is currently a conversation-generated file and **has not been confirmed uploaded to Drive**. Never claim it was remotely archived.

Research log: https://docs.google.com/document/d/1ZZPfPZXyHazuLiSqOowHQfSRecseZtzSY1gn1EEOhqc/edit

## Open acceptance gates
- independently detect arrivals versus departures on finite lane segments, with event visibility censorship
- obtain actual downstream storage occupancy and feasible supply rather than infer it from already discharged vehicles
- build an actual time-evolving finite buffer with signal conflict phases and physical braking constraints
- compare with independent SUMO executable before any policy rank claim

Reading: Tampère et al. (2011), doi:10.1016/j.trb.2010.06.004; Grégoire et al. (2015), doi:10.1109/TCNS.2014.2378871. Their prior contributions are not newly discovered by T2.
