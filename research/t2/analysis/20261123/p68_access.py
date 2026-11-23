"""Factorial interventions on the 32 P66 tapes."""
import json
from dataclasses import replace
from itertools import product
from pathlib import Path

from p39_policy_holdout import action, build_config, p31, run, score, tape_hash


def experiment():
    archived = json.loads(Path(__file__).with_name("P66_RESULT.json").read_text())["rows"]
    rows = []
    for ref in archived:
        for pocket, share, changes, headway in product((7, 14, 28), (0, .5, 1), (False, True), (2, 4)):
            cfg = replace(build_config(ref["seed"], ref["demand"], ref["turn"], pocket, 4, share),
                          downstream_offset_s=15, allow_lane_changes=changes, receiver_headway_s=headway)
            tape = p31.clock(cfg.base, ref["family"])
            if tape_hash(tape) != ref["tape"]:
                raise ValueError("Demand changed during factorial comparison")
            state = run(cfg, tape, checkpoint_at=84)
            costs = [score(run(cfg, tape, resume_from=state, phase_overrides=action(d)), 60)
                     for d in (6, 10)]
            delta = costs[1] - costs[0]
            if (pocket, share, changes, headway) == (14, .5, True, 2) and delta != ref["delta60"]:
                raise ValueError("Archived contrast mismatch")
            rows.append(dict(tape=ref["tape"], pocket=pocket, share=share, changes=changes,
                             headway=headway, costs=costs, delta=delta))
    return rows


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2))
