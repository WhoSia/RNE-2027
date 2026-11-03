# T2 v5.7 — Spatiotemporal junction occupancy

Study date: 20261103. Synthetic microscopic corridor only, no visualization deliverables.

Run in this folder:
```bash
python -m unittest test_v56 test_v57 -q
python audit_historical_v57.py
python experiment_v57.py
```
Older exact baseline is `network_v56.py`; the corrected engine is `network_v57.py`. New `temporal_conflicts.py` is an independent half-open interval auditor and admission predicate. Setting `occupancy_s=0` restores old simulation metrics exactly (tested); durations 2s,5s are sensitivity knobs only. 

Experiment output: 216 runs with 12 exploration and disjoint 12 holdout seeds for each of 3 demand cohorts ×3 occupancy durations. Repeated historical audit: 72 v5.6 traces ×2 assumed durations=144 audits. Source archive includes CSV and JSON. See separate EXHIBITION_20261103.md and PAPER_20261103.md.