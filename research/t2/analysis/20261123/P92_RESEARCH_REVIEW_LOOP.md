# T2 Research Director: Generate → Attack → Verify → Decide (v1.0, P92)

**Scope:** R&E 2027 T2. This is a *public, repeatable research QA protocol*, not a claim of independent agents, private system prompts, or results that have not been executed.

## A. Five independent checks in order

1. **Evidence custodian:** Read current GitHub `main` and original dated Docs; inventory exact source files, revisions, hashes, and data origin. Every claim receives one label: observed-field, independent-engine, synthetic-simulator, source-JSON-derived, deterministic-clock, hypothesis, or unexecuted-code.
2. **Hypothesis proposer:** State a sharp falsifiable operational claim about which controller, traffic state and road user is helped; define exposure, comparator, identification assumptions, and an explicit minimum success criterion.
3. **Adversarial reviewer:** Invent a counterexample or confounder **before** examining test outcomes. Mandatory attempts: sign reversal at different onset/offset, a worst affected road user, window/terminal cutoff sensitivity, detector invisibility, omitted pedestrian/conflicting movement, model mismatch, and leakage between matched tapes. Do not suppress failed tests.
4. **Independent verifier:** Compare full JSON inputs with a separately coded aggregation; require deterministic replay, vehicle conservation, exact zone-sum identity, record-level ID/time order and reproducible output hashes. A git commit is **not** a test run. Halt claims when simulator access is unavailable.
5. **Decision auditor:** Reweight projects after each validated result. Evaluate marginal identification value, field transport, novelty, independence of evidence, implementation effort, and risk of confounding. Report changes and why another project lost/gained rank.

## B. Decision policy for DFS/BFS

- **DFS depth gate:** A mechanism hypothesis can receive two consecutive stages of refinement only if at least one new stage achieves a predeclared validation gate or eliminates a specific competing explanation.
- **BFS breadth gate:** After two stages on one mechanism, require one orthogonal audit (field observation coverage, independent simulator, pedestrian/conflicting-direction users, actuated gap-out, or literature challenge). Breadth stage must yield an artifact or a falsifiable exclusion—not another wish-list.
- **Stop gate:** Abandon a high-scoring task when it repeats an existing measure, lacks an identifiable comparator, or requires observations unavailable in the current source. Mark blocked and promote the next feasible task.
- **Reproducibility gate:** Code-only evidence is `PENDING_EXECUTION`. Full test PASS requires archived stdout/result, exit code, full comparison (including negative cases), and remote file/hash verification.
- **Documentation gate:** Every version writes to the *same dated Google Docs running diary*, with results, limitations, status, priority updates and commit SHA. Save supplementary artifacts to the dated shared-drive project folder; do not use github-actions[bot] or create proliferating branches.

## C. Applied adversarial review: P87 → P92

### Claim at risk
'Less downstream entrance blockage means lower full-network vehicle-seconds.'

### Falsifier already observed
P91 source reaggregation: 51/55 P87 cases with lower denied-seconds and **lower** full-red-seconds still have greater total vehicle-seconds. So neither individual binary blockage indicator nor their conjunction establishes lower cost.

### Mechanism not yet proven
The decomposition
`delta_cost = delta_outside + delta_A + delta_B + delta_pocket + delta_receiver`
holds by algebra **if** all five terms are measured at the exact engine score sampling instant (after movement/admission), using the same t-range and subtracting matched baseline counters. P88 code contains assertions; **the actual 192-case run remains unexecuted** in the available environment.

### Relevant FHWA critique
- In the *Traffic Signal Timing Manual*, ch. 3, queue startup lost time is derived from departure-headway behavior, often approximated as 2s; effective green also accounts for yellow/clearance intervals, so a binary prohibition for 2s is only a sensitivity model, not measured startup loss.
  https://ops.fhwa.dot.gov/publications/fhwahop08024/chapter3.htm
- In *Signal Timing Under Saturated Conditions*, FHWA warns against unconditionally equating a longer cycle's lower lost-time fraction with superior throughput; turn-lane access can reduce actual discharge during long green.
  https://ops.fhwa.dot.gov/publications/fhwahop09008/guidance.htm
- FHWA's coordination manual explicitly treats upstream platoon arrivals, phase offsets and non-coordinated gap-out. A purely upstream or downstream isolation model cannot determine full-corridor optimization.
  https://ops.fhwa.dot.gov/publications/fhwahop08024/chapter6.htm

### Unexecuted follow-ups and acceptance criteria
- **P88:** Run `python p88_spatial_audit.py > P88_RESULT.json`; verify original 192 P87 delta triplets, 192 exact spatial cost identities, upstream/downstream per-zone counter identities and downstream exit conservation before accepting any reported mechanism.
- **P89:** Run `python p89_startup_loss.py > P89_RESULT.json`; require 192 loss-0 matches to P87 for cost and denied; compare each of 0/1/2/3s separately for onset, share and clock. Nominal and effective green are exposures, not observed discharges.
- **P92:** Construct a capacity-versus-delay negative control with saturated vs under-saturated arrival conditions and disaggregate *actual exit counts and output headways*. Reject the assumption that lost-green seconds directly convert to a fixed count of delayed vehicles.
- **Field validation:** independent simultaneous receiver stopline and downstream exit with verified signal-to-movement mapping. Existing P80/81 nighttime trajectories do not observe the last downstream section; maintain censoring in claims.

## D. Updated portfolio scores (not probabilities)
- 0.97 field simultaneous observation, including movements and physically identifiable downstream exit.
- 0.96 P88 spatial/outlet conservation, highest-value *feasible model* check.
- 0.93 P89 full loss-time sensitivity simulation and sensitivity against the observed headway.
- 0.92 P92 actual-discharge headway negative control, needed to distinguish signal exposure from throughput.
- 0.89 competing-direction and pedestrian user cost/control constraints.
- 0.87 actuated gap-out with minimum-green and missing-detection robustness.
- 0.85 held-out platoon/offset cohorts with independent model cross-check.

**Corrective note:** Do not treat P89's unequal nominal displayed-green seconds over [84,1440) as the *cause* of P87 delay differences; all P87 vehicles have cleared by 1440, and relevant overlap between demand, queues and green windows must be assessed before identifying a horizon artifact.
