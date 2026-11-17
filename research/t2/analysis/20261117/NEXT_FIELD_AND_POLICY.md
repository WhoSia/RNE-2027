# T2 — field inputs and exact policy comparison

**Development order.** Use Jinju first to implement domestic file ingestion
and establish precisely which movement counts are observed. The delivered
sample is midnight-heavy. Use already released DLR data for trajectory and
signal-clock checks. Keep the DLR 18:00–18:30 UTC holdout sealed. Use the
Monaco MoST network as a second, simulation-only test of transfer and
coordination after the same two-junction scenario is expressible in both
models.

- [Jinju receipt, observed fields and replay boundary](../../data/20261117_jinju/README.md)
- [CityArtery scene and clock requirements](../../data/20261117_cityartery/README.md)
- [MoST scenario and version notes](https://github.com/lcodeca/MoSTScenario)

Before treating a Jinju corridor as phase-resolved field input, verify the
approach/camera index, lane and controller movement crosswalk, valid study
window, phase-state timestamps (including transitions), and measurement
position. If counts are departures, measure or bound the inflow separately.
Do not estimate a peak/off-peak curve from the current released CSV.

## Decision rule

Let the feasible plan catalogue constrain protected movements, minimum
green and crossing time, transition and clearance, cycle and offset. Count
vehicles in finite storage and track time alignment and free-flow travel
separately. For each fixed arrival world, enumerate all small-catalogue
candidate plans using the same demand and service mechanisms. Define the
regret of plan a in world w as cost(a,w) minus the best feasible cost in
that world. At decision time restrict worlds to the set consistent with
information available by then. Choose the plan with the smallest worst
regret in that set. Also report the minimum worst absolute cost, total
delay, residual queues, lost green and pedestrian worst wait. A stricter
pedestrian/queue constraint can alter the feasible set itself.

Use an identical feasibility set when comparing information sources. A
monotone reduction in worst regret under nested observations on the same
enumerated worlds follows from being able to ignore extra information.
Its numerical size is only a property of the modeled support; held-out
days and independent sensor errors are needed to estimate realized value.
One cannot use a realized within-window platoon as a prospective covariate.

See [the source-to-test rationale](LITERATURE_TO_TESTS.md) for the
measurements and comparators behind this design.

## Outcomes and next questions

- [D51 boundary sweep](late-arrival/grid.json): 42/252 strict reversals
  when adding modeled amber service, all at arrival ticks 9–14. No changes
  in the 120 second-window contexts.
- [24-world offset comparison](offset-information/grid.json): pooled and
  counts-only worst regrets are 900 and 765 vehicle-seconds. Adding storage
  gives 704, with observed onset as an abstract feature giving 498. The
  demand-count policy's total cost exceeds the fixed policy's total cost
  across these worlds; measure both.
- [Jinju count-compatible witness](../../data/20261117_jinju/count_compatible.json):
  opposite plan rankings occur for each of three synthetic clock alignments
  given the same observed counts interpreted as two hypothetical arrivals.

Test whether an upstream green with low discharge coincides with a full
downstream link, compared with low discharge after sparse inflow. Add
start-up headway, physically usable pocket and link storage, turn shares
and lane asymmetry, vehicle length mix, phase timestamp error, detector
coverage and queue censoring separately. Then test whether information about
downstream storage reduces held-out regret beyond pocket observation and
counts alone. Treat the explanation as disproved if the supposed blocked
opportunity occurs while there is enough downstream space for the next
vehicle and lane movement. A second comparison with point queues and SUMO
needs the same lanes, demand, phase calendars and downstream restrictions.
SUMO supplies vehicle dynamics; the small model supplies exact enumeration,
a competing witness and auditable limits of the decision information.
