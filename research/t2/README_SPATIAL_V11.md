# T2 v1.0–v1.1 — Spatial left-turn pocket and two-through-lane model

This is the **science-fair engineering model**, not an attempt to claim
a fundamentally new traffic-flow theory. No real intersection calibration
has been performed; no automation, GitHub Actions or main merge required.

## Implemented layers
- `spatial_v10.py`: single full through lane, physical branchpoint and
  finite turn pocket. Deterministic cellular motion, phase and clearance.
  7m cells, one cell/second, no acceleration/heterogeneous vehicles.
- `dual_lane_v11.py`: two through lanes A/B, left pocket attached to A,
  route prepositioning, optional A→B moves only when adjacent and both
  front/rear cells are free within the configured change zone.
  **Not MOBIL**, **not Hidas gap acceptance**.
- `site_v11.py` and `fixtures/synthetic_dual_site_v11.json`:
  physical road, demand and signal inputs retain source/provenance.
  Source labels do not establish external validity.
- `run_site_v11.py`: same generated arrivals, four pocket interventions.
- `separation_court_v11.py`: conditional model theorem and 150 finite checks.
- `plot_dual_lane_v11.py`: reproducible figure from scenario summary.

## Regression and experiments
```bash
python -m unittest discover -s research/t2 -p "test_spatial_v10.py" -v
python -m unittest discover -s research/t2 -p "test_dual_lane_v11.py" -v
python -m unittest discover -s research/t2 -p "test_site_v11.py" -v
python -m unittest discover -s research/t2 -p "test_run_site_v11.py" -v
python -m unittest discover -s research/t2 -p "test_separation_court_v11.py" -v
python research/t2/factorial_v10.py
python research/t2/update_sensitivity_v10.py
python research/t2/demand_sweep_v10.py
python research/t2/dual_lane_factorial_v11.py
python research/t2/separation_court_v11.py
python research/t2/run_site_v11.py research/t2/fixtures/synthetic_dual_site_v11.json research/t2/results/example_v11.json
```

Local reconstructed prototype: **26 tests passed**; 384 spatial factorial,
768 update-rule, 384 demand screen, 384 two-lane factorial; 150 conditional
independent-lane demonstrations. Figures and animation included in separate
local reproducibility bundle. IMPORTANT: the GitHub connector-authored file
versions are not proven byte-identical to the locally executed sources.
Run the exact checked-out branch tests before release certification.

## Engineering interpretation
The result is a *conditional surface*, not a single optimal pocket length.
At 30% turning demand, 1800-second synthetic output increases much more
with added pocket length when through cars use only the pocket-adjacent
shared lane than when they have an independent lane. An all-through-B
scenario is exactly noninterfering by construction, but actual roads can
share downstream storage and support nontrivial merging.

Next steps: ground an actual site with a dimensioned lane diagram, signal
phase table and anonymous safe aggregate per-cycle flows; split calibration
and independent validation periods; examine model discrepancy. Do not
physically manipulate active traffic signals.
