# XR1 preregistration (external review r2) — does the red-onset paradox survive movement-separated downstream links?

**Frozen before any P129 outcome was computed.** External reviewer (Claude, 2nd review), 2026-11-23.

## Question
In legacy T2, left (L) and through (S) vehicles discharge into ONE shared finite receiver. Is the
"denied down / network vehicle-seconds up" red-onset paradox a property of finite downstream storage
in general, or of two movements *competing for one shared receiver*?

## Engine change
`DualConfig.receiver_split` (default `False`) gives L and S their own `ReceivingCells` with the same
cell count C, exit headway and downstream clock. `receiver_split_left_free=True` additionally makes the
L link always green (an uncontrolled destination). Legacy path must stay byte-identical (checked on
P87, P114, P115, P118, P124, P126, P127, P128 before this run; 14/14 legacy unit tests + 6 new tests).

## Topologies
- `shared` (legacy regression baseline)
- `split_same_clock` (two C-cell links, same downstream clock)
- `split_left_free` (two C-cell links, L link uncontrolled)

## Unseen cohort
Timing seeds **88401..88408** (never used before), label seeds 86001/86002, families
`stochastic_uniform`/`stochastic_platoon4` (P118 generator, unchanged) → 32 distinct timestamp tapes per
left share. Left shares .25/.50/.75; capacities C = 4 and 8; horizon 4800 s, t84 checkpoint per config;
red onset (phi30=15, phi60=30) as in P118/P126/P127. 3 topologies × 3 shares × 2 C × 32 tapes × 2 periods
= 1,152 arms. Every arm must clear all 60 vehicles.

## Primary gate (share .75, C = 4)
Count paradox pairs `denied30<denied60 and cost30>cost60` per topology on the same 32 tapes.
- `split_same_clock` paradox ≤ 8/32 → **core red-onset paradox requires a shared receiver**; thesis is
  restricted to merges / shared downstream storage.
- ≥ 24/32 → paradox **survives** movement separation.
- otherwise → partial; report the counts and do not round.

## Secondary (reported, no gate)
Same counts for every share × C × topology; signed cost-delta sums; for share .75, C = 4 and 8 tapes
(timing seed 88401–88402), the full offset grid (30 × 60) under `shared` and `split_same_clock`:
fraction of tapes where both signs of cost30−cost60 occur, and whether the left-green overlap sign rule
(P116, unchanged) keeps ≥ 75 % strict accuracy.

## Not claimed
Same synthetic engine; not SUMO, not field. 32 tapes = 16 timing-seed × family clusters × 2 label seeds,
not 32 independent demand populations.
