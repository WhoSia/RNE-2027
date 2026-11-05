# P11-U dependency contract

The D19 paired analysis imports `src.cell_link_model.Config` and `simulate` from D18 unchanged. The checked D18 blob was Git SHA-1 `1738f8a9a033302477c370903a913c76ddda7cf1`, verified against the source branch; the copied D19 `src/cell_link_model.py` must remain byte-identical.

`run_experiments_cleaned.py` in GitHub is a renamed copy of D18's experiment runner after *only* dead-code and unnecessary import cleanup; all resulting `case_results.json` entries match the original. The D19 full Drive ZIP uses `run_experiments.py` with the same cleaned content. `run_audit.py` adds synthetic paired metrics and plots.

Run from the research version directory:
```
python -m unittest discover -s tests -q
python run_audit.py
python run_experiments_cleaned.py # on GitHub layout only
```

No site-data calibration, SUMO, or original P10 engine regression was done during D19. P12 frozen.
