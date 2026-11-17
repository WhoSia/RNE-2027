# Phase-order reversal follow-up

The prior 24-vehicle pair used one inflow, one dedicated-lane geometry and equal green budgets. The reported response was capped crossing time minus scheduled departure, summed over all vehicles. The reference leading-minus-lagging contrast was +110 vehicle-seconds in the point model and −99.25 vehicle-seconds in SUMO.

For the follow-up, retain the phase start times and 60 s cycle. Vary point-model permitted service through the nominal amber interval and headway independently. In SUMO, replace yellow by red in the same slots as a synthetic comparison and vary Krauss tau separately. Tau is a desired minimum time headway, not an observed discharge headway. The red substitution changes the displayed signal drivers respond to and is a simulator control, never a proposal for physical signal timing.

Attribute the paired cost by movement and by vehicle. Accept a crossing only with adjacent upstream and downstream observations. Classify a bracket spanning a signal transition explicitly. Retain scheduled counts, departures, uncrossed counts and the paired input check in all conditions.

Use a separate D51 comparison to vary finite pocket storage and service windows. Preserve pre-tick occupancy and all legacy D51 defaults. Compare the same forecast envelope and synthetic context across calendars. The SUMO network has dedicated approach lanes. It does not implement that finite-pocket geometry.

No DLR holdout, reviewer classifications or observed sensor error rates enter these experiments.
