# T2 E-track / T-track interface — measurement before policy claims

Date: 2026-11-21. Separate two sources of evidence:
- Exhibition sensing track E: source-labeled *physical* RF trials.
- Existing traffic model track T: finite-receiver, short-pocket,
  paired-tick84 synthetic worlds and feasibility-constrained actions.

The two tracks are complementary but must NOT be joined by silently
inventing a Wi-Fi-to-road simulator. The earlier PHYS-10 support
distance failed to certify beneficial policies; the latest arrival-clock
audit showed changes in route-matched arrival timing could alter
signal-policy ranks. Both facts argue for respecting uncertainty.

## Data handoff contract (UNEXECUTED until actual data)

Only after signed-off independent physical trial records exist,
derive a **measured conditional confusion model**
`P(rf_output, abstention | manual_cause, placement, session)`.
Use full five-class prediction confusion, missingness, latency,
and observed cross-placement drift. Do not fabricate CSI time
series from the T2 state and then call it detector validation.

The T2 side receives a clean **observation category**, not
radio signals, and compares ambiguity sets under a fixed
operationally admissible signal-action family.

For a decision-time observation o, let W(o) be the set of
traffic worlds compatible with o and the measured sensor-error
model. For any candidate abstract policy a against baseline,
report `L(o) = inf_{w in W(o)} ΔJ_a(w)` and
`U(o) = sup_{w in W(o)} ΔJ_a(w)`.
The classifier cannot resolve a policy preference when the
interval crosses zero, absent a better decision rule or more
information. Report worst-case regret as a separate output.

## Four distinct gates

1. **Radio validity:** do metal toy objects perturb the measured
   authorized CSI channel in controlled stationary and moving
   conditions? If not, stop hardware sensing claim.
2. **Causal label observability:** do the two physical regions
   yield distinct response signatures over unseen sessions and
   placements? If not, report failure regardless of in-sample F1.
3. **Decision usefulness:** for which actual T2 worlds does the
   additional observation change the preferred action or reduce
   worst-case regret? Diagnostic F1 alone is insufficient.
4. **Operational/empirical transport:** are traffic demand,
   feasible green/yellow/pedestrian phases, driver behaviors and
   sensor geometry grounded in legally allowed field evidence?
   This is OPEN and is not established by a tabletop demonstration.

## Stop negative-feedback loops

- No measured physical RF files currently in project; gate 1 OPEN.
- Do not adjust PHYS-04~11 policy parameters to make a RF sensor
  'look useful'. The real-world data source determines which
  sensor errors are admissible.
- The old T2 random uniform generator had identical timestamps
  across seeds: transport requires truly varied temporal demand.
- Even if all four stages pass in a lab, an actual road signal
  would require authority, external field trials and independent
  safety approvals; a student demonstration never modifies
  a public controller.
