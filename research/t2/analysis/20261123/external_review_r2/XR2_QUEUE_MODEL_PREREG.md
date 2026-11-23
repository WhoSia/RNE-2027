# XR2 preregistration (external review r2) — minimal tandem queue with blocking vs the left-overlap rule

**Frozen before P130 outcomes were computed.** External reviewer (Claude, 2nd review), 2026-11-23.

## Model (p130_queue_model.py; independent code, imports nothing from T2)
Arrival → free travel τ_u=20 s → stopline queue → upstream phase service (L: 1 per 2 s; S: 1 per s) →
shared store of capacity C (admit only if < C held) → minimum dwell τ_d=C−1 s → exit 1 per 2 s while the
downstream signal is green (FIFO).
- **M0**: left-green overlap seconds in [84,400) only (P116 rule, unchanged).
- **M1**: movement queues, finite store, storage carry-over between windows. No lane interaction.
- **M2**: M1 + lane-A head-of-line blocking with a k=1 pocket, S lane share 0.5 (own RNG, seed 0).
All parameters above are fixed now; nothing is fitted to T2 output.

## Claim being tested
Total cost differences that the overlap *sum* cannot explain (P122–P124) come from **when** each
window opens relative to the store content and queue stocks carried from the previous window.
A model with only queue stocks + finite store should therefore (a) beat M0 on the sign of
cost30(φ30) − cost60(φ60), and (b) work on the equal-overlap pairs where M0 has no information.

## Cohort (unseen)
Timing seeds 88501–88504 × label seeds 86001/86002 × {stochastic_uniform, stochastic_platoon4} = 16
tapes; left share 0.50 and 0.75; C = 4 and 8; full offset grid (30 + 60 offsets) → 64 configs,
5,760 T2 arms, 115,200 crossed (φ30, φ60) pairs (not independent; cluster = tape).

## Gates
- **G1 (useful):** pooled strict sign accuracy of M1 or M2 ≥ M0 + 3 percentage points.
- **G2 (explains P122-type pairs):** on pairs with equal left overlap, strict sign accuracy ≥ 75 %.
- **G3 (rank):** median Spearman ρ between model and T2 cost across offsets (within period) ≥ 0.7.
- **Failure:** if neither M1 nor M2 passes G1 and G2, the claim that queue stock + finite store is
  sufficient is rejected; the residual is attributed to cell/lane mechanics not in the model.
Report per-variant accuracy, coverage, and per-tape spread; do not tune after seeing results.
