# v6.6 — Multi-factor synthetic study
384 original-mode executions = 2 demand rates × 2 side-turn proportions × 2 temporal shapes × 2 green splits × 2 lateral acceleration limits × 12 seeds. There are 192 matched main-versus-side green comparisons.
At the fixed 800s horizon, mean [side-biased minus main-biased] cumulative exposure (veh·s):
turn share 25%, diffuse +4166.91; 25%, pulse +3652.15;
turn share 60%, diffuse −3330.47; 60%, pulse −3873.28.
Thus a policy ranking reversal occurs in this *synthetic engine* when modeled turn share changes. Strong confounding caveat: only 177/384 original runs completed all vehicles by 800s. This is a **censored exposure** outcome and does not establish all-complete trip-time policy optimality. The side movement is modeled as one turning stream, no pedestrians or physical receiving supply.
Demand pulses compress each 20s interval's same vehicle arrivals into its first 5s while preserving exact vehicle IDs/origins/count. This is a designed synthetic intervention, not observed platoon data.
Experimental cells sharing seeds are correlated; no 384-independent-observation inference.
