# T2-P22 — Adversarial multi-role audit: what survives the exact-source replication?

2026-11-22 KST. First new DLR input files were fetched **after** the [P22 preregistration](P22_ADVERSARIAL_REALITY_GATE_PREREG_20261122.md) was committed. Source is the prior exact GitHub-main P19 results and the original DLR-UT v1.3.1 stopline-count metadata from the R&E shared dataset lake. **Do not conflate empirical counts with causal policy improvements.**

## 1. BFS → DFS provenance, not a dataset collection contest

Historical chat archive was actually reopened from Drive: \`20261027.md\`, \`20261111.md\`, \`20261117.md\`, \`20261121 1.md\` in \`00_CHAT_ARCHIVE/김우준_CHAT_ARCHIVE\`. The research decision tree is:

1. **Physical T2 traffic question:** short left-turn pocket, lane bypass, finite downstream receiver, arrival clocks, phase interactions, conservation and independently executable physics.
2. **Empirical observability / RF-CURTAIN:** do real sensors identify *different causes* of blockage? Controlled physical measurement must precede any RF→policy claim.
3. **Value of information and admissible policy:** do additional pre-decision observations change a *legally feasible* signal choice and lower regret? Do not optimize post-treatment knowledge.

The parallel **data acquisition sequence** is separate: already-owned DLR first; Utah SPaT+BSM and INTERACTION TC/DR as targeted external observations; static CSI for independent RF feasibility. Download count is not a research metric. The two INTERACTION files reported downloaded to the user's PC were not yet visible in connected Drive and no actual file move was reported; the verified incoming directory remains https://drive.google.com/drive/folders/1k-EEwOyBgUVoQaGwQsModGfmP92w0Gzv .

Earlier failed paths restored: a signature signal paradox disappeared when lane bypass was allowed; changes to the terminal cost could reverse some narrow counterexample signs; DLR 2.05s gap and exit-selected cohort were post hoc; SUMO time-step comparisons were sensitive; a staged RF pocket obstruction is not the same thing as a nonempty traffic pocket. Each remains a relevant negative control.

## 2. Audit method and reproducible evidence

- Frozen P19 synthetic model: 256 rows, **16 distinct full arrival-tape hashes**, 32 tape×downstream-offset blocks, 128 geometry-matched cross-offset pairs. Model cost sign is not measured traffic performance.
- Pre-inspection frozen DLR windows (2023-09-24, Sunday): **12:00–12:15 UTC**, **18:00–18:15 UTC**, and previously analyzed **23:30–23:45 UTC**. Not cherry-picked based on observed crossings.
- DLR README describes \`meta_data/traffic_volume\` CSV as **one-second counting of traffic participants when their center crosses a lane stopline**. The code verifies all three exact raw file SHA256, UTC timestamps, one-second grid continuity, movement names, and binary indicator fields. No K047 opening or protected holdout.
- [Executable code](p22_block_and_stopline_audit.py) Git blob \`6b6a475130f09a493b6e6789bd85592b238954ee\`; [seven tests](test_p22_block_and_stopline_audit.py) blob \`a832aa8eaf098c0e6fe30bfab132193d234376f1\`. Both byte-match locally tested source via \`git hash-object\`. **7/7 tests PASS using the actual source CSV files**, not fixtures alone. Full JSON SHA256 \`85a216ac134791238f5462254bffbf4792874ec33be05a0069dda0172a4275b7\`; test log SHA256 \`81a6152ca55b9ab91e581295f276df05a2aef80f3e316ace08f1890d77c050e8\`.
- [Structured results](P22_ADVERSARIAL_STOPLINE_AND_BLOCK_RESULTS_20261122.json) are a compact digest; full source and output are supplied in the exact-binary local reproduction ZIP. No double-counted source measurements.

### Observed DLR stopline counts

| Predeclared 2023-09-24 UTC | Source byte SHA256 prefix | Valid 1-s rows | Movement columns | Per-movement crossing indicators (sum) | Seconds with ≥1 indicated crossing |
|---|---|---:|---:|---:|---:|
| 12:00–12:15 | 98e4e0a59370 | 900 | **32** | **436** | 336 |
| 18:00–18:15 | 62bc193f77d7 | 900 | **27** | **192** | 178 |
| 23:30–23:45 | 00f6f29b2be6 | 893 | **12** | **17** | 17 |

The midnight-side file starts at 23:30:07; it does **not** cover a full 900 seconds. All available rows are 1-second spaced and all movement indicators are 0/1. The schema is NOT constant across files: columns for absent movements may be omitted from a file. We do not infer zero traffic in an omitted column without a verified source contract. These counts represent *published derived stopline-crossing observations*, not unique matched vehicle IDs, exact headways, queues, turn-pocket overflows or downstream spillback.

The 12:00 window has far more crossings than the late-night window, but **high throughput is not proof of congestion**. Signal-head→lane mapping, observed green intervals, vehicle-level stopline times, queue-tail positions and camera field of view remain open.

### P19 computational pseudoreplication and seed sensitivity

| Outcome for virtual 8s protected-left modification | Offset 0s | Offset 15s |
|---|---:|---:|
| Reused-geometry world rows | 128 | 128 |
| Negative model delta (intervention helpful) | 33 | 35 |
| Positive model delta (intervention harmful) | **61** | **0** |
| Ties | 34 | 93 |
| Distinct tape hashes | **16** | **16** |
| Tape blocks containing *any* harmful scenario | 14/16 | **0/16** |
| Cost-difference sum across dependent geometries | **+5108** | **−12100** |

One-sided exact Clopper-Pearson upper confidence bound with 0 adverse tape-block observations in 16 iid/exchangeable **hypothetical** trials: \`1-0.05^(1/16)=0.17074972298248094\`. Independently evaluated with **Wolfram Language**, matching local Python. It is **not** a confidence interval for real-world intersections: random pseudo-tapes and a single engine do not supply a validated exchangeable sample of traffic days.

**Adversarial observation:** offset0 total +5108 is *not leave-one-seed stable*; excluding seed115 yields **−2248**, excluding seed118 yields **−2230**. These are leave-one-seed diagnostics conducted after P19's results were known, so label exploratory, not preregistered primary contrasts. They demonstrate risk of relying on aggregate model cost.

### Post-prereg exploratory objective check

[Exact-source 256-world rerunner](p22_penalty_sensitivity.py), verified against **all 256 frozen P19 deltas at p60**. At penalty 0,60,120 the offset0 harmful/helpful/tie split stayed 61/33/34, and offset15 remained 0/35/93. Aggregate cost totals offset0: +3428,+5108,+6788; offset15: −7420,−12100,−16780. **A model cost penalty sensitivity survived this particular range, but this cannot rescue the unverified physical phase or generalization.** Exact postprereg exploratory JSON locally hashed SHA256 \`4140b1eb1204be8bef1eff625be5dc44f044ff3ee7d1eb1dbada68ebee22415d\`. This comparison is not a newly preregistered result.

## 3. Explicit review panel — internal roles, not independent models

| Role | Claim under review | Objection / falsification | Verdict |
|---|---|---|---|
| BUILDER | The T2 main-source P19 result is reproducible | P18 exact PHYS-04 and P20 512-path receiver shadow audit reproduce **specified model laws**, but share many assumptions | **ACCEPT internal computational reproducibility** |
| SKEPTIC | Offset15 phase is never harmful | 0/128 pseudo-replicates collapse to 0/16 tape blocks; no legal controller or real-world traffic input; future harm is unbounded without exchangeability | **REJECT general-purpose superiority claim** |
| STATISTICIAN | World-level totals are robust | Seed115 or seed118 deletion alone reverses offset0 sum sign; pseudorandom tape reuse violates independent-row binomial analysis | **REJECT iid world-level inference** |
| EMPIRICAL AUDITOR | Previous DLR night sample measures queue failures | 17 crossing-bin events vs 436 in preregistered midday, and varying movement columns; no independently validated stopline→signal mapping or queue tail | **REJECT queue/spillback interpretation** |
| SENSOR AUDITOR | Pocket occupancy in the model proves RF detection | Source has no actual CSI measurements; stationary obstacles, moving queues, downstream blockage labels differ | **HOLD RF field/bench inference** |
| POLICY REVIEWER | P19 policy is executable and safe | Virtual 3s no-service clearance does not implement a verified yellow/all-red, pedestrian, conflict, minimum-green or phase-change contract | **HOLD deployment/real-policy claim** |

MCP_Hub provider was inspected: its currently surfaced 24 actions are bounded utilities, scientific metadata, transport and verification—not a callable general-purpose peer-reasoning LLM. We **did not impersonate another LLM or 김세호**. The four-plus roles above are an internal adversarial reading of evidence; only the exact upper-bound arithmetic was independently checked in Wolfram. Genuine review independence would require an external reviewer with access to the full evidence and independent reproduction.

## 4. Next course and stop rules

- **Physical (priority1):** import official DLR map/stopline lane linkage, signal-state codebook, and identify at least one *actually controlled* movement and vehicle-level crossing condition before estimating discharge headways. Then execute independently specified SUMO with frozen geometry/tape. Retain adverse comparisons instead of changing objective after observing outcomes.
- **Sensor (priority2):** do not replace physical ground-truth labels by an RF five-class simulation; evaluate stationary-object vs nearby-motion with actual permissioned CSI and independent ground truth, plus cheap baseline.
- **Decision information (priority3):** predefine feasible phase action set, then estimate value of predecision observables and worst-case regret across distinct test days/tapes. If no different-action same-observation world is found under ε=5, preserve NO_WITNESS rather than silently dropping matching constraints.

No real traffic-signal actuation, K047 still sealed, CIM ~5GB still hold/unseen, INTERACTION not yet accessible from PC downloads, no GitHub Actions bot, no speculative policy-effect claims. Source lineage: P22 exact local script/log, existing original DLR metadata and P19 frozen JSON, archival chat excerpts specified above.
