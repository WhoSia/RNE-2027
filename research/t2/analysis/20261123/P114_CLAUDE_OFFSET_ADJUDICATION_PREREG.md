# P114 — Claude external review adjudication; offset confounding pilot preregistration

Date: 2026-11-23. This document is written BEFORE inspecting P114 simulation output. Source: user-provided Claude report `R&E 2027 T2 연구 외부 독립 심사 보고서.md`, independently audited as an external *claim*, not adopted as truth.

## Scientific correction
The P87 red/green onset comparison changes phase offset as well as cycle length. Therefore it estimates **the effect of the joint policy bundle (period + relative offset + initial red duration)**, not an isolated 30-versus-60 period effect. No assertion that phase *alone* is causal without more controls. Earlier P100/P101 synthetic results and LIRA confidence stay restricted to their exact policy bundles.

## Frozen pilot grid and stop conditions
- seed blocks 86001,86002; arrival families `uniform`, `platoon4`, share .75, arrival intensity 900/h; same old T2 generator. 4 tapes, not four fully independent temporal demand scenarios.
- one cell=7m, pocket 1 cell, receiver 4 cells, original 6-second left-first override at t=84, same pre-t84 checkpoint.
- period 30 with 30 possible integer phase offsets 0..29; period 60 with 60 possible integer offsets 0..59, each **50% green**. 4×90=360 scenario arms. Use `ReceivingCells.green` patch but never change shared geometry or arrival IDs.
- horizon 4800s, not 1440; strict all 60 cars finally departed and exact conservation, otherwise mark `CENSORED`; policy ranking forbidden with terminal residual. Total cost = entire-network occupancy; if fully departed equals total sum(exits-arrival) up to a consistent tick convention.
- T2 P87 special cases: (period30,phi0)/(period60,phi0) correspond both begin green; (period30,phi15)/(period60,phi30) both begin red. Verify exact P101 results for the four tapes after running.
- For **each tape** report all 30+60 policy alternatives: minimum, mean, median and maximum of cost; compare **phase-averaged** period contrast and **phase-optimized** contrast; keep them distinct from arbitrary cross-product contrasts.
- Compute a conservative **independent calendar-only** left-service overlap statistic on t84..400 using actual phase(c.base,t) with P69 override, and evaluate Spearman correlation and tie-aware sign classification on same periods. Restrict any mechanistic conclusion to calendar rank predictive utility; do not claim overlap is sufficient without queue state.
- Primary falsifier: at least one tape must reverse signed 30s-60s cost ranking between selected offset policies; if none, Claude's phase reversal not supported in pilot. Secondary: optimal and mean comparisons may disagree with selected red/green onset.
- Exit gate: any arm with remaining cars at 4800 fails outcome inference; stop, extend horizon or use unbiased censored-value bounds with explicitly reported n. Never penalize with an arbitrary terminal constant.
- This pilot cannot validate Claude's full-sweep counts 45.7%, 26.7%, 96/96 or 90.1%; those remain externally reported until the exact grid and denominator are independently reproduced.

## External reviewer errors requiring scrutiny
- P97 denominator: 192 tapes×two periods×three adjacent loss increments = 1152 **arm-level adjacent comparisons**; previous 576 comes from collapsing across one dimension. An example counter count 2 should be reported as 2/1152 only if the underlying JSON corroborates.
- P100 and P106 incoming **uniform and platoon4 time vectors are deterministic functions of demand and count**, so distinct seeds vary route/turn selection, not temporal arrival process.
- Claude says no original doc corrections on GitHub; P109 README explicitly amended (verify remote main before a status claim), while P103 archived historical text is immutable and superseded by P109.
- Do not accept claims of new engine equivalence merely because `eclipse-sumo` installs.
