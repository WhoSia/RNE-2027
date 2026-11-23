"""Cross downstream offset, upstream phase order and green split on matched demand."""
from collections import Counter, defaultdict
from dataclasses import replace
from itertools import product
import json

from p69_fixed_budget import build_config, p31, run, schedule, score


def phases(left, order):
    if order == "left_first":
        return schedule(left)
    switch = 87 + 24 - left
    return ((84, 87, "-"), (87, switch, "S"), (switch, switch+3, "-"),
            (switch+3, 114, "L"), (114, 120, "-"))


def experiment():
    summary = defaultdict(Counter)
    pairs = defaultdict(Counter)
    offsets = (0, 15, 30, 45)
    for seed, share, clock in product(range(85001, 85017), (.25, .5, .75), p31.FAMILIES):
        cfg = build_config(seed, 900, share, 7, 4, .5)
        tape = p31.clock(cfg.base, clock)
        ranks = {}
        for offset in offsets:
            extended = replace(cfg, base=replace(cfg.base, duration_s=1440),
                               downstream_offset_s=offset)
            cp = run(extended, tape, checkpoint_at=84)
            costs = {}
            for order, left in product(("left_first", "through_first"), (6, 10)):
                arm = run(extended, tape, resume_from=cp, phase_overrides=phases(left, order))
                assert arm["remaining"] == 0 and arm["generated"] == len(tape)
                costs[order, left] = score(arm, 0)
            for order in ("left_first", "through_first"):
                delta = costs[order, 10] - costs[order, 6]
                ranks[offset, order] = (delta > 0) - (delta < 0)
                summary[f"{offset}/{order}"][str(ranks[offset, order])] += 1
            for left in (6, 10):
                delta = costs["through_first", left] - costs["left_first", left]
                pairs[f"order_effect/{left}"][str((delta > 0) - (delta < 0))] += 1
        for order in ("left_first", "through_first"):
            signs = {ranks[o, order] for o in offsets}
            pairs[f"offset_strict_reversal/{order}"][str({-1, 1} <= signs)] += 1
    return dict(split_ranks_by_offset_order=summary, paired=pairs)


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2))
