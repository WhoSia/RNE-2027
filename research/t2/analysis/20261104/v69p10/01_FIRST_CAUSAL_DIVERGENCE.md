# P10 causal event witness
Case: original P2, upstream_peak, link storage 18m, seed 223, signal plan (24,24,24), horizon 1200s. Car footprint 6.5m: 2 cars fit, 3 cars do not. Side green until t=53s. Car clearance (18.85m+4.5m)/4mps=5.8375s. Last green admission is t=47.1625s.

At dt 0.05, vehicle 1 leaves upstream link at 47.05s and vehicle 8 enters connector 0 at 47.00s. At dt 0.25, vehicle 1 link receipt at 47.50s and vehicle 8 cannot enter until 87.25s. At dt 0.50, vehicle 8 enters at 47.0 even though vehicle 1 only frees storage at 47.50; this is retroactive capacity use caused by tick-end receive and tick-start entrance.

The first major per-vehicle event difference is the vehicle8 first connector admission, from 47.0 to 87.25, i.e. a phase-boundary discontinuity. Other vehicles propagate this consequence through queues. This is a mechanistic identification for one fixed test case, NOT proof of a universal sole cause.
