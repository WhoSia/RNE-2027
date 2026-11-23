"""Compare fixed-horizon policy costs with costs after the original cohort clears."""
from collections import Counter
from dataclasses import replace
import json
from pathlib import Path

from p75_trace_pairs import build_config, p31, run, schedule, score, tape_hash
from p79_policy_rank import winner


def experiment():
    archive = json.loads(Path(__file__).with_name("P76_RESULT.json").read_text())
    transitions = Counter()
    changes = []
    for cell in archive:
        for row in cell["rows"]:
            cfg = replace(build_config(row["seed"], 900, cell["share"], 7, 4, .5),
                          downstream_offset_s=15)
            tape = p31.clock(cfg.base, cell["clock"])
            assert tape_hash(tape) == row["tape"]
            deltas = []
            for extra in (0, 1200):
                extended = replace(cfg, base=replace(cfg.base, duration_s=cfg.base.duration_s + extra))
                cp = run(extended, tape, checkpoint_at=84)
                arms = [run(extended, tape, resume_from=cp, phase_overrides=schedule(d))
                        for d in (6, 10)]
                assert all(r["generated"] == len(tape) for r in arms)
                if extra:
                    assert all(r["remaining"] == 0 for r in arms)
                deltas.append(score(arms[1], 60) - score(arms[0], 60))
            original, cleared = deltas
            assert original == row["delta_capacity_4"]
            transition = winner(original) + "->" + winner(cleared)
            transitions[transition] += 1
            if winner(original) != winner(cleared):
                changes.append(dict(seed=row["seed"], share=cell["share"], clock=cell["clock"],
                                    original=original, cleared=cleared))
    return dict(transitions=transitions, changed_cases=changes)


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2))
