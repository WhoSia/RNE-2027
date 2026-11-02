# T2 v5.2 — Physical pocket model audit / 2026-11-02

**Source**: fork of `research/t2/microscopic/v51/network_v51.py`; corrected terminal straight-outflow misclassification before acceptance of any bay-length results.

## What code actually changes
`PocketGeometry((L0,L1,0))` adds P0 and P1 finite physical-location queues. A route whose final link is M0/M1 is a synthetic branch/turn, entering its own pocket only when x≥(link length−pocket length), occupancy lower than floor(length/6.5m), and entrance net gap acceptable. Otherwise vehicle remains in through lane and can impede through traffic. Lateral motion time is **instantaneous**, not MOBIL/LC2013. Movement clearance on each junction is serialized by shared next_junction_release; all exit and through movements still share main phase, no protected turn phase. The main road terminal M2 **does not use any turn pocket**; main_outflow is distinct from main_exit. J2 pocket geometry required zero.

## Test provenance
46/46 tests PASS locally: 37 revised regression tests derived from v4.9-v5.1, 9 new pocket-specific tests. Zero-pocket mode maintains v5.1 primary measures under matched manifests. Per-step conservation, per-lane gaps, exposure reconstruction and no multiple crossing per junction in one dt are checked. These internal tests cannot establish fidelity to field traffic.

## Exploratory training execution
4 physical bay lengths (15,30,60,90m) × 3 synthetic demand cases × 3 candidate signal plans × 8 seeds = 288 runs, horizon 440s, arrivals until 260s, dt0.5s; identical generated OD across policies and lengths within each demand×seed.

## Independent-seed replication
Another 8 seeds not used in exploratory study, comparing 15 and 90m, 3×3×2×8=144 runs. All 9 demand×policy groups showed negative mean long−short cumulative vehicle seconds, and 7/8 or 8/8 seed pairs improved. For balanced/fixed: −341.6 vehicle·sec, approximate 95% t CI [−559.0,−124.1]; main_peak/fixed −345.7 [−429.5,−261.9]; side_peak/fixed −416.4 [−550.3,−282.6]. These uncertainty intervals reflect seed variation only, not model discrepancy or real-world uncertainty. 15m bays yield cap=2, 90m cap=13 with 4.5m effective car length and 2.0m minimum gap.

## Policy-ranking caution
Exploratory 8 seeds: best policy at every pocket length was main_priority_38 for balanced/main_peak and fixed_32 for side_peak. Independent 8 seeds: best remained main_priority_38 for balanced/main_peak, but side_peak at 90m switched to coordinated_32 by only 58.625 vehicle·sec mean; paired fixed vs coordinated CI included 0. Thus **do not report an established ranking reversal**. The best among three candidate policies is not a global optimum.

## Main mechanistic and external limits
- No actual site map, field counts, fitted car-following, measured turn fractions, lane widths or geometry, lane-changing clearance duration, diverging taper or turn-only protected phase.
- Parallel pocket service shares the `main` stage, not true independently timed left turn; one moving vehicle/junction/tick conflict restriction is conservative and idealized.
- No traffic safety empirical claims; no SUMO cross-simulator numerical comparison.
- Expected bay overflow phenomenon is **already known**; see Yin et al. 2011; Yang et al. 2022; FHWA guide. New engineering challenge is to implement and externally validate a named Korean corridor, then analyze observational sufficiency.

## Next scientific gate
Implement protected turn stage + conflict graph and continuous or discrete gap-accepted lane-change with explicit taper, check parity in SUMO, then acquire authorized/non-identifying Gyeongnam counts and timing. Compare independent day queue profiles / spillback indicators / travel time distributions.
