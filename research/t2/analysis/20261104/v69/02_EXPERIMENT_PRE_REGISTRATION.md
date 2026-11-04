# v6.9-P0 — Controlled local versus joint policy protocol
Four demand classes: balanced, upstream_peak, downstream_side_peak, platooned; two receiving-link storage capacities 18m and 60m; common external arrival lists include vehicle ID, arrival second, entry direction, vehicle class. Training RNG seeds 101,103,107; holdout seeds 211,223,227,229. The four holdout seed identities repeat across the 8 scenario cells: use seed-cluster uncertainty, not n=32 independence.
Policy families:
(1) local-independent: tune each of the two main-green splits via independent 1-junction runs, with J1's main arrivals approximated by upstream arrivals +15s free flow, ignoring spillback, and fixed downstream offset 0;
(2) offset-only: locally selected green splits unchanged, tune offset on coupled training network;
(3) splits-only: tune two green splits on coupled training network but offset 0;
(4) full-joint: exhaustive 27-plan coupled training search.
This design deliberately changes both model information and policy class between (1) and (4); it does not isolate pure value of cooperation. No test seed is used for policy selection. Prefer full-cohort completion when interpreting total travel time.
Test commands: python -m unittest -q test_corridor.py test_optimizer.py; python experiment.py; python ablation.py; python holdout_oracle.py; python summary_analysis.py.
Full source and CSV preserved in dated shared Drive ZIP; GitHub audit notes are not a substitute for executable source sync.