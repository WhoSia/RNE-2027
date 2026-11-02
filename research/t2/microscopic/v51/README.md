# T2 v5.1 — Microscopic connection service, safety audit and holdout

Run from this folder with Python 3.10+ (standard library only):

```bash
python -m unittest discover -s . -p 'test*.py' -v
python experiment_v51.py
python replicate_v51.py
```

Main scripts: `network_v51.py` (3 active signals, finite link queues, IDM, legal OD paths, movement-level service headways), `test_v49_reference.py`, `test_v50_regression.py`, `test_v51.py`, `experiment_v51.py` (216 paired synthetic runs), `replicate_v51.py` (192 independent-seed synthetic runs). Baseline `experiment_v50.py` is vendored for immutable signal policy definitions; it is not a second experiment in this package.

Output: `runs.csv`, `means.csv`, `paired_model_effect.csv`, `robust.csv`, `summary.json`, `heldout_paired_offsets.csv`, `heldout_summary.json`.

**Not field-calibrated; no proof of collision-free numerical dynamics.** The code asserts finite-link vehicle conservation and discrete within-link spacing but does not model geometric intersections, pedestrians, road regulations or emergency responses. See RESEARCH_AUDIT.md for historical failure and separate-seed evidence.
