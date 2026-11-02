# T2 v5.0.1 local integration-window precondition (2026-11-02)

After v5.0 experiment completed, an additional edge-case audit found that the corrected exposure identity assumes `horizon/dt` is an integer. The original engine loop truncates `int(horizon/dt)`, so a nonintegral horizon makes the independent censoring sum disagree with the integration loop. The local release includes a guard:

```python
if not math.isclose(horizon/dt, round(horizon/dt), rel_tol=0., abs_tol=1e-9):
    raise ValueError('horizon must be an integer multiple of dt')
```

The local release test suite now passes **26/26** tests. The previously committed `network_v50.py` and `test_v50.py` on the research branch remain at the earlier 25-test version because a sequential GitHub content-update attempt was rejected. Until GitHub is synchronized, the corrected **ZIP source is the exact v5.0.1 canonical implementation**; the GitHub v5.0 source should only be executed at integral multiples of its specified timestep (the executed study does so: horizon 580s, dt 0.5s). This post-experiment input guard does not change any of the 216 completed results.

[Google Docs research ledger](https://docs.google.com/document/d/1zaUc5dScw47gwm49UjxGF94dbtxWFa9h7igd6fvlzXU/edit)
