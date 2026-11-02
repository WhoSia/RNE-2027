# T2 v5.0 — Research-only reproducibility package

Includes `network_v50.py` (three-signal multi-OD microscopic corridor with corrected vehicle-time ledger and configurable IDM), `experiment_v50.py` (separable green/offset × microscopic sensitivity), `test_v49_reference.py`, `test_v50.py`, the full raw outputs and a reproducibility audit. No posters, figures or dashboard in this package.

## Reproduce with Python >=3.10

```sh
python -m unittest test_v49_reference test_v50 -v
python experiment_v50.py
```

All demands are SYNTHETIC. 216 runs; 25 unit tests pass. This archive does **not** imply calibration or SUMO agreement. `v49_exposure_correction.csv` corrects the historical v4.9 vehicle-second ledger without modifying its primary archive.
