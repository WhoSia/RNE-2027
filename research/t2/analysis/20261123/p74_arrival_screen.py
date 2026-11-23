"""Compare T2 signal choices on matched arrival clocks and downstream capacities."""
import json
from dataclasses import replace
from itertools import product
from pathlib import Path
from statistics import mean
from p69_fixed_budget import build_config, p31, run, schedule, score, tape_hash

archive = json.loads(Path(__file__).with_name("P73_RESULT.json").read_text())
cells = []
for share, clock, capacity in product((.25, .5, .75), p31.FAMILIES, (2, 4)):
    rows = []
    for ref in archive[str(share)]["rows"]:
        cfg = replace(build_config(ref["seed"], 900, share, 7, capacity, .5),
                      downstream_offset_s=15)
        tape = p31.clock(cfg.base, clock)
        cp = run(cfg, tape, checkpoint_at=84)
        costs = [score(run(cfg, tape, resume_from=cp, phase_overrides=schedule(d)), 60)
                 for d in (6, 10)]
        delta = costs[1] - costs[0]
        if clock == "platoon4" and capacity == 4:
            assert (delta, tape_hash(tape)) == (ref["delta"], ref["tape"])
        rows.append(dict(seed=ref["seed"], tape=tape_hash(tape), delta=delta))
    cells.append(dict(share=share, clock=clock, capacity=capacity, rows=rows,
                      better=sum(r["delta"] < 0 for r in rows), mean_delta=mean(r["delta"] for r in rows)))
print(json.dumps(cells, indent=2))
