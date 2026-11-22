# P39 evidence and priority decisions

SUMO 1.28.0, 8 runs. Lead-minus-lag approach vehicle-seconds for tau 1.0 and 1.5 were +7.75 and +52.00 with no amber service and −99.25 and −57.25 with the amber program. Reversal rate: 2/2 within this benchmark. T2 shares 24 scheduled arrivals, 100 m nominal approach and green starts, but topology, motion and amber semantics differ. All six FIFO contrasts were −137; receiver denials were zero. Smaller pocket activated access denials but did not change the cost contrast. An exploratory warning: FIFO ignores closures, so compare open versus closed within the cellular receiver. At capacities 2/4, the 0–50 s closure changed contrasts from −285 to −87 and −42 to +61. Both arms activate receiver denial. SUMO still needs an equivalent finite link, pocket and downstream boundary.

Policy: 128 worlds on 8 unseen tapes. Both proposed rules ran fixed 6 s in all worlds. Pocket occupancy was positive 128/128, two receiver spaces were available 27/128, and hindsight preferred extension in 8/128, fixed in 1/128. The pressure condition blocked all activation; no candidate clears the advancement rule. All achieved identical cost and worst regret 189. The observed pocket count and non-pocket count are proxies with different aggregation scopes; the ratio is not calibrated pressure. Keep fixed as the reference, build a movement-separated queue/receiver observation, and establish its activation coverage on development tapes before a fresh holdout.

## Local adoption review

Scores are priorities using the P38 weights (.35 relevance, .30 discrimination, .20 readiness, .15 feasibility). Pass criteria concern the local claim only. Evidence confidence is a rubric rating, not a probability.

| Candidate | Relevance | Discrimination | Ready | Feasible | Score | Previous | Local decision |
|---|---:|---:|---:|---:|---:|---:|---|
| Match T2/SUMO finite link and closure, then test amber | .99 | .97 | .84 | .72 | .913 | .896 | Continue. Both engines now runnable and T2 stress has a discriminating contrast. Require shared geometry and activated receiving denial before interpreting parity. |
| P95 delay and maximum queue on observed cost ties | .92 | .85 | .90 | .90 | .892 | .874 | Raise. Aggregate policy cost cannot distinguish inactive decisions and tails. |
| Independent upstream/downstream observation | .99 | .93 | .67 | .75 | .872 | .872 | Retain. No additional field labels in P39. |
| Pocket-full versus inaccessible | .94 | .92 | .70 | .80 | .865 | .865 | Retain. Access denials occurred but the bridge has no independent cause labels. |
| Fix movement-specific policy features, activation test and new holdout | .96 | .90 | .62 | .75 | .843 | .881 | Narrow. Reject current rule, keep the question. |

Bridge reproducibility .85, construct fidelity .55 and field external validity .40. Policy holdout execution .85, genuine action coverage 0/128 and external benefit evidence .00. These claims are separate. Priority order between .892 and .872 is sensitive to modest readiness changes. The first priority stays ahead under a shift of .05 weight from relevance to feasibility (.900 vs .891 for the P95 candidate).

Run in this directory:

```sh
PYTHONPATH=../..:../../efficiency_loop python p39_engine_bridge.py
PYTHONPATH=../..:../20261122 python p39_policy_holdout.py
```
