# T2 — 2026-11-24 (Asia/Seoul) research ledger

All **new** experiment artifacts produced after **2026-11-24 00:00 KST** are stored under this dated directory and its [dated shared Drive folder](https://drive.google.com/drive/folders/1fUSmPVn5AmsrUhNXvrvZhtamtqeGPhWk). The preceding [20261123](../20261123) directory, original T2 code, and older Docs are preserved.

**Shared Drive Google Docs (separate, not appended to the previous day's giant diary):** [20261124 daybook](https://docs.google.com/document/d/1f71vxkv8Fbro5L_7Bsl7gLCICZDyst5jw2mBS6bIxDo/edit), [P136 experiment report](https://docs.google.com/document/d/19JWVWsrrDT9jJ_YpdLN_xvniWd5O1wAeC3cyjBsqgR4/edit), [P137–P138 new holdout + adversarial audit](https://docs.google.com/document/d/1qh53hZSeCQhRwDBKDLMZ34AIJ0F0Y6CvKvu4rM_Gi0w/edit).

## P136 — preregistration before any outcomes
- [Prereg](P136_OFFSET_DIVERSIFIED_PROXY_REGRET_PREREG.md), commit `6709321b121e46e9915cb30145c5f5246e66bc29`
- [Runnable source](p136_offset_diversified_proxy_regret.py) · [full 64 pair records](P136_RESULT.json) · [run stdout](P136_RUN_LOG.txt)
- T2 P130 S-first shared-global-exit split2+2 fork, **unseen** timestamp seeds `88601,88602`; 16 route/time/share tapes × 4 **pre-frozen** (phi30,phi60) packages `(0,30),(15,0),(7,15),(23,45)` ×2 periods = **128 simulator arms, 64 paired choices**. Every tape has 60 terminal IDs; tracing matches refusal attempt seconds exactly.
- 30s cheaper 35/64, 60s cheaper 29/64; aggregate balance gate PASS, **but offset-specific cohorts are severely imbalanced**: 30-win counts `1,16,2,16` out of 16 per fixed package.
- Proxy chooses whichever counterfactual period has smaller *measured after policy rollout* denial metric, ties choose 60s. Pooled refusal-second and refused-attempt proxy: 52/64 correct, full regret **19,372 vehicle-s**; fixed30 **36,866**, fixed60 **125,011**. Unique refused vehicle ID proxy: 30/53 covered correct and full regret **48,405**. Seconds and attempts passed their INITIAL prereg benchmark vs the best constant-period policy. **Not a deployable online controller**; it needs BOTH counterfactual rollout proxy scores, not t84 observable features.

## P137 — stricter reference benchmark evaluated on *new unseen timestamps*
- [Prereg](P137_NEW_TAPE_CALENDAR_BASELINE_PREREG.md), commit `38f98702fa81929d6e4d0bbc593994c6a9a8b7eb`
- [Runnable source](p137_calendar_proxy_fresh_holdout.py) · [all results](P137_RESULT.json) · [run stdout](P137_RUN_LOG.txt)
- Calendar-only lookup `(0,30)→60;(15,0)→30;(7,15)→60;(23,45)→30` fitted on P136 **then frozen before running** P137 with timing seeds `88701,88702`. Same 16 new tapes ×4 offset packages×2 periods = **128 new simulator arms**, 64 paired choices; no repeated timing seeds from P136/P135/XR1.
- Calendar lookup **61/64 correct** and **1,646 vehicle-s** regret. Refused seconds and attempts proxies **50/64 correct**, **19,280 vehicle-s** regret; unique ID proxy **29/52 covered correct**, **48,613** regret. Fixed30 **38,484**, fixed60 **124,800** regret.
- **All three proxies FAIL predeclared additional-value test** versus the calendar-only baseline. P136 proxy improvement vs a *constant* period does not demonstrate incremental predictive value over phase offset information.

## P138 — reaggregation, zero new simulations
- [Independent JSON arithmetic and matched-tape audit](p138_offset_stratum_leakage_audit.py) · [machine-readable conclusions](P138_AUDIT_RESULT.json)
- Both P136/P137 have the exact same four offset-condition win counts (30s wins `1,16,2,16`) under distinct unseen time seeds. The overall 35:29 class balance is mixture balance, NOT balance inside policy-offset strata.
- After aggregating four offset decisions WITHIN each of the 16 original demand tapes in P137, frozen calendar rule has lower regret in **11 tapes**, refusal-second proxy wins in **2**, and **3** tie. Full total gap = **19,280 - 1,646 = 17,634 vehicle-s** in favor of the calendar rule. The 16 tapes retain route/timing-root dependence; no naive independent-intersection CI.
- Explicitly do NOT count P138 as simulation and do not claim external SUMO/field validation.

### Replay
From repository root:
```bash
export PYTHONPATH="research/t2:research/t2/analysis/20261122:research/t2/analysis/20261123:research/t2/analysis/20261124"
python research/t2/analysis/20261124/p136_offset_diversified_proxy_regret.py
python research/t2/analysis/20261124/p137_calendar_proxy_fresh_holdout.py
python research/t2/analysis/20261124/p138_offset_stratum_leakage_audit.py
```
These scripts regenerate JSON, so keep immutable Git revisions of the accepted results. Avoid rerunning in untrusted directory without saving a diff.

### Scientific director's stop / next gate
**Reject** generic claims that current post-treatment `receiver_denied_seconds`, refusal attempts, or unique refused IDs alone enable superior practical control. They use information collected after running both alternative policies; without a pre-intervention state predictor this is *surrogate accounting*, not on-line decision making. Freeze any next surrogate selection rules BEFORE opening future seed outputs, compare against the trained calendar-only rule and the oracle; prioritize SUMO XR3→XR7 E0e exact-ID stage parity and independent real-geometry reproduction. XR1 split-link residual paradox (7/32) **falsifies** `REQUIRES_SHARED_RECEIVER` logical necessity; XR2 pooled M1 accuracy 0.895 masks 1/16 red-onset agreement at share .75 / C8. Those corrections were committed before the date rollover in the [20261123 external-review directory](../20261123/external_review_r2).

**Status counts:** 20261124 P136 + P137 = **256 new T2 full trace arms**, P138 = **zero** new simulations. One GitHub `main` branch / WhoSia account / no github-actions[bot]. 

## P139–P143 — pre-treatment guards fail temporal and route-label transfer

**Do not continue threshold-tuning DFS without new scientific features.** The P136-trained offset-only policy is a very strong comparator within this synthetic model; switching to Q-thresholds after seeing P140's favorable share50 outcomes **does not transport** to P141's new timing tapes. Synthetic trace-derived predecision states are not real roadside sensor measurements.

- [P139 prereg](P139_PRESTATE_QUEUE_GUARD_PREREG.md) · [code](p139_prestate_queue_guard.py) · [pure tests](test_p139_prestate_queue_guard.py) · [16-checkpoint actual preflight](P139_PREFLIGHT_RESULT.json). Original rule demanded receiver occupancy >=3 at t84. Actual 16/16 frozen t84 checkpoints had receiver occupancy=0 and upstream+outside+pocket stock 8–19. **UNINFORMATIVE_NO_TRIGGERS**. **No 128-arm P139 full replay**; only two diagnostic arms were run. Do not claim P139 validation.
- [P140 prereg](P140_UPSTREAM_QUEUE_HOLDOUT_PREREG.md) · [source](p140_upstream_queue_holdout.py) · [4/4 unit tests](test_p140_upstream_queue_holdout.py) · [128-arm full JSON](P140_RESULT.json) · [execution log](P140_RUN_LOG.txt). New time seeds 88901/88902, Q>=14 override only at offset(7,15). Frozen calendar **58/64 correct / regret 4,035** vehicle-s; queue guard **54/64 / regret 21,875**, +17,840 regret; 8 triggers (2 beneficial, 6 harmful). SHARE .5 improved 4,035→1,731 (2 triggers helpful), share .75 worsened 0→20,144 (6 triggers harmful). **PREREG FAIL**. Fresh timestamp seeds, but route seeds still86001/86002.
- [P141 prereg](P141_DEMAND_CONDITIONED_GUARD_PREREG.md) before results · [source](p141_demand_guard_holdout.py) · [results](P141_RESULT.json) · [run log](P141_RUN_LOG.txt): post-P140 hypothesis was frozen before unseen time seeds89001/89002: choose30 only if share<=.50 AND Q>=14 at offset(7,15). 128 complete arms, 64 matched pairs. Calendar **59/64 / regret3,111**, guard **57/64 / regret5,107**; two triggers **both harmful**, extra +1,996 regret. **PREREG FAIL**. This is a falsification of the *posthoc-trained* P140 interaction, not a claim no state model can work.
- [P142 prereg](P142_NEW_ROUTE_SEED_TRANSFER_PREREG.md) before P141/P142 outcome · [source](p142_new_route_seed_transfer.py) · [results](P142_RESULT.json) · [run log](P142_RUN_LOG.txt): route-label seeds **86101/86102** and time seeds **89101/89102** both new, exact same frozen P141 policy, 128 complete trace arms/64 pairs. Calendar **62/64 / regret120**, guard same; all share50 t84 upstream Q in range **8–12**, below threshold14, **0 rule triggers**. Label **UNINFORMATIVE_NO_TRIGGERS**, not a successful controller.
- [P143 posthoc audit](p143_guard_transport_audit.py) · [machine-readable](P143_AUDIT_RESULT.json) · [3/3 rule/seed pure tests](test_p141_p142_frozen_policy.py): reaggregates three 64-pair results, no new engine arms. Guards added regret P140+17,840, P141+1,996, P142+0; the last is purely no-trigger. Input tapes are repeated under four relative-offset packages; not 64 independent intersections per cohort. Common physical T2 model, no SUMO/field parity.

**New full simulation counts:** P140/P141/P142 = 128×3 = **384 full T2 trace arms**, plus **2 P139 diagnostic arms** and **16 P139 checkpoint observations** (P139's planned 128 not executed); P143 = 0. Native Docs reports both [P139–P140](https://docs.google.com/document/d/1cXhj-D5cNiz63oKGdZzJSk0hysEUSKrcCw8hdn1LHaw/edit) and [P141–P143](https://docs.google.com/document/d/1jNjyVrbZcBh8rdNVAVYdfbnMQX5CbF9Ul1dGyOlelac/edit) are created INSIDE the [dated shared Drive folder](https://drive.google.com/drive/folders/1fUSmPVn5AmsrUhNXvrvZhtamtqeGPhWk) with file parent membership verified. Also appended to the independent [20261124 Google Docs daybook](https://docs.google.com/document/d/1f71vxkv8Fbro5L_7Bsl7gLCICZDyst5jw2mBS6bIxDo/edit).

**Director next gate:** STOP trying slight threshold changes on same T2 simulator. Switch BFS to (1) actual SUMO XR7 per-ID insertion/stopline/final-exit parity and unmeasured queue-service differences; (2) independently specified finite-buffer movement-specific queue service-window model with explicit observable-state and tie arbitration, and (3) measurement feasibility of prestate route-share information. P125 conservation identity is prior art. Until SUMO E0e exit-time parity passes, **policy sign transport is forbidden**.
