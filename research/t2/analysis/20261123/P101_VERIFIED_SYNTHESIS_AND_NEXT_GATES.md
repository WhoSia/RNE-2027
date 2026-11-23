# P88–P101 verified synthesis: who gains, where delay migrates, which clock matters

2026-11-23. This replaces any pre-execution assumption that P88/P89 simulator validation remained pending. All results below were actually run using source-locked Python 3.13, with raw output archived at the same paths.

## Source and run integrity
- Main development source for `dual_lane_v11.py`, `receiving_cells_v15.py`, `spatial_v10.py`, `physical_transfer_screen.py`, `p31_two_arrival_families.py`, `p19_receiver_service_opportunity.py`, `p25_p26_physical_followups.py`, `p39_policy_holdout.py` was compared by **Git blob SHA** with local restored files. **8/8 match**.
- Source was restored from the 2026-11-22 P56 archived source ZIP and selected version-matched `main` files. A dated source-bridge JSON preserving exact current-file blobs supported transport; direct git network/DNS was unavailable.
- Unit tests `test_p93_spatial_movement_identity` (3), `test_receiving_cells_v15` (5), `test_dual_lane_v11` (6): **14/14 PASS**.
- All P88/P89/P99/P100/P101 simulator arms completely cleared; all signed counter identities passed. No `github-actions[bot]`; GitHub contents API written by WhoSia.

## P88/P93: 96 original tapes, 192 exact cycle pairs, 384 arms
All 192 original P87 `delta(cost,denied,full_red)` triplets reproduced. Each signed spatial decomposition summed exactly to source cost; each left/through by-zone reconstruction summed to spatial totals, downstream departure count matched network-out increase.

| Category | n | Outside | A approach | B approach | Pocket | Receiver | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| Green onset, denied lower/cost higher | 12 | 0 | +4,732 | +3,134 | −331 | −1,488 | +6,047 |
| Red onset, denied lower/cost higher | 43 | +7,466 | +40,587 | −11,245 | +2,529 | −1,732 | +37,605 |
| Green onset, both lower | 75 | −26,745 | −100,653 | −863 | −6,986 | −8,219 | −143,466 |
| Red onset, both lower | 39 | −2 | −11,765 | −22,084 | +24 | −2,234 | −36,061 |

In 12 green-onset paradox pairs: **12/12 have higher through-vehicle seconds**, left higher in 7/12. Aggregate left +1,494 / through +4,553. In 43 red-onset paradox pairs: **43/43 higher left-vehicle seconds, 43/43 A-lane increase and B-lane decrease**, 39/43 through decrease and 35/43 outside waiting increase. Aggregate left +46,853 / through −9,248. This is more precise than the initial 55-pair aggregate. It is not a field estimate.

- [Complete P88 output](P88_RESULT.json) GitHub SHA from commit `853e114629c9f892708d6a0fb6539b6697305212`; local UTF-8 SHA256 `8d66e2d25e6ad7e2234013a92bbe62a8fa3c4c490c15db45fdec6dc1033c0362`.
- [Shared Drive P88 exact JSON](https://drive.google.com/file/d/1qgJ5EKOJz_DMoZngFXMDxoIDDFYdjHTd/view).

## P89: startup service mask is not effective green nor actual discharge
All P89 768 matched pairs/1536 simulator arms completed, and loss=0 copied P87 192/192. Green onset: 30-second wins at losses 0/1/2/3 = 83/72/72/62 out of 96; signed cost sums −145,003/−160,241/−158,416/−169,159. Red onset: wins 51/40/41/33; cost sums −13,485/+34,178/+26,518/+98,489. Reduced win count need not imply reduced aggregate savings. The binary 0–3s service veto is a model intervention, not measured HCM headway-based lost time.

P89 [full JSON](P89_RESULT.json), SHA256 `26c29040fc6ebdc72f56a32a2b4a0b6d41717f13f8fc1985f079139615a63551`; [Drive](https://drive.google.com/file/d/1GjPnMctY-e6NVaokhx3J-iEtr_rtJZrc/view).

## P96: first vehicle out is not the objective
Five representative cases replayed. For seed85001/share0.50/uniform/red, 30s period has first receiver departure at 99s versus 60s at 114s, **yet** 30s incurs +126 network vehicle-seconds, with left +265 and through −139. Early first exit alone does not establish lower network delay. [P96 paired ID-level evidence](P96_RESULT.json).

## P97–P98: two absolute cost monotonicity exceptions
Among **576 paired incremental comparisons** (`0→1`, `1→2`, `2→3` startup loss) per onset/period/tape, **574** cost increases and **2** cost decreases. P98 traces reveal both initial downstream first exits move 1s *later* while later groups reorganize:
- seed85003/share0.50/uniform/red/30s: loss 2→3s, cost 5,048→4,795 (−253); left −496, through +243; A −616, B +176, pocket +9, receiver +202, outside −24.
- seed85009/share0.50/uniform/green/60s: loss 0→1s, cost 4,716→4,262 (−454); left −465, through +11; A −526, B +45, pocket +9, receiver +18, outside 0.
No recommendation to deliberately waste green follows from two isolated synthetic exceptions. [P97](P97_RESULT.json) · [P98](P98_RESULT.json).

## P99 finite observation window falsification
Re-ran P89 on horizon t=1464, so [84,1464) is exactly 23×60s and both clocks/onsets have **690 nominal green seconds** at zero loss. All 768 signed P89 cost/denied pairs reproduced byte-level values, **0 changed rankings**, all exited. Thus the previously unequal displayed-green seconds under [84,1440) cannot explain the P87/P89 signed vehicle-seconds differences. [P99](P99_RESULT.json).

## P100 prospectively held-out new route seeds
[Pre-registration](P100_HOLDOUT_PREREG.md) committed before seeing any new outcomes, seeds86001–86032, shares .25/.50/.75 and two clock families, 192 distinct tapes ×2 onsets = 384 pairs (768 arms).
- Primary high left share .75, red onset paradox threshold ≥52/64; **64/64 PASS**.
- Exploratory low share .25, green onset threshold ≥20/64; **29/64 PASS**.
- Both onsets paradox on same tape **0/192**.
These are a new **synthetic seed holdout**, not new field observation. [P100](P100_RESULT.json).

## P101 prospective follow-up mechanism on the SAME 64 P100 high-left-share tapes
[Pre-registered](P101_MECHANISM_PREREG.md) after P100 outcomes and before P101 spatial review; 64 tapes ×2 onsets×2 periods = 256 arms, 128 pairs. **128/128 signed P100 deltas and spatial/turn-class identities reproduced**; all cleared.
- Red onset: 64/64 paradox; 64/64 left-turn cost higher; 64/64 A approach higher; 64/64 B approach lower; 64/64 outside higher. Total left +85,706, through −7,966, cost +77,740.
- Green onset on same 64 tapes: 0/64 paradox; 0/64 left-turn cost higher; 0/64 A approach higher. Total left −206,120, through −7,894, cost −214,014.
- All three preregistered 58/64 mechanism minimums PASS. **This is not a second independent sample**; it is deeper analysis of exactly the P100 heldout tapes.

[P101](P101_RESULT.json) SHA256 `1f5c9410f088f1776c3db6c010039eac34b55192d9ea6bce9ec4e6f607d0ff35`. [Drive](https://drive.google.com/file/d/1IFYidwiQMtpbQ4lE6sATqBbin_c8d9O3/view).

## Director's adversarial interpretation, next portfolio
**What is now established:** Within this bounded, deterministic four-cell simulator, short downstream cycles can reduce upstream blockage while redistributing delay from through to left-turn traffic. The onset-dependent pattern withstands independent new *route seeds*, per-car space-time accounting and a matched complete-window comparison.

**What is not established:** Physical onset timing optimality, real head-to-lane mapping, pedestrian safety/delay, independent engine transportability, or valid controlled field improvement. In particular **Varaiya max-pressure stability results apply to an unbounded-queue formulation**; do not transport the theorem to a finite 4-cell receiving link. FHWA defines effective green including startup and clearance effects, not by the arbitrary P89 binary veto. See [FHWA chapter 3](https://ops.fhwa.dot.gov/publications/fhwahop08024/chapter3.htm).

Reweighted priorities (ordinal research management scores, not posterior probabilities):
1. **0.98** independent simultaneous observed stopline→downstream departure, signal head and lane/turn movements (up from .97: synthetic reproduction is now strong while external identification remains absent).
2. **0.96** independent micro/mesoscopic engine with matched path, storage and timing, rerun new holdout (up from .90: the evidence gap now dominates).
3. **0.93** opposing direction and pedestrian waiting / clearance cost (up from .92).
4. **0.90** actual queue-headway startup loss measurement with multi-cycle clock alignment (P89 is binary sensitivity only).
5. **0.87** detector-error-aware actuated early termination with fairness bounds, after users/observations are defined.
6. **0.85** alternate downstream capacity/pocket geometry holdout and source alias tests (synthetic-only; do not claim priority over external verification).

Research stop rule: no third consecutive synthetic seed extension without first attempting one genuinely independent external/second-engine evidence source. Repeated random seeds alone do not increase model validity.
