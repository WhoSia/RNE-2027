"""Replay each P76 four-slot comparison and vary only the terminal cost."""
import json
from collections import Counter
from dataclasses import replace
from pathlib import Path
from p75_trace_pairs import build_config, p31, run, schedule, score, tape_hash
from p79_policy_rank import winner


def experiment():
    cells = json.loads(Path(__file__).with_name("P76_RESULT.json").read_text())
    penalties = (0, 15, 30, 60, 120)
    transitions = {p: Counter() for p in penalties}
    slopes = Counter()
    for cell in cells:
        for row in cell["rows"]:
            cfg = replace(build_config(row["seed"], 900, cell["share"], 7, 4, .5),
                          downstream_offset_s=15)
            tape = p31.clock(cfg.base, cell["clock"])
            assert tape_hash(tape) == row["tape"]
            cp = run(cfg, tape, checkpoint_at=84)
            short, long = (run(cfg, tape, resume_from=cp, phase_overrides=schedule(d))
                           for d in (6, 10))
            intercept = score(long, 0) - score(short, 0)
            slope = long["remaining"] - short["remaining"]
            slopes[slope] += 1
            reference = row["delta_capacity_4"]
            assert intercept + 60 * slope == reference
            for p in penalties:
                delta = intercept + p * slope
                assert delta == score(long, p) - score(short, p)
                transitions[p][winner(reference) + "->" + winner(delta)] += 1
    return dict(transitions=transitions, remaining_difference=slopes)


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2))
