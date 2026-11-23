"""Sweep the turn probability while holding seeds and signal offset fixed."""
from dataclasses import replace
import json
from pathlib import Path
from statistics import mean
from p69_fixed_budget import build_config, p31, run, schedule, score, tape_hash

reference = json.loads(Path(__file__).with_name("P71_RESULT.json").read_text())
output = {}
for share in (.25, .5, .75):
    rows = []
    for ref in reference:
        cfg = replace(build_config(ref["seed"], 900, share, 7, 4, .5), downstream_offset_s=15)
        tape = p31.clock(cfg.base, "platoon4")
        checkpoint = run(cfg, tape, checkpoint_at=84)
        costs = [score(run(cfg, tape, resume_from=checkpoint, phase_overrides=schedule(d)), 60)
                 for d in (6, 10)]
        delta = costs[1] - costs[0]
        if share == .5:
            assert tape_hash(tape) == ref["tape"] and delta == ref["t2"][1]
        rows.append(dict(seed=ref["seed"], tape=tape_hash(tape), delta=delta))
    output[share] = dict(ten_better=mean(r["delta"] < 0 for r in rows),
                         mean_delta=mean(r["delta"] for r in rows), rows=rows)
print(json.dumps(output, indent=2))
