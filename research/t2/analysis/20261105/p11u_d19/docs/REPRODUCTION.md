# Reproduction guide — D19

Runtime: Python 3.13+ preferred, no services or credentials. `matplotlib` is needed for `run_audit.py` and the cleaned legacy runner; model code and tests need only the standard library.

```bash
cd T2_P11U_D19
python -m unittest discover -s tests -v
python run_experiments.py
python run_audit.py
```

The model CTM is copied unchanged from the D18 sealed package. The experiment-runner refactor removes unreachable code and normalizes `Infinity` to JSON `null` for unbounded counterfactual capacities. `results/case_results.json` is identical in content to D18's. The new paired metric uses the same Config except for `downstream_closed_until_s=0` and compares source queues at matching time indices.

**Do not interpret either model as real traffic or certified signal optimization.**
