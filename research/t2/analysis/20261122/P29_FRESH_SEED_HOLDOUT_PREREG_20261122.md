# T2-P29 — Fresh synthetic seed holdout for P27 long-stage hypothesis

2026-11-22 KST. **Protocol committed before any P29 holdout run.** P27's 24s duration was selected following an outcome-informed diagnostic pilot and is exploratory. P29 independently fixes 4 **previously unused seed labels** to check whether the 24s-vs6s model behavior recurs; no real-world generalization or independence beyond 4 complete timestamp tapes is claimed.

- Seeds `120,121` with demand1650vph/left fraction0.50 and seeds `122,123` with demand1800vph/left fraction0.45. None belongs to P18 104–111 or P19/P25–28 112–119.
- Exact original canonical `main` engine and timestamp generator, original scenario factor grid receiver slots(2,4) × offset(0,15) × pocket(14m,28m) × B-share(0,.5) × receiver-headway(1,2). Total **4 tapes × 32 geometry/headway conditions = 128 synthetic worlds**.
- Each world uses one frozen tick84 checkpoint, baseline and the same two model-native hypothetical stage lengths **6 vs 24s**, with 3s model `-` in front, no-service from the end of action to tick120. Check base config, immutable checkpoint, tape equality and generated vehicle conservation.
- Primary: count model cost 24s<6s, =, > within matched checkpoint, globally and by receiver headway and downstream offset. Secondary: left stopline crossing events ticks87–119, receiver-denial attempts (attempt frequency, **not unique cars**), whether benefit depends on offset.
- A 24s intervention is not an authorized signal plan. No controlled-lane legal yellow/all-red/pedestrian clearance, SUMO vehicle following or RF detection is in the model.
- Do not tune seed, geometry, threshold or action after seeing result; publish all 128 records with SHA and tests. Do not compute p-values on duplicated arrival tapes. This remains **synthetic model transport**, not an empirical out-of-sample road study.
