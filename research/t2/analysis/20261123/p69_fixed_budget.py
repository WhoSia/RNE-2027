"""Paired green reallocation with clearance and finite receiver disruption."""
import json
from dataclasses import replace
from itertools import product
from pathlib import Path
from p39_policy_holdout import build_config, p31, run, score, tape_hash


def schedule(left):
    end = 87 + left
    return ((84,87,"-"), (87,end,"L"), (end,end+3,"-"), (end+3,114,"S"), (114,120,"-"))


def experiment():
    rows = []
    refs = json.loads(Path(__file__).with_name("P66_RESULT.json").read_text())["rows"]
    for ref in refs:
        for pocket, offset, headway, blocked in product((7,28), (0,15), (2,4), (False,True)):
            cfg = replace(build_config(ref["seed"], ref["demand"], ref["turn"], pocket, 4, .5),
                          downstream_offset_s=offset, receiver_headway_s=headway,
                          receiver_closures=((92,108),) if blocked else ())
            tape = p31.clock(cfg.base, ref["family"])
            if tape_hash(tape) != ref["tape"]:
                raise ValueError("Arrival tape mismatch")
            cp = run(cfg, tape, checkpoint_at=84)
            arms = []
            for left in (6,10):
                result = run(cfg, tape, resume_from=cp, phase_overrides=schedule(left))
                arms.append(dict(cost=score(result,60), occupancy=score(result,0),
                                 left_out=result["network_out_L"], through_out=result["network_out_S"]))
            rows.append(dict(tape=ref["tape"], family=ref["family"], pocket=pocket, offset=offset,
                             headway=headway, blocked=blocked, arms=arms,
                             delta=arms[1]["cost"]-arms[0]["cost"]))
    return rows


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2))
