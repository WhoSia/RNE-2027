# T2 P11-X / D22 reproducibility
Python >=3.10; stdlib model/tests; matplotlib for optional image only.

```sh
python -m unittest discover -s tests -v
python run_case.py
python visualize.py
```

- `src/lane_fifo.py`: new multi-zone reference.
- `baseline/lane_fifo_W_original.py`: unchanged W reference from pinned GitHub blob.
- `tests/`: unchanged 25 legacy tests + new 9 tests.
- `results/`: exact synthetic counterfactual JSON, offline standalone HTML, timeline PNG.
- Scope: synthetic audit only, not actual T2 engine integration, not a validated microscopic traffic model. P12 policy code frozen.
