# P40–P51 evidence and decisions

| Cycle | Verified local outcome | Adoption decision |
| --- | --- | --- |
| P40 | Aligned scheduled demand, nominal receiver length and the observed downstream discharge calendar. Point-estimate signs agree 1/4; upstream approach geometry still differs. | Keep the paired receiver contract. Do not transfer policy rankings. |
| P41 | 0/119 equal-cost pairs changed overall censored P95, peak upstream backlog or uncrossed count. 31/119 changed individual crossing history. | Lower priority of more whole-cohort metrics; measure individual effects. |
| P42 | Pocket length 10/30/95 m and receiver exit headway 1/2/3 s. No setting matched more than 1/4 SUMO signs. | Reject pocket-length tuning as a sufficient explanation. |
| P43–P44 | Across 12 default-clock cells, 7 had robust lagging, 1 robust leading and 4 unresolved signs after crossing-time bounds. In the 20 m closed case, .25 and .5 s bounds span zero; the 1 s lead advantage survives. | Apply timing bounds before interpreting rank and refine the integration step. |
| P45 | At .125 s, 10 m closed is robustly leading, 20 m closed remains unresolved. | Reject convergence of the policy sign over tested resolutions. |
| P46 | At fixed 1 s driver action interval, 3/16 contrasts fail collision screening, 12 robustly favor lagging and 1 favors leading. SUMO switches to ballistic integration when required by the action interval, so this does not isolate driver reaction alone. | Exclude failed pairs and vary amber as a targeted diagnostic. |
| P47 | Individual changes in 31/119 tied worlds exceed 10 s in the beneficial direction for at least one vehicle; 4/119 contain harm over 10 s. 6/119 contain both positive and negative changes. No opposite-signed net movement totals. | Retain individual benefit/harm; separate this from movement-level redistribution. |
| P48 | All 3 selected collision pairs run without reported collisions after restoring upstream amber. All 3 robustly favor leading in these retests. | Test the intervention across all receiver conditions before generalizing. |

P44 bounds the difference for a fixed run. Each observed crossing is in the interval between the last upstream and first downstream sample; non-crossings retain the horizon penalty. Integration-step changes can also change the simulated trajectory itself. Neither the collision screen nor the crossing bounds establish real traffic safety.

## Updated priorities

Weights carried forward from P38: relevance .35, discrimination .30, readiness .20, feasibility .15. These are project judgments, separate from measured rates.

| Candidate | Relevance | Discrimination | Readiness | Feasibility | Weighted |
| --- | ---: | ---: | ---: | ---: | ---: |
| Verify shared upstream movement and physical startup/discharge before advancing rank comparison | .98 | .95 | .82 | .75 | 0.905 |
| Independent upstream/downstream field annotation | .99 | .93 | .67 | .75 | 0.872 |
| Per-vehicle harms and benefits on new held-out tapes | .91 | .83 | .85 | .85 | 0.865 |
| Pocket-full versus inaccessible | .94 | .92 | .70 | .80 | 0.865 |
| Movement-specific observations and guarded policy re-test | .96 | .90 | .62 | .75 | 0.843 |
| Repeat whole-cohort P95 and peak backlog on the same ties | .70 | .35 | .95 | .95 | 0.683 |

Overall comparison reproducibility .90 given deterministic replay; construct fidelity .60 given shared downstream calendar and unmatched upstream geometry; external validity .40 given synthetic engines and no independent field labels. Physical headway, amber and topology remain material factors. The immediate validation target is per-movement upstream insertion, stop-line crossing, downstream discharge, and queue evolution rather than an aggregate cost-only match.

## P49–P51 follow-through

P49: amber produced 16/16 valid comparisons across default and fixed driver clocks. Robust leading occurred in 6/8 with the default clock and 4/8 with the fixed clock. Both clocks favored lagging in both samples for the 20 m open receiver. The 20 m closed case changed sign with the clock under amber. P48 collision recovery therefore does not imply a general leading-phase advantage.

P50/P51: movement cost components reproduce each aggregate. The 10 m closed red-clearance case favors leading for left turns in both engines (SUMO −33.125, T2 −417) while the through contrast has opposite signs (SUMO −11.125, T2 +330). For the 20 m open case the through contrast is +117.625 versus −242. Next, the first priority is to match upstream movement paths and measure insertion debt, first stopline crossing and downstream release on the same arms. Movement-level diagnosis is now executable, but treatment equivalence is still open.
