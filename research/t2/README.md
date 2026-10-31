# T2 — Figure 7(c) spatial prototype (v0.2)

## Status: UNVALIDATED / NOT A REPRODUCTION

This prototype assigns moving positions **x_i(t)** in 25-ft cells to vehicles on:
1. inner shared left/through lane;
2. independent outer through lane;
3. finite left-turn bay connected at a divergence.

Runs 1-second updates with 2-cell/s maximum movement, a mandatory cell gap, 2s stopline discharge, and separate protected turn/through green times. Inputs follow part of Emtenan & Day (2021), Figure 2: 3000 vehicles/h, 40% left turns, 150s cycle, 60s straight green, 54s left green, 100ft vs 500ft bays, 4200s horizon.

### Verified deterministic outputs (seed 42)

| Bay | Arrivals | Inner S exits | Outer S exits | Left exits | Total exits | Remaining |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 100 ft | 3500 | 371 | 815 | 514 | 1700 | 1800 |
| 500 ft | 3500 | 204 | 815 | 269 | 1288 | 2212 |

The **longer bay paradoxically reduces discharge** in this prototype. This disagrees with the source paper's Figure 2 qualitative mechanism and is a **calibration / lane-transfer model failure**, not a discovery about real traffic. The model's bay entry rule, shared-lane movement, car-following, and injection queue require further independent review.

### Reproduce

```bash
python research/t2/spatial_model.py
python -m unittest discover -s research/t2/tests -v
```

Requirements: Python 3.10+ standard library only. Generated `outputs/` are ignored in Git; numeric summaries and tests are committed. Original paper PDFs remain in the controlled Research OS Google Drive library.

### Validation gates before an empirical claim

- Physical lane geometry and diverge/merge priority consistent with documented vehicle trajectories.
- Verify 100ft vs 500ft traffic mechanics with micro-level event audits, not throughput alone.
- Compare individual x(t), stopline headway, movement split, lost green, and vehicle conservation.
- Seed ensembles, discharge/arrival sensitivity, benchmark against SUMO or properly calibrated microscopic simulation.
- Cross-check against Emtenan & Day (2021) original Figures 2, 3 and 7.
- Never tune parameters to force agreement without held-out evidence.

### Collaboration

Changes should be developed on feature branches, reviewed by teammates in pull requests, and only merged to `main` when tests and the source-comparison gate pass.
