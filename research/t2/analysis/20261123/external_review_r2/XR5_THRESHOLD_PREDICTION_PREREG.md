# XR5 preregistration (external review r2) — an out-of-sample prediction for the storage threshold

**Frozen before P133 outcomes were computed.** External reviewer (Claude, 2nd review), 2026-11-23.

## Prediction (derived, not fitted)
Under red onset, the short cycle (period P, 50 % green) gives a red of R = P/2 s at the start of the
left phase. The protected left discharges one vehicle per h = 2 s. If the shared store holds at least the
left vehicles discharged during one short red, i.e. **C ≥ C\* = ⌈R / h⌉ + 1** (the +1 is the vehicle
already entering at red start), left service is not starved by the short cycle and the paradox should
vanish. For P = 30 this gives C\* = 9 − 1 … reported frontier 7→8; we therefore state the rule as
**C\* ≈ R/h ± 1** and predict the location of the transition for new periods:

| short/long period | R (s) | predicted transition (paradox ≥ 50 % → ≤ 10 %) |
|---|---|---|
| 24 / 48 | 12 | between C = 5 and C = 7 |
| 30 / 60 | 15 | between C = 7 and C = 9 (known: 7→8) |
| 40 / 80 | 20 | between C = 9 and C = 11 |
| 50 / 100 | 25 | between C = 12 and C = 14 |

## Design
Left share 0.75, shared receiver, red onset (φ = P/2 for both arms), timing seeds 88701–88708 ×
label seeds 86001/86002 × {uniform, platoon4} = 32 unseen tapes, C = 4..16. Upstream calendar unchanged.

## Pass / fail
Pass for a period pair if the first C with paradox rate ≤ 10 % lies inside the predicted window and
every C at least 2 below the window has rate ≥ 50 %. The rule is **falsified** if ≥ 2 of the 3 new
pairs (24/48, 40/80, 50/100) fail.
