# P11-W / D21 — Local, scoped research witness

From directory containing `src`, `tests`:

```bash
python -m unittest discover -s tests -v
python run_case.py
python render.py
```

Python 3.10+, matplotlib for PNG only. `spatial_conflict_witness.html` can be viewed offline without dependencies. `results/*.csv` and JSON contain **synthetic** results.

The original V-stage implementation was read from GitHub, branch `research/t2-spatial-fig2-v02`, blob `c9c6c56a36097cbf7d48c996eee545d1e495f599`. This package is a minimal scoped extension; the historical default `global` is preserved. To model multi-intersection network demand, **set `Demand.conflict_zone` explicitly**.

Research only. No signal phase optimization, no traffic control, no safety decision. P12 frozen.
