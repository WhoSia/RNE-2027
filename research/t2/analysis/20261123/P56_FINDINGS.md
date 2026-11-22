# P56 — Common downstream calendar across engines

Use the same 24 arrivals, 10 m nominal receiver and 50 s startup closure. At six offsets, verify the actual SUMO downstream phase at each 0.125 s observation. T2 retains its dedicated through B lane and turn pocket; SUMO retains dedicated approach lanes. Both use the no-amber benchmark.

Total approach cost favors the same phase order in all five cases where the SUMO sampling bounds resolve the sign. Offset 30 is unresolved (−1.75 to +2.5 vehicle-seconds), giving 5/6 jointly resolved and agreeing. Through-only point signs agree in 4/6, with disagreements at 0 and 50 seconds. The conservative per-through bound is ±2 vehicle-seconds (16 scheduled vehicles × 0.125 s), and all six signs survive it. All comparisons share one arrival tape. This is a calendar sensitivity experiment, with no estimate of performance on new tapes.

Decision: prioritize matched trajectory and movement-level validation (.97 relevance, .96 discrimination, .88 readiness, .77 feasibility; weighted .919). Independent field annotation remains .872. Overall cost is useful as a first screen; require separate movement-level agreement before transferring conclusions.

Run: `PYTHONPATH=../..:../../efficiency_loop python p56_cross_engine_offsets.py`. The P40 baseline remained byte-identical after the calendar refactor.
