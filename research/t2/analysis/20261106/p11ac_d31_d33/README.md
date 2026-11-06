# T2 P11-AC — D31/D32/D33, 2026-11-06

Research unit 31: historical original P10 replay and event-schema bridge.
Research unit 32: SUMO independent run gate; no binary available, therefore NOT_EXECUTED.
Research unit 33: synthetic two-approach fixed vs actuated policy court with censored-outcome handling and exploratory demand stress.

Run from a clean extracted ZIP with Python >= 3.10:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python run_study.py
python stress_study.py
python visualize.py
```

Unmodified archived P10 replay receipt is under `references/p10_replay.json`. The source original P10/P9/P2 ZIPs and their prior SHA receipts are retained separately in the 20261106 D26 Drive folder. External SUMO is NOT installed; prepare reproducible scenario under results/sumo_scenario and never claim simulation unless `independent_sumo_run` is EXECUTED. All results are explicitly SYNTHETIC except original P10 replay.

No live signal actuation or infrastructure connectivity. For full report see docs/.
