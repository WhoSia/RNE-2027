# T2 P11-W / D21 — Spatial Conflict Scope Audit

Date: 2026-11-05. Research-only synthetic event model. P12 SIGNAL POLICY remains FROZEN.

## What was audited

- Base: `WhoSia/RNE-2027` branch `research/t2-spatial-fig2-v02`, file `research/t2/analysis/20261105/p11v_d20/src/lane_fifo.py`; Git blob SHA-1 `c9c6c56a36097cbf7d48c996eee545d1e495f599` as read directly through GitHub connector.
- Existing `eligible()` compared a movement kind with **every active demand across every intersection**, regardless of spatial independence. Capacity checks were already resource-specific. That conflated *type-level conflict* with *spatially shared conflict*.
- Fix: append `conflict_zone: str = "global"` to `Demand`, and require both matching zone and incompatible kinds. `global` default retains exact legacy semantics for existing call sites; **multi-intersection callers must populate zones explicitly**. Empty zone or kind rejected. No new dependencies. End timestamp checked before mutation.

## Controlled witness

Car A: zone A, enter 0 s, resource rA, release 5 s. Pedestrian B: zone B, request 1 s, resource rB, duration 1 s. Conflict kind pair (`car`,`ped`).

- Original/global zone: B enters at 5 s, synthetic wait 4 s.
- Explicit disjoint zones: B enters at 1 s, synthetic wait 0 s.
- Explicit same zone J: B enters at 5 s, synthetic wait 4 s.
- Resource occupancy capacity remains globally shared across zones, preserving physical competition for an explicitly shared resource.

This is an algorithmic counterexample, **not** validated transport demand, physical crossing clearance, safety, or a traffic efficiency estimate.

## Verification

25 local unittest cases passed: 8 copied D20 legacy cases, 8 D20 timestamp/queue measurement cases, 9 new spatial scope tests (including a 12-intersection invariance check). Existing tests are reconstructed from the GitHub connector's retrieved content and are included in the archive; their exact upstream blob identity was not independently proven for the local reconstructed files. No legacy P10 main engine or SUMO run.

## Research decision

- **Development:** explicit spatial conflict zones are required for multi-intersection models. Per-zone conflicts are necessary but not sufficient for realistic movement geometry.
- **Data/replication:** data from Jinju and inD should determine road geometry and movement path mappings, not merely vehicle/pedestrian labels. No site-specific field measurements were acquired here.
- **Science fair:** keep finite turn-pocket storage, crosswalk occupancy, and upstream spillback as a small measurable physical question; source example supplies a model-bug elimination test only.
- **Journal:** event causality, spatial conflict graph semantics, network decomposability, conservation, and numerical convergence are candidates, with novelty and mathematical proof unverified.
- **Policy:** P12 frozen: idea notes only, no optimization search, controller deployment or policy performance claims.

## Unresolved critical cases

1. A movement that passes through multiple junction conflict zones cannot be represented by one `conflict_zone` field. Need explicit set/geometry semantics after source map audit.
2. `global` default permits accidental network-wide blocking if callers omit the zone. In a future breaking version, explicit zone metadata should be validated for multi-intersection networks.
3. Sorting lane-head requests by `(arrival, identity, lane)` is deterministic, not a physically calibrated right-of-way or fairness policy.
4. Unlimited upstream waiting buffer: no true finite-space backward spillback in this module.
5. Event float times, fixed occupation duration, and absence of acceleration or route geometry remain important limits.
6. Primary P10 original main-engine replay and matched independent SUMO remain outstanding.

## MCP-Hub and external reviewed skill provenance

MCP-Hub `hub_discover_reviewed_skills` identified Ponytail code-review skill at `DietrichGebert/ponytail` pinned commit `7801d061243d7b753bad0e0b3c057cd250b11755` and Superpowers pinned `obra/superpowers` commit `22f0b463e7a5e579904dd6211a520321035526f7`. Fetched Ponytail `skills/ponytail/SKILL.md` from pinned repository commit, blob `d64edd32265ba21cbf5270158f04e97d96925f27`. Adopted minimal complete change and regression checks. Neither skill installed or ran as external coding agent in this conversation. MCP-Hub `hub_analyze_public_unified_diff` counted a synthetic example, not correctness audit of full source.
