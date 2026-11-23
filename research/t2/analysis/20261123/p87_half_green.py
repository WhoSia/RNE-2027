"""Compare equal green fractions at two cycle lengths from a common signal onset."""
from collections import Counter
from dataclasses import replace
from itertools import product
import json
from unittest.mock import patch

from receiving_cells_v15 import ReceivingCells
from p85_signal_coordination import build_config, p31, phases, run, score


def measure(cfg, tape, checkpoint, period, start_green):
    def green(link, tick):
        assert tick >= 84 and not link.config.closure_windows
        return ((tick - 84) % period < period // 2) == start_green

    with patch.object(ReceivingCells, "green", green):
        result = run(cfg, tape, resume_from=checkpoint, phase_overrides=phases(6, "left_first"),
                     trace=True)
    assert result["remaining"] == 0 and result["generated"] == len(tape)
    frames = (f for f in result["frames"] if f["t"] >= 84)
    full_red = sum(len(f["receiver"]) == 4 and
                   (((f["t"] - 84) % period < period // 2) != start_green) for f in frames)
    return dict(cost=score(result, 0), denied=result["receiver_denied_seconds"], full_red=full_red)


def experiment():
    summary = {}
    rows = []
    for seed, share, clock in product(range(85001, 85017), (.25, .5, .75), p31.FAMILIES):
        cfg = build_config(seed, 900, share, 7, 4, .5)
        tape = p31.clock(cfg.base, clock)
        cfg = replace(cfg, base=replace(cfg.base, duration_s=1440), downstream_offset_s=0)
        checkpoint = run(cfg, tape, checkpoint_at=84, trace=True)
        for onset in ("green", "red"):
            short, long = (measure(cfg, tape, checkpoint, p, onset == "green") for p in (30, 60))
            delta = {k: short[k] - long[k] for k in short}
            totals = summary.setdefault(onset, Counter())
            for k, value in delta.items():
                totals[k + "_sum"] += value
                totals[k + ("_lower" if value < 0 else "_higher" if value > 0 else "_equal")] += 1
            rows.append(dict(seed=seed, share=share, clock=clock, onset=onset, delta=delta))
    return dict(summary=summary, rows=rows)


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2))
