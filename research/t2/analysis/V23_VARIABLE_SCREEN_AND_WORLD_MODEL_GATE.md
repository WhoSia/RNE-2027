# T2 v2.3 Variable Screen and World-Model Gate — 2026-11-01

Source: archived executed FIXED v2.2 engine, NOT verified GitHub remote parity. All data SYNTHETIC.

Design: seeds 0/1/2; pocket 14/70 m; demand 1200/2400 veh/h; left share .25/.65; arrivals uniform/platoon; downstream offset 0/30s. 96 runs and 48 paired comparisons, 720 seconds per run. Lane changes on, through B share 0, four-cell downstream receiving link.

Network exits (70m minus 14m): positive 30 pairs; zero 18; negative 0; mean +3.35417 vehicles/720s; range 0..11. Uniform mean +2.875; platoon mean +3.83333; demand 1200 mean +3.20833 and 2400 mean +3.5.

Caution: These results do not prove monotonicity, physical validity, or external predictive power. Network exits are not the same as stopline crossings; finite horizon effects and arrival timing can bias comparisons. 7m cells and one-second movements are uncalibrated conventions. Through B share zero is a special-case mechanism test. Actual queue length, gap acceptance, lane change behavior and saturation headways are unobserved. Source parity with GitHub is STILL FAILED; never imply these are tests of remote HEAD.

Next: source-level reconciliation, independent transition-level event oracle, causes of zero-effect pairs, factorial interactions with realistic through-lane split and time-varying demand, robust holdout, independent SUMO comparator, legal de-identified Korean intersection observations.

Drive: T2_v23_variable_screen_96_runs.csv and T2_v23_paired_effects_48_pairs.csv in shared-drive 02_REPRO_ARTIFACTS. GitHub Actions prohibited; no bot-authored commits.
