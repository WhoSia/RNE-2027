"""Branch the four downstream clocks from one offset-zero state at tick 84."""
from collections import Counter
from dataclasses import replace
from itertools import product
import json
from pathlib import Path
from unittest.mock import patch

from receiving_cells_v15 import ReceivingCells
from p85_signal_coordination import build_config, p31, phases, run, score


def experiment():
    original_green = ReceivingCells.green
    results = []
    counts = {}
    orders = ("left_first", "through_first")
    offsets = (0, 15, 30, 45)
    for seed, share, clock in product(range(85001, 85017), (.25, .5, .75), p31.FAMILIES):
        cfg = build_config(seed, 900, share, 7, 4, .5)
        tape = p31.clock(cfg.base, clock)
        cfg = replace(cfg, base=replace(cfg.base, duration_s=1440), downstream_offset_s=0)
        assert not cfg.receiver_closures
        cp = run(cfg, tape, checkpoint_at=84)
        deltas = {order: [] for order in orders}
        for offset in offsets:
            def shifted_green(link, tick):
                assert tick >= 84
                return original_green(link, tick + offset)

            with patch.object(ReceivingCells, "green", shifted_green):
                for order in orders:
                    arms = [run(cfg, tape, resume_from=cp, phase_overrides=phases(left, order))
                            for left in (6, 10)]
                    assert all(r["remaining"] == 0 and r["generated"] == len(tape) for r in arms)
                    deltas[order].append(score(arms[1], 0) - score(arms[0], 0))
        results.append(dict(seed=seed, share=share, clock=clock, deltas=deltas))
    reference = json.loads(Path(__file__).with_name("P85_RESULT.json").read_text())
    for order in orders:
        zero = [r["deltas"][order][0] for r in results]
        assert Counter(str((d > 0) - (d < 0)) for d in zero) == reference[
            "split_ranks_by_offset_order"][f"0/{order}"]
        counts[order] = sum(min(r["deltas"][order]) < 0 < max(r["deltas"][order])
                            for r in results)
    return dict(offsets=offsets, reversals=counts, rows=results)


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2))
