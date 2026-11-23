# P100 preregistration — new held-out demand seeds for onset × turning share

**Frozen before any P100 result read.** Date 2026-11-23; after source-locked P88/P89/P97–P99 full T2 simulation tests.

## Question
Is the sharp red-onset × high left-turn-share pattern seen in P87/P95 a feature of only the original 16 random route seeds (85001–85016), or does it recur in new synthetic route assignments?

## Locked intervention and arrivals
- New route seeds **86001–86032 inclusive**, disjoint from P85–P89 discovery seeds.
- For each seed: turn shares **0.25, 0.50, 0.75** × arrival families **uniform, platoon4** (as in frozen P31) = 192 unique seed/share/family tapes; no re-fitting or selection after seeing outcomes.
- Generate each tape from `build_config(seed, 900, share, 7, 4, .5)`; freeze exact checkpoint at t=84 and set full model duration 1440, downstream offset zero.
- Common left-first upstream 6-second left green; downstream 50% displayed green at **30s or 60s** cycle and green/red onset at decision. Two onsets per tape, thus **384 pairs and 768 simulation arms**.
- Score `cost = outside + A + B + pocket + receiver` vehicle-seconds with terminal penalty 0. `denied` is one-bit upstream receiver-entry blocked seconds; `full_red` as P87.

## Locked primary and secondary tests
1. **Primary reproduction:** under red onset with share 0.75, fraction of paradox pairs `denied_delta<0<cost_delta`. Original was 32/32. Predeclared descriptive evidence target: at least **52/64** in held-out tapes, and report exact count even on failure.
2. **Secondary:** green onset at share 0.25 paradox rate (original 11/32); report and check at least **20/64**, explicitly exploratory.
3. Matched-onset complementarity: the same tape paradox in both green and red; original 0/96, report exact count, do not treat 384 pairs as independent.
4. By seed block and family, report signs of `cost_delta_red - cost_delta_green` and spatial dependence only as a **separate** unexecuted P101, unless traced.
5. All 768 arms **must clear all vehicles** and all 384 paired deltas must conserve source score components. If any fail, do not count those outcomes as successes without documenting failure.

## What is not claimed
Random seeds in one deterministic synthetic model are not independent field replications. A successful 64/64 high-share cohort cannot establish a real-world 100% rate. The denominator is **64 tapes with 32 seed blocks**, and both onsets on a tape are paired, not independent.

## Decision after results
If held-out high-share red paradox >=52/64, prioritize movement-specific traces for representative held-out cases; otherwise demote generalization and investigate the failed inputs. In either case return to the separate independent field/SUMO gate after two consecutive synthetic-only tests. Retain the 0.97 field observation priority until proper downstream exit visibility is acquired.
