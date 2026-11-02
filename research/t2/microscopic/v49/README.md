# T2 v4.9 — Exhibition-grade synthetic microscopic corridor

Three active signals and 6 incoming lanes: M0/M1/M2 lengths 160/180/180m; S0/S1/S2 are 85m each. All roads and OD demand are invented. Each vehicle has a route, IDM longitudinal speed/position updates, physical storage and receiving-supply constraints. Each time step checks conservation of generated = completed + internal + source-pending vehicles. Separate static main/side green stages and individual intersection offsets; 13 local tests PASS. No SUMO execution, field calibration, or collision-free safety proof.

Experiment 3 demand patterns × 4 candidate policies × 5 seeds = 60 matched runs, dt=0.5s, arrivals to 320s, observation to 580s. Primary metric is total vehicle-seconds including unfinished trips, not only mean duration of completed trips.

Mean system vehicle-hours (fixed / coordinated / main-priority / side-priority):
- Balanced: 3.065 / 2.970 / 2.486 / 4.138
- Main peak: 7.848 / 7.740 / 6.658 / 9.215
- Side peak: 6.949 / 7.046 / 7.242 / 7.589

Relative difference (main-priority vs fixed): -18.9%, -15.2%, +4.2%. This is an IN-MODEL sensitivity, not real Korean signal performance. Green split and offsets are both changed between those policies; causal attribution to green split alone is invalid.

Reproduce with commands: python -m unittest discover -v ; python run_experiment.py ; python make_dashboard.py ; python make_poster.py . Plot/PDF creation additionally requires matplotlib, reportlab and Nanum Korean font.

Full raw data/source/figures ZIP: https://drive.google.com/file/d/1M80THBvfxpUovwGA_o7V6ZYPsdGFiFsT/view
A3 exhibition board (visually inspected): https://drive.google.com/file/d/13YG5cnta0S99T32I1isD-QyGnY9Xacij/view
Offline animated HTML: https://drive.google.com/file/d/19sKz0SQKZ7G6-8oXCFUFqEvEx0eAQbD0/view
SHA256 of ZIP: 30246a78eeff28e273d1254fbbfdf26b2900f02db05354d16a55ded111ecc96f.

**Not implemented or verified:** full left/right-turn lane conflicts, realistic signal safety plan, MOBIL lane-changing, pedestrian phases, buses, grade, heterogeneous vehicle classes, SUMO parity, independent Gyeongnam observed data. This is the first linked microscopic-network prototype, not an accomplished traffic-field model. Details in the ZIP and T2 20261102 Google Docs.