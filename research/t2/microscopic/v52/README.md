# T2 v5.2 — finite branching-pocket micro-network

**Status:** Executable research prototype; 46 tests pass; 288 exploratory + 144 independent-seed simulations. NOT field-calibrated.

Run (from this directory, all reference source dependencies included in this package):

```
PYTHONPATH=. python -m unittest discover -p 'test_*.py'
PYTHONPATH=. python experiment_v52.py
PYTHONPATH=. python heldout_v52.py
```

Files: `network_v52.py` reference physics; `test_pockets.py` nine pocket-specific tests; 37 ported legacy regression tests; `experiment_v52.py` and `heldout_v52.py`; respective CSV+JSON; `EXHIBITION_POSITION.md` and `PAPER_POSITION.md` kept separate; `RESEARCH_AUDIT.md` names failures and constraints. The `patch_v52.py` implementation transformation script is an audit helper, but because the terminal-outflow correction was made after the patch, `network_v52.py` is the authoritative source.

No illustration/poster was created in this cycle by request. Relevant literature has established bay spillback already: Yin et al. (2011) DOI 10.3141/2257-12; Yang et al. (2022) Physica A 599 127439; Qi et al. (2007) DOI 10.3141/2023-11; FHWA Traffic Signal Timing Manual ch6. 
